from pathlib import Path
import json,hashlib,shutil,zipfile
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Three-way-hammer'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
install=json.loads((W/'installation.json').read_text())
for n,h in {**install['after'],**install['protected']}.items():assert sha(R/n)==h,('Source changed after checks',n)
checks=[]
for stage in [5,8]:
 q=json.loads((O/f'verification-stage{stage}/checks.json').read_text());assert not q['errors']and all(c['passed']for c in q['checks']);checks+=q['checks']
q=json.loads((O/'password-handoff/checks.json').read_text());assert not q['errors']and all(c['passed']for c in q['checks']);checks+=q['checks']
export=json.loads((W/'export-verification.json').read_text());full=json.loads((W/'full-suite.json').read_text())
summary=dict(nativeChecks=len(checks),failed=[],browserErrors=[],directions=['center','right','left'],forms=['Chronos normal','Chronos Chromium','Dracodia normal','Dracodia Chromium'],sourceFrames=192,newWholeDrawings=30,exactWholePoseRightMirrors=64,retainedCenterReadyLiftPeak=34,approvedLeftFrames=64,export=export,gameAndSharedSamplerUnchanged=install['protected'],fullSuite=full)
(W/'verification.json').write_text(json.dumps(summary,indent=2));(O/'verification.json').write_text(json.dumps(summary,indent=2))
archive=R/'_ART_SOURCES/three_way_hammer_1111';archive.mkdir(exist_ok=True,parents=True)
for folder in ['generated','jobs','reviews']:shutil.copytree(W/folder,archive/folder,dirs_exist_ok=True)
for p in W.iterdir():
 if p.is_file()and p.suffix in ['.py','.json','.lua','.js','.txt']:shutil.copy2(p,archive/p.name)
refs=archive/'references';refs.mkdir(exist_ok=True)
for name in ['blue-hammer.png','purple-hammer.png','chronos.png','chronos-exact-head.png','dracodia.png']:shutil.copy2(W.parent/'heavy_hammer_1111/references'/name,refs/name)
for name in ['blue-down','blue-recovery','drac-down']:shutil.copy2(W.parent/'solid_hammer_1111/generated'/(name+'.png'),refs/('approved-left-'+name+'.png'))
ex=archive/'exports';ex.mkdir(exist_ok=True)
for p in(W/'exports').iterdir():
 if p.is_file()and p.suffix in ['.aseprite','.webp','.png']and'_roundtrip'not in p.name:shutil.copy2(p,ex/p.name)
qa=R/'docs/qa/three_way_hammer_1111';qa.mkdir(exist_ok=True,parents=True)
for name in ['verification.json','installation.json','export-verification.json','full-suite.txt']:shutil.copy2(W/name,qa/name)
for stage in [5,8]:
 for name in ['checks.json','trace.json','three-direction-pixels.json']:shutil.copy2(O/f'verification-stage{stage}'/name,qa/f'stage{stage}-{name}')
