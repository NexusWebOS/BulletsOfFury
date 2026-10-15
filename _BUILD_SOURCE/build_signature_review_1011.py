"""Portable review of real opening supplies, enemy signatures and Stage X."""
from pathlib import Path
from PIL import Image
import json,re,hashlib,datetime
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/previews/signature_specials_1011'
SHOTS=ROOT/'_shots/signature_specials_1011'
OUT.mkdir(parents=True,exist_ok=True)
source=(ROOT/'assets/signature_specials_1011.js').read_text(encoding='utf-8')
pilots=[dict(key=k,name=n,bonus=b) for k,n,b in re.findall(r"^ (\w+):\{name:'([^']+)',bonus:'([^']+)'\}",source,re.M)]
rebels=[dict(key=k,kind=a,name=n) for k,a,n in re.findall(r"(\w+):\{kind:'([^']+)',name:'([^']+)'\}",source.split('const FS11_REBELS=',1)[1].split('};',1)[0])]
report=json.loads((SHOTS/'report.json').read_text(encoding='utf-8'))
if report['failed'] or report['errors']:raise SystemExit('Native verification must pass before publishing the review.')
secondary=json.loads((SHOTS/'secondary-report.json').read_text(encoding='utf-8'))
if secondary['failed'] or secondary['errors']:raise SystemExit('The final focused native checks must pass.')
native_count=report['passed']+secondary['passed']
suite=(ROOT/'_shots/signature_specials_1011-suite.log').read_text(encoding='utf-8')
suite_exit=json.loads((ROOT/'_shots/signature_specials_1011-suite-exit.json').read_text())['exit_code']
if suite_exit or 'FALVA/LIZZIE BUILD OK, 0 ERRORS' not in suite:raise SystemExit('Full suite must reach its passing final summary.')
suite_count=len(re.findall(r'^  ok ',suite,re.M))
for key in [k['key']+'-'+phase for k in pilots for phase in ['incoming','base','enhanced']]+['rebel-'+k['key'] for k in rebels]+['stagex-reward','coop-start','coop-falva-helper','rebel-voss-fusion']:
    with Image.open(SHOTS/(key+'.png')) as im:im.convert('RGB').save(OUT/(key+'.webp'),quality=92)
data=dict(pilots=pilots,rebels=rebels,native=dict(passed=native_count,failed=0,errors=[]))
owners=['assets/signature_specials_1011.js','_BUILD_SOURCE/test_signature_specials_1011.cjs','_BUILD_SOURCE/probe_signature_specials_1011.py','_BUILD_SOURCE/probe_signature_secondary_1011.py','_BUILD_SOURCE/build_signature_review_1011.py','_BUILD_SOURCE/probe_signature_review_1011.py']
qa=dict(date=datetime.datetime.now(datetime.timezone.utc).isoformat(),request='Stage X enhances all nine pilot specials; enemy Rebels own their signatures; opening boxes deliver native specials.',
        owners=owners,hashes={s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in owners},
        regression=dict(passed=suite_count,failed=0,exit_code=suite_exit,final_summary='FALVA/LIZZIE BUILD OK, 0 ERRORS'),native=report,focused_native=secondary,
        scope='Protected controlled Chromium scenarios. Natural Rebel AI releases; accelerated real damage/physical death clear on the right Stage X route. Left reward gate covered in the suite.',
        resolved=['P2 pickup replaced the global P1 special: seat-owned abilities and timers now remain independent.',
                  'Atlas icon readiness needed the owning sheet, and the native fixture needed the actual pilot menu index.',
                  'Gang shields absorb a hit before hull damage; the clear now uses repeated real hits.',
                  'The map capture waits for authored assets and full live typing; its complete reward copy is159 characters.',
                  'Secondary Fusion keeps its correct single callout; attached co-op effects now use both seats in their existing render passes.'],
        git='Local only; HEAD7539951 unchanged; existing staged/unstaged/untracked work preserved.')
preview_result=SHOTS/'preview-report.json'
if preview_result.exists():
    qa['preview']=json.loads(preview_result.read_text(encoding='utf-8'))
