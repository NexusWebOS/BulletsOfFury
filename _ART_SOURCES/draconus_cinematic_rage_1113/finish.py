from pathlib import Path
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import json,hashlib,shutil,zipfile
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Draconus-new-rage';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
C=json.loads((O/'checks.json').read_text());I=json.loads((W/'installation.json').read_text());V=json.loads((O/'recording-verification.json').read_text());A=json.loads((W/'editable-verification.json').read_text());B=json.loads((W/'broad-checks.json').read_text());M=json.loads((W/'manifest.json').read_text());H=json.loads((W/'hand-socket-audit.json').read_text())
assert len(C['checks'])==27 and all(c['passed']for c in C['checks'])and not C['errors']
assert C['runtimeHash']==sha(R/'assets/draconus_cinematic_rage_1113.js')
assert all(sha(R/n)==h for n,h in I['protected'].items())
assert all(sha(R/'assets'/n)==h for n,h in I['installed'].items())
assert all(sha(R/'assets/game/shared/combat/draconus_cinematic_rage_1113'/n)==h for n,h in I['textures'].items())
assert V['complete']and V['nativeSourcesUnchanged']and not V['errors']and not V['stats']['tapErrors']and V['stats']['peak']>.001
assert all(sha(R/n)==h for n,h in V['sourceHashes'].items())
assert set(V['phases'])=={'rage','kame_fire','foreground','background','beam'}
strikes=[e for e in V['stats']['newArtEvents']if e['type']=='formation-strike'];release=[e for e in V['stats']['newArtEvents']if e['type']=='formation-release']
assert [e['index']for e in strikes]==list(range(1,27))and len(release)==1
assert A['exactFrames']==740 and not A['errors']and len(H)==5
movie=O/'draconus-new-rage-kamehameha-and-center-smash.mp4';assert sha(movie)==V['sha256']

names=[('Chromium: center ground contact','chrome-new-center-ground-contact.png'),('Both hands cup the energy ball','new-two-hand-gather-foreground.png'),('Both palms thrust and sustain the wave','new-two-hand-wave-foreground.png')]
board=Image.new('RGB',(750*3,750),'#10202b');draw=ImageDraw.Draw(board)
for i,(label,name)in enumerate(names):
 im=Image.open(O/name).convert('RGB').crop((265,70,1015,780));board.paste(im,(i*750,40));draw.text((i*750+16,12),label,fill='white')
board.save(O/'visual-proof.png')

