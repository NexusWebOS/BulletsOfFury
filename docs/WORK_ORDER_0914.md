# Bullets of Fury — easiest-to-hardest work order

**169 entries: 133 complete / 7 partial / 29 pending.**

Work in ascending workOrder, an estimate of implementation plus verification difficulty. Respect prerequisites and skip externally blocked items while continuing ready work. Re-rank when investigation changes the estimate; retain IDs and explain the change.

Completed entries are excluded. The list below contains every unfinished item exactly once. Partial items retain that status. Difficulty bands are estimates, not promises that an unchecked feature already works. Asset/naming dependencies can be skipped until available.

## Small changes and focused checks

1. **UI-18 · Pending** — Stage-clear screen: keep achievement notices and Fury Point conversion clear of the sign-off, password and Continue areas at every supported aspect ratio.

## Moderate presentation and behavior work

2. **UI-19 · Pending** — Loadout arsenal: add D-pad/controller paging with generated control prompts and stronger selected-row/combination glow before equipping.
3. **UI-20 · Pending** — Pilot Select: restore the deliberate arcade reveal sequence so identity and affiliation type first, then each stat bar fills separately with synchronized sounds; preserve the clean GOOD LUCK pilot-and-ship launch card.

## Shared systems and progression

4. **ENG-19 · Pending** — Respawn safety: clear or neutralize lethal lower-screen patterns and preserve a readable invulnerability window so a death cannot immediately chain into another.

## Complex encounter choreography

5. **S1-14 · Pending** — Hard Razorback Duo: prevent overlapping sonic releases, missile locks and recovery windows from creating unavoidable stacked patterns while preserving the two-tank challenge.
6. **S1-15 · Pending** — Furious Razorback: retune consecutive retina rocket salvos and distinguish red warnings, projectiles, explosions and armor during peak attack density.

## Shared systems and progression

7. **ENG-20 · Pending** — Hard/Furious hazard readability: separate warning, hostile projectile, explosion and enemy-palette values when several red effects overlap.

## Small changes and focused checks

8. **S1-16 · Pending** — Razorback early-turret hit feedback: flash the targetable central turret white during the machine-gun phase and keep destroyed-part feedback local to the struck module.
9. **UI-21 · Pending** — Stats accuracy and fit: correct the BULLETS FIRED metric/value mismatch and keep long labels and values inside their authored bays.

## Moderate presentation and behavior work

10. **S1-17 · Pending** — Give the Hard Razorback Duo readable per-tank condition/target feedback in addition to the combined encounter bar so the player can identify which tank is close to breaking.
11. **S1-18 · Pending** — Replace the temporary low-passed shared engine loop with a dedicated tracked-tank tread/roller recording and verify movement start, stop and dual-tank ownership.
12. **UI-22 · Pending** — Loadout catalog readability: enlarge or page the combination cells and display the selected combination name/price/state so opacity alone is not the only locked/unlocked cue.
13. **UI-23 · Pending** — Pilot Select completeness: warm ship/emblem art before the screen appears and restore callsign, role/special and biography detail without contaminating the clean GOOD LUCK launch card.

## Current boss brief — awaiting Stage 2 identity

14. **S2-10 · Pending** — Accelerating screaming head frames and shrieks/shake; two fire-ring X cycles; final white flash, absent boss and residual explosions. Dependency: Mike: Stage 2 boss identity.
15. **S2-11 · Pending** — Continue scrolling after defeat; RNG different-pilot dialogue addressing the player about the assimilated military mech. Dependency: S2-10.

## Moderate presentation and behavior work

16. **S4-16 · Pending** — Authored left/right escape arrows: flipped pair, flashing with synchronized warning sounds for the giant strike. Dependency: SpriteCook.

## Shared systems and progression

