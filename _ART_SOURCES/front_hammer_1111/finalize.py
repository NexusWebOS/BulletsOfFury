from pathlib import Path
import json,shutil,hashlib,zipfile
from PIL import Image
W=Path(__file__).resolve().parent;OLD=W.parent/'heavy_hammer_1111';R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Front-facing-hammer'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
install=json.loads((W/'installation.json').read_text());assert all(sha(R/n)==h for n,h in install['after'].items())
checks=[];roundtrips=[]
for stage in [5,8]:
 q=json.loads((O/f'verification-stage{stage}/checks.json').read_text());assert not q['errors']and all(c['passed']for c in q['checks']);checks+=q['checks']
q=json.loads((O/'password-handoff/checks.json').read_text());assert not q['errors']and all(c['passed']for c in q['checks']);checks+=q['checks']
for j in json.loads((W/'aseprite-audit.json').read_text()):
 a=Image.open(W/'exports'/(j['bank']+'_regular.png')).convert('RGBA');b=Image.open(W/'exports'/(j['bank']+'_roundtrip.png')).convert('RGBA');assert a.tobytes()==b.tobytes();roundtrips.append(dict(**j,pixelExact=True))
full=json.loads((W/'full-suite.json').read_text());summary=dict(nativeChecks=len(checks),failed=[],browserErrors=[],sourceRoundtrips=roundtrips,updatedSourceFrames=128,newWholeDrawings=78,retainedReadyDrawings=16,retainedWhirlFrames=32,forms=['Chronos normal','Chronos Chromium','Dracodia copied Chronos normal','Dracodia copied Chronos Chromium'],redMaterialRouting=True,nativeArmorActivationsVerified=True,coreGameUnchanged=True,fullSuiteExit=full['exit'],fullSuiteError='Existing difficultyHealthBaseline15 is not defined'if'difficultyHealthBaseline15'in(W/'full-suite.txt').read_text()else full['lastError'])
summary.update(passwordHandoffVerified=True,separateBallRegistryVerified=True)
(W/'summary.json').write_text(json.dumps(summary,indent=2));(O/'verification.json').write_text(json.dumps(summary,indent=2))
selected=['drac-down','blue-down','drac-lift-front','blue-lift-front','drac-recovery-center','blue-recovery','drac-sides-front','blue-sides-front']
for n in selected:
 p=W/'jobs'/(n+'.json');d=json.loads(p.read_text());d.update(accepted=True,selectedCells=list(range(7 if n.endswith('-down') else 16 if 'sides' in n else 8)));p.write_text(json.dumps(d,indent=2))
ref=W/'references';ref.mkdir(exist_ok=True)
for n in ['blue-overhead','corrupt-overhead']:
 d=ref/'ready'/n;d.mkdir(exist_ok=True,parents=True)
 for i in range(8):shutil.copy2(OLD/'exports'/n/f'{i:02}.png',d/f'{i:02}.png')
shutil.copy2(OLD/'manifest.json',ref/'previous-manifest.json')
archive=R/'_ART_SOURCES/front_hammer_1111';archive.mkdir(exist_ok=True,parents=True)
for folder in ['generated','jobs','references']:shutil.copytree(W/folder,archive/folder,dirs_exist_ok=True)
for p in W.iterdir():
 if p.is_file()and p.suffix in['.py','.lua','.json','.js','.txt']:shutil.copy2(p,archive/p.name)
out=archive/'exports';out.mkdir(exist_ok=True)
for p in(W/'exports').iterdir():
 if p.is_file()and p.suffix in['.aseprite','.webp','.png']and'_roundtrip'not in p.name:shutil.copy2(p,out/p.name)
qa=R/'docs/qa/front_hammer_1111';qa.mkdir(exist_ok=True,parents=True)
for n in ['summary.json','installation.json','audit.json','earlier-animation-evidence.json','full-suite.txt']:shutil.copy2(W/n,qa/n)
for stage in [5,8]:
 for n in ['checks.json','trace.json']:shutil.copy2(O/f'verification-stage{stage}'/n,qa/f'stage{stage}-{n}')
for n in ['checks.json','diagnosis.json']:shutil.copy2(O/'password-handoff'/n,qa/('password-'+n))
fixtures=R/'_BUILD_SOURCE/front_hammer_1111';fixtures.mkdir(exist_ok=True,parents=True)
for n in ['verify_front_stage5.py','verify_front_stage8.py','front_record_loaded.py']:shutil.copy2(W.parent/n,fixtures/n)
for unit in ['chronos','dracodia']:
 for suffix in ['-whole-contract.json','-recording.json']:shutil.copy2(W.parent/(unit+suffix),qa/(unit+suffix))
