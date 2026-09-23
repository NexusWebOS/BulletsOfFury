# Stage 1 jet AI on Hard and Furious — September 23, 2026

The four ordinary Stage 1 jet variants now get difficulty specific behavior on Hard and Furious. Normal remains the authored baseline. The yellow-map rush and purple-map kamikaze files keep their separate attack books.

Each ordinary jet reads the nearest player's column at a short interval and chooses its own offset intercept lane. Straight routes steer toward that lane; corner and curve routes only sharpen a turn when pursuit agrees with the authored direction. Jets retain one constant airspeed as they bank. Their existing evasive rolls and missile dodges still have priority.

Hard and Furious jets also get more hull health, 17% and 28% greater airspeed, and shorter weapon intervals. Their twin guns commit to a bounded downward aim for a burst; Furious makes one correction halfway through. Regular bomber rockets and the black bomber's single launches aim toward the player. The black bomber retains its left, right, then four-missile sequence, with the four-missile fan rotated slightly toward the target. All shots keep their authored projectile art, launch points, muzzle effects, and sounds. The regular Stage 1 attack remains dodgeable because the gun burst commits its aim and a player move can break that line.

The settings are in `S1_JET_ELITE` in `assets/game.js`. They apply only when `run.stage===1` and `diffKey` is Hard, Furious, or Insanity. Stage 3's Fire-Shark loop/charge and Stage 4/6 jet uses are untouched.

## Checks

- `node --check assets/game.js`: passed.
- Real Chromium probe `_BUILD_SOURCE/probe_stage1_jet_elite_0923.py`: passed with no page or console errors. It measured increasing HP, speed, fire cadence, pursuit, aimed guns and missiles, the black bomber's 1–1–4 order, preserved corner route direction, and no cross-stage spill. Rendered screenshot inspected at `_shots/stage1_jet_elite_0923/furious.png`.
- The full game suite reaches its final summary at `_shots/stage1_jet_elite_0923/suite_final.log`: 4,889 passing and 81 failing (exit 1). The 81 failing assertion names match the recorded pre-change baseline exactly; no new failures.

Nothing committed or pushed.
