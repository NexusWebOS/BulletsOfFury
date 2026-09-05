# PASSOVER 0905 — SpriteCook goes live, Mike's 17-item list closes, and the carrier gets six phases

Fourteen drops, `0905g` … `0905t`, all on `main` and pushed. **Read `CLAUDE.md` first** — its three
rules are the reason most of today went the way it did, and several new traps were added to it.

---

## READ THIS FIRST: what went wrong today was almost never the code

Nine of the day's real defects were **measurement errors, not bugs** — and in four cases a
measurement told me something confidently false that I then reported as established. If you take one
thing from this document, take this section.

⚠ **A PROBE THAT PASSES ON A KEY IS NOT A PROBE THAT PASSES ON PIXELS.** The laser alert sign was
drawn, on screen, correctly sized, and INVISIBLE through three green probes: one asserted the draw
asked for the art key (true, and worthless); one counted "red pixels" that were the RIME WALL name
text; one trapped `ctx.drawImage` and caught nothing because **`ctx` carries its OWN `drawImage`**
that shadows `CanvasRenderingContext2D.prototype`. Trapping the own property found 26 blits at
exactly the right coordinates. The cause was draw ORDER — it ran before the hull, which painted over
it. Only a screenshot ever found it.

⚠ **SAME-STATE FRAME ISOLATION DOES NOT EXIST IN THIS RENDERER**, and CLAUDE.md already said so
(the draw reads `performance.now()` directly). Two captures seconds apart differ across the WHOLE
FRAME — terrain scroll, rain, dialogue typing on. A near-white count over a fixed box picks all of
that up, which is how I "proved" the lane plate whitened the boss hull, shelved finished art for two
drops, and reported a mechanism I did not understand. An **amplified difference image** showed the
truth in one look. Look before you quantify.

⚠ **THE BOSSES MOVE.** Two A/B arms captured at the same beam phase sit at different x, so a fixed
sample box compares boss-present against boss-absent. One run reported "48.6% vs 1.3%, my change
caused it" while measuring an empty crop. **And pinning the position is not enough — the canvas
holds the LAST DRAWN frame, so a pin must be followed by a step before the capture.**

⚠ **A PROBE MUST RUN LONG ENOUGH FOR THE MECHANIC'S OWN TIMESCALE.** Three separate false negatives:
a telegraph probe that ended before 55% of a 3s warn; a Warden probe that advanced ~2s of game time
against a 3.6s phase and so never reached the mode it was testing; a sweep whose period (4.2s)
exceeded the beam's life (4.3s) so the fan swung out and never came back — measured 56..78 degrees
when the design was 30..78, and it looked perfectly reasonable on screen.

⚠ **A GREP FILTER THAT HIDES THE IMPORT TABLES ALSO HIDES EVERY CONCATENATED DRAW.** I audited the
carrier's art families by excluding lines matching `'s6mb_'+` — which is exactly how a real draw site
builds its key. That put `gravityripple` on an "unreferenced" list while it drew under every gravity
mine, and it is the same blind spot that had already left `omegabomb-reflected` there. Grep the
family NAME with no prefix filter, or count `XART.get` keys in a live run.

⚠ **CHECK THE DIRECTORY BEFORE BUYING ART.** A manifest grep reports **zero** `s4w_` and `s6mb_`
keys because game.js registers them at RUNTIME into `XART._src`. There are **221 files** in
`assets/game/stage4_warfare/` and a full set in `assets/game/s6_carrier_attacks/`. That check saved
roughly 128 credits of regenerating art the repo already owned, twice in one session.

---

## SpriteCook is wired in — this is new and it changes the workflow

CLAUDE.md's "SpriteCook IS NOT IN THIS REPO" is superseded. It is a Claude plugin now
(`spritecook@spritecook`, MCP at `mcp.spritecook.ai`), authorized as **@coleforge**. Art can be
generated from a session. ⚠ **Installing is not authorizing** — `/plugin install` places the config;
the OAuth grant is a separate `/mcp` in an interactive terminal.

**Credits: 346 → 222 today.** Five generations, all recorded with their lineage in
`docs/spritecook_briefs/*/spritecook-assets.json`.

Five traps in what it returns, all measured, all in CLAUDE.md:

- **`edit_asset_id`, not `reference_asset_id`** — the latter is "something in a similar style", i.e.
  a lookalike. A damage state or a re-view is an EDIT. Wrong slot silently yields a different unit.
- **`width`/`height` are HINTS**, even with `smart_crop=false` (`size_behavior:"hint"` in the
  response). 256x256 requested came back 257x274 and 266x263.
- **`pixel:true` does not give pixel art** — 19,063 colours against a 61-colour authored plate.
- **Every model advertises `supports_transparency:false` and alpha comes back anyway.**
- **Count colours on OPAQUE pixels only** — counting RGB under transparent pixels inflated 19,063
  to 35,374, a figure absurd enough to get a real defect dismissed.

`_BUILD_SOURCE/normalize_spritecook_plate_0905.py` fixes canvas and palette and solves the pivot by
**silhouette IoU** (bbox edges and centroid are both dragged by whatever the new damage added). It
guards against a non-indexed reference: a PIL palette holds 256 colours and the Olive Warden's hull
is 22,597, which would have silently truncated and repainted the ship.

---

## What landed

### Mike's 17-item list is CLOSED

