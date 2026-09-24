# Symbiote finale art (September 24)

`ground_portal_rise_sheet.png`: 16 frames, 4 columns x 4 rows, 1448 x 1086 RGBA. Ground-contact anchor is bottom center of each cell. 150 ms per frame is the review cadence; combat may vary timing by phase. No ship is baked into any frame.

`void_death_sheet.png`: 16 frames, 4 columns x 4 rows, 1448 x 1086 RGBA. This is an overlay with an empty center through the crush; the actual selected player's ship must be composited separately underneath and scale/crush into the last explosive frames. Palette is black, gray, white, and red; no purple.

`preview.html` plays both sheets side by side and supports frame scrubbing. The other sheets are authored source layers for the four-form final boss and remain separate from the player-death assets.

`ground_portal_beam_sheet.png`: 8 frames, 4 columns x 2 rows. The beam is a separate bottom-center anchored overlay raised from the ground portal at its burst. The lane is warned before extension. Its live collision can catch a player lifting straight out late; moving across the warned lane remains the counter.
