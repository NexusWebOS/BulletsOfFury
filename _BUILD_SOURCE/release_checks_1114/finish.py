from pathlib import Path
from playwright.sync_api import sync_playwright
import json,hashlib,shutil,zipfile,difflib,sys
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Release-checks-1114';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
F=json.loads((O/'full-results.json').read_text());N=json.loads((O/'checks.json').read_text());G=json.loads((O/'weapon-gate/weapon-gate-checks.json').read_text());T=json.loads((O/'targeting-checks.json').read_text());V=json.loads((O/'retina-recording.json').read_text());A=json.loads((W/'editable-verification.json').read_text());B=json.loads((O/'asset-helper-checks.json').read_text());I=json.loads((W.parent/'stage5_bomber_assault_1114/installation.json').read_text())
assert all(q['exit']==0 for q in F)and '==== FALVA/LIZZIE BUILD OK, 0 ERRORS ===='in(O/'full-suite.log').read_text()
assert all(q['passed']for q in N['checks'])and not N['errors']and N['runtimeHash']==sha(R/'assets/stage5_bomber_assault_1114.js')
assert all(q['pass']for q in G['checks'])and not any(G[k]for k in ['pageErrors','consoleErrors','HTTPerrors'])
assert all(q['passed']for q in T['checks'])and not T['errors']and not V['errors']and not V['stats']['tapErrors']and V['stats']['cues']['retinaLockBeep']>=10
assert all(sha(R/n)==h for n,h in V['hashes'].items())and sha(O/'bomber-retina-rotation-flash-beeps.mp4')==V['movieSha256']
assert A['exactFrames']==256 and not A['errors']and B['helpers']and len(B['nativeCells'])==16 and not B['errors']
protected={n:h for n,h in I['protected'].items()if n!='assets/difficulty_rules_1101.js'};assert all(sha(R/n)==h for n,h in protected.items())
passes=F[-1]['passedLines'];native=len(N['checks'])+len(G['checks']);target=len(T['checks']);seconds=float(V['media']['format']['duration'])
page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Green checks and bomber targeting</title><style>body{{max-width:1280px;margin:24px auto;padding:0 16px;background:#08121c;color:#edf6ff;font:17px/1.5 system-ui}}video{{width:100%;background:#000}}a{{color:#91d9ff}}</style><h1>Full checks: {passes:,} passed, zero failures</h1><p>The bomber's own targeting ring rotates and flashes continuously during tracking, with repeating warning beeps that accelerate toward commitment. It turns red and holds the committed target just before firing, then cools and reacquires.</p><video controls preload="metadata" src="bomber-retina-rotation-flash-beeps.mp4"></video><p>{seconds:.1f}-second native Furious attack checkpoint, real shared sound, invulnerable review pilot. {native} native bomber/weapon checks and {target} new targeting checks pass. The full suite reaches its final zero-error summary. This verifies code and the shown behavior; Mike's home playtest still covers the complete experience.</p><p><a href="README.md">Changes and verification</a> · <a href="full-suite.log">Full test output</a></p></html>'''
(O/'playback.html').write_text(page,encoding='utf-8');seeks=[];errors=[]
with sync_playwright()as pw:
 br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1400,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.goto((O/'playback.html').as_uri());p.wait_for_function('document.querySelector("video").readyState>=2')
 for f in [.10,.45,.85]:
  q=p.evaluate('''async f=>{const v=document.querySelector('video');v.currentTime=v.duration*f;await new Promise((r,j)=>{v.addEventListener('seeked',r,{once:true});setTimeout(()=>j(Error('seek timeout')),10000)});await v.play();await new Promise(r=>setTimeout(r,120));v.pause();return{width:v.videoWidth,height:v.videoHeight,error:v.error?.message||null,at:v.currentTime}}''',f);assert q['width']==1280 and q['height']==844 and not q['error'];seeks.append(q)
 p.screenshot(path=str(O/'playback-preview.png'),full_page=True);br.close()
assert not errors
readme=f'''# Full checks green and active bomber retina — November14,2026

Mike requested the health-helper crash fixed, all full checks passing before release readiness, and a bomber retina that keeps beeping, rotating and flashing until it is about to fire.

The full _BUILD_SOURCE/test_fl.js runner now reaches its final summary with **{passes:,} passing assertions, zero failures and exit0**. The game syntax check and all11 changed JavaScript/test sources parse. The full exact log is full-suite.log. Earlier attempt logs are retained and are superseded by this completed final run.

## Shared health-helper fix

The live game had the difficulty helpers in the late difficulty_rules_1101.js owner, while the old headless bootstrap never loaded that file. The first crash was difficultyHealthBaseline15; fixing that exposed the same missing DR15 shared state farther into the suite. assets/difficulty_helpers_1114.js now supplies the same pure math and shared DR15 data before game.js in both index.html and the test runner. The late rules file attaches its existing EHP/encounter callbacks and live tuning to that shared owner. Normal/Hard/Furious compound15% math, Easy legacy health and interval values, rounding and minimum health are unchanged. Nine new regression assertions exercise all four difficulties, explicit keys and the minimum-health boundary. The native browser confirms early and late helpers share one owner. The actual miniboss's original full pools and native damage behavior still pass across all four difficulties.

## Failures uncovered after removing the abort

The first complete run exposed12 failures rather than hiding them behind the early exception. Each was repaired against current source behavior, without deleting or skipping assertions:

- Stage2's current authored route schedules nine original volcanic roles plus cinderwasp, basalt bomber, lava snake and fire jet. The legacy soak still demanded eye/crawler/golem, and its separate source assertion demanded the replaced magma orb. The110-second soak and roster assertions now require the actual nine scheduled roles and current thirteen-type plan, and still reject retired roles/foreign aliases.
- The sixteen original Armored Leech attack/roll cells had been moved into UNUSED_ASSETS/cleanup_2026-10-06 but remained referenced by the base fleet/manifest. They are recovered pixel-exactly into their own small stage8_leech_recovery_1114.png atlas with complete live cell/root registration. The archive and all other atlases remain intact. All16 cells decode at256x256 through actual XART. Newer encounter art owners remain intact.
- The old miniboss flash test searched for a literal b.flash=0.18 that the real markHit owner had replaced. It now applies actual native damage and checks both HP loss and a flash lasting at least.18seconds. Existing rendered damage/expiry checks remain.
- Help already clamps every label and fit result to HELP_MIN>=11. Its source test now verifies those effective rendering clamps rather than rejecting a smaller requested size that is never drawn at that size.
- The current selected Stage8 importer contains96 actor/effect frames plus4 crystal chunks. The stale assertion demanded104. It now requires the actual100 and checks every sheet exists on disk.
- The approved October24 Chronus order is dialogue → native armor activation → combat. Two tests still required the superseded opening jump. They now verify the current direct handoff and that armor completes before combat attacks. Production Chronus formation, wave and attack owners remain untouched.
- Each alternate StageX route fixture now starts with a fresh campaign pending-route record, rather than inheriting a completed previous route. Campaign controls tests follow the current Start-confirm/Back-toolbar behavior. The final input fixture also uses the native logical confirm API because earlier tests deliberately stub the public Input.tap method. Toolbar protection, alternate route save/load, full encounter and return checks remain; the added Back assertion raises coverage.

## Rotor/flash/beep targeting

S5B14 now plays the existing decoded retinaLockBeep through the shared mixer repeatedly while tracking. Its owner clock starts at.18-second gaps and accelerates toward.085seconds as the lock approaches commitment. There are no detached timers. At the existing.38-second pre-fire commitment the beeps stop and the optic holds red at the committed aim; real cannon bursts, cooling and reacquisition keep their owner. Breaking both cannons, pausing, leaving combat or losing the last live pilot stops further scheduling. Tracking falls back from an out/dead target instead of following an unavailable seat. Player Retina/input ownership stays separate.

The ring's rotation and flash are authored frames: eight original tracking poses × sixteen prepared headings × two palette brightness states =256 fixed80x80 cells with pivot[40,40]. Every frame retains a completely empty20x20 center and binary alpha. Gameplay selects frames at32 heading steps/second and alternates bright/dim authored palettes; it adds no runtime rotation, tinting, opacity effects or generated shapes. Locked red/cooling visuals retain their existing bank. All256 frames roundtrip exactly through the new editable Aseprite document. These are prepared variants of the approved optic, not256 new generated designs.

{native} native bomber/weapon checks pass across all four difficulties, plus{target} focused targeting checks. These cover continuous heading/flash changes, accelerating owner-timed beeps, committed target/quiet pre-fire window, cannon-break cancellation, pause, actual real-clock burst/cool/reacquire, unchanged full HP and no browser update/draw errors. The native XART/early-late-helper probe and all changed-source syntax checks also pass.

The {seconds:.1f}-second H264/AAC preview contains{V['stats']['cues']['retinaLockBeep']} real mixer beep calls, actual native tracking/burst/cooling/reacquisition, non-silent mixer output and source-hash continuity. It uses a prepared Furious checkpoint and an explicitly labeled invulnerable review pilot. Full media decoding and three playback seeks pass. Open playback.html. This is a targeted behavior preview, not an unassisted clear or release certification. Mike's home playtest remains the complete experience/balance check; nothing has been published or installed as a release.

## Recovery

The production changes are the early shared helper, the late owner's helper relocation, the Stage5 controller/metadata and new tracking sheet, recovered leech sheet/registration, their script includes and corrected regression fixtures. assets/game.js stays byte-identical, including its line endings. The test runner keeps CRLF. Critical original Chronus formation/wave and current Draconus normal/Chromium/rage/ship/gun owners stay byte-identical.

Source/evidence: _BUILD_SOURCE/release_checks_1114 and docs/qa/release_checks_1114. Exact original snapshots, repair-before files, native source identities, exporter, atlas input hashes and the new editable Aseprite source are retained. The existing Stage5 source package has this follow-up under updates/retina_cues_1114. This supersedes its earlier missing-health-helper warning and16-frame-only tracking presentation. Do not rerun the old Stage5 installer/builder/finish step by itself over this follow-up: rebuild old base banks first if needed, then run this follow-up's art.py / author.py / install.py / repair.py and all checks. Local paths/review dependencies require the existing project. No commit, push, installer or publication.
'''
for p in[O/'README.md',R/'docs/RELEASE_CHECKS_RETINA_1114.md']:p.write_text(readme,encoding='utf-8')
source=R/'_BUILD_SOURCE/release_checks_1114';source.mkdir(exist_ok=True)
for p in W.iterdir():
 if p.is_file():shutil.copy2(p,source/p.name)
ex=source/'exports';ex.mkdir(exist_ok=True)
for p in(W/'exports').iterdir():
 if p.is_file()and p.suffix in ['.aseprite','.webp','.png']:shutil.copy2(p,ex/p.name)
(source/'README.md').write_text(readme,encoding='utf-8')
update=R/'_ART_SOURCES/stage5_bomber_assault_1114/updates/retina_cues_1114';update.mkdir(parents=True,exist_ok=True)
for p in[W/'art.py',W/'author.lua',W/'author.py',W/'author-manifest.json',W/'tracking-art-audit.json',W/'editable-verification.json',W/'stage5_bomber_assault_1114.js',W/'stage5_bomber_assault_art_1114.js',W/'exports/retina_tracking_1114.aseprite',W/'exports/retina_tracking_1114.webp']:shutil.copy2(p,update/p.name)
(update/'README.md').write_text(readme,encoding='utf-8')
qa=R/'docs/qa/release_checks_1114';qa.mkdir(parents=True,exist_ok=True)
for p in[O/'full-results.json',O/'full-suite.log',O/'checks.json',O/'weapon-gate/weapon-gate-checks.json',O/'targeting-checks.json',O/'asset-helper-checks.json',W/'editable-verification.json',W/'repair-report.json']:shutil.copy2(p,qa/p.name)
paths=['assets/difficulty_helpers_1114.js','assets/difficulty_rules_1101.js','assets/stage5_bomber_assault_1114.js','assets/stage5_bomber_assault_art_1114.js','assets/stage8_leech_recovery_1114.js','assets/game/levels/stage_05/miniboss/assault_1114/retina_tracking_1114.webp','assets/game/levels/stage_08/enemies/atlas/stage8_leech_recovery_1114.png','index.html','_BUILD_SOURCE/test_fl.js','_BUILD_SOURCE/test_difficulty_helpers_1114.cjs','_BUILD_SOURCE/test_mutator_1003.cjs','_BUILD_SOURCE/test_stage8_1003.cjs','_BUILD_SOURCE/test_campaign_focus_1004b.cjs','_BUILD_SOURCE/test_campaign_controls_1004h.cjs']
summary=dict(fullPasses=passes,fullFailures=0,fullExit=F[-1]['exit'],nativeChecks=native,targetingChecks=target,editableFrames=A['exactFrames'],recoveredCells=16,changedSyntaxSources=len(B['syntax']),movieSeconds=seconds,realMixerBeeps=V['stats']['cues']['retinaLockBeep'],movieSha256=V['movieSha256'],sourceHashes={n:sha(R/n)for n in paths},protected=protected,playbackSeeks=seeks,errors=errors)
(O/'verification.json').write_text(json.dumps(summary,indent=2));(qa/'verification.json').write_text(json.dumps(summary,indent=2))
note=f'''## November14,2026 — Full suite green; continuous bomber lock warnings

Mike requested the missing health-helper error fixed and all full checks passing.
The early shared difficulty_helpers_1114.js now owns pure math/DR15 state; late
rules attach live tuning. Original health and15% rules remain. The full runner
reaches its final summary: {passes:,} passed,0 failures,exit0.12 exposed failures were
fixed: exact archived leech cells restored with live roots, current roster/intro/
font/frame-count assertions, isolated alternate-route fixtures and real input API.
No tests are skipped. Native game.js and critical Chronus/Draconus owners remain.
Bomber target optic continuously rotates/flashes in256 authored variant cells and
repeats accelerating shared-mixer beeps while tracking; red lock commits and goes
quiet. Pause/cannon break/target loss cancel scheduling.60 native bomber/weapon
checks,7 cue checks,16 native recovered-cell decodes and syntax all pass. New
audible Furious preview is a labeled invulnerable attack checkpoint; home playtest
is still the full experience check. Source only; no release publication.
Docs: docs/RELEASE_CHECKS_RETINA_1114.md; _BUILD_SOURCE/release_checks_1114.
This supersedes earlier missing-helper/full-suite warnings and the old static optic.

'''
p=R/'HANDOFF_CODEX.md';b=p.read_bytes()
if note.splitlines()[0].encode()not in b:assert p.read_bytes()==b;p.write_bytes(note.encode()+b)
rule='''\n\n## November14 — early difficulty owner and active enemy targeting cues

Mike requires full checks green before readiness and continuous beeping/rotation/
flashing for Stage5's enemy laser retina until pre-fire commitment. Keep shared
difficulty_helpers_1114.js before game.js in browser and headless bootstrap; late
difficulty_rules_1101 attaches its existing live tuning to the same DR15 state.
Preserve original HP/compound15% math. Never reintroduce duplicate late helpers.
Keep native owner-timed repeated beeps, quiet committed red aim and authored256-cell
rotation/brightness library with an empty center; no runtime raster transforms.
Keep cannon-break, pause and exit cancellation. Preserve16 exact restored leech
cells/live root registration and current-spec regression coverage. Don't restore
old opening-jump/retired-roster tests or let fixture state leak between routes.
Full suite now passes8,969 assertions with0 errors. Evidence/rebuild and the
targeted audible preview are in docs/RELEASE_CHECKS_RETINA_1114.md. Do not rerun the
old Stage5 base builder/installer alone over this follow-up. No release published.
'''
p=R/'AGENTS.md';b=p.read_bytes()
if rule.splitlines()[2].encode()not in b:assert p.read_bytes()==b;p.write_bytes(b+rule.encode())
with zipfile.ZipFile(O/'BOF-health-helper-and-retina-sources.zip','w',zipfile.ZIP_DEFLATED,compresslevel=3)as z:
 for p in source.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(source))
assert all(sha(R/n)==h for n,h in protected.items())
print('Saved green full suite:',passes,'passes;60 native and7 targeting checks; audible preview and recovery sources.',flush=True)
