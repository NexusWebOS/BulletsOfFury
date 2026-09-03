# 0903p — CO-OP: the split stats screen, and every hit credited to the pilot who fired it

Mike: *"when you do the end stats screen, you do a split screen where we show their seperate
stats"* — and, asked which shape: *"Side by side in one panel for co-op please."*

Built on `claude/bullets_betav0.7` at `26dc4dae`. Baseline captured BY NAME before any edit:
**3,186 ok / 276 sections / 68 fail**. After: **3,188 ok / 66 fail, zero new failures by name**,
totals 3,254 both sides.

---

## ⚠ SEPARATE STATS NEEDED SEPARATE CREDIT, AND THERE ARE ~40 WRITE SITES

`stageStats.kills++`, `.hits++`, `.dmgDealt+=` and friends live in `hitEnemy`, `killEnemy`, the
boss and miniboss paths, the specials and the blast chains — roughly forty sites. Editing each to
say which pilot is how one gets missed; this file already says so at `_dmgSrc`, which exists for
exactly that reason.

So `stageStats` is a **seat pointer** now, like `player` and `run`:

- `withSeat()` swaps it. A death, damage taken or a bomb fired inside a seat window lands on that
  seat's sheet without the site knowing.
- The player-bullet loop runs OUTSIDE any seat window, so every round is **stamped with the seat
  that fired it** — once, at the end of that seat's turn in `updatePlay`, not at the 33
  `pBullets.push` sites — and `shooterSet(b.seat)` points `stageStats` and `run.score` at that
  seat for the length of that bullet's processing. Set per bullet, restored after the loop: the
  `_dmgSrc` idiom.
- `spawned` is a STAGE fact, not a seat one. It is mirrored onto seat 2 so both rows share the
  real denominator instead of being counted twice.

**Known, recorded so nobody measures it as a mystery:** damage that lands LATER than the frame it
was fired on — a bomb's blast chain, a special ticking on its own clock — is credited to whichever
seat the swap is on when it lands, which outside a window is seat 1. First cut.

Proved in the live game before a pixel was drawn: P2 fires from inside its own seat window, P2's
`hits`/`dmgDealt`/`kills` and `run2.score` move, P1's do not; a P2 death lands on P2's sheet; the
shooter swap is restored after the loop.

---

## THE SCREEN: ONE PANEL, TWO SHEETS

`computeStageResults` now computes a sheet per seat (`scSheet`). `_res.rows/pct/rank/bonus/face`
are still seat 1's, exactly as every existing consumer reads them — the password branch and the
stage-advance handler are untouched. `_res.seats` is the only new field and is `null` in solo.

Each half is the solo layout scaled into its own column: portrait on the **outside** edge, rows
beside it, its own score bar under the rows, its rank under its portrait. The header and the
password stay shared across the panel, because the stage was cleared once. Every coordinate is a
fraction of the SAME panel rect the solo screen measured in 0807n (interior x 0.046..0.951,
y 0.086..0.907), so nothing can land on a bevel the solo layout already learned to avoid. Row
pitch is the solo pitch; type steps down two sizes.

The two columns animate in **lockstep** off seat 1's counters: a row fills for both pilots at once
and moves on when BOTH have reached their segment count. Two independent tickers would finish at
different times and the panel would sit half-done waiting on the slower player, which reads as a
hang. The rank stamps once BOTH score counters have landed, and drives `drawStageClear._stamp` —
the password and PRESS FIRE beneath key off that field and did not change.

⚠ **THE SOLO BODY IS GATED, NOT EDITED.** Everything from the portrait to the rank stamp is
byte-for-byte the solo screen it was, inside `if(!_coop){…}`. Rendered before and after with
identical fabricated stats: **0 differing pixels of 1,105,920.**

⚠ **AND THE GATE BROKE BOTH MODES ON THE FIRST CUT.** The shared PASSWORD block reads `rowsX` and
`rowsW`, which the gate had made block-scoped to the solo branch — a ReferenceError in solo AND
co-op, at the exact moment the panel is meant to finish. They are declared outside the gate now;
solo assigns its column, co-op hands the password the whole interior so it centres under both
sheets. The skip-ahead in the enter handler and the bonus payout cover seat 2 as well.

---

## CO-OP: WHAT REMAINS

Pilot specials are still one global `special` shared by both seats. Deferred damage (bombs,
ticking specials) credits seat 1. Campaign co-op is out of scope by construction.

## NEXT, IN MIKE'S ORDER

Shadow Orb impact sound · stage-1 jets that appear instead of entering · stage-4 shield breaks
rounds instead of deflecting · chaingun turrets +50% and diagonal bursts · stages 5–9 static idle
frames + muzzle flashes · stage-6 boss rebuild (SpriteCook) · stage-8 miniboss · the boss
telegraph (glow bottom-to-top, 1..2..3, f.f.f) · stage-7 boss black edges · stage-6 miniboss.
