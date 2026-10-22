"""Lab 15 numerical acceptance checks and CSV estimation boundaries."""
import copy
import csv
from datetime import date
from io import StringIO
from pathlib import Path
from statistics import mean, stdev, correlation
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import portfolio as p


def synthetic_prices():
    """Synthetic data for tests only, never submitted as market prices."""
    out = StringIO()
    writer = csv.writer(out)
    writer.writerow(['Date', 'A', 'B', 'C'])
    prices = [100., 100., 100.]
    returns = []
    for month in range(61):
        if month:
            changes = [0.002 + (month % 7) * .001,
                       -.003 + (month % 5) * .002,
                       .001 + (month % 3) * .003]
            returns.append(changes)
            prices = [price * (1 + change) for price, change in zip(prices, changes)]
        writer.writerow([date(2021 + month // 12, month % 12 + 1, 1).isoformat(), *prices])
    return out.getvalue(), returns


class StabilityTests(unittest.TestCase):
    def test_meridian_acceptance_runs(self):
        original_report = p.report()
        base = p.lowest_risk_mix(p.VEHICLES, p.CORRELATIONS)
        changed = list(p.VEHICLES)
        changed[3] = (changed[3][0], .07, changed[3][2])
        stress = p.lowest_risk_mix(changed, p.CORRELATIONS)
        corr = copy.deepcopy(p.CORRELATIONS)
        corr[2][3] = corr[3][2] = .50
        probe = p.lowest_risk_mix(p.VEHICLES, corr)
        for result, weights, ret, risk in [
            (base, [0, .2, .25, .55], '6.51%', '9.44%'),
            (stress, [0, .1, .1, .8], '6.53%', '12.94%'),
            (probe, [0, .4, 0, .6], '6.52%', '9.73%'),
        ]:
            self.assertEqual(result['weights'], weights)
            self.assertEqual(f"{result['expected_return']:.2%}", ret)
            self.assertEqual(f"{result['volatility']:.2%}", risk)
        self.assertAlmostEqual(max(abs(a-b) for a,b in zip(base['weights'], stress['weights'])), .25)
        self.assertEqual(p.report(), original_report)

    def test_infeasibility_and_custom_reserves(self):
        self.assertIsNone(p.lowest_risk_mix(p.VEHICLES, p.CORRELATIONS, objective=.09))
        self.assertIsNone(p.lowest_risk_mix(p.VEHICLES, p.CORRELATIONS, reserve_eligible=set()))
        result = p.lowest_risk_mix(p.VEHICLES, p.CORRELATIONS, objective=.04,
                                  reserve_minimum=.03, reserve_eligible={'Treasury bills'})
        self.assertGreaterEqual(result['weights'][0], .05)
        self.assertAlmostEqual(sum(result['weights']), 1)

    def test_estimates_and_36_returns_not_35(self):
        text, returns = synthetic_prices()
        for last_36 in (False, True):
            result = p.estimate_from_csv(StringIO(text), last_36=last_36)
            selected = returns[-36:] if last_36 else returns
            self.assertEqual(result['months'], len(selected))
            for index, asset in enumerate(result['vehicles']):
                column = [row[index] for row in selected]
                self.assertAlmostEqual(asset[1], mean(column) * 12)
                self.assertAlmostEqual(asset[2], stdev(column) * 12 ** .5)
            self.assertAlmostEqual(result['correlations'][0][1], correlation(
                [r[0] for r in selected], [r[1] for r in selected]))

    def test_bad_prices_dates_and_short_window(self):
        text, _ = synthetic_prices()
        lines = text.splitlines()
        bad_inputs = [text.replace('2021-02-01', '2021-01-01'),
                      '\n'.join(lines[:2] + lines[3:]),
                      text.replace('100.0', 'nan', 1),
                      text.replace('100.0', '0', 1),
                      text.replace('100.0', '', 1)]
        for bad in bad_inputs:
            with self.assertRaises(ValueError):
                p.estimate_from_csv(StringIO(bad))
        with self.assertRaisesRegex(ValueError, '37 monthly prices'):
            p.estimate_from_csv(StringIO('\n'.join(lines[:20])), last_36=True)


if __name__ == '__main__':
    unittest.main()
