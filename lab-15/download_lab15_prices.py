"""Free Yahoo Finance adjusted prices for Lab 15; no API key or subscription.

Run from the workspace root with .venv/bin/python model/src/download_lab15_prices.py.
Downloads daily observations, then selects the final trading day of each complete
month. Raw responses and retrieval metadata are retained for inspection.
"""
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import date, datetime, timezone
import json
from pathlib import Path
from math import isfinite
import ssl
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

import certifi

TICKERS = ['SGOV', 'IEF', 'LQD', 'VTI', 'VXUS']
OUTPUT = (Path(__file__).resolve().parent if (Path(__file__).resolve().parent / 'prices.csv').exists()
          else Path(__file__).resolve().parents[1] / 'outputs' / 'lab-15')


def download_prices():
    end = date.today().replace(day=1)  # Current month is incomplete.
    # Include 61 price observations, needed for 60 monthly returns.
    start = date(end.year - 5 - (end.month == 1), end.month - 1 or 12, 1)
    first = int(datetime.combine(start, datetime.min.time(), timezone.utc).timestamp())
    last = int(datetime.combine(end, datetime.min.time(), timezone.utc).timestamp())
    context = ssl.create_default_context(cafile=certifi.where())
    raw_dir = OUTPUT / 'sources'
    raw_dir.mkdir(parents=True, exist_ok=True)

    def fetch(ticker):
        url = (f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}'
               f'?period1={first}&period2={last}&interval=1d&events=div%2Csplits')
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(request, context=context, timeout=30) as response:
            raw = response.read()
        received = datetime.now(timezone.utc).isoformat()
        payload = json.loads(raw)
        if payload['chart']['error']:
            raise ValueError(f'{ticker}: {payload["chart"]["error"]}')
        result = payload['chart']['result'][0]
        if result['meta']['symbol'] != ticker or result['meta']['currency'] != 'USD':
            raise ValueError(f'{ticker}: unexpected symbol or currency.')
        timestamps = result['timestamp']
        adjusted = result['indicators']['adjclose'][0]['adjclose']
        if len(timestamps) != len(adjusted):
            raise ValueError(f'{ticker}: incomplete adjusted-close series.')
        observations = {}
        for timestamp, price in zip(timestamps, adjusted):
            observed = datetime.fromtimestamp(timestamp, ZoneInfo('America/New_York')).date()
            if start <= observed < end:
                # Keep the final daily observation, even if null; never silently
                # substitute an earlier price for a missing month-end observation.
                observations[observed.strftime('%Y-%m')] = (observed.isoformat(), price)
        (raw_dir / f'{ticker}.json').write_bytes(raw)
        return ticker, observations, dict(ticker=ticker, source=url,
            history_page=f'https://finance.yahoo.com/quote/{ticker}/history/',
            downloaded_at_utc=received, field='indicators.adjclose[0].adjclose',
            currency='USD', monthly_observations=observations)

    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(fetch, TICKERS))
    by_ticker = {ticker: observations for ticker, observations, _ in results}
    months = []
    year, month = start.year, start.month
    while date(year, month, 1) < end:
        months.append(f'{year:04d}-{month:02d}')
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    if len(months) != 61:
        raise ValueError('Expected exactly 61 complete monthly prices.')
    output_rows = []
    for period in months:
        values = [by_ticker[ticker].get(period) for ticker in TICKERS]
        if any(item is None or item[1] is None or not isfinite(item[1]) or item[1] <= 0 for item in values):
            raise ValueError(f'Missing or invalid month-end adjusted price for {period}.')
        if len({item[0] for item in values}) != 1:
            raise ValueError(f'Month-end trading dates differ in {period}.')
        output_rows.append([values[0][0], *[item[1] for item in values]])
    with (OUTPUT / 'prices.csv').open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['Date', *TICKERS])
        writer.writerows(output_rows)
    manifest = dict(method='Last trading day adjusted close, sampled from daily Yahoo data',
                    price_rows=len(output_rows), return_months=len(output_rows)-1,
                    first_observation=output_rows[0][0], last_observation=output_rows[-1][0],
                    sources=[metadata for _, _, metadata in results])
    (OUTPUT / 'sources.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f"Saved {OUTPUT / 'prices.csv'}: {len(output_rows)} price rows, "
          f"{output_rows[0][0]} through {output_rows[-1][0]}.")


if __name__ == '__main__':
    download_prices()
