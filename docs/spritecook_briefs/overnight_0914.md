# SpriteCook production brief — Mike's overnight request, September 14

Status: **Ship exception authorized by Mike:** the Furyship candidate pack was generated
with the built-in image generator; see [delivery](../FURYSHIP_ASSETS_0914.md). Other
assets below remain ungenerated. SpriteCook is unavailable to this task. Do not
extend the ship-specific exception to other explicitly SpriteCook-only work,
extract OAuth tokens, or expose signed download URLs. Use the connected service's
credit check and owning atlas registration/repack workflow when it is available.

## Missile progression

Use the existing authored red-band silver missile roster as the family reference,
with the equipped pilot band preserved. Produce separate transparent-background
Super, Ultra and Uber upgrade icons plus matching supply boxes. Strong readable
size/tier distinctions, consistent dark outlines, pixel density and metallic
shading. Render candidates beside the existing x5/x10/x20 supply art before
approval. Do not reuse a quantity-only box as a tier upgrade icon.

Damage: Standard 1.0, Super 1.25, Ultra 1.5625, Uber 1.953125.
Super ammunition cap 50; Ultra 35; Uber 20. These are manual retina/free missiles,
separate from the passive homing upgrade. Higher tiers scale up progressively.
Death resets the equipped tier to Standard. Ultra appears only after Super is
acquired and the pilot survives into the following wave; Uber follows Ultra.
Keep upgrade icon and ammunition-box roles distinguishable at in-game size.

## New space fighter

Mike approved `assets/game/gravity_mode/furyship_somersault_13.png` on September 14.
The source and existing reel have been inspected. See [the production contract](../FURYSHIP_REFERENCE_0914.md) for exact dimensions, source hash and requested views/effects. Use that approved concept to create
the component family matching the current ship-parts anchors: center hull,
wings, engine/thruster elements and any existing transformation joints.
Consistent common canvas and pivot across all component frames. Produce true
perspective frames for barrel rolls/somersaults, not flat rotations alone.
Thrusters, speed and transformation effects must remain separate authored reels.

Produce nine pilot palettes preserving luminance, outlines and ordnance colors.
Yuri/Yamado; Maverick/Moonraker; Lizzie/Lavender; Falva/Foxtrout; Cole/Collisto;
Juggernaut/Janis; Axel/Aristotle; Freezer/Falcon.
Decker/Draven (named by Mike on September 14).
New title: SPACE FIGHTER plus pilot model, replacing GRAVITY MODE ENGAGED.
Preserve the old fighter as a password unlock, spcboy, once replacements exist.

## UI and pilot art

- Regenerate Life Up in current Bullets of Fury styling; Continue Up complementary
  but clearly distinct.
- New Yuri boxed avatar must match the other eight pilot boxes, with red lights.
  Preserve Yuri identity; preview alongside the full existing roster.
- Achievement, Boss Rush and Time Attack buttons should match existing menu art.
  Reuse Mike's Nexus II chain/lock overlay for the two locked modes.
- Pause buttons match existing menu chrome and green cursor styling: Resume,
  Return to Main Menu, Restart Level, Options, Help, Quit Game.
- No-continue completion trophy avatar, readable at account/avatar size.

## Bitmap font delivery

Stage titles for all nine authored stage biomes, plus coordinated main-menu,
stage-select and announcer face; readable dialogue face.
Provide mapped glyphs, consistent baseline/cap height and spacing. At minimum:
A–Z, a–z where dialogue uses it, 0–9, spaces, punctuation and controller labels.
Preview actual long menu labels, all nine stage names, Autosav01.json SAVED,
missile tier names and pilot dialogue at shipping sizes. Avoid narrow decorative
strokes disappearing at native pixel scale. Font atlas/maps must be registered
together through their owning workflow; never overwrite manifests ad hoc.

## Verification

Inspect representative source frames first, then generate full strips.
Normalize using common anchors/scale, inspect intermediate and belly/perspective
frames, and verify final keys through XART/game drawImage in real Chromium.
Follow docs/ATLAS_REPACK_0903.md before changing any packed sheet/cells.
This brief records requested production; it is not evidence of completed assets.
