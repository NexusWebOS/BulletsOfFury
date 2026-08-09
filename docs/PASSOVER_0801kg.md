# BULLETS OF FURY — SESSION PASSOVER (drops 0801hl → 0801kg)

Written so this conversation can continue elsewhere without losing context.
Everything below is measured from the current build, not recalled.

**Build:** `/tmp/build/BulletsOfFury/` · 495 MB · manifest **9,517 refs, 0 missing**
**Harness:** `node _BUILD_SOURCE/test_fl.js` — **1,736 assertions / 151 sections / 2 failing**
**Latest package:** `BulletsOfFury_0801kg.zip`

> A harness result of **0 failures is a CRASH, not a pass.** Always check the
> assertion and section counts too. This caught me four times this session.

---

## 1. THE TWO REMAINING HARNESS FAILURES

| assertion | status |
|---|---|
| `the stage-7 boss triggers at the end of the stage` | pre-existing, never diagnosed |
| `every mount fires a projectile type that actually exists` | pre-existing, never diagnosed |

---

## 2. BUGS MIKE REPORTED, AND WHERE THEY STAND

### FIXED — root cause found and verified

**Miniboss unkillable.** Drop 0801if added a gate sealing the hull until all four
cannons die — but **nothing in the game ever set `c.dead`**. Zero occurrences. The
gate could never open. Cannons now take damage through their own hitboxes.
*Also:* `hb` is `[x,y,w,h]` in **384px sprite space**, not an `{x,y,w,h}` offset —
reading it as an object gave `undefined` and every hit missed.
*Also:* `_lastHitX/_lastHitY` were only set on the **boss** path. Fourteen
`hitSubBoss` call sites and not one passed an impact point, so the hitbox test read
a stale value. `hitSubBoss(dmg, hx, hy)` now takes it as an argument.

**Miniboss drew as one unit.** The draw called `nql_intact_01` — the original plate
with all four cannons baked in. The separated plates built in 0801ic–0801ie were
registered and **never referenced by anything**. Now the hull draws alone and each
living cannon draws as its own plate.

**Boss bar never filled.** `nbb_fill` is 512 wide but its art occupies only
**x 108..403 — 21% to 79%**. Clipping from x=0 showed nothing below 21% health.
Now clips between the fill's real edges.

**Every miniboss bar read empty.** `nmb_frame` has a **100% opaque interior**;
drawing it last buried its own fill. Solid frames are now backplates, drawn first.
*Also:* `nmb_seg` is **39×33 — one tick**, and stretching it across the bar made a
solid block. Narrow seg plates now tile, and only to the health level.

**No shock rings, barely any debris.** They were being created correctly — 1 ring
and 10 chunks per kill — but the draw call had landed inside **`drawRaceFight()`**,
the race system Mike deleted. Nothing calls it. Moved into `drawWorld`.

**New art not loading at all.** `warmStage` preloads by **stage folder** and by
**boss/sub-boss kind name**. Every family built this session is named differently
and lives outside a stage folder, so none were ever decoded and every draw took its
fallback. Now warms `nqx_ nsr_ ndbr_ nbs_slot_ nchx_` plus the debris ramps a stage
uses. Stage requests: ~280 images (warming all 1,024 debris keys pushed it to 1,256,
which risks the stall that hit the liquid beds).

**Tanks missing at the coast.** *Not the wave.* `SUBBOSS[1].at = 0.45` put the
quadlaser at **mapScroll 1224**; the coastline is at **1416**; and since 0801hn the
miniboss **holds the scroll until it dies**. The stage froze short of land and the
beach wave could never fire. Moved to `at: 0.62`.

**Jets firing large bullets.** `mg` fires a **lock-on missile every 6th cycle**, and
the racer's flight phases called `enemyLockOn` directly. Added a pure `gun` mode;
`enemyLockOn` now refuses any unit on it.

**Jets appearing randomly / from the bottom.** The `racer` pattern ran
cross → curl → dive → flee; traced, it wandered (56,−17) → (422,207) → (283,188) →
(316,410). Replaced with **`strafedive`**: one pass, top to bottom, leaning toward
the player, guns firing throughout.
**Eight harness assertions were enforcing the OLD behaviour** — including one named
*"the pair enters from opposite bottom corners"*. That is why it survived three
rounds of fixes. Retired with notes.

**Whole miniboss frame lit on any hit.** `b.flash` drove a full-sprite tint. Each
cannon now has its own `c.flash`; only the plate that was hit lights. The hull uses
`b._qlArmor` — an amber outline pulse — instead of a white wash.

**Purple/magenta on damage frames.** Concentrated on the `_crit` plates.
**309,116 px healed across 1,085 sprite files**, zero remaining.

### STILL OPEN

