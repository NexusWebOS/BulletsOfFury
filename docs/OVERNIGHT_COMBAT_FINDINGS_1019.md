# Overnight combat findings — October 19, 2026

The current build completed all 30 protected campaign cases: Stages 1–9, with
both Stage 6 routes, on Normal, Hard and Furious. This final whole-campaign
regression includes the heavy pools, side-entry cleanup and rocket-plane repair.
Native enemy damage and stage progression remained active. All thirty runs
finished without page, console, draw or asset errors. The final equal-window
boss/miniboss census also completed all 57 cases without errors.

Six final Stage 7–8 cases also completed on all difficulties with the Harrier
rotor, volcano-head and Warden timing layers installed. The final Furious Rebel
route cleared again after the last attack-coordination refinement. All were
error-free, with no forced kills or phase changes.

These are progression checks with a visible protected bot, default starting
equipment and finite ammunition. They establish that the encounters can advance;
they do **not** establish human win rates or prove the five-on-five is finished
balancing. The bot's protection also makes its remaining life count irrelevant.

[Open the interactive review](previews/overnight_1019/index.html). It contains
497 live enemy/movement specifications, 57 equal-window boss/miniboss cases, difficulty
filters, native full-field captures, attack traits and accepted animation onions.
The original captures/reports remain under `_shots/overnight_combat_1019/`.

## Changes made

### Stage 5 enemies and Stage 9 hulls

The Stage 5 problem had two concrete causes. Space rounds could hit ordinary
enemies while their centers were still above the playfield. In the continuous
fire fixture, this killed 11–26 enemies per minute offscreen. Their authored
28–120 HP pools were also passing through a 12-HP fodder cap. A large station
could die before displaying its first attack.

Claude's shared-tree helper restored the authored Stage 5 pools and added a
visibility gate for ordinary space enemies. In its continuous-fire test,
offscreen kills fell to zero. Silent deaths fell from 21 of 24 arrivals to
roughly 9 of 24 in the deliberately severe fixture that parks the firing ship
beneath every arrival. Fast kills are still possible; surviving aircraft now
have time to use their actual controllers.

The no-player-fire matrix confirms that these controllers were present. From
the first opaque body pixels in the actual wave entrance, Normal's frigate first
fires after about 3.03 seconds; interceptor 2.13; skimmer 1.40; gravity craft 3.18;
minelayer 3.78; satellite 3.38; portal mine 3.00; station 4.00; leech 2.87.
These timings include the visible entry, unlike the older hull-center figures.
Rammers attack by contact and
repair craft have a support role. Those two roles should not be classified as
idle because they have few or no bullets.

Stage 9 had the same health-cap fault. Its authored 30–66 HP hulls were all
flattened to 19 on Normal, 21 on Hard and 29 on Furious in the measured setup.
`late_hulls_1019.js` restores the authored relative weights with native difficulty,
pressure and co-op scaling retained. The current native probe passes 74 checks:
eight types × three difficulties, real projectile damage, damaged pixels and
palette return. It also verifies that gunships remain heavier than interceptors.

A further 101 native checks cover all eleven Stage 5 hull types on all three
difficulties, including actual primary space-laser damage, hit pixels and expiry.

### Restored pools in co-op

The follow-up co-op audit exposed a normalization mistake: comparing the current
EHP against Normal EHP with the same party canceled the native party multiplier.
It affected the restored Stage 5, 7, 8 and 9 pools. These pools now apply the
existing `COOP_EHP_MUL=1.25` once, with their native difficulty and pressure ratios.
Normal examples are station 120 → 150, toxic tank 44 → 55, carrier 180 → 225 and
Stage 9 gunship 62 → 78. Solo values and the independent Claude helper file are
unchanged by this correction. Higher-difficulty party/solo ratios are not
exactly 1.25 because EHP is integer-rounded before its normalization ratio is
formed; all 75 corrected party pools stay within one HP of the disabled-repair
party pool multiplied by the native factor.

