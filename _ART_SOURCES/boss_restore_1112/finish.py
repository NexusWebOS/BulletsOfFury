from pathlib import Path
import json,shutil,hashlib,zipfile,html
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Recovered-boss-animations';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=json.loads((O/'checks.json').read_text());installation=json.loads((W/'installation.json').read_text());recordings=json.loads((O/'recording-verification.json').read_text());broad=json.loads((W/'broad-checks.json').read_text());M=json.loads((W/'manifest.json').read_text())
assert all(c['passed']for c in checks['checks'])and not checks['errors']and checks['runtimeHash']==sha(R/'assets/boss_restore_1112.js')
assert recordings['nativeSourcesUnchanged']and all(r['complete']and not r['errors']and r['stats']['peak']>.001 for r in recordings['reports'])
assert all(sha(R/n)==h for n,h in installation['protected'].items())
for n in ['boss_restore_1112.js','boss_restore_art_1112.js']:assert sha(W/n)==sha(R/'assets'/n)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Recovered boss animations</title><style>body{max-width:1320px;margin:24px auto;padding:0 18px;background:#101820;color:#edf5ff;font:17px/1.5 system-ui}h1{font-size:28px}h2{font-size:22px}video{width:100%;background:#05090e}article{margin:24px 0;padding:18px;background:#192432;border:1px solid #3d4b5d}button{font:inherit;margin:8px;padding:8px}a{color:#91d9ff}img{max-width:100%}</style><h1>Recovered hammer sweeps and original Chronus rage</h1><p>The earlier complete sideways-sweep poses are restored for both bosses, normal and Chromium. Chronus uses his original hammer throw, STOP/recoup, power stance, lightning transformation and Kamehameha charge/thrust/blast/return.</p><p>These are native animation checkpoints with an invulnerable observer, with real sound. They demonstrate the restored build and are not full-fight clears.</p><article><h2>Chronus — both armor forms, original rage and Kamehameha</h2><video id="stage5" controls preload="metadata" src="chronus-restored-rage-and-swings.mp4"></video><div id="chapters5"></div></article><article><h2>Draconus — left and right sweeps, both armor forms</h2><video id="stage8" controls preload="metadata" src="draconus-restored-side-swings.mp4"></video><div id="chapters8"></div></article><p><a href="BOF-recovered-boss-animation-sources.zip">Recovery sources and registration</a> · <a href="README.md">Changes and verification</a> · <a href="checks.json">Native checks</a></p><script>const chapters=CHAPTERS;for(const [stage,rows]of Object.entries(chapters)){const v=document.querySelector('#stage'+stage),box=document.querySelector('#chapters'+stage);for(const row of rows){const b=document.createElement('button');b.textContent=row.label;b.onclick=()=>{v.currentTime=row.at;v.play()};box.append(b)}v.addEventListener('play',()=>document.querySelectorAll('video').forEach(o=>{if(o!==v)o.pause()}))}</script></html>'''.replace('CHAPTERS',json.dumps({str(r['stage']):r['chapters']for r in recordings['reports']}))
(O/'playback.html').write_text(page,encoding='utf-8');errors=[];seeks=[]
with sync_playwright()as pw:
 br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1400,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.goto((O/'playback.html').as_uri())
 for stage in [5,8]:
  p.wait_for_function('s=>{const v=document.querySelector("#stage"+s);return v.readyState>=1&&Number.isFinite(v.duration)}',arg=stage,timeout=30000)
  for at in [.05,.5,.94]:
   q=p.evaluate('''async({stage,at})=>{const v=document.querySelector('#stage'+stage);v.currentTime=v.duration*at;await new Promise((ok,no)=>{v.addEventListener('seeked',ok,{once:true});setTimeout(()=>no(Error('Video seek timeout')),15000)});await v.play();await new Promise(ok=>setTimeout(ok,200));v.pause();if(v.error)throw Error(v.error.message);return{stage,at,seconds:v.currentTime,duration:v.duration,width:v.videoWidth,height:v.videoHeight}}''',dict(stage=stage,at=at));assert q['width']==1280 and q['height']==844;seeks.append(q)
 p.screenshot(path=str(O/'playback-preview.png'),full_page=True);br.close()
assert not errors;(O/'playback-verification.json').write_text(json.dumps(dict(seeks=seeks,errors=errors),indent=2))
archive=R/'_ART_SOURCES/boss_restore_1112';archive.mkdir(exist_ok=True);E=archive/'exports';E.mkdir(exist_ok=True)
sources=[]
for n,a in M['banks'].items():
 for mat in ['regular','chrome','red','hit','red_hit']:
  p=R/f'assets/game/shared/combat/{a["folder"]}/{n}_{mat}.webp';shutil.copy2(p,E/p.name);sources.append(dict(bank=n,material=mat,path=str(p.relative_to(R)),sha256=sha(p)))
legacy=['chronos_rageform_1026.js','chronos_kamehameha_1026.js','chronos_kame_1025.js','chronos_rage_presentation_1026.js','chronos_energy_audio_1026.js','chronos_lightning_audio_1026.js']
L=archive/'legacy-owners';L.mkdir(exist_ok=True)
for n in legacy:shutil.copy2(R/'assets'/n,L/n)
for p in W.iterdir():
 if p.is_file()and p.suffix in ['.py','.js','.json','.log']:shutil.copy2(p,archive/p.name)
(archive/'source-hashes.json').write_text(json.dumps(sources,indent=2));shutil.copy2(O/'checks.json',archive/'native-checks.json')
readme=f'''# Recovered sideways hammer poses and original Chronus rage — November12,2026

Mike rejected the later sideways poses and specifically requested recovery of earlier working attacks, plus the original Stage5 rage formation and Kamehameha. The two full16-pose blue side banks and original corrupted side sheet were recovered from boss_strike_1109b. The corrupted sheet already contains two eight-pose directional sweeps: sources0–7 for left,8–15 for right. They are registered as separate16-cell timelines with deliberate contact/follow-through holds. Source5 is the fully extended left contact; source12 is the fully extended right contact. The first attempted mapping put the second windup at impact; visual review caught it, and the final mapping/previews replace it. The recovered poses use regular, Chromium, red and matching hit materials. All visible RGBA pixels and alpha match the exact original cells; transparent RGB is ignored by the lossless exporter. No body/weapon assembly, interpolation or replacement generated artwork is added. The original576px cells/pivot[288,288], alpha masks, material variants and head landmarks are used directly. Original editable Aseprite sources remain at _ART_SOURCES/boss_strike_1109b; directional registration is reproducible from build.py. Earlier17-frame HA21 banks and later whole/heavy/front candidates were inspected before selecting the recovered full-body sweeps.

boss_restore_art_1112.js loads after the current overhead metadata and before boss_animation_1109.js registers atlas cells. It replaces only the four side banks. boss_restore_1112.js matches recovered contact frame8 to the native hit moments, retaining native impact counts and full authored follow-through/recovery. A small floating-point tolerance prevents a native right-hand contact from rounding back to frame7. Center/right/left ground-smash banks, whirlwind, ships, separate thrown hammer, pickups and modular guns remain protected.

Stage5's original C45/C46/C47/CF48/CF49/CF50 render, pose, hand-socket, glow, sound and transformation owners are restored through their existing saved functions. The later RF1110 replacement no longer intercepts Stage5 rage artwork or adds a second strike schedule. The original hammer throw, raised-palm STOP/recoup, planted charge,26 accelerating lightning strikes, red arms-out release, scenery dimming, remaining-HP red gauge, depth flight, strafe, gather, two-handed thrust, large wave, recovery and foreground return run again. The original charge/release/wave audio and its native mix remain. Original reel and STOP art preload at Stage5 entry. Existing legacy presentation methods are restored unchanged; no new effect family is generated. Draconus's separate RF1110 rage and modular-gun owners stay active.

{len(checks['checks'])} focused native checks pass with no page/update/draw errors. They include actual fully extended original source poses at both native side contacts for both characters/materials, full authored cycles with broad physical head travel, source-alpha landmarks, exact original-cell exports, all three ground-smash directions with four Furious contacts/planted clearance/native FOV agreement, previous-grip continuity, original transformation protection, exactly26 strikes/one final release, actual old body-frame draws, the complete native Kamehameha phase sequence and original audio roles, and retained Draconus gun HP/selection. Each blue swing retains16 distinct poses; the corrupted left/right sweeps retain8 distinct poses each across16 timing cells. Both short checkpoint videos contain decoded H264/AAC sound and finish through their real native controllers; six player seeks pass. They use an invulnerable observer and prepared attack checkpoints, not full-fight or unassisted balance claims. Earlier full-stage films predate this restored presentation.

Required syntax checks pass. The full test_fl.js suite still exits1 before its summary on the existing missing difficultyHealthBaseline15 helper at assets/combat_polish_0927b.js:151. Exact output is in broad-checks.json/full-suite.log. No game.js or old owner-file rewrite, commit, push, installer or publication. The source package is a recovery patch for the existing game, not a standalone game build.

Open playback.html for the actual restored-build previews and chapter buttons. Chronus: original transformation/wave plus normal/Chromium sweeps. Draconus: both directional sweeps in normal/Chromium. Canonical game names remain Chronos and Dracodia. Source hashes, bank metadata and restoration scripts are retained in _ART_SOURCES/boss_restore_1112.
'''
for p in [O/'README.md',archive/'README.md',R/'docs/BOSS_ANIMATION_RECOVERY_1112.md']:p.write_text(readme,encoding='utf-8')
summary=dict(checks=len(checks['checks']),errors=checks['errors'],broad=broad,sourceHashes=sources,runtime=checks['runtimeHash'],protected=installation['protected'],playbackSeeks=len(seeks),films=[dict(stage=r['stage'],seconds=r['media']['format']['duration'],sha256=r['sha256'],assistance=r['setup']['assistance'])for r in recordings['reports']]);(O/'verification.json').write_text(json.dumps(summary,indent=2))
qa=R/'docs/qa/boss_restore_1112';qa.mkdir(parents=True,exist_ok=True)
for p in [O/'checks.json',O/'verification.json',O/'playback-verification.json',W/'broad-checks.json',W/'full-suite.log']:shutil.copy2(p,qa/p.name)
note=f'''## November12,2026 — Recovered sideways sweeps and original Chronos rage/wave

Mike rejected the later side poses and explicitly requested recovery, including
the original Stage5 rage formation and Kamehameha. BR1112 restores the full
boss_strike_1109b sideways sweeps in both characters/materials. Dracodia's original
sheet contains both directions: source5/12 are the fully extended left/right
contacts, each within its own eight-pose sweep. Timeline frame8 follows native hit
clocks; overhead directions/current ships/modular guns retain their owners.
Stage5 restores C45/C46/C47/CF48/CF49/CF50 through saved pre-RF1110 functions:
throw/STOP/charge/26 strikes/release, original gather/thrust/wave/return and sound.
Do not replace these Stage5 animations with RF1110 again. Draconus RF1110 stays.
{len(checks['checks'])} focused native checks pass, no renderer errors; two short audible native
checkpoint films and6 playback seeks pass. Full suite retains its existing
difficultyHealthBaseline15 abort. No game.js/old owner edits, commit or installer.
Docs: docs/BOSS_ANIMATION_RECOVERY_1112.md; sources _ART_SOURCES/boss_restore_1112.

'''.encode('utf-8')
p=R/'HANDOFF_CODEX.md';old=p.read_bytes()
heading='## November12,2026 — Recovered sideways sweeps and original Chronos rage/wave'.encode('utf-8')
if heading in old:
 start=old.index(heading);end=old.find(b'\n## ',start+len(heading));end=len(old)if end<0 else end+1
 updated=old[:start]+note+old[end:]
else:updated=note+old
assert p.read_bytes()==old;p.write_bytes(updated)
p=R/'AGENTS.md';old=p.read_bytes();rule='''

## November12 — recovered side attacks and critical original Stage5 rage

Mike explicitly rejected the FH1111/HA1111 sideways drawings. BR1112 now restores
the earlier boss_strike_1109b full side sweeps for both bosses, normal/Chromium.
The original corrupted sheet contains two sweeps; source5/12 are the fully
extended left/right contacts, registered at timeline frame8. Preserve those and
native counts/recovery. This supersedes prior side-bank preservation notes only.
Mike also explicitly requires Stage5 Chronos's original rage formation and
Kamehameha: C45/C46/C47/CF48/CF49/CF50 keep the throw, STOP/recoup, stance,26 strikes,
red release, original gather/thrust/wave/depth return and sound. RF1110 must not
intercept those Stage5 animations again. Keep Draconus RF1110, new ship forms,
all current ground-smash directions and both modular guns. Read
docs/BOSS_ANIMATION_RECOVERY_1112.md before changing these restored routes.
'''.encode('utf-8')
heading='## November12 — recovered side attacks and critical original Stage5 rage'.encode('utf-8')
if heading in old:
 start=old.index(heading);end=old.find(b'\n## ',start+len(heading));end=len(old)if end<0 else end+1
 updated=old[:start]+rule.lstrip()+old[end:]
else:updated=old+rule
assert p.read_bytes()==old;p.write_bytes(updated)
with zipfile.ZipFile(O/'BOF-recovered-boss-animation-sources.zip','w',zipfile.ZIP_DEFLATED,compresslevel=3)as z:
 for p in archive.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(archive))
assert all(sha(R/n)==h for n,h in installation['protected'].items())
print('Recovered animations installed,56 native checks and6 video seeks passed; source archive and handoff saved.',flush=True)
