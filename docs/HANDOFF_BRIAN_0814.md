# BULLETS OF FURY — PATCH NOTES FOR BRIAN

**Supersedes `Updates_Notes4Brian-Love you booboo.pdf` (main @ e8f8e62).**
Everything below is on `main`. Three drops: **0814a, 0814b, 0814c**.

---

## MIKE'S LIST — 6 OF THE 8 OPEN ITEMS ARE CLOSED

| # | item | state |
|---|---|---|
| 1 | Freezer picks up flamethrower but uses ice breath — they are SEPARATE attacks | **DONE** 0814a |
| 2 | Fire orb and ice orb keep swapping icons, and fire randomly one or the other | **DONE** 0814a |
| 3 | fireiceorb fires a basic fireorb | **DONE** 0814a |
| 5 | Stage 1 does not move the camera to the blown-up dam | **open** |
| 6 | Stage 2 boss projectiles — "awful" | **DONE** 0814c |
| 7 | Stage came sliding in instead of the lava continuing | **DONE** 0814c |
| 8 | Bosses do not die into explosions; only stage 1 does | **DONE** 0814c |
| 10 | Still using plain dialogue where the game has its own boxes | **DONE** 0814b |

Plus, not on his list and not started: **level 9 reached through level 5**, the full-size
cutscenes, and the stage-9 bonus/portal packs.

---

## THE SHAPE OF ALL SIX FIXES IS THE SAME

Not one of these was missing art, and not one needed a new system. In every case the thing Mike
was asking for **already existed and was unreachable from the place that needed it**:

- **items 1–3** — `weaponVariant()` answers *"what should the next crate dispense"*. Every runtime
  surface was asking it *"what am I holding?"*. The pickup's variant was baked at spawn and thrown
  away on collect. One missing record, three symptoms.
- **item 10** — 0811m built exactly the dialogue panel Mike wants, **inside `storyDraw`**, where
  nothing else could call it. Two other surfaces went on drawing faux boxes.
- **item 8** — the 9.4-second boss death set-piece runs on every stage. Only stage 1 had a DRAW
  that gets out of the way.
- **item 6** — `kind:'eshot'`, what every ship boss fires, was in neither projectile table, so it
  fell through to two flat circles while 252 authored projectile cells sat in the manifest.
- **item 7** — the lava was already the arena; it just never moved, because the fight pins the
  scroll the bed is drawn against.

**Grep for the consumer, not the definition.** That is the single highest-value habit on this
codebase, and every drop this session found another instance.

---

## 0814a — ITEMS 1, 2, 3

`heldVariant(w)` / `run.wvars[]` records what the pilot is actually carrying; `weaponVariant` is
the fallback only.

- **"keep swapping icons"** — `drawPowerups` called `weaponIconKey` with no variant, **once per
  frame**, re-rolling `Math.random()`. A falling crate genuinely alternated between the
  flamethrower and ice-breath icons at 60Hz. The comment above `WVAR_NAME` predicted this exact
  failure in 0812l and no call site honoured it.
- **"fire randomly one or the other"** — `orbIsFire()` was `run.stage===3`, so the same orb was
  fire on 3 and ice on 4 with no pickup involved.
- **flamethrower ≠ ice breath** — `flameIsIce()` was `_pilotKey()==='freezer'` unconditionally.
  Ice breath is exclusive to Freezer from stage 2 (proved: 9 stages × 8 pilots × 200 rolls, zero
  leaks). Stage 3 no longer withholds the whole slot — that also took away the flamethrower
  `freezerL3Begin` hands him off the magma mech, a beat that had been coming out as frost against
  its own narration.
- **the fire-ice orb had no projectile.** `nts_` is a complete authored thermoshock weapon — **45
  keys, zero references anywhere in game.js**: a 12-frame split fire/ice ball, four flame shard
  plates and four frost ones, an 8-point burst star that IS the eight-way discharge specified back
  in 0801fj, a charge reel, a release ring, an impact.

