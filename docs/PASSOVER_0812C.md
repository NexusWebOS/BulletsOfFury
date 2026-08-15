# Passover 0812c — "a miniboss is still just the hitbox square"

Mike said one was never replaced and the thread never named the stage. It is not one, it is three,
and none of them is unbuilt — **nothing warms their hull art**, so the fight opens on the
placeholder and swaps to the real ship a second or two later. That is the square in the screenshot.

---

## 1. ⚠ THE FIRST TWO ANSWERS WERE BOTH WRONG, AND THE PROBE WAS THE REASON BOTH TIMES

Recorded because the wrong answers were confident and the same trap catches every art question here.

**Attempt 1 said four minibosses were hitbox squares.** Stage 1, 6, 7 and 8 rendered as red
rectangles; stage 8 rendered nothing at all. Every one of those was **the probe**, not the game:

> ⚠ **`XART.rdy()` IS FALSE ON ITS FIRST CALL — IT IS WHAT STARTS THE DECODE.** A probe that
> spawns a miniboss and screenshots in the same synchronous block photographs the placeholder, and
> reports art that works perfectly as broken.

Split spawn from render, with a **real-time** wait between them, and all eight draw their art.

**Attempt 2's box detector was also wrong.** It called a sprite "boxy" when every scanned row shared
the same left and right extent — which is equally true of a sprite **larger than the scan window**.
Stage 1 scored `136 tones, lefts=1, rights=1`: rich art, flagged as a flat box.

Neither would have been caught by looking at the numbers. Both were caught by **opening the PNG**.

---

## 2. What is actually wrong, measured

`XART.rdy` wrapped to record every key the draw asks for, at the exact moment of the spawn, after a
full `beginStage` + `warmStage` and a long settle — i.e. what the player sees when the miniboss
arrives:

```
stage  kind         name                   NOT READY at spawn
1      quadlaser    QUAD-LASER GUNSHIP     nsd_fog_5                          (scenery)
2      siegeember   EMBER SIEGECARRIER     nsb_siege_ember                    <- ITS OWN HULL
3      thornrime    RIME THORN             nsb_thorn_rime                     <- ITS OWN HULL
4      blacksteel   BLACKSTEEL RAPTOR      nsb_blacksteel + 11 nrs_ signs     <- ITS OWN HULL
5      subcore      ENERGY CORE            9x np5_ orbs/asteroids             (scenery)
6      ss           SUB-BOSS               8x npo_ props, nwx_rainH_0         (scenery)
7      ratking      OVERFLOW EXCAVATOR     —
8      herald       HERALD OF DEATH        nev_venom_0_0 + 5x mba_vr_*_clean
```

⚠ **A KIND NAME IS NOT AN ART PREFIX.** `warmStage` already did `addPrefix(SUBBOSS[n].kind)` —
`'siegeember'` — and the hull key is `'nsb_siege_ember'`. That single assumption is why these were
uncovered while **stage 1 looked fine for the wrong reason**: it is warmed by an explicit
`addPrefix('nqx_')` added in 0801kd, not by the kind rule.

The `_PACKOF` table beside it existed for exactly this job and covered **only two retired kinds**
(`obsidiandrill`, `glacierrail`) — neither of which any stage still uses.

## 3. The fix

Four entries added to `_PACKOF`, driven off the stage's own `SUBBOSS[n].kind`:

```
siegeember -> nsb_siege_ember     thornrime -> nsb_thorn_rime
blacksteel -> nsb_blacksteel      herald    -> nev_venom_
```

**Kept narrow: one key each** for the three hulls, eleven for the Herald's attack reel. 0801kl had
to cut this same block back from 555 images because warming every pack stalled the liquid beds.

After, at the same measurement point:

```
stage 2   1 not ready -> 0        stage 3   1 not ready -> 0
stage 4  12 not ready -> 11       stage 8   6 not ready -> 0
```

**Every miniboss now has zero unready art of its own at spawn**, and the renders show real hulls —
the ember carrier on sand, the rime thorn on ice, the blacksteel raptor on the airbase.
Proof: `docs/proofs/miniwarm_s1..8_0812c.png`.

⚠ **STAGE 4's REMAINING 11 ARE ROAD SIGNS** (`nrs_air_force_base`, `nrs_checkpoint_ahead`, …) plus
`nst4_crash_overlay` — scenery, not the miniboss, and left alone here. Worth connecting to the
tester's separate *"signs scroll when told not to"*: the sign system is unwarmed on the one stage
that uses it most.

⚠ **THE HERALD'S `mba_vr_*_clean` PLATES ARE NOT IN `XART._src` AT ALL** — zero keys start with
`mba_vr`, so `XART.rdy` on them can never return true. Warming the venom reel made those calls stop
happening, so the fallback path is now the one that runs and it draws. **This is not resolved, it is
routed around.** Stage 8's boss is already on the not-yet-built list; whoever takes it should start
here.

---

## 4. Suite

**2,512 assertions / 223 sections / 5 failures** — the same five long-standing ones.

New **§218** pins the four warm entries and asserts all eight stages name a miniboss. It pins the
*assumption*, not the numbers: if someone adds a ninth miniboss and warms it by kind name, this is
the assertion that should catch them.

---

## 5. Still owed from the tester's list

- **Stage 8 boss**: four forms, very high HP, same attack pattern. Mike: *"filler shit"* — and see
  the `mba_vr` note above before starting.
- **Signs scroll when told not to** — investigated here and **NOT REPRODUCED**; it needs Mike's
  word, not a code change. Two hypotheses were measured and both refuted:
  - *the terrain and the props scroll at different rates* — `drawLevelMaster` consumes the master
    as `srcY = rangeSrc - (mapScroll/range)*rangeSrc` while signs draw at `y - mapScroll`, so they
    drift whenever `scrollLen ≠ plateH - VH`. Checked all eight stages: **`scrollLen` is null
    everywhere and `range === rangeSrc` on every stage.** In step.
  - *the signs miss the camera translate* — they do not; `drawBG` calls `drawLevelMaster`,
    `drawStageProps` and `drawRoadSigns` in one transform state.

  Measured on stage 4: world 800 wide, `VW` 480, `camX` 0..320, sign x positions
  `222 247 254 274 296 | 500 512 557 576 594` — five each side, all reachable by the camera, and
  they alternate as the 0801cu note intended. Filmstrip at 18/30/45/62% of the level shows them
  pinned to the tarmac while it moves past.

  ⚠ **The question is what "scroll" means.** Mike's own 0810h instruction was *"they do not scroll
  ever, they are objects that stay put"*, and objects that stay put **on the map** must move up the
  screen as the level advances — which is what they do. If he means screen-fixed, that is a
  different design and his call.
- **A waterfall sits in the middle of the road** — not yet located; `drawLiquidFalls(srcY)` is the
  place to start, and note it takes SOURCE-space y while props take map-space.
- **The barrel roll fires on micro-adjustments** — hold/toggle shift (tester) vs a cooldown (Mike).
  **Needs Mike's call**, it is a feel change to core movement.
