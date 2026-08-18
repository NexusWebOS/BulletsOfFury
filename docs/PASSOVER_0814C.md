# DROP 0814C — ITEMS 6, 7 AND 8: A PLACEHOLDER ROUND, A FROZEN ARENA, AND A FADE ONLY ONE STAGE HAD

Three of Mike's items, and all three turned out to be a system that was built once and never
reached the places that needed it.

---

# 1. ITEM 8 — ONLY STAGE 1 HANDED ITS BOSS OVER TO THE EXPLOSION

> Bosses do not die into explosions - they should vanish with the explosion taking over.
> **Only stage 1 does this.**

The death SET-PIECE was never the problem. `updateBoss`'s dead branch runs **9.4 seconds** of
scaled blasts, falling debris, screen shake and the whiteout, for every boss on every stage.

What only stage 1 had was the other half: **a draw that gets out of the way.**
`drawBossSprite`'s `damkeeper` branch fades the hull between 1.8s and 2.6s and chars it toward
black on the way. `shipBossDraw` (stages 2, 3 and 5 — the ships Mike cast himself), `mechDraw`,
`sxDraw`, `genesisDraw` and `drawModularBoss` have **no `b.dead` handling at all**. They draw an
intact hull at full opacity for the whole nine seconds, so the boss sits inside its own explosion
instead of being consumed by it.

⚠ **AND `drawBossSprite` ALONE HELD FOUR COPIES OF THE FADE, ON TWO DIFFERENT CURVES** — 1.8→2.6
in two branches and 2.6→4.1 in the other two, charring at 0.30 against 0.26. Every one of them
was written to do the same thing.

`bossDeathAlpha(T)` / `bossDeathChar(T)` are that curve, once. The fade is applied at **`drawBoss`,
the single entry point** — five rigs that each remember to fade is five that can forget, and a rig
added later would arrive with the bug already in it.

⚠ **`_bossFade` IS PUBLISHED BECAUSE A HANDFUL OF DRAWS HARD-SET `globalAlpha = 1`.** Those lines
mean "back to normal", and normal is no longer 1 once the boss is dissolving. Audited: four sites
in the boss paths, three of them after the hull is drawn (harmless), one inside genesis's piece
loop (repointed at `_bossFade`).

## ⚠ AND STAGE 8'S BOSS DID NOT FADE — IT CEASED TO EXIST

Measured: on stage 8 the VILE boss issues **zero `drawImage` calls on the frame after it dies.**

`drawBoss` gated the modular path on `boss.modular && !boss.dead`. The comment four lines above it
describes that exact bug — *"This was gated on !boss.dead, so the moment a sectional boss died it
fell out of the modular path and drawBossSprite picked up the LEGACY body art"* — and 0724bx
applied the fix to the `_ship` branch and **not to the branch the note is about**. Stage 8 has no
`bset` and no legacy plate, so it landed on the vector fallback and the boss vanished the instant
it was killed: no dissolve, no wreck, nothing for the explosion to consume.

That is the sharpest possible version of Mike's item, and it was one stage away from the thing
being fixed.

## Measured — `probe_bossfade_0814c.py`, all eight stages, real Chromium

`ctx.drawImage` is counted **only for the duration of the `drawBoss()` call**, so the figure is
the boss's own contribution and nothing else's.

| stage | boss | t=0.5s | t=3.0s | FX still live |
|---|---|---|---|---|
| 1 | damkeeper | 3 | **0** | 254 |
| 2 | infernoreaver | 1 | **0** | 304 |
| 3 | cryospear | 1 | **0** | 271 |
| 4 | glacierfortress | 1 | **0** | 321 |
| 5 | xenoregent | 1 | **0** | 315 |
| 6 | doomsdaycarrier | 1 | **0** | 471 |
| 7 | sludgeemperor | 1 | **0** | 363 |
| 8 | vileexistence | 1 | **0** | 275 |

⚠ **THE "FX STILL LIVE" COLUMN IS THE POINT, NOT DECORATION.** "0 boss pixels" is also what a
frozen game looks like. The live explosion count is what separates *the explosion took over* from
*nothing is happening*.

