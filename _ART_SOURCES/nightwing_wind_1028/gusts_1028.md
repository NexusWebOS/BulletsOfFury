# Nightwing — animated wind gusts, October 28

Mike rejected the circular wind rounds as mechanical rings/cogs. Replaced that projectile and its generic sonic muzzle family with directional animated air streams. The PixelLab source has open teal/ivory curls, a pointed leading tip and wispy tail; candidate 4 was selected from 16 options, then animated into 16 frames. No rings, metal casing or central disc in the new source.

## Assets and runtime

Owning source: `_ART_SOURCES/nightwing_wind_1028/build.py` and `gust_assets.py`. Raw generated frames, keyframe, job provenance and a 16-frame editable `wind-gust.aseprite` are retained. The existing `wind_bullet.aseprite` contains the new packed directional sheet as one editable atlas frame. Previous circular art files and older recordings are preserved but inactive.

One common proportional source scale per bank, nearest-neighbor normalization and offline directions only. Travel bank: 32 directions × 16 phases, 64px cells, fixed [32,32] pivot, leading tip at [32,40] before direction baking. Muzzle: 32 directions × 8 phases, same canvas/pivot, source tip at [32,58]. All 768 new cells have transparent outer borders. Cache-distinct `_gusts_1028.png` URLs and index version prevent the old disc from being reused.

Runtime selects/blits authored cells; no new runtime rotation, scaling, tint or decorative generation. Gusts follow actual projectile velocity at 24fps. The dedicated `nw30wind` muzzle family follows each real moving barrel and delegates all other native muzzle families. Existing collision-warning asterisks remain intentionally: yellow/red stars indicate a predicted player impact, not the projectile's art.

Corrected hull/guns/exhausts/charge/dash rings are byte-identical to the prior identity pass. Attack counts, timing, damage, HP, collision, defensive clears and non-interceptable Wind ordnance are unchanged. Other projectiles retain their renderer. No game.js/test_fl.js edits, commit or push.

PixelLab keyframe job `b5986218-1399-4445-be0c-cf08ba36f449`, candidate 4. Animation job `9c1789b8-64ba-4aa4-819d-195ecf675e54`, frames 1–16.

