# Stage 3 miniboss: ordinary weapons reach the core

Mike reported that the exposed core could only be hit with missiles.
The live miniboss is the authored Cryogenic Siege Carrier (`frostcruiser`),
drawn by `playthrough_1011.js`. Its modular weapons had valid hitboxes, but
`mr27HullAt` looked up its `frost1002` / `pt11_frost` skin in `MR27_ART`, where
neither current hull exists. It returned false across the entire body.
That made the ordinary projectile and orb collision paths miss the exposed
reactor. A locked missile used the direct encounter target and still hit.

## Repair

The owning mask builder `_BUILD_SOURCE/mr27_hull_mask_1017.py` now measures the
actual `PT11_ART.ice_parts[0]` hull with its mounted `[3]` reactor, using the
same pivots and proportional scales as the native draw. The generated
`MR27_HULL_MASK.rows.pt11_frost` contains a48×48 occupancy grid of those pixels.
The original Iron/Rime/Storm masks remain identical.

The Frost-specific `mr27HullAt` adapter in `assets/playthrough_1011.js` converts
the world impact into that mask's coordinates, including `_drawY`. Other
encounters delegate to the original owner. `mr27At` still checks live guns
and rocket boxes first, then the painted hull/core. Entry, invulnerability
and dead-body gates remain. No weapon stats, HP, attacks, authored pixels,
hit-flash timers or other-stage collision owners changed.

Both loader URLs use `?v=frost-core-1017` to retire stale browser scripts.

## Actual Chromium verification

`python _BUILD_SOURCE/probe_frost_core_1017.py --before` reproduced the issue.
`python _BUILD_SOURCE/probe_frost_core_1017.py` passes43 checks across Easy,
Normal, Hard and Furious, with zero page/console/asset errors.

Normal, all weapon modules destroyed, approximately1.67 seconds of real firing:

| Weapon | Core/hull HP lost before | HP lost after |
|---|---:|---:|
| Machine gun |0|126|
| Spread fire |0|201|
| Laser |75|81|
| Flamethrower |210|216|
| Ice orb |0|69.7|
| Fire orb |0|735|
| Chaingun |0|194|
| Locked missile |24|24|

Lasers and flame already had a broader fallback route; the repair restores
the missing physical collision used by bullets and orbs. No damage tuning
was added. The probe pins the encounter's position when measuring routing;
it calls the real input, projectile, encounter and drawing owners.

Additional checks verify the core while all weapons remain intact, each
weapon's separate routing, the actual changed hit-flash pixels and expiry,
the core following its draw position, bare air remaining clear, and a final
kill made only with level1 machine-gun rounds. Screenshots at the regular
field of view and a painted mask overlay were inspected.

`node --check assets/game.js` and the two changed runtime scripts pass.
The complete `node _BUILD_SOURCE/test_fl.js` finishes with8754 passes,
zero errors, final `FALVA/LIZZIE BUILD OK` and exit0. See
`docs/qa/frost_core_1017.json`; scratch captures are in `_shots/frost_core_1017`.
Existing `game.js`, modular roster, orbs and test harness retain their
starting SHA256 values. No commit or push.
