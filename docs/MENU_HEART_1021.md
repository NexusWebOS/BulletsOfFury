# Menu windows and Chrome Heart — October21

The tutorial menu now uses a neutral deployment prompt in a dedicated generated menu frame. No pilot name or portrait is used to ask about training. Instructor Cole remains the instructor during the actual tutorial.

## Four reusable menu windows

Separate generated S/M/L/XL art in `assets/game/shared/ui/menu_windows_1021/`. Source crops retain even720px-wide canvases and proportional scaling. The runtime preserves corners with nine-slice rendering, maps header/body apertures through the same transform, wraps text and fits its height, then centers the actual bitmap glyphs. No portrait column is present. Intended game layouts: S384x132, M456x196, L456x286, XL456x366. The L tutorial menu keeps choices, recommendation, and controls separate from the paragraph.

## Five preview choices

Open http://127.0.0.1:8794/_shots/menu_heart_1021/review.html . The five directions are Fury Threat Console, Holoscan, Field Manual95, Arcade Data Cartridge, and Hangar Service Lift. These are review concepts, not live replacements. Robot details and baked mockup text are illustrative; the chosen implementation must use BOF’s real B.O.B. parts/turntables and live440-total/240-core stats with fitted text. The original Overdrive-derived card remains pending Mike’s choice.

## BARBIE / Chrome Heart

A real final-stage victory with Falva or Lizzie, including an eligible co-op seat, saves the account unlock `bof_chrome_heart_v1`. Both campaign and arcade final victories qualify on every difficulty. Starting a level, clearing a different stage, a debug/bossmode fight or winning as another solo pilot does not unlock it. Entering BARBIE before the unlock explains the requirement; afterward the native difficulty and pilot selection lead directly to the optional fight. This does not unlock the password merely by typing it.

Chrome Heart is a newly authored pink/pearl chromium Hammer actor with a heart reactor and solid chrome heart hammer.112 PixelLab animation/effect frames ship as seven compact atlases. The attack book is dance volleys, a targeted overhead slam with impact Retina, an absorbing breakable heart shield, a moving hammer waltz with ring bursts and a wider heart bouquet. All four difficulty settings tune HP, telegraph duration, shot count, speed and recovery. Aimed heart fans use actual-ray FOVs, with committed vectors and safe reaction time. The shield absorbs without deflection; hits flash the body and shield through native hit owners. The core has a Retina target. Measured chest/hammer offsets match projectile and slam origins.

The secret arena clears normal stage scheduling, retains native ship controls, weapons, dodge invulnerability, mixer cues and the Hammer death/explosion/fly-off sequence. Restart stays in the secret encounter. Its final fly-off leads to a dedicated result window without normal Stage5 Forge/unlock/progression menus. Normal Hammer encounters retain their established art and combat.

## Music

Aqua’s “Barbie Girl” instrumental cover is offered in the Tency/Karaoke Version licensing catalog: https://www.tencymusic.com/music-licensing/aqua/barbie-girl.html (ISRC FR3Z80700459,3:17,130BPM). It is a re-recording, not Aqua’s master. Purchase/licensing is required; no paid file or preview was ripped or bundled. The game currently uses its existing Hammer track. After supplying a locally licensed instrumental, set its relative asset path in `assets/chrome_heart_music_1021.js` (`CH21_MUSIC`). It then uses `Snd.music`, retaining the existing master/music sliders, mute, pause and warp handling.

## Verification

See `_ART_SOURCES/menu_heart_1021/final-verification.json` for exact current counts and `_shots/menu_heart_1021/verification.json`, `cross-browser.json` and `full-suite.log` for details. Native Edge contracts cover four difficulty attack books, real damage flashes, shield absorption, actual routed audio decode/playback, restart, death/fly-off/result routing, unlock/save/reload and the ordinary Hammer. Chrome/Firefox/Edge checks cover actual keyboard menu input, all five animation selections and desktop/mobile review layout. The review reel is native game rendering, not a Python mock. Automated fixtures are not a human survival-rate measurement.

Source art, prompt set, PixelLab job IDs and shield repair receipt are in `_ART_SOURCES/menu_heart_1021/`. Generated menu sources and concepts used built-in image_gen; animated banks and shield transparency repair used PixelLab. No source raw artwork is needed at game boot. No GitHub publish was performed in this pass.


## Selected dossier — October21

Mike selected Holoscan / Exploded View (02), now implemented. The five-concept selection is resolved. See HOLOSCAN_1021.md and ../_shots/holoscan_1021/review.html. The remaining concepts stay archived for future expansions.
