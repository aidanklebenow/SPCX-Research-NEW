"""Lab 11 Visa one-at-a-time operating sensitivity; standard library only.

Run from Visa: python3 -B lab-11/Lab11_sensitivity.py
Uses the frozen Lab11_engine.py via functions, not its inherited Lab 10 CLI.
Writes results, full visible output and an AI-assisted report beside this file.
"""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
from contextlib import redirect_stdout

import Lab11_engine as engine

HERE = Path(__file__).resolve().parent
OUTPUTS = ('operating_profit', 'fcfe', 'per_share')
TOLERANCE = 1e-6


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def differences(left, right, prefix=''):
    """Return changed leaf paths, checking all inputs including opening history."""
    if isinstance(left, dict) and isinstance(right, dict):
        result = []
        for key in sorted(set(left) | set(right)):
            path = f'{prefix}.{key}' if prefix else key
            if key not in left or key not in right:
                result.append(path)
            else:
                result += differences(left[key], right[key], path)
        return result
    return [] if left == right else [prefix]


def evaluate(data, name, driver=None, level=None):
    result = dict(name=name, driver=driver, level=level, inputs=deepcopy(data),
                  rows=[], checks=[], accounting_valid=False, valuation_valid=False,
                  errors=[], outputs={k: None for k in OUTPUTS})
    try:
        rows = engine.project(deepcopy(data))
        result['rows'] = rows
        for i, r in enumerate(rows):
            result['checks'].append(dict(
                year=r['year'], balance_gap=engine.gap(r),
                cash_bridge_gap=r['cash']-r['opening_cash']-r['cfo']-r['cfi']-r['cff'],
                cash=r['cash'], cash_floor=data['assumptions']['minimum_cash'],
                revolver=r['revolver'], revolver_limit=data['assumptions']['revolver_limits'][i]))
        # Retain signed outputs even when checks fail; flag them as unusable.
        result['outputs']['operating_profit'] = rows[-1]['operating_income']
        result['outputs']['fcfe'] = rows[-1]['fcfe']
        engine.check(rows, data)
        result['accounting_valid'] = True
    except (ValueError, KeyError, TypeError, IndexError) as error:
        result['errors'].append(f'Accounting/financing invalid: {error}')
        return result
    if any(r['fcfe'] < 0 for r in rows):
        result['errors'].append('Value unavailable: negative FCFE retained; no positive-only valuation or unsupported funding assumption.')
        return result
    try:
        valuation = engine.value(rows, data)
        result['valuation'] = valuation
        result['outputs']['per_share'] = valuation['per_share']
        result['valuation_valid'] = True
    except ValueError as error:
        result['errors'].append(f'Value unavailable: {error}')
    return result


def usable(run, output):
    return run['accounting_valid'] and (output != 'per_share' or run['valuation_valid'])


def analyze(base, ranges):
    pristine = deepcopy(base)
    before = evaluate(deepcopy(base), 'base_before')
    if not before['accounting_valid']:
        raise ValueError('Base accounting checks failed: ' + '; '.join(before['errors']))
    runs = []
    for driver, spec in ranges['drivers'].items():
        if base['assumptions'][driver] != spec['base']:
            raise ValueError(f'{driver}: selected range base differs from frozen model base')
        for level in ('lower', 'base', 'higher'):
            values = spec[level]
            if len(values) != 5 or any(not 0 <= v < 1 for v in values):
                raise ValueError(f'{driver}/{level}: require five rate fractions in [0, 1)')
            data = deepcopy(pristine)
            data['assumptions'][driver] = list(values)
            changed = differences(pristine, data)
            expected = [] if level == 'base' else [f'assumptions.{driver}']
            if changed != expected:
                raise ValueError(f'{driver}/{level}: unexpected input changes {changed}')
            run = evaluate(data, f'{driver}_{level}', driver, level)
            run['changed_input_paths'] = changed
            run['only_selected_input_changed'] = True
            run['deltas'] = {k: run['outputs'][k]-before['outputs'][k]
                             if usable(run, k) and usable(before, k) else None for k in OUTPUTS}
            runs.append(run)
    after = evaluate(deepcopy(pristine), 'base_restored')
    if base != pristine or after['inputs'] != before['inputs']:
        raise ValueError('Base inputs were mutated')
    if after['accounting_valid'] != before['accounting_valid'] or after['valuation_valid'] != before['valuation_valid']:
        raise ValueError('Restored-base status differs')
    max_difference = max(abs(x[k]-y[k]) for x, y in zip(before['rows'], after['rows']) for k in x)
    for key in OUTPUTS:
        a, b = before['outputs'][key], after['outputs'][key]
        if a is None or b is None:
            if a != b:
                raise ValueError(f'Restored {key} availability differs')
        else:
            max_difference = max(max_difference, abs(a-b))
    if max_difference > TOLERANCE:
        raise ValueError(f'Restored base differs by {max_difference}')
    spans = {}
    for driver in ranges['drivers']:
        group = [r for r in runs if r['driver'] == driver]
        spans[driver] = {}
        for key in OUTPUTS:
            values = [r['outputs'][key] for r in group if usable(r, key)]
            spans[driver][key] = dict(valid_runs=len(values), complete=len(values)==3,
                                     span=max(values)-min(values) if values else None)
    rankings = {}
    for key in OUTPUTS:
        if all(spans[d][key]['complete'] for d in spans):
            rankings[key] = sorted(spans, key=lambda d: spans[d][key]['span'], reverse=True)
        else:
            rankings[key] = None  # Incomplete/invalid cases never receive a ranking.
    return dict(base_before=before, runs=runs, base_restored=after, spans=spans,
                rankings=rankings, restored_base_pass=True,
                max_restored_difference=max_difference, tolerance=TOLERANCE)


