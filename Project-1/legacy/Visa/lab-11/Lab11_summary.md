# Lab 11 — Visa operating sensitivity

**Aidan adopted the suggested prediction under revised instructor instructions he reported. Analysis is AI-assisted. A substitute review is included under the instructor accommodation Aidan reported because class ran long.**

Run UTC: 2026-09-29T21:36:49.453024+00:00. The original Lab 10 model is unchanged. All amounts are USD millions except value per share.

## Inputs and ranges

All changes apply to FY2026–FY2030. The entire linked model is rerun from a fresh independent copy each time. Other input rates stay fixed; dollar statement accounts recalculate.

| Driver/scenario | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---:|---:|---:|---:|---:|
| gross_growth / lower | 13.0% | 12.0% | 11.0% | 10.0% | 9.0% |
| gross_growth / base | 15.0% | 14.0% | 13.0% | 12.0% | 11.0% |
| gross_growth / higher | 17.0% | 16.0% | 15.0% | 14.0% | 13.0% |
| incentive_ratio / lower | 27.5% | 27.7% | 27.9% | 28.1% | 28.3% |
| incentive_ratio / base | 28.5% | 28.7% | 28.9% | 29.1% | 29.3% |
| incentive_ratio / higher | 29.5% | 29.7% | 29.9% | 30.1% | 30.3% |

**Revenue growth before client incentives — judgment:** Pre-incentive growth calculated from filings: 10.55% FY2024, 12.20% FY2025, 15.15% nine months FY2026. A +/-2 percentage-point shift tests moderate departures from the approved path; it is not a historical confidence interval or company guidance.

**Client incentives / revenue before incentives — judgment:** Historical ratios calculated from filings rose from 27.36% FY2023 to 28.25% FY2025. +/-1 percentage point tests a meaningful change in partner economics; the stress range is broader than one annual movement, not a probability interval.

