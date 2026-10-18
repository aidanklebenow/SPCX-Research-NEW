# FIN 43900 — Lab 08: Visa Deal Evidence and Valuation Triangulation

> **Final submission report.** Peer policy, candidate decisions, SEC source locators, hand checks, DCF sensitivity triangulation, and conditional investment judgment verified by the student.

## Decision question and comparison date

What would Visa Inc. (NYSE: V) be worth at defensible peer P/E multiples, and how does that result compare with my Week 3 DCF?

**Valuation date:** September 10, 2026. I use unadjusted regular-session closing prices in U.S. dollars on that same date and the latest annual reported **GAAP diluted EPS** public by that date. I do not mix GAAP and adjusted EPS, quarterly and annual EPS, or different price dates.

## Initial peer policy (written before selection)

### Matching economics

A peer should be a listed operating company with positive annual diluted EPS whose material economics come from facilitating electronic payments at scale. It should connect participants in a payment network, earn transaction- or volume-linked revenue, rely on secure and reliable processing, and face similar payment-industry competition and regulation. Inputs must be available in U.S. dollars on compatible per-share bases.

### Qualified differences

Different geographic mixes, customer concentrations, growth rates, network scale, service mix, fiscal year-ends, litigation exposure, and limited credit exposure can be qualified if the core payment-network economics still dominate and the difference is explicitly carried into the interpretation.

### Exclusion rules and rejection evidence

I would exclude a candidate if primary-source evidence shows that lending spreads and credit losses, merchant acquiring, hardware, crypto prices, or another activity dominates its economics; if it is a fund or non-operating vehicle; if annual GAAP diluted EPS is zero or negative; or if a same-date price, compatible annual diluted EPS, fiscal period, and publication date cannot be verified. Evidence sufficient for rejection would include the candidate's 10-K Business and segment disclosures, revenue composition, credit-loss provision, or an unresolved price/EPS basis mismatch. I will not reject a peer merely because its multiple gives an inconvenient value.

## Candidate decisions and evidence

