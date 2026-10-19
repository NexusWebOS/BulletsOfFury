# Stage4 Warden gun, tank clearance and roadside pressure â€” October18

Mike requested unshootable miniboss bullets, an engine rule against overlapping
tanks, more standing shoulder nuclear missiles and an authored center weapon.

## Behavior

`assets/warden_center_1018.js` protects Iron Warden gunfire at creation and at
the shared ordnance adapters. Both current MG rounds and legacy `s4brass` rounds
are weapon-proof and non-interceptable. Later family adapters cannot restore
shootability. Genuine rocket/missile ordnance keeps its native counterplay.

The new `gunC` is a fifth independent part with8% of the existing maximum hull
budget; it does not add hull HP. It uses a forward central hardpoint, paired
barrel sockets, authored idle/charge/fire/cooling poses, actual silhouette
collision, Retina targeting, native damage/markHit and module rupture. The
standard MG turn cycles live L/C/R guns while retaining its current round
budget and difficulty cadence. A destroyed center gun stops firing. Destroying
all five parts still exposes the native core-fan/ram last stand. The complete
authored Warden hull and existing helper flight controllers remain in use.

The original central placement was screened by the painted hull nose. Native
J-fire exposed that error; the gun now mounts forward at40% of hull height,
where ordinary shots can reach its barrels. Muzzle placement, collision and
Retina share the same fixed art pivot and rotation.

`assets/ground_traffic_1018.js` owns clearance for tank-class moving ground
vehicles across stages. It reserves full hull footprints after the complete
spawn chain, including the larger Stage4 render footprint and `_noSep` tanks.
Existing tank pairs bypass the generic sideways-shoving solver. Incoming
vehicles reserve upstream rows; moving vehicles brake before occupied ground,
and a final shared pass covers controllers that own movement themselves.
Terrain rows and lane anchors follow positional corrections. Weapons retain
their native clocks. Props, fixed launch pads, bosses and arsenal minibosses
remain separate actors. Highway reinforcements choose a free lane before
spawning. The standing engine rule is also recorded in `AGENTS.md`.

Roadside nuclear pad spacing changes as follows, measured in scrolling pixels:

| Difficulty | Previous gap | New gap | Maximum live pads |
|---|---:|---:|---:|
| Easy |640|380|2|
| Normal |540|300|3|
| Hard |420|230|4|
| Furious |300|180|4|
| Insanity |260|150|4|

The first pad becomes eligible at100px instead of180px. Side alternation,
standing/ascent gun and Retina interception, existing countdowns, fixed atomic
landing warnings, pauses, terrain anchoring and boss-approach gates remain
native. A45s controlled sample produced5/7/8 pads on Normal/Hard/Furious.

## Authored art

PixelLab had no remaining generations, so the built-in image generator used
the actual Iron Warden sheet as the armor/palette reference. One full-sheet
generation supplies16 poses. Its1254px fractional grid is retained as a source;
the owning `_BUILD_SOURCE/build_warden_center_1018.py` exports16 loose256x256
RGBA frames, a shared128,104 mechanical pivot and one0.70 proportional scale.
Measured adjacent-row steel fragments are removed during grid extraction;
actual flame and smoke poses are preserved. No atlas is edited.

The builder owns PNGs, per-pose muzzle points, hardware masks, registration
audit, manifest and `assets/warden_center_art_1018.js` together. Source and
generation provenance live in `_ART_SOURCES/warden_center_1018/`. Native frame
scrubbing and onions are in the review's `frames.html`.

## Verification

`node --check assets/game.js` and both new runtime owners pass. The complete
`node _BUILD_SOURCE/test_fl.js` reaches its final BUILD OK banner and exits0:
8,785 printed ok checks,0 errors, matching the current measured baseline.

150 real Chromium checks pass, with no game page, console, draw or asset errors:

- 46 focused checks: all three difficulties, actual J-fire and missile routing,
  registered muzzle emission, central module loss/flash/expiry, traffic at birth
  and across30s motion, live tank attacks and component hit pixels, shared
  Stage1/3/7 tank spawns, and denser alternating nuclear pads.
- 61 existing roadside-missile checks: primary weapons, manual Retina,
  standing/ascent/tail interception, committed return, atomic pixels/sounds,
  terrain seams, pauses, difficulty pressure and reset/boss gates. Bounds were
  updated to the explicitly requested3/4-pad density.
- 33 existing Warden last-stand checks: destroying all five parts, warned fan
  lanes, committed ram, departure/return, collision and negative control.
- 10 delivered review checks: real controls, isolated saves, regular480x512 FOV
  with side HUD, both shoulders, committed atomic target, all16 XART frames
  rendered through the game context, and onion scrubbing.

Primary-routing fixtures use a short recovery window and aim at an actual
barrel to isolate part interception. All attack-turn checks retain native AI.
These are focused encounter/traffic regressions, not a complete campaign run.
An initial missile fixture used a zero vector, which native missile motion
correctly converted to an eastward heading; it now uses a slow southward vector.
The hit-flash fixture reads the struck tank module as well as its hull timer.

Evidence: `_shots/stage4_engine_1018/`; durable report:
`docs/qa/stage4_engine_1018.json`. Gameplay review:
`docs/previews/stage4_engine_1018/index.html`. No commit or push was requested.
