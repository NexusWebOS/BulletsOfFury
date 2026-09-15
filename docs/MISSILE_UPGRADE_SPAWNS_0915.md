# MSL-06 / MSL-07 — ordinary-play missile-tier upgrade boxes

MSL-06 and MSL-07 are complete. The authored Super, Ultra and Uber boxes now enter ordinary stage play from the same authored-wave boundary that advances their progression gate.

## Live progression

1. A Standard pilot receives the first Super-box offer on the second authored wave.
2. Collecting Super replaces Standard, enforces the 50-round cap and locks Ultra.
3. Surviving the following authored wave marks Ultra ready and immediately offers its cyan box.
4. Collecting Ultra enforces the 35-round cap and locks Uber until the following survived wave.
5. Collecting Uber enforces the 20-round cap and completes the chain.

Only one active tier box exists per player. A missed box may be offered again on a later authored wave. Death resets the pilot to Standard and clears the gate, as before. In co-op, each offered box carries a seat owner and only that pilot may collect it; one player cannot consume or invalidate the other player's progression.

The falling boxes use the dedicated SpriteCook crate family from MSL-08. Collection resolves each box to the corresponding existing `missileup_super`, `missileup_ultra` or `missileup_uber` grant, keeping the tier/cap logic in one place.

## Verification

- Focused test: `_BUILD_SOURCE/test_missile_upgrade_spawns_0915.cjs` — 12 passed, 0 failed.
- Native Chromium stepped Standard → Super/Ultra-ready → Ultra/Uber-ready and showed the live Super, Ultra and Uber box offers; the final report was `tier:"ultra"`, `box:"missileupbox_uber"`, with zero console errors.
- Full `_BUILD_SOURCE/test_fl.js`: 4,337 passing assertions and the exact established 57 failure names.
- Two legacy quantity-box assertions now set Standard tier inside their own setup. This prevents earlier tier simulations from leaking an Uber 20-round cap into tests whose stated purpose is standard x50 and +1 stock behavior.
- `node --check assets/game.js` passed. `_BUILD_SOURCE/test_fl.js` remains pure CRLF.
