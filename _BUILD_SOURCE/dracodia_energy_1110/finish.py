from native import *
import hashlib,shutil,zipfile
reports={n:json.loads((O/(n+'.json')).read_text())for n in ['verification','compatibility','art-verification']}
assert all(all(r['checks'].values())for r in reports.values())
archive=R/'_BUILD_SOURCE/dracodia_energy_1110';a=json.loads((O/'art.json').read_text());m=json.loads((O/'manifest.json').read_text());m['verification']={n:len(r['checks'])for n,r in reports.items()};m['full_suite']={'exit':1,'blocker':'Existing ReferenceError: difficultyHealthBaseline15 is not defined at combat_polish_0927b.js:151 / test_fl.js:4537; suite does not reach final summary.'};m['generated_masters']={'phoenix-vortex':[1774,887],'brain-shield':[1774,887],'purple-lightning':list(Image.open(O/'purple-lightning-master.png').size)};m['banks']=len(a['banks']);(O/'manifest.json').write_text(json.dumps(m,indent=2))
count=sum(len(r['checks'])for r in reports.values());doc=f'''# Dracodia Phoenix and Neural Archon energy revision — November11,2026

Phoenix chest lasers now start from a fully filled circular aperture. The current whole-body pose owns that socket; original housing pixels cover the shaft at the rim. The background Order of the Phoenix sequence uses a new eight-pose flame vortex with rear/front layers, growing charge banks and an authored exit dissolve. Its native cannon gate, corner rushes, fire copies and return remain in charge.

Neural Archon uses source-fitted circular eye fills, two laser pulses on Normal and three on Hard/Furious, with short harmless gaps. Its default rotation is laser, laser, lightning, laser, laser, shield. It repositions between volleys and returns through the native main-form handoff after six completed attacks.

Lightning uses new large192x512 purple forked strikes based on the approved blue bolt. Normal has two waves of two strikes; Hard/Furious have three waves of three strikes. Ground warnings commit ahead of each wave. A clear column moves by one adjacent column per wave, bouncing at the edges; actual bright frame pixels own damage only during the strong strike interval. Native audio and pause/clear ownership are retained.

The shield uses new purple storm-cloud/electric artwork, with deploy, circulating loop and break banks. Existing absorption budgets and body hit flashes remain native.

## Sources and ownership

- Late owners: assets/dracodia_energy_art_1110.js and assets/dracodia_energy_1110.js, appended to index.html.
- Runtime pages: assets/game/levels/stage_08/effects/dracodia_energy_1110/.
- Source archive: _BUILD_SOURCE/dracodia_energy_1110/.
- Three generated masters, exact prompts, source hashes, metadata and reproducible offline assets.py are archived.
- Six tagged editable Aseprite documents contain {sum(map(len,a['banks'].values()))} fixed-cell timeline frames across {len(a['banks'])} banks and {len(a['pages'])} packed PNG pages. timeline.json maps each tag to its native bank and pivot.
- Runtime adds ordinary fixed image blits and frame selection. New effect sizing, palette, reveal and dissolve frames are authored offline. Original whole boss bodies remain native. Earlier form owners and game.js were not edited.

## Verification

{count} scoped checks pass across native gameplay, compatibility/audio and source export. Checks include actual eye and bolt damage, harmless eye gaps, a successful input-only three-wave dodge with GOD disabled and zero invulnerability, committed targets, adjacent safe lanes, native shield absorption, visible white hit flash/expiry, finite break, pause freeze, clear/audio cancellation, all three difficulty settings, reduced motion, full-book main-form return, and native copy defeat.

Eighteen representative Aseprite exports match integrated pixels exactly, including empty exit poses. New generated effect frames have binary alpha and all cells/packed rectangles are even. No page or console errors were observed.

Required node --check assets/game.js and both new scripts pass. Required node _BUILD_SOURCE/test_fl.js exits1 at the previously recorded missing difficultyHealthBaseline15 helper (combat_polish_0927b.js:151; test_fl.js:4537), before its final summary. The failure is outside these owners and was not changed here.

## Review media

dracodia-upgraded.mp4 contains native Phoenix core, full charged vortex/copy sequence, eye pulses, input-only lightning dodge and shield. Clips use native form checkpoints; the stationary presentation pilot is invulnerable except in purple-lightning.mp4, which records ordinary movement with no GOD or invulnerability. No attack clocks are changed during footage. GIF previews are included. Source only; no commit, push or installer.
''';(O/'README.md').write_text(doc,encoding='utf-8')
archive.mkdir(parents=True,exist_ok=True)
for n in ['assets.py','build.py','runtime.js','install.py','native.py','probe.py','compatibility.py','author.lua','roundtrip.lua','verify_art.py','package.py','finish.py']:shutil.copy2(W/n,archive/n)
for n in ['art.json','manifest.json','prompts.json','phoenix-vortex-master.png','brain-shield-master.png','purple-lightning-master.png','README.md','verification.json','compatibility.json','art-verification.json','native-capture.json']:shutil.copy2(O/n,archive/n)
shutil.copytree(O/'editable',archive/'editable',dirs_exist_ok=True);shutil.copy2(W/'full-suite.log',archive/'full-suite.log');shutil.copy2(O/'README.md',R/'docs/DRACODIA_ENERGY_1110.md')
note=f'''## November11,2026 — Dracodia circular optics and purple storm volleys

Mike requested full circular Phoenix/eye laser apertures, stronger Phoenix wind,
an aggressive laser brain, large purple lightning volleys and an animated shield.
D124 now owns those effects/attacks through two appended late scripts. Source-fit
housing collars cover beam corners; generated fire vortex and purple shield use
fixed authored banks. Brain uses2/3-pulse lasers and2/3 committed lightning waves
with adjacent moving safe lanes. Native HP, parts, shield budgets, flashes, pause,
clear, form return and copy defeat remain. {count} scoped checks pass, no browser
errors;18 editable-source roundtrips match. Full suite retains the old missing
difficultyHealthBaseline15 abort. Game.js and prior form owners are unchanged.
Sources/evidence: docs/DRACODIA_ENERGY_1110.md and _BUILD_SOURCE/dracodia_energy_1110/.
No commit, push or installer. Preserve the latest whole-hammer banks below.

'''
for name in ['HANDOFF_CODEX.md','CLAUDE.md']:
 pth=R/name;s=pth.read_text(encoding='utf-8')
 if not s.startswith('## November11,2026 — Dracodia circular optics'):pth.write_text(note+s,encoding='utf-8',newline='\n')
