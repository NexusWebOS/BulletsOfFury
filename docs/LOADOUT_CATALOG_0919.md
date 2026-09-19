# Loadout catalog repair — 2026-09-19

UI-19 and UI-22 are complete. The Loadout arsenal now displays nine element combinations across two pages instead of ten compressed cells per row. Controller D-pad left/right selects BASE or an element and changes pages; up/down scrolls weapon rows. A equips, B returns to the six bays, and Start launches. The authored pad graphics label these actions. Mouse wheel and two-step click selection also work.

The focused row and selected combination pulse visibly. A line above the catalog states the chosen weapon/form and whether it is OWNED, BOSS LOCKED, or purchasable in the Armory with its current Fury Point price. Selection accepts the weapon already in the current bay and can switch its form. The first page's authored icons are warmed at screen entry.

Verification: `node --check assets/game.js`, `git diff --check`, and a native Chromium Playwright probe passed. The browser probe traversed to the ninth element using repeated pad taps, moved six rows, equipped Fire on Spread via the A button, decoded first and last page icons, and saw no page/console errors. Screenshots were inspected at top and bottom. The broad legacy suite finished with 76 failures; the previous run had 79, and no new failing assertion name appeared.
