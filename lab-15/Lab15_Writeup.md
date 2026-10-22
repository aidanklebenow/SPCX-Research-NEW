# Lab 15 — Results, Explanation, and Student Checkout

Prepared October 22, 2026 with AI assistance. The numerical results below were computed by the student's portfolio engine. Partner observations and the student's final decision remain to be entered personally.

## The decision question

Which mix carries the least risk while meeting the mandate—and does the answer survive a one-point change in one estimate?

## V — Verify the training case

Use Meridian, objective **6.5%**, reserve minimum **3%**, with bills and the 10-year note checked as reserve-eligible.

| Scenario | Bills | 10-year note | IG bonds | Equity | Return estimate | Volatility |
|---|---:|---:|---:|---:|---:|---:|
| As loaded | 0% | 20% | 25% | 55% | 6.51% | 9.44% |
| Equity return estimate 8% → 7% | 0% | 10% | 10% | 80% | 6.53% | 12.94% |
| IG–equity correlation 0.25 → 0.50, original returns | 0% | 40% | 0% | 60% | 6.52% | 9.73% |

The first stress moves equity by **25 percentage points**. Both return and risk are recalculated; the app does not type these answers into the interface. Tests use a copy of the correlation table, leaving the original at 0.25. For your own engine proof, restore equity to 8%, change both IG–equity correlation cells to 0.50 in `portfolio.py`, save and rerun the page, then restore 0.25.

Lab 14's printed report remains unchanged byte for byte.

## Your universe — Five ETFs

Choose **My five ETFs** in the app. For this analysis, use the Lab 13 draft's **7.5% objective**, **10% reserve minimum**, and **only SGOV** as reserve-eligible. The sidebar's draft preset fills the two numbers; confirm eligibility yourself.

| Ticker | Role | All-month annual return estimate | All-month annual volatility |
|---|---|---:|---:|
| SGOV | Short Treasury reserves | 3.72% | 0.50% |
| IEF | Intermediate Treasuries | -1.79% | 7.65% |
| LQD | Investment-grade corporate bonds | -0.81% | 9.79% |
| VTI | U.S. equities | 13.13% | 15.94% |
| VXUS | International equities | 10.12% | 15.17% |

These are arithmetic monthly mean × 12 and sample monthly standard deviation × √12, based on Yahoo adjusted prices downloaded October 22, 2026. Historical estimates are not forecasts. The table rounds for readability; the engine retains full precision.

### Five-year window versus last 36 monthly returns

The full dataset has 61 month-end prices from **September 30, 2021 to September 30, 2026**, creating 60 monthly returns. The final 36 monthly returns use 37 prices from **September 29, 2023 to September 30, 2026**.

| Scenario | SGOV | IEF | LQD | VTI | VXUS | Return estimate | Volatility | Reserves |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| All 60 returns | 55% | 0% | 0% | 30% | 15% | 7.50% | 6.80% | 55% |
| Last 36 returns | 80% | 0% | 0% | 10% | 10% | 7.58% | 2.32% | 80% |

**Largest change: 25 percentage points in SGOV**, from 55% to 80%. VTI drops 20 points and VXUS drops 5 points.

Interpretation: the shorter window estimates stronger equity returns and lower volatility than the full window. Less equity is then needed to clear the fixed objective. It also excludes the 2022 selloff. This changes the sample being measured; it does not establish that future risk is lower. The zero weights in IEF and LQD are results under these particular estimates, not a claim that either ETF is inherently unsuitable.

### Separate one-point stress on the five-year data

Switch back to all months. Reduce only VTI's expected annual return by **1.00 percentage point**, from the underlying **13.1342275% to 12.1342275%**. Other return estimates, volatility estimates, correlations, objective, and reserve rule stay fixed. The visible inputs round to two decimal places.

| Scenario | SGOV | IEF | LQD | VTI | VXUS | Return estimate | Volatility |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original full-window inputs | 55% | 0% | 0% | 30% | 15% | 7.50% | 6.80% |
| VTI estimate minus one point | 55% | 0% | 0% | 45% | 0% | 7.50% | 7.22% |

**Largest change: 15 percentage points.** VTI rises 15 points and VXUS falls 15 points. The return estimate still clears the objective at unrounded precision. The optimizer needs more VTI after its estimate falls, and the allocation satisfying the objective changes abruptly on the 5-point grid. This was an AI-assisted technical stress test, not a substitute for your partner's independent attack.

## Explain the search function to a partner

Open `lowest_risk_mix()` in `portfolio.py`. Use these notes to study before the required no-AI explanation.

