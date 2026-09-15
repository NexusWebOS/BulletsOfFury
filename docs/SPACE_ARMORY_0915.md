# SPACE-24 — Fury HQ Space Division armory

Space Stages 5 and 9 now receive a dedicated Fury HQ supply crate in addition to their normal Gravity Mode weapon crates. It arrives after seven seconds and then every 19 seconds during ordinary combat or every 24 seconds during a boss. A shuffled three-item bag deals each reward once before repeating, while each crate stores its result at spawn so the contents never reroll while falling.

## Generated art

The production set lives in `assets/game/ui/space_armory_0915/`:

- `fury_hq_box.png` — blue gunmetal Fury HQ / Space Division crate.
- `helper_orb_icon.png` and `helper_orb.png` — pickup badge and deployed autonomous orb.
- `akimbo_icon.png` — crossed dual-cannon upgrade badge.
- `proximity_mine_icon.png` and `proximity_mine.png` — pickup badge and deployed red/gray sensor mine.
- `shrapnel_long.png` and `shrapnel_forked.png` — two separate rotating mine fragments.
- `space_armory_magenta_source.png` — preserved generated chroma-key sheet.
- `imagegen-assets.json` — source regions, trim regions, dimensions and hashes.

All runtime pieces are individually trimmed RGBA files. The source uses a flat magenta background so the silver, blue, red and cyan interiors survive extraction cleanly.

## Rewards

- **Helper Orb:** orbits the collecting pilot for 30 seconds, independently acquires the nearest forward target inside 430 pixels and fires a cyan support lance every 0.56 seconds. A second pickup refreshes its lifetime.
- **Akimbo Weapons:** lasts for the current space stage. Laser Cannon grows from two to four physical firing hardpoints, producing 24 pulses over its existing six-beat burst. Shadow Orb launches two separately travelling charged orbs. Volley Missiles grows from its normal three-missile rack to four independently guided missiles.
- **Proximity Mine:** deploys immediately behind the collecting craft, arms in 0.42 seconds, and watches a 62-pixel sensor radius including the target hull edge. Contact or proximity triggers a 104-pixel splash blast for 20 damage and twelve outward shrapnel projectiles for 7 damage each. An untriggered mine self-detonates after 18 seconds.

The crate is shootable by the normal space weapons and the generic special/projectile container paths. Intact crates cannot be collected by collision; only the released badge can be collected.

## Verification

- `_BUILD_SOURCE/test_space_armory_0915.cjs`: 23 passed, 0 failed.
- `node --check assets/game.js`: passed.
- Asset validation: eight unique trimmed RGBA runtime files with transparent backgrounds.
- Native Chromium fixture: generated crate, three badges, deployed orb, deployed mine and both shrapnel bodies decoded and rendered in the Stage-5 playfield.
- Full `_BUILD_SOURCE/test_fl.js`: 4,338 passing assertions and 56 failures; no new failure name. The former baseline failure `stage 1: the sand tanks spawn (scroll never)` now passes.
