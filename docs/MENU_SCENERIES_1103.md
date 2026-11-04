# Scrolling menu environments — November 3, 2026

Six new generated HD 16-bit environment families are installed in the native menus. Three transparent foreground layers provide independent parallax. Nine original 2172×724 generated images and editable Aseprite sources are preserved; the runtime has nine 1536×512 images and six 1536×1280 portrait crops.

| Family | Surfaces | Foreground |
|---|---|---|
| Orbital Fury | Title, credits | Stars / ion dust |
| Fury Command | Modes, co-op setup, difficulty, training prompt | Steel catwalk / cabling |
| Ready Hangar | Pilot selection, co-op roster | Steel catwalk / cabling |
| Decker's Forge | Forge, loadout, Re-Spec, armory | Steel catwalk / cabling |
| Coastal HQ | Campaign hub and save/load prompts | Coastal clouds / mist |
| Secure Data Vault | Options, passwords, help, achievements, vault | Steel catwalk / cabling |

The new designs use BOF's inspected dark steel, chromium edges, cyan/blue equipment lights and amber heat. The generated backgrounds contain no characters, aircraft, text or controls; native owners supply those elements.

## Rendering and ownership

assets/menu_sceneries_1103.js maps environments to menu states. Source pixels use integer translation and source clipping. Standard viewports use bounded smooth camera travel, with independent foreground motion. Portrait views choose the taller exports; foreground ceiling/lower edges retain their native height. The new renderer adds no runtime tint, generated scenery, scaling, filters or opacity animation.

Three optional core guards route title, campaign hub and co-op background treatment. The armory has one optional background guard. Original typography, portraits, ships, controls, audio, unlocks, saves and Forge economics keep their owners. The Forge retains its authored frame/header/footer and weapon bays; scenery occupies its measured central aperture.

Mode Back locking and the Start menu's frozen snapshot remain native. The menu camera pauses with that snapshot and resumes without accumulating paused time. Live combat, in-game pause, cinematics, mission-map geography and story/stage cards keep their own renderers. The classic review path is ?menubg=classic. Viewports taller than the 1280px portrait bank retain native fallback; desktop and 390×844 portrait are verified.

## Generation and export

Generation used built-in image_gen. Exact prompts/references: _BUILD_SOURCE/art_sources/menu_sceneries_1103/prompts.json. Original PNGs and editable .aseprite sources are alongside that file. Runtime assets/checksums: assets/game/shared/ui/menu_sceneries_1103/manifest.json.

Aseprite v1.3.18.6-dev exported all images offline at even sizes, retaining foreground alpha. Reproduce with _BUILD_SOURCE/menu_sceneries_1103/export_assets.py and an installed Aseprite executable; ASEPRITE_PATH can override discovery. The editor binary is not bundled.

## Verification

Sixteen native menu views pass, including desktop, 390×844 portrait, co-op setup and roster. Bitmap fonts are ready in every desktop view. Representative actual screenshots were inspected, including the completed pilot reveal and Forge bays. Background-region pixels visibly change during scrolling; near/far displacements differ.

Live-loop keyboard checks pass title → modes → Arcade → difficulty → pilot; preserve the intentional Back lock; open/close Start with a frozen background; and open/close co-op setup. The classic fallback passes. The environment renderer declines combat without changing its draw counts. These are keyboard checks, not a physical controller test or a gameplay balance pass.

The local preview server omitted expansion/ from its public game-asset mapping, causing four 404s for older menu images. That mapping is corrected at the same address. Final native browser checks have no page/console/HTTP errors.

Syntax checks pass for the modified core, armory owner and new module. The required full suite still exits 1 before its final summary on the pre-existing difficultyHealthBaseline15 ReferenceError at assets/combat_polish_0927b.js:151. No new assertion-failure names appear before that setup error; the CRLF test fixture is unchanged. The full suite is not green.

## Review

Native menu review: http://127.0.0.1:58090/review.html

Installed game: http://127.0.0.1:65041/game/index.html?quality=high&menus=1103

Review controls sit outside the game canvas. Its separate origin isolates fixture progress from the normal game session. The fixture is absent from the installed page. Evidence: docs/qa/menu_sceneries_1103.json and _shots/menu_scrolling_1103/.
