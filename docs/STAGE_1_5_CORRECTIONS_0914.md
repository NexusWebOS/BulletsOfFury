# Stage 1–5 corrections — September 14, 2026

Mike requested this pass after the four-weapon graphics and sound update. His
clarifications were that surviving stage-1 fodder should burn at half health,
and that space Volley Missiles should behave like the passive homing upgrade
while keeping their authored space ordnance style.

## Encounter changes

- **Stage 1:** Fodder always draws its clean authored hull. Living enemies at
  half health draw animated fire and rising, fading smoke; quarter health adds
  a second vent. Death effects remain owned by the existing death sequence.
  Razorback has its own suppression, pressure windup/release, rocket and ram
  reports. Overlord guns, rockets, lances, wind attacks and charge have dedicated
  cues, with a continuous rotor bed that expires when the encounter ends.
- **Stage 2:** Projectile sheet rows that depict birth and growth no longer
  cycle as misaligned flight animations. A reviewed full flight pose stays
  fixed, with a moving pixel light band. Inferno ordnance also retains one flight
  frame. Direction and existing movement patterns remain intact.
- **Stage 3:** Ten planned barge spawns are stored in
  `STAGE3_STORED_BOATS_0914.json`; their art and controllers remain available.
  Ordinary ice-drone shots use larger authored blue flight plates with dark
  outlines, retaining their original velocities and collision dimensions.
  Rime Wall now fires every laser pattern only from the measured left, center
  and right cannon tips. The center uses the authored FOV warning and a laser
  charge. The whole boss plate remains intact.
- **Stage 4 miniboss:** Olive Warden cycles mounted spread machine guns,
  centered dual straight machine guns and mounted rocket salvos. Bullet and
  rocket art, flashes and sounds follow the actual hardpoints. The blue hull
  chaingun attachments are removed. Rockets have a visible rack charge and are
  shootable. Machine rounds use the reviewed orange tracer frame `mgcf_1_5`.
- **Stage 4 boss:** Sovereign helpers sit outside its shield over the two
  generator columns, fitting inside the actual 480-pixel camera. The whole
  carrier plate is scaled to 264 pixels; its shield and four generator sprites
  remain authored art. A wide held laser damages both generator nodes in a
  column on the same tick, and also reaches live helpers within its finite
  beam. The shield still protects the carrier until all generators are down.
  The unpowered boss warns its dive, clears its entire hull below the screen,
  flies overhead with a shadow made from the current flight frame, then returns
  through the opposite edge. The overhead pass cannot cause a ground-plane
  hull collision. Helpers retain their independent attack pressure. Their gun,
  heat, windup and laser sounds now use authored encounter reports.
- **Stage 5:** The sky portion lasts five seconds before the transformation,
  and scenery keeps scrolling through launch and the boss fight. The selected
  pilot uses the finished authored spaceship. Volley Missiles launch immediately
  as three independent passive homing rounds from the two sides and nose, retain
  corresponding left/center/right locks, and reacquire forward targets when
  needed. Forced crossover and seed behavior are removed from active firing.
  Laser Cannon's own sound gain is 0.30; Shadow Orb's direct and inherited
  detonation payloads are 35% stronger. Regent's formation stays centered, its
  escorts visibly charge before firing along a locked direction, and each grid
  row warns its next opening. The encounter reserves sound-effect headroom at
  gain 0.40 while preserving voice gain and the player's sound preferences.

Twenty-four encounter sound routes reuse the existing authored bank, with their
own gain, filter and retrigger gates. No atlas, art asset or manifest was rewritten.
Small contact effects and Volley impacts retain their explosion layers while
using one gated impact report instead of stacking generic explosions underneath.

## Verification

