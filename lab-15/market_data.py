"""Free, timestamped Yahoo Finance observations. No subscription or API key."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from math import isfinite
import re
import ssl
from urllib.parse import quote
from urllib.request import Request, urlopen

import certifi


def parse_quote(payload, ticker, fetched_at=None):
    """Keep Yahoo's trade timestamp separate from the time we fetched it."""
    chart = payload.get('chart', {})
    if chart.get('error') or not chart.get('result'):
        raise ValueError('Yahoo returned no quote for this ticker.')
    result = chart['result'][0]
    meta = result['meta']
    if meta.get('symbol', '').upper() != ticker.upper():
        raise ValueError('Yahoo returned a different ticker.')
    price, stamp = meta.get('regularMarketPrice'), meta.get('regularMarketTime')
    if not isinstance(price, (int, float)) or not isfinite(price) or price <= 0 or not stamp:
        raise ValueError('Yahoo returned an invalid price or trade timestamp.')
    previous = meta.get('chartPreviousClose', meta.get('previousClose'))
    change = (price / previous - 1) * 100 if previous and previous > 0 else None
    history = []
    indicators = result.get('indicators', {}).get('quote', [{}])[0]
    for timestamp, close in zip(result.get('timestamp', []), indicators.get('close', [])):
        if close is not None and isfinite(close) and close > 0:
            history.append(dict(time=datetime.fromtimestamp(timestamp, timezone.utc).isoformat(),
                                price=close))
    return dict(ticker=ticker, name=meta.get('longName') or meta.get('shortName') or ticker,
                price=price, currency=meta.get('currency', 'Unknown'), change_percent=change,
                trade_time=datetime.fromtimestamp(stamp, timezone.utc).isoformat(),
                fetched_at=fetched_at or datetime.now(timezone.utc).isoformat(),
                exchange=meta.get('fullExchangeName', meta.get('exchangeName', 'Unknown')),
                delay_minutes=meta.get('exchangeDataDelayedBy'), history=history,
                source=f'https://finance.yahoo.com/quote/{quote(ticker, safe="")}/')


def fetch_quotes(tickers):
    """Fetch independently: one failed symbol cannot hide the other prices."""
    tickers = tuple(dict.fromkeys(tickers))
    if not 1 <= len(tickers) <= 6:
        raise ValueError('Choose one to six tickers.')
    context = ssl.create_default_context(cafile=certifi.where())

    def fetch(ticker):
        if not re.fullmatch(r'[A-Za-z0-9.^=\-]{1,20}', ticker):
            return dict(ticker=ticker, error='Unsupported ticker format.')
        url = (f'https://query1.finance.yahoo.com/v8/finance/chart/{quote(ticker, safe="")}'
               '?range=1d&interval=1m')
        try:
            with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}),
                         context=context, timeout=8) as response:
                payload = json.loads(response.read())
            return parse_quote(payload, ticker)
        except Exception as error:
            return dict(ticker=ticker, error=f'Quote unavailable: {error}')

    with ThreadPoolExecutor(max_workers=min(6, len(tickers))) as pool:
        return list(pool.map(fetch, tickers))
