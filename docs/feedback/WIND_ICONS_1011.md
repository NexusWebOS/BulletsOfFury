# Wind projectile badges and elemental reward

October 11 follow-up: all45 borders are now Wind green. Nine actual 16-pose
combat projectile reels are generated and wired. The final suite is8,503/0;
36 Chromium checks pass. Current details and combined animated review are in
[WIND_PROJECTILES_1011.md](WIND_PROJECTILES_1011.md) and
`docs/previews/wind_projectiles_1011/index.html`. The earlier work below records
the original badge delivery; both original and green source sheets are retained.

Mike rejected the earlier Wind hardware/carrier pictures. The upgrade menu
needs the game's framed weapon-icon style, with actual fired projectiles and
effects. The Stage 6 boss awards the Wind element itself, represented by its
own gust symbol.

## Delivered

Nine projectile families have five distinct level badges each, with readable
Roman I–V tags: Wind bullets, spread pellets, a missile, laser, gust breath,
tornado orb, mist, heavy slugs and electrical orb. Their octagonal emerald frames,
dark interiors and emerald/white fired-shot art match the authored menu family.
The separate hexagonal Wind emblem contains three curled gust lines. It is
used on the field pickup, Powers Gained screen and Forge element selector.
It never substitutes a weapon badge for the elemental reward.

All 46 shipping cells are 128×128 with pivot64,64 and transparent margins.
The returned tier sheet's actual row gutters are measured; no tag is clipped
by a nominal grid cut. Common proportional source scales preserve the drawn
silhouettes. Original rejected pictures remain archived. Combat projectile
timing, damage, recipes, reward ownership and save migration are unchanged.

## Sources and owners

- Built-in `image_gen` produced the base nine badges, 36 tier variants and
  separate symbol. Exact prompts, all three raw images, original references,
  hashes and registration are in `_ART_SOURCES/wind_icons_1011/`.
- Shipping graphics: `assets/game/shared/ui/wind_icons_1011/`.
- Owning build: `python _BUILD_SOURCE/build_audio_fx_1010.py`, invoking
  `wind_icon_art_1011.py`, updates pixels and `assets/audio_fx_art_1010.js`
  together. No shared atlas edit is involved.
- Runtime: `assets/audio_wind_1010.js` maps every slot/level explicitly and
  registers the separate symbol for `inf_wind` and `turn_inf_wind_0918`.
- Review: `python _BUILD_SOURCE/build_wind_icon_review_1011.py` creates
  `docs/previews/wind_icons_1011/index.html`. The earlier audio review also
  shows the replacement badges, a level selector and the separate symbol.

## Verification

The full suite reaches its final summary with 8,416 passing assertions and
zero errors. Native Chromium checks: ten for all 45 alias pixels, the real
Forge and upgrade-menu draws, Stage 6 reward creation/collection and Powers
Gained symbol, plus eight for preview loading, tier selection and playback.
No page, console, renderer or missing-asset errors remain. Durable evidence:
`docs/qa/wind_icons_1011.json`; native captures: `_shots/wind_icons_1011/`.

Visual inspection caught a cut crossing the tier tags; measured gutters fixed
it before final verification. Initial native fixtures selected the Forge's
loadout row and tried to re-earn an already owned element. The corrected
fixtures exercise the element selector and an actual newly earned drop.
The existing audio review could receive a negative first-frame time delta;
its clock now clamps that delta before indexing the animation reel.

These are controlled native menu/reward checks, not a natural Stage 6 clear.
All prior staged, unstaged and untracked work is preserved. Local only; no
commit or push requested. Main HEAD remains7539951.
