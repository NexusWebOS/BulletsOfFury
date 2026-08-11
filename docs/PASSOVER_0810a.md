# PASSOVER 0810a

    verify_0730a   454 passed /  6 failed      (was 311/17 — and that 311 was a TRUNCATED run)
    test_fl       2094 passed /  2 failed
    both files parse · gamecode.js back-ported and symbol-checked

**Read `HARNESS_TRIAGE.md` before you trust any harness number in this project.**

---

## 0. DO THIS FIRST ON THE MAIN PC

1. **Re-run both harnesses.** Five of the six `verify` failures and both `test_fl` failures are
   `_chroma_backup/`, `_superseded/` and `_halo_backup/` — working folders that live on the MAIN
   machine and are not in this tree. They should go green there with no code change.
   **If any of them still fails on the main PC, that is a real finding** — it would mean a backup
   genuinely went missing rather than being on the other box.
2. **Play `COLE1`, `COLE2`, `COLE3`.** Almost everything below is feel work that assertions cannot
   settle, and none of it has been played.
3. **Stage 3 with the ice orb at level 5** — that is the one I most want eyes on. See §4.

## 1. TRANSITIONS

`2 -> 3` (lava -> ice) and `3 -> 4` (ice -> sky -> town) are built, live, per-join enabled.
`1 -> 2` was already there. `4 -> 5` is the boss chase and stays blocked on the stage-4 boss.

**The TRANS table was keyed by DESTINATION and read by SOURCE.** Every entry from 2 on described
the wrong join — `TRANS[2]` said "water into lava, arriving at the volcano" when stage 2 IS the
volcano. Re-keyed, with the old bug pinned as a guard. Details in `TRANSITIONS_STEP3.md` / `STEP4.md`.

## 2. ENEMY BEHAVIOUR — the contract

Every arsenal unit now runs **TELL → COMMIT → RECOVER**, with the **aim locked at the start of the
tell**. That last part is the whole fairness contract: `droneFire` used to solve the aim at the
instant the bullet spawned, so an aimed shot tracked you to the muzzle and no move beat it. In a
one-hit game that is an unavoidable death, not a difficulty.

Because the art cannot telegraph — every drone is a 4-frame idle loop, no fire pose — the tell
rides the glow ramp and the unit's own change of MOTION. That is Contra's trick, and it is the only
channel available.

**`stageHeat()`** ramps a level 0 → 1, S-shaped: tells compress toward the floor, cooldowns tighten
~35%, and past half-heat units double-tap off one tell. Floors hold at the worst case the game can
produce (FURIOUS, end of stage): 0.35s tell, 0.40s recover.

Built: **level 2** (cinderwasp / basaltbomber / magmaorb), **level 3** (sharddart / cryoeye /
glaciercarrier), **level 5** (fractureskimmer / nullprism / ragetalon / deathchoir / furymine), and
the **arsenal mini tier** (caldera → 2, frostbite → 3, dambreaker → 4).

Full design and rationale in `ENEMY_BEHAVIOUR.md`.

## 3. FIVE DEAD SYSTEMS FOUND

Each looked wired and did nothing:

* **`ARSENAL_MINIS`** — declared at brace depth 2 INSIDE `spawnEnemy`, so nothing could consume it.
  None of the three minibosses could spawn. Hoisted. `ARSENAL_DRONES` / `arsenalDroneArt` /
  `arsenalDronesFor` were stranded in the same block.
* **`DEAD_SUBBOSS`** — same scoping trap, read from `spawnSubBoss`. Guarded with
  `typeof DEAD_SUBBOSS!=='undefined'`, which is what made it SILENT: always false instead of a
  ReferenceError. **OVERLOAD REACTOR has been spawning on stage 4 the whole time it was "retired".**
  Stage 4 genuinely has no sub-boss now.
* **`furymine`'s attack** — set `_mineArmed=1`; one write, zero readers. The unit hung in the air
  and never fired, exploded or threatened anything.
