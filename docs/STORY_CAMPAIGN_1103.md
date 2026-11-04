# Bullets of Fury — campaign cutscenes

Revision 9 completes the normal campaign handoffs. Easy/Normal now play the Chronos homecoming, overnight upgrade and scramble before their existing completion/difficulty menu; Hard/Furious continue into Stage 6. Stage X destruction plays before the native reward/map continuation, with repeated results calls guarded against duplicate settlement. Each mission preloads its selected-pilot story and dialogue portraits. The approved shaded, scrolling 16-bit color fields and diagonal divider are retained, following Mike's clarification to keep the divider and use the scrolling arcade opener as the shading reference.

Revision 8 replaces the flat color fields with Neo-Geo intro-style color animation: deep colored shadows, stepped highlights, diagonal energy ribbons and pixel dithering. Actual BOF pilot-intro plates were exported and used as style references. Each of the nine themes has sixteen shared shades and twenty-four animated sweep/color-cycle frames at 12fps. The corrected Cole and Maverick identities, all pilot animation pixels and the divider are unchanged.

Revision 7 corrects Cole and Maverick. Cole's headset face now follows Mike's supplied `coleyoung.png` / `boxcole.png` references: blue eyes, brown spiky haircut and beard, olive flight suit and raised green collar. Maverick wears neon green and keeps his aviators. Both 24-frame talking/turning/emotion sets are updated, including Cole as Decker's remote contact. The brown/olive color-panel theme belongs to Cole; the black/green theme belongs to Maverick. See `Cole-Maverick-corrected.png` / `.gif` and `source-art/CURRENT_IDENTITIES.md`.

Revision 6 replaces the divider with hard 4-pixel stepped console art and adds nine solid-color panel themes with sparse scrolling pixel bars. The panels scroll in opposite directions on a seamless 16-phase loop; the clock continues between dialogue beats. Current colors after the identity correction: Cole brown/olive, Axel blue, Decker gold, Maverick black/green, Freezer purple, Juggernaut orange, Yuri red, Lizzie yellow and Falva white/pink accents.

Revision 5 adds 216 generated 16-bit headset frames: 24 per pilot, with four front talking shapes, left/right three-quarter and profile talking pairs, plus happy, sad, angry, scared, surprised and determined pairs. The active speaker talks while text reveals and closes their mouth when it finishes. Listening pilots face inward. The existing black/gray comic frame remains. Use the Pilot animations controls in the review to play any clip or all clips.

Revision 4's neon-green portrait was mislabeled as Cole; revision 7 supersedes that identity label and assigns neon green to Maverick. All nine headset POV portraits retain their generated 16-bit pixel style.

Revision 3 regenerates every headset POV portrait as 16-bit pixel art for all nine pilots. Each new portrait has a 128 x 128 native canvas, at most 32 opaque colors and hard alpha. Standalone portraits use exact 2x pixels; comic portraits use exact 3x pixels, face each other, and end behind the gray footer. The black comic panels and wide gray divider are retained. See `Headsets-16bit.png` and `Headset-shot.png`.

Revision 2 corrects the four reviewed shots: black comic panels with a wide gray divider and chest edges hidden by their footer; a smaller Decker seated at the left workstation with an unobstructed holo table; a separate four-frame mass alien descent using current Stage8 drone identities and no baked pink ship; transparent native aircraft over the visible volcanic landing pad.

Open **Start Review.cmd** to choose any of the nine pilots and replay a scene.
The review uses the current BOF installation, with this additive update loaded last.

| Campaign event | New sequence |
|---|---|
| Furnace Tyrant defeated / Stage 2 | Scroll to volcanic dish, authored shrinking landing, black fade, native stats |
| Before ice / Stage 3 | Cockpit discovery, pilot-specific cable hookup, restored comms/maps, freezing landscape |
| Ice cleared / Stage 3 | Native fly-off, HQ reunion, safety-lock and auto-flight orders, Command Bay investigation |
| Highway cleared / Stage 4 | Scroll into connected launch complex, land, black fade, native stats |
| Before orbital mission / Stage 5 | Headset split-screen, mainframe upload, faceless satellite infection, jump scare and Decker recoil, Federation prototype intel |
| Chronos cleared / Stage 5 | Earth descent, HQ welcome, lounge, overnight chaingun upgrade, escalating radar/alarm, monitor explosion, five-ship scramble |
| Sky battle cleared / Stage 6 | Correct remaining threat for either choice, underground signal traced into sewers |
| Stage X cleared | Route-specific Harrier destruction or five-on-five rebel dogfight and crashes |

These bindings follow the existing campaign's event order. The original request's highway/space/return stage numbers were offset from the current build; levels are not renumbered.

Dracodia's replacement recording uses the current black-violet, **faceless** symbiote. No dragon or revealed face is used. The original opening and native sewer portal ending remain with their existing owners.

The update contains 126 fixed-cell banks / 2,426 frames, including existing cast/aircraft exports and new generated artwork. All delivered cell dimensions are even. Perspective, recession, exhaust lighting and black fades are stored in authored frames; playback selects and positions them.

