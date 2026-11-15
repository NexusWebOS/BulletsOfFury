---
name: coleforge-portability
description: Apply ColeForge authored-graphics rules and portable game architecture
  across menus, rendering and game systems. Use when establishing rendering policy,
  designing ports, auditing dependencies or changing graphical behavior.
---

# ColeForge Graphics & Portability

## Standing sprite clarity rule

When this work creates, exports, integrates or reviews sprites or raster game art/animation, apply [the ColeForge sprite clarity standard](../coleforge-sprite-clarity/SKILL.md). Blurry or muddy finished frames are not acceptable; use direct master exports and verify the actual animation at its intended game/display size.


## Current graphics contract

Read [references/authored-graphics.md](references/authored-graphics.md) before implementing game
graphics. It preserves Mike's existing `portable-sprite-games` contract. Current explicit user
instructions take precedence; do not infer an exception from a public skill or an old build.

Authored-sprite mode is the default for ColeForge sprite games. HTML may host the game; it must
not manufacture the game artwork. HUDs, menus, backgrounds and effects use the same rule.
Ordinary movement, frame selection, blitting, clipping, draw order and flips remain permitted.
Camera translation is permitted; camera rotation/zoom must not become a shortcut for sprite
transforms. Use a fixed logical resolution with integer display scaling and letterboxing.

## Establish the rendering mode

- Existing projects retain their documented rendering policy.
- 2D and pre-rendered 3D sprite games follow the authored-frame contract.
- A request for a genuine real-time 3D game authorizes planning its ordinary mesh/camera/rig
  pipeline. Record that choice and its allowed techniques explicitly; this does not authorize
  CSS game graphics or new procedural visual effects. Use `coleforge-3d-production`.
- If a request only says '3D style' and the distinction affects implementation, progress on
  design/assets, then clarify real-time 3D versus pre-rendered sprites before the dependent work.

## Portable core

Keep game rules, timing, collision, AI, animation state, content tables and input actions separate
from host APIs. Use narrow rendering, audio, input, loading, persistence and platform-service
adapters. Shared simulation must run without a DOM, window, wall-clock animation events or a
specific renderer. Prefer explicit ticks and a fixed simulation step; render rate is independent.

Describe content with stable IDs and simple serializable values. Preserve raw sources and a
reproducible import/export path. Include units, tick rate, coordinate conventions, frame rects,
origins, muzzle/socket anchors, hit/hurt boxes, animation phases, layer order and sound events.
Seed gameplay randomness where replay/testing needs it; cosmetic variation must not perturb AI.

## Targets and evidence

Separate host portability, engine portability and a verified platform build. Do not promise 'any
console' from clean architecture or a desktop wrapper. Choose budgets from an actual target:
CPU/GPU time, RAM/VRAM, sprite/texture/atlas limits, storage/streaming and audio voices/codecs.
Keep fidelity tiers as data/asset substitutions while preserving mechanics. Do not invent a
shared Genesis/SNES/Neo-Geo limit or call their aesthetic a hardware compliance result.

Preserve asset provenance and known license terms. Flag missing terms as unresolved; owning a
copy or seeing a logo does not establish rights. Keep platform SDK/certification dependencies
explicit and avoid unsupported legal or platform-approval claims.

For meaningful changes verify adapter boundaries, reproducible loading and frame timing. For
a port, run the real build on available target hardware and report exactly what was exercised.
## Standing retro reference direction

For every 16-bit or retro game Mike creates, including retro-styled host games and native console/handheld work, apply the [standing retro art direction](../coleforge-art-direction/references/retro-art-direction.md) as a default visual reference. Mike adopted the selected art styles on November 6, 2026; he does not need to name those games again. Choose the family that fits the genre/camera, retrieve actual relevant images, preserve approved project identity and the current request, and retain authored-frame graphics. Adapt detail to the actual target rather than inventing a shared hardware limit. This adds art direction; it does not approve new mechanics, replace unrelated existing art or establish an unauditioned sound signature.
