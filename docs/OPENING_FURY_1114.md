# Fury Division cinematics — November 14 correction

Active original BOF build: D:/BOF-Downloads/2026-11-14/RevG-source, based on fa1a40fca. The original C: checkout is preserved.

Mike rejected the detached pilot face pasted into an aircraft nose over tiled jungle, and the split-screen Chronos finale. Both are superseded by assets/cinematic_corrections_1114.js, loaded after assets/opening_fury_1114.js.

Stage 5 uses the exact original pre-comic h3EndingDraw and hf17Warm captured in CB1110.base. The native core shot, overload, explosions, scattering armor, aftermath and reentry remain. No giant aircraft/comic split-screen is drawn. No death timing, damage, progression or reward changes were made.

Stage 1 is a horizontal strip of three distinct full scene panels with ink borders and visible paper gutters. A 1.65-second camera slide moves between an actual selected-pilot aircraft flying over a newly illustrated aerial jungle valley, the selected pilot's complete authored cockpit portrait, and the forward view toward the blast. All nine current cockpit plates are used intact. The rejected detached portrait/aircraft nose composite is bypassed. Dialogue sits in the authored comic paper caption. The right-side BOOM graphic, game explosion sound and brief warm flash lead into the jungle order, resolve and fade to the complete native level card and launch. Start keeps the native skip continuation.

The prior requested Fury Division logo/crawl, 107.82-second readable prologue with pixel transitions, closing hope passage and 12-second campaign-map zoom remain. Newly generated art, raw source PNGs and exact prompts are retained in OPENING_FURY_ART_1114.json.

Verification: syntax passes for both new runtime modules; the full regression runner exits 0 with 8,969 passing assertions, zero failures and its success banner. Native Chromium verifies all nine selected pilots, actual map selection to comic, skip to card, complete comic to launch and one BOOM cue. The Stage 5 death checkpoint advances through drain, pulse, lock, missile, engulf, burst and aftermath in order, with one core impact and zero calls to the rejected split-screen renderer. Reentry and the native Stage Clear continuation were independently checked. Page, console and asset error collections are empty. These are cinematic checkpoint checks, not full campaign playthroughs.

Evidence and audio-enabled real-time recordings: _shots/opening_1114/review.html. Opening/map video remains current; Stage 1 video was replaced after the correction. Initial rejected screenshots retained in the C: temporary evidence directory are obsolete. QA: docs/qa/opening_fury_1114.json. Reproducible probes and recorder: _BUILD_SOURCE/probe_opening_fury_1114.py, probe_cinematic_corrections_1114.py and record_opening_fury_1114.py; use the running D: server on port 8765. These copies save to the build's _shots/opening_1114 directory.

No commit or push was performed.
