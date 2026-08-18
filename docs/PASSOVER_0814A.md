# DROP 0814A — THREE WEAPON REPORTS, ONE DEFECT: NOTHING RECORDED WHAT THE PILOT WAS HOLDING

Mike's items 1, 2 and 3, from the list Brian handed over at `main @ e8f8e62`:

> 1. Freezer picks up flamethrower but uses ice breath. They are SEPARATE attacks, and ice breath
>    is exclusive to Freezer from level 2 onward.
> 2. Fire orb and ice orb keep swapping icons, and fire randomly one or the other.
> 3. fireiceorb fires a basic fireorb.

The handoff calls 1–3 "one cluster around weapon identity". They are closer than that: **they are
one bug with three symptoms.**

---

# 1. THE VARIANT A PILOT IS HOLDING WAS NEVER WRITTEN DOWN

`weaponVariant(w, opt)` answers **"what should the next crate dispense?"** — it reads `run.stage`,
it reads the pilot, and for Freezer's flame slot on stage 4+ it calls `Math.random()`.

Every runtime surface in the game was asking that function **"what am I holding?"**

    the HUD icon · the equipped box · the world pickup · attackElement · the projectile
    the flame reel · the legacy fallback · weaponDisplayName

There was nowhere else to ask. The pickup's variant IS baked at spawn — `spawnContainer` writes
`wvar` onto the crate, `breakContainer` carries it to the weapon pickup — and `applyPowerup` read
it **for the announcement banner and then dropped it on the floor.** Nothing persisted it.

So all three reports are that guess being wrong in a different way:

| Mike's words | the mechanism |
|---|---|
| "keep swapping icons" | `drawPowerups` called `weaponIconKey` **with no opt, once per frame**. On stage 4+ that re-rolls `Math.random()`. A falling crate genuinely alternated between the flamethrower and the ice breath icon at 60Hz. |
| "fire randomly one or the other" | `orbIsFire()` was `run.stage===3`. The **same orb** was fire on stage 3 and ice on stage 4 — icon, element, ball art and shard art all flipping at a stage boundary with no pickup involved. |
| "picks up flamethrower but uses ice breath" | the flame path never asked about the pickup at all. It asked `_pilotKey()==='freezer'`. |
| "fireiceorb fires a basic fireorb" | literally true, and it had never been otherwise. |

⚠ **THE COMMENT ABOVE `WVAR_NAME` PREDICTED THE ICON FLICKER EXACTLY** — *"a variant re-rolled per
frame would flicker between two icons while the crate is falling"* — and then **no call site
honoured it.** 0812l wrote the warning and built the baking; the consuming half was never done.
A warning in a comment is not a mechanism.

`heldVariant(w)` is the missing half. It reads `run.wvars[]`, which `applyPowerup` now writes from
`p.wvar`. `weaponVariant` keeps its own job and is the **fallback only**, for a slot granted with
no pickup behind it (debugEquip, a loaded save, the attract demo), so nothing regresses.

---

# 2. ITEM 1 — THE FLAMETHROWER AND THE ICE BREATH ARE TWO ATTACKS NOW

`flameIsIce()` returned true for Freezer **unconditionally**. The two attacks could not be told
apart because nothing in the engine distinguished them: 0801fl's own comment says *"when he
acquires flamethrower, turn it into ice breath instead"*, which was Mike's spec at the time and
is the spec he has now replaced.

Every flame-gated site routes through that one function now — the draw, the hit width, the
element, the freeze-on-hit, the legacy icon — so they cannot disagree again.

## The dispenser table, with Mike's new rule folded in

    freezer, stage 1     flamethrower      (ice breath is not his yet)
    freezer, stage 2     ICE BREATH        "from level 2 onward"
    freezer, stage 3     flamethrower      ice breath disabled on the ice level, per 0812l
    freezer, stage 4+    either            "he can obtain both"
    everyone else        flamethrower      ALWAYS — ice breath is exclusive to Freezer

