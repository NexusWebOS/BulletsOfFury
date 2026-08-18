# Bullets of Fury

An HTML5 canvas vertical shoot-em-up. Nine stages, nine pilots, hand-authored pixel art
throughout. **Mike (ColeForge) owns every creative and design decision.** Claude implements.

---

## Read this first

Three rules matter more than anything else in this file.

**1. Filenames lie. Render the art before you trust it.**
This has cost real days. `slatejet` is the debris library, not jets. `nxp_smoke` is an explosion.
`nqm_vent` is a mechanical vent port. `nx_smoke` has cross-frame bleed from a bad slice. When you
need to know what a family is, resolve a **mid-reel** frame and look at it — frame 0 of an effect
is usually a 4px spark, and a family name with no index returns nothing at all.
`assets/data/ART_TAXONOMY.json` exists solely because of this and is the source of truth.

**2. A green suite proves state, not pixels.**
`_BUILD_SOURCE/test_fl.js` has ~2,400 assertions and has been green through: jets that never
fired, a muzzle flash drawing on an invisible frame, a stats screen misaligned by half a row, and
stage 1 spawning retired enemy types for weeks. **`_BUILD_SOURCE/shoot.py` is the answer** — real
Chromium, real index.html, pixels read off the canvas. If a change cannot be seen there, it is not
verified.

**3. `0 failures` can mean a crash.**
Always check the assertion COUNT and that the run reaches the `FALVA/LIZZIE BUILD OK` banner. A
syntax error mid-suite reports zero failures and looks like a pass.

---

## Layout

```
assets/game.js        the whole game — large, single file
assets/manifest.js    9 namespaces: BOF BOFA BOFFI BOFPI BOFQL BOFRS BOFTK BOFTM BOFX
assets/game/atlas/    packed sheets; most art is a CELL in a sheet, not a loose file
assets/data/          ART_TAXONOMY.json, STAGE1_ROSTER_SPEC.json, thruster_mounts.json
_BUILD_SOURCE/        test_fl.js, shoot.py, verify_atlas_0806z.js, one-off art scripts
docs/                 76 passovers, one per drop, newest last
```

## Commands

```bash
node --check assets/game.js                  # always, after any edit
node _BUILD_SOURCE/test_fl.js                # the suite. ~10 min. check the COUNT.
node _BUILD_SOURCE/verify_atlas_0806z.js     # every cell resolves, 20 screens, 8 stages

python3 _BUILD_SOURCE/shoot.py --state PILOT --pilot cole
python3 _BUILD_SOURCE/shoot.py --state PLAY --stage 1 --seconds 20 --fps 4 --gif
python3 _BUILD_SOURCE/shoot.py --script scenario.js --warm 300
```

`shoot.py` needs `pip install playwright && playwright install chromium`.

---

## How this codebase bites

These are not hypotheticals. Each cost a debugging session.

**Find the branch that OWNS the object.** `spawnEnemy` has several exits and a
`switch(type)` that overwrites earlier assignments. Setting `base.art` at the top does nothing —
it must go in the switch. Three attempts were burned learning this.

**`if(base.art===undefined){` in `spawnEnemy` is never closed.** Its body is comment blocks and
then top-level declarations, so the function swallows everything after it. Brace-matching and
line-bounding both give wrong answers. Bound by the next top-level `function`.

**A key does not own its file.** ~750 cells are aliased. Check before deleting.

**`e.art` is a NAME, not a cell key.** `drawNewEnemyArt` does `ENEMY_ART[e.art]` and then builds
`base+'_'+enemyArtState(e)` — idle/fire/death/wreck. Hand it a raw cell key and the lookup misses,
it returns false, and the unit falls through to legacy rigs: it spawns, moves, shoots, collides,
and draws **nothing**. `ENEMY_ART_FOOT` (2.15) already compensates for uniform-canvas margin, so a
trimmed rect needs `_foot=1` or it draws 2.15× too big.

**`XART.rdy(k)` returns false on its FIRST call** — that call is what starts the lazy load. Every
one-shot readiness check reads false and looks like missing art. Poll it.

**The player never fires in `shoot.py`.** Firing needs an input tap the harness does not simulate,
so `pBullets` stays empty and any weapon FX measures as dead. A test must call `pShoot()` itself.
`_BUILD_SOURCE/probe_weapons.py` is that test — it drives `pShoot()` directly and asserts on what
lands in `pBullets`, for all nine primaries plus Decker's shotgun and Lizzie's mount.

**A WORLD coordinate drawn into SCREEN space with no camera. This has now bitten THREE times:**
the launch seam (0810a), the outbound routes (0810c) and the level-1 opening's ship (0810e). On an
800-wide stage it is a silent 160px sideways jump. `drawWorld` applies `translate(-camX)` and every
cinematic that draws `player.x`, `o.px` or a master must do the same. A source assertion now
enforces it — deliberately in SOURCE, because the behavioural check is what got fooled:
`probe_seam.py` had been COMPUTING the ship's x as `player.x - camX` instead of recording what was
drawn, so it asserted the fix it was meant to test and called a 160px offset clean. **A probe that
recomputes the thing under test cannot find the bug.** Record what the game actually drew.

**`pShoot` is a chain of early returns, and a weapon that claims the trigger silences everyone.**
`sonicFire` → `dkFire` → Lizzie's mount → the primary, each returning on a claim. `dkFire` returns
true *while reloading* — deliberately, it is what makes the shotgun a shotgun — so any pilot-gate
that is missing there costs another pilot their entire weapon. This is not hypothetical: it cost
Lizzie her turret completely (0810b). When a weapon "does nothing", look UP the chain first.

**State declared inside `spawnEnemy`'s unclosed `if` is re-initialised on every spawn.** A `let`
there is not module state — each wave spawn gives you a fresh one. Anything that must persist
belongs with the pools at the top of the file.

**`_selfPat` gates whether a pattern survives.** A unit not listed there has its pattern
overwritten by a later block. Drive it from a table, never hand-list.

**Assertions can defend a bug.** One required `ship_<pilot>_t` under a comment calling it "the
flameless airframe" — it is the flame-BAKED one. Another pinned the exact stats-screen coordinates
Mike had asked to be replaced. When an assertion fails after a deliberate change, read it before
fixing the code.

**A flat tint destroys the glyph, and it looked like a font bug for three drops.** `ENTER`
rendered as `BNTBR`. The glyph map is correct (A→g00 … E→g04), both atlases hold a clean `E`, and
the slice rects match the true column runs exactly — all three were checked and all three were
innocent. Every letter in this face is a bright face drawn over its own **opaque** dark drop
shadow, and `drawFrameTinted` flooded the cell with `source-atop`, repainting the shadow the same
colour as the face. The E's arm gaps ARE shadow, so they filled in and it became a solid block.
Now `'color'` — source hue/sat, destination luminosity, then `destination-in` to re-mask. This is
what "palette/luminance swaps, not overlays" means; the rule is load-bearing, not taste. **When
text looks wrong, render it tinted AND untinted before touching the map or the atlas** — that one
comparison would have ended it immediately.

**`shoot.py --warm N` is a single synchronous burst.** It never yields, so lazily-loaded art never
arrives no matter how high N goes — 1400 warm frames still showed a black screen where 200 warm
plus `--seconds 2 --fps 3` showed the scene. Each screenshot is a separate `evaluate`, and *that*
boundary is what lets the network run. Use `--seconds/--fps` whenever the shot needs art the state
loads on entry.

---

## Standing creative rules

- Never create placeholder or procedural sprites. Search the existing art first. If unsure which
  fits, render candidates and ask.
- Purple halos are **converted to a black edge**, never deleted.
- Palette/luminance swaps, not overlays. Ordnance keeps its authored colour through a camo swap.
- Every enemy gets: shock ring (fast), debris, white flash, smoke. Tanks and jets also get a smoke
  ring (mid-speed growth).
- One thruster system. `nthp_<pilot>_0..3`, mounted per `assets/data/thruster_mounts.json`.
  The flame-baked `ship_*_t` variants are deleted; never reintroduce them.
- No propellered enemies except the helicopter boss.
- Mike gives high-level direction. **Measure before changing** — pixel positions, frame sizes,
  mount offsets. Do not stop to ask; continue and fix. His approvals are direct: "Ding ding ding."

---

## Stage biomes are AUTHORED — do not "fix" them

Mike, 2026-08-17, asked directly about stages 1, 2 and 7: **"this is totally fine. I design the
stages this way."**

- **Stage 1 "RUMBLE IN THE JUNGLE"** opens on water and islands and becomes ORANGE DESERT for most
  of its length. Intended.
- **Stage 2 "IT'S HOT IN HERE"** is pale sand and tan rock nearly end to end, with only a couple of
  small lava vents. Intended — the heat builds, it is not a lava field.
- **Stage 7 "NOT ANOTHER SEWER LEVEL"** reads as green swamp with stone aqueducts. Intended.

A subtitle is not a promise about the whole stage. Do not repoint a master because the biome drifts
from the stage name — that is the design. **Stage 5 was different**: `storm800_rc2_master` was a
literal storm plate on a space stage, which Mike DID want changed. The test is whether the art is
wrong for the stage, not whether it matches the title.

## Current state (2026-08-18)

**0814c — items 6, 7 and 8.** Full writeup: `docs/PASSOVER_0814C.md`.

⚠ **ITEM 8: THE BOSS DEATH SET-PIECE WAS NEVER THE PROBLEM.** `updateBoss` runs 9.4s of blasts,
debris, shake and the whiteout for every boss on every stage. Only stage 1 had the other half — a
DRAW that gets out of the way. `shipBossDraw`, `mechDraw`, `sxDraw`, `genesisDraw` and
`drawModularBoss` have **no `b.dead` handling at all**. ⚠ **AND `drawBossSprite` ALONE HELD FOUR
COPIES OF THE FADE ON TWO CURVES** (1.8→2.6 and 2.6→4.1, charring 0.30 vs 0.26). One curve now
(`bossDeathAlpha`/`bossDeathChar`), applied at **`drawBoss`, the single entry point** — five rigs
that each remember to fade is five that can forget. `_bossFade` is published so the few draws that
hard-set `globalAlpha=1` can restore to the boss's base opacity instead of to solid.
⚠ **STAGE 8'S BOSS DID NOT FADE — IT CEASED TO EXIST.** Measured **zero drawImage calls on the
frame after it dies**. `drawBoss` gated the modular path on `!boss.dead`, and the 0724bx note four
lines above describes exactly that bug — the fix was applied to the `_ship` branch and **not to
the branch the note is about**. Stage 8 has no legacy plate, so it landed on the vector fallback.
⚠ **`hitBoss` CANNOT KILL A MODULAR BOSS** — `if(boss.modular){ modularHit(dmg); return; }`
returns before the `hp<=0 -> bossDie()` check. My probe killed bosses that way and reported stage
8 as refusing to die; it was the probe refusing to kill it. Force-kill is `boss.hp=0; bossDie();`.

