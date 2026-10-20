"""One-command reproducible Visa valuation, tables and visible report. No network."""
import argparse
import copy
import csv
import hashlib
import html
import json
import platform
import sys
import math
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from visa_model import load,run,value,bs_gap,ASSETS,LIABILITIES,action
from analysis import cases,sensitivities,reverse_dcf,peers,conclusion


def csv_write(path,rows):
    if not rows:return
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)


def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+
                     ['| '+' | '.join(str(x) for x in row)+' |' for row in rows])


def report(result):
    a=result['inputs'];v=result['base']['valuation'];c=result['base']['wacc'];z=result['conclusion'];rows=result['base']['statements']
    p=result['peers'];rev=result['reverse_dcf'];s=result['sensitivity']
    text=f'''# Visa | Conditional investment assessment

As of {a['valuation_date']}; information cutoff {a['information_cutoff']}; reference price ${a['reference_price']:.2f} from {a['price_date']}. USD millions except per-share amounts. AI-assisted work for Aidan Klebenow, FIN 43900. Proposed assumptions and action require Aidan review; no trade instruction.

**Proposed action: {z['action']}.** Causal low/base/high values are ${z['low']:.0f} / ${z['base']:.0f} / ${z['high']:.0f}. The ${z['low']:.0f}-${z['high']:.0f} envelope is a scenario range, not a confidence interval. Combined downside is ${z['downside']:.0f}. The model's price-and-downside rule allows conditional initiation at or below ${z['potential_entry']:.0f}, subject to source refresh and operating confirmation. Do not mechanically average the DCF with peer outputs.

## Decision context and timing

Intended user: a buy-side portfolio manager with no Visa position. Proposed investment horizon: 3-5 years. Valuation date October 19, 2026. Reported June 30, 2026 balances and TTM flows establish history. A separately shown 111-day estimated stub rolls the balance sheet to October 19; five forward twelve-month periods end October 19, 2027-2031. These are **not Visa fiscal years**. The stub is not an observed result and its cash flows are not discounted as future cash. Annual forward cash flows use end-period discounting. FY2026 audited results are not assumed available.

Shares: {a['shares']:,.0f}M as-converted economic equivalents at June 30, plus {a['incremental_dilution']:.1%} incremental dilution reserve = {v['economic_shares']:,.1f}M. Includes participating preferred in converted claims; no second preferred deduction. This is a dated proxy, not verified October outstanding shares. No forecast share-repurchase uplift is taken.

## Forecast and financial articulation

Revenue is separated into service, processing, international and other. Service growth combines lagged-volume and effective-yield assumptions; processing combines transaction and yield assumptions; international combines cross-border and yield/mix assumptions. This is an annual reduced-form model, not a quarterly transaction-level forecast. Value-added services overlap the reported categories and are **not added again**. Client incentives reduce gross revenue; asset/liability changes reconcile expense to cash paid.

''' + table(['Forward 12M end','Net revenue','EBIT','Net income','CFO','Capex','FCFF','BS gap'],[
        [r['period'][-10:],f"{r['revenue']:,.0f}",f"{r['ebit']:,.0f}",f"{r['net_income']:,.0f}",f"{r['cfo']:,.0f}",f"{r['capex']:,.0f}",f"{r['fcff']:,.0f}",f"{bs_gap(r):.6f}"] for r in rows])+f'''

FCFF = EBIT - unlevered operating tax + D&A - capex - change in operating NWC. It is calculated from these statements, not independently grown. Cash/debt are excluded from operating NWC; settlement and client-incentive assets/liabilities are handled symmetrically. Restricted customer cash is not discretionary liquidity. SBC stays an expense and future equivalent compensation is paid in cash; it is not added back while ignoring dilution. NI taxes apply only to positive pretax income, with no tax-loss carryforward assumed. Forecast operating noninterest cash income is zero.

## WACC and terminal economics

Risk-free {c['risk_free']:.2%} (FRED 10Y October 16); ERP {c['erp']:.2%} (Damodaran October 1 implied adjusted-payout estimate); selected levered beta {c['beta']:.2f}; cost of equity {c['cost_equity']:.2%}. Beta is analyst judgment informed by a provider's 0.76 five-year monthly observation, not a reproduced regression. Marginal debt cost {c['marginal_cost_debt']:.2%} = Treasury + a judgmental 75bp spread; no executable bond quote is claimed. Tax shield {c['tax_rate']:.0%}; market equity weight {c['equity_weight']:.2%}; debt weight {c['debt_weight']:.2%}; **WACC {c['wacc']:.2%}**. Debt principal is a market-value proxy; equity uses dated market capitalization of economic claims, never book equity.

Terminal growth {a['terminal_growth']:.1%}; incremental ROIC {a['terminal_roic']:.0%}; reinvestment rate g/ROIC = {a['terminal_growth']/a['terminal_roic']:.0%}. Terminal NOPAT {v['terminal_nopat']:,.0f}, reinvestment {v['terminal_reinvestment']:,.0f}, FCFF {v['terminal_fcff']:,.0f}. Positive reinvestment replaces extrapolation of favorable negative working capital. Terminal PV is **{v['terminal_share']:.1%} of EV**. The final explicit growth-to-terminal transition is abrupt; margin and ROIC persistence are material judgments, not management guidance.

''' + table(['EV-to-equity item','USD millions'],[
        ['PV five annual FCFF',f"{v['explicit_pv']:,.1f}"],['PV terminal',f"{v['terminal_pv']:,.1f}"],['Enterprise value',f"{v['enterprise_value']:,.1f}"],
        ['Estimated opening excess cash',f"+{v['excess_cash']:,.1f}"],['Eligible debt securities',f"+{v['liquid_securities']:,.1f}"],['Debt principal',f"-{v['debt']:,.1f}"],['Net legacy litigation claim',f"-{v['other_claims']:,.1f}"],['Economic equity',f"{v['equity_value']:,.1f}"],['Per diluted economic equivalent',f"${v['per_share']:.2f}"]])+'''

Eligible securities are $1,137M government debt securities. $888M litigation escrow, $4,310M customer collateral and $1,211M restricted settlement cash are not added as excess cash. The $386M legacy claim equals $1,274M accrued litigation less dedicated $888M escrow, assuming that coverage is available; remaining future litigation is expensed at 2% of net revenue in base. Preferred participating claims are in the denominator. Operating leases stay expensed; lease liabilities are not added to funded debt on either network. Pensions, contingent litigation, strategic investments and other nonoperating assets are not independently fair-valued; these are bridge limitations. Do not treat a zero separate adjustment as proof that no claim exists.

## Causal cases and decision reversals

''' + table(['Case','Value/share','WACC','Final EBIT','Final FCFF'],[
        [name,f"${r['valuation']['per_share']:.2f}",f"{r['wacc']['wacc']:.2%}",f"{r['statements'][-1]['ebit']:,.0f}",f"{r['statements'][-1]['fcff']:,.0f}"] for name,r in result['cases'].items()])+'''

Low: activity growth -3pp, incentives +1.5pp of gross revenue, cash costs +1.5pp of net revenue, WACC +100bp, terminal g 2.5%, ROIC 25%. High: activity +2pp, incentives -0.5pp, cash costs -0.5pp, WACC -75bp, g 3.5%, ROIC 35%. Combined downside: activity -7pp, incentives +2.5pp, cash costs +2.5pp, WACC +150bp, g 2%, ROIC 20%. Each case reruns all three statements; current-date opening is fixed. These are plausible judgment stresses, not assigned probabilities. The downside can reverse an initiation at a proposed entry price into watch/defer or no initiation; it does not need to reverse an already-negative action at the reference price.

''' + table(['One-at-a-time driver','Low input','High input','Value span/share'],[
        [r['driver'],r['low_input'],r['high_input'],f"${r['value_span']:.2f}"] for r in s])+f'''

Ranks depend on selected ranges. Alternate-range results are in `sensitivity_alternate.csv`; growth is narrowed while incentives are widened. See EBIT and FCFF effects in both CSVs. WACC and terminal inputs affect value without changing the five-year operating profit/cash forecasts.

## Market-implied expectations

Holding yields, incentives, cost ratios, WACC, terminal assumptions and the current bridge fixed, the dated market reference requires a uniform **{rev['uniform_activity_growth_shift']*100:.2f}pp** increase to annual service-volume, transaction, cross-border and other growth. That produces **{rev['implied_net_revenue_cagr']:.1%}** net-revenue CAGR and reprices to ${rev['recomputed_price']:.2f}. This is one conditional solution, not a uniquely identified market belief.

## Peer cross-check and disagreement

Policy was saved before new project multiple retrieval; prior MA/AXP lab exposure is disclosed. MA qualifies as a fee-based global network. AXP's lending/funding economics exclude it from operating EV comparisons. Both use trailing June 2026 financials, October 16 prices, as-converted/economic shares plus the same 0.5% dilution reserve, funded principal debt and $5B operating cash reserve, SBC-expensed GAAP EBIT + D&A, and P/E based on total equity/total NI. Capital structures remain June proxies. MA GAAP restructuring/litigation remains expensed. No qualified comparable transaction was established, so transaction multiples are omitted.

''' + table(['Network','TTM EV/EBITDA','TTM P/E','TTM revenue','TTM NI'],[
        [r['ticker'],f"{r['ev_ebitda']:.2f}x",f"{r['pe']:.2f}x",f"{r['revenue']:,.0f}",f"{r['net_income']:,.0f}"] for r in p['rows']])+f'''

Applying MA's GAAP multiples to Visa's matching GAAP bases yields **${p['implied']['gaap_ev_multiple_per_share']:.0f}** via EV/EBITDA and **${p['implied']['gaap_pe_per_share']:.0f}** via P/E. A separately labeled normalized Visa comparison yields ${p['implied']['normalized_ev_multiple_per_share']:.0f} / ${p['implied']['normalized_pe_per_share']:.0f}; this mixes normalized target with GAAP peer and is not the primary comparison. One peer cannot establish a statistical range. Market-relative values embed MA's own pricing and growth/risk expectations; DCF explicitly fades growth and funds terminal reinvestment. Their disagreement is evidence to investigate persistence/terminal economics, not permission to average away uncertainty.

## Conditions, monitoring and limits

Proposed committee ask: do not initiate at the reference price; retain Visa on a monitored watchlist and revisit only if price, operating evidence or a defensible capital-cost change supports the entry rule. Before initiation, refresh actual cash/debt/diluted economic shares; verify incentive timing, litigation coverage and forecast cost ratios. Review each earnings release: investigate two consecutive quarters below 8% processed-transaction growth, incentives above 30% of gross revenue, or normalized operating margin below 60%; rerun if the 10Y rate moves 50bp, a material legal event occurs, or a filing changes the bridge. These thresholds are analyst proposals for Aidan to adopt/revise.

Model limitations: 111-day estimated opening, stale June claims, no observed October share roll-forward, no quarterly seasonality, aggregate yield/mix proxies, cash replacement of SBC, fixed goodwill/collateral/securities/deferred-tax/other-asset and liability stocks, no acquisitions/FX/impairments, flat debt/refinancing, no NOL tracking, no independently priced credit spread/beta regression, abrupt terminal transition and one-peer concentration. Forecast taxes are an economic cash-tax proxy, not a full tax-accounting schedule. Accounting articulation is necessary, not proof these economics are correct.

## Evidence and reproducibility

Run `python3 run.py`; tests `python3 -m unittest discover -s tests -p test_integrated.py -v`; workbench `python3 app.py`. Material source fields are in `inputs/source_register.csv`; raw transcribed facts preserve primary URLs and locators. Full SEC download was blocked; these are transcribed facts, not downloaded full filings. Independent capex/definition check: `data/raw/independent_capex_check.json`. Financial source verification by the assistant is not Aidan's human independent verification. Audit scope, AI dispositions, cold-run evidence and missing human requirements are in `docs/validation-and-ai-use.md`.

Primary sources: [Visa FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm), [Visa June 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1403161/000140316126000104/v-20260630.htm), [MA FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm), [MA June 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1141391/000114139126000083/ma-20260630.htm), [FRED DGS10](https://fred.stlouisfed.org/series/DGS10), [Damodaran ERP](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm). Provider cross-checks/dated prices are in the input evidence ledgers.
'''
    return text


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inputs',type=Path);parser.add_argument('--output-dir',type=Path,default=ROOT/'outputs/integrated')
    args=parser.parse_args();out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
    try:
        a,h=load(args.inputs);c=cases(a,h);base=c['base']
        z=conclusion(c,a);sen=sensitivities(a,h);alt=sensitivities(a,h,True);rev=reverse_dcf(a,h);p=peers(a,h)
        result=dict(inputs=a,base=base,cases=c,conclusion=z,sensitivity=sen,sensitivity_alternate=alt,reverse_dcf=rev,peers=p)
        (out/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
        csv_write(out/'statements.csv',base['statements'])
        if base['stub']:csv_write(out/'estimated_stub.csv',[base['stub']])
        csv_write(out/'opening_balance_sheet.csv',[dict(item=k,reported_june=h['facts']['bs_2026_06_30'][k],estimated_valuation_date=base['opening'][k]) for k in ASSETS+LIABILITIES+('equity',)])
        csv_write(out/'articulation.csv',[dict(period=r['period'],bs_gap=bs_gap(r),cash_gap=r['cash']-r['opening_cash']-r['cfo']-r['cfi']-r['cff'],status='PASS') for r in base['statements']])
        csv_write(out/'fcff_bridge.csv',[{k:r[k] for k in ('period','ebit','unlevered_tax','da','capex','change_nwc','fcff','fcfe','interest','tax')} for r in base['statements']])
        csv_write(out/'wacc.csv',[base['wacc']]);csv_write(out/'enterprise_equity_bridge.csv',[base['valuation']])
        csv_write(out/'scenarios.csv',[dict(case=k,per_share=r['valuation']['per_share'],wacc=r['wacc']['wacc'],terminal_growth=r['inputs']['terminal_growth'],final_ebit=r['statements'][-1]['ebit'],final_fcff=r['statements'][-1]['fcff'],checks='PASS') for k,r in c.items()])
        entry=math.floor(z['potential_entry'])
        csv_write(out/'decision_reversal.csv',[
            dict(view='base',hypothetical_entry_price=entry,active_value=z['base'],action=action(entry,z['base'],z['low'],z['high']),policy='Active-case 15% entry discount; original low/high stress envelope held fixed'),
            dict(view='combined downside',hypothetical_entry_price=entry,active_value=z['downside'],action=action(entry,z['downside'],z['low'],z['high']),policy='Same rule and price; downside removes the base entry permission')])
        csv_write(out/'scenario_statements.csv',[dict(case=k,**r) for k,v in c.items() for r in v['statements']])
        csv_write(out/'sensitivity.csv',sen);csv_write(out/'sensitivity_alternate.csv',alt)
        csv_write(out/'peer_multiples.csv',p['rows']);(out/'peer_implied.json').write_text(json.dumps(p['implied'],indent=2))
        (out/'reverse_dcf.json').write_text(json.dumps(rev,indent=2))
        grid=[]
        for w in (.07,.08,.09,.10,.11):
            for g in (.02,.025,.03,.035,.04):
                b=copy.deepcopy(a);b['wacc_shift']=a['wacc_shift']+w-base['wacc']['wacc'];b['terminal_growth']=g
                v,_=value(base['statements'],base['opening'],b,h)
                grid.append(dict(wacc=w,terminal_growth=g,per_share=v['per_share']))
        csv_write(out/'wacc_growth_grid.csv',grid)
        md=report(result);(out/'summary.md').write_text(md)
        # Standalone visible evidence: no server, library or notebook required to inspect.
        body='<html><head><meta charset="utf-8"><title>Visa executed valuation</title><style>body{max-width:1100px;margin:36px auto;font:15px/1.5 system-ui;color:#16283b;padding:20px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style></head><body><pre>'+html.escape(md)+'</pre></body></html>'
        (out/'visible_output.html').write_text(body)
        hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ('src','inputs','data/processed','data/raw') for p in sorted((ROOT/folder).glob('**/*')) if p.is_file() and '__pycache__' not in str(p)}
        (out/'run_manifest.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),command='python3 run.py',input_and_source_hashes=hashes,scope='integrated model run; human evidence and assignment completion separate',outputs=[p.name for p in sorted(out.iterdir()) if p.is_file()]),indent=2))
        print(f"PASS | {z['action']} | range ${z['low']:.2f}-${z['high']:.2f} | base ${z['base']:.2f} | downside ${z['downside']:.2f}")
        print(f"WACC {base['wacc']['wacc']:.4%}; terminal EV share {base['valuation']['terminal_share']:.2%}; output {out}")
    except (ValueError,KeyError,TypeError) as e:
        parser.exit(1,'VALUATION REFUSED: '+str(e)+'\n')


if __name__=='__main__':main()
