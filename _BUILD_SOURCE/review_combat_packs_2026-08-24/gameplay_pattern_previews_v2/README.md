# Enemy attack pattern previews

- 192 individual 640×480 GIFs at 16 fps.
- Review artifacts only; nothing is wired into the game.
- Uses each combatant's supplied attack frames, weapon anchors, projectile art, counts, spreads, speeds, and event timing.
- Adds a 250 ms offset so pattern time zero aligns with attack frame 4 instead of firing before the visual telegraph.
- Suppresses independent muzzle VFX because the attack frames already contain baked muzzle flashes.
- Uses minimal category-based drift only to keep the firing origin readable. The combat JSON does not define movement AI.
- Player marker moves laterally to make aimed bursts visibly track a target.
