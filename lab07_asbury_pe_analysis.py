"""FIN 43900 Lab 07. Save this file as lab07_asbury_pe_analysis.py.

Run from AIFinance2026: python3 lab07_asbury_pe_analysis.py
Standard library only; no downloads, installations, or file writes at runtime.
Fraction arithmetic preserves exact input ratios until final display rounding.
"""

from fractions import Fraction
from statistics import median


# EDITABLE INPUTS: use strings to preserve the intended decimal values.
# Frozen December 31, 2024 prices; subsequently reported FY2024 total GAAP
# diluted EPS. Keep prices and EPS on a consistent stock-split basis.
TARGET = {"ticker": "ABG", "name": "Asbury Automotive",
          "price": "243.03", "eps": "21.50"}
PEERS = [
    {"ticker": "AN", "name": "AutoNation", "price": "169.84", "eps": "16.92"},
    {"ticker": "GPI", "name": "Group 1 Automotive", "price": "421.48", "eps": "36.81"},
]
LAB_URL = "https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/lab-07-comparable-policy.md"
CASE_URL = "https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/teach-comps-worked-example.md"


def positive(value):
    """Return an exact positive number, or None for unusable input."""
    if value is None or isinstance(value, bool):
        return None
    try:
        number = Fraction(str(value).strip())
    except (ValueError, ZeroDivisionError, TypeError):
        return None
    return number if number > 0 else None


def ticker(company):
    return str(company.get("ticker") or "").strip().upper()


def fixed(value, places):
    """Exact round-half-up formatting; never round a calculation input."""
    scale = 10 ** places
    scaled = abs(value) * scale
    units, remainder = divmod(scaled.numerator, scaled.denominator)
    if remainder * 2 >= scaled.denominator:
        units += 1
    sign = "-" if value < 0 and units else ""
    return f"{sign}{units // scale:,}.{units % scale:0{places}d}"


def money(value):
    if value is None:
        return "not meaningful"
    return ("-$" if value < 0 else "$") + fixed(abs(value), 2)


def multiple(value):
    return "not meaningful" if value is None else fixed(value, 6) + "x"


def analyze(target, peers):
    """Deduplicate by normalized ticker; first occurrence wins, with a notice."""
    rows, notices, seen = [], [], set()
    for peer in peers:
        symbol = ticker(peer)
        if not symbol:
            notices.append("Excluded peer with missing ticker: identity cannot be verified.")
            continue
        if symbol == ticker(target):
            notices.append(f"Excluded {symbol}: target cannot be its own peer.")
            continue
        if symbol in seen:
            notices.append(f"Excluded duplicate {symbol}: first occurrence retained; review conflicting inputs.")
            continue
        seen.add(symbol)
        price, eps = positive(peer.get("price")), positive(peer.get("eps"))
        pe = price / eps if price is not None and eps is not None else None
        rows.append({"ticker": symbol, "price": price, "eps": eps, "pe": pe})

    valid = {row["ticker"]: row["pe"] for row in rows if row["pe"] is not None}
    target_eps = positive(target.get("eps"))
    target_price = positive(target.get("price"))
    center = median(valid.values()) if valid else None

    def implied(pe):
        return pe * target_eps if pe is not None and target_eps is not None else None

    baseline = implied(center)
    removals = []
    for row in rows:
        remaining = {key: value for key, value in valid.items() if key != row["ticker"]}
        remaining_median = median(remaining.values()) if remaining else None
        estimate = implied(remaining_median)
        change = estimate - baseline if estimate is not None and baseline is not None else None
        removals.append({"excluded": row["ticker"], "remaining": remaining,
                         "median": remaining_median, "estimate": estimate, "change": change})
    return {"rows": rows, "notices": notices, "valid": valid,
            "target_eps": target_eps, "target_price": target_price,
            "median": center, "minimum": implied(min(valid.values())) if valid else None,
            "estimate": baseline, "maximum": implied(max(valid.values())) if valid else None,
            "removals": removals}


