---
name: portable-sprite-games
description: Apply Mike's portable, authored-frame graphics rules when creating, modifying, or reviewing any of his game projects, including Bullets of Fury. Use for gameplay rendering, animation, effects, HUDs, menus, and game assets.
---

# Portable sprite games

## Standing sprite clarity rule

When this work creates, exports, integrates or reviews sprites or raster game art/animation, apply [the ColeForge sprite clarity standard](../coleforge-sprite-clarity/SKILL.md). Blurry or muddy finished frames are not acceptable; use direct master exports and verify the actual animation at its intended game/display size.


Build HTML-hosted games with portable game logic and authored sprite graphics inspired by Sega Genesis, Super Nintendo, and Neo-Geo. HTML is the host and presentation surface; it must not supply graphical effects. This is an ongoing preference across Mike's game projects, including Bullets of Fury, unless he explicitly overrides it.

## Standing even pixel dimensions rule

All ColeForge games, explicitly including Bullets of Fury, require **even frame pixel width and height**. Mike clarified this on November14,2026. Follow [even frame dimensions](../coleforge-even-frame-dimensions/SKILL.md): pad odd crops transparently, preserve roots and body size, and validate actual cells. Animation frame counts may be odd; do not duplicate or drop poses merely for count parity.

## Graphics contract

- Express rotations, turns, perspective changes, fades, flashes, dissolves, lighting, shadows, smoke, explosions, trails, distortion, and other visual effects through authored animation frames or pre-rendered image assets. If an asset is missing, create or request the asset, or use a plainly identified temporary frame; do not substitute a browser effect.
- The only runtime image orientation changes allowed are horizontal and vertical flipping. No runtime rotation, skew, perspective transformation, arbitrary sprite scaling, mesh deformation, or tweening of these properties. Directional poses and changing sizes need authored frames.
- Do not use CSS transitions, CSS keyframe animation, opacity animation, gradients, filters, blur, glow, box/text shadows, blend modes, masks, SVG effects, WebGL shaders, canvas compositing effects, or engine equivalents to enhance game graphics. This restriction applies to HUDs, menus, overlays, and backgrounds as well as gameplay.
- Use ordinary transparent sprite pixels for cutouts. Display pre-authored pixel alpha as stored; do not animate global alpha or generate transparency effects at runtime. Prefer palette-authored, opaque/dithered effect frames when practical for a future demake.
- Permit sprite/frame selection, image loading and decoding, source rectangles in atlases, positioning, clipping to the viewport, draw order, camera movement, tile placement, and sprite flipping. These are basic rendering operations, not permission to synthesize visual effects. Moving sprites and scrolling backgrounds remain allowed; motion does not require a separate frame for every screen position.
- Canvas 2D or an engine sprite renderer may blit images. HTML/CSS may size and position the hosting surface. Do not interpret the rule as forbidding the minimal drawing API needed to display the game.
- Use a fixed logical resolution, nearest-neighbor sampling, and integer pixel placement for rendering. Whole-viewport integer scaling for display is allowed; keep it distinct from scaling individual sprites as an effect. Use letterboxing where needed.
- Use bitmap fonts and authored UI imagery for visible game presentation. Native HTML controls may support development tools or accessibility outside the game artwork; they must not become a source of game visual effects.

## Portability contract

- Keep simulation, input actions, collision, timing, animation state, and game rules independent of DOM/CSS/browser APIs. Place browser input, audio, storage, loading, and rendering behind small adapters.
- Use explicit data for frame sequences, durations, sprite origins, hitboxes, hurtboxes, tile maps, palettes, and layer ordering. Advance animation using game time and explicit states, not browser animation events.
- Prefer a fixed simulation timestep and simple, documented data structures that can be translated to other languages. Treat frame rate and animation playback rate as separate concepts.
- Keep original assets and reproducible atlas/frame metadata available. Do not bake game rules into CSS, HTML layout, engine-only visual graphs, or browser-specific effects.
- A portable architecture supports future ports; it does not guarantee operation on every language or console. Genesis, SNES, and Neo-Geo are artistic influences, not an imposed shared hardware specification. Do not invent palette, sprite-count, memory, audio, or resolution limits. Establish target-specific budgets only when an actual port or demake is requested.

## Apply and verify

Before changing graphics, inspect the relevant rendering and asset paths and apply this contract alongside project-specific skills. Resolve conflicting visual suggestions in favor of authored frames unless Mike explicitly requests an exception.

For existing games, scope migrations to the requested work. Identify relevant violations and explain any remaining ones; do not silently rewrite unrelated systems or claim a complete audit after a partial inspection.

Verify new visual behavior in the running game when possible, and inspect the changed rendering paths for prohibited runtime effects, including effects hidden inside engine helpers. Confirm flipping, frame timing, pixel alignment, camera movement, and intended viewport scaling. State missing assets or verification limits plainly. When proposing an effect, describe the frames/assets it requires instead of offering CSS or shader shortcuts.
## Standing retro reference direction

For every 16-bit or retro game Mike creates, including retro-styled host games and native console/handheld work, apply the [standing retro art direction](../coleforge-art-direction/references/retro-art-direction.md) as a default visual reference. Mike adopted the selected art styles on November 6, 2026; he does not need to name those games again. Choose the family that fits the genre/camera, retrieve actual relevant images, preserve approved project identity and the current request, and retain authored-frame graphics. Adapt detail to the actual target rather than inventing a shared hardware limit. This adds art direction; it does not approve new mechanics, replace unrelated existing art or establish an unauditioned sound signature.
