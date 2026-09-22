# Bullets of Fury — easiest-to-hardest work order

**195 entries: 170 complete / 12 partial / 13 pending.**

Work in ascending workOrder, an estimate of implementation plus verification difficulty. Respect prerequisites and skip externally blocked items while continuing ready work. Re-rank when investigation changes the estimate; retain IDs and explain the change.

Completed entries are excluded. The list below contains every unfinished item exactly once. Partial items retain that status. Difficulty bands are estimates, not promises that an unchecked feature already works. Asset/naming dependencies can be skipped until available.

## Shared systems and progression

1. **ENG-23 · Partial** — Audit and repair the Forge/weapon upgrade loop. The Stage-1-to-2 boss reward, two combines, re-spec, Loadout swap, death persistence, audible UI cues, campaign manual-slot and autosave round-trips, and Stage-3 entry have Chromium proof. Stage-1 through Stage-9 boss elements and all 81 weapon/element pairings have Chromium proof. Weapon switching now applies the exact forged level without leaking an aura to bare weapons; full natural-play combinations still need review.

## Complex encounter choreography

2. **S1-15 · Pending** — Furious Razorback: retune consecutive retina rocket salvos and distinguish red warnings, projectiles, explosions and armor during peak attack density.

## Shared systems and progression

3. **ENG-20 · Pending** — Hard/Furious hazard readability: separate warning, hostile projectile, explosion and enemy-palette values when several red effects overlap.

## Current boss brief — awaiting Stage 2 identity

4. **S2-10 · Pending** — Accelerating screaming head frames and shrieks/shake; two fire-ring X cycles; final white flash, absent boss and residual explosions. Dependency: Mike: Stage 2 boss identity.
5. **S2-11 · Pending** — Continue scrolling after defeat; RNG different-pilot dialogue addressing the player about the assimilated military mech. Dependency: S2-10.

## Shared systems and progression

6. **ACH-06 · Partial** — Entire game without spending a continue: 1000 points plus a generated trophy avatar. Award trigger is complete; SpriteCook trophy avatar remains. Dependency: SpriteCook.
7. **ENG-02 · Partial** — Migrate all dangerous non-laser boss/miniboss attacks to the shared warning rule. Covered families now include the Stage-2 Inferno Reaver nine-lane shotgun fan, Stage-5 Chrome Hammer Archmage vertical boomerang, committed spiked-ball launch and fused mega-wave corridor, Stage-6 Doomsday Carrier twin-battery cyclone fan, alternating storm-node fans, four-barrel prism crossfire, paired gravity mines, accelerating omega bombs, mirrored cluster fan, chrome flak fan and Thunderhead, Stage-7 DUAL SCOOP DREDGER minefield and Toxic Portal Warden cripple-phase rail groups, Stage-8 BLACK COCOON crescent wall, RAVENOUS ASCENDANT five-needle fan, ABYSSAL LEVIATHAN nine-lane solar wheel, FURIOUS DEATH seven-gunship fan and four-lane straight-missile salvo, Stage-9 Event Horizon, independent Warp Sentinel radial/aimed volleys, and every row of the Tidal Sovereign cascade; remaining encounter families need review.

## Complex encounter choreography

8. **S3-10 · Pending** — Hard boss: Juggernaut-like dash with authored charge effects, fluid circular return and persistent hull-shaped shadow. Dependency: SpriteCook.
9. **S3-12 · Partial** — Furious Rime Wall: enlarged blue laser with matching Simon-Says warning is integrated; black/blue hull palette and full Hard-pattern parity remain. Dependency: SpriteCook.
10. **S2-08 · Partial** — Missile-sequence head fight is recorded as a design note; distinct Super Missile Box and encounter sequence remain to be built.

## Largest asset, mode and full-stage passes

11. **SPACE-12 · Partial** — New ship and flight reels integrated. Twelve large solid top-view components rise from below individually with sound, then rotate and orbit without fades or mirrored perspective tricks. Remaining: flight-reel silhouette/wingspan consistency and exact final component fit.
12. **PRE-10 · Partial** — Existing ship used in space, pilot palettes, transformation and space death/roll support have proof; the later replacement concept and complete new frame set are still pending.
13. **ENG-14 · Partial** — All pilots retain barrel roll and somersault access; existing ground/space support is present, but full nine-pilot regression and the replacement ship frames remain.
14. **S4-08 · Pending** — Furious third helper: elite black camo, opaque black/white Maverick-style ball with glowing blue charge growth. Dependency: SpriteCook.
15. **S4-09 · Pending** — Dark Chromium attack: fade darker, shatter/disintegrate the ball into dual rotating energy flames with appropriate sounds. Dependency: SpriteCook.
16. **S4-10 · Pending** — Dark Chromium lethal hit: explicitly requested ship-disintegration death and sound; preserve ordinary burn/spin/crash deaths elsewhere. Dependency: SpriteCook.
17. **ACH-14 · Pending** — Wire playable Boss Rush and Time Attack behind their real unlock condition; do not fake a final campaign clear.
18. **SPACE-06 · Partial** — Stage 5 full enemy/projectile/boss balance round: first readability fixes have proof; full natural-play review with Mike remains.
19. **SPACE-07 · Pending** — Stage 6 full enemy/projectile behavior cleanup round with Mike; separate from the completed Tempest/Retina work.
20. **SPACE-08 · Partial** — Stage 7 full enemy/projectile behavior cleanup round with Mike. First Warden hyper chaingun and leg-strike leap pass is integrated; natural-play balance and the wider stage remain.
21. **SPACE-09 · Pending** — Stage 8 full enemy/projectile behavior cleanup round with Mike.
22. **SPACE-10 · Pending** — Stage 9 full enemy/projectile behavior cleanup round with Mike.

## Broad asset and engine conversion

23. **ENG-21 · Pending** — Complete a vehicle-wide authored direction-frame audit for all remaining tanks and jets; remove live canvas rotation where it produces warped or wonky turns, while retaining correct pivots, shadows and weapon mounts.

## Largest asset, mode and full-stage passes

24. **PRE-11 · Partial** — Build short, readable Campaign transition scenes with two or three existing pilots, top-down ships, front-facing portraits, and cockpit/POV dialogue where the story supports them.

## Shared systems and progression

25. **ENG-24 · Partial** — Create and audition a full ElevenLabs plus ColeForge sound pass for every forged weapon combination, miniboss, boss, enemy projectile, fire hazard and shield destruction. A 20-cue local ColeForge bank is integrated; ElevenLabs and remaining encounter voices need finishing. Dependency: ElevenLabs key.

Full completed list and evidence: [request checklist](REQUEST_CHECKLIST_0914.md).
