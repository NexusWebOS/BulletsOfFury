# Furious live fight recorder

This is an isolated development driver, not a shipping gameplay mode.
It runs the actual `index.html` and native game loop in Microsoft Edge through
Playwright. Its single privileged combat change is player-damage immunity.
It does not force enemy damage, HP, phases, attacks, poses or victories.

The pilot reacts to observations delayed by 220ms, decides at roughly 10Hz,
steers with native movement, fires, releases fully charged Fusion shots,
uses Retina / Multi-Retina missiles and double-taps directions for evasions.
It intentionally is not perfect. Protected contacts are logged; footage is
not a survivability or balance benchmark.

Starting pilot: Cole. Starting primary and space gun levels: 3, with basic
level1 weapons and a visible-entry observation beat for the three small
arsenal elites. Speed: 2.
Auto-missile level: 1. Initial missile stock comes from native Furious rules.
Native pickups can change these during a fight. Enemy stats and difficulty
are unchanged. Fresh browser contexts isolate saves/unlocks and scores.

## Repeat the run

Requires Python, Playwright and installed Microsoft Edge. From this folder:

```powershell
python record.py --parallel 1
python record.py --only s05_boss_chromehammer,s06_boss_warhive,s06_rebel_fighters
python record.py --resume --parallel 1
python gallery.py
python serve_review.py
```

`jobs.json` is the explicit coverage list. One or two simultaneous recordings
are recommended; heavier concurrency can reduce the native rendering rate.
The recorder uses real elapsed time. Videos target 30fps; native game render
rate is reported honestly. No accelerated stepping or synthetic animation.

The game root is discovered when installed beneath `_BUILD_SOURCE/`.
`BOF_GAME_ROOT` and `BOF_CAPTURE_DIR` can override source/output locations.
Output is under `review/` by default. Reports identify native defeat versus
timeouts/errors. A time-limited recording is never labeled a completed fight.
Repeat captures preserve their prior video/report with a timestamp.

The captured cabinet is composed from visible live game canvases in their
current native layout, including both Siege Console HUD panels. Music and
effects come from the running game's audio nodes. Raw WebM files are retained;
`-seek.webm` copies only rebuild the container index, without re-encoding pixels
or changing time. The gallery uses ordinary HTML outside the game.

`native_regression.py` is a separate isolated fixture for the two Chronos
bugs uncovered during full-fight testing. Its fixture edits are not used by
the recording bot. No generation service or new paid art is used in this pass.
