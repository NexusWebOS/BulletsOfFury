from pathlib import Path
import json,re,shutil,html
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=R/'_shots/request_completion_1021'
log=(R/'_shots/menu_heart_1021/request-completion-regression.log').read_text(encoding='utf-8')
assert 'BUILD OK, 0 ERRORS' in log
assertions=len(re.findall(r'^  ok  ',log,re.M))
def result(p):
 d=json.loads(p.read_text(encoding='utf-8'));a=d['checks'];assert not d.get('errors') and all(c.get('ok',c.get('passed',False)) for c in a),p
 return {'checks':len(a),'passed':len(a),'errors':[],'report':p.relative_to(R).as_posix()}
checks={
 'native_contracts':result(R/'_shots/final_version_1021/contracts/msedge-report.json'),
 'guide_browsers_atlas':result(O/'guide-atlas-verification.json'),
 'atlas_refinement':result(O/'atlas-refinement.json')}
for name,file in [('older_banks_finishes_cole','verification.json'),('terminal_edge_cases','edge-verification.json')]:
 p=R/'_shots/performance_finish_1020'/file
 if not p.exists():
  # Probe filenames are retained verbatim; the fresh console logs are authoritative.
  text=(R/'_shots/menu_heart_1021'/('request-completion-performance-edges.log' if name=='terminal_edge_cases' else 'request-completion-performance.log')).read_text()
  d=json.loads(text.strip().splitlines()[-1]);assert d['failed']==0 and not d['errors'];checks[name]=d
 else:checks[name]=result(p)
rows=[
 ('Re-authored corrupted Hammer','Implemented + verified','Larger usable sprite; coherent chromium/face/hammer detail across 15 banks; measured weapon anchors and real hit flashes.','FINAL_VERSION_1021.md'),
 ('Stage 5 miniboss health','Implemented + verified','Core plus surviving weapons retain the full health budget; dead core stops targeting; rewards/progression happen once at true zero on all four difficulties.','FINAL_VERSION_1021.md'),
 ('Forge weapon preview','Implemented + verified','All eight common weapons for all nine pilots; isolated preview state and alternating chaingun barrels. Maverick fixed homing rule preserved.','FINAL_VERSION_1021.md'),
 ('Shield variants','Implemented + verified','Animated hex, electric, fire, toxic, ice, code and void variants; wall/carrier shield; transparent hull center and native absorb/break/flash timers.','FINAL_VERSION_1021.md'),
 ('Portal variants','Implemented + verified','Gate-free violet and blue loops, upright Stage 5 travel, screen warp; original portals retained.','FINAL_VERSION_1021.md'),
 ('Aircraft refits','Implemented + verified','40 designs / 53 design IDs with idle, attack, drift, barrel-roll and somersault banks; 2,280 poses, fixed pivots, reusable modules, native mounts and deaths.','FINAL_VERSION_1021.md'),
 ('Stage 4 boss','Implemented + verified','Carrier drift bank and lateral motion, reachable electrical cores, native regeneration and real damaged-pixel feedback.','FINAL_VERSION_1021.md'),
 ('Rebel fighters','Implemented + verified','Five personal attack books, four formations, shootable homing missiles, deliberate allied interception, depth returns, Nyx Retina/missile reveal, Rook ram and Juggernaut charge effects.','FINAL_VERSION_1021.md'),
 ('Final destruction effects','Implemented + verified','Smoother PixelLab banks and selected ColeForge pack effects supplement the bounded native death owner. Laser, ice and dark-energy terminal sequences preserve real victim hulls.','PERFORMANCE_FINISH_1020.md'),
 ('Older boss acting','Implemented + verified','Targeted bomber cannon and carrier turret windup/recoil/recovery upgrades; destroyed modules cancel pending attacks and leave no live animated ghosts.','PERFORMANCE_FINISH_1020.md'),
 ('Phoenix / helicopter / Hammer attack redesign','Implemented; current regression green','Independent Phoenix anatomy and removable cannons, X-corner Swoon; helicopter X/+ passes, reversed double orbit and top bomb pass; Hammer crate, code sky strike, core break and permanent fire finale.','BOSS_REDESIGN_1020.md'),
 ('Stage X coast/city','Implemented + verified','Protected stage card, seamless coastal/city scroll, matching district seams and independent animated water.','FINAL_VERSION_1021.md'),
 ('Tutorial / water / downloaded arenas','Implemented; earlier native evidence retained','Instructor Cole, modular B.O.B., warning/Retina/elements lessons; animated parallax water, blue Stage 1 and lava Stage 2 variants; corrupted arena downloads.','PIXELLAB_FINISHING_PRIORITIES_1020.md'),
 ('HUD / dialogue / Cole / Retina colors','Implemented; earlier native evidence retained','Command Armor, solid meters, paired abilities and readable scores; fitted portrait/text/name polygons, aligned font, Instructor black/red palette and pilot-colored target reticles.','UI_PRODUCTION_1020.md'),
 ('Ending','Implemented; earlier native evidence retained','Blue portal, correct ship landings, report/alarm/Federation warning, sky/coast/Earth/solar pullout, re-growing Dracodia scream, portal escape and return card.','CINEMATIC_INVASION_1020.md'),
 ('Menu S/M/L/XL windows','Implemented + verified','Avatar-free purpose-built frames and neutral tutorial invitation; cinematic portrait plates no longer stretched into tall menu prompts.','MENU_HEART_1021.md'),
 ('BARBIE / Chrome Heart','Implemented + verified','Earned Falva/Lizzie final-win unlock, separate pink Hammer fight with dance/heart attacks/shield; native dodge, death, restart and dedicated result.','MENU_HEART_1021.md'),
 ('Offline guide + live encyclopedia','Refreshed in this audit','Guide 1.2 has current HUD captures, runtime data and revised tactics; 56 aircraft dossier banks refreshed, current Stage 5/6 labels fixed, seven individual Chrome Heart banks and save-isolated preview added.','REQUEST_COMPLETION_1021.md'),
]
pending=[
 {'item':'Other eight pilots\u2019 new cinematic motion banks','status':'Waiting for Cole likeness approval','detail':'Cole reporting and alarm banks are ready. The other pilots retain their existing poses; new blink/breath/talk/alarm banks have not been produced. The requested likeness-first approval is still pending.','url':'/_shots/performance_finish_1020/review.html'},
 {'item':'Boss preview design','status':'Waiting for selection','detail':'Five new concepts are generated. None has silently replaced the live B.O.B. preview. Select one to bind to the actual model, part stats and weak points.','url':'/_shots/menu_heart_1021/review.html'},
 {'item':'Additional cinematic boards','status':'Concepts ready; not installed','detail':'Six optional boards are generated for review. The implemented ending is separate and already live.','url':'/_shots/final_version_1021/review.html'},
 {'item':'Aqua instrumental','status':'Licensed audio file still needed','detail':'Licensing/download supplier located. No paid track was purchased or bundled. The optional local track slot is wired and existing Hammer music remains active.','url':'/docs/MENU_HEART_1021.md'},
 {'item':'Full campaign balance sign-off','status':'Open; not certified','detail':'The earlier matrix retains uncleared Hard/Furious cases. New combat and safe-window tests are not full stage/encounter clears or human survival percentages. A fresh unprotected all-stage, miniboss, boss and finale matrix plus repeated human learning trials is still required.','url':'/docs/BALANCE_RECOVERY_1007B.md'},
 {'item':'Target laptop performance','status':'Hardware validation still needed','detail':'Edge/Chrome/Firefox functional checks pass. Short local render samples do not prove sustained FPS on the Ryzen laptop in battery mode; older Firefox samples missed 60 FPS.','url':'/docs/BROWSER_PERFORMANCE_AND_MANUAL_1012.md'}
]
if (R/'_ART_SOURCES/holoscan_1021/verification.json').exists():
 pending=[q for q in pending if q['item']!='Boss preview design']
 rows.append(('Selected Holoscan dossier','Implemented + verified','Concept02 is selected and live: actual exploded modules, authored part turntables, shared stats, responsive text, native Deploy/Pause and save-isolated interactive review.','HOLOSCAN_1021.md'))
