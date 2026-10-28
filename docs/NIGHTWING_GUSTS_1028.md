# Nightwing — animated wind gusts, October 28

Mike rejected the circular wind rounds as mechanical rings/cogs. Replaced that projectile and its generic sonic muzzle family with directional animated air streams. The PixelLab source has open teal/ivory curls, a pointed leading tip and wispy tail; candidate 4 was selected from 16 options, then animated into 16 frames. No rings, metal casing or central disc in the new source.

## Assets and runtime

Owning source: `_ART_SOURCES/nightwing_wind_1028/build.py` and `gust_assets.py`. Raw generated frames, keyframe, job provenance and a 16-frame editable `wind-gust.aseprite` are retained. The existing `wind_bullet.aseprite` contains the new packed directional sheet as one editable atlas frame. Previous circular art files and older recordings are preserved but inactive.

One common proportional source scale per bank, nearest-neighbor normalization and offline directions only. Travel bank: 32 directions × 16 phases, 64px cells, fixed [32,32] pivot, leading tip at [32,40] before direction baking. Muzzle: 32 directions × 8 phases, same canvas/pivot, source tip at [32,58]. All 768 new cells have transparent outer borders. Cache-distinct `_gusts_1028.png` URLs and index version prevent the old disc from being reused.

Runtime selects/blits authored cells; no new runtime rotation, scaling, tint or decorative generation. Gusts follow actual projectile velocity at 24fps. The dedicated `nw30wind` muzzle family follows each real moving barrel and delegates all other native muzzle families. Existing collision-warning asterisks remain intentionally: yellow/red stars indicate a predicted player impact, not the projectile's art.

Corrected hull/guns/exhausts/charge/dash rings are byte-identical to the prior identity pass. Attack counts, timing, damage, HP, collision, defensive clears and non-interceptable Wind ordnance are unchanged. Other projectiles retain their renderer. No game.js/test_fl.js edits, commit or push.

PixelLab keyframe job `b5986218-1399-4445-be0c-cf08ba36f449`, candidate 4. Animation job `9c1789b8-64ba-4aa4-819d-195ecf675e54`, frames 1–16.

## Verification

- 17 new art/native-render checks pass: dimensions, borders, distinct phases, provenance, unchanged aircraft/effects, both real emitters, six-round first fan, five native dual volleys, Wind classification/no interception, moving muzzle anchors, real source-cell draws for all 32 directions, animation phases, native recovery/lifetime and other-projectile delegation. No game/draw/HTTP errors.
- 20 existing native Nightwing regression checks pass, including true white damage flash/expiry, one target/HP pool, recoil guns, exhaust sizes, warning/charge and bullet rules.
- Fresh 135.64s live Furious fight reaches native defeat; 57.86 nativefps average. GOD/input bot, ordinary allies, carrier skipped via native ace spawn in setup. First 35s withhold player fire. No enemy HP/phase/timer writes. Four wind charge/release sequences appear. 10 film checks pass; no game, console, HTTP or bot errors. Audio mean -18.6dB, peak -2.2dB. Actual decoded frames inspected.
- 14 playback checks pass: both 1280×800 videos decode audio/moving frames, support range206 and three seeks, no review errors. Initial review favicon404 corrected.
- All 32 PNG banks / 3144 cells plus registry rebuild byte-identically. Syntax passes. Full suite finishes with the same five baseline failures, exit1: single-hit flash duration; opening-jump dialogue warning; jump return before Chromium; opposite StageX route persistence; StageX right full encounter.

Review: http://127.0.0.1:64935/. Local evidence: `C:/Users/Mike/Documents/New project/BOF-Nightwing-Gusts-1028/`. Portable native probe: `_BUILD_SOURCE/probe_nightwing_gusts_1028.py`; recording helper: `_BUILD_SOURCE/record_nightwing_gusts_1028.py`. Aggregate checks: `docs/qa/nightwing_gusts_1028.json`.


## October28 — Remove bullet markers / teal Wind gunfire
Mike removed Nightwing projectile collision asterisks. pw5Impact now excludes only NW30-owned rounds. Normal turret bullets use the existing authored directional teal Wind-gust animation at32px; heavy gusts retain64px rendering. All NW30 rounds classify as Wind and remain unshootable. Prelaunch tells and unrelated projectile alerts remain with their original owners.18 native checks pass; actual marker-free teal bullet pixels inspected. Syntax passes; full suite exits1 before summary because UNUSED_ASSETS/retired_art_1022/manifest.json is missing locally. Previously downloaded review movies are historical and unchanged.
