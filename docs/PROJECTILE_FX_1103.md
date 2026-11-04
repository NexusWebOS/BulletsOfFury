# Projectile gallery and pixel-glow pass — November 3

Mike: *"make a webpage showing all projectiles in the game and how they animate, and glow etc. Next, do a
pass to make the ones lacking or are janky to properly pixel glow inside with the pixels, snake around,
do cool effects, even show me things maybe I didn't know I needed."*

## The gallery

`projectile-gallery.html` (repo root; serve the repo over http, e.g. bof-static on 8766).

Every distinct projectile is filmed through the **shipping** `drawBullets()` chain while the real
`updatePlay()` moves, spins and ages it: 24 frames at 30 fps, centred on the round, on the opaque game
canvas. Before (module off) and after (module on) play side by side, with filters for owner, stage, soft
blur, still frames, procedural-only and "changed by the pass". There are backdrop swatches (screen-blended)
and a per-round frame strip and draw diagnostics.

- Capture: `_BUILD_SOURCE/capture_projectile_gallery_1103.py [--tag before --off PFX13_OFF | --tag after]`
  with the in-page harness `_BUILD_SOURCE/projectile_gallery_1103.js` (PG3). Output:
  `_shots/projectiles_1103/{before,after}/catalog.json + strips/*.webp`.
- Coverage: all nine stages' opening wave slices plus every miniboss and boss on Furious, Stage 6
  rebels, every pilot × weapon at level 3, Yuri at levels 1/5, the Lightning Orb, the space weapons,
  missile levels and charge shots. A **registry** pass also fires every `FIRETYPES`/`PROJ`/
  `CFX_STAGE_PROJECTILE` kind alone on its own stage. Registry clips are labelled "out of context"
  because owner flags are missing, so a few fall back to generic art (e.g. `laser`, `omegawarhead` and
  `tlvNeedle` all show the same green missile there).
- Result: **286 distinct projectiles** (34 player, 252 enemy/boss; 752 filmed clips before folding).
  Enemy signatures carry their **stage**: the first version merged a Stage 9 `mg` into the Stage 1 `mg`,
  so the page showed almost only Stage 1. They also carry any short `_…kind/art/fam/form…` string key
  that later refits use to pick art. Registry kinds fire on every stage, and the page folds a kind that
  draws the same art keys (recorded per clip) into one card that reads "same art on S…"; a checkbox shows
  the folded copies. A jump bar links each stage section.
- Trap: the game's image queue advances inside its own `loop()`, which `shoot.TRAP_RAF` holds. Lazily
  requested art never decodes while the harness steps `updatePlay` by hand, and changing stage releases
  the previous stage's art. So each case first runs unfilmed, the trapped loop is pumped for real frames
  with wall time between them, and only then is the case rerun and filmed. Without this the Lightning
  Orb filmed as its white fallback ring. In real play it shows its art about 0.5 s after the first shot.
- Trap: the game canvas is `alpha:false`, so "lit" means brighter than the black clear, not alpha.

## What the audit found (before)

| finding | count |
|---|---:|
| lit with `shadowBlur` (soft Gaussian smear — the opposite of the 1015 pixel-glow rule) | 21 |
| still or near-still (fewer than 3 distinct frames of 24) | 37 |
| procedural shapes only | 0 (the Lightning Orb showed its fallback ring only until its art decoded) |

The soft-blur users are the Razorback missile/sonic, player laser beam, laser-mist children, Maverick
lance, ice orb/shards, space volley and Yuri's Lightning Orb/Bolt. The stills are mostly missiles, shells
and needles, plus the ice shard and lightning bolt.

**Stage 5 performance:** its regular waves pushed **3,418 blurred draws in 10 seconds** through the
canvas. Round drawing cost **103 ms a frame** with the GPU flush included. This is the same blur cost
SPACE_LASER_GLOW_0916 removed for one weapon, still present in the others.

## The pass — `assets/projectile_fx_1103.js` (PFX13), loaded last

Renderer only. `window.PFX13_OFF=1` disables it, and `PFX13.cfg.{glow,inner,trails,pop,rim,graze}`
switch the features.

1. **Blur → pixel glow.** While rounds draw, a requested `shadowBlur` never reaches the canvas. Each draw
   made under it gets 2–3 hard rings: the round's own silhouette tinted to its glow colour, grown in
   whole pixels, alpha on the PXG ladder and palette-stepped on the game clock. Ring reach is capped at
   about a third of the sprite's size. Primitive fills get stepped rect/stroke rings.
