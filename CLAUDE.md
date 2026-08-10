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

**State declared inside `spawnEnemy`'s unclosed `if` is re-initialised on every spawn.** A `let`
there is not module state — each wave spawn gives you a fresh one. Anything that must persist
belongs with the pools at the top of the file.

**`_selfPat` gates whether a pattern survives.** A unit not listed there has its pattern
overwritten by a later block. Drive it from a table, never hand-list.

**Assertions can defend a bug.** One required `ship_<pilot>_t` under a comment calling it "the
flameless airframe" — it is the flame-BAKED one. Another pinned the exact stats-screen coordinates
Mike had asked to be replaced. When an assertion fails after a deliberate change, read it before
fixing the code.

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

## Current state (2026-08-10)

Suite: **~2,393 assertions / 215 sections / 2 failures**, both `_superseded` (see below).

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
- The dam swap is wired and data-driven (`cfg.destroyed`) but points at no art. RC2 ships no
  destroyed COMPOSITE for stage 1, and its dam objects do not match the dam painted into the
  plate — template-matched at six scales, all noise. The real fix is drawing stage 1 as
  Background + placed Objects the way RC2's README intends, which would also give the damaged and
  breaching states mid-fight.
- The pilot-card hint row renders ENTER as "BNTBR" — every `E` in that face resolves to the `B`
  glyph. The map looks sequential (A→g00 … E→g04) and only E is wrong, so it is not an offset.
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

**Next:** the stats-screen alignment; the `E`→`B` glyph in the hint face; camo schemes for stages
2–3; and cinematics — `CF_PilotArcadeIntros`, `CF_PilotCutscenePack` and `CF_FuryHQCutscenes` are
extracted in `_ART_SOURCES/` (224 files) and entirely unwired.
