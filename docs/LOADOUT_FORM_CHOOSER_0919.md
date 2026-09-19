# Loadout form chooser — 0919

The form chooser now uses the displayed badge rectangles for mouse selection. A click on a different badge moves focus; a second click equips the focused form. Clicking outside the form badges leaves the selection unchanged. The Re-spec button remains independently clickable.

While the chooser is open, the arsenal catalog rows and their status readout are hidden. The authored Loadout plate, form badges, focused weapon heading, and matchup banner remain visible. Returning to arsenal browsing restores the catalog.

Chromium proof: `_shots/loadout_form_click_0919/selected.png` and `equipped.png`. The focused probe selected Ice Breath from Freezer's Flamethrower bay, then equipped it on the next click; the weapon bay list stayed unchanged and no browser console errors occurred.

Validation: `node --check assets/game.js` passed. Full `_BUILD_SOURCE/test_fl.js` remains nonzero at 76 historical assertion failures; the current failure set has one fewer than the earlier 77-failure baseline and no new failing assertion names.
