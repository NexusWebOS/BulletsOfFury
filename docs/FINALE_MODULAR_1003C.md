# Stage 8 — modular forms and the single refilling gauge

Mike's October 3 correction supersedes the earlier whole-plate constraint for
this boss: every alien transformation must be modular, including the knight.
The earlier eight vertically stacked health gauges were the wrong interpretation.
He also caught the generated knight "head" containing chest armor; the live rig
uses a newly generated **head only**, mounted on the separate torso.

## Current implementation

`assets/finale_modular_1003c.js` follows the existing finale controller and keeps
its eight individual health pools, boss signatures, difficulty values, code
teleports, gravity/orbit attacks, recovery windows and one final portal reward.
Every form now renders independent authored components:

| Form | Live component rig |
| --- | --- |
| Host | Existing torso and two independently moving/breakable arms |
| Helicopter | Hull, tail, two autocannons, two rocket racks and rotor |
| Furnace | Torso, two cannon/claw arms, two legs and reactor |
| Cryo Hive | Hull, two emitter batteries and four independent ice guns |
| Storm | Gun-free hull, two autocannons, two missile racks and lightning barrel |
| Knight | Torso, corrected head, two arms, two legs, sword and shield |
| Harrier | Hull, two fan pods, two missile batteries and central beam cannon |
| Warden | Torso, two pincer arms, two gatlings and two legs |

The knight's sword is a child of its hand/arm. Its separately generated charge
reel follows the blade through power-up, jump, downward strike and horizontal
follow-up. Sword damage uses the same moving blade segment (with swept sampling),
not the old detached target-circle hit. The wrist aims the landing strike at the
committed target. Authored FOV and Retina markers warn before the attacks.

Forward-kinematic poses also supply module hit rectangles, Retina targets and
weapon muzzle positions. Guns aim and recoil independently. Breaking an emitter
cancels its pending/active beam and removes it from subsequent volleys. Breaking
the sword arm removes its child sword and interrupts the combo; breaking the
physical shield prevents a new code wall. A fully disarmed form can still use
its reactor's gravity/orbit attacks, so the encounter cannot stall.

The HUD draws **one authored boss housing**. During takeover the same interior
fills eight times, successive colors covering the preceding fill (0.4-second
fills with 0.1-second holds). Combat then shows only the current form's actual
HP fraction and color. This is eight lives across the final boss encounter,
not eight extra health pools for each transformation. Existing per-form HP is
unchanged by this pass.

## Authored assets and reproduction

Built-in `image_gen.imagegen` produced seven component kits, the sword power-up
reel, a corrected head and a corrected gun-free Storm hull. No API fallback or
SpriteCook was used. Exact prompts are in
`_ART_SOURCES/finale_modular_1003c/prompts.json` and `corrections.json`.

`_BUILD_SOURCE/build_finale_modular_1003c.py` owns sheet registration and measured
source rectangles. PNG source pixels and transparency remain untouched. The
runtime manifest records source paths and SHA-256 hashes. Joint pivots and
attachment dimensions are in `FMC_RIGS`; the importer deliberately does not
assume generation followed the requested grid ordering. Earlier whole-plate
sources remain preserved but are no longer warmed/drawn by this runtime.

## Verification

- `node --check assets/game.js` and the new runtime syntax check pass.
- Full `_BUILD_SOURCE/test_fl.js`: **6,893 passing assertions, exit 0**, final
  `FALVA/LIZZIE BUILD OK, 0 ERRORS` banner. Previous baseline: 6,818, exit 0.
- `_BUILD_SOURCE/probe_finale_modular_1003c.py`: **122 native Chromium checks**,
  exit 0, zero page/console errors. Uses `_BUILD_SOURCE/shoot.py`, lazy readiness
  polling and yielded frame batches. Actual game-context `drawImage` calls are
  recorded using logical XART keys, including the corrected head and charge FX.
- All eight forms take real player projectile damage on their components and
  lose those components independently. All attack books finish with recovery;
  destroyed laser modules lose pending and active beams. The real blade hits
  the warned stationary target for slash, downward jump and follow-up sweep,
  and does not hit a remote point outside its geometry.
- One boss housing per draw; all eight intro fills and active-form health/color
  verified. Eight intact form entries lead to exactly one final reward.
- Inspected all seven new assembled rigs, powered sword/head, damaged modules
  and refill screenshots. Recorded actual engine motion through the intro,
  every rig and the knight combo; recording has zero browser errors.

Initial native pass: 119 checks, exit 0. Visual/geometry review then refined the
sword's approach offsets and wrist aiming; three additional stationary-target
checks pass in the final 122-check run. There were no failed suite/probe runs in
this pass. Fixtures use an invulnerable pilot and do not establish campaign-win
balance or a final difficulty rating.

Local review: `http://127.0.0.1:8794/_shots/finale_modular_1003c/review.html`.
Play: `http://127.0.0.1:8794/index.html?build=d69cffa4-modular-finale-1003c`.
Portable report: `docs/qa/finale_modular_1003c.json`.

No commit or push. Existing dirty work was preserved. `assets/game.js` remains
LF and `_BUILD_SOURCE/test_fl.js` remains CRLF.
