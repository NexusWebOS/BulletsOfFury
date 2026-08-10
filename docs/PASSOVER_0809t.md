# Passover 0809t — facing each other, and the campaign stops being backable

## 1. Cutscene portraits face each other

Mike: *"be sure in the campaign section cut scenes you flip the characters to be facing each other
while talking."*

Every pose in `CF_FuryHQCutscenes` is authored facing **screen-left** — Axel's drawn pistol points
that way and the rest angle with it. So the RIGHT slot was already looking inward and it is the
LEFT one that has to mirror. `drawCutscene` now flips the left slot only; centre is left alone,
it has nobody to face.

## 2. The campaign is not backable

Mike: *"do not make k/b back you out of the campaign menu, selecting a level or starting a
campaign. They need to press start, where a glowing pop up window will appear with options such as
Save Game, Load Game, Options, Return to Main Menu — this way the game can register when were no
longer in the campaign mode."*

**That last clause is the actual requirement.** Backing out on a stray key left nothing to hook —
the game slid back to the menus without ever being told the campaign had ended. Leaving is
deliberate now, through one exit, and `campaignEnd()` is the single place that knows.

The back keys on `CAMPHUB` / `STAGESEL` / `PILOT` open `campPause` instead. Selecting a level and
starting a campaign are untouched — those are confirm, not back. The check runs *before*
`menuBackTick` so one press cannot be read as both, and is skipped entirely while the pause owns
input.

The window is `dlg_window` with a pulsing shadow — the glow is cast **by** the authored panel, not
a drawn box — holding the four authored buttons: `btn_save`, `btn_load`, `btn_options`, `btn_exit`.
EXIT GAME *is* RETURN TO MAIN MENU, per Mike. Save and Load open a three-slot list on the same
panel with the slot summary in the BOF face.

`dlg_window` has a deep frame — thick top rail, bottom lip with an emblem — so the list needs real
padding at both ends. At the first sizing the bottom button was clipped by the lip.

## ⚠ 3. The persistence already existed, and I duplicated it

`campSnapshot` / `campWriteSlot` / `campReadSlot` / `campApply` / `campSlotUsed`, keyed
`bof_campaign_slot<i>`, plus CAMPHUB's own save and load flow, have been in the file since the
save-slot drop. I wrote a second copy before `node --check` caught it with `Identifier
'CAMP_SLOTS' has already been declared`.

Two lessons worth keeping:

- **Grep for `camp` before adding campaign state.** The save system sits far down the file, well
  past the hub's drawing code, and a `grep -i slot` truncated at the first dozen hits misses it
  entirely — which is exactly what happened.
- A test that wrote `bof_camp_0` by hand showed `SLOT 1 EMPTY` and looked like a bug in the label.
  It was the *test* using a key the game never uses. Re-run through `campWriteSlot` and it reads
  back `SLOT 1  STAGE 3  COLE`. **Drive persistence tests through the game's own writer.**

The pause reuses all of it. It adds a way *in* from anywhere in the campaign; it does not add a
second store.

## 4. An assertion that pinned a whole line

Section 215 pinned the literal `if(typeof menuBackTick==='function' && menuBackTick()) return;`
and failed the moment that line legitimately gained a `!campPause &&` guard.

Its stated intent is *"checked once in drawScene, not copied into each screen"* — still true. So
the pin moved to the call rather than the whole line, and a **count** assertion now enforces the
"once" the prose was really about. Four assertions were added for the pause itself: the back key
opens it, it offers save/load/options/exit, all four button keys resolve to real art, and
`campaignEnd()` actually clears campaign mode.
