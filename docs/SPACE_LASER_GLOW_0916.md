# 0916ab — the space stages were one `shadowBlur`, and it was the player's own laser

The brief was "profile why the two SPACE stages are dramatically slower than every other stage".
They were, and the space rendering path had nothing to do with it.

## The answer

`drawBullets`' `spaceLaser` arm set `ctx.shadowBlur=7` and blitted the pulse under it, **once per
round on screen**. Stage 9 measured **138 shadow-blurred draws per frame**. Stage 1 measured about
one (a missile pickup). That is the entire difference.

The glow is baked into a small cached plate now and blitted, and the pulse is drawn by the same
call it always was.

## The measurements

All in real headless Chromium with no GPU, via `_BUILD_SOURCE/capture_clip_0916.py` (runs the game
at real time, reports frames-drawn ÷ wall-seconds) and the probes listed at the bottom.

### It is the shadow, confirmed by suppression

`probe_shadowblur_0916.py` runs the same scene twice, identical except that `ctx.shadowBlur` is
made a no-op on the second:

| stage 9 | fps |
|---|---:|
| shipped | 1.3 – 1.5 |
| `shadowBlur` suppressed | **54.1 – 55.5** |

A **36–41×** swing from one property. The same test on stage 1 moved nothing (55.6 → 55.8), which
is the control that makes the stage-9 result mean something.

### It is the player's laser, not the background

Per-segment timing with a forced flush (`probe_segments_0916.py`), stage 9, before the fix:

| segment | ms/frame |
|---|---:|
| `drawBullets` | **663.4** |
| `drawMfx` (inside it) | 290.4 |
| `drawBG` | 3.1 |
| `drawLevelMaster` | 2.9 |
| `drawS9Void` | 2.1 |
| everything else | < 1 |

**The starfield, `l5FieldDraw`, `l5RocksDraw`, `drawS9Void` and the warp-drive layer are all
innocent.** They were the obvious suspects and they were wrong.

### Before / after, interleaved

Sequential runs on this machine drift badly — the same build gave 43.5 fps and then 34.3 minutes
apart, and the control stage ranged 34.8 to 56.5 across the session. So the before/after is
measured **inside one browser session**, alternating arms every four seconds, with the order
flipped each round (`probe_lasarab_0916.py`). Both paths ship: stubbing `spaceLaserGlowCanvas`
selects the original per-round blur exactly.

Counting only windows that actually had ≥20 laser rounds on screen:

| | old (per-round `shadowBlur`) | new (baked plate) |
|---|---:|---:|
| **stage 9** median | 8.9 fps | **59.7 fps** |
| stage 9 range | 2.0 – 9.5 | 57.8 – 59.8 |
| **stage 5** median | 7.8 fps | **58.7 fps** |
| stage 5 range | 3.1 – 27.5 | 58.2 – 60.0 |

The new arm sits on the 60 fps cap. It is also doing **more** work in each window — it draws 282–410
rounds where the old arm managed 98–307, because running faster spawns more — so the comparison is
conservative.

⚠ **Windows with no rounds alive were excluded, and that exclusion is load-bearing.** The first run
of this A/B reported the old path at 0.7, 8.2, 8.7 and then **60.0** fps. The 60.0 window had zero
laser rounds in it. A cost that is per-round reads as free whenever the screen happens to be empty,
and averaging that in would have understated the fix by a factor of three.

### After, profiled again

`drawBullets` on stage 9 is now **10.1 ms/frame**, down from 663.4. Nothing pathological is left:
`drawEffects` 3.1, `drawMfx` 3.0, `drawEnemy` 2.5, `drawBG` 1.9.

## Did the picture change?

`probe_laserpixels_0916.py` renders both paths at identical positions over four destination
colours and four sub-pixel offsets, 160 comparisons, and diffs every channel.

**Worst single-channel delta over an opaque destination: 19 / 255**, confined to the halo and the
one-pixel column at the pulse's edge. Invisible at 1×; `docs/proofs/space_laser_0916/_compare.png`
shows before, after, and the difference amplified **12×** to make it visible at all.

Why it is not zero, and why it is not smaller:

- **The pulse itself is byte-identical by construction.** `drawImage(lp, _ldx, _ldy, _lw, _lh)` is
  the same call with the same arguments as before. Only the halo comes off a plate.
- The halo is stored 8-bit premultiplied and then composited, which quantises it. That is
  intrinsic to caching a glow at all — the Magma Ward fix has the same property; nobody measured
  it at the time.
- ⚠ **The transparent-destination case reports 255/255 and it is a readback artefact, not a
  difference.** `getImageData` returns *unpremultiplied* colour, so a pixel at alpha 1/255
  reconstructs its RGB by dividing by that alpha: two halos differing by one unit of alpha in the
  faintest fringe read as a 255-unit colour difference. The game never draws the playfield onto
  nothing. Scored separately in the probe for exactly this reason.

## Two wrong answers on the way, both worth keeping

