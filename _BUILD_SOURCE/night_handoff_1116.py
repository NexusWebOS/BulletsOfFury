from pathlib import Path
import json,hashlib,re
R=Path(__file__).resolve().parents[1];S=Path(__file__).parent;O=R/'_shots/cinema_overnight_1116';A=R/'_ART_SOURCES/cinema_overnight_1116';A.mkdir(exist_ok=True)
for p in S.glob('night_*1116.py'):
 data=p.read_text(encoding='utf8');data=data.replace("R=Path(r'D:\\BOF-Downloads\\2026-11-14\\RevG-source')","R=Path(__file__).resolve().parents[1]")
 (R/'_BUILD_SOURCE'/p.name).write_text(data,encoding='utf8',newline='\n')
for p in S.glob('night_*1116.js'):
 (R/'_BUILD_SOURCE'/p.name).write_text(p.read_text(encoding='utf8'),encoding='utf8',newline='\n')
for name in ['night_cinema_1116.js','night_hq_art_1116.js','night_city_atlas_1116.js','night_weather_1116.js']:
 p=R/'assets'/name;(A/name).write_bytes(p.read_bytes())
q=json.loads((O/'static-report.json').read_text());assert q['activeScripts']==753 and q['final']['passes']==8969 and q['finalSummaryReached'] and not q['newFailures']
old=R/'_shots/release_qa_1116/review.html';b=A/'release-review-before-night.html'
if not b.exists():b.write_bytes(old.read_bytes())
s=old.read_text(encoding='utf8');note='<aside style="padding:18px;border:2px solid #8ccce8;background:#102333">This is the earlier release pass. The current overnight build has additional cinematic, atlas and weather fixes. <a href="../cinema_overnight_1116/review.html">Open the current overnight review and recordings.</a></aside>'
if 'Open the current overnight review and recordings.'not in s:s=s.replace('<main>','<main>'+note,1);old.write_text(s,encoding='utf8',newline='\n')
p=R/'docs/CINEMA_OVERNIGHT_1116.md';s=p.read_text(encoding='utf8').replace('at661.991s','at659.648s')
text='''

## Checkpoint — 7 AM EST

- Final shipping set after weather change:753 external scripts+5 inline blocks parse. Full core suite8,969/0, actual final summary reached and failing-name comparison unchanged. Pipeline requires core exit0 and complete log before collecting. All four night scripts LF; original game.js, test_fl.js, online.js, cockpit/comic/release code bytes preserved against the start hashes. Main engine LF/tests CRLF unchanged. Receipts: final-verification.json, static-report.json, full-suite-post-weather.log.
- Applied weather owner was rechecked from the actual shipping index (not duplicate injected code):48 native weather pixel comparisons and5 special-context fallbacks remain identical. Full Furious Stage6 native input/GOD replay reached defeat at127.219s, with0 page/console errors and0 invalid rectangles. Its one canceled existing ghostrider music preload is retained separately as ERR_ABORTED, not a failed script or HTTP response. Original low-level per-tile-transform prototype was slower and was not shipped.
- Bounded same-tab replay completed all18 original-order starts (Normal1-5, Hard1-4), native protected no-fire60 simulated seconds each. No timeout, page error or captured exception. This replay yields every6 frames; the original stalled test yielded every30. The original stall was not reproduced, its root cause remains unproven, and its partial receipt remains linked. Do not label it a confirmed game fix or erase it.
- Review board now includes26 full clips: opening, native Chronos/HQ sequence, five current Stage3/4/kit clips and eighteen full protected encounters. The current Stage6 weather replay replaces the earlier Stage6 film in the preferred list; older films remain. All nine gameplay contact boards (72 native frames) and current story contacts were visually inspected. Prior release review now links to this newer pass without overwriting its historical evidence.
- Current Freezer overflow widget uses the original224-character retained optional line, scrolls40px, exposes the final row and completes once. The23 longest current story lines complete and fit their original boxes. Exact retained optional text was not restored to the active campaign.
- A further fresh Normal campaign smoke is running with Cole and default resources, normal damage and no GOD/lives/HP/phase/timer edits. Its limited input bot is for actual opening→map→comic→gameplay/death/handoff flow, not human balance certification. Do not claim its outcome until its final receipt exists.
- Portable reproduction recipes and current four-script sources copied into _BUILD_SOURCE; editable art masters and manifests remain in _ART_SOURCES/cinema_overnight_1116. Builder experiments/raw discarded fixtures are distinct from shipping owners. No commit/push or public score operations.

Remaining: finish the running campaign-flow smoke, refresh the final video/audio/browser review receipt, final handoff and8AM report. Release HOLD remains: human full-mode/difficulty playthroughs, real8BitDo/two-player hardware, separate-machine internet co-op, target-hardware performance, narrow-window menu readability and packaging are not certified by these fixtures.
'''
if '## Checkpoint — 7 AM EST'not in s:s+=text
p.write_text(s,encoding='utf8',newline='\n')
note='November16 overnight cinematic QA: preserve assets/night_cinema_1116.js (reading holds, comms continuity, required-art waits and friendly radio material), night_hq_art_1116.js (approved orange-vest conference), night_city_atlas_1116.js (transparent source padding/empty end frame) and night_weather_1116.js (pixel-identical off-canvas weather culling). Current evidence: docs/CINEMA_OVERNIGHT_1116.md and _shots/cinema_overnight_1116/review.html. Core8969/0,753+5 scripts parse. GOD films are not human balance/campaign wins; release remains HOLD. No commit/push without Mike.'
for name in ['AGENTS.md','HANDOFF_CODEX.md']:
 p=R/name;raw=p.read_bytes();mark=b'November16 overnight cinematic QA:'
 if mark not in raw:
  eol=b'\r\n'if b'\r\n'in raw else b'\n';first,sep,rest=raw.partition(eol);p.write_bytes(first+eol+eol+note.encode('utf8')+eol+eol+rest)
receipt={'files':{str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()for p in [R/'index.html',*(R/'assets'/n for n in ['night_cinema_1116.js','night_hq_art_1116.js','night_city_atlas_1116.js','night_weather_1116.js'])]},'noCommitPush':True};(O/'shipping-manifest.json').write_text(json.dumps(receipt,indent=2),encoding='utf8');print('Portable sources and current handoff saved; release HOLD')
