"""Collect current evidence and update only this pass's notes and art registration."""
from pathlib import Path
import json,hashlib,subprocess

R=Path(__file__).resolve().parents[1];S=R/'_shots/barrage_revision_1025'
native=json.loads((S/'probe/report.json').read_text(encoding='utf8'))
sockets=json.loads((S/'sockets/report.json').read_text(encoding='utf8'))
browser=json.loads((S/'browser/report.json').read_text(encoding='utf8'))
review=json.loads((R/'docs/previews/barrage_revision_1025/review.json').read_text(encoding='utf8'))
assert all(c['passed']for report in[native,sockets,browser]for c in report['checks'])
films=[]
for src in dict.fromkeys(x['src']for x in review):
 f=R/src.lstrip('/');q=json.loads((f.parent/'report.json').read_text(encoding='utf8'));assert all(q['checks'].values());films.append(q)
paths=['assets/game.js','assets/bullethell_1025.js','assets/herald_bomber_1025.js','assets/herald_chaos_art_1025.js']
syntax=[]
for path in paths:
 q=subprocess.run(['node','--check',path],cwd=R,capture_output=True,text=True);syntax.append({'file':path,'exitCode':q.returncode});assert q.returncode==0,q.stderr
suite=subprocess.run(['node','_BUILD_SOURCE/test_fl.js'],cwd=R,capture_output=True,text=True)
(S/'full-suite.log').write_text(suite.stdout+suite.stderr,encoding='utf8')
suite_result={'command':'node _BUILD_SOURCE/test_fl.js','exitCode':suite.returncode,'finalSummaryReached':False,
 'reason':'Existing missing _BUILD_SOURCE/retired_art_archive_1022.cjs; aborts at first require before assertions.','log':'_shots/barrage_revision_1025/full-suite.log'}
assert suite.returncode==1 and 'retired_art_archive_1022.cjs'in suite.stderr
def h(path):return hashlib.sha256((R/path).read_bytes()).hexdigest()
qa={'scope':'Stage3 scenery contrast; Stage6 reactor-only barrage; Dredger physical launchers and dorsal lobs; Herald red chaos, corner swoops and claw bombing',
 'native':{'passed':len(native['checks'])+len(sockets['checks']),'failed':0,'reports':['_shots/barrage_revision_1025/probe/report.json','_shots/barrage_revision_1025/sockets/report.json']},
 'browser':{'passed':len(browser['checks']),'failed':0,'report':'_shots/barrage_revision_1025/browser/report.json'},
 'films':[{'case':q['case'],'video':q['video'],'seconds':q['timeline'][-1]['seconds'],'decodedPeakDb':q['decodedPeakDb'],'checks':q['checks']}for q in films],
 'syntax':syntax,'requiredSuite':suite_result,'review':'docs/previews/barrage_revision_1025/index.html',
 'sourceHashes':{p:h(p)for p in paths},'method':'Native observation clips use an invulnerable input bot with no enemy HP or phase writes. Isolated damage/cancellation fixtures are labelled in the probes. This pass did not edit game.js or test_fl.js.'}
(R/'docs/qa/barrage_revision_1025.json').write_text(json.dumps(qa,indent=2),encoding='utf8')

