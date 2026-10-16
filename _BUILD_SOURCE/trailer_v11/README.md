# Trailer v11 — the Steam trailer on the gasline track, flown by the Furious bot

Mike, 1014: show all nine pilots and their abilities, the ten levels, a short fight with the final boss,
most bosses and minibosses, then end on **STOP! HAMMERTIME?!** — the Stage-5 boss dancing to the HAMA track,
STOP! with his hand out, a robot thrown at the pilot, a second robot thrown AT THE CAMERA that cracks the
screen, then the logo, COMING NOVEMBER 2026, the copyright and the Phoenix engine line.

Output (gitignored): `_shots/trailer_v11/BulletsOfFury_Trailer_v11.mp4` (1920x1080, 60 fps, 109.6 s,
-13.4 LUFS, -0.8 dBFS peak) and `BulletsOfFury_Trailer_v11_phone.mp4` (960x540, 30 fps).

## Pipeline

    python capture11.py          # films every take in plan11.py into takes11/ (real Chromium, real game)
    python whiteness9.py         # per-frame white-flash measure, so a cut never lands on a hit flash
    python render_audio.py       # renders each take's sound log through the game's own audio files
    python edit10.py             # builds edl11.json from cut11.py (+ ending11.py) over the beatmap
    python compose.py            # renders the picture from the EDL (segments/)
    python mix9.py               # mixes song, HAMA music2, take audio and SFX, then muxes

`brand9.py` pulls the logo, pilot bodies and portrait boxes out of the game's art; `crack11.py` draws the
four glass-crack stages. `brand/robot_tumble_0..7.png` are the eight 176x200 cells of
`assets/game/levels/stage_05/boss/hama_art_0928/helper_airborne_tumble/atlas.png`; `brand/fine_*.png` are the
fine-print lines set in `BOFCommandSignal.ttf` (the stage faces have no `@`). brand/ is committed for those.

## What changed from v10

- **The takes are flown by `_BUILD_SOURCE/bot/furybot.js`** (`fury11.py`), not by the v9 dodge autopilot.
  The game's real `playerHit` is restored and nothing is topped up — a death in a take is a real death. A
  take still chooses its encounter, pilot and starting weapon (the camera crew choosing the scene).
- `capture11.py` waits for PLAY before a mid-stage take's warm-up counts: stage starts now load their
  combat resources behind a LOADING bar, and a take that started counting at once filmed the bar.
- `T_hama` (plan11.py) films the HAMA breakdown with burst fire and the pickup pop-ups stubbed, so the
  ending is clean of white hit-flash and floating text.
- The ending (`ending11.py`, inlined in `cut11.py`) locates the STOP / HAMMER / TIME slams from the
  `hammerImpact` events in the take's own sound log, and the two tosses from the boss's own pose modes.
- The robot thrown at the camera is the robot's own tumble cycle as a `fly` layer in `compose.py`
  (geometric scale 0.55 → 9.0 over 0.62 s); compose also gained image-sequence layers (`seq`).
- `music2` lays the HAMA track (the one the fight plays) under the ending, matched to the song's level.

## Traps

- The claims list was named `CLAIMS` and overwrote the dict `claim()` uses — it is `CLAIM_CARDS`.
- `bossHitTest` writes `_s4CoreHit`, `_hammerModuleHit`, `_carrierBayHit`, `_lastPart`… — the bot saves and
  restores them around its planning (`FB.playSafe`) or a probe changes which part the next real shot hits.
- `CHROME` is playwright's default browser; the old Linux path is gone.
- Pilot screen time is uneven (3.9–9.9 s per pilot) and the X_rival_duel take has 0 frames (its map route
  is broken in this build); XREBEL covers the Stage-X fight.
