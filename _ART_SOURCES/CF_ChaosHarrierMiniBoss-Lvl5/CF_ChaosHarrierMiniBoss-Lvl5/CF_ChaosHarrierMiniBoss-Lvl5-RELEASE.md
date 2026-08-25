# CF_ChaosHarrierMiniBoss-Lvl5

Production pack for the corrected Level 5 Chaos Harrier space mini-boss.

- 6 fixed-canvas ship states; runtime idle holds frame 0 without hull swapping
- 6-frame registered internal-light glow overlay at 352x320
- Side pods are laser cannons; both burst patterns use laser projectiles only
- Missiles launch only from the exposed red bays while attack_open is held
- Reactor-powered giant beam emits from the nose and has a dedicated 6-frame muzzle flash
- 8-frame teleport warp with mirrored warp-in/out timelines
- 4-frame continuous nose beam, twin side-laser travel, and impact animations
- Hard-alpha runtime PNGs with zero hidden RGB
- Exact #FF00FF normalized sources plus untouched generated sources
- Engine-neutral AI, animation, attack, teleport, difficulty, map, and validation JSON
- Dedicated breakup/death explosion art remains a future companion pack; the AI emits a death-sequence event hook
