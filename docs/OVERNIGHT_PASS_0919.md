# Overnight repair pass — 2026-09-19

The current runtime was audited against `docs/WORK_ORDER_0914.md`, `docs/TODO_PORTRAITS.md`, asset folders, and the broad harness. Two historical missing-art reports are stale: all nine pilots already have their 12 core dialogue portraits and one standing body, and `assets/game/ui/forge_0917/` contains the 405 element/weapon/level badges. The broad legacy suite ends with 74 failures and includes many source-text assertions; it is not a reliable count of newly broken behavior.

## Repairs

- Stage-clear achievement cards stay queued while the debrief is visible. The next screen plays them; the debrief's score conversion, sign-off, password, and Continue remain unobscured.
- `BULLETS FIRED` displays the actual shot count. Its fill follows shots toward a 1000-round saturation point; `WEAPON ACCURACY` remains the separate hits/shots percentage.

## New art

Built-in ImageGen edit with `yuri-idle.png` as the identity reference: combat-alert expression, same mohawk, tattoo, goatee, black scarf and red jacket. Saved as `assets/game/pilot_portraits/yuri-alert-0919.png`; runtime key `port_cf_yuri_alert`.

Built-in ImageGen edit with `cole-idle.png` as the identity reference: urgent combat-alert expression, same swept hair, beard, dark green flight armor and metal-corner framing. Saved as `assets/game/pilot_portraits/cole-alert-0919.png`; runtime key `port_cf_cole_alert`.

Built-in ImageGen generation using the approved fire-laser palette as style reference: transparent 180-degree Fire Whip lash with hot white/yellow core and red ember edge. Saved as `assets/game/player_weapons/fire_whip_0919/fire_whip_fx.png`; runtime key `fire_whip_fx_0919`.

Built-in ImageGen generation using the existing Fire laser badge as UI reference: isolated Fire Whip badge. Saved as `assets/game/player_weapons/fire_whip_0919/fire_whip_icon.png`; runtime key `micon_firewhip_0919`. The Fire Whip remains asset-ready only; attack movement, collision, damage and forge selection are not implemented in this pass. Existing art was not replaced.

## Verification

`node --check assets/game.js` and `python _BUILD_SOURCE/probe_overnight_pass_0919.py` pass. Chromium confirms 2,841 shots display as `2841`, accuracy as `63%`, queued achievements pause during stage clear then resume, and all four new asset keys decode without page errors. Visual proof: `_shots/overnight_0919/stageclear_debrief.png`.
