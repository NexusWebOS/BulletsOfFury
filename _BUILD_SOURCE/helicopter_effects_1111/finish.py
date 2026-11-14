from pathlib import Path
from PIL import Image
import json,shutil,hashlib,zipfile
W=Path(__file__).parent;R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/dracodia-helicopter';A=R/'_BUILD_SOURCE/helicopter_effects_1111';reports={n:json.loads((O/(n+'.json')).read_text())for n in ['verification','art-verification']};assert all(all(q['checks'].values())for q in reports.values());art=json.loads((O/'art.json').read_text());before=json.loads((W/'before.json').read_text());assert all(hashlib.sha256((R/'assets'/n).read_bytes()).hexdigest()==h for n,h in before.items()if n!='index.html')
for src,target in [('runtime.js','helicopter_effects_1111.js'),('candidate/helicopter_effects_art_1111.js','helicopter_effects_art_1111.js')]:assert(W/src).read_bytes()==(R/'assets'/target).read_bytes(),'Live candidate mismatch'
count=sum(len(q['checks'])for q in reports.values());manifest={'version':'H125','date':'2026-11-11','banks':len(art['banks']),'frames':sum(map(len,art['banks'].values())),'pages':len(art['pages']),'checks':{n:len(q['checks'])for n,q in reports.items()},'unchanged_sources':before,'new_sources':art['sources'],'runtime':['assets/helicopter_effects_art_1111.js','assets/helicopter_effects_1111.js'],'full_suite':{'exit':1,'blocker':'Existing ReferenceError: difficultyHealthBaseline15 is not defined at assets/combat_polish_0927b.js:151; test_fl.js:4537. Final summary not reached.'}};(O/'manifest.json').write_text(json.dumps(manifest,indent=2))
doc=f'''# Dracodia helicopter weapon effects — November11,2026

Mike requested the helicopter equivalent of the Phoenix/Neural Archon effect upgrade: better animated gunfire, missiles and explosions.

The copied helicopter now uses new eight-pose gold muzzle flashes and animated pointed tracers. Actual current pod recoil/aim sockets own each flash. New red/chromium missiles retain a stable metallic body with eight exhaust/smoke phases and64 authored headings. Larger launch bursts reuse the same hot flame sequence. New16-pose fuel explosions replace the copied helicopter's missile impact/interception effect and its old purple pod-break bursts. A broken pod gets one160px blast plus two delayed112px secondary blasts; missile impacts use72px blasts. Smoke, metal fragments, hot lobes and empty end frames are authored into the source.

## Preserved behavior

HC79 still owns all movement, rotor poses, weapon pods, recoil, aiming, committed gun corridors, native player locks, difficulty counts, physical homing, interception, damage, HP and parts. Gunfire stays non-interceptible. The2/3/4 missiles per living pod remain shootable. Destroying a pod cancels its queued callbacks and removes its target; the other pod keeps fighting. Native sonic fronts, warned charge, hit flash, copy return and death owners remain. No body redesign or extra HP was added. D124's Phoenix/brain effects and game.js are unchanged.

## Authored source and runtime

- Owners: assets/helicopter_effects_art_1111.js and assets/helicopter_effects_1111.js, appended after D124.
- Pages: assets/game/levels/stage_08/effects/helicopter_1111/.
- Source archive: _BUILD_SOURCE/helicopter_effects_1111/.
- Four raw generated masters, exact prompts, actual helicopter reference and source hashes are retained. Sprite-sheet adaptation uses fixed source cells and proportional exports. The missile's lower metallic body is held from one approved source pose so only its exhaust changes.
- Seven tagged Aseprite timelines hold2096 frames, including64 offline directions for muzzle, launch, tracer and missile banks. timeline.json maps editor frames to runtime frame indices. Twenty-one representative Aseprite exports match integrated pixels exactly, including empty timed frames.
- Five lossless packed PNG pages. Even logical cells and packed rectangles; shared bank pivots; binary alpha. Runtime uses ordinary fixed source blits and frame selection. No runtime rotation, scaling, additive blending, filters or animated alpha are added.
- New decorative explosions do not add damage. Effects cap at24, expire after800ms plus any authored delay, freeze with game time and clear with the native owner. Legacy trail emission is suppressed only at a tracked helicopter missile's exact native exhaust point; other trails remain native.

## Observed verification

{count} scoped checks pass across native gameplay and source export. Native evidence covers both pod emitters at their current recoil sockets, ordinary player gunfire intercepting actual homing missiles, exactly one burst per intercepted missile, difficulty counts, independent native locks, an input-only non-GOD gun-corridor dodge, pod callback cancellation, visible hit flash and expiry, finite explosions, pause, clear, reduced flashing, sonic/charge compatibility, decoded gun/rocket/blast cues, complete preload, bounded effect lists, and unchanged earlier owners. No page or console errors in completed captures.

The reduced-flashing check initially stopped at95 ticks, before the last queued missile pair. Its corrected130-tick check observes all8 launches; no runtime change was required. An initial capture failed under system memory pressure. The successful capture uses a16-worker HTTP server to limit asset-loader memory; this is capture infrastructure only.

Required game.js and new-script syntax checks pass. The required full test suite still exits1 at the recorded missing difficultyHealthBaseline15 helper (combat_polish_0927b.js:151 / test_fl.js:4537), before its final summary. That existing failure was not changed.

## Finished review

helicopter-upgraded.mp4 shows native gunfire, missile volleys, actual player-fired interceptions, and native pod destruction. Chapters start at selected form/attack checkpoints. The presentation pilot is invulnerable; intercepted missiles use ordinary fire inputs, and the pod-destruction chapter begins through native modularHit. Separate safe-corridor verification uses normal movement, no GOD and zero invulnerability. No HP/phase/clock edits occur during each recorded chapter. Source only; no commit, push or installer.
''';(O/'README.md').write_text(doc,encoding='utf-8')
A.mkdir(parents=True,exist_ok=True)
for n in ['assets.py','runtime.js','install.py','native.py','reduced_check.py','author.lua','roundtrip.lua','verify_art.py','package.py','finish.py','reference.py','before.json']:shutil.copy2(W/n,A/n)
for n in ['art.json','manifest.json','prompts.json','muzzle-master.png','missile-master.png','tracer-master.png','explosion-master.png','verification.json','art-verification.json','README.md']:shutil.copy2(O/n,A/n)
shutil.copy2(W/'helicopter-reference.png',A/'helicopter-reference.png');shutil.copytree(O/'editable',A/'editable',dirs_exist_ok=True);shutil.copy2(W/'full-suite.log',A/'full-suite.log');shutil.copy2(O/'README.md',R/'docs/DRACODIA_HELICOPTER_EFFECTS_1111.md')
note=f'''## November11,2026 — Animated helicopter gunfire, missiles and blasts

H125 upgrades Dracodia's copied helicopter with four new generated effect masters:
gold muzzle/tracer pulses, red/chromium missiles with animated engine/smoke, and
fuel/metal explosions for native missile interceptions and staggered pod breaks.
2096 frames across seven tagged Aseprite banks /five PNG pages;64 authored headings.
HC79 body, rotor, pod HP, recoil sockets, aiming, warning/counter lanes, native
locks/shootable missiles, sonic/charge/return/death owners remain. D124 unchanged.
{count} scoped checks pass;21 source exports are pixel-exact. Successful native
capture has no browser errors. Full suite retains missing difficultyHealthBaseline15.
Sources/evidence: docs/DRACODIA_HELICOPTER_EFFECTS_1111.md and
_BUILD_SOURCE/helicopter_effects_1111/. No commit, push or installer.

'''
for n in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/n;s=p.read_text(encoding='utf-8')
 if not s.startswith('## November11,2026 — Animated helicopter'):p.write_text(note+s,encoding='utf-8',newline='\n')
