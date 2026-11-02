# Current Breaker selected generation prompts

Tool: built-in `image_gen`, transparent background, both existing
`poses_source.png` and `human_source.png` under `stage9_amplify_1101` supplied
as identity references. Originals remain in the Codex generated image directory;
the selected copies below are the project-owned sources.

## actions_source.png

Selected output: `exec-0bfd6b92-3f96-4c29-8651-16b137fc4215.png`.

Use case: identity-preserve. Production sprite animation sheet for the exact existing blue-white liquid humanoid Current Breaker in the two references. FRAME FORMAT: 1536x1536 transparent PNG, EXACTLY 4 columns by 4 rows, sixteen equal 384x384 cells. Uniform scale and common chest pivot x192 y144 inside EVERY cell; full body approximately300px tall, generous transparent margins, no touching adjacent cells. Preserve his smooth blank blue face with glowing white eyes, muscular translucent cobalt water body, white flowing vein highlights, cyan water tendrils, feet and hands, proportions and frontal identity. No clothing or armor. Same video-game pixel cluster style and palette as reference. Make an animation rather than a pose collection: ROW1 four consecutive LEFT HAND WATER GRENADE throwing frames: palm gathers at waist, arm winds behind shoulder, forward throw with open hand toward viewer, recovery. Other hand guards body. ROW2 four consecutive matching RIGHT HAND throwing frames, mirrored action but same forward-facing face, shoulders turn slightly. ROW3 tidal-water shove first four frames: both hands open wide at waist, both arms gather inward, cupped palms pull back close to chest, shoulders brace and lean forward. ROW4 tidal shove final four frames: both palms thrust forward together, full extension pushing toward viewer, elbows recoil smoothly, return to wide open-palm stance. Keep whole body, head and chest size constant in all16 cells. Draw HANDS EMPTY: summoned water balls and tidal effects are separate game layers. Distinct clear poses and smooth anatomy, no giant foreshortened hands. Transparent background, no text, no grid lines, no labels, no shadows or scenery.

## yaw_source.png

Selected output: `exec-d54a0dd8-02e2-4273-865d-9699aeae06f9.png`.

Use case: identity-preserve. Production pseudo-3D turntable sprite sheet of the exact existing blue-white WATER humanoid Current Breaker from these references. FRAME FORMAT:1536x768 transparent PNG, EXACTLY4 columns x2 rows, eight equal384x384 cells. Full body identical300px height, one chest pivot x192 y144, feet atsame baseline330, uniform proportions and plenty of margin. KEEP the exact cobalt liquid material, white flowing water vein highlights, cyan foamy contours, smooth blank face and white eyes, muscular body and limb proportions. Do NOT redesign him as armor or a robot. Arms held out diagonally with open palms charging liquid energy, same pose throughout. Eight ACTUAL three-dimensional yaw views around his upright vertical body axis, read left-to-right top row then bottom: FRONT0deg, FRONT-RIGHT45, RIGHT PROFILE90, BACK-RIGHT135, BACK180, BACK-LEFT225, LEFT PROFILE270, FRONT-LEFT315. Camera remains slightly above eye level consistently like the approved frontal sprite; humanoid stays upright. Actual shoulders, head, face and back change with viewpoint. Do not planar-rotate a front sprite. No visible face/eyes on back views. No ground plane, scenery, balls, text, labels or grid lines. True transparent background. Keep all8 distinct views registered, stationary chest, consistent head/body size, entire feet/hands insideeach cell. Pixel-art clustered shading matching reference.

## Normalization and retained source art

The returned PNGs are1254x1254 and1774x887; the owner normalizes their grids
using shared transparent padding into fixed384px chest-pivot cells with one proportional scale per bank. Full
source frames1 and5 are exchanged to keep each windup on the same hand as its
throw. The turntable uses actual front/profile/back source views plus baked
opaque source-flow interpolation, rather than runtime planar rotation.

The prior orb/morph bank and existing wave art remain identity sources.
The wave loop gains32 baked flow frames. The original16 Falva-derived roller
spin cells (`kaia_roller_1028/spin.png`, original source `nfrb_3`) preserve alpha
and luminance while moving into a blue/white water palette. Moving emissive
water masks use the existing `pixel_glow_1015.rings` baker and native hard rings.
