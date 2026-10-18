# FIN 43900 — Project 1

Prepared October 6, 2026 with Codex assistance for Aidan Klebenow. **Scaffold and audit, not a finished valuation or submission.** Recommended target: Visa (NYSE: V), provisional pending Aidan's decision and Edition A admission/history review. No existing coursework was moved or edited. No remote repository or submission was created.

Start with [audit](research/compliance_audit.md), [target evaluation](research/target_selection.md), and [next steps](NEXT_STEPS.md).

| Folder | Purpose |
|---|---|
| checkpoints/edition-a | Unchanged original baseline and first Brightspace receipt; currently absent |
| checkpoints/edition-b | Honest research evolution from the actual baseline |
| data/raw, data/processed | Filing evidence and normalized history, kept separate |
| inputs | Decision context, sources, assumptions and peer policy |
| src, tests | Integrated operating forecast, FCFF/WACC valuation and checks to build |
| outputs | Visible statements, bridge, cases, sensitivity, reverse DCF and conditional decision to build |
| validation | Reproducible audit logs, human-only locked record and AI-use evidence |
| research | Compliance audit, eligibility/target recommendation and architecture |
| legacy | Exact Visa evidence snapshots; SHA-256 inventory in manifest.json |
| deliverables | Memo/deck, three recordings and corrected transcripts |
| submission | Final seven-part manifest using official filenames, not invented names |

Run the existing-evidence audit from this directory:

```bash
python3 validation/run_legacy_audit.py
```

This runs frozen legacy checks and saves logs. It does not run a Project 1 FCFF model or qualify as a fresh-environment cold run. Use Python 3; current legacy code uses only the standard library. No dependencies required for this audit. `src/` and `tests/` are intentionally awaiting the integrated model; the architecture is specified in research/model_architecture.md.

## Integrity boundary
Edition A and its first successful Brightspace receipt were not found in the inspected course folder. Prior valuation-specific AI work is evident. Do not create a retroactive AI-closed baseline, backdate commits, or treat an AI-assisted lab prediction as human-authored AI-off work. Recover the actual checkpoint and clarify any target-change or missing-baseline remedy with the instructor. The due date, complete rubric, annotated excerpt and official bundle filenames still require Brightspace verification.
