# Visa | Code and Validation

**Video 2 · Python model · Five-year forecast · Validation results**

---

## 1. Python Data Pipeline

**Visa filings → Reported history → Normalized inputs → Five-year forecast → Valuation**

- **Source data:** Preserved facts from Visa’s FY2025 annual filing and June 2026 quarterly filing, with source references.
- **Trailing results:** FY2025 + nine months of 2026 − nine months of 2025.
- **Forecast starting point:** June reported balances roll forward through a separately labeled October opening estimate.

Reported facts and forecast assumptions remain separate.

---

## 2. Earnings Normalization Bridge

**Reported earnings → Recurring legal costs → Normalized taxes → Normalized earnings**

- Retain recurring litigation expense at **2% of net revenue**.
- Apply a **20% normalized tax rate**.
- Preserve reported history and historical operating cash flow.

**Trailing operating profit: $27.0B reported → $28.3B normalized**

These policies are analyst judgments. The bridge documents their effects; the Python engine applies them directly.

---

## 3. Five-Year Engine Architecture

**Revenue and incentives → Costs and taxes → Working capital and investment**

**Linked income statement + balance sheet + cash-flow statement → Free cash flow → Value per share**

- Five forward annual periods end **October 2027–2031**; these are anniversary years, not Visa fiscal years.
- **Free cash flow:** Operating profit after unlevered tax + depreciation and amortization − capex − working-capital investment.
- **Valuation:** Discount cash flows at WACC, then bridge enterprise value to equity using eligible cash, securities, debt, other claims, and diluted economic shares.

---

## 4. Validation Test Suite

### 28 passing tests in the saved record

**24 integrated tests + 4 workbench tests**

- **Balance-sheet articulation:** Assets equal liabilities plus equity; account balances roll forward.
- **Cash-flow tie-outs:** Operating cash flow and changes in closing cash reconcile.
- **Valuation linkage:** Free cash flow matches the underlying statements.
- **Directional checks:** Higher WACC lowers value with positive cash flows; higher terminal growth raises this model’s value after reinvestment.
- **Error handling:** Deliberate cash and disconnected-cash-flow errors are rejected; invalid inputs are refused and reset restores the base case.

**Reproducibility:** A saved fresh-environment run reproduced model results exactly.

These checks support consistency and reproducibility. They do not prove forecast assumptions. Test results shown here are preserved evidence, not a new live run.

---

## 5. Locked Changed-Input Test Results

**One input changed: terminal growth increased by 50 basis points.**

| Measure | Before | After |
|---|---:|---:|
| Terminal growth | 3.0% | 3.5% |
| Value per share | $267.46 | **$284.26** |
| Recommendation | Do Not Initiate | **Do Not Initiate** |

**Prediction: approximately $284/share**  
**Actual increase: $16.80/share · 6.28%**

- **Held fixed:** Five-year cash flows, WACC, opening balances, and share count.
- **Recalculated:** Terminal earnings, required reinvestment, cash flow, and terminal value.
- **Decision reference:** October 16, 2026 price of **$402.61**; original base input file unchanged.

**Record timing:** Prediction transcription frozen October 19, 2026 at 22:35:24 UTC; additional verification at 22:35:54 UTC.

**Verification disclosure:** Aidan supplied the prediction; Codex ran the verification. The same change had appeared in earlier automated tests. This record does not establish an unexposed prediction or an AI-closed student run.
