# PASSOVER — drop 0806z   (SHEETS REGROUPED BY MEANING, AND 213 MB I HAD DUPLICATED)

Build: `BulletsOfFury_0806z`
Harness: **2,068 assertions / 189 sections / 0 failing**.
Full verification: **PASS — playable, and every graphic resolves.**

---

## 1. SHEETS NOW HOLD ART THAT BELONGS TOGETHER

> "you got the missile box powerup with my stages? enemies with font sheets?"

Fixed. Grouping is by USE now, from a capture across all 20 states, all 9 pilots, all 8 stages
and every weapon level — not by key prefix and pixel budget:

    ui         3 sheets    88 MB    boot, menus, buttons, cursors, map, select
    common     4          112 MB    art two or more stages share
    s1         1           18 MB    s5   1    38 MB
    s2         2           58 MB    s6   3   125 MB
    s3         2           52 MB    s7   1    29 MB
    s4         1           13 MB    s8   1    13 MB
    unreached 59        2,047 MB

`assets/data/atlas_groups.json` records which sheet is in which bucket, so per-stage preload or
eviction is a small job whenever you want it.

## 2. ⚠ MY REGROUPS DUPLICATED 994 IMAGES — 213 MB

This game has **750 aliased files**: two or more keys naming the same file on purpose, because
the art is identical. 0806w handled that correctly — every key sharing a file got the SAME cell.

**Then 0806x and 0806z regrouped by iterating `for k in cells` and packing each KEY
independently, which quietly forked every alias back into its own copy.** Hashing all 9,535
cells found 653 duplicate groups and 994 redundant copies. `nmb_fill` alone was stored 17 times.

Collapsed: every duplicate group now points at one cell.

**The tell was a single assertion** — `nst4b_tr_in` and `ncon_3_4` stopped being equal — and I
nearly wrote it off as another stale path check like the six I had just re-pointed. It was the
only thing in 2,000+ assertions that noticed 213 MB going missing. Section 189 now asserts the
INVARIANT, so a future repack that forks an alias fails loudly instead of costing memory
silently.

## 3. WHY I STILL HAVE NOT DELETED THE UNUSED ART

> "when I said delete all graphics I wasn't using, I truly meant JUST that"

Full coverage touched **1,914 of 9,535** cells. The other 7,621 are two different things and only
one of them is what you mean:

* **66 families are PARTLY used** — `mfx_mg` 3 of 25 frames, `nhxv_g_s` 1 of 24, `ovrotor` 24 of
  72, the boss cannon rotations 9 of 37. That is **623 untouched frames inside families that are
  demonstrably live.** They are not unused art; they are frames a run did not land on. Deleting
  them breaks rotations, spins and weapon tiers the moment a different frame comes up.
* **3,175 families never touched at all** — but that set still contains `ncm_font_c` (a font),
  `nbb_fill` (UI bar fills) and Maverick's `nhxv_*` charge tiers. All reachable; the probe never
  hit that glyph, that bar value, that charge level.

**Observation cannot tell "art Mike isn't using" from "art this run didn't reach."** Acting on it
is how 0724dq happened — green suite, 4,000+ browser errors.

`docs/UNUSED_ART_CANDIDATES.txt` lists all 3,175 family names. You know your own art. Mark the
ones that are genuinely dead and I will delete exactly those and nothing else.

## 4. STILL OPEN

* The deletion above, once you have marked the list.
* Helix contact burst POSITION · flame / ice fade-on-release · miniboss slow/shield ·
  stats-screen alignment · the ice-level freeze retest.
