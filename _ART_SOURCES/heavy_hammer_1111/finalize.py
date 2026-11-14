from pathlib import Path
import json,hashlib,shutil,zipfile
from PIL import Image
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Heavy-hammer-motion'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
install=json.loads((W/'installation.json').read_text())
assert all(sha(R/n)==h for n,h in install['after'].items()),'An installed owner changed after verification.'
checks=[];roundtrips=[]
for stage in [5,8]:
 q=json.loads((O/f'verification-stage{stage}/checks.json').read_text());assert not q['errors']and all(c['passed']for c in q['checks']);checks+=q['checks']
for j in json.loads((W/'aseprite-audit.json').read_text()):
 a=Image.open(W/'exports'/(j['bank']+'_regular.png')).convert('RGBA');b=Image.open(W/'exports'/(j['bank']+'_roundtrip.png')).convert('RGBA');assert a.tobytes()==b.tobytes();roundtrips.append(dict(**j,pixelExact=True))
full=json.loads((W/'full-suite.json').read_text());summary=dict(nativeChecks=len(checks),failed=[],browserErrors=[],sourceRoundtrips=roundtrips,sourceFrames=160,originalDrawings=124,overheadTimelineFramesPerForm=32,overheadUniqueDrawingsPerForm=31,sideUniqueDrawingsPerForm=15,whirlUniqueDrawingsPerForm=16,wholePoseRightMirrors=True,coreGameUnchanged=True,fullSuiteExit=full['exit'],fullSuiteError='Existing difficultyHealthBaseline15 is not defined'if'difficultyHealthBaseline15'in(W/'full-suite.txt').read_text()else full['lastError'])
(W/'summary.json').write_text(json.dumps(summary,indent=2));(O/'verification.json').write_text(json.dumps(summary,indent=2))
archive=R/'_ART_SOURCES/heavy_hammer_1111';archive.mkdir(exist_ok=True,parents=True)
for folder in ['jobs','references']:
 shutil.copytree(W/folder,archive/folder,dirs_exist_ok=True)
(archive/'generated').mkdir(exist_ok=True)
for p in(W/'jobs').glob('*.json'):
 j=json.loads(p.read_text());src=W/'generated'/(j['name']+'.png')
 if j.get('accepted')and src.exists():shutil.copy2(src,archive/'generated'/src.name)
for p in W.iterdir():
 if p.is_file()and p.suffix in['.py','.lua','.json','.js','.md','.txt']:shutil.copy2(p,archive/p.name)
(archive/'exports').mkdir(exist_ok=True)
for p in(W/'exports').iterdir():
 if p.suffix in['.aseprite','.png','.webp']and'_roundtrip'not in p.name:shutil.copy2(p,archive/'exports'/p.name)
qa=R/'docs/qa/heavy_hammer_1111';qa.mkdir(exist_ok=True,parents=True)
for n in ['summary.json','audit.json','installation.json','aseprite-audit.json','full-suite.txt']:shutil.copy2(W/n,qa/n)
for stage in [5,8]:
 for n in ['checks.json','trace.json']:shutil.copy2(O/f'verification-stage{stage}'/n,qa/f'stage{stage}-{n}')
for unit in ['chronos','dracodia']:
 for suffix in ['-whole-contract.json','-recording.json']:shutil.copy2(W.parent/(unit+suffix),qa/(unit+suffix))
