# Shared enemy no-one-shot rule — September 15, 2026

## Implemented rule

The shared damage boundary now prevents one damaging event from erasing a fresh enemy health pool. If a fresh ordinary hull, authored shield or destructible boss component receives lethal damage, that event leaves the pool at 1. A later distinct impact or a later continuous-beam tick can finish it.

The rule preserves actual damage accounting: only health or energy removed is credited. Legacy one-HP fodder is promoted to a real two-point pool on its first lethal hit, takes one point of damage and can die to the next hit. A nonlethal opening hit does not grant an extra survival event later.

Covered health pools include:

- ordinary enemy hulls and their six authored shield families;
- Stage 4 drones, helper fighters and generator nodes;
- Razorback plates, Blacksteel wings, Tempest apertures and turret hardware;
- Furnace plates and barriers, Stage 7 toxic cores and Stage 6 Carrier nodes and bays;
- Xeno pieces, sectional rigs, modular boss parts and Stage 6 mech limbs;
- high-damage missile, elemental, laser and authored shrapnel routes that reach these pools.

Boss and miniboss main hulls retain their existing encounter HP floors and phase gates. Destroyable scenery, race obstacles and hostile projectile objects remain on their authored object-health rules.

## Approved piercing exception

The Stage 4 wide player laser remains a piercing weapon. One pass can still destroy both aligned shield-generator nodes in its column, including the helper route that invokes `hitBoss` for each node. This is the explicit dual-node behavior Mike requested and is not treated as a default enemy one-shot.

## Verification

- `node --check assets/game.js`, `_BUILD_SOURCE/test_fl.js` and `_BUILD_SOURCE/test_no_one_shot_0915.cjs`: pass.
- Focused suite section 304i: 14/14 checks pass, covering first/second impacts, continuous beam ticks, one-HP promotion, per-target state, shield-to-hull routing, components, modular parts and elemental overkill.
- Full confirmation suite: 3,931 checks pass and 56 recorded assertions fail; exit code 1. No new failure name appears against the 57-name recorded baseline. The baseline Stage 7 result-transition assertion passed on both final runs. The repository's documented intermittent Stage 1 sand-tank scheduler assertion failed once, then passed on confirmation.
- Real Chromium through `_BUILD_SOURCE/shoot.py`: 16 frames at 4 fps over 4 seconds, all requested authored Stage 2 images returned HTTP 200, and no page or console errors were reported.
- Pixel review: `_shots/no_one_shot_0915/native/shot_0002.png` and `shot_0004.png` show the hull alive at 1 HP and the hex shield alive at 1 energy after the first oversized missile. `shot_0007.png`, `shot_0010.png` and `shot_0013.png` show the second shield break, protected hull's first-hit survival and later destruction.

The Chromium scene is deterministic and invulnerable so each boundary is visible on a stable frame. It verifies live rendering and damage transitions rather than natural-play balance.