pth=R/'assets/data/ART_TAXONOMY.json';registry=json.loads(pth.read_text(encoding='utf-8'));entry={'role':'dracodia_source_fitted_circular_optics_phoenix_fire_vortex_purple_lightning_and_animated_neural_shield','owner':'_BUILD_SOURCE/dracodia_energy_1110/assets.py','manifest':'_BUILD_SOURCE/dracodia_energy_1110/manifest.json','note':'Three generated masters;371 banks /2984 fixed even timeline cells in six tagged Aseprite documents. Current source pose owns circular aperture and housing rim. Ordinary fixed blits only; native HP/parts/shield/hit feedback/form return retained. See docs/DRACODIA_ENERGY_1110.md.'};registry={'d124_':entry,**{k:v for k,v in registry.items()if k!='d124_'}};pth.write_text(json.dumps(registry,indent=2)+'\n',encoding='utf-8',newline='\n')
with zipfile.ZipFile(O/'dracodia-energy-source.zip','w',compression=zipfile.ZIP_DEFLATED)as z:
 for pth in archive.rglob('*'):
  if pth.is_file()and'__pycache__'not in pth.parts:z.write(pth,pth.relative_to(archive))
 for pth in(W/'candidate').glob('*.js'):z.write(pth,'runtime/'+pth.name)
 for pth in(W/'candidate/art').glob('*.png'):z.write(pth,'runtime/art/'+pth.name)
print(json.dumps({'scoped_checks':count,'frames':m['frames'],'banks':m['banks'],'pages':m['pages'],'source_archive':str(archive)}),flush=True)
