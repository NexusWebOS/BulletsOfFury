# Enemy Movement Pattern Library — 2026-08-30

These drawings are design references supplied by the developer. They are not sprites and should not be loaded by the game at runtime.

## Stage 1 authoritative encounter map

`wave setup.png` defines the Stage 1 encounter order and terrain placement. Read it from the bottom upward, matching the level's upward camera travel.

### Developer-defined legend

- Red circles in the water are boats.
- The single black circle accidentally placed among the red water circles is also a boat.
- Two additional boats enter on the left side of the water section.
- Yellow circles are fast attack jets.
- Yellow lines show the jets' movement from the top of the screen toward the player.
- Yellow jets enter one at a time in a rapid ripple. The requested 2–3 ms separation is represented by a visible 2–3 rendered-frame stagger (approximately 33–50 ms at 60 FPS), because 2–3 ms occurs inside one rendered frame.
- Black circles on land are tanks.
- Tanks face vertically south, move only forward or backward, fire from fixed lanes, and show recoil/kickback when firing. They do not sway, bob, or strafe sideways.
- Red boundary lines are terrain that tanks may not cross.
- Purple circles are kamikaze jets that enter from the top and commit to a collision run at the player.
- Purple lines show their movement paths.
- The large blue circle at the dam is the Stage 1 boss arena.
- The small blue marker is intentionally not assigned a gameplay meaning yet. The developer and Codex will review the miniboss separately.

### Wave-order rule

Fast jet ripples rotate through four lane orders. A small per-run seed chooses the first order, then the sequence cycles through all four, preventing a single memorized opening while keeping every pattern fair and testable.

The Stage 1 miniboss begins only after the second fast-jet ripple has cleared its scheduling gate. This document does not alter the miniboss's combat behavior.

## Stored future movement references

The following drawings are preserved for later enemies. Their circles are enemy bodies and their lines are paths, but their enemy assignments are deliberately deferred until the developer reviews them:

- `flight2.png`
- `flight3.png`
- `flight4.png`
- `flightpattern.png`
- `overnunder.png`
- `pat1.png`
- `pat2.png`
- `sidebyside.png`
- `sidebyside2.png`