2. **Inner light.** Glowing rounds get their own brightest pixels added back on a travelling ladder step.
3. **Snake trails.** The pass walks back along the recorded flight path in fixed 2-px steps, so the tail
   is continuous at any frame rate. A jump of more than 40 px ends the walk.
   - energy rounds wriggle on a sine with a braided counter-strand
   - tracers get a two-step streak
   - missiles/rockets shed seeded flickering embers
   - colour comes from the round's own art, or its requested glow colour
4. **Spawn pop.** Enemy rounds are born with a 2-frame pixel ring.
5. **Threat rim.** Enemy rounds get a dark 1-px outline dilated from their own silhouette. Cells with an
   opaque background are detected and only lit from inside, so a box never gets a rim.
6. **Graze flash.** An enemy round within 6–26 px of the pilot whitens and throws sparks.
7. **Lightning Orb warm-up.** Its 10 tiny PNGs are requested at load. The first shots of a session drew
   the white fallback ring for about 0.5 s.

How it hooks: the shipping `drawBullets` is a **chain** of about 15 wrappers. Some draw beams, shields or
debris after the base; others swap `pBullets`/`eBullets` for filtered copies and draw their own rounds.
Calling the chain once per round multiplied those effects (my first version did this). Now the chain
runs exactly once. For its duration only, `Array.prototype[Symbol.iterator]` is watched: a `for…of`
over any array whose element is a live round announces that round as the loop reaches it. Nested loops
pass through, trails and pops draw once per round per frame, and the iterator is restored in `finally`.
Trail phase uses a golden-angle counter, never `Math.random`.


## Second review: frame integrity (Mike's screenshots)

Mike: *"double check for frames to make sure they don't have pixel cut off or additional frames during
the animation. the s8/s9 needles keep turning blue... s6 omega needs to remain the same size."*

Two new audits:
- `_BUILD_SOURCE/audit_projectile_frames_1103.py` reads every filmed frame and flags:
  bleed, cut, pump, hueflip, blank, pop, crop and before/after mismatch. It writes contact sheets to
  `_shots/projectiles_1103/audit/`.
- `_BUILD_SOURCE/audit_projectile_reels_1103.py` decodes every reel the rounds draw, inside the game,
  and measures cell size, content bounds, detached slivers, dropout cells and edge-cut cells.

The video audit alone over-reports pump and pop on normal flicker, so I judged every source reel by eye.
Root causes found, all in the shipping draw (the "before" films show them too):

| symptom | cause | fix (all in PFX13, art files untouched) |
|---|---|---|
| bar or stub under the Stage 5 mine/orb and the Stage 9 water orb | a detached strip baked into every cell of the authored sheet | **cell hygiene**: a drawn cell's thin, nearly rectangular, much smaller detached strips are cleared from a cached copy |
| Herald needles flip red/blue, then end up blue | `drawBossProjectileArt` draws `bpfx_proj_laser` frame by frame as each decodes (only frame 0 preloaded) and lets the round's own art draw otherwise | Herald dark claw needles (`_target17Element:'dark'` + `_heraldPart1003`) keep their red needle; every premium reel is warmed at load and used only once all 8 frames are ready |
| Stage 4 kinetic tracer flips with a blue ball | the same premium-reel race | the same gate |
| s6omega breathes | its 8 authored frames draw the canister at 46/42/32 px widths | hold frame 0 for the flight |
| Stage 3 ice missile jitters and nearly vanishes | `targeting_1017` loops `bfx_cryo_m_*`, the Cryo boss **muzzle** burst (cells 139–208 px, frame 5 nearly empty), as flight art | hold the fullest crystal cell `bfx_cryo_m_2` |
| s9lattice / s7spore collapse to a speck once a second | 12-frame bloom reels (44→215→44 px) looped | bloom in once, then ping-pong the 150–178 px plateau on the round's own flight clock |

Regressions from my first pass, also fixed:
- **Trails** were as wide as small rounds and wriggled off them (magma, photon, lava comet, rift
  shot). They are now at most 4 px, about three body lengths, wriggle within 1.4 px, and rounds under
  7 px get a straight streak.
- **Graze** whitened the whole sprite, which read as a glitch. It is now sparks plus one brighter
  inner-light step.
- **Trail colour** comes from the round's largest layer, not its first. The blue tail on a purple
  bomber orb came from a glow layer.

Capture-harness bugs found on the way:
- Warm-up passes never drew rounds, so art requested only at draw time never loaded. This made the
  Frost Cruiser slug film invisible. Prime mode now draws live rounds every 4th step.
