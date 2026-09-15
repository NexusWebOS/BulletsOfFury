# Bullets of Fury — request checklist

Updated 2026-09-15. **148 entries: 79 complete / 8 partial / 61 pending.**

**69 remain unfinished.** 13 depend on SpriteCook production assets; 0 needs a model-name decision. These are included in the totals.

Consolidated requests in this conversation; superseded variants folded into the latest request. Rows count deliverables, not effort or percent of development time.

Complete gameplay entries mean implementation and recorded native-browser proof. Source-identification entries mean the approved file was located and visually inspected; they do not certify asset production or integration. Evidence records the checked version and limitations; earlier scenes are not all re-recorded in each batch. Partial means a limited pass exists and the remaining work is stated. Unchecked rows are unfinished.

Detailed specifications: [original request ledger](OVERNIGHT_REQUESTS_0914.md). Execution sequence: [easiest-to-hardest work order](WORK_ORDER_0914.md).

## Current batch and next work

Just verified: Stage 4 cinematic defeat and regenerated highway; playable SpriteCook Stage 5 transformer on Easy/Normal. Stage 2 identity answer still required; full difficulty balancing remains SPACE-06. [Proof](BOSS_BATCH_0915.md).

Work in ascending workOrder, an estimate of implementation plus verification difficulty. Respect prerequisites and skip externally blocked items while continuing ready work. Re-rank when investigation changes the estimate; retain IDs and explain the change.

Mike selected furyship_somersault_13.png and approved image_gen for its replacement family. The new ship, rolls, somersaults, parts, transition effects, all nine palettes and SPCBOY legacy selection are integrated. His latest assembly direction uses solid top views, rotation and individual bottom arrivals; perspective blending is superseded. SPACE-12 remains partial for flight silhouette/width consistency and exact component fit. The remaining encounter and feature queue is preserved.

## Tally by area

| Area | Complete | Partial | Pending | Total |
| --- | ---: | ---: | ---: | ---: |
| Earlier handoff, weapons and Tempest | 9 | 1 | 0 | 10 |
| Shared combat, warnings and targeting | 7 | 3 | 5 | 15 |
| Stage 1: fodder, Razorback and jungle chopper | 6 | 0 | 6 | 12 |
| Stage 2: lava enemies, Magma Ward and Furnace Tyrant | 4 | 1 | 6 | 11 |
| Stage 3: ice enemies, miniboss and Rime Wall | 7 | 0 | 7 | 14 |
| Stage 4: Olive Warden and Sovereign | 7 | 0 | 11 | 18 |
| Stages 5-9: space and encounter cleanup | 16 | 2 | 4 | 22 |
| Manual missile tiers and supplies | 4 | 0 | 5 | 9 |
| Pause, saving, title and pilot selection | 15 | 0 | 0 | 15 |
| Achievements, timers and unlockable modes | 1 | 0 | 13 | 14 |
| Arcade and shared difficulty rewards | 3 | 1 | 4 | 8 |

## Checklist

### Earlier handoff, weapons and Tempest

