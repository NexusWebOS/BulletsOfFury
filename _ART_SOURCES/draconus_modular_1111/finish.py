from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil,subprocess,zipfile,html
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Draconus-rotor-and-full-stages'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=json.loads((O/'gun-verification/checks.json').read_text());installed=json.loads((W/'installation.json').read_text());suite=json.loads((W/'preflight.json').read_text());editable=json.loads((W/'editable-verification.json').read_text())
repair=json.loads((O/'stage8-repair-verification.json').read_text());repair_info=json.loads((W/'stage8-repair.json').read_text())
assert len(repair['checks'])==7 and all(c['passed']for c in repair['checks'])and not repair['errors']
assert repair['repairHash']==repair_info['after']==sha(R/'assets/playtest_repairs_1108.js')
assert len(checks['checks'])==35 and all(c['passed']for c in checks['checks'])and not checks['errors']
assert checks['runtimeHash']==sha(R/'assets/draconus_modular_1111.js')
assert all(sha(R/n)==h for n,h in installed['protected'].items())
for n in ['draconus_modular_1111.js','draconus_modular_art_1111.js']:assert sha(W/n)==sha(R/'assets'/n)
for p in (W/'exports').glob('*.webp'):assert sha(p)==sha(R/'assets/game/shared/combat/draconus_modular_1111'/p.name)
assert editable['exactLayerFrames']==216
reports=[]
for stage in range(5,9):
 p=O/f'stage-{stage}/report.json';r=json.loads(p.read_text());assert r['completed']and r['decoded']and r['nativeJSUnchanged']and not r['errors']and not r['consoleErrors'],stage
 assert not r['capture']['tapErrors']and r['capture']['peak']>.001 and len(r['capture']['waves'])==r['setup']['expected'],stage
 reports.append(r)
assert len(reports[3]['capture']['gunPhases'])==36,'Full Stage 8 film must actually show the modular barrel.'
# Preserve every native H264 packet; convert only the audio to AAC and add a
# normal seek index for desktop players. Verify before replacing our delivery.
ff=imageio_ffmpeg.get_ffmpeg_exe();probe=shutil.which('ffprobe');assert probe
def media(p,count=False):
 args=[probe,'-v','error']+(['-count_packets']if count else[])+['-show_streams','-show_format','-of','json',str(p)]
 return json.loads(subprocess.check_output(args))
for r in reports:
 stage=r['stage'];p=(O/f'stage-{stage}-furious.mp4').resolve();tmp=(O/f'stage-{stage}-compatible.mp4').resolve();assert p.parent==O.resolve()and tmp.parent==O.resolve()
 if not r.get('compatibleDelivery') and shutil.disk_usage(O).free<=p.stat().st_size+150_000_000:
  data=media(p,True);r['compatibleDelivery']=dict(nativeCaptureSHA256=sha(p),nativeMedia=data,videoPacketsPreserved=next(s['nb_read_packets']for s in data['streams']if s['codec_type']=='video'),audio=next(s['codec_name']for s in data['streams']if s['codec_type']=='audio'),video='Unmodified native H264 capture',seekIndex='Native fragmented MP4; actual browser seeking checked below',fullDecode=r['decoded'],reason='Preserved the original complete film when the drive became full; no space-intensive optional conversion.')
  r['encoding']='Original native H264/Opus MP4 capture, fully decoded and browser checked.';r['deliverySHA256']=sha(p)
  (O/f'stage-{stage}/report.json').write_text(json.dumps(r,indent=2))
 if not r.get('compatibleDelivery'):
  assert not tmp.exists()and shutil.disk_usage(O).free>p.stat().st_size+150_000_000
  before=media(p,True);beforehash=sha(p)
  q=subprocess.run([ff,'-v','error','-i',str(p),'-map','0:v:0','-map','0:a:0','-c:v','copy','-c:a','aac','-b:a','128k','-movflags','+faststart',str(tmp)],capture_output=True)
  assert q.returncode==0,q.stderr.decode(errors='replace')
  after=media(tmp,True);v=lambda x:next(s for s in x['streams']if s['codec_type']=='video')
  assert v(before)['codec_name']==v(after)['codec_name']=='h264' and v(before)['nb_read_packets']==v(after)['nb_read_packets']
  assert abs(float(before['format']['duration'])-float(after['format']['duration']))<.15
  assert any(s['codec_name']=='aac'for s in after['streams'])
  subprocess.run([ff,'-v','error','-threads','2','-i',str(tmp),'-f','null','-'],capture_output=True,check=True)
  assert sha(p)==beforehash;tmp.replace(p)
  r['compatibleDelivery']=dict(nativeCaptureSHA256=beforehash,nativeMedia=before,videoPacketsPreserved=v(after)['nb_read_packets'],audio='AAC stereo 128kbps',video='Original H264 packets copied without re-encoding',seekIndex='faststart',fullDecode=True)
  r['encoding']='Original native H264 video packets with compatible AAC audio and faststart seeking.'
  r['media']=media(p);r['bytes']=p.stat().st_size;r['deliverySHA256']=sha(p)
  (O/f'stage-{stage}/report.json').write_text(json.dumps(r,indent=2))
 print('Verified compatible complete film:',stage,flush=True)
