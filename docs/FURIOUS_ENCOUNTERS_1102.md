# Furious storm encounters and comparison films — November 2

Mike requested all Stage1–9 miniboss/boss encounters on Normal, Hard and Furious,
the selected Stage6/7 Furious concepts made playable, four Stage2–5 replacement
concept boards, and a game-wide sound review. No commit or push was requested.

## Encounter ownership

`assets/furious_encounters_1102.js` owns Razorwake (Stage6 miniboss) and Thunderhead
(Stage6 left boss route), exclusively on Furious and outside StageX. The existing
`assets/sumpjaw_duo_1031.js` remains the Stage7 Furious miniboss owner. Its two
independent mechanical worms are retained. Rough Riders remains the separate
Stage6 right route on all three difficulties.

Razorwake has two independently destructible guns, wind-shear ports, a continuous
departure/rolling-pass/return and descending tornado turns. Thunderhead has four
gun modules, two pressure chambers, electric fronts, tornado gates and a final
hurricane reactor turn. All live pools sum to the displayed health budget. Core
damage stays protected until every weapon pool is exhausted. Defeat/progression
happens once through native owners. Part destruction cancels its target, rounds
and pending hazards. Source-alpha targets, real hit flashes and weapon-specific
contact decals remain active. Ordinary wind rounds reject offensive interception
from birth; native defensive clears and physical missile rules remain separate.

The roll uses complete authored depth views and pre-baked directional plates.
Solid charred gun variants preserve exact alpha. No CSS/canvas rotation of a
static sprite substitutes for directional frames. Warning coverage includes the
measured full wing span, with a committed 1.15-second rolling-pass warning.

The controller caches cropped authored cells in a bounded64MB LRU, released on
leaving Stage6. An isolated native RAF sample improved from48.8 to58.1fps.
Roll pixels compare exactly, and idle silhouette alpha is unchanged; fractional
nearest sampling changes some idle RGB pixels. Native hit-flash and expiry
checks pass. Final full-cabinet recordings measure41.2fps for Razorwake and59.2
for Thunderhead. The remaining Razorwake capture dip is retained as an explicit
review limitation; this is not a claim of60fps recording. Extra diagnostic takes
are kept outside the published57-film collection.

## Art sources and rebuilds

Production raw images and exact built-in Imagegen prompts are saved under
`_BUILD_SOURCE/furious_encounters_1102/`:

- `razorwake_source.png`: eight source-preserving roll/idle/depth views.
- `thunderhead_source.png`: storm hull and separate gun/chamber pieces.
- `storm_source.png`: tornado, hurricane and wind/lightning explosion art.
- `PROMPTS.md`: exact prompts, selected source identities and built-in tool mode.

Sources use the selected October31 Razorwake/Thunderhead boards and inspected
native Stage6 artwork as identity/style references. `setup_furious_sources_1102.py`
copies the selected source files. `build_furious_encounters_1102.py` owns the
38 fixed-cell banks, measured mounts/muzzles, palette flow, charred wrecks,
hit plates, source hashes and taxonomy entries. Output:
`assets/game/levels/stage_06/boss/furious_1102/`. Cells are even with shared pivots
and proportional scale. Native NW30 wind round/muzzle artwork is reused.

Four proposal boards, with separate exact prompts, are under
`_BUILD_SOURCE/furious_encounters_1102/concepts/`: Pyroclast Wardens (Stage2),
Cryocode Bastion (Stage3), Roadbreaker Aftershock (Stage4), Parallax Eclipse
(Stage5). These are proposals only; no Stage2–5 replacement is installed.

## Sound quality

`assets/audio_quality_1102.js` routes actual HTTP media through one shared
post-mix compressor. Native cue gains, sliders, filtering, retrigger gates and
voice limits retain ownership. File playback retains its native direct path.
Suspended contexts resume before routing; no silent media source is claimed.

`audit_audio_quality_1102.py` verified 603 registered cues, all 366 unique source
files decoding in Chromium, and all 366 producing audible post-mix playback.
The stacked combat stress test measured peak 0.779 and RMS 0.245 with zero routing
errors. Original retro/chip waveforms are preserved; no destructive remastering.
`audit_audio_routes_1102.py` exercised 136 live enemy cases, 108 pilot/weapon cases,
18 missile cases and 15 pickups, with no missing cue requests or silent firing
routes. Reports are in `_shots/furious_encounters_1102/audio/`.

The exact native pool slot is selected for each source, so variations are checked
independently rather than accidentally replaying the first variant. An additional
audible action check covers all nine pilot specials and all 41 unique native
music routes. Master mute reaches zero output and playback resumes after native
AudioContext suspension. `audit_audio_actions_1102.py` passes 5/5.

## Verification and films

`probe_furious_encounters_1102.py`: 29/29 native ownership/pool/socket/pixel/defeat
and difficulty/route checks. `probe_storm_contacts_1102.py`: 6/6 continuous flight,
real native storm deaths, native evasion, actual part contact and error checks.
`inspect_storm_art_1102.py` exports actual native roll pixels and measures warning
coverage. These isolated fixtures are separate from the full fight recordings.

`record_boss_comparison_1102.py` records all current Stage1–9 minibosses/bosses plus
the Rough Riders alternate route on all three difficulties: 57 films. It uses
native inputs, Cole's level5 loadout and labelled native invulnerability. After
fresh spawn it never writes enemy HP, attack clocks or phases. Stage6's unrelated
pre-boss team-choice scene is marked already completed in this isolated fixture;
boss-specific entrances, dialogue, transformations and defeat remain native.
The input pilot taps native Retina to reveal Nyx; it never changes her cloak flags.
Normal campaign still ends at Stage5; Normal6–9 are clearly labelled review-only
fights using Normal tuning. Each movie retains source hashes, timeline, accepted
cue counts, native frame rate, full audio/video decode and completion receipts.

`capture_mix_1102.py` taps the actual post-compressor output, preserving the mix
heard in game. `publish_boss_comparison_1102.py --install` refreshes only the new
local preview routes and preserves all other pages. Gallery:
`http://127.0.0.1:8805/current/boss-comparison-1102.html`.

Completed media is relocated to
`D:/BOF-Downloads/2026-10-31/current/boss-comparison-1102-media/` through
`archive_boss_media_1102.ps1`, with junctions preserving the original `_shots`
paths. This avoids duplicate repository copies and system-drive exhaustion.
The archiver validates both absolute roots and moves only passed recording jobs.

Syntax checks pass. The required full suite exits 1 before assertions/final
summary because the existing ignored
`UNUSED_ASSETS/retired_art_1022/manifest.json` is absent. This is not a green full
suite; see `_shots/furious_encounters_1102/full-suite.log`.

Final collection:57/57,19 per difficulty,122minutes total. Collection contracts
pass20/20; actual browser URL playback/three seeks pass57/57; desktop/mobile,
audio selection and transformation chapter controls pass11/11. Dracodia's real
rebirth, all four copied forms, protected full base pool and final defeat are
present on every difficulty. Actual movie pixels were inspected for these forms,
the new storm attacks and both Sumpjaw actors. Details: `BOSS_COMPARISON_1102.md`.
