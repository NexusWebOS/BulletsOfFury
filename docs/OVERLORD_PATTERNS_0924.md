# Level 1 helicopter attacks — 2026-09-24

The opening downward machine-gun burst now leads into a banked horizontal sweep,
the warning-light ram, existing curved reentry, south-facing sonic attacks, a
staggered pod salvo, and a lane-selection rush. All difficulties receive the new
sequence. The authored hull, rotor, flashes, ordnance, warning art and audio remain
in use; no atlas or generated asset changes were needed.

| Setting | Normal | Hard | Furious |
| --- | --- | --- | --- |
| Sweep speed (world pixels/second) | 125 | 210 | 330 |
| Continuous sweep traversals | 1 | 1 | 3 |
| Twin-gun interval | 95 ms | 68 ms | 45 ms |
| Missiles per pod | 2 | 4 | 8 |
| Alternating missile interval | 170 ms | 130 ms | 95 ms |
| Vertical rush traversals | 4 | 4 | 12 (three sets of four) |
| Final committed lane warning | 500 ms | 420 ms | 340 ms |
| Full vertical traversal time | 850 ms | 640 ms | 480 ms |

The requested 3–5 ms final warning is interpreted as a visible 0.3–0.5 second
window (3–5 ms is less than one frame). It is followed by a 120 ms warning fade,
then a committed charge with no player retargeting. Hard/Furious show all four
candidate cones and cycle the active one before locking. The boss alternates
south/north passes, then rotates and descends from above into recovery.

Sweep banking reaches 25 degrees, and both bullets and muzzle flashes use live
rotated hardpoints. The missile warning shakes the hull and flashes both pods
with an overhead warning symbol, without a FOV cone. Rockets alternate pods one
at a time. Sonic pressure fronts remain south-facing even when travelling in a
three-shot spread; broad fronts and fan rounds are larger than their previous
counterparts.

The optional warning blink clock separates elapsed animation time from held
warning progress. Previously, a held final progress value could permanently
select an invisible blink frame. Optional alpha now fades both the cone and
its highlight; ordinary warning callers retain their defaults.

## Verification

- `node --check assets/game.js`: passed.
- `python _BUILD_SOURCE/probe_overlord_patterns_0924.py`: passed in real Chromium.
  Tests all three difficulty sequences, sweep counts/bank/anchors, missile counts
  and stagger timing, fan geometry, lane commitment despite moving the player,
  4/4/12 alternating rush legs, recovery, all four authored warning cones, and
  missile warning with zero cones. The full native Furious sequence reaches
  every new attack without forced handoffs.
- Native contact checks: rolling, somersaulting, and moving clear survive;
  remaining in the charge lane unprotected begins player death.
- Screenshots inspected: banked sweep, three-shot south fan, pod warning,
  staggered missiles, candidate lanes, committed lane and charge. No page or
  console errors. Evidence: `_shots/overlord_patterns_0924/report.json` and PNGs.
- Full suite reached its final summary: **4,884 passing checks, 82 failures,
  exit 1**. No added failure names versus the immediately preceding music-fix
  baseline (84 failures); two variable Stage 1 jet checks passed this time.
  Log: `_shots/test_fl_overlord_0924_final.log`.
- `git -c core.whitespace=cr-at-eol diff --check`: passed. Game file remains LF.

Mike authorized publishing these changes and the preceding music recovery to
GitHub main on September 24. The verification above covers the uploaded code.
