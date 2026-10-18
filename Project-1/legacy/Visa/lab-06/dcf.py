"""Visa Lab 06; run python dcf.py. Cash in USD millions; shares in millions.
Sources and dates: Visa_Reverse_DCF.md. No original dcf.py was found;
this restores the published Lab 05 twelve-line output contract.
"""
from pathlib import Path
import os

# EDITABLE INPUTS. LTM ended June 30, 2026 = FY2025 + 9M2026 - 9M2025.
# SEC FY2025 10-K cash flows p.65; June 2026 10-Q cash flows p.10.
operating_cash_flow = 23059 + 16342 - 16821
interest_paid = 587 + 600 - 539
capital_expenditures = 1482 + 1178 - 1093
tax_rate = .20  # estimate, 2026-09-10
starting_fcff = operating_cash_flow + interest_paid*(1-tax_rate) - capital_expenditures
growth_rates = [.12,.11,.10,.09,.08]  # forecast estimates, 2026-09-10
wacc = .10  # rounded estimate; derivation in report
terminal_growth = .03  # long-run estimate, 2026-09-10
cash = 12359 + 1137 - 3000  # June cash + debt securities - estimated reserve
debt = 24131  # June 10-Q Note 8, debt principal including commercial paper
diluted_shares = 1898  # Q3 Class A-equivalent diluted average, Note 13
wacc_values = [.09,.10,.11]
terminal_growth_values = [.02,.03,.04]
target_price = 367.21  # Visa IR/StockAnalysis close, 2026-09-10 16:00 EDT
price_timestamp = "2026-09-10 16:00 EDT"
shift_lower, shift_upper = -.05,.10  # -5 and +10 percentage points
# END INPUTS

def dcf(fcff,growth,rate,terminal,cash_amount,debt_amount,shares):
    if terminal >= rate:
        raise ValueError("Terminal growth must be less than WACC.")
    if len(growth)!=5 or fcff<=0 or shares<=0:
        raise ValueError("Require five growth rates and positive FCFF/shares.")
    if terminal<=-1 or any(g<=-1 for g in growth):
        raise ValueError("Growth must exceed -100%.")
    forecast = []
    for g in growth:
        fcff *= 1+g
        forecast.append(fcff)
    pv = sum(f/(1+rate)**t for t,f in enumerate(forecast,1))
    tv = forecast[-1]*(1+terminal)/(rate-terminal)
    pv_tv = tv/(1+rate)**5
    ev = pv+pv_tv
    equity = ev+cash_amount-debt_amount
    return forecast+[pv,tv,pv_tv,ev,equity,equity/shares,pv_tv/ev]

def sensitivity(fcff,growth,cash_amount,debt_amount,shares,rates,terminals):
    return [[None if g>=r else dcf(fcff,growth,r,g,cash_amount,debt_amount,shares)[10]
             for g in terminals] for r in rates]

def reverse(fcff,growth,rate,terminal,cash_amount,debt_amount,shares,target,low,high):
    if low>=high or any(g+low<=-1 or g+high<=-1 for g in growth):
        raise ValueError("Invalid bracket: annual growth must exceed -100%.")
    def price(shift):
        return dcf(fcff,[g+shift for g in growth],rate,terminal,cash_amount,debt_amount,shares)[10]
    if not price(low)<=target<=price(high):
        return None
    for _ in range(100):
        middle = (low+high)/2
        difference = price(middle)-target
        if abs(difference)<.000001:
            return middle
        if difference<0:
            low = middle
        else:
            high = middle
    raise ArithmeticError("Bisection did not converge.")

