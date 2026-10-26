# GPT poses -> PixelLab motion provenance

Frame format: live Phoenix/infused-host cells 512×512, core pivot (256,256); live Chronos cells 448×448, pivot (224,258). Uniform transparent canvases and one proportional scale per actor. PixelLab input cells are 256×256. Source crops may be odd: shared padding/normalization produces even delivered cells.

Actual native references are in reference/. GPT output sheets are each 1254×1254; their raw output remains untouched. Phoenix/host normalization is recorded in pose_geometry.json. Chronos uses source crop rectangles (0,0,640,700), (640,0,1280,700), (0,700,640,1280), (640,700,1280,1280), shared scale .52 and respective measured core locations (351,393), (304,395), (342,215), (315,276), placed at (239,219) on 448px. Crops extending beyond the raw sheet use transparent padding. The normalized whole inputs in poses/ were inspected before animation.

GPT pose direction: preserve the native silhouette/palette/weapon identity and connected anatomy. Phoenix: neutral spread, raised-wing anticipation, firing downstroke and recovery. Infused host: neutral claws, drawn-back elbows, forward claw lunge and recovery. Chronos: neutral, overhead hammer hold, extended casting arm and kneel with hammer beside him. Each request supplied the native rendered reference; this is not a generic robot replacement.

jobs.json records all nine initial pinned-endpoint PixelLab jobs; motion/ preserves their 17 images each. phoenix_v3/ preserves the nine-image replacement wing interpolation, job a21ca76e-5ad0-438d-a83e-6e403792dba1. Its input was poses/phoenix_0_256.png, ending at phoenix_1_256.png, seed 102424, eight generated frames, transparent. Motion request: one slow continuous wing lift with different equally spaced wing angles, fixed chest/paired cannon pods/two barrels each, no firing/effects/spin/translation/zoom.

Accepted source frame lists are recorded per delivered bank in the generated manifest. Rejected candidate frames remain here for comparison; they must not be blindly reactivated. Builder: _BUILD_SOURCE/build_boss_integrity_1024.py. Native verification and limitations: docs/BOSS_INTEGRITY_REPAIR_1024.md.
