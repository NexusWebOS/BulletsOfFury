# Resume here — 2026-09-16, end of session

Everything below is pushed to `origin/main`. Last commit: `8ed5f1a8`.

## Do this first

~~**`8ed5f1a8` (S4-16, escape arrows) is NOT verified in the running game.**~~ **DONE 0916r** -
`_BUILD_SOURCE/probe_escape_0916.py` is the probe this section asked for and it is in the repo now.
The steps below are what it does; it found one real defect, recorded in `docs/ESCAPE_ARROWS_0916.md`.
The original note follows.

**`8ed5f1a8` (S4-16, escape arrows) was NOT verified in the running game.** It parses and is guarded
(`if(charging)` + `XART.rdy`), but the probe that would have proved it was interrupted before it ran.
Verify before anything else:

1. Drive stage 4 on **furious**, spawn the boss, call `stage4GiantStrikeStart(boss)`.
2. Trap the blit by wrapping **the context instance's** `drawImage` — never the prototype (CLAUDE.md
   0905h) — and confirm: two arrows, one each side, one drawn with a **negative x scale** (the pair
   is one plate mirrored), and that they **flash** rather than hold.
3. The flash must land on `l23WarnSound`'s beat: both read `k * L23_WARN_ARROWS`.

A half-written probe for exactly this is in the session scratchpad as `probe_escape.py`; it is not
in the repo. Rewriting it is ~20 lines against `_BUILD_SOURCE/shoot.py`'s server.

## What landed today (11 commits, `9872cfa2` … `8ed5f1a8`)

- The debrief is one **full-screen authored plate**, regenerated three times as Mike refined it:
  edge-to-edge → wide bays → eight slots → a **square rank box with a word strip beside it**. Bays are
  MEASURED off each plate (flood the dark recesses, take fractions), so a new plate costs one pass.
- **CONTINUES LOST** and **UPGRADES ACQUIRED** slots, with the counters that feed them.
- Stage 1's briefing is **Mike's own copy** (`SC_BRIEF`), not a sentence built from table names.
- **Rank**: his seven authored plates, each cut at its waist into shield + word banner for the two
  bays. F is the TOP of the ladder (Furious), L the floor. D is **DUMMY** on his art.
- **NEW WEAPONS UNLOCKED** (`GS.UNLOCKS`) between the debrief and the exit; the debrief's exit is now
  `scLeaveStage(R)`, which is the seam any further between-stage screen should use.
- The **new wordmark** on the title and opener, keyed from his magenta with the halo blacked.
- Typography: narrow glyphs no longer squish, `!` `?` `.` `,` get their own air, the clock reads
  **MM:SS**, and the colon renders as a colon rather than an equals.
- **Cover art** (2 candidates) + the **Forge** design note and its measured art inventory.
- Earlier in the day: the campaign **freeze** (deleted declarations killing the rAF chain), the pilot
  screen's **pad lock-out**, RESET CONTROLS in options, the 6-button Genesis scheme.

## Open questions Mike has not answered

1. **Yuri's Lightning Orb** — the unlock page announces it after stage 2 (his words), but the engine
   grants it as the **stage-4** victory reward. Move the grant or move the announcement?
2. **Stage 3** has no unlock row, so no page appears after it. What should it announce?
3. The debrief's stat rows still read `LABEL = VALUE`. Mike said "not =, use semicolon" about the
   CLOCK; if he meant every separator, it is one pass.
4. The Forge doc's four questions (persistence, co-op, draft placement, which three fusions first).

## Next in the work order (`docs/WORK_ORDER_0914.md`)

| id | wo | what |
|---|---|---|
| ~~S4-16~~ | 27 | **DONE 0916r** - verified in Chromium (16/0). The arrows were right; the warning SOUND was firing 279 times a charge (`l23WarnSound` divides by `B.warm`, which the strike never set). See `docs/ESCAPE_ARROWS_0916.md`. |
| ACH-02 | 42 | achievement menu/button + bottom-centre unlock notification that slides/fades down |
| ENG-15 | 52 | HUD incoming-lock indicator above EQUIPPED: grey idle, red flashing, distance-accelerated beeps |
| ENG-02 | — | still partial: the remaining non-laser boss attacks that need the shared warning |
| S2-09, S3-10, S3-12 | — | Furnace giant-beam art; Hard/Furious stage-3 boss behaviour |

## Standing checks

- `node --check assets/game.js` after every edit; `node _BUILD_SOURCE/test_fl.js` before a push.
- Suite baseline is **56 names**; 57 with the intermittent stage-1 sand-tank fixture. Compare NAMES
  with numbers masked, never the count alone.
- Anything visual: prove it in real Chromium through `_BUILD_SOURCE/shoot.py`, not from the source.