- [x] **PRE-01 · Complete** — Trailer end card: BUILT WITH THE ASSISTANCE OF AI & HUMAN TOOLS. [Evidence](qa/trailer_endcard_0913_validation.json).
- [x] **PRE-02 · Complete** — Tempest: two independent south-facing jets; red-to-green hit feedback, rapid turns/slides and charge/thrust sounds. [Evidence](TEMPEST_FIGHTER_0913.md).
- [x] **PRE-03 · Complete** — Tempest: face thrust direction, leave the entire screen and return with fluid flight. [Evidence](TEMPEST_RETURN_0913.md).
- [x] **PRE-04 · Complete** — Cole Sonic Boom: authored charge/release/contact visuals and dedicated sounds. [Evidence](WEAPON_FEEDBACK_0913.md).
- [x] **PRE-05 · Complete** — Juggernaut charge dash: visible anchored boost, motion and launch/landing sounds. [Evidence](WEAPON_FEEDBACK_0913.md).
- [x] **PRE-06 · Complete** — Juggernaut wrecking balls: ship-anchored chains, readable steel impacts and separate chain/hit sounds. [Evidence](WEAPON_FEEDBACK_0913.md).
- [x] **PRE-07 · Complete** — Laser Mist: emitter/split/impact visuals and sounds; preserve its 3-to-9-to-27 pattern. [Evidence](WEAPON_FEEDBACK_0913.md).
- [x] **PRE-08 · Complete** — Cole's silent middle nuclear detonation: separate impacts now each receive their sound. [Evidence](BUGFIX_0913.md).
- [x] **PRE-09 · Complete** — Razorback and rotated Tempest collision fixes: pellets and held lasers respect exposed parts and finite beam geometry. [Evidence](BUGFIX_0913.md).
- [ ] **PRE-10 · Partial** — Existing ship used in space, pilot palettes, transformation and space death/roll support have proof; the later replacement concept and complete new frame set are still pending. [Evidence](proofs/spaceship_0913a/report.json).

### Shared combat, warnings and targeting

- [x] **ENG-01 · Complete** — Shared laser-family warning: three-second green/yellow/red FOV charge with overhead alert. [Evidence](qa/shared_laser_warnings_0914.json).
- [ ] **ENG-02 · Partial** — Migrate all dangerous non-laser boss/miniboss attacks to the shared warning rule; laser families are covered. [Evidence](READABLE_ATTACKS_0914.md).
- [x] **ENG-03 · Complete** — Shared bounded horizontal glide/follow integrated and verified in Frost Cruiser and Jungle chopper; later Warden choreography remains S4-06. [Evidence](MOVEMENT_BATCH_0914.md).
- [x] **ENG-04 · Complete** — Player flamethrower: 25% smaller draw and collision footprint, Fire Orb palette, nozzle remains connected. [Evidence](READABLE_ATTACKS_0914.md).
- [ ] **ENG-05 · Pending** — No default enemy dies to a single hit: consistent damage accounting across ordinary enemies, pieces, shields and high-damage weapons.
- [ ] **ENG-06 · Partial** — Tap Retina targets known live boss parts, nodes and helpers, excluding protected hulls; complete the remaining encounter/weapon-router audit. [Evidence](RETINA_TARGETS_0914.md).
- [x] **ENG-07 · Complete** — Stage-6 Retina: select electrical nodes and open bays while protected hull remains excluded; manual missiles damage the selected piece. [Evidence](RETINA_TARGETS_0914.md).
- [x] **ENG-08 · Complete** — Retina Scan upgrade: hold Retina and tap direction to acquire up to four distinct visible targets. [Evidence](RETINA_SCAN_0914.md).
- [x] **ENG-09 · Complete** — Multi-lock launch: manual missiles release sequentially at 50ms spacing, spending one ammo per actual launch. [Evidence](RETINA_SCAN_0914.md).
- [x] **ENG-10 · Complete** — Multi-lock lifecycle: five-second firing window, flashing expiry, death cancellation and pause freeze. [Evidence](RETINA_SCAN_0914.md).
- [ ] **ENG-11 · Pending** — Shared enemy shield break/stun: dizzy levitation/spin and bounded splash damage, reusing authored boss/helper effects.
- [ ] **ENG-12 · Pending** — Shared elemental absorption: fire absorbs 50% fire damage and ice absorbs ice, with matching absorbed-damage popup text.
- [ ] **ENG-13 · Pending** — Shared elemental weakness: fire deals 2x to ice and ice 2x to fire across relevant enemy, boss, helper and shield routes.
- [ ] **ENG-14 · Partial** — All pilots retain barrel roll and somersault access; existing ground/space support is present, but full nine-pilot regression and the replacement ship frames remain. [Evidence](proofs/spaceship_0913a/report.json).
- [ ] **ENG-15 · Pending** — HUD incoming-lock indicator above Equipped: gray idle, red flashing and distance-accelerated beeps until evasion or hit. Dependency: SpriteCook.

