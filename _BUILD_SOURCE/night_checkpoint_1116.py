from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116';S=R/'_ART_SOURCES/cinema_overnight_1116';C=Path(__file__).parent
doc=R/'docs/CINEMA_OVERNIGHT_1116.md';s=doc.read_text(encoding='utf8');marker='## Checkpoint — 3:35 AM EST'
if marker not in s:s+='''

## Checkpoint — 3:35 AM EST

- Native row inventory: 6,804 cases (all nine pilots, every ordered co-op pair, Normal/Hard/Furious, two routes, 14 current row sets). No exceptions, unresolved placeholders or invalid durations. Repeated short reading holds were found before repair; after repair no listed row falls below the defined full-text hold.
- Current owner `assets/night_cinema_1116.js`: post-Stage1 replies now come from the ship's FLIGHT SYSTEM on an onboard console, preserving lost squad comms until the service data-link. Stage4 arrival no longer requests the removed power cell. Ordinary story conversations retain at least 2.25 seconds after typing (long lines get more); physical HQ departure/guard/death timings remain unchanged.
- Full native director contract pass: 126 pilot/scene runs, 1,008 shot visits; 139 checks passed. Pause, reveal, next, Start skip and exactly-once callbacks verified. These are prepared director fixtures at60Hz with4Hz actual drawing, not campaign wins or real-time audio certification.
- Cole/Hard visual pass: 224 checkpoint renders, 13,457 actual bitmap draws. No out-of-bounds source rectangles, skipped images, smoothing or canvas-state leaks. Contact boards and original screenshots retained under render-before/ and render-after/.
- The HQ conference insert still had the retired black outfit. Built-in imagegen edited the four existing poses using the approved row-B orange-vest Juggernaut reference. Exact prompt, returned master, normalized whole frames, lossless master/comic WebP and editable layered source retained. Returned1774x887 atlas was transparently padded per cell to888x444; no master stretching. C16, D1110 and HQ1110 banks now share the corrected version. Direct comic export keeps the original shared crop754x270. This is four retained poses, not sixteen new poses.
- Controlled required-art delay reproduced three defects: the director advanced after15 seconds while a portrait remained unready, resumed mid-line, and the opening could not be skipped when a background failed to decode. New loading guard keeps time/text at zero until required art is ready, consumes loading-screen A/click edges and preserves Start skip. All four delayed-decode/skip checks now pass, with the original failing receipt retained.
- Initial arrival sweep reached PLAY with every selected pilot and no browser exceptions, but repeated Stage7 visits reused intentional once-only approach flags. Its manually reset co-op fixture also overlapped the ships. A fresh-page/native-startRun sweep is running; do not call those fixture artifacts production bugs or count all original visits as full approach playback.

Sources/backups: _ART_SOURCES/cinema_overnight_1116. Evidence: _shots/cinema_overnight_1116. Engine/test files remain untouched in this overnight pass. No commit, push, deployment or public score writes.
''';doc.write_text(s,encoding='utf8',newline='\n')
for f in C.glob('night_*1116.py'):
 code=f.read_text(encoding='utf8');code=re.sub(r"R=Path\(r'D:[^']+'\)","R=Path(__file__).resolve().parents[1]",code);(R/'_BUILD_SOURCE'/f.name).write_text(code,encoding='utf8',newline='\n')
for n in['night_cinema_1116.js','night_hq_prompt_1116.txt']:
 if(C/n).exists():(S/n).write_bytes((C/n).read_bytes())
tax=R/'assets/data/ART_TAXONOMY.json';d=json.loads(tax.read_text(encoding='utf8'));d={'nq16_':{'role':'approved_cast_HQ_conference_costume_correction','owner':'_BUILD_SOURCE/night_hq_art_1116.py','manifest':'_ART_SOURCES/cinema_overnight_1116/hq-conference.json','note':'Four retained poses; even888x444 master and754x270 direct comic crop. Native draw pixels and editable-source export verified separately. No new16-frame animation claim.'},**d};tax.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Saved overnight progress and portable source/probe recipes.')
