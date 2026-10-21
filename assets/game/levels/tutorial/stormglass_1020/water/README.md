# PixelLab Stormglass ocean animation

Mike requested actual new PixelLab water for the tutorial. PixelLab generated the deep-teal256x256 base tile and a32-phase PixMiniMax animation with the same starting and ending reference. The shipped loop contains32 distinct source poses; it changes the waves and foam rather than sliding a recolored old tile.

- Seed job: `09d1b679-e3a5-4506-8be8-011ac609a5c5`.
- Animation job: `afa80ee9-340a-4002-8fff-90a9f79a0d69`.
- Runtime: `224x224` opaque frames,12fps, fixed pivot[112, 112], scale1.0 throughout.
- Spatial seam finishing: identical32px overlap for every frame. Raw originals remain archived. No per-frame fitting, frame duplication, ping-pong playback or synthetic temporal interpolation.
- One lossless `1824x912` texture with2px edge extrusion, below2048px on either axis. Atlas, cell metadata and runtime registration are generated together.
- Water pack including loader: 375,493bytes. Raw frames and previews stay outside shipping assets.
- Preserves ocean10px/s/camera0.24; far clouds15px/s/camera0.36; architecture28px/s/full camera; near clouds39px/s/camera0.82. All scenery draws below combat.
- No recoloring canvas allocation or legacy-water fallback in the tutorial renderer. One lazy-loaded texture; campaign water is unchanged.

