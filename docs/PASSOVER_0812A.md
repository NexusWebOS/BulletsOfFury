# Passover 0812a — the beta tester's input list

Mike's tester, and Mike's own ranking of it. Three of the items are done; the rest are listed with
what was measured about each so nobody has to rediscover it.

---

## 1. Mouse buttons are programmable inputs

> *"Add mouse buttons as programmable inputs. A better control for me would be Left click (Fire).
> Right Click (Missiles), Retina Lock (Space bar)."*

⚠ **NO NEW INPUT PLUMBING WAS NEEDED — the gamepad already showed the way.** Pad buttons are
pushed into the same `keys` map as `pad_b0..15`, which makes them bindable, tappable and holdable
through `down()`/`tap()`/`tapAny()` with no special case anywhere. Mouse buttons are `mouse0/1/2`
in exactly that map, so every consumer that understands a bind understands a click, and the rebind
screen picks them up for free because it stores whatever key name it observes.

Verified with **real DOM MouseEvents on the canvas**, not by poking internals:

```
LEFT  click  ->  keys.mouse0 = true   fire held = true
RIGHT click  ->  keys.mouse2 = true   bomb held = true
```

Defaults are now `fire: j, mouse0, pad_b0, pad_b7` · `bomb: k, mouse2, …` · `retina: c, space, …`
— **added, not substituted.** `keybindValidate` only refills an action that is missing or empty, so
anyone who has already played keeps their localStorage binds regardless; adding costs nothing and
removing J/K/C would strand the existing layout.

⚠ **`setk` IS NOT IN SCOPE IN THE EVENT HANDLERS.** My first cut called it — it is a `const`
declared *inside* `pollGamepad`, so every click would have thrown a ReferenceError. The handlers
mirror the keyboard's own two lines instead, including the `pressed` transition so `tap()` sees a
click once rather than every frame it is held.

⚠ **RIGHT-CLICK NEEDED THE CONTEXT MENU SUPPRESSED**, on the canvas only. Binding missiles to
button 2 is useless if the browser menu covers the playfield on every shot.

⚠ **AND MOUSE BINDS ARE FILTERED OUT OF `menuConfirm`.** It reads `tapAny(keybind.fire)`, so
`mouse0` in fire would have made *any* left click confirm the highlighted row — one click doing two
things: activating the button under the cursor **and** whatever the keyboard cursor sat on.
Gameplay keeps the click; menus keep their own semantics.

---

## 2. ⚠ THE MOUSE DIES ONE SCREEN INTO THE GAME

> *"Inconsistent inputs. Main menu lets me use mouse, but immediately rejects mouse inputs in
> random menus."*

Audited **every** menu screen for a click handler rather than guessing which ones he meant:

```
mouse OK        title · difficulty · pilot · password · options · game over · continue
KEYBOARD ONLY   mode select · campaign hub · stage select · credits · stage clear
```

**"Immediately" is exact.** TITLE takes the mouse and **MODE SELECT — the very next screen — is one
of the dead ones.** That is the whole of his experience: click through the title, get ignored.

Mode select now hovers and clicks. Its row band comes from the layout constants (`y0`/`gap` and the
324px selected pill), **not from the art**, so a pill plate with a different aspect cannot make the
clickable area disagree with what is drawn. Activation is factored into one `_modeGo()` shared by
keyboard and mouse — duplicating it is how the campaign-hub branch would get fixed in one copy and
not the other.

**The other four are still keyboard-only** and are the next job on this item.

---

## 3. The selection arrows: overlapping on the left, invisible on the right

> *"You arrow is covering and overlapping this is an easy fix. Just move the arrows outside of the
> window"* — and, separately, *"Right arrow disappears"*.

Both from one number. `menuSelMark` draws at `cx ± (halfW+16)` and options passed `ww/2-46`:

- **left arrow at `wx+30`**, and row labels are drawn at `wx+16` — so MASTER rendered as "▶ER" and
  MOVE LEFT as "M▶ LEFT";
- **right arrow at `wx+ww-30`**, which is inside the key button's span (`wx+ww-124 … wx+ww-20`),
  and the button is drawn **after** it — so it was painted over.

⚠ **0801bp HAD PULLED THEM INWARD FOR A REAL REASON, AND IT WAS NOT THE POSITION.** At `ww/2-10`
they sat at `wx-26`/`wx+ww+26` and showed as slivers — because the panel clip is
`rect(wx,wy,ww,wh)`, exactly the panel. The clip only ever needed to be tight **vertically**, to
hide scrolled rows. It is opened 26px each side now (the panel is `x:28 w:VW-56`, so 28 clear
pixels exist), and `ww/2-4` puts the arrows at `wx-12` and `wx+ww+12` — outside the frame, clear of
the labels, clear of the key buttons. Proof: `docs/proofs/options_arrows_0812a.png`.

⚠ **The probe's own check for this was worthless and is marked as such** — it scanned for "lit
pixels left of the label", on a screen with a full-bleed backdrop, so it reported x=0 and would
have reported x=0 whatever the arrows did. The screenshot is the evidence.

---

## 4. Suite

**2,505 assertions / 221 sections / 5 failures** — unchanged from the deterministic 0811u baseline.

---

## 5. Still owed from the tester's list

Everything below is his, recorded verbatim enough to act on:

- **Mouse in the remaining four screens** — campaign hub, stage select, credits, stage clear.
- **Stage-clear text centring** — his screenshot shows the label column and the value column
  disagreeing; the rank letter and portrait also collide with the first rows.
- **A miniboss is still the hitbox square.** Mike: *"never replaced it"*. Which stage is not
  identified in the thread.
- **Stage 8 boss**: four forms, very high HP, *"attack pattern is the same through all 4 forms"*.
  Mike: *"filler shit"*, not yet coded.
- **Signs scroll when told not to**, and a waterfall sits in the middle of the road.
- **The barrel roll fires on micro-adjustments.** His suggestion: hold or toggle **shift** to
  suppress it; Mike wanted a cooldown too. This is a feel change to the core movement and wants
  Mike's call on which of the two.
