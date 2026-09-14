# BulletsOfFury reference pass

Read-only source inspection; no edits or integration into the game repository.

- `assets/game.js`, `eShoot` around line 23095: machine-gun shots pass through a forward-cone clamp and use the approved pellet sprite. Adapted into a ±0.66-radian facing cone, limited-speed turret aim, and the local `mfx_ea_0_3` pellet crop.
- `_BUILD_SOURCE/gamecode.js`, `droneFire` around 2759: aimed lances and fans centered on the target. Adapted into rotating cannon shots and short three-round fans with 0.17-radian spacing.
- `_BUILD_SOURCE/gamecode.js`, homing boss profile around 5165 and enemy homing pattern around 9187: alternate gun fire and missile salvos, with lock-on warnings. Adapted into separated burst/spread/lock/salvo/reload stages.

These are standalone adaptations of the game's behavior conventions, not a claim that the full BulletsOfFury runtime is embedded. Speed values use pixels per second in the standalone engine. The original game remains unchanged.

New mount generation used built-in ImageGen with the jet as the style reference: two isolated cells containing a round armored twin-cannon turret and a separate bolted hydraulic carriage, gunmetal/crimson/cyan colors, genuine alpha, no cockpit/wings/exhaust/labels. The resulting turret is normalized around its bearing center. Carriages remain attached to the wing while the cannon carriage travels a short distance along the local rail.
