# Boss animation sources — November 9

Eight accepted GPT-generated source montages and three explicitly mirrored opposite-side exports. `chronos-right.png` is a rejected left-biased attempt; it is not referenced by the game.

The editable `.aseprite` files preserve full cells and separate regular, Chrome, red, white-hit and red-hit layers. Regular is visible by default. No individual frame is resized to its bounding box. Normalization crops an expanded montage region, keeps its connected whole actor, uses one proportional scale per bank, aligns roots/soles, and applies common padding. Runtime cells are 576 × 576; source gutter overlap is not allowed to crop hammer heads.

Run `python build.py` to rebuild Aseprite sources, WebP exports and collision/weapon metadata under `exports/` and `manifest.json`. The installed Aseprite executable path is configured at the top of that script; pass only the source directory to the Lua author through the script. `python build.py --metadata-only` reconstructs masks/landmarks without altering existing artwork.

`prompt-specifications.json` records the final generation specifications and accepted/rejected roles. `jobs.json` is generated anew by the builder, so its source paths resolve to this checkout.

Runtime integration: `assets/boss_animation_art_1109.js` and `assets/boss_animation_1109.js`, loaded last in `index.html`. See `docs/BOSS_ANIMATION_1109.md` for physical ownership and `docs/qa/boss_animation_1109.json` for verification.