**Also found:** the orb and its shards have **never** taken the elemental bonus — `attackElement`
has answered for them since 0801fn and nothing ever asked it. **This raises orb damage on stages 2
and 3.** A declared rule finally firing, but Mike should see it. Thermoshock at 2× on both is my
call, not his.

**Also found:** the 0810a particle leak is back in `assets/game.js` — the expiry test sat below two
branches that draw and `continue`. `FIRE_ICE_FIX.md` records it as fixed; it crossed to
`gamecode.js` and not to the authoritative file.

---

## 0814b — ITEM 10

`dlgBox()` is `storyDraw`'s panel lifted out unchanged. `storyDraw` is nine lines now; `thawDraw`
and `freezerL3Draw` use it. Two dialogue renderers again, not three: `drawCommWindow` is the modal
one, `dlgBox` the in-play one.

Before, measured: thaw **0 authored panels / 16 faux rects / 32 canvas fillText / 0 BOF glyphs**;
freezerL3 **0 and 0** — there was no box of any kind, not even a bad one.

**Then the counters went 4/4 green on a picture that was wrong three ways**, which is the part
worth reading:

1. the text ran off its rail (196×96 was sized for canvas BOFmil; the BOF face is far wider)
2. two panels stacked on stage 3 — the thaw fires for everyone, freezerL3 on the same stage for
   Freezer. Invisible while both were small faux boxes in different corners
3. bottom-right is spoken for — the panel ran **under** the EQUIPPED box. **The overrun check said
   0 and was right: occlusion is not overrun**, and only the picture distinguishes them

The probe now re-measures every drawn line against the rect `drawPanel` was handed, counts distinct
panels, and intersects them with the EQUIPPED corner. **Run against the pre-drop tree it fails 3 of
4** — the fourth is the control.

---

## 0814c — ITEMS 6, 7, 8

- **item 8** — one fade curve (`bossDeathAlpha`), applied at `drawBoss`, the single entry point.
  `drawBossSprite` alone held four copies on two different curves. **Stage 8's boss did not fade,
  it ceased to exist**: `drawBoss` gated the modular path on `!boss.dead` and the 0724bx note four
  lines above describes that exact bug — the fix went to the `_ship` branch, not the branch the
  note is about. All 8 stages measured: solid at 0.5s, **zero draw calls at 3.0s**, explosion
  still running.
- **item 6** — `deriveFireType('eshot','pellet',{h:18})`. Authored birth reel driven off `b.t`,
  family from `PELLET_FAM[run.stage]`. Measured on stage 2: 16 rounds, `mfx_mg_2_*`, **0 arcs**.
- **item 7** — `_arenaLavaScroll` at 40 px/s while `mapScroll` stays held. Measured: level **+0.0
  px** over 4s, lava **+160.7 px**. The `_gen||_mech` gate is gone — the open lava is the arena's
  requirement, not the unit's.

---

## TRAPS — EACH OF THESE COST A CYCLE THIS SESSION

**`spawnEnemy`'s unclosed `if` — ask the engine, not the source.**
`node _BUILD_SOURCE/probe_scope_0814a.js <name> ...` reports `typeof` at global scope using
test_fl's own vm. It correctly identifies `liveType` as swallowed. It also reports
`ARSENAL_DRONES` as GLOBAL, contradicting CLAUDE.md — **re-measure that note rather than quoting
it.**

**`drawWorld` takes `dt`. Calling it bare makes `mapScroll` NaN**, silently and permanently — NaN
propagates, the master maps nowhere, the level just stops. Nothing thrown, nothing logged.

**NaN compares false against everything**, so the probe printed `+nan px  OK`. A probe that cannot
fail on a broken number is not measuring one.

**The scroll lives in the DRAW, not the update.** `mapScroll` is advanced inside
`drawLevelMaster`, so a fixture looping bare `updatePlay` measures it as +0 and reports the level
as dead.

**`hitBoss` cannot kill a modular boss** — `if(boss.modular){ modularHit(dmg); return; }` returns
before the `hp<=0 → bossDie()` check. Force-kill is `boss.hp=0; bossDie();`.

