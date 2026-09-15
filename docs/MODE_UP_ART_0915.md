# MODE-08 — dedicated Life Up and Continue Up art

MODE-08 is complete. Life Up and Continue Up now use separate authored pickup plates in the live powerup renderer instead of sharing the old Life Up sprite and composing a runtime `C` badge.

## Production assets

- SpriteCook job: `30e0c1a0-2b62-4e24-a3ce-99f88255a742`
- Source asset: `779c4d87-c2e6-419e-9807-2ea6f20eb6c1`
- Model: `gpt-image-2.5-flare`, 1K, medium quality
- Credits: 8 used; 14 remained after generation
- Canonical source: `assets/game/ui/pickups_0915/life_continue_source.png`
- Runtime crops: `life_up.png` and `continue_up.png`, each 442 x 546 RGBA
- Active Life Up replacement: `life_up_wings.png`, a 1520 x 882 transparent winged edit; see [wing regeneration](LIFE_UP_WINGS_0915.md).
- Alpha cleanup removed only source pixels below alpha 8. The authored edge translucency remains intact.
- Crop coordinates, dimensions, hashes and SpriteCook provenance are recorded in `assets/game/ui/pickups_0915/spritecook-assets.json`.

Both pickups share the same rugged gunmetal silhouette. Life Up uses red/orange lighting and a baked `1UP` face; Continue Up uses blue/cyan lighting and a baked `C` face. Each draws from its own file at a proportional 48–50 px gameplay height with pixel smoothing disabled. The shipped `pu_life` asset remains available as a cold-load fallback and no existing atlas cell was overwritten.

## Runtime and QA

- `drawModeUpPickup` owns the dedicated route for only `life` and `continueup`; unrelated pickups retain their existing renderer.
- `BOFDEBUG.powerups` completes the debug bridge with a live-array getter, matching its existing enemy and projectile getters, so native pickup fixtures do not reach private engine bindings.
- Focused test: `_BUILD_SOURCE/test_mode_up_art_0915.cjs` — 7 passed, 0 failed.
- Native Chromium: both registered images decoded, two independent pickups rendered at gameplay scale, and the page reported zero console errors.
- Full `_BUILD_SOURCE/test_fl.js`: 4,337 passing assertions and the established 57 failure names. No new failure name appeared; the prior Stage-7 results assertion did not recur.
- `node --check assets/game.js` passed.
