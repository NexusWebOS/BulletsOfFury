# Regenerated Firewhip — September 23, 2026

Replaced the straight fire-laser strip used by Firewhip with a generated eight-frame living-fire reel. Its silhouette narrows from a bright root to an authored pointed lash tip; individual flame tongues change between frames. SpriteCook GPT 2.5 Sunburst, asset `88bf8613-369c-4dc6-90d4-bddf1ad46fcf`, 14 credits. Original source, prompt, normalized frames and SHA-256 prefixes are in `assets/game/player_weapons/fire_whip_0923`.

The renderer maps the flame from its bottom root to its top tip along the existing whip curve. Visual subdivision uses 64 slices with overlapping interior joints; the final tip retains its alpha silhouette. Flame animation runs at 16 fps independently of sweep reversals. The approved circular fire muzzle stays at the root. Collision sweep sampling, reach, damage and attack timing are unchanged.

`_BUILD_SOURCE/build_fire_whip_0923.py` removes near-invisible alpha residue, aligns the emitting roots and normalizes each frame to 64 x 256 without synthesizing or painting sprite artwork. Loose XART registrations avoid atlas changes.

Syntax check passed. `_BUILD_SOURCE/probe_firewhip_muzzle_0923.py` verifies the moving live root, stop behavior, exactly one muzzle, Forge preview and all eight actual frame keys through the game context. No page or console errors. Inspected live/Forge screenshots and exported a flame-loop GIF in `_shots/firewhip_muzzle_0923`.

Final suite: `_shots/firewhip_regenerated_final_suite_0923.log`, 4,889 passing assertions, exit 1 with the same 81 failing assertion names as `_shots/firewhip_muzzle_suite_0923.log`; no new failures. No commit or push performed.
