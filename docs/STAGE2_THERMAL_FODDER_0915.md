# Stage 2 thermal fodder durability and shields — September 15, 2026

## Implemented roster rule

All twelve authored volcanic combat hulls now pass through `stage2ThermalHp`, which applies a 25% durability lift after the shared shots-to-kill calculation. Difficulty, campaign pressure and co-op scaling still enter once through `EHP`; the Stage-2 lift then makes this biome's lava and magma units deliberately tougher than other early-stage fodder.

Each of the twelve receives a weak, one-way breakable shield from the existing shared shield engine. The roster uses fire, hex and volt families to keep silhouettes readable. Shield capacity stays near 18–22% of hull health with the engine's four-point minimum, typically two base-gun hits. A break protects the hull from that hit, then triggers the existing shield-break popup, splash, 1.15-second lift/rotation stun and post-stun frenzy.

The Stage-2 heat barrel and other props remain unshielded. Bosses and minibosses remain outside this rule.

## Verification

- Focused VM section 304g: 6/6 checks pass across all twelve hulls, exact durability calculation, weak one-way capacities, three visual families, bare props and live break/stun handoff.
- Real Chromium through `_BUILD_SOURCE/shoot.py`: three representative hulls show the fire, hex and volt shells over the actual Stage-2 biome; no enemy bullets, boss bullets, page errors or console errors.
- Pixel review confirms all three authored hulls remain readable inside the shields and the bubble footprints fully surround their collision silhouettes.
- Full suite: 3,909 checks pass and the same 57 recorded assertions fail; exit code 1, with no new failure name.
- Proof frame: `_shots/stage2_thermal_fodder_0915/native/shot_0001.png`.

