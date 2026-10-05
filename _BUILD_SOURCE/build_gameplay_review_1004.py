"""Assemble the local recording-repair review and portable QA evidence."""
from pathlib import Path
import json,html,re
R=Path(__file__).resolve().parents[1];O=R/'_shots/gameplay_audit_1004'
read=lambda p:json.loads((O/p/'report.json').read_text(encoding='utf-8'))
repair,routes,polish,maps,modules,cinematic=[read(p) for p in ['repair','routes','polish','map','modules','cinematic']]
suite=(O/'suite-final.txt').read_text(encoding='utf-8')
assert '==== FALVA/LIZZIE BUILD OK, 0 ERRORS ====' in suite
count=len(re.findall(r'^  ok ',suite,re.M))
qa={'recording':{'name':'2026-10-04 00-46-51.mp4','duration':'61:29','visual_samples':1845,'interval_seconds':2,'contact_sheets':77,'limitations':'Sampled entire timeline, not every video frame or complete audio. Stage 1 combat absent.'},
 'suite':{'command':'node _BUILD_SOURCE/test_fl.js','exit_code':0,'assertions':count,'baseline':7022,'summary':'FALVA/LIZZIE BUILD OK, 0 ERRORS','initial_nonzero':'Four outdated global Forge discovery expectations; updated fixtures for run-earned elements and explicit purchases; no assertions removed.'},
 'storm_defeat':{'result':routes['storm'][-1],'fixture':'Ordinary L3 machinegun cadence, real collision/damage, autoaim, invulnerable pilot; not a human balance clear.'},
 'donors_full_hp':repair['donors'],'donors_low_hp':modules['forms'],'helicopter_disarm':modules['disarm'],
 'hammer':{'floor':repair['hammerFloor'],'reserve':repair['hammerReserve'],'death':cinematic['death']},
 'forge':{'previews_errors':routes['previews'],'up':repair['forge']},'orbs':{'fire_real_update':polish['fireOrb'],'motion':'30/60 FPS finite consistency assertion'},
 'rebels':{'formation':repair['rebels'],'completion':polish['rebelFinish']},'pressure':polish['pressure'],'enemies':routes['enemies'],
 'passwords':routes['passwords'],'stage6_exit':routes['stage6Exit'],'map':maps,'gas':modules['gas'],
 'knight_tells':{'recover_draws':cinematic['recoverWarnings'],'tell_draws':cinematic['tellWarnings']},
 'browser_errors':{n:d['errors'] for n,d in zip(['repair','routes','polish','map','modules','cinematic'],[repair,routes,polish,maps,modules,cinematic])},
 'reference':'https://www.youtube.com/watch?v=6rXONPQvoTw','review':'_shots/gameplay_audit_1004/review.html','human_campaign_clear':False}
(R/'docs/qa/gameplay_repair_1004.json').write_text(json.dumps(qa,indent=2)+'\n',encoding='utf-8')
cards=[
 ('Map / connected islands','map/selected-jungle.png','Nine authored pieces, connected around a central city. Arrival zoom and selection camera.'),
 ('Map / compact layout','map/compact.png','Selected island remains visible above the progression cards and live briefing.'),
 ('Rebels / final transmission','repair/rebel-death.png','Whole ship burning spin, large shocked portrait and all five individual health readouts.'),
 ('Rebels / white fade','polish/rebel-white-death.png','Portrait fades to white. Victory waits for every crash and queued transmission.'),
 ('Hammer / in-engine destruction','cinematic/death-5.png','Separate authored body, head and arm play the dramatic death before the cutscene.'),
 ('Hammer / return to Earth','repair/earth-homecoming.png','Return to the game engine; distant Earth, final explosions, crew welcome and forward flight.'),
 ('Furious / reserve recovery','repair/hammer-reserve.png','The first 8% crossing guarantees one recovery to 38%, then resumes active rage attacks.'),
 ('Stealth / approved silhouette','routes/approved-stealth-colors.png','Opening fighter in red and green; elite remains blue through banks and damage.'),
 ('Finale / alien helicopter','modules/helicopter-disarmed.png','Campaign sweep, charges, re-entry and sonic combo. This capture has its left gun and rack removed.'),
 ('Finale / Furnace','modules/lowhp-2.png','Actual Furnace controller advances through arms, reactor and eye phases.'),
 ('Finale / Cryo','modules/lowhp-3.png','Real battery, relay and crossfire; independent gun ownership and persistent damage.'),
 ('Finale / Storm','modules/lowhp-4.png','Real battery, escorts, siege weapons and lightning lance.'),
 ('Finale / powered knight','cinematic/knight-recover.png','Hammer leaps, chains, guns and spells. Live sword geometry and power effect; warnings clear after tells.'),
 ('Finale / Harrier','modules/lowhp-6.png','Ace movement paired with carrier flurry, spread and beam controllers.'),
 ('Finale / Warden','modules/lowhp-7.png','Current Warden chase, articulated swipes, jump and stomp controller, plus alien flank casts.'),
 ('Stage 3 / Frost Cruiser','polish/frostcruiser.png','Shorter dead time and stronger attacks while preserving the original attack vocabulary.'),
 ('Stage 4 / miniboss','polish/olivewarden.png','More sustained fire and surviving central-gun pressure.'),
 ('Forge / navigation','routes/forge-up.png','All preview combinations and repeated Up input checked. Historical discoveries do not unlock every run.'),
 ('Stage 8 / new attacks','routes/enemy-s8gunship.png','New enemies release committed multi-shot volleys with distinct projectile patterns.'),
 ('Stage 7 / gas visibility','modules/readable-gas.png','Four overlapping cloud sprites; player and effects stay visible through normalized opacity.')]
