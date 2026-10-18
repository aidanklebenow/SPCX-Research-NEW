# Visa Inc. — Lab 06: Sensitivity and Reverse DCF

**Valuation date:** September 10, 2026. **Market reference:** $367.21 per Class A share, regular-session close at 16:00 EDT (20:00 UTC), independently displayed by [Visa investor relations](https://investor.visa.com/stock-information/quote-chart/default.aspx) and [StockAnalysis price history](https://stockanalysis.com/stocks/v/history/). Retrieved September 10, 2026.

**Result:** Base value is **$217.42 per diluted Class A-equivalent share**. The valid sensitivity-corner range is **$171.86–$299.05**. The prescribed reverse-DCF search returns **No solution in the specified bracket**: even a +10-percentage-point shift values the shares at $326.01, below the target.

## Scope and existing files

This implements the five-year [Lab 06 requirements](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-03/lab-06-sensitivity-and-reverse-dcf.md), superseding the interrupted request for a separate ten-year model. It solves a uniform shift in **FCFF growth**, not revenue growth.

The course folder, Downloads, Documents and Desktop were inspected before editing. No original file named `dcf.py` or `Visa_Reverse_DCF.md` was found. The available `visa_dcf.py`, `visa_inputs.json`, and earlier Visa reports were read. Those files are preserved. Therefore byte-for-byte preservation of a missing file cannot be claimed. The new `dcf.py` restores the twelve-output contract from [Lab 05](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-03/lab-05-dcf-build.md), with its editable inputs at the top. No additional calculation script was created for Lab 06.

The ZIP `/Users/aidanklebenow/Downloads/0001403161-26-000104-xbrl.zip` was inspected for unsafe paths, symlinks and unreasonable decompression sizes before extracting data-only copies. No document code was executed. The original archive was preserved; temporary extraction copies were removed to recover disk space. Its SHA-256 is `f15092a4aa6410612118948661254ce21f9e0a632e858746820bbda5dd7de5c6`.

The main document identifies VISA INC., Form 10-Q, fiscal Q3 2026, quarter ended June 30, 2026. The nine-month period starts October 1, 2025. SEC lists accession **0001403161-26-000104**, filing date **July 29, 2026**, and acceptance July 28 at 18:08:12. [SEC filing index](https://www.sec.gov/Archives/edgar/data/1403161/000140316126000104/0001403161-26-000104-index.htm)

## Sourced Visa inputs

USD M means millions of U.S. dollars. Share amounts are millions of Class A-equivalent shares. Forecast years are successive annual periods, not labeled fiscal-year forecasts. All analyst estimates below are dated September 10, 2026.

| Input | Value | Unit | Period / as-of | Classification and exact locator |
|---|---:|---|---|---|
| Operating cash flow | 23,059 / 16,342 / 16,821 | USD M | FY2025 / 9M2026 / 9M2025 | Reported; [10-K](https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm), cash-flow statement p.65, and [10-Q](https://www.sec.gov/Archives/edgar/data/1403161/000140316126000104/v-20260630.htm), cash-flow statement pp.9–10; net operating cash row |
| Interest paid on debt | 587 / 600 / 539 | USD M | Same three periods | Reported; same filings, supplemental cash-flow disclosures p.65 / p.10; interest payments on debt row |
| Capital expenditures | 1,482 / 1,178 / 1,093 | USD M | Same three periods | Reported; same cash-flow statements, purchases of property, equipment and technology |
| Tax rate for interest adjustment | 20.00 | % | Model date | Estimate; normalized assumption, not reported effective or cash tax rate |
| Starting FCFF | 21,531.40 | USD M annually | LTM ended June 30, 2026 | Calculated below using the prescribed lab formula |
| Five growth rates | 12 / 11 / 10 / 9 / 8 | % annually | Forecast Years 1–5 | Estimates retained from the earlier Visa forecast; context: [Q3 release](https://www.sec.gov/Archives/edgar/data/1403161/000140316126000103/q32026earningsrelease.htm), Key Business Drivers and Financial Highlights |
| WACC | 10.00 | % annually | Model date | Rounded estimate; build-up below |
| Terminal growth | 3.00 | % annually | After Year 5 indefinitely | Estimate of sustainable nominal cash-flow growth; not Visa guidance |
| Cash and equivalents | 12,359 | USD M | June 30, 2026 | Reported; [10-Q](https://www.sec.gov/Archives/edgar/data/1403161/000140316126000104/v-20260630.htm), balance sheet p.2 |
| Liquid debt securities | 1,137 | USD M | June 30, 2026 | Reported; same 10-Q, Note 6, available-for-sale debt securities table p.16 |
| Operating cash reserve | 3,000 | USD M | Model date | Estimate; no claim that this is a disclosed required reserve |
| Nonoperating cash input | 10,496 | USD M | June balances, model adjustment | Calculated: 12,359 + 1,137 − 3,000 |
| Debt principal | 24,131 | USD M | June 30, 2026 | Reported; same 10-Q, Note 8, debt table p.18; includes commercial paper |
| Diluted shares | 1,898 | Million equivalent shares | Three months ended June 30, 2026 | Reported; same 10-Q, diluted Class A EPS denominator and Note 13, pp.23–24 |
| Target price | 367.21 | USD/share | September 10, 2026, 16:00 EDT | Market input; Visa IR and independent price-history link above |

Current and prior-YTD cash flow and interest were checked against the local inline XBRL contexts `c-1` and `c-26`. Operating cash uses `us-gaap:NetCashProvidedByUsedInOperatingActivities` and interest uses `us-gaap:InterestPaidNet`; USD scale is 6. Diluted shares use `us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding`, Class A context `c-27`, scale 6. These tags corroborate the displayed tables; they are not independent economic estimates.

## Starting FCFF: period reconciliation

The latest quarter alone is not treated as an annual cash flow:

**LTM = FY2025 + nine months FY2026 − nine months FY2025.**

| Item | FY2025 | +9M2026 | −9M2025 | LTM USD M |
|---|---:|---:|---:|---:|
| Operating cash flow | 23,059.00 | 16,342.00 | 16,821.00 | 22,580.00 |
| Interest paid | 587.00 | 600.00 | 539.00 | 648.00 |
| Capital expenditures | 1,482.00 | 1,178.00 | 1,093.00 | 1,567.00 |

Sources: cash-flow and supplemental disclosure rows identified above.

**FCFF = operating cash flow + interest paid × (1 − tax rate) − capital expenditures**

**FCFF = 22,580.00 + 648.00 × 80% − 1,567.00 = $21,531.40M.**

Independent arithmetic check: compute FCFF separately for the three periods using the same 20% rate: 22,046.60 + 15,644.00 − 16,159.20 = 21,531.40.

This is the lab's cash-flow-based FCFF proxy. It retains actual working-capital movements, settlement cash effects, tax timing, client incentives, litigation payments and the cash-flow statement's stock-compensation add-back. It is not a separately normalized NOPAT-based valuation. Interest income and other nonoperating cash effects are not stripped out, so adding nonoperating assets can create some overlap; this is a limitation of applying the required simplified formula. No claim is made that reported cash flows will recur unchanged.

Settlement balances and customer collateral are not added to cash or counted as conventional borrowing. Restricted litigation cash is excluded. Debt principal is a proxy rather than a market-value debt measurement. Acquisitions and buybacks are not deducted as capital expenditures: acquisition payments are separate investing flows and buybacks are financing flows. The fixed diluted denominator does not forecast additional repurchases or employee dilution. These choices keep the bridge transparent, but do not replace a detailed treatment of all future claims.

Visa has multiple participating classes. The chosen EPS denominator already incorporates relevant Class B and C conversions and participating securities, plus employee equivalents; it is not simply the cover-page Class A count. It is a quarterly weighted average, not an exact September spot diluted count. The quarter-end as-converted count is 1,880M in Note 11; the difference from 1,898M primarily reflects timing and denominator conventions. Do not subtract preferred book equity again when its participation is reflected in the equivalent-share denominator.

## WACC and forecast assumptions

The 10% center is an **estimate**, not the classroom rate silently copied onto Visa:

| Component | Value | Classification / source |
|---|---:|---|
| 10-year Treasury rate | 4.95% | Market input; September 10, 2026, 10 Yr column in [Treasury daily nominal par yield table](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026); retrieved September 10 |
| Equity beta | 1.05 | Analyst estimate, not an independently measured regression |
| Equity risk premium | 5.00% | Analyst estimate consistent with the lab's suggested approach |
| Cost of equity | 10.20% | Calculated: 4.95% + 1.05 × 5% |
| Pretax cost of debt | 5.50% | Analyst estimate, not an observed Visa bond yield |
| After-tax cost of debt | 4.40% | Calculated at 20% tax |
| Equity weight / debt weight | 96.65% / 3.35% | Approximation using price × 1,898M shares and debt principal |
| Weighted cost | 10.0059% | Calculated; rounded to **10.00%** for the centered lab grid |

The beta and debt-cost estimates need independent refinement; this is a transparent build-up, not a fully market-estimated WACC.

The 12%→8% FCFF growth path is an estimate. For context, Visa reported Q3 net revenue growth of 14%, payment-volume growth of 10% and processed-transaction growth of 10%. [Q3 release, highlights](https://www.sec.gov/Archives/edgar/data/1403161/000140316126000103/q32026earningsrelease.htm) Revenue growth does not guarantee FCFF growth. No model input was increased to force agreement with the price.

## Five-year base valuation and reasonableness

Each forecast cash flow arrives at year-end. Terminal value is measured at the end of Year 5 and discounted five years, because it represents all subsequent cash flows valued at that date.

| Output | USD M except per-share value |
|---|---:|
| FCFF Year 1 | 24,115.17 |
| FCFF Year 2 | 26,767.84 |
| FCFF Year 3 | 29,444.62 |
| FCFF Year 4 | 32,094.64 |
| FCFF Year 5 | 34,662.21 |
| PV of explicit FCFF | 109,610.81 |
| Terminal value at Year 5 | 510,029.61 |
| PV of terminal value | 316,688.26 |
| Enterprise value | 426,299.07 |
| Add nonoperating cash | 10,496.00 |
| Subtract debt | −24,131.00 |
| Equity value | 412,664.07 |
| Divide by diluted shares, millions | 1,898.00 |
| **Value per diluted share, USD** | **217.42** |

Terminal value represents **74.29%** of enterprise value. Base value / market price = **0.5921×**, inside the lab's 0.5×–2× reasonableness band. Being inside the band is a basic plausibility check, not evidence the assumptions are correct.

The input I distrust most is **the five-year FCFF growth path**: it assumes stable cash conversion despite litigation, incentives and working-capital timing. The estimated WACC is also consequential. The base value is approximately 40.79% below the market price.

## Sensitivity analysis

All inputs except WACC and terminal growth remain fixed. Values are USD per diluted share.

| WACC / terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 9% | 225.12 | 255.93 | 299.05 |
| **10%** | 195.15 | **217.42** | 247.12 |
| 11% | 171.86 | 188.57 | 210.05 |

The center cell is the base case. Value decreases down each valid column and increases across each valid row; assertions verify both directions. The valid corners give **$171.86–$299.05**. Any edited cell with terminal growth ≥ WACC is printed as **Invalid**.

## Reverse DCF

The variable is one uniform shift, s, added to each forecast growth rate. For example, +1 percentage point changes 12% to 13%; it does not multiply 12% by 1.01.

Held fixed: starting FCFF $21,531.40M; 10% WACC; 3% terminal growth; $10,496M nonoperating cash; $24,131M debt; 1,898M diluted shares; five forecast years; year-end discounting; Year-5 terminal timing; and the shape of the original growth path. The underlying CFO, interest, capex, tax and cash-reserve assumptions also stay fixed.

| Search point | Uniform shift | Adjusted annual FCFF growth | Modeled USD/share | Modeled minus target |
|---|---:|---|---:|---:|
| Lower bound, not a solution | −5.00 pp | 7%, 6%, 5%, 4%, 3% | 175.44 | −191.77 |
| Original forecast | 0.00 pp | 12%, 11%, 10%, 9%, 8% | 217.42 | −149.79 |
| Upper bound, not a solution | +10.00 pp | 22%, 21%, 20%, 19%, 18% | 326.01 | −41.20 |
| **Solution** | **Unavailable** | **No solution in the specified bracket** | **Unavailable** | **Unavailable** |

The price is above the entire permitted curve. Under these fixed assumptions, explaining the target would require a shift above +10 points or a change to another assumption. The script does not enlarge the bracket or mislabel a boundary as a solution. It rejects any bracket that produces growth ≤ −100%.

There is no Visa root within the prescribed bracket, so a Visa solution cannot be verified within $0.01. This is the required no-solution outcome, not a numerical failure. The training root and the solver's feasible-target behavior are separately tested. A reverse DCF describes one assumption set consistent with a price, **not proof of mispricing**.

## Graph

The script contains the required matplotlib heatmap and reverse-DCF curve. With these inputs the curve must show the target above the bracket and explicitly state that no solution exists; it must not draw a fictitious solved-shift marker.

**Generation status:** blocked by insufficient disk space when installing matplotlib. The PNG has not yet been generated or visually inspected. This section will be updated only after successful generation.

## Conditional call and monitoring

**Initiate if** the market price is at or below the updated base DCF value, currently approximately **$217.42**, and refreshed filings still support the cash-flow forecast; **otherwise wait**. This is a conditional classroom decision rule, not a claim that the stock must fall to that price.

**Monitor:** the next reported full-year operating cash flow growth rate. Compare it with the prior full-year $23,059M base and investigate growth below 8%, the lowest rate in the forecast path, before retaining that path. Use consistent fiscal periods and identify litigation or tax-timing effects before interpreting the result.

## Validation and reproduction

Before Visa calculations, `training_checks()` verifies:
- All twelve published Lab 05 outputs to within 0.0001 of the rounded reference.
- All nine sensitivity cells at two decimals.
- The $30 training target: shift **+1.7779 percentage points**, with repricing error below $0.01.
- Invalid WACC/terminal cells, invalid growth brackets and unreachable targets.

Training reference grid:

| WACC / terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 9% | 28.60 | 32.94 | 39.02 |
| 10% | 24.36 | 27.50 | 31.69 |
| 11% | 21.06 | 23.41 | 26.44 |

The numerical checks executed successfully. End-to-end chart execution remains blocked by disk space; completion is not claimed.

In the Visa folder, activate the course environment once per terminal session:

```bash
source .venv/bin/activate
```

Once matplotlib is installed, the single lab command is:

```bash
python dcf.py
```

This prints the twelve Visa lines, training evidence, sensitivity and reverse results, and writes `visa_sensitivity_reverse_dcf.png`. No second calculation script is required. The dependency-installation attempt failed with **No space left on device**. No unrelated user files were deleted.

## Formulas and preparation note

FCFF_t = FCFF_(t−1) × (1 + growth_t + s).

PV forecast = sum of FCFF_t / (1 + WACC)^t, t = 1…5.

Terminal value_5 = FCFF_5 × (1 + terminal growth) / (WACC − terminal growth).

Enterprise value = PV forecast + terminal value_5 / (1 + WACC)^5.

Equity value = enterprise value + nonoperating cash − debt.

Per-share value = equity value / diluted Class A-equivalent shares.

Bisection first verifies that the target lies between the endpoint prices; only then does it repeatedly halve the interval until the price residual is below $0.000001.

Prepared with ChatGPT/Codex assistance for Aidan's FIN 43900 work. Sources and calculations were checked by the assistant; Aidan should review and understand the estimates and follow the course's disclosure requirements. No partner contribution or personal verification by Aidan is invented.
