# Sovereign, Hammer, carrier roster, Wind and late-stage pressure

Mike's October 17 request is implemented for the gameplay portion. The separate
Stage 7–8 black-void, portal and final-arena regeneration **waits for PixelLab**,
as Mike explicitly selected. Existing portal and arena art stays in production;
the unused built-in-generator drafts are not loaded or included in this release.

## Result

- Sovereign uses the regular combat FOV for the actual next lightning fan and
  its moving gap, including the first pursuit volley after its overhead return.
  Ball lightning retains weapon proof and cannot be shot down by ordinary gun,
  spread, beam, orb or missile interception. No legacy arrow signage returns.
- Its two helpers are new authored lightning-infused aircraft, 192 px wide,
  twice the Warden helper's 96 px size. They have independent entry, tracking
  warning, committed bursts, orbit motion and recovery. Their existing native
  hull, shield and gun pools retain damage routing and visible hit feedback.
- Hammer's restoration has a 7–9 second window and needs 2/3/4/5 unique missile
  impacts on Easy/Normal/Hard/Furious-or-Insanity. Raised-hammer and body missile
  impacts count. A single missile cannot count repeatedly. Ordinary bullets
  flash the actual hit without silently cancelling restoration. The whole-body
  Chromium charge wash progresses only after missile impacts; core/hammer
  emissive animation and short real hit flashes remain active. The last required
  missile revokes the granted heal and enters the existing stun/punish state.
- Stage 5 gets the Earth Eclipse Siege Bomber that occupied Stage 6. Stage 6's
  miniboss is the newer six-battery cargo fortress, adapted to miniboss HP,
  targeting, death, reward and progression. Its reactor waits for all six guns.
- Stage 6's left-route boss is the earlier fan-driven Warhive Harrier. Two fans,
  four laser batteries and two missile racks are independent targets with their
  own pools, hit pixels, warnings and weapon shutdown. All eight must be destroyed
  before its bay/reactor opens. The final reactor has a deliberately small pool.
  Enlarged overhead returns are outside the player's collision plane. No ace
  replacement is spawned when its reactor dies. The rebel route stays separate.
- Cole's Stage 6 team conversation and route selection keep player flight,
  scrolling, live enemies and existing projectiles running. Only new enemy
  arrivals and the scheduled wave cursor wait until the route is chosen.
- Highway tanks have a new heavier animated hull/tread bank, independent twin
  cannon and missile racks, larger 88×104 physical bounds, more durability than
  Stage 1 armor, regular warnings, committed metal shells and rack volleys.
  The full footprint is checked against the paved mask. Racks and cannon support
  separate native Retina missile locks. Existing Hard/Furious reinforcements use
  these same actors rather than an unrelated extra controller.
- Wind MG, spread and chaingun get compact authored ammunition. Wind laser uses
  one continuous full-length authored frame rather than repeating body tiles.
  Other oversized Wind effects are reduced visually. Damage/progression stays
  with each weapon; Maverick's fixed homing lasers remain excluded.
- Stage 7 adds complementary toxic formations and sustained reinforcement
  pressure, increasing Normal → Hard → Furious. Existing warning/recovery owners
  remain active, with additional attack slots/cycles and shorter recovery gaps.
  Ground tanks are clamped to the central floor at spawn, after native motion
  and after separation; side crawlers and aircraft keep their intended routes.

## Art and ownership

Eight banks contain 128 distinct exported poses. Frames are uniformly even:
256×256 jet/hull/turret, 64×96 ammunition, 128×512 continuous Wind laser.
One physical pivot and one proportional scale apply per complete bank. Source
rectangles, socket registration, common scale, hashes and output bounds live in
`_ART_SOURCES/assault_1017/manifest.json`. Rebuild with
`python _BUILD_SOURCE/build_assault_1017.py`; inspect its onion output under
`_shots/assault_revision_1017/art/`. No main atlas was edited.

Owners: `assault_sprites_1017`, `storm_guard_1017`, `hammer_counter_1017`,
`stage6_roster_1017`, `stage6_radio_1017`, `highway_armor_1017`,
`sewer_assault_1017`, `wind_refit_1017`, plus the generated art manifest.
They are loaded after the existing targeting owner. This pass needs no new
`game.js` mutation; separate local modular/spread/tutorial work is retained.

## Verification

Native Chromium: 88 passing checks, zero failures and zero browser/asset errors,
both in the working tree and in the exact scoped GitHub candidate. This includes
the interception matrix across three difficulties, first pursuit warning,
missile-count/duplicate protection, both miniboss lifecycles, the eight-module
reactor gate, safe overhead contact, real keyboard movement during live radio,
wave preservation, actual shell draws, compact Wind pixel bounds, central tank
placement and increasing Stage 7 pressure. Native hit-pixel differences and
timer expiry are checked for the lightning guard, Harrier fan/laser/rack and
highway rack; the rack also receives a native independently locked missile.
The cannon plays all sixteen authored recoil/reload poses; its shells originate
at the measured barrel tips and incoming fire can hit the cannon's full extent.
Reinforcements stop refilling the crowd gates as the authored fight approaches.

Required `node --check assets/game.js` and all new runtime syntax checks pass.
`node _BUILD_SOURCE/test_fl.js` reaches its final BUILD OK summary: 8,742 passing
assertions, zero failures, exit 0. Existing Warden entry-safety: 43/43, no browser
errors. Native captures and logs are under ignored `_shots/assault_revision_1017`.
The existing targeting/stationary-core/highway regression also passes 96/96.
Portable evidence: `docs/qa/assault_revision_1017.json`.

These are controlled native fixtures and visual checks, not a claim of a full
human campaign clear or final subjective difficulty approval. The requested
PixelLab artwork remains outstanding until that service is connected.
