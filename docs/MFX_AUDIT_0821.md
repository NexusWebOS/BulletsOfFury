# mfx_ AUDIT — THE DELETION OPEN SINCE 0808c, ANSWERED

0808c left this open: *"mfx_ (252 cells) — the one deletion I have not confirmed, and 39% of the
delete list"*, and Brian carried it forward to Mike as a standing call: **"`mfx_` marked DELETE
but live"**.

**Measured answer: do not delete it. There is nothing to gain.**

---

## 1. WHAT IS ACTUALLY LIVE

A static grep cannot answer this — the 44 source references are DYNAMIC
(`drawMfx('mfx_hom_0_'+_dnf, ...)`, `drawMfx(_ek, ...)`), so the key is built at runtime. So
`XART.rdy`/`XART.get` were wrapped and every request recorded across:

- all 8 stages, 30s each
- all 9 pilots, 12s each with the trigger held
- all 6 weapon types x 8 levels
- every SHIPBOSS spawned AND killed

    252 cells total    52 live    200 not exercised

| family | live | not exercised |
|---|---|---|
| `mfx_mg` | **25 (all)** | 0 |
| `mfx_emr` | **4 (all)** | 0 |
| `mfx_ea` | 22 | 114 |
| `mfx_bpow` | 1 | 2 |
| `mfx_spr` | 0 | **28** |
| `mfx_exA/B/C` | 0 | **32** |
| `mfx_hom` | 0 | **10** |
| `mfx_bshot` | 0 | 10 |
| `mfx_bmg` | 0 | 4 |

## ⚠ 2. "NOT EXERCISED" IS A FLOOR, NOT A FACT — AND THE SWEEP PROVED IT ON ITSELF

The first pass covered stages and pilots only, and reported `mfx_emr` as 4 dead cells. Adding
weapon tiers and boss deaths moved **all four of them to LIVE**, and `mfx_ea` gained 7 more.

**Every round of extra coverage resurrected keys.** A wider sweep would very likely resurrect
more. Anything deleted off a list like this is deleted on the strength of "I did not happen to
reach it", which is exactly the reasoning this repo keeps getting caught by.

`mfx_spr` is the one genuinely suspicious entry: 28 cells, and weapon 1 (spread) was fired at all
eight levels without touching one of them.

## ⚠ 3. AND DELETING WOULD FREE ZERO BYTES

This is what actually settles it. Where the cells physically live:

    nca_77   188 mfx_ cells  of 1588 on that sheet   1.81 MB
    nca_6     22             of  507                 4.88 MB
    nca_73     4             of  454                 4.63 MB
    nca_75     4             of  723                 5.20 MB
    nca_7      1             of  214                 3.21 MB
    nca_76     1             of  394                 1.20 MB

**Not one sheet is exclusively `mfx_`.** Every cell shares an atlas with hundreds or thousands of
others. Removing the manifest keys removes the *names*; the PIXELS stay in the shared PNGs, so
the download, the decode and the disk are all unchanged.

The only way these bytes go away is the **repack into named sheets** — which 0808c listed as its
own open item on the same page. The deletion was never separable from the repack.

---

## RECOMMENDATION

**Close it as "will not do", and fold it into the repack if that ever happens.** Deleting 200
manifest keys today would carry a real risk (any key resurrected by coverage this sweep did not
reach becomes a missing-art bug) for a measured benefit of zero bytes.

If Mike wants the roster tidier regardless, the safe order is: repack first, then let the packer
drop whatever no longer has a reference — which makes the liveness question the packer's problem
rather than a judgement call.

Nothing was deleted. This is decision-support only.