17. **ACH-02 · Pending** — Achievement menu/button and bottom-center unlock notification that slides/fades downward. Dependency: SpriteCook.
18. **ACH-06 · Partial** — Entire game without spending a continue: 1000 points plus a generated trophy avatar. Award trigger is complete; SpriteCook trophy avatar remains. Dependency: SpriteCook.
19. **ENG-15 · Pending** — HUD incoming-lock indicator above Equipped: gray idle, red flashing and distance-accelerated beeps until evasion or hit. Dependency: SpriteCook.
20. **ENG-02 · Partial** — Migrate all dangerous non-laser boss/miniboss attacks to the shared warning rule. Covered families now include the Stage-2 Inferno Reaver nine-lane shotgun fan, Stage-5 Chrome Hammer Archmage vertical boomerang, committed spiked-ball launch and fused mega-wave corridor, Stage-6 Doomsday Carrier twin-battery cyclone fan, alternating storm-node fans, four-barrel prism crossfire, paired gravity mines, accelerating omega bombs, mirrored cluster fan, chrome flak fan and Thunderhead, Stage-7 DUAL SCOOP DREDGER minefield and Toxic Portal Warden cripple-phase rail groups, Stage-8 BLACK COCOON crescent wall, RAVENOUS ASCENDANT five-needle fan, ABYSSAL LEVIATHAN nine-lane solar wheel, FURIOUS DEATH seven-gunship fan and four-lane straight-missile salvo, Stage-9 Event Horizon, independent Warp Sentinel radial/aimed volleys, and every row of the Tidal Sovereign cascade; remaining encounter families need review.

## Complex encounter choreography

21. **S2-09 · Pending** — Generate improved authored Furnace giant-beam graphics that also support the Stage-3 Furious palette variant. Dependency: SpriteCook.
22. **S3-10 · Pending** — Hard boss: Juggernaut-like dash with authored charge effects, fluid circular return and persistent hull-shaped shadow. Dependency: SpriteCook.
23. **S3-12 · Pending** — Furious boss: black/blue palette and all Hard patterns, plus giant beam derived from the improved Furnace art. Dependency: SpriteCook.
24. **S2-08 · Partial** — Missile-sequence head fight is recorded as a design note; distinct Super Missile Box and encounter sequence remain to be built.

## Largest asset, mode and full-stage passes

25. **SPACE-12 · Partial** — New ship and flight reels integrated. Twelve large solid top-view components rise from below individually with sound, then rotate and orbit without fades or mirrored perspective tricks. Remaining: flight-reel silhouette/wingspan consistency and exact final component fit.
26. **PRE-10 · Partial** — Existing ship used in space, pilot palettes, transformation and space death/roll support have proof; the later replacement concept and complete new frame set are still pending.
27. **ENG-14 · Partial** — All pilots retain barrel roll and somersault access; existing ground/space support is present, but full nine-pilot regression and the replacement ship frames remain.
28. **S4-08 · Pending** — Furious third helper: elite black camo, opaque black/white Maverick-style ball with glowing blue charge growth. Dependency: SpriteCook.
29. **S4-09 · Pending** — Dark Chromium attack: fade darker, shatter/disintegrate the ball into dual rotating energy flames with appropriate sounds. Dependency: SpriteCook.
30. **S4-10 · Pending** — Dark Chromium lethal hit: explicitly requested ship-disintegration death and sound; preserve ordinary burn/spin/crash deaths elsewhere. Dependency: SpriteCook.
31. **ACH-14 · Pending** — Wire playable Boss Rush and Time Attack behind their real unlock condition; do not fake a final campaign clear.
32. **SPACE-06 · Partial** — Stage 5 full enemy/projectile/boss balance round: first readability fixes have proof; full natural-play review with Mike remains.
33. **SPACE-07 · Pending** — Stage 6 full enemy/projectile behavior cleanup round with Mike; separate from the completed Tempest/Retina work.
34. **SPACE-08 · Pending** — Stage 7 full enemy/projectile behavior cleanup round with Mike.
35. **SPACE-09 · Pending** — Stage 8 full enemy/projectile behavior cleanup round with Mike.
36. **SPACE-10 · Pending** — Stage 9 full enemy/projectile behavior cleanup round with Mike.

Full completed list and evidence: [request checklist](REQUEST_CHECKLIST_0914.md).