⚠ **STAGE 3 USED TO RETURN `null`, WHICH WITHHELD THE WHOLE SLOT.** That was not a choice, it was
a limitation: while the flamethrower and the ice breath were one weapon, *"disable ice breath …
for him"* could only be honoured by removing the slot. Now it can be honoured as written. Stage 3
is also where `freezerL3Begin` hands him a flamethrower off the magma mech as an **authored story
beat** — *"Weapon cooler… offline. Pulled this off that magma mech back there."* — and before this
drop that beat handed him a weapon that came out as **frost**, contradicting its own narration.
`run.wvars[4]='flamethrower'` is now stated there explicitly rather than left to a table default.

⚠ **ONE ASSERTION FAILED AND IT WAS DEFENDING THE LIMITATION, NOT THE RULE.** §"the flame slot
cannot DROP for Freezer on stage 3" pinned `weaponVariant(4)===null`. Read before fixing, per
CLAUDE.md. It is repointed onto what Mike actually said — the slot drops, and over 200 rolls it is
**only ever the flamethrower** — which is a stronger claim than the one it replaced.

---

# 3. ITEM 3 — THE FIRE-ICE ORB HAD AN ICON, A NAME, A TABLE ROW AND NO PROJECTILE

`freezerOrbCharge` → `launchFireball` → a plain fireball. That was the entire weapon.

**`nts_` was already in the manifest: 45 registered keys with ZERO references anywhere in
`game.js`.** Rendered (rule 1, `docs/proofs/` and the contact sheet that produced this list):

    nts_orb_0..11    224x224   a 12-frame ball split fire/ice, flame and frost tongues turning
    nts_shard_0..7    64x64    FOUR FLAME PLATES AND FOUR FROST ONES
    nts_burst_0..7   256x256   an eight-point star of alternating fire and ice bolts
    nts_chg_0..3     192x192   a charge reel: sparks converging -> swirl -> the split sphere
    nts_rel_0..3     256x256   the release ring
    nts_imp_0..3     256x256   the impact
    nts_cmp_0..4      64x64    single flame / frost components

That eight-point burst star **is** the discharge Mike specified in 0801fj — *"shoot fire out all 8
directions 1 by 1 but with a small tic delay"* — and the four-and-four shard split is why. The art
had the whole weapon in it; nothing had ever asked for it.

Wired: same flight, same three tiers, same brake-and-unload beat, so the fireball Mike signed off
in 0801fm is **bit-identical** and only the identity changes. The rays alternate fire and ice, the
charge draws `nts_chg_*` **off the charge fraction rather than a clock** (0811y/0812g), and the
burst star is driven by `_rayI` so one arm appears per ray.

⚠ **12 FRAMES, NOT 8.** `%8` on the orb reel silently drops a third of the animation and reads as a
stutter at the wrap. `TS_REEL_N` carries every reel's length.

⚠ **THE FIREICE CASE MUST BE TESTED BEFORE THE FIRE ONE IN `drawBullets`.** `orbIsFire()` is true
for fireice as well — it *is* half fire — so a fire-ice orb would otherwise fall straight into the
fireball's art and the bug would survive the fix wearing a new cause.

---

# 4. TWO THINGS FOUND ON THE WAY IN, BOTH IN THESE SAME WEAPONS

## 4a. ⚠ THE ORB AND ITS SHARDS HAVE NEVER TAKEN THE ELEMENTAL BONUS

`attackElement` has answered for kind `'orb'` and kind `'shard'` since 0801fn and **nothing ever
asked it.** Grep `elementMultiplier`: its only call sites were the fireball and the flame. So
Mike's own rule — *"all fireattacks do 2x damage to ice enmies, vice versa on stage 2"*, the
entire reason the fireball exists on the ice level — **has never once applied to the weapon it was
written for.**

The shards fall through to the GENERIC bullet collide, which knows nothing about elements, so the
multiplier is solved once per volley and baked onto the projectile at spawn. Element and stage are
both fixed by then and the hot path pays nothing.