The native co-op probe passes **226 checks across 75 enemy/difficulty cases**.
It compares solo, disabled-repair co-op and current co-op pools, then fires through
Player 2's real weapon and collision path. Native hull/shield damage, white hit
pixels and actual palette return are checked. An initial full-render comparison
reported five failures on frigate/rammer views; repeated draws at the same expired
timer reproduced the discrepancy, while direct native hull comparisons matched.
After a warm full-render pass, the complete comparisons also matched. This was
a render-comparison artifact, not a runtime flash-timer fix. Historical failed
reports and their nonzero exits remain under the ignored evidence folder.

### Large side arrivals and late heavy fleets

The later audit preserved each wave's actual spawn position. Spawn clearance
can put a large aircraft farther than 80 pixels beyond the edge, but generic
cleanup still removed anything beyond that fixed margin. Some bombers and
skimmers disappeared on their first simulation frame, before any attack.

Cleanup now uses the larger authored/rendered width, existing entry clearance
and a small margin. Routes, spawn positions and collisions are unchanged. The
highway bomber, orbital skimmer, storm bombing skimmer and Stage 9 comet now
survive their side entrances and attack. Both-side checks cover all difficulties,
continuous visible motion, real primary damage, actual hit pixels and palette
return. Stage 6 bombs are measured through their ground-target owner and impact,
rather than classified as a silent gun because they release few ordinary rounds.

The Stage 4 rocket plane had a separate controller conflict. Its newer attack
owner replaced the old gun clock, but only slowed interceptors during commitment.
The rocket plane crossed the useful field before finishing its entry and tell.
It now slows through that visible commitment and resumes its route in recovery.
First releases follow the warning by about 0.88 / 0.77 / 0.67 seconds on N/H/F.
Both entrances reproduce the old missing volley with this repair disabled.
The complete side-arrival probe passes **163 checks**, without browser errors.

Six late heavy hulls also shared the fodder cap. Their authored Normal pools
are restored with native difficulty/pressure/co-op ratios retained:

| Heavy unit | Authored Normal HP |
| --- | ---: |
| Stage 7 toxic tank | 44 |
| Stage 7 sludge barge | 76 |
| Stage 8 death orb | 92 |
| Stage 8 carrier | 180 |
| Stage 8 bomber | 124 |
| Stage 8 tentacle cannon | 108 |

Scouts keep their pools. These six units can establish a native warning once
the actual muzzle is inside the combat field, before the large hull's center.
Primary contacts beyond the canvas are rejected using **y=0**. Hits still work
in the visible top band above old `PLAY.y=46`; area attacks retain their owner.
The fleet probe passes **133 checks**: positive/negative boundary controls,
unchanged scouts, actual hull/shield damage, damaged pixels and native expiry.

The Stage 7 top-entry skimmer followed its crossing route before descending into
view. That entry now descends inward, then rejoins the native pass. Both side
entries remain intact. Thirty-seven native checks pass, including a disabled
control that never appears/fires, warnings/releases and shield damage/flash.

The heavy trials park a Level 1 MG under each arrival; they are not human win
rates. Early fixtures remain excluded where replacing the exposed key map
failed to hold fire, the authored primary rule selected Chaingun, incidental
pickups changed gear, or old actors/delayed releases were not fully cleared.
Corrected MG samples choose the weapon through its actual loadout API and record
real rounds. Focused fire can still kill a Normal enemy before its first volley;
no invulnerable entry or guaranteed enemy shot was added.

### Stage 6 Rebels and stealth

The old encounter allowed all five basic guns to overlap most signature attacks.
The player also had to distinguish those attacks from bright allied fire. The
candidate gives major specials priority and rotates the remaining gun lanes.
Gun tells commit to a position; invisible Nyx fire belongs to her separately
warned ambush. Rook's grab keeps its own priority.

| Native 90-second sample | Normal | Hard | Furious |
| --- | ---: | ---: | ---: |
| Opening: contacts before → current | 25 → 17 | 28 → 18 | 32 → 20 |
| Gang: contacts before → current | 35 → 18 | 31 → 26 | 31 → 19 |
| Opening: enemy projectile peak before → candidate | 15 → 11 | 14 → 9 | 14 → 11 |
| Gang: enemy projectile peak before → candidate | 17 → 12 | 14 → 12 | 16 → 12 |

