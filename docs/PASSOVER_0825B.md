# PASSOVER 0825B — Shield Scope, Stage 8 Visibility, and Entry Spacing

## Result

- The imported energy-shield runtime remains available for selected miniboss and boss encounters.
- Ordinary enemies no longer receive shields automatically. Encounters must opt in explicitly with `enemyShieldEquip(enemy, family, energy, options)`.
- Stage 8 no longer spawns the quarantined `el_hd` multipart carrier. Both remaining `el_hd` wave slots now use the intact Void Hauler.
- The anti-stacking pass no longer pushes aircraft from the hidden entry runway across the camera reveal line.

## Runtime contract

- `ENEMY_SHIELD_LOADOUT` is intentionally empty. Shield families are reserved assets, not a general-enemy modifier table.
- The shield showcase equips its test subjects explicitly; it does not prove or create ordinary-enemy loadouts.
- Stacked aircraft that are still above the fitted camera split sideways. Once both hulls have entered, the regular shortest-axis separation rule resumes.
- Vertical separation uses the fitted camera top instead of the obsolete hard `y=-100` clamp.
- Stage 8 carrier beats at 35.5 and 52.5 seconds use live, drawable Hauler art and never the culled `el_hd` body.

## QA harness repair

- `shoot.py` and `probe_enemies.py` now use a threaded local asset server.
- Manual frame stepping traps the browser-owned `requestAnimationFrame` chain before calling `loop()`; one manual frame no longer creates another live animation loop.
- Synthetic time stays monotonic across batches, and batches yield briefly so lazily touched art can decode.
- The enemy probe measures the fitted camera bounds, exempts authored in-place reveals such as the Stage 7 sludge maw, and clears encounter miniboss gates after rendering them so later roster entries are still audited.

## Verification

- `node --check assets/game.js` — pass.
- `node --check _BUILD_SOURCE/test_fl.js` — pass.
- `python -m py_compile _BUILD_SOURCE/probe_enemies.py _BUILD_SOURCE/shoot.py` — pass.
- `git diff --check` — pass.
- Stage 8 25-second Chromium entry audit: 14 spawned, 0 invisible, 0 vanished, 0 pop-ins.
- Stage 8 real Chromium capture at `stageTimer=25.03`: rendered gameplay, HUD, enemy hulls, projectiles, and continuous space background successfully.
- Regression section 51 forbids `el_hd` from Stage 8 and requires the live Hauler carrier lanes.
- Regression section 213b proves stacked hidden entrants remain outside the camera until their own movement brings them in.
- Regression section 237 proves all 84 shield assets and six families remain live while ordinary enemies auto-equip none.
- Full regression run returns only the same seven pre-existing stale failures: Stage 6 master/scroll expectations, preload threshold, missing historical `_superseded` ledgers, and stale cloud-stage palette expectations.
