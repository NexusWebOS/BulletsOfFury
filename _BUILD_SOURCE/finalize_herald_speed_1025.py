"""Publish measured evidence for the faster Herald bomber revision."""
from pathlib import Path
import hashlib,json,subprocess
from publish_barrage_revision_1025 import latest

R=Path(__file__).resolve().parents[1];O=R/'_shots/herald_speed_1025'
native=json.loads((O/'probe/report.json').read_text());browser=json.loads((R/'_shots/barrage_revision_1025/browser/report.json').read_text())
film_path,film=latest('herald');cards=json.loads((R/'docs/previews/barrage_revision_1025/review.json').read_text());card=next(q for q in cards if q['id']=='herald-bomber')
assert all(c['passed']for q in [native,browser]for c in q['checks'])and all(film['checks'].values())
furious=next(q for q in native['runs']if q['difficulty']=='furious');duration=furious['plan']['duration'];drops=[sum(b['pass']==i for b in furious['births'])for i in range(2)]
syntax=[]
for name in ['assets/game.js','assets/herald_bomber_1025.js']:
 q=subprocess.run(['node','--check',name],cwd=R,capture_output=True,text=True);assert not q.returncode,q.stderr;syntax.append({'path':name,'exitCode':q.returncode})
suite=subprocess.run(['node','_BUILD_SOURCE/test_fl.js'],cwd=R,capture_output=True,text=True);(O/'full-suite.log').write_text(suite.stdout+suite.stderr,encoding='utf8')
audio={k:v for k,v in film['sound']['playing'].items()if k in ['jetDash','bossfireVileexistence','combatOrb0927','bossWeaponCharge']}
assert all(audio.get(k,0)>0 for k in ['jetDash','bossfireVileexistence','combatOrb0927','bossWeaponCharge']),audio
qa={'scope':'Herald bomber matches corner-flight speed and rapidly drops red energy from both living claws',
 'native':{'passed':len(native['checks']),'failed':0,'report':'_shots/herald_speed_1025/probe/report.json'},
 'browser':{'passed':len(browser['checks']),'failed':0,'report':'_shots/barrage_revision_1025/browser/report.json'},
 'measurements':{'oldFuriousPassSeconds':4.6,'currentFuriousPassSeconds':duration,'speedMultiplier':4.6/duration,'oldDropsPerPass':[3,3],'currentDropsPerPass':drops,'waveSeconds':furious['plan']['interval'],'peakLive':furious['peakLive']},
 'film':{'report':film_path.relative_to(R).as_posix(),'video':film['video'],'seconds':film['timeline'][-1]['seconds'],'decodedPeakDb':film['decodedPeakDb'],'checks':film['checks'],'observedPlayback':audio,'chapters':{k:card[k]for k in ['warning','attack','peak','recovery']}},
 'syntax':syntax,'requiredSuite':{'command':'node _BUILD_SOURCE/test_fl.js','exitCode':suite.returncode,'finalSummaryReached':False,'reason':'Existing missing _BUILD_SOURCE/retired_art_archive_1022.cjs aborts before assertions.','log':'_shots/herald_speed_1025/full-suite.log'},
 'sourceHashes':{name:hashlib.sha256((R/name).read_bytes()).hexdigest()for name in ['assets/herald_bomber_1025.js','index.html']},
 'method':'Real Chromium via shoot.py native loop. Continuous invulnerable Furious film, weapons withheld, native enemy HP and attack-book progress. Explicit damage fixtures are separate.'}
