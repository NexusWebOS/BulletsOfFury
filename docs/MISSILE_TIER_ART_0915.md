# MSL-08 — Super, Ultra and Uber missile-tier art

MSL-08 is complete. The production family contains six independent pieces: a badge icon and armored pickup box for Super, Ultra and Uber. Every piece now carries the legendary `M` missile mark plus the full tier name, so no tier depends on an `S`, `U` or `X` abbreviation.

## Assets

- Canonical transparent family sheet: `assets/game/ui/missile_tiers_0915/missile_tiers_source.png`
- Preserved Uber chroma-key source: `assets/game/ui/missile_tiers_0915/uber_magenta_source.png`
- Runtime assets: `super_icon.png`, `ultra_icon.png`, `uber_icon.png`, `super_box.png`, `ultra_box.png`, `uber_box.png`
- Crop coordinates, dimensions, hashes and image-generation provenance are recorded in `assets/game/ui/missile_tiers_0915/imagegen-assets.json`.

The progression changes both color and construction. Super is navy blue with a fast twin-exhaust missile and reinforced fins. Ultra is orange and black with a broader segmented warhead, four-fin chassis and hotter exhaust. Uber is nuclear green with a faceted multi-stage warhead, exposed energy core, triple vector exhaust and swept wings visibly rooted into the fuselage. Its matching heavy crate carries the same assembled connected-wing missile. The Uber source was generated against a solid magenta plate and keyed to transparent RGBA for runtime use.

The dedicated renderer preserves each source aspect, disables smoothing, keeps the labels upright and leaves the existing x5/x10 quantity-box paths unchanged. Ordinary waves use these boxes through the existing Super/Ultra/Uber upgrade lifecycle.

## Verification

- Focused test: `_BUILD_SOURCE/test_msl08_art_0915.cjs` — 15 passed, 0 failed.
- Asset inspection: all six files are trimmed RGBA images with transparent backgrounds and unique hashes.
- Native Chromium: all six files decoded and rendered together at gameplay scale; the fixture reported `ready:true`, `count:6`, and zero console errors.
- Full `_BUILD_SOURCE/test_fl.js`: 4,337 passing assertions and the exact established 57 failure names; no failure name changed.
- `node --check assets/game.js` passed.