def training_checks():
    growth = [.08,.06,.05,.04,.03]
    actual = dcf(100,growth,.10,.03,50,300,50)
    expected = [108,114.48,120.204,125.0122,128.7625,448.4408,1894.6486,
                1176.4277,1624.8685,1374.8685,27.4974,.7240]
    assert all(abs(a-b)<.0001 for a,b in zip(actual,expected))
    cells = sensitivity(100,growth,50,300,50,[.09,.10,.11],[.02,.03,.04])
    assert [[round(v,2) for v in row] for row in cells]==[
        [28.60,32.94,39.02],[24.36,27.50,31.69],[21.06,23.41,26.44]]
    shift = reverse(100,growth,.10,.03,50,300,50,30,-.05,.10)
    assert shift is not None and abs(shift*100-1.78)<.01
    assert abs(dcf(100,[g+shift for g in growth],.10,.03,50,300,50)[10]-30)<.01
    assert reverse(100,growth,.10,.03,50,300,50,1000,-.05,.10) is None
    assert sensitivity(100,growth,50,300,50,[.03],[.03,.04])==[[None,None]]
    try:
        reverse(100,growth,.10,.03,50,300,50,30,-1.08,.10)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid bracket accepted")
    return shift,cells

def visa_price(shift):
    return dcf(starting_fcff,[g+shift for g in growth_rates],wacc,terminal_growth,cash,debt,diluted_shares)[10]