[Annual filing](https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm) · [Interim filing](https://www.sec.gov/Archives/edgar/data/1403161/000140316126000104/v-20260630.htm)

## Results and signed changes from base

| Run | FY2030 operating profit | Change | FY2030 FCFE | Change | Value/share | Change |
|---|---:|---:|---:|---:|---:|---:|
| gross_growth_lower | 42,242.58 | -4,034.26 | 32,932.90 | -3,210.41 | 251.89 | -21.87 |
| gross_growth_base | 46,276.85 | +0.00 | 36,143.32 | +0.00 | 273.76 | +0.00 |
| gross_growth_higher | 50,609.70 | +4,332.85 | 39,594.88 | +3,451.57 | 297.18 | +23.42 |
| incentive_ratio_lower | 46,936.00 | +659.15 | 36,634.15 | +490.84 | 277.48 | +3.72 |
| incentive_ratio_base | 46,276.85 | +0.00 | 36,143.32 | +0.00 | 273.76 | +0.00 |
| incentive_ratio_higher | 45,617.70 | -659.15 | 35,652.48 | -490.84 | 270.05 | -3.72 |

## Output spans

| Input | Operating profit span | FCFE span | Value/share span |
|---|---:|---:|---:|
| gross_growth | 8,367.12 | 6,661.98 | 45.29 |
| incentive_ratio | 1,318.30 | 981.68 | 7.43 |

Spans are maximum minus minimum across valid lower/base/higher results. Any incomplete comparison is not ranked. These are effects over the selected ranges, not probabilities or a universal ranking of Visa’s drivers.

## Aidan’s adopted prediction — reconciliation

[Aidan’s adopted prediction and full reconciliation](Lab11_prediction.md)

| Output | Adopted predicted change | Actual change | Actual minus predicted (percentage points) |
|---|---:|---:|---:|
| operating_profit | +9.00% | +9.36% | +0.36 |
| fcfe | +9.00% | +9.55% | +0.55 |
| per_share | +8.00% | +8.55% | +0.55 |

The AI estimate used roughly five years of extra compounding. Differences arise because depreciation depends on earlier PP&E, capex and working capital change with activity, interest is largely fixed, and the valuation discounts different annual cash flows plus a separately normalized terminal value. This explanation is AI-generated, not Aidan’s submitted reflection.

## Interpretation — AI-assisted draft for Aidan to review

Revenue growth is the larger driver **over these ranges** for all three outputs. Its operating-profit span is $8,367.12 million versus $1,318.30 million for incentives; its FCFE span is $6,661.98 million versus $981.68 million. Its value-per-share span is $45.29 versus $7.43, approximately 6.1 times larger.

The reason is compounding: increasing the growth assumption in each of five years raises the revenue base used in the following year. Higher revenue flows into operating profit, net income and FCFE after taxes and reinvestment. For the higher-growth case, FY2030 operating profit increases from $46,276.85 million to $50,609.70 million and FCFE increases from $36,143.32 million to $39,594.88 million. Discounting the higher cash flows and normalized terminal value raises value per share from $273.76 to $297.18.

Client incentives are payments or discounts to Visa’s clients that reduce the revenue Visa keeps. Raising the incentive ratio reduces retained revenue, earnings and cash flow. However, this model also reduces many operating expenses when net revenue falls because it holds expense-to-net-revenue ratios fixed. That partially offsets the damage from incentives. Actual costs might not fall as readily, so the model may understate that risk. Changes in incentive assets and liabilities also affect when the expense becomes a cash payment.

This ranking is conditional: growth is shifted by ±2 percentage points, while incentives are shifted by ±1 point. Different ranges or cost assumptions could produce a different comparison. The table does not assign probabilities or establish that any scenario will occur.

**Research and valuation implication:** The sensitivity results alone do not justify replacing the $273.76 base estimate with the $297.18 higher-growth estimate. They show how dependent the valuation is on sustained growth. A reasonable next research priority is to assess whether transaction activity, cross-border activity and value-added services can support the assumed growth path, then check incentive pressure and the flexibility of operating costs. This is a proposed research conclusion for Aidan to assess, not a new factual forecast or current trading recommendation.

**Reflection prompt:** One notable result is the much smaller incentive sensitivity despite incentives being a major business expense. The differing ranges, five-year growth compounding and assumed cost response explain why size of an expense alone does not determine sensitivity. Aidan should state whether this was personally surprising rather than treat this draft as a record of his reaction.

## Sensitivity concepts

- One-at-a-time sensitivity changes one independent assumption path while keeping other independent inputs at base; linked statements still recalculate.
- A wider input range generally produces a larger output span, so rankings depend on the tested ranges.
- A sensitivity table shows conditional outcomes, not their likelihood. No probability distribution was estimated here.

## Verification and valuation limitations

Restored base: **PASS**, largest difference across all statement values and displayed outputs = 0.0; tolerance = 1e-06 in each output’s units. Base inputs are unchanged. Each changed run alters exactly one independent assumption path.

Full inputs, signed statement details, check blocks and base restoration are in [Lab11_output.txt](Lab11_output.txt) . Negative cash flows are never dropped. If any year has negative FCFE, this runner marks value unavailable instead of invoking the inherited positive-only valuation convention. Operating outputs remain available if accounting/financing checks pass; invalid runs are flagged and excluded from ranking.

Per-share values remain conditional teaching-model values at the September 30, 2025 discount anchor. Fixed opening shares, simplified costs/financing and the abrupt 3% terminal regime remain unchanged. No current market price or current investment recommendation is inferred.

## Substitute review

Aidan reported that the instructor allowed a substitute for the partner exchange because class ran longer than expected. The following AI-assisted question, response and check document that substitute; they do not represent a live exchange or a check of another student’s model.

**Review question:** Why does revenue growth have a larger effect on Visa’s valuation than client incentives, and could the selected ranges explain the difference?

**Response:** Revenue growth compounds over the five forecast years. Over the tested ranges, it creates a $45.29 value-per-share spread, compared with $7.43 for incentives. However, growth changes by ±2 percentage points each year and incentives by ±1 point, so the ranking depends partly on those choices. The model also ties many operating expenses to net revenue, which partially offsets the effect of higher incentives. The result supports researching growth sustainability first, but does not mean incentives are unimportant or that growth will always be the larger driver.

**Arithmetic and input check:** In the higher-growth case, value per share increases from $273.76 to $297.18: $297.18 − $273.76 = **+$23.42 per share**. The annual pre-incentive growth path changes from 15%, 14%, 13%, 12%, 11% to 17%, 16%, 15%, 14%, 13%. The incentive path stays at 28.5%, 28.7%, 28.9%, 29.1%, 29.3%, and all other independent assumptions remain at base. Full linked statements recalculate, all accounting/financing checks pass, and the restored base matches exactly.

**Mechanism and comparison check:** Higher growth raises revenue, operating profit and FCFE after taxes and reinvestment. Another company could have a different main driver because of its cost structure, capital needs and selected input ranges. No other student’s model was examined, so no numerical cross-company comparison is claimed.

**Reflection:** The smaller incentive effect is notable because incentives are a substantial expense. Its size reflects both the narrower tested range and the modeled operating-cost response. Sensitivity results describe conditional outcomes, not probabilities; they do not by themselves justify replacing the base valuation with the higher-growth case.

## Submission package and status

The three reading files are this summary, [Lab11_prediction.md](Lab11_prediction.md), and [Lab11_output.txt](Lab11_output.txt). They contain the ranges, results, visible checks and prediction reconciliation without requiring a reader to run code or open other local files. The Python engine, inputs, tests and machine-readable results remain saved locally as supporting work.

The numerical analysis, prediction reconciliation, interpretation draft and substitute review are included. The prediction and substitute review follow the instructor accommodations Aidan reported. Upload and submission have not been performed.

Local maintenance note: the existing sensitivity runner generates a summary. Preserve this edited submission summary before rerunning that script so review and partner notes are not overwritten.
