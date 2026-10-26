from pathlib import Path
import json,hashlib

R=Path(__file__).resolve().parents[1];O=R/'_shots/dracodia_download_reveal_1025'
native=json.loads((O/'probe/report.json').read_text());info=json.loads((R/'_shots/dracodia_transformation_1025/latest.json').read_text());folder=Path(info['folder']);film=json.loads(Path(info['report']).read_text());play=json.loads((folder/'playback.json').read_text())
assert all(q['passed']for q in native['checks'])and all(film['checks'].values())and all(play['checks'].values())
qa={'scope':'Authored turning symbiote carrier downloads the actual live Dracodia final form with continuous pose, scale and pixels',
 'native':{'passed':len(native['checks']),'failed':0,'report':'_shots/dracodia_download_reveal_1025/probe/report.json','pixelChecks':[q for q in native['checks']if 'pixels'in q['name']or'position jump'in q['name']]},
 'video':{'path':film['video'],'seconds':film['timeline'][-1]['seconds'],'decodedPeakDb':film['decodedPeakDb'],'nativeFps':film['sound']['frames']/film['timeline'][-1]['seconds'],'checks':film['checks'],'chapters':film['chapters'],'report':Path(info['report']).relative_to(R).as_posix()},
 'playback':play,'syntax':{'assets/game.js':0,'assets/dracodia_rebirth_1023.js':0,'assets/dracodia_download_reveal_1025.js':0},
 'requiredSuite':{'command':'node _BUILD_SOURCE/test_fl.js','exitCode':1,'finalSummaryReached':False,'reason':'Existing missing _BUILD_SOURCE/retired_art_archive_1022.cjs aborts before assertions.'},
 'sourceHashes':{p:hashlib.sha256((R/p).read_bytes()).hexdigest()for p in ['assets/dracodia_download_reveal_1025.js','assets/dracodia_rebirth_1023.js','index.html']},
 'method':'Native Chromium loop and actual drawImage pixels. Explicit native-damage checkpoint starts the continuous recorded rebirth. No animation timers or phases skipped. Native speech finishes naturally before the separate damage fixture.'}
