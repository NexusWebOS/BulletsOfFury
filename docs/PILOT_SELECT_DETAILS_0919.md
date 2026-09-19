# Pilot Select identity and reveal — 2026-09-19

Pilot Select now types the selected pilot's name, role, callsign, affiliation and biography before filling each stat bar in sequence. The special ability and its existing boxed icon land after the bars. The right bay has a compact responsive layout so Cole's five stats and long biography, Falva's five stats and Lizzie's card remain in the panel. The existing full-body pilot and rotating ship stay visible. On confirmation, the GOOD LUCK slide still shows only the pilot and ship.

The difficulty screen starts decoding all nine roster portraits, ship level views, standing poses, affiliation badges and special icons; direct Pilot Select entry repeats that warm-up. No new art was generated.

Chromium visual QA captured all nine fully revealed cards at 1280×720 and Cole's dense card in a fresh 1024×768 session. The GOOD LUCK slide was also captured. No page errors occurred. Screenshots are in `C:\Users\Mike\Documents\New project\pilot_details_shots`. `node --check assets/game.js` passed. The full legacy suite returned 75 existing assertions versus the prior 76-failure baseline, with no new failure names.
