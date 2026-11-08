from pathlib import Path
import json,shutil,hashlib
W=Path(__file__).resolve().parent
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
V=Path(r'C:/Users/Mike/Documents/New project/BOF-Furious-Boss-Videos-1104')
S=R/'_BUILD_SOURCE/razorwake_modular_1104'
Q=R/'docs/qa/razorwake_modular_wind_1104';Q.mkdir(parents=True,exist_ok=True)
shutil.copy2(W/'REPORT.md',R/'docs/RAZORWAKE_MODULAR_WIND_1104.md')
for src,name in [(W/'probe/report.json','native.json'),(W/'art-checks/report.json','art.json'),(W/'full-suite.log','required-suite.log'),(V/'preview-checks.json','preview.json'),(V/'report.json','recording-preview.json')]:shutil.copy2(src,Q/name)
F=R/'_shots/boss_comparison_1102/razorwake-modular-wind-1104'
shutil.copy2(F/'batch.json',Q/'movie-batch.json');shutil.copy2(F/'stage6-mini/report.json',Q/'movie-report.json')
for label in ['modular-wind','modular-wind-cached']:
 p=W/'profile'/(label+'.json')
 if p.exists():
  a=json.loads(p.read_text());out={k:a[k] for k in ['label','fps','p95','p99','top','errors']};out['functions']=a['details']['stats']['functions'];(Q/(label+'-profile.json')).write_text(json.dumps(out,indent=2))
for name in ['rotary-attack.png','wing-storm-warn.png','wing-storm-attack.png','one-gun-detached.png']:shutil.copy2(W/'probe'/name,Q/name)
shutil.copy2(W/'film-review.png',Q/'film-review.png')
for p in W.glob('*.py'):shutil.copy2(p,S/p.name)
shutil.copy2(W/'REPORT.md',S/'REPORT.md')
p=R/'assets/data/ART_TAXONOMY.json';raw=p.read_bytes();data=json.loads(raw)
data['rw117_']={'role':'furious_stage6_razorwake_disjoint_hinged_wings_rotary_chainguns_static_source_thrusters_and_charged_wind_arsenal','owner':'_BUILD_SOURCE/razorwake_modular_1104/build_razor.py','manifest':'assets/game/levels/stage_06/miniboss/razorwake_modular_1104/manifest.json','note':'Two built-in image_gen sources with exact prompts and editable Aseprite retained.2620 authored even-cell frames/25banks/34pages,32headings and24hinge poses. Separate complete gun pods detach without erasing wings; native1653HP/2gun-core gate/hit flashes/rewards preserved. Supersedes live Furious Razorwake only. One static source exhaust uses baked glow/throttle banks. No PixelLab generation claimed. See docs/RAZORWAKE_MODULAR_WIND_1104.md.'}
newline='\r\n'if raw.count(b'\r\n')>raw.count(b'\n')/2 else'\n';p.write_bytes((json.dumps(data,indent=2,ensure_ascii=False)+'\n').replace('\n',newline).encode('utf8'))
note='''<!-- razorwake-modular-wind-1104 -->
## November5 — Razorwake modular chainguns, hinged wings and wind arsenal

RW117 replaces live Furious Razorwake art/attack book with regenerated intact fuselage/wings and two detachable rotary guns. Actual spinning/recoiling gun mouths fire straight wind-slug streams; strong one-source exhaust uses authored pixel-light grades. Core cyclone1015 charge and accelerating24-pose wing flaps darken the layered city, show the real metal warning and launch a generated sweeping tornado. Preserve native1653HP, two496HP guns/661HP core gate, source-pixel hits, finite wind hazards and once-only native defeat.2620authored/Aseprite-verified frames/656exact masks;35native checks and11preview checks pass. Source-stable native full fight54.83engineFPS, audible and complete. Readiness caching removes repeated scans; separate instrumented profile remains40.93FPS and is documented honestly. Required broad suite retains the pre-existing missing health-helper setup error. See docs/RAZORWAKE_MODULAR_WIND_1104.md; current review http://127.0.0.1:65120/?razorwake=modular-wind-1104#razorwake . Core game.js unchanged; no commit/push.

'''
for name in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/name;raw=p.read_bytes()
 if b'<!-- razorwake-modular-wind-1104 -->'not in raw:
  nl='\r\n'if raw.count(b'\r\n')>raw.count(b'\n')/2 else'\n';p.write_bytes(note.replace('\n',nl).encode('utf8')+raw)
checks=json.loads((Q/'native.json').read_text());art=json.loads((Q/'art.json').read_text());batch=json.loads((Q/'movie-batch.json').read_text())['jobs']['stage6-mini'];movie=R/batch['path']
receipt=dict(nativePassed=sum(c['passed']for c in checks['checks']),nativeTotal=len(checks['checks']),artPassed=art['passed'],frames=art['frames'],masks=art['masks'],movie=batch,movieSHA256=hashlib.sha256(movie.read_bytes()).hexdigest(),review='http://127.0.0.1:65120/?razorwake=modular-wind-1104#razorwake',gameSHA256=hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest(),sources={name:hashlib.sha256((R/name).read_bytes()).hexdigest()for name in ['assets/razorwake_modular_1104.js','assets/razorwake_modular_art_1104.js','assets/projectile_fx_1103.js','index.html']},requiredSuite='pre-existing ReferenceError: difficultyHealthBaseline15 is not defined',limits='No full campaign or human dodgeability certification; no commit/push.')
(Q/'summary.json').write_text(json.dumps(receipt,indent=2));print('Saved',receipt['nativePassed'],'native checks,',art['frames'],'frames, final film and source receipts.')
