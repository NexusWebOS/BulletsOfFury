# Proven whole-cycle prompts

Use semantic input roles. Preserve the chosen fighter's identity rather than copying the motion model. Adjust counts, grid and dimensions when the actual guide differs.

## Walk

> Image 1 is the exact smooth SpriteCook WALK motion/layout guide only. Retain all eight complete whole-body poses in row-major order, alternating foot contacts, loading, passing/recovery, opposite arm action, root axis and loop closure. Image 2 is the sole approved full-character identity and costume for [fighter]. [List distinguishing face, hair, clothing, footwear, physique and carried prop.] Image 3 is a rendering-quality example only. Draw the same fighter in every pose, with fixed anatomical lengths, torso thickness and natural head-to-body ratio. Keep eyes/face readable. Each frame is a complete drawn character, never assembled parts or pasted heads. Remove any coat, hair, weapon or footwear copied from the motion guide that is absent from the identity. Preserve the identity's actual accessories and bare feet. Eight complete figures, four columns by two rows, equal cells, generous transparent gutters and complete limbs/props. Crisp arcade pixel clusters, no blur, shadows, scenery, labels or grid lines. True transparent alpha.

## Run

> Image 1 supplies the exact SpriteCook RUN motion only: preserve eight ordered poses, opposite arm pumping, forward torso lean, contact/compression/passing/recovery, loop closure and two genuine flight phases. Image 2 is this same fighter's newly drawn WALK and supplies the face, costume, material shading, head size, torso thickness and anatomical limb lengths. Image 3 is the approved full-character identity. Running bends and leans that same body; it does not enlarge it to fill the frame. [Restate distinguishing identity details.] No new garments, coat tails, weapons or hairstyle from the guide. Each pose is one complete drawing, with full extents in the fixed cell. Crisp hard pixel clusters, deliberate material shading, clean transparent gutters; no scenery, text, grid lines or blur.

Do not describe an eight-pose coherent sheet as a character-part tileset. The workflow reuses **motion**, not sliced heads/limbs. A single targeted correction should preserve the rest of an accepted cycle; retain rejected sources outside runtime/package assets for provenance.

Original exact prompts and input metadata from accepted examples are bundled beside these patterns as `accepted-tyler-walk-prompt.json` and `accepted-tyler-run-prompt.json`. They are examples, not permission to force Tyler's face or outfit onto the roster.
