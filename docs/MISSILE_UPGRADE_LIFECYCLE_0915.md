# Manual missile upgrade lifecycle foundation — September 15, 2026

## Implemented engine path

The manual missile upgrade state is now independent for each player and follows the requested order:

1. Standard can accept a Super pickup immediately.
2. Taking Super replaces Standard, clamps the bank to 50 and locks Ultra.
3. The next authored stage-wave dispatch marks Ultra eligible if the player is still alive.
4. Taking Ultra replaces Super, clamps the bank to 35 and locks Uber until another authored wave.
5. Taking Uber replaces Ultra and clamps the bank to 20.
6. A real unshielded player death resets the equipped manual tier and upgrade gate to Standard.

The gate uses a monotonic per-player wave serial rather than the stage-local `waveIdx`, so an upgrade acquired near a stage boundary can mature during the next stage. Co-op advances both players' independent gates when a shared authored wave dispatches. Campaign snapshots preserve the tier, gate, eligibility and serial; older saves fall back to Standard.

`applyPowerup` accepts the future authored pickup kinds `missileup_super`, `missileup_ultra` and `missileup_uber`. Ineligible or out-of-order pickups are refused. No placeholder pickup art or temporary spawn was added.

## Current limitation

`MSL-06` and `MSL-07` are complete. The SpriteCook boxes from `MSL-08` now spawn from authored-wave boundaries, obey the existing next-wave gate, retry after missed offers, and remain seat-bound in co-op. See [ordinary-play spawn proof](MISSILE_UPGRADE_SPAWNS_0915.md).

## Verification

- Syntax checks pass for `assets/game.js`, `_BUILD_SOURCE/test_fl.js` and `_BUILD_SOURCE/test_manual_missile_tiers_0915.cjs`.
- Focused suite section 304j: 30/30 checks pass across exact tier math, caps, pickup routing, sequential eligibility, two wave gates, co-op ownership, persistence and the real death-path hook.
- Full suite: 3,960 checks pass and 57 recorded assertions fail; exit code 1. The only failure name outside the 57-name recorded baseline is the repository's documented intermittent Stage 1 sand-tank scheduler assertion, while the baseline Stage 7 transition assertion passes.
- Real Chromium through `_BUILD_SOURCE/shoot.py`: 23 frames at 5 fps over 4.6 seconds after 60 warm frames, with no page or console errors.
- Pixel review: `shot_0002.png` shows Super with Ultra eligible after a wave, `shot_0006.png` shows Ultra with Uber eligible, `shot_0013.png` shows Uber and its 20-round cap, and `shot_0018.png` shows the Standard death reset.

The Chromium sequence invokes the actual upgrade, wave-observer, `useBomb` and reset functions. Its labels are verification instrumentation; the authored pickup presentation remains outstanding.
