from pathlib import Path
import json,hashlib,shutil,zipfile
W=Path(__file__).resolve().parent; R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury'); O=W.parents[1]/'outputs/Solid-metal-hammers'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
install=json.loads((W/'installation.json').read_text())
for n,h in {**install['after'],**install['protected']}.items(): assert sha(R/n)==h,('Changed since verification',n)
checks=[]
for stage in [5,8]:
 q=json.loads((O/f'verification-stage{stage}/checks.json').read_text()); assert not q['errors']and all(c['passed']for c in q['checks']); checks+=q['checks']
q=json.loads((O/'password-handoff/checks.json').read_text()); assert not q['errors']and all(c['passed']for c in q['checks']); checks+=q['checks']
export=json.loads((W/'export-verification.json').read_text()); full=json.loads((W/'full-suite.json').read_text())
summary=dict(nativeChecks=len(checks),failed=[],browserErrors=[],sourceFrames=64,newWholeDrawings=48,retainedReadyDrawings=16,forms=['Chronos normal','Chronos Chromium','Dracodia normal','Dracodia Chromium'],straightShaftRigidHeadVisualReview=True,export=export,protectedGameplayHashes=install['protected'],fullSuite=full)
(W/'verification.json').write_text(json.dumps(summary,indent=2)); (O/'verification.json').write_text(json.dumps(summary,indent=2))
archive=R/'_ART_SOURCES/solid_hammer_1111'; archive.mkdir(parents=True,exist_ok=True)
for folder in ['generated','jobs']: shutil.copytree(W/folder,archive/folder,dirs_exist_ok=True)
shutil.copytree(W/'reviews',archive/'reviews',dirs_exist_ok=True)
refs=archive/'references'; refs.mkdir(exist_ok=True)
for name in ['blue-hammer.png','purple-hammer.png','chronos.png','chronos-exact-head.png','dracodia.png','drac-grip-master.png','hammer-motion-study.png','PyCciI-motion-study.png']:
 shutil.copy2(W.parent/'heavy_hammer_1111/references'/name,refs/name)
shutil.copy2(W.parent/'heavy_hammer_1111/generated/guided-blue-o1.png',refs/'guided-blue-o1.png')
for p in W.iterdir():
 if p.is_file()and p.suffix in ['.py','.lua','.json','.js','.txt','.html']: shutil.copy2(p,archive/p.name)
ex=archive/'exports'; ex.mkdir(exist_ok=True)
for p in (W/'exports').iterdir():
 if p.is_file()and p.suffix in ['.aseprite','.png','.webp']and'_roundtrip'not in p.name: shutil.copy2(p,ex/p.name)
qa=R/'docs/qa/solid_hammer_1111'; qa.mkdir(exist_ok=True,parents=True)
for name in ['verification.json','installation.json','export-verification.json','audit.json','full-suite.txt']: shutil.copy2(W/name,qa/name)
for stage in [5,8]:
 for name in ['checks.json','trace.json']: shutil.copy2(O/f'verification-stage{stage}'/name,qa/f'stage{stage}-{name}')
shutil.copy2(O/'password-handoff/checks.json',qa/'password-checks.json')
for unit in ['chronos','dracodia']:
 for suffix in ['-recording.json','-whole-contract.json']: shutil.copy2(W/(unit+suffix),qa/(unit+suffix))
