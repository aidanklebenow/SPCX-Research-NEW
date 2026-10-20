"""Local analyst workbench; standard library only. Run python3 app.py, open localhost:8765."""
import argparse
import copy
import json
import math
import sys
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse,parse_qs

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from visa_model import load,run,bs_gap
from analysis import cases,conclusion

CONTROLS={
    'growth_shift':dict(label='Activity growth shift',minimum=-.07,maximum=.05,step=.005,scale=100,unit='pp',basis='Activity and other growth; downside -7pp tests a payments slowdown; +5pp is a stretch beyond base. Yields remain fixed.'),
    'incentive_shift':dict(label='Client incentives / gross revenue',minimum=-.01,maximum=.03,step=.0025,scale=100,unit='pp shift',basis='TTM gross-revenue incentive burden is about 28%; -1pp to +3pp spans renewal/mix pressure, not guidance.'),
    'cash_expense_shift':dict(label='Cash operating expense burden',minimum=-.025,maximum=.025,step=.0025,scale=100,unit='pp shift',basis='Up/down 2.5pp of net revenue tests operating leverage and compliance costs; SBC remains expensed and cash-funded.'),
    'capex_ratio':dict(label='Capex / net revenue',minimum=.03,maximum=.06,step=.0025,scale=100,unit='%',basis='Reported FY2023-25 spending was roughly 3.2-3.7%; 3-6% includes heavier technology investment.'),
    'wacc_shift':dict(label='WACC stress',minimum=-.015,maximum=.015,step=.0025,scale=10000,unit='bp',basis='Plus/minus 150bp around the sourced-component base; this is a risk stress, not an observed bond quote.'),
    'terminal_growth':dict(label='Terminal nominal growth',minimum=.02,maximum=.04,step=.0025,scale=100,unit='%',basis='2-4% long-run nominal growth range; must stay below WACC. ROIC funds reinvestment.'),
    'terminal_roic':dict(label='Terminal incremental ROIC',minimum=.20,maximum=.40,step=.025,scale=100,unit='%',basis='20-40% incremental capital efficiency is judgment; terminal reinvestment = NOPAT x g / ROIC.')}


def calculate(payload):
    a,h=load();b=copy.deepcopy(a)
    if set(payload)-set(CONTROLS)-{'fault'}: raise ValueError('Unknown driver; accounting/provenance are locked')
    for key,c in CONTROLS.items():
        v=float(payload.get(key,a[key]))
        if not math.isfinite(v) or not c['minimum']-1e-12<=v<=c['maximum']+1e-12:
            raise ValueError(key+' outside defended control bounds')
        b[key]=v
    fault=payload.get('fault',False)
    if not isinstance(fault,bool):raise ValueError('Fault probe must be a boolean')
    b['break_cash']=fault
    r=run(b,h)
    # Market/reference scenario band remains frozen; live controls change the active view.
    baseline=run(a,h)
    return dict(status='PASS',valuation=r['valuation'],wacc=r['wacc'],statements=r['statements'],
                inputs={k:b[k] for k in CONTROLS},base_value=baseline['valuation']['per_share'],
                delta=r['valuation']['per_share']-baseline['valuation']['per_share'],
                checks=[dict(period=x['period'],bs_gap=bs_gap(x),cash_gap=x['cash']-x['opening_cash']-x['cfo']-x['cfi']-x['cff']) for x in r['statements']])


class Handler(BaseHTTPRequestHandler):
    def send(self,status,body,content_type='application/json'):
        raw=body.encode();self.send_response(status);self.send_header('Content-Type',content_type+'; charset=utf-8')
        self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(raw)

    def do_GET(self):
        path=urlparse(self.path).path
        if path=='/':self.send(200,(ROOT/'src/workbench.html').read_text(),'text/html')
        elif path=='/api/base':
            a,h=load();c=cases(a,h)
            self.send(200,json.dumps(dict(controls=CONTROLS,base={k:a[k] for k in CONTROLS},context={k:a[k] for k in ('valuation_date','price_date','reference_price','status')},conclusion=conclusion(c,a),result=calculate({}))))
        elif path=='/health':self.send(200,'{"status":"ok"}')
        else:self.send(404,'{"error":"not found"}')

    def do_POST(self):
        if urlparse(self.path).path!='/api/calculate':self.send(404,'{"error":"not found"}');return
        try:
            n=int(self.headers.get('Content-Length','0'))
            if not 0<n<10000:raise ValueError('Invalid request length')
            data=json.loads(self.rfile.read(n))
            if not isinstance(data,dict):raise ValueError('Require driver object')
            self.send(200,json.dumps(calculate(data),allow_nan=False))
        except (ValueError,KeyError,TypeError) as e:
            self.send(422,json.dumps(dict(status='VALUATION REFUSED',error=str(e))))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8765);args=p.parse_args()
    print(f'Visa workbench: http://127.0.0.1:{args.port} | Ctrl-C to stop',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
