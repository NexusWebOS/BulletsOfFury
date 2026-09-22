# Fast score tally and Fury Supplies — September 22

- [x] Solo and co-op results finish the score, row, rank, password and Fury Points presentation within 0.8 seconds. A/Fire snaps the presentation to its final values; another press continues. Score uses a stable results snapshot. Repeated renders neither re-award score nor convert Fury Points twice.
- [x] Added **Fury Supplies** after loadout. If a space-stage transition skips weapon loadout, supplies remain available without showing spaceship upgrades. The completed campaign finale skips shopping.
- [x] Extra life: **250 FP**, maximum **9 lives**. Extra continue: **750 FP**, added to the existing run's Continue Up reserve. Unlimited continues cannot be purchased. Co-op exposes separate P1/P2 life rows and the shared continue reserve.
- [x] Purchases use the existing earned Fury Point balance. Repeatable supply spending persists in the profile ledger and survives normalization/reload without changing weapon-upgrade prices. Score remains untouched. Existing campaign snapshots include purchased lives and continue reserves.
- [x] Insufficient funds, full life stock, unlimited continues and profile-save failure never charge points. Save failure also rolls back granted stock. Holding Fire does not buy repeatedly.
- [x] D-pad selects, A buys/selects, B returns to loadout when available, Start continues without buying; rows are clickable. Fixed shared widescreen debrief pointer mapping for supplies and existing forge/loadout menus.
- [x] Reused authored life/continue icons, debrief panel strips, graphical lettering and pad prompts on a black background. No generation credits spent.

## Verification

`_BUILD_SOURCE/probe_supplies_0922.py` runs the real game in Chromium with empty temporary storage. Verified the native results → unlocks → loadout → supplies route; keyboard, held-fire and mouse purchases; Back/return; skip/exit exactly once; co-op purchase and tally; profile round-trip and campaign stock snapshot; all purchase guards and failed-save rollback. Totals were final before one second, including a 2.5-million-point score. Page and console errors: zero.

Inspected screenshots of the quick tally, shop, purchase feedback, portrait window and co-op rows. Evidence: `_shots/supplies_0922/`. Updated the existing Arcade route and forge-chain assertions to include the new optional supplies menu. Existing work preserved; nothing committed or pushed.

Final verification: node --check assets/game.js passed. The full node _BUILD_SOURCE/test_fl.js suite reached its final summary and exited 1 with 75 failures, all present in the recorded 76-failure baseline; no new failure names. The intermittent sand-tank spawn failure did not recur. Log: _shots/supplies_0922/test_fl_final.log.
