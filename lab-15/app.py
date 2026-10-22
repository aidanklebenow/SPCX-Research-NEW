"""Lab 15 dashboard. Run with streamlit run model/src/app.py."""
import hashlib
import importlib
from io import BytesIO, StringIO
from datetime import datetime, timezone
from pathlib import Path
import sys

import altair as alt
import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
import portfolio
import market_data

portfolio = importlib.reload(portfolio)
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = (Path(__file__).resolve().parent if (Path(__file__).resolve().parent / 'prices.csv').exists()
            else ROOT / 'outputs/lab-15')
COLORS = ['#0f766e', '#2563eb', '#d97706', '#8b5cf6', '#db2777', '#64748b']
ETF_TICKERS = ('SGOV', 'IEF', 'LQD', 'VTI', 'VXUS')

st.set_page_config(page_title='Portfolio Studio · Lab 15', page_icon='◈', layout='wide')
# Preserve these widget values when visiting a page that does not render them.
for saved_key in list(st.session_state):
    if (saved_key != 'reserve_minimum' and saved_key.startswith(('return_', 'reserve_', 'manual_'))) or saved_key in {
        'partner_notes', 'decision', 'decision_reason'
    }:
        st.session_state[saved_key] = st.session_state[saved_key]
st.markdown('''<style>
.block-container {padding-top:2.2rem;padding-bottom:3rem;max-width:1440px;}
h1,h2,h3 {letter-spacing:-0.035em;}
[data-testid="stMetric"] {background:var(--secondary-background-color);border:1px solid color-mix(in srgb,var(--text-color) 16%,transparent);border-radius:12px;padding:16px;color:var(--text-color);}
[data-testid="stMetricLabel"] {color:var(--text-color);opacity:0.85;}
.studio-eyebrow {color:var(--text-color);opacity:0.85;font-size:12px;font-weight:700;letter-spacing:0.16em;}
.studio-intro {color:var(--text-color);opacity:0.85;font-size:17px;max-width:850px;line-height:1.6;}
</style>''', unsafe_allow_html=True)


@st.cache_data(ttl=60, show_spinner=False)
def quotes_cached(tickers):
    return market_data.fetch_quotes(tickers)


@st.cache_data(show_spinner=False)
def optimize(vehicles, correlations, objective, minimum, eligible):
    return portfolio.lowest_risk_mix(vehicles, correlations, objective, minimum, set(eligible))


def chart_style(chart):
    # Let Streamlit apply light/dark text, legend, and axis colors.
    return chart.configure_view(stroke=None).configure_axis(
        gridOpacity=0.15).configure_legend(title=None)


def allocation_chart(result, vehicles):
    data = pd.DataFrame([{'Asset': asset[0], 'Weight': weight}
                         for asset, weight in zip(vehicles, result['weights'])])
    chart = alt.Chart(data).mark_arc(innerRadius=72, outerRadius=112, cornerRadius=3).encode(
        theta=alt.Theta('Weight:Q'), color=alt.Color('Asset:N', scale=alt.Scale(range=COLORS)),
        tooltip=['Asset:N', alt.Tooltip('Weight:Q', format='.1%')])
    st.altair_chart(chart_style(chart).properties(height=260), width='stretch')


def show_mix(title, result, vehicles):
    st.subheader(title)
    if result is None:
        st.warning('no mix meets the objective')
        return
    one, two, three = st.columns(3)
    one.metric('Return estimate', f"{result['expected_return']:.2%}")
    two.metric('Annualized volatility', f"{result['volatility']:.2%}")
    three.metric('Reserve weight', f"{result['reserve_weight']:.2%}")
    allocation_chart(result, vehicles)
    st.dataframe(pd.DataFrame({'Asset': [v[0] for v in vehicles],
                               'Weight (%)': [w * 100 for w in result['weights']]}),
                 hide_index=True, width='stretch',
                 column_config={'Weight (%)': st.column_config.NumberColumn(format='%.2f')})