def make_chart(cells,shift):
    folder = Path(__file__).resolve().parent
    os.environ.setdefault("MPLCONFIGDIR",str(folder/".matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig,axes = plt.subplots(1,2,figsize=(13,5.5),layout="constrained")
    valid = [v for row in cells for v in row if v is not None]
    colors = [[float("nan") if v is None else v for v in row] for row in cells]
    image = axes[0].imshow(colors,cmap="YlGnBu",aspect="auto")
    axes[0].set_xticks(range(len(terminal_growth_values)),[f"{g:.0%}" for g in terminal_growth_values])
    axes[0].set_yticks(range(len(wacc_values)),[f"{r:.0%}" for r in wacc_values])
    axes[0].set(xlabel="Terminal growth",ylabel="WACC",title="Visa sensitivity: USD per diluted share")
    for i,row in enumerate(cells):
        for j,v in enumerate(row):
            color = "white" if v is not None and v>(min(valid)+max(valid))/2 else "black"
            axes[0].text(j,i,"Invalid" if v is None else f"{v:.2f}",ha="center",va="center",color=color,fontsize=12)
    axes[0].add_patch(Rectangle((len(terminal_growth_values)//2-.5,len(wacc_values)//2-.5),1,1,fill=False,edgecolor="#ed7800",linewidth=3))
    fig.colorbar(image,ax=axes[0],label="USD/share",shrink=.8)
    shifts = [shift_lower+(shift_upper-shift_lower)*i/200 for i in range(201)]
    axes[1].plot([s*100 for s in shifts],[visa_price(s) for s in shifts],color="#176381",linewidth=2.5,label="Modeled price")
    axes[1].axhline(target_price,color="#a63232",linestyle="--",label=f"Target USD {target_price:.2f}")
    axes[1].axvline(0,color="gray",linestyle=":",label="Unshifted forecast")
    note = "No solution in the specified bracket"
    if shift is not None:
        axes[1].scatter([shift*100],[target_price],color="#ed7800",zorder=5)
        axes[1].axvline(shift*100,color="#ed7800",linestyle="--",label=f"Solution {shift*100:+.2f} pp")
        note = f"Solved shift: {shift*100:+.2f} percentage points"
    axes[1].set(xlabel="Uniform growth shift (percentage points)",ylabel="USD per diluted share",
                title="Visa reverse DCF: five-year FCFF growth",xlim=(shift_lower*100,shift_upper*100))
    axes[1].grid(alpha=.2)
    axes[1].legend(loc="upper left",fontsize=9)
    axes[1].text(.03,.04,note,transform=axes[1].transAxes,fontsize=10,bbox={"facecolor":"white","edgecolor":"#cccccc"})
    fig.suptitle(f"Visa | Close {price_timestamp} | Base WACC {wacc:.0%}, terminal growth {terminal_growth:.0%}",fontsize=13)
    path = folder/"visa_sensitivity_reverse_dcf.png"
    fig.savefig(path,dpi=180)
    plt.close(fig)
    return path

def main():
    training_shift,training_grid = training_checks()
    result = dcf(starting_fcff,growth_rates,wacc,terminal_growth,cash,debt,diluted_shares)
    labels = [f"FCFF Year {i}" for i in range(1,6)]+[
        "Present value of the explicit FCFF","Terminal value at Year 5",
        "Present value of the terminal value","Enterprise value","Equity value",
        "Value per diluted share","Present value of terminal value / enterprise value"]
    for label,value in zip(labels,result):
        print(f"{label}: {value:.4f}")
    print(f"\nTraining PASS: twelve outputs; nine cells; USD 30 shift {training_shift*100:+.4f} pp")
    for row in training_grid:
        print(" | ".join(f"{v:.2f}" for v in row))
    cells = sensitivity(starting_fcff,growth_rates,cash,debt,diluted_shares,wacc_values,terminal_growth_values)
    assert wacc_values==sorted(wacc_values) and terminal_growth_values==sorted(terminal_growth_values)
    assert wacc==wacc_values[len(wacc_values)//2] and terminal_growth==terminal_growth_values[len(terminal_growth_values)//2]
    for row in cells:
        valid = [v for v in row if v is not None]
        assert all(a<b for a,b in zip(valid,valid[1:]))
    for column in zip(*cells):
        valid = [v for v in column if v is not None]
        assert all(a>b for a,b in zip(valid,valid[1:]))
    print("\nVisa sensitivity — USD/share\nWACC / g | "+" | ".join(f"{g:.0%}" for g in terminal_growth_values))
    for rate,row in zip(wacc_values,cells):
        print(f"{rate:.0%} | "+" | ".join("Invalid" if v is None else f"{v:.2f}" for v in row))
    corners = [v for v in [cells[0][0],cells[0][-1],cells[-1][0],cells[-1][-1]] if v is not None]
    print(f"Valid corner range: USD {min(corners):.2f} to {max(corners):.2f}" if corners else "No valid corners")
    print("Direction checks PASS; base is in the center.")
    ratio = result[10]/target_price
    print(f"Base/market: {ratio:.4f}x; "+("inside" if .5<=ratio<=2 else "outside")+" the 0.5x–2x band.")
    shift = reverse(starting_fcff,growth_rates,wacc,terminal_growth,cash,debt,diluted_shares,target_price,shift_lower,shift_upper)
    print(f"\nTarget: USD {target_price:.4f}; {price_timestamp}. Bracket: {shift_lower*100:+.2f} to {shift_upper*100:+.2f} pp")
    print(f"Held fixed: FCFF {starting_fcff:.4f} USD M; WACC {wacc:.2%}; terminal growth {terminal_growth:.2%}; cash {cash} USD M; debt {debt} USD M; diluted shares {diluted_shares} M; five year-end flows; Year-5 terminal timing; base growth path {growth_rates}.")
    print(f"FCFF bridge fixed: CFO {operating_cash_flow}, interest paid {interest_paid}, capex {capital_expenditures} USD M; tax {tax_rate:.0%}.")
    if shift is None:
        print("No solution in the specified bracket")
        print("Solved shift, solution growth, solution price and residual: unavailable (no root).")
        for bound in [shift_lower,shift_upper]:
            print(f"Boundary check ONLY {bound*100:+.2f} pp: growth {[round(g+bound,6) for g in growth_rates]}; modeled USD {visa_price(bound):.4f}; difference USD {visa_price(bound)-target_price:+.4f}")
    else:
        assert abs(visa_price(shift)-target_price)<.01
        print(f"Solved shift: {shift*100:+.4f} percentage points")
        print("Adjusted growth: "+", ".join(f"{g+shift:.4%}" for g in growth_rates))
        print(f"Modeled price: USD {visa_price(shift):.6f}; difference USD {visa_price(shift)-target_price:+.6f}")
    print("Reverse DCF is one conditional assumption set, not proof of mispricing.")
    print("Chart saved:",make_chart(cells,shift))

if __name__=="__main__":
    main()
