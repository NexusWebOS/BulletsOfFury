# Opener pilot-and-ship lineup — 2026-09-15

UI-07 complete. The two silhouette cards and scrolling roster now pair front-facing authored pilot cutouts with each pilot's ship. Cole opens the first card and leads the nine-pair sweep. The sweep takes 12 seconds instead of 2.9; every pair passes the central spotlight with its own name and colored rim. A subtle authored-color layer preserves identity within the silhouette treatment.

All nine *_body_0 figures were visually inspected before use. They are transparent, front-facing cutouts, avoiding the opaque-square silhouette produced by framed portraits. Lizzie uses ship_lizzie_pv2 because her cinematic sheet still depicts the superseded bomber. Silhouette cache follows source-image identity for costume changes.

All pair assets warm together at opener start. Pair beats pause for ordinary lazy decoding, bounded to four seconds so a missing asset cannot trap the opener. Existing any-input skip, music handoff, later montage and title menu stay in place. This modifies the title opener, not the stage introduction cards.

Native Chromium: all nine pair samples inspected; all source assets ready; Cole and corrected Lizzie screenshots saved under _shots/opener_lineup_0915. Registered Enter input through the opener handler reached title. Console errors zero. Later gameplay montage was not independently replayed.

Syntax passed. Full suite: 3,850 passed, 58 known failures, exit 1; no new failure names. See [QA](qa/opener_lineup_0915.json). Recreate the isolated review with `python _BUILD_SOURCE/create_opener_lineup_review_0915.py`.
