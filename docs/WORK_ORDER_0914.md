# Bullets of Fury — easiest-to-hardest work order

**148 entries: 79 complete / 8 partial / 61 pending.**

Work in ascending workOrder, an estimate of implementation plus verification difficulty. Respect prerequisites and skip externally blocked items while continuing ready work. Re-rank when investigation changes the estimate; retain IDs and explain the change.

Completed entries are excluded. The list below contains every unfinished item exactly once. Partial items retain that status. Difficulty bands are estimates, not promises that an unchecked feature already works. Asset/naming dependencies can be skipped until available.

## Current boss brief — awaiting Stage 2 identity

1. **S2-10 · Pending** — Accelerating screaming head frames and shrieks/shake; two fire-ring X cycles; final white flash, absent boss and residual explosions. Dependency: Mike: Stage 2 boss identity.
2. **S2-11 · Pending** — Continue scrolling after defeat; RNG different-pilot dialogue addressing the player about the assimilated military mech. Dependency: S2-10.

## Moderate presentation and behavior work

3. **MODE-08 · Pending** — Regenerate Life Up and create Continue Up pickup art matching Bullets of Fury through SpriteCook. Dependency: SpriteCook.
4. **MSL-08 · Pending** — Generate matching Super/Ultra/Uber upgrade icons and ammo boxes, including the distinct Super Missile Box. Dependency: SpriteCook.
5. **ACH-12 · Pending** — New-game menu order: Campaign, Arcade, Co-op, Boss Rush, Time Attack, with missing mode buttons generated. Dependency: SpriteCook.
6. **S4-16 · Pending** — Authored left/right escape arrows: flipped pair, flashing with synchronized warning sounds for the giant strike. Dependency: SpriteCook.

## Shared systems and progression

7. **MODE-01 · Partial** — Arcade mirrors the same encounters without campaign map/cutscenes; core start flow exists and Stage-9 credit fallback is now excluded, but all transition routes still need a parity audit.
8. **ENG-06 · Partial** — Tap Retina targets known live boss parts, nodes and helpers, excluding protected hulls; complete the remaining encounter/weapon-router audit.
9. **ENG-12 · Pending** — Shared elemental absorption: fire absorbs 50% fire damage and ice absorbs ice, with matching absorbed-damage popup text.
10. **ENG-13 · Pending** — Shared elemental weakness: fire deals 2x to ice and ice 2x to fire across relevant enemy, boss, helper and shield routes.
11. **ENG-11 · Pending** — Shared enemy shield break/stun: dizzy levitation/spin and bounded splash damage, reusing authored boss/helper effects.
12. **MODE-04 · Pending** — Hard enemies and shields get +15% HP across Campaign and Arcade, with explicit encounter-specific modifiers applied consistently.
13. **S2-02 · Pending** — Lava/magma fodder: tougher hulls and weak breakable shields using the shared stun/break system.
14. **S2-07 · Pending** — Hard miniboss and boss: additional 25% HP and 50% fire absorption using the shared elemental rules.
15. **ENG-05 · Pending** — No default enemy dies to a single hit: consistent damage accounting across ordinary enemies, pieces, shields and high-damage weapons.
16. **MSL-04 · Pending** — Manual tier damage/size progression: Standard -> Super x1.25 -> Ultra x1.5625 -> Uber x1.953125; keep passive missiles separate.
17. **MSL-05 · Pending** — Hard ammo caps: Super 50, Ultra 35, Uber 20 across every pickup, save/load and firing route.
18. **MSL-06 · Pending** — Tier acquisition replaces current manual missile; death resets to Standard.
19. **MSL-07 · Pending** — Ultra eligibility requires Super plus survival until the next spawn wave; Uber requires the same after Ultra.
20. **ACH-01 · Pending** — Persistent once-per-profile/account achievement registry, points and future Steam mapping.
21. **ACH-02 · Pending** — Achievement menu/button and bottom-center unlock notification that slides/fades downward. Dependency: SpriteCook.
22. **ACH-03 · Pending** — Nine Campaign Clear - <Pilot> achievements for Campaign or Arcade completion, 100 points each.
23. **ACH-04 · Pending** — Each stage cleared on Normal or above: 10 points.
24. **ACH-05 · Pending** — Each stage on Normal or above without losing a life: 200 points.
25. **ACH-07 · Pending** — Each stage without firing a manual missile: 100 points, unlock once per profile.
26. **ACH-08 · Pending** — Each weapon maxed to level 5: its own 20-point achievement.
27. **ACH-10 · Pending** — Stage-1 boss/miniboss speed awards: under two minutes 200 points; under one minute 500. Stacking policy not yet settled.
28. **ACH-06 · Pending** — Entire game without spending a continue: 1000 points plus a generated trophy avatar. Dependency: SpriteCook.
29. **ACH-11 · Pending** — Hard boss victories: individual 200-point achievements; Furious victories: 500 points each.
30. **ACH-13 · Pending** — Boss Rush/Time Attack gray chain-and-lock presentation using Nexus II art, denial sound on selection, unlock only on final campaign clear.
31. **ENG-15 · Pending** — HUD incoming-lock indicator above Equipped: gray idle, red flashing and distance-accelerated beeps until evasion or hit. Dependency: SpriteCook.
32. **ENG-02 · Partial** — Migrate all dangerous non-laser boss/miniboss attacks to the shared warning rule; laser families are covered.

## Complex encounter choreography

