# DROP 0814F — TWO OPEN-LIST ITEMS WERE ALREADY FIXED. THE LIST WAS STALER THAN THE CODE.

Working the open list in order, "quickest route" first. Both quick candidates turned out to be
closed already — the finding of this drop is the STALENESS, and it is worth a drop because acting
on either entry as written would have produced wrong work.

## 1. THE BARREL ROLL — MIKE DECIDED, AND IT SHIPPED

CLAUDE.md's "Waiting on Mike" still offered shift-suppress vs cooldown as an open choice. The code
answers it: `BR_COOL=5.0` with Mike's own words quoted at the constant ("lets do a 5 second
cooldown on barrel rolling"), a re-arm bar drawn on the HUD, and the 0805u mount-gate intact.
Shift-suppress was NOT added — consistent with the entry's own "his call on which, not both".

⚠ **ACTING ON THE STALE ENTRY WOULD HAVE ADDED THE SECOND MECHANISM MIKE RULED OUT.** A fresh
session reading that list would plausibly have implemented shift-suppress "to close the item" and
violated the recorded decision in the same stroke.

The trigger is still double-tap within `BR_WINDOW=0.26s` (updatePlay, before normal movement). If
accidental rolls get re-reported, the knob is the WINDOW, not the cooldown — the cooldown only
rate-limits the second roll; the window is what fires the first one.

## 2. COLE'S PORTRAIT AT RANK B — CORRECT IN STATE AND PIXELS, COLD AND WARM

The entry: "Cole's portrait shows the `crash` emotion at rank B; the table says `laugh`."
Measured on main @ cbffa29 (`probe_scface_0814f.html`), rank B built through the real
`computeStageResults` with good-but-not-great stats:

    COLD (one-shot, the way a real run reaches it):  rank B  face port_cole_laugh
    WARM (keys polled ready first):                  rank B  face port_cole_laugh

and the stage-clear screen screenshotted drawing it.

⚠ **THEN THE KEY WAS NOT TRUSTED EITHER** — "filenames lie" applies to registrations: if the art
REGISTERED as `port_cole_laugh` depicted the crash, every state check above would pass on a wrong
picture (the Decker/Freezer aintro swap, one store over). All seven cole emotions were rendered on
one labelled sheet (`probe_coleface_0814f.html`): laugh is a head-back laugh, crash is a terrified
face on a debris field, no two swapped, 7/7 resolve.

Fixed by the 0807o stage-clear rebuild (`SC_FACE` + `scPortrait`); the entry predates it.

⚠ **`scPortrait` REMAINS A ONE-SHOT `XART.rdy` CHAIN** cached into `_res.face` at results-build
time — the documented first-call trap, unfired here only because the portraits are warm by the
time a stage clears. If a future report says the stats screen shows the CARD or nothing, start
there; the fallback chain is `want → idle → port → card → null`.

## 3. THE PATTERN, FOR THE NEXT LIST PASS

0814d found the dam notes stale. 0814e found the "wide stages are 1/5/6" note stale. This drop
found TWO list entries stale. **The open list records when a thing was broken, not whether it
still is — re-measure an entry before working it.** The two probes here are the template: one
drives the real surface to the exact reported state, the other renders the art the keys resolve
to. Both are cheap, and both would have caught every stale entry found this week.
