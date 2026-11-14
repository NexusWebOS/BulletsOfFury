from pathlib import Path
import json,hashlib,shutil,zipfile
W=Path(__file__).parent;R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/helicopter-death';A=R/'_BUILD_SOURCE/helicopter_death_1111';reports={n:json.loads((O/(n+'.json')).read_text())for n in ['verification','art-verification']};assert all(all(v['checks'].values())for v in reports.values());art=json.loads((O/'art.json').read_text());count=sum(len(v['checks'])for v in reports.values());before=json.loads((W/'before.json').read_text());assert all(hashlib.sha256((R/'assets'/n).read_bytes()).hexdigest()==h for n,h in before.items()if n!='index.html');assert(W/'runtime.js').read_bytes()==(R/'assets/helicopter_death_1111.js').read_bytes()
manifest={'version':'H126','date':'2026-11-11','frames':sum(map(len,art['banks'].values())),'banks':len(art['banks']),'pages':len(art['pages']),'source_hashes':art['sources'],'unchanged_owners':before,'checks':{n:len(v['checks'])for n,v in reports.items()},'timing':{'stage1':{'shatter':6.65,'dam_reveal':6.7,'raid_gate':8.6},'dracodia':{'shatter':3.85,'native_return':5.4}},'full_suite':{'exit':1,'blocker':'Existing ReferenceError: difficultyHealthBaseline15 is not defined at combat_polish_0927b.js:151 / test_fl.js:4537; final summary not reached.'}};(O/'manifest.json').write_text(json.dumps(manifest,indent=2))
doc=f'''# Helicopter accelerating death spirals — November11,2026

Mike requested that Dracodia's helicopter and the Stage1 helicopter on either difficulty spin uncontrollably, explode faster and faster, leave the screen, then shatter into visible debris with explosions trailing behind.

H126 replaces only those helicopter death visuals/directors. Native lethal damage and defeat owners still start each sequence. Whole airframes use64 offline yaw poses with baked rotor motion. The spin accelerates continuously, the wreck flies toward a lower side edge, and cook-off intervals fall from460ms toward55ms. Blasts stay at their emitted world positions to form a trail. Small actual-airframe pieces shed during the late spin. The final edge blast removes the hull and ejects real rotor/fuselage/pod pixel chunks, which tumble, travel offscreen and receive finite terminal explosions. No surviving hull fades or hangs in the air.

## Ownership and progression

- Stage1 applies to the actual damkeeper helicopter regardless of difficulty. Normal/Easy/Hard retain the actual critical metal body; Furious retains its existing green palette. Its original lethal-hit reward, Forge drop, enemy clear and post-helicopter raid remain native and occur once. Dam reveal remains at6.7s; the follow-up raid still opens at8.6s. The old stationary cook-off/fullscreen whiteout is replaced by the requested death spiral.
- Dracodia's form1 enters the native v19copyDeath state at real core exhaustion. Its visible spin/shatter lasts5.4s, then delegates to the original return/final-reform branch. Dead-copy HP remains0; main-life HP and remaining copies are never healed. Both non-final main-form return and last-copy terminal defeat were observed. Already destroyed pods remain absent through four authored hull variants.
- Dead wrecks expose no Retina targets or contact damage. Native weapon/lock cancellation remains in effect. Pause freezes motion, explosions and chunks together; native clear removes the copy's effect owner.
- Original game.js, Stage1 repair/raid owner, HC79 body/weapons, H125 weapon effects, D124 and native return code are byte-identical. No commit, push or installer.

## Authored source

Two appended owners: assets/helicopter_death_art_1111.js and assets/helicopter_death_1111.js. Packed images: assets/game/shared/combat/helicopter_death_1111/. Sources: _BUILD_SOURCE/helicopter_death_1111/.

1776 frames in176 banks and35 lossless PNG pages. Stage-scoped preload selects the appropriate hull family and shared explosions. Six spin families preserve the real hulls;166 actual-pixel fragments have eight authored tumble poses each. Four explosion sizes are exported directly from the approved H125 generated master. Source cells/pivots are fixed and even; all rendering uses ordinary integer source blits. Rotation, body/rotor combinations and chunk turns are baked offline, with no new runtime image rotation, scaling, tint, opacity animation, blend/filter or generated canvas effects. Reduced motion slows body/chunk rotation and skips the brightest explosion startup poses while preserving native timing/progression.

Eleven tagged Aseprite source documents and timeline.json preserve all banks. Thirty-three representative exports match integrated pixels exactly, including empty explosion ends. Actual Stage1 source textures/rotor frames were exported losslessly from XART; HC79 whole-body/pod sources and the original H125 explosion master remain archived with SHA256 provenance.

## Observed verification

{count} scoped checks pass across native gameplay and source/export geometry. Native Normal and Furious Stage1 clips show the full sequence. Easy/Hard ownership and pause checks also pass. Checks cover accelerating spin/cook-off, a moving explosion trail, visible real-airframe chunks, once-only shatter/completion/reward, native dam/raid follow-up, Dracodia's main-life return without HP restoration, destroyed-pod identity, safe dead wrecks, pause/clear, reduced motion, complete preload, unchanged owners, and native last-copy final reform/terminal death. Completed browser captures have no page/console/draw errors. A socket reset printed only when one recorder closed its browser during HTTP teardown; the native checks and saved footage completed.

Required game.js and both new-script syntax checks pass. Required node _BUILD_SOURCE/test_fl.js still exits1 at the previously recorded missing difficultyHealthBaseline15 helper (combat_polish_0927b.js:151 / test_fl.js:4537), before its final summary. That unrelated failure remains unchanged.

## Finished media

helicopter-death-spirals.mp4 shows Stage1 Normal, Stage1 Furious, then Dracodia. Separate MP4/GIF clips are included. These are real-renderer encounter checkpoints with native lethal damage, an invulnerable presentation pilot and untouched death clocks during each chapter; they are not whole-campaign completion footage.
''';(O/'README.md').write_text(doc,encoding='utf-8')
for n in ['assets.py','runtime.js','install.py','export.py','reference.json','before.json','verify.py','final_check.py','verify_art.py','editor_plan.py','author.lua','roundtrip.lua','package.py','finish.py']:shutil.copy2(W/n,A/n)
for n in ['art.json','manifest.json','verification.json','art-verification.json','README.md','editor-plan.json','explosion-master.png']:shutil.copy2(O/n,A/n)
shutil.copy2(R/'_BUILD_SOURCE/helicopter_effects_1111/prompts.json',A/'explosion-provenance-prompts.json');shutil.copytree(O/'editable',A/'editable',dirs_exist_ok=True);shutil.copytree(W/'roundtrip',A/'roundtrip',dirs_exist_ok=True);shutil.copy2(W/'full-suite.log',A/'full-suite.log');shutil.copy2(O/'README.md',R/'docs/HELICOPTER_DEATH_SPIRALS_1111.md')
note=f'''## November11,2026 — Helicopter runaway death spirals

H126 gives every Stage1 helicopter difficulty and Dracodia form1 accelerating
authored yaw, moving cook-off trails, an edge blast and real-airframe shatter.
Six actual hull variants /1776 frames /35 stage-scoped pages; eleven editable
Aseprite documents. Native rewards/Forge drops/HP pools/remaining copies persist.
Stage1 dam6.7s and raid8.6s remain; copy death delegates home/final reform at5.4s.
{count} scoped checks pass, including last-copy terminal defeat;33 source exports
match. Full suite retains the existing missing difficultyHealthBaseline15 abort.
Prior owners and game.js unchanged. Docs: docs/HELICOPTER_DEATH_SPIRALS_1111.md;
sources/evidence: _BUILD_SOURCE/helicopter_death_1111/. No push or installer.

'''
for n in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/n;s=p.read_text(encoding='utf-8')
 if not s.startswith('## November11,2026 — Helicopter runaway'):p.write_text(note+s,encoding='utf-8',newline='\n')
