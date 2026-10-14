# Stage 3–4 playthrough pass — October 14, 2026

Yuri's Stage-4 special upgrade was erased by `beginStage`, alongside temporary
pickup state. Stage entry now retains his earned Storm gate and chain tier.
The live HUD and Stage-4 reward panel identify Thunder Storm using the existing
Storm icon. The held-trigger/release ability works in Stage 5; later entries,
co-op ownership and an unearned fresh run are also checked.

## Encounters

The new runtime owner is `assets/stage34_assault_1014.js`. Its boss behavior is
limited to Stage 3 and Stage 4, retaining the existing authored hull plates,
separate mounted weapons, health, destruction and hit-target systems.

- **Stage 3 miniboss:** the Frost Cruiser keeps its ice identity and modular
  graphics. Its nuclear replacement/form-change sequence is suppressed.
- **Stage 3 boss:** rapid physical turret slugs, shootable missile volleys, and
  four charged ice salvos. Core electricity, blue/white hull glow and thunder
  build while the background darkens. Authored FOV and the alert precede each
  salvo; the two missing shot lanes stay open. The hull steps right between
  salvos, then recovers before its next attack. There are no laser attacks in
  this encounter controller.
- **Stage 4 miniboss:** rapid machine-gun bursts and missile-box volleys. New
  helpers approach from south at an enlarged depth, cast shadows, twist toward
  the player and fire real MG shots after reaching the combat plane. Their
  native family graphics and health remain separate from the parent. Damage
  draws retain their camo palette.
- **Stage 4 boss:** a visible committed charge with screen shake, supported
  controller rumble and the approved chip engine bed revving in pitch. All four
  generators translate/rotate/scale with the hull. Their native point damage
  and Retina targets share those same positions.
- Crossing above mid-screen starts the alert and an orbiting Retina. The
  repeated lock beeps lead into a committed volley from the shaking missile
  boxes. Retreat south before release cancels the trap. Once released, those
  missiles remain shootable; destroyed boxes stop emitting independently.
- Storm charges darken the scenery while foreground parts glow and blue
  electricity animates around the core. Thunder accompanies the warmup and
  release. Lightning balls are protected from ordinary interception through
  the common ordnance policy; physical MG slugs and missiles retain their own
  identities.
- The Sovereign also exits south, returns above the player enlarged and
  north-facing with a hull shadow, and enters a northbound pursuit while
  releasing lightning balls behind it. The overhead phase cannot contact-hit
  the player. The final-quarter shield handoff uses this same flight sequence.

Easy, Normal, Hard and Furious retain separate timings and projectile pressure.
Normal -> Hard -> Furious increases MG cadence, missile waves and travel speed,
while shortening charge/lock windows. Warning/shot targets commit before release;
rolling and somersaulting retain their native invulnerability rules.

## Aircraft formations

`flight_variants_1012.js` adds bowling/fan breaks, paired crisscrosses and
staggered individual bomb peel-offs to the existing route rotation. They retain
native formation health, difficulty counts, warned releases, authored falling
bombs, encounter gates and death cancellation. Authored heading/roll banks are
used across the supported stages. Primary and fallback hit renders preserve
the aircraft's palette and leave the real damage timer intact.

No atlas, boss art, frame canvas, ship reference or weapon-upgrade family was
replaced. Uniform scale is used for depth; the whole authored plates and mounted
parts remain registered. Maverick's fixed homing lasers are unchanged.
The engine/lock/thunder/missile cues reuse approved sound-bank entries and respect
saved volume/mute settings. Haptic requests are conditional on device support.

## Verification

- `node --check` passes for game.js and both edited/new gameplay modules.
- Full `_BUILD_SOURCE/test_fl.js`: **8,700 passing assertions, zero errors**,
  final BUILD OK summary and exit 0.
- `_BUILD_SOURCE/probe_stage34_assault_1014.py`: **60 checks pass**, no page,
  console or missing-asset errors. Actual browser key events exercise Yuri's
  hold/release. All four difficulties are covered for the cold encounters;
  real bullets test missile interception and lightning-ball protection.
- `_BUILD_SOURCE/probe_stage34_visuals_1014.py`: **13 checks pass**, no browser
  errors. Native background pixels, authored FOV gaps, missile-box geometry,
  surviving emitters, pause, complete overhead entry, primary/fallback palettes
  and unchanged reused late-stage controllers are checked.
- Native charge, lock, pursuit and helper screenshots were visually inspected.
  Haptics capability is simulated; no physical-controller or complete human
  campaign/balance claim is made.

Portable records: `docs/qa/stage34_assault_1014.json` and
`docs/qa/stage34_visuals_1014.json`. Logs/captures: `_shots/stage34_assault_1014/`.
Earlier fixture failures remain in ignored logs: obsolete synthetic keyboard
state, late projectile sampling, a shot-down point inside the boss shield, and
an overhead seek that skipped native exit initialization. Final fixtures use
real input, live ordnance and the complete flight sequence.

The source edit keeps game.js LF and test_fl.js CRLF. Local unrelated work is
preserved; publication contains only this completed pass.
