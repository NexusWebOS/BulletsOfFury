# Chaos Harrier MK II — sequential lasers and orbital pursuit

This correction supersedes the simultaneous crossfire from the earlier MK II pass.
The wing attack fires left then right. The Hard/Furious salvo fires left, center,
then right. Every individual emitter gets its own green/yellow/red warning and
release sound. There is only one active laser object, used by both rendering and
damage. The legacy `cross` state alias also runs the sequential salvo.

The ship pursues the player's position along an upper elliptical arc while idle,
acquiring a target and recovering between shots. Its speed is bounded and its
pursuit center eases toward the player. It settles during the second half of the
warning and the short laser release so the warned lane stays dodgeable. Wing
burns last 0.46 seconds, the center burn 0.62 seconds, followed by 0.24 seconds
of recovery before the next independently warned emitter.

The old `ch_sideflash` art contained two miniature barrels. It is removed from
this encounter's draw path. The inspected eight-frame `bpfx_muzzle_laser` reel
now supplies a bright single nozzle flash, held on its bright middle frames
during sustained fire. Transient shots also start on a visible flash frame.
Flashes resolve the live weapon hardpoint on every draw, including rotation and
the left mechanical housing's mirror. The center aperture and all four gun-frame
nozzle coordinates were corrected; muzzle, beam and collision origins share those
transforms. Only the active gun uses charge/recoil art. Beam widths are now 18
pixels for a wing cannon and 28 for the center; the beam-body crop excludes caps.

## Verification

- `node --check assets/game.js` passes.
- `_BUILD_SOURCE/probe_harrier_modular_0923.py` passes in real Chromium. Its salvo
  capture observes left/center/right in order, each with a separate warning,
  maximum one live beam, and more than 25 pixels of orbital movement.
- Actual `drawImage` matrices verify the flash origin, laser origin and transformed
  nozzle pixel agree within 0.001 backing-store pixels. Warning damage remains
  zero; release damage, safe lanes, all difficulties and death cleanup pass.
- No page or console errors. Screenshots inspected in
  `_shots/harrier_sequential_0923/`; `results.json` stores the measured results.
- Full suite log: `_shots/harrier_sequential_suite_0923.log`.
  Completed with 4,898 passes / 81 failures, exit 1. Failure names match the earlier
  81-name baseline. Compared with the prior MK II run, only the known intermittent
  Stage 1 sand-tank spawn assertion returned; no new failure names were introduced.

No new generation, commit or push was performed for this correction.
