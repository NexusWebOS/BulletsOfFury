from pathlib import Path
import json,subprocess,sys,shutil,hashlib,zipfile
from PIL import Image

W=Path(__file__).resolve().parent;S=W/'cap_strikes_1111';O=W.parent/'outputs/End-cap-strikes'
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=['assets/game.js','assets/boss_animation_1109.js','assets/whole_hammer_1110.js','assets/rigid_hammer_1110.js']
before={n:sha(R/n)for n in protected}
backup=S/'before';backup.mkdir(exist_ok=True)
if not (backup/'overhead_slam_art_1111.js').exists():shutil.copy2(R/'assets/overhead_slam_art_1111.js',backup/'overhead_slam_art_1111.js')
target=R/'assets/game/shared/combat/cap_strikes_1111';target.mkdir(exist_ok=True,parents=True)
files=list((S/'exports').glob('*.webp'));assert len(files)==30,len(files)
for p in files:shutil.copy2(p,target/p.name)
shutil.copy2(S/'cap_strikes_art_1111.js',R/'assets/overhead_slam_art_1111.js')
assert before=={n:sha(R/n)for n in protected}
(S/'installation.json').write_text(json.dumps({'protected':before,'textures':len(files),'banks':list(json.loads((S/'manifest.json').read_text())),'change':'Six complete end-cap-led attack banks; original native attack owners preserved.'},indent=2))
print('Installed square end-cap strike drawings for both bosses.',flush=True)
for name in ['game.js','overhead_slam_art_1111.js']:
 subprocess.run(['node','--check',str(R/'assets'/name)],check=True)
allchecks=[]
for stage in ['5','8']:
 subprocess.run([sys.executable,str(W/('verify_caps_stage'+stage+'.py')),stage],check=True)
 checks=json.loads((O/('verification-stage'+stage)/'checks.json').read_text())
 assert all(c['passed']for c in checks['checks'])and not checks['errors'],checks
 allchecks.extend(checks['checks'])
full=subprocess.run(['node',str(R/'_BUILD_SOURCE/test_fl.js')],cwd=R,capture_output=True,text=True,encoding='utf8',errors='replace')
(S/'full-suite.txt').write_text(full.stdout+'\n'+full.stderr,encoding='utf8')
print('Broad suite exit:',full.returncode,'; final error:',full.stderr[-700:],flush=True)
subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch','--script-param','out='+S.as_posix(),'--script',str(S/'audit-layers.lua')],check=True)
roundtrips=[]
for row in json.loads((S/'layer-audit.json').read_text()):
 n=row['bank'];a=Image.open(S/'exports'/(n+'_regular.png')).convert('RGBA');b=Image.open(S/'exports'/(n+'_roundtrip.png')).convert('RGBA');assert a.tobytes()==b.tobytes(),n
 roundtrips.append(dict(**row,pixelExact=True))
summary={'nativeChecks':len(allchecks),'nativeFailed':[],'browserErrors':[],'sourceRoundtrips':roundtrips,'geometry':json.loads((S/'geometry-review.json').read_text()),'fullSuiteExit':full.returncode,'fullSuiteError':'Existing missing difficultyHealthBaseline15 helper'if'difficultyHealthBaseline15 is not defined'in full.stderr else full.stderr[-700:]}
(S/'summary.json').write_text(json.dumps(summary,indent=2))
for unit in ['chronos','dracodia']:
 for suffix in ['-whole-contract.json','-recording.json']:
  shutil.copy2(W/(unit+suffix),S/(unit+suffix))
archive=R/'_ART_SOURCES/cap_strikes_1111';archive.mkdir(exist_ok=True,parents=True)
for name in ['generated','references']:
 shutil.copytree(S/name,archive/name,dirs_exist_ok=True)
for p in S.iterdir():
 if p.is_file()and p.suffix in['.py','.lua','.json','.js','.txt']:shutil.copy2(p,archive/p.name)
exports=archive/'exports';exports.mkdir(exist_ok=True)
for p in(S/'exports').iterdir():
 if p.suffix in['.aseprite','.png','.webp']and'_roundtrip'not in p.name:shutil.copy2(p,exports/p.name)
qa=R/'docs/qa/cap_strikes_1111';qa.mkdir(exist_ok=True,parents=True)
for name in ['summary.json','geometry-review.json','audit.json','installation.json','full-suite.txt','chronos-whole-contract.json','dracodia-whole-contract.json','chronos-recording.json','dracodia-recording.json']:
 shutil.copy2(S/name,qa/name)
