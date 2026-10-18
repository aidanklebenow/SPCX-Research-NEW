# Lab 10 — Visa (V)

Created September 24, 2026. This folder contains the separate Visa application of the Lab 09 engine. The verified ABG training case remains in `../lab-09/`; earlier Visa DCF and comparable-company work remains in its original location.

## File index, in working order

| Step | File | Contents and status |
|---|---|---|
| 1. Sources | [Source register](sources/Lab10_sources_README.md) | Exact resources used, their purposes, and download limitations. |
| 2. Historical evidence | [Lab10_history_and_sources.md](Lab10_history_and_sources.md) | FY2023–25 filing-linked history, ratios, capex provider comparison, audited opening balance sheet, and Aidan’s reported manual checks. |
| 3. Assumptions and discussion | [Lab10_summary.md](Lab10_summary.md) | Labeled forecast assumptions, Visa accounting choices, valuation explanation, sensitivity, price comparison, and pending partner review. |
| 4. Model inputs | [Lab10_visa_inputs.json](Lab10_visa_inputs.json) | Historical figures, FY2025 opening balances, and a separate forecast-assumption section. Null historical fields mean not separately reported, not zero. |
| 5. Executable model | [Lab10_visa_proforma.py](Lab10_visa_proforma.py) | Standard-library Python; five-year income statements, balance sheets, cash flows, financing checks and FCFE valuation. |
| 6. Verification | [Lab10_test_visa_proforma.py](Lab10_test_visa_proforma.py) | Eight tests covering accounting links, refusal behavior, financing limits and economic sensitivity. |
| 7. Saved results | [Lab10_output.txt](Lab10_output.txt) | Actual base run, deliberate-error run and test output with exit codes. |
| 8. Price observation | [sources/Lab10_market_observation.json](sources/Lab10_market_observation.json) | Dated provider observation and comparison-denominator caveat. It is a research note, not a downloaded exchange feed. |

`__pycache__/` is an automatically generated Python cache, not a lab deliverable.

## Dates and scope

- Historical annual periods: FY2023, FY2024, FY2025, each ending September 30.
- Opening balance sheet and valuation discount anchor: September 30, 2025.
- Forecast annual periods: FY2026–FY2030.
- Research and market-comparison date: September 24, 2026.
- June 2026 10-Q: used for growth context, not substituted for the annual opening balance sheet.
- $273.76/share: draft annual-model result, not a September 2026 spot valuation or investment recommendation.

The model combines historical evidence with research available in September 2026. It is not a historical backtest. Forecast assumptions are choices to review, not numbers reported in the 10-Ks.

## Run from the Visa folder

```bash
python3 lab-10/Lab10_visa_proforma.py
python3 lab-10/Lab10_visa_proforma.py --break-2026-cash
python3 lab-10/Lab10_test_visa_proforma.py
```

The deliberate-error command should exit with code 1 and refuse valuation. The other commands should exit with code 0.

## Completion status

The local draft, source grid and model verification are complete. Aidan reported completing two independent filing checks (FY2025 net income and net property/equipment/technology) and shared a successful model run. Review of judgment explanations in his own words, the actual partner exchange, GitHub upload and submission remain pending. AI-generated practice prompts do not count as partner participation.

Growth revision: Aidan approved pre-incentive revenue growth of 15%, 14%, 13%, 12%, 11% for FY2026–30. The 3% terminal assumption is retained; the abrupt transition remains disclosed. The original path is a slower-growth comparison in the summary.

## GitHub upload checklist — corrected against the assignment

The [Lab 10 instructions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/lab-10-proforma-your-company.md) request GitHub links to Markdown, Python and other files as needed. They do not require nine files. The earlier nine-file list was the complete working package, not a course requirement.

For the current organization, upload these four core files together:

- `Lab10_summary.md`: assumptions, methodology, value, price comparison and actual partner review (still pending).
- `Lab10_history_and_sources.md`: required three-year history, sources, ratios and reported manual checks.
- `Lab10_visa_proforma.py`: runnable five-year model and deliberate-error refusal.
- `Lab10_visa_inputs.json`: required runtime inputs; keep beside the Python file.

Recommended fifth file: `Lab10_output.txt`, which lets a reviewer see the statements, checks and refusal without running the model and resolves the report's output link. It includes the saved test results; the optional test script is needed only to rerun that separate test suite.

Optional supporting files: `Lab10_test_visa_proforma.py`, `Lab10_README.md`, `sources/Lab10_sources_README.md`, and `sources/Lab10_market_observation.json`. The core report/history already contain the filing citations and dated market observation.

Do not upload `__pycache__/`, `.pyc` files or the personal parent `AGENTS.md`. No full filing downloads are included.

Uploading a draft does not complete the lab: finish the actual partner exchange and remaining personal explanations/reflection before final checkout. Upload and submission have not been performed by the assistant.
