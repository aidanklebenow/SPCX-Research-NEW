# FIN 43900 — Lab 10: Visa (V)

Prepared September 24, 2026 with Codex assistance. **Working draft for Aidan’s review; not yet ready to claim full lab completion.** The model and source work are complete locally. Aidan reported completing two manual filing checks (FY2025 net income and net property/equipment/technology) and shared a successful model-run transcript. Aidan approved the revised growth path; review of the remaining judgment explanations in his own words and the real partner exchange remain pending. Nothing has been uploaded or submitted.

Assignment: [Lab 10 — Pro-Forma: Your Company Through It](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/lab-10-proforma-your-company.md).

## Start here

The separate Visa engine estimates **$273.76 per opening as-converted share**. Its five projected balance sheets and cash-flow bridges reconcile to zero, and unrestricted cash exceeds the $5,000 million floor. No revolver borrowing is needed in the base case. This is a condensed annual teaching model, anchored September 30, 2025 and researched in September 2026; it is not a current-date investment valuation.

Read [history and sources](Lab10_history_and_sources.md), then the assumptions below, then [the execution and refusal results](Lab10_output.txt). The executable is [Lab10_visa_proforma.py](Lab10_visa_proforma.py), with editable inputs in [Lab10_visa_inputs.json](Lab10_visa_inputs.json). ABG remains in `../lab-09/` and was rerun successfully at $291.75/share without changes.

## D — the company-specific line

Draft explanation to discuss in your own words: **Visa earns network/service fees, and client incentives reduce that revenue; I model those incentives and their payment timing instead of ABG’s inventory and floor-plan borrowing.**

Pre-incentive revenue is the sum of service, data processing, international transaction and other revenue. It is not gross profit or the value of payments processed. FY2025 pre-incentive revenue is 55,751; incentives are 15,751; net revenue is 40,000. Visa’s statements do not report conventional gross profit, combined SG&A or merchandise inventory. The required history grid marks those absent lines explicitly and provides operating-margin and expense-ratio substitutes. [FY2025 10-K, MD&A and Note 3][25]

Visa’s settlement receivables/payables reflect payment clearing; customer collateral is restricted and offset by an equal liability. Neither is a retailer’s inventory-financing balance. Litigation escrow is also restricted, so the cash floor and surplus-cash valuation exclude it. [FY2025 10-K, Notes 1, 4–5][25]

## R — labeled assumption set

All forward policy choices are judgments even when calibrated to history. “Guidance” below means a filing’s estimated amortization schedule, not promised growth. These are **AI-assisted draft reasons**, not statements that Aidan has already defended; review and rewrite them before checkout.