@st.fragment(run_every='60s')
def market_watch(tickers, full=False):
    st.subheader('Market watch')
    st.caption('Free Yahoo Finance · latest regular-session trade · refreshes every 60 seconds while this page is open.')
    if st.button('Refresh prices', key='refresh_quotes'):
        quotes_cached.clear()
    with st.spinner('Checking Yahoo Finance…'):
        quotes = quotes_cached(tuple(tickers))
    good = [q for q in quotes if 'error' not in q]
    for column, quote in zip(st.columns(len(quotes)), quotes):
        with column:
            if 'error' in quote:
                st.metric(quote['ticker'], 'Unavailable')
                st.caption('Yahoo could not supply this quote. Try refresh.')
            else:
                delta = quote['change_percent']
                st.metric(quote['ticker'], f"{quote['price']:,.2f} {quote['currency']}",
                          f'{delta:+.2f}%' if delta is not None else None,
                          help='Change from the previous regular-session close.')
                trade = datetime.fromisoformat(quote['trade_time'])
                age = max(0, (datetime.now(timezone.utc) - trade).total_seconds())
                st.caption(f"Trade: {trade:%b %d, %H:%M:%S} UTC")
                if age > 20 * 60:
                    st.caption('Older last trade · market may be closed or feed delayed.')
                st.caption(f"Fetched: {datetime.fromisoformat(quote['fetched_at']):%H:%M:%S} UTC")
                st.link_button('Yahoo Finance ↗', quote['source'])
    st.caption('Yahoo may delay quotes. Fetch time is not trade time. After hours, the last regular-session trade remains displayed. Quotes do not alter the monthly lab estimates.')
    if full and good:
        st.divider()
        symbol = st.selectbox('Intraday chart', [q['ticker'] for q in good], key='intraday_symbol')
        chosen = next(q for q in good if q['ticker'] == symbol)
        if chosen['history']:
            history = pd.DataFrame(chosen['history'])
            chart = alt.Chart(history).mark_line(color='#0f766e', strokeWidth=2).encode(
                x=alt.X('time:T', title='Trade time (UTC)'),
                y=alt.Y('price:Q', title=f"Price ({chosen['currency']})", scale=alt.Scale(zero=False)),
                tooltip=[alt.Tooltip('time:T', title='UTC', format='%b %d %H:%M'),
                         alt.Tooltip('price:Q', format='.2f')]).properties(height=330)
            st.altair_chart(chart_style(chart), width='stretch')
            st.caption(f"{chosen['name']} · {chosen['exchange']} · Yahoo's latest available intraday session.")
        else:
            st.info('Yahoo supplied a quote but no intraday chart observations.')


