# Lab 14 — Portfolio Baselines

Aidan Klebenow | FIN 43900 | October 20, 2026

## Question and inputs

What does each simple portfolio earn and risk, and does any meet the Meridian mandate?

The engine uses the course-authored training inputs, not market estimates:

| Investment vehicle | Expected annual return | Annual volatility |
|---|---:|---:|
| Treasury bills | 3.5% | 0.5% |
| Treasury 10-year note | 4.3% | 7.0% |
| Investment-grade bond fund | 5.0% | 6.0% |
| Global equity index fund | 8.0% | 16.0% |

| Correlation | Bills | 10-year | IG bonds | Equity |
|---|---:|---:|---:|---:|
| Bills | 1.00 | 0.10 | 0.05 | 0.00 |
| 10-year | 0.10 | 1.00 | 0.80 | -0.10 |
| IG bonds | 0.05 | 0.80 | 1.00 | 0.25 |
| Equity | 0.00 | -0.10 | 0.25 | 1.00 |

The expected-return objective is 6.5%: the labelled CPI estimate of 2.5% plus four percentage points. Bills and the 10-year Treasury note are reserve-eligible in this case.

## Run the files

Download portfolio.py and mandate.py into the same folder. In Terminal, navigate to that folder and run:

```bash
python3 portfolio.py
python3 mandate.py
```

Both files use only the Python standard library. Each calculation has a reusable function. Returns, volatilities and calculation weights use decimals internally. The optional CUSTOM_WEIGHTS_PERCENT section accepts percentages; set SHOW_CUSTOM_PORTFOLIO to True to display a fourth experimental portfolio. It is False for the required three-baseline output.

## Computed results

| Portfolio | Bills / 10-year / IG / equity weights (%) | Return | Volatility | Reserve-eligible | Meets 6.5%? |
|---|---|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | Yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | No |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | No |

Inverse-volatility weights total 99.9% when rounded for display; unrounded weights sum to 100%.

None meets both the expected-return objective and all currently checkable mandate rules. The benchmark meets the return objective but fails reserves. Equal weight and inverse volatility pass the checkable rules but miss the return objective. Expected return does not guarantee a realized return or establish achievement of the rolling five-year net objective.

## Validation and benchmark mandate check

The known answers match. Lab14_validation.txt records actual script runs and these checks:

- Changing both IG-equity correlations from 0.25 to 0.50 raises benchmark volatility from 10.46% to 11.00%. Original inputs were restored.
- Setting correlation to 1.3 makes the program refuse to run with a clear range error.
- Editing only one side of the table makes the program refuse to run with a symmetry error.
- All four automated Lab 14 tests pass.
- Candidate E in mandate.py is exactly 40% IG bonds and 60% equity. It fails only the reserve check among the five implemented checks.

The reserve minimum is 4 × $0.75 million / $100 million = 3.0%. Candidate E holds 0.0% in eligible reserves. Its weights sum to 100%, it is long-only, 100% is redeemable within five business days, and the diversified funds do not breach the single-company rule under the case's exemptions. The calendar-year loss rule still requires CIO clarification; turnover cannot be assessed without prior holdings.

An additional weight experiment moved from 40% bonds / 60% equity to 60% bonds / 40% equity. Expected return fell from 6.80% to 6.20%, and volatility fell from 10.46% to 8.09%. It still had zero eligible reserves. The original benchmark was restored.

## Diversification and hand calculation

Diversification means combining different investments so portfolio performance is not dependent on one investment's movements. When correlation is below +1, returns do not move perfectly together; this reduces variance relative to a perfectly positively correlated mix at the same weights and individual volatilities.

For the benchmark, using percentage units:

```text
Expected return = 0.4 × 5 + 0.6 × 8 = 6.80%
Variance = (0.4 × 6)^2 + (0.6 × 16)^2
           + 2 × 0.4 × 0.6 × 6 × 16 × 0.25
         = 5.76 + 92.16 + 11.52
         = 109.44
Volatility = sqrt(109.44) = 10.46%
```

If correlation were +1, volatility would be 0.4 × 6 + 0.6 × 16 = 12.00%. The actual 10.46% therefore demonstrates diversification. This particular portfolio is less volatile than equity alone (16%) but more volatile than bonds alone (6%); it is not an example of being less risky than both assets. Volatility measures variability, not the maximum possible loss.

## Code logic

The covariance matrix entry for vehicles i and j is their correlation multiplied by their two volatilities. The diagonal holds individual variances because self-correlation is one.

The portfolio variance calculation is:

```python
variance = sum(weights[i] * weights[j] * covariance[i][j]
               for i in range(len(weights)) for j in range(len(weights)))
```

Each pair's covariance is scaled by both allocation weights. The loops include all pairs, including both (i,j) and (j,i), which produces the factor of two in the two-asset cross term. Taking the square root converts variance into volatility. Omitting the cross term would incorrectly produce about 9.90% for the benchmark.

Expected return is the sum of weight times expected return for each vehicle. Reserve weight adds only the two eligible Treasury vehicles. Objective attainment is evaluated separately from mandate compliance.

## Reflection: inverse volatility

Inverse volatility assigns each vehicle a weight proportional to 1 divided by its volatility. Bills have only 0.5% supplied volatility, making their reciprocal much larger than the other vehicles' reciprocals. After normalizing to 100%, bills receive 84.3%. The rule chooses weights using individual volatilities; it does not use expected returns or correlations to choose weights. This produces low volatility but falls short of the return objective.

## Reflection: which baseline to show the CIO first

An AI-assisted proposed choice for student review is the benchmark. It is the client's existing reference and immediately reveals a concrete policy conflict: its 6.80% expected return meets the goal, but its 0% reserves violate the 3% minimum. Equal weight and inverse volatility then show how reducing volatility can also sacrifice expected return. This comparison motivates searching for a feasible allocation rather than assuming any baseline is suitable. The student must decide whether to adopt this judgment and be able to explain it.

## Participation and AI-use record

The student reports running both Python programs independently and swapping laptops with the partner. AI assisted with code, explanations, validation, and this write-up. The output evidence establishes technical behavior; it does not establish completion of the no-AI explanations or the partner's specific break test. No partner question, student quiz answer, or unconfirmed activity has been invented. The AI posed a quiz about the covariance term, but no student answer is recorded in this chat.

## Before Thursday

The assignment also asks for a student-selected universe of three to six funds, with each ticker, name and role, and five years of monthly adjusted closing prices in prices.csv, oldest month first. Record sources and download dates. Final fund choices and price collection remain preparation for Thursday, not completed work in this package.

## Assignment sources

- Lab: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-14-portfolio-baselines.md
- Slides: https://cinderzhang.github.io/FIN43900-Fall2026/lessons/week-09/slides-session-14.html