p=R/'assets/data/ART_TAXONOMY.json';registry=json.loads(p.read_text(encoding='utf-8'));entry={'role':'actual_stage1_and_dracodia_helicopter_accelerating_death_yaw_real_pixel_shatter_and_explosion_trails','owner':'_BUILD_SOURCE/helicopter_death_1111/assets.py','manifest':'_BUILD_SOURCE/helicopter_death_1111/manifest.json','note':'Six64-yaw hull banks;166 real-airframe fragments with eight tumble poses; direct-master authored explosions. 1776 frames,35 stage-scoped pages,11 tagged Aseprite sources. Native once-only defeat/HP/reward/dam/raid/copy return/final reform retained. See docs/HELICOPTER_DEATH_SPIRALS_1111.md.'};registry={'h126_':entry,**{k:v for k,v in registry.items()if k!='h126_'}};p.write_text(json.dumps(registry,indent=2)+'\n',encoding='utf-8',newline='\n')
with zipfile.ZipFile(O/'helicopter-death-sources.zip','w',compression=zipfile.ZIP_DEFLATED)as z:
 for p in A.rglob('*'):
  if p.is_file()and'__pycache__'not in p.parts:z.write(p,p.relative_to(A))
 for p in(W/'candidate').glob('*.js'):z.write(p,'runtime/'+p.name)
 for p in(W/'candidate/art').glob('*.png'):z.write(p,'runtime/art/'+p.name)
print(json.dumps({'checks':count,'native_checks':len(reports['verification']['checks']),'frames':manifest['frames'],'source_archive':str(A)}),flush=True)
