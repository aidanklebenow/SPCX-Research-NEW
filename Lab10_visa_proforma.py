"""FIN 43900 Lab 10 — Visa (V), USD millions except per-share amounts.

Standard library only. Annual teaching model anchored September 30, 2025;
assumptions researched September 24, 2026. See Lab10_summary.md for limitations.
Run: python3 lab-10/Lab10_visa_proforma.py
Refusal: python3 lab-10/Lab10_visa_proforma.py --break-2026-cash
"""

import argparse
import json
from math import isfinite
from pathlib import Path


DATA_PATH = Path(__file__).with_name('Lab10_visa_inputs.json')
ASSETS = ('cash', 'escrow', 'securities', 'settlement_receivable', 'receivables',
          'collateral_asset', 'incentive_assets', 'prepaid', 'ppe', 'goodwill',
          'intangibles', 'other_assets')
LIABILITIES = ('payables', 'settlement_payable', 'collateral_liability',
               'compensation', 'incentive_liability', 'accrued_liabilities',
               'debt', 'litigation_liability', 'deferred_tax', 'other_liabilities',
               'revolver')
WC_ASSETS = ('receivables', 'settlement_receivable', 'incentive_assets')
WC_LIABILITIES = ('payables', 'settlement_payable', 'compensation', 'incentive_liability')


def load_inputs(path=DATA_PATH):
    return json.loads(Path(path).read_text())


def gap(r):
    return sum(r[k] for k in ASSETS) - sum(r[k] for k in LIABILITIES) - r['equity']


def require_close(actual, expected, message):
    if not isfinite(actual) or not isfinite(expected) or abs(actual - expected) > 1e-6:
        raise ValueError(f'{message}: {actual - expected:,.6f} million')


def project(data):
    o, a = data['opening'], data['assumptions']
    require_close(gap(o), 0, 'Opening balance-sheet gap')
    p, rows = o.copy(), []
    for i, year in enumerate(range(2026, 2031)):
        r = p.copy()
        r['year'] = year
        r['gross_revenue'] = p['gross_revenue'] * (1 + a['gross_growth'][i])
        r['incentives'] = r['gross_revenue'] * a['incentive_ratio'][i]
        r['revenue'] = r['gross_revenue'] - r['incentives']
        for key, rate in a['expense_ratios'].items():
            r[key] = r['revenue'] * rate
        r['depreciation'] = p['ppe'] * a['ppe_depreciation_rate']
        r['amortization'] = a['intangible_amortization'][i]
        if r['amortization'] > p['intangibles'] - a['indefinite_intangibles'] + 1e-6:
            raise ValueError(f'FY{year}E: amortization exceeds finite-lived assets')
        r['operating_income'] = (r['revenue'] - sum(r[k] for k in a['expense_ratios'])
                                 - r['depreciation'] - r['amortization'])
        r['interest'] = p['debt'] * a['debt_rate'] + p['revolver'] * a['revolver_rate']
        r['pretax'] = r['operating_income'] - r['interest']
        r['tax'] = max(r['pretax'], 0) * a['tax_rate']
        r['net_income'] = r['pretax'] - r['tax']
        r['capex'] = r['revenue'] * a['capex_ratio']
        r['ppe'] = p['ppe'] + r['capex'] - r['depreciation']
        r['intangibles'] = p['intangibles'] - r['amortization']
        for key in ('receivables', 'payables', 'compensation'):
            r[key] = o[key] / o['revenue'] * r['revenue']
        for key in ('settlement_receivable', 'settlement_payable'):
            r[key] = o[key] / o['gross_revenue'] * r['gross_revenue']
        for key in ('incentive_assets', 'incentive_liability'):
            r[key] = o[key] / o['incentives'] * r['incentives']
        r['change_wc_assets'] = sum(r[k] - p[k] for k in WC_ASSETS)
        r['change_wc_liabilities'] = sum(r[k] - p[k] for k in WC_LIABILITIES)
        r['change_incentive_assets'] = r['incentive_assets'] - p['incentive_assets']
        r['change_incentive_liability'] = r['incentive_liability'] - p['incentive_liability']
        r['incentive_cash_paid'] = (r['incentives'] + r['change_incentive_assets']
                                     - r['change_incentive_liability'])
        # NI already includes incentive expense. Only the balance changes enter CFO.
        # Compensation, including historical SBC-equivalent cost, is paid in cash.
        r['cfo'] = (r['net_income'] + r['depreciation'] + r['amortization']
                    - r['change_wc_assets'] + r['change_wc_liabilities'])
        r['debt_repaid'] = a['debt_maturities'][i]
        r['debt_issued'] = r['debt_repaid'] * a['refinance_fraction']
        if r['debt_repaid'] > p['debt_principal'] + 1e-6:
            raise ValueError(f'FY{year}E: repayment exceeds debt principal')
        r['debt_principal'] = p['debt_principal'] + r['debt_issued'] - r['debt_repaid']
        # Carrying-value adjustments stay fixed; no fee amortization or FX modeled.
        r['debt'] = p['debt'] + r['debt_issued'] - r['debt_repaid']
        r['fcfe_before_revolver'] = (r['cfo'] - r['capex']
                                    + r['debt_issued'] - r['debt_repaid'])
        r['dividends'] = max(r['net_income'], 0) * a['dividend_payout']
        r['buybacks'] = max(r['net_income'], 0) * a['buyback_payout']
        r['equity'] = p['equity'] + r['net_income'] - r['dividends'] - r['buybacks']
        before = p['cash'] + r['fcfe_before_revolver'] - r['dividends'] - r['buybacks']
        limit = a['revolver_limits'][i]
        if before < a['minimum_cash']:
            r['change_revolver'] = min(a['minimum_cash'] - before, max(0, limit - p['revolver']))
        else:
            r['change_revolver'] = -min(p['revolver'], before - a['minimum_cash'])
        r['revolver'] = p['revolver'] + r['change_revolver']
        r['fcfe'] = r['fcfe_before_revolver'] + r['change_revolver']
        r['cfi'] = -r['capex']
        r['cff'] = (r['debt_issued'] - r['debt_repaid'] + r['change_revolver']
                    - r['dividends'] - r['buybacks'])
        r['opening_cash'] = p['cash']
        r['change_cash'] = r['cfo'] + r['cfi'] + r['cff']
        r['cash'] = p['cash'] + r['change_cash']
        r['assets'] = sum(r[k] for k in ASSETS)
        r['liabilities'] = sum(r[k] for k in LIABILITIES)
        rows.append(r)
        p = r
    return rows


