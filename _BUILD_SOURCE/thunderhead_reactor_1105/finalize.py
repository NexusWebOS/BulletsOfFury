from pathlib import Path
import json,shutil,hashlib
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');V=W.parent/'BOF-Furious-Boss-Videos-1104'
F=R/'_shots/boss_comparison_1102/thunderhead-reactor-final-1105'
j=json.loads((F/'batch.json').read_text())['jobs']['stage6-boss'];probe=json.loads((W/'probe/report.json').read_text());art=json.loads((W/'art-checks/report.json').read_text());pv=json.loads((V/'preview-checks.json').read_text());compat=json.loads((W.parent/'BOF-Razorwake-Tempest-1105/compat-report.json').read_text())
assert j['passed']and art['passed']and all(c['passed']for c in probe['checks']+pv['checks']+compat['checks'])
url='http://127.0.0.1:65122/?thunderhead=reactor-final-1105#thunderhead'
s=(W/'REPORT.md').read_text(encoding='utf8')
for a,b in {'@CHECKS@':str(len(probe['checks'])),'@FPS@':f"{j['nativeFps']:.2f}",'@SECONDS@':str(j['seconds']),'@PEAK@':str(j['peakDb']),'@PREVIEW@':str(len(pv['checks'])),'@URL@':url}.items():s=s.replace(a,b)
(W/'REPORT.md').write_text(s,encoding='utf8',newline='\n');(R/'docs/THUNDERHEAD_REACTOR_1105.md').write_text(s,encoding='utf8',newline='\n')
S=R/'_BUILD_SOURCE/thunderhead_reactor_1105';S.mkdir(parents=True,exist_ok=True);A=W/'authored';M=json.loads((A/'manifest.json').read_text())
for p in W.glob('*.py'):shutil.copy2(p,S/p.name)
for n in ['SPEC.md','REPORT.md']:shutil.copy2(W/n,S/n)
for n in ['manifest.json','author.lua']:shutil.copy2(A/n,S/n)
(S/'strips').mkdir(exist_ok=True)
for n in M['banks']:
 shutil.copy2(A/(n+'.aseprite'),S/(n+'.aseprite'));shutil.copy2(A/'strips'/(n+'.png'),S/'strips'/(n+'.png'))
Q=R/'docs/qa/thunderhead_reactor_1105';Q.mkdir(parents=True,exist_ok=True)
for src,name in [(W/'probe/report.json','native-checks.json'),(W/'art-checks/report.json','art-checks.json'),(W/'performance.json','performance.json'),(W/'full-suite.log','existing-suite-failure.log'),(V/'preview-checks.json','preview-checks.json'),(W.parent/'BOF-Razorwake-Tempest-1105/compat-report.json','compatibility.json'),(F/'batch.json','batch.json'),(F/'stage6-boss/report.json','recording-report.json')]:shutil.copy2(src,Q/name)
for p in (W/'probe').glob('*.png'):shutil.copy2(p,Q/p.name)
for p in (W/'film-inspection').glob('*contact*.png'):shutil.copy2(p,Q/p.name)
for n in ['core-flow-contact.png','hull-only.png','source-contact.png']:shutil.copy2(W/n,Q/n)
for n in ['index.html','manifest.json','report.json','prepare.py','server.py','check_preview.py']:shutil.copy2(V/n,Q/('preview-'+n))
shutil.copytree(V/'posters',Q/'posters',dirs_exist_ok=True)
hashes={n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in ['assets/game.js','assets/thunderhead_reactor_1105.js','assets/thunderhead_reactor_art_1105.js']};(Q/'source-hashes.json').write_text(json.dumps(hashes,indent=2))
film=json.loads((F/'stage6-boss/report.json').read_text());assert film['sourceHashes']['assets/thunderhead_reactor_1105.js']==hashes['assets/thunderhead_reactor_1105.js']
entry={'role':'furious_stage6_thunderhead_socketed_wind_beams_coordinated_batteries_rising_reactor_and_background_perspective_cyclone',
 'owner':'_BUILD_SOURCE/thunderhead_reactor_1105/build_art.py','manifest':'assets/game/levels/stage_06/boss/thunderhead_reactor_1105/manifest.json',
 'note':'Re-authored approved TM115/THS114/RW118 source pixels, no generation charge. 3127 fixed even-cell frames in 158 banks, 16 ship depth sizes, 32 directional gun poses/recoil/emission, animated beam coupling and metal lip, chamber swirl moving north, actual native warning, 16 perspective cyclone sizes, coloured module breakaway and finite shards. Destroyed modules expose original empty hull wells; no extra receiver or full wreck silhouette. Native 6348 HP, six-part gate, hit feedback and rewards preserved. Sources/Aseprite/QA retained; see docs/THUNDERHEAD_REACTOR_1105.md.'}
p=R/'assets/data/ART_TAXONOMY.json';raw=p.read_bytes();data=json.loads(raw)
if 'tc119_'not in data:
 nl=b'\r\n'if b'\r\n'in raw else b'\n';pos=raw.rfind(nl+b'}');addition=json.dumps({'tc119_':entry},indent=2,ensure_ascii=False).encode('utf8')[2:-2];p.write_bytes(raw[:pos].rstrip()+b','+nl+addition+nl+b'}'+nl);assert json.loads(p.read_bytes())['tc119_']==entry
header=f"""## November 5, 2026 - Thunderhead reactor and background cyclone (TC119)

Mike's Thunderhead pass is installed: animated cannon/beam coupling and metal lip;
four independent guns reserve three real allies and one player target in 75% of cycles;
rotating gun/recoil/muzzle poses, upward swirling reactor glass, fading storm shade,
native warning and loud matching lightning. The giant cyclone now uses a turn north,
distant south entry, 4.4s charge, recoil launch, distant recovery and foreground return.
Sixteen authored depth sizes keep all mounts and exhaust together. Modules leave their
original empty hull wells, explode under native unitDeathFX rules and shatter after
physical breakaway. No extra receiver/full dark weapon-shaped wreck is drawn.
Native 6,348 HP and all six gates retained. {len(probe['checks'])} native, 6 compatibility,
3,127 art-frame/64 mask and 14 preview checks pass. Full native film: {j['nativeFps']:.2f} FPS
over {j['seconds']}s, Cole GOD/input bot, 70s player hold-fire, live native allies/audio.
Existing test_fl.js dependency failure remains documented; game.js unchanged.
Owner: assets/thunderhead_reactor_1105.js; sources: _BUILD_SOURCE/thunderhead_reactor_1105/.
Evidence/limits: docs/THUNDERHEAD_REACTOR_1105.md. No commit/push requested.
Review: {url}

"""
for n in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/n;raw=p.read_bytes()
 if b'Thunderhead reactor and background cyclone (TC119)'not in raw[:5000]:
  nl='\r\n'if raw.count(b'\r\n')>raw.count(b'\n')/2 else'\n';p.write_bytes(header.replace('\n',nl).encode('utf8')+raw)
(Q/'delivery.json').write_text(json.dumps({'checks':len(probe['checks']),'compatibility':6,'frames':art['frames'],'masks':art['masks'],'preview':len(pv['checks']),'fps':j['nativeFps'],'seconds':j['seconds'],'url':url,'runtimeSha256':hashes['assets/thunderhead_reactor_1105.js'],'movie':j['path']},indent=2))
print('Saved Thunderhead sources, report, taxonomy, handoff and native-film receipts.')
