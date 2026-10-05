# Thirteen passwords — October 4

The password screen retains difficulty and pilot selection. `HARR6` and `REBEL6`
then launch the selected full Stage 6 boss encounter immediately, skipping the
opening flight, enemy waves, miniboss and route selection. Each fight retains its
own introduction and four friendly wingmates. Stage X rematches remain separate.

| Destination | Password |
| --- | --- |
| Stage 1 | FURY |
| Stage 2 | IRON |
| Stage 3 | DAM5 |
| Stage 4 | STRM |
| Stage 5 | ORBT |
| Stage 6 | TURB |
| Stage 7 | SEWR |
| Stage 8 | DETH |
| Stage 9 | RIFT9 |
| Stage X — Harrier | XHARR |
| Stage X — Rebels | XREBEL |
| Stage 6 — direct Harrier fight | HARR6 |
| Stage 6 — direct Rebel fight | REBEL6 |

Direct Stage 6 Harrier uses Level 6 boss music. Rebel fights and both Stage X
encounters use Level X music. Shortcut state is consumed once, cleared by ordinary
stage passwords, and explicitly reset when launching Stage X from the campaign.

Implementation: `assets/gameplay_repair_1004.js`; campaign reset:
`assets/campaign_focus_1004b.js`. No art or music files changed.

Verification: syntax checks passed for the base game and both changed extensions.
The complete `_BUILD_SOURCE/test_fl.js` suite reached its final summary with 7,118
passing assertions, exit 0, including 29 new password assertions. Native Chromium
probe `_BUILD_SOURCE/probe_password_routes_1004d.py` passed 36 checks, including
actual keyboard entry for all thirteen codes and actual startRun for all four
encounter codes. Zero page or console errors. Inspected password entry, complete
Harrier hull, Rebel arrival and five friendly ships in screenshots.

Portable report: `docs/qa/password_routes_1004d.json`. Logs and screenshots:
`_shots/password_routes_1004d*`. This verifies routing and encounter entry, not a
human completion of every campaign stage. All work remains local and uncommitted.
