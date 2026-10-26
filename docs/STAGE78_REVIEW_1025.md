# October25 — Furious review, Warden walking and Dracodia download

Mike requested a timestamped audit of the recorded Furious Stage7/8/9 fights,
then explicitly chose **Analyze and implement in this pass**. The review is
`docs/FURIOUS_789_REVIEW_1025.md`, with 24 observations and clickable markers in
the preserved original-video review. Original timestamps always refer to those
original MP4s, not the revised captures or the in-game BOSS clock.

The latest rebirth presentation is now owned by
`assets/dracodia_download_reveal_1025.js`: the rotating carrier downloads the
actual live final body with continuous pose and size through the reveal. See
[rotating download and fresh clip](DRACODIA_DOWNLOAD_REVEAL_1025.md). The full-fight
films below predate this focused rebirth revision.

## Creative contract

Mike's new first-host arm direction supersedes the older October24
darken-in-place behavior **for the infused first host only**. Destroyed arms
explode, detach and shatter into their actual authored pixels. The other four
copied forms retain their native designs and separate combat ownership.

The Stage7 motion reference was inspected at
[Raiden II, 02:52](https://youtu.be/1oj6zi1ZfNw?t=172). Its useful cues are
alternating grounded support, planted toes, bent-knee recovery and a stable body
heading. The Warden retains its own bronze/olive armor, green windows, joints,
independent parts, HP and authored jump/swipe attack art.

## Runtime and assets

Final owner: `assets/stage78_review_1025.js`, loaded after boss_integrity and the
Chronos owners. `assets/game.js` and `_BUILD_SOURCE/test_fl.js` are untouched.

- Four SpriteCook v1.5 walking banks, eight poses each. Fixed 256 cells, common
  hip pivots, translation-only hip registration and one proportional world
  scale per bank. Ground distance drives diagonal gait pairs. Support toes
  remain fixed in world space during stance. Body steering, native claw paths,
  projectiles, FOV and real hit masks share the same world transform.
- Walking occupies the intervals between attack groups. Native warning times
  remain intact. Two of every three automatic swipe-to-jump continuations now
  recover on the ground, allowing the spider motion to be seen.
- New walking cells use actual alpha for collision; transparent padding is
  unhittable. Retina targets are measured on opaque toes in every pose.
- Native hit timers are retained. A pulse envelope returns authored colors
  between repeated hit pulses. First-host white flashes use only the damaged
  arm/core's actual alpha. The final main plate and Volcano draw retain their
  complete silhouettes with the same readable pulse envelope.
- First-host eye sockets are measured in all 45 connected poses. An eight-pose
  red/white aperture flare covers the eye, sharing the native animated laser's
  root. Claw wind-up holds the raised pose through firing. One measured socket
  owns its FOV origin, ordinary rounds, alternating physical rockets and native
  muzzle flashes. Rockets remain interceptable; ordinary rounds retain their
  native offensive-interception rules.
- Both 33.3% arms remain independent. The 33.4% core stays protected until both
  break. Connected alpha masks remove only each destroyed arm. Its actual art
  breaks away, then splits into irregular alpha-bearing shards while retaining
  rotation. No rectangular body tiles or invented debris sprites are used.
- After the arms break, the core folds once and remains a ball between routes.
  Continuous 9.6-second paths cover the field without the former horizontal
  laser stops. Native shootable code bombs drop at difficulty-based intervals,
  with at most four active and 112-unit target spacing. Furious bombs retain
  their native 1.8-second flight-plus-arming reaction window.
- The organic arena uses the original full plate, low-amplitude moving tissue
  bands, brightness pulses and existing code particles on an independent clock.
  Original biome colors, outlines and copied-form arenas are retained.
- The loved native falling explosions remain. Actual body fragments supplement
  the intermediate fall and final death. Shards stay opaque and leave the field;
  their native owner, stage and bounded lifetime prevent leaking across retries.
- Rebirth keeps the native portal, protected player, reactions, exactly24
  accelerating electrical beats, 25.6-second final-arena swap and 28.5-second
  monologue handoff. Scan bands reconstruct the actual fusion plate while it
  spins; code streams, progressive download completion and real authored
  branching lightning replace the blue pinwheel. Rotation settles continuously
  upright, reaches 100%, then releases the native whiteout and explosion cue.
- The small Stage9 rendering bug is also fixed: twin blue hit plates now share
  the visible hull's rotation, fusion scale and disabled opacity. Hidden twin
  health and the native convergence rules are preserved.

Compiler: `_BUILD_SOURCE/build_stage78_review_1025.py`. Original imported and
generated SpriteCook sources and asset IDs/hashes live under
`_BUILD_SOURCE/stage78_review_1025/`; runtime sheets and measured frame metadata
are in `assets/game/shared/combat/stage78_review_1025/manifest.json`. No signed
URLs or credentials are saved. 20 lossless sheets total approximately 1.31 MB.
The eight branching bolt poses reuse inspected authored Hammer electrical art;
no new ship-bearing cinematic was generated.

## Verification and review

`_BUILD_SOURCE/probe_stage78_review_1025.py`: **27/27 native checks**, including
actual white damaged pixels/expiry, planted feet, sockets, physical rocket
interception, alpha arm removal, health budget, ball coverage, code-bomb warning
time, decoded native audio, 24 lightning beats, final reveal and independent
background motion. The probe uses labeled isolated fixtures and is separate
from the continuous full-fight recordings.

Additional pixel/transform coverage:
`_BUILD_SOURCE/probe_stage789_pixels_1025.py`: **9/9 passed**, for **36/36 total**.
Evidence is kept in
`_shots/stage78_review_1025/pixels/`. Continuous revised recordings are under
`_shots/stage78_review_1025/full/`; the original takes remain untouched.

Final continuous takes: Stage7 **03:56.46** (the `stage7-180723` folder), Stage8
**12:14.03**. Both reached native defeat with zero player deaths and no page,
console or asset errors. Full independent decode, audible AAC playback and
duration checks pass. Chromium played/seeks/frame-steps all five viewer videos;
clicking an issue from revised footage correctly seeks into the original take.
Selected files, source hashes and checks: `docs/qa/stage78_review_1025.json`.

The final Warden take contains 47.71 seconds of chase/crawl versus 8.54 in the
original; three jump states occupy 11.34 seconds versus the original 21 states
and 79.34 seconds. These are observations from the two bot runs, not a human
difficulty benchmark. Starting health is the same 6150 in both takes.

The before/after viewer is built by
`_BUILD_SOURCE/publish_stage78_review_1025.py` at
`docs/previews/stage78_review_1025/index.html`. Findings always jump into the
original take; revised native phase markers belong to the selected revised take.

Syntax checks pass. Required `node _BUILD_SOURCE/test_fl.js` exits 1 **before any
assertions or final summary** because
`_BUILD_SOURCE/retired_art_archive_1022.cjs` is missing. This is the recorded
pre-existing baseline; no missing-module bypass or fabricated green summary.

## Remaining findings

Later copied-form effect congestion, Volcano offscreen choreography, the Hammer
copy's rectangular rage aura and Stage9 projectile/pickup contrast are documented
follow-ups. The requested Warden and first-host/ball/background/rebirth changes
are implemented. Invulnerable input-bot footage verifies functioning native
encounters and transitions; human dodge difficulty still needs Mike's play review.

No commit or push. Existing unrelated staged, unstaged and untracked work is
preserved.