**`updateBullets` is not a name in this engine.** The player-bullet loop is inline in `updatePlay`,
so a bullet test needs a live stage under it.

**A quantity that is consumed cannot be measured after it is gone.** The thermoshock ray test flew
the ball 200 frames then read `pBullets`, which is correctly EMPTY by then, and called that "no
rays fired".

**A fix that adds ordering breaks every test that assumed there was none.** After the dialogue
queue landed, the freezerL3 probe case measured zero panels and read as a regression. It was the
queue working.

**Colour-classifying a band of the canvas measures the LEVEL, not the thing.** The first weapon
probe reported **143,194 warm pixels with ICE BREATH equipped** — the stage-2 desert — and failed
on correct code. Sample the PLATE the draw path asked for, alpha-masked, instead.

**Render before you substitute.** `flare` was the obvious pick for the boss round; the contact
sheet showed frames 0–4 are a bead and 5–7 are streaks, so cycling it swings the shape.

**Assertions that pin a LINE rather than a RULE.** Four hit this session:
- `indexOf("'port_'+thaw.pk+'_smile'")` failed on code where the pilot beat still uses the smiling
  portrait
- `weaponVariant(4)===null` on stage 3 was pinning a *limitation* (you could not withhold ice
  breath without withholding the flamethrower) rather than Mike's rule
- two 0813x arena assertions described 0813x's **solution** rather than the requirement, and Mike
  overruled the solution

All four are behavioural now.

---

## HOW TO VERIFY

    node --check assets/game.js                          always, after any edit
    node _BUILD_SOURCE/test_fl.js                        2,661 ok / 5 failures / ~10 min
    node _BUILD_SOURCE/probe_scope_0814a.js <names>      is this identifier really global?

    python _BUILD_SOURCE/probe_weaponid_0814a.js         items 1-3, state      (node)
    python _BUILD_SOURCE/probe_weaponid_0814a.py         items 1-3, pixels
    python _BUILD_SOURCE/probe_dialogue_0814b.py         item 10
    python _BUILD_SOURCE/probe_bossfade_0814c.py         item 8, all 8 stages
    python _BUILD_SOURCE/probe_stage2arena_0814c.py      items 6 and 7

**The five suite failures are the long-standing ones** — preload count, two `_superseded` ledger
checks, the volley round count, the flash families. More than five: check `git status` for deleted
art before debugging anything.

**Zero failures can also mean a crash.** Check the assertion COUNT.

**A green suite proves state, not pixels.** Every drop here has a `.py` probe that drives real
Chromium, and each one found something the state checks could not see.

---

## STILL OPEN

- **#5 — the stage-1 dam.** Read CLAUDE.md's note first: there are TWO dams, `ndam_*` is OBJECT
  art (222×290, four staged variants) and does **not** overlay the dam painted into the plate —
  that was template-matched and disproved, do not repeat the test.
- **level 9 through level 5** — no mechanism yet. Stage 9 has a `_levelCfg` case and a connector
  entry but **no `STAGES[]` entry**, so `beginStage(9)` has no `curStage`.
- **the new packs** — `CF_StoryCutscenes-Vol.1`, `CF_FuryHQCutscenes-Vol.1` (full-size cinematics),
  `CF_Stage9BonusPack-Lvl9`, `CF_Stage9PortalCombatPickups-Lvl9`. Untouched.
- **the apostrophe renders as a comma** in dialogue ("LET,S"). The glyph resolves, so it is not the
  missing-punctuation case. `glyphBox` bottom-aligns every glyph and 0809q's `FONT_DESC` has no
  counterpart for top-hanging marks. ⚠ **Do not write that table from the argument** — rendered,
  `p39` and `p44` are both carved slabs and which way up each sits is not readable off the plates.
  One render settles it.
- **orb damage on stages 2 and 3 is higher** now that the elemental multiplier reaches it. Mike's
  rule, but he has not seen the numbers.
