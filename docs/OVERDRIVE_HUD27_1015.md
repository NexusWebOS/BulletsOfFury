# Overdrive HUD27 — solid health, custom font and equipment panel

2026-10-15, build `overdrive1015-hud27-r1`, preview port8781.
Revises Corner26 in stages3/7 to match Mike's requested changes.

Health uses newly generated uninterrupted green/red fill plates. There are no
segment gaps; HP clips the continuous plate proportionally. The existing local
portrait and rectangular gauge frame remain. Fill switches red at30% HP.

PixelLab generated the original **Overdrive Arcade HUD** font:80 glyphs,
16x16 cells, actual source atlas128x160 /8columns x10rows, baseline13, cap top3
and height10. This actual grid differs from the service's generic10x8 wording;
the builder uses the measured PNG dimensions. Raw atlas and generated TTF are
retained. Runtime uses the bitmap masks directly with nearest sampling and
colored faces/dark offset shadows; no browser-font substitute in player HUD.
Lives, ammo, action, Score and High Score all use this generated font. Text
measurement uses glyph bounds and consistent baseline/advance, centered inside
the two equipment text fields and the score columns. Unlimited ammo reads INF
because the generated repertoire has no infinity glyph; finite ammo is numeric.

The equipment panel is204x78, with a bordered66x56 gun inset at left and two
104x16 text slots at right. Ammo and action are centered in their actual slots,
not anchored to an outside edge. Gun pictures change with the equipped weapon:
rifle, Desert Eagle, spread shotgun, minigun, fusion beam, napalm and rockets.
The rifle icon is newly generated; six existing actual weapon pickup pictures
are cropped/padded locally into64x40 display cells without changing originals.
Stage7 shotgun/laser map to spread-shotgun/fusion-beam art; weapon depletion
returns the shown picture to rifle through the existing actual weapon state.

Stage7 scenery is darkened25% by a black-alpha exposure pass immediately after
the actual Three.js room render. Actors, front-cover flats, projectiles, effects
and subsequent HUD draws retain their authored colors. Lighting/shadows and the
reactor/Helios glow remain active. The overlay's DoubleSide material accounts
for the native screen-space camera orientation. Native frozen before/after RGB
region ratios: 0.750437, 0.750737, 0.750159, close to
0.75 after8-bit rounding. A foreground barrel was excluded from the floor sample
because foreground objects deliberately bypass this scenery pass. The equipment
HUD region is pixel-identical before/after exposure. Stage3's top-down floor
does not use this stage7 room pass.

Boss bar moves another20px down (center113) to clear the taller equipment box;
target alerts and stage7 boss messages follow. Conversations, saved high score,
health/ammo values, weapon behavior, controls, AI and encounter pacing remain.

Owner `_research/build_hud27.py`; source art/font/prompts/job IDs/hashes at
`art/hud27/source`.90registered PNGs:80glyphs,3UI pieces,7weapon images.
Runtime `js/hud27.js`, registered by `index.html`. The existing Corner26 model
and status API are extended rather than replacing score/state ownership.
No original game artwork was uploaded.41included PixelLab generations used,
1722 remained afterward; no cash credits used.

## Verification

37/37 native Chromium checks; no page/console/shader/asset errors. Real keyboard
actions check prone/crawl, roll, free aim, blindfire, jump, grenade and ammunition
use. Native fixtures check full/half/empty/damaged health, unsegmented source,
four stage7 gun selections, every generated glyph, exact text-field centers,
score/high-score persistence, equipment exposure isolation, boss spacing and
conversation frames. Screenshots inspected. Base suite completed BUILD OK /
0ERRORS /exit0; JavaScript syntax checks passed. All820prior PNG hashes match.
This focused presentation pass does not claim a new full campaign/controller
hardware playthrough. Probe `_research/probe_hud27.py`.
Evidence `docs/qa/overdrive_hud27_1015.json`, `docs/qa/hud27_views`.

Local only, no assets/game.js edit, commit or push. Preserve concurrent work.
