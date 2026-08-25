# Combat pack review — no wiring performed

## Decision

The five supplied ZIPs are isolated in this review folder. Nothing was copied to `assets/game`, added to `assets/manifest.js`, or connected in `assets/game.js`.

- **Volume 1:** hold. It supplies 208 enemy behavior JSON files but only stage-level preview reels, not the per-enemy runtime frames needed for visual approval. It contains 34 unique pattern sets, so many enemies still behave identically.
- **Volume 2:** hold. It supplies 48 combatants and 32 VFX families with clean binary alpha, but only 23 unique pattern sets. Baked attack flashes conflict with separate muzzle references, 39 death reels end in a dissolve-style silhouette loss, and 11 combatants have at least one frame touching the canvas edge.
- **Doomsday Carrier Mk II:** conditional candidate. All 98 full-boss frames preserve the 640×320 origin, hard alpha, and safe borders. The six patterns are visually readable, but several gameplay rules are underspecified.

## How the supplied enemy system works

Each Volume 2 combatant has a six-frame 10 fps power loop, an eight-frame 12 fps firing reel, a four-frame hit reel, and an eight-frame death reel. JSON declares fixed weapon anchors and says projectiles spawn on firing frame 4. Four attack patterns are then selected: a basic aimed burst, a fan, a composite/signature volley, and a below-35%-HP rage volley.

That is a **firing system**, not a complete enemy behavior system. The JSON does not define entry formation, movement, retreat, strafing, dodging, player-zone limits, or safe-gap policy. The current game already owns those through its entry AI, roster-specific ticks, and `ENEMY_VOLLEY`; a later integration would need one clear owner for movement and one for shooting to avoid double-firing.

## Blocking findings

1. **Behavior duplication:** 208 Volume 1 enemies collapse to 34 firing sets; 48 Volume 2 combatants collapse to 23. The four Volume 2 fortress bosses share the same aimed burst, 54-degree fan, 104-degree secondary barrage, and 360-degree critical rage with only palette/projectile/speed changes. That does not meet the requirement that every enemy, miniboss, and boss behave differently.
2. **Firing timing conflict:** the reels declare projectile spawn on frame 4 (about 250 ms into a 12 fps animation), while many JSON pattern events begin at 0, 110, and 220 ms. The event clock needs an explicit relationship to the firing reel or projectiles will precede their muzzle flash.
3. **Double muzzle risk:** attack frames visibly bake muzzle bursts into the hull, yet every JSON also names a separate muzzle VFX. Choose baked port lighting or independent muzzle animation—not both.
4. **Dissolve deaths:** 39 of 48 death reels lose over 65% of initial silhouette coverage by the final frame, often through a repeating circular mask. Replace those with solid breakup/explosion frames and a hard removal after the final explosion; do not opacity-fade the hull.
5. **Canvas-edge risk:** 14 frames across 11 combatants touch an outer canvas edge. These need padding or inspection before atlasing to avoid clipping.
6. **Early-stage density:** several standard Stage 1 units receive 12-shot 360-degree critical rings; hazards receive 16-shot rage rings. That is too much shared omnidirectional pressure for early fodder and conflicts with the current Stage 1 projectile-volume tuning.
7. **Hazard identity:** ammo crates, fuel barrels, fuel tanks, and river mines share one four-pattern detonation kit and reference a military cannon muzzle. Their behavior should be proximity/fuse/chain-reaction driven without gun-style muzzle flashes.

## Doomsday Carrier attack explanation

- **Cyclone Barrage (phase 1):** alternates the two lower pods, firing six three-way fans over 1.28 seconds. Its 220 ms telegraph is the shortest and should be tested at gameplay scale.
- **Prism Crossfire (phase 1):** four upper barrels fire mirrored diagonal lanes three times, reversing the cross angle on the middle volley.
- **Omega Bomb Run (phase 2):** both bays release reflectable bombs after a 720 ms warning. The pack needs explicit deflection input/window, reflected speed/damage, fuse behavior after reflection, and boss-hit result.
- **Chrome Flak Fan (phase 2):** alternating lower cannons fire four timed airburst shells. The JSON specifies five child angles but not child speed, collision size, or lifetime.
- **Storm Cage (phase 2):** four nodes deploy into the lower field and link into a rotating-gap enclosure. Link thickness, damage cadence, activation telegraph, and safe-gap width are missing.
- **Doomsday Fusion (phase 3):** combines bomb corridors, cyclone tracers, prism pressure, and the central beam. It has only a prose description—no deterministic event timeline—so it cannot yet be wired faithfully.

## Approval path

1. Approve/reject the six Carrier visuals individually.
2. Redesign the four fortress bosses and elite/miniboss families so each has a distinct fight mechanic, not a recolored shared template.
3. Replace dissolve deaths and decide whether firing flashes are baked or separate.
4. Supply the nine Volume 1 runtime packs if those 208 animations are candidates for use.
5. After a second preview pass, wire one stage behind a feature flag and playtest bullet density before expanding to the whole roster.
