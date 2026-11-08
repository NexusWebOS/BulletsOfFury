# Official mouse and keyboard tester build - November 5, 2026

The current local production game is packaged with every asset and extension, including the November 5 Razorwake, Thunderhead and Sumpjaw revisions. This is a snapshot of the current working game; no commit or upload was requested.

## Tester delivery

- ZIP: `BulletsOfFury-Official-2026-11-05-Tester.zip` (3,561,130,693 bytes / 3.56 GB).
- 18,772 entries; 3,619,157,078 payload bytes unpacked.
- Build ID: `BOF-Official-2026-11-05-MK-0903eec65a`.
- ZIP SHA256: `a5aa7e81dd8ee76b8a43dcc96a8dfcfccb18db85c42f1878f15873490823dcd0`.
- Core SHA256: `0903eec65a966a55980baef7a2eddf59ab4a3f18a8e77868ccb52fa90d231c91`.
- Extract everything, then double-click **START-BOF.cmd**. Keep the server console open. Windows 10/11, Windows PowerShell and an existing desktop browser are sufficient. No Python or Node installation is required. Game resources load locally without internet; optional online services still require their normal connection.
- Source metadata and per-file SHA256 hashes are included as BUILD-INFO.json and FILE-MANIFEST.json. HOW_TO_PLAY.txt and README-TESTER.txt explain controls and saves. All 18,674 files in assets/ and all 91 in extensions/ are included. Developer repositories, personal folders and review videos are excluded.

## Input contract

| Action | Mouse / keyboard |
|---|---|
| Primary fire | Left click / J |
| Retina | Right click / C |
| Missiles | Space / K |
| Multi-Retina | Hold Mouse Button 4 (Back thumb button; browser button 3) / Y |
| Multi-Retina alternative | Short right click, then right click again within 300 ms and hold the second press |
| Charge | Mouse Button 5 / H |

The first click must be at most 250 ms. The second held press uses the existing native scanner; Space launches the existing marked-target volley. Releasing stops acquisition while normal mark lifetimes remain. Menus keep Space as Confirm rather than treating it as missile/Back. Right-click context menus and thumb-button browser navigation are suppressed on the playfield. Pause, scene change and focus loss clear the gesture. Player 2 and controller controls retain their existing paths.

A one-time saved-profile migration reserves Space, right click and Mouse4 for these requested roles, preserves unrelated custom inputs, and respects subsequent remapping. The in-game Help captions are updated. The code uses the original missile, scan and damage paths.

## Verification and limits

- **23/23 focused checks passed** with real Edge mouse/keyboard events and CDP Back-button events: defaults, saved-profile migration, custom rebindings, native lock/missile/marked-target volley, both Multi-Retina shortcuts, menu Confirm, context/navigation suppression, timing boundaries, pause, focus loss and Player 2 separation. No page errors.
- **21/21 final package checks passed** from a full clean extraction: every ZIP entry CRC, all 18,771 payload SHA256 hashes, complete assets, standalone Windows server with Python/Node removed from PATH, audio byte ranges, offline boot, Stage 1-9 load/render, current boss atlas decoding, actual combat audio output, same-origin restart/save/control persistence, zero missing local resources or JavaScript errors.
- Combat audio analyser peak was 0.6032695174217224; this verifies decoded output, not subjective loudness or physical speakers.
- Syntax checks for assets/game.js and _BUILD_SOURCE/test_fl.js passed. Git diff whitespace check passed. Core LF and harness CRLF were preserved.
- The existing full regression harness still exits 1 before its final summary: `difficultyHealthBaseline15 is not defined` in assets/combat_polish_0927b.js:151, invoked by test_fl.js:4537. This was already present before this input change; it is not a full-suite pass.
- An initial packaging probe incorrectly called Stage 10 through beginStage(10). Stage X uses its own route on the Stage 6 setup, so that invalid fixture was replaced with the real Stage 1-9 table. No runtime workaround was added for this test mistake.
- This pass does not establish a full campaign completion, physical thumb-button driver compatibility, every pilot or physical controller verification. The tester should use the provided feedback details: stage, pilot, difficulty, weapon and reproduction steps.

Evidence: docs/qa/official_tester_build_1105/. Reproduction scripts: _BUILD_SOURCE/official_tester_build_1105/. Runtime art and combat balance were not changed by this input pass.
