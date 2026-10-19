# Stage 6 Harrier size and allied wing — 18 October 2026

Mike's latest correction removes the energy core from the **main Harrier**.
The Fortress miniboss keeps its six-battery reactor encounter. This supersedes
the main-carrier core section and solo-wing behavior in the earlier Stage 6
repair notes.

The Harrier now has only its eight real damage pools: two fans, four laser
batteries and two missile racks. Destroying the last module immediately starts
the original falling-carrier sequence. There is no core sprite, reactor target,
opening gate or extra core HP. The same encounter launches the existing blue
Nightwing at 2.4 seconds; only defeating that fighter awards the stage clear.

The existing whole carrier plate is 1.45 times its previous width and height,
668.16 × 375.84 world pixels. The regular 480 × 512 playfield and camera zoom
remain unchanged. Uniform scaling covers the hull, fan and weapon mounts,
module hitboxes, Retina bounds, launch bay, warnings, beams, muzzle positions,
damage bursts and smoke. Its combat height and smaller lateral sway keep the
objectives reachable. The blue jet starts inside the enlarged bay at 48% of its
combat size and approaches the player's plane with one proportional depth
scale; its native launch point includes the falling offset exactly once.

Two old solo-fight overrides caused the disappearing allies:

- `stage6_sequence_1013.js` removed the approach wing, erased its rounds and
  skipped its AI, arsenal and drawing during the miniboss.
- `part2_combat_1010.js` emptied the wing every Harrier frame and after a quick
  encounter launch, also deleting its radio line.

Both overrides are removed. The same living allies continue targeting real
modules, firing and drawing through the Fortress, carrier breakup and blue-ace
fight. Scheduled 25-second departures wait until combat/warnings finish;
genuine damage retreats remain. Reinforcements are selected from the actual
five-pilot team before launch, avoiding random arrivals being discarded by a
later filter. The existing team limit and support-pressure rules remain.

Hit flashes still use `markHit` and the native part timers. Their clocks now
advance during departures, scaled returns and breakup as well as combat, so
an injured or destroyed module does not remain white through a flight phase.
The Fortress aperture, combat radio, real escort actors and their caps remain.
Stage X's legacy Harrier and the Rebel encounter retain their own controllers.

The delivered review is `docs/previews/stage6_repair_1018/index.html`, revision
`harrier-wing-1018`. It includes actual allied actors and isolated review saves.
The obsolete `scene=reactor` link redirects to the corrected Harrier scene.
The Fortress reactor remains a separate scene. Co-op and compact HUD were
checked in native Chromium.

Verification and source hashes are recorded in
`docs/qa/stage6_harrier_wing_1018.json`; native logs and inspected screenshots
are under `_shots/harrier_wing_1018/`. Checks cover module hits by guns,
Retina missiles and beams, real allied damage and pixels, launch geometry,
attached fan effects, flash expiry, route selection, the complete Rebel intro
and the previous Levels 4–6 regression fixtures. These are controlled native
encounter fixtures, not another full campaign or a human balance assessment.

The gun fixture now explicitly selects Machine Gun through the real loadout
action and clears temporary primary replacements. Its initial last-rack miss
was a retained Sonic Boom with 10.15 seconds left claiming the trigger, rather
than a failed module hit route. Flash-expiry fixtures now isolate a quiet hit
window from the newly restored allies' fresh impacts. No runtime hit-feedback
timers were suppressed to make those checks pass.

`assets/game.js` changes only the scheduled wing-departure guard relative to
this task's starting file, preserving LF. `_BUILD_SOURCE/test_fl.js` remains
byte-identical with CRLF. Existing unrelated local work is preserved. No new
art, atlas edits, uploads, commits or pushes were needed.
