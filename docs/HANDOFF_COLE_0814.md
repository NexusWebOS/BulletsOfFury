# BULLETS OF FURY — HANDOFF FOR COLE

**Branch `drop-0814e`, four drops: 0814e → 0814h.** Based on main @ `cbffa29` (0814d).
Full writeups: `PASSOVER_0814E/F/G/H.md`. Merge is a fast-forward; nothing on main was touched.

---

## WHAT LANDED

| drop | one line |
|---|---|
| **0814e** | The "hitbox square" miniboss is **stage 8** — the Herald was drawing frames 0–3 of its own venom attack stream as its hull (`mba_vr_*` is 0 keys anywhere). Recast onto your lock pack's **SPAWN CARRIER** (intact/damaged/critical), same wiring as magmaward/rimewall/olivewarden. Verified in pixels. |
| **0814f** | Two open-list items measured already-fixed: the barrel roll (your 5s cooldown shipped, `BR_COOL=5.0`) and Cole's rank-B portrait (draws `laugh`, and the art under the key IS a laugh — all 7 emotions contact-sheeted). |
| **0814g** | Stale sweep: font 404 (fixed 0811z), antipatterns hook (config gone), particle leak (re-fixed in 0814a) — all closed. The live one hid a real bug: **the UI editor saved to `assets/ui_layout.json` while the game reads `assets/data/ui_layout.json`** — every layout you ever saved went where the game never looks. Both editor paths fixed; the game now ships a literal-`null` layout file so http boots stop 404ing while provably changing nothing (6/6 links measured). |
| **0814h** | "Very tanky" measured: the stage-8 boss was **22,370 hp — 12.1× hpBase, 8× the bosses either side**. `hpx` was a share applied as a multiplier. Normalised to **4,070 total** (the `hpBase×2.2` budget), forms 740 → 903 → 1,095 → 1,332. The 0812o per-form attack identities are untouched. |

---

## ⚠ YOUR CALLS — EACH IS ONE LINE TO CHANGE

1. **Stage-8 boss hp.** 4,070 total is a fivefold cut in the direction of your own "very tanky",
   but you have not played it. Too easy now → raise the `2.2` in `_vBase`; the shape follows.
2. **RESOLVED 0825c — Spawn Carrier stats/name.** The intact Spawn Carrier hull remains, and Mike
   restored the encounter's authored name **HERALD OF DEATH**. hp 340 and `pat:'void'` are unchanged.
3. **The herald's venom stream** (`nev_venom_0_*`, a genuinely good 11-frame attack reel) is now
   unused. It could become a Spawn Carrier attack; nothing references it today.
4. **The lock pack ships an alternative 4-form stage-8 boss** (symbiote_carrier → winged_predator
   → razorhalo → nullheart, named anchors, damage states). Current `mbv_` art is complete and
   draws, so nothing forces the swap — recasting is a design call, not a repair.
5. Standing from before, unchanged: **% glyph** in the BOF face (stats screen borrows stage 2's
   molten one), **camo for stages 2/3**, **`mfx_` marked DELETE but live**, and **orb damage on
   stages 2/3 is higher since 0814a** (the elemental bonus finally reaches it — you have not seen
   the numbers).

---

## STILL OPEN, HONESTLY RANKED

- **Signs that scroll when told not to** and **the waterfall in the middle of the road** — the
  last two tester items. Both need repro hunting; neither is quick. 0813c fixed one signs bug
  (`_masterSrcY` mapping) so what remains may be stage-specific or already dead — re-measure
  before working it.
- **The lock-pack integration** — the big one: boss rebuilds 4–9, 104 enemies with damage
  triplets, the stage-6 Sky Citadel contract, Shadow Blast, stage 9's whole chain. Plus the two
  cutscene packs, the stage-9 packs, and thermoshock (diff against what 0814a already wired
  first). Each is its own drop; each pack carries its own CLAUDE_HANDOFF/README.
- **Level 9 through level 5** — still no mechanism, and stage 9 still has no `STAGES[]` entry.
- **The apostrophe rendering as a comma** ("LET,S") — one render of `p39`/`p44` settles it.

## ⚠ THE PATTERN THIS SESSION KEPT FINDING

**Eight open-list entries re-measured; five were stale.** The dam notes, "wide stages are 1/5/6",
the barrel roll, the portrait, the font 404, the hook, the leak — the list records when a thing
broke, not whether it still is. The probes in `_BUILD_SOURCE/probe_*_0814*.html` are the template:
drive the real surface to the reported state, screenshot it, and only then work it. Every one of
them runs in headless Edge with no node and no python (see the CLAUDE.md section on that).

## HOW TO VERIFY (needs a machine with node — this one has none)

    node --check assets/game.js
    node _BUILD_SOURCE/test_fl.js          # THE COUNT, not just failures. 4-or-5 fail baseline;
                                           # the volley fixture moves on its own (0814d note).

⚠ **The suite has not run on any of these four drops.** Parse-checked only. If any 0813-era
assertion pins `SUBBOSS[8].kind==='herald'` or the vile hp line verbatim, it will fail honestly —
read it, then repoint it at the rule (0814f's §180 precedent).

The four probes, headless Edge, from the repo root:

    _BUILD_SOURCE/probe_minibosshull_0814e.html?stage=N   any stage's miniboss, parked + shot
    _BUILD_SOURCE/probe_coleface_0814f.html               all 7 cole emotions, labelled
    _BUILD_SOURCE/probe_uilayout_0814g.html               the ui_layout chain, 6 checks
    _BUILD_SOURCE/probe_vileforms_0814h.html?form=0..3    the four vile forms, hp ledger + shot
