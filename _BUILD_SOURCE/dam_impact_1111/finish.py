from pathlib import Path
import json,hashlib,shutil,zipfile
W=Path(__file__).parent;R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/dam-impact';A=R/'_BUILD_SOURCE/dam_impact_1111';reports={n:json.loads((O/(n+'.json')).read_text())for n in ['verification','art-verification']};assert all(all(q['checks'].values())for q in reports.values());before=json.loads((W/'before.json').read_text());assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in before.items()if n not in ['index.html','assets/helicopter_death_1111.js']);assert(W/'runtime.js').read_bytes()==(R/'assets/dam_impact_1111.js').read_bytes();count=sum(len(q['checks'])for q in reports.values());manifest={'version':'H127','date':'2026-11-11','checks':{n:len(q['checks'])for n,q in reports.items()},'changed':['index.html','assets/helicopter_death_1111.js','assets/dam_impact_art_1111.js','assets/dam_impact_1111.js'],'before_hashes':before,'flash':{'frames':33,'pages':9,'logical':[480,512],'standard_rise':.16,'hold':.18,'fade':1.18},'dam':{'source':[340,286],'target_source_top':128,'camera_run_in':3.6,'crash':6.65,'swap':6.83,'raid':8.6},'full_suite':{'exit':1,'blocker':'Existing difficultyHealthBaseline15 ReferenceError in combat_polish_0927b.js:151 / test_fl.js:4537; final summary not reached.'}};(O/'manifest.json').write_text(json.dumps(manifest,indent=2))
doc=f'''# Stage1 helicopter dam impact and white-fade reveal — November11,2026

Mike corrected the Stage1 helicopter death: it must spin into the dam and explode, then use a white screen flash that fades back to the destroyed dam. H127 supersedes H126's Stage1 offscreen exit. Dracodia's copied-helicopter death remains under its previous director.

## Finished sequence

The existing accelerating spin/cook-off begins at the actual death position. A forward-only3.6s terrain approach brings the actual CoastlineDam plate into view. The helicopter reels toward a lower staging point, then flies into the central gate at source coordinate(340,286), measured from the approved680x4212 intact/destroyed plates. The camera settles before impact; current source-window geometry owns the aircraft's final world position. It never snaps or scrolls backwards, including when the dam is already in view.

The native shatter blast begins at6.65s. An authored full-screen white pulse rises over160ms, holds180ms, then fades back over1.18s. The damaged plate swaps at6.83s while every screen pixel is white. Camera framing remains fixed during the swap/reveal, so the broken gate replaces the intact gate at the same position. The normal background, player and debris emerge as white recedes. The existing post-helicopter raid still opens at8.6s. Native reward, Forge/Continue drops and raid ownership remain unchanged.

Reduced motion uses a slower420ms white buildup,160ms hold and1s reveal; its plate swap also happens at full white. Pause freezes the aircraft, map travel and white frame together. Retry clears the owner and flash. No fullscreen white remains after the transition.

## Source and integration

New late owners: assets/dam_impact_art_1111.js and assets/dam_impact_1111.js. Nine small pages under assets/game/shared/combat/dam_impact_1111/ contain33 fixed480x512 authored white/alpha levels, drawn with ordinary image blits. No runtime opacity, filter, additive blend or procedural full-screen effect was added. The editable white-flash.aseprite intensity bank retains all levels; five exported source states match exactly. Native motion selects those states for rise/hold/fall.

H126 received only a position-selection helper and optional dam-swap time. Its default path math is unchanged. H127 supplies the Stage1 path/camera/swap/flash behavior; all other forms delegate unchanged. game.js, HC79, H125, D124 and the native Stage1 repair/raid owner are byte-identical. Source archive: _BUILD_SOURCE/dam_impact_1111/. Source/raw dam measurements, guarded installer, pre-change backups, edited H126 candidate, exact flash frames, Aseprite source and QA are retained.

## Observed verification

{count} scoped checks pass. Native Normal/Furious recordings confirm the aircraft hits the actual gate, scroll moves forward and holds for impact, the full framebuffer becomes RGB255 white, the map switches only at full white, fade/reveal completes, the destroyed dam appears and the native raid/reward continue. Easy/Hard, early/late map positions, reduced motion, pause and retry checks also pass. Dracodia's default trajectory matches its prior equation exactly. All flash pages and both terrain states preload before use. No browser/console/draw errors occurred.

Required syntax checks pass. The full suite still exits1 at the recorded missing difficultyHealthBaseline15 helper (combat_polish_0927b.js:151 / test_fl.js:4537), before its final summary. That unrelated failure remains unchanged.

## Review media

dam-crash-transition.mp4 shows Normal then Furious. dam-crash.gif shows the Furious sequence. Real-renderer checkpoints start near the boss encounter, with a stationary invulnerable presentation pilot and real native lethal damage. Death clocks are not edited during the recorded sequence. No commit, push or installer.
''';(O/'README.md').write_text(doc,encoding='utf-8')
for n in ['build.py','runtime.js','install.py','verify.py','verify_art.py','author.lua','package.py','finish.py','inspect_dam.py','before.json','source-measurements.json']:shutil.copy2(W/n,A/n)
for n in ['art.json','manifest.json','verification.json','art-verification.json','README.md']:shutil.copy2(O/n,A/n)
shutil.copytree(O/'editable',A/'editable',dirs_exist_ok=True);shutil.copytree(W/'roundtrip',A/'roundtrip',dirs_exist_ok=True);shutil.copy2(W/'full-suite.log',A/'full-suite.log');shutil.copy2(W/'dam-reference.png',A/'dam-reference.png');shutil.copy2(W/'candidate/helicopter_death_1111.js',A/'helicopter_death_1111.updated.js');shutil.copy2(O/'README.md',R/'docs/DAM_IMPACT_TRANSITION_1111.md')
note=f'''## November11,2026 — Helicopter crashes into the dam under a white fade

Mike corrected Stage1's death exit: the spinning helicopter now hits the actual
central dam gate. H127 brings the dam into view smoothly, holds its framing and
swaps to the destroyed plate at full authored white, then fades back to normal.
Both palettes/difficulties use the route. Native8.6s raid/rewards remain. H126's
default copied-helicopter path is unchanged; only its optional route/swap hooks
were added. {count} scoped checks pass; five Aseprite white states match exactly.
Full suite retains the existing missing difficultyHealthBaseline15 failure.
Docs/sources: docs/DAM_IMPACT_TRANSITION_1111.md;_BUILD_SOURCE/dam_impact_1111/.
This supersedes only H126's Stage1 edge-exit description. No push or installer.

'''
for n in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/n;s=p.read_text(encoding='utf-8')
 if not s.startswith('## November11,2026 — Helicopter crashes into'):p.write_text(note+s,encoding='utf-8',newline='\n')
