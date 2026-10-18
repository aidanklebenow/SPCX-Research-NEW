"""Reproduce Lab 13 evidence, verify frozen legacy hashes, and stage local files."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import mandate
OUT = ROOT / 'outputs/lab-13'
SUB = ROOT / 'submission/lab-13'
OUT.mkdir(parents=True, exist_ok=True)
SUB.mkdir(parents=True, exist_ok=True)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifest = json.loads((ROOT / 'legacy/manifest.json').read_text())
    mismatches = [entry['snapshot'] for entry in manifest['files']
                  if not (ROOT / entry['snapshot']).is_file()
                  or digest(ROOT / entry['snapshot']) != entry['sha256']]
    runs = {}
    for name, args in {
        'legacy_tests': ['validation/run_legacy_audit.py'],
        'lab13_tests': ['-m', 'unittest', 'discover', '-s', 'tests', '-v'],
        'Lab13_output': ['src/mandate.py'],
    }.items():
        run = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)
        (OUT / f'{name}.txt').write_text(run.stdout + run.stderr)
        runs[name] = {'command': [sys.executable, *args], 'exit_code': run.returncode}
    probe = dict(mandate.CANDIDATES['A'])
    probe['Cash'], probe['Global equity index fund'] = -2, 64
    (OUT / 'Lab13_probe.txt').write_text(mandate.report({'A negative-weight probe': probe}))
    passed = not mismatches and all(r['exit_code'] == 0 for r in runs.values())
    audit = {
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'python': sys.version, 'technical_validation_passed': passed,
        'legacy_files_checked': len(manifest['files']), 'legacy_hash_mismatches': mismatches,
        'runs': runs,
        'submission_ready': False,
        'remaining': ['Final student review and GitHub links submitted through Brightspace'],
        'scope': 'Lab 13 portfolio mandate; no integrated Visa FCFF/WACC validation claimed',
    }
    for source in [ROOT / 'src/mandate.py', OUT / 'Lab13_output.txt', OUT / 'Lab13_probe.txt']:
        shutil.copy2(source, SUB / source.name)
    audit['sha256'] = {str(p.relative_to(ROOT)): digest(p) for p in
                       [ROOT / 'src/mandate.py', ROOT / 'tests/test_mandate.py',
                        ROOT / 'research/course-requirements/lab-13-portfolio-mandate.md',
                        SUB / 'Lab13_summary.md',
                        *sorted(OUT.glob('*.txt'))]}
    (OUT / 'run_manifest.json').write_text(json.dumps(audit, indent=2) + '\n')
    print(json.dumps(audit, indent=2))
    return 0 if passed else 1

if __name__ == '__main__':
    sys.exit(main())