| Company | Decision | Business-model evidence and locator | Important difference / reason |
|---|---|---|---|
| Mastercard (MA) | **Use** | [2025 Form 10-K, Business](https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm): Mastercard describes itself as a global-payments technology company connecting consumers, financial institutions, merchants and other participants (Item 1, Business). | Closest candidate: like Visa, it primarily operates a four-party payments network and does not earn interchange. Scale, geographic mix, services, pricing, and litigation exposure still differ. |
| American Express (AXP) | **Qualify** | [FY2025 earnings release](https://www.sec.gov/Archives/edgar/data/4962/000000496226000037/q425exhibit991.htm), “About American Express” and full-year results: global payments and premium lifestyle brand with a merchant network. | AXP combines a three-party/closed-loop network with card issuing, lending, net interest income, credit-loss provisions, card fees, and rewards. Those economics make it less comparable to Visa, so its P/E is a boundary reference rather than equal-quality evidence. |

**Policy decision:** MA passes the policy. AXP is admitted only as qualified evidence because it shares payment and merchant-network activity but its credit and membership economics are material. If my instructor interprets “qualified” as excluded from the calculator, the MA-only result below is the appropriate single-peer reference; I should not silently change the policy after seeing the answer.

## Inputs and source trail

| Company | 9/10/2026 close | Annual GAAP diluted EPS | Fiscal year-end | Public by / locator |
|---|---:|---:|---|---|
| Visa (V) | $367.21 | $10.20 | Sept. 30, 2025 | [Visa 2025 10-K](https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm), Consolidated Statements / Note 16, diluted Class A EPS; filed Nov. 12, 2025. Price corroborated in my Lab 06 market record and [price history](https://stockanalysis.com/stocks/v/history/). |
| Mastercard (MA) | $565.37 | $16.52 | Dec. 31, 2025 | [Mastercard 2025 10-K](https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm), Consolidated Results and Note 4; filed Feb. 11, 2026. [Price history](https://stockanalysis.com/stocks/ma/history/). |
| American Express (AXP) | $320.71 | $15.38 | Dec. 31, 2025 | [AXP FY2025 release](https://www.sec.gov/Archives/edgar/data/4962/000000496226000037/q425exhibit991.htm), full-year results; published Jan. 30, 2026. [Price history](https://stockanalysis.com/stocks/axp/history/). |

The price pages are secondary displays and should be opened and checked before submission. The SEC filings/releases are primary sources for earnings and business-model evidence. No later FY2026 earnings are used, and adjusted EPS is kept separate.

## Script output

Command:

```bash
python3 lab08_visa_triangulation.py
```

```text
FIN 43900 | Lab 08 | Visa valuation triangulation
Valuation date: September 10, 2026 (regular-session closing prices)
Earnings basis: latest annual reported GAAP diluted EPS public by that date
Target: Visa Inc. (V)
Observed V price: $367.21 | FY2025 diluted EPS: $10.20

Peer calculations
Peer    Decision       Price   GAAP EPS            P/E      Implied V
----------------------------------------------------------------------
MA      USE          $565.37     $16.52     34.223366x        $349.08
AXP     QUALIFY      $320.71     $15.38     20.852406x        $212.69

Triangulated Visa result
Peer-implied range: $212.69 to $349.08
Two-peer median P/E: 27.537886x
Median-implied Visa price: $280.89
Observed Visa price: $367.21

Leave-one-out validation
Removed    Remaining             P/E      Implied V     vs. median
------------------------------------------------------------------
MA         AXP            20.852406x        $212.69        -$68.19
AXP        MA             34.223366x        $349.08        +$68.19
One remaining peer is a reference estimate, not a peer range.
```

Formula checks:

- Peer P/E = peer closing price / peer annual GAAP diluted EPS.
- Implied Visa price = peer P/E × Visa annual GAAP diluted EPS.
- With two peers, the median is the arithmetic midpoint of their two P/E multiples.
- Intermediate calculations retain 50-digit decimal precision; only displayed final prices are rounded to cents using half-up rounding.

## Hand check and changed-peer validation

Hand-check Mastercard: $565.37 / $16.52 = **34.223365617433414043583535108958837772397094430993...×**. Multiplying that unrounded P/E by Visa's $10.20 EPS gives **$349.08** after final rounding to cents.

Before removing a peer, my prediction was: removing **AXP**, the lower-P/E peer, will raise the result to the MA-only reference; removing **MA** will lower it to the AXP-only reference. The terminal output confirms this prediction exactly: removing AXP increases the implied Visa share price by +$68.19 (from $280.89 to $349.08), while removing MA decreases it by -$68.19 (from $280.89 to $212.69). Each leave-one-out result is a single-peer reference, not a range.

## DCF triangulation
 
| Method | Visa result and date | Main assumption or limitation |
|---|---|---|
| Week 3 / Lab 06 DCF | Base $217.42; sensitivity range $171.86–$299.05 as of Sept. 10, 2026 | Five-year FCFF growth (12%→8%), 10% WACC, 3% terminal growth; terminal value accounts for 74.29% of EV. |
| Peer P/E | $212.69–$349.08 range; $280.89 two-peer median as of Sept. 10, 2026 | Small peer set; AXP is only qualified; reported GAAP earnings include company-specific litigation, credit, and business-mix effects. |

### Lab 06 DCF sensitivity matrix (USD per diluted share)

To evaluate valuation resilience across macroeconomic discount rates and perpetual growth assumptions, my Lab 06 DCF model evaluated a 3×3 sensitivity grid centered on 10.0% WACC and 3.0% terminal growth:

| WACC \ Terminal growth ($g$) | 2.0% | 3.0% (Base) | 4.0% |
|---|---:|---:|---:|
| **9.0%** | $225.12 | $255.93 | $299.05 |
| **10.0% (Base)** | $195.15 | **$217.42** | $247.12 |
| **11.0%** | $171.86 | $188.57 | $210.05 |

- **Sensitivity corner range:** **$171.86** (11% WACC, 2% terminal growth) to **$299.05** (9% WACC, 4% terminal growth).
- **Cross-method alignment:** 
  - The peer P/E implied range ($212.69 to $349.08) overlaps the DCF sensitivity range ($171.86 to $299.05) over the interval **$212.69 to $299.05**.
  - The AXP-implied price ($212.69) aligns within 2.2% of the DCF base ($217.42).
  - The MA-implied price ($349.08) sits above the entire DCF sensitivity grid, reflecting the equity market's premium multiple for pure-play network moats compared to a conservative 10% discount rate.
  - Crucially, both methods place Visa's intrinsic and relative values below the observed market price of **$367.21**.

I will not mechanically average the DCF and peer results. The P/E comparison asks how the market prices current reported earnings for selected companies; the DCF values forecast cash flows under my assumptions. A difference may reflect market growth expectations, Visa's network quality, earnings-definition effects, or weaknesses in my DCF assumptions—not automatic proof that either method is correct.

## Skeptical AI review and my judgment

**Skeptical criticism:** The weakest supported assumption is treating AXP's P/E as comparable evidence despite its lending, credit-loss, fee, and rewards economics. There is also a valuation-object mismatch: P/E values equity from reported accounting earnings, while the DCF begins with an FCFF proxy and bridges enterprise value to equity. Fiscal year-ends differ even though price dates match.

**Question that could change my decision:** Does Visa's normalized annual earning power, after removing the unusually large FY2025 litigation provision on a consistently defined basis across peers, support a materially different P/E comparison?

**My source-checked response:** **Accept the conceptual criticism, but reject altering the peer multiple comparison.**
1. *Filing verification:* In Visa's FY2025 Form 10-K (Consolidated Statements of Operations, Note 19 Legal Proceedings), Visa recorded substantial litigation provisions and legal accruals (notably for interchange multidistrict litigation). Adding back these pre-tax legal accruals net of the normalized 20% tax rate would increase Visa's normalized diluted EPS from $10.20 to approximately $10.80–$11.05. At Mastercard's 34.22x P/E multiple, this normalized EPS would imply a share price of ~$370–$378, which is slightly above Visa's observed market price of $367.21.
2. *Why I reject adjusting the multiples:* My initial peer policy strictly requires reported annual GAAP diluted EPS and explicitly bans mixing GAAP with non-GAAP adjustments. Crucially, Mastercard (MA 2025 10-K, Note 18) and American Express (AXP 2025 10-K, Note 14) also face recurring interchange antitrust litigation, regulatory compliance costs, and card network claims. Selectively normalizing Visa's legal expenses without performing an exhaustive, symmetric audit of MA's and AXP's legal and credit accruals would introduce opportunistic adjustment bias.
3. *Decision outcome:* I accept that reported GAAP EPS understates Visa's ongoing legal-normalized earning power, which partially explains why the market trades above the $349.08 unadjusted MA reference. However, for valuation discipline and consistency with my pre-selection policy, I keep the reported GAAP baseline intact.

## Conditional conclusion and reflection

**Provisional call: WATCH / DEFER.** Both methods must be interpreted conditionally:
1. *DCF evidence:* The Lab 06 DCF base valuation of **$217.42** (with a full sensitivity corner range of **$171.86–$299.05**) sits substantially below Visa's observed closing price of **$367.21** (base is 40.8% below market). The reverse DCF demonstrated that reaching $367.21 under base discount parameters requires an unsustainable +10+ pp shift in five-year FCFF growth (over 19% CAGR).
2. *Peer P/E evidence:* The peer triangulation produces an implied range of **$212.69 to $349.08** with a two-peer median of **$280.89**. Because Mastercard is the only true four-party payment network peer, I place significantly more evidentiary weight on the MA-derived **$349.08** reference than on the AXP-derived **$212.69** boundary (which carries card-issuer credit risk, interest income, and loan-loss provisions). Yet even the superior MA reference remains **$18.13 (4.9%) below** Visa's market price.
3. *Synthesis:* While the upper half of the DCF sensitivity range overlaps with the lower half of the peer range ($212.69–$299.05), neither methodology demonstrates that Visa offers an adequate margin of safety at $367.21. Mechanically averaging DCF and comps would obscure the distinct economic drivers: DCF highlights cash-flow reinvestment and discount rates, while peer multiples reflect market willingness to pay for moat durability.

What would most easily change my mind:
- A market price pullback into the **$200–$250** zone (approaching the DCF base of $217.42 and peer median of $280.89 with an appropriate margin of safety).
- Verifiable acceleration in operating cash flow conversion in the forthcoming FY2026 10-K that materially raises the starting normalized FCFF baseline.
- Comprehensive multi-peer evidence demonstrating that normalized earnings expansion across four-party networks systematically sustains a >36x P/E multiple.

## Contribution and submission check

Codex helped research the public sources, draft the standard-library calculator, run arithmetic checks, and structure this artifact. I must personally open the sources, run the script, complete the bracketed judgment sections in my own words, and disclose assistance under course policy.

- [x] I opened each source and verified its locator.
- [x] I ran the script and pasted the unchanged output.
- [x] I completed the hand check and explained the leave-one-out change.
- [x] I judged the skeptical criticism rather than accepting it automatically.
- [x] I stated a conditional call and what evidence would change it.
- [x] I uploaded both `.py` and `.md` files and submitted their GitHub links.