Both arms start from RNG seed 1019 and use the same protected route, full allied
AI, no player fire and a 0.95-second exposure throttle. Different attack branches
consume random values differently after divergence; these are not paired human
survival trials. All four allies remained active in all twelve samples.

A further two starting seeds, 2026 and 5019, cover three seeds × opening/gang ×
three difficulties. Mean contacts fell from 29 to 16.5 on Normal and 30 to 20.5
on Hard. The initial Furious candidate still produced eight-round nearby
pockets and averaged 30.3 contacts versus 32.3 before the pass. A focused trial
reserved major specials to one background gun rather than two; its six Furious
samples averaged 24.2 contacts and peaked at five nearby rounds. That final
coordination is installed. A production-default repeat reproduced seed 1019's
20/19 contacts, and the complete Furious Rebel route cleared error-free.
All four allies remained active in every pressure sample. Attack speeds,
warnings and signature arsenals are unchanged by this last refinement.

Twenty-four stationary signature controls and three locked-missile controls
also completed without errors. Fusion uses the native beam collection; Helix
uses separate ordnance as well as rounds. Rook's twenty parallel slugs leave a
narrow center gap on all three difficulties: a stationary center miss does not
mean an inactive weapon. Native hooks catch and move the protected actor even
without directional input. These contacts are not life losses or unavoidable
attack claims. Mike's first human review should still be Normal with ordinary
starting gear, then Hard/Furious after readability is accepted.

The initial opacity implementation was incomplete: elemental owners paint their
rounds outside the ordinary bullet loop, and some nested helpers overwrite
opacity. The final bounded drawing scope now covers the actual ordinary,
elemental and Wind owners. Twelve native checks compare real gun, missile and
special pixels: friendly art dims, while player art keeps its normal brightness.
Ship and HUD drawing stay outside this scope.

PixelLab stealth uses the actual Nyx and friendly ships. Delivered clips are a
32-frame refraction loop, 29 distinct forming frames and those same 29 forming
frames reversed for dissipation. The separate generated dissipation was rejected
because it invented a fighter silhouette. All clips share a 160 × 192 canvas,
pivot 80,96 and common transparent padding. Friendly stealth retains a 52%
visible hull. Fourteen native checks cover all delivered poses, actual blind
primary damage/hit flash while Nyx is cloaked, lock loss/reacquisition and all
five friendly aircraft.

### All nine friendly cloaks and Lizzie's attached gun

The final native audit tested the actual selected hull for every pilot. All nine
retain their centered cloak and a readable silhouette. A real fifteen-second
Lizzie pickup was allowed to dock before the native rescue scene began. During
formation movement, the hull moved while the normal attachment update paused;
the gun stayed at its old anchor, 50.04 game pixels away, and remained fully
opaque instead of sharing the hull's 0.52 cloak opacity.

The fix adjusts only the mount's drawing to its real pilot during that rescue
and multiplies its opacity by the friendly cloak. Its position state, loan timer
and firing cadence remain native. Before/after full-field captures verify the
attachment. The new probe passes 23 checks; the original 14 cloak, counter-scan
and reveal checks pass again. The Rebel route also completes on all three
difficulties after this final render change, with no browser errors.

### Rime shoulder apertures

The supplied shoulder screenshot is the Stage 3 Rime Wall. Its two authored
dark cavities now contain a low idle light and a stronger pixel charge. The
light uses the existing real PixelLab frost-charge poses, clipped to measured
cavity masks rather than laid over the hull as floating discs. Each side has
32 fixed 80 × 80 frames and pivot 40,40.

The native Rime probe passes 64 checks, including cavity containment, idle and
charged pixels, translation with the hull, authored steel between hits,
ordinary primary damage to the exposed core, mortars/beams, and owner/part
damage flash with expiry. The existing whole-body charge wash was replaced by
the socket light; actual hit feedback remains active.

### Stage 8 Hammer and Herald

The Hammer runs the real Stage 5 controller. Its visible whirl had four drawings
on a flat clock. Claude first corrected that clock to follow the native reel.
PixelLab then supplied eight proper front/quarter/side/back views, now stepped
on the native eight-drawing reel. A separate 31-frame real tumble changes the
ball's visible surface instead of rotating a nearly symmetric static plate.