page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Draconus: new rage and center smash</title><style>body{max-width:1280px;margin:24px auto;padding:0 18px;background:#101820;color:#edf5ff;font:17px/1.5 system-ui}h1{font-size:28px}video,img{width:100%;background:#05090e}button{font:inherit;margin:6px;padding:9px;background:#d9edff;color:#102131;border:0;border-radius:3px;cursor:pointer}button:focus-visible{outline:3px solid #ffe16c}a{color:#91d9ff}small{display:block;margin:14px 0}</style><h1>Draconus: new rage and center smash</h1><p>New whole-character frames show his STOP/recoup, red rage transformation, two-handed hip-level energy-ball gather, forward thrust and sustained red wave. The center smash now takes the rigid hammer overhead and down onto its cap directly in front, including Chromium armor.</p><video id="v" controls preload="metadata" src="draconus-new-rage-kamehameha-and-center-smash.mp4"></video><div id="chapters"></div><small>Recorded in the updated game on Furious, with native sound and complete rage attacks. Prepared checkpoints and an invulnerable observer; this is not a full-stage or unassisted balance clear.</small><h2>Hand and hammer alignment</h2><img src="visual-proof.png" alt="New Chromium center contact, two-handed gather and forward wave"><p><a href="README.md">Changes and verification</a> · <a href="BOF-Draconus-new-rage-sources.zip">Editable frames and recovery sources</a></p><script>const rows=CHAPTERS,v=document.querySelector('#v');for(const c of rows){const b=document.createElement('button');b.textContent=c.label;b.onclick=()=>{v.currentTime=c.at;v.play()};document.querySelector('#chapters').append(b)}</script></html>'''.replace('CHAPTERS',json.dumps(V['chapters']))
(O/'playback.html').write_text(page,encoding='utf-8')
seeks=[];errors=[]
with sync_playwright()as pw:
 br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1400,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.goto((O/'playback.html').as_uri());p.wait_for_function('()=>{const v=document.querySelector("#v"),im=document.querySelector("img");return v.readyState>=1&&Number.isFinite(v.duration)&&im.complete&&im.naturalWidth>0}',timeout=30000)
 for t in [.04,.24,.43,.65,.82,.96]:
  q=p.evaluate('''async t=>{const v=document.querySelector('#v');v.currentTime=v.duration*t;await new Promise((ok,no)=>{v.addEventListener('seeked',ok,{once:true});setTimeout(()=>no(Error('Seek timeout')),15000)});await v.play();await new Promise(ok=>setTimeout(ok,180));v.pause();if(v.error)throw Error(v.error.message);return{seconds:v.currentTime,width:v.videoWidth,height:v.videoHeight}}''',t);assert q['width']==1280 and q['height']==844;seeks.append(q)
 p.locator('#chapters button').filter(has_text='Rage transformation').click();p.wait_for_timeout(250);q=p.evaluate('()=>{const v=document.querySelector("#v");return{at:v.currentTime,paused:v.paused}}');assert not q['paused'];p.evaluate('document.querySelector("#v").pause()');p.screenshot(path=str(O/'playback-preview.png'),full_page=True);br.close()
assert not errors;(O/'playback-verification.json').write_text(json.dumps(dict(seeks=seeks,chapterButton=q,errors=errors),indent=2))

source=R/'_ART_SOURCES/draconus_cinematic_rage_1113';source.mkdir(exist_ok=True)
for dirname in ['generated','references']:shutil.copytree(W/dirname,source/dirname,dirs_exist_ok=True)
for file in W.iterdir():
 if file.is_file()and file.suffix in ['.py','.js','.lua','.json','.log','.md']:shutil.copy2(file,source/file.name)
ex=source/'exports';ex.mkdir(exist_ok=True)
for file in(W/'exports').iterdir():
 if file.is_file()and file.suffix in ['.aseprite','.webp']:shutil.copy2(file,ex/file.name)
sources={str(p.relative_to(source)).replace('\\','/'):sha(p)for p in source.rglob('*')if p.is_file()};(source/'source-hashes.json').write_text(json.dumps(sources,indent=2))

readme=f'''# Draconus generated rage, two-handed Kamehameha and center smash — November13,2026

Mike rejected the reused open-palm casting and requested proper new Draconus rage frames matching Stage5 Chronus's transformation and two-handed attack, plus a real directly-ahead Chromium hammer slam. This pass generates63 usable complete character drawings:16 STOP/recoup,16 transformation,16 hip-gather/thrust/recovery and15 usable center hammer poses. The duplicate-weapon source13 is rejected. The new center bank has32 timing cells across all materials; formation also has32 timing cells. The casting bank has16 real poses in foreground and separately prepared background sizes. These are whole character-and-held-weapon drawings, never body/weapon assembly or pose interpolation. The original highest-detail selected PNGs remain in generated/; every normalized actor uses the same 1:1 import scale and registered512px canvas/pivot[256,256]/baseline410. The smaller casting variant is exported directly from the master. Twelve generated round energy-ball poses expand and pulse across16 timing cells; four clipped raw orb frames are rejected.

The Chromium center bank now has a real T-shaped rigid metal head/shaft through the overhead arc, lowering on the centerline onto its cap below the hands, then lifting and regripping. Native root, target, hit, sound, count and once-per-stroke owners consume its new actual alpha mask and cap landmarks. Normal/Chromium/red/hit materials share identical geometry. Left/right diagonal smashes and intentional whirlwind turns keep their owners.

Draconus now throws the held weapon through his existing owner, shows his own raised STOP palm and exhausted recoup, compresses into a strength-gathering stance, rises and roars in red metal. Stage5's original c45Aura/cgSwirl/cgBolt geometry and pixels are baked offline around the new Draconus frames, including front/back rising red electrical arcs, silhouette flame aura, the original26 accelerating scatter/closing-in strike schedule and one final center release with the original CF50 hot rings and gradual scenery dimming. Native Draconus cues and the shared mixer remain. The copied effects are prepared on a genuinely transparent authoring canvas; opaque first-pass exports were rejected before final recording. No new raster transforms or effect manufacture are added to gameplay.

The wave now uses a genuine two-handed hip gather, visible round ball in the actual hollow between both hands, torso/hip untwist, both palms thrusting toward the viewer, sustained hold and recovery. The five gather sockets are measured against actual transparent hand gaps, not just labels. The release origin is centered between the forward palms. Foreground and background socket metadata drives both native collision/warnings and the visible ball/beam. The red beam uses the exact original Chronus wave source/palette, prepared at the copied boss's native background distance. The separate round energy ball is newly generated to match its red/white palette. The existing palm-volley gestures retain their timing/rounds and original non-matte RGB pixels; identified magenta generation matte is removed and white hit art is rebuilt against the same cleaned alpha.

The earlier low-health action-boundary rage fix and full finite cycle3 book remain: opening wave, all foreground palms, all background palms and repeat charged wave, then native return. There is no HP healing, copied-form clock reset or restoration of defeated weapon pools. Original Stage5 C45/C46/C47/CF48/CF49/CF50 files, game.js, ships, independent modular gun and earlier recovery owners remain byte-identical.

{len(C['checks'])} focused native checks pass, with no page/update/draw errors. They include the real Chromium activation followed by actual centered impact below the hands; broad vertical centerline travel; both armor materials/all directions and all four Furious contacts; real native damage/white feedback/expiry; measured cap/warning agreement; real low-health rage commitment; complete native rage cycles, round counts and finite return; no healing or weapon restoration; retained modular gun; both casting depths and actual hand/release sockets. Five additional pixel-gap measurements confirm the ball is inside the cupped hands. {A['exactFrames']} Aseprite frame/material/effect exports across{A['banks']} banks roundtrip pixel-exactly. This count includes materials, prepared effects, timed repeats and retained palm gestures; it is not a count of new character drawings.

The final{float(V['media']['format']['duration']):.1f}-second Furious recording contains decoded H264/AAC sound, all five native rage phase markers, exactly26 new visible strike events and one release, complete foreground/background volleys and repeat wave, source-hash continuity and no runtime errors. Six playback seeks and the actual rage chapter button pass. It uses prepared checkpoints and an invulnerable observer, not a full-stage or unassisted balance clear. Earlier full-stage films and Draconus previews predate this change. Open playback.html for chapter buttons and visual-proof.png for lossless native alignment shots.

Required syntax checks pass. The full test_fl.js suite still exits1 before its final summary on the existing missing difficultyHealthBaseline15 helper at assets/combat_polish_0927b.js:151. Exact output is preserved in full-suite.log; this is not release certification.

Production integration adds assets/draconus_cinematic_rage_art_1113.js and assets/draconus_cinematic_rage_1113.js at the end of index.html, plus textures in assets/game/shared/combat/draconus_cinematic_rage_1113. Existing source art/owners are preserved; the late registration replaces only the copied boss's center bank and requested rage presentation. Native HP, input, shot, destruction, sound and progression owners remain. No commit, push, installer or publication.

Generated with the built-in image tool; PixelLab credits were not used. Prompt briefs and rejected candidates are retained in PROMPTS.md. For the existing project, rebuild in order: artprep.py, build.py, bake.py, effect_sizes.py, clean_palms.py, ball_export.py, final_sockets.py, author.py, install.py, prepare_checks.py/verify.py, prepare_record.py/record.py, finish.py. Python/Pillow/numpy/scipy/Playwright, the existing native review helpers and this machine's source-built Aseprite are required. The source package is a patch for the existing game, not a standalone game or bundled Aseprite installer.
'''
for p in[O/'README.md',source/'README.md',R/'docs/DRACONUS_CINEMATIC_RAGE_1113.md']:p.write_text(readme,encoding='utf-8')
summary=dict(nativeChecks=27,editable=A,sourceHashes=V['sourceHashes'],filmSha256=V['sha256'],seconds=V['media']['format']['duration'],phases=V['phases'],strikes=len(strikes),releases=len(release),pixelHandSockets=H,playbackSeeks=len(seeks),errors=errors,broad=B,protected=I['protected'],newWholeCharacterDrawings=63,newEnergyOrbDrawings=12)
(O/'verification.json').write_text(json.dumps(summary,indent=2));qa=R/'docs/qa/draconus_cinematic_rage_1113';qa.mkdir(parents=True,exist_ok=True)
for p in[O/'checks.json',O/'verification.json',O/'playback-verification.json',W/'editable-verification.json',W/'hand-socket-audit.json',W/'broad-checks.json',W/'full-suite.log']:shutil.copy2(p,qa/p.name)
note='''## November13,2026 — New Draconus rage/Kamehameha and actual center cap slam

Mike rejected reused open-palm casting and the copied Chromium center hit.
DCR13 supplies63 usable NEW whole-character drawings: STOP/recoup, strength
compression/red release, hip-level two-hand ball gather, forward double-palm
thrust/hold/recovery and a rigid T-shaped hammer's center overhead/ground arc.
The duplicate-head source13 is rejected.32-cell center/formation timelines,
16-pose casts at both depths; a newly generated ROUND red/white energy ball.
The ball is measured inside the actual cupped-hand gap; release is between
forward palms. Original Stage5 aura/swirl/bolt pixels are baked transparently;
26 original accelerating scatter strikes, hot rings/dimming and exact red wave.
Retained palm-volley matte is cleaned without changing non-matte RGB/rounds.
Stage5's original C45/C46/C47/CF48/CF49/CF50 and all protected owner files remain.
27 native checks pass;740 Aseprite frame/material/effect exports are exact.
Actual continuous audible Furious preview completes both center materials and
the native full rage book,26 strikes/one release, no healing/restored weapons.
Six seeks and rage chapter pass. Prepared checkpoints/invulnerable observer;
earlier full-stage films predate this art. Broad suite keeps its existing health
helper abort. No game.js edit, commit, push, installer or publication.
Docs: docs/DRACONUS_CINEMATIC_RAGE_1113.md; _ART_SOURCES/draconus_cinematic_rage_1113.

'''
p=R/'HANDOFF_CODEX.md';old=p.read_bytes();heading=note.splitlines()[0].encode('utf-8')
if heading not in old:assert p.read_bytes()==old;p.write_bytes(note.encode('utf-8')+old)
rule='''

## November13 — generated Draconus rage and center hammer replacement

Mike requires Draconus's OWN new rage frames with Stage5 Chronus's transformation
effects and actual two-handed hip-gather/Kamehameha thrust/hold/recovery. DCR13
supersedes reused RF1110 open-palm casting and the old center overhead geometry.
Preserve the new STOP/recoup, red strength poses, measured hollow hand sockets,
double-palm release, transparent baked original Stage5 aura/swirl/26-strike/ring
presentation and original red wave. Do not restore pink generation matte or
opaque effect backgrounds. Center cap impacts must fall directly in front below
both hands in normal/Chromium; keep one rigid T head/shaft. Source13 duplicate
weapon and clipped orb sources12–15 are rejected. Existing diagonal and whirlwind
owners, native damage/flash/HP/rounds, ships/guns and full finite rage book remain.
Stage5 original C45/C46/C47/CF48/CF49/CF50 still must remain untouched. New poses
are whole authored actors, never body/held-weapon assembly or runtime rotation.
Evidence/rebuild: docs/DRACONUS_CINEMATIC_RAGE_1113.md.
'''
p=R/'AGENTS.md';old=p.read_bytes()
if rule.splitlines()[2].encode('utf-8')not in old:assert p.read_bytes()==old;p.write_bytes(old+rule.encode('utf-8'))
with zipfile.ZipFile(O/'BOF-Draconus-new-rage-sources.zip','w',zipfile.ZIP_DEFLATED,compresslevel=3)as z:
 for p in source.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(source))
assert all(sha(R/n)==h for n,h in I['protected'].items())
print('Saved final preview/player,63 new character poses,740 exact editable frames and complete recovery handoff.',flush=True)
