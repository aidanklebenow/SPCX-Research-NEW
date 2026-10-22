# Lab 15 — Portfolio Stability Decision

**Question:** Which mix carries the least risk while meeting the mandate—and does the answer survive a one-point change in one estimate?

Built with AI help, a learning demonstration, not investment advice.

## Start here

- [Lab write-up: verified results, interpretation, and remaining personal checkout](Lab15_Writeup.md)
- [Styled Mermaid flowcharts and how they align with the app](Portfolio_App_Flowchart.md)
- [Prices, provenance, and validation notes](Data_and_Validation.md)

## Run the app

From this folder, using Python 3.10 or newer:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py --browser.gatherUsageStats false
```

Streamlit prints the local URL and opens the app. On the author's original workspace, the existing environment can run it with `.venv/bin/python -m streamlit run model/src/app.py --browser.gatherUsageStats false`. A local URL works only while that computer's app is running; GitHub hosts the source and rendered write-up, not a running Streamlit service.

## What the app does

- **Dashboard:** Meridian training and bundled five-ETF universes, CSV upload, editable estimates, reserve checkboxes, two optimized allocations, and the largest weight change.
- **Manual allocation:** sliders automatically rebalance the other weights so the total stays at 100%; charts and return/reserve checks update immediately.
- **Charts:** allocation donuts, allocation comparison bars, risk versus return, adjusted historical ETF growth, and intraday market prices.
- **Market quotes:** free Yahoo Finance observations refreshed every 60 seconds while the page is active, with trade and fetch timestamps. Quotes may be delayed; after hours the latest regular-session trade is shown. Failed quotes are labeled unavailable.
- **How it works:** a plain-English explanation of the controls, math, and investment vocabulary.
- **Lab notebook:** enter your own partner observations and decision, then download the session record as Markdown.
- **Light/dark mode:** native Streamlit theme colors for text, panels, and chart labels. Change theme in the upper-right menu → Settings → Theme.

The optimizer enforces the return estimate and reserve minimum on a long-only 5-point grid. It does not guarantee returns or losses, or enforce additional issuer and trading-policy rules. Market quotes are kept separate from the completed monthly data used for the lab.

## Data

[prices.csv](prices.csv) has 61 month-end adjusted prices for SGOV, IEF, LQD, VTI, and VXUS, from 2021-09-30 through 2026-09-30, giving 60 monthly returns. Downloaded free from Yahoo Finance on 2026-10-22. [sources.json](sources.json) records exact URLs, download timestamps, and sampled observations. Original responses are in [sources](sources/).

To refresh the historical dataset after a later month completes:

```bash
.venv/bin/python download_lab15_prices.py
```

## Verification

```bash
.venv/bin/python portfolio.py
.venv/bin/python -m unittest discover -s tests -v
```

The original Lab 14 output is preserved in [Lab14_Unchanged_Output.txt](Lab14_Unchanged_Output.txt). Meridian matches all three lab acceptance cases. Tests cover CSV estimation, infeasibility, slider totals, manual portfolio metrics, scenario editing, window changes, page navigation, and trade-versus-fetch timestamps. Quote tests use fixtures; actual Yahoo connectivity was also checked separately for all five ETFs.

## Student-authored work still required

The write-up clearly identifies the partner attack, partner code question, and final personal allocation decision that must be supplied by the student. Numerical results and an explicitly labeled decision draft are provided; no partner activity or quiz submission is fabricated.