| Value / assumption | Label | Reason |
|---|---|---|
| Opening balance sheet: September 30, 2025, assets 99,627; liabilities 61,718; equity 37,909 | history | Use the latest audited annual balance sheet; every account is mapped in the source file. [25] |
| Historical net revenue: 32,653 / 35,926 / 40,000 in FY2023–25 | history | Establish actual scale and growth before forecasting; use filings rather than prior unsourced report values. [23] [24] [25] |
| FY2026–30 **pre-incentive** revenue growth: 15%, 14%, 13%, 12%, 11% | judgment | Approved by Aidan after reviewing the evidence. Calculated pre-incentive growth was 10.55% in FY2024, 12.20% in FY2025 and 15.15% in the first nine months of FY2026; value-added services grew 32% in that nine-month period. Maintain near-term strength, then moderate toward historical low-teens growth. The exact annual decline is a scenario choice, not management guidance. [25] [Q26] |
| Incentives / pre-incentive revenue: 28.5%, 28.7%, 28.9%, 29.1%, 29.3% | judgment | FY2023–25 ratios rose from 27.36% to 28.25%. Allow modest continuing pressure from client competition rather than hold the take rate permanently fixed. [25] |
| Personnel / net revenue: 17.4025% | judgment | Hold FY2025’s ratio as a neutral cost baseline; this includes the economic cost of compensation historically paid in shares. [25] |
| Marketing / net revenue: 4.2100% | judgment | Maintain FY2025 brand and client marketing intensity. [25] |
| Network / net revenue: 2.2350% | judgment | Preserve observed processing costs without assuming unverified operating leverage. [25] |
| Professional fees / net revenue: 1.8975% | judgment | Keep FY2025’s legal, consulting and client-engagement cost intensity. [25] |
| General/administrative / net revenue: 4.8150% | judgment | Retain the observed corporate-cost ratio. Do not count it again through a synthetic SG&A subtotal. [25] |
| Litigation expense: 3% of net revenue, paid in the year incurred | judgment | Historical expense is volatile: about 2.84%, 1.29%, 6.41% of revenue. A recurring 3% allowance recognizes continuing risk without treating the FY2025 spike as permanent; this remains a major uncertainty. [23] [24] [25] |
| Property/technology D&A: 29.8640% of opening net PP&E | judgment | Apply the FY2025 derived 1,142 / FY2024 PP&E 3,824 rate. It includes software amortization but excludes acquired-intangible amortization; do not charge all D&A to PP&E. [25] |
| Acquired-intangible amortization FY2026–30: 63, 62, 43, 29, 10 | guidance | Use the filing’s estimated runoff of existing finite-lived intangibles; no future acquisitions are assumed. Indefinite-lived intangibles of 27,415 are not amortized. [25, Note 8] |
| Capex: 3.7% of net revenue | judgment | Approximately FY2025’s 1,482 / 40,000 = 3.705%, above earlier years, to fund technology and network investment. [25] |
| Tax: 20% of positive pretax earnings; no loss tax benefit | judgment | Above the historical 17–18% effective rates, allowing for less favorable tax benefits/mix. Assume cash taxes equal tax expense; hold deferred tax balances fixed. [23] [24] [25] |
| Receivables, payables and accrued compensation: constant FY2025 ratios to net revenue | judgment | Scale ordinary operating balances with activity instead of plugging the balance sheet. Opening balances are 3,126 / 555 / 1,863. [25] |
| Incentive assets and liabilities: constant FY2025 ratios to incentive expense | judgment | Use 7,315 / 15,751 and 10,369 / 15,751 to link contract assets and unpaid incentives to expense; the change determines incentive cash payments. Actual contract timing can differ. [25] |
| Settlement receivable/payable: FY2025 ratios to pre-incentive revenue | judgment | Scale opening balances 4,191 / 4,568 with network activity; these are volatile snapshots, not stable lending assets. Both sides enter the cash-flow bridge. [25] |
| Inventory and floor-plan financing: none | judgment | Visa has no reported merchandise-inventory/floor-plan structure. Client incentives are the explicitly modeled replacement feature. [25] |
| FY2026–30 principal maturities: 5,587; 2,750; 1,470; 1,176; 1,500 | history | Contractual maturity schedule disclosed at September 30, 2025. [25, Note 10] |
| Refinance 100% of scheduled principal; no net term borrowing | judgment | Keep the capital structure stable instead of importing ABG’s deleveraging assumption. Refinancing is assumed, not a claim that future funding has been arranged. Hold carrying-value adjustments and FX fixed. |
| Term interest: 3.5% of opening carrying debt; revolver interest: 6% of opening revolver | judgment | Use an explicit funding-cost allowance above FY2025 interest/carrying debt; it is not a quoted refinancing rate. Opening-balance interest avoids circularity but simplifies intrayear financing. |
| Revolver caps: 7,000 in FY2026–27; zero in FY2028–30 | judgment | The reported 7,000 facility expires in May 2028. For annual modeling, assume no availability from FY2028 unless a renewal is verified. Do not add the commercial-paper program to this facility as extra liquidity. [25, Note 10] |
| Minimum unrestricted cash: 5,000 | judgment | Preserve a substantial operating/settlement buffer, separate from restricted client funds. This is a modeling choice, not Visa’s stated minimum. |
| Dividends: 25% of positive NI; buybacks: 50% of positive NI | judgment | Retain cash flexibility while modeling shareholder distributions; this is more conservative than FY2025 repurchases. Distributions reduce equity/cash but are not expenses or deductions from pre-distribution FCFE. |
| Share compensation: cash-equivalent expense; no SBC addback or share issuance | judgment | Charge the economic compensation cost while keeping the claim base fixed. This is a normalized forecast, not a projection of Visa’s reported SBC accounting. |
| Cash/investment income: zero; investment securities frozen at 2,832 | judgment | Avoid capitalizing earnings on cash and also adding that same cash. No extra valuation credit is assigned to investment securities or other non-operating investments, making that omission conservative. |
| Escrow 2,990 and legacy litigation accrual 3,033: fixed; customer collateral asset/liability 3,625 each: fixed | judgment | Do not guess legacy settlement dates or claim restricted funds as shareholder cash. New litigation expense is paid as incurred; legacy releases, payments and share-conversion effects are outside this simplified case. |
| Prepaid assets 2,679; other assets 3,944; goodwill 19,879; accrued liabilities 5,466; deferred tax 5,549; other liabilities 1,519: fixed | judgment | Keep residual balances explicit instead of hiding an equity/cash plug. This omits detailed tax, lease, FX and acquisition schedules; operating lease costs remain in expenses. |
| New acquisitions, asset sales, goodwill impairment, OCI/FX movements and equity issuance: zero | judgment | A standalone operating case cannot predict individual deals or market remeasurements. Change these only with a corresponding balance-sheet and cash-flow entry. |
| Cost of equity: 9% | judgment | A transparent required-return scenario for this mature network business. It is not an estimated CAPM result and is not the earlier DCF’s WACC merely renamed; sensitivity to 8–10% is shown below. |
| Terminal growth: 3%; stable-growth reinvestment after FY2030 | judgment | Fade below explicit growth and charge additional PP&E and working capital needed for growth. Term debt stays flat through refinancing, so there is no ABG-style debt-repayment addback. |
| Fixed denominator: 1,930 million opening as-converted shares | history | FY2025 Note 15 includes all participating common/preferred claims. Using the opening claim base is a separate judgment: buybacks do not mechanically lift this valuation by shrinking a forecast denominator. [25] |
| Opening surplus cash credit: 17,164 − 5,000 = 12,164 | judgment | Value unrestricted cash above the operating floor once, assuming it is accessible to equity holders. Exclude escrow, collateral and forecast accumulated cash; the forecast has no cash-interest income. |