assert suite.returncode==1 and 'retired_art_archive_1022.cjs'in suite.stderr
(R/'docs/qa/herald_speed_1025.json').write_text(json.dumps(qa,indent=2),encoding='utf8')
def stamp(t):return f'{int(t//60)}:{t%60:04.1f}'
doc=f'''# Herald faster bomber passes — October25

[Fresh Furious clip](previews/barrage_revision_1025/index.html#herald-bomber).
The bomber chapter now shows the faster revision in a new continuous 52-second
native film. Existing recordings are preserved.

The bomber used a separate 4.6-second flight and a sequential 0.62-second warning
plus wait before each release. It now travels at the exact world speed of the
diagonal corner swoop. The shorter horizontal route takes {duration:.2f}s on
Furious, {4.6/duration:.2f} times the previous speed.

Both living claws rapidly release animated red energy, with attached energy
muzzle flashes. Furious waves are 70ms apart while the sockets cross the screen.
Measured complete passes release {drops[0]} and {drops[1]} projectiles, versus 3
per pass in the previous film. Selected drops burst into radial chaos; direct
rounds form the falling carpet. All releases use the actual current claw mouths.

The complete carpet is committed during the existing 1.05-second pass warning.
Native green/yellow/red fields show its lanes before takeoff; the carpet and
radial bursts retain an escape opening. Broken claws immediately cancel their
scheduled releases and active rounds. Native HP, hit/Retina, visible white
damage, wing animation, breakup and finite returns remain authoritative.
Projectile budget stays at 128; the focused Furious observation peaks at
{furious['peakLive']}. Launch audio uses the existing shared cue with a 130ms
retrigger gate and silent paired partners. No new artwork was needed.

Film checkpoints: warning {stamp(card['warning'])}, fast pass {stamp(card['attack'])},
red burst {stamp(card['peak'])}, native return {stamp(card['recovery'])}.
The gallery supports slow motion and frame stepping. The invulnerable observation
bot withholds fire; this verifies presentation, not human difficulty.

## Verification

- {len(native['checks'])} native Chromium checks pass across Normal, Hard and
  Furious: measured corner-speed agreement, at least eight drops per pass,
  committed warnings/opening, exact birth sockets, unshootable energy from birth,
  bounded rounds, unchanged observation HP, actual white damaged pixels and
  expiry, broken-claw cancellation and decoded audio routes.
- {len(browser['checks'])} review-browser checks pass for all eight chapters,
  playback/seeking, audio enabled, frame stepping, slow motion and byte ranges.
  The new Herald film fully decodes with {film['decodedPeakDb']}dB audio; actual
  playback includes all four charge/flight/launch/burst cues. No page, console or
  asset errors.
- JavaScript syntax checks pass. Required test_fl.js exits 1 before assertions or
  its final summary because the existing retired_art_archive_1022.cjs helper is
  missing. This is not a full-suite pass.

Evidence: docs/qa/herald_speed_1025.json, _shots/herald_speed_1025/, and
{film_path.parent.relative_to(R).as_posix()}/. Reproduce using
_BUILD_SOURCE/probe_herald_speed_1025.py, record_barrage_revision_1025.py --cases
herald, publish_barrage_revision_1025.py and check_barrage_revision_1025.py.
This pass did not edit game.js/test_fl.js, commit or push.
'''
(R/'docs/HERALD_SPEED_1025.md').write_text(doc,encoding='utf8')
title='## October25 — Herald bomber matches corner speed and drops rapidly'
note=f'''{title}

Mike's faster Herald request is live: bomber world speed equals the corner swoop; Furious passes take {duration:.2f}s instead of 4.6s ({4.6/duration:.2f} times faster). Both surviving claws rapidly drop red energy with native muzzle flashes, 70ms wave cadence and {drops[0]}/{drops[1]} drops per complete pass versus 3/3 previously. Full-pass native warnings commit the carpet and escape opening before flight. Radial bombs remain mixed with direct falling energy; native hits, breakup, cancellation, HP and 128-round budget remain. New continuous audible 52s film replaces the Herald gallery chapters; old takes preserved.

{len(native['checks'])} native Normal/Hard/Furious checks and {len(browser['checks'])} review-browser checks pass. Actual cue playback and full decode verified; no browser/asset errors. Review: docs/previews/barrage_revision_1025/index.html#herald-bomber. Notes/evidence: docs/HERALD_SPEED_1025.md and docs/qa/herald_speed_1025.json. Syntax passes; required suite still exits 1 before assertions/summary on existing missing retired_art_archive_1022.cjs. No game.js/test_fl.js edits, commit or push.

'''
for name in ['HANDOFF_CODEX.md','CLAUDE.md']:
 path=R/name;raw=path.read_bytes()
 if title.encode()not in raw:
  addition=note.replace('\n','\r\n')if b'\r\n'in raw else note
  path.write_bytes(addition.encode()+raw)
path=R/'AGENTS.md';raw=path.read_bytes();rule='- Herald bomber passes match corner-flight world speed; commit the whole drop carpet before the rapid paired-claw releases. Keep the visible red energy, muzzle flashes, escape opening and broken-claw cancellation. See docs/HERALD_SPEED_1025.md.'
if rule.encode()not in raw:path.write_bytes(raw+(('\r\n'if b'\r\n'in raw else'\n')+rule+'\r\n').encode())
path=R/'docs/BARRAGE_READABILITY_1025.md';text=path.read_text(encoding='utf8')
start=text.index('Herald film checkpoints:');end=text.index('\n\n## Ownership and art',start)
text=text[:start]+f'''Herald's faster bomber revision is documented in
[Herald speed](HERALD_SPEED_1025.md): roughly {4.6/duration:.1f} times faster passes,
rapid paired-claw drops and a newly recorded film. Current bomber checkpoints:
warning {stamp(card['warning'])}, fast pass {stamp(card['attack'])}, red burst
{stamp(card['peak'])}, return {stamp(card['recovery'])}. Gallery buttons use the
current film. The Dredger top-lob film retains its complete four-shell Furious turn.'''+text[end:]
text=text.replace('- 48 native Chromium checks pass,','- The preceding readability pass had 48 native Chromium checks pass,')
path.write_text(text,encoding='utf8')
print(json.dumps({'native':len(native['checks']),'browser':len(browser['checks']),'duration':duration,'drops':drops,'audio':audio,'review':card['src']}),flush=True)