| item | detail |
|---|---|
| **Tanks not *at* the coastline** | they land at scroll **1477**, coast is **1416**. Mike wants them right at it. Tuning number. |
| **Miniboss fires `dart`** | `dart` was scrapped in 0801hj. It fires 65 rounds, first at 1.7s, but among `flare, dart, emissile, mg`. |
| **399 frames of magma art orphaned** | see §6 |

---

## 3. THE APPROVED PROJECTILE SET

Mike's six, from drop 0801hj:

```
pellet    jets and planes        (mfx_mg_2_*  / kind:'mg' alias)
flare     tanks                  (mfx_ea_3_*)
comet     gunships               (mfx_ea_1_*)
blast     fire enemies, faces S  (mfx_bpow_*)
homing    heli boss and above    (mfx_hom_*)
missile   fodder, no homing      (mfx_emr_*)
```

**SCRAPPED — must never appear:** `dart`, `gem`, `laser`. Quarantined to
`_superseded/projectiles/` with `PROJECTILE_LEDGER.json`.

**Off-spec kinds that were in use and are now routed:**
`embullet` → pellet · `bolt` → pellet (the `eShoot` default) · `groundup` → keeps
its scaling behaviour but draws `_fx:'flare'`, or `_fx:'blast'` for the tank main gun.

Current stage-1 state:
```
racer       mg (pellet)
intcp       mg (pellet)
topgun      mg (pellet) + emissile
jungletank  mg (pellet)          <- should be FLARE, still to route
sandtank    groundup/blast
```

---

## 4. STAGE 1 — THE AUTHORED PLAN

`buildStagePlan` has **eight return points**. Stage 1 returns before the
`// common early` tail. Three legacy blocks used to append on top of it — a
`stageNum>=3` section, two stage-1 tails, and the unguarded common-early block —
giving **34 entries where 15 were authored**. All gated off.

**The plan is sorted by time at the assignment point** (`stagePlan=buildStagePlan(num)`),
because the dispatcher walks the array with a single `waveIdx` and an out-of-order
entry blocks everything behind it.

```
t= 2.0   two racers, flyby, no fire
t= 6.0   racers, machine guns
t= 8.2   racers, missiles
t=21.0   grass jets in off the LEFT edge
t=24.0   grass jets in off the RIGHT edge
t=30.0   diagonal file of four topguns
t=36.0   FOUR JUNGLETANKS, beach          <- terrain-gated
t=44.0   sand tanks, pair                  <- terrain-gated
t=47.0   air pair
t=50.0   sand tanks, three                 <- terrain-gated
         MINIBOSS at scroll 0.62
t=58..81 five air-only waves, no ground past halfway
         HELICOPTER BOSS
```

**Ground waves gate on TERRAIN, not the clock** — `_s1Ground` checks `_s1OnLand()`
and defers a beat if still at sea, rather than letting the coastline rule convert
the tanks into ships.

**Stage constants:** coastline `mapScroll 1416` (camY 3384 on a 4800 master) ·
`JUNGLE_CAP` 7 live, dispatch at cap−4 · `curStage.length` 62s.

---

## 5. UNIT BEHAVIOUR, MEASURED

| unit | hp | size | speed | pattern | fires |
|---|---|---|---|---|---|
| racer | 5 | 44px | — | **strafedive** | pellet, top→bottom |
| intcp | 3 | 39px | — | weave | pellet |
| topgun | 4 | 43px | — | topgun | pellet + missile |
| jungletank | 11 | 52px | 65 px/s | tankhold | groundup |
| sandtank | 5 | 34px | 0 lateral | **sandtank** | blast |

**Tank rules (Mike):** slow · shake while moving · kick back and shake when firing ·
**never wobble or strafe**. `sandtank` pins its lane every frame — measured 0.00px
drift over 240 frames. `_selfPat['sandtank']` and `_selfPat['strafedive']` must stay
set or the generic pattern block overwrites them (it swung the tank 92px).

**MINIBOSS — Quad Laser:** hp 185 · 196px · 4 cannons at 23 hp each ·
hull sealed until all four die · first shot 104f · peak 24 rounds.
**BOSS — Jungle Overlord-X:** hp 299 · 170×130 · 72-frame rotor · first shot 59f ·
peak 34 rounds · `phase` never leaves 0 (unfixed).

---

## 6. THE MAGMA COLOSSUS — ART BUILT, NOTHING WIRED

**399 frames referenced by no code.** The GIFs sent during the session were real
renders of real art, but they were previews — none of it is connected to the game.

```
mgx_        14   8 whole-body poses at 256x256 + the lassoed head
nqm_       175   core charge/split, shield, eyes, iris, rise, form, shoot sign
nqv_        56   magma veins, all 7 pieces
nch_        22   chain overlay kit (armor-cap, body-socket, anchor-clamp)
bfx_       216   boss fire FX, 12 bosses x projectile/muzzle/impact
```

