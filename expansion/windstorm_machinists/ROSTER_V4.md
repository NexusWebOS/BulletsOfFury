# Machinists appearance revision

7 October 2026. Selected user-requested revision:

- Rolf: cobalt-blue hair, blue jacket/armor and trousers.
- Wren: black undersuit and white armor panels.
- Chaz: blond hair, red forehead bandana with tied tails, red outfit.

Portraits, pilot avatars and full-body identity poses use versioned `identity/*_v4.png` files. The manifest and preview select this revision; earlier artwork remains preserved. Shared-body palette entries now reflect these outfit colors. Portrait borders use the game's exact authored template and retain its alpha geometry.

Source: `source/machinists_identity_v4.png`. Preview: `previews/machinists_v4.png`. Exact built-in image_gen prompt and provenance: `roster-v4-generation.json`. `build-roster-v4.cjs` rebuilds the selected derivatives and is called automatically by the main asset builder.