def fmt(value, signed=False):
    if value is None:
        return 'N/A'
    return f'{value:+,.2f}' if signed else f'{value:,.2f}'


def visible_output(result, ranges):
    print('LAB 11 | VISA | ONE-AT-A-TIME OPERATING SENSITIVITY')
    print('Run UTC:', result['run_utc'])
    print('AI prediction SHA256:', result['prediction_sha256'])
    print('Annual model discount anchor: 2025-09-30; not a current spot valuation.')
    print('Years: FY2026, FY2027, FY2028, FY2029, FY2030')
    for driver, spec in ranges['drivers'].items():
        print(f'\n{driver}: {spec["units"]}; label: judgment')
        for level in ('lower', 'base', 'higher'):
            print(f'  {level}: ' + ', '.join(f'{v*100:.1f}%' for v in spec[level]))
        print('  Range reason:', spec['reason'])
    print('\nRESULTS: FY2030 profit/FCFE in USD millions; value in USD/share; signed deltas from base')
    print('Run | Profit | Delta | FCFE | Delta | Value | Delta | Status')
    for r in result['runs']:
        cells = []
        for k in OUTPUTS:
            cells += [fmt(r['outputs'][k]), fmt(r['deltas'][k], True)]
        status = 'PASS' if r['accounting_valid'] and r['valuation_valid'] else '; '.join(r['errors'])
        print(r['name'] + ' | ' + ' | '.join(cells) + ' | ' + status)
    print('\nSPANS (max - min among valid runs; rank only complete comparisons)')
    for driver, outputs in result['spans'].items():
        for key, span in outputs.items():
            print(f'{driver}/{key}: {fmt(span["span"])}; valid {span["valid_runs"]}/3')
    for key, ranking in result['rankings'].items():
        print(f'{key} ranking OVER THESE RANGES: {ranking or "Unavailable: incomplete valid comparison"}')
    for r in [result['base_before'], *result['runs'], result['base_restored']]:
        print('\n' + '='*70 + '\nFULL STATEMENTS AND CHECKS: ' + r['name'])
        print('Actual independent assumptions:', json.dumps(r['inputs']['assumptions'], sort_keys=True))
        print('Changed independent paths:', r.get('changed_input_paths', []))
        for check in r['checks']:
            print(f"FY{check['year']}: BS gap={check['balance_gap']:.8f}; cash gap={check['cash_bridge_gap']:.8f}; "
                  f"cash={check['cash']:.2f} >= {check['cash_floor']:.2f}; revolver={check['revolver']:.2f} <= {check['revolver_limit']:.2f}")
        print('Complete accounting/financing gate:', 'PASS' if r['accounting_valid'] else 'FAIL')
        for error in r['errors']:
            print(error)
        if r['rows']:
            engine.table('INCOME STATEMENT', r['rows'], ['gross_revenue','incentives','revenue']
                         + list(r['inputs']['assumptions']['expense_ratios'])
                         + ['depreciation','amortization','operating_income','interest','tax','net_income'])
            engine.table('BALANCE SHEET', r['rows'], list(engine.ASSETS)+['assets']
                         +list(engine.LIABILITIES)+['liabilities','equity'])
            engine.table('CASH FLOWS AND INCENTIVE TIMING', r['rows'],
                         ['change_incentive_assets','change_incentive_liability','incentive_cash_paid',
                          'change_wc_assets','change_wc_liabilities','cfo','capex','cfi',
                          'debt_issued','debt_repaid','change_revolver','fcfe','dividends','buybacks',
                          'cff','opening_cash','change_cash','cash'])
    print(f"\nRESTORED BASE PASS: max difference {result['max_restored_difference']}; tolerance {TOLERANCE}")


