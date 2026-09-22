# Campaign flight bridge — 2026-09-20

Stage 1 Campaign clear now plays a short flight scene before the campaign map. The selected pilot flies with Cole, or Axel when Cole is selected. Their existing top-down ship cutouts travel over the authored Stage-1 jungle terrain while a three-line radio exchange uses the current framed dialogue UI, compact front-facing comm portraits, pilot tint and dialogue font. The Start skip prompt sits clear of the dialogue panel. Arcade still advances without this scene. The archived HQ ensemble scenes remain archived.

`_BUILD_SOURCE/probe_campaign_bridge_0920.py` exercised Yuri and Cole in real Chromium, captured both at `_shots/campaign_bridge_0920/`, and verified the Stage Clear route enters the scene, leaves it for Stage Select, and completes the Level-2 map unlock animation. Both page and console error lists were empty. The screenshots were inspected; both ships, portraits, text and skip prompt fit without overlap.

`node --check assets/game.js` and `git -c core.whitespace=cr-at-eol diff --check` passed. The full `node _BUILD_SOURCE/test_fl.js` run reached its summary with 76 failing assertion names, exactly the recorded `_shots/qa_0920_audio/test_fl_final.log` set. It exits nonzero; no new failing names appeared.

This is one transition, so PRE-11 remains partial. Later-stage scenes and any cockpit/POV beats still need story and visual review.
