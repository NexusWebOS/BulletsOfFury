# STEP 4 — 3 -> 4 · ICE -> SKY -> TOWN

    verify_0730a: 257 passed / 17 failed   (all 17 pre-existing, unchanged from STEP 3)
    test_fl:      2093 passed / 190 sections / 2 failed  (the missing _superseded folder)
    Route runs 436 frames, four beats, hands off to stage 4.

`TRANS[3]` after the re-key: `via:['ice','sky']`, *"ice up into the sky, then scale DOWN into the
town"*. Leaving the Cryo Behemoth, climbing out of the ice shelf, coming down into stage 4.

---

## 1. THE BEATS

    PAST   2.0s   nst3_master keeps scrolling and accelerating, the shelf passing BEHIND
    SKY    1.8s   the authored sky washes down from the top — the climb
    TOWN   2.4s   stage 4 enters SMALL and scales up to 1:1 as you come down into it
    FADE   1.0s   to black, into the stage-end stats

Player **held**, as in both routes before it — 0 position changes across all 436 frames, asserted.
The climb is carried entirely by the world, which is also how the opening's own TAKEOFF and SKY
phases do it: the ship never moves, the ground leaves.

The town can never appear before the sky has fully landed, so there is no frame where you see the
town through the ice. Asserted, same shape as the ice-never-leads-the-lava guard in STEP 3.

## 2. "SCALE DOWN INTO THE TOWN"

Read as the **camera's** move, not the plate's. Descending toward ground makes that ground larger,
so the town is drawn scaled DOWN — small and far below — and grows to 1:1 as you arrive. The other
reading of the phrase ("draw the town scaled down, then bring it in") lands on the same picture,
which is why I built it without asking.

    S34_TOWN_SCALE0 = 0.34        enters at about a third size
    smoothstepped                 no snap at either end
    resolves to EXACTLY 1:1       asserted

That last one matters: at the end of the beat the town is pixel-for-pixel the view stage 4 opens
on, drawn with the stage's own geometry and scaled about the centre of the screen. The handoff is
not a cut, it is the same image at the same size.

It is **one constant** if you meant the camera pulling back instead.

The town is hazed while it is distant and the haze burns off as it rises — atmospheric perspective
is what makes it read as depth rather than a rectangle being zoomed.

## 3. THE SKY IS THE AUTHORED PLATE, AND THAT IS NOT A DETAIL

`TRANS_FLAT.sky` is `null` on purpose and there is a standing assertion saying so. `tflat_sky` was
extracted from the ORBITAL stage — it is a dark starfield, a fine space texture and a terrible
daytime sky, and it is the exact mistake the opening cinematic already made once and had corrected
in 0724cx. This route uses `nl6sky_stage06_sky_scroll_640x960`, the same plate the opening settled
on. **Asserted both ways: the authored key is present, and `tflat_sky` appears nowhere in it.**

## 4. ⚠ THE OPENING'S HIGH-ALTITUDE CLOUD LAYER HAS NEVER DRAWN

`openingDraw` asks for two cloud banks *"at two rates so the speed ramp reads as depth"*:

    nl6c_high_altitude_bank_     <- NOT IN THE MANIFEST. No such family, at any index.
    nl6c_low_rolling_bank_0..5   <- exists

The loop guards each with `if(!XART.rdy(fk)) continue;`, so the missing layer fails silently and
the opening has been running on one rate this whole time. Nothing errors; the depth cue the comment
describes is simply half absent.

I have not touched the opening — it is your approved cinematic and this is a separate call. This
route takes both of its layers from the family that exists, at different rates, sizes and alphas,
so it actually gets the parallax the opening is asking for.

## 5. AND THE 2 -> 3 BACK-PORT WAS INCOMPLETE — CAUGHT BY WIDENING THE MARKER

The STEP 3 back-port used the water dispatch line as its end marker:

    if(outboundIsWaterRoute(o)){ outboundDrawWater(o); ctx.restore(); return; }

That line sits in the **middle** of `outboundDraw`'s dispatch chain, so every route added after it
fell outside the copied region. `outboundDrawLavaIce` was back-ported as a function and its
dispatch line was not — `gamecode.js` had the route defined and never called.

It reported "IDENTICAL" both times, because the region it compared genuinely was.

The region now ends after the whole of `outboundDraw`, and the sync proves the crossing directly:
every route function, every dispatch line, and the per-join enablement are counted in both files
and compared, rather than trusting a region boundary to have been drawn in the right place.

    outboundDrawWater      game.js=3  gamecode.js=3
    outboundDrawLavaIce    game.js=3  gamecode.js=3
    outboundDrawSkyTown    game.js=2  gamecode.js=2
    + both dispatch lines and fromStage===3

## 6. WHERE THE JOINS STAND

    1 -> 2  water                built 0801a
    2 -> 3  lava -> ice          built 0810a
    3 -> 4  ice -> sky -> town   built 0810a
    4 -> 8                       still behind DBG.transitions

## 7. TEST IT

    COLE3   drops you at the stage-3 boss on its last sliver — kill it and the route plays
            (arcade mode; campaign goes to the stage-select instead)

Worth watching for specifically: whether 0.34 is the right size for the town to enter at, and
whether the sky beat wants to be longer than 1.8s — the climb is the part with no landmark in it,
so it is the easiest one to feel short.

## 8. STILL OPEN

* **The rival race collides with 2 -> 3, 4 -> 5 and 6 -> 7** (STEP 3 §4). Still your design call,
  still tripwired on `RIVAL_ENABLED`.
* **The opening's missing cloud family** — §4 above.
* **`_levelCfg()` ignores its argument.** Three routes now avoid leaning on it; the trap is still
  there for the fourth.
* Step 5 is **4 -> 5 · THE BOSS CHASE** — `TRANS[4]`, *"highway, ascent, space, slow-mo kill"*. The
  roadmap has called this the big one since 0724cw, and unlike the three built so far it is not a
  terrain wash: it wants a chase, a scripted kill, and a slow-motion beat. That one should be
  specced before it is built.
* The **dam swap** from STEP 2 is still blocked on art.