p=R/'assets/data/ART_TAXONOMY.json';registry=json.loads(p.read_text(encoding='utf-8'));entry={'role':'dracodia_helicopter_gold_gunfire_red_chromium_missiles_engine_smoke_and_fuel_explosions','owner':'_BUILD_SOURCE/helicopter_effects_1111/assets.py','manifest':'_BUILD_SOURCE/helicopter_effects_1111/manifest.json','note':'Four generated masters;2096 fixed even frames,64 authored headings,seven tagged Aseprite timelines and five packed PNG pages. Current HC79 recoil socket owns muzzle; native physical missiles/interception/HP/locks/return retained. Native missile impacts and pod bursts use finite authored explosions. See docs/DRACODIA_HELICOPTER_EFFECTS_1111.md.'};registry={'h125_':entry,**{k:v for k,v in registry.items()if k!='h125_'}};p.write_text(json.dumps(registry,indent=2)+'\n',encoding='utf-8',newline='\n')
with zipfile.ZipFile(O/'helicopter-effect-sources.zip','w',compression=zipfile.ZIP_DEFLATED)as z:
 for p in A.rglob('*'):
  if p.is_file()and'__pycache__'not in p.parts:z.write(p,p.relative_to(A))
 for p in(W/'candidate').glob('*.js'):z.write(p,'runtime/'+p.name)
 for p in(W/'candidate/art').glob('*.png'):z.write(p,'runtime/art/'+p.name)
print(json.dumps({'checks':count,'frames':manifest['frames'],'pages':manifest['pages'],'source_archive':str(A)}),flush=True)