### Stage 1: fodder, Razorback and jungle chopper

- [x] **S1-01 · Complete** — Surviving fodder burns at half HP with animated fire/smoke; remove static damaged fire plates. [Evidence](STAGE_1_5_CORRECTIONS_0914.md).
- [x] **S1-02 · Complete** — Jet guns: remove the extra generic steering/spread volley; use authored straight twin guns/rocket sequence. [Evidence](READABLE_ATTACKS_0914.md).
- [x] **S1-03 · Complete** — Miniboss and boss weapon/charge sounds wired to their attacks. [Evidence](STAGE_1_5_CORRECTIONS_0914.md).
- [x] **S1-04 · Complete** — Razorback baseline: faster projectiles, sonic boom and movement. [Evidence](RAZORBACK_SPEED_0914.md).
- [ ] **S1-05 · Pending** — Hard Razorback: fight two simultaneously.
- [ ] **S1-06 · Pending** — Furious Razorback: 50% larger, Furious palette, hyper tank behavior and Furious sonic waves.
- [x] **S1-07 · Complete** — Jungle chopper pursuit and orbit transitions stabilized while retaining its attack patterns. [Evidence](MOVEMENT_BATCH_0914.md).
- [x] **S1-08 · Complete** — Chopper rotor bed exists; obtain and tune the requested proper helicopter/propeller sound through the available sound engine or ElevenLabs. [Evidence](ROTOR_AUDIO_0914.md).
- [ ] **S1-09 · Pending** — Dam entrance: fly up from below above the player, whole-frame shadow, quick whip spin into position.
- [ ] **S1-10 · Pending** — Chopper introduction: boss bar fades in, fills left-to-right with repeated existing chimes; fight/music start after filling.
- [ ] **S1-11 · Pending** — Below 50%: frenzy plus four alternating down/up passes across distinct lanes; passes two and four rain bullets.
- [ ] **S1-12 · Pending** — Chopper pass warning: eight synchronized red flashes/beeps, then committed fast but reactable charge with a shooting window.

### Stage 2: lava enemies, Magma Ward and Furnace Tyrant

- [x] **S2-01 · Complete** — Enemy projectile strips: use reviewed stable flight poses with pixel animation instead of misaligned growth frames. [Evidence](PROJECTILE_PIXEL_GLOW_0914.md).
- [ ] **S2-02 · Pending** — Lava/magma fodder: tougher hulls and weak breakable shields using the shared stun/break system.
- [x] **S2-03 · Complete** — Furnace head lasers: commit aim before release and provide a predictable dodge window. [Evidence](READABLE_ATTACKS_0914.md).
- [x] **S2-04 · Complete** — Furnace flamethrower: 25% wider visual and collision footprint. [Evidence](READABLE_ATTACKS_0914.md).
- [x] **S2-05 · Complete** — Furnace flame shield: use the actual authored flame shield from the first frame through every phase. [Evidence](ENCOUNTER_VISUAL_0914.md).
- [ ] **S2-06 · Pending** — Furnace rollerball: slow-to-medium-to-fast-to-super-fast spin and accelerating horizontal travel, dodgeable by roll/somersault.
- [ ] **S2-07 · Pending** — Hard miniboss and boss: additional 25% HP and 50% fire absorption using the shared elemental rules.
- [ ] **S2-08 · Partial** — Missile-sequence head fight is recorded as a design note; distinct Super Missile Box and encounter sequence remain to be built. [Evidence](OVERNIGHT_REQUESTS_0914.md).
- [ ] **S2-09 · Pending** — Generate improved authored Furnace giant-beam graphics that also support the Stage-3 Furious palette variant. Dependency: SpriteCook.
- [ ] **S2-10 · Pending** — Accelerating screaming head frames and shrieks/shake; two fire-ring X cycles; final white flash, absent boss and residual explosions. Dependency: Mike: Stage 2 boss identity. [Evidence](BOSS_BATCH_0915.md).
- [ ] **S2-11 · Pending** — Continue scrolling after defeat; RNG different-pilot dialogue addressing the player about the assimilated military mech. Dependency: S2-10. [Evidence](BOSS_BATCH_0915.md).

