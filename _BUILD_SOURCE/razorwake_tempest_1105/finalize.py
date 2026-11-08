from pathlib import Path
import json,shutil,hashlib,subprocess
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');V=W.parent/'BOF-Furious-Boss-Videos-1104'
F=R/'_shots/boss_comparison_1102/razorwake-tempest-final-ready-1105';D=R/'_shots/boss_comparison_1102/razorwake-vortex-final-1105'
j=json.loads((F/'batch.json').read_text())['jobs']['stage6-mini'];dj=json.loads((D/'batch.json').read_text())['jobs']['stage6-mini'];native=json.loads((W/'probe/report.json').read_text());art=json.loads((W/'art-checks/report.json').read_text());compat=json.loads((W/'compat-report.json').read_text());preview=json.loads((V/'preview-checks.json').read_text())
assert j['passed']and dj['passed']and art['passed']and all(x['passed']for x in native['checks']+compat['checks']+preview['checks'])
url='http://127.0.0.1:65121/?razorwake=tempest-final-1105#razorwake'
s=(W/'REPORT.md').read_text(encoding='utf8')
for a,b in {'@NATIVE@':str(len(native['checks'])),'@FPS@':f"{j['nativeFps']:.2f}",'@SECONDS@':str(j['seconds']),'@PEAK@':str(j['peakDb']),'@PREVIEW@':str(len(preview['checks'])),'@URL@':url}.items():s=s.replace(a,b)
(W/'REPORT.md').write_text(s,encoding='utf8',newline='\n')
(R/'docs/RAZORWAKE_TEMPEST_1105.md').write_text(s,encoding='utf8',newline='\n')
Q=R/'docs/qa/razorwake_tempest_1105';Q.mkdir(parents=True,exist_ok=True)
for source,name in [(W/'probe/report.json','native-checks.json'),(W/'art-checks/report.json','art-checks.json'),(W/'compat-report.json','compatibility.json'),(V/'preview-checks.json','preview-checks.json'),(F/'batch.json','fight-batch.json'),(F/'stage6-mini/report.json','fight-native-report.json'),(D/'batch.json','vortex-batch.json'),(D/'stage6-mini/report.json','vortex-native-report.json'),(W/'full-suite.log','pre-existing-suite-failure.log'),(W/'composite-firing-performance.json','sustained-fire-performance.json'),(W/'pruned-firing-performance.json','prior-layered-drawing-performance.json')]:shutil.copy2(source,Q/name)
for p in (W/'probe').glob('*.png'):shutil.copy2(p,Q/p.name)
for p in (W/'film-inspection').glob('*contact.png'):shutil.copy2(p,Q/p.name)
for n in ['index.html','manifest.json','report.json','prepare.py','server.py','check_preview.py']:shutil.copy2(V/n,Q/('preview-'+n))
shutil.copytree(V/'posters',Q/'posters',dirs_exist_ok=True)
hashes={n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in ['assets/game.js','assets/razorwake_tempest_1105.js','assets/razorwake_tempest_art_1105.js']};(Q/'source-hashes.json').write_text(json.dumps(hashes,indent=2))
p=R/'assets/data/ART_TAXONOMY.json';raw=p.read_bytes();data=json.loads(raw);entry={'role':'furious_stage6_razorwake_rolling_gun_runs_committed_bursts_accelerating_throttle_storm_helix_and_native_vortex_crash','owner':'_BUILD_SOURCE/razorwake_tempest_1105/build_art.py','manifest':'assets/game/levels/stage_06/miniboss/razorwake_tempest_1105/manifest.json','note':'Built-in imagegen wind Helix loop referenced from actual Maverick ball, one tapered static exhaust source; originals/prompts retained. 1,601 fixed even-cell frames in 38 banks/88 compact pages, source-pixel teal charge/aura, precomposed pixel-identical hull/wing layers, independent rotary gun rolls, branching lightning, orb growth and nine-fragment rupture. Supersedes live RW117 attack book and selected presentation; existing native gun/core masks and gates retained. No PixelLab job claimed. Native shield/GOD/life handling and exclusive throw/fall/crash; 33 encounter and 6 compatibility checks; final live film 57.10 FPS. See docs/RAZORWAKE_TEMPEST_1105.md.'}
if 'rw118_'not in data:
 nl=b'\r\n'if b'\r\n'in raw else b'\n';pos=raw.rfind(nl+b'}');addition=json.dumps({'rw118_':entry},indent=2,ensure_ascii=False).encode('utf8')[2:-2];p.write_bytes(raw[:pos].rstrip()+b','+nl+addition+nl+b'}'+nl)
 assert json.loads(p.read_bytes())['rw118_']==entry
head=f"""## November 5, 2026 - Razorwake aggressive storm Helix (RW118)

Mike's revised Furious Stage6 miniboss is installed. New rolling forward gun runs,
three fixed south burst lanes, accelerating/reversed throttle passes, teal source-pixel
charge and a breakable growing wind Helix orb replace the old wind ribbons/tornado book.
Native fatal capture carries the burning wreck above view and crashes it at lower-middle;
the orb exits with the throw and the death banner waits for impact. Native protections,
module hit feedback, intact wings, core gate, damage and once-only defeat remain active.
1,785HP versus the actual Hard fortress's 1,552. Offline hull/wing composition removed
the drawing bottleneck without reducing art quality. Final native fight: {j['nativeFps']:.2f} FPS
through {j['seconds']} s, with no synthetic phases; sixty seconds hold-fire, input-only GOD bot.
33 encounter checks, 6 route checks, 1,601 Aseprite/frame checks, 24 masks and 14 preview checks pass.
Required test_fl.js still fails at the pre-existing difficultyHealthBaseline15 dependency.
Core game.js unchanged. No commit/push requested; preserve other pending changes.
Owner/source/evidence: docs/RAZORWAKE_TEMPEST_1105.md and _BUILD_SOURCE/razorwake_tempest_1105/.
Live review with full fight and separate natural fatal-orb clip: {url}

""".replace('Stage6','Stage 6').replace('1,552','1,552')
marker=b'Razorwake aggressive storm Helix (RW118)'
for n in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/n;raw=p.read_bytes()
 if marker not in raw[:4000]:
  nl='\r\n'if raw.count(b'\r\n')>raw.count(b'\n')/2 else'\n';p.write_bytes(head.replace('\n',nl).encode('utf8')+raw)
S=R/'_BUILD_SOURCE/razorwake_tempest_1105';S.mkdir(parents=True,exist_ok=True)
for p in W.glob('*.py'):shutil.copy2(p,S/p.name)
for n in ['SPEC.md','REPORT.md','PROMPTS.json']:shutil.copy2(W/n,S/n)
(Q/'delivery.json').write_text(json.dumps({'nativeChecks':len(native['checks']),'compatibilityChecks':len(compat['checks']),'artFrames':art['frames'],'masks':art['masks'],'previewChecks':len(preview['checks']),'nativeFps':j['nativeFps'],'vortexFps':dj['nativeFps'],'url':url,'runtimeSha256':hashes['assets/razorwake_tempest_1105.js'],'movie':j['path']},indent=2))
print('Saved final report, authored sources, taxonomy, handoff and QA receipts.')
