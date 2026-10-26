"""Summarize verified delivery and preserve prior handoff bytes and user work."""
from pathlib import Path
import json,hashlib,argparse
R=Path(__file__).resolve().parents[1];a=argparse.ArgumentParser();a.add_argument('--review-url',required=True);args=a.parse_args()
def read(p):return json.loads((R/p).read_text(encoding='utf8'))
native=read('_shots/warden_tidal_1025/probe/report.json');browser=read('_shots/warden_tidal_1025/browser/report.json');items=read('docs/previews/warden_tidal_1025/review.json')
assert len(native['checks'])==42 and all(c['passed']for c in native['checks'])and not native['errors']
assert len(browser['checks'])==34 and all(c['passed']for c in browser['checks'])and not browser['errors']
full=next(v for v in items if v['id']=='stage9-full');vf=R/full['src'].lstrip('/');verify=json.loads((vf.parent/'verification.json').read_text(encoding='utf8'));report=json.loads((vf.parent/'report.json').read_text(encoding='utf8'))
walk=next(v for v in items if v['id']=='warden');wv=R/walk['src'].lstrip('/');wr=json.loads((wv.parent/'report.json').read_text(encoding='utf8'))
assert all(verify['checks'].values())and all(wr['checks'].values())
assert {e for s in report['timeline']for e in (s.get('water')or{}).get('done',[])}>= {'flood','geysers','mortars','mist','undertow','maelstrom'}
assert report['audio']['deaths']==0
files=['assets/game.js','assets/stage78_review_1025.js','assets/bullethell_1025.js','assets/warden_tidal_1025.js','assets/warden_tidal_art_1025.js','_BUILD_SOURCE/build_warden_tidal_1025.py','index.html']
hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest()for f in files}
qa={'nativeChecks':[{k:c[k]for k in ['name','passed']}for c in native['checks']],'browserChecks':browser['checks'],'stage9Video':verify,'wardenVideo':{'path':walk['src'],'checks':wr['checks'],'sourceFps':wr['sound']['frames']/wr['timeline'][-1]['seconds']},'sha256':hashes,
 'reviewUrl':args.review_url,'nativeReport':'_shots/warden_tidal_1025/probe/report.json','browserReport':'_shots/warden_tidal_1025/browser/report.json',
 'fullSuite':{'exitCode':1,'finalSummaryReached':False,'reason':'Missing pre-existing _BUILD_SOURCE/retired_art_archive_1022.cjs; suite stops at its first require before assertions.'},'method':report['method']}