**Partner attack and two-sentence answer — required below the table:**

- Partner name/date: **PENDING**.
- Actual judgment attacked and partner’s exact question: **PENDING**.
- Aidan’s two-sentence answer: **PENDING**.
- Aidan’s actual attack on partner’s model and their response: **PENDING**.

Optional practice prompt (AI-generated, **not** partner participation): “Why should incentives rise only 0.2 percentage points per year, and which client-contract evidence would make you change that?” A useful response should explain both the history behind the number and a measurable condition for changing it. A specific attack on a partner might address a mismatch between reported and organic growth, or an unsupported constant margin; tailor it to their actual model.

## I — how the statements connect

1. Grow revenue before incentives, subtract incentive expense, and deduct the separate operating expenses, property/technology depreciation and acquired-intangible amortization.
2. Deduct interest and taxes to compute NI. Roll PP&E as opening PP&E + capex − depreciation, and intangibles as opening intangibles − amortization.
3. Calculate operating balances from the stated ratios. Incentive cash paid = expense + increase in incentive assets − increase in incentive liabilities. CFO starts with NI, adds D&A, subtracts increases in modeled operating assets, and adds increases in operating liabilities. Incentive expense is already in NI, so it is not subtracted twice.
4. Show maturing principal and assumed refinancing separately. FCFE = CFO − capex + debt issued − debt repaid + net revolver borrowing. Subtract dividends/buybacks to obtain the cash change. Ending cash comes from the cash-flow statement, never from assets minus liabilities.
5. Equity rolls forward from opening equity + NI − dividends − buybacks. The checks independently verify balance sheets, cash, equity, PP&E, intangibles, debt, incentives, income and financing links.

