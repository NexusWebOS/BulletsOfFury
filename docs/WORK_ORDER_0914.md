# Bullets of Fury — easiest-to-hardest work order

**139 entries: 62 complete / 10 partial / 67 pending.**

Work in ascending workOrder, an estimate of implementation plus verification difficulty. Respect prerequisites and skip externally blocked items while continuing ready work. Re-rank when investigation changes the estimate; retain IDs and explain the change.

Completed entries are excluded. The list below contains every unfinished item exactly once. Partial items retain that status. Difficulty bands are estimates, not promises that an unchecked feature already works. Asset/naming dependencies can be skipped until available.

## Small changes and focused checks

1. **UI-09 · Pending** — Pilot-select words reveal letter-by-letter and stat bars fill left-to-right.
2. **UI-08 · Pending** — Pilot select fills the screen rather than the old 640x480 presentation.
3. **ACH-09 · Pending** — Boss-fight timer in upper right, 00:00 format, correct pause/entry/death lifecycle.

## Moderate presentation and behavior work

4. **ENG-03 · Partial** — Reusable horizontal gliding/follow helper exists; integrate and verify it in the requested encounters.
5. **S3-05 · Pending** — Miniboss baseline: more aggressive, player-X-aligned return and horizontal following until laser commitment.
6. **S1-07 · Pending** — Jungle chopper: remove erratic motion while retaining the approved attack patterns.
7. **S1-08 · Partial** — Chopper rotor bed exists; obtain and tune the requested proper helicopter/propeller sound through the available sound engine or ElevenLabs.
8. **UI-10 · Pending** — Pilot-select ship animation: onion-align and center every rotation frame.
9. **UI-07 · Pending** — Title/intro silhouettes: all nine front-facing pilots beside their ships, scrolling from Cole through the remaining roster.
10. **UI-06 · Pending** — Generate any missing dedicated pause/menu bitmap buttons; current pause uses existing authored font/cursor and game UI chrome. Dependency: SpriteCook.
11. **MODE-08 · Pending** — Regenerate Life Up and create Continue Up pickup art matching Bullets of Fury through SpriteCook. Dependency: SpriteCook.
12. **MSL-08 · Pending** — Generate matching Super/Ultra/Uber upgrade icons and ammo boxes, including the distinct Super Missile Box. Dependency: SpriteCook.
13. **ACH-12 · Pending** — New-game menu order: Campaign, Arcade, Co-op, Boss Rush, Time Attack, with missing mode buttons generated. Dependency: SpriteCook.
14. **S4-16 · Pending** — Authored left/right escape arrows: flipped pair, flashing with synchronized warning sounds for the giant strike. Dependency: SpriteCook.

## Shared systems and progression

