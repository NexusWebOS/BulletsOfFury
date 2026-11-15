# Export and verification

## Authoring normalization

1. Inspect actual canvas dimensions and alpha before splitting. Resample the entire canvas uniformly with nearest-neighbor; never stretch its axes differently. Keep the declared grid and empty gutters.
2. Clear exterior-connected pale matte when present. Generated RGBA can contain almost-white or gray backgrounds with alpha 170–225 and faint colored RGB noise. A simple alpha-128 threshold does not always remove them. Flood from cell boundaries through exterior matte; do not globally delete white pixels. Enclosed eyes, soles and white-hot fire cores must survive.
3. Remove only confirmed stray export debris. Do not discard legitimate detached weapon tips, hair strands, flame tongues or deliberately separate effects because a connected-component heuristic calls them small.
4. Calibrate one whole action bank to the standing unit and expected pose projection. Every drawing in that action shares the factor. Compare anatomical landmarks across idle/walk/run; a numeric projected-height ratio alone cannot validate them.
5. Register the pelvis/root and floor through whole-frame translation. Preserve intentional airborne floor gaps. Expand the export cell for extents rather than clipping or resizing one pose.

## Native pixels and editor documents

OpenBOR can use the first model frame's palette for subsequent frames. Reindex new native drawings into the existing model palette; preserve transparent index 0. Do not silently replace every other action's palette to suit one new bank. Check binary alpha and complete margins in the actual indexed PNGs.

Create Aseprite documents with complete fixed-cell cels, one authored-character layer, action tags, durations and an origin slice. A single layer is intentional here: detachable weapons/effects may be separate assets, but people are not cutout rigs. Export without trimming, deduplication, ignored empty frames, or per-pose scaling.

Store integer milliseconds explicitly. Prefer `sprite.frames[i].duration = duration_ms / 1000` over a round trip through floating tick values. Verify the resulting file by exporting it again and comparing pixels and exact frame durations. GIFs require 10 ms time increments; preserve loop totals when rounding. OpenBOR delay values use centiseconds and the project maps these to its simulation speed; do not confuse them with 60 Hz display frames.

## Visual and runtime evidence

Inspect 1x and integer 2x previews, previous-only and next-only onions, both together, frames two apart, and last-to-first. Compare the same body in its existing idle, new walk and new run. Watch for scale pulsing, head/hair redesigns, shirt/coat changes, glued feet, missing passing poses, foot sliding, malformed knees, arm/leg motion on the same side, and props changing size.

In-game verification must show the actual game scale, camera, floor and palette. Exercise new frames in the native engine; a web GIF is insufficient. A coverage fixture may force animations to prove every frame loads and advances, but it does not prove AI selection, gameplay feel, anatomical consistency or a good gait. Test actual run input/chase selection and stopping/approach separately when changed.

After integration, run the relevant movement, combat, defeat and encounter regressions. Preserve the existing unit, bounding/hit boxes unless the move actually requires a change. Make the final asset rebuild stage reapply the accepted clips so an older exporter cannot revert them. Install only task-owned files with a backup and before/after hashes.

The bundled validation script reports structural faults and measured heights. Treat those measurements as diagnostic evidence, not automatic art approval. Do not claim literal console hardware compliance from an indexed PNG or a 16-bit visual style.
