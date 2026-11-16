from pathlib import Path
import hashlib,json,datetime
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116';O.mkdir(parents=True,exist_ok=True);S=R/'_ART_SOURCES/cinema_overnight_1116';S.mkdir(parents=True,exist_ok=True)
paths=['assets/game.js','assets/release_cinema_1116.js','assets/cockpit_talk_1114.js','assets/comic_motion_1111.js','assets/online.js','index.html','_BUILD_SOURCE/test_fl.js']
receipt={p:hashlib.sha256((R/p).read_bytes()).hexdigest()for p in paths}
for p in paths:
 target=S/(Path(p).name+'.before')
 if not target.exists():target.write_bytes((R/p).read_bytes())
(O/'baseline-hashes.json').write_text(json.dumps(receipt,indent=2),encoding='utf8')
doc=R/'docs/CINEMA_OVERNIGHT_1116.md'
if not doc.exists():doc.write_text('''# Overnight cinematic QA — November 16, 2026

Mike authorized review and confirmed fixes for all cinematics, rendering and flow bugs while he sleeps. Work is in original BOF at D:/BOF-Downloads/2026-11-14/RevG-source. Preserve existing work; no commit/push/deployment. Default overnight review window ends at 8 AM America/New_York. This is an active work log, not release certification.

## Starting checkpoint

Prior release pass: main suite 8,969/0, 749 shipping scripts and five inline blocks parse. Stable controller seats, online native HUD/audio/input, Stage6 standalone entry, nine-pilot ending holds, row-B guitar identity and host aspect fitting are already applied. Retain all of them. Main report: RELEASE_READINESS_1116.md. Engine LF/tests CRLF; one writer. Baseline hashes and source backups are retained under _shots/cinema_overnight_1116 and _ART_SOURCES/cinema_overnight_1116.

## Current work

- Inventory current runtime scene branches and reading/continuity properties for every pilot and ordered co-op pair.
- Review actual pixels at multiple animation times, current approved identities, clipping and all handoffs.
- Reproduce confirmed faults before changing production owners. Keep archived scenes and rejected artwork inactive.

## Evidence limits

Metadata checks, direct-render checkpoints, native sequence playback and actual gameplay clears are distinct evidence. Do not call a fixture recording a full campaign win. An all-night pass does not imply physical controller, WAN co-op or target-hardware certification.
''',encoding='utf8',newline='\n')
print('Saved overnight baseline and live journal.')