### Stage 3: ice enemies, miniboss and Rime Wall

- [x] **S3-01 · Complete** — Remove the ten boat spawns and store their definitions/assets for later use. [Evidence](STAGE3_STORED_BOATS_0914.json).
- [x] **S3-02 · Complete** — Ice-drone projectiles: larger visible dark-edged blue art over the snow. [Evidence](STAGE_1_5_CORRECTIONS_0914.md).
- [x] **S3-03 · Complete** — Rime Wall: beams originate only at the visible side cannon exits; middle uses a warned finite charge/pulse, not another full beam. [Evidence](READABLE_ATTACKS_0914.md).
- [x] **S3-04 · Complete** — Rime Wall beam palette: strong dark-blue rim, restrained light core readable over ice. [Evidence](qa/shared_laser_warnings_0914.json).
- [x] **S3-05 · Complete** — Frost Cruiser tracks sampled player X, returns from above on a committed vertical lane and follows horizontally until laser commitment. [Evidence](MOVEMENT_BATCH_0914.md).
- [ ] **S3-06 · Pending** — Miniboss laser: darken screen, crackling lightning charge and laser sounds; widen 25%, sweep across the viewport with the intended diagonal escape route.
- [x] **S3-07 · Complete** — Hard/Furious miniboss: black/royal-dark-blue palette and 35% larger hull. [Evidence](FROST_CRUISER_VARIANT_0914.md).
- [ ] **S3-08 · Pending** — Hard/Furious miniboss: player Retina lock, charged shootable spiral rocket volley alternating left/right.
- [ ] **S3-09 · Pending** — Furious miniboss: combine rockets with a late committed charge into the player.
- [ ] **S3-10 · Pending** — Hard boss: Juggernaut-like dash with authored charge effects, fluid circular return and persistent hull-shaped shadow. Dependency: SpriteCook.
- [ ] **S3-11 · Pending** — Hard boss below 50%: double laser firing and shootable homing laser balls; evade by leaving the screen or breaking lock with roll/somersault.
- [ ] **S3-12 · Pending** — Furious boss: black/blue palette and all Hard patterns, plus giant beam derived from the improved Furnace art. Dependency: SpriteCook.
- [ ] **S3-13 · Pending** — Furious cannon feints: faster Simon-Says sequencing, yellow/red/yellow/red/red-flash then fire; no green and no overhead asterisk only on Furious.
- [x] **S3-14 · Complete** — Frost Cruiser: missiles stay on wing turrets; nose shoots broad, tall Falva-style black/blue laser bolts with stable art and animated pixel glow. [Evidence](FROST_NOSE_LASER_0914.md).

### Stage 4: Olive Warden and Sovereign

