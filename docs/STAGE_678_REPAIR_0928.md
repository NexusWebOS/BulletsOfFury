# Stage 6–8 repair pass — September 28

The mutated alien vessel is **Stage 8's first boss form**, as Mike clarified. Stage 6 keeps the Harrier carrier and its Ace encounter.

## Encounter changes

- The Harrier's hull is damageable and selectable by Retina alongside its engines and bay. Its boss bar represents the remaining hull and module pools, including shared difficulty scaling. Its own Stage 6 boss track starts with the encounter. Carrier destruction still releases the independently scaled Ace.
- Stage 6's Eclipse Siege Bomber receives a 42% HP reduction after the shared miniboss floors and difficulty multipliers. Core and module pools stay synchronized. Native solo Furious spawn: 6,521 total HP.
- Stage 6 no longer draws incoming or above-unit warning arrows. Stage 5/6 miniboss directional arrows are suppressed while their attack FOV and warning audio remain.
- Stage 7's vent keeps a fixed hardware plate and animates only its toxin stream. The lamprey sprite was regenerated with its complete mouth and silhouette inside the canvas.
- The toxic boss remains anchored to its ground position as the camera and sewer travel during escape. Authored explosion reels receive a green palette; explosion samples drive the spreading blasts. The initial defeat shriek remains, without a repeating shriek loop.
- A generated sewer connector replaces the baked ground portal and extends the corridor north. A centered animated vortex opens for the ship, holds its open frame, then contracts and dissipates. Toxic explosions fill the screen before the fade and stats transition.
- Stage 8 restores its authored music, scrolls throughout combat, and clears the portal entry's movement lock. Its alien fleet fires readable binary bolts, bursting data bombs, and dark matter with committed FOV tells. The mutated first boss form uses a complete new hull with independently targetable cannon/core sections and its own data attack sequence.
- Cached terrain canvases now supply their actual `height` to `levelScrollRange()`. This fixes the zero-range condition that could strand encounter scrolling.

## Art and package

Three production assets live in `assets/game/stage678_repair_0928/`: `sewer_connector.png`, `lamprey.png`, and `mutated_vessel.png`. Built-in image generation prompts and normalization details are recorded in `generation.json`. Existing fleet, data ordnance, explosion and portal art are reused.

The playable ZIP was rebuilt at **499,012,361 bytes**, below the decimal 500 MB limit. The connector uses the existing high-quality scenery compression; the new enemy and boss sprites remain lossless. Development files and the separate expansion remain excluded.

## Verification and scope

- `node --check assets/game.js` and the repair addon passed.
- `node _BUILD_SOURCE/test_fl.js` reached its final summary with **0 errors**.
- `_BUILD_SOURCE/probe_stage678_repair_0928.py` passed in native Chromium against source and the compressed release. It checks exact Harrier damage, its four Retina targets/bar, Ace handoff, miniboss HP, the anchored escape, portal frames, scrolling, and decoded Stage 8 music. The release also moved the pilot 105 pixels and fired six shots through the actual held-control path after portal entry. No page or console errors were observed.
- Rendered screenshots and JSON evidence are under `_shots/stage678_repair_0928/`. The release archive passed its CRC check and runtime-file checks.

These are focused encounter and transition checks, not a complete manual Furious campaign playthrough. This pass changes Stage 8's first boss form; its later forms retain their existing designs. Updated files are synchronized to the Desktop GitHub Coding checkout with backups; no GitHub commit or push is included in this pass.