def guide():
    st.title('A guide to your portfolio')
    st.markdown('<p class="studio-intro">Start here. You don’t need to know Python to understand what the app is testing.</p>', unsafe_allow_html=True)
    st.caption('Appearance: open the top-right menu → Settings → Theme to choose light, dark, or your system theme. Text, panels, and chart labels follow that choice.')
    for title, body in [
        ('1 · Choose the investments', 'Meridian is the professor’s four-asset training example. My five ETFs loads SGOV, IEF, LQD, VTI, and VXUS from your saved Yahoo monthly adjusted prices. Upload CSV lets you bring another three-to-six-fund universe.'),
        ('2 · Set the rules', 'The return objective is the minimum estimated annual return you want. The reserve minimum is the fraction that must be in assets you mark reserve-eligible. The optimizer searches long-only allocations in 5-percentage-point steps. Other mandate rules, including issuer limits, require separate checks.'),
        ('3 · Read the two answers', 'As loaded is the reference: original returns and all monthly data. Current inputs uses your edits and selected estimation window. Both use the same current objective and reserve rules. A changed answer shows sensitivity to estimates.'),
        ('4 · Move the allocation dials', 'Each slider controls one asset’s percentage. Moving it automatically spreads the remaining money across the other assets in their existing proportions. If the others were all zero, the remainder is split evenly. The weights always total 100%. These are hypothetical allocations; no trades are placed.'),
        ('5 · Understand the charts', 'A donut shows how your money is split. The allocation bars show how the optimizer’s answer changed. The risk-versus-return chart compares estimates, not guaranteed outcomes. The historical growth chart shows each ETF’s adjusted price rebased to 100; it is not a strategy backtest.'),
        ('6 · Test stability', 'Try reducing one return estimate by 1.00 percentage point. Then compare all months with the last 36. The largest weight change tells you the biggest allocation move. A 25-point change means a quarter of the portfolio moved in that asset.'),
        ('7 · Read market prices correctly', 'Market watch requests free Yahoo quotes every 60 seconds while visible. It shows the last regular-session trade and its time separately from when the quote was fetched. Quotes can be delayed or unavailable; after hours they can be the closing trade. A quote is today’s price; adjusted historical prices include payout and split adjustments.'),
    ]:
        with st.container(border=True):
            st.subheader(title)
            st.write(body)
    st.subheader('A small glossary')
    st.table(pd.DataFrame([
        ('Weight', 'The fraction of your money assigned to an investment. 30% means $30 of every $100.'),
        ('Return estimate', 'An assumed or historical-average annual gain. It is not a forecast or guarantee.'),
        ('Volatility', 'How widely returns fluctuate. Smaller means less variation in this model, not no chance of loss.'),
        ('Correlation', 'How two investments tend to move together. Diversification depends on these relationships.'),
        ('Reserve', 'The investments your mandate allows to satisfy its liquidity buffer.'),
        ('Infeasible', 'None of the tested mixes can satisfy both rules at the same time.'),
        ('Percentage point', 'A change from 20% to 25% is 5 percentage points.'),
    ], columns=['Term', 'Meaning']))
    st.info('In Meridian, lowering equity’s return estimate from 8% to 7% moves equity from 55% to 80%. More equity is needed to reach the unchanged objective, and estimated volatility rises from 9.44% to 12.94%.')


def draft_preset():
    st.session_state['objective'] = 7.5
    st.session_state['reserve_minimum'] = 10.0


with st.sidebar:
    st.markdown('### ◈ Portfolio Studio')
    st.caption('AI FINANCE · LAB 15')
    page = st.radio('Explore', ['Dashboard', 'Market quotes', 'How it works', 'Lab notebook'])
    st.divider()
    source = st.selectbox('Investment universe', ['Meridian training', 'My five ETFs', 'Upload CSV'])
    uploaded = st.file_uploader('Upload prices.csv', type=['csv']) if source == 'Upload CSV' else None
    st.number_input('Return objective (%)', value=6.5, step=0.1, key='objective')
    st.number_input('Reserve minimum (%)', min_value=0.0, max_value=100.0,
                    value=3.0, step=1.0, key='reserve_minimum')
    last_36 = st.toggle('Use only the last 36 months', value=False)
    if source != 'Meridian training':
        st.button('Use my Lab 13 draft: 7.5% / 10%', on_click=draft_preset)
        st.caption('For the short-term Treasury buffer, select only SGOV below. Confirm the remaining mandate rules separately.')
    st.caption('Estimates are historical inputs, not promises. No trading or payment connection.')

objective = st.session_state['objective'] / 100
minimum = st.session_state['reserve_minimum'] / 100

if page == 'How it works':
    guide()
    st.caption('built with AI help, a learning demonstration, not investment advice.')
    st.stop()

if page == 'Market quotes':
    st.title('Markets, with context')
    st.write('Latest available free quotes for your five research ETFs.')
    market_watch(ETF_TICKERS, full=True)
    st.caption('built with AI help, a learning demonstration, not investment advice.')
    st.stop()

st.markdown('<div class="studio-eyebrow">PORTFOLIO STUDIO / LAB 15</div>', unsafe_allow_html=True)
st.title('Portfolio Stability Decision' if page == 'Dashboard' else 'Your lab notebook')
st.caption('built with AI help, a learning demonstration, not investment advice.')
st.markdown('<p class="studio-intro">Find the lowest-risk mix that meets your rules. Then see what changes when your estimates do.</p>', unsafe_allow_html=True)