def report(result, ranges, prediction):
    lines = ['# Lab 11 — Visa operating sensitivity', '',
             '**Aidan adopted the suggested prediction under revised instructor instructions he reported. Analysis is AI-assisted; partner exchanges remain unverified.**', '',
             'Run UTC: '+result['run_utc']+'. The original Lab 10 model is unchanged. All amounts are USD millions except value per share.', '',
             '## Inputs and ranges', '',
             'All changes apply to FY2026–FY2030. The entire linked model is rerun from a fresh independent copy each time. Other input rates stay fixed; dollar statement accounts recalculate.', '',
             '| Driver/scenario | 2026 | 2027 | 2028 | 2029 | 2030 |', '|---|---:|---:|---:|---:|---:|']
    for driver, spec in ranges['drivers'].items():
        for level in ('lower','base','higher'):
            lines.append('| '+driver+' / '+level+' | '+' | '.join(f'{v:.1%}' for v in spec[level])+' |')
    for spec in ranges['drivers'].values():
        lines += ['', '**'+spec['label']+' — judgment:** '+spec['reason']]
    lines += ['', '[Annual filing]('+ranges['sources']['annual']+') · [Interim filing]('+ranges['sources']['interim']+')', '',
              '## Results and signed changes from base', '',
              '| Run | FY2030 operating profit | Change | FY2030 FCFE | Change | Value/share | Change |',
              '|---|---:|---:|---:|---:|---:|---:|']
    for r in result['runs']:
        cells=[]
        for key in OUTPUTS:
            cells += [fmt(r['outputs'][key]), fmt(r['deltas'][key],True)]
        lines.append('| '+r['name']+' | '+' | '.join(cells)+' |')
        if r['errors']:
            lines += ['', '**'+r['name']+' status:** '+'; '.join(r['errors']), '']
    lines += ['', '## Output spans', '', '| Input | Operating profit span | FCFE span | Value/share span |', '|---|---:|---:|---:|']
    for driver, outputs in result['spans'].items():
        lines.append('| '+driver+' | '+' | '.join(fmt(outputs[k]['span']) for k in OUTPUTS)+' |')
    lines += ['', 'Spans are maximum minus minimum across valid lower/base/higher results. Any incomplete comparison is not ranked. These are effects over the selected ranges, not probabilities or a universal ranking of Visa’s drivers.', '',
              '## Aidan’s adopted prediction — reconciliation', '',
              '[Aidan’s adopted prediction](Lab11_prediction.md) · [Unchanged numerical record](Lab11_AI_prediction.json)', '',
              '| Output | Adopted predicted change | Actual change | Actual minus predicted (percentage points) |', '|---|---:|---:|---:|']
    high=next(r for r in result['runs'] if r['name']=='gross_growth_higher')
    for key in OUTPUTS:
        base=result['base_before']['outputs'][key]
        actual=(high['outputs'][key]/base-1)*100 if usable(high,key) and base else None
        predicted=prediction['predicted_percent_changes'][key]
        lines.append(f'| {key} | {predicted:+.2f}% | {fmt(actual,True)}% | {fmt(actual-predicted if actual is not None else None,True)} |')
    lines += ['', 'The AI estimate used roughly five years of extra compounding. Differences arise because depreciation depends on earlier PP&E, capex and working capital change with activity, interest is largely fixed, and the valuation discounts different annual cash flows plus a separately normalized terminal value. This explanation is AI-generated, not Aidan’s submitted reflection.', '',
              '## AI explanation for Aidan to assess', '',
              'A growth-rate shift compounds across five years. Incentive rates instead change the revenue retained from a given pre-incentive revenue base. In this model, most operating costs also scale with net revenue, which partly offsets the earnings effect of higher incentives. Incentive asset/liability changes additionally affect cash-payment timing. Holding expense ratios fixed is a model assumption, not proof Visa can immediately reduce every cost.', '',
              'Read the spans before choosing your conclusion. A wider growth range and five-year compounding can affect which input ranks first. A different range or cost structure could change the ranking; neither scenario has an assigned probability.', '',
              '## Verification and valuation limitations', '',
              f"Restored base: **PASS**, largest difference across all statement values and displayed outputs = {result['max_restored_difference']}; tolerance = {TOLERANCE} in each output’s units. Base inputs are unchanged. Each changed run alters exactly one independent assumption path.", '',
              'Full inputs, signed statement details, check blocks and base restoration are in [Lab11_output.txt](Lab11_output.txt) and [Lab11_results.json](Lab11_results.json). Negative cash flows are never dropped. If any year has negative FCFE, this runner marks value unavailable instead of invoking the inherited positive-only valuation convention. Operating outputs remain available if accounting/financing checks pass; invalid runs are flagged and excluded from ranking.', '',
              'Per-share values remain conditional teaching-model values at the September 30, 2025 discount anchor. Fixed opening shares, simplified costs/financing and the abrupt 3% terminal regime remain unchanged. No current market price or current investment recommendation is inferred.', '',
              '## Required student and partner work — pending', '',
              '- Prediction: **adopted by Aidan**, using AI assistance under the revised instructor instructions he reported. The original estimate was recorded before scenario execution; adoption was confirmed afterward. See Lab11_prediction.md. No additional unaided prediction is treated as required here.',
              '- Partner pre-run input/unit/range check: **not performed or verified**.',
              '- Partner question, Aidan’s response and the check Aidan performs on their analysis: **pending**.',
              '- Aidan’s own conclusion about the largest driver over these ranges, prediction error, and whether the result changes his valuation conclusion or research priority: **pending**.',
              '- Final partner discussion, reflection, GitHub upload and individual submission: **pending**.', '',
              '## Reproduce', '', '```bash', 'python3 -B lab-11/Lab11_sensitivity.py', 'python3 -B lab-11/Lab11_test_sensitivity.py', '```', '',
              'Keep the engine, frozen inputs, ranges and numerical AI prediction beside the runner. The runner regenerates this report, results and visible output; put student/partner notes in a separate Lab11-named file to preserve them.', '']
    return '\n'.join(lines)


