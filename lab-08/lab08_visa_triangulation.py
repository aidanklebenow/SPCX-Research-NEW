"""FIN 43900 Lab 08: Visa peer P/E valuation triangulation.

Run: python3 lab08_visa_triangulation.py
Inputs are hard-coded, sourced historical observations; no data is fetched.
P/E = peer price / peer GAAP diluted EPS.
Implied Visa price = peer P/E * Visa GAAP diluted EPS.
"""

from decimal import Decimal, ROUND_HALF_UP, localcontext
from statistics import median


VALUATION_DATE = "September 10, 2026"
TARGET = {
    "name": "Visa Inc.",
    "ticker": "V",
    "price": Decimal("367.21"),
    "eps": Decimal("10.20"),
    "fiscal_period": "FY ended September 30, 2025",
}
PEERS = (
    {
        "name": "Mastercard Incorporated",
        "ticker": "MA",
        "price": Decimal("565.37"),
        "eps": Decimal("16.52"),
        "decision": "USE",
    },
    {
        "name": "American Express Company",
        "ticker": "AXP",
        "price": Decimal("320.71"),
        "eps": Decimal("15.38"),
        "decision": "QUALIFY",
    },
)


def money(value):
    """Format a final dollar result to cents using conventional half-up rounding."""
    rounded = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"${rounded:,.2f}"


def multiple(value):
    """Show a multiple to six decimals without changing the stored calculation."""
    shown = value.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
    return f"{shown:.6f}x"


def main():
    with localcontext() as context:
        context.prec = 50
        peer_pes = {peer["ticker"]: peer["price"] / peer["eps"] for peer in PEERS}
        implied = {ticker: pe * TARGET["eps"] for ticker, pe in peer_pes.items()}
        median_pe = median(peer_pes.values())
        median_price = median_pe * TARGET["eps"]

        print("FIN 43900 | Lab 08 | Visa valuation triangulation")
        print(f"Valuation date: {VALUATION_DATE} (regular-session closing prices)")
        print("Earnings basis: latest annual reported GAAP diluted EPS public by that date")
        print(f"Target: {TARGET['name']} ({TARGET['ticker']})")
        print(f"Observed V price: {money(TARGET['price'])} | FY2025 diluted EPS: {money(TARGET['eps'])}")

        print("\nPeer calculations")
        print(f"{'Peer':<7} {'Decision':<9} {'Price':>10} {'GAAP EPS':>10} {'P/E':>14} {'Implied V':>14}")
        print("-" * 70)
        for peer in PEERS:
            ticker = peer["ticker"]
            print(
                f"{ticker:<7} {peer['decision']:<9} {money(peer['price']):>10} "
                f"{money(peer['eps']):>10} {multiple(peer_pes[ticker]):>14} "
                f"{money(implied[ticker]):>14}"
            )

        low = min(implied.values())
        high = max(implied.values())
        print("\nTriangulated Visa result")
        print(f"Peer-implied range: {money(low)} to {money(high)}")
        print(f"Two-peer median P/E: {multiple(median_pe)}")
        print(f"Median-implied Visa price: {money(median_price)}")
        print(f"Observed Visa price: {money(TARGET['price'])}")

        print("\nLeave-one-out validation")
        print(f"{'Removed':<10} {'Remaining':<10} {'P/E':>14} {'Implied V':>14} {'vs. median':>14}")
        print("-" * 66)
        for removed in peer_pes:
            remaining = next(ticker for ticker in peer_pes if ticker != removed)
            remaining_price = implied[remaining]
            change = remaining_price - median_price
            sign = "+" if change >= 0 else "-"
            print(
                f"{removed:<10} {remaining:<10} {multiple(peer_pes[remaining]):>14} "
                f"{money(remaining_price):>14} {sign + money(abs(change)):>14}"
            )
        print("One remaining peer is a reference estimate, not a peer range.")


if __name__ == "__main__":
    main()