⚠ **ITEM 6: `kind:'eshot'` IS IN NEITHER `FIRETYPES` NOR `PROJ`, AND IT IS WHAT EVERY SHIP BOSS
FIRES.** `_shipShot` is the muzzle for every pattern of every ship boss and mini (ember, lance,
void, siege, rime, mslfan, beamfan). Every round fell through the whole draw chain to the last
rung — and `ebullet` is not a registered key, so that is `circle(3.4)` + `circle(1.6)`: **two flat
vector circles**, one size, one colour, no animation, in a game holding 252 authored `mfx_` cells.
That is the whole of "awful", and it is **not a stage-2 problem** — stage 2 is where Mike met it.
Now `deriveFireType('eshot','pellet',{h:18})`: authored birth reel off `b.t`, and the family comes
from `PELLET_FAM[run.stage]`, so the round is **the colour Mike already chose for the stage**.
⚠ **`flare` WAS THE OBVIOUS PICK AND THE CONTACT SHEET DISQUALIFIED IT** — `mfx_ea_3_` frames 0-4
are a bead and 5-7 are thin streaks, so cycling it swings the shape (0811y's trap). Render first.

⚠ **ITEM 7 CORRECTS 0813x, AND IT CORRECTS THE SOLUTION, NOT THE DIAGNOSIS.** "Stage came sliding
in instead of the lava continuing." 0813x read Mike's "have that floor render back in by scrolling
downward" as wanting the TERRAIN back and slid the master into frame. **What he is pointing at is
that the lava STOPS**: `_bossHold` pins `mapScroll`, and the bed is drawn against it, so the lava
cycled its frames while travelling nowhere. `_arenaLavaScroll` is its own clock at `ARENA_LAVA_SPD`
(40px/s, the level's own rate). **The `_gen||_mech` gate goes with the slide** — the open lava is
the ARENA's requirement, not the unit's.

⚠ **THE SCROLL LIVES IN THE DRAW, NOT THE UPDATE.** `mapScroll` is advanced inside
`drawLevelMaster`, so a fixture looping bare `updatePlay` measures it as +0 and reports the level
as dead. Drive `drawWorld` too. ⚠ **AND `drawWorld` TAKES `dt` — CALLING IT BARE MAKES `mapScroll`
NaN**, silently and permanently (NaN propagates; the level just stops). `drawLevelMaster` refuses a
bad dt now, same as the `stateT` clamp. ⚠ **NaN COMPARES FALSE AGAINST EVERYTHING**, so the probe
printed "+nan px OK" — a probe that cannot fail on a broken number is not measuring one.

⚠ **TWO 0813x ASSERTIONS PINNED THE FIX MIKE OVERRULED**, both describing 0813x's solution rather
than the requirement. Repointed and made behavioural (the lava advances while the level does not).

**0814b — item 10: the right dialogue box was built inside a function nothing else could reach.**
Full writeup: `docs/PASSOVER_0814B.md`.

⚠ **0811m BUILT EXACTLY THE PANEL MIKE WANTS AND BUILT IT INSIDE `storyDraw`.** A hundred lines of
local code, unreachable, while `thawDraw` drew a `fillRect`+`strokeRect` box in canvas BOFmil with
a hand-rolled wrap and `freezerL3Draw` drew **no box at all**. Measured on the pre-drop tree: thaw
**0 panels / 16 faux rects / 32 canvas fillText / 0 BOF glyphs**; freezerL3 **0 and 0** — not even
a bad box. `dlgBox(o)` is that body lifted out unchanged; `storyDraw` is nine lines now.
⚠ **THERE ARE TWO LEGITIMATE DIALOGUE RENDERERS, NOT THREE** — `drawCommWindow` is the MODAL one
(it dims the whole screen) and `dlgBox` is the in-play one. 0811m's note says why; it is still the
reason.
⚠ **`freezerL3Draw` USED `setTransform(1,0,0,1,0,0)` TO ESCAPE THE CAMERA**, which also throws away
the 2x backing store — it rendered at half the size of every other glyph in the game. Undo the
camera by translating `camX`, never by resetting the transform.

⚠⚠ **THE COUNTERS WENT 4/4 GREEN ON A PICTURE THAT WAS WRONG THREE WAYS.** Rule 2, inside the probe
written to enforce rule 2. All three were invisible to "authored panel + authored face + no faux
rect" and obvious in the saved frame:
  1. **the text ran off its rail** — 196x96 was sized for canvas BOFmil; the BOF face is far wider,
     and the portrait bay left a 96px column. Now every line is re-measured with `msgMeasure` at
     the height it was drawn at, against the rect `drawPanel` was HANDED.
  2. **two panels stacked** — `thawStart` fires from `beginStage(3)` for everyone and
     `freezerL3Begin` fires on the same stage for Freezer. Invisible while both were small faux
     boxes in different corners. The narration QUEUES now; the probe counts distinct panel rects.
  3. **bottom-right is spoken for** — the panel ran UNDER the EQUIPPED box, which draws after it:
     `SHOW TH`, `FEEL`, tails hidden rather than missing. ⚠ **THE OVERRUN CHECK SAID 0 AND WAS
     RIGHT — occlusion is not overrun**, and only the picture distinguishes them. 0806d's
     bottom-right was correct for a 196px box; `nequipbox` did not exist until 0812p.
⚠ **AND THE LAST ROW SAT ON THE BOTTOM RAIL** — the draw tested a row's TOP and drew its full height
below it. **Fixing that meant fixing the SOLVER in the same breath**: it counted row TOPS while the
drawer required the FOOT to clear, so it would have believed in a row the drawer refused and the
tail would have vanished silently — 0811m's truncation bug by a new route. `rowsFit(h)` is one
definition used by both.
⚠ **A FIX THAT ADDS ORDERING BREAKS EVERY TEST THAT ASSUMED THERE WAS NONE** — after the queue, the
freezerL3 probe case measured zero panels and read as a regression. It was the queue working; the
case drives the real sequence now.
⚠ **AN ASSERTION PINNED A STRING LITERAL, NOT THE RULE** — "the pilot beat uses the smiling
portrait" was `indexOf("'port_'+thaw.pk+'_smile'")`, so asking `pilotPortrait(pk,'smile')` instead
failed it on code where the pilot beat still uses the smiling portrait. Behavioural now: it wraps
`pilotPortrait` and records what the draw asks for (`yuri/smile`).
⚠ **THE PROBE WAS RUN AGAINST THE PRE-DROP TREE AND FAILED 3 OF 4.** A probe that has only ever
been green is not evidence. The fourth is the control.

⚠ **OPEN, FOUND NOT FIXED: THE APOSTROPHE RENDERS AS A COMMA** — "THEN LET,S SHOW THEM" in the proof
frame. The glyph RESOLVES (`sfont1_p39`/`sfont3_p39` are registered), so this is not the missing-
punctuation case `fontGlyph` handles. `glyphBox` bottom-aligns EVERY glyph in the cap box, and an
apostrophe is a TOP-hanging mark — 0809q added `FONT_DESC` for glyphs that hang BELOW the baseline
and there is no counterpart for ones that hang ABOVE it. ⚠ **DO NOT WRITE THAT TABLE FROM THE
ARGUMENT.** Rendered, `p39` and `p44` are both chunky carved slabs and which way up each is meant
to sit is not readable off the plates. Settle it with one render: `'` and `,` through
`msgTextLeft` at dialogue size beside a `.`, with and without a `dy=0` override.

**0814a — Mike's items 1, 2 and 3 are ONE defect, and it is now closed.** Full writeup:
`docs/PASSOVER_0814A.md`.

⚠ **THE VARIANT A PILOT IS HOLDING WAS NEVER RECORDED ANYWHERE.** `weaponVariant(w, opt)` answers
"what should the next crate dispense" — it reads the stage, and for Freezer's flame slot it calls
`Math.random()`. **Every runtime surface was asking it "what am I holding?"** The pickup's variant
IS baked at spawn (`spawnContainer` -> `wvar`); `applyPowerup` read it for the announce banner and
**threw it away**. `heldVariant(w)` / `run.wvars[]` is the missing half. `weaponVariant` is the
FALLBACK now, for a slot granted with no pickup behind it.
⚠ **"KEEP SWAPPING ICONS" WAS `drawPowerups` CALLING `weaponIconKey` WITH NO OPT, ONCE PER FRAME**
— re-rolling `Math.random()` at 60Hz, so a falling crate really did alternate between the
flamethrower and ice breath icons. **The comment above `WVAR_NAME` predicted this exact failure
and no call site honoured it.** A warning in a comment is not a mechanism.
⚠ **"FIRE RANDOMLY ONE OR THE OTHER" WAS `orbIsFire()` BEING `run.stage===3`** — the same orb was
fire on 3 and ice on 4, icon/element/ball/shards all flipping at a stage boundary with no pickup
involved. It reads the held variant now; `ORB_FIRE_ON_L3` is enforced where it belongs, in what
the level DISPENSES.
⚠ **FLAMETHROWER AND ICE BREATH ARE SEPARATE ATTACKS.** `flameIsIce()` was `_pilotKey()==='freezer'`
unconditionally. Every flame-gated site routes through that ONE function now. Ice breath is
exclusive to Freezer, from stage 2 (proved exhaustively: 9 stages x 8 pilots x 200 rolls).
**Stage 3 no longer returns `null` for the slot** — that withheld his flamethrower too, and stage 3
is where `freezerL3Begin` hands him one off the magma mech as an authored beat that had been
coming out as frost against its own narration.
⚠ **`nts_` IS A COMPLETE THERMOSHOCK WEAPON — 45 KEYS, ZERO REFERENCES.** A 12-frame split
fire/ice ball, **four flame shard plates and four frost ones**, an 8-point burst star that IS
0801fj's eight-way discharge, a charge reel, a release ring, an impact. "fireiceorb fires a basic
fireorb" was literal: the weapon had an icon, a name and a table row and **no projectile**.
⚠ **TEST THE FIREICE CASE BEFORE THE FIRE ONE IN `drawBullets`** — `orbIsFire()` is true for
fireice too (it IS half fire), so it would otherwise fall into the fireball's art.
⚠ **12 FRAMES, NOT 8** on `nts_orb_`. `TS_REEL_N` carries every reel's length; `%8` silently drops
a third of it and reads as a stutter.
⚠ **THE ORB AND ITS SHARDS HAVE NEVER TAKEN THE ELEMENTAL BONUS.** `attackElement` has answered
for `'orb'`/`'shard'` since 0801fn and **nothing ever asked it** — `elementMultiplier`'s only call
sites were the fireball and the flame. Mike's "all fireattacks do 2x to ice enemies" has never
applied to the weapon it was written for. Now baked onto the projectile at spawn (the shards fall
through the GENERIC collide, which knows nothing about elements). **This raises orb damage on
stages 2 and 3 — a declared rule firing, but Mike should see it.** Thermoshock at 2x on both is
MY call, not his.
⚠ **THE 0810a PARTICLE LEAK IS BACK IN `assets/game.js`, IN THESE SAME TWO WEAPONS.** The expiry
test sat at the BOTTOM of the particle loop, after the `_fbDecal` and `_iceChip` branches, and
both draw and `continue` — so neither was ever marked dead. `FIRE_ICE_FIX.md` records this as
fixed; it crossed to `gamecode.js` and not to the authoritative file. **A fix recorded as landed
is not a fix observed landing.** Test is at the top now; all three kinds drain to 0.
⚠ **AN ASSERTION FAILED AND WAS DEFENDING A LIMITATION, NOT A RULE** — "the flame slot cannot DROP
for Freezer on stage 3" pinned `weaponVariant(4)===null`, which was the only way to withhold ice
breath while it and the flamethrower were one weapon. Repointed onto Mike's actual words.
⚠ **THE SUITE BASELINE WAS RUN, NOT ASSUMED** — a clean `git worktree` at HEAD: **2,659/5/2,664**
against this drop's **2,660/5/2,665**. The first run came back 2,658/6 with the total unchanged,
so the delta was one assertion and findable in one line. Rule 3's COUNT check only works if you
know what the count was.

**New tools.** `_BUILD_SOURCE/probe_scope_0814a.js` answers **"is this identifier actually global,
or did `spawnEnemy`'s unclosed `if` swallow it?"** by asking the engine instead of the source —
CLAUDE.md records that brace-matching and line-bounding both give wrong answers there. It
correctly identifies `liveType` as swallowed. ⚠ **It also reports `ARSENAL_DRONES` as GLOBAL,
contradicting the note below — re-measure that rather than quoting it.**
⚠ **`updateBullets` IS NOT A NAME IN THIS ENGINE** — the player-bullet loop is inline in
`updatePlay`, so a bullet test needs a live stage under it.

⚠ **AND THE PIXEL PROBE'S FIRST CUT MEASURED THE LEVEL, NOT THE WEAPON.** It classified every lit
pixel in a 180x230 band and reported **143,194 warm pixels with the ICE BREATH equipped**, failing
on correct code — the stage-2 desert. **153,866 "lit" pixels in a 165,600-pixel band is the tell.**
The fix is not a better threshold: **the claim is about the ART, so sample the PLATE the draw path
asked for, alpha-masked.** Now flamethrower 60.2% warm / 0.0% cold, ice breath 0.0/79.3, fire orb
97.3/0.0, ice orb 0.3/58.5, **fire-ice 42.8 AND 28.7**.
⚠ **A QUANTITY THAT IS CONSUMED CANNOT BE MEASURED AFTER IT IS GONE** — the ray test flew the ball
200 frames then read `pBullets`, which is correctly EMPTY by then, and called that "no rays
fired". Accumulate as they appear.

**0813x — the stage-2 boss floor, and a spawn offset measured from a moving edge.** Two of Mike's
reports; both measured in pixels. Full writeup: `docs/PASSOVER_0813X.md`.

⚠ **`arenaLiquid` DOES NOT PUT THE FLOOR BEHIND THE LAVA — IT STOPS THE FLOOR BEING DRAWN.** The bed
is painted UNDER the master (0801dp), so returning before the master blit leaves the lava that was
always underneath as the only thing on screen. Nothing occludes it; nothing draws it.
⚠ **IT WAS AUTHORED IN 0806f FOR THE MAGMA COLOSSUS, WHO RISES OUT OF THE LAVA** and needs an open
surface to break. 0810q/0810s scrapped him; stage 2 fields the INFERNO REAVER, a gunship that never
touches the ground, and **the flag stayed on the STAGE**. Now gated on the boss carrying `_gen` or
`_mech`. The cfg flag is untouched, so re-casting the Colossus anywhere restores the corridor.
⚠ **SAME SHAPE AS THE 0810m SPLIT LOGGED BESIDE IT** — one flag standing in for a unit's requirement,
left pointing at whatever unit arrives next. 0810m caught the miniboss half; the replaced-boss half
survived because its symptom is only an absence, not a teleport.
⚠ **THE FLOOR NOW TRAVELS BACK DOWN INTO FRAME** (Mike's call): open lava for `ARENA_FLOOR_HOLD`
(1.1s) while the boss arrives, then a smoothstep down over `ARENA_FLOOR_IN` (1.6s), then the held
level. Downward is the level's own direction, so it reads as the level catching up, not a wipe.
⚠ **DELETING THE EARLY RETURN IS THE WRONG FIX** — it drops stage 2 into `_loopDraw`, which is
0810m's teleport. **`_loopDraw` is still the boss backdrop on stages 1/3/4/6/8 — unmeasured, its
own drop.**
⚠ **`_masterSrcY` CARRIES `srcY - _floorDy`** so the blit and the props share ONE number; an offset
only the blit knew about would re-open 0813c exactly. **`_arenaFloorT` is ABOVE `spawnEnemy`** or
its unclosed `if` would make it per-spawn state and restart the slide on every wave.

⚠ **THE SPAWN OFFSET WAS STATIC; THE EDGE IT WAS MEASURED FROM WAS NOT.** `offLeftX`/`offRightX`
returned constants — in WORLD space — while `drawWorld` runs under `translate(-camX)` with camX
following the player. Measured stage 1: **left runway 6px vs right 326px, a 54x swing from nothing
but the player's x**, always collapsing on the side the player stands on. Now anchored to
`camLeftX()`/`camRightX()` with `ENTRY_CLEAR` (64) as the guaranteed screen runway: **64px both
sides at camX 0/160/320, at w=95 and w=29.**
⚠ **EVERY STAGE IS 800 WIDE WITH camX 0..320 — MEASURED, ALL EIGHT.** The "wide stages are 1, 5 and
6" line below predates the stacked art pack and is **STALE**. That staleness is why this was only
ever hunted on stage 1.
⚠ **THIS IS WHY EVERY POP-IN PROBE PASSED IT** — the camera window is a strict subset of the world,
so outside-the-world is always outside-the-camera. **The fault was the SIZE of the runway, not its
sign, and only a screen-space measurement sees it.**
⚠ **A HALF-MIGRATED COORDINATE SYSTEM IS WORSE THAN EITHER WHOLE ONE** — helpers on the camera with
the clamp's trigger still on the world edge measured **−19px**, i.e. hull on screen at spawn.
⚠ **`inPlace` IS NOW EXEMPT EXPLICITLY**; guarded at 240 / 700 / inPlace-500, all moved=0.
⚠ **IT ONLY HELPS UNITS THAT MOVE HORIZONTALLY.** A traced bare `s1jetDelta` sat at −6px for 24
frames. **If pop-ins persist, that and the `_edgeM = w*0.66` pin (0811o/0811t, untouched) are next.**

⚠ **THIS DROP WAS FIRST WRITTEN AGAINST AN 0813g ZIP WHILE TRUNK WAS AT 0813w** and was nearly
copied over wholesale, which would have erased sixteen drops. **Check the remote's HEAD before
writing a line, not before pushing** — `git ls-remote` plus one `git log -1` is the whole cost. The
first pass also labelled itself 0813h/i/j, all three of which already existed on trunk as different
work: **a drop letter is not a private namespace.**
⚠ **NO `node` ON THAT MACHINE — headless Edge ran both the parse check and the real game.** See
§9 of the passover for the exact invocation and its three traps. **The suite was NOT run**, and the
0806f-era §180 assertions are expected to FAIL: they pin the exact line this drop replaces. Read
them before fixing them.

**0813g — MAGMA VENT is stage 2's miniboss; the roster said 40px, the ART is 223px.**
⚠ **`lavamaw` READS AS w:40,h:38 IN THE VOLC ROSTER AND ITS ART IS 223x220** (`nvl_maw_0..5`, six
frames). The stage was shrinking a miniboss-sized caldera to a speck. At 196x194 it is scaled DOWN.
⚠ **`spawnEnemy('lavamaw')` RETURNING NOTHING PREDATES THIS** — it is in `_DELETE` from 0801ip, and
that note says the ART was kept on purpose. Check whether a behaviour is yours before owning it.
⚠ **`spawnSubBoss__inner` VALIDATES NOTHING** — any string builds a generic 130x120 sub-boss with no
art. Eight candidates at identical w/h all drawing a red box is the FALLBACK, not a roster.
⚠ Two assertions pinned siege ember; Mike overruled it, so they now track his choice.

**0813e — level 7's purple halos are black edges; stage 5's MAP NODE is a volcano.**
⚠ **`BOFFI` RECTS ARE `[sheetIndex, x, y, w, h]` — FIVE elements.** Reading them as `[x,y,w,h]` made
every rect `None` and the halo script edited nothing — which SAVED it, because `nca_74.png` is shared
and a wrong rect corrupts art well outside level 7. Cell-bounded, alias-deduped, `.bak` per sheet.
1,577px converted (`nsw_circ/ring/dist/distr`, the level-7 shock effects). Alpha untouched.
⚠ **INTERIOR magenta is NOT a halo** — `nsw_barge_0`/`nsw_sentry_0` keep theirs; so do the RC2
masters, whose magenta is punched to alpha for the sludge. Only OUTER-BOUNDARY pixels convert.
⚠ **`nsw_combined` (598px) is UNUSED** — 0 references; its halo cannot reach the screen.
⚠ **STAGE 5'S MAP REGION IS THE "CENTRAL CITADEL — EMBER RISE"** (game.js:32843) but the level is
`bg:'space'` / voidbat / orbital. The ring layout and index mapping are both sound; the mismatch is
thematic and is MIKE'S map-design call. The map plate would not resolve, so polys were plotted on a
blank field — do not move one off that alone.

**0813d — the tanks were displaced from OUTSIDE their own pattern, and only 3 of 8 stages have new bosses.**
⚠ **`enemyEntrySweep` (updatePlay:14580) MOVED THE TANKS, NOT `tankpatrol`.** A setter trap on a
roadtank's `x` caught all 62 lateral writes coming from there — the pattern case moved them zero.
Removing the obvious lane-drift block inside `tankpatrol` first changed the numbers WITHOUT stopping
the slide, which is the tell. Same shape as the standing jet-displacement note. Now gated on
`_vkind==='tank'`. Residual: one unit still shows ~2px steps, not chased.
⚠ **WHEN A "FIX" CHANGES THE NUMBER BUT NOT THE BEHAVIOUR, IT IS NOT THE CAUSE.** Trap the write.
⚠ **ONLY STAGES 2/3/5 RUN `nsb_*` BOSSES** (item 5). Stages 1/4/6/7/8 still draw legacy art via
`spawnBoss`'s switch (`damkeeper` → `ovbody_intact`). FIVE unassigned new-pack bosses exist —
blacksteel, jungle_cruiser, olive_carrier, siege_ember, thorn_rime — all resolving, none wired.
The stage mapping is MIKE'S call; not guessed.
⚠ **`probe_bossart.py`'s "8 minibosses have no art key" IS A PROBE FAULT** — `SUBBOSS` is keyed by
stage number and stores art under another field. That audit is unfinished; do not quote it.

**0813c — stage 5 is space now, and the roadside signs were scrolling the WRONG WAY.**
⚠ **`storm800_rc2_master` IS A STORM PLATE.** Stage 5's master was cloud, rain and lightning for
essentially all 5120px, with ONE orbital band at ~45% — sample that band alone and it looks like
space, which is how it survived. Stage 5 now loops `norb5_arena` (its own orbital art, measured dark
and seamless: first row vs last differs 12.5/765) via the new `loopMaster` flag.
⚠ **GROUND PROPS AND THE GROUND USED DIFFERENT MAPPINGS.** Terrain shows rows `[srcY, srcY+VH]` with
srcY DECREASING, so features travel DOWN; `drawRoadSigns`/`drawStageProps` used `y - mapScroll`,
which travels UP. Measured: crater down 105px while the sign moved up 105px. `drawLevelMaster` now
publishes `_masterSrcY` and both prop draws read it. The 0810h note saying they "already stay put"
compared the two PROPS to each other and never to the terrain.
⚠ **`XART.rdy()` AND UNDECODED MASTERS FAKED THREE "NO BUG HERE" RESULTS** before this was measured —
and one probe printed a PASS having measured zero stages. Check that a probe measured something.
⚠ **THERE IS NO BRIDGE ASSET** (item 3): `cfg.props` holds exactly ONE prop game-wide,
`nst4_crash_overlay`, an 800x600 pileup drawn 1:1 — the crash object Mike approved. Not deleted.

**0813b — the levels were bilinear-doubled EVERY FRAME, and that is why they looked upscaled.**
⚠ **`ctx.imageSmoothingEnabled=true` sat on the FRAME SETUP** (game.js:37729), so it overwrote the
init default before the first backdrop ever drew. `SS=2` puts the 800-wide masters on a 1600px
backing, so a high-quality bilinear DOUBLE invented a pixel between every authored pair. The
`drawLevelMaster` geometry was innocent — it draws 1:1 (`drawW→drawW`, `winH=VH`).
⚠ **AND `image-rendering:auto` BLURRED IT AGAIN** on the way to the display (index.html:36).
⚠ **THIS IS WHY A DOZEN DRAWS SET THE FLAG LOCALLY.** Sprites opted out; backdrops never did, so the
art split into crisp sprites over soft levels. Those local `=false` lines are now redundant.
⚠ **CHANGING THE INIT LINE ALONE DOES NOTHING** — measure the flag at runtime, not the edit.
Measured: stage 1 backdrop crop 21,423 colours → 13,927, and 192/192 2px column pairs uniform.
`_BUILD_SOURCE/probe_sharp.py`.
⚠ **NINE ITEMS FROM MIKE'S 0813B MESSAGE ARE STILL OPEN** — see the tail of `PASSOVER_0813B.md`
(stage-5 sky vs space, scrolling signs, the highway bridge, sideways tanks, un-replaced
bosses/minibosses, level-7 purple halos, wrong level-5 map region, background squares on space/sky,
stage-8 chain lightning). The stage-6 "door/side sky overlay" he ordered deleted was **not** deleted:
the obvious key renders as a flat blue noise field, not an overlay. Rule 1, third save.

**→ START HERE: `docs/HANDOFF_BRIAN_0814.md` (the current patch notes), then
`docs/PASSOVER_0814C.md`, `docs/PASSOVER_0814B.md`, `docs/PASSOVER_0814A.md`, then `docs/PASSOVER_0813G.md`, then `0813E`, `0813D`, `0813C`, `0813B`, `0813A`, then `0812G`, then `0812F`, `0812E`, `0812D`, `0812C`, `0812B`, `0812A`, `0811Z`, `0811Y`, `0811X`, `0811W`, `0811V`, `0811U`, `0811T`, `0811S`, `0811R`, `0811Q`, `0811P`, `0811O`, `0811N`, `0811M`, `0811L`, then `docs/PASSOVER_0811_HANDOFF.md`.**

**0813a — the flamethrower now hits what it visibly touches.**
⚠ **`flameDraw` PAINTS A UNIFORM COLUMN; `flameHit` TAPERED.** The draw is `flameHalfW(lv,1)` wide
for the plume's whole length; the hit test evaluated `flameHalfW` at the travel fraction, which
narrows to `flameBase` at the nozzle — **96px drawn against 35px tested at lv5**. An enemy inside
the visible fire beside the ship took nothing, and because the taper is invisible art-side it read
as a damage bug, not a width one.
⚠ **AND THE PLUME IS ANCHORED AT THE NOZZLE, NOT THE TIP.** `f.bot` is the emitter (at the ship);
`f.top` is the far tip. `ICE_H` shortened the ice reel by holding `f.top` and pulling the BOTTOM up
— shortening it *at the ship*, so the frost floated 27px clear of its own nozzle. Anchor at `f.bot`
and the TIP pulls back. Fire is bit-identical (`dh===reach`).
The shape is now in one place — `FLAME_ICE_W/H`, `flameHalfWDrawn`, `flameSpanTop` — and
`flameDraw` reads its scale from those, so the two cannot drift apart again.
Also: stage 2 fired **red pellets on the lava stage** via `PELLET_FAM[2]=0` (`#ff6b5a`) — not the
boss, the stage table; the reaver's charged **fire orb** (homes far, commits inside 96px, never
re-acquires); wobble + shootable rockets under the rake; the missile-lock **beep removed**; the
save menu gated on the map actually being reached.

**0812g — the muzzle flash now matches the round it fires, all 8 tiers, both weapons.**
⚠ **THE FLASH WAS CLAMPED TO FIVE TIERS** (`_mgMuzLv=min(5,lv)` at all five assignment sites), so
after 0812d gave the ROUNDS eight colours the gun lit one colour and the bullet left in another.
⚠ **AND IT RAN ON THE WALL CLOCK** — `(performance.now()/45|0)%6` on a 0.07s one-shot, so which of
four authored frames you saw depended on when you pulled the trigger. Now a one-shot off
`_mgMuzT`, exactly the correction 0811y made to the pellet.
⚠ **`node --check` CANNOT CATCH WHAT NEARLY SHIPPED HERE.** I inserted the block between the two
legacy branches, leaving `let _p87muz` declared AFTER a branch that reads it — a temporal-dead-zone
ReferenceError on every spread shot, syntax-clean. Runtime probe or nothing.
⚠ **AND IT MUST NOT EARLY-RETURN** — Cole's Aegis aura and the orbit orbs draw after it, so a
`return` deletes them whenever the gun is lit. It sets a flag; both legacy branches gate on it.
⚠ **TIER 8 DOES NOT FIRE THE MACHINE GUN AT ALL** — `coleTier()>=8` returns immediately, the fusion
cannon replaces it. Asking tier 8 for a muzzle level reads the previous shot's value.

**0812f — the boss art was unwarmed too, and the whole NEWBOSS table is dead.**
⚠ Audited all eight bosses the way 0812c audited the minis. `addPrefix('infernoreaver')` cannot
match `nsb_inferno_reaver`, so **stages 2 and 3 opened their boss fight on the hull silhouette**.
warmStage is table-driven now: any ship boss warms its own hull key, any NEWBOSS stage its idle
reel, any ship mini its hull — so a boss added later is covered by existing code.
⚠ **ALL FOUR `NEWBOSS` ENTRIES POINT AT UNREGISTERED ART** (`chopper_`, `fboss_`, `iboss_`,
`tankboss_` — absent from every namespace). `_hasNewBoss` can therefore NEVER be true and every
stage falls through; stage 1 draws the LEGACY helicopter sprite, which is what you actually see.
§221 pins that as STATE — it fails the day the art is registered, which is the reminder to finish
the wiring or delete the branch.

**0812e — the JUNGLE CRUISER is stage 1's miniboss; the quad-laser is unassigned, not deleted.**
⚠ **THE SOURCE FOLDER AND THE BUILD DISAGREE, AND THE SOURCE IS THE WRONG ONE TO READ.**
`_ART_SOURCES/BOF2_South_Facing_Ships_v1/` frames are the UN-recoloured originals; the imported
plates measure ember-red on 2, rime-teal on 3, gunmetal on 4 — every one matching its stage. All
six hulls are in use (3 minis, 3 bosses). "Filenames lie" extends to source folders.
⚠ **STAGE 6 FIELDED A UNIT LITERALLY NAMED "SUB-BOSS"** — `SUBBOSS[6]` said `'ss'` and the spawn
switch had NO arm for it, so it took the generic 130x120 default: no art, no profile, stock HP.
Nothing failed and nothing logged. Now the STORM LANCE. §220 asserts every stage names its mini.
⚠ **`shipBossDraw` NOW TAKES A `pal`** — palette-swapped hulls via `xartPalette` (cached per
key+mode, one canvas per run). A `pal` hull must ALSO warm its SOURCE key or it opens the fight on
the silhouette fallback — the 0812c bug via a new unit. §220 asserts that too.
⚠ **NINE ASSERTIONS FAILED ON A ONE-WORD CHANGE THAT BROKE NOTHING** — they tested the quad-laser
by asking what stage 1 happens to field. Test a unit BY KIND; couple to the stage only when the
claim is about the stage.

**0812d — the nca_87 pack is now the machine gun and the spread, all 8 tiers.**
⚠ **nca_87 IS NOT SLICED** — one whole-sheet key, no cell keys exist. The 4x4 / 192-pitch grid was
measured off its own alpha and is indexed directly (no manifest edit: the manifest is generated).
Rows: 0 muzzle flash · 1 round in flight · 2 impact · 3 straight + two authored diagonals + flash.
⚠ **ROW 1 IS THE 0811y TRAP AGAIN** — 50px wide at frame 0 vs 26px at frame 2, a 92% swing. Driven
MONOTONICALLY off `b.t`, holding on the last frame. Never the wall clock, never a loop.
⚠ **THE DIAGONALS ARE AUTHORED AT ±46.2°, NOT 45** — spread picks the nearest pose and rotates by
the RESIDUAL only, the idiom `nhxv_` already set.
⚠ **NEW ART MUST GO FIRST IN `drawBullets`** — both arms are chains of five `continue` fallbacks,
and drop 0720 lost an entire pack to exactly that. §219 asserts the ORDER.
⚠ **WHITE AND BLACK MUST NOT USE THE HUE SWAP** — `xartPalette`'s default `'color'` composite takes
hue from the fill, and achromatic fills have none, so both come out the same grey. It carries a
`multiply` path for black and a colour+`screen` path for white; tiers 3 and 4 need them.
⚠ **ONE SHADOWED DRAW IS NOT A GLOW** — measured every tier's halo at 14..26 of 255, present but
invisible, and tier 8's purple read BLUE under the round's own casing. The halo is its own pass now.
Tier 8's BODY is my choice (authored gold), not Mike's — he specified bodies for 1-7 only.

**0812c — the miniboss "hitbox square" is an UNWARMED HULL, on three stages.**
⚠ **A KIND NAME IS NOT AN ART PREFIX.** `warmStage` warmed `addPrefix(SUBBOSS[n].kind)` —
`'siegeember'` — while the hull key is `'nsb_siege_ember'`, so stages 2/3/4 opened their miniboss
fight on the placeholder and swapped to the real ship a second later. Stage 1 only looked fine
because 0801kd warms `'nqx_'` explicitly. `_PACKOF` now maps the three hulls and the Herald's reel.
⚠ **AND BOTH OF MY FIRST TWO ANSWERS WERE PROBE ARTEFACTS** — `XART.rdy()` is false on its first
call *because it starts the decode*, so spawning and screenshotting in one synchronous block
photographs the placeholder; and a "boxy" test based on equal row extents also fires on any sprite
larger than the scan window. **Open the PNG.**
⚠ The Herald's `mba_vr_*` plates are **not in `XART._src` at all** — routed around, not resolved.

**0812b — six art files were MISSING FROM THE WORKING TREE, deleted and never committed:**
`logo.png` and `stage1..5.png`. Restored with `git checkout --`.
⚠ **CHECK `git status` FOR ` D ` LINES BEFORE TRUSTING A 404 OR A SUITE COUNT.** This cost two boot
404s whose paths `grep` could not find (they are built at runtime from the manifest, which was
right), **eight extra suite failures** (5 → 13; nine assertions across four sections exist to catch
exactly this), and every `%` on the stats screen — `%` lives in ONE sheet in the build and that
sheet is `stage2.png`. The zip Mike already sent predates the deletion and is intact; checked.
CLAUDE.md's "two 404s at boot" is now fully closed: one was the font path (0811z), the other two
were these. Only `assets/data/ui_layout.json` still 404s, and it is optional and guarded.

⚠ **`stageText`'s third argument is named `cx` and IS THE CENTRE** (`let x = cx - total/2`).
Three stats-screen call sites passed a column EDGE as that centre: the row labels, SCORE and its
digits, and PASSWORD. So the long labels grew 60px LEFT over the portrait column — **nothing moved
into the portrait**, which is why "the rank collides with the rows" had no cause where it appeared
to. The row VALUES were already correct (`right - width/2`); that mismatch of two rules IS the
tester's "label column and value column disagree". Measure with `_tw`/`_twMix` and offset by half.
⚠ **The password is the one value that must NOT be right-aligned** — `shown` is a growing prefix,
so a pinned right edge types backwards. Left-anchored, anchor measured from the FULL password.

**Mouse: all 13 menu screens now take a pointer** (`§217` asserts it). Stage select could not use
`menuMouseList` — the flags are at authored map coords, hit-tested through the same
`S=0.75 / MX=0 / MY=64` transform the draw loop uses. ⚠ **Two-stage: click a flag to SELECT, click
the selected one to DEPLOY.** One click doing both launches a level you were only pointing at.

**0812a — the beta tester's input list.** Mouse buttons are bindable now: they go into the same
`keys` map as `pad_b0..15`, so `down()`/`tap()`/`tapAny()` and the rebind screen all understand a
click with no special case. Defaults ADDED (not substituted): fire `j,mouse0,…`, bomb `k,mouse2,…`,
retina `c,space,…`.
⚠ **`setk` IS LOCAL TO `pollGamepad`** — my first cut called it from the event handlers and would
have thrown a ReferenceError on every click. Mirror the keyboard's own two lines instead.
⚠ **Mouse binds are FILTERED OUT of `menuConfirm`** — it reads `tapAny(keybind.fire)`, so `mouse0`
would make any click both activate the button under the cursor and confirm the highlighted row.
⚠ Right-click needs `contextmenu` suppressed on the canvas or the browser menu covers the playfield.

⚠ **THE MOUSE DIES ONE SCREEN INTO THE GAME.** Audited every menu:
**mouse OK** — title, difficulty, pilot, password, options, game over, continue.
**KEYBOARD ONLY** — mode select, campaign hub, stage select, credits, stage clear.
TITLE takes the mouse and MODE SELECT, the very next screen, was dead. Fixed there; the other four
remain.

⚠ **THE OPTIONS ARROWS: THE CLIP WAS WRONG, NOT THE POSITION.** `ww/2-46` put the left arrow at
`wx+30` over labels drawn at `wx+16` ("MASTER" → "▶ER") and the right one inside the key button's
span, which is drawn after it. 0801bp had pulled them inward because at `ww/2-10` the panel clip
`rect(wx,wy,ww,wh)` cut them to slivers — that clip only ever needed to be tight VERTICALLY. Opened
26px each side; `ww/2-4` now puts them outside the frame.

**0811y — THE MACHINE GUN PELLET WAS SWAPPING A BLOB FOR A STREAK, 7× A SECOND.**
⚠ **0811v's wobble fix did NOT cover these** — it repaired the arsenal branch, gated
`if(b._boss …)`, i.e. boss bullets only. Pellets from planes/ships/jets take the FIRETYPES path.
Two different bugs wearing one description.

The picker was `['mfx_mg_2_0','mfx_mg_2_2'][floor(performance.now()/70)%2]`. Those are not two
poses of one thing: **18x20 ink 123 (a blob) against 20x45 ink 380 (a streak), +209%**.
`mfx_mg_<fam>_0..4` is a BIRTH SEQUENCE, and at a fixed draw height of 16 that toggle swung the
round's on-screen width between ~14px and ~7px in flight. Now driven from `b.t`: `000111222333444…`,
monotonic, holds on the tracer.
⚠ **AND IT WAS THE ONLY FIRETYPE USING THE WALL CLOCK** — comet, homing and missile all already
animate off `b.t`, so two pellets fired a frame apart were in step with each other and out of step
with their own flight.

⚠ **FIVE PELLET COLOUR FAMILIES WERE AUTHORED AND FOUR HAD NEVER BEEN DRAWN** — `mfx_mg_0..4` are
red/blue/orange/green/white, 25 plates, of which the game used TWO. No palette swap was needed;
`PELLET_FAM` just points each stage at its own. `T.glow` may be a function now so the halo follows
the plate. **Worth auditing `mfx_ea_`/`mfx_hom_`/`mfx_emr_` for the same two faults** — both were
invisible until someone rendered the reel.

**0811x — the laser, done properly after 0811w failed at it.** The failure was METHOD: 0811w added
tiered light additively with **no live baseline**. With a baseline taken first, two faults were
obvious and were nothing to do with tiering — **level 4 was pure white** (`#ffffff` over `#ffffff`,
reading as a hole in the screen over blue water) and **level 3 a pale mint** (`#5fe07a`, receding
where the others pop). Swapped via **`xartPalette(key, hex)`**, which composites with `'color'` —
hue/sat from the fill, **luminosity from the plate** — so the authored shading and the 6-frame
animation survive. Level 3 → `#25c94a`, level 4 → `#ffc21a` gold. `col`/`glow` moved with them or
the muzzle would have clashed with its own beam. Set now reads orange → blue → green → gold → red.
⚠ **ONLY THE TWO THAT MEASURE WEAK WERE TOUCHED** — swapping all five would be redesigning Mike's
weapon rather than fixing what he pointed at.

⚠ **TWO PROBE FAULTS INVENTED GAME BUGS.** "Levels 1 and 2 do not draw" was `player.fireCd` carrying
between tiers on one page, so `pShoot` early-returned. And the crop framed the wrong column because
it used the beam's WORLD x against a SCREEN-space canvas — the world-vs-screen fault this file
records for the launch seam, the outbound routes and the dialogue window, now a fourth time and the
first inside a probe. **`xartPalette` is now proven on a moving, animated, per-frame sprite**, which
is the hard case for the rest of the projectile palette work.

**0811w — the laser. One real fix; the visual upgrade FAILED and is reverted.**
⚠ **THE LIVE LASER HAS BEEN FIRING OUT OF NOTHING.** The v2.2 branch asks for `nlz_<lv>_m0..5` and
the manifest holds **ZERO at all five levels**, while the legacy muzzle orb was gated off whenever
the v2.2 beam was live. Orb ungated — existing authored code, only ever needed to be allowed to run.

⚠ **THE FIVE BEAM PLATES ARE THE SAME PICTURE IN FIVE HUES** — all 64x320, ink 57–62%, core width
59–63%, luminance 157–189. **The art cannot carry a tier progression.** Level 3 is a flat poster
green with almost no lit centre (why Mike singled it out); level 4 reads dirty grey. What the laser
needs is ART with per-tier internal contrast, not draw tuning.

⚠ **THE WIDTH ALREADY GROWS** — `beam.w = 14+lv*4`, 18px to 34px, driving the hit column too. My
first probe drew every tier at a constant 14 and I nearly rebuilt a progression that works. **A
probe that invents its own scale is not showing the game.**

⚠ **MY DRAW-SIDE TIERING WASHED THE SCREEN WHITE, TWICE, AND IS REVERTED.** Additive layers compound
far faster than their alphas suggest — three `lighter` passes over a plate that carries its own
light, plus the pulse blobs already there, saturate long before any one layer looks strong. **And I
had no baseline: I rendered the ART before changing anything but never the LIVE beam.**

⚠ **FRAME-DIFFING TO SIZE THE BEAM DOES NOT WORK HERE AND I KNEW THAT.** With/without diff reported
~475px lit at every tier — the whole row — because `drawWorld` reads `performance.now()` directly.
Documented in 0811m, by me, and walked into again. Use the crop; quote `beam.w`, which is read off
the object rather than inferred from pixels.

**0811v — THE PROJECTILE WOBBLE IS A 48° SPRITE FLIP, and 0811p's "closed" was premature.** The
arsenal/boss bullet branch rotated by `Math.atan2(b.vx, -b.vy)` under a ±0.42 clamp. Negating vy
puts straight-down at **±π** — exactly where every bullet in a vertical shmup lives — so **every**
value of vx clamps to ±0.42: a straight round is drawn permanently tilted **24°** carrying no
heading information, and the instant vx crosses zero the sprite snaps **48.1°**. `atan2(vx, vy)` is
0 for straight down and continuous; the same crossing now moves 0.004 rad, and straight-down means
rotation 0, which is what this branch's own "drawn exactly as authored, no flip" contract asks for.

⚠ **THE OTHER `atan2(vx,-vy)` SITES ARE NOT THIS BUG.** 20558/20756 feed a 24-way sprite index
through `mod 24`, so ±π lands on the same index; 21320 has no clamp, and π correctly points an
up-authored sprite down. **The fault was that formula COMBINED WITH a near-zero clamp.**

⚠ **AND A PROBE REFUSED MY FIRST HYPOTHESIS.** I said the wobble was bilinear smoothing on rotated
sprites, by analogy with the ship hulls (0811r), and built `probe_bulletshimmer.py` to confirm it —
it returned **25.4% churn smoothed against 28.5% nearest**, i.e. worse under my own fix. The metric
counts discrete pixel differences, which nearest maximises. The nearest-neighbour change on the
bullet pass is KEPT but on pack-contract/crispness grounds, **not** as the wobble fix. An analogy
was doing the work that evidence should have.

## ⚠ THE SUITE IS DETERMINISTIC NOW — **2,505 / 221 / 5**, EVERY RUN

Three fixtures (202 miniboss aura, 208 volley length, 212 curveL) run the LIVE stage plan, which
picks waves and cadences from `Math.random` — so each measured a different battle every time and
the suite returned **4, 5 or 6 failures with no code change between runs**. That is worse than an
occasional red: rule 3 says ALWAYS CHECK THE COUNT, and a count that moves on its own teaches
everyone to stop reading it. `seedWaves()` / `unseedWaves()` wrap those three. **Three consecutive
runs now give identical 2500 ok / 5 fail / 221 sections.**

⚠ **IT SETTLED ON 5, NOT 4, AND THAT IS THE FIX WORKING.** *"every volley fired is 5-8 rounds"* now
fails every run with the same numbers (6, 3) instead of one run in three. Same defect, now always
visible. A consistently red test you can attribute beats a flaky one you learn to ignore.

⚠ **BUT THAT RED IS NOT YET ATTRIBUTABLE TO THE GAME.** Run standalone at 14/17/20/26 seconds with
the fixture's own setup copied verbatim, the boat fires **ZERO rounds at every length**. The fixture
only produces volleys because of state left by the ~200 sections before it, so its result is
meaningless in isolation and **no threshold should be touched on the strength of it**. Lifting it
out means first establishing which accumulated globals the boat needs. Recorded, not worked around.

**A different count now means something actually changed.**

**0811t — the jet-speed claim, VERIFIED, and a bug 0811o put in.** `probe_jetspeed.py` measures
per-frame displacement (not a velocity read off the unit — that reports intent, not what moved it).
**`straight` is exactly 96, min/median/max.** ⚠ 0811o's claim that the edge pin caused the variance
was only HALF right: `curveL` reads 60..128 IDENTICALLY with the pin on and gated, so those two
open items overlapped rather than being one bug. With separation off the high end collapses to 96 —
the >96 excursions are `enemySeparate` doing its job, and the 60 dip is `jetTick`'s own `_entered`
clamp at x=22. Every part of the residual is a deliberate mechanism.

⚠ **AND THE MEASUREMENT FOUND A BUG 0811o INTRODUCED.** `_inField` latched when the unit's BOX was
inside `[0,W]`, but the pin clamps to `_edgeM` (`w*0.66`) — a stricter bound — leaving a band where
the latch fires and the pin instantly snaps: **one frame at 923 px/s against a 96 airspeed.**
Latching on `_edgeM` makes the transition a no-op by construction. **A fix that removes a 91px
teleport and leaves a 15px one is not finished, and only measuring the thing it claimed to fix
would ever have shown that.**

**0811s — projectile variety, and it made the screen QUIETER.** Four new volley shapes for the four
things Mike named: **`rake`** (machine gun — a 3-round burst that WALKS across its arc each volley,
not another fan), **`salvo`** (missiles, gated on `_eMslAllow()`), **`curtain`** and **`ripple`**
(screen-filling; ripple's stagger is a y offset, which IS a delay because bullets move per frame).

⚠ **"RANDOM PATTERNS" IS ROTATION BETWEEN SHAPES, NOT RANDOMNESS INSIDE ONE.** Jittering angles
inside a pattern breaks the rule this layer exists for — a pattern must hold its shape so what the
player learned still applies. Rows carry `alt:[...]` and cycle; `_volSeed` (from spawn position,
NOT `Math.random`) desynchronises units of the same type so a wave replays identically.

⚠ **SCREEN-FILLING SPANS THE CAMERA, NOT THE WORLD** — stage 1's world is 800 against a 480 camera,
so a `worldWidth()` curtain measures wide and plays thin. Same trap as the pop-in (0811o).

⚠ **MEASURED A/B, AND VOLUME WENT DOWN**: stage 1 −3%, **stage 5 −20%**, stage 7 −2%; peak on screen
169→143 on stage 5. The screen-filling rows carry `every` 7–9 (RARE — `every` is the cooldown
multiplier) and no screen-filling appears before stage 5. The baseline arm collapses every
`alt:[...]` back to its first entry, which is exactly the old table.

⚠ **`salvo` FIRING NOTHING ONCE IS THE MISSILE BUDGET, NOT A DEAD PATTERN** — `_eMslAllow()` is
`Math.random()<0.45` on stage 1. One failed roll and a dead system look identical from one sample.
Measured 23/40. A new missile source that ignored that gate would silently undo Mike's cut.

**0811r — speaker colour, typing sound, and black edges that were already there.** The cutscene
name and body now carry the speaker's own `PILOTS[].tint` as a palette swap, and the scene types
with a blip on every third character.

⚠ **THE PILOT SHIPS ALREADY HAD BLACK EDGES; SMOOTHING WAS DISSOLVING THEM.** Measured first: source
boundary pixels are **93–98% dark, magenta ~0** on every hull. `drawPlayer` blits a 226x271 cell at
h=60 — a 4.5x downscale — under the init-time `imageSmoothingEnabled=true, quality='high'`, and
measured at the drawn size **78–95% of the boundary comes out semi-transparent** (nearest: 11–19%).
A black rim at 30% alpha reads as haze, not a line. Nearest-neighbour is set around that one blit —
the contract a dozen other draws in this file already state and the player hull never did.
⚠ The trade: nearest at 4.5x samples rather than averages, so the hull is crisper AND harder
(Lizzie's roundel thins). One line to revert. See `docs/proofs/shipedge_0811r_smooth_vs_nearest.png`.

⚠ **TWO DISAGREEING TINT TABLES FOR THE SAME NINE PILOTS** — `STORY_TINT` has COLE orange
(`#ff6b3a`), `PILOTS[].tint` has him green (`#7ad63a`, matching his emblem). `PILOTS` matches the
art and wins in the cutscene; `STORY_TINT` was left alone rather than changed blind. Reconcile by
rendering both, not by picking.

⚠ **`stageWrap` HARD-CODED `null` FOR ITS TINT** — no caller could colour a wrapped block at all.
`tintC`/`tintA` are appended and optional; nine-argument callers are unaffected.

⚠ **`pcUpdate`'s typing blip tests `(C.typed|0)%3` EVERY FRAME, not per character**, so one letter
can blip twice and only its `Math.random()<0.5` coin keeps it from buzzing. The cutscene fires on
the character advancing instead. The pilot-card version is deliberately untouched.

**0811q — the cutscene fits its boxes; "wide/fullscreen" is a DECISION, not a fix.** The dialogue
ran out over the right rail because the text was laid out to the PANEL, not to its interior.
Measured off the plate: `dlg_window` is 1465x808, interior **x 0.0389 / w 0.9208 / top 0.0817**
(`DLGW_IN_*`) — the cutscene assumed 0.0199/0.9603, a column 6% wider than the frame starting 2%
left of it. The body size is solved against the box now instead of hard-coded at S(15) with "three
lines of room" assumed (three was true only of the too-wide column). New: **`stageWrapCount`**,
the same greedy wrap **without drawing** — `stageWrap` only reports its count after drawing, which
is too late to choose a size, so a block could be fitted to its width but never its height.

⚠ **THE BOTTOM RAIL CANNOT BE MEASURED DOWN THE CENTRE** — a dark star medallion sits there, so a
centre scan runs past the rail and reports h 0.915. Rails are symmetric; bottom is taken as top.
⚠ **`drawCommWindow` keeps its own looser insets deliberately** — they are wider, so its text sits
inside its frame; it was not changed blind on a surface this drop never rendered.

⚠ **FULLSCREEN COSTS SOMETHING AND IT IS MIKE'S CALL.** All ten cutscene plates are **640x480
(1.333)**; the viewport is **480x512 (0.938)**. The design space is already correct for the art —
the letterbox is 4:3 plates in a near-square playfield. `Math.max` cover crops **203 of 640 design
px, 31.7% of the width**, eating both stairwells and clipping a portrait; stretching distorts 42%.
**New plates at the playfield's aspect are the only clean answer, and `drawCutscene` already fits
whatever aspect it is handed** (SW/SH are two numbers). Art job, not a code one.

**0811p — "projectiles appear wobbly SOMETIMES" is one system, and it is fixed.** "Sometimes" was
the diagnosis: a shape that is always the same is an authored corkscrew, one that changes with the
frame time is a bug — so it was measurable without asking which projectile. `probe_wobble.py` flies
every enemy bullet kind twice over the same simulated duration, steady 1/60 against a jittering
frame time. **Ten of eleven are 0.00 lateral and frame-rate independent** (mg, shell, dart, ice,
flare, minigunT, chaingunT, bolt, emissile, groundup). One is not: the swirl missile.

⚠ **TWO CLOCKS IN ONE MOTION.** The swirl added a per-FRAME offset to position while its phase
advanced on real TIME, and `b.x += b.vx` has no `dt` either — so forward travel is per-frame and
the corkscrew is per-second, and any hitch desynchronises them. Its amplitude also scaled with
frame rate (summing a cosine over frames is `amp/(HZ*dt)`). It is an absolute function of time now,
applied as its delta. **The 60fps look is reproduced deliberately** (`SWIRL_AMP = 1.9*60/7.4`) —
Mike signed that swirl off in 0808w, so the fix is frame-rate independence, not a straight line.
Measured 27.68 steady both before and after; drift 4.84 → 1.03.

⚠ **THE WHOLE ENEMY BULLET SYSTEM MOVES PER FRAME, NOT PER SECOND** (`b.x += b.vx`, no `dt`). That
is the residual 1.03px. Putting `dt` on that line changes the speed of every enemy bullet in the
game — every `spd` in every `eShoot` call was tuned against per-frame motion — so it is a balance
change across nine stages wearing a bug fix. **Left alone deliberately; it needs Mike.**


**0811o — "ENEMIES APPEARING OUT OF THIN AIR" IS CLOSED, on all eight stages (probe_popin: 0).**
Two causes, and neither was the one the handoff's §2.3 was chasing — **no y transform was needed on
any unit; every real pop-in was horizontal**, so the drivable-band assertions that blocked the
mirror were never the obstacle.

1. **`VW` is the VIEWPORT (480); stage 1's world is 800.** Waves authored a right-side entry as
   `VW+28` = 508, a third of the way in from the real edge. `offRightX()`/`offLeftX()` now say what
   was meant (a no-op where world === viewport).
2. ⚠ **The catch-all edge pin in the enemy loop snapped ANY unit to `w*0.66` from the world edge on
   its FIRST TICK**, so no wave could ever author a side entry — measured, and the margin is a
   function of the unit's own width (`w95 → 63`, `w44 → 29`, `w60 → 40`). Its exemption list was
   **hand-written** (the `_selfPat` trap): routed jets, `volc` skimmers and plain `straight`
   crossers were absent. It is gated on geometry now — `_inField`, "has been fully inside once".

⚠ **THAT PIN IS ALSO "something outside jetTick displaces them"** — the note below, next to
"observed jet speed varies 96–138". A 91px teleport on frame one is exactly that. **The two open
items were one bug**; the speed figure is worth re-measuring on `probe_stack`'s seeded harness.

⚠ **AND THE PROBE HAD BEEN ASKING THE WRONG QUESTION TWICE.** It tested only the TOP edge (so
corner-route jets authored off the SIDE read as pop-ins — acting on that would have broken the
routes), and it read `e.x` at `spawnEnemy`'s RETURN, before `l6Crosser` and friends correct it
(so `octo`/`fang` read as `x=480`). **Four of the eight "bugs" it reported did not exist.** It
measures the full box on the first DRAWN frame now, and respects `{inPlace:1}` — a declaration
carried at the spawn site by units authored to appear where they are (a splitter's halves, a
surfacing maw), so the design is not mistaken for a bug.


**0811n — dialogue portraits, and the boats.** The speaker's portrait is in the stage dialogue
window's left bay, **mirrored** (the pack is authored facing screen-left; `drawCutscene` mirrors its
left slot for the same reason). Deliberately NOT `drawCommWindow` — that helper dims the whole
screen and is a modal, against this file's own "never hold the player in a dialogue box during
active combat".

⚠ **AND THE BOATS DO NOT FIT IN THE RIVER — that is why "boats on water" failed in FOUR drops.**
Measured: widest contiguous water on the rows stage 1's boats occupy is **32px**; the footprint
`pickWaterX` demanded was **47px**. It returned null at every x on every row, forever, which looks
exactly like "there is no water here" — so three drops were spent on WHEN to call it when the answer
was always going to be null. It tests the **keel** now (`NAVAL_KEEL`), not the beam. Two further
things the measurement separated: a one-shot solve cannot hold (a naval unit cancels the scroll to
hold station, so **the river slides out from under it**), and **two thirds of "779 boats on land"
was the deliberate `_beached` withdrawal from 0809n**. Live-on-land 252 → 2.
⚠ Fewer boats are now on screen (they move to water or withdraw rather than sitting on jungle).
That is a gameplay change Mike has not seen — if he wants more, the fix is in the wave scripts.


**0811m — five of the nine items on Mike's bug list.** The pickup icon chain (his L3 fireorb and L2
icebreath reports were ONE bug — the world pickup asked **XART** for a `micon_` key, which is
permanently false, and there were **four** element tables in the path contradicting each other;
also slots 0/1/2 had never drawn an icon at all); Decker's shotgun box (grantable since 0805i and
with **no draw branch**, so it appeared as a blank capsule); the level-1 dialogue window (bottom
left, `dlg_window`, BOF font, auto-fitted — and a **line-breaker for the BOF face at last**:
`msgMeasure` / `msgWrap` / `msgTextLeft` / `msgFitH`); and the arcade pickup banner
(type → sweep → hold → slide). **Not attempted: cinematic fullscreen, projectile wobble, projectile
variety, and the pop-in half of "enemies from thin air".**

⚠ **`micon_` IS IN THE THIRD ART STORE AND THE NOTE BELOW SAYING "the world pickups already use
iconDraw correctly" WAS WRONG** — that is why this path went unchecked after 0810r. Use `iconBlit`,
which knows all three stores, from every surface.

⚠ **THREE INSTRUMENTS IN A ROW WRONGLY REPORTED THE BANNER DEAD** — a source grep of
`updatePlay`/`drawWorld` (the call is one level down in `updateEffects`), a before/after frame diff
(the stage scrolls; ~963k pixels move either way), and a same-state double draw (this renderer
reads `performance.now()` directly, so two draws of one tick still differ everywhere).
**Same-state frame isolation is not available here. The screenshot is the proof.**

⚠ **`curveL bleeds LEFT` JOINS THE ORDER-DEPENDENT ASSERTIONS** (with §202 and the volley one). Two
suite runs with no code change between them gave 6 failures then 4. In isolation, seeded, with
separation off and on and three seeds, curveL is **-177 every time** against a -60 threshold.
Re-run before blaming a change, and read the COUNT.

The handoff
covers drops 0810s–0811j — what landed, what is still owed WITH the exact reason each unfinished
attempt failed, every trap found, and the eight new probes. 0811L is the newest drop and
supersedes its §2.1.

**Landed in 0811l:** the jet **banking channel** (a lean is now derived from the heading the
aircraft CHOSE, `_hx*_spd`, not the ground it covered — an external push is invisible to attitude,
which is what had blocked separation for a drop); **enemy separation** (`enemySeparate`, with a
formation deadzone and terrain veto, measured 50.3% → 20.0% settled burial on stage 1 and
150.7% → 52.4% on stage 4, and shown in `docs/proofs/separation_0811l_{off,on}.png`).

⚠ **AND STAGES 4 AND 6 HAD BEEN FIELDING 26x26 ONE-HP JETS THAT NEVER FIRED, for six drops.**
0810p repointed their waves onto `s1jetDelta`/`s1jetBomber`; `S1_JETS` and `NEF_S1` are keyed
`s1jetdelta`/`s1jetbomber`, so every lookup missed and the units took the generic defaults —
`26x26 hp 1 pattern sine atk NONE` against `95x105 hp 6 pattern s1jet atk mg`. The line "⚠ BOTH
SPELLINGS ARE REQUIRED" was in this file the whole time; **nothing asked, so nothing failed.**
`rosterKey()` normalises the spelling across all three tables. **This makes stages 4 and 6
materially harder and the waves may want re-tuning — Mike's call.**

⚠ **Two probe lessons from that drop, both general.** A `worst`-of-run maximum cannot tell
"stacked" from "spawned on the same point"; and an **unseeded** A/B on this game measures wave
randomness, not the change — the same arm swung 839→424. `probe_stack.py` seeds `Math.random`
and reports settled burial. **The 839 / 71.9% baselines quoted in the handoff are retracted.**

**The two 404s at boot are identified:** `assets/data/ui_layout.json` and
`assets/fonts/BlackOpsOne.ttf`. Worth checking the first before the stats-screen alignment work.


**0810s–0811b, all committed and each verified in real Chromium:** the five ship bosses (stages 2/3/5 + minis on 2/3) and the Blacksteel Raptor as stage 4's miniboss — stage 4 had had NONE, its table still named the retired `subreactor`; Mike's fire orb + ice breath icons and the EQUIPPED box that was drawing the wrong one; the quad-laser's four beams and its charge phase; stage 7 on Mike's corrected plate with the sludge behind it, darkened to 50% value; the enemy volley layer and the five silent rosters armed; Mike's loopable runway; the arcade intro cards' blank panel; music on the Fury HQ cutscenes.

⚠ **The recurring failure this stretch was systems that were declared and never fired** — the quad-laser's muzzles, `_qlChg`, `enemyVolley` sharing a `fireCd` its unit's tick owns, `micon_` asked of the wrong store, `lordshadows` registered and referenced nowhere. In every case the state looked right and no pixel moved. **Render it, then believe it.**


Suite: **2,636 assertions / 234 sections / 5 failures** (drop 0813a) — the preload count, the two
`_superseded` ones, the volley round count and the naval flash families. ⚠ **If you see more than
five, check `git status` for deleted art before you debug anything** — a missing file trips nine
assertions across four sections and reads as an unrelated pile of failures.
Entry joins: **`probe_arrival.py` green on all eight stages** (see the connector section below —
and read the warning there before trusting any older arrival number).

### ⚠ THERE ARE TWO DIVERGENT TREES. READ THIS BEFORE MERGING ANYTHING.

A laptop session delivered `BulletsOfFury_0810a.zip` on 08-11. **It forked from a snapshot older
than this repo's first commit** (its `game.js` is 30,364 lines against 30,979 at `2cd089c`), so it
has *no common ancestor here and cannot be 3-way merged*. It is missing everything from 0809 on —
campaign save slots, `campPause`, the attract reel, the Fury HQ cutscenes, `xartPalette`, the
stage-1 RC2 rebuild. Copying it over trunk would erase all of that.

It is preserved verbatim as orphan branch **`laptop-0810a`** and is being ported forward feature by
feature. **Never sync that tree wholesale.** Its zip is also incomplete — 78 files short, including
`jungle800_rc2_master.png`, the whole BOF font set, `ART_TAXONOMY.json` and `shoot.py`.

**The port is COMPLETE.** All four pieces are on trunk: the TRANS re-key, transitions **2→3**
(lava→ice) and **3→4** (ice→sky→town), and the **TELL→COMMIT→RECOVER** enemy contract with
`stageHeat()`. Guarded by suite sections 133b and 133c. The only thing deliberately NOT ported is
the `ARSENAL_MINIS` consumer — see the note at its declaration. The branch stays as the record of
what the laptop tree was; nothing further is owed to it.

### Landed 0810a–0810b

**The 3-2-1 jerk is fixed.** It was three quantities plus a camera that nothing forced to agree —
at GO the ship jumped +160 x, +92 y, +14 h (a 23% pop) and the camera then slid 159px back.
`playShipPose()` is now the single pose both sides read, the launch's settle phase eases onto it,
`snapCamToPlayer()` fixes the camera in `beginStage`, and `_drawLevelRegion` draws through the same
`translate(-camX)` `drawWorld` uses. All three deltas are 0. Measured by `probe_seam.py`.

**⚠ There are TWO intro systems.** Stage 1 uses `GS.OPENING` (the runway cinematic); stages 2–9 use
`GS.INTRO` → `GS.LAUNCH`. "Stage 2's intro is the model" means `drawLaunch`. The fork is in
`beginStage`, gated on `DBG.opening && num===1 && XART.rdy('nst4b_exit')` — and `XART.rdy` is false
on its first call, so a cold boot can silently take the LAUNCH path on stage 1.

**The TRANS table was keyed by DESTINATION and read by SOURCE.** `TRANS[2]` said "water into lava,
arriving at the volcano" when stage 2 *is* the volcano. Eight keys covering seven joins, 1→2 twice,
8→9 missing. Latent only because just stage 1 was switched on. Re-keyed; its eight assertions had
been green while wrong because they were written from the table they checked.

**Lizzie's turret fired nothing, and Decker's shotgun was why.** `beginStage` never cleared
`run.dkT` despite the comment promising it, and `dkActive()` checked only the timer, not the pilot.
Both fixed and pilot-gated. Decker's shotgun itself was always correct.

**Axel's orb and laser are now runtime `xartPalette` swaps of Falva's `florb_`/`fllaser_`.** Note
this is *not* the `aorb_`/`nadb_` hue-rotation Mike rejected in 0805d — different source art (her
helper balls, not her charge orb) and a live swap rather than a baked second copy. Verified by
`probe_palette.py`: hue moves ~100°, luminance holds within 0.05.

**The ARSENAL MINI TIER is live** — caldera on 2, frostbite on 3, dambreaker on 4. Mike: "those
are enemies we have."

⚠ I blocked on this once for the wrong reason, so the correction is worth keeping: I read
`ARSENAL_MINIS` as feeding `SUBBOSS` and refused to wire it. **It does not.** It is a separate,
lighter tier that arrives mid-wave EARLIER than the sub-boss, with no WARNING banner and no scroll
hold, so a level reads mini → sub-boss → boss. Nothing is displaced, and the suite now pins both
halves. The stage assignment is Mike's own, recorded verbatim in the laptop drop: *"that dambreaker
isnt the same miniboss I have in level 1 currently"* — so level 1 keeps its quadlaser and
dambreaker moves to 4. The old `{1:'dambreaker'}` keying was simply wrong.

⚠ **AND I WAS WRONG THAT THE ARSENAL BLOCK WAS ALREADY HOISTED.** I read grep line numbers as
proof of scope. `spawnEnemy`'s unclosed `if` swallows everything below it whatever column it sits
in, so `ARSENAL_DRONES`, `ARSENAL_MINIS`, `arsenalDroneArt` and `arsenalDronesFor` are ALL still
function-scoped — the laptop's "dead systems" finding was right about trunk too. The mini tier is
now hoisted above `spawnEnemy`; **the other four are not**, and anything outside `spawnEnemy`
reading them is silently getting `undefined`. Left for its own drop because it has a real blast
radius. When it bit, the suite reported **0 failures with the count down from 2,421 to 1,567** — a
crash wearing a pass, rule 3 exactly. Always read the COUNT.

### Fixed in 0810f — Mike's bug list

- **Lizzie's MG was barely faster than the primary.** 0.16 against ~0.20; now 0.075. Damage
  untouched at 7 — that was measured for the one-or-two-shot brief and was not the complaint.
- **Both loaned weapons now expire.** 15s each, and they die with you. The mount previously had
  NO expiry at all and Decker's ran 24s. `dkEnd()` / `lzMountEnd()` are single exits shared by the
  clock and the death path so they cannot drift apart.
- **The stage exit drew TWO ships** — `drawWorld` draws the real player, and `drawFlyover` drew
  another on top. It now drives `player.y`. The fade also started at 1.25s against a 1.35s hover,
  so the ship faded out where it stood instead of leaving; beats are derived now.
- **The stage-3 crate wore an ice orb over a fireball.** `weaponIconKey` was right all along
  (verified at runtime); the FALLBACK substituted `ice_icon_` with no `orbIsFire()` check, and it
  runs for every pickup because `XART.rdy` is false on its first call. It no longer substitutes
  when the element would be wrong.
- **Level 4's waterfall was in a second table.** 0801ku nulled stage 4's `liquid` but left
  `FALL_FOR[4]='nlf_water'` plus a FULL-WIDTH drop `{y:2904, x0:0, x1:799}`. Removed.
- **`enemyEntrySweep` had no caller for two drops.** It ported cleanly in 0810d and its one call
  site — in the enemy update loop — did not come with it. **When porting a function, grep for
  the CALL SITE, not just the definition.**

### Probes added — all four drive the real game in real Chromium

| tool | proves |
|---|---|
| `probe_seam.py` | ship/camera/terrain deltas across an intro→PLAY seam |
| `probe_weapons.py` | what `pShoot()` actually puts in `pBullets`, all nine pilots |
| `probe_palette.py` | a palette swap moves hue and holds luminance, i.e. is not an overlay |
| `probe_arrival.py` | the opening's last frame and PLAY's first are the same picture (0/393,600 px) |
| `probe_enemies.py` | per-unit BLIT COUNT and SPAWN position — invisible vs vanished vs pop-in |
| `scenario_seam.js` / `scenario_special.js` | drop `shoot.py` into the launch, or into a live special |

⚠ `probe_seam.py` runs its whole sequence in ONE `evaluate` — deliberate, because the game takes
`dt` from `performance.now()` and stepping one frame per `evaluate` gives every frame a `dt` of
~1.6 **seconds**. But that means it hits the `--warm` trap: lazily-loaded art never arrives, so
`mapScroll` reads 0. Trust it for ship and camera, never for terrain.

⚠ `shoot.py` captures inflate `dt` between shots — each screenshot is a separate `evaluate`, so the
next frame sees the real wall-clock gap as its `dt`. A 6.3s launch finishes in far fewer captures
than `--seconds`/`--fps` implies.

⚠ **Section 202 (miniboss shield aura) is FLAKY.** It simulates 200 seconds of play to reach the
miniboss and its result depends on state left by earlier sections — it failed once and passed on a
re-run of the identical file, and the same play loop reaches the miniboss every time in isolation.
Before blaming a change for it, re-run, or lift the loop into a standalone probe.

**The repo is now git.** `SETUP.md`'s move happened; `core.autocrlf=false` is pinned locally so a
revert restores byte-identical files. A second session is wiring the bosses in the same working
tree, so commits interleave — check `git log` before assuming a change is yours.

**`shoot.py` now composites all three canvases** (`#hud`, `#equipcv`, `#screen`). It only grabbed
`#screen` before, so the HUD and equipment box were invisible to the one tool that proves pixels.
Long warms plus many captures still exhaust the renderer — take deep warms and sequences in
separate runs.

**Done in the 0809 drops:** campaign save slots (3, localStorage) with a session-only CONTINUE;
stage 1 rebuilt from RC2 (flipped, ocean punched to alpha, coast re-measured to 4605, two-tower
bridge mirrored, zero magenta); stage 1–3 enemy rosters from the art lock, halo converted to a
black edge, with baked damage states replacing procedural vents; barrels/props with radius splash
and chain detonation; stage 1 waves finally fielding the naval opening and the barrel dumps (6
types → 14); the three elites revived (`el_em`/`el_lr`/`el_cs`, six waves that spawned nothing);
player impact FX and muzzle flashes for every weapon; the EQUIPPED box (it asked for `micon_*`,
which has never existed — 18 icons extracted from `nia_icons`); cap-height glyph metrics.

**Done recently:** stage 1 roster built from `CF_BOFFinalArtSources-Vol.2` (16 units sliced, halo
converted, black-edged, flash + black camo, unit 12's wing repaired across a cell boundary);
naval and tank behaviour tables; jet routes with banking; the BOF font made the single face for
stage banners and all UI; menus backable via `menuBack()`; keyboard password entry.

**Known open:**
- `_superseded/` does not exist and is not recoverable — gitignored, so it was never in a drop
  zip, and it is in none of the four full-build archives. Its two assertions now FAIL rather than
  throw (a throw there killed the run at section 149 and looked like a pass). Git is the
  reversibility mechanism it existed for; decide whether to retire them.
- **The stage 1 dam ending — read this before touching it, there are TWO dams.**

  The art exists. `ndam_intact` / `ndam_damaged` / `ndam_breach` / `ndam_destroyed` are in
  `assets/game/`, registered, 244–254×350, magenta-keyed. De-keyed rect of `ndam_intact` is
  (10,28)–(231,317) = 222×290. I twice recorded this art as missing; both times wrong. **Search
  `assets/game/` by filename before concluding art is missing** — not just the RC2 pack, not just
  the atlas cells.

  ⚠ **But `ndam_*` does NOT overlay the dam painted into the plate.** Template-matched
  `ndam_intact` against the top 1000px of `jungle800_rc2_master.png` across scales 1.0–3.8: best
  mean-abs-diff **37.26**, which is noise — a true match on identical art scores under 8. (Best
  candidate was scale 1.4 at (251,155); not a match.) **Don't repeat this test.**

  So the two mechanisms are for different things:
  - `cfg.destroyed` → `stageMasterKey` is a whole-master key substitution. It needs a destroyed
    800×4800 RC2 master, which RC2 does not ship. Wrong tool for `ndam_*`.
  - `ndam_*` is OBJECT art — keyed, 222×290, four staged variants. Meant to be **drawn as** the
    dam, not composited over the painted one.

  Recommended: the boss arena uses the `ndam` object as the dam it fights at, progressing
  intact → damaged → breach on damage tiers and → destroyed on the kill during the white flash.
  Uses the art as authored, needs no new plate. **Coordinate first — the boss is being wired in
  another chat; check `git log` before editing boss code.** De-key by flooding from the border
  (never a colour-match sweep), despill the rim rather than deleting it, halo → black edge.
- ~~The pilot-card hint row renders ENTER as "BNTBR"~~ **fixed in 0809q** — it was the tint, not
  the glyph map. See "A flat tint destroys the glyph" above.
- Stage 1 fields no camo tank variants yet (`s1tankheavy_b` and friends are registered, unused).
- Camo (`_blk`) exists for stage 1 only. Stage 2 is volcanic and stage 3 frozen; black is the
  wrong scheme for either and picking one is Mike's call.
- The stats screen is misaligned in the browser — labels sit ~half a row above their bars, and
  COLE/RANK collide with the first two rows. Correct in a Python render, wrong in the game.
- Cole's portrait shows the `crash` emotion at rank B; the table says `laugh`.
- Two 404s at boot.
- The `validate_antipatterns.py` hook errors on every write — its script path does not exist.
- ~~Jets: observed speed varies 96–138 even on `straight`.~~ **CLOSED and MEASURED in 0811t**
  (`probe_jetspeed.py`). **`straight` is exactly 96 — min, median and max.** The residual on
  CURVED routes is fully attributed and every part of it is deliberate: the >96 excursions
  (125–143) are `enemySeparate` pushing a jet clear of another unit (capped at `SEP_CAP`), and
  the 60 dip on `curveL` is `jetTick`'s own `_entered` clamp at x=22 pinning a jet that reaches
  the left margin. ⚠ 0811o's claim that the edge pin caused this was only HALF right — `curveL`
  reads identically with the pin on and gated, so the two open items overlapped rather than being
  one bug. `enemyEntrySweep`'s blanket exclusion of routed jets dodges the *old* banking coupling
  (removed in 0811l) and can now be reconsidered on its own merits.
- Stage 1 pop-in: **CLOSED in 0811o**, 0 on all eight stages.
- Two 404s at boot: **identified** — `assets/data/ui_layout.json` and
  `assets/fonts/BlackOpsOne.ttf`.
- Stage 1: 2 of 29 units still appear on screen rather than entering, both at (21,67).
- `mfx_` (252 cells) is marked DELETE in the taxonomy but is the **live** art for every enemy
  pellet and missile. Confirm with Mike before removing.

**Cinematics are wired.** The arcade reel runs after the ColeForge logo (`GS.ATTRACT`, any button
to the title) and is a **demo, not a slideshow** — three beats per pilot: the authored `aintro_*`
plate with **nothing drawn over it**, a cross-fade to their card, then the real game. The demo sets
`run.pilot`, calls `beginStage`, and drives `updatePlay`+`drawWorld` directly the way the harness
does; the ship climbs in from below the bottom edge and `startSpecial()` fires the pilot's ability
on cue. Nothing is baked, so it cannot go stale when a weapon or a stage changes. `PRESS START`
blinks over the demo only — a cabinet never puts its chrome on the pilot art.

⚠ **`beginStage` drives the state.** It runs the stage card and launch sequence and hands the
screen to `GS.OPENING`, so anything calling it from another state must take the screen back
immediately (`setState`) or its own draw is never reached again. `updatePlay` has no state gate of
its own, which is why the demo runs fine under `GS.ATTRACT`.

⚠ **The arcade intro pack had Decker and Freezer swapped** — the pack's own folder names, not the
registration, which was byte-identical to source. Rule 1 one level further out: distrust the
*source directory* names too. The other seven check out against `port_*_idle`.

**The arcade plates are rebuilt as `background + pilot-layer` and their panels are DRAWN**
(`drawAintroPanels`). The pack's flattened composite carried both panels — a faux rounded box with
PILOT DEPLOYED in a mono face, and another with the name in a generic sans — and the bottom one was
painted directly over a proper authored HUD frame the background already had. Now the top is BOF
text with a rule under it and no box, and the bottom is `dlg_window`, per Mike. Both lines
shrink-to-fit; JUGGERNAUT and PRINCESSES OF THE SKY both reach the frame at nominal size.

Drawing the name from the pilot key makes the Decker/Freezer swap **structurally impossible** to
reintroduce. The affiliations ("ORDER OF THE MATRIX", "PRINCESSES OF THE SKY" …) only ever existed
as baked pixels — they are transcribed into `AINTRO_AFFIL` and exist nowhere else, so do not
regenerate the plates from the pack without carrying that table forward.

`attractIdleTick` is defined and **never called** — the 12-second idle trigger is dead code.

**The campaign is not backable.** k/backspace/escape no longer exit `CAMPHUB`/`STAGESEL`/`PILOT`
in campaign mode — they open `campPause`, a glowing `dlg_window` holding the four authored buttons
(`btn_save`, `btn_load`, `btn_options`, `btn_exit`; EXIT GAME *is* RETURN TO MAIN MENU, per Mike).
The point is `campaignEnd()`: one place that knows the campaign is over, which a stray back key
never gave us. Checked before `menuBackTick` so one press cannot be read as both.

⚠ **Campaign persistence already existed** — `campSnapshot`/`campWriteSlot`/`campReadSlot`/
`campApply`/`campSlotUsed`, keyed `bof_campaign_slot<i>`, with CAMPHUB's own save/load flow. I
duplicated the whole thing before noticing (`CAMP_SLOTS` redeclared). **Grep for `camp` before
adding campaign state** — the save system is far down the file, past the hub drawing code.

**Cutscene portraits face each other** — every pose in the pack is authored facing SCREEN-LEFT
(Axel's drawn pistol is the giveaway), so `drawCutscene` mirrors the LEFT slot only.

**`xartPalette(key, mode)` is the panel palette swap — use it, not `xartTint`.** `xartTint` is a
`source-atop` flood, the same overlay that flattened the font's drop shadow into the E→B bug; on
`dlg_window` it erases every bevel and rivet and leaves a coloured slab. `xartPalette` preserves
luminance per mode: `black` multiplies toward a dark neutral (`'color'` **cannot** darken — black
has no hue or saturation to donate, so it only desaturates), `white` strips the silver's blue cast
then lifts, and any hex uses `'color'` so the metal keeps its shading. Cached per key+mode.
The pause menu is full-screen: black frame on the root, silver kept on save/load, slots red /
white / blue. The Fury HQ scenes now have a state to run in
(`GS.CUTSCENE`): `HQ_SCENES` carries all eight ensemble scenes from ColeForge's own cutscene bible
verbatim, `drawCutsceneState` types a line at a time over `drawCutscene`, and `hqTrigger(when,
stage, next)` fires them at the boundaries the bible names — `pre` 1 and 8, `post` 1/3/4/6/7/9.
It is campaign-only, plays each scene once per run, and calls straight through to its continuation
when a stage has no scene, so arcade and every unscened stage are untouched.

Two slots, and a speaker keeps its side: whoever talks takes the slot the PREVIOUS speaker is not
in, so the listener stays on screen dimmed instead of the portraits swapping sides every line.

## THE ENTRY CONNECTORS ARE BUILT — all nine stages (drop 0810j)

Mike's 0810i brief is in `docs/HANDOFF_CONNECTORS.md`. The **entry** half is done and measured.

Every stage now flies a connecting section of its own animated flat, with the level's own first
frame **butted directly onto it**. One mechanism, both intro systems: `entryConnectorDraw(stage,dy)`
next to `TRANS_FLAT`, driven by `launchConnDy()` on the launch path and by `openingDrawArrival` on
stage 1's. It keeps the load-bearing decision from 0810e — it calls `drawBG(0)` under a translate
rather than reimplementing the master blit — so "the last cinematic frame IS the first play frame"
stays structurally true instead of a claim to re-verify.

**Measured, honestly this time: 0 differing pixels of 299,842 on six of eight stages** (stage 2: 13
px, stage 4: 6 px, stage 5: 0.64%). `python3 _BUILD_SOURCE/probe_arrival.py` runs all of them.

### ⚠⚠ THE OLD "0 of 393,600" NUMBER WAS NEVER REAL. Do not cite it.

`probe_arrival.py` grabbed the canvas on the `play` branch **without stepping first**. The state
flips at the END of `drawOpening`, inside a step that has already drawn a cinematic frame — so the
"first play frame" was that cinematic frame, and the probe compared two consecutive cinematic
frames. Both static by then, so it returned 0 differing pixels *whatever the handoff looked like*.
It could not fail. That number is quoted in this file's history and in the handoff doc as the bar
for this work, and it was measuring nothing.

Same family as the `probe_seam.py` lesson one step further out: that probe RECOMPUTED the value
under test, this one READ THE WRONG FRAME. **A probe must draw the frame it intends to measure,
then read it.** With that fixed, three real seams appeared that had been invisible for two drops:

- **CRT SCANLINES WERE PLAY-ONLY.** `drawWorld` ends with `drawScanlines()` — a black row every 2px
  at 8% alpha — and no cinematic ever drew them, so every other row darkened the instant PLAY took
  over. Invisible on a dark stage and to every state-based check; on stage 1's bright water it was
  **half the pixels in the frame** moving at the handoff. Both cinematics draw them now.
- **THE LEGACY RUNWAY DREW ON ALL NINE STAGES.** `seqRunway` returns null for every stage but 1
  (Mike, 0801bf: "only stage 1 gets the runway intro") and `drawLaunch`'s else-branch drew
  `X.get('runway')` anyway. The suite asserted "no OTHER stage flies a runway" and passed, because
  it asked the *table* while the pixels came from a different path. Rule 2, in one line.
- **STAGE 6's ENTRY WAS TWO DEAD REFERENCES AND A STALE COLOUR.** `nsky6_par` — the cloud deck its
  sky branch asked for — **is not a registered key** and never drew a pixel. What stage 6 actually
  showed for ten seconds was `SEQ[6].fill`, `#2a6ac0`, DAYLIGHT BLUE left over from before the
  stage became the night cloud sky fortress, and then it cut to a night level. That is "stage 6's
  is broken and horrible", entirely. Connectors read `_levelCfg`, never SEQ's stale copy.

`_drawLevelRegion`, `_region` and `_liquidFrame` are **deleted** — the widening-clip reveal and the
band tiler that served it. Six assertions moved with them (sections 47, 49, 62, 133b) rather than
being dropped; the camera guard now names `entryConnectorDraw`.

⚠ Source assertions that read `drawLaunch.toString()` see **comments too** — the first cut of the
new ones failed because the comment explaining what was removed named what was removed. They strip
comments now. A source assertion a docstring can defeat is not measuring anything.

### Still open on this brief

- **The craft draws twice at the join.** `drawLaunch` draws the ship and a hand-rolled `nthp_`
  plume itself; PLAY draws the player through its own path. Nothing forces them to agree — the same
  shape as the pose seam 0810a fixed, one layer in. It is the whole of the residual 2.5–4.3% in the
  probe's "whole band" column. The fix is 0810a's: one draw, read by both sides.
- **The ship is INVISIBLE on PLAY's first tick, every stage, every time.** `player.reset()` leaves
  `invuln` at 120 and the player draw hides it on a 4-on/4-off blink
  (`Math.floor(player.invuln/4)%2`). It was solid a frame earlier in the cinematic. This is a second
  live cause of "clips it in and out" — 0810a fixed the height pop, not this. Whether a fresh stage
  start should carry visible i-frames at all is **Mike's call**, so it is left alone.
- **Stage 5 is the only stage above 0.01%** (1.09%), and it is now diagnosed: `drawWorld` draws
`l5FieldDraw` (orbital hardware, asteroid belt) and `l5RocksDraw` for stage 5, and those live in
drawWorld rather than in `drawBG` — so the connector, which calls `drawBG(0)`, cannot include them
and the field pops in on PLAY's first tick. Fixing it means either moving the stage-5 field into
drawBG or having the connector call it; both are stage-specific and the field is dynamic, so it is
left recorded rather than guessed at.
- The seam between flat and level is a **hard butt-join**, not feathered. That reads as a direct
  connection and matches "no more fake transitions"; if Mike wants it blended it is a small change.
- Stage 9 has a `_levelCfg` case and a connector entry but **no `STAGES[]` entry**, so it is off the
  probe's default list and `beginStage(9)` has no `curStage`.

## THE STAGE-2 EXIT IS BUILT TOO (drop 0810k) — `probe_exit.py`

> "Level 2 boss cuts to the lava instead of a connecting section at the end of the level and
> another one to lead us to the cinematic that we can scroll infinitely."

**He was describing two cuts and both were real.** `outboundDrawLavaIce` drew the master through a
modulo loop keyed off `o.scroll`, which starts at 0 — and `sY = H - (0 % H) - VH` is `H - VH`, the
**bottom** of the plate. So the boss died at the top of the level and the volcano jumped straight
back to the level's **first frame**; then `tflat_lava` wiped down over it. Invisible to every state
check, because mapScroll, camX and the player were all exactly where they belonged. Only pixels can
see a wrong picture drawn in the right place.

`exitConnectorDraw(stage, dy)` is `entryConnectorDraw` run the other way: the join sits at screen
`y = dy`, the level below it via `drawBG(0)` under `translate(0,+dy)`, the connector surface above.
At `dy = 0` the outbound's first frame **IS** PLAY's last frame — **0 differing pixels of 299,842**,
measured. Past `dy = VH` the level is gone and the flat tiles on alone, so it scrolls for as long as
the cinematic wants and cannot run out. That is the "infinitely" half, as a property of the
construction rather than a length someone has to guess.

`levelScrollRange()` is new and was the missing piece: `drawLevelMaster` computed the level's length
inline and nothing else could ask, which is *why* the routes looped from an arbitrary offset. The
route now spends its travel on whatever scroll the level has LEFT first — the caldera genuinely
passes behind — and only then on `exitDy`.

⚠ **The ice-never-leads-the-lava ordering is structural now, not incidental.** It used to hold
because the lava arrived as a timed wash that always finished first. With the lava joined on, how
long it takes to own the screen depends on how much level was left when the boss died, and a boss
that dies early leaves scroll behind it. The freeze clock therefore does not start until
`exitDy >= VH`. Section 133b's assertion moved onto that quantity.

**Scanlines were missing on the way OUT as well** — `drawOutbound` now draws them, so leaving a
level no longer snaps them off just as arriving used to snap them on.

**Still open here:** the 1→2 water and 3→4 sky-town routes still use the old loop-and-wash and have
the same first-frame jump. They were not touched because Mike named level 2 and both are signed off,
but `exitConnectorDraw` is generic and they should move onto it. `probe_exit.py` defaults to stage 2
for exactly that reason — point it at 1 or 3 and it will fail honestly.

## THE MINIBOSS BUGS (drop 0810l) — one fixed, one NOT REPRODUCIBLE

**Miniboss 1's white flash is fixed, and the cause was an unreachable branch.** The hit always
registered — `hitSubBoss` took the hp and set `b.flash` — and nothing ever drew it, because the
quadlaser's body does not read `b.flash` at all. Its pulse is driven by `_qlArmor`, and `_qlArmor`
was only ever set on the BLOCKED path, which `return`s before the hull can open. So the draw's
`_sealed ? blue : amber` had an amber half that **could never run**: the hull could only pulse while
still sealed, the exact opposite of the point. One assignment makes it reachable, and the colour is
white per Mike (0807b's own rule was "do not let the hull flash white until you break all the
turrets" — by then they are broken). Its assertion moved with it.

**A `//` comment had swallowed a statement.** `b.hp-=dmg; b.flash=0.18;   // long enough that a
single hit registers visually if(typeof stageStats!=='undefined')stageStats.dmgDealt+=dmg;` — the
comment ran on past "visually" and ate the line. **No sub-boss damage has ever reached the stats
screen**, on any stage. Nothing threw; the number was just quietly wrong.

### ⚠ "The miniboss on level 2, broken" DID NOT REPRODUCE — and the probe that said it had lied

`probe_boss.py` first reported **0 blits** for BOTH minibosses, with the art polled ready, the body
key resolving, the unit alive and on screen, and `subBossActive` true — every branch the draw tests
was correct and the count still said nothing was drawn. **A screenshot showed both units drawn in
full, health bars and all** (`docs/proofs/miniboss_0810l_both.png`). Wrapping
`CanvasRenderingContext2D.prototype.drawImage` and then calling `drawSubBoss()` by hand does not
count what the real frame draws.

So the verdict in that probe is now a **frame diff** — render with the unit, render without it, see
whether the picture changed. Stage 1 moves 401,466 px, stage 2 moves 174,574 px. Both draw.

**This means level 2's miniboss is not invisible and not missing, and I could not find what Mike is
seeing.** It spawns, enters, reaches the playfield and draws its damage states. Ask him what
"broken" looks like — does it not take damage, not die, not block, arrive at the wrong point, or
something else. Do not "fix" it blind.

**DONE 0810n — see the gauge section below. Superseded note:** (handoff section 3, "The hud and fills, remove
and make your own please"). The `nbb_`/`nmb_` art fills are still what draws, through
`drawHealthBarV2`. ⚠ `drawHUDCustom` returns early and only `drawHUDCustomImg` reaches the boss
gauge — whatever replaces it must be reachable from the path that actually RUNS, and given the
above, prove that with a frame diff rather than a blit count.

## STAGE 2's MINIBOSS AND BOSS (drop 0810m) — Mike's 0810m report

> "It cuts to this broken drill tank I told you to remove, teleports me to a animated lava tileset
> section from where i was on the level and he does absolutely nothing."

**THE TELEPORT WAS ONE FLAG DOING TWO JOBS, and it fires on every stage, not just 2.** `_bossRun`
is `bossActive || _sbRun`, and the arena block keyed off it does two things that are both a hard
change of place: `arenaLiquid` stops drawing the master and leaves the animated lava bed (authored
for the stage-2 BOSS, 0806f), and `_loopDraw` maps the master by `mapScroll % H` instead of by
`scrollFrac` through `rangeSrc` — **a different mapping of the same plate**, so switching to it
jumps the terrain to an unrelated part of the level. Every miniboss on every stage was doing that.
Split into `_realBossRun` (arena) and `_bossRun` (hold the scroll). The miniboss hold was already
implemented where mapScroll stops advancing, which is all Mike's rule asks for.

**The Obsidian Drill Tank is retired** — `DEAD_SUBBOSS`, same as subreactor. "He does absolutely
nothing" was literal: it has no attack case of its own.

### The Magma Colossus build — one fixed, two diagnosed and NOT guessed at

**Fixed: the torso now draws LAST.** It was drawn first with every seated limb painted over it,
against this file's own note ("drawOrder is back-to-front for painting, torso last so it sits on
top"). That is "overlaying instead of underlaying" — nothing tucked behind anything.

⚠ **A NEAR-MISS WORTH KEEPING: there are TWO contracts in this file and the wrong one fits.** The
MECH BOSS header guarantees every component is a locked 384x384 canvas that composites at (0,0)
with 0 channel difference. I applied that to the genesis seated draw and it is WRONG — GENESIS's
own header says `mbg2_p_*` are "the sprites cut from Mike's sheet — the loose limbs, not the
position-locked damage canvases", and `BOFX.mechpieces` gives each its own size (head 142x173,
torso 274x334, leg 200x432). Centring them stacks the whole mech on one spot. Caught before it
shipped only by reading on. **The `_p_` set is loose art placed by sockets; the `<comp>_<state>`
set is position-locked. Never mix the two contracts.**

**FIXED: "his head is too close" was TWO HEADS.** `GEN_HAULS` hauled a `head` limb and genesis
never checked `MECH_SKIP_PART` — which exists precisely because 0801dy measured `mbg2_p_torso` ink
at 274x334 against a whole assembled master of 267x350: **the torso sheet piece IS the body and head
together.** So the chain fished a head out of the lava and seated it over the one that had already
risen with the torso. The fight honours the skip; genesis never got it — the same "grep for the CALL
SITE, not just the definition" lesson. Driven off `MECH_SKIP_PART` now rather than hand-listed, so
the two cannot disagree again, and the filtered list rides on `G.hauls` because `genesisUpdate`
indexes it to pick the next haul and to know when it is done. mbg2 hauls four times, ending on the
cannons. It costs no HP — 0809m moved that to `MECH_HP_SHARE` entirely — only the beat.
Proof: `docs/proofs/magmacolossus_0810n_genesis.png`.

**FIXED: the fused form was a scatter of oversized parts, and it was the FIGHT that was wrong.**
Rendered at full health, the Colossus came out as two enormous detached cannons, a shrunken torso
and one leg — most of the mech missing. Two causes, both the same mistake:

- `mechDraw` preferred `<tag>_p_<piece>` — the LOOSE sheet art — whenever a part was intact, and
  only fell back to the locked `<tag>_<comp>_<state>` once it took damage. The sheet pieces each
  carry their own socket region so they cannot tile flush, which is why 0731f hung them with
  `MECH_SEP` gaps and 0809l tried to fit each into its component box. Neither worked.
- The aimed-cannon rotation frames are in the loose set's coordinate system — `BOFX.mechrot` gives
  them a **538x538** canvas against the master's 384 — so at `S*0.85` one forearm drew ~257px
  against a 288px whole mech, docked by its own anchor well off the body.

The locked set needs none of that because the pack guarantees it, and I verified rather than
trusting: eight cells, all 384x384, composited at (0,0) give an ink bbox of exactly 267x350 — the
master's own size — and it draws as the complete machine (`docs/proofs/magmacolossus_0810m_fight_vs_reference.png`).
Intact now takes the same path damage always took: full canvas, shared rect, no seat maths, no gap.
The loose set stays as the fallback for any tag with no locked state, and genesis still uses it for
pieces in FLIGHT, where loose art is correct.

⚠ The trade: the cannon no longer visibly tracks its aim, because the rotation set is unusable
alongside the locked components. Re-fitting that set into the 384 master canvas buys both back and
is art work, not code. Mike's call whether it is worth it.

⚠ Still not identical to the reference — the torso reads narrower and the limbs sit slightly wider,
which is per-part idle motion (`mechPartMoves`), not placement. Worth a look next.

### One of the five standing failures was a stale assertion, not a bug

"0 components carry a limb HP pool (5 limbs x 20%)" counted parts stamped `_limb` — the flat share
the haul used to write. **0809m deleted that deliberately**: the legs arrive on one trunk and the
cannons together, so a group pool meant shooting the left cannon damaged the right. Mike asked for
six separate targets. It could only ever fail. Replaced with the contract that actually holds —
every part DOCKED (the 0809m fix for "957 probes found nothing hittable"), per-component shares,
summing to 100%, and the haul writing no pool. All four pass. **Standing failures: 5 → 4.**

## ⚠ MIKE'S 0810q LIST — WHAT IS DONE AND WHAT IS NOT

**Done and verified:** the transition regression (my clip band sat off-screen for the whole
cinematic — `probe_arrival` stayed green because it only measures the handoff FRAME); level 1 now
uses level 2's entry (`DBG.opening=false`); the game-over countdown is off the 3-2-1; the
"BOOOOO" on kills (a flag collision — the death-halt wrote `e._frozen=true` and `true>0` sent
EVERY enemy down the ice-shatter branch); barrels are scenery again; level 3's slow zig-zag is
replaced with committed moves; the fireball icon.

⚠ **THE WEAPON ICONS WERE NEVER LOST.** Every `micon_` family is registered — fireorb,
thermoshock, iceorb, icebreath, mg, spread, missile, laser, firewall. The HUD asked
`ASSETS.has(wIcon)`, and they live in **XART**. The legacy store has never held them, so the test
was false for every weapon on every frame and the else-branch drew the text "L3" where the icon
should be. **When art looks "basic", check which store is being asked before concluding anything
is missing.**

### NOT DONE — still owed to Mike from this list

1. ~~Scrap the level 2/3 bosses and the level 3 miniboss~~ **done in 0810s** — see THE SHIP
   BOSSES below. He cast the replacements himself off the South-Facing Ship sheet.
2. ~~Lasers from the beams on the level 1 miniboss~~ **done in 0810s** — see THE QUAD-LASER'S
   BEAMS below.
3. **More projectiles, and patterns that force the player to hold specific spots.** Five new boss
   patterns and the quad-laser's four lanes land this for BOSSES. The ordinary enemy roster is
   still the stage-3 change only, and is the rest of the ask.
4. **Enemies still appearing out of thin air on level 1** — the long-standing pop-in; 2 of 29
   units were last measured entering at (21,67).

## STAGE 7 IS MIKE'S CORRECTED PLATE (drop 0810t)

*"replace stage 7 with that sheet as an overlay, clean up all purple and white specs and halos,
and use the sludge for the background."*

**No new draw path was needed.** The liquid bed is drawn UNDER the master and shows through
wherever the master is transparent, and stage 7 has declared `liquid:'nlq_sludgeF'` all along. So
the job was punching the plate's white background to alpha: **30 regions, 68.4% of the plate**,
up from 0.21%. 167 white specs (558 px) were FILLED rather than punched " a blob under 24px
inside the structure is a spec, and punching it opens a pinhole of sludge in the middle of a pipe.

⚠ **White was swept GLOBALLY, against the standing border-flood rule, and that is measured.**
A border flood cannot be used here because the ENCLOSED gaps must become channel too. A sweep is
only safe when the key is cleanly separated, and it is: 68.43% at pure 255, the structure topping
out at 229, and exactly **one pixel** in the 235-254 band between them. The build script
re-checks that gap every run and refuses if it closes.

⚠ **Two things I got wrong here, both caught by rendering, not by reading.** I built the
channel as literal `#FF00FF` first, on a reading that `drawStageBG` keys magenta at runtime " it
does not, the magenta in the RC2 plates is punched to alpha OFFLINE. Stage 7 rendered as a screen
of raw magenta with pipes on it. And I claimed the sludge had "never drawn" after measuring the
old master **converted to RGB, which DISCARDS ALPHA** " it has 8,412 alpha-0 px, the exact figure
game.js already records. **When a plate's channel is alpha, an RGB histogram cannot see it.**

⚠ `h:4062` is load-bearing and its absence is SILENT: every reader of `cfg.h` falls back to
4800, so omitting it mismaps the whole stage rather than throwing. Pinned by an assertion now.

## THE SHIP BOSSES (drop 0810s) — stages 2, 3, 5 and two minibosses

`BOF2_South_Facing_Ships_v1`, cast by Mike: the volcano hull is the lava boss, the ice hull the
ice boss, bottom-right is stage 5, and the two remaining bottom hulls are the stage 2 and 3
minibosses under palette swaps he specified ("fire red", "black/ice blue").

| kind | slot | pattern | what it denies |
|---|---|---|---|
| `infernoreaver` | stage 2 boss | `ember` | a wall of fire with one moving two-column gap |
| `cryospear` | stage 3 boss | `lance` | three lanes, two closed, the safe one rotates |
| `voidbat` | stage 5 boss | `void` | converging Vs from both wingtips |
| `siegeember` | stage 2 mini | `siege` | broadsides left then right — you cross on the beat |
| `thornrime` | stage 3 mini | `rime` | a slow spiral that closes every straight line |

One table (`SHIPBOSS`), one attack function, one draw. **None of the five aims at the player** —
the file already argues for that at `eshot`'s `push()`, and it is what "shmup patterns where I
have to keep myself at certain spots" asks for. All scale by `DIFF.ebSpeed`.

The magma/cryo rigs are **not deleted**, only unassigned, and the glacier rail is deliberately NOT
in `DEAD_SUBBOSS` — it was replaced rather than reported broken, and retiring it would empty
section 105's sectional-damage coverage, which protects machinery other rigs still use.

⚠ **`spawnSubBoss__inner` ASSIGNS the global and returns nothing.** It ends on `subBoss=b;
subBossActive=true;`. `probe_shipboss.py` read its return value and reported both minibosses as
failed spawns; every fixture in `test_fl.js` reads `subBoss` for exactly this reason.

⚠ **`spawnBoss` seeds `maxhp` from the stage, `spawnSubBoss__inner` seeds a flat 100.** One
multiplier across both means two completely different fights — the minis came out at **42 HP**
against the quad-laser's 210. They carry absolute HP now.

⚠ **A palette swap can pass its own numbers and still be wrong.** The first `ice_black` moved
mean hue to 0.55 and saturation to 0.25 — exactly on target — and rendered as uniform gunmetal
slate, dark everywhere and blue nowhere. Value and saturation have to curve in OPPOSITE
directions (`vv**1.9` and `vv**2`) so the hull crushes to black and only the lit edges carry the
ice. **Render the swap; the mean hue will lie to you.**

## THE QUAD-LASER'S BEAMS FIRE NOW (drop 0810s)

The four muzzle anchors were read into `_qlCan` at spawn and used for one thing — a muzzle
flash gated on `b._muz`, **which nothing ever set for this unit**, so even that never drew. The
guns were geometry and a health pool; the fight fell through to the generic sub-boss cases. That
is why shooting the turrets off changed nothing visible.

Each live cannon holds a **fixed vertical lane** and they fire together, so breaking one OPENS
its lane permanently — the arena widens as you earn it. Then the nose runs charge lasers.
`_qlChg` / `_qlChgN` were declared for that in 0801if and **read by nothing**; the charge phase
had never been built.

⚠ `_muz` was only ever decremented for ENEMIES. Any sub-boss setting it would hold its flash
lit for the whole fight. Ticked in `updateSubBoss` now.

⚠ `probe_quadlaser.py` failed all three live cases on its first run and **the game was
right**. It snapshotted the unit's x at setup, but `updateSubBoss` drifts an air miniboss to
WORLD centre, so a stage-1 unit placed at `VW/2`=240 is near 496 by the time it shoots — every
volley read as off by a constant 256. Lanes are computed at FIRE time now.

## ⚠ THERE ARE THREE ART STORES, AND micon_ IS IN THE THIRD ONE (drop 0810r)

This has now cost **three** wrong fixes, so it is going near the top.

    BOFX.img + BOFX.cells   -> XART.rdy / XART.get      (most art)
    ASSETS                  -> ASSETS.has / .blit       (legacy)
    BOFX.icons              -> iconDraw / _iconDrawCell (the 57 micon_ weapon icons)

**`micon_` keys are in NONE of the first two.** Measured: zero `micon_` entries in `BOFX.img`,
zero in `BOFX.cells`. They are 57 `[x,y,w,h]` rects in `BOFX.icons`, indexing the `nia_icons`
sheet, and `iconDraw()` exists to read exactly that. So `XART.rdy('micon_fireorb_3')` can only ever
be false, and so can `ASSETS.has()`.

Mike: "I see your using a basic graphic for fireball icon, Im assuming yuo lost the icons." Nothing
is lost. `drawHUDCustomImg` asked ASSETS, then (after my first wrong fix) XART, and never the one
function that knows — so it drew the text "L3" where the icon belongs. It calls `iconDraw` first
now, with XART and ASSETS behind it.

⚠ **BUT THAT IS PROBABLY NOT THE SURFACE HE IS LOOKING AT.** `drawHUDCustom` (the `nhud_bar` HUD)
returns before `drawHUDCustomImg` ever runs, and it shows the weapon as **pips**, not an icon —
confirmed by rendering it. ~~The world pickups already use `iconDraw` correctly.~~ **THAT WAS
FALSE and it cost two more drops** — the world pickup branch asked `XART.rdy()` for a `micon_` key,
which can only ever be false, so it never drew one in its life. Fixed in 0811m; see
`docs/PASSOVER_0811M.md`. **Every surface must go through `iconBlit`.**

**When art looks "basic" in this project, find out WHICH STORE owns the key before concluding
anything about the art.**

### 0810s — it WAS the equipped box, and it had this bug plus a second weapon table

Mike supplied refreshed fire orb / ice shard tier icons. Rendering the existing ones FIRST
(`docs/proofs/icons_existing_0810s.png`) settled that **nothing was lost** — `micon_fireorb_1..5`
are hexagon tier icons in the same house style. The art was never the fault; the SURFACE was.

The EQUIPPED box lives in `index.html` as its own classic script on its own canvas, and it:

- probed `micon_*` against **XART**, so the candidate was false for every weapon on every frame
  and it silently drew an older `*_icon_*` set. **Its own comment asserted "micon_* DOES NOT
  EXIST. NOT ONE OF THE 30 KEYS THIS ASKED FOR IS REGISTERED"** — which is how the wrong
  conclusion survived three drops. A confident comment is not a measurement.
- kept a **second weapon table** hard-coding `5:'iceorb'`, bypassing `weaponIconKey` entirely, so
  slot 5 could never show the fireball whichever store answered. Measured: stage 3 with the
  fireball equipped drew an ICE icon (`docs/proofs/icons_equipbox_0810s.png`). Drop 0806d fixed
  exactly this in `weaponIconKey`; this surface never asked it.

**`iconBlit(g, key, x, y, h, centred)`** is `iconDraw` into a caller-supplied context — the
reason the box could not simply call `iconDraw` — so both surfaces share one lookup and cannot
drift apart again.

Icon entries may now name their own sheet via a **5th element** on the rect (`_iconDrawCell` read
`'nia_icons'` as a literal, and that is a CELL inside `nca_28`, not a loose file). Every existing
4-element entry is untouched. New art: `assets/game/nia_icons2.png`, refreshing
`micon_fireorb_1..5` and `micon_icebreath_1..5`.

⚠ **The bottom row is ICE BREATH, and 0810s guessed it was a new "ice shard" family.** Mike
named it on the resend: *"heres your fireball and ice breath icoNS i FOUND THEM!"*. It is
Freezer's weapon and the family already existed, so the refreshed art reaches him purely by being
registered under the right name — `weaponIconKey` already routes `w===4` to `micon_icebreath_*`
for him, and for nobody else (Cole's slot 4 stays firewall). The invented `micon_iceshard_*` is
removed rather than left as a phantom family, which is the whole of Mike's atlas complaint in
miniature. Icon cells are back at 57. **When art arrives unlabelled, the family name is a
question for Mike, not an inference.**

## THE ATLAS REORG (drop 0810r) — STARTED, AND IT IS A NAMING PROBLEM FIRST

Mike: "I cant even find the icons on the atlas sheets ... make these atlas's easier to understand,
named properly, and sorted properly ... This is mandatory."

**Measured before touching anything:** 9,726 registered keys, 9,998 cell entries (the difference is
aliases), **86 sheets named `nca_0.png` .. `nca_86.png`, 317 MB**, with no relationship between a
sheet's number and its contents — `tflat_water`, a boss cannon and a pilot portrait share nca_77.

`_BUILD_SOURCE/atlas_reorg.py` is the tool. It is **table-driven, not prefix-guessed**: the game's
own `ENEMY_ART`, every per-stage roster, `STAGES[].boss`, `SUBBOSS[].kind` and `BOFX.mechboss` are
dumped to `assets/data/ART_INDEX_SOURCE.json`, plus the types each stage was *observed* to spawn in
a real 45s run. Run it with no arguments for a dry run; it writes nothing yet.

It already produces the shape Mike asked for — projectiles, missiles, per-stage enemies, **one sheet
per boss** (`BOFX.mechboss` turned out to be twelve separate boss rigs hiding behind `mbXX_`
prefixes), pickups/icons, portraits, ships, terrain, fx, ui.

### ⚠ THE BLOCKER, AND IT IS NOT PACKING

**5,064 of 9,726 keys cannot be classified by name at all — 316 families** like `nhxv`, `ntxl`,
`nvl`, `ovrotor`, `ncyc`, `nmrv`, `nslc`, `nlgt`, `nwf`, `nbs`, `nrmp`, `nsf`, `nel`, `nqv`. They
are not in `ENEMY_ART` and no roster names them.

Repacking those into well-named sheets would produce tidy files full of keys nobody can find — the
complaint would survive the fix. **The reorg needs a NAME MAP for those 316 families before the
repack is worth doing**, and the only reliable way to build one is rule 1: render a mid-reel frame
of each family and identify it. That is the next task, and it is the expensive half.

**Do NOT repack before the names exist.** Packing is a few hundred lines and is reversible; renaming
9,726 keys twice is not.

### Also from 0810r, not yet done
- ~~the stage-7 overlay~~ **done in 0810t**, see above.
- **The two stage-1 sheets are NOT on disk** — they came through as pasted images. They need saving
  as files before they can be used. The second one is the DAM BREACHED variant, which is the
  `cfg.destroyed` master this file has recorded as "RC2 does not ship" since 0801cr.
- `~/Desktop/3dmodel-Ref/CF_WeaponPickupsProjectiles-Vol.2.zip` (505 entries, per-weapon folders
  with pickup + projectile atlases and JSON) is almost certainly where the fireball icons live.
- Purple/white spec and halo cleanup on the new sheets.

## THE stageText FALLBACK RESTORED UI TEXT ACROSS THE WHOLE GAME (drop 0810o/p)

The guard added inside `stageText` for the stage-clear panel turned out to be load-bearing far
beyond it. Comparing the beta sweeps before and after (`docs/proofs/betapass_0810o_all_menus.png`
vs `betapass_0810p_all_menus.png`), text reappeared on:

TITLE (`INSERT COIN`) · DIFF (the difficulty blurbs) · PILOT (name, callsign, bio, FIRE RATE /
ATTACK RANGE) · CAMPHUB (`CAMPAIGN`, the control hints) · STAGESEL (the stage panel) · CREDITS (the
section headers) · STAGECLEAR (title and all nine rows) · CONTINUE (`PRESS FIRE TO CONTINUE`)

All of it was being *requested* and silently dropped, because `stageText` bails to nothing when its
glyph SHEET has not decoded while its glyph MAP has. Any screen that asked for authored text early
in its life drew none. **If a screen ever looks bare, check this first.**

## "THE ENEMIES BROKEN" — EVERY STAGE NOW FIELDS ITS WHOLE WAVE SCRIPT (drop 0810p)

Measured with `spawnEnemy` wrapped over 45s of real play per stage (`scratchpad/refused.py`):

| stage | before | after |
|---|---|---|
| 4 | asked 36, spawned 23 — **13 refused** | 26 / 26 |
| 6 | asked 28, spawned 23 — 5 refused | 26 / 26 |
| 3 | 2 refused | 25 / 25 |
| 8 | 1 refused | 18 / 18 |

**Stage 4 was running a third emptier than its script intended.** The refused names sit in
`spawnEnemy`'s inlined `_DELETE` set because their art resolves ZERO registered keys — the cull is
CORRECT and must stay; un-culling puts back units that spawn, fly, shoot and kill with nothing
drawn. The bug was that the WAVE SCRIPTS still named them.

⚠ **Both obvious repairs are wrong, and the file already records why.** Un-culling reintroduces the
invisible-enemy bug (fifteen reports). Remapping via `DEAD_TYPES`→`'drone'` is the fix Mike
explicitly rejected: *"the units he told me to delete were the ones my fix put back."* So the waves
were repointed at units that EXIST, keeping every wave's shape, count and route:

- stage 4 jets → `s1jetDelta` / `s1jetBomber` (the RC2 military jets)
- stage 6 jets → `s1jetDeltaB` / `s1jetBomberB`, the **black** variants — stage 6 is the night sky
- stage 4 mini tanks → `sandtank`, which 0801im built on the tnkM_ sprites *precisely so Mike's
  deletion of minitank could stand*
- stage 3 minishipA/B → `mdrone` / `frost` from NEF_S3
- stage 8 `el_hd` → `hauler`, stage 8's own live carrier

⚠ **RULE 1 EARNED ITS KEEP HERE.** `ENEMY_ART` aliases `jet1..jet5` onto `air_air1..7`, which
*sound* like the obvious jet replacements. Rendered, they are **alien drone-ships** — round, eyed,
podded — and would have been badly wrong on a military airbase. Render before substituting.

⚠ `DEAD_TYPES` and `liveType` are STILL function-scoped inside `spawnEnemy` and still unreachable
(0801ce measured it and worked around it by inlining `_DELETE` rather than hoisting). They are dead
weight now — the inlined set is the live mechanism. Left alone deliberately: hoisting them would
re-enable the remap-to-drone Mike rejected.

**Stage 9 still fields nothing** — no `buildStagePlan` branch, not in `STAGES[]`. Unchanged.

## DEAD_SUBBOSS IS IN SCOPE NOW, AND THE DRILL TANK IS ACTUALLY GONE (drop 0810p)

`const DEAD_SUBBOSS` sat BELOW `spawnEnemy`'s unclosed `if(base.art===undefined){`, so it was
function-scoped — the trap this file already records for `ARSENAL_DRONES`. Measured:
`typeof DEAD_SUBBOSS` was `"undefined"` at global scope, the guard in `spawnSubBoss__inner` was
permanently false, and **every retired sub-boss still spawned**. Drop 0810m's retirement of the
Obsidian Drill Tank was inert for two drops while its commit said the unit was gone.

Hoisted above `spawnEnemy`. Verified at runtime: `typeof` is `object`,
`spawnSubBoss('obsidiandrill')` returns null, `subBossDone` clears so stage 2 runs on to the Magma
Colossus, and `quadlaser` still spawns.

⚠ **The hoist alone takes the suite from 2,447 to 1,112 with ZERO failures printed** — five
fixtures spawned a retired kind and dereferenced the null. That is rule 3 twice over: the crash
wears a pass, and only the COUNT gives it away. All five now ask `sbRetired(kind)` first, and the
retirement contract is asserted on its own terms instead (reachable / refuses to spawn / clears the
gate / a live kind still spawns / the art stays registered). **Suite 2,443 / 4 failures** — the drop
from 2,447 is 5 added and ~9 skipped, and it is explainable, which is the only kind of count change
worth accepting.

**If you retire another sub-boss:** add it to the table, then run the suite and expect fixtures to
fall over. `sbRetired()` in test_fl.js is the pattern.

## THE BOSS / MINIBOSS GAUGE IS OURS NOW (drop 0810n)

> "The hud and fills, remove and make your own please for all bosses and mini bosses."

`drawHealthBarV2` keeps its name and signature — every call site already lands there, which is the
one change that cannot miss the path that actually runs — and its body is drawn, not blitted: a
bevelled plate, a segmented drain (26 for a boss, 16 for a miniboss), a white DAMAGE-LAG ghost that
trails the true value so a big hit reads as one, and colour carrying the state (green / amber / red,
pulsing under 25%). 168 `nbb_`/`nmb_` keys are off the screen; the art stays registered so reverting
is this one function. Proof: `docs/proofs/boss_gauge_0810n_states.png`.

⚠ **THERE WERE THREE BOSS BARS, not one**, and which one you saw depended on which art had decoded:
the `nhud_bar` block, the `hud_bar` block gated on `XART.rdy('nbb_frame_'+stage)`, and a hand-rolled
red-to-amber gradient with nine dividers in BOTH `drawHUDOverlay` and `drawHUDCustomLegacy`. That is
most of the history of this gauge being reported wrong in a different way each time. All of them
call the one drawn gauge now, and an assertion pins that no HUD path hand-rolls another.

Three assertions that pinned the art bar (clipped fill, per-stage theme, the PINS ITSELF note) moved
onto the behaviour they were protecting: drains by fraction, always draws, takes its space from the
caller.

**Next, in order:**
1. Mike's calls on the Colossus — the duplicate head, and whether the cannon rotation set is worth
   re-fitting to the 384 master canvas to buy back the aim pose.
2. Mike's two calls above on the Colossus (the head, and the fused-form swap).
3. "Almost no minibosses or bosses past level 1 truly work right" — the teleport above was a large
   part of it; the rest needs per-stage checking with `probe_boss.py`.
4. Move 1→2 and 3→4 onto `exitConnectorDraw`; then the 5→6, 6→7, 7→8 outbound joins.

**Waiting on Mike** (both from the beta tester's list, 0812a/b):
- **The barrel roll fires on micro-adjustments.** Tester wants hold/toggle **shift** to suppress it;
  Mike wanted a cooldown. Feel change to core movement — his call on which, not both.
- **A `%` in the BOF face.** There is none in any of the eight BOF sheets; the stats screen borrows
  stage 2's molten one, tinted to match. Authored art, so his call. `§217` pins the borrow and will
  fail the moment a real one exists, which is how it gets removed.

Still owed from the tester's list, no decision needed: the miniboss that is still a hitbox square
(stage not identified), the stage 8 boss (4 forms, same pattern, very tanky), signs that scroll
when told not to, and a waterfall in the middle of the road.

**The `o.px` camera fix (0810c), for the record.**
`outboundStart` captures `o.px = player.x`, which is a **world** coordinate, and all three
`outboundDraw*` functions draw the held player at `o.px` in **screen** space with no `camX`
translate. On an 800-wide stage that puts the ship up to 160px off where it was when the boss
died. It is the same class of bug as the launch seam (0810a) — world coords drawn through no
camera — but 1→2 shipped this way and Mike has signed it off, so the fix is his call, not a
silent correction. If he wants it: subtract the `camX` that was live at `outboundStart`, captured
alongside `px`/`py`, rather than the current `camX`, which keeps drifting after the handoff.

⚠ **The bosses are being wired in another chat in this same tree.** Nothing has been committed
there since `73b3009`, but check `git log` before touching boss code.