shutil.copy2(O/'password-handoff/checks.json',qa/'password-checks.json')
for unit in ['chronos','dracodia']:shutil.copy2(W/(unit+'-whole-contract.json'),qa/(unit+'-whole-contract.json'))
report=f'''# Center, right and left hammer ground smashes — November 11, 2026

Mike approved the solid-metal left smash and asked for the same smash directly ahead of the actor plus a right smash made by mirroring. Chronos and copied Chronos Dracodia now have all three directions in normal and Chromium forms, with matching red and hit variants.

The default overhead bank is now a centered ground strike, with the lower endcap landing between the actor's boots. The existing first17 ready/lift/peak poses per character are retained. Seven centered downswing and eight recovery drawings per character provide30 new complete authored poses. The approved left32-frame bank is retained pixel-for-pixel in every material. The right32-frame bank is an exact whole-pose mirror of that left bank, including head/cap/hand landmarks, alpha spans and a reflected native pivot255 instead of256, so world offsets are exact sign inversions. Six32-frame banks give192 timeline/source frames; this count includes64 retained left frames,64 whole-pose mirrors,34 retained center ready/lift/peak poses and30 new drawings. No cropped/pasted weapons or body parts, no frame interpolation or flexible metal joints. New center poses remain at the existing detail budget and common512x512 cell/boot baseline410. All source imports use the same proportional .86 calibration.

The current native attack keeps one committed direction for its complete warn, leap, planted repetitions and recovery. Successive attacks choose center, right, then left while preserving the existing1/2/4 native contact count by difficulty. The prior ready grip is kept during the initial lift; direction changes at the high pose, avoiding an immediate cross-body flip at attack start. A late TD1111 block in assets/whole_hammer_1110.js routes the whole-pose rows and copied sampler, extends full-combo clearance to all directions, and preloads the added red banks. Actual warning/landing/damage owners consume each selected bank's measured cap and pivot. Side sweeps and whirlwind retain their separate existing banks. Held/released/catch ownership, native armor HP and activation, music and impact cues remain with their existing controllers.

Installed:30 material WebPs under assets/game/shared/combat/three_way_hammer_1111; six bank registrations in assets/overhead_slam_art_1111.js; a scoped late direction extension in assets/whole_hammer_1110.js. assets/game.js and assets/boss_animation_1109.js retain their pre-change hashes. Other ongoing work, including the pilot/comic updates, is preserved.

Verification: {len(checks)} focused native checks pass, with no browser errors. Both characters and both normal/Chromium forms exercise each of the three directions through real native ticks. Four-contact Furious sequencing, planted roots, horizontal clearance and actual cap-to-warning alignment are checked in all12 combinations. Lossless native contact/windup screenshots cover those same12 combinations. Existing difficulty counts, real native Chromium activation, hit flash/expiry, ball banks, whirlwind and held/released weapon contracts remain verified. The actual HAMMER password route keeps intro/dance/break/attack animation ownership. A legacy windup probe initially counted only the literal original overhead bank name; it now checks the complete overhead family while retaining the behind-head phase/count assertion. This was a probe update, not removal of the windup requirement.

All192 Aseprite exports match source pixels exactly; all material alpha masks match. Every right pose and its physical landmarks are checked against the corresponding left reflection. Final whole-pose onion reviews and native screenshots are retained in reviews/. The broad game suite exits{full['exit']} before its summary on the existing missing difficultyHealthBaseline15 helper; log retained. The native opening leap still follows its original controller; these fixtures are scoped boss reviews, not a claimed campaign clear. No audio changes or new audio recording are claimed.

Open playback.html to select directly-in-front, right or left and step all four forms. all-four-center.gif and all-four-right.gif show the requested new directions. Exact built-in image generation/edit prompts and selected/rejected raw candidates are retained under jobs/ and generated/. PixelLab credits were not used. Editable sources and verification are in BOF-three-way-hammer-sources.zip. Rebuilding retained poses uses the sibling solid_hammer_1111 source archive from the preceding approved pass; existing side/whirl registrations retain their older source owners.

No commit, push, installer or publication was requested or performed.
'''
for p in [O/'README.md',archive/'README.md',R/'docs/THREE_WAY_HAMMER_1111.md']:p.write_text(report,encoding='utf8')
note=f'''## November11,2026 - Center and mirrored-right hammer ground smashes

Mike approved the rigid left hit and requested a directly-ahead center smash
and mirrored right smash for all four forms. Six32-frame overhead banks now
cover center/right/left for Chronos and Dracodia, normal and Chromium. The
approved left plates are unchanged; right poses/physical anchors mirror exactly.
TD1111 keeps a committed attack direction and prior grip during the initial lift.
Center/right/left attacks preserve native counts, planted roots, warnings and HP.
{len(checks)} focused native checks and192 exact Aseprite frames pass. Full suite
retains the missing difficultyHealthBaseline15 abort. Source/evidence:
_ART_SOURCES/three_way_hammer_1111; docs/THREE_WAY_HAMMER_1111.md.
No game.js/shared-sampler edit, commit, push or installer.

'''.encode('utf8')
p=R/'HANDOFF_CODEX.md';old=p.read_bytes()
if b'Center and mirrored-right hammer ground smashes'not in old:
 assert p.read_bytes()==old;p.write_bytes(note+old)
with zipfile.ZipFile(O/'BOF-three-way-hammer-sources.zip','w',zipfile.ZIP_DEFLATED,compresslevel=3)as z:
 for p in archive.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(archive))
print('Saved three-direction source archive and native evidence:',len(checks),'checks.',flush=True)
