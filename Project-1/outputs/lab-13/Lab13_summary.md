# Lab 13 — Portfolio Mandate Defense

## 1. Statement Classification (S1–S10)

- **S1 (Seven-year horizon; annual rebalancing): Hard Constraint.** Reason: Defines structural governance timeline and operational cadence.
- **S2 (CPI + 4% net return over rolling five-year periods): Objective.** Reason: Establishes quantitative return target above inflation.
- **S3 ($0.75M quarterly payouts; twelve months held in eligible reserves): Hard Constraint.** Reason: Mandatory liquidity requirement to service scheduled distributions.
- **S4 (60% global equity / 40% U.S. investment-grade bond benchmark): Preference / Benchmark.** Reason: Serves as strategic performance reference point rather than an absolute rule.
- **S5 (Long-only; no borrowing, short sales, or derivatives): Hard Constraint.** Reason: Explicit prohibition against leverage and derivative instruments.
- **S6 (Single-issuer maximum of 8%): Hard Constraint.** Reason: Quantitative concentration ceiling to mitigate credit risk.
- **S7 (Annual turnover maximum of 25% without approval): Hard Constraint.** Reason: Operational trading limit designed to control transaction costs.
- **S8 (At least 90% redeemable within five business days): Hard Constraint.** Reason: Portfolio liquidity floor ensuring rapid asset liquidation capability.
- **S9 (Calendar-year loss no greater than 10%, with no measure or breach rule): Unverifiable Promise / Missing.** Reason: Lacks defined measurement mechanics and breach protocols, requiring CIO clarification before enforcement.
- **S10 (No stated sector/ESG/tax/home-bias preference; optimization objective unspecified): Missing.** Reason: Absence of guiding parameters requires explicit client clarification before portfolio construction.

## 2. Code-Understanding Quiz

Issuer aggregation line in `src/mandate.py`:

```python
companies[info['issuer']] = companies.get(info['issuer'], 0.0) + weight
```

**Why checking individual holdings fails for B:** Candidate B holds different securities from the same parent issuer across separate allocations that individually pass the 8% threshold, but their combined exposure breaches the single-issuer maximum. Evaluating line items in isolation ignores ultimate credit concentration.

## 3. Candidate D Judgment & Skeptical Colleague Response

**Judgment:** Candidate D satisfies all quantitative hard constraints (long-only, liquidity, max issuer limits), but creates a severe long-term suitability risk regarding the CPI + 4% real return objective (S2) by moving into 100% cash.

**Skeptical Colleague Response:**

> While shifting 100% into cash technically satisfies all our quantitative hard constraints like liquidity and long-only limits, we are completely abandoning our core return objective. If we hold cash indefinitely, inflation will erode our purchasing power, meaning we fail our mandate by default even if we avoid market drawdowns.

## 4. CIO Question & Breach Consequence

**Question:** How is the 10% calendar-year loss limit measured (mark-to-market versus realized year-end valuation), and what exact remediation protocol is triggered upon breach?

**Consequence on portfolio design:** Mark-to-market measurement alone does not automatically require liquidation. Any portfolio adjustment depends entirely on the CIO's specified breach procedure (e.g., whether a formal waiver is granted or a mandatory rebalancing haircut is enforced), which dictates our risk budgeting tolerance during market drawdowns.

## 5. Investment Policy Statement (IPS) & Mapping

An Investment Policy Statement (IPS) serves as the foundational governance document establishing a portfolio's return objectives, risk tolerance, and structural constraints. Mapping S1–S10: S1 and S2 establish governance cadence and return objectives; S3, S5, S6, S7, and S8 set enforceable hard constraints; S4 acts as the benchmark preference; and S9 and S10 represent unverifiable promises or missing parameters requiring clarification.

## 6. Reflection

Passing every checkable quantitative rule does not guarantee suitability because automated checks cannot evaluate qualitative governance factors or unquantified strategic risks. The statement type I found hardest to classify was the calendar-year loss rule (S9), as it sits awkwardly between an investor's emotional risk tolerance and a clear accounting mandate.

## 7. Project 2 Client Mandate Draft

- **Objective:** Achieve long-term capital appreciation with a target net annualized return of 7.5% over a 5-year horizon.
- **Hard Constraints:** Maximum single-issuer concentration of 7%, minimum liquidity buffer of 10% in short-duration Treasuries, and zero tolerance for calendar-year realized losses.
- **Client Question:** What is your exact liquidity withdrawal schedule over the next 24 months to ensure our fixed-income duration matching remains aligned?

## 8. Python Script Output and Validation

The reserve minimum is computed as four quarterly distributions of $0.75 million divided by the $100 million reserve: **3.0%**.

### Candidates A–D

Command: `python3 src/mandate.py`

```text
Reserve minimum: 3.0%

Candidate A
Weights sum to 100: 100.0% pass
Long-only (lowest weight): 0.0% pass
Reserve >= 3.0%: 14.0% pass
Redeemable in 5 days >= 90%: 100.0% pass
Largest single company <= 8%: 0.0% pass
Calendar-year loss: requires CIO clarification
passes every checkable rule

Candidate B
Weights sum to 100: 100.0% pass
Long-only (lowest weight): 0.0% pass
Reserve >= 3.0%: 1.0% FAIL
Redeemable in 5 days >= 90%: 85.0% FAIL
Largest single company <= 8%: 9.0% FAIL
Calendar-year loss: requires CIO clarification
fails 3 rule(s)

Candidate C
Weights sum to 100: 100.0% pass
Long-only (lowest weight): 0.0% pass
Reserve >= 3.0%: 2.0% FAIL
Redeemable in 5 days >= 90%: 100.0% pass
Largest single company <= 8%: 8.0% pass
Calendar-year loss: requires CIO clarification
fails 1 rule(s)

Candidate D
Weights sum to 100: 100.0% pass
Long-only (lowest weight): 0.0% pass
Reserve >= 3.0%: 100.0% pass
Redeemable in 5 days >= 90%: 100.0% pass
Largest single company <= 8%: 0.0% pass
Calendar-year loss: requires CIO clarification
passes every checkable rule
```

Candidate A passes every checkable rule. Candidate B fails the reserve, liquidity, and issuer-concentration rules; its Acme exposure is 5% bonds plus 4% stock, totaling 9%. Candidate C fails only the reserve rule. Candidate D is 100% cash and passes all five checks. Passing these checks does not establish achievement of the return objective.

### Negative-weight probe

For candidate A, Cash was changed to -2% and the global equity index fund to 64%. All other weights were held fixed.

```text
Reserve minimum: 3.0%

Candidate A negative-weight probe
Weights sum to 100: 100.0% pass
Long-only (lowest weight): -2.0% FAIL
Reserve >= 3.0%: 10.0% pass
Redeemable in 5 days >= 90%: 100.0% pass
Largest single company <= 8%: 0.0% pass
Calendar-year loss: requires CIO clarification
fails 1 rule(s)
```

The probe fails only long-only. Weights still sum to 100%, and the reserve remains sufficient at 10%. The original candidate A inputs are preserved after the probe.
