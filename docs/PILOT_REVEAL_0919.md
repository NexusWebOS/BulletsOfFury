# Pilot Select reveal (UI-20)

The live Pilot Select renderer now starts a fresh reveal when the visible pilot changes. The selected pilot's name and affiliation type in sequence. Stat labels appear with their corresponding bars, which fill one at a time using the existing `statTick` sound. Selecting a pilot still shows the clean GOOD LUCK card with the pilot and ship.

Verification: `node --check assets/game.js`, `node _BUILD_SOURCE/test_pilot_reveal_0914.cjs` (9/9 pilots), `node _BUILD_SOURCE/test_pilot_deploy_pad_0916.cjs`, and live Chromium capture via `_BUILD_SOURCE/shoot.py --state PILOT` at early, middle and finished reveal frames. The full legacy suite retains known unrelated failures.
