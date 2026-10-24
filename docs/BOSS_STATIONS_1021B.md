# Boss Mode stations and starter bosses (1021b)

Mike: *"I would love to be able to drag my boss onto positions in the scene, select an action where I've
placed him such as orbit, fly in, fly out, fly and fire etc. Many of our actions with the terminology and
then our human language description for easy UI."*

## How to use it (SCENE tab)

1. **Drag the BOSS chip** (top bar, green dashed box) onto the field. Or pick the **STATION** tool (key `3`)
   and click. Or, with SELECT, grab the boss himself and drop him somewhere.
2. A picker opens beside him: **WHAT DOES HE DO HERE?** Every card has a name, a plain sentence, and the
   engine term underneath. Pick one.
3. He gets a numbered marker. Drop more spots; he visits them in order and the phase loops.
4. Drag a marker to move it. Double-click it (or **CHANGE WHAT HE DOES...**) to change the action. The dock
   shows its settings in plain words ("circle size", "how many laps", "shoots while circling").
5. **THE PLAN** (dock, nothing selected) and the code panel list the phase as sentences:
   `ORBIT at the centre - direction clockwise`.
6. **STARTER BOSS** loads one of three complete fights to edit: THE GATEKEEPER (find the gap), THE CHARGER
   (bait and dodge), THE TURRET KING (don't stand still). Each is an entrance phase, then phases at full HP,
   66% and 33%.

## The 17 actions

| MOVE | | ATTACK | |
|---|---|---|---|
| FLY IN | swoops in from off-screen and settles | FLY & FIRE | shoots the whole way to the next spot |
| FLY OUT | goes to the spot, then leaves the screen | STRAFE RUN | flies a straight line raking bullets |
| HOVER | floats and bobs for a while | CHARGE | warning lane, ram through it, back from the top |
| ORBIT | circles the spot | DIVE BOMB | warns, drops toward the player, pulls back up |
| SIDE SWEEP | glides wall to wall at this height | SPIN & SPRAY | spins in place spraying a spiral |
| ZIGZAG | snakes downward | WALL OF BULLETS | walls with a gap that moves |
| FIGURE EIGHT | loops a figure eight | SNIPE | quick aimed burst |
| PULL BACK | backs off to the top to regroup | NOVA BLAST | charges, then rings in every direction |
| BLINK | vanishes and reappears here | | |

## How it is built (nothing is a mock)

- A phase with stations carries `plan: [{id, beh, x, y, p}]`. The editor **builds** the phase's keys and
  zones from it (`buildPlan`); every built key and zone carries `st:<id>`, and a rebuild replaces exactly
  those. Hand-laid waypoints (no `st`) survive and run after the stations.
- The engine never reads `plan` or `st`. It runs the built keys and zones through the same scene director
  as before, so PREVIEW, ATTACH LIVE and APPLY + PLAY TEST all run exactly what the stations built.
- Telegraphs (CHARGE, DIVE BOMB) are attack zones that start **off**; the arrival key switches them on and
  the strike key switches them off (the existing `zone` action).
- A spin ends with a zero-time key back to rot 0, or the next move would unwind 360 degrees.

## Engine change: a looping phase hands over on HP

`sceneDirectorTick` used to let a looping track own the boss for ever, so a later track triggered by
`hp` or `phase` could never start. Now, at every key boundary, a later track whose hp or phase trigger has
**become** true takes over (`sceneHandsOver`). Triggers that were already true when the track started do not
cut it short, and `start`/`time` tracks never interrupt.

## Proof

- `_BUILD_SOURCE/probe_stations_1021b.py`: 19/0 in real Chromium, 0 page errors. It drags the chip
  (HTML5 drag and drop), picks ORBIT and CHARGE, drags a station, changes a setting, loads THE CHARGER,
  PLAY TESTs it, watches the engine walk Entrance -> Teach with the lane telegraph live, and sees the
  handoffs at 60% and 30% HP. `--bust` disables the handoff: the two handoff checks fail (17/2).
- `_BUILD_SOURCE/probe_scene_editor_0911a.py`: 16/0 (three expectations had gone stale since 0916:
  the tool count, the Magma Ward slot name, and the default phase name).
- Suite section 389 (`test_scene_handoff_1021b.cjs`).
