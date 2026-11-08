# Stage 5 scene restoration — November 6, 2026 / revision E

Mike selected the original starfield and space parallax for Stage 5.

## Cause and repair

The November 2 layered-stage owner replaced Stage 5's `bg_stage05_loop_0923`
with orbital structures/Earth over a different space bed. Independently, Stage 5's
ascent called `stage6TransitionBackgroundDraw`, which the same owner had replaced
with the mainland city renderer. This put buildings behind the cloud/kit sequence.
The revision D performance edits did not rewrite those scene functions, but the
wrong scene routes remained in the delivered build.

Stage 5 now opts out of the layered scenery override. The original 680×2720
starfield loop, its existing independent asteroid/scenery owner, native travel
clock, warp/gate encounters and boss backdrop remain active. Orbital source art is
retained on disk but is not drawn or required by Stage 5's layered preloader.

`stage5AscentBackgroundDraw` reads the original 680×5000 blue sky directly at
native scale. The Stage 4 outbound band, Stage 5 legacy sky-to-space helper and
live Furyship intro use it. Stage 6's city transition/weather renderer cannot leak
into this route. The existing finite cloud deck, twelve-piece assembly, 1000px/s
travel, HQ dialogue, opaque-white backdrop swap and 48px ship remain unchanged.
The countdown and gameplay retain the same space-scroll clock.

## Verification

Twelve focused checks passed in real headful Edge/Chromium at 1366×768 with SS=2.
Captured the complete unskipped native ascent, charge, scatter, snap, pixel glow,
whiteout, reveal, countdown and gameplay; then checked retained-ship entry.
Draw instrumentation counted 1202 original sky blits and 979 original starfield
blits with no layered-city/orbital blits during that captured sequence. The
backdrop switched at the first reveal frame with white coverage exactly 1.
Countdown-to-play scroll advanced 131.832px rather than resetting.
Sky wrap boundary samples retained full-height coverage, source bounds and 1:1
proportions. Stage 6 and 9 still select their current layered scene configurations.
No browser page exceptions occurred. Screenshots were visually inspected.

`node --check assets/game.js` and the layered-stage module syntax check passed.
`node _BUILD_SOURCE/test_fl.js` exits 1 before its final summary at the pre-existing
`difficultyHealthBaseline15` missing helper in `combat_polish_0927b.js:151`.
This is a focused scene regression check, not a full-campaign or new FPS benchmark.
Revision D audio, asset paging/loading, tutorial deployment and weapon fixes remain.

Evidence: `docs/qa/stage5_scene_1106/`; replay/probes:
`_BUILD_SOURCE/stage5_scene_1106/`; local live video:
`_shots/stage5_scene_1106/stage5-restored-live.mp4` (real engine, silent capture).

Eight additional checks passed from the packaged fullscreen Windows EXE using a
separate QA save profile. The packaged core and layered-stage sources match the
repaired repository exactly; the actual original sky, transformation and space
combat render with no page exceptions or console errors. Stage4's outbound helper
produced byte-identical sky pixels to the dedicated ascent renderer at the same
travel value.

Revision E installer: all 18,953 payload entries verified by CRC/SHA256.
Revision E ZIP: 18,957 entries, all 18,956 packaged files verified.
ZIP SHA256: 4829f8cb726c693ed335854b982d0edcc68c0948a6f27f26ade7500023ee3e7d.
No commit or GitHub publication was requested or performed.
