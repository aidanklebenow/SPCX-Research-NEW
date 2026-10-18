# Lab 11 — Visa base assumption table

Snapshot taken September 29, 2026 from the approved Lab 10 model. No new sensitivity ranges are selected here. Labels and reasons remain those of Lab 10; this is not a new partner review or student prediction.

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


[23]: https://www.sec.gov/Archives/edgar/data/1403161/000140316123000099/v-20230930.htm
[24]: https://www.sec.gov/Archives/edgar/data/1403161/000140316124000058/v-20240930.htm
[25]: https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm
[Q26]: https://www.sec.gov/Archives/edgar/data/1403161/000140316126000104/v-20260630.htm