⚠ **THE CPU PROFILE AND A DIRECT STOPWATCH AGREED ON THE WRONG FUNCTION.** Both charged ~82% of
the frame to `A.blit` — the profile at 622 ms/frame, a timing trap around the call at 229 ms per
call, worst 756 ms. A micro-benchmark then measured that exact blit, that exact rect, out of that
exact 1024×9383 master, at **0.005 ms**. Canvas2D rasterisation is **deferred**: draw calls are
recorded and flushed later, and the flush is charged to whichever call triggers it. `A.blit` was
where the bill was *paid*, not where it was *incurred* — it happened to be the first thing in the
frame to force a flush. A sampling profiler cannot see that distinction and neither can a
stopwatch, which is why two independent instruments agreed and both were wrong. **The fix is to
make the cost non-deferred while measuring** — `getImageData(0,0,1,1)` after each draw phase, which
cannot be reordered past queued work. That is `probe_segments_0916.py`, and it named `drawBullets`
in one run.

⚠ **AND THE WRITE COUNT IS NOT THE COST.** Stage 9 wrote `shadowBlur` 167 times a frame at 1.4 fps;
stage 1 with the laser equipped wrote it 135 times a frame at 55.6 fps. Nearly the same count,
forty times the cost — because stage 1's writes are almost all zeros (resets), and a shadow's price
is the blur radius and the area under it, not the assignment. Trace the value, not the call.

## Three more traps this cost

⚠ **`ctx.drawImage` IS WRAPPED TWICE AND BOTH WRAPPERS ARE `game.js` FRAMES.** Drops 0724dq and
0724dr each installed a guard on the context. So "the nearest game.js ancestor" of every blit in
the game is one of those wrappers, and the profile ranks `ctx.drawImage` at 70% while naming
nobody. `profile_space_0916.py` walks straight through them.

⚠ **`window.ASSETS` IS UNDEFINED WHILE BARE `ASSETS` WORKS** — a module-scope `const` lives in the
global *lexical* environment, not on `window`. CLAUDE.md records the identical trap for `Snd` and
`Snd.TAME`. The first trap on `A.blit` silently installed nothing.

⚠ **A HEREDOC COLLAPSES `\n` IN A PYTHON STRING.** CLAUDE.md already says scripts containing
backslashes go through the Write tool, never a heredoc. Cost one syntax error.

## The change

`assets/game.js`, two hunks:

- **`spaceLaserGlowCanvas(key, col, lw, lh, px, py)`** beside `spaceLaserPulseCanvas`. Bakes the
  halo into a cached plate. Keyed on the exact float size (no rounding — quantising would move the
  art) and on the sub-pixel phase to a quarter pixel. Measured: the game draws **2 distinct
  (key | colour | w×h) combinations** over 1,350 rounds, because `b.h` is a constant 26.
- the `spaceLaser` arm of **`drawBullets`** — blits the plate at an integer origin, then draws the
  pulse with the original call.

Three details that are each a measurement, not a preference:

1. **Only the shadow is baked.** Two earlier cuts baked shadow + sprite together; the pixel probe
   refused both (163/255, then 39/255 after the phase fix). Under `lighter` the two draws add and
   addition is associative, so splitting them reproduces the single shadowed draw — and it leaves
   the sprite's own call untouched.
2. **The sub-pixel phase is baked in and the blit lands on an integer.** Blitting a pre-scaled
   plate at a fractional origin resamples the pulse a *second* time and softens its edge; the error
   tracked the fractional offset exactly.
3. **`SPACE_LASER_GLOW_PAD = 10`, measured not guessed.** `probe_halopad_0916.py` bakes each of the
   ten plates with a 60px pad and finds the outermost pixel with any alpha: the halo reaches at most
   **8 px** past the sprite on any side. 10 leaves room for the phase and a pixel of margin. The
   first cut used 20, which is pure fill rate — 54×60 per round against 34×40, 58% more. Dropping
   it to 10 clipped nothing (the pixel probe was re-run and returned the same 19/255).

Nothing else changed. One `shadowBlur` line was removed from the file, and it is the one identified.
The other 237 `shadowBlur` uses are untouched.

## Still open

- **`drawBullets` remains the biggest single segment at 10.1 ms/frame**, and the other 237
  `shadowBlur` sites have not been examined. Nothing else measured pathological on the two space
  stages, but a stage with a different weapon mix could have its own.
- **The absolute numbers are software rasterisation.** Mike's machine has a GPU and will not have
  seen 1.4 fps. The *ratio* is what transfers, and a `shadowBlur` per projectile is expensive
  everywhere — Canvas2D shadows are poorly accelerated on every backend.

## Tools added (all committed this time — `scratchpad/miniprof.py` was gitignored and is gone)

| script | what it answers |
|---|---|
| `profile_space_0916.py` | CDP CPU profile, native time attributed to the nearest game.js frame, `--paths` for full ancestry |
| `probe_segments_0916.py` | per-draw-phase cost with a forced flush — the one that found it |
| `probe_shadowblur_0916.py` | A/B with `shadowBlur` suppressed; `--trace` for value and site |
| `probe_lasarab_0916.py` | interleaved old/new A/B in one session, gated on live round count |
| `probe_laserpixels_0916.py` | 160-way pixel comparison of the two paths |
| `probe_halopad_0916.py` | how far the blur actually reaches, which sets the pad |
| `probe_blit_0916.py` | call count, size and per-call timing for `A.blit` |
| `probe_bigatlas_0916.py` | the micro-benchmark that exonerated the 1024×9383 master |
| `probe_lasersizes_0916.py` | distinct (key, colour, size) the laser draws — sizes the cache |
