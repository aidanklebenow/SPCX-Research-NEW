"""Standard-library audit of frozen legacy evidence; not Project 1 cold-run validation."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys
ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / 'validation' / 'logs'
LOG.mkdir(exist_ok=True)
checks = [('lab10_tests', 'lab-10/Lab10_test_visa_proforma.py', [], 0),
          ('lab11_tests', 'lab-11/Lab11_test_sensitivity.py', [], 0),
          ('abg_known_answer', 'lab-09/proforma.py', [], 0),
          ('abg_broken_cash', 'lab-09/proforma.py', ['--break-2026-cash'], 1),
          ('visa_broken_cash', 'lab-10/Lab10_visa_proforma.py', ['--break-2026-cash'], 1),
          ('earlier_fcff', 'earlier-research/visa_dcf.py', [], 0)]
results = []
for label, rel, args, expected in checks:
    script = ROOT / 'legacy' / 'Visa' / rel
    command = [sys.executable, str(script), *args]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    (LOG / (label + '.txt')).write_text('UTC: ' + started + '\nCommand: ' + repr(command) + '\nExit: ' + str(run.returncode) + '\nSTDOUT:\n' + run.stdout + '\nSTDERR:\n' + run.stderr)
    ok = run.returncode == expected
    if label == 'abg_known_answer': ok = ok and 'Value per share: $291.75' in run.stdout
    if label.endswith('broken_cash'): ok = ok and 'VALUATION REFUSED' in run.stderr and 'Value per share:' not in run.stdout
    results.append(dict(check=label, passed=ok, expected_exit=expected, actual_exit=run.returncode, script_sha256=hashlib.sha256(script.read_bytes()).hexdigest(), utc=started))
    print(label + ': ' + ('PASS' if ok else 'FAIL'))
(LOG / 'legacy_audit.json').write_text(json.dumps({'python':sys.version,'executable':sys.executable,'scope':'legacy snapshots only; not fresh-environment cold run or integrated FCFF validation','results':results}, indent=2) + '\n')
sys.exit(0 if all(r['passed'] for r in results) else 1)
