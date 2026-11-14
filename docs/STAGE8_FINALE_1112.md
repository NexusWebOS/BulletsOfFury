# Stage 8: No Safe Sky

The true Stage 8 campaign victory now plays the new 93-shot finale through the late, scoped `stage8_finale_1112.js` owner. The native boss death, win/unlocks, score, saves and all combat remain authoritative. The enemy references are Mike's supplied BOF II cover and seven-enemy sheet; all nine returning aircraft were exported from the native renderer. Includes Holt, the mystery rescue, mecha-boat escape, HQ loss, planetary invasion and skeletal code Dracodia. Details and source/verification locations: `docs/STAGE8_FINALE_1112.md`.


Runtime: `assets/stage8_finale_1112.js` and `assets/stage8_finale_art_1112.js`; art/audio under `assets/game/shared/cinematics/finale_1112/`. Script tags are last, after the current boss work. Only a true campaign victory at Stage 8 activates this presentation. Other modes/stages retain their owners. Start skips to the continue card; confirm reads/advances, then returns to the native title. All visuals are authored frames at fixed sizes; the runtime only blits/clips/moves them. The asset working set is bounded to adjacent shots. Audio uses the native mixer and cancels on exit.

Source package: C:\Users\Mike\Documents\Codex\2026-11-10\you-are-a-cinematic-director-for-3\outputs\BOF-Stage8-Finale-1112

`source/story.json` holds dialogue/timing. `source/build_finale.py` composes authored banks; `source/editable/` contains Aseprite sources. `verification/` contains native image, source roundtrip, installation and movie reports. `Bullets-of-Fury-No-Safe-Sky.mp4` is the complete cinematic film.
