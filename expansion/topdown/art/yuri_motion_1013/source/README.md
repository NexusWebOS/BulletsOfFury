# Yuri movement revision — October 13, 2026

Generated with the built-in image_gen tool from Yuri's approved in-game
directional sprites and identity plate. Exact prompts and returned originals
are retained here. Layout references contain the approved seed at its original
size on a transparent canvas; they are reference material, not runtime art.

Accepted sources: yuri_east.png (second generation), the seven other directional
sheets, and yuri_south_run_fire.png. The south sheet returned only six firing
poses, so the dedicated twelve-pose sheet supplies that action. The generator
returned sixteen poses in the north/northwest loops and fourteen in northeast
walk/fire. All distinct authored poses are retained; runtime uses a normalized
cycle, so extra poses do not change movement speed or stride duration.

Final source prompt for east: yuri_east.v2.prompt.txt. Other
directions use their *.v2.prompt.txt; south fire has its own exact prompt.
The initial *.prompt.txt files document the original requested layout.

Owner: expansion/topdown/_research/build_yuri_motion_1013.py.
316 PNG exports / 24 banks. Exports share 320x320 transparent canvases and
pivot 160,256. This adds 32 px transparent margins to the planned 256 px canvas
to retain boots and rifles around asymmetric torso pivots. Each directional
sheet uses one proportional scale measured against the approved 176 px standing
body; the independent south firing sheet has its own common bank scale.
Source crops, translations, scale and SHA256 are recorded in manifest.json.

Connected-component isolation separates complete authored bodies, including
limbs crossing nominal source grid boundaries. It preserves alpha and never
repaints, warps, mirrors or synthesizes in-between poses. Torso/ground
registration avoids rifle/foot swings moving the whole character sideways.
All 316 exports were drawn and inspected through native game ART in Chromium.
