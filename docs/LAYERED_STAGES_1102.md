> November6: Stage5 orbital/Earth scenery is retired from the live route by Mike’s request. The original starfield/space parallax and dedicated ascent sky are restored. Other stages keep this layer pack. See `STAGE5_SCENE_RESTORATION_1106.md`.

# Layered stage integration / Tesla power — November 2

LS112 activates the approved Stage 2–9 and X scenery routes. Stage 1 keeps its existing artwork. Runtime owner: assets/layered_stages_1102.js, metadata: assets/layered_stages_art_1102.js. Rebuild: python _BUILD_SOURCE/build_layered_stages_1102.py. The complete approved source pack, prompts and original provenance remain in _ART_SOURCES/layered_stages_1102.

| Stage | Integrated scenery | Material / special handoff |
|---|---|---|
| 2 | Volcanic relay corridor | Original generated eight-frame lava below alpha terrain; native mountain-to-lava reveal retained |
| 3 | Ice relay and lake crossing | Sixteen-frame water below frozen islands |
| 4 | Desert airbases, six-coil electric pad | Twenty-four-frame powered tips, coil bands and traveling arc palette pulses; separate forward highway chase |
| 5 | Orbital structures and Earth | Slow passive scenery over independently moving space bed; native gate/warp ownership |
| 6 | Illuminated mainland city | Sixteen-frame dark water; matching arrival and gameplay sampler; native Rough Riders scroll interlock |
| 7 | Maintenance and industrial sewer | Sixteen-frame toxic bed; real stone aperture retained through an offline source-pixel join; extended native rescue plate |
| 8 | Living biomechanical route | Sixteen-frame violet biofluid; native portal entry and special boss arenas retained |
| 9 | Distant cosmic fragments | Sixteen-frame cosmic current bed; scenery cannot become an enemy or target |
| X | Waterfront city | Forward coastal city cycle above sixteen-frame water; no reversed city districts |

The native stage scroll budgets and encounter schedules remain authoritative. Expanded finite scenery maps onto that same progress; looping travel uses existing unwrapped clocks. Ground footprints are baked from the new terrain, with a Stage 4 paved-spine mask. The old highway director still uses its original logical gaps while weapon bodies and empty pads follow actual visual travel. Stage 4's base image never repeats during the chase. Scenery layer order remains material, transparent terrain, authored power/ambient layers, then native entities and warnings. Stage 5 and 9 new objects are passive background pixels.

All lighting, liquid deformation and animation alpha is authored offline. Runtime selects fixed frame rectangles and blits at native size with ordinary source-over rendering. There are 113 distinct fixed frames in eight editable Aseprite banks; all eight export back to exactly matching RGBA frames. Tesla animation retains the approved empty pad's geometry and six measured tip sockets; the preview aircraft is not baked into terrain. The independent efxClock drives material and power phase; pause holds it, and terrain holds do not freeze the liquids.

Verification: 37 native stage/animation checks, 11 native arrival/chase/weapon-anchor checks and 22 current-behavior sewer rescue checks pass (70 total). All nine route views and Tesla pixels were inspected in the actual engine. The sewer fixture was updated for the November 2 radio, actual hide/stop semantics and current core hash; its older hardcoded October expectations are not production contracts. Source masks, frame uniqueness and Aseprite roundtrips are recorded with the native evidence in docs/qa/layered_stages_1102.json. The required full suite still exits 1 on its pre-existing difficultyHealthBaseline15 harness load-order error, identical before and after this change. This is not a full campaign balance certification.

Stage X building destructibility and cinematic story progression were outside this scenery wiring pass. Existing local work and core game.js/test_fl.js are preserved. No commit or push.
