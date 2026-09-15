# Chrome Hammer one-hand boomerang — September 15, 2026

## Implemented attack

The Stage 5 Easy/Normal Chrome Hammer now alternates its existing committed leap sequence with a new one-hand hammer throw:

- Chrome Hammer returns to the upper station and grips the detached hammer in his raised right hand.
- The hammer spins progressively faster for 1.55 seconds while the shared combat warning moves green to yellow to red.
- The vertical warning lane and reticle lock to the player's position when the charge starts. Moving later cannot drag the lane.
- The weapon releases down the committed lane in 0.70 seconds with a small boomerang bow, then turns below the playfield.
- It magnetically homes back to the boss's raised hand at a capped 315 pixels per second. There is no teleport or invisible reset.
- The hammer remains dangerous on both legs, with the normal player invulnerability window preventing stacked contact damage.
- Charge, release, magnetic return and catch each have a distinct material sound built in the existing sound engine.

## New authored components

The existing transformation sheets did not contain a hammerless body or a detachable hammer. Mike authorized image generation for this pass. The generated component source is preserved beside the derived transparent runtime assets:

- `assets/game/stage5_hammer/boomerang_components_source_0915.png`
- `assets/game/stage5_hammer/boomerang_body.png`
- `assets/game/stage5_hammer/boomerang_hammer.png`

The boss body and weapon are independent layers. Runtime rotation animates the hammer without rotating the robot or leaving a second hammer on the body.

## Verification

- `node --check assets/game.js`: pass.
- Focused VM section 304e: 12/12 checks pass for commitment, spin acceleration, release, outbound speed, capped return speed, catch, alternating flow, collision, four distinct sound beats, asset registration and timing.
- Full suite: 3,897 checks pass and the same 57 recorded assertions fail; exit code 1, with no new failure name. The Stage-7 route assertion was refreshed to match the already-implemented Campaign-map and direct-Arcade split; runtime behavior was unchanged.
- Real Chromium through `_BUILD_SOURCE/shoot.py`: 50 frames at 12 fps over 4.17 seconds, both new PNGs returned HTTP 200, no page or console errors.
- Pixel review: red release lane, detached outbound hammer, bottom turn, magnetic climb and raised-hand catch are all visible at the actual 480x512 game resolution.
- Review video: `_shots/hammer_boomerang_0915/BulletsOfFury_ChromeHammer_Boomerang_0915.mp4`.

The Chromium scene is a deterministic invulnerable visual proof. It verifies rendering and the complete animation path; it is not a natural-play balance verdict. Full Stage 5 balance remains tracked by `SPACE-06`.