⚠ **THIS RAISES ORB DAMAGE ON STAGES 2 AND 3 ONLY.** It is a declared rule finally firing rather
than a balance change I chose, but it is a damage change and Mike should see it. The dial is
`elementMultiplier`.

⚠ **AND THERMOSHOCK IS SET TO 2x ON BOTH ELEMENTAL STAGES — THAT ONE IS MINE.** The weapon is fire
AND ice in one projectile, so the half that counts is always the opposing half. Mike specified the
weapon, not its multiplier. One line to make it 1 if he wants the halves to cancel.

## 4b. ⚠ THE PARTICLE LEAK 0810a FIXED IS BACK, IN THE EXACT SAME TWO WEAPONS

`FIRE_ICE_FIX.md` §1b describes this defect and says it was fixed. In `assets/game.js` the expiry
test `if(p.t>=p.life)p.dead=true;` sat at the **BOTTOM** of the particle loop, after the
`_fbDecal` and `_iceChip` branches — **both of which draw and `continue`.** Neither kind was ever
marked dead; neither was ever filtered out.

Measured when it last happened: **32.58ms of frame with them against 2.88ms without — 91%**, and
`_iceChip` is the worse of the two because it re-tints its sprite every frame, per particle.

The test is at the TOP of the loop now. Setting `dead` there does not skip the draw — the branches
below still run and the filter at the end is what removes it. Guarded:
`_fbDecal`, `_iceChip` and the new `_tsFx` all **drain to 0** after two seconds.

⚠ The doc says the fix "crossed safely" to `gamecode.js`. It did. It is `assets/game.js` — the
authoritative artifact — that has it at the bottom. **A fix recorded as landed is not a fix
observed landing.**

---

# 5. VERIFICATION — STATE AND PIXELS, SEPARATELY, BECAUSE THEY ANSWER DIFFERENT QUESTIONS

## The suite

    baseline HEAD 636e9db    2,659 ok  /  5 failures  /  2,664 total
    this drop                2,660 ok  /  5 failures  /  2,665 total

⚠ **THE BASELINE WAS RUN, NOT ASSUMED** — a clean `git worktree` at HEAD, same machine, same
node. My first run came back **2,658 / 6**, total unchanged at 2,664, so the whole delta was one
assertion moving from pass to fail and it was findable in one line. Rule 3's COUNT check only
works if you know what the count was.

The five failures are the five long-standing ones: preload count, two `_superseded` ledger checks,
the volley round count, the flash families. **Net +1 assertion** — the repointed stage-3 one became
two (the slot drops / it is only ever the flamethrower).

## `_BUILD_SOURCE/probe_weaponid_0814a.js` — the state, **30/30**

Drives the real engine in `test_fl.js`'s vm and asks the questions Mike's sentences ask, including
the two exhaustive ones:

- **no pilot but Freezer can EVER be dispensed ice breath** — 9 stages x 8 pilots x 200 rolls, 0 leaks
- **a crate with a baked variant answers ONE icon over 240 frames**, while the dispenser rule
  genuinely does re-roll over the same 240 — which is the flicker, isolated
- a fire orb carried off stage 3 keeps its icon and keeps firing fire; an ice orb carried onto
  stage 3 stays ice
- the full charge fires **all eight rays, four flame and four frost**
- the plain fireball is **unchanged** — no `_ts`, same weapon Mike signed off

## `_BUILD_SOURCE/probe_weaponid_0814a.py` — the pixels, **5/5**, real Chromium

| case | held | drew | leaked | plate warm% | plate cold% |
|---|---|---|---|---|---|
| FLAMETHROWER *(item 1)* | flamethrower | `nfw_wall_` | – | **60.2** | 0.0 |
| ICE BREATH *(item 1)* | icebreath | `nibr_` | – | 0.0 | **79.3** |
| FIRE ORB *(control)* | fireorb | `nfb_orb` | – | **97.3** | 0.0 |
| ICE ORB *(control)* | iceorb | `nio_` | – | 0.3 | **58.5** |
| FIRE-ICE ORB *(item 3)* | fireice | `nts_orb_`, `nts_shard_` | – | **42.8** | **28.7** |

