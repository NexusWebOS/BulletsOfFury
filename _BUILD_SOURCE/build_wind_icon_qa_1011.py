"""Keep final Wind badge source and native UI evidence reproducible."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
art=json.loads((ROOT/'assets/audio_fx_art_1010.js').read_text().split('const AP10_FX_ART=',1)[1].strip().rstrip(';'))
paths={'menus_and_reward':'_shots/wind_icons_1011/report.json','audio_review':'_shots/audio_1010/preview-report.json'}
reports={k:json.loads((ROOT/v).read_text()) for k,v in paths.items()}
assert all(not r['failed'] and not r['errors'] for r in reports.values())
log='_shots/wind_icons_1011/full-tests.log';text=(ROOT/log).read_text(encoding='utf-8',errors='replace')
receipt=json.loads((ROOT/'_shots/wind_icons_1011/suite-exit.json').read_text(encoding='utf-8-sig'))
assert receipt['exit_code']==0 and 'FALVA/LIZZIE BUILD OK, 0 ERRORS' in text
banks={k:art[k] for k in ['wind_icons','wind_symbol']}
for rows in banks.values():
 for a in rows:assert digest(a['path'])==a['sha256'] and a['w']==128 and a['h']==128 and a['pivot']==[64,64]
report=dict(date=datetime.now(timezone.utc).isoformat(),request='Replace Wind hardware pictures with authored-style projectile badges and a separate Stage6 Wind symbol.',
 tool='built-in image_gen',prompts='_ART_SOURCES/wind_icons_1011/prompts.json',
 sources={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'_ART_SOURCES/wind_icons_1011').glob('*raw.png')},
 owners=['build_audio_fx_1010.py','wind_icon_art_1011.py','build_wind_icon_review_1011.py','assets/audio_wind_1010.js'],
 banks=banks,source_registration=json.loads((ROOT/'_ART_SOURCES/wind_icons_1011/registration.json').read_text()),
 verification=dict(full_suite_command='node _BUILD_SOURCE/test_fl.js',exit_code=receipt['exit_code'],
  final_summary='FALVA/LIZZIE BUILD OK, 0 ERRORS',passing_assertions=sum(s.startswith('  ok ') for s in text.splitlines()),log=log,log_sha256=digest(log),
  native_passed=sum(r['passed'] for r in reports.values()),native_reports=reports,native_report_paths=paths),
 preview='http://127.0.0.1:8794/docs/previews/wind_icons_1011/index.html',
 limits=['Controlled fixtures verify native menus and the real boss-drop reward handler; they do not constitute a natural Stage6 fight clear.'],
 git='Main7539951. Local only. All prior staged, unstaged and untracked work preserved.')
(ROOT/'docs/qa/wind_icons_1011.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(dict(assertions=report['verification']['passing_assertions'],native=report['verification']['native_passed'],icons=45,symbols=1)))
