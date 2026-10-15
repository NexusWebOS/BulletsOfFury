# Signature specials, opening supplies and Stage X

Mike chose **enhanced specials** as the additional Stage X unlock, upgrading
each playable pilot's signature. He clarified that the fighters needing their
own combat specials are the **enemy Rebels**. The opening supply should bring
the player's special toward the ship in a box.

## Implemented

Each new run receives one authored special supply per player after the opening
cinematic releases control. The box visibly descends before seeking its owner.
Shots or contact open it; the released icon then homes to that pilot and
activates the actual native ability. Cole receives Nuke Strike rather than
the random Sonic Cannon loan. The existing weapon crates and later drops
remain available. The native HUD uses the corresponding special name and icon.

Co-op supplies are independently owned. The existing seat window now swaps
each player's special, attached helper state and chain tier, and updates both
timers once per frame. Attached authored effects render in both seats within
their original under/over passes. Native checks cover Cole and Lizzie pickups
and Falva's orbiting helper around the second player's ship.

Defeating either Stage X encounter permanently unlocks **Signature Mk II for
all nine playable pilots**. Entering Stage X, an ordinary Stage 6 fight, a
living boss with a stale clear flag, or an old `done` boolean cannot award it.
The reward requires the matching spawned Stage X boss to reach its real defeat
state. Existing Air Superiority supplies are still awarded. The campaign map
names the new reward, and future pickups use Mk II.

The earned receipt persists in `bof_signature_mk2_v1` and campaign snapshots.
Campaign restore can recover that receipt; an old save cannot erase an earned
profile upgrade. All Mk II ability windows last 20 seconds:

| Pilot | Improvement |
| --- | --- |
| Axel | Reflected projectile damage ×1.5; the five-hit shield pool remains |
| Decker | Cloaking window extended to 20 seconds |
| Maverick | Charged Helix damage ×1.25 |
| Freezer | Time scale 0.4 instead of 0.5; Stage 6 still runs at full flight speed |
| Juggernaut | Wrecking Ball rotation ×1.2 |
| Yuri | One extra chain tier while active, restored on cleanup |
| Cole | Two extra nuclear warheads |
| Lizzie | Two extra atom bombs |
| Falva | Roller Ball contact damage ×1.25 |

The existing Rebel arsenals are now introduced consistently: Voss leads with
Turbo Overdrive, Nyx with Ghostknife Cloak, Rook with Heavy Gun Barrage, Kaia
with Twin Seeker Rack, and Jace with Molten Helix Nova. Their first personal
supply carries their signature, and each attack gets a readable name and the
authored Rebel ability badge. Existing secondary patterns, charge warnings,
shootable counters, and one/two-attacker difficulty limits remain intact.
Rook's next cycle still includes his physical grapple.

## Ownership and review

- Runtime: `assets/signature_specials_1011.js`, loaded last in `index.html`.
- Regression coverage: `_BUILD_SOURCE/test_signature_specials_1011.cjs`, included
  in the existing full suite. The core `assets/game.js` is untouched by this pass;
  `_BUILD_SOURCE/test_fl.js` retains CRLF.
- Native gameplay: `_BUILD_SOURCE/probe_signature_specials_1011.py`, using
  `shoot.py`, real Chromium, the game's renderer, actual keyboard inputs and
  lazy asset readiness.
- Portable review: `python _BUILD_SOURCE/build_signature_review_1011.py` creates
  `docs/previews/signature_specials_1011/index.html` from passing native captures.
- Durable results: `docs/qa/signature_specials_1011.json`.

The browser pass observes all nine real deliveries, both co-op owners, all five
natural Rebel signature releases, an accelerated Stage X clear through the real
damage and physical death controllers, the rendered reward, save/apply and a
fresh boot. Keyboard hold/release checks exercise Maverick's Helix and Falva's
Roller at both ability levels. HUD checks observe real icon draw calls.
Screenshots are protected controlled scenarios; the Stage X clear is not a
natural human campaign win. The left Harrier reward gate is covered in the
regression suite; the native clear uses the right Rebel route.

Final verification: **8,468 passing assertions**, the suite's final zero-error
summary and exit 0; **57 native gameplay checks** plus **6 preview checks**, all
passing with no browser or missing-asset errors. The focused companion probe
verifies the final secondary Fusion label and co-op effect rendering changes.

Earlier checks found and fixed P2 replacing P1's active special. The native
fixture also needed to select the actual menu pilot index, wait for atlas-backed
icons, hit the gang guard before hull damage, and wait for campaign art and
live typing before capturing the reward. Final results are recorded in the QA
file after the suite's final summary and native checks complete.

These changes are local. This request did not ask for a GitHub upload.