qa_dir=ROOT/'docs/qa';qa_dir.mkdir(parents=True,exist_ok=True)
(qa_dir/'signature_specials_1011.json').write_text(json.dumps(qa,indent=2),encoding='utf-8',newline='\n')
note=f'''# 2026-10-11 - LOCAL: opening specials, Rebel signatures and earned Stage X Mk II

Mike chose enhanced specials as Stage X's additional unlock and clarified that
the fighters are the enemy Rebels. Read `docs/feedback/SIGNATURE_SPECIALS_1011.md`
and `docs/qa/signature_specials_1011.json`. One authored opening supply per seat
descends, opens through shots/contact, then delivers the actual pilot special.
Cole receives warheads. Co-op abilities/helpers/chain tier use the seat window,
and both timers tick once. Each Rebel's first personal supply carries its own
signature; existing secondary patterns, warnings and difficulty caps remain.
The actual matching Stage X boss defeat earns all-nine Signature Mk II, saved
in the profile and campaign receipt. All windows20s, distinct ability bonuses,
native name/icon HUD, visible map reward, existing supply rewards preserved.
Runtime owner: `assets/signature_specials_1011.js`, loaded last. Core game.js
untouched by this pass; test_fl.js retains CRLF. Full suite{suite_count:,}/0,
final summary, exit0; native{native_count}/0, zero browser errors. Native
clear is accelerated real Rebel damage/deaths, not a natural human victory.
Earlier co-op, atlas readiness and fixture/typing threshold issues are resolved.
Review: `docs/previews/signature_specials_1011/index.html` with all9 pilots,
all5 enemy signatures and the reward. Local only; main HEAD7539951 unchanged.

'''
marker=b'# 2026-10-11 - LOCAL: corrected Wind projectile badges and reward symbol'
heading=b'# 2026-10-11 - LOCAL: opening specials, Rebel signatures and earned Stage X Mk II'
for name in ['HANDOFF_CODEX.md','CLAUDE.md']:
    file=ROOT/name;raw=file.read_bytes()
    if heading not in raw:
        nl=b'\r\n' if raw.count(b'\r\n')>raw.count(b'\n')/2 else b'\n'
        block=note.encode('utf-8').replace(b'\n',nl)
        if marker not in raw:raise SystemExit('Current handoff marker missing: '+name)
        file.write_bytes(raw.replace(marker,block+marker,1))