See `verification/report.json` for focused native Chromium checks and `Cutscene-review.jpg` for actual game captures. The full existing test suite still exits 1 before its final summary on the recorded `difficultyHealthBaseline15` harness error. The existing online anonymous-signup endpoint was unreachable during local review; scene art loads locally.

Revision 9 verification: `verification/revision9/campaign.json` and `campaign-installed.json` exercise native result settlement and HQ continuations for Stages 2–6, all nine selected headset identities, Easy/Normal saved-clear resume, both earned Stage X pursuit routes, both connected landing-to-stats exits, and physical keyboard reveal/advance/skip. These are focused continuation fixtures in Chromium, not a full combat campaign playthrough. The core and sidecar syntax checks pass. The required existing suite still exits 1 before its final summary at `assets/combat_polish_0927b.js:151` / `_BUILD_SOURCE/test_fl.js:4537`, because `difficultyHealthBaseline15` is undefined in its harness. The core game and test harness are unchanged by this update.

`overlay` contains the two late scripts and their art. `source-art` preserves generated masters and provenance. Installation changes only these added files and appends their script references to the current index. No commit or upload is performed.

Editable Aseprite timelines are in source-art/aseprite. All 126 banks / 2,426 frames reopen with exact pixel equality. Rebuild native exports with source/build_cutscenes.py, supplying --game, --out, --refs and --sources; the packaged source-art/generation_sources.json resolves the included PNG masters.

Revision 3 evidence: `verification/revision3/art-report.json` verifies all nine native portraits and that the other 88 banks are byte-identical; `verification/revision3/report.json` and `installed-report.json` verify all nine comic panels and prior shot corrections in Chromium. `verification/aseprite.json` records exact pixel round-trip of all 106 banks / 1,785 frames.

Revision 4 evidence: `verification/revision4/art-report.json` confirms only Cole's portrait and the two affected comic panels changed; the other 103 banks are byte-identical. `verification/revision4/installed-report.json` checks the installed game.

Revision 5 source: `source-art/headset_motion_1103/<pilot>/` contains the generated master, native spritesheet and 24 separate PNGs. Tagged native/panel timelines are in `source-art/aseprite/`. `BOF-Headset-Frames.zip` is the portable native frame pack. `Headset-Animation.gif` and `Headset-frames.png` preview the full cast. To rebuild the new frames after the base exporter, run `source/build_headset_motion.py --out <this-folder> --sources source/headset_motion_sources.json`; regenerate timelines with `source/author_timelines.py`.

Revision 5 verification: `verification/revision5/motion-report.json` checks all 216 rendered frames against native source pixels, turn order, distinct emotions and talking/idle behavior. `report.json` checks the earlier corrected shots; the installed equivalents are `motion-installed-report.json` and `installed-report.json`. Other 97 prior art banks remain byte-identical.

Revision 6 source: `source-art/comic_scroll_1103/` preserves both generated masters, the 228 x 128 pixel divider, nine native 64 x 64 color tiles, palette roles and scroll metadata. `Comic-scroll-preview.gif` shows actual game captures and `Comic-color-panels.png` shows all pilot themes. Rebuild after the base exporter and headset-motion exporter with `source/build_comic_scroll.py --out <this-folder> --sources source/comic_scroll_sources.json`, then regenerate Aseprite timelines.

Revision 6 verification is in `verification/revision6/`. `scroll-art-checks.json` verifies flat colors, hard pixel geometry and exact opposite-direction loop closure; `motion-report.json` verifies all scrolling phases and pilot frames in Chromium; `report.json` verifies the earlier corrected shots. Installed reports carry the installed suffix. Only the divider changes among the prior 117 art banks; the other 116 remain byte-identical. Nine scrolling banks are added.

Revision 7 evidence: `verification/revision7/identity-report.json` records the user reference hashes, corrected palette roles and exactly 10 affected banks, with 116 banks byte-identical. `motion-report.json` and `motion-installed-report.json` verify all 216 pilot frames and scrolling panel phases; the shot-correction reports verify earlier fixes. The Aseprite report verifies 126 banks / 2,354 frames without pixel differences. Other seven pilots, the pixel divider and earlier level cutscenes retain their existing art.

Revision 8 source: `source-art/neogeo_panels_1103/` contains the generated master, nine native 96 x 96 shaded tiles, palettes, frame metadata and inspected BOF intro references. Re-export the current backgrounds with `source/build_neogeo_panels.py --out <this-folder> --sources source/neogeo_panels_sources.json`, then regenerate timelines with `source/author_timelines.py`. This is the final background exporter after the earlier baseline/headset/divider builders. `NeoGeo-panels-preview.gif` shows native game captures; `Comic-color-panels.png` shows all nine themes.

Revision 8 evidence is under `verification/revision8/`: shade/palette/loop checks, all pilot/frame checks and installed equivalents. Eighteen background/composition banks change; 108 prior banks, including all corrected pilots and the pixel divider, keep identical bytes. Runtime only selects authored frames; no browser lighting or color effect is introduced.