33. **S1-10 · Pending** — Chopper introduction: boss bar fades in, fills left-to-right with repeated existing chimes; fight/music start after filling.
34. **S1-09 · Pending** — Dam entrance: fly up from below above the player, whole-frame shadow, quick whip spin into position.
35. **S1-12 · Pending** — Chopper pass warning: eight synchronized red flashes/beeps, then committed fast but reactable charge with a shooting window.
36. **S1-11 · Pending** — Below 50%: frenzy plus four alternating down/up passes across distinct lanes; passes two and four rain bullets.
37. **S2-06 · Pending** — Furnace rollerball: slow-to-medium-to-fast-to-super-fast spin and accelerating horizontal travel, dodgeable by roll/somersault.
38. **S3-06 · Pending** — Miniboss laser: darken screen, crackling lightning charge and laser sounds; widen 25%, sweep across the viewport with the intended diagonal escape route.
39. **S3-08 · Pending** — Hard/Furious miniboss: player Retina lock, charged shootable spiral rocket volley alternating left/right.
40. **S3-09 · Pending** — Furious miniboss: combine rockets with a late committed charge into the player.
41. **S2-09 · Pending** — Generate improved authored Furnace giant-beam graphics that also support the Stage-3 Furious palette variant. Dependency: SpriteCook.
42. **S3-10 · Pending** — Hard boss: Juggernaut-like dash with authored charge effects, fluid circular return and persistent hull-shaped shadow. Dependency: SpriteCook.
43. **S3-11 · Pending** — Hard boss below 50%: double laser firing and shootable homing laser balls; evade by leaving the screen or breaking lock with roll/somersault.
44. **S3-13 · Pending** — Furious cannon feints: faster Simon-Says sequencing, yellow/red/yellow/red/red-flash then fire; no green and no overhead asterisk only on Furious.
45. **S3-12 · Pending** — Furious boss: black/blue palette and all Hard patterns, plus giant beam derived from the improved Furnace art. Dependency: SpriteCook.
46. **S4-06 · Pending** — Hard Warden: rapid turret spreads/center flurries plus circular/glide/charge/shake ramming sequence.
47. **MODE-05 · Pending** — Hard/Furious elite duplicates: authored palette variations, shields and capable aggressive fighter behavior; Furious more demanding.
48. **MODE-07 · Pending** — Continue Up reward in all modes for qualifying deathless sections, or Hard/Furious elite kills; enforce defined reward eligibility.
49. **S4-07 · Pending** — Warden helpers: two on Hard, three on Furious; matching palettes, shielded stationary MG fighter and aggressive player-like missile protector.
50. **S4-11 · Pending** — Hard/Furious Sovereign helpers: 50% more shield HP, faster straight/diagonal attacks and forward horizontal blocking row.
51. **S4-12 · Pending** — Generator hit enrages helpers red with an asterisk; move to screen sides and face player for 5-7 seconds of staggered rapid streams with traversable gaps.
52. **S4-13 · Pending** — Enraged helpers react to generator damage with limited upward/backward tracking, preserving the edge-hugging/spider-walk dodge route.
53. **S4-14 · Pending** — Hard Sovereign chain lightning: double and widen with extra projectiles; Furious faster/wider and more frequent lightning balls.
54. **S4-15 · Pending** — Furious Sovereign giant lightning strike: five-second charge, yellow/red FOV, red flash, darkened screen/crackling core; bottom corners remain safe.
55. **S1-05 · Pending** — Hard Razorback: fight two simultaneously.
56. **S1-06 · Pending** — Furious Razorback: 50% larger, Furious palette, hyper tank behavior and Furious sonic waves.
57. **S2-08 · Partial** — Missile-sequence head fight is recorded as a design note; distinct Super Missile Box and encounter sequence remain to be built.

## Largest asset, mode and full-stage passes

58. **SPACE-12 · Partial** — New ship and flight reels integrated. Twelve large solid top-view components rise from below individually with sound, then rotate and orbit without fades or mirrored perspective tricks. Remaining: flight-reel silhouette/wingspan consistency and exact final component fit.
59. **PRE-10 · Partial** — Existing ship used in space, pilot palettes, transformation and space death/roll support have proof; the later replacement concept and complete new frame set are still pending.
60. **ENG-14 · Partial** — All pilots retain barrel roll and somersault access; existing ground/space support is present, but full nine-pilot regression and the replacement ship frames remain.
61. **S4-08 · Pending** — Furious third helper: elite black camo, opaque black/white Maverick-style ball with glowing blue charge growth. Dependency: SpriteCook.
62. **S4-09 · Pending** — Dark Chromium attack: fade darker, shatter/disintegrate the ball into dual rotating energy flames with appropriate sounds. Dependency: SpriteCook.
63. **S4-10 · Pending** — Dark Chromium lethal hit: explicitly requested ship-disintegration death and sound; preserve ordinary burn/spin/crash deaths elsewhere. Dependency: SpriteCook.
64. **ACH-14 · Pending** — Wire playable Boss Rush and Time Attack behind their real unlock condition; do not fake a final campaign clear.
65. **SPACE-06 · Partial** — Stage 5 full enemy/projectile/boss balance round: first readability fixes have proof; full natural-play review with Mike remains.
66. **SPACE-07 · Pending** — Stage 6 full enemy/projectile behavior cleanup round with Mike; separate from the completed Tempest/Retina work.
67. **SPACE-08 · Pending** — Stage 7 full enemy/projectile behavior cleanup round with Mike.
68. **SPACE-09 · Pending** — Stage 8 full enemy/projectile behavior cleanup round with Mike.
69. **SPACE-10 · Pending** — Stage 9 full enemy/projectile behavior cleanup round with Mike.

Full completed list and evidence: [request checklist](REQUEST_CHECKLIST_0914.md).