- [x] **S4-01 · Complete** — Warden: remove blue chainguns; mounted spread machine guns, center dual straight guns and mounted rocket salvos with anchored flashes/sounds. [Evidence](STAGE_1_5_CORRECTIONS_0914.md).
- [x] **S4-02 · Complete** — Audit stage-4 apparent orange beams and upper rocket racks: short machine shots and mapped muzzle origins verified; long lines are road markings and racks belong to the authored whole Warden hull. [Evidence](ENCOUNTER_VISUAL_0914.md).
- [x] **S4-03 · Complete** — Sovereign helpers: stay outside the shield above each generator column. [Evidence](STAGE_1_5_CORRECTIONS_0914.md).
- [x] **S4-04 · Complete** — Wide piercing laser: hit/destroy both generator nodes in its column on the same tick and reach live helpers. [Evidence](STAGE_1_5_CORRECTIONS_0914.md).
- [x] **S4-05 · Complete** — Unpowered Sovereign: warned charge, fully offscreen exit, overhead hull/shadow pass and opposite-edge return. [Evidence](STAGE_1_5_CORRECTIONS_0914.md).
- [ ] **S4-06 · Pending** — Hard Warden: rapid turret spreads/center flurries plus circular/glide/charge/shake ramming sequence.
- [ ] **S4-07 · Pending** — Warden helpers: two on Hard, three on Furious; matching palettes, shielded stationary MG fighter and aggressive player-like missile protector.
- [ ] **S4-08 · Pending** — Furious third helper: elite black camo, opaque black/white Maverick-style ball with glowing blue charge growth. Dependency: SpriteCook.
- [ ] **S4-09 · Pending** — Dark Chromium attack: fade darker, shatter/disintegrate the ball into dual rotating energy flames with appropriate sounds. Dependency: SpriteCook.
- [ ] **S4-10 · Pending** — Dark Chromium lethal hit: explicitly requested ship-disintegration death and sound; preserve ordinary burn/spin/crash deaths elsewhere. Dependency: SpriteCook.
- [ ] **S4-11 · Pending** — Hard/Furious Sovereign helpers: 50% more shield HP, faster straight/diagonal attacks and forward horizontal blocking row.
- [ ] **S4-12 · Pending** — Generator hit enrages helpers red with an asterisk; move to screen sides and face player for 5-7 seconds of staggered rapid streams with traversable gaps.
- [ ] **S4-13 · Pending** — Enraged helpers react to generator damage with limited upward/backward tracking, preserving the edge-hugging/spider-walk dodge route.
- [ ] **S4-14 · Pending** — Hard Sovereign chain lightning: double and widen with extra projectiles; Furious faster/wider and more frequent lightning balls.
- [ ] **S4-15 · Pending** — Furious Sovereign giant lightning strike: five-second charge, yellow/red FOV, red flash, darkened screen/crackling core; bottom corners remain safe.
- [ ] **S4-16 · Pending** — Authored left/right escape arrows: flipped pair, flashing with synchronized warning sounds for the giant strike. Dependency: SpriteCook.
- [x] **S4-17 · Complete** — Regenerated repeating highway with matching roadside vegetation across loop boundaries. [Evidence](BOSS_BATCH_0915.md).
- [x] **S4-18 · Complete** — Four crossed smoke rings, intact falling ship with accelerating overlaid explosions, white flash and residual blasts. [Evidence](BOSS_BATCH_0915.md).

### Stages 5-9: space and encounter cleanup