* **`warmStage` step 4** — its header promises it warms "the art for every enemy type in its plan"
  and the step was simply absent (the numbering was reused, so the gap read as a renumber). Every
  enemy sprite was still cold when the first wave spawned, which is the "appearing out of thin air"
  pop-in.
* **`micon_*` weapon icons** — ZERO keys exist. The EQUIPPED box has never drawn an icon. Still
  open: needs art. See §5.

## 4. FIRE / ICE — the FPS bug

**Two root causes, both measured in the running game, both fixed.**

    ctx.shadowBlur per shard   107ms of a 123ms frame (87%)   ->  8fps became 64fps
    a particle leak            10,000 particles, capped, never expiring (91% of the frame)

The engine already had `bakeGlow`/`drawMfx` written for exactly the shadowBlur problem, with a
comment calling it "the single most expensive canvas op in a browser". The shard and orb layers had
never been routed through it. They are now.

Also corrected, per your note: **fire shards draw `fshard_*`** (14 frames that existed and were
referenced once in the whole engine) instead of the fireball's flame reel squashed to 17px, and
**ice shards draw `iceshard_*`** instead of the frozen ORB squashed down.

Real load — holding FIRE, the weapon's own `maxOrbs` gate enforced — is **2 orbs, 289 shards,
median 3.9ms (256 fps)**.

> ⚠ I told you "450+ shards" and you reacted to it. That figure was my benchmark bypassing the
> weapon's 2-orb cap, not the game. I then tested halving the count at equal damage: **it moves the
> median by 4%.** Cutting the spray would cost the weapon its look for nothing, so `shardN` is
> untouched. Detail in `FIRE_ICE_FIX.md`.

**`index.html` pointed at `assets/fonts/BlackOpsOne.ttf`, a folder that does not exist.** The font
never loaded, so all 145 `BOFmil` draw calls fell through to Courier. Fixed — every label in the
game will look different, and that has not been seen by anyone yet.

## 5. STILL OPEN

* **`micon_*` weapon icons do not exist** — needs art, not code. The EQUIPPED box draws its frame
  and nothing else, verified live at 0 lit pixels.
* **`gamecode.js` reconciliation.** It has genuinely diverged from `assets/game.js` in the
  stage-update region; back-porting cost four attempts this drop. The 0805a stale-source guard
  exists for exactly this. Best done on the main PC where you can rebuild and test.
* **`4 -> 5` boss chase** — blocked on the stage-4 boss.
* **Dead code, safe to delete when you want it gone:** `flamePair()` (defined, called from
  nowhere, and its comment references a `_flameRaw` that does not exist), and 14 orphaned
  `nep_`/`nbp_` projectile keys, all level 9.
* **Level 1's miniboss** is still the quadlaser, untouched, per your note about dambreaker.

## 6. WHERE I WAS WRONG THIS DROP

Recording these because each one nearly shipped as a false conclusion:

* Reported "450+ shards" — was my harness exceeding the game's own cap. Real ceiling 289.
* Reported three "real gaps" from the harness triage. **Two were wrong**: the supply-box RNG exists
  (I searched for `_r<0.50` and the variable is `r` — my own regex confirmed my error), and the
  flamethrower fallback is unnecessary because the composite it guarded was deleted outright.
* Reported the entrance sweep as done. It went into `droneTick`, which runs only for ARSENAL
  drones — and stage 1 has none, so the level the complaint came from never got it. Fixed in §2.
* Claimed the backup folders were "excluded when the build was zipped". They are on the main PC.
* Nearly reported a bullet-vs-lava readability problem that does not exist: the answer flips
  entirely on which luminance statistic you pick. Measured properly, the pellet reads on every
  stage. See `ENEMY_BEHAVIOUR.md` §4f.

The common thread in almost all of it: **matching source TEXT instead of running the thing.** Every
false failure in the harness triage was a string match that broke on a rename or a growing function.
