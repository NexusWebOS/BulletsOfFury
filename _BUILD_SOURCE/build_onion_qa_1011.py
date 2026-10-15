"""Persist the exact source-identity and native-pixel evidence for the correction."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
bank=json.loads((ROOT/'assets/part2_art_1010.js').read_text().split('const P2_ART=',1)[1].strip().rstrip(';'))
paths={'source_and_game':'_shots/part2_1011/report.json', 'onion_preview':'_shots/part2_1010/review/report.json',
       'presentation':'_shots/part2_1010/presentation/report.json','finishing':'_shots/part2_1010/finishing/report.json'}
reports={k:json.loads((ROOT/v).read_text()) for k,v in paths.items()}
log=ROOT/'_shots/part2_1010/onion-full-tests-final.log';text=log.read_text(encoding='utf-8',errors='replace')
assert 'FALVA/LIZZIE BUILD OK, 0 ERRORS' in text
assert all(not q['failed'] and not q['errors'] for q in reports.values())
report=dict(date='2026-10-11', feedback='Atomic crop/anchor, Furnace origin and exact opening stealth fighter palette corrections',
    owners=['build_part2_art_1010.py','prepare_part2_onion_1011.py','repair_part2_art_1011.py','part2_combat_1010.js'],
    art={k:dict(cells=len(v),unique_plates=len({a['sha256'] for a in v}),dimensions=[v[0]['w'],v[0]['h']],pivot=v[0]['pivot']) for k,v in bank.items()},
    source_count=dict(atomic_original=28,atomic_drawn_inbetweens=4,fire_column=32,fire_root=16,stealth='original whv_ace/skycarrier family, three palettes; original roll aliases retained'),
    source_audit=json.loads((ROOT/'_ART_SOURCES/part2_1011/audit.json').read_text()),
    verification=dict(syntax='node --check assets/game.js, part2_combat_1010.js, part2_art_1010.js: pass',
      final_summary='FALVA/LIZZIE BUILD OK, 0 ERRORS',passing_assertions=sum(s.startswith('  ok ') for s in text.splitlines()),exit_code=0,
      initial_nonzero_run='Stopped before final summary: test canvas lacked bezierCurveTo. Test-local canvas stub completed/restored; full suite rerun to final summary.',
      native_passed=sum(r['passed'] for r in reports.values()),reports=reports),
    preview='docs/previews/part2_1010/index.html?revision=20261011',
    limits=['Controlled invulnerable fixtures verify native art and encounter continuity, not a natural Furious campaign clear.'],git='No commit or push; preserve all earlier staged, unstaged and untracked work.')
f=ROOT/'docs/qa/animation_onion_1011.json';f.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(dict(assertions=report['verification']['passing_assertions'],native=report['verification']['native_passed'],art=report['art'])))
