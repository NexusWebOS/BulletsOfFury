from pathlib import Path
from datetime import datetime,timezone
import argparse,json,hashlib,subprocess

R=Path(__file__).resolve().parents[1];a=argparse.ArgumentParser();a.add_argument('--suite-exit',type=int,required=True);args=a.parse_args()
matrix=json.loads((R/'_shots/bullethell_1025/probe/matrix.json').read_text(encoding='utf8'))
pixels=json.loads((R/'_shots/bullethell_1025/pixels/report.json').read_text(encoding='utf8'))
browser=json.loads((R/'_shots/bullethell_1025/browser/report.json').read_text(encoding='utf8'))
clips=json.loads((R/'_shots/bullethell_1025/video/recordings.json').read_text(encoding='utf8'))
for group in [matrix,pixels,browser]:assert all(c['passed']for c in group['checks'])and not group['errors'],group
assert len(clips)==12 and all(all(q['checks'].values())for q in clips)
for file in ['assets/game.js','assets/bullethell_1025.js']:subprocess.run(['node','--check',str(R/file)],check=True)
baseline=json.loads((R/'docs/qa/stage78_review_1025.json').read_text(encoding='utf8'))
hashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest()for f in ['assets/game.js','assets/bullethell_1025.js','assets/stage78_review_1025.js','assets/dracodia_rebirth_1023.js','assets/boss_integrity_1024.js']}
unchanged=hashes['assets/game.js']==baseline['runtimeHashes']['assets/game.js'];assert unchanged
native=len(matrix['checks'])+len(pixels['checks'])
result=dict(created=datetime.now(timezone.utc).isoformat(),nativePassed=native,nativeFailed=0,nativeErrors=[],matrixPassed=len(matrix['checks']),pixelPassed=len(pixels['checks']),browserPassed=len(browser['checks']),browserErrors=browser['errors'],clips=[dict(stage=q['stage'],role=q['role'],video=q['video'],method=q['method'],seconds=q['timeline'][-1]['seconds'],sourceFps=q['sound']['frames']/q['timeline'][-1]['seconds'],decodedPeakDb=q['decodedPeakDb'],checks=q['checks'])for q in clips],runtimeHashes=hashes,gameJsMatchesOriginalCapture=unchanged,fullSuite=dict(exitCode=args.suite_exit,reachedFinalSummary=False,preexistingMissing='_BUILD_SOURCE/retired_art_archive_1022.cjs'),review='docs/previews/bullethell_1025/index.html')
(R/'docs/qa/bullethell_1025.json').write_text(json.dumps(result,indent=2),encoding='utf8')
(R/'_shots/bullethell_1025/delivery.json').write_text(json.dumps(result,indent=2),encoding='utf8')
heading='## October25 — Bullet hell sections for Warden, Dracodia and all nine minibosses'
note=f'''{heading}

Mike requested bullet hell sections after the Furious encounter review. New final owner assets/bullethell_1025.js, after stage78_review_1025.js: rotating rings, gun/cannon braids, sonic rakes and a Herald feather vortex. Raised claws own first-body Dracodia fans; final main-body code flowers interlock with the archive army and preserve original attack-book progress. Native warning colours, committed openings, finite waves/recovery, live sockets/muzzle effects and shared audio remain authoritative. Normal/Hard scale down. Ordinary new bullets reject offensive interception from birth while allowing native defensive clears. Destroyed parts cancel pending/released volleys; shield retaliation and escorts receive separate windows. No new art generation.

{native} native checks pass ({len(matrix['checks'])} encounter, {len(pixels['checks'])} damage/phase/audio), plus {len(browser['checks'])} browser review checks. Actual damage/expiry/part-break/ball/rebirth/final-ledger pixels inspected. Twelve audible real-time checkpoint clips, with an explicitly selected final-body fixture, all decode/play/seek/frame-step. Review docs/previews/bullethell_1025/index.html; contracts/build/evidence docs/BULLETHELL_1025.md and docs/qa/bullethell_1025.json. Earlier full recordings and timestamped findings preserved. assets/game.js hash still matches the original Furious capture; test_fl untouched. Syntax passes. Required full suite exits{args.suite_exit} before assertions/summary because retired_art_archive_1022.cjs is missing (pre-existing). No commit/push.

'''
for name in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/name;old=p.read_bytes()
 if heading.encode()not in old:
  nl='\r\n'if b'\r\n'in old else'\n';p.write_bytes(note.replace('\n',nl).encode('utf8')+old)
p=R/'AGENTS.md';old=p.read_bytes();label='## October25 bullet hell sections'
if label.encode()not in old:
 nl='\r\n'if b'\r\n'in old else'\n'
 text='''
## October25 bullet hell sections

- assets/bullethell_1025.js owns the new Warden/Dracodia and nine campaign miniboss barrages. Preserve native HP/form pools, original attack-book progress, authored projectile art, part flashes, committed openings and finite recovery.
- New ordinary barrage rounds reject offensive interception before their first update, while retaining native defensive clears. Physical missiles keep their native rules. Broken wings/claws/guns cancel their warnings and rounds.
- Preserve the escort, archive-army and Warden shield-counter interlocks. First-body Dracodia raises the real claws before committing warnings and uses those same sockets for release. See docs/BULLETHELL_1025.md.
'''
 p.write_bytes(old+text.replace('\n',nl).encode('utf8'))
print(json.dumps({'native':native,'browser':len(browser['checks']),'clips':len(clips),'gameJsUnchanged':unchanged,'fullSuiteExit':args.suite_exit}),flush=True)
