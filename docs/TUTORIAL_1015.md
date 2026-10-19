# The Training Flight (1015)

Mike: *"Design an in-game tutorial level for Bullets of Fury by asking players if they would like a
tutorial before entering the game. This is strongly recommended as Bullets of Fury is not your average
shmup by any means and combines many genre's and styles alike."*

Runtime: `assets/tutorial_1015.js`, loaded last in `index.html`. It wraps `startRun`, `drawScene`,
`drawIntro`, `updatePlay`, `playerHit`, `useBomb`, `applyPowerup`, `playPauseChoose` and `setState`;
`game.js` is not edited. Probe: `_BUILD_SOURCE/probe_tutorial_1015.py` (frames in `_shots/tutorial_1015/`).

## The question

A new game that would open on Stage 1 — Campaign, Arcade or Co-op, straight off pilot select or the co-op
roster — stops on **GS.TUTASK** before anything starts. An HQ dispatcher explains why, in the in-play
dialogue panel with their dispatch portrait:

> BULLETS OF FURY IS NOT YOUR AVERAGE SHMUP. IT MIXES ARCADE SHOOTING WITH DODGE ROLLS, LOCK-ON MISSILES,
> PILOT SPECIALS, ELEMENTS AND THE FORGE. FLY THE TRAINING ROUTE FIRST - WE STRONGLY RECOMMEND IT.

- **YES - TAKE THE TRAINING FLIGHT** is the default, under *STRONGLY RECOMMENDED FOR FIRST-TIME PILOTS*.
- **NO** starts the game exactly as before (*STRAIGHT TO STAGE 1*, or *START THE CAMPAIGN*).
- **BACK** returns to pilot select / the co-op roster.
- A pilot who has finished the flight is still asked, but the default becomes NO (`bof_tutorial_v1`).
- Never asked: password starts, loads and continues, debug jumps, any later stage.

The dispatcher follows the Stage-5 rule: a Fury pilot at HQ, never one who is in the air (Cole for
Decker, Decker for Cole, Falva for Lizzie, Lizzie for Falva, Cole or Decker otherwise).

## The flight

A TRAINING FLIGHT card (*FURY HQ PROVING GROUND — NOTHING OUT HERE CAN KILL YOU*) replaces STAGE 1, then
the ordinary launch, then 13 lessons over the real Stage-1 field with the real ship, weapons and HUD.
The stage's own content is held off: its wave plan is emptied, its clock is pinned at 0 (no crates,
miniboss, boss or life-up roll), the combat-pressure ambush clock is parked, stage chatter is skipped,
and any unit or round some other system spawns is removed before it is drawn. A hit is shown and
counted (*HIT - IN A REAL FIGHT THAT COSTS A SHIELD OR A LIFE*), never charged. Key names come from the
live binds, keyboard and pad (`J / PAD A`), so a rebound control reads correctly.

| # | Lesson | What it teaches | Done when |
|---|--------|-----------------|-----------|
| 1 | move | 8-way flight | all four pilot-tinted Retina beacons touched |
| 2 | fire | hold fire, the gun never runs dry | four training drones down |
| 3 | crate | supply crates, weapon levels I–V, dying drops to the base gun | the crate's weapon collected |
| 4 | roll | double-tap left/right, full i-frames, 5 s recharge, the ROLL bar | one barrel roll |
| 5 | somer | double-tap up, loop with i-frames, 7 s recharge | one somersault |
| 6 | missile | manual missiles, limited stock, missile crates | one missile fired |
| 7 | retina | lock with Retina, missiles fly to the lock, multi-lock scan | a missile launched on a lock |
| 8 | warn | the shared green / yellow / red lane warning | two clean dodges (moves on after five) |
| 9 | strike | ground-strike reticles track in green, commit, strike in red | three survived (moves on after six) |
| 10 | special | the pilot's own special (name from the pilot card) in the red crate; Juggernaut's charge | the special collected |
| 11 | brief1 | elements, the Forge, 2× opposing element, ½ own element | FIRE to continue |
| 12 | brief2 | enemy shields and the stun, kill chains, score → Fury Points | FIRE to continue |
| 13 | exam | a wave that shoots back, plus strikes | the wave cleared |

Each lesson clears the previous one's targets, rounds and reticles. Targets are real stage-1 units held
on a tether below the instruction panel. Text types on the game clock (64 characters a second), not on
the panel's wall-clock typewriter, so a slow frame cannot leave an instruction half-written.

**Leaving.** Finishing hands back to the same `startRun(1)` the pilot screen was about to make, with
the run's mode and co-op seat restored. Campaign still opens on its prologue and Arcade on Stage 1.
During the flight the pause menu's RESTART LEVEL row reads **SKIP TUTORIAL** and does the same.
RETURN TO MAIN MENU / QUIT drop the flight whole.

## Verification

`probe_tutorial_1015.py`: 42 checks, real Chromium, key presses only (an input driver reads the screen
the way a player would). It covers the question, YES / NO / BACK defaults, the whole flight for Cole,
Juggernaut and Lizzie (every lesson completed, 0 foreign units on the field, no life lost), NO in arcade
and campaign, SKIP TUTORIAL from pause into the campaign prologue, co-op flying solo and getting both
seats back, and the bypass cases. 0 page or console errors on every arm.

## Traps

- The shared `dlgBox` typewriter runs on `performance.now()`; under a stepped clock (or a hitch) the
  panel stays half-typed. Pass `shown` from a game-clock counter.
- Training targets placed near the top sit behind the instruction panel; the lane warning then looks
  like it comes out of the panel. `tutTop()` keeps them below it.
- Writing a regex or `\n` into JS through a Bash heredoc mangles the escapes (CLAUDE.md, 0912t); use the
  editor or `String.fromCharCode`.