All frames are 256 × 256 with pivot 128,128 and one proportional scale per bank.
The 32nd ball frame was an off-palette source hold and was omitted. A direct
32-frame turn and a later attempt at 45-degree intermediate clips were rejected:
they idled or jumped through wrong directions and changed the weapon hand.
The accepted bank has one hammer and the native core/hammer target arrangement.

Twenty-five native checks pass across N/H/F: all 39 poses really blit, the reel
matches the Stage 5 controller, all eight hammer targets sit on opaque hammer
heads, ordinary primary damages the form/native armor, and owner/part hit pixels
flash and return. Counter swings, throws, broken-hammer and giant states retain
their authored owners. Those states remain candidates for additional real motion
if the form audit demonstrates a gap; the new bank does not claim to replace
every Hammer pose.

The Herald previously relied on three broadly shared patterns; disarming it
left a small repeating head salvo. It now adds live-cannon rakes, wing-lance
rakes, and two independent head/core defenses. Destroyed modules cancel their
own attacks. The first candidate's 840-round Furious disarmed minute was rejected
as excessive and tuned down before acceptance.

| Final equal 60-second Herald fixture | Normal | Hard | Furious |
| --- | ---: | ---: | ---: |
| Intact ordinary rounds | 66 | 138 | 234 |
| Intact beams | 14 | 14 | 20 |
| Disarmed ordinary rounds | 66 | 170 | 308 |
| Disarmed beams | 6 | 6 | 12 |
| Disarmed projectile peak | 6 | 15 | 20 |

Twenty-nine separate native escape checks pass: the slowest Juggernaut can
escape each of the four added attack types from either edge using ordinary
movement on every difficulty. Stationary positive controls actually get hit.
Ordinary primary can damage the disarmed core. These are explicit pattern
checks, not a whole-fight human win claim.

### Harrier fan animation and the complete Colossus book

The copied Harrier's fan pods swayed, but their blades stayed static. A PixelLab
AI candidate added flames and changed the fan palette, so it was rejected. The
accepted PixelLab workbench reel rotates only the actual authored rotor through
sixteen axial positions. The hub, rim and housing remain native and fixed. The
runtime uses a 64 × 64 annulus with pivot 32,32 at each measured native axle.

Nineteen Chromium checks pass on Normal, Hard and Furious: all sixteen actual
positions blit at both axles, pixels stay inside the rotor cavity, exposed fans
take ordinary primary damage and visibly flash, and broken fans lose their rotor
while the surviving fan continues. The lower missile rack covers the vertical
firing line to its fan until the rack is destroyed; the test uses that native
damage route. No hit-routing or flash-throttle change was needed.

The complete Colossus attack book also prevents a false animation diagnosis.
The first visible arm laser arrives at 48.62 seconds on Normal, 45.62 on Hard and
44.22 on Furious. The initial 36-second sample could not observe it. The full
book gives the first arm tell 1.35 / 1.16 / 0.98 seconds, then the other arm
1.05 / 0.88 / 0.74. Furious adds a third 0.74-second arm attack. Core-missile
events increase 12 / 15 / 18. Downloaded enemies also fire during these windows;
the aggregate ordinary-round count is not solely the Colossus's output.

The Stage 8 volcano head is a different authored symbiote head from Stage 2's
approved Furnace bank. Its single rotating image is now replaced by 32 generated
drawings from four pinned quarter-turns. Sixteen timed charge frames contain ten
distinct lamp states and holds, copying only the generated lamp pixels onto its
actual face. The full-loop attempt only blinked
and was rejected; the charge candidate's broad white armor wash was excluded.

Every frame is 128 × 128 with pivot 64,64 and scale 1. Registration uses only
integer translations of at most one pixel, measured from the physical lamps.
The renderer selects the nearest drawing, then supplies only the small remaining
angle. Warning rays, laser roots and the alpha damage mask use that same pose.
Twenty-eight native checks pass: every accepted frame actually draws on all
three difficulties, laser roots agree with the rendered lamps, the native clock
completes a full rotation, ordinary primary damages the detached head, and actual
owner/part flashes expire to the authored palette.

### Warden warning timing

