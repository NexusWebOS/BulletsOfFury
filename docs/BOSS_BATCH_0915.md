# Stage 4 defeat and new Stage 5 transformer â€” 0915

Mike's full new brief is preserved in BOSS_DESIGNS_0915.md. The current Stage 2 identity question remains unanswered; no Stage 2 boss swap, head generation, shriek audio or dialogue implementation is claimed.

## Stage 4

Four authored smoke rings at 0/90/+45/-45 degrees expand across the ship. A major blast starts the cookoff. The whole ship remains visible and falls at 18 pixels/second while overlaid explosions accelerate from roughly 0.36 to 0.055 seconds apart. White rises at 6 seconds, hides the hull at 6.7, holds through 7.3, and fades by 8.6. Residual authored explosions continue; exit is delayed to 9.8 seconds.

The chase uses a regenerated sibling highway image, preserving the desert road, cacti and shrubs. Alternating vertically reflected tiles put identical edge rows together at both joins and preserve continuous downward movement. This is a runtime repeat treatment, not a claim that the raw generated PNG has identical top and bottom rows. Existing full-stage master is retained. Chase speed is 480/560/620 pixels/second through the cinematic.

## Stage 5 Easy/Normal

Xenoregent spawns route to CHROME HAMMER (working name) only on Easy/Normal Stage 5. Xenoregent and all its art remain available and still serve Hard/Furious. It has not been placed in Stage 6 or 9.

SpriteCook produced the canonical chrome robot, 12-frame ship fold/unfold, hammer attack, curl/uncurl and blue/red charge reels, plus a separate generated green reticle. Asset IDs, job IDs, dimensions and SHA prefixes are stored in assets/game/stage5_hammer/spritecook-assets.json. 96 credits spent; last balance 22. Ship form is a folded alien silhouette with its hammer incorporated along the center; it is not a conventional jet. Source reels have fixed 640-square frames and retain their original canvases.

The harmless flyby rises from below, fully leaves the top, returns, brakes at 35% screen height and unfolds. Hammer mode commits green/yellow/red target warnings, performs a bottom-to-top white charge scan, leaps, releases eight laser bolts on impact, then either retargets once or leaps home. Blue shield charge absorbs 75% damage before curling.

Ball mode lasts 15 seconds, starts at 130/150 pixels per second, spins and reflects at all four playfield edges. Ordinary shots, including passive homing missiles, trigger three seconds of red/black rage, 2.25x speed and six-spike green laser volleys. Repeated shots sustain rage without postponing laser release. Manual gmiss missiles cancel rage and knock the ball away at 190 pixels/second; manual and passive missiles remain distinct. Existing x5 crates/pickups upgrade; supply rolls permit only x10/x20. Uncurl returns to hammer mode.

Laser art uses the reviewed authored eglaser_0 cell via a dedicated render path, with oriented shaft collision and full-length offscreen culling. This prevents the Stage 5 generic projectile palette from substituting small orbs.

## Verification and remaining work

Focused tests: 20/20, including real spawner routing, entrance immunity, committed warnings, all four rebounds, passive/manual distinction, sustained rage fire, supply filtering, 15-second duration, Hard preservation, and Stage 4 death timing. Syntax passed. Full suite: 3,850 pass / 58 recorded failures, exit 1, final summary reached, no new failure names against qa/pilot_reveal_0914.json. Details in qa/boss_designs_0915.json.

Native Chromium: Stage 4 rings, intact falling ship, white coverage, absent hull with residual blasts; regenerated road and repeat join inspected. Stage 5 ship entrance, transformation, hammer, yellow target/red charge, black ball, red rage, corrected green lasers, manual knockback and return to black inspected. A fixture-only onclick-before-DOM error was fixed; subsequent loads produced no new runtime errors. Native review controls are under ignored _shots/boss_designs_0915 and _shots/stage4_death_0915.

This is a playable first fight pass. Full natural-play difficulty balancing remains under SPACE-06; no measured one-in-four survival rate is claimed. Stage 2 death/head/audio and RNG dialogue are pending the boss identity answer. Nothing committed or pushed.