doc='''# October25 barrage readability and Herald flights

Review: [current clips](previews/barrage_revision_1025/index.html). Eight chapters,
six new audible native films. The three Herald chapters share one continuous
52-second film. Earlier recordings remain available; they predate these fixes.

| Encounter | Current behavior |
|---|---|
| Stage3 | Scenery-only black lighting at0.46 strength, after the background pass. The original ice terrain, water clocks and outlines remain. Projectiles, warnings, aircraft and HUD retain their native brightness. Same-frame before/after comparison is included. |
| Stage6 Siege Fortress | Removed the added battery barrage scheduler. All six laser batteries keep their native attacks. Only the exposed reactor receives the added barrage, between complete battery/missile turns. The native all-six-batteries gate, complete HP pool, reactor attacks and miniboss defeat remain. |
| Stage7 Caustic Dredger | Fans use the actual four barrel apertures in each authored gun assembly, with attached toxic muzzle flashes. The previous centre-bottom socket was between barrel mouths. Successive barrage turns alternate with sludge from the top liquid opening: warned arcing lobs, splash, then outward toxic rounds with committed dodge sectors. |
| Stage8 Herald | Round animated red chaos replaces the faint feather rounds. Claws emit the barrage and energy flashes. New warned corner swoops change heading/depth and animate the existing wings. Two Furious bomber passes release red bombs from surviving claws; warned bursts retain a dodge sector. Broken claws cancel their pending bombs, shots and flashes. Native core/head last stand, damage, Retina, white hit feedback and breakup remain. |

Herald film checkpoints: first red volley about0:01.2; first diagonal strike
about0:09.5; bomber flight about0:18.1, with the attack view at0:20.1; bomber
return complete about0:30.7. Gallery buttons use timestamps measured from this
film. The Dredger top-lob film shows its complete four-shell Furious turn.

## Ownership and art

`assets/bullethell_1025.js` owns the reactor interlock, measured Dredger sockets,
turret flashes and bounded dorsal lob turn. Native `tb28` owns its arcs/reticles.
`assets/herald_bomber_1025.js` owns the new Herald flight book, claw sockets,
ordinary red energy, muzzle attachment and Stage3 scenery lighting. Existing
module HP, hit detection and death owners remain authoritative.

The red orb is a palette variant of the eight existing authored
`bpfx_proj_void` frames. All source alpha, neutral armor/outline pixels and bright
glints are preserved. The whole bank uses128×128 cells and a64,64 pivot. Builder:
`_BUILD_SOURCE/build_herald_chaos_1025.py`; registry:
`assets/herald_chaos_art_1025.js`; provenance:
`assets/game/levels/stage_08/miniboss/herald_chaos_1025/manifest.json`.
No generated replacement hulls or paid asset jobs were needed.

Every new launch uses the shared mixer/retrigger gate. Dredger uses
`bossfireSludgeemperor` and `combatToxic0927` (the existing toxic-spit alias);
Herald uses `bossfireVileexistence`, `combatOrb0927`, `jetDash` and the native
charge cue. Fans have one audible launcher. Cancelled launchers retain no delayed
release. Ordinary energy is unshootable from birth and keeps defensive clears.
Projectile budgets are capped at128; warnings commit their openings before fire.

## Verification

-48 native Chromium checks pass, including actual scenery/projectile pixels,
  measured opaque barrel mouths and liquid opening, visible muzzle and hit
  flashes, native flash expiry, decoded attack audio, short return rotations,
  native reactor gate and destroyed-launcher cancellation.
-34 review-browser checks pass: eight chapters, play/decode/seek with audio,
  frame stepping, slow motion and byte-range requests. No page, console or asset
  errors. Six films fully decode, with sound peaks between-8.5 and-6.7dB and
  observed native rendering near60fps.
-`node --check` passes for game.js and all three affected/new runtime registries.
-Required `node _BUILD_SOURCE/test_fl.js` exits1 before assertions or final
  summary: `_BUILD_SOURCE/retired_art_archive_1022.cjs` is missing. This is the
  recorded pre-existing suite blocker; no full-suite pass is claimed.

Observation films retain native enemy HP/phases and use an invulnerable movement
bot; Stage6 companions attack normally. Explicit native-damage/cancellation
fixtures are separate. Human difficulty still needs player review.

Evidence: `docs/qa/barrage_revision_1025.json` and
`_shots/barrage_revision_1025/`. Reproduce with `probe_barrage_revision_1025.py`,
`probe_barrage_sockets_1025.py`, `record_barrage_revision_1025.py`,
`publish_barrage_revision_1025.py` and `check_barrage_revision_1025.py` under
`_BUILD_SOURCE/`. This pass did not edit game.js or test_fl.js, commit or push.
'''
doc=doc.replace('\n+-','\n- ').replace('\n-48','\n- 48').replace('\n-34','\n- 34').replace('\n-`','\n- `').replace('\n-Required','\n- Required')
(R/'docs/BARRAGE_READABILITY_1025.md').write_text(doc,encoding='utf8')