- [x] **SPACE-01 · Complete** — Stage 5 scrolling continues through extended five-second sky launch and boss fight. [Evidence](STAGE_1_5_CORRECTIONS_0914.md).
- [x] **SPACE-02 · Complete** — Laser Cannon volume reduced at its game sound route. [Evidence](STAGE_1_5_CORRECTIONS_0914.md).
- [x] **SPACE-03 · Complete** — Shadow Orb direct/inherited detonation damage increased 35%. [Evidence](STAGE_1_5_CORRECTIONS_0914.md).
- [x] **SPACE-04 · Complete** — Space Volley Missiles: three independently targeted passive homing rounds using the authored space ordnance style. [Evidence](STAGE_1_5_CORRECTIONS_0914.md).
- [x] **SPACE-05 · Complete** — Regent port readability: serialize warned ports and helper tells; remove overlapping full-screen grid/impact clutter. [Evidence](READABLE_ATTACKS_0914.md).
- [ ] **SPACE-06 · Partial** — Stage 5 full enemy/projectile/boss balance round: first readability fixes have proof; full natural-play review with Mike remains. [Evidence](READABLE_ATTACKS_0914.md).
- [ ] **SPACE-07 · Pending** — Stage 6 full enemy/projectile behavior cleanup round with Mike; separate from the completed Tempest/Retina work.
- [ ] **SPACE-08 · Pending** — Stage 7 full enemy/projectile behavior cleanup round with Mike.
- [ ] **SPACE-09 · Pending** — Stage 8 full enemy/projectile behavior cleanup round with Mike.
- [ ] **SPACE-10 · Pending** — Stage 9 full enemy/projectile behavior cleanup round with Mike.
- [x] **SPACE-11 · Complete** — Identify and inspect the replacement ship concept: Mike approved furyship_somersault_13.png; source and existing reel inspected. New asset production remains SPACE-12/13/14. [Evidence](FURYSHIP_REFERENCE_0914.md).
- [ ] **SPACE-12 · Partial** — New ship and flight reels integrated. Twelve large solid top-view components rise from below individually with sound, then rotate and orbit without fades or mirrored perspective tricks. Remaining: flight-reel silhouette/wingspan consistency and exact final component fit. [Evidence](FURYSHIP_SOLID_ASSEMBLY_0914.md).
- [x] **SPACE-13 · Complete** — Intro sustains 1,000 px/s vertical travel through a finite cloud deck and clearing. Travelling top/bottom caps removed; fixed side banks remain. Compact assembly energy, full white reveal, speed effects and animated exhaust integrated. [Evidence](FURYSHIP_SOLID_ASSEMBLY_0914.md).
- [x] **SPACE-14 · Complete** — All nine pilot palettes integrated across ship and components; new flight, Stage 9 and space death rendering verified. SPCBOY selects the preserved original ship and campaign snapshots save/restore that selection. [Evidence](FURYSHIP_LIVE_0914.md).
- [x] **SPACE-15 · Complete** — Rename Gravity Mode announcement to Space Fighter variants: Yuri Yamado; Maverick Moonraker; Lizzie Lavender; Falva Foxtrout; Cole Collisto; Juggernaut Janis; Axel Aristotle; Freezer Falcon. [Evidence](EASY_QUEUE_0914.md).
- [x] **SPACE-16 · Complete** — Decker Space Fighter model: Draven; use SPACE FIGHTER DRAVEN in the assembly/reveal announcement. [Evidence](SUPPLY_AUDIT_0914.md).
- [x] **SPACE-17 · Complete** — Remove transparent scenery asteroids/comets: visible bodies must be opaque physical objects that can be avoided or destroyed. [Evidence](DIALOGUE_HAZARDS_0914.md).
- [x] **SPACE-18 · Complete** — Replace Stage-5 projectile size/growth animation with one reviewed static source frame and stepped pixel glow; confirm the same stable-frame treatment on Stage-2 lava saw blades. [Evidence](PROJECTILE_PIXEL_GLOW_0914.md).
- [x] **SPACE-19 · Complete** — SpriteCook chrome hammer robot, ship transformation, blue/red charge and black spiked-ball animation family. [Evidence](BOSS_BATCH_0915.md).
- [x] **SPACE-20 · Complete** — Easy/Normal Stage 5 replacement: harmless bottom flyby, top return and unfold; retain Xenoregent without assigning it to Stage 6/9. [Evidence](BOSS_BATCH_0915.md).
- [x] **SPACE-21 · Complete** — 15-second bouncing spiked ball; ordinary fire enrages into faster laser volleys, manual missiles knock back; x10/x20 supplies only. [Evidence](BOSS_BATCH_0915.md).
- [x] **SPACE-22 · Complete** — Hammer leap attacks with generated green/yellow/red committed target reticles, upward charge scan, return leap or follow-up strike. [Evidence](BOSS_BATCH_0915.md).

### Manual missile tiers and supplies