- `node --check assets/game.js` passes. Runtime LF and suite CRLF are preserved.
- Complete `node _BUILD_SOURCE/test_fl.js`: **3,724 passed / 61 failed, exit 1**.
  It reaches its final summary. All 61 assertion names match the preceding
  `docs/qa/weapon_feedback_0913.json` baseline after normalizing changing numeric
  observations. All 21 new section-299 assertions pass. Six older fixtures were
  updated to reflect the requested clean stage-1 hull, independent space missiles,
  dedicated encounter sounds and quieter cannon. The remaining failures predate
  this pass; this is not a clean full-suite result.
- Real Chromium: **42 passed / 0 failed**, zero page, console or controlled-loop
  errors. The probe uses `shoot.py`'s controlled frames, polls lazy assets and
  yields between batches. It checks actual `XART.get` keys and game-context
  `drawImage` calls; screenshots were inspected. Actual held laser input destroys
  both nodes in one column while leaving the other column alive. The native sky
  scene stays in its extended portion for three seconds while visibly scrolling.
- The sources reconstruct the runtime byte-for-byte. Complete checks, baseline
  assertion names, hashes and native observations: `docs/qa/stage_1_5_0914.json`.

## In-game preview

`_shots/stage_1_5_0914/video/BulletsOfFury_Stages_1_to_5_0914.mp4` contains
**76 seconds, 2,280 fully decoded frames, 960×1024 at 30 fps**, H.264 video and
48 kHz stereo AAC sound. Ten native game cuts show the requested changes:

| Time | Scene |
| --- | --- |
| 0–5s | Half-health fodder fire and smoke |
| 5–11s | Razorback suppression and pressure attack |
| 11–17s | Overlord weapon sounds |
| 17–21s | Stable stage-2 projectile flight poses |
| 21–25s | Visible ice-drone shots |
| 25–31s | Stage-3 cannon warning, charge and lasers |
| 31–40s | Warden's three gun and rocket acts |
| 40–52s | Sovereign helpers, paired generator piercing and complete flyover |
| 52–66s | Extended authored sky and spaceship transformation |
| 66–76s | Regent formation, row warnings, Laser Cannon, Shadow Orb and passive volleys |

The demo pilot is protected from damage. Native debug encounter setup selects
attack windows; the Sovereign demo starts after its 75% and 50% health gates with
1-HP generators so actual held laser input can show both columns breaking within
the cut. Gameplay health gates are unchanged. Music is not included. Accepted
game sounds, loops and game-module cues are aligned to captured frames, without
export-only normalization. Every sound-effect mixer render peaks below 1.0;
the densest Regent cut peaks at 0.7932. Existing voice-pool reuse during rapid
fire is reproduced, rather than reported as zero voice cuts.

The local audio exporter also fixes the inherited recorder's scheduling of
game-module noise: Chromium's `AudioBufferSourceNode.start` overload must be
pinned alongside its parent method. Earlier diagnostic renders that accidentally
started these noise cues at time zero are not evidence of live-game clipping.

## Sources and safe reproduction

`_BUILD_SOURCE/stage_1_5_0914/` contains `runtime.js`, `integrate.py`,
`append_tests.py`, `inspect_art.py`, `probe.py`, `record.py`, `audio_export.py`
and `validate.py`. The actual game remains self-contained in `assets/game.js`.
The ignored `_shots/stage_1_5_0914/` holds the exact pre-pass dirty runtime and
suite, comparison artifact, complete logs, art inspection and screenshots.

Run `integrate.py --dry-run` to create only the comparison artifact. The mutation
path accepts the archived before-runtime or the exact reconstructed runtime and
refuses subsequent edits. `append_tests.py` similarly refuses subsequent suite
changes. Do not run older integration scripts over this newer build. A fresh
source change should be compared and integrated deliberately rather than
overwriting work. `record.py --resume` reuses completed takes; remove only a
specific stale take's report entry when deliberately recording that changed
scene again. `validate.py` collects proof after the current suite, probe and
recording finish.

Existing staged, unstaged and untracked work, previous recordings and trailer
scratch remain preserved. No GitHub changes were integrated. Nothing committed
or pushed.
