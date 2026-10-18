# Project 1 — Start here

This is the dedicated Project 1 workspace. Labs are in the repository's separate `lab-06` through `lab-13` folders.

## Current status

The project scaffold, preserved Visa models, research notes, and legacy validation evidence exist. The complete integrated Project 1 model and final deliverable bundle have not been completed. The student reports the deadline is tomorrow night; confirm the exact cutoff in Brightspace.

## Work in priority order

1. Obtain the current assignment prompt, rubric, required filenames, and exact deadline from Brightspace. Recover the actual Edition A checkpoint and receipt; the checkpoint folders are currently empty.
2. Finalize Visa's valuation date, information cutoff, horizon, share basis, and exclusions in `inputs/decision_context.json`.
3. Collect the underlying financial statements and reconcile the opening history. Populate `inputs/source_register.csv` and `inputs/assumption_challenges.csv`; both currently contain headers only.
4. Build the integrated operating forecast, FCFF, sourced WACC, and enterprise-to-equity bridge using the preserved Visa models as references. Existing Lab 10/11 teaching values are FCFE outputs, not the completed Project 1 FCFF valuation.
5. Produce scenarios, sensitivity, reverse DCF, peer comparisons, and internally consistent statements. Validate the integrated model before relying on its results.
6. Prepare the required memo/deck, recordings, transcripts, and final submission files against the official checklist.

## Where files belong

| Folder | Purpose |
|---|---|
| `checkpoints/` | Actual baseline and subsequent editions |
| `data/raw/` | Original source documents |
| `data/processed/` | Reconciled historical data |
| `inputs/` | Model assumptions, context, and source registers |
| `src/` | Model code |
| `tests/` | Model tests |
| `outputs/` | Generated model results |
| `research/` | Research, architecture, and compliance audit |
| `legacy/` | Preserved earlier Visa coursework and models |
| `validation/` | Validation scripts and evidence |
| `deliverables/` | Memo/deck, recordings, and transcripts |
| `submission/` | Final Project 1 package |

See [NEXT_STEPS.md](NEXT_STEPS.md) for the detailed build sequence and [research/compliance_audit.md](research/compliance_audit.md) for the existing gap assessment.

The preserved Lab 13 files under `src/`, `tests/`, and `outputs/lab-13/` are historical development evidence. The standalone Lab 13 submission is at `../lab-13/`; it is separate from Project 1.
