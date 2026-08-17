# PASSOVER 0813E — level 7's purple halos are black edges now

**Item 6 done.** **Item 7 diagnosed** — the remaining call is Mike's map design, not code.

---

## 6. "theres still purple halo's left on level 7"

**1,577 halo pixels converted to a black edge** across the level-7 plates. Alpha untouched, so every
silhouette is pixel-identical; only the RGB beneath the rim changed. Standing rule honoured —
converted, never deleted.

The offenders were the level-7 shock effects, not the enemies:

| plate | what it is | halo px |
|---|---|---|
| `nsw_circ_0..3` | muzzle compression pulse | 619 |
| `nsw_dist_0..3` + `nsw_distr_0..3` | trailing distortion, drawn at 50% on `'lighter'` | 776 |
| `nsw_ring_0..3` | the damaging front | 179 |
| `nsw_exca_atk_0`, `nsw_maw_0` | 1px each | 3 |

Black is especially right for `nsw_dist`: on an **additive** layer black contributes nothing, so the
purple fringe stops glowing without a pixel being removed.

**Deliberately left alone.** `nsw_barge_0` (7px) and `nsw_sentry_0` (8px) carry magenta *inside* the
silhouette, which may be authored colour — only outer-boundary pixels were converted. The RC2
masters' magenta is untouched too: it is punched to ALPHA on purpose as liquid openings (game.js:2439,
8,412px on stage 7) with `nlq_sludgeF` showing through. Terrain, not a halo.

Verified after: every drawn plate scans to **0** halo pixels, and the plates still render correctly
(`docs/proofs/halo7_after.png` — ring, distortion, pulse, maw, barge, shambler all intact).

### ⚠ The script's first run edited NOTHING, and that was it working

`BOFFI` rects are **`[sheetIndex, x, y, w, h]` — five elements, not four**. Read as `[x,y,w,h]` every
rect resolved to `None`, so the script refused rather than writing to a wrong rectangle. That refusal
mattered: `nca_74.png` is a shared sheet, and a bad rect would have corrupted art far outside level 7.

Backups written beside each modified sheet: `nca_74.png.bak`, `nca_75.png.bak`, `nca_17.png.bak`.

### Left: `nsw_combined`, 598px — unused

`nsw_combined` (sheet `nca_66` @2697,1548) still carries 598 halo px, but it has **0 references** in
game.js. Its halo cannot reach the screen. Not converted, to avoid touching another shared sheet for
no visual gain. Convert it if it is ever wired up.

## 7. "your hvoering the wrong section when we go to level 5" — DIAGNOSED, needs Mike

`CMAP_REGIONS` (game.js:32813) lays the eight stages out in a ring, and **stage05 is dead centre**:

| region | centre (640x480) | | region | centre |
|---|---|---|---|---|
| stage01 | 130,129 | | stage05 | **315,230** |
| stage02 | 305, 88 | | stage06 | 306,372 |
| stage03 | 449,106 | | stage07 | 122,365 |
| stage04 | 528,240 | | stage08 | 104,238 |

The index mapping is sound — array order matches `index` 1–8, so nothing is off by one.

**The mismatch is thematic.** The stage-effects table (game.js:32843) describes that centre node as
*"stage05: the central citadel — ember rise"* with tint `#ff8a5a`, i.e. volcanic. But stage 5 the
LEVEL is `bg:'space'`, subtitle "ALL FOR ONE, NONE FOR ALL", boss `voidbat` — and after 0813c it now
loops `norb5_arena`, an orbital starfield. So hovering stage 5 highlights a lava citadel in the middle
of the map while the level behind it is deep space. The volcano reads as stage 2's ground
("IT'S HOT IN HERE").

**Not changed.** Either the centre node is the wrong node for stage 5, or stage 5 is the wrong stage
for that node — that is map design and Mike's call. I also could not load the campaign-map plate to
confirm visually (no key matched `cmap|campmap|worldmap|nmap`), so the polygons were plotted on a
blank field. **Do not move a polygon off this evidence alone** — render the map under it first.

## Suite

**2,636 assertions / 234 sections / 5 failures** — the same long-standing five, unchanged by the art
edit.

## Still open

- **3** — no bridge asset exists anywhere; `cfg.props` holds one prop game-wide. Blocked on Mike.
- **5** — stages 1/4/6/7/8 still on legacy boss art; five unassigned `nsb_*` bosses available.
  Blocked on Mike naming the mapping.
- **7** — above.
- **8** — square boxes around background objects on space/sky. Repro exists:
  `docs/proofs/stage5_scrollwalk.png`.
- **9** — old chain-lightning graphic in stage 8's scrolling terrain.
