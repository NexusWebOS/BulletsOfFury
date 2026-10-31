# Yuri32 — upward fire, flat slides and reusable cover poses

The user requested the upward counterpart of front-facing downward fire,
walk/run entries into a flat ground slide, and object-free cover/back-to-cover,
partial pop-out and return poses. This pack adds215 directional exports from
112 selected source drawings, arranged into21 named animation banks.

- Front-facing straight-up idle and8 braced firing drawings. The rifle remains
  vertical, gaze follows upward, and runtime projectiles originate at its barrel.
- 19-frame walk-to-slide and23-frame run-to-slide per facing; a flat seated hold
  and11-frame grounded recovery. The running approach has contact, crossover,
  push-off and flight before lowering into a feet-first slide. Ground slides
  keep the existing0.65-second movement; the separate downhill chute is untouched.
- Standing back-to-cover,13-frame lowering into crouched cover,19-frame standing
  partial peek and17-frame crouched partial peek, with explicit return and entry
  banks. Controlled return motions reverse the authored lean. Bodies, weapons,
  boots and hair remain complete; no wall, crate or other environmental object
  is baked into the exported sprites. Left/right banks share the character unit.

The approved brown mohawk, close beard, red sleeves/shoulder badge and dark
tactical armor are supplied as identity references. Every new source is256x256
with padding, never stretched; exports retain the established192x224 cell and
96,160 anchor at a common half-scale. Ground contact roots keep soles registered;
running flight phases preserve their airborne foot height. Sockets are measured
from each authored barrel. Sources, selection indices and cleanup receipts are
retained. Generated arcs/flashes were cleaned with exact PixelLab pixel edits
or excluded; an illuminated recovery take was rejected.

Runtime js/yuri32.js adds the straight-up aim and firing override, remembers
walk/run state at slide entry and selects entry/hold/recovery. Back-contact cover
poses apply when the actual cover object is behind Yuri's torso; forward cover
keeps its existing over-object poses. Tall cover uses standing variants, low
cover uses the crouched versions. Return uses the same reversible peek state.
The cover library also provides separately named reusable entry/return clips.
Existing Escape29 movement, damage, bindings, Yuri31 roll/twist/floor fire,
enemies, scenery and base assets remain unchanged. The only existing runtime
file modified is the index loader/build stamp; behavior is scoped to the new
module. No new controls or balance changes.

Validation:20 native Chromium checks pass, all215 frames decode, no page/console
errors, binary alpha/even dimensions/unclipped bounds pass. Inspected source
contacts, onion views and actual up-fire, flat-slide, crouched/standing cover
captures. The ordinary-input corridor/door-slide route and cover checks pass4/4
and reach visible level4. The required game syntax and base suite finish with
exit0 / BUILD OK, 0 ERRORS.820 retained art hashes and the earlier gameplay/Yuri31
files match their prior hashes. M30 buttons are simulated, not a hardware test.

Build: overdrive1015-yuri32-r1. Review: art/yuri32/preview.html. Export owner:
_research/build_yuri32.py. QA: _research/probe_yuri32.py and existing corridor
route probe; reports/captures: docs/qa/overdrive_yuri32* and yuri32_views.
No commit or push was made.
