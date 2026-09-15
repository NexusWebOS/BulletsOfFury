# Pilot ship rotation alignment — 2026-09-14

UI-10 complete. Pilot-menu ship drawing centers the alpha bounds of each authored image instead of its transparent canvas. One shared canvas scale per pilot preserves narrow side views and avoids scale changes while lazy assets decode. The decoded-image WeakMap follows XART costume cache replacement automatically. No atlas, gameplay ship rendering, rotation timing or authored pixels changed.

Native Chromium: inspected all 72 stock rotation frames and nine before/after onion overlays. Confirmed one scale per reel and centered visible bounds. Actual Axel and Decker menu previews and roster thumbnails rendered correctly; menu console errors zero. B-42 alternate costume was not separately captured. Existing source art has intentional perspective changes; this fixes positional drift without deforming those poses.

Syntax passed. Full regression: 3,850 passed, 58 known failures, exit 1; no new names against the pilot-reveal baseline. [Measurements](qa/ship_alignment_0914.json). Recreate review pages with `python _BUILD_SOURCE/create_ship_alignment_review_0914.py`; captured onion sheet is under `_shots/ship_alignment_0914/onion.png`.

Next queued item: UI-07, all nine front-facing pilots beside their ships in the title/intro presentation.
