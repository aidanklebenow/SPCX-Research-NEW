"""FIN 43900 Lab 09: ABG training case; USD millions except per-share values.

Run: python3 proforma.py
Demonstrate refusal: python3 proforma.py --break-2026-cash
Source: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/lab-09-proforma-build.md
Built with Codex assistance. Standard library only.
"""

import argparse
from math import isfinite


OPENING = dict(revenue=17999.0, inventory=2135.8, ppe=3070.4,
               other_assets=6371.6, cash=40.4, floor_plan=2027.0,
               debt=3572.0, other_liabilities=2127.5, equity=3891.7,
               revolver=0.0)
ASSUMPTIONS = dict(
    growth=0.018, gross_margin=0.1705,
    sga_ratios=(0.665, 0.655, 0.645, 0.645, 0.645),
    depreciation_ratio=82.4 / 3070.4, impairment=120.0, capex=250.0,
    tax_rate=0.255, inventory_days=2135.8 / (17999.0 - 3071.7) * 365,
    floor_plan_ratio=2027.0 / 2135.8, working_capital_ratio=0.008,
    minimum_cash=25.0, revolver_limit=850.0, revolver_rate=0.06,
    repayment=150.0, buyback=150.0, floor_plan_rate=0.0467,
    debt_rate=0.0544, cost_of_equity=0.10, terminal_growth=0.025,
    shares=17.951349,
)


def balance_gap(row):
    assets = sum(row[k] for k in ('cash', 'inventory', 'ppe', 'other_assets'))
    liabilities = sum(row[k] for k in
                      ('floor_plan', 'debt', 'revolver', 'other_liabilities'))
    return assets - liabilities - row['equity']


def assert_balanced(rows, assumptions=ASSUMPTIONS):
    """Refuse valuation if a balance sheet or financing constraint fails."""
    for row in rows:
        gap = balance_gap(row)
        prefix = f"FY{row['year']}E: balance-sheet gap {gap:.1f} million"
        if not all(isfinite(v) for v in row.values()):
            raise ValueError(f'{prefix}; non-finite model value')
        if abs(gap) > 1e-6:
            raise ValueError(prefix)
        if row['cash'] < assumptions['minimum_cash'] - 1e-6:
            raise ValueError(f"{prefix}; cash {row['cash']:.1f} below minimum")
        if not -1e-6 <= row['revolver'] <= assumptions['revolver_limit'] + 1e-6:
            raise ValueError(f'{prefix}; revolver outside permitted limits')


def project(opening=OPENING, assumptions=ASSUMPTIONS):
    a = assumptions
    previous = opening.copy()
    rows = []
    for index, year in enumerate(range(2026, 2031)):
        r = dict(year=year)
        r['revenue'] = previous['revenue'] * (1 + a['growth'])
        r['gross_profit'] = r['revenue'] * a['gross_margin']
        r['cost_of_sales'] = r['revenue'] - r['gross_profit']
        r['sga'] = r['gross_profit'] * a['sga_ratios'][index]
        r['depreciation'] = previous['ppe'] * a['depreciation_ratio']
        r['impairment'] = a['impairment']
        r['operating_income'] = (r['gross_profit'] - r['sga']
                                 - r['depreciation'] - r['impairment'])
        r['interest'] = (previous['floor_plan'] * a['floor_plan_rate']
                         + previous['debt'] * a['debt_rate']
                         + previous['revolver'] * a['revolver_rate'])
        r['pretax'] = r['operating_income'] - r['interest']
        r['tax'] = max(0, r['pretax']) * a['tax_rate']
        r['net_income'] = r['pretax'] - r['tax']
        r['inventory'] = r['cost_of_sales'] * a['inventory_days'] / 365
        r['floor_plan'] = r['inventory'] * a['floor_plan_ratio']
        r['capex'] = a['capex']
        r['ppe'] = previous['ppe'] + r['capex'] - r['depreciation']
        r['change_other_wc'] = a['working_capital_ratio'] * (r['revenue'] - previous['revenue'])
        r['other_assets'] = previous['other_assets'] + r['change_other_wc'] - r['impairment']
        r['repayment'] = a['repayment']
        if r['repayment'] > previous['debt']:
            raise ValueError(f'FY{year}E: repayment exceeds outstanding term debt')
        r['debt'] = previous['debt'] - r['repayment']
        r['other_liabilities'] = previous['other_liabilities']
        r['buyback'] = a['buyback']
        r['equity'] = previous['equity'] + r['net_income'] - r['buyback']
        r['change_inventory'] = r['inventory'] - previous['inventory']
        r['change_floor_plan'] = r['floor_plan'] - previous['floor_plan']
        # Course convention: floor-plan changes are inside operating cash flow.
        r['cfo'] = (r['net_income'] + r['depreciation'] + r['impairment']
                    - r['change_inventory'] - r['change_other_wc'] + r['change_floor_plan'])
        r['fcfe'] = r['cfo'] - r['capex'] - r['repayment']
        r['opening_cash'] = previous['cash']
        cash_before_revolver = previous['cash'] + r['fcfe'] - r['buyback']
        if cash_before_revolver < a['minimum_cash']:
            r['change_revolver'] = min(a['minimum_cash'] - cash_before_revolver,
                                       a['revolver_limit'] - previous['revolver'])
        else:
            r['change_revolver'] = -min(previous['revolver'], cash_before_revolver - a['minimum_cash'])
        r['revolver'] = previous['revolver'] + r['change_revolver']
        r['cash'] = cash_before_revolver + r['change_revolver']
        r['cfi'] = -r['capex']
        r['cff'] = -r['repayment'] - r['buyback'] + r['change_revolver']
        r['change_cash'] = r['cfo'] + r['cfi'] + r['cff']
        r['assets'] = r['cash'] + r['inventory'] + r['ppe'] + r['other_assets']
        r['liabilities'] = r['floor_plan'] + r['debt'] + r['revolver'] + r['other_liabilities']
        r['liabilities_equity'] = r['liabilities'] + r['equity']
        rows.append(r)
        previous = r
    return rows


