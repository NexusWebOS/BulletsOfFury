"""Persist final native evidence and source provenance for the drawn-motion pass."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


banks = json.loads((ROOT / 'assets/part2_art_1010.js').read_text().split('const P2_ART=', 1)[1].strip().rstrip(';'))
paths = {
    'drawn_motion': '_shots/part2_motion_1011/report.json',
    'preview': '_shots/part2_1010/review/report.json',
    'presentation': '_shots/part2_1010/presentation/report.json',
    'finishing': '_shots/part2_1010/finishing/report.json',
}
reports = {name: json.loads((ROOT / path).read_text()) for name, path in paths.items()}
assert all(not r['failed'] and not r['errors'] for r in reports.values())
log_path = '_shots/part2_motion_1011/full-tests.log'
log = (ROOT / log_path).read_text(encoding='utf-8', errors='replace')
assert 'FALVA/LIZZIE BUILD OK, 0 ERRORS' in log
assert not any(line.startswith('  FAIL ') for line in log.splitlines())
runtime = ['assets/game.js', 'assets/part2_art_1010.js', 'assets/part2_combat_1010.js',
           'assets/part2_motion_1011.js', 'assets/part2_fire_renderer_1011.js']
syntax = {}
for path in runtime:
    result = subprocess.run(['node', '--check', path], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    syntax[path] = dict(exit_code=result.returncode, sha256=digest(path))
art = {name: dict(cells=len(rows), unique_images=len({r['sha256'] for r in rows}),
                 dimensions=[rows[0]['w'], rows[0]['h']], pivot=rows[0]['pivot'])
       for name, rows in banks.items()}
assert all(a['w'] % 2 == 0 and a['h'] % 2 == 0 for rows in banks.values() for a in rows)
for rows in banks.values():
    for a in rows:
        assert digest(a['path']) == a['sha256'], a['key']
sources = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
           for p in sorted((ROOT / '_ART_SOURCES/part2_motion_1011').glob('*raw.png'))}
report = dict(
    generated_utc=datetime.now(timezone.utc).isoformat(),
    request='Drawn barrel rolls and somersaults for all stealth fighters; complete Furnace fire crown; Maverick helix palettes; smooth atomic cloud.',
    owners=['_BUILD_SOURCE/build_part2_art_1010.py', '_BUILD_SOURCE/part2_motion_art_1011.py',
            '_BUILD_SOURCE/build_part2_review_1010.py', '_BUILD_SOURCE/build_drawn_motion_qa_1011.py',
            'assets/part2_combat_1010.js', 'assets/part2_motion_1011.js', 'assets/part2_fire_renderer_1011.js'],
    art=art,
    totals=dict(registered_cells=sum(len(rows) for rows in banks.values()),
                unique_images=len({a['sha256'] for rows in banks.values() for a in rows}),
                newly_drawn_source_poses=112, derived_palette_cells=128),
    source_images=sources,
    prompts=['_ART_SOURCES/part2_motion_1011/prompts.json', '_ART_SOURCES/part2_motion_1011/orange_prompts.json'],
    source_audit=json.loads((ROOT / '_ART_SOURCES/part2_motion_1011/audit.json').read_text()),
    verification=dict(syntax=syntax, suite_command='node _BUILD_SOURCE/test_fl.js',
                      final_summary='FALVA/LIZZIE BUILD OK, 0 ERRORS',
                      passing_assertions=sum(line.startswith('  ok ') for line in log.splitlines()),
                      suite_log=log_path, suite_log_sha256=digest(log_path),
                      native_passed=sum(r['passed'] for r in reports.values()),
                      native_failed=sum(r['failed'] for r in reports.values()),
                      native_report_paths=paths, native_reports=reports),
    preview='http://127.0.0.1:8794/docs/previews/part2_1010/index.html?revision=20261011-motion',
    limits=['Controlled encounter fixtures verify pixels, movement, attacks and errors; they do not establish a natural human Furious campaign clear.'],
    git='Local only. Main HEAD 7539951; prior staged, unstaged and untracked work preserved. No commit or push requested.',
)
target = ROOT / 'docs/qa/drawn_motion_1011.json'
target.write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(dict(assertions=report['verification']['passing_assertions'],
                      native=report['verification']['native_passed'], **report['totals'])))
