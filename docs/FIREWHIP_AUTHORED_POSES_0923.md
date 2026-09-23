# Firewhip authored poses — September 23, 2026

Supersedes the strip deformation described in FIREWHIP_LASH_0923.md. The runtime now displays 16 generated whole-whip poses: windup, curl, outward lash, reversal, and return. Each pose stays anchored at the ship muzzle, without mirroring or strip deformation.

Whip frames and the eight approved circular muzzle frames share a palette sampled from the game's flamethrower (`nfw2_2`, fire palette `#ff6924`) and fire orb (`nfb_orb3_3`). Their original alpha is preserved apart from faint background residue. Existing damage, reach, and half-stroke timing are retained. Collision uses merged alpha-mask cells from the displayed poses, including crossed frames between updates, with one hit per target per half-stroke.

## Assets and provenance

- Folder: `assets/game/player_weapons/fire_whip_lash_0923/`.
- Master SpriteCook asset: `7eebc4c8-e086-42fc-8951-26f5ad1dc255` (GPT2.5 Sunburst).
- Normalized animation source: `a980929d-629a-4d6f-bc09-8237e238da7e`.
- Animation asset: `c1fe952b-34ab-4e7a-843f-0f07643864b7` (pixel-engine-v1.5, 16 frames).
- Generation consumed 42 credits: 16 for the referenced master and 26 for animation.
- Prompts, source reel, normalized poses, collision metadata, and PNG hashes are retained in the asset folder.
- Builder: `_BUILD_SOURCE/build_fire_whip_lash_0923.py`. After regenerating poses, synchronize its `collision.json` output with `FIRE_WHIP_POSES` in `assets/game.js`.

## Verification

- `node --check assets/game.js`: passed.
- `_BUILD_SOURCE/probe_firewhip_muzzle_0923.py`: passed in real Chromium. Verified all 16 whole-sprite draws, matching circular muzzle, moving anchor, attack stop, every baked collision cell, and one hit per stroke. No page or console errors. Inspected rendered contact sheet and detail screenshot.
- Full suite reached its summary: 4,889 passing, 81 failing, exit 1. No new assertion names against the recorded 81-failure baseline. Compared with the immediately preceding 80-failure run, the known intermittent sand-tank spawn assertion returned.
- Visual replay: `_shots/firewhip_muzzle_0923/authored_whip.gif`.

Changes remain local; no commit or push was requested for this revision.
