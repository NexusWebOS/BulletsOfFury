# Chrome Hammer: final reactor and Earth approach

Mike requested a defeated, stationary Boss5, chromium energy bleeding away,
the core pulsing under Retina, a player shot, then fire/chromium ignition and
armor scattering through space. He explicitly approved sending only the
current `arch_stun_0920` pose1 reference to PixelLab.

`assets/hammer_finale_1017.js` owns that ending through the existing
`h3EndingStart/Tick/Draw` hooks. It calls the original defeat start once, so
cleanup, music and rewards retain their owners. The original combat pose
renderer and old acted-death reel never draw during the new finish.

- The exact authored kneeling plate remains fixed at its defeat position.
  Its existing violet panels darken as PixelLab discharge filaments detach.
  The last words retain their portrait and authored dialogue frame.
- The reactor pulses at its measured source position127,145. PixelLab light
  is confined to authored emissive sockets; the generated oversized reactor
  ring/outer halo is excluded. A source-pixel glow companion preserves the
  core shape. Retina uses the actual selected pilot reticle and lock beeps.
- One committed missile leaves the native Furyship nose and reaches that
  core. Only this impact begins ignition. Native `markHit` and flash expiry
  remain visible through the complete actor renderer.
- Two seconds of generated fire/chromium ignition precede one rupture.
  Eighteen cuts of the actual armor scatter radially and keep tumbling after
  the generated burst clears. Reassembling the cuts reproduces every RGBA
  source pixel exactly; they add no replacement armor pixels. No combat rig
  is split, and the dead boss cannot reform or resume an attack.
- The established orbital/surface/aftermath cutaways and cheering follow.
  The superseded second close-up death remains skipped by its existing owner.

Earth is rendered separately from the moving authored Stage5 starfield.
Its center has no dependency on `mapScroll`, `_stage5SpaceScroll` or `camX`.
During descent the existing Furyship travels north and shrinks to the
destination; Earth grows from30% to82% of the viewport width. Its original
aspect ratio is preserved. The existing end fade and Stage Clear handoff
remain. Every pilot uses the native Furyship renderer and its actual palette.

## Art ownership

`_BUILD_SOURCE/build_hammer_finale_1017.py` owns all149 shipping PNGs (1.39MiB) and
`assets/hammer_finale_art_1017.js`. Four PixelLab jobs each return32 generated
poses plus the input reference; only the32 generated energy poses ship.
The AI-generated armor is discarded in favor of the immutable authored plate.

Energy banks use fixed320×320 transparent canvases, pivot160,160, source
scale1 and common32,32 padding. The authored plate, dimmed plate and core
glow use256×256, pivot128,128. Armor cuts use96×96, pivot48,48, with measured
original centers. No frame fits, axis stretching, fabricated tween frames
or shared atlas changes. Source reference, prompts, job IDs, returned PNGs,
registration, hashes and export audit are in `_ART_SOURCES/hammer_finale_1017`.
Private tool responses and download links remain under ignored `_shots/`.

## Verification and review

Run `python _BUILD_SOURCE/probe_hammer_finale_1017.py` for the actual Chromium
ending, impact flash pixels, shot order, Retina, fragment drift, Earth
framing, all nine pilot variants, Stage Clear handoff and isolated review.
Native screenshots and neighboring-frame onions are under
`_shots/hammer_finish_1017/`; the public verification summary is
`docs/qa/hammer_finale_1017.json`.

October17 verification:33/33 native Chromium checks, zero page/console/asset
errors. Every bank has32 distinct even frames. The whole-actor impact flash
changes its actual opaque pixels and expires; all18 fragments persist beyond
the fireball. All nine native pilot variants and the final Stage Clear handoff
pass. Required `node --check assets/game.js` passes, and the complete
`node _BUILD_SOURCE/test_fl.js` reaches8754 passes, zero errors and the final
`FALVA/LIZZIE BUILD OK` banner. The core suite does not load this new ending
layer; the Chromium probe verifies that layer. `game.js`, `test_fl.js`,
`smooth_motion_1009.js` and `gameplay_repair_1004.js` retain their starting
SHA256 values, including existing unrelated local changes and line endings.

Review `docs/previews/hammer_finale_1017/index.html`. It embeds the real game
at the regular field of view with the approved side HUD, and isolates storage
before boot so replaying the finish cannot replace normal campaign saves.
