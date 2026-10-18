"""Visa five-year FCFF DCF. Python standard library only.

Run from the course folder: python3 Visa/visa_dcf.py
Prints a reproducible report; does not write files or fetch changing data.
USD millions and millions of as-converted shares, except USD/share.
Source dates and modeling limitations are documented in Visa_DCF_Methodology.md.
"""
import json
from pathlib import Path


def starting_fcff(data):
    """Construct TTM fundamentals; normalize tax and working-capital investment."""
    history = data['history']
    ttm = {key: history['fy2025'][key] + history['nine_months_2026'][key]
           - history['nine_months_2025'][key] for key in history['fy2025']}
    tax = data['assumptions']['tax_rate']
    working_capital = ttm['revenue'] * data['assumptions']['annual_nwc_investment_to_revenue']
    fcff = ttm['ebit'] * (1 - tax) + ttm['da'] - ttm['capex'] - working_capital
    return ttm, working_capital, fcff


def dcf(fcff0, growth_rates, wacc, terminal_growth, cash, debt, shares):
    if len(growth_rates) != 5:
        raise ValueError('Exactly five annual growth rates are required.')
    if not -1 < terminal_growth < wacc or shares <= 0 or fcff0 <= 0:
        raise ValueError('Require positive starting FCFF/shares and -1 < terminal growth < WACC.')
    if any(g <= -1 for g in growth_rates):
        raise ValueError('Annual growth must exceed -100%.')
    fcff = fcff0
    forecast = []
    for year, growth in enumerate(growth_rates, 1):
        fcff *= 1 + growth
        forecast.append({'year': year, 'growth': growth, 'fcff': fcff,
                         'pv': fcff / (1 + wacc) ** year})
    fcff6 = fcff * (1 + terminal_growth)
    terminal = fcff6 / (wacc - terminal_growth)
    pv_terminal = terminal / (1 + wacc) ** 5
    pv_explicit = sum(row['pv'] for row in forecast)
    ev = pv_explicit + pv_terminal
    equity = ev + cash - debt
    return dict(forecast=forecast, fcff6=fcff6, terminal=terminal,
                pv_terminal=pv_terminal, pv_explicit=pv_explicit,
                enterprise_value=ev, equity_value=equity, price=equity / shares)


def reverse_growth(target_price, fcff0, wacc, terminal_growth, cash, debt, shares):
    """Solve constant five-year FCFF CAGR by bracketed bisection."""
    def price(growth):
        return dcf(fcff0, [growth] * 5, wacc, terminal_growth, cash, debt, shares)['price']
    low, high = -0.90, 1.0
    if not price(low) <= target_price <= price(high):
        raise ValueError('Market price lies outside the growth search bracket.')
    for _ in range(100):
        mid = (low + high) / 2
        if price(mid) < target_price:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def analyze(data):
    ttm, nwc, fcff0 = starting_fcff(data)
    b = data['balance_sheet']
    cash = b['cash'] + b['liquid_debt_securities'] - data['assumptions']['operating_cash_reserve']
    debt, shares = b['debt_principal'], b['as_converted_shares']
    scenarios = {name: dcf(fcff0, s['growth'], s['wacc'], s['terminal_growth'], cash, debt, shares)
                 for name, s in data['scenarios'].items()}
    base = data['scenarios']['base']
    implied = reverse_growth(data['market_price'], fcff0, base['wacc'], base['terminal_growth'], cash, debt, shares)
    return ttm, nwc, fcff0, cash, scenarios, implied


def main():
    data = json.loads(Path(__file__).with_name('visa_inputs.json').read_text())
    ttm, nwc, fcff0, cash, scenarios, implied = analyze(data)
    base = scenarios['base']
    print('VISA (V): five-year FCFF DCF — research date ' + data['research_date'])
    print(f"Comparison price: ${data['market_price']:.2f}; close {data['price_date']}")
    print('Amounts in USD millions; shares in millions. Estimates are not company guidance.')
    print('\nTTM ending June 30, 2026:', ttm)
    print(f'Assumed annual working-capital investment: {nwc:,.2f}')
    print(f'Normalized starting FCFF: {fcff0:,.2f}; cash added: {cash:,.2f}')
    print('\nYear | FCFF growth | FCFF ($M) | PV ($M)')
    for r in base['forecast']:
        print(f"{r['year']:4} | {r['growth']:11.1%} | {r['fcff']:9,.2f} | {r['pv']:9,.2f}")
    for key in ['fcff6', 'terminal', 'pv_terminal', 'pv_explicit', 'enterprise_value', 'equity_value']:
        print(f'{key}: {base[key]:,.2f}')
    print('\nScenario values per share:')
    for name, result in scenarios.items():
        print(f"{name}: ${result['price']:.2f}")
    print(f"Base value vs market: {base['price']/data['market_price']-1:.1%}")
    print(f"20% margin-of-safety reference price: ${base['price']*.8:.2f}")
    print(f'Market-implied constant FCFF growth: {implied:.4%}')
    print(f"Terminal share of enterprise value: {base['pv_terminal']/base['enterprise_value']:.1%}")
    print('\nSensitivity: value/share; terminal growth columns 2%, 3%, 4%')
    b = data['balance_sheet']
    for wacc in [.08, .09, .10]:
        values = [dcf(fcff0, data['scenarios']['base']['growth'], wacc, g, cash,
                      b['debt_principal'], b['as_converted_shares'])['price'] for g in [.02, .03, .04]]
        print(f"WACC {wacc:.0%}: " + ' | '.join(f'${p:.2f}' for p in values))
    print('\nConclusion: WAIT under the base assumptions; review the methodology and risks.')


if __name__ == '__main__':
    main()
