"""Independent published-answer and failure-boundary checks for Lab 13."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import mandate as m

class MandateTests(unittest.TestCase):
    def test_published_answers(self):
        self.assertAlmostEqual(m.reserve_minimum(), 3)
        expected = {'A': ([100, 0, 14, 100, 0], 0),
                    'B': ([100, 0, 1, 85, 9], 3),
                    'C': ([100, 0, 2, 100, 8], 1)}
        for name, (values, failures) in expected.items():
            rules = m.evaluate(m.CANDIDATES[name])
            self.assertEqual([r[1] for r in rules], values)
            self.assertEqual(sum(not r[2] for r in rules), failures)

    def test_required_probe_and_restoration(self):
        original = copy.deepcopy(m.CANDIDATES)
        probe = copy.deepcopy(m.CANDIDATES['A'])
        probe['Cash'], probe['Global equity index fund'] = -2, 64
        rules = m.evaluate(probe)
        self.assertEqual([r[1] for r in rules], [100, -2, 10, 100, 0])
        self.assertEqual([r[2] for r in rules], [True, False, True, True, True])
        self.assertEqual(m.CANDIDATES, original)

    def test_attack(self):
        self.assertTrue(all(r[2] for r in m.evaluate(m.CANDIDATES['D'])))

    def test_invalid_weights(self):
        for value in (float('nan'), float('inf')):
            weights = dict(m.CANDIDATES['A'], Cash=value)
            with self.assertRaises(ValueError):
                m.evaluate(weights)
        with self.assertRaises(ValueError):
            m.evaluate({'Cash': 100})

    def test_loss_rule_never_tested(self):
        self.assertEqual(len(m.evaluate(m.CANDIDATES['A'])), 5)
        self.assertIn('Calendar-year loss: requires CIO clarification', m.report())

if __name__ == '__main__':
    unittest.main(verbosity=2)
