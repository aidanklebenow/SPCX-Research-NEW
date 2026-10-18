"""Lab 11 regression checks for scenario isolation and invalid outputs."""
import json
import unittest
from copy import deepcopy
from unittest.mock import patch
import Lab11_sensitivity as s

class SensitivityTests(unittest.TestCase):
    def setUp(self):
        self.base=json.loads((s.HERE/'Lab11_base_inputs.json').read_text())
        self.ranges=json.loads((s.HERE/'Lab11_ranges.json').read_text())

    def test_isolation_restoration_and_arithmetic(self):
        original=deepcopy(self.base)
        result=s.analyze(self.base,self.ranges)
        self.assertEqual(self.base,original)
        self.assertEqual(result['max_restored_difference'],0)
        self.assertAlmostEqual(result['base_before']['outputs']['per_share'],273.7619836133012)
        for run in result['runs']:
            self.assertTrue(run['accounting_valid'] and run['valuation_valid'])
            expected=[] if run['level']=='base' else ['assumptions.'+run['driver']]
            self.assertEqual(s.differences(original,run['inputs']),expected)
            for key in s.OUTPUTS:
                self.assertAlmostEqual(run['deltas'][key],run['outputs'][key]-result['base_before']['outputs'][key])
        for driver in self.ranges['drivers']:
            for key in s.OUTPUTS:
                values=[r['outputs'][key] for r in result['runs'] if r['driver']==driver]
                self.assertAlmostEqual(result['spans'][driver][key]['span'],max(values)-min(values))

    def test_failed_accounting_excludes_rankings(self):
        with patch.object(s.engine,'check',side_effect=ValueError('deliberate broken balance')):
            run=s.evaluate(self.base,'broken')
        self.assertFalse(run['accounting_valid'])
        self.assertFalse(s.usable(run,'operating_profit'))
        self.assertIsNone(run['outputs']['per_share'])

    def test_negative_cash_flow_retained_without_valuation(self):
        rows=s.engine.project(deepcopy(self.base))
        rows[-1]['fcfe']=-100
        # Synthetic signed-flow fixture isolates the valuation gate.
        with patch.object(s.engine,'project',return_value=rows), patch.object(s.engine,'check'), patch.object(s.engine,'value') as value:
            run=s.evaluate(self.base,'negative')
        self.assertEqual(run['outputs']['fcfe'],-100)
        self.assertTrue(run['accounting_valid'])
        self.assertFalse(run['valuation_valid'])
        value.assert_not_called()

    def test_unresolved_valuation_keeps_operating_comparison(self):
        with patch.object(s.engine,'value',side_effect=ValueError('deliberate unresolved valuation')):
            result=s.analyze(self.base,self.ranges)
        self.assertIsNone(result['rankings']['per_share'])
        self.assertIsNotNone(result['rankings']['fcfe'])
        self.assertTrue(all(r['outputs']['fcfe']>0 for r in result['runs']))

if __name__=='__main__':
    unittest.main(verbosity=2)
