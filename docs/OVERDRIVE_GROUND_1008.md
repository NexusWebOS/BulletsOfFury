# October 8, 2026 — Overdrive ground campaign

Mike requested the Warrior arena/control/destruction upgrade, then a playable
on-foot mission and a separate hostile Machinists tank mission with a named ally.
This work extends the existing standalone `expansion/topdown/` build. It does
not integrate a new ground mode into `assets/game.js` or change the base atlas.

## Current entry point

`expansion/topdown/index.html`: select Levels 2, 3 or 4. Start from results
advances to the following mission. See `expansion/topdown/README.md` for exact
controls, behavior, art builders and limitations. F1 opens contextual Help.

- **Level 2:** direct smooth movement; independent mouse/right-stick/Q-E turret
  aim; Shift/C hull lock for sideways strafe; player charge tension and recoil;
  gold/silver/crimson laser tiers; authored tank missiles; destructible buildings
  and concrete walls with collision/LOS retirement, generated bursts/dust and
  solid rotating fragments. Original **The Warrior** has a helmet torso, two
  arms and a sideways-turning chassis. Its attacks are volleys and a warned ram,
  without boss charge orbs. Arena zoom fits the helmet and player; out-of-map
  margins clear correctly. Tank deaths use an anchored 720-degree burning spin,
  crash, shock ring, explosions and a solid wreck.
- **Level 3:** existing Miami route plus a generated gate-free terrain edit;
  independent movement/aim; helmeted authored pilot bodies; six finite-ammo
  weapons, reload, prone/crawl, vulnerable roll, committed grenade release,
  stealth/wall noise, tall-stack foreground occlusion. One hit causes death and
  consumes a life. Three fortress sentries hold a dynamic gate; opening removes
  movement/projectile/vision collision. Crossing the north exit completes it.
- **Level 4:** generated coastal rail/factory route; rocket, rail and siege enemy
  tank roles; choose Hotwire/Phoenix/Niel support in the briefing. Rogue Wren,
  Rolf and Chaz attack both the player and companion. Their calibrated modules
  use shared draw/hit/muzzle transforms and distance-driven track phases.
  Detached pieces keep their exact mounted art, opacity, angle and anchor.
  Broken modules cancel owned projectiles and give recovery openings.

## Ownership

Loose generated assets and intact sources: `art/ground_1008/` and
`art/campaign_1008/` under `expansion/topdown/`. Each directory has its owning
Python builder, source/prompt records and runtime manifest. Existing ground,
on-foot and Windstorm/Machinist assets are referenced, not duplicated into a
new base atlas. The early Huntsman concept is retained but is not the active boss.

New gameplay modules: `structures.js`, `boss_warrior.js`, `campaign.js`, and
`boss_machinists.js`. The previous `boss_razorback.js` remains as historical code
and is not loaded. `DESIGN.md` explicitly labels the older proposal as history.

Mike authorized GitHub publication on October 8. This publication contains the
standalone expansion code, authored art and sources, owning builders, native
probes and portable results. Unrelated base-game HUD edits and other user work
remain local. Development captures remain under ignored `_shots/`.

## Verification

- `node --check` passed for every expansion JS file and `assets/game.js`.
- Full `node _BUILD_SOURCE/test_fl.js`: **7,952 passing assertions, zero errors,
  exit 0**, and `FALVA/LIZZIE BUILD OK` final summary.
- `probe_ground_1008.py`: **23/23** native Chromium checks.
- `probe_campaign_1008.py`: **29/29** native Chromium checks.
- Both probes use `_BUILD_SOURCE/shoot.py`'s server helper. No page/console/HTTP
  errors. Stage, menu, gate, charge/weapon, arena, breakage, death and result
  screenshots were inspected. All campaign warm keys decode.
- Logs, JSON results and captures are in ignored `_shots/ground_1008/`.

Native Chromium subprocess launch requires sandbox escalation on this host;
automatic approval review allowed the read/verify commands.

Protected fixtures establish mechanics, collision, pixels and transitions.
They do not establish unassisted clear rates or final balance. Existing generated
body/track sequences retain some pose/detail drift. Fusion fires piercing pulses.
Save-state and base flight-campaign integration remain separate work.