- Enemy signatures now carry the stage.

### Third pass: what the re-audit turned up

- **Invisible rounds while art loads.** Some owners return "handled" without drawing anything when
  their art isn't decoded yet. The Herald chaos orbs do this (`if(!XART.rdy(HB25_ART.key))return true;`
  in herald_bomber_1025), and so does `targeting_1017`. PFX13 now counts real draw calls per round.
  Any live round the chain visited without a single draw gets a pixel-glow orb in its own colour
  until the art arrives (`cfg.fallback`). After warm-up, a scan of every stage's miniboss, boss and
  opening waves triggers it only for the Herald orbs and a few Tidal Fusion `s9pair`, both on
  still-loading art. In real-time play the Herald sheet is ready about 4 s after boot.
- **Cell hygiene audit** (`audit_projectile_clean_1103.py` → `audit/cleaned.png`) shows all 53 cells
  the cleaner modifies, original beside cleaned. Only specks and bars come off: under the
  ice/water slugs, the water-orb stub and the mine bar. Rockets, missiles, crescents and shards are
  untouched. The "shelf" rule (a wide flat piece wholly beyond the body in the outer band of the
  cell) catches the mine bar (41x19) and the ragged orb stub that the strip rule missed.
- **Bloom reels:** `s9lattice` and `s7spore` loop a 12-frame bloom (44→215→44 px). They now bloom once,
  then ping-pong the plateau.
- **Not bugs:** the pink band in some Stage 5 clips is the bomber's FOV warning beam, drawn in the same
  pass. `s4bomb` blinks red/green by design. The Event Horizon `s9needle` is a horizontal bolt
  travelling horizontally.
- **Gallery pairing:** enemy clips are keyed per encounter as well as stage, so before/after always
  film the same source. The page folds identical art (same kind, flags and art keys) behind one card.
- **Capture harness deadlock:** the Playwright `route()` interceptor makes Python answer every
  request. Once warm-up passes began drawing inside long `evaluate()` calls, the browser and Python
  waited on each other, and the run sat at 0 % CPU. The interceptor is gone; the game is local.
  Warm-up draws also skip blur, because their pixels are discarded.

## Verified

`python _BUILD_SOURCE/probe_projectile_fx_1103.py` runs real Furious fights: Stage 2 boss, Stage 5
waves, Stage 8 miniboss and Stage 1 waves. Report: `_shots/projectiles_1103/live/report.json`. RESULT
**14/14**, re-run after every module change in all three passes.

- **Renderer only.** On sampled frames the same game state is drawn by the shipping chain and by PFX13.
  Every round's primitive state and the `Math.random` call count must match. The fight itself is **not**
  deterministic run to run: two module-off runs already differ. So comparing separate runs proves
  nothing, and this probe doesn't do it.
- No `shadowBlur` reaches the canvas while rounds draw.
- Cost, same frames, GPU flush included:
  - Stage 5: **103 ms → 4.9 ms**
  - other stages: +0.25 to +0.8 ms for trails, rims and rings (budget: under +1 ms)
- Zero page/console errors.

Gallery coverage, final films (828 clips per side, per encounter, folded to **276 distinct** on the
page): soft blur 21 → 2, still clips → **0**, invisible rounds → 0. Every remaining before/after
mismatch is an intended change on the same art (cleaned bars, pixel glow, trails).
- The 2 "blur" entries are Stage 5 `_hc1007Part` rounds. Their blur comes from the bomber's FOV warning
  lines (`l23FovDraw` via `combatWarningDraw`), which are drawn inside the bullet pass between rounds.
  The per-clip stat counts the whole pass, so those clips are charged with the boss's telegraph. The
  rounds themselves are converted.
- The 1 still is `spaceLaser` level 5, whose approved pulse plus baked glow plate PFX13 deliberately
  leaves alone.

Core suite: `node _BUILD_SOURCE/test_fl.js` exits 1 before its summary with
`ReferenceError: difficultyHealthBaseline15 is not defined` in `combat_polish_0927b.js`. That file
carries another session's uncommitted edit. The failure is identical with this module removed from
`index.html`, so it is not caused here.

## Open

- The pixel rings follow each sprite's silhouette. A round whose sheet has an opaque cell background is
  only lit from inside: no ring, rim or graze whitening.
- Registry-only kinds that never appear in a live slice (owner-specific art) show generic art in the
  gallery. A longer per-stage capture would find the remaining natural ones.