fixtures=R/'_BUILD_SOURCE/heavy_hammer_1111';fixtures.mkdir(exist_ok=True,parents=True)
for n in ['verify_heavy_stage5.py','verify_heavy_stage8.py','heavy_record_loaded.py']:shutil.copy2(W.parent/n,fixtures/n)
report=f'''# Reference-led heavy hammer motion — November 11, 2026

Chronos and Dracodia's copied Chronos form now use the same heavy overhead mechanics studied from Mike's hammer.gif and PyCciI.gif: two hands on the hilt, low regrip, lift, behind-head load, hip/shoulder drive, forward body bend, lower end-cap contact, planted impact hold and rebound. Existing Normal/Hard/Furious one/two/four-contact patterns remain; the later contacts stay planted.

Each form has a 32-frame overhead cycle containing 31 distinct whole drawings and one deliberate contact hold; 15 distinct whole side-swing drawings plus a contact hold and complete-pose right mirrors; and 16 newly drawn fullbody views for the native whirlwind. The whirlwind winds in from the carry, turns through real side/back views, and settles toward the ready pose. Side contacts retain a visible perpendicular T joint and lead with the outside cap. Total: 124 original complete drawings, 160 timeline cells across eight banks. The rejected sliding contact and clipped/malformed candidates are excluded. This supersedes the earlier four-pose side banks and sparse held attacks.

These are complete authored actor-and-held-weapon drawings, generated with the built-in image tool. PixelLab was not charged. Actual user motion guides and canonical character/head/weapon images supplied distinct roles in every prompt. Exact prompts, selected source-cell lists and rejected-candidate reasons are in jobs/. Uniform source-sheet model-unit calibration and whole-pose boot registration import directly from the original masters. Native cells are 512x512 with pivot [256,256] and boot baseline410; this removes unused transparent padding from the prior640 cells while preserving world-space offsets and body detail. No body/weapon assembly, head stamps, runtime image rotation or pixel interpolation.

Current registrations: assets/overhead_slam_art_1111.js supplies the new eight heavy_hammer_1111 banks. assets/boss_animation_1109.js samples actual fractional frame indexes for the longer banks and allows room for the complete planted combo. The late HA1111 block in assets/whole_hammer_1110.js selects existing native whirlwind/recovery states and matches the authored hammer position. Its recovery is scoped to one transition. Existing detached hammer flight, native HP/audio/damage/death/progression owners remain. assets/game.js is unchanged.

Verification: {len(checks)} focused native checks pass with no browser errors; both held/released/catch contracts pass; all160 editable-source frames export pixel-exactly. Real native screenshots, film contact sheets and recordings accompany source GIFs and a self-contained frame playback page. Planted silhouettes stay within the playfield on every sampled difficulty/material. Regular and chrome live recordings retain decoded native audio. These are scoped attack reviews with an invulnerable observer, not a full-campaign completion claim. The broad suite still exits1 before its final summary on the existing missing difficultyHealthBaseline15 helper; full log included.

Open playback.html to pause, slow and step both forms together. both-overhead.gif, both-sides.gif and both-whirl.gif are paired source previews. chronos-hammer.mp4 and dracodia-hammer.mp4 show the running engine. Sources: eight tagged single-layer Aseprite documents, lossless PNG/WebP exports, manifests, exact prompts and reference guides. Rebuild with build.py then Aseprite --batch --script-param out=<source-folder> --script author.lua. Requires Python/Pillow/NumPy/SciPy and Aseprite; previews go into preview/ when rebuilt under _ART_SOURCES.

No installer, commit or push was requested or performed.
'''
(O/'README.md').write_text(report,encoding='utf8');(archive/'README.md').write_text(report,encoding='utf8');(R/'docs/HEAVY_HAMMER_MOTION_1111.md').write_text(report,encoding='utf8')
p=R/'HANDOFF_CODEX.md';old=p.read_bytes();note=f'''## November11,2026 - Reference-led heavy hammer motion for both forms

Mike's two hammer GIFs now guide Chronos and Dracodia/Chronos.32-frame overhead
cycles (31 whole drawings + planted contact hold),15 unique side poses + hold,
full-pose right mirrors and16 actual body-turn whirlwind views per form.
124 original drawings /160 timeline cells. Hilt grips and rigid T heads;
whole-combo landing clearance; one-transition-only whirlwind recovery.
Sources: _ART_SOURCES/heavy_hammer_1111/. Current eight banks override earlier
sparse held attacks through the overhead_slam addon; native flight/catch stays.
{len(checks)} native checks, both weapon contracts and160 pixel-exact source frames pass;
full suite keeps old missing difficultyHealthBaseline15 error. No game.js edit,
commit/push/installer. docs/HEAVY_HAMMER_MOTION_1111.md; docs/qa/heavy_hammer_1111/.

'''.encode('utf8')
if b'Reference-led heavy hammer motion for both forms'not in old:
 assert p.read_bytes()==old,'Concurrent handoff edit';p.write_bytes(note+old)
pack=O/'BOF-heavy-hammer-animation-sources.zip'
with zipfile.ZipFile(pack,'w',zipfile.ZIP_DEFLATED,compresslevel=3)as z:
 for p in archive.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(archive))
print('Finalized',len(checks),'native checks,160 exact source frames,124 original complete drawings. Pack:',pack,flush=True)