Balances are condensed: current/noncurrent classifications are not separately forecast. Restricted cash and related frozen balances have zero changes, so the unrestricted cash bridge has the same change as total cash in this simplified forecast. The model is not a full reproduction of Visa’s SEC-format statements.

## DCF / FCF vocabulary

**DCF** means discounted cash flow: translate future cash into today’s value at a required return. **FCF** means cash remaining after operating needs and investment. **FCFE** is for equity holders after net borrowing; discount it at cost of equity. **FCFF** is before financing cash flows, for lenders and shareholders together; discount it at WACC, then bridge enterprise value to equity. This lab uses FCFE. Dividends and buybacks distribute FCFE rather than create it.

## V — valuation and dated market comparison

The discount anchor is September 30, 2025, with FY2026–30 treated as five year-end cash flows. The research uses information available in September 2026, so this is neither an untouched historical backtest nor a September 2026 spot valuation. The [June 2026 10-Q][Q26] was checked for growth context: nine-month revenue 33,764 versus 29,276 (+15.33%); Q3 revenue 11,633 versus 10,172 (+14.37%). FY2026 is estimated, not reported annual history. The model’s FY2026 balance sheet is not calibrated to the already reported June balances.

For the terminal year, NI grows at 3%; net PP&E investment is 3% of closing PP&E and working-capital investment is 3% of closing modeled operating NWC. Total terminal capex therefore covers D&A plus growth investment. This avoids carrying the explicit period’s higher growth-related reinvestment into a 3% perpetuity unchanged. NI scaling and a flat debt balance are explicit terminal approximations. The transition from 11% pre-incentive revenue growth in FY2030 to a 3% stable-growth terminal regime is abrupt; no additional transition years are modeled. This remains a teaching-model limitation. No existing debt is subtracted again from FCFE value, and no gross repayment is added back merely because ABG did so.

Formula: terminal FCFE = NI2030 × 1.03 − 0.03 × PP&E2030 − 0.03 × operating NWC2030. Terminal value = terminal FCFE / (cost of equity − growth). Add discounted five-year FCFE and discounted terminal value, then the one-time opening surplus cash credit. Future ending cash is not added: its originating FCFE has already been valued.

Under the lab’s stated convention, negative explicit FCFE years are labeled and excluded from the positive-cash-flow sum; this can overstate value in loss cases compared with recognizing funding needs. The base case has no negative years. A negative final-year or sustainable terminal FCFE refuses valuation, because the positive-growth perpetuity premise would be unsupported.

