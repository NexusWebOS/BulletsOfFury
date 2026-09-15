# Manual missile tiers and ammo caps — September 15, 2026

## Implemented progression

Manual Retina/free-fire missiles now use one shared four-tier table. The same exact multiplier controls projectile dimensions and direct-hit damage:

| Tier | Damage multiplier | Runtime damage | Size multiplier | Ammo cap |
| --- | ---: | ---: | ---: | ---: |
| Standard | 1.000000 | 24 | 1.000000 | 999 |
| Super | 1.250000 | 30 | 1.250000 | 50 |
| Ultra | 1.562500 | 37.5 | 1.562500 | 35 |
| Uber | 1.953125 | 46.875 | 1.953125 | 20 |

The authored pilot missile art remains intact and scales around the same center and heading. The launch plume scales with the body. The player’s passive automatic homing rack still uses its own `missileLevel`, count, damage, size and `_auto` route, so a manual tier cannot inflate the passive upgrade.

## Ammo boundary

All manual-ammo pickups now go through one tier-aware clamp, including single missiles, x2/x5/x10 compatibility routes, x20/x35/x50/x100 boxes and the cinematic grant. Firing sanitizes the held count before spending a missile, preventing an old/debug/save value above the tier cap from leaking into play.

Campaign snapshots persist the tier and store a clamped ammo count. Older saves with no tier load as Standard. Load, missile-rush restore, continue and rift-return routes all apply the current cap. Co-op carries `missileTier` in each seat’s independent run state.

The tier upgrade pickups and death reset remain tracked separately by `MSL-06`; this pass establishes the runtime tier state, progression and cap boundary they will use.

## Verification

- `node --check assets/game.js`, `_BUILD_SOURCE/test_fl.js` and `_BUILD_SOURCE/test_manual_missile_tiers_0915.cjs`: pass.
- Focused suite section 304j: 18/18 checks pass for exact names/multipliers, launch damage and dimensions, fallback behavior, ammo spend, passive separation, co-op ownership, every pickup route, save/load, missile rush and firing-time clamping.
- Full suite: 3,949 checks pass and 56 recorded assertions fail; exit code 1, with no new failure name against the 57-name baseline. The recorded Stage 7 transition assertion passes.
- Real Chromium through `_BUILD_SOURCE/shoot.py`: two final frames after 60 warm frames, no page or console errors. All requested authored missile and Stage 5 background assets returned HTTP 200.
- Pixel review: `_shots/manual_missile_tiers_0915/native_caps/shot_0001.png` shows the four actual runtime missile renders at their proportional sizes with exact damage and cap labels.

The Chromium plate uses the real `useBomb` launch path, then parks the missiles so their scale can be compared on one frame.