def check(rows, data):
    o, a = data['opening'], data['assumptions']
    if len(rows) != 5:
        raise ValueError('Require five projected years')
    require_close(gap(o), 0, 'Opening balance-sheet gap')
    p = o
    for i, r in enumerate(rows):
        year = f"FY{r['year']}E"
        if not all(isfinite(x) for x in r.values()):
            raise ValueError(f'{year}: non-finite value')
        require_close(gap(r), 0, f'{year}: balance-sheet gap')
        require_close(r['cash'] - p['cash'], r['cfo'] + r['cfi'] + r['cff'], f'{year}: cash-flow bridge')
        require_close(r['assets'], sum(r[k] for k in ASSETS), f'{year}: asset total')
        require_close(r['liabilities'], sum(r[k] for k in LIABILITIES), f'{year}: liability total')
        require_close(r['equity'], p['equity'] + r['net_income'] - r['dividends'] - r['buybacks'], f'{year}: equity roll-forward')
        require_close(r['ppe'], p['ppe'] + r['capex'] - r['depreciation'], f'{year}: PP&E roll-forward')
        require_close(r['intangibles'], p['intangibles'] - r['amortization'], f'{year}: intangible roll-forward')
        require_close(r['debt'], p['debt'] + r['debt_issued'] - r['debt_repaid'], f'{year}: debt roll-forward')
        require_close(r['debt_principal'], p['debt_principal'] + r['debt_issued'] - r['debt_repaid'], f'{year}: principal roll-forward')
        require_close(r['revenue'], r['gross_revenue'] - r['incentives'], f'{year}: net revenue bridge')
        require_close(r['operating_income'], r['revenue'] - sum(r[k] for k in a['expense_ratios']) - r['depreciation'] - r['amortization'], f'{year}: operating income bridge')
        require_close(r['net_income'], r['operating_income'] - r['interest'] - r['tax'], f'{year}: net income bridge')
        require_close(r['cfi'], -r['capex'], f'{year}: investing cash flow')
        require_close(r['cff'], r['debt_issued'] - r['debt_repaid'] + r['change_revolver'] - r['dividends'] - r['buybacks'], f'{year}: financing cash flow')
        require_close(r['fcfe'], r['cfo'] - r['capex'] + r['debt_issued'] - r['debt_repaid'] + r['change_revolver'], f'{year}: FCFE bridge')
        require_close(r['cfo'], r['net_income'] + r['depreciation'] + r['amortization'] - sum(r[k]-p[k] for k in WC_ASSETS) + sum(r[k]-p[k] for k in WC_LIABILITIES), f'{year}: CFO bridge')
        require_close(r['incentive_cash_paid'], r['incentives'] + r['incentive_assets'] - p['incentive_assets'] - r['incentive_liability'] + p['incentive_liability'], f'{year}: incentive cash bridge')
        require_close(r['collateral_asset'], r['collateral_liability'], f'{year}: collateral offset')
        if r['cash'] < a['minimum_cash'] - 1e-6:
            raise ValueError(f"{year}: cash {r['cash']:,.1f} below floor {a['minimum_cash']:,.1f}")
        if not -1e-6 <= r['revolver'] <= a['revolver_limits'][i] + 1e-6:
            raise ValueError(f'{year}: revolver exceeds available commitment')
        if any(r[k] < -1e-6 for k in ASSETS + LIABILITIES):
            raise ValueError(f'{year}: negative asset or liability')
        p = r