def self_checks():
    """Fixed case checks remain independent of edits to the working inputs."""
    target = {"ticker": "ABG", "price": "243.03", "eps": "21.50"}
    peers = [{"ticker": "AN", "price": "169.84", "eps": "16.92"},
             {"ticker": "GPI", "price": "421.48", "eps": "36.81"}]
    result = analyze(target, peers)
    checks = [
        multiple(result["valid"]["AN"]) == "10.037825x",
        multiple(result["valid"]["GPI"]) == "11.450149x",
        multiple(result["median"]) == "10.743987x",
        money(result["minimum"]) == "$215.81",
        money(result["estimate"]) == "$231.00",
        money(result["maximum"]) == "$246.18",
        money(result["removals"][1]["estimate"]) == "$215.81",
        money(result["removals"][1]["change"]) == "-$15.18",
        money(result["removals"][0]["change"]) == "$15.18",
    ]
    duplicate = dict(peers[0], ticker=" an ")
    checks.append(len(analyze(target, peers + [duplicate, target])["valid"]) == 2)
    for value in (None, "", "bad", "NaN", "Infinity", "0", "-1", True):
        for field in ("price", "eps"):
            invalid = dict(peers[0], **{field: value})
            checks.append(not analyze(target, [invalid])["valid"])
    single = analyze(target, peers[:1])
    checks.extend([len(single["valid"]) == 1,
                   single["removals"][0]["estimate"] is None,
                   analyze(target, []) ["median"] is None,
                   analyze(dict(target, eps=None), peers)["estimate"] is None,
                   analyze(dict(target, price=None), peers)["estimate"] == result["estimate"],
                   money(Fraction("1.005")) == "$1.01"])
    if not all(checks):
        raise AssertionError("Lab 07 validation failed.")
    return len(checks)


def print_summary():
    print("\nLAB SUMMARY — draft for student review")
    print("Teammate(s): [Enter actual names, or 'None' if accurate.]")
    sections = [
        ("DISCOVER", "Our initial implementation left peer-input safeguards and the "
         "leave-one-out dollar change unresolved. Reading the full lab and worked case "
         "clarified them. Exact calculations show that removing the higher-multiple GPI "
         "lowers the estimate; two peers provide a fragile comparison, not proof of fair value. "
         "P/E measures dollars of share price per dollar of annual EPS. A lower P/E may "
         "reflect weaker growth, higher risk, or unusually high earnings."),
        ("DEFINE", "Estimate ABG's share price by applying comparable retailers' P/E "
         "multiples to ABG EPS. The frozen case pairs December 31, 2024 prices with "
         "subsequently reported FY2024 total GAAP diluted EPS; it is retrospective, "
         "not a tradable information set available at year-end. Use consistent earnings "
         "and stock-split definitions. P/E values equity directly: no cash/debt bridge. "
         "Use AN for its similar vehicle retail and service/parts activities, while noting "
         "AutoNation Finance. Qualify GPI for its U.S./U.K. exposure and 54-dealership "
         "Inchcape acquisition in 2024. These are case-supported draft peer decisions "
         "for the student to review. The Visa DCF is prior-work context; Lab 07 uses ABG."),
        ("GOOD QUESTION", "How do inventory normalization and used-vehicle margin trends "
         "affect sustainable earnings across ABG, AN, and GPI? If FY2024 earnings reflect "
         "different points in that cycle, a low P/E could reflect temporarily high EPS "
         "rather than an attractive price. This is a proposed next question, not a finding."),
        ("MY CONTRIBUTION", "I supplied the case inputs, identified my saved Visa Lab 06 "
         "materials, provided the Lab 07 instructions, and specified the calculator and "
         "summary requirements. Codex read the lab and worked case, wrote the script, "
         "and ran automated checks. This record does not establish that I independently "
         "performed a hand calculation, discussed the case with a teammate, or completed "
         "the work during class; I must add only actions I actually performed."),
        ("TEST / CHECK / RESULT", "The built-in frozen-case checks passed: AN P/E "
         "10.037825x; GPI P/E 11.450149x; median 10.743987x; implied ABG range "
         "$215.81–$246.18; median estimate $231.00. Removing GPI gives $215.81 and "
         "a -$15.18 change calculated before rounding. AN alone is a single reference "
         "estimate, not a range. Removing AN gives $246.18, a +$15.18 change. "
         "Checks also cover duplicate/target exclusion, invalid inputs, zero/one peer, "
         "and invalid target inputs. These fixed-case checks remain fixed if editable "
         "inputs change; the calculation output above reflects the current inputs."),
        ("OPTIONAL ARTIFACT LINK", "[Insert GitHub link to lab07_asbury_pe_analysis.py]"),
        ("ATTESTATION", "Required wording below is for student confirmation only; "
         "class attendance and teammate participation have not been verified. "
         "Submit it only if accurate, after filling in teammate information.\n"
         "I completed this work in today’s class with the teammate(s) listed above, and this checkout is truthful."),
    ]
    for heading, body in sections:
        print(f"\n{heading}:\n{body}")