Key measurements if this gets picked up:
- torso `mbg2_m_torso` 275×335; head socket **cap at (141,45), 62×34**; chain
  launcher **plate at (137,311), 107×38**
- fusion core **1,726 px at x 92..182**, bright spine on **x=134**
- assembled figure scales by **one factor 0.389** to 241×256
- cannon muzzle anchors: `(44,239) (99,241) (284,241) (339,239)`
- specs: `docs/MAGMA_COLOSSUS_SPEC_0801iu.md`, `docs/MAGMA_COMBAT_SPEC_0801jr.md`

---

## 7. TRAPS THAT COST TIME THIS SESSION

1. **A harness pass is not a game pass.** Nearly every "verified" fix failed in
   Mike's build. Mocks report `complete=true` on every image, hiding the entire
   `warmStage` class of bug.
2. **`0 failures` = a crash.** Check assertion and section counts.
3. **Tests can encode the rejected spec.** Eight assertions were enforcing the
   bottom-corner jet entry Mike had explicitly rejected.
4. **A sine repeats its values** — `sin(t*2π)` gave byte-identical frames four
   separate times. Use a ramp for a travelling front.
5. **Thresholds tuned to one sample generalise badly.** Magenta needed three
   attempts; the right invariant was the *ratio* (green collapses, red and blue
   stay high), not any absolute brightness.
6. **A proxy measurement is not the thing.** A tall bounding box ≠ pointing south;
   brightest ≠ most saturated; no movement ≠ correctly held still.
7. **`_selfPat` must include any new self-driven pattern**, or the generic block
   overwrites it.
8. **Art built ≠ art wired ≠ art warmed.** All three are needed.

---

## 8. IMMEDIATE NEXT STEPS

1. Drop the beach tanks to land **right at** scroll ~1430
2. Route the miniboss off `dart` onto the approved six
3. Wire the magma boss draw path to `mgx_`/`nqm_`/`nqv_`, then its intro state machine
4. Chase the two long-standing harness failures

---

## 9. THE THREE OUTSTANDING QUESTIONS — DIAGNOSED (drop 0801kj)

Mike: *"what about the patterns not being the ones I asked? or the 2nd miniboss not
being replaced? or the 2nd boss not doing the intro? whats causing that?"*

All three have the **same root cause as the quadlaser**: the art was registered and
the draw path was never pointed at it.

### 9.1 The 2nd miniboss

`SUBBOSS[2] = {at:0.45, kind:'obsidiandrill'}` — the TABLE is correct. But the draw
emits `nsx_odt_core_hull_intact` — the **old sectional set**. The 70 `nobd_` frames
registered in 0801hm are never referenced.

**All eight bodies from 0801hm are orphaned:**

```
legion-command-tank   70   ORPHANED     obsidian-drill    70   ORPHANED
mirv-stalker          70   ORPHANED     glacier-rail      70   ORPHANED
sludge-crawler        70   ORPHANED     rampart-zero      61   ORPHANED
toxic-leviathan       73   ORPHANED     cyclone-carrier   71   ORPHANED
```

555 frames. The code draws the 205-key `nsx_` set instead.

### 9.2 The 2nd boss intro

`STAGES[1].boss = 'magmacolossus'` is correct. There is **no intro state machine at
all**, and the 399 magma frames (§6) are unreferenced. Nothing to play.

### 9.3 The patterns

The units spawn at the right times and places, but run **generic movement**:

| Mike's spec | what runs |
|---|---|
| grass jets: in from the tip, TURN, to the MIDDLE, PAUSE, levitate, ORBIT, then attack | `weave` — snakes straight down. Measured: 3 near-stationary frames, no mid-screen hold |
| beach tanks: horizontal row of 4, each set back further, firing **one by one** | four spawns at staggered y. No firing order |
| diagonal file of 4, top-left to right | four spawns. No file movement |

Only `strafedive` (racer) and `sandtank` are purpose-written. Everything else is
placement without choreography.

### 9.4 Also wrong vs `BOSS_ROLES_0801hm.md`

```
stage 5 miniboss   is subcore        should be rampart-zero
stage 7 miniboss   is ratking        should be toxic-leviathan
stage 7 boss       is toxicleviathan should be sludge-crawler
stage 6 boss       is stormsovereign should be cyclone-interceptor-carrier
```

### The pattern behind all of it

Three separate times this session the same failure: **art registered, manifest
clean, warm list updated — and the draw still pointing at the old keys.** Adding a
key to the manifest does nothing on its own. The checklist for any new art is:

1. registered in the manifest
2. **referenced by the draw path**
3. warmed by `warmStage`

Only step 1 was reliably happening.
