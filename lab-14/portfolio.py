"""Lab 14 portfolio baselines. Standard library only; inputs use decimals.

From this folder: python3 portfolio.py
Course-authored training inputs, not current market estimates.
"""
from math import isclose, isfinite, sqrt

# Order is shared by the correlation matrix and every weight vector.
VEHICLES = [
    ('Treasury bills', 0.035, 0.005),
    ('Treasury 10-year note', 0.043, 0.07),
    ('Investment-grade bond fund', 0.05, 0.06),
    ('Global equity index fund', 0.08, 0.16),
]
CORRELATIONS = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
]
OBJECTIVE = 0.065  # CPI estimate 2.5% + 4 percentage points.
RESERVE_ELIGIBLE = {'Treasury bills', 'Treasury 10-year note'}

# EDIT YOUR WEIGHTS HERE. Enter percentages: 25 means 25%, not 0.25.
# These four numbers must add up to 100. Starting example, not a recommendation.
SHOW_CUSTOM_PORTFOLIO = False  # Set True for experiments; lab prints three baselines.
CUSTOM_WEIGHTS_PERCENT = {
    'Treasury bills': 25.0,
    'Treasury 10-year note': 25.0,
    'Investment-grade bond fund': 25.0,
    'Global equity index fund': 25.0,
}


def custom_weights(vehicles):
    if set(CUSTOM_WEIGHTS_PERCENT) != {name for name, _, _ in vehicles}:
        raise ValueError('Custom weights must name exactly the four investment vehicles.')
    weights = [CUSTOM_WEIGHTS_PERCENT[name] / 100 for name, _, _ in vehicles]
    validate_weights(weights, len(vehicles))
    return weights


def validate_inputs(vehicles, correlations):
    n = len(vehicles)
    if not n or len({v[0] for v in vehicles}) != n:
        raise ValueError('Investment vehicle names must be unique and nonempty.')
    if any(not isfinite(r) or not isfinite(s) or s <= 0 for _, r, s in vehicles):
        raise ValueError('Returns must be finite and volatilities finite and positive.')
    if len(correlations) != n or any(len(row) != n for row in correlations):
        raise ValueError('Correlation table must have one row and column per vehicle.')
    for i in range(n):
        for j in range(n):
            value = correlations[i][j]
            if not isfinite(value) or not -1 <= value <= 1:
                raise ValueError(f'Correlation [{i}][{j}] must be between -1 and 1.')
            if not isclose(value, correlations[j][i], rel_tol=0, abs_tol=1e-12):
                raise ValueError('Correlation table must be symmetric; edit both cells.')
        if not isclose(correlations[i][i], 1, rel_tol=0, abs_tol=1e-12):
            raise ValueError('Each diagonal correlation must equal 1.')


def covariance_matrix(vehicles, correlations):
    validate_inputs(vehicles, correlations)
    return [[correlations[i][j] * vehicles[i][2] * vehicles[j][2]
             for j in range(len(vehicles))] for i in range(len(vehicles))]


def equal_weights(vehicles):
    return [1 / len(vehicles)] * len(vehicles)


def inverse_volatility_weights(vehicles):
    inverse = [1 / volatility for _, _, volatility in vehicles]
    total = sum(inverse)
    return [value / total for value in inverse]


def validate_weights(weights, size):
    if len(weights) != size or any(not isfinite(w) or w < 0 for w in weights):
        raise ValueError('Supply one finite, nonnegative weight per vehicle.')
    if not isclose(sum(weights), 1, rel_tol=0, abs_tol=1e-10):
        raise ValueError('Weights must sum to 1 (100%).')


def expected_return(weights, vehicles):
    validate_weights(weights, len(vehicles))
    return sum(weight * vehicle[1] for weight, vehicle in zip(weights, vehicles))


def portfolio_volatility(weights, covariance):
    validate_weights(weights, len(covariance))
    # Include EVERY pair i,j: diagonal terms are individual variances;
    # off-diagonal terms include each pair twice, providing the familiar 2ab term.
    variance = sum(weights[i] * weights[j] * covariance[i][j]
                   for i in range(len(weights)) for j in range(len(weights)))
    if variance < -1e-12:
        raise ValueError('Negative portfolio variance: check the covariance inputs.')
    return sqrt(max(0, variance))


def reserve_weight(weights, vehicles):
    validate_weights(weights, len(vehicles))
    return sum(w for w, vehicle in zip(weights, vehicles)
               if vehicle[0] in RESERVE_ELIGIBLE)


def meets_objective(portfolio_return, objective):
    return portfolio_return >= objective - 1e-12


def baseline_weights(vehicles):
    benchmark = {'Investment-grade bond fund': 0.4, 'Global equity index fund': 0.6}
    return {'Benchmark': [benchmark.get(name, 0) for name, _, _ in vehicles],
            'Equal weight': equal_weights(vehicles),
            'Inverse volatility': inverse_volatility_weights(vehicles)}


def report():
    covariance = covariance_matrix(VEHICLES, CORRELATIONS)
    lines = ['Lab 14 — course training inputs', f'Objective: {OBJECTIVE:.2%}']
    portfolios = baseline_weights(VEHICLES)
    if SHOW_CUSTOM_PORTFOLIO:
        portfolios['My custom portfolio'] = custom_weights(VEHICLES)
    for name, weights in portfolios.items():
        result = expected_return(weights, VEHICLES)
        lines.extend(['', name])
        lines.extend(f'  {vehicle[0]}: {weight:.1%}'
                     for weight, vehicle in zip(weights, VEHICLES))
        lines.extend([f'  Expected return: {result:.2%}',
                      f'  Volatility: {portfolio_volatility(weights, covariance):.2%}',
                      f'  Reserve-eligible: {reserve_weight(weights, VEHICLES):.1%}',
                      f'  Meets objective: {"yes" if meets_objective(result, OBJECTIVE) else "no"}'])
    return '\n'.join(lines)


if __name__ == '__main__':
    try:
        print(report())
    except ValueError as error:
        raise SystemExit(f'Input error: {error}')
