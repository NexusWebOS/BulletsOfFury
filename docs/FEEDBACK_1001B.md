# October 1 (b): trailer feedback

Mike's notes from the trailer v9 redo, on the October 1 build. Runtime: `assets/feedback_1001b.js`, loaded after `campaign_world_0930.js` and before the widescreen HUD. Stage 9 launch and clock: `assets/game.js`. Art: the files listed below. Suite section: `_BUILD_SOURCE/test_feedback_1001b.cjs`.

## What changed

| Note | What was wrong (measured) | Now |
|---|---|---|
| Bomber squads flash white | The stage 6 squadron did take `e.flash`, but the flash was a 74% white flood blitted at 55–85% alpha. Paint and palettes read through it as a faint haze. The storm bombers peaked at 70%. | A solid silhouette in the hit colour (white, or the red/blue elemental crit). It fades with `e.flash`. The carried bomb keeps its authored colour. |
| Falva's box shows its top under the box | Her sheet had a 244 px box pitch but was sliced at 256. Idle and the emotions carried 12 rows of the next cell's top rail. Talk-small/medium/wide/o were cut 22 rows low; crash/sad/victory 11 rows low. The compact `comm_` set that the dialogue box actually draws had the same faults at half scale. | All 12 frames rebuilt as one box: portraits 256×244, comm 128×122. Shifted frames take idle's top rail. Rebuild with `_BUILD_SOURCE/fix_falva_portraits_1001b.py`; it always runs from the untouched backups in `_BUILD_SOURCE/_backups/`. The other eight pilots measured clean. |
| Portals stay on screen into stage 9 | `stage9PortalEscapeDraw` drew the gate at `1-p*0.72` alpha, so at p=1 it stayed at 28%. That was the grey dish through the countdown, on GO, and at the start of play. | The gate shrinks shut and is gone when the ship is clear. |
| No water pop-up on stage 9; scroll as fast as stage 5 | The launch drew `entryConnectorDraw(9)`, whose surface is the water flat. Play rode `mapScroll` (about 40 px/s, frozen for bosses). | The launch draws the stage 9 void itself. Stage 9 has its own clock (`_stage9SpaceScroll`) at `STAGE5_SPACE_CRUISE` (1000 px/s) from the run through GO and play, handed over at GO. Combat still reads `mapScroll`. |
| Stage 7 portal: no pausing or hesitating | 2.2 s standing self-destruct, then a 1.9 s deceleration onto a ground-fixed portal, then a 0.4 s hold, then the entry. | One run with no braking (see timeline below). The radio is pinned to the top so it never covers the rift. |
| Stage X: water plateau with a giant mountain (SpriteCook) | The duel borrowed stage 6's sky. | A SpriteCook plate (`assets/game/stagex_1001/stagex_arena.png`; source and prompt in `_BUILD_SOURCE/stagex_1001/`): a flooded tableland ringed by cliffs, with a snow-capped mountain in the centre. The camera flies in from the southern cliffs, then circles the peak. The plate drifts up and down, so the arena never runs out. |
| Stage 6 left/right moves 340 | The world is 680 wide against a 480 view, so the camera has only 200 px of travel. | The whole stage 6 backdrop (sky, city and clouds) slides 340 px over 2.6 s: right when you choose LEFT, left for RIGHT. It is tiled three across with mirrored outer copies, so no edge shows. Measured at 2.5–3.5 world px per frame through the turn, zero before it. |
| Stage 9: smaller, cleaner asteroids, plus watery ones (SpriteCook) | `spawnS9Meteor` blew the small crystal comet up 300–500%, about 225–375 px wide, three per shower. | Six SpriteCook plates in `assets/game/s9_asteroids_1001/`: three clean grey rocks and three wrapped in seawater. Bodies are 46–74 px. Showers keep their corridors, gravity and bounce. Watery rocks burst through the tidal-geyser death. |

## Stage 7 escape timeline

| Time | Beat |
|---|---|
| 0.0 s | The wreck goes critical; Decker calls the self-destruct. |
| 0.9 s | Full thrust. The sewer races underneath at 880 px/s and never slows. |
| 2.8 s | A rift tears open in the air ahead, mid-flight. The pilot: "WHAT IS THIS?! WHAT IS HAPPENING TO ME?!" |
| 3.2 s | The rift pulls the ship in, spinning and shrinking. |
| 4.5 s | Swallowed. The rift snaps shut through its closing frames. |
| 4.7 s | Flames roll up the screen and engulf it. |
| After | Decker, then Cole, over the fire; fade; stage clear. |

## Verification

- Every check ran in real Chromium through `_BUILD_SOURCE/scene1001.py`, a scripted-scene stepper with per-frame grabs. Frames were inspected for:
  - the stage 9 entry, before and after;
  - the stage 9 asteroid showers;
  - the Stage X duel;
  - the stage 6 turn, also measured by frame-to-frame shift;
  - the stage 7 escape;
  - bomber hits;
  - Falva in the in-play dialogue box.
- Probe trap, again: pinning `player.invuln` hides the ship on the damage-blink phase. Use `playerHit=function(){}` instead.
- `shoot.py` now honours `BOF_CHROME` (the preinstalled `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`) and its static server is quiet.
- These are rendering and flow checks, not balance certification.