**Market observation:** [Stock Analysis](https://stockanalysis.com/stocks/v/) displayed **$367.98 at the September 24, 2026, 4:00 p.m. EDT close** when opened during this work. The separately displayed $367.30 after-hours price is not used. Visa’s own quote page returned an older September 23 close of $361.52 when opened, so it was not relabeled as today’s price.

Comparison sentence/question: **The annual model says $273.76 per opening as-converted share, while the September 24 market close was $367.98; using the same 1,930 million-share claim base for comparison, what growth, incentive costs, required return, or valuation-date update would explain the difference?** Multiplying market price by that common denominator gives a comparison equity value, not Visa’s actual current market capitalization. A current investment valuation would first update the balance sheet, remaining forecast timing, distributions and share count. No buy/sell recommendation follows from this exercise.

## Model results and sensitivity

Recalculated after Aidan approved the 15%, 14%, 13%, 12%, 11% pre-incentive revenue growth path. USD millions except share values. Full statements and checks are in `Lab10_output.txt`.

| Result | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
|---|---:|---:|---:|---:|---:|
| Net revenue | 45,841.3 | 52,112.9 | 58,722.3 | 65,584.0 | 72,592.9 |
| Operating income | 29,128.9 | 33,168.0 | 37,418.8 | 41,806.7 | 46,276.8 |
| Net income | 22,598.3 | 25,829.6 | 29,230.2 | 32,740.6 | 36,316.7 |
| FCFE | 22,672.3 | 25,831.3 | 29,161.9 | 32,618.1 | 36,143.3 |
| Ending unrestricted cash | 22,887.5 | 29,346.6 | 36,585.8 | 44,648.5 | 53,554.3 |
| Ending equity | 43,558.6 | 50,016.0 | 57,323.5 | 65,508.7 | 74,587.9 |
| Revolver | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Balance-sheet gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Cash-flow bridge gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

- PV of explicit FCFE: **$111,658.39 million**.
- FY2031 terminal FCFE: **$37,345.93 million**.
- PV of terminal value: **$404,538.24 million**.
- Opening surplus cash credit: **$12,164.00 million**.
- Equity value: **$528,360.63 million**.
- Value per share: **$273.76**; terminal share of equity value: **76.56%**.

Sensitivity recomputes terminal reinvestment at each growth rate while holding the five-year operating forecast fixed. These are scenarios, not probability estimates.

| Cost of equity | Terminal g = 2% | Terminal g = 3% | Terminal g = 4% |
|---|---:|---:|---:|
| 8% | $283.29 | $329.21 | $398.08 |
| 9% | $242.17 | $273.76 | $317.99 |
| 10% | $211.37 | $234.21 | $264.66 |

A one-percentage-point increase in incentives / pre-incentive revenue in every forecast year lowers value to **$270.05**. This is an AI-generated stress case, not a partner review.

The original 15%, 12%, 11%, 10%, 9% path is retained as a slower-growth comparison: **$256.38/share**, versus **$273.76/share** for the approved base case. All other assumptions are identical. The comparison can be reproduced by passing a copy of the inputs with `assumptions.gross_growth` replaced by `growth_review.slower_growth_comparison` to the model’s `project` and `value` functions.

The deliberate cash error produces `VALUATION REFUSED: FY2026E: balance-sheet gap: -5,723.533023 million`, exit code 1, and no per-share valuation. All eight tests pass after the growth revision, covering accounting links, refusal, incentive pressure, revolver constraints and terminal-value safeguards.

## E — finish the actual checkout

- [x] Aidan reported verifying FY2025 net income and net property/equipment/technology; recorded in `Lab10_history_and_sources.md`.
- [x] Before the growth revision, Aidan shared a successful `python3 lab-10/Lab10_visa_proforma.py` run: exit code 0, all checks pass, equity value $494,807.15 million and $256.38/share. This is user-provided evidence for the earlier version. `Lab10_output.txt` now records the revised model and passing tests.
- [ ] Aidan reviews/rephrases the judgment reasons and explains the Visa-specific line to a real partner.
- [ ] Record the partner’s question, Aidan’s two-sentence answer and the reverse exchange under the assumption table.
- [ ] Complete the reflection in your own words: which assumption would you defend longest, and which filing number surprised you? Suggested item to examine: the size of client incentives relative to pre-incentive revenue.
- [ ] Upload the reviewed `.md`, `.py`, `.json` and output files to the course GitHub location and record links; submit individually according to course procedure. **Not performed.**

Run from the Visa folder:

```bash
python3 lab-10/Lab10_visa_proforma.py
python3 lab-10/Lab10_visa_proforma.py --break-2026-cash
python3 lab-10/Lab10_test_visa_proforma.py
```

The second command intentionally fails; it does not alter the saved inputs or ABG case.

[23]: https://www.sec.gov/Archives/edgar/data/1403161/000140316123000099/v-20230930.htm
[24]: https://www.sec.gov/Archives/edgar/data/1403161/000140316124000058/v-20240930.htm
[25]: https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm
[Q26]: https://www.sec.gov/Archives/edgar/data/1403161/000140316126000104/v-20260630.htm
