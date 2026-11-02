# Earth-camo rolling kamikaze — October31

Mike replaced the Stage1 kamikaze's straight committed dive with constant barrel
rolls, faster rolling near contact, animated exhaust and turning pursuit that
tries to orbit the moving pilot. Ordinary Delta/Strike aircraft keep their
existing roles and palettes.

`assets/kamikaze_orbit_1031.js` (KO31) owns this scoped override after S1B. It
steers at bounded turn rates through approach, orbit, strike, recovery and exit;
movement follows the heading rather than a lateral position shove. A short
committed final vector keeps a close strike dodgeable. It attempts two passes,
with a20s pursuit cap and finite exit. Predictive edge steering avoids clamping
the aircraft at the camera edges. A shared simulation clock and circulating approach slots coordinate the wave.
Neighbour prediction and staggered strikes keep the fuselages apart as they bank
past each other. The formation clock pauses with live simulation.

Roll phase advances continuously at about0.85 turns/s far away and smoothly
accelerates toward5.55 turns/s near contact. The current authored roll pose and
heading cell render both the hull and its shadow. Per-pose measured tail sockets
carry the eight-frame animated blue exhaust. Rendering never rotates a static
hull canvas and never spends the native ripple-release delay.

Native HP, damageability, white hit flash/expiry, player body contact, enemy death
and rewards remain with existing owners. This aircraft emits no added bullets.
The shared `jetDash` cue fires once on each strike, through the existing mixer.
Freeze/stagger handling and the native frame-delayed entrance are retained.

## Art ownership

`_BUILD_SOURCE/build_kamikaze_orbit_1031.py` reuses the actual current
`air_refit_1021/s1jetdelta_b/roll.webp` bank. Its16 authored poses become512
roll/heading cells:128x128 RGBA, one64,64 fuselage pivot, one proportional scale
and32 baked headings. All512 cells have transparent margins with no clipped edge
candidates.

The palette maps existing material/camo clusters to light tan, orange-brown and
olive while retaining source luminance, dark seams and neutral highlights. The
static blue exhaust patches are removed from the derived hull only; their exact
source rectangles and per-pose attachment points are recorded. Animated S1A
exhaust replaces them in game. No new raster generation or atlas repack is used.

The builder registers `assets/kamikaze_orbit_art_1031.js` together with
`assets/game/levels/stage_01/enemies/kamikaze_orbit_1031/manifest.json` and the
loose sheet. Source/crop hashes and palette recipe are retained in that manifest.

## Verification and previews

`probe_kamikaze_orbit_1031.py`:37 native Chromium checks pass. They cover Normal,
Hard and Furious against stationary/horizontally moving pilots, plus diagonal
Furious movement, all16 roll poses, animated exhaust, near-contact acceleration,
heading changes/orbit/strike/finite exit, native HP and no unwanted rounds.
Actual rendered camo pixels flash white when hit and recover after30 native
frames. An unprotected player takes the real native ram hit. A three-plane
native wave is checked for separated fuselages and readable rendered hulls.
That check uses white hull pixels in the game context: its opaque canvas alpha
channel is not a hull mask. Close banked wing passes are allowed; aircraft
centres must not pile onto the same strike point.

`record_kamikaze_orbit_1031.py` records real RAF and native sound. The invulnerable
observer uses normal movement inputs to weave horizontally and vertically.
Enemy HP, attack clocks and phase states are not edited during footage. These
are animation/attack demonstrations rather than campaign balance runs.

| Clip | Length | Native rate | Decoded strike cues |
|---|---:|---:|---:|
| Single aircraft |14.68s|59.3fps|2|
| Three-plane wave |17.98s|59.7fps|6|

Both H264/AAC30fps faststart MP4s fully decode. The guide's existing kamikaze
card alone is replaced; all162 other current films remain. The focused page
offers both recordings. Seven Chromium playback checks verify current selection,
preserved other cards, seeking, decoded sound and no page/console/asset errors.

Local focused preview:
`http://127.0.0.1:8805/current/kamikaze-orbit-1031.html`

Current ignored evidence: `_shots/kamikaze_orbit_1031/` contains source/contact
sheets, native traces, damaged-pixel and ram-contact screenshots,37 checks,
two films and telemetry, decode/publish receipt and seven playback checks.
`publish_kamikaze_orbit_local_1031.py --install` updates only the existing local
review server's scoped file whitelist.

Syntax and whitespace checks pass. Required `node _BUILD_SOURCE/test_fl.js`
exits1 before assertions/final summary because this checkout still lacks
`UNUSED_ASSETS/retired_art_1022/manifest.json`. `assets/game.js` and
`_BUILD_SOURCE/test_fl.js` remain unchanged in this pass. No commit/push.
