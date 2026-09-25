# Stage 7 sewer asset prompts

These two bitmap assets were generated here with the built-in image-generation tool, using local gameplay art as style references. No SpriteCook tool was used.

## `sluice_vent_8f.png`

Reference: `_shots/stage7_baseline_0925/shot_0008.png`.

> Create a production-ready 16-bit pixel-art SPRITE SHEET for a Stage 7 sewer gameplay hazard in Bullets of Fury. Use the provided gameplay screenshot as the strict visual style and palette reference: corroded bronze-green pipework and concrete, luminous chartreuse sludge channels, dark outlines. STRICT 4 COLUMNS by 2 ROWS of EIGHT EQUAL square cells. In EVERY frame the SAME compact industrial sewer pressure outlet is anchored at exactly the same point at the LEFT edge of its cell, firing horizontally RIGHT across a corridor. Frames 1-2: closed grate with pulsing amber caution lamp and subtle green leakage, visibly harmless; frame 3: pressurized bright green nozzle glow and small droplets, still a warning; frames 4-5: coherent high-pressure horizontal stream of toxic chartreuse sludge extends from left to near the right edge, lethal active frame; frame 6: stream breaks into splashing droplets, still active; frame 7: stream collapses to a short spill; frame 8: grate cools with residual drips. Show the full nozzle and the ENTIRE stream tip within every frame, consistent physical dimensions and anchor, crisp chunky pixels readable over busy sewer terrain. True transparent alpha background, generous transparent cell gutters. No floor, no wall, no scene background, no labels or text, no numbers, no grid marks, no magenta, no purple, no UI. The green stream must not appear in warning frames except tiny leakage at nozzle. No circular explosion.

## `sluice_warning_lane.png`

References: `_shots/stage7_baseline_0925/shot_0008.png`, `assets/game/stage7_sewer_0925/sluice_vent_8f.png`.

> Create ONE reusable 16-bit pixel-art transparent overlay asset for Bullets of Fury Stage 7. It is a sewer PRESSURE-JET WARNING projected along the floor, NOT the attack itself. Use the supplied sewer gameplay screenshot and matching mechanical vent sprite as strict style references. A long, low horizontal lane marker viewed straight top-down, roughly 6:1 aspect ratio: two rows of alternating amber-orange and black pixel hazard chevrons running left-to-right, with bright amber pixel lamps at both ends and faint chartreuse reflection along its center. Industrial warning paint / holographic floor projection, hand-authored chunky pixels, strong readable silhouette over olive concrete. Leave the ENTIRE area outside the narrow strip genuinely transparent alpha; no background, no pipe, no fluid jet, no text, no letters, no numbers, no grid. Show a single complete strip centered in the image with generous transparent margins. The chevrons should point away from the vent toward the stream tip. Designed to be drawn at about 200 by 24 gameplay pixels as a telegraph before a toxic burst.
