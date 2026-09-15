# MSL-08 — Super, Ultra and Uber missile-tier art

MSL-08 is complete. SpriteCook produced one matched six-piece family: separate Super, Ultra and Uber upgrade badges plus matching tier supply boxes. The Super box is an authored upgrade crate with an `S` plate and missile body, visually separate from the existing x5/x10 quantity boxes.

## Assets

- SpriteCook job: `a6e2e79b-399a-4e4b-bb54-175b8518cac2`
- Source asset: `3b97b686-8256-45ac-9ed7-423114cbbd9f`
- Model: `gpt-image-2.5-flare`, 1K, medium quality
- Credits: 8 used; 6 remained after generation
- Canonical source: `assets/game/ui/missile_tiers_0915/missile_tiers_source.png`
- Runtime assets: `super_icon.png`, `ultra_icon.png`, `uber_icon.png`, `super_box.png`, `ultra_box.png`, `uber_box.png`
- Crop coordinates, dimensions, hashes and generation provenance are recorded in `assets/game/ui/missile_tiers_0915/spritecook-assets.json`.

The family uses dense dark gunmetal, silver missile bodies and one common red equipment band. Super uses red/orange energy, Ultra uses cyan-white, and Uber uses violet-white. Both the badge and crate families grow visibly by tier. The dedicated renderer preserves each source aspect, disables smoothing, keeps the tier letters upright, and leaves the existing quantity-box paths unchanged.

## Verification

- Focused test: `_BUILD_SOURCE/test_msl08_art_0915.cjs` — 15 passed, 0 failed.
- Native Chromium: all six files decoded and rendered together at gameplay scale; the fixture reported `ready:true`, `count:6`, and zero console errors.
- Full `_BUILD_SOURCE/test_fl.js`: 4,337 passing assertions and the exact established 57 failure names; no failure name changed.
- `node --check assets/game.js` passed.

The art and renderer are ready for the MSL-06/MSL-07 ordinary-play spawn and wave-gate connection. Those gameplay rows remain partial until that follow-up is implemented and tested.