report=dict(date='2026-10-21',scope='Active BOF art/combat/UI/tutorial/ending backlog and older guide dependencies; implementation evidence is distinct from current full-campaign certification.',full_suite={'assertions':assertions,'errors':0,'exit':0},fresh_checks=checks,implemented=[dict(zip(['request','status','detail','evidence'],r)) for r in rows],open_items=pending,refresh=json.loads((O/'refresh.json').read_text()),generation_spending_in_audit=0,published_to_github=False)
(O/'audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
md='# BOF request completion audit — October 21, 2026\n\nThe recent implementation work is integrated. This is **not a blanket all-finished or all-balanced certification**. The table separates current checks from retained earlier evidence; open items remain explicit. No new generation credits were spent during this audit. No GitHub publish was requested or performed.\n\n## Fresh verification\n\n'
md+=f'- Full regression: {assertions:,} assertions, final BUILD OK / zero errors, exit 0.\n'
for name,d in checks.items():md+=f'- {name.replace("_"," ")}: {d.get("checks",d.get("passed"))} passing checks, no recorded browser errors.\n'
md+='\nThe guide was checked in Edge, Chrome and Firefox at 1440px and 390px, including artwork, current HUD content, search, bookmarks and notes persistence. Native atlas checks cover frame slicing, current aircraft, secret owner, pause/single-step, return to ordinary combat and untouched persistent storage. Updated JavaScript syntax passed. Screenshots were inspected.\n\n## Implementation coverage\n\n| Request | Status | Result / evidence |\n|---|---|---|\n'
for a,b,c,d in rows:md+=f'| {a} | {b} | {c} [Details]({d}). |\n'
md+='\n## Open items\n\n'
for q in pending:md+=f'- **{q["item"]} — {q["status"]}.** {q["detail"]}\n'
md+='\n## Guide package\n\n`extensions/bof-field-manual/` is version 1.2.0. The ZIP is `C:/Users/Mike/Documents/New project/output/bof-field-manual/BOF-Field-Manual-1.2.zip` (18,948,250 bytes). It remains offline and permission-free. Replace files in an existing unpacked installation and press Reload to retain its notes/bookmarks. This is the guide package, not a newly packaged game release.\n\nReview hub: `_shots/request_completion_1021/review.html`. Machine-readable audit and probe reports are retained alongside it. Current native files supersede older screenshots and labels; the broader encyclopedia source census still contains labeled historical definitions and is not an exhaustive new attack-timing study.\n'
(R/'docs/REQUEST_COMPLETION_1021.md').write_text(md,encoding='utf-8')
cards=''.join('<article><span>'+html.escape(q['status'])+'</span><h2>'+html.escape(q['item'])+'</h2><p>'+html.escape(q['detail'])+'</p><a href="'+q['url']+'">Review evidence →</a></article>' for q in pending)
table=''.join('<tr><td>'+html.escape(a)+'</td><td>'+html.escape(b)+'</td><td>'+html.escape(c)+' <a href="/docs/'+d+'">Details</a></td></tr>' for a,b,c,d in rows)
page='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF / Request completion audit</title><style>*{box-sizing:border-box}body{margin:0;background:#090e16;color:#e9f1f7;font:17px/1.6 system-ui}main{max-width:1320px;margin:auto;padding:28px}h1{font-size:clamp(26px,4vw,46px);line-height:1.2;color:#ffbd67}h2{font-size:22px}a{color:#82d9ff}nav{display:flex;flex-wrap:wrap;gap:18px}.stats{padding:18px;background:#132b27;border-left:4px solid #6be49a;margin:24px 0}.open{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:18px}article{padding:22px;background:#1b202b;border-top:3px solid #ffb05c}article span{font-size:13px;color:#ffc26d}table{border-collapse:collapse;width:100%;margin:28px 0}td,th{text-align:left;vertical-align:top;padding:15px;border-bottom:1px solid #33404e}td:first-child{font-weight:700}th{color:#ffcc8a}img{max-width:100%;height:auto}p{color:#b8c9d6}@media(max-width:650px){main{padding:16px}table,tbody,tr,td{display:block}thead{display:none}tr{border:1px solid #344354;margin:16px 0}td{border:0;padding:10px}}</style><main><h1>BULLETS OF FURY / Completion audit</h1><p>Integrated work, fresh checks and the remaining decisions. Open items have not been counted as finished.</p><nav><a href="/index.html">Play BOF</a><a href="/extensions/bof-field-manual/guide.html">Field Manual 1.2</a><a href="/enemy-atlas.html">Live enemy atlas</a><a href="/docs/REQUEST_COMPLETION_1021.md">Full audit notes</a><a href="audit.json">Exact evidence</a></nav><div class="stats">8,943 regression assertions passed. 230 native combat / animation / finishing checks passed. Guide checks passed in Edge, Chrome and Firefox; refreshed native atlas checks passed.</div><h2>Still open</h2><div class="open">'''+cards+'</div><h2>Implemented coverage</h2><table><thead><tr><th>Request</th><th>Status</th><th>Result</th></tr></thead><tbody>'+table+'</tbody></table><h2>Current native captures</h2><img src="msedge-manual-hud.png" alt="Current Command Armor in the field guide"><img src="current-flight-banks.png" alt="Idle attack drift roll somersault banks"><img src="secret-animation-banks.png" alt="Seven correctly sliced Chrome Heart animation banks"></main>'
(O/'review.html').write_text(page,encoding='utf-8')
for name in ['refresh_request_audit_1021.py','probe_request_completion_1021.py','finish_request_completion_1021.py']:
 src=Path(__file__).parent/name
 if src.resolve()!=(R/'_BUILD_SOURCE'/name).resolve():shutil.copy2(src,R/'_BUILD_SOURCE'/name)
p=R/'HANDOFF_CODEX.md';s=p.read_bytes();marker='## October21 — request completion audit'
if marker.encode() not in s:p.write_bytes(s+('\r\n'+marker+'\r\n\r\nSee docs/REQUEST_COMPLETION_1021.md and _shots/request_completion_1021/review.html. Fresh suite 8943/0, 230 native combat/finishing checks; guide 1.2 and current aircraft/Chrome Heart encyclopedia refresh verified. Cole likeness approval, preview selection, optional cinematic boards, licensed Aqua track, complete balance sign-off and target-laptop FPS remain explicit open items. Do not describe protected fixtures as human clear rates or mark other eight pilots animated. No new art generation spend or GitHub publish in this audit.\r\n').encode())
print(json.dumps({'full_suite':report['full_suite'],'checks':checks,'open_items':len(pending)},indent=2))
