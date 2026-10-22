# Decker's Upgrade Center (2026-10-22)

Mike: *"forge/loadout should allow you to enter - The Forge or Select your Loadout, our exisiting screens. But a player
may have forgotten to upgrade a weapon, or wants to re-spec. This should be Decker's Upgrade Center. and be located on
the map directly next to Fury HQ and we can travel to it too and select it to enter it."*

Runtime: `assets/upgrade_center_1022.js`, loaded after `start_menu_1022.js`. `window.UC22_OFF=1` turns it off.

## For the player

- **On the campaign map** a hangar island sits east of Fury HQ, labelled UPGRADE CENTER.
- **UP from Stage 1** flies the jet there; the camera frames Fury HQ and the center together and the briefing card
  reads DECKER'S UPGRADE CENTER. DOWN, LEFT, RIGHT or B fly back to Stage 1. A click on the island goes there; a second
  click enters. FIRE never deploys a stage from here.
- **FIRE enters**: Decker at his bench, the upgrades and re-specs this stage still has, and three choices:
  THE FORGE, SELECT YOUR LOADOUT, LEAVE. Both are the existing screens. When either closes, the game comes back to
  the map with the jet still parked and Decker's screen open, so a player can forge and then change the loadout.
- **The START menu's FORGE / LOADOUT row** opens the same screen.

## Notes

- The Forge keeps the stage's own upgrade and re-spec budget. `forgeStart` refills it on every open, so the counts are
  put back, as the START menu already did.
- The camera has its own eased value written over the close follow-camera. Easing the shared camera settled halfway
  between the two targets (measured zoom 1.13 against the 0.48 asked for).
- Once the Stage 9 bonus is earned the map only selects Stage 9 (Mike's rule), so the center cannot be reached then.
- **Art:** the island is the authored 0930 northern hangar island (`campaign_0930/northern_hq_island.png`), which left
  the map when Fury HQ moved onto its 1004f region. SpriteCook had 2 credits, so nothing was generated. A dedicated
  plate drops in by repointing `UC22_ART`.

## Verification

`_BUILD_SOURCE/probe_upgrade_center_1022.py` (real Chromium, real key presses): **20/0, 0 page or console errors**, with
a busted arm (`UC22_OFF=1`: UP from Stage 1 no longer reaches it). `probe_start_menu_1022.py` 33/0 with its FORGE /
LOADOUT steps moved onto the center. `probe_menu_confirm_0918f.py` 9/0. Proof frames: `docs/proofs/upgrade_center_1022/`.