| item | drop | note |
|---|---|---|
| 2 cutscene shootdowns | 0905m | motion in 0905e; the three hostiles now in the hero ships' 3/4 view |
| 4 stage-4 miniboss | 0905h + 0905i | helpers removed at source; attack frame added |
| 5 boss helper projectiles | 0905c | before today |
| 7 laser telegraph | 0905h + 0905p | 3s warn, yellow→red sign, alarm, lane plate |
| 17 stage 3 | 0905e | the telegraph was wearing the lava boss's red |

### The Cryo Spear degrades (0905g)
Damaged and critical plates, generated as EDITS of the intact plate (IoU 0.919), normalized, wired,
and verified by the art key the draw asks for at 100/50/20% HP.

### The Olive Warden (0905h, 0905i)
Helpers removed **at the source** — they were built in `stage4WarfareInit`, not summoned mid-fight,
so suppressing the mode would have left them alive and shooting. `summoned` now derives from
`drones.length`, so the reveal, the draw and the 300px collision reach switch off together.
An attack frame was the ONLY thing item 4 actually lacked; muzzles and rounds already existed.
⚠ It is driven by the WALL attack, not by every round — keyed to the MG it never expired (930 attack
frames, 0 idle) — and gated above 0.62 HP because `_animKey` overrides the damage plate and would
visually HEAL the boss at critical.

### Three carrier families drawn (0905j) and prismbeam reshaded (0905k)
`crystalimpact`, `prismbeam`, `ricochetimpact` — all already on disk, none cost a credit. prismbeam
is a TILE, so it and crystalimpact became the **PRISM LANCE** on the existing head/tile/cap beam.
Reshaded 4-5 colours → a 14-colour shared ramp; ⚠ the tiles must keep **seam 40/40** or the beam
bands, and `_BUILD_SOURCE/reslice_prismbeam_0905.py` solves that by searching for the row pair that
already differs least rather than hoping.

### The Doomsday Carrier fights six phases (0905o)
Mike's spec is `docs/CARRIER_MK2_PHASES.md`, verbatim. The phases advance on **events** — shield
break → bay death → shield break → turrets dead → last stand — not on health. Health is a FLOOR only
(`CARRIER_PHASE_FLOOR`), because the bays take damage from nothing but deflected warheads and a
player who never deflects one could otherwise stall forever. Phase 3 RESTORES the shield on entry or
the alternation never happens.

### The Rime Wall's telegraph, rebuilt to a diagram (0905q, r, s, t)
Beams fire from the **cannon tips** (`L/C/R` at y+0.430, not `TL/TR` at y−0.105 up inside the hull);
rowed or swept; the side cannons **rotate** 30..78 degrees on their own side while the centre stays
pinned at 0.000, leaving 30-degree safe bands; the lane plate is wired; a pixel glow runs bottom to
top across the warn; the arrows hold SOUTH at every sweep angle and appear one by one with an alert
each, while the laser charges with its own sound.

---

## The suite — read this before you believe a count

**It is NOT deterministic. Four runs today gave 65, 67, 64, 67 failures.** This was proved with a
drop that changed **six PNG files and nothing else** — `git diff` on game.js and manifest.js empty,
byte for byte — and the count still moved by two. CLAUDE.md's "THE SUITE IS DETERMINISTIC NOW"
heading is struck through with that as the evidence.

⚠ **Compare failure NAMES against a clean `git worktree` at HEAD, never totals.** That is the only
check that separated real from flaky every time. Twice today it mattered: two assertions that failed
after the six-phase rework were REAL and mine (they pinned the old four-phase fight, and were
repointed, not reverted — CLAUDE.md's "read an assertion before fixing it"); and two corner-run
failures that came up twice in a row, which is not the flake pattern, turned out to be present in a
control worktree WITHOUT the change.

Current: **~3,216 ok / 64–67 fail**, band explained. `cornerLR` and the corner-vs-curve pair
oscillate; the stage-1 sand-tank fixture does too.

---

## OPEN — nothing here needs generation; 222 credits remain

**Mike's calls, not engineering:**
- **The prism lance's placement.** The one attack whose home I chose rather than him. Phases 2 and 4
  (taps + charged); phase 6 is the carrier's own energy cannon instead. Levers: two cadences, two
  widths (30/64), which phases carry it.
- **`retired_rigs_0..2`** — delete or keep, from the 0903 atlas repack.
- **The debrief shows six stats, not nine.** Four asked for in 0807o are off-screen because his
  concept panel has six slots.
- **The 2x cutscene face** is live on three surfaces he never asked to change; one accessor reverts.
- **Whether the 3s warn applies to every beam on stages 2–3 or only the big ones** — one constant.

**Not imported:** `CF_Stage9PortalCombatPickups-Lvl9` (179 entries, at `C:\s9p`) and four
`CF_EnemyTeleportFX` families (phase-needle, plasma-bloom, crimson-shatter, gravity-maw).

**Standing:** the Siege Ember "spin" has never reproduced. And ⚠ **an unrelated Pixeltable plugin
ships a `PostToolUse` hook that errors on every Write/Edit** — edits still land; the script itself
runs clean by hand, so it is the harness's invocation. Uninstalling that plugin ends it.

---

## ⚠ THE BIGGEST GAP, AND IT IS NOT CODE

**Nobody has played any of this at human pace.** The six-phase carrier was verified by forcing each
event; the Rime Wall telegraph by driving single beams and measuring angles. That proves the wiring
and the geometry. It does not prove the FEEL — whether phase 6's cannon-plus-slide is dodgeable,
whether a 3-second warn is too slow once you know it, whether the prism lance stacks badly on the
bay mechanic. Every one of those is a number away from being fixed and none of them can be found
from a probe. **Play it before tuning it.**