The longer 150-second audit reached the existing Furious stomp and toxic-mortar
patterns. They were absent from the short opening sample, rather than absent
from the game. It also exposed a concrete override fault: the later authored
claw controller reset every claw tell to Normal's 1.1 seconds, overwriting both
difficulty progression and the older shortened Furious stomp follow-up.

| Current Warden tell | Normal | Hard | Furious |
| --- | ---: | ---: | ---: |
| Ordinary claw | 1.10 s | 0.94 s | 0.80 s |
| Gun battery | 1.65 s | 1.40 s | 1.16 s |
| Authored Furious post-stomp claw | — | — | 0.46 s |

`warden_timing_1019.js` repairs those timings while retaining the native geometry,
weapons, damage and phase book. Thirty-one native checks pass, including actual
claw contacts in stationary controls, slowest-ship keyboard responses after a
quarter-second delay in either direction, the short Furious follow-up, live
battery releases and actual module hit pixels/expiry. These isolate the claw
counterplay and do not promise safety from every simultaneous hull or bullet.

The 150-second ordinary-round totals changed from 671/701/784 to 675/745/832;
ground attacks changed from 14/16/20 to 14/16/21. Stage pressure and random timing
remain in those observations, so they are descriptive rather than matched human
balance trials. Native phase histories and actual tells are the stronger evidence
for this repair.

### Password audit and harness correction

The password audit reached an unready font and failed UI Images in later browser
cases. Its cleanup returned to Title, starting menu downloads immediately before
closing the browser/server. The corrected harness closes the context directly
and separates teardown messages from active observations. All nine tank cases
then passed with zero active or teardown errors, both with and without a tested
image-recovery guard. No recovery attempts were needed in either clean pass.

The guard passed six deliberate native request-failure controls, but is excluded
from the game: the corrected harness did not need that additional production
layer. Its source and experiment remain under the ignored diagnostic folder.
The earlier lazy-font explanation was incomplete; bitmap-font initialization is
eager. Original failed reports and nonzero exits remain intact. The old
`final-current` aggregate observed all fifteen routes but includes 58 close/menu
network messages and exits nonzero. The fresh `final-shipping` run with the
current index and corrected harness completed all fifteen password/difficulty
cases with zero active or teardown errors. The six music cases advance on real
unmodified audio clocks; maximum observed clock drift was 0.030 seconds.
Counts use each recorded duration, including tank preparation.

### Lizzie's mounted MG and Spread Fire

Lizzie's mounted gun was selecting the space weapon's cadence before reaching
the mount branch: 9 rounds per second in space versus 24 on the ground. The mount
now owns its cadence in either setting. The native regression reproduces the
old 9-round case when the repair is disabled.

Spread's authored muzzle ink had a shared 2.0–2.4 pixel rightward bias. The helper
removed the added +2 offset and verified all nine actual ship noses. The separate
machine-gun progression regression still passes 233 checks.

A Lizzie-only Spread cadence fault was not reproduced: her Level 3 Spread used
the same 5.6 px/frame and 7.5 volleys/second as Cole. Mike explicitly requested
slower pellets, so the scoped tuning changes her Spread travel to 4.76 px/frame
and retains the measured cadence. Thirteen native checks verify this alongside
all nine muzzle positions. The mounted special MG uses its separate clock.

## What the broader audit establishes

- The live roster matrix covers 497 wave/movement specifications across nine
  stages and three difficulties. Each has a no-player-fire sample of up to
  sixteen seconds, native rendering, projectile traits and body/release times.
  A natural earlier exit ends that sample. Ordinary rounds distinguish parent,
  helper and unattributed sources. Detached splits can lack an owner; they are
  retained as unattributed, not silently assigned to the parent.
- Twelve no-projectile role types have ram, claw, hazard or support roles. None is evidence
  of an idle shooter by itself. The Stage 7 Hellhugger, for example, uses claws
  and contact rather than a gun.
- The archived Stage 7–8 veterans correctly withdraw when a boss is incoming.
  The original isolation fixture accidentally raised that real withdrawal flag.
  Correcting the fixture produced attacks in all eighteen veteran cases. Their
  native beam collection was added to the observer; the legacy Herald and
  Raptor do use beams. No production withdrawal rule was removed.
