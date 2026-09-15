# Generated pause buttons — 2026-09-15

UI-06 complete. A SpriteCook metal-and-green button plate now backs all six pause actions: Resume, Return to Main Menu, Restart Level, Options, Help and Quit Game. Existing authored bitmap labels, cursor, entrance timing and controls remain in use. Three-part horizontal drawing preserves the endcaps while fitting the center to the existing hit rectangles. Selected rows brighten and glow. The existing panel remains a temporary lazy-decode fallback.

Asset: assets/game/ui/pause_0915/button.png. Owning asset ID, hash, generation provenance and rejected versions are preserved in the adjacent spritecook-assets.json. No atlas mutation. Source draw rectangle uses alpha >180 to exclude the diffuse surrounding glow; the full original image remains on disk.

First processed candidate clipped its left endcap; cleanup did not repair it, so neither was integrated. The replacement was visually inspected before use. Total batch cost 16 credits, 118 remaining.

Native Chromium verified all labels and both selection states over the real frozen stage, selection from Resume to Return to Main Menu, and resume to play. No console errors. Save/quit operations were not re-exercised for this art-only change. Screenshot: _shots/pause_art_0915/menu.png. Reproduce with `python _BUILD_SOURCE/create_pause_art_review_0915.py`.

Syntax and whitespace checks pass. Full regression: 3,851 passed, 57 known failures, exit 1, no new failure names. [QA](qa/pause_art_0915.json).

Next: MODE-08 Life Up and Continue Up pickup graphics.
