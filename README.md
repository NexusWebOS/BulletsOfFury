# Bullets of Fury — Codex Edition

This branch is a separate development build of **Bullets of Fury**. It preserves the main branch
while collecting the gameplay corrections, repaired boss presentation, and cinematic asset packs
prepared during the Codex production pass.

Branch: `codex/codex-edition`

## Run the game

The game is browser-based and should be served over HTTP rather than opened directly from disk.
From the repository root, run:

```powershell
python -m http.server 8000
```

Then open <http://127.0.0.1:8000/> in a modern desktop browser.

See [SETUP.md](SETUP.md) for project setup notes and [HOW_TO_PLAY.txt](HOW_TO_PLAY.txt) for controls
and gameplay instructions.

## Codex Edition gameplay changes

- Restores the original game sound routing and removes the replacement audio override.
- Restores the legacy sustained laser for every pilot except Maverick, who retains his distinct
  widening laser behavior.
- Corrects the reversed diagonal art used by upgraded spread fire.
- Uses the Stage 5 master background throughout its arrival transition.
- Replaces Level 5's former space loop with the supplied full-length blue/violet nebula scroll;
  satellite hardware, random planets, comets, and miscellaneous orbital scenery are disabled so
  only the authored asteroid field and interactive asteroid hazards remain over it.
- Removes the conflicting legacy Stage 6 cloud/background layers and synchronizes its weather to
  the authored master scroll.
- Replaces abnormal offscreen ship-boss fly-ins with readable, bounded arcade manoeuvres.
- Adds selected boss movement identities informed by the reviewed combat reference packages
  without loading those packages directly at runtime.
- Adds repaired Spawn Carrier graphics and matching spawn/muzzle effects.
- Installs the supplied official **BONUS STAGE** card with its embedded lettering intact.
- Types **STAGE X CLEAR** letter by letter over the live post-boss battlefield, starts the stage-clear
  music during that beat, and carries the same uninterrupted track through the fly-off into stats.
- Runs Stage 7 on the supplied Toxic Sewer master and gives its boss clear a bespoke eight-frame
  sewer-portal handoff: the portal forms, pulls the live pilot ship inside, closes, yields to the
  Stage 8 card, then opens over Stage 8 and releases the ship directly into combat. This route
  deliberately skips the ordinary outbound, runway, countdown, and `GO` transition.
- Reassigns Stage 5 to `lvl3-alt`, Stage 8 to the former Stage 5 Egyptian track, and the former
  Stage 8 theme to both the ending and menu credits.

## Cinematic and visual libraries

The build includes production-ready source assets for later cutscene composition:

- `assets/game/cinematic_backgrounds/` — full-size Fury HQ interiors.
- `assets/game/cinematic_campaign/` — Earth Division branding, exteriors, alliances, seated scenes,
  and pilot campaign images.
- `assets/game/cinematic_characters/` — full-size transparent character pose sets.
- `assets/game/cinematic_ships/` — top-down and pseudo-3D pilot-ship views.
- `assets/game/cinematic_level_approaches/` — empty cinematic approaches for each stage.
- `assets/game/cinematic_level_transitions_topdown/` — top-down transition environments.
- `assets/game/generated_cinematic/` — large 32-frame explosion families, color variants, sizes,
  previews, and cinematic backgrounds.

The explosion collection includes orange, blue, green, and purple variants at 128×128, 192×192,
256×256, 320×256, and 320×320 where provided. Individual frames and packed strips are both kept
for flexible runtime integration.

## Verification

This edition was checked with the project’s browser and gameplay probes:

- JavaScript syntax check passed.
- Browser smoke test completed with no JavaScript errors.
- Laser and upgraded spread-fire rendering probes passed.
- Stage 5 and Stage 6 background handoffs measured zero differing pixels at the join.
- Ship-boss manoeuvre simulation completed without the former repeated offscreen fly-ins.
- The Bonus Stage card was captured successfully from the live intro renderer.
- The complete Stage 7 results-to-Stage 8 portal handoff was captured deterministically; it reached
  live Stage 8 play without browser errors, a duplicate player ship, or a stale death overlay.

## Repository policy

`codex/codex-edition` is intentionally separate from `main`. Scratch captures, extracted review
packages, temporary generation inputs, and local QA workspaces are not part of the published build.
Runtime assets and their manifests remain in `assets/game/`.
