# Classic study — 2026-11-05

Public source sections were downloaded for private analysis. Overview boards sampled every four seconds across four 8-minute intervals; denser 12-images/second sequences were inspected for attacks, reactions, destruction and lifting/throwing. Comix Zone playback was also observed in the browser. This is a sequence study, **not a claim to have watched every frame of full longplays**. Labels are approximate because section downloads retain keyframe padding. No reference-game sprites or footage belong in shipped Elementalist assets.

| Game/version | Gameplay | Study / directly visible findings |
|---|---|---|
| Streets of Rage 2, NTSC Genesis | [LongplayArchive](https://www.youtube.com/watch?v=mGByha3KYI0) | Approx 02:00–10:00; detail 03:08–03:12 combo, 08:38–08:42 barrels. Max's short blows cause immediate bent/backward pain; stronger contact launches victims. Other enemies wait at depth offsets. Street → bar → rain alley → bridge changes composition. Skate strikes wooden barrels; separated staves/rings appear and pickups are revealed. This interval is mainly **Max then Skate**, not Axel. |
| Comix Zone, NTSC Genesis | [LongplayArchive / RetroGameSpacko](https://www.youtube.com/watch?v=wVT1hwu26fo) | Approx 01:00–09:00; detail 01:45–01:49. Sketch alternates compact guard/load and full extended blows; finisher sends mutant away. Sweep marks/contact lettering emphasize impact. Duck, aerial, landing and floor poses differ. Water/reflections and machinery animate within panels. Primarily a **single combat plane**, so its movement system is not a belt-scroller template. |
| Final Fight, arcade | [RedSevenNine](https://www.youtube.com/watch?v=c56OlLWw5L8) | Approx 01:00–09:00 includes intro/attract; active play ~02:44 onward. Detail 03:08–03:12 grab/throw, 03:40–03:44 reactions/jump kick. Cody loads and lifts/launches victims then releases. Jump kicks hold extended legs along airborne trajectories. Enemies use different depth offsets, horizontal falls and grounded states. Warehouse distinguishes crates/wood barrels/metal drums; subway has a broad combat floor. **Footage is arcade; local Cody/level sheets below are SNES. Do not mix their timings.** |
| Maximum Carnage, NTSC SNES | [LongplayArchive / Spazbo4](https://www.youtube.com/watch?v=dNAL08spYds) | Approx 03:15–11:15; detail 08:51–08:55 reactions, 08:59–09:03 dumpster. Squat/lift → overhead hold → walk under separate object → deep release lunge → enemy knockdown. Pain, backward launch, floor and rise differ. Opponents occupy opposite sides/depths. Compact lives/score/player HP and target identity/HP at top. Lamps occlude building/floor as foreground objects. |

## Sheets actually inspected

Library: `C:/Users/Mike/Desktop/Game Sprite Research`. Source IDs allow recovery elsewhere.

- [Axel 10976](https://www.spriters-resource.com/sega_genesis/sor2/asset/10976/): full and enlarged combat rows; jab extension, chamber/extend/recoil kick, turns, uppercut and floor/rise. **Marked prototype bank** must not be counted as retail animation.
- [SoR2 objects 34508](https://www.spriters-resource.com/sega_genesis/sor2/asset/34508/): upright/damaged vending boxes, wooden staves, warped trash cans, flipping table, vase pieces, flame phases. Material-specific outcomes.
- [Weapons 34509](https://www.spriters-resource.com/sega_genesis/sor2/asset/34509/): separate pipe/sword/knife orientations support modular entities and authored spin.
- [HUD 176703](https://www.spriters-resource.com/sega_genesis/sor2/asset/176703/): bitmap fonts, bars, timer pieces.
- [SoR2 stage 1 485061](https://www.spriters-resource.com/sega_genesis/sor2/asset/485061/): facade/floor modules and separate foreground lamps/fence/objects; layout alone does not specify parallax speeds.
- [Sketch Turner 160680](https://www.spriters-resource.com/sega_genesis/comixzone/asset/160680/): long full-figure banks, directional punches, low/high kicks, twists, rolls, jumps/effects; native crop inspected.
- [Comix page 1 613509](https://www.spriters-resource.com/sega_genesis/comixzone/asset/613509/): panel compositions, sewer pipes/water and repeated architecture with landmarks.
- [Cody SNES 52942](https://www.spriters-resource.com/snes/finalfight/asset/52942/): torso follow-through, throws/jump kicks, pain/fall/floor/rise. Bottom **Custom** row excluded as original evidence.
- [Final Fight SNES slum 74178](https://www.spriters-resource.com/snes/finalfight/asset/74178/): distant skyline separate from facade/floor and crates/tires. Decorative wrecked car does not prove a specific destructible-car mechanic.
- [Spider-Man SNES 25229](https://www.spriters-resource.com/snes/spidermancarnage/asset/25229/): labelled **Lift: one drawing; Hold: one; Hold Walking: four; Throw: three**. Punch bank two visible drawings, uppercut four. Counts describe labelled sheet banks, **not playback duration/simulation ticks**. Strong separate whole-fighter carry/release reference.
- [MC enemies 76955](https://www.spriters-resource.com/snes/spidermancarnage/asset/76955/): overview of archetype bodies/reactions; no detailed timing measurement.
- [MC street 71146](https://www.spriters-resource.com/snes/spidermancarnage/asset/71146/): facade/floor, separate lamps, trash can and objects; clear low-clutter lane.

Exact original simulation timing, hitboxes and AI code were not reverse-engineered. Proposed Elementalist attack slots/timings are design decisions. Decoded 30 FPS copies and 12 FPS detail samples cannot establish every original 60 Hz hold. Use native capture/frame advance for exact timing. Do not claim every listed game permits every carryable object or destructible car; these are Mike's explicit Elementalist requirements.