(R/'docs/qa/warden_tidal_1025.json').write_text(json.dumps(qa,indent=2),encoding='utf8')
def clock(t):return f'{int(t)//60:02}:{int(t)%60:02}'
chapters='\n'.join('| '+i['name'].split(' · ',1)[1]+' | '+clock(i['start'])+'–'+clock(i['end'])+' |'for i in items if i['id']not in ['warden','stage9-full'])
doc=f'''# Warden and Tidal Sovereign — October 25

[Watch the updated recordings]({args.review_url}). The review includes a {walk['end']:.1f}s Warden checkpoint, the complete {verify['duration']:.2f}s Furious Stage9 fight, and six water attack jump points.

## Stage7 corrections

| Problem | Cause and correction |
|---|---|
| Pilot retreats while the boss appears to slide | Chase mode moved the floor even after the chassis reached its screen target. Gait now measures body travel relative to that moving floor; stance feet ride its exact delta. Backward recovery also animates from its actual movement. Ground scroll stops with no usable legs or during a braced barrage. |
| Turrets shift while firing | The old battery pose converged their mounts inward, while chaingun poses stretched and extended the guns. Each complete gun now rotates around a fixed rear trunnion at local ±34,12. Its FOV and muzzle use the same resulting geometry. |
| Both live arms appear to disappear | Retired swipe and jump-crouch frames folded the forearms across the face, changing their silhouette and burying the return. The same connected walking claws and fixed hip pivots now perform the windup, strike, return, takeoff and landing. Native destroyed parts still break and lose their targets. |

## Stage9 upgrade

The existing whole Tidal Sovereign keeps its three native damage states. Each now has32 actual liquid poses on a fixed320×256 canvas,12fps, common160,128 pivot and one scale. Only the measured water apertures change: circles rotate and wing/core/nose water flows. Armor, seams, outlines and every alpha pixel stay byte-identical to each source damage state. The three banks total392,646bytes and reuse the approved blue water art.

| Furious attack | Behavior |
|---|---|
| Flood | Three water fronts, a 1.25 s first warning, 1.55 s between rows and a 150 px opening; the next gap shifts only after its tell starts. |
| Geysers | Six committed marks, a 1.35 s reaction window and 0.58 s stagger; tall water spires leave lateral escape space. |
| Laser mortars | Six arcing shots from the large circles, a 1.12 s charge plus 1 s flight; marked impacts erupt into water laser spires. Defensive clears cancel the pending eruption. |
| Mist lasers | The two lower cannon tips alternate four charged 0.48 s pressure beams, with water mist. A fifth pulse joins below half health. |
| Undertow | Five cutter-wave volleys from the circles and shootable physical torpedoes from the lower cannons. |
| Maelstrom | Six alternating circle barrages rotate around a committed opening. Water energy remains ordinary unshootable ordnance; defensive clears remain available. |

Normal and Hard use fewer flood rows and longer reaction windows. Attacks finish their hazards and recovery before the next turn; the old supplemental targeter is interlocked. Pending water hazards stop with their native boss owner. Measured cannon tips are (120,226) and (200,226); water circles are (96,87) and (224,87) on the 320×256 source canvas.

The complete water hull stays inside the visible camera bounds, keeping both circles and cannon tips readable as the pilot moves. The native sentinel fight, convergence, portal collapse,6500HP Furious water pool, vulnerability, death and rewards remain owned by the encounter. Pool initialization now occurs on the first live water frame, removing the old one-frame generic-health reset. No phase or health writes are used by the delivered full-fight bot.

## Current fight timestamps

These are absolute positions in the new full Stage9 recording. The bot defeats the sentinels normally, withholds weapons for one water rotation, then resumes fire through native defeat at {report['defeatSeconds']:.2f} s. GOD prevents player damage. This establishes runtime/visual coverage; human difficulty still needs player review.

| Water section | Full-fight timestamp |
|---|---|
{chapters}

The Warden clip advances the native loop to its first chase, then captures45s at real time with an invulnerable input bot withholding weapons so all live arms remain visible. It is a checkpoint, not a full new Stage7 kill. Earlier complete Stage7/8 fights and all original [timestamped 7/8/9 findings](FURIOUS_789_REVIEW_1025.md) remain available in the older review.

## Verification and ownership

-42 native Chromium checks pass, including actual visible claw pixels through every swipe, planted floor-relative feet, fixed turret pivots, all96 water hull cells, actual animated/hit pixels and expiry, safe flood gaps, geyser collisions, mortar clears, camera edge visibility, audio decoding/playback, phase entry and cleanup.
-34 browser review checks pass: both recordings and six chapters decode, play with audio, seek, frame-step and run in slow motion; byte-range requests and page/console/asset checks pass.
-The complete Stage9 MP4 passes all9 delivery checks; the Warden clip passes7. Stage9 has zero player deaths and no page, console or asset errors. Source render rate is {report['audio']['frames']/report['timeline'][-1]['seconds']:.1f} fps.
-Syntax passes for game.js and all updated modules. Required `node _BUILD_SOURCE/test_fl.js` exits1 before any assertions or final summary because `_BUILD_SOURCE/retired_art_archive_1022.cjs` is missing. That existing blocker is retained and reported.

Runtime: `assets/stage78_review_1025.js` (gait, claws, gun pivots), `assets/bullethell_1025.js` (braced gait state), `assets/warden_tidal_1025.js` (water owner). Generated hull registry: `assets/warden_tidal_art_1025.js`, owned by `_BUILD_SOURCE/build_warden_tidal_1025.py`. Art taxonomy registers `wt25_`. No production atlas was repacked.

Evidence: `docs/qa/warden_tidal_1025.json`; `_shots/warden_tidal_1025/` contains native fixtures, visible-pixel proofs, source masks, raw audio/video, full-decode logs and browser screenshots. Pre-existing user changes remain in place. No commit or push.
'''
for old,new in [('Stage7','Stage 7'),('Stage9','Stage 9'),('has32','has 32'),('each32','each 32'),('fixed320','fixed 320'),('common160','common 160'),('canvas,12fps','canvas at 12 fps'),('captures45s','captures 45 s'),('exits1','exits 1'),('total392,646bytes','total 392,646 bytes'),('6500HP','6,500 HP'),('all96','all 96'),('all9','all 9'),('passes7','passes 7')]:doc=doc.replace(old,new)
doc=doc.replace('\n-42','\n- 42').replace('\n-34','\n- 34').replace('\n-The','\n- The').replace('\n-Syntax','\n- Syntax')
(R/'docs/WARDEN_TIDAL_1025.md').write_text(doc,encoding='utf8')
note=f'''## October25 — Connected Warden walking and Tidal water arsenal

Mike's current correction: moving retreat floor now drives the Warden gait even at a stationary screen position; feet follow the same floor delta. Guns rotate around fixed trunnions, with no convergence/extension/recoil translation. Same connected claws perform all swipe phases; native destroyed-part ownership remains. Tidal has32 liquid frames per native whole-hull damage state (96 fixed320×256 frames; all armor/alpha unchanged), six coordinated water turns, measured circle/cannon sockets and native white-hit feedback. Native convergence, portal,6500 Furious water pool and death/rewards remain; initialize the water pool before its first live frame so hits cannot land on a temporary seed. Supplemental targeting is interlocked.

42 native checks and34 browser review checks pass. The complete water hull stays visible at both camera edges. New audible Warden45s checkpoint and complete{verify['duration']:.2f}s Furious Stage9 take (all six water patterns, native defeat, zero deaths/errors) decode/play/seek/frame-step. Docs and QA: docs/WARDEN_TIDAL_1025.md and docs/qa/warden_tidal_1025.json. Review: docs/previews/warden_tidal_1025/index.html. Original7/8/9 timestamped analysis and older films remain. Syntax passes; required full suite still exits1 before assertions/summary due missing retired_art_archive_1022.cjs. game.js/test_fl unchanged by this pass; no commit/push.

'''
for name in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/name;old=p.read_bytes()
 if note.splitlines()[0].encode()not in old:p.write_bytes(note.encode('utf8')+old)
