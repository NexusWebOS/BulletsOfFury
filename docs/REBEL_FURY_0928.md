# REBEL FURY 0928 — the Stage 6 right-route boss as a squad fight

Mike: *"ensure the fury fight is great for stage 6"* (same message as the Normal/Hard/Furious
encounter upgrades and the targeted-ball FOV rule).

Code: `assets/rebel_fury_0928.js` (loaded after `furious_review_0927.js`), one hook in `game.js`
(`rf28PaceMul` on the squad's cooldown). Suite section 375 (`test_rebel_fury_0928.cjs`, 36 assertions).
Probe: `_BUILD_SOURCE/probe_rebel_fury_0928.py --diff normal|hard|furious [--intro] [--shots N]`.

## What it was (measured before the change)

`probe_rebel_fury_0928.py`, four allies (the real right route), level-1 gun, parked pilot:

* Normal: 90 s after the 29 s radio intro; Furious: 212 s.
* Five ships hovered in a line and took single turns from one shared list (fan / lightning / dash /
  charged cast) whichever rebel it was; 0–6 enemy rounds on screen; nothing changed as the squad
  died; Furious differed only in HP and cooldown.
* `fr27RebelDrawShip` (the sliced ship draw) had dropped the hit flash — rebels never flashed.

## What it is now

**Signatures, from each rebel's roster role** (`roaming_rebels_0922/roster.json`): every 3rd turn on
Normal, every 2nd on Hard/Furious, every turn in a Hard+ last stand.

| rebel | role | move | tell |
|---|---|---|---|
| Voss | leader | IRON TALONS — 3/4/5 committed targeted balls around the pilot; Hard+ burst on landing (escape gap toward the pilot) | tb28 lanes + reticles |
| Nyx | infiltrator | GHOSTKNIFE — cloaks, commits a lane through the pilot, dashes through it (Hard+ wake knives), re-enters from above | committed lane |
| Rook | enforcer | BREACH HAMMER — column slam + ring of rounds; Hard+ second slam on the pilot's new column | column lane; the ring is an explosion (no lane) |
| Kaia | signal hacker | SIGNAL CAGE — fixed lightning strikes ringing the pilot, centre spike, exit gap; Furious outer ring | reticles only |
| Jace | interceptor | RAZOR RUN — pulls to the edge, strafes the pilot's row (committed), drops a stick of rounds | row lane |

**Formations** (the squad holds its turns while forming): WALL OF FURY (columns; 1/2/3 sweeps, each
walking a third of the spacing), PINCER (the two outer ships stream across the pilot's row, kept above
the radar/LOCK box), FIVE-POINT LOCK (Hard+, converging targeted balls, arc centred on the screen),
REBEL FURY spiral (Furious, opens below 45% squad health).

**Losses**: a survivor answers on the compact HUD-bay comm, survivors' next turn is their signature,
the squad hurries (cooldown ×0.93/0.89/0.85 per fallen), the last rebel makes a stand (Hard+ with a
20%/25% shield; Furious it inherits the fallen's signatures). Death adds the jet smoke ring.

**Shields**: Hard — Voss; Furious — all five (22% of the hull), a broken shield returns once at 60%
when a formation forms. Tinted `nes_bubble` shell per rebel + a shield row under the HP bar.

**Intro** (29 s, lines unchanged): the squad arrives in a V, weaves while it talks, the speaker rolls,
and each ship rolls out of the V to its slot.

## Measured after

Same bot and loadout: Normal 109 s (was 90), Hard 146 s, Furious 193 s (was 212), 0 errors on every
run. Full suite 5,674 ok / 0 errors. The hulls give back 10% because the squad now evades, dashes off screen and carries
shields; the first Furious cut (shields rebuilt at every formation) held the fight to one kill in
240 s and was the reason regen is now once per rebel.

## Traps found on the way

* **The 0927 radio panel sits in the play area.** Fine for the intro; mid-fight it covered the Wall of
  Fury's lanes. Squad lines now use the compact comm in the reserved HUD bay (the engine's original
  squad-radio treatment).
* **A held hit tint under four allies' fire is a white silhouette.** The restored flash is a 10 Hz,
  55% strobe.
* **A drop accumulator that banks distance off screen fires two rounds on one frame** at the entry
  edge (Razor Run, 21 px apart). Capped while off screen.
* **An alternating wall shift repeats the first sweep.** Measured 11 distinct columns for 3 sweeps;
  a progressive third-spacing walk gives 14.
* **A shield break stuns the ship, and a stunned ship holds the formation clock** — a test that breaks
  a shield and expects the next formation must clear the stun.

## Mike's calls

* The squad's radio lines are mine (`RF28_LINES`, one table) — rewrite freely.
* Fight length: +20% on Normal with the same bot before the 10% hull trim.
* Stage X duels keep the signatures and skip formations, radio and the last stand.