- The 57 boss/miniboss cases use equal sixty-second windows and include live
  helpers, native openings and armor formation. First projectile is not the
  same as first danger: Hammer melee, shields, grabs, portals and cinematic
  introductions need their phase histories and captures as context.
- Stage 7 Warden's original opening ordinary-round totals were nearly flat across N/H/F
  (221/220/232). Its recovery does shorten, from about 1.1 to 0.8 to 0.52 seconds;
  long shared swipe/jump durations dominate the window. The longer review and
  warning-override repair above address a measured cause; the encounter was not
  inactive.
- The complete campaign films and focused tests cover damage-driven phases.
  Opening-only counts cannot establish late-phase difficulty. The additional
  Dracodia form audit records actual body keys/rotations, attack sources, beam
  rendering and cue invocations for the individual copied forms and Volcano head.

The Stage 6 factory audit adds thirty cases: ten authored role/direction
combinations on each difficulty. The earlier collector had left fifteen
scheduled stealth passes queued, then attributed their encounter activity to
the first drone sample. Those plans are now materialized for collection and
cleared between cases; each aircraft replays through `fb2FlightSpawn`. The fresh
Stage 6 audit covers 98 cases without collector or browser errors and replaces
the old Stage 6 rows. Other stages retain their verified source rows, with
capture provenance recorded per row.

| Native stealth pass | Normal | Hard | Furious |
| --- | ---: | ---: | ---: |
| Red: actual missiles | 2 | 2 | 2 |
| Green: fixed ground marks | 1 | 1 | 2 |
| Green: mark warning | 1.75 s | 1.60 s | 1.45 s |
| Orange: actual gun rounds, depending on direction | 3–6 | 6–9 | 3–9 |

All thirty cases use their actual weapons and have full-field first-release
captures. Shorter visible passes can yield fewer bursts even with faster clocks;
raw round count is not a difficulty score. These actor clocks begin when the
aircraft spawns, after the separate pre-flight plan warning. Ground marks are
warning creation, not impact; the warning duration is shown explicitly.

## Why earlier checks missed these problems

The earlier checks emphasized state transitions, health bounds and completing
encounters. Those can pass while an enemy dies before its first visible shot,
a mounted weapon takes the wrong clock, or a four-view sprite looks still.
The late-loaded controllers and separate projectile render owners also made
an early function or opacity setting an unreliable description of the live game.
The original matrix's central placement also concealed the large side-spawn
cleanup fault. An actor vanishing before it appears is not a valid entry check.
Current measurements preserve authored positions, retire old actors and delayed
releases, and track opaque sprite bounds through the native drawing transform.
The previous hull-center timing gate is retained only in historical reports.

The next fixture correction preserved `aiAttach` state, which authored formation
builders attach after spawning. Replaying only `pattern:'ai'` had omitted that
movement and falsely suggested very slow drone entries. The matrix now separates
curve, rush, charge, loop and diagonal configurations. Adaptive and ambush
directors are disabled for isolated rows while owned helpers remain. A reset of
the native ambush director had overridden the fixture's long timer; stack-traced
controls identified its nine missiles rather than crediting them to a truck or
volcano unit. These corrections affect measurement, not production directors.
Opaque-body and warning pixels are sampled every twelve simulation frames;
release clocks are measured every frame, so tiny timing differences below that
pixel-sampling interval should not be overinterpreted.

### A real short diagonal firing window

With its real movement restored, Sharddart's diagonal pass left the stationary
camera before shooting on all difficulties. A following-camera diagnostic let
Normal and Hard fire, but Furious still left before finishing its charge. The
other Sharddart formations fired normally. `drone_commit_1019.js` now holds only
this pass's lateral line during its first visible firing commitment, continuing
a slow descent, then lets the native diagonal route resume. A three-second bound
prevents a blocked gun from holding the pass indefinitely. Native aim, projectile
speed, damage and charge clocks are unchanged.

Fifteen Chromium checks pass: all three disabled controls reproduce the missing
shot; all three current passes fire after their actual 0.55 / 0.47 / 0.40-second
charge; real primary hits flash and expire; the diagonal flight resumes. Native
comparison runs leave the rush Sharddart and Cryoeye movement/attack clocks
identical with the layer enabled or disabled. Initial trials that braked too
late, and a strict floating-point comparison at the exact 0.40-second boundary,
remain recorded as failed trials. The final implementation is separately tested.

