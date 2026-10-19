# Furnace Tyrant: visible eye rotation and both authored arm weapons

Mike requested a smoother Stage 2 head phase: glowing eyes, shake and rumble,
a full turn with both eye lasers, and continued vulnerability to accurate fire,
missiles and ice orbs. He also requested restoring the flamethrower and moving
travelling fire waves to the arm that fires magma balls.

## Result

`assets/furnace_assault_1017.js` owns this revision only for the actual Stage 2
Furnace Tyrant. Other stages and borrowed Furnace encounters delegate to the
previous owners. The shared `assets/game.js` was not edited by this pass.

- The eyes and forehead lens charge through PixelLab poses while the native
  alert, directional tells, camera shake and existing charge/reactor audio run.
- The two eye beams commit to one complete clockwise or counterclockwise turn.
  They use the same measured sockets as the visible skull. The final part of
  the tell fixes the station; the released sweep does not track the player.
- After the turn there is a beam-free recovery. The existing head pool, armor
  transitions, ice damage advantage, hit routing and death remain authoritative.
  Actual player rounds, missiles and ice orbs hit the rotating head without
  cancelling its lasers. Native continuous-beam collision still owns damage.
- The flamethrower again uses a continuous native beam during its firing
  windows. The existing balance owner's warned gaps remain. The cannon arm
  alternates its native charged magma shot with an authored travelling fire
  wave, using the real muzzle and committed release heading. The wave retains
  its existing curved-edge collision and animation.
- Owner and part flash timers are retained. The new head's real pixels visibly
  flash through the native tint path, including the ice hit color, then expire.

| Difficulty | Head charge | Complete turn | Recovery |
|---|---:|---:|---:|
| Easy | 2.15 s | 6.40 s | 1.55 s |
| Normal | 1.85 s | 5.80 s | 1.30 s |
| Hard | 1.65 s | 5.10 s | 1.05 s |
| Furious / Insanity | 1.45 s | 4.50 s | 0.85 s |

## PixelLab art and registration

Mike explicitly authorized sending the centered `furnace_head_00.png` reference
to PixelLab. Four pinned quarter-turn jobs generated 32 front-facing poses;
two defective poses were excluded, leaving 30 accepted genuine drawings.
The first 40-pose attempt yawed away from the camera and remains archived and
unregistered. The two excluded quarter poses also remain in the source archive.

The charge bank contains 16 generated poses plus the exact neutral reference.
Sixteen generated eye-laser poses are exported into body, origin and tip modules.
Their common proportional draw scale keeps the muzzle compact. Only the straight
body repeats; the final instance is clipped, never stretched to fit a remainder.

All head frames are 320 x 320 with physical pivot 160,160. Body/root/tip laser
modules are 64 x 96, 64 x 32 and 64 x 40. All are even, fixed per bank and exported
at source scale 1. Head normalization uses transparent padding and integer
translation, with no independent size fitting. Actual eye/lens clusters measure
roll and mounting positions. The maximum angular gap is 26.24 degrees; a small
rigid residual rotation makes angular travel continuous between genuine poses.
The largest three-lamp fit error is 2.228 source pixels, about 1.13 game pixels.

Forty-seven source-pixel eye/lens glow companions use the exact head rectangle.
No pasted core disc or procedural replacement head is added. Total registered
art: 142 PNGs, 2.19 MiB. This uses loose assets and does not repack shared atlases.

- Builder: `_BUILD_SOURCE/build_furnace_head_1017.py`.
- Registration: `assets/furnace_head_art_1017.js` and `assets/data/ART_TAXONOMY.json`.
- Sources, prompts and audit: `_ART_SOURCES/furnace_pixellab_1017/`.
- Onions, native captures and detailed logs: ignored `_shots/furnace_pixellab_1017/`.
- Live review: `docs/previews/furnace_1017/index.html`. This embeds the actual
  game with its regular playfield and side HUD, not a substitute boss renderer.

## Verification

`python _BUILD_SOURCE/probe_furnace_assault_1017.py`: **54 passed / 0 failed**, no
page, console or asset errors. Easy through Furious exercise both arms and the
complete head turn. The probe checks actual generated keys, mounted beam roots,
real weapon projectiles, native collision, actual damaged pixels, natural flash
expiry and native sound execution. Screenshots and registered onions inspected.

Final review control/pilot verification: **5 passed / 0 failed**, no browser
errors. Cole's actual aircraft and loadout agree; armor/head/full-intro controls
work, and the live armor fight releases both flame beams and cannon fire waves.

`node --check assets/game.js`, the new runtime and the generated art manifest:
passed. Required full suite reached its final summary: **8,754 pass lines,
0 errors**, `FALVA/LIZZIE BUILD OK`, exit 0. This suite guards the existing build;
the real Chromium probe verifies the new late-loaded owner and pixels.

Nine starting source/test/launcher hashes remain unchanged, including game.js,
the CRLF assertion harness and separate local gameplay work. Only two new loader
tags are added to the existing index. No Git commit or push by this pass.
