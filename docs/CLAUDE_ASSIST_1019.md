# Claude Code assist pass - October 19, 2026

Mike asked Claude Code to help Codex's overnight combat pass (docs/OVERNIGHT_COMBAT_1019.md) "as much as
possible with animation, effects, glows, enemy AI". To keep one writer per file, Claude took items 7, 8, 6 and 4
of that list and worked only in a new late layer, `assets/claude_assist_1019.js` (loaded right after
`rime_defense_1019.js`). game.js, test_fl.js and every Codex owner file are untouched. `window.CA19_OFF=1`
turns the whole layer off - every probe below uses that as its busted arm.

| Item | Mike | Cause found (measured first) | Change | Proof |
|---|---|---|---|---|
| 7 | Lizzie's MG slow in space with her special | Docked heavy MG: 24 rounds/s on stage 1, 9/s on stage 5. `_weaponCadence` returns the space-weapon beat before it reaches the mount check, while `pShoot` still hands the trigger to the mount. | Mount owns the cadence wherever it is docked. | `probe_lizzie_space_mg_1019.py` 4/0; busted 9/s fails |
| 8 | Center the Spread muzzle flash on all ships | Flash ink 2.0-2.4 px right of the nose on all nine. `wm26PlayerNose` adds a flat +2 after its own pixel anchor. | +2 removed (also re-centres nose MG rows). | `probe_spread_muzzle_1019.py` 10/0 (all <= 0.4 px); busted 1/9; `probe_machinegun_1018.py` still 233/0 |
| 8 | "slow down on Lizzie, it was going so fast" | NOT REPRODUCED: with each pilot's real stats Lizzie's Spread is 5.6 px/frame and 7.5 volleys/s at L3, identical to Cole/Maverick/others (Yuri and Falva are faster, 9/s). | none | needs Mike: which weapon / stage / state |
| 6 | Stage 5 enemies don't shoot | (a) `spaceBulletHit` has no visibility gate and space-laser rounds live to y<-50: the laser killed whole waves above the screen (station, gravity well, satellite, minelayer: 0 visible frames). (b) Every S5SPACE hull spawned at 12 HP - authored 28-120 hp passed through `EHP()`, the fodder cap. | Space rounds hit an ordinary enemy only once its centre is on screen (bosses/minibosses/pieces/rocks and locks unchanged). Authored hp restored as the Normal pool, EHP's difficulty/co-op ratio kept (MODE-04 Hard +15% holds). | `probe_stage5_fire_1019.py --fire`: 0 off-screen kills, station 120 hp; busted 11 off-screen kills, 12 hp. Stage 9 also 0 off-screen kills |
| 4 | Stage-8 Hammer form doesn't spin like the real Hammer | Same states on both. Stage 5's whirlwind reel winds up and accelerates on `h.whirl.reel`; Stage 8 stepped 4 poses on a flat `t*9`. Ball rotation measured equal (~570 deg/s) - it looks still because its art is nearly radially symmetric. | Stage-8 whirl poses ride `reel/2`; spin/twirl winds up. | `probe_hammer_whirl_1019.py` 11 -> 19 changes/s, 100% on the reel; busted flat 9/9 |

Open / for Codex's item 9 and asset backlog:
- First Stage-5 volleys land 1.3-5 s after a unit arrives; a direct `_fcd` clamp did not move it (the enemy
  behaviour/pattern controller wrappers own that timing). Stage 9 shows the same "dies before shooting" pattern
  (s9interceptor 7/12) - not changed, not named by Mike.
- Stage-8 Hammer: an authored rolling-ball reel with asymmetric features and a twirl/overhead reel are needed
  for the remaining "lacks animation" gap; that is art, not code.

No commit, no push. Evidence JSON under `_shots/claude_assist_1019/`.
