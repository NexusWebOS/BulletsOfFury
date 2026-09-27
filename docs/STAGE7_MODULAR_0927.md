# Modular Stage 7 encounters — September 27, 2026

Mike requested a new toxic tank miniboss, an independently destructible Warden,
an upright portal at the final floor threshold, and menu/opening corrections.
These are local changes; no commit or push is part of this pass.

## Encounter implementation

`assets/stage7_modular_0927.js` owns both Stage 7 encounters. Stage 9 retains its
existing late encounter director. Other bosses remain whole authored plates.

- **Caustic Siege Tank:** generated chassis, two rotating and destructible gun
  mounts, and mortar reactor. Crossfire, committed charge, toxic fan volleys,
  and delayed mortar impacts. The entire 176px chassis stays inside the central
  solid-ground corridor (34.5–65.5% of the 680px authored map), including its
  short forward charge. Guns project beyond the armored prow so ordinary lasers
  and bullets can reach them. Armor damage is reduced while guns survive.
- **Warden:** six real module pools: two front legs, two rear legs, and two
  independently destructible gun turrets. The two canisters are visual energy
  reservoirs and never become destructible targets.
- Either gun and either front leg can break first. One missing front leg creates
  a balance lean. Both missing trigger a mechanical scream/drop; rear legs
  extend and unlock. Rear-leg destruction exposes a weaker core shield.
- The shield has no HUD bar while the legs protect it. Once exposed, the normal
  shield bar appears. Hits trigger a limited counter-volley, with 0.90/0.72/0.58s
  cooldown on Normal/Hard/Furious. Shield damage does not overflow into core HP.
- Surviving guns use aimed reticle/FOV attacks after shield loss. With both guns
  gone, the face mask lifts and the core fires rapid sweeping green beams.
- Pursuit reverses the actual terrain scroll at 100/130/160px/s. Leg damage
  totaling 16% of its pool interrupts the chase and gives a retreat/stun opening.
  A planted-step cadence drives the individually rigged legs.
- Alternating front swipes, crossed swipe, aerial slam, bounces, mortar rain,
  extended-barrel chaingun fire, and toxic orb fans have distinct attack/recovery
  timing. The big leap follows/orbits the pilot, then freezes its landing marker
  for the final 0.68s. The native green/yellow/red reticle and asterisk-on-sign
  precede impact. Landing releases three staggered twelve-orb rings, offset like
  the Furnace Tyrant's Furious slam.
- Death uses the generated 16-frame toxic explosion and separate 16-frame slime
  spew. Stage 7 completion still enters the existing campaign/arcade handoff.

The final floor threshold is 610 source pixels below the decorative circular
void baked into `nst7_master_v3`. The boss trigger waits for this actual terrain
position, instead of the elapsed stage timer alone. The new upright gate opens
at the top of that last traversable floor and closes after the Warden emerges.

## Art

Seven new sheets are stored in `assets/game/stage7_modular_0927/`: Warden parts,
tank parts, upright portal (16 frames), explosion (16), spew (16), toxic orb (8),
and spiral shield (8). Generated using the built-in image tool, not SpriteCook.
Original alpha is preserved. Parts are trimmed from their generated cells by
the runtime using alpha bounds; no packed atlas was repacked. The Warden's old
plate and the magma projectile were used as visual references.

Prompts, source files, dimensions, and hashes: `docs/stage7_modular_art_0927.json`.

## Menus and opening

Left/Right navigation in the password keypad remains on the current row,
including DELETE/CLEAR/ENTER. Cover B fills the game viewport in both the opener
and title menu. Readable six-and-a-half-second pilot beats introduce the danger
to Earth and the **Fury Fighters**, followed by a nine-second cover beat. The
retired slogan is removed; no prerecorded gameplay was added.

## Verification

Evidence and counts are in `docs/qa/stage7_modular_0927.json`. Reusable probes:

- `_BUILD_SOURCE/probe_stage7_modular_0927.py`: both encounters on all three
  difficulties; attack histories, finite projectiles, full tank footprint limits,
  module destruction stages, screenshots, page errors, and console errors.
- `_BUILD_SOURCE/probe_stage7_contracts_0927.py`: native bullet, laser, and
  Retina missile damage to modules; real keyboard bottom-row navigation;
  full-size title and cover screenshots.
- `_BUILD_SOURCE/test_stage7_modular_0927.cjs`: damage gates, shield retaliation,
  chase interruption, committed landing, three rings, and end-form choices.
- `_BUILD_SOURCE/record_stage7_modular_0927.py`: native rendered inspection clips.

Review recordings use an invulnerable pilot. The module-progression clip forces
named part damage so both endings are visible. They are silent visual recordings,
not claims of a human campaign clear or final difficulty balance. Real hardware
feel and complete campaign difficulty playtesting remain separate work.
