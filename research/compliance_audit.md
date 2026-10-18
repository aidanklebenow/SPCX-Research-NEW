# Project 1 compliance audit — October 6, 2026

Authority: complete assignment prompt supplied by Aidan in this conversation. Brightspace governs due date, Edition A window, exact seven-part filenames and rubric. Those items, the annotated excerpt and full 300-point rubric were not available locally. Public course home inspected: https://github.com/CinderZhang/FIN43900-Fall2026 . This audit establishes coverage against the supplied prompt, not a score or verified submission status.

## Existing structure inspected
Visa is a file workspace without its own .git directory; labs 06–12, earlier-research and a .venv are present. SPCX-Research-NEW is the separate older Git checkout, with a clean short-status result at inspection; it retains duplicated Visa lab material. SpaceX files are preserved in archive/SpaceX. No Edition A/receipt or complete Project 1 bundle was found in the inspected course tree. The new Project-1 repository keeps independent snapshots and hashes.

| Requirement | Finding | Required action |
|---|---|---|
| Intended buy-side user, no position, horizon, target, valuation date/currency/share basis/exclusions | Partial: USD, Visa and various historical anchors exist; no single project context | Complete inputs/decision_context.json; approve horizon/date and compatible shares |
| Operating-company admission gate | Visa suitable in our interpretation; gate history not found | Recover Week 2 target/admission record; pivot requires instructor clarification |
| Original Edition A, first Brightspace receipt, Edition B evolution | Unverified; extensive valuation-specific AI work predates new scaffold | Recover actual originals/receipt; never fabricate AI-closed history; document evolution honestly |
| Material historical filing/source traces | Partial: Lab10_history_and_sources.md has detailed mapping; full filings absent locally | Save dated filing excerpts/full documents and source register; independently recheck material amounts |
| Facts vs normalization vs forecast/output; contamination catalog | Partial: labeled assumptions; litigation normalization discussed | Add explicit reported-to-normalized IS/BS/CF bridge for every material adjustment and basis change |
| Five-year personalized three-statement forecast | Existing Lab 10 engine balances and ties cash for FY2026–30 | Reuse operating architecture, update valuation timing, document frozen lines and cash/SBC policies |
| Base year reconciles to filing | Partial: mapped opening BS and history; tests assert totals, not full filed IS/CF | Add independent machine-readable filed benchmark; reconcile reported IS/BS/CF and normalized bridge |
| Every driver value · basis · challenge · evidence that changes it | Partial reasons/ranges; lacks complete reversal-evidence register | Populate assumption_challenges.csv for all load-bearing drivers; record actual challenger credits |
| Five-year FCFF from pro-forma forecast | Missing integration: earlier FCFF grows starting cash flow separately; Lab10/11 use FCFE | Build FCFF directly from checked operating statements; remove independent top-line FCFF growth loop |
| Sourced WACC and enterprise/equity/share bridge | Partial old assumed WACC/bridge; FCFE uses Ke | Build dated component WACC and compatible cash/debt/share bridge including other claims |
| Low/base/high causal cases and downside decision reversal | Partial old FCFF cases and single-driver FCFE sensitivity | Rerun complete statements and FCFF for causally linked cases and named downside |
| WACC–g sensitivity, terminal share, reverse DCF | Present in older standalone DCF, not integrated model | Regenerate with pro-forma-derived FCFF, sustainable terminal reinvestment and current-date bridge |
| Peer policy established before selection | Retrospective use/qualify labels exist, not proof of prospective policy | Freeze a project policy before new peer selection; disclose prior exposure |
| One EV and one equity multiple with definitions | Visa Lab08 is P/E only; ABG multiples are training/company-specific | Add consistent target-peer EV/EBITDA or EV/EBIT plus P/E, matched periods and accounting treatment |
| Transaction evidence context | No qualified target transaction valuation set found | Use only if comparable control/synergy/time basis defensible; otherwise explain exclusion |
| Method disagreement | Some older triangulation; AXP median mechanically included | Explain differing growth/risk/basis, exclude or bracket qualified peers; no mechanical average |
| Synthetic/known answer | ABG reproduced $291.75; saved reference in Lab09 | Verify against exact published starter answers; add FCFF-specific known-answer reconciliation |
| Independent load-bearing source/definition check | Saved capex/provider reconciliation; Aidan reported two filing checks without separately transcribed amounts | Preserve old evidence; capture reproducible old/new source amounts, definitions and locators |
| Directional test written before execution | Lab11 AI prediction timestamp before run; human adoption afterward | Can support disclosed AI-assisted directional work only; create new prospective test in integrated engine |
| Locked Changed-Input Record: human-authored AI-off | NOT met by Lab11 AI-assisted prediction; lab accommodation does not prove project waiver | Student writes prediction with AI off and genuinely locks before run; include timestamp/commit, units, decision effect and diagnosis |
| BS/cash, DCF boundaries/monotonicity, bridge checks | Eight Lab10 and four Lab11 tests pass; no full integrated checks | Retain articulation tests; add sourced base-year, FCFF/FCFE tax-adjusted cross-check, WACC/g and bridge tests |
| Peer/multiple consistency validation | Partial arithmetic and leave-one-out; no target EV definitions test | Validate EV claims, earnings periods, lease/SBC/normalization/currency/share policy |
| Highest-risk failure test | Broken cash and two-account masking tests refuse valuation | Add stale-date/restricted-cash/share-basis and disconnected-FCFF failures; declare chosen highest-risk failure |
| Clean fresh-environment cold run | NOT established by current audit or old runs | Fresh temporary checkout and venv; run complete model/tests; freeze command/env/hash/stdout/stderr/exit logs |
| Accepted/corrected/qualified/rejected AI output with independent evidence | Assisted lab records exist; full project disposition not frozen | Record specific output, decision, original claim, independent source/locator and model effect |
| Conditional valuation range, evidence dates, triggers | Older WAIT reports conditional on old engines and prices | New memo: initiate/watch-defer/do-not-initiate, defensible range, conditions, monitor/reversal triggers |
| Seven-part bundle, three bounded videos and corrected transcripts | No complete final bundle found | Import official checklist; prepare unchanged A, B, repo/output, Videos 1/2/3, memo/deck and frozen evidence/transcripts |
| Access/integrity final receipt | Unverified | Check links/access and receipt in Week 8; no new analysis during final access pass |

## Material conflicts to preserve
Lab06 uses 10% WACC, 1,898 million diluted weighted-average shares and $3,000M reserve. Earlier FCFF base uses 9%, 1,880 million as-converted shares and $3,000M reserve. Lab10 uses cost of equity, 1,930 million opening as-converted shares and $5,000M floor. Dates differ. These are separate models, not interchangeable values. Lab10's $273.76 is a September 30, 2025 anchored FCFE teaching output, not an October 2026 project range.

Lab10 clips negative explicit FCFE to zero under its lab rule. Lab11 retains signed flows and refuses unresolved valuation; neither rule should be blindly carried into a project FCFF DCF. Retain signed FCFF. Negative explicit cash flow is economically valid if financing/survival and terminal assumptions are defensible. A failed articulation or unresolved terminal basis must stop valuation.

Lab12 partner discussion concerns NVIDIA and is only as reported; it does not establish a fresh-eyes challenge of Visa's drivers. AI substitute review remains separately labeled under the reported lab accommodation, without assuming a project-level waiver.