15. **MODE-01 · Partial** — Arcade mirrors the same encounters without campaign map/cutscenes; core start flow exists and Stage-9 credit fallback is now excluded, but all transition routes still need a parity audit.
16. **ENG-06 · Partial** — Tap Retina targets known live boss parts, nodes and helpers, excluding protected hulls; complete the remaining encounter/weapon-router audit.
17. **ENG-12 · Pending** — Shared elemental absorption: fire absorbs 50% fire damage and ice absorbs ice, with matching absorbed-damage popup text.
18. **ENG-13 · Pending** — Shared elemental weakness: fire deals 2x to ice and ice 2x to fire across relevant enemy, boss, helper and shield routes.
19. **ENG-11 · Pending** — Shared enemy shield break/stun: dizzy levitation/spin and bounded splash damage, reusing authored boss/helper effects.
20. **MODE-04 · Pending** — Hard enemies and shields get +15% HP across Campaign and Arcade, with explicit encounter-specific modifiers applied consistently.
21. **S2-02 · Pending** — Lava/magma fodder: tougher hulls and weak breakable shields using the shared stun/break system.
22. **S2-07 · Pending** — Hard miniboss and boss: additional 25% HP and 50% fire absorption using the shared elemental rules.
23. **ENG-05 · Pending** — No default enemy dies to a single hit: consistent damage accounting across ordinary enemies, pieces, shields and high-damage weapons.
24. **MSL-04 · Pending** — Manual tier damage/size progression: Standard -> Super x1.25 -> Ultra x1.5625 -> Uber x1.953125; keep passive missiles separate.
25. **MSL-05 · Pending** — Hard ammo caps: Super 50, Ultra 35, Uber 20 across every pickup, save/load and firing route.
26. **MSL-06 · Pending** — Tier acquisition replaces current manual missile; death resets to Standard.
27. **MSL-07 · Pending** — Ultra eligibility requires Super plus survival until the next spawn wave; Uber requires the same after Ultra.
28. **ACH-01 · Pending** — Persistent once-per-profile/account achievement registry, points and future Steam mapping.
29. **ACH-02 · Pending** — Achievement menu/button and bottom-center unlock notification that slides/fades downward. Dependency: SpriteCook.
30. **ACH-03 · Pending** — Nine Campaign Clear - <Pilot> achievements for Campaign or Arcade completion, 100 points each.
31. **ACH-04 · Pending** — Each stage cleared on Normal or above: 10 points.
32. **ACH-05 · Pending** — Each stage on Normal or above without losing a life: 200 points.
33. **ACH-07 · Pending** — Each stage without firing a manual missile: 100 points, unlock once per profile.
34. **ACH-08 · Pending** — Each weapon maxed to level 5: its own 20-point achievement.
35. **ACH-10 · Pending** — Stage-1 boss/miniboss speed awards: under two minutes 200 points; under one minute 500. Stacking policy not yet settled.
36. **ACH-06 · Pending** — Entire game without spending a continue: 1000 points plus a generated trophy avatar. Dependency: SpriteCook.
37. **ACH-11 · Pending** — Hard boss victories: individual 200-point achievements; Furious victories: 500 points each.
38. **ACH-13 · Pending** — Boss Rush/Time Attack gray chain-and-lock presentation using Nexus II art, denial sound on selection, unlock only on final campaign clear.
39. **ENG-15 · Pending** — HUD incoming-lock indicator above Equipped: gray idle, red flashing and distance-accelerated beeps until evasion or hit. Dependency: SpriteCook.
40. **ENG-02 · Partial** — Migrate all dangerous non-laser boss/miniboss attacks to the shared warning rule; laser families are covered.

## Complex encounter choreography

