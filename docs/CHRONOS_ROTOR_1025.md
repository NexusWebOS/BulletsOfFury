# Chronos full-turn rotor, gold ammunition and red wave

Mike's follow-up requires a visible full360-degree barrel turn, muzzle fire, golden slugs and an animated red/white energy wave. Inspected the supplied MakeAGif reference https://makeagif.com/i/VCa_Rx, including consecutive firing frames. Reference inspection remains in ignored `_shots/chronos_rotor_1025/`.

Final runtime owner: `assets/chronos_rotor_1025.js`, after C30. `assets/chronos_rotor_art_1025.js` performs deterministic native-canvas transformations of existing authored pixels: longitudinal circumferential texture transport and a complete rotating muzzle disk within its projected ellipse.36 cached ten-degree poses, fixed104x208 canvas/pivot54,46. Fixed receiver, collars, body and hand grips. Continuous angular accumulator accelerates during firing; a full turn returns exactly to its starting pixels. These are code-driven authored-image transforms, not newly generated PixelLab frames. Previous16-frame wobble is superseded.

Native flash timer now selects the existing authored fire reel at the bore plane, in gold. Native rounds use a deterministic gold luminance-preserving palette. Their transparent source padding is removed before rendering at10x24, matching existing collision extents. Previous color blend preserved too much blue and padded source reduced the visible bullet to only a few pixels. Damage, audio, module health/bar, Retina and death owners remain native. Existing red-body hit flashes and expiry verified again.

The C30 wave's animated authored frames retain their alpha, motion and white core. Only the palette changes to red/white. No blue-energy pixels remain in the inspected active frame. Wave anticipation, locked lane, damage and two-handed poses remain unchanged.

Native probe `_BUILD_SOURCE/probe_chronos_rotor_1025.py`:11 passed,0 failed, no page/console errors. Full-turn endpoint equality, native muzzle position, visible projectile pixels, red/white pixel counts, real scaled body damage/flash expiry and player wave contact included. The old16-phase distinctness check is retained as source regression, not evidence of the new36-angle rotation. Inspected native angle contact sheet and firing screenshot.

Audible56-second Furious checkpoint recording: `_BUILD_SOURCE/record_chronos_rotor_1025.py`; invulnerability/phase checkpoints labeled, not a full-fight clear. Inspected decoded frames for muzzle fire, gold projectiles and animated red/white wave. Delivery verification6/6, decoded sound and browser play/seek/frame preview. Primary preview updated; previous C30 preview archived as `rotary-rage-review.html`. Scratch and video live under ignored `_shots/chronos_rotor_1025/`.

Syntax checks pass for game.js and both new files. Required test_fl exits1 before any assertions/final summary due the previously recorded missing `_BUILD_SOURCE/retired_art_archive_1022.cjs`. No commit/push; unrelated work preserved.
