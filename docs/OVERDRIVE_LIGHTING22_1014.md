# Lighting22 — cover placement, shading and readable projectiles

Local build `overdrive1014-lighting22-r1`, October 14, 2026. Runtime:
`expansion/topdown/js/lighting22.js`, with hooks in `grid21_renderer.js` and
`prism_bastion_1013.js`. All 820 previous character/component PNG hashes
match. No sprite generations, palette replacements or atlas edits.

## Visible changes

- Three.js Lambert materials and computed surface normals now light the corridor
  walls, floor, ceiling and doors. A warm overhead spotlight, cool ambient/rim
  lighting and the cyan door/reactor light preserve the dark industrial feel.
  Helios lights the corridor orange; Yuri's gunfire produces brief warm lighting.
- Real crisp 512px shadow mapping receives box-shaped proxy silhouettes for
  existing barrels, crates, cover and Yuri. Proxies write no visible color; the
  original sprites remain the visual objects. Shadow maps update only when a
  caster placement/state changes. Authored texture sampling stays nearest, with
  no mipmaps, antialiasing or full-scene blur.
- Foreground cover now has solid, textured 3D bodies filling the transparent
  seams of the decorative artwork. Its healthy lip is at logical y374, in front
  of Yuri. Damage lowers the broken lip and zero HP removes that segment's body.
  Near-side attackers still render in front of cover. Bodies pass the camera
  during room traversal; the existing eight-room sequence stays intact.
- Yuri's rifle, shotgun, minigun and laser draw after cover, with larger authored
  projectile heads, contrast edging, brighter centers and short sprite trails.
  The minigun head scale is .94 versus the old .34. Visible impact/expiry echoes
  last 75ms, carry no extra collision/damage, and clear on room breach.
- Incoming bullets/lasers get larger heads and short trails; prism orbs are
  larger. Projectiles batch by far/near depth layer to avoid one texture upload
  per pellet. Existing collision tests, damage, ammunition and cadence stay fixed.
- Other top-down on-foot stages draw player ordnance at 1.95x and enemy ordnance
  at 1.45x, keeping the original lifted gun socket position. Tank/ship renderers
  are unaffected. Attached muzzle flashes are slightly larger in the base.

The lighting uses the official Three.js
[Lambert material](https://threejs.org/docs/pages/MeshLambertMaterial.html) and
[spotlight](https://threejs.org/docs/pages/SpotLight.html) APIs in the locally
pinned 0.186.1 build. Every visible character, prop and projectile retains its
authored source art.

## Native verification

23 visual checks and 24 synthetic raw M30 input checks passed with zero
page, shader, console or asset errors. A logical 640x480 pixel capture accounts
for the main canvas's scaling; checks do not accidentally sample the upper-left
portion of a larger canvas. Standing, prone, crouch, peek and roll pixels below
the solid wall lip match the same view with Yuri removed, proving occlusion.
Disabling shadow reception changes 961 actual pixels.
Each weapon's drawn projectiles visibly changes the sampled pixels, including
bright minigun heads and trails. Lifted on-foot projectile bounds grow around
the same socket center, for both Yuri and enemies. Broken-cover and incoming
ordnance screenshots were inspected. Reactor/Helios lighting and original run
art were verified.

Normal full stage, ordinary input only: mouse 140.967s and D-pad
Retina 146.933s, 1/1 damage,
zero deaths, 33 kills, all eight cores and both boss forms. All seven room
transitions and the spread-shotgun, laser and minigun capsules completed.
M30 checks use the receiver's documented synthetic HID layout; physical button
presses were not performed. Median headless render benchmark:
21.07ms including actual compositing; hardware-dependent,
not an FPS guarantee. Required base suite finished BUILD OK / 0 ERRORS / exit 0.

Evidence: `docs/qa/overdrive_lighting22_1014.json` and `docs/qa/lighting22_views`.
No `assets/game.js` edit, commit or push. Existing unrelated local work retained.
Preview: http://127.0.0.1:8781/expansion/topdown/index.html?fullscreen=0&build=overdrive1014-lighting22-r1