def value(rows, data):
    check(rows, data)  # Valuation cannot bypass the accounting/financing gate.
    a = data['assumptions']
    ke, g, shares = a['cost_of_equity'], a['terminal_growth'], a['shares']
    if not all(isfinite(x) for x in (ke, g, shares)) or not ke > g >= 0 or shares <= 0:
        raise ValueError('Require finite cost of equity > terminal growth >= 0 and positive shares')
    # Lab rule: only positive explicit FCFE is valued. Negative years remain visible.
    explicit = sum(max(r['fcfe'], 0) / (1 + ke) ** t for t, r in enumerate(rows, 1))
    last = rows[-1]
    if last['revolver'] > 1e-6:
        raise ValueError('Terminal revolver remains outstanding; resolve financing before valuation')
    # Normalize to stable-growth reinvestment: capex - D&A = g * closing PP&E;
    # working-capital investment = g * closing operating net working capital.
    # Flat term debt is refinanced; no ABG debt-repayment addback is applied.
    nwc = sum(last[k] for k in WC_ASSETS) - sum(last[k] for k in WC_LIABILITIES)
    terminal_fcfe = last['net_income'] * (1 + g) - g * last['ppe'] - g * nwc
    if last['fcfe'] <= 0 or terminal_fcfe <= 0:
        raise ValueError('Negative FCFE: terminal value requires positive sustainable cash flow')
    if a['refinance_fraction'] != 1:
        raise ValueError('Non-base refinancing: define a consistent terminal debt policy before valuation')
    terminal_pv = terminal_fcfe / (ke - g) / (1 + ke) ** 5
    # No interest income is projected. Credit existing unrestricted surplus once;
    # do not add forecast ending cash, escrow or client collateral to valuation.
    surplus_cash = max(data['opening']['cash'] - a['minimum_cash'], 0)
    equity = explicit + terminal_pv + surplus_cash
    return dict(explicit_pv=explicit, terminal_fcfe=terminal_fcfe,
                terminal_pv=terminal_pv, surplus_cash=surplus_cash, equity=equity,
                per_share=equity / shares, terminal_share=terminal_pv / equity)


def table(title, rows, keys):
    print('\n' + title)
    print(f"{'USD millions':<31}" + ''.join(f"FY{r['year']}E".rjust(13) for r in rows))
    for key in keys:
        print(f'{key:<31}' + ''.join(f'{r[key]:>13,.1f}' for r in rows))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--break-2026-cash', action='store_true')
    parser.add_argument('--inputs', type=Path, default=DATA_PATH)
    args = parser.parse_args()
    data = load_inputs(args.inputs)
    try:
        rows = project(data)
        if args.break_2026_cash:
            rows[0]['cash'] = data['opening']['cash']
        print('FIN 43900 | Lab 10 | Visa (V) | annual teaching model')
        print('Discount anchor: 2025-09-30; research date: 2026-09-24')
        table('INCOME STATEMENT', rows, ['gross_revenue', 'incentives', 'revenue']
              + list(data['assumptions']['expense_ratios'])
              + ['depreciation', 'amortization', 'operating_income', 'interest', 'pretax', 'tax', 'net_income'])
        table('BALANCE SHEET (current/noncurrent incentive and debt balances combined)', rows,
              list(ASSETS) + ['assets'] + list(LIABILITIES) + ['liabilities', 'equity'])
        table('CASH FLOW (unrestricted cash; frozen restricted balances)', rows,
              ['net_income', 'depreciation', 'amortization', 'change_wc_assets',
               'change_wc_liabilities', 'incentive_cash_paid', 'cfo', 'capex', 'cfi',
               'debt_repaid', 'debt_issued', 'change_revolver', 'fcfe', 'dividends',
               'buybacks', 'cff', 'change_cash', 'opening_cash', 'cash'])
        print('\nCHECK BLOCK (each accounting gap must be zero)')
        for r in rows:
            g = gap(r)
            c = r['cash'] - r['opening_cash'] - r['change_cash']
            print(f"FY{r['year']}E: BS gap={0 if abs(g)<1e-6 else g:.6f}; "
                  f"cash bridge={0 if abs(c)<1e-6 else c:.6f}; "
                  f"cash floor={r['cash'] >= data['assumptions']['minimum_cash']}; "
                  f"revolver={r['revolver']:,.1f}"
                  + ('; negative FCFE (excluded under lab rule)' if r['fcfe'] < 0 else ''))
        v = value(rows, data)
        print('All accounting and financing checks PASS.')
        for k in ('explicit_pv', 'terminal_fcfe', 'terminal_pv', 'surplus_cash', 'equity'):
            print(f'{k}: ${v[k]:,.2f} million')
        print(f"Terminal share of equity value: {v['terminal_share']:.2%}")
        print(f"Fixed opening as-converted shares: {data['assumptions']['shares']:,.0f} million")
        print(f"Value per share: ${v['per_share']:.2f}")
        print('Annual-model value, not a September 2026 spot valuation. See report for dated market comparison.')
    except (ValueError, KeyError, TypeError) as error:
        parser.exit(1, f'VALUATION REFUSED: {error}\n')


if __name__ == '__main__':
    main()
