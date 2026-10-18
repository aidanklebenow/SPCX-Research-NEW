# Current folder guide — September 29, 2026

- **Today’s Lab 11 upload files:** [submission folder](lab-11/submission/). Upload its three files together. These copies preserve the edited submission text if the working runner regenerates its report.
- **Lab 11 working model and evidence:** [lab-11](lab-11/).
- **Gemini handoff:** [Lab11_Gemini_handoff.md](lab-11/Lab11_Gemini_handoff.md).
- **Labs 06–10:** existing numbered folders; model/input paths preserved.
- **Earlier Visa research:** [earlier-research](earlier-research/); original dates and assumptions retained.
- **Previous SpaceX work:** `../archive/SpaceX/`.
- **Separate existing Git checkout:** `../SPCX-Research-NEW/`; preserved with Git history. It is not the current Visa workspace.

The historical file list below refers to documents now grouped in `earlier-research/`. No upload or submission has been performed.

---

# FIN 43900 — Visa company switch

Prepared September 10, 2026. Previous SpaceX work is preserved.

**Lab 10 update — September 24, 2026:** Start with [the Visa pro-forma draft](lab-10/Lab10_summary.md) and [three-year history/source grid](lab-10/Lab10_history_and_sources.md). The separate FY2026–30 FCFE engine balances and estimates $273.76/share at its September 30, 2025 annual discount anchor; it is not a September 2026 spot valuation. Eight tests pass, including deliberate valuation refusal. Aidan reported verifying FY2025 net income and net property/equipment/technology and shared a successful model run. Personal judgment explanations, partner exchange and GitHub upload/submission remain pending. The older investment report below retains its original date and assumptions.

Start with [the investment report](earlier-research/Visa_2026-09-10_Investment_Report.md), then [the DCF explanation](earlier-research/Visa_DCF_Methodology.md). The decision is WAIT under the base assumptions, with a $250.92/share estimate versus a September 9 close of $367.39.

Files:

- `Visa_2026-09-10_Investment_Report.md`: buy/wait analysis following the available SpaceX report structure.
- `Visa_DCF_Methodology.md`: sourced inputs, normalized FCFF bridge, five-year forecast, scenarios, reverse DCF and limitations.
- `visa_dcf.py`: executable standard-library Python model.
- `visa_inputs.json`: editable reported data, assumptions and source URLs.
- `Visa_Research_Sources.md`: dated source register.
- `lab-06/`: Lab 06 sensitivity and reverse-DCF calculator and report.
- `lab-07/`: Lab 07 comparable-company calculators and summary.
- `lab-08/`: Lab 08 Visa peer-triangulation calculator and report.
- `lab-09/`: Lab 09 ABG training-case pro-forma engine, verified output, and summary (Visa-specific application belongs to Lab 10).
- [lab-10/](lab-10/Lab10_README.md): Separate Visa model, ordered file index, source register, sourced FY2023–25 history, labeled assumptions, dated price comparison, tests and pending partner-review fields.

Run from the AidanKlebenow folder:

```bash
python3 Visa/earlier-research/visa_dcf.py
```

Run the organized labs from the `Visa` folder:

```bash
python3 lab-06/dcf.py
python3 lab-07/lab07_asbury_pe_analysis.py
python3 lab-08/lab08_visa_triangulation.py
python3 lab-09/proforma.py
python3 lab-10/Lab10_visa_proforma.py
python3 lab-10/Lab10_test_visa_proforma.py
```

## Earlier-lab coverage

The company selection, source register, decision report and Python valuation are now available as materials for the company switch. The root Python introduction notebook remains available and was not altered.

No instructions for Labs 1, 2 or 4 were found in the course folder. Only the SpaceX Lab 3 report and final report were available as structural references. Consequently, this package does **not** claim completion of every past lab or compliance with an unseen rubric. Once the assignment instructions are available, map these materials to each required deliverable and fill any gaps. Do not backdate this research or invent partner contributions or earlier activity logs.

Growth revision: Aidan approved pre-incentive revenue growth of 15%, 14%, 13%, 12%, 11% for FY2026–30. The 3% terminal assumption is retained; the abrupt transition remains disclosed. The original path is a slower-growth comparison in the summary.

## Lab 11 — started September 29, 2026

[Starting checkpoint](lab-11/Lab11_start.md): Visa base reverified at $273.76/share; inputs, assumption table and visible output saved separately. Accepted driver ranges and sensitivity runs are complete; all scenarios pass and the base is restored. See [results](lab-11/Lab11_summary.md). Aidan adopted the AI-assisted prediction under reported revised instructor instructions. Interpretation and an AI-assisted substitute review are saved under the instructor accommodation Aidan reported. No live partner exchange or submission is claimed.
