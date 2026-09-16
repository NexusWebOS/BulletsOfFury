# 0916 — S4-16 verified, and the warning beep it was supposed to be synchronized with

`8ed5f1a8` shipped the Stage-4 giant strike's escape arrows **unverified**, said so in its own
commit message, and `docs/RESUME_0916.md` made verifying them the first item of the next session.
This is that verification. The arrows were fine. **The thing they were meant to be synchronized
with was not.**

Mike, S4-16: *"Authored left/right escape arrows: flipped pair, flashing with synchronized warning
sounds for the giant strike."*

## 1. The arrows — measured, and correct as shipped

`_BUILD_SOURCE/probe_escape_0916.py`, real Chromium, the Furious Stage-4 Sovereign forced into
`stage4GiantStrikeStart`, reading the game context's OWN `drawImage` with the live CTM:

- they **draw**: 234 of 330 charge frames, **two per lit frame**, never one, never three;
- **one of the pair carries a negative x scale** every time — it is one plate, mirrored, so the
  two cannot drift apart;
- they sit **in the safe lanes**: left at world x 140.5 inside a lane ending at 181.6, right at
  539.5 inside a lane starting at 498.4 — the 17% of the camera at each edge the strike leaves
  open — at the player's own altitude, pointing outward;
- they **flash rather than hold**: 104 dark frames, in **7 bursts**, which is `L23_WARN_ARROWS`.

Proof frame: `docs/proofs/escape_0916/strike_arrows_lit.png` — gold chevrons outside the red cone,
one each side, with the player between them.

## 2. ⚠ The defect the verification found: 279 alert calls in one five-second charge

`l23WarnSound(B)` is shared with the beam warns and reads **`B.warm`**. The giant strike's object
carried `charge` and never set `warm`:

```
const k = clamp(B.t / Math.max(.001, B.warm), 0, 1);   // B.warm undefined  ->  k = NaN
const n = Math.floor(k * L23_WARN_ARROWS);             //                      n = NaN
if (n === B._arrowN) return; B._arrowN = n;            // NaN === NaN is FALSE, every frame
...
if (n > 0 && B._warnSfx) return;                       // NaN > 0 is FALSE, so this never gates
```

Both guards are defeated by the same NaN — the "have I already fired on this arrow" test *and*
the "only the first arrow speaks" test. Measured on the shipped build: **279 calls to the alert
across one charge**, gated audibly only by `alertLockon`'s 1.10s TAME row. The design is **one**.

And it made the feature's own headline claim impossible: the arrows flash on `q = t/charge` and
the sound had no beat at all, so "synchronized with the warning sounds" could not have been true
however the picture behaved.

**The fix is one field** — `warm: S4_GIANT_STRIKE.charge` on the strike object — so the beep and
the arrows derive the same `k` from the same number. After it: **2 calls**, and both are events —
`alertLockon` on the first arrow, `dangerAlert` at the yellow→red transition, which
`stage4GiantStrikeTick` fires separately and deliberately.

⚠ **THE LESSON IS THE SHAPE, NOT THE FIELD.** `l23WarnSound` takes any warn-shaped object, and
nothing checks that the object it is handed has the field it divides by. NaN then travels through
two guards that both read as "false, carry on". Any future caller of it must carry `warm`, and
section 362 pins a bare object still producing NaN so that this stays visible rather than becoming
folklore.

## 3. ⚠ And the probe made the world-vs-screen mistake, for the sixth time in this repo

Its first run reported the RIGHT arrow **59px inside the danger zone** on code that was correct.
`stage4GiantStrikeDraw` runs inside `drawWorld`'s `translate(-camX)`, so a recorded blit is
`(world - camX) * scale` and the lane bounds are world coordinates. `camX` was 100. CLAUDE.md
already records this class for the launch seam (0810a), the outbound routes (0810c), the level-1
ship (0810e), `probe_seam.py` itself and Bullets of Debug's FOV cone (0912h). **Before reporting a
position, subtract — or add back — the camera.**

⚠ And the first proof frame was taken after the run finished, so it showed the strike with **no
arrows in it at all** — a picture indistinguishable from "they never drew" on a build where they
drew 234 times. The frame is now read inside the rAF callback that drew it.

## 4. Measured

- `probe_escape_0916.py` — **16 ok / 0 fail**, 0 page or console errors.
- Suite **4,579 ok / 57 fail**, final summary reached, exit 1 — failure names identical, with the
  numbers masked, to a clean `git worktree` at `97265703` (4,552 / 57). Section 362 is 11/11.
