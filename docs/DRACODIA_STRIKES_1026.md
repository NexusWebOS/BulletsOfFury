# Dracodia independent lightning strikes - October26

Mike clarified that only the surrounding lightning should spiral at the ending.
The main lightning should strike faster and faster without spinning with him.
[Current audible recording](http://127.0.0.1:53746/_shots/dracodia_strikes_1026/video/take-96a7a9af/dracodia-final-transformation.mp4). Earlier takes remain preserved.

`assets/dracodia_depth_1026.js` now locks every downward channel's endpoints
for its strike. Core channels use fixed vertical playfield positions; distant
channels select a non-circular permutation of nine lanes with beat-locked bends.
Neither geometry uses the boss yaw or a frame-by-frame orbital clock.

The ending uses an independent integrated clock: at elapsed u after 23s,
phase=5u+3u*u and rate=5+6u. Cadence accelerates from 5 to 20.6 strikes/s through
the 25.6s flash. Each beat fades and releases for its last 28%, rather than leaving
a continuously moving electrical curtain. Extra channels remain silent visual
partners to the original 24 native audible beats.

Only the surrounding rear/front helix spirals, appearing during the final storm
from 23s and running on its own clock. The boss keeps the already approved
accelerating depth loop and incomplete preflash assembly. Complete native form
still appears only after full whiteout cover. All health, protection, arena,
speech, hit feedback and defeat ownership remain native.

Boss Cinematics was updated and validated with the fixed-channel/independent
cadence guidance and current project reference. No new art generation or audio
routes, game.js/test_fl.js edits, commit or push.

## Verification

34 native checks pass, including actual distant-strike and helix pixels,
identical channel geometry at different boss yaws within one beat, increasing
independent cadence, release intervals, spiral absent before the final storm,
all depth poses, delayed complete-body reveal, native health/hits/flash expiry
and no page/console errors. Native screenshots inspected.

All 21 recording checks and 6 playback checks pass. The continuous audible
film fully decodes, and its decoded frames were inspected. Browser playback and
Range seeking pass with no asset or browser errors. Required full suite still
exits 1 before assertions/final summary due existing missing
`_BUILD_SOURCE/retired_art_archive_1022.cjs`; syntax checks pass.

Use the existing probe, recorder and playback helper with `--strikes`.
Evidence: `docs/qa/dracodia_strikes_1026.json` and `_shots/dracodia_strikes_1026/`.
The film is an explicit native-damage transformation checkpoint, not a full fight.
