# Wind projectile direction — October 17, 2026

Mike clarified: "i want spread fire wind machine gun projectiles, not large slugs."

For the next PixelLab art pass, replace the metallic bullet-body appearance of
the current `windBullets` and `windSpread` banks. These should be small green
Wind rounds, with compact bright cores and short curling air trails. Spread
fire must read as separate small pellets in its existing fan; machine-gun fire
must read as a fast stream of distinct small rounds. Do not turn either into
large slugs, missiles, elongated beams or large swirls. Keep chaingun rounds
within the same compact family while retaining their weapon identity.

The live owner already draws MG at 13–17 px and spread at 10.8–14 px by level.
Those are total projectile-art spans, including the trail, not body widths.
Preserve the existing combat stats, trajectories and upgrade rules. Maverick's
homing lasers remain excluded from elemental upgrades.

Use the game's actual projectiles and weapon icons as style/size references.
Choose even frame dimensions first, retain one uniform canvas, stable physical
pivot and proportional scale per bank, and follow FRAME_RESOLUTION_RULES.md.
Create at least sixteen distinct animation frames and inspect onions plus
native in-game pixels before accepting replacement art.

Implemented in the PixelLab pass later on October 17. Three independently
generated16-frame families replace the MG, spread and chaingun appearances.
The real renderer consumed every frame and the largest observed spans stayed
within23 native pixels even at maximum upgrade level. Wind's existing projectile
speeds, firing patterns and upgrade rules remain with their original owners.
See PIXELLAB_VOID_1017.md and qa/pixellab_void_1017.json for verification.
