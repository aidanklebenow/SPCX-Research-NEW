# Lab 10 source register

Research performed September 24, 2026. The linked filings were inspected online. **No complete 10-K or 10-Q files were successfully downloaded into this folder.** Download attempts failed because of certificate validation and SEC access errors. The source links below and the extracted history grid document the research; they must not be described as local copies of the filings.

## Primary historical evidence

| Resource | Purpose |
|---|---|
| [Visa FY2023 Form 10-K](https://www.sec.gov/Archives/edgar/data/1403161/000140316123000099/v-20230930.htm) | FY2023 financial statements, MD&A and accounting notes; FY2022 comparative revenue/PP&E for growth and depreciation denominators. |
| [Visa FY2024 Form 10-K](https://www.sec.gov/Archives/edgar/data/1403161/000140316124000058/v-20240930.htm) | FY2024 financial statements, MD&A and notes; comparative cross-checks. |
| [Visa FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm) | FY2025 history and audited opening balance sheet; revenue/client incentives; restricted funds; PP&E/intangibles; debt maturities/revolver; as-converted shares. |

See [Lab10_history_and_sources.md](../Lab10_history_and_sources.md) for item-level filing links and statement/page locators. Gross profit, combined SG&A and inventory are not separately reported in these statements; the report explicitly identifies the substitutions or non-applicability. FY2025 property/technology D&A of 1,142 is derived from total D&A less acquired-intangible amortization, not copied as an exact Note 7 amount.

## Additional resources

| Resource | Used for | Limits |
|---|---|---|
| [Course Lab 10 instructions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/lab-10-proforma-your-company.md) | Deliverables, labels, refusal checks, market comparison and partner-review requirements. | Does not establish that any student/partner activity occurred. |
| [Visa quarter ended June 30, 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/1403161/000140316126000104/v-20260630.htm) | Recent revenue and growth context for the FY2026 assumption. | Does not replace the FY2025 annual balance-sheet anchor or fully calibrate the FY2026 forecast. |
| [Visa Q3 FY2026 earnings release](https://www.sec.gov/Archives/edgar/data/1403161/000140316126000103/q32026earningsrelease.htm) | Supplemental research on quarterly performance, capital returns and business context. | No numerical growth assumption is presented as management guidance. |
| [Stock Analysis annual cash flow statement](https://stockanalysis.com/stocks/v/financials/cash-flow-statement/) | Course-required provider capex comparison with each annual filing. | Provider is a cross-check; filing figures remain the historical source of record. Annual columns are distinguished from TTM. |
| [Stock Analysis Visa quote](https://stockanalysis.com/stocks/v/) | Displayed September 24, 2026 regular-session close of $367.98. | A dated website observation, not a live executable quote; saved in `Lab10_market_observation.json`. |
| [Visa investor-relations quote page](https://investor.visa.com/stock-information/quote-chart/default.aspx) | Attempted primary-source market-price verification. | Opening the page returned September 23's $361.52 close. It was not used as September 24's closing price. Earlier search snapshots were not used as final closing prices. |

## Existing local work consulted

- Visa folder `README.md` and root `visa_inputs.json`: recovered earlier course context and source locations. Prior model inputs were not automatically treated as current verified inputs.
- `../lab-09/proforma.py`, relative to the Lab 10 folder: inspected the ABG model structure and reran the verified $291.75/share case. The ABG file was not changed.
- Earlier Visa DCF values are contextual references; this model uses FCFE and its own labeled assumptions.

## Evidence versus modeling choices

Historical financial figures and contractual debt maturities come from filings. Forecast growth, incentive ratios, expense policies, tax rate, refinancing, cash floor, payouts, discount rate and terminal policy are judgments. The finite-lived intangible amortization schedule is a forward estimate disclosed in the FY2025 filing. No synthetic forecast, AI practice question or manual-check placeholder should be described as filing data, a completed partner review or a student verification.
