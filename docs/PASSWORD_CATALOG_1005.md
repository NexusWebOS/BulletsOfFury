# Pinned in-game passwords — October 5

Mike requested all new and current passwords pinned in the game. The Password
menu now has a permanent **Pinned Passwords** button above the on-screen keypad.
It is reachable by mouse and the existing D-pad/A navigation. The existing pad
Retina/C binding also opens it outside typing mode; typed C remains a normal letter.

Nine pages cover all 59 codes: stages, sky encounters, main bosses, minibosses,
alternate/musical fights, finale phases, finale copies, unlocks and Cole scene
previews. Stage/encounter/scene entries derive from their live registries. Additional
registered stage codes automatically appear on an Other Stage Codes page. The
three older unlock handlers and two musical encounter handlers are included
explicitly because they are outside the stage-password registry.

The D-pad changes pages and rows. A fills the selected code and returns to entry;
B closes the catalog and preserves the current entry. Mouse rows select codes and
the Prev/Next headings change pages. Selection never submits, launches a fight,
grants an unlock or writes storage. Enter/Start submits through the existing
difficulty/pilot flow. The catalog is always visible, independent of saved progress.

The same native keyboard check caught an existing double-Backspace deletion:
the raw text queue deleted once, then the bound-key path deleted again. Raw
keyboard edits now consume their duplicate key tap before the old entry path runs.
The explicit typing mode likewise consumes duplicate raw letter taps. Backspace
edits text and never acts as Back. Queued letters are discarded while browsing so
navigation cannot leak into the password box on return.

The new view reuses existing game panel helpers, stage bitmap fonts and generated
pad graphics. Code lettering is 17 pixels, labels have an 11-pixel floor, and all
rendered text is measured against its panel. No replacement sprites, new bitmap
assets or atlas edits were needed.

Runtime: `assets/password_catalog_1005.js`, registered after the encounter routes
in `index.html`. Full reference: [all current passwords](PASSWORD_ENCOUNTERS_1005.md).
Native verification: `_BUILD_SOURCE/probe_password_catalog_1005.py`. It checks all
59 selections, registry completeness, nine-page bounds, native pointer opening,
keyboard/pad ownership, single-character Backspace and normal FINAL2 submission.
All nine pages and the entry button are captured from the game canvas and visually
inspected. Portable results: `docs/qa/password_catalog_1005.json`.

Verification passed: 7,274 full-suite assertions (exit 0), 89 native Chromium
checks and zero browser errors.

This follow-up remains local until Mike requests publication.
