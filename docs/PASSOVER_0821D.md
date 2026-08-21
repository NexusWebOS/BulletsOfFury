# 0821d — THE PELLET TRAIL, WIRED

Mike, on the two orphaned reels: *"yes wire them up"*.

`ndk_trail_0..3` was registered, drawn from real art, and referenced **nowhere**. It is now drawn
behind every one of Decker's seven pellets, rotated to that pellet's own heading and animated at
the pack's declared rate.

---

## THE PACK DOCUMENTED ITS OWN INTENT, AND IT SETTLED THE AMBIGUITY

Vol.1's map defines the families the game's key names had left ambiguous:

    buckshot   4 frames  24x32  fps 16  loop   pivot [12,16]   -> ndk_shot_
    spread     7 angle_frames from BuckshotSpread              -> ndk_ang_
    trail      4 frames  32x64  fps 11  loop  facing up  origin [16,4]  -> ndk_trail_

All three numbers are honoured: **fps 11**, looping, and the origin treated as the NOSE so the
tail streams behind the pellet rather than through it.

## ⚠ THE TRAIL DOES NOT REPLACE THE HEAD — COMPOSED ALL THREE WAYS FIRST

Rendered at game scale before writing a line, per rule 1:

    head only     the pellet today: a slug with a flame stub, barely readable over water
    trail only    NO crisp slug — the trail's own nose is faint and the pellet position
                  ends up ABOVE the visible fire
    trail + head  the authored angle plate's slug lands exactly on the trail's nose

So the head keeps its job (seven authored tilts, no rotation loss) and the trail supplies the
length and the motion the pellet never had.

**SCALE is inherited, not chosen.** The head draws at `h=20` from a 32-tall plate, so the same
pixel scale `20/32` applied to the 32x64 trail keeps the two in proportion by construction — the
trail cannot drift out of scale if either is retuned.

**ROTATION comes from the pellet's own velocity**, `atan2(vx,-vy)`, not from its lane index. 0 is
straight up, which is the facing the art was authored in, and it stays correct if `DK_SPREAD` is
ever re-tuned.

## ⚠ THE PELLET HAD NO CLOCK

`dkshot` is created with `t:0` and **nothing ever advanced it** — it has sat at zero since the
pellet was written, and nothing read it either. The mover advances it now.

⚠ It is deliberately NOT `performance.now()`. A wall clock driving a 4-frame loop is the standing
anti-pattern in CLAUDE.md: the reel then runs at a rate nothing in the game controls, and it
cannot be stepped by the harness.

## ndk_shot_ IS STILL UNUSED, AND THAT IS THE HONEST ANSWER

It is the same 24x32 pellet as `ndk_ang_`, animated (4 frames of flame flicker) instead of aimed
(7 authored tilts). `ndk_shot_0` and `ndk_ang_3` are byte-identical, which is why they share an
atlas cell.

Once the trail is in, **the trail IS the fire** — the head's small flame stub is no longer what
the player reads, so animating it buys nothing and would cost the per-lane tilt. Forcing it into
service would have been contrived. Left registered and unused, and recorded here rather than
quietly wired somewhere it does not belong.

If Mike wants it anyway, the swap is: draw `ndk_shot_[frame]` as the head and take the angle from
`ctx.rotate(_rot)` instead of the lane plate — one branch, and it trades authored tilts for
rotated ones.

---

## ⚠ A PROBE THAT LIED TWICE BEFORE IT TOLD THE TRUTH

The before/after took three attempts, and both failures are worth recording because neither is
specific to this drop:

1. **Two separate simulations are not an A/B.** Running the scene twice put the pellets at
   different heights, so the panels compared two different moments. Fixed by simulating ONCE and
   drawing the same frame twice with only the trail toggled.
2. ⚠ **THE PAGE'S OWN rAF KEEPS RUNNING BETWEEN SCREENSHOTS.** Even with one simulation, the live
   loop advanced the bullets while the first screenshot was being taken, so the second panel had
   moved on ~100px. `window.requestAnimationFrame = ()=>0` before the capture is what makes two
   screenshots comparable at all.

*A screenshot pair only proves something if the only thing that changed between them is the thing
under test.*

---

## HOW TO VERIFY

    node --check assets/game.js
    node --max-old-space-size=3072 _BUILD_SOURCE/test_fl.js     2,701 ok / 3 fail

The 3 are environmental: the preload key count and the two `_superseded/` ledger checks.
