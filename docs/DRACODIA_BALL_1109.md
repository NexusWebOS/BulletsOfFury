# Dracodia's Chronos ball — November 9, 2026

The hammer copy has its own complete front-facing curl, compact pseudo-3D rolling shell and reverse unfold. Sixteen source drawings per bank, with regular, chromium, rage, white-impact and red-impact materials sharing identical alpha. The accepted fold draws the compaction into the poses; one proportional unit scale is used per bank. Fixed 384×384 fold and 256×256 rolling cells preserve detail while limiting the ten decoded sheets to 65 MiB. No runtime tinting, rotation or sprite resizing was added.

Built-in GPT image generation supplied the raster poses, using the approved forward-facing Dracodia and existing Chronos fold/roll as identity and motion references. Aseprite owns normalization and editable five-layer sources; the prompt set is [prompts.json](../_ART_SOURCES/dracodia_ball_1109/prompts.json). The first oversized fold is retained as a rejected reference and is excluded from runtime.

The native attack-book slot that previously aliased `ball` to a standing hammer spin now selects the real rolling form. The explicit standing `spin` attack remains available. A short approach keeps the full transformation clear of the health bar. The native one-piece body mask and Retina target follow the displayed pose; no invisible held hammer or gun targets remain during ball mode.

| Phase | Timing and behavior |
|---|---|
| Approach and curl | 0.35 s movement into clear view, followed by 1.25 s authored curl; native green/yellow/red committed-path warning |
| Roll | Up to 3.85 s, 16 authored axial poses, 9 radians/s animation clock; Normal ×1, Hard ×1.15, Furious ×1.45 travel |
| Ordinary impact | Brief red authored silhouette; velocity stays unchanged |
| Rocket impact | Brief white authored silhouette; direction commits away from the current shooter |
| Counter reaches edge | Stops rolling and unfolds; no immediate ricochet back toward the player |
| Recovery | 0.22 s orienting the shell, then 1.15 s reverse unfold into a clear upper position; native combat resumes |

The forgiving ram radius is distinct from the measured visual spike extents reserved at the arena edges. Native health floors, form pools, phase progression, score, defeat and cleanup remain owned by RD74/J3. Native charge, throw and impact audio cues are reused. Stage 5 Chronos and other Dracodia forms keep their existing behavior.

Validation and recordings are saved beside the game under `_shots/dracodia_ball_1109`. The GIFs are full-height native-engine Furious checkpoints, with an invulnerable observer. The gun impact is explicitly triggered; the counter recording launches a real inventory Retina rocket and records its travel and deflection. The full regression suite retains its existing `difficultyHealthBaseline15` ReferenceError at `assets/combat_polish_0927b.js:151` and does not reach its final summary.

Runtime: `assets/dracodia_ball_1109.js`; assets: `assets/game/shared/combat/dracodia_ball_1109`; editable sources and prompts: `_ART_SOURCES/dracodia_ball_1109`.

Final evidence: 32/32 focused native checks passed across Normal/Hard/Furious and regular/chromium/rage; red/white native damaged-pixel checks and expiry passed. The live capture launched a real inventory Retina rocket, recorded its deflection, and recorded no ricochet after the counter. The final recording has26 native SFX starts, peak0.6764, and no browser/audio errors. Inspected full-height480×512 GIFs show both recovery and the red/white impacts. Native game.js hash remains b46bb789b6344f31d0ecba126169447d491152670c09decc6da624bc4b5d2215.
