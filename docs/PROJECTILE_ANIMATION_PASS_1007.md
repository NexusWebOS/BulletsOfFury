# Projectile and animation pass — October 7, 2026

Fixed confirmed visual defects, with no new art files, atlas repacks, hitbox changes, damage changes or difficulty tuning.

## What changed

- **Herald / Stage 8:** the live `s8pair` route was cycling four small-to-large charge examples as flight frames. Stage 7 had the same sheet contract mismatch. These shared charge sheets now use one complete flight pose with smooth internal luminance pulses and a travelling pixel highlight. Source outlines, palettes and transparent gutters are preserved. The crescent blade turns around its bright core; the toxic missile uses its hull pivot instead of its exhaust.
- **All projectile directions:** a zero vertical velocity was being replaced with `1` in several renderers, tilting exactly horizontal rounds. Zero components now remain zero while the original source-facing conventions remain intact.
- **Player projectiles:** flight visuals have a simulation-owned clock separate from damage/fuse clocks. Flame, shard, laser and spread fallback animations no longer jump with wall-clock time. Negative direction offsets can no longer request nonexistent negative frame indices. Reflected rounds retain a running visual clock.
- **Chaingun:** screenshot review exposed a second size-changing reel in the active `repair30` tracer renderer. Its complete first casing now remains fixed while an internal highlight moves through it, including every infused palette. All 108 shared chaingun loadouts were replayed after this correction.
- **Stage 4 lightning machine gun:** its eighth source cell is completely transparent. The flight loop now plays the seven real lightning frames, preventing an intermittent invisible round. All 32 final samples on each difficulty remain visible; the original failing samples are retained with the raw audit.
- **Pilot animation:** engine light follows simulation time; thrust animation advances continuously as acceleration changes, instead of repeatedly recalculating phase from a changing playback rate. Paused/zero-step rendering does not advance those clocks.
- **Destruction:** authored aircraft hull fragments used pixels-per-second launch speeds in a per-frame particle updater, immediately throwing them far offscreen. Their new seconds-based integration gives identical travel at 30/60/120 Hz and preserves their lifetime. They use their own authored fragment draw only; the duplicate generic spark path no longer receives records without a spark radius.
- **Supporting effects:** Stage 3/6 tinted cloud canvases now expose valid dimensions. The blue Ace launch starts with a defined vertical offset, so its launch burst has a finite position even when entered directly.

## Native evidence

| Coverage | Result |
|---|---:|
| Registered projectile kinds × four difficulties | 144 × 4; 4,608 visible frame samples |
| Dedicated boss projectile variants × four difficulties | 25 × 4; 1,664 frame samples |
| Live encounter/stage observations | 164 |
| Valid shared-weapon loadouts | 9 pilots × 8 weapons × 3 levels × 4 difficulties = 864 |
| Yuri-only Lightning Orb, correctly unlocked | 3 levels × 4 difficulties = 12 |
| Final actual-primary rechecks | 108 chaingun + 12 Lightning Orb |
| Final replay of affected scenes | 20 clean runs |
| Clock tests | 30/60/120 Hz on all four difficulties |
| Plane/spacecraft death observations | 8 |
| Fixed-pose source families with identical bounds/pixel occupancy | 27; internal RGB still animates |
| Repository suite | 7,697 assertions; final success banner: True |
| Final verification checks | 53/53 |
| Recorded browser errors | 0 |

The 164 observations comprise every regular boss and miniboss on stages 1–9, Rebels, the blue Ace, final host/ghost/home plus all nine copied forms (including Hammer), and all nine stage-opening slices on each difficulty. Boss observations run 24 simulated seconds; stage slices run 36. They use the real update and native Canvas draw paths with a protected pilot. The space miniboss uses live cross-beam draws rather than spawning discrete bullet objects; those beams were traced too.

The original sweep recorded 6 fixtures with non-finite scene draws. Their causes were traced to cloud dimensions, Ace launch initialization and duplicate debris rendering. The raw discovery evidence is retained; each affected configuration has a clean final replay. A source-text regression initially expected the old `||` expression; it now requires the corrected `??` expression while retaining the original `-PI/2` facing contract.

The first player matrix attempted 972 selections, including the Yuri-only weapon on other pilots and without its unlock. Auxiliary missiles initially obscured that fixture mistake. Those 108 original Orb selections are excluded from primary-weapon proof; 12 valid unlocked Yuri cases replace them. The retained 864 shared-weapon cases each contain their expected primary family. The reusable harness now respects the pilot/unlock requirements.

Maverick's homing lance intentionally retains Level I combat stats while the acquired laser level controls its color (`updatePlay` and `maverickLaserVolley` in `assets/game.js`). The coverage check initially expected the selected tier in `run.wlevel` for every weapon; it now verifies this existing lance contract explicitly. No gameplay behavior was changed to satisfy that check.

Inspected authored Stage 3/4 reel contacts: bodies remain fixed while exhaust/sparks change, so these genuine motion reels were retained. Stage 7's separate eight-frame orb and three-frame beam routes were also retained. The earlier 541-frame source audit identified tight-cropped cells; an opaque edge alone was not treated as clipping or permission to remove pixels.

## Review and reproduction

- Animated before/after and live Herald capture: `_shots/projectiles_1007/review.html`.
- Read-only source audit: `_BUILD_SOURCE/audit_projectiles_1007.py`.
- Full native matrix: `_BUILD_SOURCE/probe_projectiles_1007.py`.
- Player matrix: `_BUILD_SOURCE/probe_pilot_animations_1007.py`.
- Final targeted checks/comparisons: `_BUILD_SOURCE/probe_animation_fixes_1007.py`.
- Actual primary/chaingun checks: `_BUILD_SOURCE/probe_primary_animation_1007.py`.
- Stage 4 transparent-cell replay: `_BUILD_SOURCE/probe_lightning_animation_1007.py`.
- Portable results: [JSON](qa/PROJECTILE_ANIMATION_1007.json), [CSV](qa/PROJECTILE_ANIMATION_1007.csv).
- Required suite: `node --check assets/game.js` and `node _BUILD_SOURCE/test_fl.js`.

These are bounded visual/engine checks, not human clears, sustained hardware frame-rate benchmarks, or an exhaustive test of every co-op/forge/status-effect combination. The pass is local and has not been committed or pushed. Existing balance findings and unrelated work are preserved.