p=R/'assets/data/ART_TAXONOMY.json';registry=json.loads(p.read_text(encoding='utf-8'));registry={'h127_':{'role':'stage1_dam_impact_authored_white_flash_and_destroyed_plate_reveal','owner':'_BUILD_SOURCE/dam_impact_1111/build.py','manifest':'_BUILD_SOURCE/dam_impact_1111/manifest.json','note':'33 fixed480x512 white/alpha frames in nine pages. Actual gate source(340,286), forward-only approach, plate swap at full white, native8.6s raid retained. Supersedes Stage1 edge exit only; copied-helicopter path unchanged. See docs/DAM_IMPACT_TRANSITION_1111.md.'},**{k:v for k,v in registry.items()if k!='h127_'}};p.write_text(json.dumps(registry,indent=2)+'\n',encoding='utf-8',newline='\n')
with zipfile.ZipFile(O/'dam-impact-sources.zip','w',compression=zipfile.ZIP_DEFLATED)as z:
 for p in A.rglob('*'):
  if p.is_file()and'__pycache__'not in p.parts:z.write(p,p.relative_to(A))
 for p in(W/'candidate').glob('*.js'):z.write(p,'runtime/'+p.name)
 for p in(W/'candidate/art').glob('*.png'):z.write(p,'runtime/art/'+p.name)
print(json.dumps({'checks':count,'native_checks':len(reports['verification']['checks']),'source_archive':str(A)}),flush=True)