figs=''.join(f'<figure><a href="{src}" target="_blank"><img src="{src}" loading="lazy" alt="{html.escape(title)}"></a><figcaption><h3>{html.escape(title)}</h3><p>{html.escape(note)}</p></figcaption></figure>' for title,src,note in cards)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bullets of Fury — Recording repairs</title>
<style>*{box-sizing:border-box}body{margin:0;background:#070d17;color:#e5edf5;font:16px/1.6 system-ui,sans-serif}main{max-width:1480px;margin:auto;padding:32px}a{color:#7fdaff}header{border-bottom:1px solid #334a62;padding:20px 0 32px}h1{font-size:clamp(28px,4vw,52px);line-height:1.1;margin:12px 0}h2{margin-top:42px}h3{font-size:19px;margin:0}p{margin:12px 0;color:#b4c6d8}.eyebrow{letter-spacing:.22em;color:#7ee8ec;font-size:12px}.stats,.passwords{display:flex;gap:16px;flex-wrap:wrap;margin:24px 0}.stats span,.passwords span{background:#102137;border:1px solid #29425d;padding:12px 18px;border-radius:8px}strong{color:#fff}code{font-size:19px;color:#fcda83}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}figure{margin:0;background:#101b29;border:1px solid #283c54;border-radius:10px;overflow:hidden}img{display:block;width:100%;max-height:680px;object-fit:contain;background:#020509}figcaption{padding:18px 22px}details{background:#101b29;padding:18px 22px;border-radius:8px;margin:28px 0}li{margin:8px 0}footer{padding:30px 0;color:#a9bdcf}@media(max-width:760px){main{padding:18px}.grid{grid-template-columns:1fr}}</style>
<main><header><div class="eyebrow">BULLETS OF FURY / OCTOBER 4</div><h1>The recording repair pass</h1><p>Progression fixes, stronger encounters, cinematic deaths and a rebuilt campaign map.</p>
<div class="stats"><span><strong>ASSERTIONS</strong> passing</span><span><strong>0</strong> browser errors in completed probes</span><span><strong>61:29</strong> sampled visual timeline</span></div>
<a href="../../index.html?build=gameplay-repair-1004">Launch current local game</a> · <a href="../../docs/GAMEPLAY_AUDIT_1004.md">Timestamped audit and implementation notes</a> · <a href="../../docs/qa/gameplay_repair_1004.json">QA results</a>
</header><h2>Jump into the encounters</h2><div class="passwords"><span>Stage 9 <code>RIFT9</code></span><span>Stage X / Harrier <code>XHARR</code></span><span>Stage X / Rebels <code>XREBEL</code></span></div>
<details open><summary>What the checks establish</summary><ul><li>Stage 4 boss defeated through normal damage in 126 seconds; test pilot was invulnerable and auto-aimed.</li><li>All seven donor controllers ran at full and low HP. Broken weapon and delayed-lock ownership checks pass.</li><li>Hammer reaches its 8% floor, restores 38%, resumes attacks, dies in-engine, then enters the still sequence.</li><li>All five Rebel deaths complete, each portrait is shown, then victory proceeds. Stage 6 returns to the map.</li><li>All Forge previews and repeated Up inputs render without errors. A real L3 Fire Orb damages its primary target and nearby enemies.</li></ul><p>The recording was reviewed as 1,845 timestamped frames across all 61:29, not every frame or the complete audio. Stage 1 combat is absent. These controlled native Chromium checks are not full human campaign clears or final balance certification.</p></details>
<h2>Captured from the running game</h2><div class="grid">CARDS</div><footer>Existing work preserved. Changes are local; no commit or push. Open a screenshot to inspect it at full size.</footer></main></html>'''
(O/'review.html').write_text(page.replace('ASSERTIONS',f'{count:,}').replace('CARDS',figs),encoding='utf-8')
print(json.dumps({'review':str(O/'review.html'),'assertions':count,'cards':len(cards)}))