try:
    raw = None
    if source == 'Meridian training':
        dataset = 'Meridian'
        loaded_vehicles, loaded_correlations = portfolio.VEHICLES, portfolio.CORRELATIONS
        active_vehicles, active_correlations = loaded_vehicles, loaded_correlations
        default_eligible = portfolio.RESERVE_ELIGIBLE
        st.caption('MERIDIAN · fixed course training inputs · objective and reserves are editable in the sidebar')
        if last_36:
            st.info('The 36-month switch applies to historical prices. Meridian uses fixed training inputs.')
    else:
        if source == 'My five ETFs':
            raw = (DATA_DIR / 'prices.csv').read_bytes()
        elif uploaded:
            raw = uploaded.getvalue()
        else:
            st.info('Upload monthly adjusted prices to begin, or choose My five ETFs.')
            st.stop()
        dataset = hashlib.sha256(raw).hexdigest()[:16]
        loaded = portfolio.estimate_from_csv(BytesIO(raw))
        active = portfolio.estimate_from_csv(BytesIO(raw), last_36=last_36)
        loaded_vehicles, loaded_correlations = loaded['vehicles'], loaded['correlations']
        active_vehicles, active_correlations = active['vehicles'], active['correlations']
        default_eligible = {'SGOV'} if source == 'My five ETFs' else set()
        st.caption(f"{source.upper()} · {active['months']} monthly returns · prices {active['price_start']} → {active['price_end']}")
        if loaded['months'] < 60:
            st.warning('Fewer than five years of monthly returns. Use 61 monthly prices for 60 monthly returns.')
        st.caption('A historical average is an estimate, not a forecast. Market quotes are displayed separately.')

    with st.expander('Return estimates & reserve eligibility', expanded=True):
        st.write('Change a return estimate to stress the answer. Tick only the assets your mandate permits as reserves.')
        changed_vehicles, eligible = [], set()
        for index, (name, estimate, volatility) in enumerate(active_vehicles):
            left, right = st.columns([3, 2])
            with left:
                edited = st.number_input(f'{name} return estimate (%)', value=estimate * 100,
                    step=0.1, format='%.2f', key=f'return_{dataset}_{last_36}_{index}') / 100
            with right:
                if st.checkbox(f'{name} reserve-eligible', value=name in default_eligible,
                               key=f'reserve_{dataset}_{index}'):
                    eligible.add(name)
            changed_vehicles.append((name, edited, volatility))
    eligibility = tuple(sorted(eligible))
    baseline = optimize(loaded_vehicles, loaded_correlations, objective, minimum, eligibility)
    current = optimize(changed_vehicles, active_correlations, objective, minimum, eligibility)

    if page == 'Lab notebook':
        st.subheader('Your evidence, ready to review')
        rows = []
        for label, result in [('As loaded', baseline), ('Current inputs', current)]:
            rows.append({'Scenario': label, 'Weights (%)': ', '.join(f'{v[0]} {w * 100:.0f}' for v, w in zip(loaded_vehicles, result['weights'])) if result else 'no mix meets the objective',
                         'Return estimate': f"{result['expected_return']:.2%}" if result else '—',
                         'Volatility': f"{result['volatility']:.2%}" if result else '—'})
        st.dataframe(pd.DataFrame(rows), hide_index=True, width='stretch')
        partner = st.text_area('Partner exercise: what did they change, and what happened?', key='partner_notes')
        decision = st.selectbox('Your allocation decision', ['Not decided', 'Adopt', 'Pilot', 'Reject'], key='decision')
        condition = st.text_area('Your reason and the condition that would change your decision', key='decision_reason')
        st.caption('These are your own observations and judgment. Leave them blank until you have completed the exercise.')
        report = ['# Lab 15 — App session record', f'Generated: {datetime.now(timezone.utc).isoformat()}',
                  f'Universe: {source}', f'Objective: {objective:.2%}; reserve minimum: {minimum:.2%}.',
                  f'Reserve-eligible: {", ".join(eligibility) or "none"}.',
                  f'Current window: {"last 36 months" if last_36 and raw else "all months / Meridian inputs"}.',
                  '\n## Return estimates used',
                  *[f'- {v[0]}: loaded {original[1]:.4%}; current {v[1]:.4%}' for original, v in zip(loaded_vehicles, changed_vehicles)],
                  '\n## Results']
        for row in rows:
            report.append(f"- {row['Scenario']}: {row['Weights (%)']}; return {row['Return estimate']}; volatility {row['Volatility']}.")
        if baseline and current:
            difference = max(abs(a-b) for a,b in zip(baseline['weights'], current['weights'])) * 100
            report.append(f'Largest weight change: {difference:.2f} percentage points.')
        report += ['\n## Partner exercise', partner or 'Not completed.', '\n## My decision', decision,
                   condition or 'Reason and condition not yet entered.',
                   '\nBuilt with AI help. No partner work or final decision is implied by blank fields.']
        st.download_button('Download this lab record (.md)', '\n\n'.join(report),
                           file_name='Lab15_session_record.md', mime='text/markdown')
        st.info('The prepared Lab15_Completion_Guide.md in Class_Notes/Lab_15 contains the verified full-window, 36-month, and one-point stress results, plus the remaining student steps.')
        st.stop()

    left, right = st.columns(2, gap='large')
    with left:
        show_mix('As loaded · all months' if raw else 'As loaded · Meridian', baseline, loaded_vehicles)
    with right:
        show_mix('Current inputs · lowest-risk mix', current, changed_vehicles)
    if baseline and current:
        changes = [{'Asset': v[0], 'As loaded': a * 100, 'Current inputs': b * 100}
                   for v, a, b in zip(loaded_vehicles, baseline['weights'], current['weights'])]
        largest = max(abs(a-b) for a,b in zip(baseline['weights'], current['weights'])) * 100
        st.metric('Largest weight change (percentage points)', f'{largest:.2f}')
        data = pd.DataFrame(changes).melt('Asset', var_name='Scenario', value_name='Weight (%)')
        bars = alt.Chart(data).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
            x=alt.X('Asset:N', title=None, axis=alt.Axis(labelAngle=0, labelLimit=210)),
            xOffset='Scenario:N', y=alt.Y('Weight (%):Q', scale=alt.Scale(domain=[0, 100])),
            color=alt.Color('Scenario:N', scale=alt.Scale(range=['#94a3b8', '#0f766e'])),
            tooltip=['Asset', 'Scenario', alt.Tooltip('Weight (%):Q', format='.2f')]).properties(height=260)
        st.altair_chart(chart_style(bars), width='stretch')
    else:
        st.info('Largest weight change is unavailable unless both scenarios have a feasible mix.')

    st.divider()
    st.header('Build your own mix')
    st.write('Move a weight dial. The other weights rebalance automatically so your total stays at 100%.')
    prefix = f'manual_{dataset}'
    state_key = f'{prefix}_weights'
    if state_key not in st.session_state:
        initial = [round(w * 100) for w in current['weights']] if current else [100 // len(changed_vehicles)] * len(changed_vehicles)
        initial[0] += 100 - sum(initial)
        st.session_state[state_key] = initial
    for i, value in enumerate(st.session_state[state_key]):
        if f'{prefix}_{i}' not in st.session_state:
            st.session_state[f'{prefix}_{i}'] = value

    def move_dial(index):
        adjusted = portfolio.rebalance_weights_percent(st.session_state[state_key], index,
                                                       st.session_state[f'{prefix}_{index}'])
        st.session_state[state_key] = adjusted
        for i, value in enumerate(adjusted):
            st.session_state[f'{prefix}_{i}'] = value

    if current and st.button('Set dials to the current lowest-risk mix'):
        values = [round(w * 100) for w in current['weights']]
        st.session_state[state_key] = values
        for i, value in enumerate(values):
            st.session_state[f'{prefix}_{i}'] = value
    controls, visual = st.columns([1, 1.3], gap='large')
    with controls:
        for i, asset in enumerate(changed_vehicles):
            st.slider(f'{asset[0]} weight (%)', 0, 100, step=1,
                      key=f'{prefix}_{i}', on_change=move_dial, args=(i,))
        st.caption(f"Total allocation: {sum(st.session_state[state_key])}% · manual dials use 1-point steps; the optimizer uses 5-point steps.")
    manual = portfolio.evaluate_mix([w / 100 for w in st.session_state[state_key]],
                                    changed_vehicles, active_correlations, eligible)
    with visual:
        allocation_chart(manual, changed_vehicles)
    one, two, three = st.columns(3)
    one.metric('Your mix · return estimate', f"{manual['expected_return']:.2%}")
    two.metric('Your mix · annualized volatility', f"{manual['volatility']:.2%}")
    three.metric('Your mix · reserve weight', f"{manual['reserve_weight']:.2%}")
    passes = portfolio.meets_objective(manual['expected_return'], objective) and manual['reserve_weight'] >= minimum - 1e-12
    if passes:
        st.success('Your manual mix meets the selected return and reserve rules.')
    else:
        missing = []
        if not portfolio.meets_objective(manual['expected_return'], objective):
            missing.append('return estimate below objective')
        if manual['reserve_weight'] < minimum - 1e-12:
            missing.append('reserve weight below minimum')
        st.warning('Your manual mix: ' + '; '.join(missing) + '.')
    points = [{'Portfolio': name, 'Return (%)': result['expected_return'] * 100,
               'Volatility (%)': result['volatility'] * 100}
              for name, result in [('As loaded', baseline), ('Current optimum', current), ('Your manual mix', manual)] if result]
    st.subheader('Risk and return, side by side')
    scatter = alt.Chart(pd.DataFrame(points)).mark_circle(size=180, opacity=.9).encode(
        x=alt.X('Volatility (%):Q', scale=alt.Scale(zero=True)),
        y=alt.Y('Return (%):Q', scale=alt.Scale(zero=True)),
        color=alt.Color('Portfolio:N', scale=alt.Scale(range=COLORS)),
        tooltip=['Portfolio', alt.Tooltip('Return (%):Q', format='.2f'), alt.Tooltip('Volatility (%):Q', format='.2f')]).properties(height=280)
    target = alt.Chart(pd.DataFrame({'Target': [objective * 100]})).mark_rule(
        strokeDash=[5, 5], color='#d97706').encode(y='Target:Q')
    st.altair_chart(chart_style(scatter + target), width='stretch')
    st.caption('Further right means more estimated fluctuation. Higher means more estimated return. The dashed line is your return objective. Overlapping points have the same estimates.')

    if raw:
        with st.expander('Historical growth · compare each ETF from the same starting point', expanded=False):
            prices = pd.read_csv(StringIO(raw.decode('utf-8-sig')))
            date_col = prices.columns[0]
            rebased = prices.copy()
            for ticker in prices.columns[1:]:
                rebased[ticker] = prices[ticker] / prices[ticker].iloc[0] * 100
            history = rebased.melt(date_col, var_name='ETF', value_name='Growth of 100')
            chart = alt.Chart(history).mark_line(strokeWidth=2).encode(
                x=alt.X(f'{date_col}:T', title='Month'), y=alt.Y('Growth of 100:Q', scale=alt.Scale(zero=False)),
                color=alt.Color('ETF:N', scale=alt.Scale(range=COLORS)),
                tooltip=[alt.Tooltip(f'{date_col}:T', title='Month'), 'ETF', alt.Tooltip('Growth of 100:Q', format='.2f')]).properties(height=320)
            st.altair_chart(chart_style(chart), width='stretch')
            st.caption('Adjusted historical prices rebased to 100. Full saved window, including payouts and split adjustments from Yahoo. This is an asset comparison, not a backtest of your manual mix.')
    st.divider()
    watchlist = tuple(v[0] for v in loaded_vehicles) if raw else ETF_TICKERS
    market_watch(watchlist)
except (ValueError, UnicodeError, OSError) as error:
    st.error(str(error))
    st.stop()
