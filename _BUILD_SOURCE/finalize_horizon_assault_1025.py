from pathlib import Path
import json,hashlib,subprocess

R=Path(__file__).resolve().parents[1];O=R/'_shots/horizon_assault_1025'
native=json.loads((O/'probe/report.json').read_text());browser=json.loads((O/'browser/report.json').read_text())
info=json.loads((O/'video/latest.json').read_text());film=json.loads(Path(info['report']).read_text());review=json.loads((R/'docs/previews/horizon_assault_1025/review.json').read_text())
assert all(c['passed']for r in[native,browser]for c in r['checks'])and all(film['checks'].values())
syntax=[]
for path in ['assets/game.js','assets/horizon_assault_1025.js']:
 q=subprocess.run(['node','--check',path],cwd=R,capture_output=True,text=True);assert q.returncode==0,q.stderr;syntax.append({'path':path,'exitCode':q.returncode})
suite=subprocess.run(['node','_BUILD_SOURCE/test_fl.js'],cwd=R,capture_output=True,text=True);(O/'full-suite.log').write_text(suite.stdout+suite.stderr,encoding='utf8')
assert suite.returncode==1 and 'retired_art_archive_1022.cjs'in suite.stderr
qa={'scope':'Stage9 Event Horizon miniboss: faster spin, vertical flight and charged eye energy bomb',
 'native':{'passed':len(native['checks']),'failed':0,'report':'_shots/horizon_assault_1025/probe/report.json'},
 'browser':{'passed':len(browser['checks']),'failed':0,'report':'_shots/horizon_assault_1025/browser/report.json'},
 'film':{'video':film['video'],'seconds':film['timeline'][-1]['seconds'],'decodedPeakDb':film['decodedPeakDb'],'checks':film['checks'],'chapters':review['chapters']},
 'syntax':syntax,'requiredSuite':{'command':'node _BUILD_SOURCE/test_fl.js','exitCode':1,'finalSummaryReached':False,'reason':'Existing missing _BUILD_SOURCE/retired_art_archive_1022.cjs aborts before assertions.','log':'_shots/horizon_assault_1025/full-suite.log'},
 'sourceHashes':{p:hashlib.sha256((R/p).read_bytes()).hexdigest()for p in['assets/game.js','assets/horizon_assault_1025.js','index.html']},
 'review':'docs/previews/horizon_assault_1025/index.html','method':'Native whole-hull art and health retained. Continuous invulnerable movement-bot demonstration with weapons withheld and no enemy HP/phase writes. Explicit damage/defensive-clear fixtures are separate.'}