(OUT/'review.json').write_text(json.dumps(data,indent=2),encoding='utf-8',newline='\n')
(OUT/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Signature specials · Bullets of Fury</title>
<style>*{box-sizing:border-box}body{margin:0;background:#090d15;color:#dce8f2;font:16px/1.5 system-ui}main{max-width:1160px;margin:auto;padding:28px}h1{color:#82e8c8;font-size:32px}h2{font-size:22px;margin-top:32px}p{max-width:880px}a{color:#88d6ff}button,select{font:inherit;padding:9px 14px;border:1px solid #456078;border-radius:6px;background:#152536;color:#edf5ff}button[aria-pressed=true]{border-color:#efc560;background:#423820}button{cursor:pointer}label{display:flex;gap:8px;align-items:center}.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:18px 0}figure{margin:0;background:#080c12;border:1px solid #30455c;border-radius:8px;overflow:hidden}figure img{display:block;width:100%;height:auto}figcaption{padding:12px 16px;color:#b9cfdf}#upgrade{background:#14232d;padding:12px 16px;border-left:3px solid #75eac4}table{width:100%;border-collapse:collapse;font-size:14px}td,th{text-align:left;padding:10px;border-bottom:1px solid #2e4053}th{color:#9adcd0}.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}.meta{color:#91adbf;font-size:14px} @media(max-width:650px){main{padding:16px}h1{font-size:25px}.pair{grid-template-columns:1fr}td,th{padding:8px}.controls label{width:100%}}</style>
<main><h1>Special supply · Signature Mk II</h1><p>The first supply box flies toward your pilot. Shoot it or meet it, then collect the released special. Beat either Stage X boss to permanently enhance all nine pilot specials. The Rebel fighters lead with their own signature attacks.</p><p><a href="../../../index.html?revision=signature-specials-1011">Play the updated game</a> · <a href="../../feedback/SIGNATURE_SPECIALS_1011.md">Implementation and checks</a></p>
<h2>Each pilot's opening pickup</h2><div class="controls"><label>Pilot <select id="pilot" aria-label="Pilot"></select></label><button class="phase" data-phase="incoming" aria-pressed="false">Incoming box</button><button class="phase" data-phase="base" aria-pressed="false">Base special</button><button class="phase" data-phase="enhanced" aria-pressed="true">Earned Mk II</button></div><p id="upgrade"></p><figure><img id="pilotShot" alt="Real game capture"><figcaption id="pilotCaption"></figcaption></figure>
<h2>Stage X reward</h2><p>Both routes earn the same permanent upgrade: Harrier Pursuit or Rebel Fury. Existing missile, life and Forge supplies are also awarded. Later special pickups use Mk II, including your next opening supply.</p><figure><img src="stagex-reward.webp" alt="Stage X signature upgrade reward in the campaign map"><figcaption>The reward after an accelerated clear through the real Rebel damage and physical death controllers.</figcaption></figure>
<h2>Enemy Rebel signatures</h2><div class="controls"><label>Enemy <select id="rebel" aria-label="Enemy Rebel"></select></label></div><figure><img id="rebelShot" alt="Real Rebel signature attack"><figcaption id="rebelCaption"></figcaption></figure><p class="meta">Their real AI collected personal supplies, charged, warned and released each special. Existing secondary attacks, shootable counters and difficulty limits remain in the encounter.</p><details><summary>Voss's secondary Fusion Cannon</summary><figure><img src="rebel-voss-fusion.webp" alt="Voss's secondary Fusion Cannon with its correct single label"><figcaption>The final focused render check verifies the secondary attack name.</figcaption></figure></details>
<h2>All nine Stage X upgrades</h2><p>Every Mk II special has a 20 second window, plus the improvement below. Axel's five-hit shield pool stays intact; Stage 6 keeps full flight speed.</p><table><thead><tr><th>Pilot</th><th>Signature Mk II</th><th>Improvement</th></tr></thead><tbody id="upgrades"></tbody></table>
<h2>Two players</h2><div class="pair"><figure><img src="coop-start.webp" alt="Independent Cole and Lizzie special supplies in co-op"><figcaption>Cole and Lizzie each keep their own pickup, ability and timer.</figcaption></figure><figure><img src="coop-falva-helper.webp" alt="Falva's authored orbiting helper attached to the second player's ship"><figcaption>The second player's attached special effects also render around their own ship.</figcaption></figure></div><p class="meta" id="checks"></p></main>
<script>let review,phase='enhanced',ready=false;const pilot=document.querySelector('#pilot'),rebel=document.querySelector('#rebel');function title(k){return k[0].toUpperCase()+k.slice(1)}function choosePilot(){const p=review.pilots.find(p=>p.key===pilot.value);document.querySelector('#pilotShot').src=p.key+'-'+phase+'.webp';document.querySelector('#pilotCaption').textContent=title(p.key)+' · '+({incoming:'Authored supply box approaching before activation',base:'Collected base signature',enhanced:p.name})[phase];document.querySelector('#upgrade').textContent=p.name+' · '+p.bonus;for(const b of document.querySelectorAll('.phase'))b.setAttribute('aria-pressed',String(b.dataset.phase===phase));}function chooseRebel(){const r=review.rebels.find(r=>r.key===rebel.value);document.querySelector('#rebelShot').src='rebel-'+r.key+'.webp';document.querySelector('#rebelCaption').textContent=title(r.key)+' · '+r.name;}fetch('review.json',{cache:'no-store'}).then(r=>r.json()).then(d=>{review=d;for(const p of d.pilots){pilot.add(new Option(title(p.key),p.key));const row=document.querySelector('#upgrades').insertRow();for(const s of [title(p.key),p.name,p.bonus])row.insertCell().textContent=s;}for(const r of d.rebels)rebel.add(new Option(title(r.key),r.key));pilot.value='cole';choosePilot();chooseRebel();ready=true;document.querySelector('#checks').textContent=d.native.passed+' native checks passed · '+d.native.failed+' failures · '+d.native.errors.length+' browser errors. Gameplay images are protected, controlled captures from real Chromium; the Stage X clear uses accelerated real damage.';});pilot.onchange=choosePilot;rebel.onchange=chooseRebel;for(const b of document.querySelectorAll('.phase'))b.onclick=()=>{phase=b.dataset.phase;choosePilot();};</script></html>''',encoding='utf-8',newline='\n')
print('Signature review: '+str(len(pilots))+' pilots, '+str(len(rebels))+' Rebels, 36 native captures')
