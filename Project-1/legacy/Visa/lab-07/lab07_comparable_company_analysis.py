"""FIN 43900 Lab 07: comparable-company valuation using supplied inputs.

Run: python3 lab07_comparable_company_analysis.py
ABG is the target; AN and GPI are the peers. No external data is fetched.
P/E = share price / EPS; implied ABG price = peer P/E * ABG EPS.
The median of two peer multiples is their arithmetic average.
"""

from decimal import Decimal, ROUND_HALF_UP, localcontext
from statistics import median


TARGET = {"name": "Asbury Automotive", "ticker": "ABG",
          "price": Decimal("243.03"), "eps": Decimal("21.50")}
PEERS = (
    {"name": "AutoNation", "ticker": "AN",
     "price": Decimal("169.84"), "eps": Decimal("16.92")},
    {"name": "Group 1 Automotive", "ticker": "GPI",
     "price": Decimal("421.48"), "eps": Decimal("36.81")},
)


def money(value):
    """Round only the displayed dollar amount to cents (half up)."""
    return f"${value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):,.2f}"


def multiple(value):
    """Display six decimals without rounding calculation inputs."""
    return f"{value.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP):.6f}x"


def main():
    # Retain 50 significant digits throughout intermediate calculations.
    with localcontext() as context:
        context.prec = 50
        peer_multiples = {
            peer["ticker"]: peer["price"] / peer["eps"] for peer in PEERS
        }
        peer_median = median(peer_multiples.values())

        print("FIN 43900 | Lab 07 | Comparable-company analysis")
        print(f"Target: {TARGET['name']} ({TARGET['ticker']})")
        print(f"Observed share price: {money(TARGET['price'])}; "
              f"EPS: {money(TARGET['eps'])}")
        print("\nPeer P/E multiples and implied ABG share prices")
        print(f"{'Peer':<8} {'Price':>12} {'EPS':>10} {'P/E':>14} {'Implied ABG':>14}")
        for peer in PEERS:
            pe = peer_multiples[peer["ticker"]]
            print(f"{peer['ticker']:<8} {money(peer['price']):>12} "
                  f"{money(peer['eps']):>10} {multiple(pe):>14} "
                  f"{money(pe * TARGET['eps']):>14}")
        print(f"\nPeer median P/E: {multiple(peer_median)}")
        print(f"Median-implied ABG share price: {money(peer_median * TARGET['eps'])}")

        print("\nLeave-one-out peer analysis (ABG remains the target)")
        print(f"{'Excluded':<12} {'Remaining':<12} {'Median P/E':>14} {'Implied ABG':>14}")
        for excluded in peer_multiples:
            remaining = {ticker: pe for ticker, pe in peer_multiples.items()
                         if ticker != excluded}
            loo_median = median(remaining.values())
            print(f"{excluded:<12} {', '.join(remaining):<12} "
                  f"{multiple(loo_median):>14} "
                  f"{money(loo_median * TARGET['eps']):>14}")
        print("With two peers, each leave-one-out median equals the remaining peer's P/E.")


if __name__ == "__main__":
    main()