⚠ **AND MY FIRST RUN REPORTED STAGE 8 AS REFUSING TO DIE. THAT WAS THE PROBE.** It killed bosses
with `boss.hp=0; hitBoss(1)`, and `hitBoss`'s first lines are `if(boss.modular){ modularHit(dmg);
return; }` — it returns **before** the `hp<=0 → bossDie()` check, because a modular unit dies when
its parts are ruined, not on a pool. `dead` stayed false and `dying` stayed 0 forever, which the
probe reported as a stage-8 game bug. The game's own force-kill is `boss.hp=0; bossDie();`.
⚠ **AND THE UNCAPPED STEP LOOP TURNED THAT INTO A HANG** — the whole probe timed out with no
output, i.e. it presented as a broken harness rather than as a finding. It is bounded now and
reports `STALLED` explicitly.

---

# 2. ITEM 6 — EVERY SHIP BOSS IN THE GAME FIRES TWO FLAT CIRCLES

> Stage 2 boss projectiles - Mike calls them **awful**.

`_shipShot` is the muzzle for **every pattern of every ship boss and ship miniboss** — ember,
lance, void, siege, rime, mslfan, beamfan; infernoreaver, cryospear, voidbat, siegeember,
thornrime, lavamaw, magmaward, sludgeemperor. It pushes `kind:'eshot'`.

**There is no `eshot` in `FIRETYPES` and none in `PROJ`.** So every one of those rounds fell
through the entire draw chain to its last rung:

    else if(ASSETS.has('ebullet')) ASSETS.blit('ebullet', b.x, b.y, 12, 11);
    else { fillStyle='#ff5a2a'; circle(3.4); fillStyle='#ffd36b'; circle(1.6); }

`ebullet` is **not a registered key**, so it is the second line: two flat vector circles, one
size, one colour, no animation, no rotation, no stage identity — in a game holding 252 authored
`mfx_` projectile cells and five authored pellet colour families.

That is the whole of "awful", and **it is not a stage-2 problem**: stage 2 is simply where Mike
met it.

Routed through `pellet` (`deriveFireType('eshot','pellet',{h:18})`), which is the type built for
this round and already solves the three things a hand-drawn circle cannot:

- `mfx_mg_<fam>_0..4` is an authored **birth sequence**, driven monotonically off `b.t` (0811y)
  rather than a wall clock, so it grows into a flame instead of strobing between shapes
- the family comes from `PELLET_FAM[run.stage]`, so the round is **the colour Mike already chose
  for that stage** — 0813a set stage 2 to family 2 precisely so it stopped firing red on the lava
- the glow follows the plate, because `pellet`'s glow is a function of the family

⚠ **THE CANDIDATES WERE RENDERED BEFORE ONE WAS PICKED.** `flare` (`mfx_ea_3_*`) was the obvious
alternative and the contact sheet disqualified it: frames 0–4 are a round bead and 5–7 are thin
vertical streaks, so cycling it swings the shape — 0811y's blob-vs-streak trap exactly.
⚠ **`h:18` AGAINST THE PELLET'S 16 IS MY CALL, NOT MIKE'S.** A boss round should read heavier
than a strafer's. One number.

---

# 3. ITEM 7 — THE LAVA WAS BOILING ON THE SPOT

> Stage came sliding in instead of the lava continuing. Needs a **constant-scrolling lava
> section** for the fire boss.

**This corrects 0813x, and the part it corrects is the solution, not the diagnosis.**

0806f made the stage-2 boss fight happen over open lava: the master stops being drawn and the
animated bed underneath becomes the arena. 0813x read Mike's follow-up (*"anyway to have that
floor render back in by scrolling downward once the fight starts?"*) as a request to bring the
TERRAIN back, and slid the whole master down into frame over 1.6s. He has now seen it and named it
exactly: **the stage came sliding in**.

⚠ **WHAT HE IS POINTING AT IS THAT THE LAVA STOPS.** `_bossHold` pins `mapScroll` the moment the
fight starts — correctly, so the player cannot outrun the boss — and the bed is drawn at
`drawAnimTerrain(frames, mapScroll, …)`. So the lava kept **cycling its frames while travelling
nowhere**. A dead-still arena is what made the open corridor read as broken, and sliding the
mountain back over it was treating the symptom.

The bed has its own clock now. `mapScroll` stays held; `_arenaLavaScroll` advances at
`ARENA_LAVA_SPD` (40 px/s — the level's own rate, so entering the arena is continuous rather than a
change of pace).

⚠ **THE `_gen || _mech` GATE GOES WITH THE SLIDE.** 0813x added it because the only justification
it could find for open lava was a boss RISING out of it, and the Inferno Reaver does not — so a
ship boss got the slide instead. Mike has now said plainly that the **fire boss** is the one who
wants the open lava, so the requirement belongs to the ARENA, not to the unit. The riser case is
unaffected: it needs the same open surface and now gets it unconditionally.

## Measured — `probe_stage2arena_0814c.py`

    ITEM 6   enemy bullets on screen : 16
             authored mfx_ keys asked: mfx_mg_2_2, mfx_mg_2_4     <- stage 2's own family
             raw ctx.arc in the pass : 0                          <- the circle fallback is dead

    ITEM 7   level scroll over 4s    : +0.0 px    (held by the fight)
             lava  scroll over 4s    : +160.7 px  (= 40px/s x 4s, exactly)

`docs/proofs/stage2arena_0814c.png` — the Inferno Reaver over a full arena of flowing lava, firing
authored flame rounds.

⚠ **THE ARC COUNT IS SCOPED TO THE BULLET PASS, NOT THE FRAME.** The HUD, the gauge and half a
dozen FX draw arcs every frame; a whole-frame count never reaches zero and means nothing.
⚠ **AND IT ASSERTS THE FALLBACK IS GONE, NOT JUST THAT GOOD ART APPEARED.** Those are different
claims — the chain could resolve authored art for some rounds and still drop others onto circles,
which is what a partial fix looks like and is invisible if you only check that `mfx_` was asked for.

---

# 4. TWO HARNESS FAULTS AND ONE REAL FRAGILITY, ALL FROM THE SAME LINE

⚠ **`drawWorld` TAKES `dt` AS A PARAMETER AND I CALLED IT BARE.** `mapScroll + undefined*40` is
NaN, and NaN propagates: every later frame stays NaN, the master maps nowhere and the level simply
stops — nothing thrown, nothing logged. The probe printed **"lava scroll: +nan px  OK"**.

Three separate things came out of that one mistake:

1. ⚠ **NaN COMPARES FALSE AGAINST EVERYTHING, SO IT PASSED EVERY CHECK.** A probe that cannot fail
   on a broken number is not measuring one. It rejects NaN explicitly now.
2. ⚠ **THE SCROLL LIVES IN THE DRAW, NOT THE UPDATE.** `mapScroll` is advanced inside
   `drawLevelMaster` (and now the lava clock beside it), so a fixture looping bare `updatePlay`
   measures **both** as +0 and reports the lava as dead. That is the shape of this engine, and the
   suite fixture had to drive `drawWorld` too. It is worth knowing before writing any scroll test.
3. **`drawLevelMaster` now refuses a bad `dt`** (`if(!(dt>=0)) dt=0;`). Same class as the `stateT`
   clamp at the head of `loop`, and the same fix: reject at the boundary rather than let it spread.

---

# 5. VERIFICATION

    suite    2,661 ok / 5 failures  — the five long-standing ones
    pixels   probe_bossfade_0814c.py     8/8 stages
             probe_stage2arena_0814c.py  items 6 and 7 both green

⚠ **TWO 0813x ASSERTIONS PINNED THE FIX MIKE JUST OVERRULED**, and both described 0813x's
SOLUTION rather than the requirement:

    "gated on the BOSS type, a gunship boss keeps its floor"   -> he does NOT want the floor
    "the floor travels back down into frame"                   -> that IS the sliding stage

Repointed onto what he actually asked for, and made **behavioural**: the lava scroll advances by
more than 50px across 180 frames while the level's advances by less. That is measurable; a source
grep for `ARENA_FLOOR_HOLD` was not.