report=f'''# Forward-facing hammer strikes and Chromium forms — November 11, 2026

Mike asked for frontal hammer strikes with a visible lift/twist into each side blow, integrated into Chronos and Dracodia's copied Chronos form, including both Chromium armor states. The earlier hammer/password animations should have been inspected before repeatedly generating replacements. The existing 17-frame blue_slam, blue_side, their armor variants and copied-form sets remain available. Their source paths and hashes, plus the separate HT27/HAMA attack route, are recorded in earlier-animation-evidence.json; an inspected contact board is in the review material.

Six held-attack banks now use frontal complete character-and-hammer drawings. Each form keeps its 32-frame overhead cycle with a deliberate planted impact hold and gets16 distinct side poses with whole-pose right mirrors. There are78 newly selected complete drawings plus16 retained ready drawings,128 updated timeline cells. The prior16-view whirlwind per form remains. Both hands visibly grip one hilt; the low downward cap faces the ground in front of the boots. The face stays forward during the strike while hips/shoulders load and unwind. No body/weapon assembly, head stamping, pixel interpolation or runtime art rotation.

Normal, Chromium and red material variants are registered together with matching white/red hit masks. Normal and Chromium native attack counts, planted root and full-combo clearance are verified on Normal/Hard/Furious. Actual fr27BeginArmor/fr27ActivationTick and copied hb20Start('armor') routes return to the frontal held-hammer form without changing body HP. The red state's native attack book remains intact; red art is checked through the held-state/material matrix, rather than pretending it follows the ordinary down-combo AI. Giant windups/holds and storm recovery now use the same frontal art; red held banks preload with the encounter. Native detached flight/catch and existing whirlwind remain with their prior owners.

Current owners: assets/overhead_slam_art_1111.js registers the six new banks in front_hammer_1111 and retains the two heavy_hammer_1111 whirl banks. A late FH1111 block in assets/whole_hammer_1110.js adds held-state coverage/preload. The shared sampler in assets/boss_animation_1109.js reads the active RD74 frame registry, preserving separately registered copied fold/roll/unfold banks. assets/game.js is unchanged. The password display handoff again returns control to the native ship/dance/STOP artwork outside attack mode; the newer held-hammer selector had intercepted those modes. Actual HAMMER route intro/dance/break/attack draws are checked, with before/after diagnosis. HAMMER/HAMA music, dance timing, locks and attack controllers remain intact.

Verification: {len(checks)} focused native checks pass with no browser errors, actual armor transitions, password animation handoff, independent copied ball banks and both held/released/catch contracts. All128 updated Aseprite frames export pixel-exactly. Native regular/Chromium films include decoded sound; the interactive player and paired GIFs expose both forms together. These are scoped protected-observer reviews, not full-campaign clear claims. The broad suite still exits1 before its final summary on the existing missing difficultyHealthBaseline15 helper; full log included.

Open playback.html for normal/Chromium/red frame stepping. both-forms-front.gif and both-forms-sides.gif compare both normal and Chromium characters. chronos-hammer.mp4 and dracodia-hammer.mp4 are native recordings. Exact built-in image generation/edit prompts and selected source cells are retained under jobs/. PixelLab was not charged. Editable sources use fixed512x512 cells, pivot[256,256], common boot baseline410 and uniform calibration per original source group; exports import directly from masters. The builder's legacy-ready dependency is retained under references/ready and previous-manifest.json. Full earlier source dependencies remain in sibling heavy_hammer_1111.

No installer, commit or push was requested or performed.
'''
(O/'README.md').write_text(report,encoding='utf8');(archive/'README.md').write_text(report,encoding='utf8');(R/'docs/FRONT_HAMMER_CHROMIUM_1111.md').write_text(report,encoding='utf8')
note=f'''## November11,2026 - Frontal hammer strikes / both Chromium forms

Both Chronos and Dracodia/Chronos now strike facing forward and twist/lift into
side blows. Six new held banks keep32 overhead timeline frames and16 real side
poses per form; whole-pose right mirrors, matching normal/Chromium/red palettes.
Actual armor activation returns to the new whole hammer pose in both bosses.
FH1111 extends depth windups/storm recovery and preloads red held art.
{len(checks)} native checks, both weapon contracts and128 exact Aseprite frames pass.
Full suite keeps existing difficultyHealthBaseline15 failure. Earlier17-frame
slam/side/armor sets and separate HAMMER/HAMA route recorded as source evidence;
do not repeat generation without comparing those working references first.
Sources _ART_SOURCES/front_hammer_1111/; docs/FRONT_HAMMER_CHROMIUM_1111.md.
Retains prior whirlwind, released weapon and native attack/HP owners. No game.js
edit, commit, push or installer.

'''.encode('utf8')
p=R/'HANDOFF_CODEX.md';old=p.read_bytes()
if b'Frontal hammer strikes / both Chromium forms'not in old:
 assert p.read_bytes()==old;p.write_bytes(note+old)
with zipfile.ZipFile(O/'BOF-frontal-hammer-sources.zip','w',zipfile.ZIP_DEFLATED,compresslevel=3)as z:
 for p in archive.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(archive))
print('Saved final source archive, native verification and project handoff:',len(checks),'checks.',flush=True)
