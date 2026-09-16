# SPACE-22 refinement — Ground-plane target reticle

The Chrome Hammer leap and boomerang warnings now use a depth-projected floor marker instead of the former straight-on circular Retina graphic. The segmented double ring is strongly foreshortened into a horizontal ellipse, with a compressed far rim, a heavier near rim, contact shadow and restrained green spill that anchors it beneath the player.

The runtime draw now preserves the authored wide aspect ratio at both warning call sites. Green, yellow and red warning progression remains driven by the existing tint stages. The previous top-down artwork is preserved as `reticle_topdown_original_0915.png`, while `reticle.png` is the active transparent production asset.

## Verification

- `_BUILD_SOURCE/test_ground_reticle_0915.cjs` validates the asset set, wide floor aspect, both runtime call sites, removal of the square draw and the preserved warning progression.
- `node --check assets/game.js` passes.
- Native Chromium review renders the production sprite as a floor projection over a moving-playfield-style ground panel.
