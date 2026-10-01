# Cinematic director pass — September 30

Local implementation; not committed or pushed. Preserve the preceding September 30 repair pass.

## What plays in the campaign

| Trigger | Story and destination |
| --- | --- |
| Stage 1 clear | Recovered orbital recording establishes the hacked relay; volcanic source identified. Freezer receives his Ice Breath briefing; Maverick hears about the straight Laser Beam option. |
| Stage 2 clear | Restored comms reveal the frozen relay; fire versus ice damage and the next loadout are explained. |
| Stage 3 clear | Ice relay coordinates lead to the missile airbase. Freezer's Thermoshock conversation and the existing private Cole/Decker prototype scene are retained. |
| Stage 4 clear | Recovered electrical core decodes the alien orbital recording; Federation hull prepares the space sortie. Yuri has a Thunder Storm explanation. |
| Stage 5 robot reveal | Cronos offers to spare the pilot, identifies himself as an AI from another dimension, and reveals his intention to control Earth. The current battle stays on screen. |
| Stage 5 clear | Recovered space chaingun becomes Decker's bullet-system conversion. Each of the nine pilots has individual responses and fitting requirements. Cole retains his existing prototype exception. |
| Stage 6 route confirmation | Harrier pursuit explains the carrier threat and later Stage X contacts. Rebel pursuit explains the stolen weapons and HotWire/Phoenix's last warning. |
| Rebel Fury contact | Shared-unit history, Division betrayal, an offer to stand down, and the rebels' refusal precede combat. |
| Stage X contact | The actual selected surviving rival answers the pilot. Two-wingman pursuit follows the Harrier route. |
| Stage 6 clear | Branch-dependent consequences lead into the sewer investigation. No later pursuit is promised after the full squad is destroyed. |
| Stage 7 clear | HQ loses the pilot's signal and holds the last portal vector; the existing Stage 8 arrival owns the pilot's emergence. |
| Stage 8 clear | The recovered radio signal connects to the existing ending. |
| Bonus Stage 9 clear | Laser Mist recovery leads back to the campaign map, not an invented next stage or premature ending. |

The director does not grant weapons, spend currency, unlock levels, or change rewards. Existing engine progression remains authoritative. Stage-clear callbacks execute once, including when skipping.

## Controls and presentation

- **A / bound fire:** reveal the current line, then advance one talk beat on the next press. No mandatory reading delay.
- **Start:** skip the entire scene and execute its continuation once.
- Automatic playback remains available, with a reading hold after each line.
- Original campaign prologue also accepts A per talk beat and Start for the full prologue. Legacy HQ beat/ensemble modes accept Start and immediate A advancement.
- Stage 6 contact dialogue stays in the live stage. Combat waits while the sky continues scrolling. No scene teleport or player reposition.
- Cronos dialogue is campaign-only and never interrupts HAMMER or HAMA music choreography.
- Graphical dialogue font, authored button prompts, current pilot comm portraits and full-screen cockpit reverse shots are reused.
- Stage 7 dialogue does not pretend the pilot has already emerged in Stage 8.

## Art

Three new generated assets: Cronos transmission bust, Decker engineering/chaingun close-up, and modern Yuri HQ lightning close-up. References were the current hammer robot, current mohawk Yuri, Decker's established identity and Cole's cinematic rendering quality. No rear chaingun body is introduced.

Sources and generation prompts: `_ART_SOURCES/cinema_0930/PROVENANCE.md`.
Runtime PNGs and dimensions: `assets/game/cinema_0930/manifest.json`.
Rebuild: `python _BUILD_SOURCE/build_cinema_0930.py`.
Only cropping transparent margins and nearest-neighbor size reduction are performed by the packer. Original generations are preserved.

## Review and integration

Open `cinematic-review.html` through the same HTTP server as the game. Choose a pilot and any of the nine aftermaths, Cronos, either pursuit, the squad confrontation, or an individual Stage X rival. This is the live engine; the preview does not complete missions or write save slots. It is not a second cinematic implementation.

Implementation: `assets/cinematic_director_0930.js`, loaded after the September 30 encounter layer in `index.html`. Existing boss/debug hosts also iframe this same index. The original campaign story file remains available as the source of the orbital recording and private prototype scene.

## Verification

See `docs/qa/cinema_0930.json` for the final test counts and browser evidence. Reproducible checks:

```
node --check assets/game.js
node --check assets/cinematic_director_0930.js
node _BUILD_SOURCE/test_fl.js
python _BUILD_SOURCE/probe_cinema_0930.py
```

Browser checks use the real frame loop and keyboard events, decoded artwork, all nine pilot conversations, real stage-clear exits, Cronos's reveal, both password exclusions, Stage X release into combat, and the review UI. Screenshots were inspected. The Stage 6 scroll probe waits for the terrain to decode before comparing movement.

Limits: new close-ups are authored still shots, not new lip-sync reels or voice recordings. Pilot comm avatars retain their existing mouth animation. This pass verifies focused scene triggers and returns, not another complete nine-stage campaign playthrough or subjective pacing approval.
