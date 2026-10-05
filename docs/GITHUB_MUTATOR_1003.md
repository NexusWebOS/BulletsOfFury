# October 3 — downloaded Claude build and selected Monster Mutator integration

Claude's latest fetched branch is `origin/claude/epic-clarke-rtfnuk`, commit
`d69cffa4e928785e069c940073f4231eabac3d92`. Its two changes after the shared
`d19c9666` base bring the Hammer arrival/damage/recovery changes, Stage 6 stealth
flights, team dialogue/turbulence, the pink Fusion beam and icon ink normalization.

The incoming delta was inspected and imported into the existing working tree.
Local HEAD remains `938d107937588370393829bbc80e48296ddac9e4`; this is **not a Git
fast-forward or a new commit**. Nothing was pushed. Existing local encounter,
HAMA, Stage 8 and art-revision work was preserved. Temporary before-snapshots,
the local diff and the import ledger are under `_shots/github_download_1003/`.
The portable ledger and verification results are in `docs/qa/mutator_1003.json`.

## Resolving the independently authored October 2 layers

Both branches had created files with the same names. The local campaign repair
layer remains `assets/feedback_1002.js`. Claude's incoming layer is preserved as
`assets/feedback_claude_1003.js`, its assertions as
`_BUILD_SOURCE/test_feedback_claude_1003.cjs`, and its notes as
`docs/CLAUDE_FEEDBACK_1002.md`. Those older notes still describe their original
paths; use the names here when reproducing the combined build.

`assets/build_integration_1003.js` gives the imported live Hammer dialogue sole
ownership of the arrival, preserves Mike's trap/Legion/Earth taunt, and starts
the requested warned jump afterward. Chromium activation waits until the jump,
landing recovery and return finish. The natural arrival was verified through
`flyby → return → unfold → warn → leap → recover → back → shield → fr_activation
→ hammer`. The world keeps scrolling during dialogue; control resumes afterward.
HAMA and HAMMER password encounters retain their separate choreography.

## Selected enemies now in authored waves

Only IDs **01, 03, 04, 06, 07, 08 and 11** are integrated. The other eight
candidates stay art-only. Existing wave times and counts remain unchanged.

| Stage | Existing slot | Approved revision | Attack and counterplay |
| --- | --- | --- | --- |
| 7 | `s7sampler` | Rifle Locust — neon-red hull, pink joints, charcoal guns | Alternating aimed rifle burst. Two rifles and two pods animate independently and can be destroyed; losing both rifles disarms it, losing pods slows it. |
| 7 | `s7lamprey` | Hellram — green flesh, black armor, yellow eyes/plasma, no wrist triangles | Warned straight ram, visible withdrawal, two heavy plasma shots. |
| 7 | `s7serpent` | Hellhugger — core, four claws, thruster | Fragile kamikaze; committed warning, fast claw lunge, recovery and departure. Destroying both foreclaws interrupts the rush. |
| 8 | `s8manta` | Blue Hybrid — blue armor, black tissue, four sensors/vertical maw | Warned five-ball cold-plasma fan. |
| 8 | `s8scout` | Hexpyre — black chassis, no spikes/central eye | Two independently animated/destructible arms, each producing a committed local ground-burst warning. Breaking an arm cancels its hazard. |
| 8 | `s8needlejet` | Imp Harrow — red eye | Two offset fireballs with a delay between releases. |
| 8 | `s8gunship` | Furnace Maw — orange armor, red/white eye, no shoulder fins | Alternating left/right heavy three-ball batteries with a recovery window. |

The existing Stage 8 gravity, Retina-targeting and code-laser aliens remain.
Hull orientation stays upright. Weapon poses supply the render, projectile
origins, lock points and part-hit geometry. Actual curved Retina missiles hit
the modules. Detached parts use the authored component pixels, followed by
native explosions and sounds; debris is capped and cleared on stage transition.
Simultaneous warnings/attacks are limited by difficulty.

`assets/mutator_1003.js` owns behavior and three modular rigs. The only new
mutator edit in `assets/game.js` is its controller dispatch case; the other
game.js delta is Claude's Chromium hit-flash fix. `assets/mutator_art_1003.js`
and `assets/game/mutator_1003/manifest.json` are generated together by
`python _BUILD_SOURCE/build_mutator_1003.py`. The importer copies ten approved
PNGs without changing pixels and records their source hashes and measured
rectangles/pivots. It does not edit or repack shared atlases.

## Verification

- `node --check assets/game.js` and checks of the new runtime scripts pass.
- `node _BUILD_SOURCE/test_fl.js`: **6,554 passing assertions, exit 0**, final
  `FALVA/LIZZIE BUILD OK, 0 ERRORS` banner. The imported-build baseline before
  the new roster was 6,444 passing assertions.
- `_BUILD_SOURCE/probe_mutator_1003.py`: **76 native Chromium checks** pass.
  Covers all seven enemies on Normal/Hard/Furious, actual authored wave
  callbacks, generated art through XART/game-context drawImage, curved Retina
  damage to a rifle, detached module retirement, ordinary bullet/hull collision,
  warning/release sound hooks, and live dialogue ownership. Easy state paths
  are covered by the assertion suite.
- Existing Stage 8 probe: **42 checks** pass, including sword sequence, full
  binary wall collision, beam damage/escape, possessed host lasers, 16 radial
  shatter fragments and straight orbital motion.
- Existing hooks-only HAMA probe: **14 checks** pass using real decoded media
  playback, timing, captions, loop/exit and separate HAMMER remix.
- Claude's stealth-flight probe passes with all three roles and old spawn
  routes; Fusion/icon probe passes for space/Cole beam art and 256 icon samples.
- Extended incoming Hammer-arrival probe passes the complete automatic
  dialogue, first jump/return, armor activation, control release and portraits.
- Actual warning, attack, module-break and hit-flash screenshots were inspected.
  The seven-enemy review passes image/control/link/mobile checks. No final probe
  reports a page or console error.

Earlier nonzero results are retained, not hidden: the first roster suite failed
six assertions (a pre-existing randomized road-tank heading check, four Hexpyre
fixture counts that incorrectly expected only one cast cycle, and excess
Hellhugger HP). The fixture now accepts complete two-mark cast cycles;
Hellhugger's late-stage HP scaling is corrected. The road-tank assertion passed
both later complete runs without modifying that test or its runtime. The first
native roster probe also exposed Hellram's point-blank follow-up being blocked;
its explicit backstep fixes that. Its old boss fixture slug was corrected.
The first full-arrival probe exposed armor activation replacing the opening
jump and a short timeout after the added taunt; both are corrected and its exit
code now reflects assertion failures.

These are controlled native encounters, **not full campaign clears or a final
difficulty/balance certification**. Enemy attack audio was verified through
native sound hooks; HAMA additionally used real audio playback capture.

## Review and reproduction

- Play: `http://127.0.0.1:8794/index.html?build=d69cffa4-mutator-1003`
- Gameplay review: `_shots/mutator_gameplay_1003/review.html`
- Art/component review: `_shots/monster_mutator_v2_1003/review.html`
- Gameplay review builder: `python _BUILD_SOURCE/review_mutator_gameplay_1003.py`
- Native probes use `_BUILD_SOURCE/shoot.py` and real Chromium. Generated review
  captures/logs stay under ignored `_shots/`; portable evidence remains in
  `docs/qa/mutator_1003.json`.
