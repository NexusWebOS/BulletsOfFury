# Bullets of Fury — Overdrive: on-foot art package

Generated with the built-in image_gen tool on 2026-10-04. Exact prompts are in `prompts.json`. Source images were copied into this project and retained intact. This is graphics and systems planning only; nothing is registered in the game engine.

Open `preview.html` for the stage, HUD composition, action preview, and object sheets. `SYSTEMS_NOTES.md` describes the later movement, stealth, combat, ammo, crate, enemy, HUD, and mission systems.

- `stage/`: Miami beach → palm park and pools → brick fortress gate. Full 512×768 export and three detail crops; 1024×1536 original in `source/`.
- `hud/`: transparent portrait overlay and separate top/bottom strips. Dynamic slots and example composition are documented in `manifest.json`.
- `pilots/`: 144 extracted candidate frames across four helmeted body families, twelve actions, three frames each. Existing directional aim/run sprites remain in `../ground/infantry/`.
- `weapons/`: six weapons, each with pickup, closed/cracked/open box, and ammo; 30 objects.
- `props/`: 16 cover, brick wall/gate, grenade, ammo, and supply-box objects.
- `enemies/`: 36 states across robot troops, turret, two tanks, and two air units.
- `fx/`: 36 muzzle, projectile, beam, napalm, impact, grenade, and rocket effect frames.
- `stealth/`: 12 scan-cone phases and four awareness/targeting cues.
- `atlases/`: nine normalized transparent review sheets. `source/` retains all eleven generated masters.

There are 278 extracted PNGs and 57 candidate animation sequences. New pilot actions mostly face east. Generated motion, fixed-size frame canvases, and centered review pivots need cleanup and additional directions before production use. The stage is a background concept, not a tiled or playable level. Enemy state sheets are not complete patrol animations. The review uses tentative palette filtering; final armor masks must exclude blue FX.

Alpha and extraction checks are saved in `verification.json`. One joined heavy death/powerup component required a provisional split. Original sheets are authoritative for cleanup. `build-assets.cjs` reproduces exports with Sharp; it does not generate art. The prior coastline map and game files are untouched.
