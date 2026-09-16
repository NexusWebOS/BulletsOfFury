# 0916 — ACH-02: the awards gallery and the unlock toast

The achievement registry has been complete since 0915 — **66 definitions**, the awards, the points,
the persistence, the Steam keys — and **nothing drew any of it**. `achievementUnlock` set
`achievementLastUnlock` and dispatched a `bof-achievement` window event that nothing listened to, so
a player could earn 1,630 points and never be told once. This is the surface for it.

## 1. The toast

Every unlock now says so: a plate at the bottom of the screen that **rises into place, holds ~2.4s
and slides back down as it fades**, carrying `AWARD <TITLE>` and `+<points>`.

⚠ **IT IS A QUEUE, NOT A SLOT.** A stage clear can award **seven at once** — 0915 measured exactly
that — and one slot would show the last and silently drop six. Measured: three unlocks in one frame
queue three toasts and play through in order.

⚠ **IT DRAWS AFTER THE SCENE, FROM THE ONE PLACE THE LOOP DRAWS EVERY SCREEN.** Hung off a single
call after `drawScene`, so it appears over PLAY, the map, the debrief — anywhere — and can never be
painted over by the screen that earned it. That is 0905h's trap (a warning sign the boss hull
covered every frame) avoided by construction rather than by luck.

⚠ **AND IT RESTS ABOVE THE CONTROL HINT ROW.** At its first resting height it sat directly over the
MENU / SELECT / START line on every menu screen — visible in the first capture, invisible to every
counter.

## 2. The gallery

A seventh title button, **AWARDS**, opening a gallery of all 66: title, points, and a locked or
unlocked state, eight at a time, UP/DOWN to scroll with drawn arrows (this face has no arrow
glyphs — 0906g), B to go back with the cursor left on AWARDS.

⚠ **SORTED BY FAMILY THEN POINTS.** `ACHIEVEMENT_DEFS` is built pilot-by-pilot then stage-by-stage,
so its raw order interleaves 100-point campaign clears with 10-point stage clears and reads as
noise.

⚠ **A LOCKED ROW IS DIMMED, NEVER HIDDEN.** Hiding them would make the gallery useless as a list of
things to go and do, which is the only reason to have one.

## 3. ⚠ The dispatch is keyed by NAME now, and that is the load-bearing change

The title menu ran on `if(m===0) … else if(m===4) … else { tryExit(); }`. **Inserting AWARDS before
CREDITS would have repointed every row below it and made one of them quit the game.** It is keyed by
the label, so a new row can only do what its own case says, and an unrecognised row now does
*nothing* — a visible bug rather than a destructive one.

`TITLE_ITEMS` and `MENU_KEYS` were already driven off one length by 0916's layout fix, so the
geometry needed no change at all: the plate scales until seven rows fit.

## 4. The button art

Generated (SpriteCook, `gemini-3.1-flash-image`) against two authored buttons uploaded as a style
reference — the route `btn_help` took in 0912a. Registered as a loose file in the code-owned block,
because `manifest.js` is GENERATED.

⚠ **THE FIRST ONE WAS REJECTED BY THE SCREENSHOT, NOT BY A CHECK.** It was a clean plate with gold
lettering and nothing else, and next to its neighbours — each of which carries an emblem panel and
an inset scene — it read as a flat bar. The second pass asks for the same *composition*: a trophy
emblem at the left end, a medal-and-laurel scene behind the lettering, amber lamps at both ends.

## 5. Measured

`_BUILD_SOURCE/probe_awards_0916.py` — **22 ok / 0 fail**, real Chromium, 0 page or console errors.

⚠ **THE TOAST'S MOTION CANNOT BE READ AS LIT PIXELS IN A BAND.** The title screen fills the bottom
band with its own art, so "the topmost lit row" is 0 on every frame whatever the toast does — the
first cut reported no movement on a build where it moves 24px. The toast's own panel blit is
trapped instead and its destination y read per frame: **502 → 478**, its full height of travel.

⚠ **AND THE ACHIEVEMENT STORE IS `localStorage`, WHICH PERSISTS.** Every arm clears it first, or the
second run of the probe measures a build where everything is already unlocked and nothing can fire.

Suite **4,647 ok / 57 fail** — zero new failure names against a clean worktree at `97265703`.
Section 364 is 18/18.

**Two assertions failed on this change and were repointed, not worked around:**
- `HELP is the fourth title button` pinned `TITLE_ITEMS.length===6` — the **count**, while its own
  name only claims HELP's position. A button Mike asked for failed an assertion about a different
  button. It now pins the position.
- My own `an unrecognised row no longer quits the game` matched the **comment explaining the fix**
  (`NO else { tryExit() }`). Section 47's trap, self-inflicted. Both of this section's source pins
  strip comments now.

Proofs: `docs/proofs/awards_0916/01_title.png`, `02_gallery.png`, `03_gallery_end.png`,
`04_toast.png`, `05_button_v2.png`.
