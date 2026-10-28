# Gosfar / Hotwire pass45 — local, 2026-10-18

Build `overdrive1018-gosfar45-r2`. Original level 3 three-relay objective remains.

The lower hexagon has a continuous five-module destructible grey wall plus a shorter right return. Yuri braces at its right edge, then lowers prone during the opening barrage. Hotwire's left slab remains indestructible. Tall side panels are visible before their half-health claymore breach. Feet are constrained to the authored hexagon rather than its painted rails.

The PixelLab lift rises after Gosfar exits. Each 15% health loss queues exactly one reinforcement visit, including skipped health bands: six visits total. Arrivals walk out of the cabin before attacking. Victory recalls the lift, animates both crew members walking inside, closes doors, fades and reaches the real Overdrive stats screen.

Gosfar uses the new silver/violet giant Gatling plates in four directions. Aim direction and projectile sockets follow the same committed target. Furious has 1500 HP, 104-round high sweeps, faster recovery, low bursts and three timed ground grenades. High fire passes over prone Yuri; low fire and grenades hit prone. Grenade targets stay committed and spread at corners instead of stacking. Half-health flamers, pickups and Hotwire's physical peek/fire/support routes remain active. The supplied Last Hope WAV starts at the boss-bar reveal.

Hotwire now shares rifle and Desert Eagle plates between NPC and playable use. Tab swaps weapons, R reloads (30-round rifle / seven-round pistol), F toggles prone, Space/H/V rolls, WASD moves and mouse aims/fires. Moving fire and continuous stationary fire use advancing clocks instead of resetting on every shot. Options/help distinguish her R reload from other pilots' existing jump binding.

Art: 192 banks / 1309 registered cells including aliases and holds. Fixed body units, even canvases, common roots, hard alpha and shared palettes. Onion review is `expansion/topdown/art/gosfar45/review/index.html`; canonical source, job IDs and rejection decisions live under `art/gosfar45/source`. Builder: `_research/build_gosfar45.py`. Exact west jump mirror was verified pixel-for-pixel. Rejected red silhouettes, white guns and whole-body firing recolors are excluded via clean whole-pose holds.

User explicitly chose “Finish with the available art” after credits depleted. No further paid generation. Five crouch-walk directions deliberately use quiet crouch holds: rifle south and Desert Eagle north/south/east/west. These are not bespoke moving clips. Some individual rejected phases also hold the nearest clean authored drawing. Do not claim all registered cells are unique or all requested animations are complete.

Validation: 366 production-module/native checks pass, including actual exported pixel motion for rifle/pistol cardinal walk/fire/run-fire, real input magazine/reload/prone, all six reinforcement waves, grenade damage/roll/prone behavior, main cinematic, escape and level 4/5 smoke checks. Full required suite: BUILD OK / 0 ERRORS / exit 0. Real Chromium input and canvas captures verify the encounter, separated grenade retinas, shared lift exit, results and Hotwire controls; no console errors. These use protected fixtures, not an unprotected Furious balance clear. Evidence: `_shots/gosfar45`; portable report: `docs/qa/gosfar45-1018.json`.

No changes to core assets/game.js or _BUILD_SOURCE/test_fl.js, no commit/push/deployment. Preserve unrelated dirty files. Active modules are gosfar45.js and hotwire45.js; compatibility state/API names gosfar43 remain intentional.