# Honest contact sheets from actual captured frames, including the final screen.
for r in reports:
 folder=O/f'stage-{r["stage"]}';paths=sorted(folder.glob('frame-*.png'))
 selected=[paths[round((len(paths)-1)*k/6)]for k in range(7)]+[folder/'final-screen.png']
 board=Image.new('RGB',(1280,464),'#08121c');d=ImageDraw.Draw(board)
 for k,p in enumerate(selected):
  im=Image.open(p).convert('RGB');im.thumbnail((320,211));board.paste(im,(k%4*320,k//4*232));d.text((k%4*320+8,k//4*232+214),p.stem,fill='white')
 board.save(O/f'stage-{r["stage"]}-contact-sheet.jpg',quality=90)
def duration(r):
 t=round(float(r['media']['format']['duration']));return f'{t//60}:{t%60:02}'
summary=dict(nativeChecks=42,gunChecks=35,stage8Repair=repair,editable=editable,fullSuite=suite,runtimeHash=checks['runtimeHash'],protected=installed['protected'],films=[dict(stage=r['stage'],difficulty=r['difficulty'],duration=duration(r),waves=len(r['capture']['waves']),nativeCompletion=r['reason'],completed=r['completed'],rendererErrors=r['errors'],consoleErrors=r['consoleErrors'],failedRequests=r['failedRequests'],gunPhases=len(r['capture']['gunPhases']),sha256=r['deliverySHA256'],assistance=r['assistance'],media=r['media'],compatibleDelivery=r['compatibleDelivery'])for r in reports])
rows='\n'.join(f'| {r["stage"]} | {duration(r)} | {len(r["capture"]["waves"])}/{r["setup"]["expected"]} | {r["reason"]} |'for r in reports)
readme=f'''# Draconus modular gun and complete Furious stage reviews

Draconus's held chaingun now has a solid fixed receiver and an independently rotating 36-phase barrel. Normal and Chromium use the same registered mechanics and their own baked materials. The complete fixed body stays behind the gun; foreground grips come from that exact same body drawing. Native rev, firing, coast, box ejection/catch, stow, break and hammer recall remain connected. The real gun alpha determines its target; its HP and white hit feedback stay separate from the body. Warnings, SHOOT graphics, muzzle flash and native ordinary rounds share the actual bore. No runtime gun rotation, warping or generated body parts are used. The current approved ship transformations and all center/right/left hammer banks remain protected.

Mike explicitly requested this modular gun, superseding the earlier whole-held-gun rule only for this gun. Other held hammer poses remain complete authored frames. DGM1111 selects static atlas cells; Chronos's 36 canonical axial phases were exported offline and recolored into Draconus materials. The empty-handed background body was edited with the built-in image tool. PixelLab credits were not used. Native health, damage timing, bullet cadence, module break, copy progression and rewards remain owned by their existing encounter code.

## Four complete films

| Stage | Running time | Native waves | Finish |
| --- | --- | --- | --- |
{rows}

All four are **Furious with real game sound and a visibly labeled invulnerable keyboard review pilot**. The recording fixture starts with a tier-5 review loadout and40 missiles; later equipment changes come from native pickups. This permits complete visual stress reviews, not unassisted difficulty clears. Enemy health, stage clocks, waves, boss phases, damage and defeat are native; no enemy HP/phase/clock/clear writes. Each movie starts at that stage's native entry and continues through its completion or the native Stage7→8 handoff. Stage8 begins with the native post-Stage7 rift arrival. Its recording visits all36 modular barrel phases. The footer is outside the1280×800 game picture. Native H264 packets and sound are preserved. Exact codecs and actual browser playback/seek checks are retained in the recording reports; when there is insufficient drive space for optional conversion, the original H264/Opus MP4 remains the delivery.

Open **playback.html** for the four full videos, seeking controls, actual-game stills and the modular-gun preview. The contact sheets and per-stage reports retain the full native trace, source hashes, sound/cue statistics and final screen. Completed films fully decode, contain video and audio, have no renderer/console errors, and leave game JS unchanged. Unsuccessful early takes are separately labeled diagnostics; they are not delivered as completed films.

## Stage8 stress-test repair

The full stress recording exposed a real update exception on the Neural Archon transition. Cached Retina descriptors retained host-arm position getters after their sockets no longer existed. Boss-flash polling incorrectly counted those descriptors as physical HP pools. The one-line production fix in assets/playtest_repairs_1108.js excludes target descriptors while retaining unique real child pools. Seven native regression checks reproduce the obsolete getter, verify the corrected polling, retain genuine per-part hit flashes, preserve HP and exercise the actual copied-form roster. The complete Stage8 film was restarted after this fix. Stages5–7 were recorded before this narrowly scoped feedback fix; their recorded runtime hashes are retained, and the graphics/combat/HP/progression owners are identical. See stage8-repair-verification.json.

## Evidence and editable sources

42 focused native checks pass:35 for both gun materials, fixed receiver/36 axial phases, actual box/catch handoff, no early shots or health reset, real muzzle/warning/ordinary rounds, coast/stow, independent gun/body damage and gun-only white feedback, break/no respawn/recall, full Chromium activation with gun retained, and prior center/right/left strikes in both bosses and materials; plus7 for the discovered Stage8 crash. Both editable Aseprite timelines reopen with36 frames and3 layers; all216 layer frames match their imported pixels. The source tag is slowed for inspection; native rev/fire rates remain controlled by the encounter. See gun-verification/checks.json and verification.json.

Required broad checks: syntax passes. **The full test_fl.js suite still exits1 before its summary on the existing ReferenceError: difficultyHealthBaseline15 is not defined**, assets/combat_polish_0927b.js:151. The exact preflight output is retained. These assisted recordings do not establish unassisted Furious balance, physical controller/co-op behavior or release readiness. No commit, push, installer or publication was performed.

Runtime: assets/draconus_modular_1111.js, assets/draconus_modular_art_1111.js, assets/game/shared/combat/draconus_modular_1111, two final script includes in index.html. Rebuild/source archive: _ART_SOURCES/draconus_modular_1111. The ZIP contains the original generated master/prompt, canonical gun references, registration/material metadata, lossless atlases, exact editable sources, build/install scripts and evidence. Canonical on-screen game spellings remain Chronos and Dracodia.
'''
(O/'README.md').write_text(readme,encoding='utf-8');(O/'verification.json').write_text(json.dumps(summary,indent=2));shutil.copy2(W/'full-suite.log',O/'full-suite.log')
cards=''.join(f'<article><h2>Stage {r["stage"]} · {duration(r)}</h2><video id="stage{r["stage"]}" controls preload="metadata" poster="stage-{r["stage"]}-contact-sheet.jpg"><source src="stage-{r["stage"]}-furious.mp4" type="video/mp4"></video><p>{len(r["capture"]["waves"])}/{r["setup"]["expected"]} native waves · {html.escape(r["reason"])}</p><a href="stage-{r["stage"]}-furious.mp4">Open full video</a> · <a href="stage-{r["stage"]}/report.json">Recording evidence</a></article>'for r in reports)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>BOF · Complete Furious Stages5–8</title><style>body{margin:24px auto;padding:0 20px;max-width:1380px;background:#0c121b;color:#eaf2ff;font:17px/1.5 system-ui}h1{font-size:30px}h2{font-size:23px}a{color:#8ad7ff}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,560px),1fr));gap:22px}article{background:#151e2b;padding:16px;border:1px solid #334257;border-radius:8px}video{width:100%;background:#05080d}img{max-width:100%}.note{padding:14px;border-left:4px solid #ffd06b;background:#182130}footer{margin:28px 0}</style><h1>Complete Furious Stage5–8 reviews</h1><p class="note">Full native stage entries, waves, boss fights and finishes, with sound. These films use a labeled invulnerable keyboard review pilot and tier-5 initial review equipment. Enemy health and progression remain native. They are assisted visual stress reviews.</p><main>CARDS</main><h2>Draconus · independent 36-phase barrel</h2><img src="draconus-modular-rotor.gif" alt="Actual game view of normal and Chromium Draconus rotating the modular gun barrel"><p>Fixed receiver, separate source-alpha gun target, normal and Chromium. The box/catch, damage, break/stow and hammer recall keep native ownership.</p><footer><a href="BOF-draconus-modular-sources.zip">Editable sources</a> · <a href="README.md">Scope and limitations</a> · <a href="verification.json">Verification</a><p>The broad suite still stops on its existing missing difficultyHealthBaseline15 helper. No release-readiness claim.</p></footer><script>document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('video').forEach(o=>{if(o!==v)o.pause()})));</script></html>'''.replace('CARDS',cards)
(O/'playback.html').write_text(page,encoding='utf-8')
# Check the actual delivered videos with a lightweight player, not another game.
playback=[];errors=[]
with sync_playwright()as pw:
 br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.goto((O/'playback.html').as_uri())
 for stage in range(5,9):
  p.wait_for_function('s=>{const v=document.querySelector("#stage"+s);return v.readyState>=1&&Number.isFinite(v.duration)}',arg=stage,timeout=60000)
  for at in [.02,.5,.97]:
   result=p.evaluate('async({stage,at})=>{const v=document.querySelector("#stage"+stage);v.currentTime=v.duration*at;await new Promise((ok,no)=>{v.addEventListener("seeked",ok,{once:true});setTimeout(()=>no(Error("Seek timeout")),20000)});await v.play();await new Promise(ok=>setTimeout(ok,350));v.pause();if(v.error)throw Error(v.error.message);return{stage,at,time:v.currentTime,duration:v.duration,width:v.videoWidth,height:v.videoHeight}}',dict(stage=stage,at=at));assert result['width']==1280 and result['height']==844;playback.append(result)
 p.screenshot(path=str(O/'playback-preview.png'),full_page=True);br.close()
assert not errors,errors;(O/'playback-verification.json').write_text(json.dumps(dict(seeks=playback,errors=errors),indent=2))
archive=R/'_ART_SOURCES/draconus_modular_1111';archive.mkdir(parents=True,exist_ok=True)
for name in ['generated','references','exports','editable','reviews']:shutil.copytree(W/name,archive/name,dirs_exist_ok=True)
for p in W.iterdir():
 if p.is_file()and p.suffix in ['.py','.js','.lua','.json','.log','.txt']:shutil.copy2(p,archive/p.name)
shutil.copy2(O/'verification.json',archive/'verification.json');shutil.copy2(R/'assets/playtest_repairs_1108.js',archive/'playtest_repairs_1108.repaired.js');shutil.copy2(O/'stage8-repair-verification.json',archive/'stage8-repair-verification.json');(archive/'README.md').write_text(readme,encoding='utf-8')
doc=R/'docs/DRACONUS_MODULAR_FULL_STAGES_1111.md';doc.write_text(readme,encoding='utf-8');qa=R/'docs/qa/draconus_modular_1111';qa.mkdir(parents=True,exist_ok=True)
for p in [O/'verification.json',O/'playback-verification.json',O/'gun-verification/checks.json',O/'stage8-repair-verification.json',W/'preflight.json',W/'editable-verification.json']:shutil.copy2(p,qa/p.name)
note='''## November11,2026 - Independent Draconus rotor and full Furious stage films

Mike explicitly approved a modular Draconus gun. DGM1111 owns the fixed whole
background body, same-source foreground grips and36 static axial gun cells in
normal/Chromium, with baked material steps. Native SF1111 box/catch/stow/break,
HP, cadence and hammer recall remain owners. No runtime gun rotation. Preserve
approved ships and three-way whole-hammer banks.42 focused checks and216 exact
editable layer frames pass. Full assisted Furious Stage5–8 videos have sound,
native waves/HP/defeat and labeled invulnerable keyboard review pilot. They are
visual stress reviews, not unassisted balance clears. Each film leaves its native
source JS unchanged. The Stage8 run exposed an obsolete-host Retina getter in
PR118 flash polling; exclude target descriptors from real-pool lists.7 native
regressions pass, and Stage8 was replayed after this one-line production fix.
Broad suite retains missing difficultyHealthBaseline15 abort.
Source: _ART_SOURCES/draconus_modular_1111; docs/DRACONUS_MODULAR_FULL_STAGES_1111.md.
No game.js edit, commit, push, installer or publication.

'''.encode()
p=R/'HANDOFF_CODEX.md';old=p.read_bytes()
if b'Independent Draconus rotor and full Furious stage films'not in old:
 assert p.read_bytes()==old;p.write_bytes(note+old)
p=R/'AGENTS.md';old=p.read_bytes();exception='''

## November11 — user-approved Draconus modular gun exception

Mike explicitly requested an independently rotating modular barrel for Draconus.
For the copied Dracodia/Chronos gun only, DGM1111 supersedes SF1111's whole-held-
gun spin/firing plates: fixed complete body, same-source foreground grips and36
static axial gun cells, normal/Chromium/baked activation materials. Preserve its
actual source-alpha gun target, native independent HP/white feedback and actual
bore warning/round origin. Catch/stow/break, cadence, module lifetimes, progression
and hammer recall retain their existing owners. Do not add runtime raster gun
rotation or apply this exception to whole-hammer poses or other bosses.
See docs/DRACONUS_MODULAR_FULL_STAGES_1111.md. Full Furious Stage5–8 films are
explicitly assisted visual stress reviews, not unassisted release validation.
'''.encode('utf-8')
if b'user-approved Draconus modular gun exception'not in old:
 assert p.read_bytes()==old;p.write_bytes(old+exception)
with zipfile.ZipFile(O/'BOF-draconus-modular-sources.zip','w',zipfile.ZIP_DEFLATED,compresslevel=3)as z:
 for p in archive.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(archive))
assert all(sha(R/n)==h for n,h in installed['protected'].items())
print('Finished four complete films, verified player seeking, editable sources and handoff.',flush=True)
