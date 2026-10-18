# Repository prerequisite audit — October 18, 2026

Lab 13 is **Portfolio Mandate Defense**, not another Visa valuation lab. Authority: [published assignment](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-08/lab-13-portfolio-mandate.md), retrieved October 18; local copy in `research/course-requirements/`. Brightspace governs quiz closure and submission details.

| Component | Finding |
|---|---|
| Labs 1–5 | Not present in this repository; completeness cannot be confirmed |
| Labs 6–8 | Visa reverse DCF, comparable-company scripts and triangulation present |
| Labs 9–11 | Pro-forma engines, outputs, sensitivity inputs/results and regression tests present |
| Lab 12 | Review and upload guide present; completeness against its rubric not independently established |
| Legacy integrity | All snapshot hashes checked by `validation/run_lab13.py`; see run manifest |
| Legacy execution | Six regression/audit checks rerun, including deliberate broken-cash refusals |
| Visa FCFF/WACC | Earlier standalone FCFF DCF present; integrated Project 1 FCFF and component-sourced WACC absent |
| Research | Target selection, architecture and compliance audit present; these document outstanding work |
| inputs/ | decision_context.json has unresolved dates, horizon and share basis; source_register.csv and assumption_challenges.csv contain headers only; peer policy present |
| checkpoints/ | Edition A/B folders contain only .gitkeep; baseline and receipt absent |
| data/ | Raw and processed folders contain only .gitkeep |
| Legacy interpretation | Lab 10/11 FCFE values use the legacy September 30, 2025 teaching anchor; not a current FCFF valuation |

No legacy file was edited. Passing arithmetic/regression checks does not establish source completeness, a current valuation, or completion of Project 1. Visa pro-forma and sensitivity regression checks pass; full integrated FCFF/WACC and peer-definition consistency cannot be certified with the current scaffold.

Lab 13's common case supplies its own holdings, weights and policy parameters. It does not require the missing Visa model or CSVs. No Visa exposure or valuation is inserted into the assigned case.
