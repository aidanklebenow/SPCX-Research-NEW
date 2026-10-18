"""Accounting refusal and economic-direction checks for the Visa teaching model."""
import subprocess
import sys
import unittest
from pathlib import Path

import Lab10_visa_proforma as model


class ModelChecks(unittest.TestCase):
    def setUp(self):
        self.data = model.load_inputs()

    def test_base_and_source_opening_balance(self):
        self.assertEqual(sum(self.data['opening'][k] for k in model.ASSETS), 99627)
        self.assertEqual(sum(self.data['opening'][k] for k in model.LIABILITIES), 61718)
        rows = model.project(self.data)
        model.check(rows, self.data)
        self.assertTrue(all(r['fcfe'] > 0 and r['revolver'] == 0 for r in rows))
        self.assertGreater(model.value(rows, self.data)['per_share'], 0)

    def test_cli_refusal_prints_no_value_and_changes_no_inputs(self):
        before = model.DATA_PATH.read_bytes()
        result = subprocess.run([sys.executable, str(Path(model.__file__)), '--break-2026-cash'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('VALUATION REFUSED: FY2026E: balance-sheet gap', result.stderr)
        self.assertNotIn('Value per share:', result.stdout)
        self.assertEqual(before, model.DATA_PATH.read_bytes())

    def test_balancing_two_accounts_cannot_hide_broken_cash_bridge(self):
        rows = model.project(self.data)
        rows[0]['cash'] += 100
        rows[0]['equity'] += 100
        with self.assertRaisesRegex(ValueError, 'cash-flow bridge'):
            model.value(rows, self.data)

    def test_incentive_pressure_reduces_value(self):
        base = model.value(model.project(self.data), self.data)['per_share']
        self.data['assumptions']['incentive_ratio'] = [x + .01 for x in self.data['assumptions']['incentive_ratio']]
        self.assertLess(model.value(model.project(self.data), self.data)['per_share'], base)

    def test_revolver_draw_repayment_and_expiry(self):
        self.data['assumptions']['minimum_cash'] = 24000
        rows = model.project(self.data)
        model.check(rows, self.data)
        self.assertGreater(rows[0]['change_revolver'], 0)
        self.assertLess(rows[1]['change_revolver'], 0)
        self.assertEqual(rows[2]['revolver'], 0)
        self.data['assumptions']['revolver_limits'][0] = 0
        with self.assertRaisesRegex(ValueError, 'below floor'):
            model.value(model.project(self.data), self.data)

    def test_expired_revolver_cannot_be_carried_forward(self):
        self.data['assumptions']['minimum_cash'] = 24000
        self.data['assumptions']['dividend_payout'] = .30
        self.data['assumptions']['buyback_payout'] = .68
        self.data['assumptions']['revolver_limits'] = [7000,7000,0,0,0]
        with self.assertRaisesRegex(ValueError, 'revolver exceeds'):
            model.value(model.project(self.data), self.data)

    def test_invalid_terminal_rate(self):
        self.data['assumptions']['cost_of_equity'] = .03
        with self.assertRaisesRegex(ValueError, 'cost of equity'):
            model.value(model.project(self.data), self.data)

    def test_negative_terminal_cash_flow_refuses(self):
        self.data['assumptions']['expense_ratios']['litigation'] = .8
        self.data['assumptions']['minimum_cash'] = 0
        self.data['opening']['cash'] += 1e6
        self.data['opening']['equity'] += 1e6
        with self.assertRaisesRegex(ValueError, 'Negative FCFE'):
            model.value(model.project(self.data), self.data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