def value_equity(rows, assumptions=ASSUMPTIONS):
    assert_balanced(rows, assumptions)  # Mandatory gate before any valuation.
    rate, growth = assumptions['cost_of_equity'], assumptions['terminal_growth']
    if not rate > growth or assumptions['shares'] <= 0:
        raise ValueError('Require cost of equity > terminal growth and positive shares')
    explicit_pv = sum(r['fcfe'] / (1 + rate) ** t for t, r in enumerate(rows, 1))
    # Required case convention: scheduled debt repayments stop after 2030.
    terminal_fcfe = (rows[-1]['fcfe'] + rows[-1]['repayment']) * (1 + growth)
    terminal_value = terminal_fcfe / (rate - growth)
    terminal_pv = terminal_value / (1 + rate) ** len(rows)
    equity = explicit_pv + terminal_pv
    return dict(explicit_pv=explicit_pv, terminal_value=terminal_value,
                terminal_pv=terminal_pv, equity=equity,
                terminal_share=terminal_pv / equity,
                per_share=equity / assumptions['shares'])


def print_table(title, rows, fields):
    print('\n' + title)
    print(f"{'USD millions':<29}" + ''.join(f"{'FY' + str(r['year']) + 'E':>13}" for r in rows))
    for label, key in fields:
        print(f'{label:<29}' + ''.join(f'{r[key]:>13,.1f}' for r in rows))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--break-2026-cash', action='store_true', help='Required deliberate error; exits without valuation')
    args = parser.parse_args()
    rows = project()
    if args.break_2026_cash:
        rows[0]['cash'] = OPENING['cash']
        rows[0]['assets'] = sum(rows[0][k] for k in ('cash', 'inventory', 'ppe', 'other_assets'))
    print('FIN 43900 | Lab 09 | Asbury (ABG) training case')
    print_table('INCOME STATEMENT', rows, [
        ('Revenue', 'revenue'), ('Cost of sales', 'cost_of_sales'), ('Gross profit', 'gross_profit'),
        ('SG&A', 'sga'), ('Depreciation', 'depreciation'), ('Impairment', 'impairment'),
        ('Operating income', 'operating_income'), ('Interest', 'interest'),
        ('Pretax income', 'pretax'), ('Tax', 'tax'), ('Net income', 'net_income')])
    print_table('BALANCE SHEET', rows, [
        ('Cash', 'cash'), ('Inventory', 'inventory'), ('PP&E', 'ppe'), ('Other assets', 'other_assets'),
        ('Total assets', 'assets'), ('Floor-plan loans', 'floor_plan'), ('Term debt', 'debt'),
        ('Revolver', 'revolver'), ('Other liabilities', 'other_liabilities'),
        ('Total liabilities', 'liabilities'), ('Equity', 'equity'), ('Liabilities + equity', 'liabilities_equity')])
    print_table('CASH FLOW (positive changes shown before sign in CFO)', rows, [
        ('Net income', 'net_income'), ('+ Depreciation', 'depreciation'), ('+ Impairment', 'impairment'),
        ('- Change in inventory', 'change_inventory'), ('- Change in other WC', 'change_other_wc'),
        ('+ Change in floor plan', 'change_floor_plan'), ('Operating cash flow', 'cfo'),
        ('Investing cash flow', 'cfi'), ('Term debt repayment', 'repayment'), ('FCFE before buybacks/revolver', 'fcfe'),
        ('Share buybacks', 'buyback'), ('Revolver draw/(repayment)', 'change_revolver'),
        ('Financing cash flow', 'cff'), ('Net change in cash', 'change_cash'),
        ('Opening cash', 'opening_cash'), ('Ending cash', 'cash')])
    print('\nCHECKS')
    for r in rows:
        gap = balance_gap(r)
        display_gap = 0.0 if abs(gap) < 1e-6 else gap
        print(f"FY{r['year']}E: assets - liabilities - equity = {display_gap:.1f}; "
              f"cash >= {ASSUMPTIONS['minimum_cash']:.1f}: {r['cash'] >= ASSUMPTIONS['minimum_cash']}; "
              f"revolver <= {ASSUMPTIONS['revolver_limit']:.1f}: {r['revolver'] <= ASSUMPTIONS['revolver_limit']}")
    try:
        result = value_equity(rows)
    except ValueError as error:
        parser.exit(1, f'VALUATION REFUSED: {error}\n')
    print(f"\nEquity value: ${result['equity']:,.2f} million")
    print(f"Share of value after 2030: {result['terminal_share']:.2%}")
    print(f"Value per share: ${result['per_share']:.2f}")


if __name__ == '__main__':
    main()
