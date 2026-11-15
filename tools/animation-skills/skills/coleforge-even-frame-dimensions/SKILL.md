---
name: coleforge-even-frame-dimensions
description: Enforce even pixel width and height for authored sprite frames when creating, editing, exporting, packing or importing ColeForge game assets, including Bullets of Fury.
---

# ColeForge even frame dimensions

Mike explicitly clarified this engine rule on November14,2026: **each frame's pixel WIDTH and HEIGHT must be even integers** in all ColeForge games, including Bullets of Fury. Examples:160×160,256×320,800×600. Reject167×159 until its frame canvas is padded to168×160.

This does **not** require an even animation frame count. Three-, five- or fifteen-frame animations are allowed. Do not drop, duplicate or retime poses to satisfy a pixel-dimension rule.

- Choose even cell dimensions before generation/export and retain a uniform cell/pivot for each bank.
- For an odd crop, add transparent padding to the next even width/height. Prefer padding on the right/bottom to preserve existing origins. Record any offset if padding elsewhere. Never stretch the artwork, crop required pixels or independently resize poses to force parity.
- Validate actual FRAME/CELL dimensions, not merely the overall atlas dimensions: eight167-pixel cells produce an even-width atlas but still violate the rule.
- Keep source rectangles, cell dimensions, origins, bounds, sheets and imported runtime descriptors synchronized. Confirm complete weapon/limb extents and native clarity after export.
- Check generated and edited assets before engine integration. A raw image-generator source may require export padding; the delivered in-game frame must comply.

Bullets of Fury already states this requirement in its project AGENTS.md and `docs/FRAME_RESOLUTION_RULES.md`; preserve its current owning builders and other project rules. Saving this shared policy alone is not proof that every historical asset has been audited or repaired.