- [x] **MSL-01 · Complete** — Missile crates spawn during live boss/miniboss fights, with a shared live-box limit. [Evidence](MISSILE_SUPPLIES_0914.md).
- [x] **MSL-02 · Complete** — Remove x2 grants: stages 1-7 use x5/x10/x20; stage 8 uses x50/x100. Stage 9 retains existing quantities because none were specified. [Evidence](MISSILE_SUPPLIES_0914.md).
- [x] **MSL-03 · Complete** — Ordinary enemy RNG drops one/two spinning authored missiles, scattering pairs; no loose drops from bosses/minibosses. [Evidence](MISSILE_SUPPLIES_0914.md).
- [ ] **MSL-04 · Pending** — Manual tier damage/size progression: Standard -> Super x1.25 -> Ultra x1.5625 -> Uber x1.953125; keep passive missiles separate.
- [ ] **MSL-05 · Pending** — Hard ammo caps: Super 50, Ultra 35, Uber 20 across every pickup, save/load and firing route.
- [ ] **MSL-06 · Pending** — Tier acquisition replaces current manual missile; death resets to Standard.
- [ ] **MSL-07 · Pending** — Ultra eligibility requires Super plus survival until the next spawn wave; Uber requires the same after Ultra.
- [ ] **MSL-08 · Pending** — Generate matching Super/Ultra/Uber upgrade icons and ammo boxes, including the distinct Super Missile Box. Dependency: SpriteCook.
- [x] **MSL-09 · Complete** — Hard/Furious missile supply frequency +25% across boss clocks, loose/legacy ammo drops and scheduled/scripted crates; queued extras avoid overlap and recursive bonuses. [Evidence](SUPPLY_AUDIT_0914.md).

### Pause, saving, title and pilot selection

- [x] **UI-01 · Complete** — Pause Backspace protection; remove the old basic instructional text. [Evidence](PAUSE_MENU_0914.md).
- [x] **UI-02 · Complete** — Pause engine presentation: frozen grayscale combat, music ducked to 28%, green flashing authored selector. [Evidence](PAUSE_MENU_0914.md).
- [x] **UI-03 · Complete** — Pause rows: Resume, Return to Main Menu, Restart Level, Options, Help, Quit; top-row default, drop-in motion and sound. [Evidence](PAUSE_MENU_0914.md).
- [x] **UI-04 · Complete** — Paused Options/Help reuse their existing screens and return to pause; restart and resume use the selected actions. [Evidence](PAUSE_MENU_0914.md).
- [x] **UI-05 · Complete** — Return/Quit: verified campaign autosave with visible Autosav0X.json notice, complete death/GAME OVER sequence and fade to title/exit. Saves are browser records, not disk JSON files. [Evidence](PAUSE_MENU_0914.md).
- [x] **UI-06 · Complete** — Generate any missing dedicated pause/menu bitmap buttons; current pause uses existing authored font/cursor and game UI chrome. [Evidence](PAUSE_ART_0915.md).
- [x] **UI-07 · Complete** — Title/intro silhouettes: all nine front-facing pilots beside their ships, scrolling from Cole through the remaining roster. [Evidence](OPENER_LINEUP_0915.md).
- [x] **UI-08 · Complete** — Pilot select fills the browser viewport; desktop, portrait and live-resize presentation verified. [Evidence](PILOT_FULLSCREEN_0914.md).
- [x] **UI-09 · Complete** — Pilot-select words reveal letter-by-letter and stat bars fill left-to-right. [Evidence](PILOT_REVEAL_0914.md).
- [x] **UI-10 · Complete** — Pilot-select ship animation: onion-align and center every rotation frame. [Evidence](SHIP_ALIGNMENT_0914.md).
- [x] **UI-11 · Complete** — Use the approved new Yuri and his seven expressions throughout portrait routes; match compact dialogue avatar framing for all nine pilots, with red for Yuri. Existing approved art reused per latest instruction. [Evidence](READABLE_TYPE_YURI_0914.md).
- [x] **UI-12 · Complete** — Generate better stage fonts for all nine stages and a matching menu/stage-select/announcer font. [Evidence](READABLE_TYPE_YURI_0914.md).
- [x] **UI-13 · Complete** — Readable all-capitals 16-bit dialogue font; compact nine-pilot portraits, centered text and panels clear of the weapon HUD. [Evidence](READABLE_TYPE_YURI_0914.md).
- [x] **UI-14 · Complete** — Generate a rectangular 16-bit dialogue frame with a cool border, centered text, and palette swaps for all nine pilots; share it across in-game dialogue. [Evidence](DIALOGUE_HAZARDS_0914.md).
- [x] **UI-15 · Complete** — B is Back; use generated D-pad, action-button and Start graphics consistently for navigation prompts. [Evidence](CONTROL_HINTS_0914.md).