(R/'docs/qa/horizon_assault_1025.json').write_text(json.dumps(qa,indent=2),encoding='utf8')
doc='''# Event Horizon assault — October25

Mike's faster spin, up/down flight and charged energy bomb are implemented for
the Stage9 miniboss. [Fresh45-second Furious review](previews/horizon_assault_1025/index.html).
The existing bullethell gallery's `9-mini` entry also uses the current film.

The old barrage stretched one complete spin bank over its firing duration.
`assets/horizon_assault_1025.js` gives the existing authored spin an independent
clock:1.75 rotations/s on Normal,2 on Hard and2.25 on Furious. Rotation brakes to
the upright source pose before the charge. The whole black drift/spin/charge
plates and their common eye pivot remain in use.

Flight has its own clock. In the Furious film the centre travels from170 to315
world pixels vertically, including during the barrage. The physical core,
rendered hull, warning origin and projectile launcher share that position.
Native horizontal manoeuvres remain. Charging pauses the vertical pass so the
large eye effect and committed firing lane are readable.

Every third native decision inserts an eye bomb, then resumes the native attack
book. The cyan energy visibly grows on the eye. Its green/yellow/red native
warning tracks briefly, locks with roughly one second remaining, then launches
a92px authored energy orb into a warned54px-radius impact. Furious charge lasts
1.65s and flight lasts1s. The shared targeted-ball owner supplies the line,
reticle, projectile travel and impact collision. Defensive clearing cancels the
bomb's splash; native defeat cancels a pending charge or flight.

The energy uses the existing animated cyan orb; no new hulls or generated assets
were needed. Charge, launch and impact use the shared `bossWeaponCharge`,
`combatOrb0927` and `warpBurst` cue routes and retrigger gates. Ordinary energy
rejects offensive interception from birth while preserving defensive clears.
Native complete HP, white damaged pixels, Retina/core ownership and defeat stay
authoritative. The final Stage9 Tidal encounter and warp remain separate.

Film checkpoints: fast barrage spin0:16.8; low vertical pass0:08.1; large charge
0:09.4; launched bomb0:10.0; impact0:10.9. The gallery also provides slow motion
and single-frame stepping. This is an invulnerable observation take with
weapons withheld, not a human difficulty verdict.

## Verification

-34 native Chromium checks pass across Normal, Hard and Furious: complete bomb
  cycles, vertical range, eye/core alignment, at least eight authored spin poses
  in half a second, unchanged HP during observation, committed aim, actual white
  hit pixels/expiry, defensive-clear cancellation, native defeat cleanup and
  decoded charge/fire/impact audio.
-11 browser review checks pass: all five checkpoints play and seek with audio,
  quarter/half speed, frame stepping, byte-range delivery and no page/console/
  asset errors. The45.22s film fully decodes at30fps; native rendering observed
  about59.6fps, with-8.5dB decoded audio and both complete bomb cycles audible.
-JavaScript syntax checks pass for game.js and the new encounter owner.
-Required `node _BUILD_SOURCE/test_fl.js` still exits1 at its first require:
  `_BUILD_SOURCE/retired_art_archive_1022.cjs` is missing. No assertions or final
  suite summary are reached; no full-suite pass is claimed.

Evidence: `docs/qa/horizon_assault_1025.json` and `_shots/horizon_assault_1025/`.
Reproduce with `_BUILD_SOURCE/probe_horizon_assault_1025.py`,
`record_horizon_assault_1025.py`, `publish_horizon_assault_1025.py` and
`check_horizon_review_1025.py`. No edits to game.js/test_fl.js, commit or push
were made by this pass.
'''.replace('\n-34','\n- 34').replace('\n-11','\n- 11').replace('\n-JavaScript','\n- JavaScript').replace('\n-Required','\n- Required')
(R/'docs/HORIZON_ASSAULT_1025.md').write_text(doc,encoding='utf8')
note='''## October25 — Event Horizon faster spin, vertical flight and charged eye bomb

Mike's Stage9 miniboss update is live in assets/horizon_assault_1025.js. The old barrage stretched one spin over its duration; the authored spin now has an independent clock (Normal1.75/Hard2/Furious2.25 rotations/s), settles upright for charge, and follows an independent vertical flight clock (170–315 centre range in the Furious film). Core/eye/hull/FOV/emission share the live position. Every third native decision charges a large cyan eye bomb, locks its aim, launches and impacts via native targeted-ball ownership, then resumes the original attack book. Native HP/hits/death and defensive clears remain; defeat cancels pending charges/flight. Existing whole authored plates and cyan energy used; final Tidal/warp unaffected.

34 native checks across Normal/Hard/Furious and11 browser checks pass. Fresh45.22s audible native-HP Furious film includes two complete bomb cycles, about59.6 native fps, decoded-8.5dB sound and no page/console/asset errors. Review: docs/previews/horizon_assault_1025/index.html; old bullethell gallery9-mini also points to the current film. Notes and QA: docs/HORIZON_ASSAULT_1025.md, docs/qa/horizon_assault_1025.json. Syntax passes; full suite still exits1 before assertions/summary due existing missing retired_art_archive_1022.cjs. This pass did not edit game.js/test_fl.js, commit or push.

'''
for file in['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/file;raw=p.read_bytes()
 if b'## October25 \xe2\x80\x94 Event Horizon faster spin, vertical flight and charged eye bomb'not in raw:
  nl=b'\r\n'if b'\r\n'in raw[:2000]else b'\n';p.write_bytes(note.encode().replace(b'\n',nl)+raw)
p=R/'AGENTS.md';raw=p.read_bytes()
if b'## October25 Event Horizon assault'not in raw:
 nl=b'\r\n'if b'\r\n'in raw else b'\n';p.write_bytes(raw+('''

## October25 Event Horizon assault

- assets/horizon_assault_1025.js owns the Stage9 miniboss fast spin, vertical flight and charged eye bomb. Keep the authored whole plates and common eye pivot; do not stretch the spin bank over the barrage duration.
- Keep the live core, eye, hull, warnings and release aligned during vertical passes. Settle upright for charge, preserve the committed reaction window, ordinary-energy interception rules, defensive clears, hit flash and native complete HP/defeat ownership. Native defeat cancels pending bombs. See docs/HORIZON_ASSAULT_1025.md.
''').encode().replace(b'\n',nl))
print(json.dumps({'nativePassed':qa['native']['passed'],'browserPassed':qa['browser']['passed'],'filmSeconds':qa['film']['seconds'],'suiteExit':1}),flush=True)