def main():
    count = self_checks()
    result = analyze(TARGET, PEERS)
    print("FIN 43900 | Lab 07 | Asbury comparable-company P/E analysis")
    print("File: lab07_asbury_pe_analysis.py")
    print("Run from AIFinance2026: python3 lab07_asbury_pe_analysis.py")
    print(f"Validation: PASS ({count} checks)")
    print(f"Lab: {LAB_URL}\nWorked case: {CASE_URL}")
    print("Basis: December 31, 2024 prices / FY2024 total GAAP diluted EPS.")
    print("Retrospective comparison; exact fractions until display rounding; no cash/debt bridge.")
    print(f"\nTarget: {TARGET.get('name', '')} ({ticker(TARGET)})")
    print(f"Price: {money(result['target_price'])}; EPS: {money(result['target_eps'])}")
    observed = (result["target_price"] / result["target_eps"]
                if result["target_price"] is not None and result["target_eps"] is not None else None)
    print(f"Observed target P/E (excluded from peers): {multiple(observed)}")
    for notice in result["notices"]:
        print(notice)
    print("\nPeer | Price | EPS | P/E | Implied target price")
    for row in result["rows"]:
        implied = (row["pe"] * result["target_eps"]
                   if row["pe"] is not None and result["target_eps"] is not None else None)
        print(f"{row['ticker']} | {money(row['price'])} | {money(row['eps'])} | "
              f"{multiple(row['pe'])} | {money(implied)}")
        if row["pe"] is None:
            print("  Not meaningful: missing, nonnumeric, or nonpositive price/EPS; excluded from aggregates.")
    print(f"\nValid peer count: {len(result['valid'])}")
    if not result["valid"]:
        print("No usable peers; no estimate or range.")
    else:
        print(f"Median peer P/E: {multiple(result['median'])}")
        if result["target_eps"] is None:
            print("Implied prices not meaningful: target EPS must be positive and available.")
        elif len(result["valid"]) == 1:
            print(f"Single-peer reference estimate: {money(result['estimate'])}; no range.")
        else:
            print(f"Minimum-implied price: {money(result['minimum'])}")
            print(f"Median-implied price: {money(result['estimate'])}")
            print(f"Maximum-implied price: {money(result['maximum'])}")
            print(f"Peer-implied range: {money(result['minimum'])}–{money(result['maximum'])}")
    print("\nLEAVE-ONE-OUT ANALYSIS (changes use unrounded estimates)")
    for removal in result["removals"]:
        remaining = removal["remaining"]
        print(f"Remove {removal['excluded']}; remaining usable peers: {', '.join(remaining) or 'none'}")
        if not remaining:
            print("  No estimate; no peers remain. Dollar change unavailable.")
        else:
            print(f"  Median P/E: {multiple(removal['median'])}; "
                  f"median-implied price: {money(removal['estimate'])}; "
                  f"change: {money(removal['change'])}")
            if len(remaining) == 1:
                print("  One remaining peer: single reference estimate, no range.")
    if not result["removals"]:
        print("No retained peer rows to remove.")
    print_summary()


if __name__ == "__main__":
    main()
