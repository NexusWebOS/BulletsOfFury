# Overdrive Warrior entrance and dossier — October 11, 2026

Mike rejected the 800 × 600 view as too distant and requested a closer 640 × 480
feel in fullscreen, a rolling entrance, tracking zoom, a generated rotating boss
card with armor/HP/targets/attacks, arcade fills and cues, and a return to combat.
Current changes are local and uncommitted.

## Live presentation

- Level 2 uses **640 × 480** from deployment through combat. Proportional fitting
  fills the available fullscreen height or width with the same aspect ratio.
- The Warrior rolls from y−154 to its actual y472 arena position over 4.2 seconds.
  The camera captures it closely, follows south, and pulls from 1.65× to 1.12×.
  Authored track dust and existing tank audio support the arrival.
- An authored 600 × 424 dossier slides across the unchanged viewport. The same
  BOF bitmap title, industrial palette, original pad prompts and approved arcade
  cue bank are used. Part HP counts and bars fill during its scan.
- The rotating showcase uses **16 authored raster yaw poses**, including actual
  side and rear representations, on fixed 512 × 512 transparent canvases. Every
  pose shares one proportional normalization scale and ground pivot (256,454).
- D-pad left/right rotates; up/down selects a part; A toggles inspection; B returns
  to overview. Pointer target rows and the model viewport work too. Inspection
  highlights the corresponding model area and explains that target.
- Start continues once the first scan/turn is complete and the prompt is ready.
  The card also exits automatically after its idle reading interval. It slides
  out over .65 seconds and the camera restores normal 1:1 combat zoom over 1.1s.
- Player movement/weapons and hostile damage are gated during the sequence;
  stage scoring time is suspended. Start pauses arrival/restoration. Existing
  Options can open while paused and return to the same entrance clock.
- Held inspection/fire controls must be released before firing after restoration.
  The supplied `BOF-O-BOSS1.mp3` begins when combat resumes. Startup voice,
  pilot selection, Insanity lock, original Options and other missions retain
  their owners. Live Warrior mounts, armor rules and modular destruction remain.

## Actual combat values shown

| Target | HP | Detail |
| --- | ---: | --- |
| Left turret | 85 | Twin guns and homing rack |
| Right turret | 85 | Twin guns and homing rack |
| Head / helmet | 120 | Breaking it removes hull protection |
| Body / hull | 220 | Armored drive chassis and ram |

**Total HP: 510.** The active helmet absorbs **82%** of hull damage. Native
verification applies 100 damage: the guarded hull loses 18 HP; after the head
breaks it loses the full 100. Card data comes from the encounter's actual maxima
and shared armor factor. Attacks: machine-gun broadsides, visor laser volleys,
homing missile salvos, and the concrete-smashing ram.

The card displays Mike's warning verbatim:

> Warning — “Stings like a butterfly, Tramples you like a giant ass tank that it is!”

## Generated art and owning workflow

Built-in image_gen used the actual in-game Warrior drawing as its identity
reference, exported through `B.draw` in Chromium. The approved Overdrive controls
plate supplied the UI style. Original returned images are preserved; a revised
turntable sheet repairs edge spacing. The build uses one affine scale for both
axes, shared padding, even output frames and fixed pivots.

- Card frame: `expansion/topdown/art/boss_intro_1011/od_warrior_card.png` (1200 × 848).
- Sixteen poses and review sheet: `art/boss_intro_1011/od_warrior_view_0..15.png`
  and `turntable_sheet.png` (2048 × 2048).
- Exact initial prompts: `art/boss_intro_1011/source/generation_prompts.json`.
- Targeted repair prompt: `art/boss_intro_1011/source/turntable_repair_prompt.json`.
- Reference, raw results, source SHA, crops, scale, exports and registration:
  `expansion/topdown/art/boss_intro_1011/`. No atlas repack.
- Owners: `_research/export_warrior_intro_1011.py`,
  `_research/build_boss_intro_1011.py`, `js/boss_intro_1011.js`.

```powershell
python expansion/topdown/_research/export_warrior_intro_1011.py
python expansion/topdown/_research/build_boss_intro_1011.py
```

The export command updates the reference from the current boss; raw generated
results remain preserved. The asset builder registers frames and metadata
simultaneously. Runtime and default launch helper use `overdrive1011-boss-intro`.
Refresh an existing browser tab to load this build.

## Verification

| Gate | Result |
| --- | --- |
| Required base syntax and full suite | 8,700 passing assertions, zero failures, final summary, exit 0 |
| New native intro/card/control probe | 42/42; no page/console/asset/decode/playback errors |
| Existing Warrior combat probe | 22/22; no browser errors |
| Original frontend/controller probe | 55/55; no browser/media errors |

**119 native checks pass.** Real keyboard arena entry; zoom/follow motion;
combat gating; pause/Options return; original panel geometry; all sixteen poses
actually drawn; four part labels/HP fills; exact warning; keyboard/controller/
pointer inspection; authored target callout; fullscreen; slide-out; smooth zoom
restoration; fire-release safety; supplied music and arcade cues; actual armor
behavior; and 1920 × 1080, 1612 × 878, 1469 × 796, 520 × 650 layouts pass.

Native screenshots were inspected for arrival, front/rear card, head inspection,
slide-out, normal close combat and paused original Options. Art is verified by
key through `ART.get` and the game's own context `drawImage` calls. The current
sizing probe delegates to this new sequence; the rejected 800 × 600 source
remains archived as `sizing_800x600_fixture_1011.py` with its historical QA record.

```powershell
python expansion/topdown/_research/probe_boss_intro_1011.py
python expansion/topdown/_research/probe_warrior_1011.py
python expansion/topdown/_research/probe_restored_frontend_1011.py
node --check assets/game.js
node _BUILD_SOURCE/test_fl.js
```

A 32-frame native animated card preview is saved as
`_shots/overdrive_intro_1011/warrior_card_preview.gif` (800 × 600, 3.2 seconds).
Reproduce with `_research/capture_intro_preview_1011.py`. This preview is visual;
the playable build carries the approved arcade audio.

Portable evidence: `docs/qa/overdrive_boss_intro_1011.json`. Full captures/logs:
ignored `_shots/overdrive_intro_1011/`. Fixtures protect the tank for visual and
control inspection; this does not establish campaign difficulty balance.
Controller polling uses synthetic reports. No commit or push in this pass.
