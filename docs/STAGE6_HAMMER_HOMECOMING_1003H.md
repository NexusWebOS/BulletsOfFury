# Stage 6 protection and Hammer homecoming — October 3

Mike requested the approved stealth bomber palettes on all Stage 6 spawn paths,
unskippable Cole/rebel dialogue with no combat, full rebel ship frames and unique
portrait boxes, Stage X music for every rebel fight, the actual Hammer likeness,
a modest Furious chromium reduction, and a generated orbital victory/Earth return.
He corrected the ship reference to the current Furyship and added a fully destroyed
aftermath held still while fading to monochrome.

## Runtime

`assets/feedback_1003h.js` loads after the existing campaign layers and before the HUD.
The layer preserves earlier work; this pass does not edit `assets/game.js`.

- Every Stage 6 bomber render route, including an untagged reinforcement, resolves
  to `stealth_1002` red/green/orange sheets. Existing attacks and warnings remain.
- Cole's dialogue types at 32 characters/sec and holds complete lines for at least
  2.6 seconds. Confirm/fire cannot advance it. Enemy AI, collision, spawning, player
  movement and weapon spending are frozen. Callisto's scripted demo still charges,
  fires and restores the original loadout. The route choice follows normally.
- Rebels enter within the camera margins. Each living rebel speaks in a generated,
  complete portrait bezel. Combat resumes only after the timed last line. Held
  weapons must be released before firing resumes. Uneven pitch-sheet rows now use
  measured ship bounds instead of an incorrect uniform 4x5 grid.
- Rebel encounters route boss music to `LevelX.mp3` while active, independent of
  stage. Other bosses keep their existing tracks.
- Cronos uses a generated portrait referenced from his actual Stage 5 boss art.
  Furious normal-encounter chromium HP is reduced from 100% to 75% of body HP;
  armor restoration is reduced proportionally. Normal/Hard, body HP, move patterns,
  HAMMER and HAMA remain unchanged. The initial jump's armor deferral is preserved.

## Ending

The normal Stage 5 Hammer death still awards its existing rewards and chaingun
unlock once. The new sequence then owns the exit, preventing the generic flyover
timer from cutting it short:

1. Orbital missile strike and an Earth-surface view of the destruction.
2. Actual-head closeup, turn, shock, cracking pose, authored electrical/fire blasts.
3. Generated final aftermath, fully destroyed. One fixed draw rectangle holds
   color for 1.25 seconds, fades saturation over 3.25 seconds, then holds monochrome
   to six seconds. There is no camera movement or simulated debris in this hold.
4. Nine pilot communications welcome the player back; the active pilot replies.
5. Generated Earth behind the live current Furyship, using the selected pilot's
   palette. The ship descends and shrinks, the real Stage 5 space-scroll clock slows
   to zero, and black fade hands off once to the normal Stage Clear screen.

The first two spaceship attempts used the legacy ship by mistake. Mike corrected
this; only the `_v2` current-Furyship images are loaded. The rejected sources are
preserved and marked inactive in the manifest. No user assets were deleted.

## Art and reproducibility

Built-in image generation produced 13 unchanged PNGs, 11 active. Exact prompts,
source paths, dimensions and SHA-256 values are in
`_ART_SOURCES/feedback_1003h/generation.json`. Assets and manifest live in
`assets/game/feedback_1003h/`; the owning importer is
`_BUILD_SOURCE/build_feedback_1003h.py`. No atlas was edited.

The standalone requested animation is
`assets/game/feedback_1003h/orbital-aftermath-monochrome.webm`.
It is recorded from the same Chromium canvas function used in the game. Full
native videos/screenshots and the local review are under `_shots/feedback_1003h/`.

## Verification

- Syntax checks: `node --check assets/game.js` and `assets/feedback_1003h.js`.
- Full suite: 6,958 assertions, final summary, zero errors, exit 0 in the completed
  final rerun. Native details are recorded in `docs/qa/feedback_1003h.json`.
- Native main probe: 34 checks, zero page/console errors, exit 0. Covers timed
  Cole/Yuri paths, Callisto, real rebel MP3 playback, all five portraits and pitch
  cells, normal/Furious armor, actual death handoff and full ending.
- Existing Hammer arrival regression and 13 Stage X warning/music checks also pass,
  exit 0, with zero page/console errors. Final homecoming recording has zero errors.
- Chromium pixel chroma on the static aftermath decreases from 66.677 to 35.659
  to exactly 0, confirming the final image is truly monochrome.
- Initial probe attempts found a harness constant-context assignment, an incorrect
  Normal-armor expectation (existing Normal armor is 30%, not 100%), and a missing
  portrait caused by an off-by-one alias substring. These were corrected; final
  screenshots were inspected. A null-armor deferral guard was also preserved.

These are controlled native encounters and recorded timelines, not campaign wins
or a claim of completed human Furious balance testing. Local work only; no commit
or push requested.
