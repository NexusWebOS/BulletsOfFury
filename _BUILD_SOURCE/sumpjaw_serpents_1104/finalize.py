from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');V=W.parent/'BOF-Furious-Boss-Videos-1104';Q=R/'docs/qa/sumpjaw_serpents_1104';Q.mkdir(parents=True,exist_ok=True);S=R/'_BUILD_SOURCE/sumpjaw_serpents_1104';S.mkdir(parents=True,exist_ok=True)
for p in W.glob('*.py'):shutil.copy2(p,S/p.name)
M=json.loads((W/'authored/manifest.json').read_text());P=R/'_shots/boss_comparison_1102/sumpjaw-serpents-final-1104';job=json.loads((P/'batch.json').read_text())['jobs']['stage7-mini'];assert job['passed'];film=json.loads((R/job['folder']/'report.json').read_text())
for a,b in [(W/'probe/report.json','native-checks.json'),(W/'art-checks/report.json','art-checks.json'),(W/'full-suite.log','full-suite.log'),(W/'profile/uncaptured-sumpjaw.json','performance.json'),(V/'preview-checks.json','preview-checks.json')]:shutil.copy2(a,Q/b)
summary=dict(native=json.loads((Q/'native-checks.json').read_text())['checks'],art=json.loads((Q/'art-checks.json').read_text()),recording=job,audio=film['audio'],sourceHashes=film['sourceHashes'],performance=json.loads((Q/'performance.json').read_text()),preview=json.loads((Q/'preview-checks.json').read_text()),gameSHA256=hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest(),artSource='Existing approved SJ98 PixelLab body_01 source, isolated and articulated offline; no new generation credits spent.',limits='Native GOD/input-only isolated fight, not full campaign or human dodgeability certification. Broad suite exits1 on existing difficultyHealthBaseline15 VM setup error. Uncaptured profile preceded the final jaw-registration and interrupted-hop recovery adjustment; final movie is source-pinned.')
(Q/'summary.json').write_text(json.dumps(summary,indent=2))
fps=f"{job['nativeFps']:.2f}";seconds=f"{job['seconds']:.3f}"
doc=f'''# Sumpjaw pair — articulated serpents and faster toxic attacks

November4: Mike requested snake-like movement and animation, faster attacks,
leaping over the pilot and around the screen, giant toxic orbs and acid volleys.
`SS116` supersedes the SJ98 animation/attack book for the existing Furious-family
Stage7 pair. Normal/Hard keep Caustic Dredger.

## Motion and attacks

- Both snakes now have independent directional heads and ten trailing armor sections.32 baked headings follow each section's actual path tangent. Continuous curves, circling and full upper/lower-screen travel replace moving a coiled plate between rests.
- The native approved skull, metal texture, green gills and intake mouth remain. Jaw motion, all gill damage combinations, bright source-pixel charge states, white hit frames and separate floor shadows are authored cells. No runtime rotation/scaling/tint/alpha animation.
- One heavy attack at a time, alternating living actors, with a0.24s director gap and0.36s recovery. The seven-turn book mixes leap/orb/acid/circle/leap/acid/orb; the second snake starts at a different offset. The other creature continues moving.
- Pounces warn for0.82s, commit before launch and take0.58–0.88s with a96px arc. Direct strikes target the actual pilot position; alternate pounces travel beyond the pilot. Each spits a giant orb during flight. Head and linked body clear their floor shadows; targets cannot be hit through an airborne peak's shadow.
- Landing Retinas use the exact32-heading open-jaw socket, including its quantization. Direct pounces can damage a stationary pilot through native contact. Landing damage starts on touchdown. Interrupting a low airborne strike settles it onto the floor instead of leaving a floating actor.
- Giant-orb turns release three72px toxic globes at the actual mouth. Acid turns release six rapid triple-shot bursts. Existing shared15% difficulty cadence and NG+ rules apply once; warning/travel durations remain explicit.
- Orb/acid/circle turns have0.68/0.68/0.7s tells, native green/yellow/red warning lanes and shared beeps. All new ordinary toxic ammunition is unshootable from birth; it expires or exits instead of persisting indefinitely.
- Mouth flashes track the turning jaw. Native charge, toxic spit, rush, impact, servo and module/death sounds use existing shared-mixer gates. The live recording has audible reports for all these roles.

## Native encounter ownership

Each creature retains1448Furious HP:25% left gill,25% right gill and50% intake
heart, total2896for the pair. Both gills must break before its own heart opens.
Separate overhead HP bars remain; all native point/beam/Retina damage, white
flashes, individual deaths, rewards and single pair progression remain SJ98-owned.
Native defeat clears launcher-owned rounds and warnings. The new animation
initializer is also exported through the existing diagnostic alias.

## Art and sources

1040fixed even-cell frames in25banks, about9MB of runtime PNGs. The head is
176x176, armor sections48x48, giant orb72x72, acid20x20 and mouth FX80x80.
Common pivots and source-measured sockets are retained. The existing approved
PixelLab body_01 image is the identity source, recorded with its SHA256 in the
manifest. This pass uses source extraction and offline Aseprite authoring; it
does not spend generation credits or claim new PixelLab animations.

- Runtime owner: `assets/sumpjaw_serpents_1104.js`, loaded after existing owners.
- Registry/runtime banks: `assets/sumpjaw_serpent_art_1104.js`, `assets/game/levels/stage_07/miniboss/sumpjaw_serpents_1104/`.
- Rebuild/editable sources: `_BUILD_SOURCE/sumpjaw_serpents_1104/`; run build_serpents.py and install.py in this environment. Existing source remains `_ART_SOURCES/sumpjaw_duo_1031/sources/pixellab/body_01.png`.
- New round art bypasses the PFX13 runtime cleanup/glow/trail generator to preserve its authored pixels. Other projectiles keep their owners. Core game.js remains unchanged.

## Verification and footage

28native checks pass: repeated four-attack books, reachable weak points,
gated hearts, source-pixel hit/expiry, direct pounce danger and exact jaw marker,
airborne target gate, interrupted-hop settlement, finite toxic pressure,
pause/render-only clocks, retry, individual/full defeat and Normal/Hard retention.
All1040frames re-exported through real Aseprite and match runtime visible RGBA
and alpha; all even fixtures are unclipped. No browser/render errors.

Uncaptured40s live profile:59.69FPS, p95frame gap16.8ms, p99gap17ms. That profile
preceded the final jaw-registration/recovery adjustment, using the same art and
attack book. The final full native MP4 fight averaged{fps}engine FPS over
{seconds}s;45s player hold-fire, native GOD and an input-only Cole pilot.
Native2896HP and all weak points/defeats remain live. Source hashes stayed
stable, complete media decode/audio and browser checks pass. Captured engine
FPS includes recorder overhead; video samples at30FPS. This is an isolated
showcase, not a full campaign or human difficulty certification.

Review: http://127.0.0.1:65119/?sumpjaw=serpents-1104#sumpjaw . The preceding
films remain preserved. QA and source hashes: `docs/qa/sumpjaw_serpents_1104/`.

Syntax checks pass. Required `node _BUILD_SOURCE/test_fl.js` exits1before its
final summary on the existing `ReferenceError: difficultyHealthBaseline15 is
not defined` at combat_polish_0927b.js:151 / test_fl.js:4537. The harness was not
modified to mask that setup failure. No commit, push or remote upload.
'''
(R/'docs/SUMPJAW_SERPENTS_1104.md').write_text(doc,encoding='utf8')
taxonomy=R/'assets/data/ART_TAXONOMY.json';data=json.loads(taxonomy.read_text(encoding='utf8'));data['ss116_']=dict(role='furious_stage7_articulated_sumpjaw_serpents_directional_heads_body_segments_jaw_anchored_toxic_attacks',owner='_BUILD_SOURCE/sumpjaw_serpents_1104/build_serpents.py',manifest='assets/game/levels/stage_07/miniboss/sumpjaw_serpents_1104/manifest.json',note='Approved SJ98 source pixels;32 baked headings, source-preserving separate head/body/tail and floor shadows, four gill states, native white hit and toxic shot/muzzle banks. Existing native pair health/gills/hearts/reward retained. No fresh generation charge.');taxonomy.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
note=f'''<!-- sumpjaw-serpents-1104 -->
## November4 — faster articulated Sumpjaw pair

SS116 replaces live SJ98 coiled-plate motion with32-heading heads and ten trailing armor sections, continuous snake curves, circling and96px pounces over the pilot. Alternate direct/overflight strikes use exact open-jaw landing Retinas; fast giant toxic orbs and six-burst acid volleys leave the real mouth with native warnings/audio. Preserve two1448HP native pools, gill/heart gates, individual bars, actual white hits, finite ordnance and once-only native defeat.1040authored/Aseprite-verified frames;28native checks pass. Uncaptured profile59.69FPS; final source-stable native full fight{fps}FPS, audible and complete. Full suite retains its pre-existing missing health-helper setup error. See docs/SUMPJAW_SERPENTS_1104.md; local review http://127.0.0.1:65119/?sumpjaw=serpents-1104#sumpjaw . No commit/push.

'''
for name in['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/name;raw=p.read_bytes();p.write_bytes(note.encode('utf8')+raw)if b'<!-- sumpjaw-serpents-1104 -->'not in raw else None
# Close the prior Thunderhead evidence handoff with its final required suite log.
old=W.parent/'BOF-Thunderhead-Modular-1104/test_fl_final.log'
if old.exists():shutil.copy2(old,R/'docs/qa/thunderhead_modular_1104/full-suite.log')
print('Saved final Sumpjaw sources, art registry, native/media checks and handoff notes.')