# Preserve every pre-existing byte in shared notes and the taxonomy.
entry={'role':'herald_red_chaos_energy','owner':'_BUILD_SOURCE/build_herald_chaos_1025.py','manifest':'assets/herald_chaos_art_1025.js',
 'note':'Mike Oct25: visible round red chaos from living Herald claws, including bomber drops. Eight authored bpfx_proj_void source frames, red chroma variant only; source alpha, neutral dark metal and bright glints unchanged. Fixed128x128 cells/pivot64,64, one common scale. Native damage/death owners remain. Complete hashes/recipe in game/levels/stage_08/miniboss/herald_chaos_1025/manifest.json.'}
p=R/'assets/data/ART_TAXONOMY.json';raw=p.read_bytes()
if b'"hb25_"'not in raw:
 nl=b'\r\n'if b'\r\n'in raw else b'\n';block=('  "hb25_": '+json.dumps(entry,indent=2).replace('\n','\n  ')+',\n').encode().replace(b'\n',nl)
 start=raw.index(b'{')+1;p.write_bytes(raw[:start]+nl+block+raw[start+len(nl):])
note='''## October25 — Barrage readability, physical Dredger launchers and Herald bombers

Mike's correction is live: Stage3 scenery dims behind all combat; Siege Fortress batteries have no added bullet hell, while the exposed all-six-batteries reactor retains its own turn. Dredger fans cycle measured physical barrel apertures with toxic flashes; alternate turns launch warned arcing sludge from the top liquid opening and splash outward. Herald uses visible round red chaos, warned Phoenix-style corner flights and two Furious bomber passes with energy releases from living claws. Native parts/HP, hit pixels, cancellation, audio and defeat ownership remain. Red art reuses the existing authored eight-frame void orb with exact alpha and fixed128x128 cells.

48 native and34 review-browser checks pass; six fresh audible movies/eight chapters fully decode/play/seek/frame-step. Review: docs/previews/barrage_revision_1025/index.html. Notes and QA: docs/BARRAGE_READABILITY_1025.md, docs/qa/barrage_revision_1025.json. Required suite still exits1 before assertions/final summary because retired_art_archive_1022.cjs is missing. This pass did not edit game.js/test_fl.js, commit or push.

'''
for file in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/file;raw=p.read_bytes()
 if b'## October25 \xe2\x80\x94 Barrage readability, physical Dredger launchers and Herald bombers'not in raw:
  nl=b'\r\n'if b'\r\n'in raw[:2000]else b'\n';p.write_bytes(note.encode().replace(b'\n',nl)+raw)
p=R/'AGENTS.md';raw=p.read_bytes()
if b'## October25 barrage corrections'not in raw:
 nl=b'\r\n'if b'\r\n'in raw else b'\n'
 p.write_bytes(raw+('''

## October25 barrage corrections

- Stage3 lighting dims scenery only; retain native projectile, FOV, aircraft and HUD brightness.
- Stage6 Siege Fortress battery guns have no added bullet hell. The exposed core may use it after the native all-six-batteries gate.
- Caustic Dredger barrages leave measured turret barrel mouths with attached muzzle flashes, or arc from the top liquid opening into warned outward splashes. Never restore the generic gap/bottom launch point.
- Herald uses visible round red chaos energy, warned Phoenix-style corner flights and bomber passes dropping from surviving claws with energy muzzle flashes. Preserve native module damage, hit feedback, cancellation and breakup. See docs/BARRAGE_READABILITY_1025.md.
''').encode().replace(b'\n',nl))
p=R/'docs/previews/bullethell_1025/index.html';raw=p.read_text(encoding='utf8')
if 'barrage_revision_1025/index.html'not in raw:
 notice='<p style="margin:0;padding:14px 32px;background:#254438;color:#e8fff7">Updated October25: <a href="../barrage_revision_1025/index.html">current Stage3 contrast, Stage6 reactor, Dredger launchers and Herald flights</a>. The clips below are the earlier captures.</p>'
 p.write_text(raw.replace('</header>','</header>'+notice,1),encoding='utf8')
print(json.dumps({'nativePassed':qa['native']['passed'],'browserPassed':qa['browser']['passed'],'verifiedFilms':len(films),'requiredSuiteExit':suite.returncode}),flush=True)