41. **S1-10 · Pending** — Chopper introduction: boss bar fades in, fills left-to-right with repeated existing chimes; fight/music start after filling.
42. **S1-09 · Pending** — Dam entrance: fly up from below above the player, whole-frame shadow, quick whip spin into position.
43. **S1-12 · Pending** — Chopper pass warning: eight synchronized red flashes/beeps, then committed fast but reactable charge with a shooting window.
44. **S1-11 · Pending** — Below 50%: frenzy plus four alternating down/up passes across distinct lanes; passes two and four rain bullets.
45. **S2-06 · Pending** — Furnace rollerball: slow-to-medium-to-fast-to-super-fast spin and accelerating horizontal travel, dodgeable by roll/somersault.
46. **S3-06 · Pending** — Miniboss laser: darken screen, crackling lightning charge and laser sounds; widen 25%, sweep across the viewport with the intended diagonal escape route.
47. **S3-08 · Pending** — Hard/Furious miniboss: player Retina lock, charged shootable spiral rocket volley alternating left/right.
48. **S3-09 · Pending** — Furious miniboss: combine rockets with a late committed charge into the player.
49. **S2-09 · Pending** — Generate improved authored Furnace giant-beam graphics that also support the Stage-3 Furious palette variant. Dependency: SpriteCook.
50. **S3-10 · Pending** — Hard boss: Juggernaut-like dash with authored charge effects, fluid circular return and persistent hull-shaped shadow. Dependency: SpriteCook.
51. **S3-11 · Pending** — Hard boss below 50%: double laser firing and shootable homing laser balls; evade by leaving the screen or breaking lock with roll/somersault.
52. **S3-13 · Pending** — Furious cannon feints: faster Simon-Says sequencing, yellow/red/yellow/red/red-flash then fire; no green and no overhead asterisk only on Furious.
53. **S3-12 · Pending** — Furious boss: black/blue palette and all Hard patterns, plus giant beam derived from the improved Furnace art. Dependency: SpriteCook.
54. **S4-06 · Pending** — Hard Warden: rapid turret spreads/center flurries plus circular/glide/charge/shake ramming sequence.
55. **MODE-05 · Pending** — Hard/Furious elite duplicates: authored palette variations, shields and capable aggressive fighter behavior; Furious more demanding.
56. **MODE-07 · Pending** — Continue Up reward in all modes for qualifying deathless sections, or Hard/Furious elite kills; enforce defined reward eligibility.
57. **S4-07 · Pending** — Warden helpers: two on Hard, three on Furious; matching palettes, shielded stationary MG fighter and aggressive player-like missile protector.
58. **S4-11 · Pending** — Hard/Furious Sovereign helpers: 50% more shield HP, faster straight/diagonal attacks and forward horizontal blocking row.
59. **S4-12 · Pending** — Generator hit enrages helpers red with an asterisk; move to screen sides and face player for 5-7 seconds of staggered rapid streams with traversable gaps.
60. **S4-13 · Pending** — Enraged helpers react to generator damage with limited upward/backward tracking, preserving the edge-hugging/spider-walk dodge route.
61. **S4-14 · Pending** — Hard Sovereign chain lightning: double and widen with extra projectiles; Furious faster/wider and more frequent lightning balls.
62. **S4-15 · Pending** — Furious Sovereign giant lightning strike: five-second charge, yellow/red FOV, red flash, darkened screen/crackling core; bottom corners remain safe.
63. **S1-05 · Pending** — Hard Razorback: fight two simultaneously.
64. **S1-06 · Pending** — Furious Razorback: 50% larger, Furious palette, hyper tank behavior and Furious sonic waves.
65. **S2-08 · Partial** — Missile-sequence head fight is recorded as a design note; distinct Super Missile Box and encounter sequence remain to be built.

## Largest asset, mode and full-stage passes

66. **SPACE-12 · Partial** — New ship and flight reels integrated. Twelve large solid top-view components rise from below individually with sound, then rotate and orbit without fades or mirrored perspective tricks. Remaining: flight-reel silhouette/wingspan consistency and exact final component fit.
67. **PRE-10 · Partial** — Existing ship used in space, pilot palettes, transformation and space death/roll support have proof; the later replacement concept and complete new frame set are still pending.
68. **ENG-14 · Partial** — All pilots retain barrel roll and somersault access; existing ground/space support is present, but full nine-pilot regression and the replacement ship frames remain.
69. **S4-08 · Pending** — Furious third helper: elite black camo, opaque black/white Maverick-style ball with glowing blue charge growth. Dependency: SpriteCook.
70. **S4-09 · Pending** — Dark Chromium attack: fade darker, shatter/disintegrate the ball into dual rotating energy flames with appropriate sounds. Dependency: SpriteCook.
71. **S4-10 · Pending** — Dark Chromium lethal hit: explicitly requested ship-disintegration death and sound; preserve ordinary burn/spin/crash deaths elsewhere. Dependency: SpriteCook.
72. **ACH-14 · Pending** — Wire playable Boss Rush and Time Attack behind their real unlock condition; do not fake a final campaign clear.
73. **SPACE-06 · Partial** — Stage 5 full enemy/projectile/boss balance round: first readability fixes have proof; full natural-play review with Mike remains.
74. **SPACE-07 · Pending** — Stage 6 full enemy/projectile behavior cleanup round with Mike; separate from the completed Tempest/Retina work.
75. **SPACE-08 · Pending** — Stage 7 full enemy/projectile behavior cleanup round with Mike.
76. **SPACE-09 · Pending** — Stage 8 full enemy/projectile behavior cleanup round with Mike.
77. **SPACE-10 · Pending** — Stage 9 full enemy/projectile behavior cleanup round with Mike.

Full completed list and evidence: [request checklist](REQUEST_CHECKLIST_0914.md).
