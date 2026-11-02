# November 1 — shared difficulty steps and regular-wave films

Mike selected both turret aim and firing speed, the same compound steps for
enemy/shield/boss health, and Furious for the requested wave recordings.

| Selected difficulty | Health and angular tracking | Firing interval |
| --- | ---: | ---: |
| Normal | 1 | Normal interval |
| Hard | 1.15 | Normal interval / 1.15 |
| Furious | 1.3225 | Normal interval / 1.3225 |

Health uses the existing Normal baseline, including its stage, party and threat
budget, then rounds the scaled value. Composite pools retain their native part
rounding and complete encounter budget. Do not multiply these values by the old
Hard/Furious bonuses again. Easy and Insanity retain their separate tuning.
Warning/commit windows, projectile speed/count, flight, unlocks, lives and
defensive/interception rules keep their existing owners.

## Implementation owners

- `assets/difficulty_rules_1101.js`, loaded after the current gameplay layers,
  owns the shared helpers and global tables. `difficultyHealthBaseline15`
  accepts the old Easy/Insanity fallback. `turretInterval15` scales a Normal
  firing interval; `turretSpeed15` scales an angular rate.
- `_BUILD_SOURCE/install_difficulty_rules_1101.py` owns explicit migrations of
  late absolute HP budgets and native turret launch/aim owners. It preserves
  each file's bytes/newline style. Do not apply a second scale inside an
  already-wrapped angular solver.
- `assets/game.js` retains the native controllers. Native boss, miniboss,
  copied-life, ally and module owners remain intact. Razorback's Hard pair
  shares the selected complete budget between both actors.
- `assets/cloud_carrier_1101.js` and `assets/carrier_assault_1101.js` now hold
  their existing actors/clocks during temporary radio dialogue and resume
  afterward. A real encounter transition still owns withdrawal/cancellation.

## Recording scope and rebuild

The review fixture runs the actual scheduled callbacks, native 60 Hz gameplay
updates, renderer, AI, hit/death owners and shared game audio. It supplies normal
pilot controls, a level-5 machine gun and native missile input. Native pickups
can change the equipped weapon during play. The pilot is
explicitly labelled invulnerable. Enemy HP, phases and attack timers are not
written by the capture pilot. Later takes use the official DBGT god owner,
armed through debugUnlocked, instead of a temporary invulnerability timer.
Each film retains a combat tail after its final release (at least 12 seconds;
later takes 18 seconds). Escaped or upstream survivors need not all be killed. Stage6 carrier assaults retain their full
queue/completion owner.

Boss/miniboss entry is suppressed only in this QA fixture. Original level lengths
and scenery remain; endless adaptive reinforcements are held to review the finite
authored book. Stage X is boss-only and therefore excluded. Both Stage 6 route
choices are recorded. The QA-only `BOF_REGULAR_WAVE_REVIEW` gate is undefined in
normal play and is never saved.

- `_BUILD_SOURCE/wave_review_1101.js`: fixture, native pilot inputs and successful
  callback receipts. Terrain/pressure retries do not count as completed waves.
- `_BUILD_SOURCE/record_all_waves_1101.py`: real-time Chromium video/audio,
  per-wave wall timestamps, production hashes and a copy/hash of the exact QA
  fixture used for each film. Gameplay and scenery share the same simulation
  delta; the browser's trapped outer loop is not resumed.
- `_BUILD_SOURCE/publish_all_waves_1101.py`: full H.264/AAC decode, unclipped
  audible audio checks, native callback coverage, thumbnails and chapter routes.
- `_BUILD_SOURCE/waves_viewer_1101.html`: level/route tabs, individual wave
  chapters, previous/next and complete level playback.

Temporary output and verification receipts belong under
`_shots/waves_all_1101/`. Failed setup takes are excluded from publication.
No commit or push is requested.

## Verification

`probe_difficulty_rules_1101.py` checks live ordinary enemy/shield pools in all
nine rosters, native turret angular steps and burst intervals, committed warning
windows, offensive bullet interception, source-rendered hit-flash pixels/expiry
and all nine native boss/miniboss budgets against the recorded Normal baseline.

Required full-suite limitation: `node _BUILD_SOURCE/test_fl.js` exits 1 before
assertions and its final summary because the existing ignored
`UNUSED_ASSETS/retired_art_1022/manifest.json` is missing. The suite is not green;
no historical assertion count is presented as a current pass.

## Published review and final receipts

Local page: http://127.0.0.1:8805/current/all-waves-1101.html

Ten films total 986.02 seconds (16:26): all nine levels plus the second Stage6
route. There are 260 unique scheduled entries and 313 selectable chapters.
Per-level counts are 36, 25, 20, 22, 14, 53, 22, 30, 38; Stage6's second route adds 53.
Carrier chapters extend through each native assault-completion receipt.
Chapters overlap where the native wave formations overlap.

- 41 native difficulty/health/aim/cadence/interception/pixel checks pass.
- 7 late helper, shield, copied-life and single-scale cannon checks pass.
- All ten H.264/AAC files fully decode, with audible unclipped audio.
  Decoded mono audio peaks are0.259–0.364; RMS0.0348–0.0568.
- Chromium verifies 30 first/middle/last chapter seeks with actual decoded
  pixels across all ten films, chapter counts, full/previous controls, rapid
  route switching, no horizontal overflow at 390px and no page/console errors.
- Native captured frames and desktop/mobile page screenshots were inspected.
  The Stage7 capture averaged 35.02 render fps; the other films 58.4–59.5.
  Delivered movies are 30fps. Stage7 performance remains a follow-up finding.
- Production hashes match the final source for every film. No final take has
  a sampled pilot death or boss/miniboss activation. Both Stage6 route choices
  and all four carrier completions are verified.
- `node --check assets/game.js` and the new shared module pass. The scoped,
  CRLF-aware whitespace check passes. game.js retains LF and test_fl.js CRLF.
  An unscoped default whitespace check reports existing CRLF/whitespace in
  unrelated working changes; those files were preserved.

Receipts are in `_shots/waves_all_1101/difficulty-checks.json`,
`difficulty-followups.json`, each film's `report.json`, and
`publication/receipts.json` / `publication/browser-playback.json`.
The preview server permits files from `_shots/`; the publisher copies its
HTML there and updates only the new local routes in current-overrides.json.
Existing individual enemy cards and their videos remain available.