def main():
    paths = {name: HERE/name for name in ('Lab11_base_inputs.json','Lab11_ranges.json',
             'Lab11_AI_prediction.json','Lab11_engine.py')}
    hashes = {name:digest(path) for name,path in paths.items()}
    base=json.loads(paths['Lab11_base_inputs.json'].read_text())
    ranges=json.loads(paths['Lab11_ranges.json'].read_text())
    prediction=json.loads(paths['Lab11_AI_prediction.json'].read_text())
    if hashes['Lab11_engine.py'] != ranges['engine_sha256']:
        raise ValueError('Frozen engine hash mismatch')
    if hashes['Lab11_base_inputs.json'] != prediction['base_input_sha256']:
        raise ValueError('Base inputs differ from prediction context')
    started=datetime.now(timezone.utc)
    if datetime.fromisoformat(prediction['created_utc'].replace('Z','+00:00')) > started:
        raise ValueError('Prediction timestamp is later than run')
    result=analyze(base,ranges)
    result.update(run_utc=started.isoformat(), input_hashes=hashes,
                  prediction_sha256=hashes['Lab11_AI_prediction.json'])
    if any(digest(paths[name]) != h for name,h in hashes.items()):
        raise ValueError('Saved input, engine or prediction changed during execution')
    capture=io.StringIO()
    with redirect_stdout(capture):
        visible_output(result,ranges)
    (HERE/'Lab11_results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    (HERE/'Lab11_output.txt').write_text(capture.getvalue())
    (HERE/'Lab11_summary.md').write_text(report(result,ranges,prediction))
    print(capture.getvalue().split('\n'+'='*70)[0])
    print('Restored base PASS. Full statements and visible checks saved in Lab11_output.txt.')


if __name__ == '__main__':
    main()
