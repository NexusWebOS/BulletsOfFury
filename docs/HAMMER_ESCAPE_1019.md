# Hammer dodge and jump strike — 2026-10-19

Requested fix: shorten post-spike persistence and replace the delayed side slide with a jump strike.

- Shared HC11 Chromium columns: total visible lifetime 1.18s -> 0.44s; damaging interval 0.10s–0.32s; 0.10s collapse. Existing 1.2s minimum warnings, spacing, authored beam art and lower-half bounds retained. Both roll (0.46s) and somersault (0.62s) outlast a full spike.
- Upper-half counter: stationary difficulty-scaled windup (Easy 1.00s, Normal 0.90s, Hard 0.80s, Furious 0.75s), followed by a 0.42s raised jump arc to the captured world target. Landing release lasts 0.16s, recovery 0.42s. Existing whole-body swing plates, measured hammer-tip collision, FOV coverage, impact sound, hit flash, module-break commitment and Stage 8 donor rig remain shared. No tracking after target lock and no airborne body damage.
- Cache refreshed for HC11 in index.html.

Validation: node syntax checks for game.js and HC11 pass; full test_fl.js exits 0 with 8,793 passing checks and final BUILD OK banner. New native Edge probe passes 17 checks across Easy/Normal/Hard/Furious, including actual startRoll/startSomersault iframe expiration versus the complete spike, harmless flight and leaving the landing target. Native screenshots inspected; no page, console or asset errors.

Evidence: _shots/hammer_escape_1019/report.json; jump-midflight.png, jump-landing.png, spike-live.png; _shots/hammer_escape_1019-tests.log. Reproduce with _BUILD_SOURCE/probe_hammer_escape_1019.py.

Local implementation only; not committed or pushed. Preserve all unrelated download, audio/FOV and Overdrive work.
