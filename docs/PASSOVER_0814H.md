# DROP 0814H — "VERY TANKY" WAS A SHARE APPLIED AS A MULTIPLIER

> Tester: "the stage 8 boss (4 forms, same pattern, very tanky)."

## 1. TWO OF THE THREE CLAIMS WERE ALREADY ANSWERED

Re-measured before working (the 0814f/g rule):

- **"same pattern" — fixed in 0812o.** `vileAttack` gives the four forms four escalating
  identities (wall-with-one-gap → aimed bursts + homing pairs → rotating rake + spiral → all of
  it faster), and the 0812o comment quotes this exact complaint.
- **"4 forms" draw, distinctly** — all 88 `mbv_` keys registered; forms 0 and 3 screenshotted via
  `probe_vileforms_0814h.html` (an armoured cocoon with a red eye; a winged skeletal horror).
  The lock pack ships an ALTERNATIVE four-form art set for stage 8 (symbiote_carrier →
  winged_predator → razorhalo → nullheart). Whether to recast onto it is Mike's call — the
  current `mbv_` art is complete and draws, so nothing forces the swap.

## 2. "VERY TANKY" FINALLY HAS A NUMBER, AND IT IS 12.1×

Read off the real builder, all four forms:

    APOSTLE COCOON       4,067
    VENOM ASCENDANT      4,962
    NECROTIC LEVIATHAN   6,020
    FURIOUS DEATH        7,321
    TOTAL               22,370      hpBase for stage 8: 1,848  ->  12.1×

Every other late boss totals 1.4–1.5× its hpBase (doomsdaycarrier ~2,256, sludgeemperor ~2,615).
The finale was EIGHT TIMES the hp of the bosses either side of it.

## 3. THE MECHANISM: hpx IS A SHARE, NOT A MULTIPLIER

`_vBase = hpBase*2.2` is exactly the band the other modular finales sit in — it reads as the whole
fight's budget. The `hpx` column (1.00 → 1.80, summing to 5.5) is the escalation SHAPE across the
forms. `vileBuildForm` applied hpx to the FULL base, handing every form its own boss-sized pool —
the same class of error as 0810s's flat-100 sub-boss seed: two knobs each believing it owned the
total.

Normalised by the hpx sum, both authored knobs keep their meaning:

    before   4,067 / 4,962 / 6,020 / 7,321   = 22,370
    after      740 /   903 / 1,095 / 1,332   =  4,070   (hpBase × 2.2, escalation intact)

Measured after the edit through the same probe — the numbers above are read off the running
builder, not computed from the source. The 0812o attack identities are untouched: the fight
escalates in pressure while each bar stays killable.

⚠ **THIS IS A BALANCE CHANGE MIKE HAS NOT PLAYED.** The direction is his own report ("very tanky")
and the target is the band his other bosses occupy, but 4,070 vs 22,370 is a fivefold change to
the campaign's finale. If it now dies too fast, the one number to raise is the 2.2 in `_vBase` —
the shape will follow.

## 4. THE SWEEP + LIST PASS, CLOSED OUT

Across 0814e–h this session: stage-8 miniboss recast onto its lock art (0814e), two stale entries
closed with probes (0814f), three more stale + the ui_layout/editor path bug fixed (0814g), and
the stage-8 boss hp normalised (0814h). The tester's list now has two items left: **signs that
scroll when told not to** and **the waterfall in the middle of the road** — both need repro
hunting, neither is quick. The big remaining work is the lock-pack integration (stages 4–9 boss
rebuilds, 104 enemies, stage 9, Shadow Blast) and the two cutscene packs.
