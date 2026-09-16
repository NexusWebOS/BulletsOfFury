# Stage 6 Doomsday Carrier storm-node fan warning — September 16, 2026

The Doomsday Carrier Mk II no longer releases its alternating storm-node fans without warning. Shield-down phases now commit the active node pair and all of its aimed paths before a 0.62-second shared green/yellow/red warning. Player movement after the warning begins cannot redirect the promised lanes or change which pair owns the volley.

The original pressure remains intact. The early shield-down phase retains two matching nodes with three lanes each at offsets `-0.16`, `0`, `0.16`, base speed `3.15` and a 1.55-second total cadence. The later shield-down phase retains five lanes per node at offsets `-0.34`, `-0.17`, `0`, `0.17`, `0.34` and a 1.12-second cadence. Warning origins follow the live authored node positions, while destroying a warned node disarms only that node's lanes. The short or charged central prism lance still begins on the warned release beat. Carrier phase changes now explicitly clear either pending fan warning, preventing an old pattern from resuming in a new phase.

Focused section 349 passes **11/11**. The full suite reaches its final summary with **4,432 passing assertions / 57 failures**: the established 56-name baseline plus the known intermittent Stage-1 sand-tank fixture, with no new failure name. Real Chromium passes **16/16** with zero page, console or game-loop errors. Four native 960×1024 frames were inspected from green through release; the fields remain behind the Carrier and storm nodes, the matching alert clears the boss gauge, and warning art is gone before the cyclone tracers appear.

Machine-readable proof: [qa/stage6_carrier_node_fan_warning_0916.json](qa/stage6_carrier_node_fan_warning_0916.json).
