# Visa | Code, Data Lineage and Validation

**Video 2 · Executive Technical Briefing · October 19, 2026**

> **Filing facts → reported and normalized history → five-year statements → checked cash flows → valuation.**

All presentation exhibits and the script are embedded here. During recording, scroll within this Markdown Preview. The simplified script is about **230 words**, with room for pauses within the **3:00 maximum**. Read straight through; navigation cues are optional.

## Python Data Pipeline and Lineage

| Stage | Implementation and lineage | Financial meaning |
|:---|:---|:---|
| Filing facts | `validation/prepare_history.py` preserves transcribed Visa facts in `data/raw/visa_filing_facts.json`, with URLs and filing locators in `inputs/source_register.csv` | FY2025 10-K and June 2026 10-Q; transcribed facts, not full downloaded filings |
| Trailing history | Preparation writes `data/processed/history.json`; `validate_history()` checks its arithmetic | TTM = FY2025 + 9M2026 − 9M2025; June 30 balance sheet remains reported history |
| Normalization | Preparation writes `normalized_history.csv`; `validation/build_evidence.py` writes `normalization_bridge.csv` | Retain litigation at 2% of net revenue; normalized tax at 20%; both are analyst judgments |
| Runtime inputs | `src/visa_model.py`: `load()` reads `history.json` and `inputs/model_inputs.json`; `run()` validates both | The bridge CSV documents adjustments; the engine applies litigation and tax policies directly, rather than loading the bridge CSV |
| Opening estimate and forecast | `opening()` estimates the June 30–October 19 opening roll-forward; `advance()` creates five forward annual periods | October 19, 2027–2031 endpoints; these are anniversary years, not Visa fiscal years |
| Statements to value | `check_period()` gates the statements; `value()` builds discounted cash flow and the equity bridge; `run.py` exports results | Operating cash flows drive value; eligible surplus cash/securities, debt, other claims, and economic shares bridge enterprise value to per-share value |

### Earnings Normalization Bridge

**USD millions · Reported or derived TTM → Normalized**

| Metric | FY2025 | TTM through June 2026 |
|:---|---:|---:|
| Litigation expense | 2,562 → **800** | 2,193 → **889.760** |
| Operating profit | 23,994 → **25,756** | 26,996 → **28,299.240** |
| Pretax income | 24,194 → **25,956** | 26,956 → **28,259.240** |
| Income tax | 4,136 → **5,191.200** | 4,364 → **5,651.848** |
| Net income | 20,058 → **20,764.800** | 22,592 → **22,607.392** |

Normalized operating profit = reported operating profit + reported litigation − recurring litigation. Normalized tax = 20% × positive normalized pretax income. Historical investment income remains in normalized historical net income; forward operating FCFF excludes it. Reported history and historical operating cash flow are not overwritten.

### Five-Year Engine

Service, processing, international, and other revenue respond to activity and yield assumptions. Client incentives reduce gross revenue; incentive assets and liabilities reconcile expense with cash paid. Costs, taxes, working capital, capex, depreciation, dividends, and financing determine closing balances.

**FCFF = EBIT − unlevered tax + depreciation and amortization − capex − change in operating working capital.**

WACC discounts FCFF. Equity value = enterprise value + eligible excess cash + liquid securities − funded debt − other claims. Divide by diluted economic equivalents for per-share value.

---

## Validation Architecture

**Saved passing record: 24 integrated tests + 4 workbench tests = 28 tests.** Separate HTTP smoke checks are additional. These are preserved results, not a new run performed for this document update.

| Validation layer | Core check | Failure detected |
|:---|:---|:---|
| Historical integrity | Filing totals, income bridges, full CFO components, restricted-inclusive cash and TTM arithmetic reconcile | Misstated periods, omitted cash components, inconsistent source totals |
| Balance-sheet articulation | Assets = liabilities + equity; PP&E, intangibles, debt, equity, and incentive accounts roll forward | Unfunded balances and broken statement links |
| Cash-flow tie-outs | CFO = net income + D&A − change in working capital; closing cash = opening cash + CFO + CFI + CFF | Cash plugs even if equity is adjusted to mask a balance-sheet gap |
| FCFF linkage | Recompute FCFF from statements and independently cross-check through tax-adjusted FCFE | A plausible-looking DCF disconnected from the operating engine |
| Monotonicity | With positive forecast cash flows, +100 bp WACC lowers EV; this model's +50 bp terminal growth raises value with reinvestment recalculated | Reversed discounting or terminal-value behavior |
| Equity bridge | A $1,000M larger cash reserve or other claim lowers equity by $1,000M with the valuation basis fixed | Incorrect signs, cash eligibility, or claim treatment |
| Boundaries and isolation | Invalid rates/dates, stale shares, liquidity failures, and restricted securities refused; reset restores base | Invalid inputs or scenario contamination |

