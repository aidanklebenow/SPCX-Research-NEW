"""Functional UI, manual allocation and Yahoo timestamp regression checks."""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import portfolio as p


class DialTests(unittest.TestCase):
    def test_endpoints_and_exact_total_across_repeated_moves(self):
        weights = [0, 20, 25, 55]
        for index, value in [(0, 100), (0, 40), (3, 0), (1, 99), (1, 1), (2, 55)]:
            weights = p.rebalance_weights_percent(weights, index, value)
            self.assertEqual(weights[index], value)
            self.assertEqual(sum(weights), 100)
            self.assertTrue(all(0 <= w <= 100 for w in weights))

    def test_proportional_rebalance_and_manual_engine(self):
        self.assertEqual(p.rebalance_weights_percent([50, 30, 20], 0, 25), [25, 45, 30])
        result = p.evaluate_mix([0, .2, .25, .55], p.VEHICLES, p.CORRELATIONS, p.RESERVE_ELIGIBLE)
        self.assertEqual(f"{result['expected_return']:.2%}", '6.51%')
        self.assertEqual(f"{result['volatility']:.2%}", '9.44%')


class YahooTests(unittest.TestCase):
    def test_trade_time_is_not_fetch_time_and_invalid_quotes_fail(self):
        from market_data import parse_quote
        payload = {'chart': {'result': [{'meta': {'symbol': 'VTI',
            'regularMarketPrice': 110., 'regularMarketTime': 1_700_000_000,
            'chartPreviousClose': 100., 'currency': 'USD'},
            'timestamp': [1_700_000_000],
            'indicators': {'quote': [{'close': [110.]}]}}], 'error': None}}
        result = parse_quote(payload, 'VTI', fetched_at='2026-10-22T21:00:00+00:00')
        self.assertNotEqual(result['trade_time'], result['fetched_at'])
        self.assertAlmostEqual(result['change_percent'], 10.)
        for value in [None, 0, float('nan')]:
            bad = copy.deepcopy(payload)
            bad['chart']['result'][0]['meta']['regularMarketPrice'] = value
            with self.assertRaises(ValueError):
                parse_quote(bad, 'VTI')


class DashboardTests(unittest.TestCase):
    def test_dashboard_dials_stress_etf_window_and_pages(self):
        from streamlit.testing.v1 import AppTest
        import streamlit as st
        st.cache_data.clear()
        quotes = [dict(ticker=t, name=t, price=100., currency='USD', change_percent=1.,
            trade_time='2026-10-22T20:00:00+00:00', fetched_at='2026-10-22T21:00:00+00:00',
            exchange='Test exchange', history=[{'time':'2026-10-22T20:00:00+00:00','price':100.}],
            source=f'https://finance.yahoo.com/quote/{t}/') for t in ('SGOV','IEF','LQD','VTI','VXUS')]
        def find(elements, label):
            return next(e for e in elements if e.label == label)
        def healthy(app):
            self.assertFalse(app.exception, [(e.message, e.stack_trace) for e in app.exception])
        with patch('market_data.fetch_quotes', return_value=quotes):
            app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py'), default_timeout=60).run()
            healthy(app)
            self.assertEqual(find(app.metric, 'Largest weight change (percentage points)').value, '0.00')
            app.slider[0].set_value(100).run()
            healthy(app)
            self.assertEqual([s.value for s in app.slider], [100, 0, 0, 0])
            self.assertEqual(find(app.metric, 'Your mix · return estimate').value, '3.50%')
            app.slider[0].set_value(40).run()
            self.assertEqual([s.value for s in app.slider], [40, 20, 20, 20])
            find(app.number_input, 'Global equity index fund return estimate (%)').set_value(7.).run()
            healthy(app)
            self.assertEqual(find(app.metric, 'Largest weight change (percentage points)').value, '25.00')
            find(app.radio, 'Explore').set_value('How it works').run()
            healthy(app)
            find(app.radio, 'Explore').set_value('Dashboard').run()
            healthy(app)
            self.assertEqual(sum(s.value for s in app.slider), 100)
            self.assertEqual(find(app.number_input, 'Global equity index fund return estimate (%)').value, 7.)
            find(app.selectbox, 'Investment universe').set_value('My five ETFs').run()
            find(app.button, 'Use my Lab 13 draft: 7.5% / 10%').click().run()
            healthy(app)
            self.assertEqual(len(app.slider), 5)
            find(app.toggle, 'Use only the last 36 months').set_value(True).run()
            healthy(app)
            self.assertEqual(find(app.metric, 'Largest weight change (percentage points)').value, '25.00')
            find(app.radio, 'Explore').set_value('Lab notebook').run()
            healthy(app)
            self.assertEqual(len(app.text_area), 2)
            find(app.radio, 'Explore').set_value('Market quotes').run()
            healthy(app)
            self.assertEqual(find(app.metric, 'VTI').value, '100.00 USD')


if __name__ == '__main__':
    unittest.main()
