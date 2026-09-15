# Persistent achievement registry — 2026-09-15

ACH-01 is complete. `assets/game.js` now owns one account/profile achievement store under `bof_achievements_v1`. It is independent of campaign save slots and records stable achievement IDs, unlock timestamps, optional event metadata, points, and a unique future Steam key.

The registry declares 66 requested achievements: nine pilot campaign clears; nine stage clears; nine no-death clears; nine no-manual-missile clears; nine Hard boss victories; nine Furious boss victories; seven level-five weapon awards; the no-continue campaign award and trophy reward key; and four Stage-1 boss/miniboss speed awards.

Unlocks are one-time and reject unknown IDs. Metadata and profile snapshots are copied before exposure, point totals are derived from validated definitions, corrupt or old-version storage falls back to an empty profile, and unknown saved IDs are discarded. Each accepted unlock is also placed on an in-memory Steam queue and emits `bof-achievement` for the future notification UI.

Gameplay triggers are now connected at the shared lifecycle boundaries. Stage results award clears on Normal or above, no-death clears on Normal or above, and missile-discipline clears on every difficulty; co-op requires both seats to satisfy a clean condition. Boss and miniboss defeat hooks award difficulty victories and Stage-1 speed tiers. Weapon pickups award the relevant level-five achievement. Campaign and Arcade victory award the selected pilot's campaign clear, and a run with no spent continue awards 1,000 points. The trophy-avatar art attached to that last achievement remains pending SpriteCook.

Stage-1 speed awards use exclusive tiers: a kill under 60 seconds earns 500 points, while a kill from 60 through 119.99 seconds earns 200. A fast kill therefore does not silently stack to 700 points.

## Verification

- `node --check assets/game.js`: pass. The file retains LF line endings.
- Focused registry and trigger checks inside `_BUILD_SOURCE/test_fl.js`: 37/37 pass. They cover the registry contract plus Easy/Normal/Hard/Furious eligibility, solo and co-op clean-run rules, exclusive speed tiers, encounter deduplication, continue use, weapon thresholds, and all runtime hooks.
- Complete harness: 3,998 pass / 56 fail, exit 1. No new failure names appeared against the preceding 57-name run; the existing intermittent `a second lance may destroy the wounded 3-drone column` assertion did not recur. The complete achievement section is green.
- Real Chromium registry proof: 16 native frames at five fps. The final frame visibly shows 66 definitions/Steam IDs, two unlocks, 110 points, duplicate rejection, and successful storage reload. Evidence: `_shots/achievement_registry_0915/native/shot_0015.png`.
- Real Chromium trigger proof: 20 native frames at five fps. The final frame shows a clean Stage-3 award, Hard Stage-2 boss award, level-five Laser award, Arcade Decker clear, no-continue award, duplicate rejection, seven unlocks and the exact 1,630-point total. All requested assets returned HTTP 200 and there were no page or console errors. Evidence: `_shots/achievement_registry_0915/native_triggers/shot_0019.png`.

The achievement menu/notification UI and trophy avatar remain queued. No commit or push is part of this pass.