**Failure probes:** +$100M disconnected FCFF is refused. A +$100M unfunded cash increase fails articulation; adding equity to mask it still fails the cash bridge. These are injected diagnostics, not Visa reporting errors.

**Known answers and reproducibility:** A $100 perpetuity at 10% produces $1,000 enterprise value. The separate Asbury teaching case reproduces $291.75/share. A saved fresh-copy, no-pip environment run reproduced `results.json` exactly. Mechanical consistency does not validate forecast economics.

---

## Locked Changed-Input Test Record

**Recorded prediction:** terminal growth rises from **3.0% to 3.5%**, increasing base value from approximately **$267 to $284/share**; Do Not Initiate remains unchanged.

| Test field | Preserved record |
|:---|:---|
| Input | `terminal_growth`: 0.030 → 0.035; +50 basis points |
| Prediction transcription frozen | October 19, 2026, 22:35:24.078338 UTC |
| Additional verification run | October 19, 2026, 22:35:54.021857 UTC |
| Prediction fingerprint | `5745c3b816ae8eb21e2251cccc1e784202b3cdb16309e93029852547cfad02bf` |
| Before value | **$267.46/share** |
| Predicted after value | **Approximately $284/share** |
| Actual after value | **$284.26/share** |
| Actual change | **+$16.80/share; +6.28%** |
| Difference from approximate prediction | **+$0.26/share**; direction agrees, not an exact numerical match |
| Decision | **Do Not Initiate → Do Not Initiate** versus the October 16 reference of **$402.61** |
| Held fixed | Opening balances, explicit five-year FCFF, WACC, economic shares, and original low/high scenario policies |
| Recomputed | Terminal NOPAT, reinvestment using growth/ROIC, terminal FCFF, and terminal value |
| Base preservation | Original 3.0% input file unchanged; only the supplemental base view uses 3.5% |

**Interpretation:** Higher perpetual growth increases valuation in this run after funding its required reinvestment. The resulting value remains below the dated market reference, so the action does not change.

**Provenance:** Aidan supplied the prediction and described it as human-authored with AI off; authorship and original writing time were not independently verified. The transcription was frozen before this additional run, but the same growth change had already appeared in automated testing. Codex executed the verification. This record does **not** establish an unexposed prediction or a student-operated AI-closed run; the qualifying human-only requirement remains unverified.

---

## Teleprompter Script

**Recording setup:** This script is about 230 words, leaving room for pauses and a slower pace within three minutes. Read only the paragraphs; bracketed cues are optional and refer to sections in this same file.

<!-- SCRIPT START -->
[SHOW: Python Data Pipeline and Lineage.]

Python loads Visa’s filing data and keeps it separate from forecast assumptions. It builds trailing results from annual and quarterly figures. An estimated opening balance sheet then feeds the five-year forecast.

[SCROLL TO: Earnings Normalization Bridge.]

The earnings bridge keeps recurring legal costs at two percent of revenue and uses a twenty-percent tax rate. These are judgment calls. Reported history stays unchanged.

The forecast connects revenue, costs, working capital, and investment across all three financial statements. Free cash flow comes from these statements and drives the valuation.

[SCROLL TO: Validation Architecture.]

The saved record contains twenty-eight passing tests.

Assets must equal liabilities plus equity. Cash movements must reconcile. Valuation cash flows must match the statements.

Deliberate cash errors fail these checks. Directional tests confirm that higher WACC lowers value and higher terminal growth raises value in this model.

[SCROLL TO: Locked Changed-Input Test Record.]

The prediction raised terminal growth from three to three-and-a-half percent, expecting about two hundred eighty-four dollars per share.

The actual result rose from two hundred sixty-seven dollars and forty-six cents to two hundred eighty-four dollars and twenty-six cents.

Forecast cash flows and WACC stayed fixed. Terminal reinvestment was recalculated. Do Not Initiate remained unchanged.

Codex ran this check, and earlier tests had used the same change. It does not establish an AI-closed student run.

A fresh-environment run also reproduced the results. These checks support consistency, while forecast assumptions still require judgment.
<!-- SCRIPT END -->

---

## Embedded Evidence and Reproduction Reference

The exhibits above consolidate the saved records in `Full_Validation_and_AI_Use.md`, `TerminalGrowth_Prediction_AsProvided.md`, `TerminalGrowth_Verification_Output.json`, `validation/cold-run/cold_run.json`, the normalization CSV, and the inspected engine/tests. Paths beginning with `src/`, `inputs/`, `data/`, or `validation/` are relative to the project root, two directories above this file. No external file is needed to follow the presentation.

For later reproduction, run from the project root, not this submission folder:

```bash
python3 run.py
python3 -m unittest discover -s tests -p test_integrated.py -v
python3 -m unittest discover -s tests -p test_workbench.py -v
```

This briefing is preparation material, not a recording or actual transcript. A one-file presentation summarizes code and saved checks; if the course requires a live execution or actual source walkthrough, the summary alone does not demonstrate those actions.
