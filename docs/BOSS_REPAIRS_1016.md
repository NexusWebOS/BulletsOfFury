# Stage 4 shield completion and Stage 5 Hammer repairs — October 16

Mike reported fire rounds following the player, excessive Hammer HP, a hammer
that stayed dim while its core charged, and a Sovereign shield that disappeared
with two of four generators still alive and blocked completion.

## Result

- Stage 4 hostile rounds commit to their release vector. The generic fire-orb,
  ground-to-air and missile update paths cannot acquire or follow a player after
  release. Speeds and interception rules retain their encounter settings.
- The campaign Sovereign shield stays powered until all four generators die.
  Its old eighteen-second overload bypass no longer contradicts that objective.
  Other stages retain their existing donor behavior.
- The newer SA14 renderer once again draws all twelve authored energy-field
  frames and calls the reconstruction effect layer. They preload with Stage 4.
  Generator plates draw over overlapping helpers and receive hit priority at
  their visible positions. Helpers retain their independent attacks.
- Campaign Hammer hull HP is capped at 1,100 / 1,700 / 1,950 / 2,200 for Easy /
  Normal / Hard / Furious, after spawn/performance scaling. Armor and other
  existing pools receive the same factor; armor created later inherits the new
  hull budget. Co-op caps are 1.5 times these values. A smaller existing budget
  never increases. Finale donors and the separate password design retain their
  own budgets. Recovery, reserve and attack phases remain present.
- The live `storm_raise` and `storm_rebuild` charge states drive weapon light
  with chest light. The usage classifier had wrongly excluded the complete
  `arch_storm_charge_0926` body reel. Its companion now lights its own hammer
  glass and core pixels at the native reel's measured mounts. No alternate boss
  form, pasted glow disc or source-plate replacement was added.

## Artwork and reproduction

The original 1536 × 1024 charge source remains unchanged. Both new companions
use that same even canvas and source coordinates; runtime crops, pivots, jitter
and proportional scale remain registered to the existing reel.

`_BUILD_SOURCE/export_hammer_charge_glow_1016.py` runs a native recovery charge,
records the actual key-space rectangles and exports the exact `XART.get` source
to ignored scratch. It records the native reel's head and core anchors in
`_BUILD_SOURCE/glow_usage_1015.json`. Then run:

```text
python _BUILD_SOURCE/pixel_glow_1015.py --keys=arch_storm_charge_0926
```

The focused owning workflow preserves all other shipped companions and rewrites
its registry and metadata together. The classifier allows this body reel;
measured emitter regions preserve the large authored energy chambers that the
ordinary small-lamp filter would mistake for paint. Selected regions contain
only existing blue/cyan light and adjacent white lightning, with hard pixel
rings. The companion files add approximately 200 KB. No atlas was repacked.

## Verification

- `node --check` passes for `game.js` and all five changed companion modules.
- Required `node _BUILD_SOURCE/test_fl.js`: **8,714 passing, zero failures**,
  final `FALVA/LIZZIE BUILD OK, 0 ERRORS`, exit 0. Updated obsolete assertions
  for the prior timed shield bypass and HP multiplier; added lower-budget and
  co-op armor checks. Earlier failed runs are recorded in the QA JSON.
- `_BUILD_SOURCE/probe_boss_repairs_1016.py`: **53/53**, no page, console or
  missing-asset errors. Three projectile families keep their direction while
  the player crosses. Real hit routing kills all four generators, reconstructs
  them at the health gates, enters pursuit and defeats the Sovereign on Normal,
  Hard and Furious. The native renderer advances energy-field frames and draws
  reconstruction. Actual generator and charging-Hammer damage changes pixels,
  and flash timers expire. The held hammer's actual region brightens with its
  light driver enabled. All four Hammer HP budgets retain difficulty ordering.
- Existing `_BUILD_SOURCE/probe_stage4_pressure_1015.py`: **50/50**, no browser
  errors. Independent Warden/helper fire, committed targets, upright generator
  mounts, helper destruction, audio and visible hit feedback remain intact.

Inspected native captures: shield with two surviving generators, four rebuilt
generators, live hammer charge, and identical-frame weapon light off/on. Evidence
is under ignored `_shots/boss_repairs_1016/`; portable checks and runtime hashes
are in [boss_repairs_1016.json](qa/boss_repairs_1016.json). These are controlled
native fixtures, not a full human campaign balance playthrough.

Shipping cache keys: `boss-repairs-1016` and `hammer-charge-1016`. The separate
local Training Flight loader, notes and source stay outside this publication.
