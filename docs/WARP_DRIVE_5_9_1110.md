# Stage 5→9 warp drive

Mike requested a warp-drive cutscene connecting Stage 5 to Stage 9. The finished sequence uses the actual earned gate-eight trigger, nine pilot-specific flight reels, changing drive instruments, and a matching Stage 9 arrival.

## Direction

The departure has three comic shots over 13.2 seconds: all eight gate locks confirmed while paired drive coils charge; the selected pilot commits to the jump; then the spacecraft accelerates through straight blue-white star lanes, recedes into the forward light and disappears in a white flash. The instrument art and native bitmap readings advance together. Charge and jump reports play once at their matching beats through the shared buffered sound system.

The departure hands control back to the original 0.95-second protected white hold and native map unlock. The map still reveals the earned bonus node, restricts selection to Stage 9 and waits for deployment. It does not automatically start the mission. Actual Stage 9 deployment plays a separate nine-second arrival: the light clears to the destination starfield, the selected native space kit appears, sensors return, and the existing launch connector continues into gameplay.

Co-op shows each active pilot's own warp reel in a separate panel. Either seat can earn the jump by passing the eight gates. Straight, vertical, stacked and impact comic dividers reuse the approved authored gutter plates. Propulsion, shrinking distance, exhaust, star streaks and the flash are authored in the image frames; this layer adds no procedural swirl, distortion, rotation, glow, fade or runtime ship shrink.

## Identity and sources

`source-art/warp/references/` holds31 fresh exports through the current game's `furyShipCanvas` and `XART.get`: all nine space kits in three views, the departure/destination scenery and the actual eighth gate. The native kit is silver/black with pilot-specific cockpit, armor and engine accents: Cole green, Axel blue, Freezer violet, Yuri red, Maverick teal, Falva pink, Lizzie bronze/ochre, Decker bright yellow and Juggernaut orange. Each generated ship reel was conditioned on that pilot's fresh actual exports and approved detailed cinematic treatment. Cole's accepted warp reel supplied staging for the other eight.

Eleven selected built-in image-generation masters contain66 new 512×512 frames: nine six-frame spacecraft reels, a six-frame drive-console bank and a six-frame emergence bank. Native arrival ships use nine exact128×128 exports, with no enlargement to manufacture detail. All production images are lossless WebP. Fixed cells, pivots, duration metadata, source hashes and bank registration are built together.

Generated sheets are in `source-art/warp/masters/`; exact cell exports are in `source-art/warp/frames/`; all20 editable timelines are in `source-art/warp/aseprite/`. `source-art/warp/generation-prompts.json` preserves the final submitted prompts and reference roles. `source/build_warp_assets.py` owns the registry and exports. All75 cells across the20 timelines reopen in Aseprite without a changed pixel.

## Runtime ownership

`assets/cinema_warp_art_1110.js` and `assets/cinema_warp_1110.js` load after the existing cinematic bridge modules. The runtime source is `source/cinema_warp_1110.js`.

- `s9WarpStart` keeps the original gate/warp state setup and ambience. Its immediate burst is deferred to the actual acceleration beat through the native sound owner.
- While the authored reel owns `GS.CUTSCENE`, the native warp state stays parked. Enemies, waves, projectiles, score, lives and the Stage 5 clock do not advance.
- Completion or Start-skip invokes the original warp clock once at its draw→white boundary. The native carry, both seats, whiteout cue, music stop, 0.95-second hold and `openStageSelect(5,{bonusUnlock:true})` remain responsible for continuation.
- Cancelling/replacing a preview clears only its owned pending warp and ambience, preventing a stale map grant.
- Stage 9 arrival uses `_warpArrival9`, reset by the original `beginStage(9)` handoff. It returns once to `GS.LAUNCH`. Gravity Mode/armor preparation and launch remain native.
- Native map selection, the Stage 5 bookmark captured on Stage 9 entry, bonus clear settlement and the existing loss→map→Stage 5 return remain unchanged.

## Review and evidence

Use `Start Review.vbs` and choose **Stage 5→9 · Warp drive** or **Arrival at Stage 9 · The other side**. Pilot and co-op selectors show the correct craft. `Stage-5-9-Warp-Preview.mp4` and `.gif` contain a silent excerpt captured from the installed native renderer. `Nine-Space-Warp-Variants.jpg` compares the nine game-rendered variants; `Warp-Frame-Review.jpg` shows all54 spacecraft source frames.

Focused evidence is in `verification/warp/`, covering all nine reels, exact native arrival kits, co-op, actual gate collision success/failure, combat protection, timed native sound, once-only map unlock, the protected Stage 9 launch and the Stage 5 failure return. This uses controlled native continuation fixtures rather than a full combat campaign playthrough. Campaign regressions and replay controls are recorded separately. `full-suite.json` records the required broader game suite and its pre-existing missing health-helper failure.

Final validation passes104/104 focused warp checks,50/50 native campaign continuation checks and17/17 replay checks. Both actual cinematic cues start decoded buffers through the native sound system; the shared charge cooldown remains intact. All20 Aseprite sources reopen with75 unchanged cells. Core and new-module syntax checks pass. The full game suite exits1 at the recorded `difficultyHealthBaseline15` error in `assets/combat_polish_0927b.js:151`.

The durable pack is `C:\Users\Mike\Documents\Codex\2026-11-10\you-are-a-cinematic-director-for-3\outputs\BOF-Cinema-1110`. This updates the development/source build. The published Windows installer is not rebuilt; no commit or push is performed.