This pass adds the missing evidence: incoming-fire fixtures, visible-body timing,
actual authored blits, equal observation windows, real damaged pixels, explicit
escape/positive controls, and ordinary-versus-ally pixel comparisons. Where a
fixture was wrong, its failure is recorded as a fixture failure rather than
invented as a gameplay fix. Native flash timers were not suppressed to preserve
palettes; transient warning overlays were separated from the hull expiry check.

## Verification and continuation

`node --check assets/game.js` passes. The required `node _BUILD_SOURCE/test_fl.js`
reaches its final **BUILD OK, 0 ERRORS** summary with 8,785 printed checks, matching
the recorded baseline. `game.js` retains LF and `test_fl.js` retains CRLF.

The new exported shipping art occupies about 2.4 MB in total. PixelLab's balance
was $8.66 after the accepted volcano-head banks; only existing credits were used. Rejected source
experiments remain separate from the shipped manifests.

Mike has returned and authorized finishing this pass and uploading the game to
`NexusWebOS/BulletsOfFury` on `main`. The overnight heartbeat is PAUSED. Final
whole-campaign progression, equal-window encounters and password startup checks
are complete. Focused native checks total **1,007 passed, 0 failed**; the final
review UI passes **25 checks** with no page, console or asset errors. The core
suite was rerun after the final mount fix and again reaches BUILD OK with all
8,785 printed checks passing, exit 0. Three final Stage 6 Rebel-route campaigns
also complete after that fix. Existing PixelLab balance last confirmed $8.47;
no jobs remain pending. Preserve unrelated local work and the separate Claude
helper. Future enhancements follow Mike's next steering.

## Remaining proposals for Mike's review

- **Five-on-five human review:** start with Normal and ordinary equipment. The
  ally dimmer and priority changes reduce protected-route contacts, but scripted
  movement still takes hits from some Turbo rows, Rook slugs and Nyx pulses.
  Those samples do not establish that an attack is unavoidable. Human aim,
  shooting missiles and choosing roll/somersault windows are not modeled there.
- **Hammer overhead bank:** the accepted real reel fixes the observed whirl and
  ball faults. The extended native book reaches the natural morph after
  43.48 / 43.48 / 47.48 seconds; all three cases are error-free. Its warning and
  nova charge each hold one body drawing, while the ball uses 31 and whirlwind
  uses eight. A distinct overhead wind-up candidate could show the hammer
  above the head while the feet stay planted, with a separate detachable flight
  bank. It would use the current Stage 8 identity, 256 × 256/pivot128,128 and
  the existing proportional scale, with a measured hammer-head target on every
  drawing. Counters, throwing and giant states currently retain their authored
  native owners. The first sixteen-frame PixelLab candidate was rejected: its
  hammer crosses to the opposite side and settles across the shoulders, then
  nearly idles. It cost $0.0434 and is preserved with onions. A single explicit
  overhead end pose was generated from the existing cloud Hammer reference and
  registered by one lossless translation before interpolation. The pinned
  sixteen-frame attempt and an alternate eight-frame model were also rejected:
  their middle poses cross/hold unevenly and then change abruptly to the correct
  endpoint. Those two attempts cost $0.0364 and $0.0366; the endpoint cost $0.08.
  No overhead bank is installed. The registered endpoint remains a reference for
  a future bank with controlled arm anatomy. Current confirmed credit balance:
  $8.47, with no jobs pending.
- **Projectile readability before more density:** retain authored ordnance
  colors and test the new ally dimmer with Mike first. Adding more simultaneous
  Rebel effects before that review could recreate the original visibility fault.
  The current roster records actual projectile families, speeds and native
  interception rules; a missing homing flag alone does not prove a straight path.
- **Further timing changes:** evaluate the repaired Warden and Herald in live
  play before increasing global bullet speed. Their new pressure comes from
  shorter tells, module-owned attacks and recovery; blanket speed changes could
  erase readable responses elsewhere.
