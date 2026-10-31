# Prism Bastion balance and presentation QA — 2026-10-13

The current normal-difficulty build clears through both breaches, Prism Heart and Helios using ordinary input-driven attacks with six armor. The production index was loaded in Chromium, with its normal art and modules. No enemy health, kill API, player armor, or invulnerability was changed during either complete run.

| Full input run | Finish | Armor | Damage / deaths | Kills | Cover blocks | Rocket intercepts | Grenades remaining |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Mouse aim | 88.68 s | 6 / 6 | 0 / 0 | 21 | 24 | 0 | 1 |
| Retina + directional buttons | 106.75 s | 6 / 6 | 0 / 0 | 21 | 42 | 3 | 1 |

The bot chooses its action and target every 250 ms. It prioritizes corner turrets, locks a controller target until defeated, uses up to three grenades per breach against groups, ducks approaching rounds, and moves out of rocket and geyser lanes. The controller run drives the game's rate-limited cursor through Retina plus directions; cursor-direction release is evaluated each tick. Both runs naturally encountered Helios's run, return, volleys, lightning and jump. This tests the input path and mechanics; it does not replace human playtesting or physical 8BitDo hardware validation. The bot reads exact target and warning state, so these flawless results are not estimates of an average player's performance.

The preceding less deliberate strategy (no grenades, infantry before turrets, frequent controller target switching) died in breach 2 at 72 seconds with mouse aim, and in breach 1 at 19 seconds with directional aiming. Those results are preserved in `_shots/bastion_balance_1013/no_resource_strategy.json`. The contrast supports a medium-difficulty candidate that rewards cover, target choice and limited resources. Keep the grenade binding visible alongside the cover and Retina controls.

A separate passive player took six real damage and fell. Isolated boss fixtures verified orange core fill, lane warnings and cover protection, white transformation flash, full Helios health, orange then animated red health fill, full offscreen run and same-edge return, timed prism volleys, lightning warning, visible jump height, and a normal-armor sidestep escaping the slam geyser. These fixtures explicitly set boss states and reset armor between independent cases; they are mechanic checks, not complete-run evidence.

All 18 checks passed, with no page or console errors. All 21 reinforcement entries began north of the screen. Screenshots were inspected for foreground cover, rear-facing player, grounded enemy feet, non-overlapping messages, health bars and boss attacks. Source hash and detailed metrics are recorded in `docs/qa/overdrive_bastion_balance_1013.json`.

Reproduce with `python expansion/topdown/_research/probe_bastion_balance_1013.py`. Evidence is saved under `_shots/bastion_balance_1013/`.
