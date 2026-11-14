# Team briefing and Decker's workshop

The nine pilots now gather around the physical conference table after Stage 3. Cole and Decker then have their private prototype scene before the next launch. After Stage 5, Decker examines the recovered Chronos cannon, checks its response on an isolated reader and explains the earned conversion. Juggernaut supplies the heavy-metal joke.

## Staging and continuity

The conference is a wide, four-pose shot with exactly nine pilots in every frame. The actual current cast supplied the references: Falva wears pink and glasses; Lizzie wears yellow and hoop earrings; Cole wears green; Decker has blond hair, black glasses and a black/gold suit. Axel and Freezer sit together in their blue/purple flight jackets. Yuri wears red; Maverick wears olive and aviators; Juggernaut keeps his large tattooed pilot identity and friendly character.

The Stage 3 sequence retains the recorder recovery, isolated timeline comparison, desert airbase lead and independent power-cell objective. New beats HQ301/HQ302 frame that evidence with the whole-team meeting. HQ303–HQ308 restore the Cole/Decker laboratory story: cases open, the yellow Level VI laser array is revealed, the dark-core/violet Level VII photon emitter is demonstrated, and Cole gives Decker an enthusiastic shoulder hug. The prototypes remain in bench trials with field clearance pending. This scene grants no weapon tier or inventory item.

The Stage 5 workshop keeps the original coastal approach and landing. B503 now shows Decker examining the actual recovered cannon's exterior. HQ501–HQ503 add Cole's question, the later-night workshop beat and changing diagnostic readings. The native earned-upgrade dialogue follows unchanged, including Cole's separate prototype line and Maverick's fixed homing lasers. B504 uses six new Juggernaut/Decker poses and an empty-hand air-guitar gesture. The radar, alarm and difficulty-specific Stage 6 launch or standby still follow.

## Authored artwork

Seven selected image-generation masters contain40 new poses: conference4; cannon inspection6; salvage diagnostics6; prototype reveal6; laser chamber6; Cole/Decker shoulder hug6; heavy-metal workshop6. All are complete authored frames, with consistent fixtures and fixed pivots. Close workshop acting is fitted inside comic panels so hands and equipment remain visible. The conference uses the full-width panel; the laser test uses a stacked reaction/readout layout. Existing authored comic divider plates provide the borders.

`source-art/hq/references/` contains24 fresh native exports and their hash manifest: nine current pilot bodies, nine dialogue portraits, the command bay, forge, lounge, Chronos barrel and both Cole pulse colors. The cannon reference is the native CH23 six-aperture grey/silver rotor with its blue status window. The laser colors and lance profiles match the actual yellow and black/violet pulse banks.

`source-art/hq/masters/` preserves the seven raw generated sheets. The conference tool returned1774×887 pixels; its four original cells are copied without resampling and padded to fixed888×444 cells. The remaining banks use512×512 cells. `source/build_hq_assets.py` creates lossless WebP atlases, frame exports, fixed pivots, durations, source rectangles and hashes together. Every frame is unique. `source-art/hq/generation-prompts.json` records final submitted prompts and pack-local reference paths. All seven editable Aseprite timelines, containing40 cells, reopen with zero changed pixels.

## Runtime ownership

`assets/cinema_hq_art_1110.js` and `assets/cinema_hq_1110.js` load after the warp cinematic modules. The editable runtime source is `source/cinema_hq_1110.js`. The new layer delegates all other scenes to their existing owners and only extends the Stage 3/5 presentation. Native earned-upgrade rows are preserved exactly for all nine pilot selections. Fixed Cole/Decker roles remain correct even when another pilot or co-op pair is selected.

The laser demonstration uses the native buffered `av3_cole_laser6` and `av3_cole_laser7` sounds once at their authored firing frames. Readings advance with each chamber/diagnostic pose. No combat projectile is spawned. Score, bonuses, inventory, saves, Forge rewards, map selection and launch callbacks remain native. Confirm still reveals/advances dialogue; Start skips to the supplied continuation once.

## Review and validation

Open `Start Review.vbs` and choose **HQ · Conference briefing**, **HQ · Cole & Decker laser prototypes**, or **HQ · Recovered chaingun workshop**. The same content plays in **After Stage 3** and **After Stage 5**. `HQ-Team-and-Lab-Preview.mp4` and `.gif` contain a shortened silent excerpt captured from the installed game renderer; the game itself plays the native sound cues. `HQ-Scene-Review.jpg` compares the actual game-rendered poses.

The focused suite passes97/97 checks across every authored frame, all nine pilot/co-op selections, exact native upgrade lines, matching readouts, actual decoded sound playback, unchanged field inventory/projectiles, real Stage 3/5 settlements and confirm/skip input. Campaign continuation checks pass50/50; replay controls pass20/20. These use controlled native continuation fixtures, not a complete combat campaign playthrough. Evidence is recorded in `verification/hq/`, `verification/campaign/` and `verification/review-controls.json`.

Core/new-module syntax checks pass. The required broader game suite retains its existing `difficultyHealthBaseline15` failure at `assets/combat_polish_0927b.js:151`. The core gameplay file and test suite are unchanged. This updates the development build; the Windows installer is not rebuilt, and no commit or push is made.