for stage in ['5','8']:
 for name in ['checks.json','trace.json']:shutil.copy2(O/('verification-stage'+stage)/name,qa/('stage'+stage+'-'+name))
fixtures=R/'_BUILD_SOURCE/cap_strikes_1111';fixtures.mkdir(exist_ok=True,parents=True)
for name in ['verify_caps_stage5.py','verify_caps_stage8.py','record_loaded.py','prepare_cap_review.py','review_cap_frames.py','finish_cap_strikes.py']:
 shutil.copy2(W/name,fixtures/name)
report='''# Square end-cap hammer strikes — November 11, 2026

Mike rejected the angled overhead contacts. The previous sequence/state checks did not establish correct visible striking geometry.

Six replacement complete-character attack banks now show one lower cap striking straight down after an over/behind-head load, and the left/right outer cap leading each side blow. Downward contacts use vertical cylinders and perpendicular depth-oriented shafts. Side contacts use horizontal cylinders with visible center-mounted downward shafts, retaining a literal rigid T joint. Chronos retains his dark finned helmet/cyan visor; Dracodia his curved horns/red eyes and purple six-spiked hammer. Both face forward.

24 complete original drawings feed96 timeline cells, including deliberate holds and whole-character right-side mirrors. No separate held weapon assembly, pasted head or runtime rotation. Direct original-master .63 export to640×640 fixed cells, torso/visor horizontal registration and common474 boot baseline. Source tips are measured from actual visible lower/outer cap pixels; native hit and landing owners consume them. The forward descent's horizontal drift is below5 source-cell pixels in both families. See the contact board and GIFs for actual drawing review.

Normal one down strike; Hard two; Furious two then left/right. One initial jump, planted follow-ups. Existing released flight/spin/empty-handed interval, native HP, audio, white/red hit rules, death/rewards and other encounters remain with their prior owners.

57 scoped native checks, both whole-held/released/catch contracts and96 source-frame roundtrips pass with no browser errors. Contact direction/alpha/straightness checks accompany actual rendered contact screenshots and live clips. The broad test suite remains at the recorded missing difficultyHealthBaseline15 helper failure before its final summary.

Current owners: assets/overhead_slam_art_1111.js now registers all six corrected banks in cap_strikes_1111. This supersedes the six held-attack drawings from whole_hammer_1110 and overhead_slam_1111, while preserving detached spin art and native controllers.

Accepted/rejected generation prompts and references, raw complete drawings, Aseprite timelines, manifests, measured contacts and reproducible builder: _ART_SOURCES/cap_strikes_1111/. Native fixtures: _BUILD_SOURCE/cap_strikes_1111/; verification: docs/qa/cap_strikes_1111/. User preview GIFs, contact board and native videos: C:/Users/Mike/Documents/Codex/2026-11-11/i-k/outputs/End-cap-strikes/.

No installer, commit or push. Frame previews illustrate authored motion; live attack clips use an invulnerable observer and do not claim full-fight/campaign validation.
'''
(R/'docs/SQUARE_END_CAP_STRIKES_1111.md').write_text(report,encoding='utf8')
(O/'README.md').write_text(report,encoding='utf8')
p=R/'HANDOFF_CODEX.md';old=p.read_bytes();note='''## November11,2026 — Square end-cap hammer strikes

Mike rejected the angled impact poses. Six fresh complete-character attack banks
now hit DOWN on the lower cap and LEFT/RIGHT with the outer cap; visible rigid T
joints, forward faces, full behind-head windups, native planted1/2/4 sequence.
Current source: _ART_SOURCES/cap_strikes_1111/. The historical overhead_slam addon
now registers these six banks. Do not regenerate the superseded tilted contacts.
57 native checks, both held/released contracts and96 source-frame roundtrips pass;
old broad-suite missing helper remains. docs/SQUARE_END_CAP_STRIKES_1111.md.
No game.js edit, installer, commit or push.

'''.encode('utf8')
if b'Square end-cap hammer strikes'not in old:
 assert p.read_bytes()==old,'Concurrent handoff change; retry safely.'
 p.write_bytes(note+old)
pack=O/'BOF-end-cap-animation-sources.zip'
with zipfile.ZipFile(pack,'w',zipfile.ZIP_DEFLATED,compresslevel=3)as z:
 for p in archive.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(archive))
 z.writestr('README.md',report)
print('Finished square end-cap hammer strikes. Native checks:',len(allchecks),'source frames:',sum(r['frames']for r in roundtrips),flush=True)
