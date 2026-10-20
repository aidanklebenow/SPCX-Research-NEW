"""FIN 43900 Lab 13: Meridian mandate checker. Python standard library only.
Run from this folder: python3 mandate.py
Weights are percentages; monetary inputs are USD millions.
This is a mandate check, not an optimizer or a guarantee of future returns.
"""
from math import isfinite

# Editable assignment inputs. Treasury notes qualify under the supplied case table.
HOLDINGS = {
    'Cash': {'issuer': 'none', 'days': 0, 'reserve': True},
    'Treasury bills': {'issuer': 'U.S. Treasury', 'days': 1, 'reserve': True},
    'Treasury 10-year note': {'issuer': 'U.S. Treasury', 'days': 1, 'reserve': True},
    'Global equity index fund': {'issuer': 'diversified fund', 'days': 2, 'reserve': False},
    'Investment-grade bond fund': {'issuer': 'diversified fund', 'days': 3, 'reserve': False},
    'Private real estate fund': {'issuer': 'diversified fund', 'days': 90, 'reserve': False},
    'Acme Corp bonds': {'issuer': 'Acme Corp', 'days': 4, 'reserve': False},
    'Acme Corp stock': {'issuer': 'Acme Corp', 'days': 1, 'reserve': False},
}
CANDIDATES = {name: dict(zip(HOLDINGS, weights)) for name, weights in {
    'A': [2, 2, 10, 60, 26, 0, 0, 0],
    'B': [1, 0, 0, 55, 20, 15, 5, 4],
    'C': [1, 1, 0, 70, 20, 0, 0, 8],
    # AI-proposed attack: feasible under the checker; exposes S2/S10 suitability.
    'D': [100, 0, 0, 0, 0, 0, 0, 0],
    # Lab 14 benchmark: no eligible reserves despite meeting the return objective.
    'E': [0, 0, 0, 60, 40, 0, 0, 0],
}.items()}
RESERVE_SIZE = 100.0
QUARTERLY_DISTRIBUTION = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5
MINIMUM_LIQUID_SHARE = 90.0
ISSUER_LIMIT = 8.0
EXEMPT_ISSUERS = {'none', 'U.S. Treasury', 'diversified fund'}
TOLERANCE = 1e-9


def reserve_minimum():
    if not isfinite(RESERVE_SIZE) or RESERVE_SIZE <= 0:
        raise ValueError('Reserve size must be finite and positive')
    for value in (QUARTERLY_DISTRIBUTION, QUARTERS_TO_COVER,
                  LIQUIDITY_WINDOW, MINIMUM_LIQUID_SHARE, ISSUER_LIMIT):
        if not isfinite(value) or value < 0:
            raise ValueError('Policy parameters must be finite and nonnegative')
    if MINIMUM_LIQUID_SHARE > 100 or ISSUER_LIMIT > 100:
        raise ValueError('Percentage limits cannot exceed 100')
    return QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100


def evaluate(weights):
    """Compute all five rules without mutating inputs; retain negative weights."""
    minimum = reserve_minimum()
    if set(weights) != set(HOLDINGS):
        raise ValueError('Candidate must specify exactly the holdings in HOLDINGS')
    if not all(isinstance(w, (int, float)) and isfinite(w) for w in weights.values()):
        raise ValueError('Weights must be finite numbers')
    companies = {}
    reserve = liquid = 0.0
    for holding, weight in weights.items():
        info = HOLDINGS[holding]
        if not isfinite(info['days']) or info['days'] < 0:
            raise ValueError('Redemption days must be finite and nonnegative')
        if info['reserve']:
            reserve += weight
        if info['days'] <= LIQUIDITY_WINDOW:
            liquid += weight
        if info['issuer'] not in EXEMPT_ISSUERS:
            companies[info['issuer']] = companies.get(info['issuer'], 0.0) + weight
    total, lowest = sum(weights.values()), min(weights.values())
    largest = max([0.0, *companies.values()])
    return [
        ('Weights sum to 100', total, abs(total - 100) <= TOLERANCE),
        ('Long-only (lowest weight)', lowest, lowest >= -TOLERANCE),
        (f'Reserve >= {minimum:.1f}%', reserve, reserve >= minimum - TOLERANCE),
        (f'Redeemable in {LIQUIDITY_WINDOW:g} days >= {MINIMUM_LIQUID_SHARE:g}%',
         liquid, liquid >= MINIMUM_LIQUID_SHARE - TOLERANCE),
        (f'Largest single company <= {ISSUER_LIMIT:g}%', largest,
         largest <= ISSUER_LIMIT + TOLERANCE),
    ]


def report(candidates=None):
    lines = [f'Reserve minimum: {reserve_minimum():.1f}%']
    for name, weights in (CANDIDATES if candidates is None else candidates).items():
        rules = evaluate(weights)
        lines.extend(['', f'Candidate {name}'])
        lines.extend(f'{label}: {value:.1f}% {"pass" if passed else "FAIL"}'
                     for label, value, passed in rules)
        lines.append('Calendar-year loss: requires CIO clarification')
        failures = sum(not passed for _, _, passed in rules)
        lines.append('passes every checkable rule' if not failures else f'fails {failures} rule(s)')
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    print(report(), end='')
