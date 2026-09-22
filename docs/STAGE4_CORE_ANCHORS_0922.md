# Level 4 electrical-core anchors — 2026-09-22

The four shield generators previously used camera-centered generator columns and
eased toward viewport-clamped positions each tick. Camera movement therefore
shifted them independently of the Storm Sovereign.

They now store their formation spacing once and derive positions directly from
the boss's world position. Scrolling, player movement and viewport bounds cannot
change that spacing. Synchronization runs at encounter creation, during shield
updates and after the boss director moves, including its early-return phases.
Rendering, electrical connections, missile targets and damage hitboxes all read
the same node positions. The independent chaingun helper attack patterns retain
their existing behavior.

Validation: syntax passed. `_BUILD_SOURCE/probe_stage4_core_anchor_0922.py`
verified four camera positions and background scrolling with a stationary boss,
exact X/Y movement with the boss, rearm, point/beam targeting and 240 director
updates with moving camera. Maximum relative-position error was floating-point
roundoff (5.7e-14). Real Chromium screenshots inspected; zero page/console errors.
Evidence: `_shots/stage4_core_anchor_0922/`.

Full suite completed: 4,905 passing checks, 75 existing failures, exit 1. Failure names match the preceding burn-effects baseline exactly. No new failures. Gameplay LF preserved. No commit or push.
