# Bullets of Fury — Active Development Build

This is the current **Bullets of Fury** production build. The active work combines gameplay
corrections, boss and miniboss redesigns, campaign systems, interface upgrades, authored asset
integration, and real-browser verification.

Release source branch: `codex/build-2026-10-26`

## Windows launcher and complete game — Rev F

[Download the current Windows release](https://github.com/NexusWebOS/BulletsOfFury/releases/tag/bof-windows-2026-11-06-revf).
Published November8,2026. Download **BOF-Install-Helper-RevF.zip**, extract it and
run **Install-BulletsOfFury.cmd**. The helper retrieves/verifies the two large
parts and opens the complete graphical installer. The native game starts in
fullscreen; the animated Fury HQ launcher and all art/audio/runtime dependencies
are included. No Python or separate browser is required for this Windows build.

Includes restored Stage5 sky/starfield and smaller ship pieces, performance and
sound fixes, improved tutorial deployment, locked Cole and updated launcher UI,
plus the current modular Furious encounters. [Contents and verification limits](docs/GITHUB_WINDOWS_PUBLICATION_1108.md).

## November 4 build

- [Download the latest playable build](https://github.com/NexusWebOS/BulletsOfFury/releases/tag/bof-build-2026-11-04)
- [Build contents and verification limits](docs/GITHUB_PUBLICATION_1104.md)
- [New weapons, effects and rotating pickup previews](docs/previews/build_1104/index.html)

Adds Spread Lasers and Plasma Cannons I–V, generated hex icons, ColeForge effects,
rotating Stage X pickups, layered scenery, pilot quality/flight improvements,
Chronos dialogue and the recent campaign/wave follow-ups. Extract all three
November 4 runtime ZIPs together. Older review films below retain their original
capture dates. This is a development prerelease with the documented existing
full-suite setup blocker.

## November2 build and review library

- [Current review hub](https://nexuswebos.github.io/BulletsOfFury/)
- [57 boss/miniboss films: Normal, Hard and Furious](https://nexuswebos.github.io/BulletsOfFury/current/boss-comparison-1102.html)
- [All regular waves:313 chapters](https://nexuswebos.github.io/BulletsOfFury/current/all-waves-1101.html)
- [Updated enemy field guide:154 individual clips](https://nexuswebos.github.io/BulletsOfFury/enemy-showcase-1031.html)
- [Playable build, videos and SHA256 checksums](https://github.com/NexusWebOS/BulletsOfFury/releases/tag/bof-complete-update-2026-11-02)
- [Publication contents and verification](docs/GITHUB_PUBLICATION_1102.md)

Download and extract all three runtime ZIPs into the same folder, then run
`START-BOF.cmd` with Python3 installed. The review films label invulnerable input
assistance; Normal Stage6–9 entries are isolated reviews. The Normal campaign
still ends at Stage5. Four Stage2–5 Furious miniboss concepts remain proposals.

## October31 review archive

- [Current boss review and Normal ending](https://nexuswebos.github.io/BulletsOfFury/boss-balance-normal-finale-1031.html)
- [Enemy field guide](https://nexuswebos.github.io/BulletsOfFury/enemy-showcase-1031.html)
- [New concept boards / pending approval](https://nexuswebos.github.io/BulletsOfFury/furious-next-wave-1031.html)
- [Full field manual](https://nexuswebos.github.io/BulletsOfFury/field-manual/guide.html) and [Rough Riders guide](https://nexuswebos.github.io/BulletsOfFury/rough-riders-guide/index.html)
- [Publication contents and verification](docs/GITHUB_PUBLICATION_1031.md)

## Run the game

The game is browser-based and should be served over HTTP rather than opened directly from disk.
From the repository root, run:

```powershell
python -m http.server 8000
```

Then open <http://127.0.0.1:8000/> in a modern desktop browser.

See [SETUP.md](SETUP.md) for project setup notes and [HOW_TO_PLAY.txt](HOW_TO_PLAY.txt) for controls
and gameplay instructions.

## Production roadmap

The tracked request ledger currently contains **151 deliverables: 128 complete, 7 partial, and
16 pending**. Twenty-three items remain unfinished.

- [Production roadmap](ROADMAP.md) — readable overview, current work, and every unfinished item.
- [Full request checklist](docs/REQUEST_CHECKLIST_0914.md) — all 151 requests with completion
  state and evidence links.
- [Easiest-to-hardest work order](docs/WORK_ORDER_0914.md) — the active 23-item execution queue.
- [Original request ledger](docs/OVERNIGHT_REQUESTS_0914.md) — detailed creative specifications.

The checklist JSON is the canonical editable tracker. Its renderer validates stable IDs, evidence
files, dependencies, and queue ordering before regenerating the human-readable documents.

## Selected gameplay changes

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

Verified production work is published on `main`. Scratch captures, extracted review packages,
temporary generation inputs, and local QA workspaces are not part of the published build. Runtime
assets and their manifests remain in `assets/game/`.
