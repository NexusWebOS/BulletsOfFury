# Current cinematic, Stage 4, password and pickup fixes — 2026-09-20

- Cinematic ship selection now resolves all nine pilots through the same `ship_<pilot>_pv2` and bank frames used by gameplay. The retired `cinship_*` cutouts are no longer registered or loaded. Original source art remains in the asset archive. The Stage-1 Campaign bridge and opening silhouette use the current ships.
- Hard/Furious Stage-4 Olive Warden escorts now accept shots at their own positions even when outside the miniboss hull rectangle. The broad-phase gate had consumed or skipped hits until the player approached the center. Ordinary rounds, Laser Mist, Yuri's lightning, held beam and flame routes now reach the escort hitboxes.
- Stage passwords now lead to difficulty selection, then pilot selection, then the selected Arcade stage. Back navigation returns to the password screen from difficulty. Special unlock passwords retain their existing behavior.
- Pickup announcements and field popups use the authored shaded game alphabet. They wait for bitmap art instead of briefly drawing a plain canvas-font fallback.

Real Chromium: `_BUILD_SOURCE/probe_campaign_bridge_0920.py` passed for Yuri/Cole and Stage Clear routing. `_BUILD_SOURCE/probe_latest_repairs_0920.py` passed password order, a distant Warden escort losing 60 HP to a shot, and graphical pickup capture. Both reported zero page/console errors. Screenshots and probe data are under `_shots/campaign_bridge_0920/` and `_shots/latest_repairs_0920/`.

The full assertion suite retains its known nonzero exit; current result and failure-name comparison are recorded in `_shots/test_fl_latest_0920_final.log`. No commit or push.

## Furious recording review (12:03:09 capture)

- The six Loadout bays now keep their weapon categories. Down opens that weapon's forms, left/right cycles its base type, and up/down browses its earned combinations. Selecting a form changes only that weapon; old cross-bay `forgePick` swaps are disabled. The Forge and Loadout headers were moved into the plate's title area, and the form readout stays inside its window.
- Difficulty elite jets retain their authored flight and volleys but no longer equip the incomplete directional shields seen around their hulls. Elemental shields on ordinary enemies and boss mechanics remain.
- The fullscreen menu has a black surround, the authored Bullets of Fury logo in the right panel, no Fury HQ caption, and centered panel rows. The Campaign map uses a seamless ocean texture in the live map and its wide extension so a tile boundary no longer cuts across the theater.
- Real Chromium proof: `_BUILD_SOURCE/probe_0920_fixed_loadout_menu.py` captured the menu, map and form states with zero page/console errors. Its equipped form changed while all six loadout positions stayed identical. The full suite still exits 1 with exactly the same 76 failure names as `_shots/qa_0920_audio/test_fl_final.log`; no new assertion failures.
