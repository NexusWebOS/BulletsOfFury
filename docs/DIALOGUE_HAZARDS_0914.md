# Solid hazards and shared dialogue frame â€” 0914

Mike requested opaque, avoidable/destructible asteroids and comets, plus a new rectangular 16-bit dialogue window with centered text and pilot palettes.

## Result

- Generated one gunmetal rectangular plate with cyan trim using the authorized image generator. Source and exact prompt are retained in `_ART_SOURCES/dialogue_0914`. The cropped 512x130 runtime asset lives in `assets/game/dialogue_0914/frame.png`; XART registers it directly, without changing an atlas.
- `dialogueFrame` caches pilot-color versions of the cyan trim while retaining neutral steel and the dark text seat. `dlgBox`, modal pilot comms, and cinematic dialogue share it. Names and completed body lines are centered within the available text column. Typewriter reveal measures the complete line, so visible letters do not shift. Existing portrait and dialogue-font assets remain in use.
- Removed the separate translucent Stage-5 asteroid scenery deck and retired decorative comet overlay. The asteroid pool owns all visible Stage-5 rocks. A real roster comet replaces 20% of rock spawn slots, preserving the existing hazard cadence.
- Asteroid hit radius derives from the authored sprite dimensions. Space lasers, volley missiles and shadow blasts can target/damage them; ordinary projectiles retain their existing collision route. Their full-opacity base draws use normal compositing. Destruction uses explosions without fading rock-shaped debris.
- Existing comet units are physical, shootable environmental bodies with no gunfire or pickup drops. Comet destruction immediately removes the body and plays the authored explosion and asteroid-break sound. Stage-9 water-rock burst behavior remains its separate authored mechanic.

## Verification

Native Chromium uses `shoot.TRAP_RAF` and the existing capture clock, loading the real index, XART assets, bitmap font and canvas renderer. The probe captures all nine frames, the full HQ launch message, actual hazard art, and a six-second PLAY preview. It checks centered text and reveal stability, real space-weapon damage, asteroid and comet contact through player damage paths, and actual draw alpha/compositing. Combat-preview firing/steering and invincibility are capture-only; collision checks separately restore the real playerHit function. The preview is silent.

Proof: `qa/dialogue_hazards_0914.json`. Screenshots and MP4: `_shots/dialogue_hazards_0914/`. All-nine contact sheet and full HQ screenshot were visually inspected. This is focused hazard/dialogue verification, not a complete replay of stages 5â€“9.

`final.patch` in `_BUILD_SOURCE/dialogue_hazards_0914` records the complete runtime delta against this drop's preserved baseline. `integrate.py` is the initial implementation recipe, not a final-build installer. The current runtime and final patch include subsequent native-review corrections. The baseline runtime hash is 5150c9c4134da494bec2d2789b9e7fecfd4c022f8647302a470945f4072109b5. Runtime LF and suite CRLF were preserved; no commit or push was made.

Final checks: `node --check assets/game.js` exited 0. Full `node _BUILD_SOURCE/test_fl.js` reached its summary: **3,852 passed / 58 failed; exit 1**. No new failing assertion names relative to the recorded baseline after punctuation normalization. The remaining 58 failures are inherited; three old modal-text source assertions now follow the shared renderer and pass. All 12 focused native checks passed with zero page/console/game-loop errors. The six-second MP4 fully decodes.