| Code step | What I should be able to explain |
|---|---|
| `covariance_matrix(...)` | Converts each correlation and pair of asset volatilities into the covariance inputs needed for portfolio risk. |
| Input checks | Rejects invalid objectives, reserve minimums, and asset names. |
| `allocations(20, len(vehicles))` | Divides twenty 5% units among the assets. Every generated mix is nonnegative and totals 100%. |
| `best = None` | No qualifying allocation has been found yet. |
| `expected_return(...)` | Multiplies each weight by its asset's return estimate and adds the contributions. |
| Reserve sum | Adds the weights only for assets selected as eligible reserves. |
| `if ... continue` | Skips an allocation that misses either the return objective or reserve floor. |
| `portfolio_volatility(...)` | Uses the covariance matrix and allocation to calculate risk, including how the assets move together. |
| `if best is None or ...` | Saves the first qualifying mix, then replaces it whenever a lower-volatility qualifying mix appears. |
| `return best` | Returns the minimum-volatility grid mix, or `None` if none qualifies. |

The manual weight dials use the same return and risk functions, but they do not perform the optimizer's search. They let the user test a chosen allocation while maintaining a total of 100%.

Partner's code question: **[enter after the exercise]**

My answer from the code: **[enter in your own words]**

## Partner attack — Complete personally

Have your partner choose the estimate they distrust, change it in your app, and read the resulting mix aloud. Record both inputs and outputs. Do not describe the technical stress above as an action your partner performed unless they actually do it.

1. My partner changed **[asset]** from **[old estimate]%** to **[new estimate]%**, moving the allocation from **[old weights]** to **[new weights]**, with a largest change of **[number]** points.
2. I would **[response]** because **[what that sensitivity implies for the mandate]**.

## Your call — Draft to review, not a completed student decision

**Suggested draft:** “Pilot the mix as a research starting point: the 36-month window shifts the largest allocation by 25 points, while a one-point lower VTI return estimate shifts two allocations by 15 points. I would consider adopting it only after confirming the reserve definition and remaining mandate rules, resolving the loss requirement, and finding the allocation sufficiently robust across defensible estimation choices.”

Your own final choice: **[adopt / pilot / reject]**

Your own reason and condition: **[enter after reviewing the stress results]**

The app enforces a return estimate floor and a reserve allocation floor. It does not enforce the separate issuer-concentration rule, guarantee zero losses, or directly establish achievement of a compounded five-year net return target. Investor taxes, advisory fees, and trading costs are not included. Confirm the scope of those rules before treating the mix as mandate-compliant.

## Estimation risk — Learn and reflect

**What is estimation risk?** Risk that the return, volatility, or correlation inputs differ from the future relationships that actually occur.

**Why can small changes cause large moves?** The optimizer selects whichever allocation just satisfies the rules at the lowest estimated risk. A small input change can make one mix fail or make another mix the new minimum. The selected allocation can jump even when the input moves only slightly.

**Your own example:** A one-point lower VTI estimate replaces the full-window 30% VTI / 15% VXUS equity split with 45% VTI / 0% VXUS. The allocation is sensitive to relative return estimates.

**Explain personally:** Why did the window change move so much into SGOV? What additional evidence would you need before adopting the answer?

## App features and quote timing

Dashboard includes paired optimized allocations, comparison bars, manual weight sliders, a risk–return chart, and adjusted-price growth charts for uploaded or bundled ETFs. **Market quotes** provides the latest available Yahoo regular-session prices and an intraday chart. **How it works** explains the controls and vocabulary. **Lab notebook** lets you record your own partner observations and decision, then download the current session as Markdown.

Free quotes refresh every 60 seconds while the quote page or dashboard is open. Trade time is shown separately from fetch time; after hours, an older closing trade remains visible. Yahoo can delay data or reject requests. Unavailable data is labeled instead of being fabricated. Market quotes never silently overwrite the fixed monthly estimation sample.

Light and dark themes use Streamlit's native text, panel, axis, and legend colors. Change the theme through the upper-right menu → Settings → Theme.

## Final checkout

- [ ] Personally rerun both Meridian cases and the correlation change, restoring the original inputs afterward.
- [ ] Compare the flowchart with your own paper drawing.
- [ ] Personally run the full and 36-month ETF cases and explain the largest change.
- [ ] Explain the search function without AI and record your partner's question.
- [ ] Complete the partner attack and replace its placeholders.
- [ ] Write your own allocation decision and condition; review the suggested draft first.
- [ ] Open the rendered GitHub `lab-15` folder and check the files before submitting its URL in the Lab 15 quiz.

No partner participation, final student judgment, or Brightspace submission is claimed by this prepared guide.
