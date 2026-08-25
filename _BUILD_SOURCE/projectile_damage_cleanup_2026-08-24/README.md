# Projectile and damage-effect cleanup review

This folder is non-live review material. Nothing here is referenced by `assets/manifest.js` or `assets/game.js`.

## Projectile scan

- Families scanned: 32
- Frames scanned: 192
- Candidate frames with disconnected micro-components removed: 144
- Families with at least one candidate change: 26
- Changed families: vfx-cosmic-crescent-arc-muzzle, vfx-cosmic-gravity-leech-orb, vfx-cosmic-ion-tracer, vfx-cosmic-lattice-fan, vfx-cosmic-manta-wave, vfx-cosmic-phase-split-bolt, vfx-cosmic-prism-impact, vfx-cosmic-rift-collapse, vfx-cosmic-void-shock-ring, vfx-cosmic-warden-beam-head, vfx-cosmic-warp-needle, vfx-heavy-blacksteel-penetrator, vfx-heavy-blacksteel-rail-muzzle, vfx-heavy-cryo-cannon-muzzle, vfx-heavy-cryo-missile, vfx-heavy-cryogenic-lance, vfx-heavy-emp-shock-ring, vfx-heavy-flak-blossom, vfx-heavy-heavy-fuse-bomb, vfx-heavy-ice-shatter-impact, vfx-heavy-incendiary-plasma, vfx-heavy-inferno-impact, vfx-heavy-inferno-micro-missile, vfx-heavy-military-cannon-muzzle, vfx-heavy-rotary-cannon-muzzle, vfx-heavy-toxic-jungle-missile

The cleanup is intentionally conservative. It runs only when one connected body owns at least 55% of visible pixels. Components near the body remain, and multi-pellet/impact families are not auto-cleaned.

## Existing damage/smoke reels

- Reels extracted from the live manifest: 25
- Reels whose frames are exact duplicates: 0
- Exact-duplicate reels: none

The CSV also records warm-pixel and neutral-smoke pixel variation. Low variation identifies effects that may technically have multiple frames while their fire/smoke remains visually frozen.

## Static damaged/critical cells

- Unique cells compared against intact counterparts: 465
- Eight-frame moving fire/smoke candidates generated: 222 (1,776 frames)
- Frame 1 is the exact shipped damaged sprite. Frames 2–8 remove the complete baked smoke cloud—including dark rims, midtones, and highlights—then move the whole plume upward and laterally while its lobes deform. Flame tongues and embers move independently over the unchanged damaged hull.
- 211 reels have visible effect-alpha/silhouette motion; the remaining 11 move effect shapes over already-opaque hull pixels.
- Canvas dimensions, damaged hull pixels, hull silhouette, and anchors remain stable.
- `previews/damage_effects/index.html` is the animated review gallery. `previews/damage_effects/qa-selected-eight-frame-sheet.png` is the compact QA sample.

## Review locations

- `previews/projectiles/`: original and cleaned candidate GIFs; changed families also have comparison PNGs.
- `previews/damage_reels/`: live damage/smoke reels extracted from atlases.
- `audit/projectile_audit.csv`: component-level projectile results.
- `audit/damage_reel_audit.csv`: reel uniqueness and effect-pixel variation.
- `candidates/projectiles/`: standalone candidate PNGs, never wired.
