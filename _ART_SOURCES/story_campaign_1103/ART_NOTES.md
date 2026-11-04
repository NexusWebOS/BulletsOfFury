# Source and rendering record

CURRENT BACKGROUNDS — REVISION 8: use the intro-referenced Neo-Geo sixteen-shade color animation in neogeo_panels_1103. Earlier flat/two-color panel records below are superseded. All current pilot identity locks remain in force.

CURRENT IDENTITY — REVISION 7: Cole follows Mike's coleyoung/boxcole references and wears olive green. Maverick is the neon-green pilot with aviators. Earlier neon-Cole notes below are historical misidentification and are superseded. The complete identity locks and source hashes are in CURRENT_IDENTITIES.md.

New imagery was generated with the built-in image-generation tool using actual current BOF cast and aircraft identity exports. Existing cast source pixels remain with C112/CP112; current Rough Riders flight cells remain with RR33. Source hashes are in `provenance.json` and native export hashes in `references/exports.json`.

Generated families: volcanic dish power states; desert launch-pad/hangar power states; empty Command Bay with enhanced map/launch/sewer views; progressive freezing landscape; radar escalation and monitor destruction; nine pilot-specific four-key cable hookups; nine aircraft with four distinct perspective keys; nine headset portraits; six Decker discovery/recoil/recovery/panic poses; connected top-down volcanic and highway destinations; empty lounge and Forge.

Latest user corrections supersede the first alien concept. `symbiote-jump.png` is the replacement based solely on the October24 faceless black/violet fluid symbiote. All four panels conceal facial anatomy. No dragon, snake, eyes, mouth or revealed face is included. The discarded two-eyed creature sheet is not in this deliverable.

The source sheets may have provider-selected dimensions. The exporter preserves one proportional scale across each family and uses transparent padding to deliver even, common cell sizes. Original source dimensions and pixels stay in the PNG masters. Generated aircraft views are keyed source drawings; recession, source-pixel exhaust light and native landing/front-return sizes are baked offline. The running game selects these frames without rotating, scaling or changing image alpha.

Nine cast actor banks preserve common pelvis/ground placement. Known left-facing Yuri/Lizzie run sources are flipped during export for the rightward HQ dispatch. Existing pilots and their ship designs are retained. The new aircraft banks are cinematic only and never replace combat hulls.

The background Forge and lounge contain no baked people; actors can be staged without duplicate cast members. The headset investigation uses the actual selected pilot, with Cole acting as the remote contact when the selected pilot is Decker.

## Headset pixel-art revision

All nine headset POV portraits were newly generated with the built-in image tool from the current cast identity sheet and the approved chunky Cole pixel-art drawing as a shared style reference. These replace the earlier detailed headset rendering. Original generated masters are `headset16-<pilot>.png`; native 128 x 128, maximum 32-color exports are in `headsets-16bit/`. No-dither palette export, hard alpha and exact 2x/3x nearest-neighbor enlargement preserve the new drawn clusters. Comic participants face inward, and the gray footer hides the bottom cut. No browser scaling or filtering was added. Other 88 banks retain exact prior bytes.

## Neon-green Cole

At Mike's request the generated Cole headset master was recolored with the built-in image editor: olive jacket panels become fluorescent green with dark green shadows; his face, skin, hair, headset, gloves, harness and buckles keep their design. Native 128 x 128 / 32-color export and fixed comic framing remain. Only headset-cole, comic-cole and comic-decker changed from revision 3. All other 103 banks retain exact prior bytes. The former olive master is archived under archive/revision3.

## Animated headset frames

Revision 5 replaces the static headset banks with 24 newly generated poses per pilot. All nine final sheets use their approved portrait as identity/style reference. Production grids are 4 columns by 6 rows. Source masters, the shared generation contract, individual normalized frames and SHA-256 provenance are in headset_motion_1103. All poses use one source scale per pilot and a shared chest baseline. Runtime selects native-size pre-exported panels, uses authored turn/talking/emotion frames and stops mouth playback after text reveal. Colors are shared over the whole 24-frame bank rather than independently quantized per cell.

## Pixel comic divider and color scroll

Revision 6 uses new generated divider and color-tile masters. Offline export fixes the divider to a 228 x 128 pixel grid and five gray shades, and color tiles to a 64 x 64 grid with two exact palette colors each. Solid base color occupies over 78% of each tile. Sixteen baked phases per selected pilot supply counter-scrolling panel fields beneath the existing animated portraits. Native timeline dimensions and source pixels remain fixed. Scene elapsed time drives frame selection, so ordinary dialogue changes do not reset the motion.
