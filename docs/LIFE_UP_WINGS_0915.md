# Winged Life Up regeneration

The active Life Up pickup now has symmetrical armored jet wings. The original SpriteCook badge remains preserved as `life_up.png`; the live registration uses the cache-safe replacement `life_up_wings.png`. Continue Up is unchanged.

The wings use stepped silver/gunmetal tips, red armor and orange vents that match the badge. The complete silhouette remains 50 pixels tall in the existing proportional renderer, making the wing span visible without reducing the `1UP` face below readable size.

## Production

- Generator: built-in `image_gen`, precise-object edit
- Edit source: `assets/game/ui/pickups_0915/life_up.png`
- Active asset: `assets/game/ui/pickups_0915/life_up_wings.png`
- Production dimensions: 1520 x 882 RGBA
- Alpha cleanup: only pixels below alpha 8 were cleared
- Provenance: `assets/game/ui/pickups_0915/imagegen-assets.json`

Final prompt:

```text
Use case: precise-object-edit
Asset type: Bullets of Fury in-game Life Up pickup sprite
Primary request: Add a matched pair of compact mechanical wings extending horizontally from the left and right sides of the existing Life Up badge.
Style/medium: crisp dense 16-bit arcade pixel art with hard pixel edges.
Composition: symmetrical front-facing icon with transparent padding; armored jet wings in gunmetal, silver, red and orange, with stepped silhouettes and a slight upward sweep.
Constraints: Preserve the central badge, large white 1UP text, palette and lighting. Add only the two wings. Genuine transparency; no backdrop, shadow, extra text, watermark or cropping.
```

## Verification

- `_BUILD_SOURCE/test_mode_up_art_0915.cjs`: 7 passed, 0 failed.
- `node --check assets/game.js` passed.
- Native Chromium rendered the winged Life Up beside the unchanged Continue Up at gameplay scale; both decoded, two pickups remained active, and the console had zero errors.
- The runtime logic and sizing formula are unchanged, so the established full-suite baseline from the immediately preceding missile-tier push remains applicable.
