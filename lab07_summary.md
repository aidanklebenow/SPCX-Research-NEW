# FIN 43900 — Lab 07: Asbury P/E comparison

Draft for student review. Fill in teammate information and the GitHub link, review the peer decisions, and confirm the attestation before submitting.

Teammate(s): [Enter actual names, or 'None' if accurate.]

## DISCOVER

Our initial implementation left peer-input safeguards and the leave-one-out dollar change unresolved. Reading the full lab and worked case clarified them. Exact calculations show that removing the higher-multiple GPI lowers the estimate; two peers provide a fragile comparison, not proof of fair value. P/E measures dollars of share price per dollar of annual EPS. A lower P/E may reflect weaker growth, higher risk, or unusually high earnings.

## DEFINE

Estimate ABG's share price by applying comparable retailers' P/E multiples to ABG EPS. The frozen case pairs December 31, 2024 prices with subsequently reported FY2024 total GAAP diluted EPS; it is retrospective, not a tradable information set available at year-end. Use consistent earnings and stock-split definitions. P/E values equity directly: no cash/debt bridge. Use AN for its similar vehicle retail and service/parts activities, while noting AutoNation Finance. Qualify GPI for its U.S./U.K. exposure and 54-dealership Inchcape acquisition in 2024. These are case-supported draft peer decisions for the student to review. The Visa DCF is prior-work context; Lab 07 uses ABG.

## GOOD QUESTION

How do inventory normalization and used-vehicle margin trends affect sustainable earnings across ABG, AN, and GPI? If FY2024 earnings reflect different points in that cycle, a low P/E could reflect temporarily high EPS rather than an attractive price. This is a proposed next question, not a finding.

## MY CONTRIBUTION

I supplied the case inputs, identified my saved Visa Lab 06 materials, provided the Lab 07 instructions, and specified the calculator and summary requirements. Codex read the lab and worked case, wrote the script, and ran automated checks. This record does not establish that I independently performed a hand calculation, discussed the case with a teammate, or completed the work during class; I must add only actions I actually performed.

## TEST / CHECK / RESULT

The built-in frozen-case checks passed: AN P/E 10.037825x; GPI P/E 11.450149x; median 10.743987x; implied ABG range $215.81–$246.18; median estimate $231.00. Removing GPI gives $215.81 and a -$15.18 change calculated before rounding. AN alone is a single reference estimate, not a range. Removing AN gives $246.18, a +$15.18 change. Checks also cover duplicate/target exclusion, invalid inputs, zero/one peer, and invalid target inputs. These fixed-case checks remain fixed if editable inputs change; the calculation output above reflects the current inputs.

## OPTIONAL ARTIFACT LINK

[Insert GitHub link to lab07_asbury_pe_analysis.py]

## ATTESTATION

Required wording below is for student confirmation only; class attendance and teammate participation have not been verified. Submit it only if accurate, after filling in teammate information.
I completed this work in today’s class with the teammate(s) listed above, and this checkout is truthful.


## Files and sources

- [Python calculator](lab07_asbury_pe_analysis.py)
- [Lab instructions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/lab-07-comparable-policy.md)
- [Worked case and primary-source locators](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/teach-comps-worked-example.md)

Run from your AIFinance2026 folder:

```bash
python3 lab07_asbury_pe_analysis.py
```
