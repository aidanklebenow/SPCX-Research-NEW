# Visa: five-year FCFF DCF and reverse DCF

Research date: September 10, 2026. Comparison price: **$367.39**, September 9 closing price, verified on [Visa's stock page](https://investor.visa.com/stock-information/quote-chart/default.aspx). This is a dated comparison, not a live quote.

**Base estimate: $250.92 per Class A equivalent share; WAIT for a new purchase under the stated assumptions.** This estimate uses actual reported fundamentals and explicitly modeled assumptions. It does not reuse the hypothetical $100M classroom FCFF or SpaceX forecasts.

## 1. Establish the starting cash flow

All amounts below are USD millions. TTM means trailing twelve months ending June 30, 2026. Calculate each TTM item as FY2025 + nine months FY2026 − nine months FY2025, avoiding double counting.

| Reported input | FY2025 | 9M FY2026 | 9M FY2025 | Calculated TTM |
|---|---:|---:|---:|---:|
| Revenue | 40,000 | 33,764 | 29,276 | 44,488 |
| GAAP operating income (EBIT) | 23,994 | 20,848 | 17,846 | 26,996 |
| Depreciation and amortization | 1,220 | 1,026 | 904 | 1,342 |
| Property, equipment and technology purchases | 1,482 | 1,178 | 1,093 | 1,567 |
| Operating cash flow | 23,059 | 16,342 | 16,821 | 22,580 |

Sources: [FY2025 10-K, statements of operations and cash flows](https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm); [June 2026 10-Q, corresponding statements](https://www.sec.gov/Archives/edgar/data/1403161/000140316126000104/v-20260630.htm).

FCFF = EBIT × (1 − operating tax rate) + D&A − capital expenditures − increase in operating working capital.

Two normalization assumptions are necessary:

- Operating tax rate: **20%**, an analyst assumption, not the reported effective rate. It avoids extrapolating temporary tax benefits.
- Annual working-capital investment: **1% of TTM revenue = $444.88M**. This is an assumed annual cash outflow, not an observed balance or 1% of revenue growth. It smooths volatile operating cash movements and must be challenged in a fuller model.

Starting normalized FCFF = 26,996 × 80% + 1,342 − 1,567 − 444.88 = **$20,926.92M**.

This is **normalized FCFF, not reported FCFF**. GAAP operating income retains stock compensation, litigation provisions and other operating charges; none is arbitrarily added back. Only D&A is added back. Historical operating cash flow minus capex is $21,013M, a useful reasonableness comparison but not identical to unlevered FCFF: it includes financing-related interest, nonoperating cash effects and actual working-capital timing. The forecast does not simply label CFO minus capex as FCFF.

## 2. Forecast five years

Assume FCFF grows **12%, 11%, 10%, 9%, and 8%**. These are analyst estimates reflecting expansion followed by maturation, not management guidance. The recent revenue trend provides context, but revenue growth does not guarantee equal cash-flow growth. This aggregate FCFF model assumes margins and reinvestment allow the stated cash growth; a detailed operating model is the next refinement.

Years 1–5 are successive twelve-month forecast intervals from the valuation date, discounted at year-end. TTM June fundamentals serve as the starting proxy. These intervals are not labeled as Visa fiscal years; no separate July–September stub forecast is included.

| Year | FCFF growth | FCFF ($M) | Present value at 9% ($M) |
|---|---:|---:|---:|
| 1 | 12% | 23,438.15 | 21,502.89 |
| 2 | 11% | 26,016.35 | 21,897.44 |
| 3 | 10% | 28,617.98 | 22,098.33 |
| 4 | 9% | 31,193.60 | 22,098.33 |
| 5 | 8% | 33,689.09 | 21,895.60 |
| Total present value | | | **109,492.59** |

Formula: FCFF_t = FCFF_(t−1) × (1 + growth_t); PV_t = FCFF_t / (1 + WACC)^t. Starting FCFF is Year 0 and is not added separately.

## 3. WACC and terminal value

**WACC = 9%** is a modeling assumption, tested at 8–10%; it is not a measured current market WACC. A full estimate would require a dated risk-free rate, equity risk premium, beta, borrowing cost and financing weights. No claim is made that these inputs have been empirically estimated here.

**Terminal growth = 3%** is assumed indefinitely after Year 5. It is lower than explicit growth and below WACC. Maintaining this growth requires continuing reinvestment; the terminal FCFF assumption treats those needs as already embedded in net cash flow, rather than assuming capex disappears.

- Year 6 FCFF = Year 5 FCFF × 1.03 = **$34,699.76M**.
- Terminal value at end of Year 5 = FCFF_6 / (0.09 − 0.03) = **$578,329.34M**.
- PV terminal = terminal value / 1.09⁵ = **$375,874.39M**.
- Enterprise value = PV explicit cash flows + PV terminal = **$485,366.98M**.

Terminal value contributes **77.4%** of enterprise value. This concentration makes long-run assumptions consequential; the price estimate is not precise merely because the calculation produces cents.

## 4. Convert business value into value per share

| Bridge | $M, except shares and price |
|---|---:|
| Enterprise value | 485,366.98 |
| Cash and equivalents | +12,359.00 |
| Liquid debt securities | +1,137.00 |
| Assumed operating cash reserve | −3,000.00 |
| Debt principal, including commercial paper | −24,131.00 |
| Equity value | **471,731.98** |
| As-converted Class A shares, millions | **1,880** |
| Value per equivalent share | **$250.92** |

Balance-sheet and share inputs are June 30, 2026: [10-Q balance sheet and Notes 6, 8, 11 and 13](https://www.sec.gov/Archives/edgar/data/1403161/000140316126000104/v-20260630.htm). The $3B cash reserve is an analyst assumption, not a disclosed requirement. Restricted litigation cash and customer collateral are excluded. Only liquid debt securities are added; other investments are omitted rather than automatically treated as freely available cash.

Use as-converted shares to reflect all participating classes and preferred conversion claims; do not subtract preferred book equity again. The period-end count is a proxy, not a complete September diluted-share reconciliation. Employee equivalents, subsequent buybacks and conversion changes can alter it. Stock compensation remains expensed; no automatic forecast buyback uplift is assumed.

Debt principal is a conservative proxy for market value. Operating leases remain operating expenses, so no separate lease-debt subtraction is made. Existing and prospective litigation payments are not individually scheduled. Retaining litigation expense in EBIT does not fully resolve payment timing or escrow/conversion mechanics. June cash/debt may have changed before the valuation date.

At unchanged enterprise value, setting the operating reserve to $0 increases value by $1.60/share; setting it to $6B reduces value by $1.60/share. Every additional $1B equity claim reduces value by approximately $0.53/share. Raising the normalized working-capital cash outflow from 1% to 2% of TTM revenue lowers starting FCFF by $444.88M; the Python inputs allow that assumption to be changed.

## 5. Scenarios and sensitivity

Scenarios are alternative assumptions, not probabilities or confidence intervals. Each retains the same starting normalized FCFF and equity bridge.

| Scenario | FCFF growth, Years 1–5 | WACC | Terminal growth | Value/share |
|---|---|---:|---:|---:|
| Bear | 7%, 6%, 5%, 4%, 3% | 10% | 2.5% | $162.71 |
| Base | 12%, 11%, 10%, 9%, 8% | 9% | 3% | $250.92 |
| Bull | 15%, 14%, 13%, 12%, 10% | 8% | 3.5% | $375.62 |

Sensitivity below holds the base five-year growth path constant:

| WACC / terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 8% | $259.96 | $303.87 | $369.72 |
| 9% | $220.70 | $250.92 | $293.24 |
| 10% | $191.28 | $213.14 | $242.28 |

The market comparison exceeds base value by about 46%; equivalently, base value is **31.7% below the market price**. The bullish case offers only about 2% upside. A discretionary 20% margin of safety below base value gives a **$200.74** review threshold; this is a model-based reference, not an automatic order or price forecast.

## 6. Reverse DCF: what growth is priced in?

Holding starting FCFF, 9% WACC, 3% terminal growth and the equity bridge fixed, Python solves for a constant annual FCFF growth rate that produces **$367.39/share**.

**Required five-year FCFF CAGR: 19.37%.** This is FCFF growth, not revenue or EPS growth. It is an inference conditional on the other assumptions, not proof of investors' exact expectations. A lower WACC, higher terminal growth or stronger starting cash flow can also explain the same price.

## 7. Reproduce and interpret

From the AidanKlebenow course folder:

```bash
python3 Visa/visa_dcf.py
```

The script uses only Python's standard library, reads `visa_inputs.json`, and prints the forecasts, scenarios, sensitivity and reverse DCF. It does not change files or refresh the market price. Calculations retain full precision; displayed amounts are rounded.

The practical conclusion is **WAIT for a new position under the base case**. Upgrade the evidence by testing normalized cash generation, tax and working-capital assumptions and estimating WACC independently. This model does not establish that a current shareholder must sell.