### Achievements, timers and unlockable modes

- [ ] **ACH-01 · Pending** — Persistent once-per-profile/account achievement registry, points and future Steam mapping.
- [ ] **ACH-02 · Pending** — Achievement menu/button and bottom-center unlock notification that slides/fades downward. Dependency: SpriteCook.
- [ ] **ACH-03 · Pending** — Nine Campaign Clear - <Pilot> achievements for Campaign or Arcade completion, 100 points each.
- [ ] **ACH-04 · Pending** — Each stage cleared on Normal or above: 10 points.
- [ ] **ACH-05 · Pending** — Each stage on Normal or above without losing a life: 200 points.
- [ ] **ACH-06 · Pending** — Entire game without spending a continue: 1000 points plus a generated trophy avatar. Dependency: SpriteCook.
- [ ] **ACH-07 · Pending** — Each stage without firing a manual missile: 100 points, unlock once per profile.
- [ ] **ACH-08 · Pending** — Each weapon maxed to level 5: its own 20-point achievement.
- [x] **ACH-09 · Complete** — Upper-right 00:00 boss/miniboss timer with pause, entrance, respawn and defeat lifecycle. [Evidence](BOSS_TIMER_0914.md).
- [ ] **ACH-10 · Pending** — Stage-1 boss/miniboss speed awards: under two minutes 200 points; under one minute 500. Stacking policy not yet settled.
- [ ] **ACH-11 · Pending** — Hard boss victories: individual 200-point achievements; Furious victories: 500 points each.
- [ ] **ACH-12 · Pending** — New-game menu order: Campaign, Arcade, Co-op, Boss Rush, Time Attack, with missing mode buttons generated. Dependency: SpriteCook.
- [ ] **ACH-13 · Pending** — Boss Rush/Time Attack gray chain-and-lock presentation using Nexus II art, denial sound on selection, unlock only on final campaign clear.
- [ ] **ACH-14 · Pending** — Wire playable Boss Rush and Time Attack behind their real unlock condition; do not fake a final campaign clear.

### Arcade and shared difficulty rewards

- [ ] **MODE-01 · Partial** — Arcade mirrors the same encounters without campaign map/cutscenes; core start flow exists and Stage-9 credit fallback is now excluded, but all transition routes still need a parity audit. [Evidence](ARCADE_RULES_0914.md).
- [x] **MODE-02 · Complete** — Arcade lives Easy/Normal/Hard/Furious = 7/5/3/3; continues = 7/5/3/1. Continue restores the same stock and the bank is run-wide, including Stage 9. [Evidence](ARCADE_RULES_0914.md).
- [x] **MODE-03 · Complete** — Difficulty descriptions show actual mode-specific lives/credits, continue prompt shows remaining Arcade credits; campaign loads restore campaign tuning. [Evidence](ARCADE_RULES_0914.md).
- [ ] **MODE-04 · Pending** — Hard enemies and shields get +15% HP across Campaign and Arcade, with explicit encounter-specific modifiers applied consistently.
- [ ] **MODE-05 · Pending** — Hard/Furious elite duplicates: authored palette variations, shields and capable aggressive fighter behavior; Furious more demanding.
- [x] **MODE-06 · Complete** — Hard/Furious Life Up frequency increased by 25%. [Evidence](EASY_QUEUE_0914.md).
- [ ] **MODE-07 · Pending** — Continue Up reward in all modes for qualifying deathless sections, or Hard/Furious elite kills; enforce defined reward eligibility.
- [ ] **MODE-08 · Pending** — Regenerate Life Up and create Continue Up pickup art matching Bullets of Fury through SpriteCook. Dependency: SpriteCook.

## Keeping this tally current

Edit stable IDs in [REQUEST_CHECKLIST_0914.json](REQUEST_CHECKLIST_0914.json), then run `python _BUILD_SOURCE/update_request_checklist.py`. Update status, evidence and workOrder together. The renderer checks IDs, evidence files and unique queue order, then recomputes totals. Do not split finished details merely to inflate completion.