(R/'docs/qa/dracodia_download_reveal_1025.json').write_text(json.dumps(qa,indent=2),encoding='utf8')
video='http://127.0.0.1:53746/'+film['video']
doc=f'''# Dracodia rotating download — October25

Mike approved the rotating frame and requested that it download the final form
continuously. [Current audible36-second video]({video}). Older takes remain.

`assets/dracodia_download_reveal_1025.js` owns this rebirth presentation after
stage78_review_1025.js. The existing24-pose symbiote turntable remains visible
inside the unbuilt scan bands. The existing16-pose Colossus wire scaffold marks
the unbuilt body; completed bands use the actual live ce20Body final-form renderer.
The smaller fusion snapshot no longer substitutes for the live body.

Measured native chest anchors register the carrier and final form. They share
the same rotating assembly while the data fills. Translation follows continuously
from the rising carrier into the final speech position. The assembled body
settles upright at the native size and animation clock before the whiteout, and
continues at that exact position as the light clears. Both the first carrier
and completed final-body pixels match their existing native renderers.

The existing24 accelerating lightning beats converge around that chest anchor.
Download completion,25.6s final-arena swap,28.5s protected speech handoff, five
finite form pools, native damage/hit flashes and defeat ownership remain.
The fusion beat uses approved combatEnergy0927 through the shared mixer instead
of a teleport cue. The original stage entrance and return portals keep their
native owners. No new assets, generated artwork or atlas changes were needed.

## Verification

- {len(native['checks'])} native Chromium checks pass:24 turning frames, increasing
  completed data bands, preserved form pools/protection,24 lightning beats,
  one reveal, identical first/completed renderer pixels, continuous final pose,
  full native speech, actual white hit pixels and native flash expiry.
- {len(play['checks'])} playback checks pass. The36.11s clip fully decodes with
  {film['decodedPeakDb']}dB sound and roughly{qa['video']['nativeFps']:.1f} native
  frames/s. Native energy/charge/lightning/explosion audio actually played;
  the transformation has no teleport cue. No page, console or asset errors.
- JavaScript syntax checks pass. Required test_fl.js exits1 before assertions
  or a final summary due the existing missing retired_art_archive_1022.cjs.

Evidence: docs/qa/dracodia_download_reveal_1025.json and
_shots/dracodia_download_reveal_1025/probe/. Reproduce with
probe_dracodia_download_reveal_1025.py, record_dracodia_transformation_1025.py
and check_dracodia_transformation_video_1025.py under _BUILD_SOURCE/.
The film uses an explicit native-damage checkpoint; it is not a complete fight.
This pass did not edit game.js/test_fl.js, commit or push.
'''
doc=doc.replace('audible36','audible 36').replace('existing24','existing 24').replace('existing16','existing 16').replace('beats,25','beats, 25').replace('completion,25','completion, 25').replace('swap,28','swap, 28').replace('pass:24','pass: 24').replace('bands,24','bands, 24').replace('The36','The 36').replace('roughly{','roughly {').replace('roughly'+str(round(qa['video']['nativeFps'],1)),'roughly '+str(round(qa['video']['nativeFps'],1))).replace('exits1','exits 1')
(R/'docs/DRACODIA_DOWNLOAD_REVEAL_1025.md').write_text(doc,encoding='utf8')
title='## October25 — Rotating carrier downloads the actual final Dracodia body'
note=f'''{title}

Mike approved the rotating frame and requested a continuous final-form download. New owner assets/dracodia_download_reveal_1025.js preserves the authored24-pose turning carrier and uses actual live ce20Body final-form pixels in completed scan bands. Measured chest anchors, common native scale, continuous motion and upright settling remove the smaller-fusion-to-live-body jump. The completed body continues through the whiteout into protected speech. All24 lightning beats, native arena/speech timings, five form pools, hit flashes and defeat remain. Fusion uses combatEnergy0927; original portal ownership remains. No new art needed.

{len(native['checks'])} native checks and{len(play['checks'])} playback checks pass; fresh36.11s audible film fully decodes at about59 native fps. First-carrier/completed-body pixel comparisons and native final hit/expiry pass; no browser/asset errors. Docs and QA: docs/DRACODIA_DOWNLOAD_REVEAL_1025.md and docs/qa/dracodia_download_reveal_1025.json. Required suite still exits1 before assertions/summary because retired_art_archive_1022.cjs is missing. No game.js/test_fl.js edits, commit or push.

'''.replace('authored24','authored 24').replace('All24','All 24').replace('and'+str(len(play['checks'])),'and '+str(len(play['checks']))).replace('fresh36','fresh 36').replace('about59','about 59').replace('exits1','exits 1')
for name in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/name;raw=p.read_bytes()
 if title.encode()not in raw:p.write_bytes((note.replace('\n','\r\n')if b'\r\n'in raw else note).encode()+raw)
p=R/'AGENTS.md';raw=p.read_bytes();rule='## October25 Dracodia rotating download\n\n- Use the authored turning carrier to download the actual live final-form body through one measured chest anchor and native scale. Preserve continuous carrier/build/speech positions, completed pixels, all24 lightning beats and native HP/reveal/death ownership. Fusion uses combatEnergy0927; do not reintroduce a small fusion snapshot, teleport pop or teleport cue for this beat. See docs/DRACODIA_DOWNLOAD_REVEAL_1025.md.\n'
if b'## October25 Dracodia rotating download'not in raw:p.write_bytes(raw+('\r\n'+rule.replace('\n','\r\n')if b'\r\n'in raw else'\n'+rule).encode())
p=R/'docs/STAGE78_REVIEW_1025.md';text=p.read_text(encoding='utf8');marker='## Creative contract'
addition='The latest rebirth presentation is now owned by\n`assets/dracodia_download_reveal_1025.js`: the rotating carrier downloads the\nactual live final body with continuous pose and size through the reveal. See\n[rotating download and fresh clip](DRACODIA_DOWNLOAD_REVEAL_1025.md). The full-fight\nfilms below predate this focused rebirth revision.\n\n'
if 'DRACODIA_DOWNLOAD_REVEAL_1025.md'not in text:p.write_text(text.replace(marker,addition+marker,1),encoding='utf8')
print(json.dumps({'native':len(native['checks']),'playback':len(play['checks']),'video':film['video'],'pixelChecks':qa['native']['pixelChecks']}),flush=True)
