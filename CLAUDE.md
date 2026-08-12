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

## Current state (2026-08-11)

Suite: **2,442 assertions / 218 sections / 5 failures** — all five pre-existing at HEAD: the boss
limb pool, the preload count, the two `_superseded` ones and the naval flash families.
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
- Jets: observed speed varies 96–138 even on `straight`; something outside `jetTick` displaces
  them. A rescale inside `jetTick` does not fix it — the other mover runs after.
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
- **Stage 5 is the only stage above 0.01%** (0.636%). Not diagnosed.
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

**Still not done: the boss/miniboss HUD replacement** (handoff section 3, "The hud and fills, remove
and make your own please"). The `nbb_`/`nmb_` art fills are still what draws, through
`drawHealthBarV2`. ⚠ `drawHUDCustom` returns early and only `drawHUDCustomImg` reaches the boss
gauge — whatever replaces it must be reachable from the path that actually RUNS, and given the
above, prove that with a frame diff rather than a blit count.

**Next, in order:**
1. **The boss/miniboss HUD** — the last unbuilt piece of the 0810i brief.
2. Get a repro from Mike for level 2's miniboss.
3. Move 1→2 and 3→4 onto `exitConnectorDraw`.
4. The remaining themed outbound joins — 5→6, 6→7, 7→8 (4→5 stays blocked on the stage-4 boss).

**Waiting on Mike:** nothing outstanding. The arsenal-mini questions are answered (they are
enemies we have; caldera 2 / frostbite 3 / dambreaker 4) and the `o.px` camera fix was approved
and shipped in 0810c.

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