`docs/proofs/weaponid_0814a_flame_vs_ice.png` is item 1 in one picture: **one pilot, one stage, one
slot, only the held variant differs** — a red flame column beside a cyan frost plume, and the
EQUIPPED box in the corner of each showing the matching icon.
`docs/proofs/weaponid_0814a_orbs.png` is items 2 and 3: three orbs, three weapons, and the fire-ice
one throwing orange shards and blue shards out of the same ball.

### ⚠ THE FIRST CUT OF THE PIXEL PROBE MEASURED THE LEVEL, NOT THE WEAPON

It classified every lit pixel in a 180x230 band as warm or cold. On stage 2 the desert reported
**143,194 warm pixels with the ICE BREATH equipped**, and the run "failed" on correct code.
**153,866 "lit" pixels in a 165,600-pixel band is the tell** — that is the backdrop; the plume is
a few hundred pixels beside it. Same family as 0813x's edge detector finding the HUD instead of
the terrain, and as `probe_seam.py` recomputing its own answer.

The fix is not a better threshold. **The claim is about the ART, so the ART is what gets sampled**:
the exact plate the draw path asked for, alpha-masked, on nothing. Backdrop cannot contribute.

### ⚠ AND READING THE SURVIVORS AT THE END MEASURES NOTHING

The .js probe's ray test flew the ball 200 frames and then read `pBullets`. The discharge takes
8 x 0.3s and then the ball detonates and every ray leaves the screen, so at frame 200 the array is
correctly **empty** — which the probe reported as "no rays fired". Rays are accumulated as they
appear now. **A quantity that is consumed cannot be measured after it is gone.**

## `_BUILD_SOURCE/probe_scope_0814a.js` — new, and generally useful

`spawnEnemy`'s unclosed `if(base.art===undefined){` swallows everything below it, and CLAUDE.md
records that **both brace-matching and line-bounding give wrong answers** about where that ends.
So ask the engine: this reuses `test_fl.js`'s own vm bootstrap and reports `typeof <name>` at
global scope.

    node _BUILD_SOURCE/probe_scope_0814a.js flameIsIce orbIsFire tsFx explode

It correctly identifies `liveType` as swallowed (matching CLAUDE.md) and confirmed all nine new
identifiers in this drop are global before a single unguarded call was written.

⚠ **IT ALSO REPORTS `ARSENAL_DRONES` AS GLOBAL**, which contradicts CLAUDE.md's note that it is
still function-scoped. Not chased in this drop — but that note should be re-measured rather than
quoted, and this tool is how.

⚠ **`updateBullets` IS NOT A NAME IN THIS ENGINE.** The player-bullet loop is inline in
`updatePlay`. Calling it threw, and there is no smaller unit to drive: a bullet test needs a live
stage under it.

---

# 6. WHAT THIS DROP DELIBERATELY DID NOT DO

- **`ORB_FIRE_ON_L3` is untouched in meaning.** *"Never spawn ice orb on this level for anyone"* is
  a rule about what the level DISPENSES, and it is enforced in `weaponVariant`. What you then
  carry off the level stays what it was — which is the whole of item 2.
- **`CAMP_SAVE_VER` is NOT bumped.** `wvars` is added to the snapshot as an optional field; an
  older slot simply has none and `heldVariant` falls back to `weaponVariant`, i.e. exactly the
  pre-0814a behaviour. Bumping would have invalidated every existing save to add one field.
- **The plain fireball's flight, tiers, damage and finish are unchanged**, asserted.
- **`gamecode.js` is not touched.** `FIRE_ICE_FIX.md` §5 records why: it is several drops behind in
  this exact region and grafting onto it produced a file that would not parse.