contract='''
## October25 grounded Warden and Tidal water arsenal

- Warden gait counts actual chassis motion relative to retreating terrain. Never scroll the retreat floor without live walking legs; braced barrages and exhausted legs stop that scroll. Keep fixed gun trunnions and the same connected claws throughout swipe windup/strike/return.
- Tidal remains one whole authored hull with96 fixed320x256 liquid frames. Keep armor/alpha unchanged, exact circle/cannon sockets, visible native hit flash/expiry and the complete6500 Furious water pool from its first live frame.
- assets/warden_tidal_1025.js owns coordinated flood, geyser, circle-mortar, turret-mist, cutter/torpedo and maelstrom turns. Preserve committed escape windows, ordinary-energy interception rules, physical torpedoes, defensive clears, shared cues, targeter interlock, native convergence/portal/death/rewards and owner cleanup. See docs/WARDEN_TIDAL_1025.md.
'''
p=R/'AGENTS.md';old=p.read_bytes()
if b'## October25 grounded Warden and Tidal water arsenal'not in old:p.write_bytes(old+contract.encode('utf8'))
print(json.dumps({'native':42,'browser':34,'videoChecks':len(verify['checks'])+len(wr['checks']),'suiteExit':1,'doc':'docs/WARDEN_TIDAL_1025.md'}))
