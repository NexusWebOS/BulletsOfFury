# FIRE / ICE WEAPONS — drop 0810a

    verify_0730a  468 passed / 6 failed        test_fl  2096 passed / 2 failed
    (the 8 remaining are the primary machine's backup folders + the missing micon_ art)

Mike: *"correct the fireball, use the fire shards, not the fireball scaled down ... the ice orb
needs to shoot shards too ... fireball especially drops the fps to below 10 ... the correct pickup
icons come out for this weapons in stages 2 and 3."*

All of it verified in the running game, not just the harness.

---

## 1. THE FRAMERATE — TWO SEPARATE BUGS, BOTH REAL

### 1a. shadowBlur on every projectile

Measured in play at weapon level 5:

    240 shards, shadowBlur live      123.1ms/frame    8 fps
    240 shards, shadowBlur stubbed    15.7ms/frame   64 fps

**The blur was 107ms of a 123ms frame — 87% of it.**

And 240 shards is not a synthetic number. `shardN` at level 5 is **9**, spawned every **0.10s**, each
living **1.3s** — so one orb sustains ~117 shards, orbs live 2.6s, and two or three overlap. Firing
the level-5 orb IS the 240-shard case.

The engine already had the answer and the shard layer never used it. `bakeGlow`/`drawMfx` exist for
exactly this, with a comment that reads:

> ctx.shadowBlur on drawImage is the single most expensive canvas op in a browser ... the bullet
> layer used to do 1-2 of them PER BULLET, per frame ... which is exactly the framerate cliff.

The shard, orb and fireball-orb draws now go through `drawMfx`, which bakes sprite+glow once per
(key, size, glow) and blits it flat forever after. Zero shadowBlur in the hot path.

### 1b. ⚠ A PARTICLE LEAK, IN THE EXACT TWO WEAPONS

The particle expiry test sat at the BOTTOM of the update loop, after two branches that draw and
`continue`:

    if(p._fbDecal){ ... continue; }     // the FIREBALL's decal
    if(p._iceChip){ ... continue; }     // the ICE ORB's hull shards
    ...
    if(p.t>=p.life) p.dead=true;        // neither ever reached this

Neither kind was ever marked dead, so neither was ever filtered out. **They lived forever.**

Measured: particles decayed to **1769 and then stopped, permanently**. Frame cost **32.58ms with
them against 2.88ms without — 91% of the frame**, spent redrawing immortal debris. `_iceChip` is
the worse of the two because it re-tints its sprite every frame, per particle.

The check runs before anything can skip it now. After the fix, particles drain to **0**.

### Net effect

    before   median 26.7 / 34.5 / 30.8 ms over three passes — degrading as the leak grew
    after    median  3.0 /  5.7 /  5.1 ms — stable, and particles return to zero

## 1c. ⚠ CORRECTION: THE 450-SHARD FIGURE WAS MY HARNESS, NOT THE GAME

I reported "450+ shards on screen" and called the count alarming. **That was my benchmark pushing
orbs in every 40 frames and ignoring the game's own limit.** The weapon caps itself:

    const maxOrbs = lv>=5 ? 2 : 1;

Two orbs, never more. Measured through the REAL firing path — holding FIRE, letting the weapon's
own gating decide — the true ceiling is **289 shards**, and it now runs at:

    median 3.9ms (256 fps) · p95 12.5ms · 2 orbs · 289 shards · particles 1

So the object count is no longer a performance problem. It was never the CAUSE — shadowBlur and
the particle leak were, and both are gone.

### And cutting the count buys nothing — tested, not assumed

Before recommending a nerf I measured it: same damage per second, fewer and meatier shards.

    as shipped   9/burst, dmg 1     292 shards   median 5.4ms   p95 19.9ms
    2/3 count    6/burst, dmg 1.5   136 shards   median 5.8ms   p95 16.3ms
    1/2 count    4/burst, dmg 2     139 shards   median 5.2ms   p95 17.6ms

**Halving the shards moves the median by 4%.** Cutting the spray would cost the weapon its look for
no measurable gain, so `shardN` stays exactly as authored.

The remaining worst-frame outliers (200-500ms, roughly one in 400 frames) are **harness noise, not
the game**: they got WORSE in the reduced-count runs, which is impossible if object count caused
them. The browser pane is not compositing during measurement and the loop is being stepped
synchronously, so single-frame outliers there are not meaningful. Whether it FEELS right still
needs playing.

## 2. THE ART — SHARDS ARE SHARDS NOW

Both weapons were spraying **shrunken copies of themselves**:

    fire shards drew  nfb_fl<lv>_*   the fireball's own FLAME reel, squashed to ~17-28px
    ice shards drew   nio_<lv>_*     the frozen ORB, squashed the same way

The dedicated sets were sitting in the manifest as an unreachable fallback: **`fshard_0..13`
(fourteen frames)** and **`iceshard_0..3`**, referenced once and twice in the entire engine.

Now: fire → `fshard_`, ice → `iceshard_`, with the old reels kept only below them as a fallback.
Confirmed in the running game by intercepting the draw calls — `fshard x240` on stage 3,
`iceshard x240` elsewhere, and neither reel appearing at all.

**A test was pinning the bug.** `test_fl` asserted `'nfb_fl'+_flv+'_'+_ff` — it required the
scaled-down fireball. Rewritten to assert the correction.

## 3. THE PICKUP ICONS

`weaponIconKey` resolves the ideal key. Measured: **`micon_*` has ZERO keys registered, for every
weapon at every level.** Its own comment claims "All three icons already existed and were simply
unreachable — micon_fireorb_1..5, micon_thermoshock_1..5, micon_iceorb_1..5". None of them exist.
That drop fixed the lookup and the art never arrived, so **the fix has never once taken effect** —
the same shape as `_flameRaw`.

The old fallback then dropped to the SLOT's base icon, which is right for the base weapons and
wrong for the variants — exactly the bug 0806d set out to kill:

    stage 3, slot 5 dispenses the FIREBALL   ->  wore the ICE ORB icon
    Freezer, slot 4 is ICE BREATH            ->  wore the FLAMETHROWER icon

`weaponIconFallback()` now picks by VARIANT, from art that is on disk. Verified live:

    laser        -> laser_icon_3
    flamethrower -> firewall_icon_3
    ice breath   -> nib_roll_0        (was firewall_icon_*)
    ice orb      -> ice_icon_3
    fireball     -> nfb_orb3_0        (was ice_icon_*)

`micon_*` is still tried FIRST, so drawing that art later needs no code change.

### The EQUIPPED box had never drawn an icon at all

`index.html` builds `micon_<weapon>_<level>` and guards on `rdy()`. With zero micon_ art it drew
the empty box forever — measured at **0 lit pixels**. It now falls through the same resolver:
**15,182 lit pixels**.

## 4. ICE BREATH

Art verified present and registered: `nib_roll_0..7`, `nib_hold_0..5`, `nib_wall_*`. Freezer's
slot-4 icon now resolves to it rather than to the flamethrower.

## 5. ⚠ gamecode.js — I STOPPED BACK-PORTING THE DRAW REGION, DELIBERATELY

`gamecode.js`'s shard block is **several drops behind** `assets/game.js` — it has no `orbIsFire`
branch at all, only the pre-fireball ice path. Splicing the new block onto that stale base produced
a file that **would not parse** (an illegal `continue`, because the surrounding loop differed). I
restored it from `_pre0810a_backup` and both files parse again.

What DID cross safely: the particle-leak fix, `weaponIconFallback` and its call site,
`weaponIconKey`, `updateEffects`.

What did NOT, on purpose: the shard/orb draw rewrite. Grafting new code onto a base that is drops
behind is how you get a bug that only appears on a rebuild, months later.

    fshard_    game.js=3   gamecode.js=1     <- the divergence, recorded rather than forced

`assets/game.js` is the authoritative artifact and the 0805a guard already refuses to build from
the stale sources. This region needs the proper reconciliation pass, and that is better done on the
primary machine where a rebuild can actually be tested.
