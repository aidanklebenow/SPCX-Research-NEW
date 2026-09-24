# FIN 43900 — Lab 09: ABG pro-forma engine

Prepared September 24, 2026 for Aidan Klebenow with Codex assistance.
ABG is the required training case; Visa remains my selected course company.

Source: [Lab 09 instructions and supplied assumptions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/lab-09-proforma-build.md).
The inputs are the course's frozen case, not independently researched current ABG figures.

## Files and execution

- `proforma.py`: standard-library-only five-year income statement, balance sheet, cash flow, checks, and FCFE valuation.
- `lab09_output.txt`: captured successful run and the separate deliberate-error result.
- `lab09_summary.md`: method, results, explanations, and remaining student activities.

From the Visa folder:

```bash
python3 lab-09/proforma.py
python3 lab-09/proforma.py --break-2026-cash
```

The second command deliberately fails with exit code 1. Running the first command again returns the unchanged base case. No external packages are needed.

## Assumptions

All monetary inputs are USD millions; shares are millions. Ratios use the exact arithmetic supplied in the assignment, without intermediate rounding.

| Input | Value | Course label |
|---|---|---|
| Organic revenue growth | 1.8% annually | Judgment |
| Gross margin | 17.05% | Judgment |
| SG&A / gross profit, 2026–2030 | 66.5%, 65.5%, 64.5%, 64.5%, 64.5% | Judgment |
| Depreciation / opening PP&E | 82.4 / 3,070.4 | History |
| Annual impairment | 120 | Judgment |
| Annual capex | 250 | Guidance |
| Tax rate | 25.5% | Judgment |
| Inventory days | 2,135.8 / (17,999.0 − 3,071.7) × 365 | History |
| Floor-plan loans / inventory | 2,027.0 / 2,135.8 | History |
| Other working capital investment | 0.8% of change in revenue | Judgment |
| Minimum cash | 25 | History |
| Revolver limit / interest rate | 850 / 6% | Judgment |
| Annual term-debt repayment / buyback | 150 / 150 | Judgment |
| Floor-plan / term-debt interest rate | 4.67% / 5.44% | History |
| Cost of equity / terminal growth | 10% / 2.5% | Judgment |
| Shares outstanding | 17.951349 | Fact supplied in lab; June 30, 2026 10-Q |

Opening FY2025 balances: revenue 17,999.0; inventory 2,135.8; PP&E 3,070.4; other assets 6,371.6; cash 40.4; floor-plan loans 2,027.0; term debt 3,572.0; other liabilities 2,127.5; equity 3,891.7. Opening revolver is zero.

## Method and valuation

The engine calculates income first, then the noncash balance-sheet accounts, then cash flow and ending cash. Depreciation and interest use opening balances. Impairment reduces other assets and is added back in cash flow because it is noncash. A revolver covers a cash shortfall up to the limit and is repaid first when cash exceeds the minimum.

FCFE = net income + depreciation + impairment − capex − change in inventory − change in other working capital + change in floor-plan loans − term-debt repayment.

Cash = opening cash + FCFE − buybacks + net revolver borrowing.

The prescribed valuation discounts the five annual FCFE at the 10% cost of equity. Terminal value is `(2030 FCFE + 2030 debt repayment) × 1.025 / (0.10 − 0.025)`, discounted five years. Adding back the repayment assumes scheduled repayments stop after 2030. This is the assignment's convention. Shares stay fixed at the supplied count despite modeled buybacks, as directed by the lab.

This values equity directly: no additional cash/debt bridge and no WACC discounting of these FCFE. The base case does not draw the revolver.

## Known-answer verification

| Line (USD millions except per share) | FY2026E | FY2030E |
|---|---:|---:|
| Revenue | 18,323.0 | 19,678.3 |
| Operating income | 844.2 | 971.4 |
| Net income | 413.6 | 527.5 |
| FCFE | 211.4 | 342.3 |
| Ending cash | 101.8 | 719.8 |
| Assets − liabilities − equity | 0.0 | 0.0 |

All listed results match the assignment at the required decimal precision.
All five balance sheets balance to numerical tolerance; all years meet the 25 minimum cash and 850 revolver limit.

- Equity value: **$5,237.34 million**.
- Value per share: **$291.75**.
- Share of value after 2030: **79.76%**.

## Deliberately broken model

The `--break-2026-cash` option sets 2026 cash to the opening 40.4 instead of the computed 101.8. The same valuation function then calls `assert_balanced` and refuses to value it:

```text
VALUATION REFUSED: FY2026E: balance-sheet gap -61.4 million
```

No equity valuation is printed in that run. The negative gap identifies missing assets: the year's 61.4 increase in cash was omitted. The demonstration does not edit or damage the saved base case.

Additional checks exercised revolver borrowing and repayment and confirmed that an insufficient credit line stops valuation.

## Explanations for student review and partner discussion

**Three central operating judgments:** organic revenue growth, gross margin, and SG&A as a percentage of gross profit. They determine sales, how much of each sales dollar remains after vehicle costs, and how much gross profit operating expenses consume. The falling SG&A ratio assumes improved operating efficiency. The terminal assumptions also matter greatly because most of the value lies after 2030.

**Why cash comes last:** cash is the result of earnings, noncash adjustments, investment, and financing. Computing it from those flows lets the balance-sheet identity act as an independent check. Entering cash merely to force a balance could hide an error.

**What floor plan means:** inventory loans from manufacturers' finance arms and banks finance vehicles held for sale. In the course model, the balance rises with inventory, interest uses opening loans, and changes in those loans enter operating cash flow. Removing that financing while retaining the vehicle inventory leaves a large funding need. The video's roughly negative $1.1 billion cash illustration is a separate scenario, not a result claimed from this base-case run.

**What the −61.4 gap reveals:** assets are short of liabilities plus equity by the omitted cash increase. It is a broken link in the statements, not a forecasting opinion.

## Student activities and submission status

The model, automated verification, and this explanatory draft were prepared with Codex assistance. This record does not establish video viewing, class attendance, or a partner exchange.

- Review the explanations and be able to explain the three judgments and cash timing in your own words.
- Complete the required partner explanation and swap-and-break exercise; the automated local demonstration is preparation, not evidence of a partner exchange.
- Discuss floor-plan financing and the meaning of the negative gap.
- Upload the files to your course GitHub repository and submit their links. No upload or submission was performed by Codex.
