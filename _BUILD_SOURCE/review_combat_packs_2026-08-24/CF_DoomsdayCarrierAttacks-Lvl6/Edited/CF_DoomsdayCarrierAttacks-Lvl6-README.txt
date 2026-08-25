COLEFORGE — DOOMSDAY CARRIER MK II ATTACK SYSTEM

Project: Bullets of Fury I
Level: 6
Boss: Doomsday Carrier Mk II
Runtime boss origin: 640x320 at (0,0)
Gameplay preview canvas: 640x480
Coordinate system: x right, y down

CONTENTS
- 23 reusable attack/VFX families with standalone transparent frames, atlases, JSON and GIF previews.
- Six position-locked full-boss firing cycles in Edited/Master Edit.
- Six gameplay choreography previews.
- Exact weapon anchors and pattern timelines in CF_DoomsdayCarrierAttackPatterns-Lvl6.json.

ENGINE RULES
- Spawn projectiles separately from full-boss frames.
- Use boss-cycle frames only for weapon-port lighting, muzzle flashes, bay motion, and center-cannon motion.
- Preserve the original MK II component hitboxes and 640x320 origin.
- Omega bombs are reflectable; swap to omegabomb-reflected after successful player deflection.
- GIF files are review previews, not runtime masters.

BACKGROUND POLICY
- Source boards use exact #FF00FF.
- Runtime PNGs use hard binary alpha and contain no source-key pixels.