report=f'''# Solid metal hammer overhead correction — November 11, 2026

Mike rejected the bowed/parallel shaft and curled side socket in the frontal hammer downswing. Those drawings made a solid metal weapon read as a rubber mallet. This correction supersedes the two overhead banks from front_hammer_1111, including the lift, downstroke and recovery for Chronos and copied Chronos Dracodia. Normal and Chromium use identical geometry, with offline material variants; red and native hit masks are included.

The new complete poses keep one straight shaft through both hands, entering the cylinder side midpoint. The head turns in depth during the overhead stroke: its near cap faces the camera at peak windup, then the lower endcap leads the ground contact. This replaces the previous upright barrel beside a parallel vertical shaft joined by a curved elbow. The head and shaft remain solid through contact. Dracodia's near-facing cap retains its three spikes in foreshortened poses. These are whole character-and-held-weapon drawings, not pasted body/weapon assemblies or runtime bending. The original canonical standalone T hammers and Mike's motion studies were inspected before drawing. Exact built-in image generation/edit prompts and raw candidates are retained in jobs/ and generated/. PixelLab was not charged.

Each overhead cycle retains32 timeline frames:8 existing ready poses and24 newly selected lift/down/recovery drawings. There are48 new whole drawings total,64 overhead frames across the two forms; Chromium shares the exact silhouette. Fixed512x512 native cells, pivot[256,256], common boot baseline410, proportional import from master sheets. The lifted head's entry into blank internal row padding is retained from the original master rather than cropped. Foot Y excludes the low head; root X uses the complete lower body band to avoid a sideways jump near contact. No per-pose resizing or image interpolation is used. All64 Aseprite exports match source pixels exactly; every material keeps identical alpha masks.

Installed assets:10 overhead WebPs in assets/game/shared/combat/front_hammer_1111/, plus assets/overhead_slam_art_1111.js with measured head/cap/alpha metadata. The existing side, right and whirlwind banks are retained byte-for-byte in the registration. assets/game.js, whole_hammer_1110.js and boss_animation_1109.js retain their pre-change hashes. Native attack timing/counts, warnings, armor activation, released flight/catch, hit flashes, HP owners and password animation guard remain with their existing controllers.

Verification: {len(checks)} focused native checks pass, no browser errors. Both bosses retain their difficulty-specific planted strike count, full-combo clearance, real native Chromium activation and visible white hit flashes. New silent native films show regular/Chromium strokes by stepping the real game loop and capturing rendered pixels, and verify whole-held / separate-released weapon contracts. A live MediaRecorder attempt stalled after the initial Chronos checks; it was stopped and replaced with bounded frame-step capture. No audio changes were made or new audio verification claimed. The actual HAMMER password route retains intro/dance/break/attack animation ownership. Sources also pass64 pixel-exact Aseprite roundtrips and matching material-mask checks. The full game suite exits{full['exit']} before its summary on the existing missing difficultyHealthBaseline15 helper; the full log is retained. These are scoped protected-observer reviews, not a claimed full-campaign clear.

Open playback.html for normal/Chromium/red frame stepping, including retained side/whirl moves. all-four-overhead.gif compares all four forms; chronos-hammer.mp4 and dracodia-hammer.mp4 show the native game. BOF-solid-metal-hammer-sources.zip contains editable sources, original generated masters, prompts and source verification. Builder dependencies for the retained ready/side/whirl material remain in sibling front_hammer_1111 and heavy_hammer_1111 source archives.

No commit, push, installer or publication was requested or performed.
'''
for p in [O/'README.md',archive/'README.md',R/'docs/SOLID_METAL_HAMMERS_1111.md']: p.write_text(report,encoding='utf8')
note=f'''## November11,2026 - Solid metal hammer correction / all four forms

Mike rejected the curled hammer socket and rubbery downswing. New complete
overhead lift/down/recovery drawings replace those poses for Chronos and
Dracodia, normal and Chromium. Straight shafts, rigid head perspective and
spiked near caps;32 frames per overhead bank,48 new complete drawings total.
Preserves side/right/whirl banks and existing native controllers. All64 source
frames roundtrip exactly;{len(checks)} focused native checks pass with no browser errors.
Full suite retains missing difficultyHealthBaseline15 abort. Current overhead
sources: _ART_SOURCES/solid_hammer_1111; docs/SOLID_METAL_HAMMERS_1111.md.
No game.js/whole_hammer/boss_animation edit, commit, push or installer.

'''.encode('utf8')
p=R/'HANDOFF_CODEX.md'; old=p.read_bytes()
if b'Solid metal hammer correction / all four forms'not in old:
 assert p.read_bytes()==old; p.write_bytes(note+old)
with zipfile.ZipFile(O/'BOF-solid-metal-hammer-sources.zip','w',zipfile.ZIP_DEFLATED,compresslevel=3)as z:
 for p in archive.rglob('*'):
  if p.is_file(): z.write(p,p.relative_to(archive))
print('Archived corrected sources and recorded native verification:',len(checks),'checks.',flush=True)
