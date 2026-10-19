# Stored bosses return as Stage 7–8 enemies — 18 October 2026

Mike asked to expand the successful retired ice-carrier encounter: restore
unused bosses as harder Stage 8 enemies and introduce that threat in Stage 7.
The existing Frost Siege Veteran at 34.5 seconds remains in Stage 8.

`assets/legacy_legion_1018.js` adds ordinary enemy actors, using whole authored
boss plates. No boss bars, miniboss gates, boss-clear rewards or continue drops
belong to these actors. They accept the normal primary weapons and Retina.

| Field enemy | Original art | Attacks | Stages |
| --- | --- | --- | --- |
| Blacksteel Hunter | Stored Blacksteel Raptor, `nsb_rap_intact` | Alternating wing-gun bursts and committed twin ion lances | 7, 8 |
| Cryo Spear Veteran | Stored Cryo Spear, `nsb_cryo_spear` | Twin ice fans and spaced, fixed glacial artillery targets | 8 |
| Hellwing Executioner | Stored Herald of Death, `nhd_idle_0` through `_5` | Twin warned beams and a projectile ring with an escape sector | 8 |
| Brood Sentinel | Retired spawn-carrier plate, `nsb_spawncarrier_intact_v2` | Aimed toxic bursts and real Crescent fighter launches | 7, 8 |

The carrier uses `s8crescent`. The old `s8scout` name is remapped to the Hexpyre
monster in Stage 8; using that name as a bay jet silently launches the wrong
actor. Crescent fighters retain ordinary damage, movement, warnings and firing.
One survives alongside the carrier on Normal, up to two on Hard/Furious. They
are independent targets after launch and withdraw without firing at the approach.

## Difficulty and composition

| Setting | Primary tell | Gun-burst rounds | Ice fan per wing | Recovery | Concurrent veteran attacks | Stage 8 director cap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Normal | 1.05 s | 3 | 5 | 1.70 s | 1 | 5 |
| Hard | 0.88 s | 5 | 7 | 1.22 s | 1 | 7 |
| Furious | 0.74 s | 7 | 9 | 0.82 s | 2 | 9 |

Special tells add 0.18 seconds; glacial impacts then have a separate 1.20-second
fixed Retina warning. Beam origins and endpoints are shared by FOV, image and
collision. Movement stops during the warning and release. Overlapping beam
preparations are excluded; artillery targets remain 70 world pixels apart.

Veteran hulls use absolute HP scaled once by difficulty and co-op, rather than
`EHP`, which deliberately compresses fodder into a small shot-count band. Stage
7 veterans have 78% of their Stage 8 hull pool. At most two restored heavies can
occupy authored beats. Their engagement ends after 16/17/18 seconds; entry and
withdrawal are bounded. Approaching an encounter cancels their beams/ground
targets and sends survivors north without refilling the crowd gate.

Stage 7 introduces the carrier at 12.5 and 44 seconds and the Raptor at 28,
keeping a toxic canister in that beat. Stage 8 uses Raptor/Herald/Spear/carrier
at 10/13/27/41 seconds. Original Blue Hybrid and Tentacle Cannon waves remain at
47 and 55; Furnace Maw moves into the three-actor carrier wave at 51. A new heavy
at 55 would only enter and withdraw before the approach, so that duplicate was
removed. Increasing Hard/Furious director room prevents the last native waves
being postponed behind the added carrier wing. Stage 7 tank floor constraints,
biomes, formal bosses, portal colours and Stage 6 encounters remain intact.

## Existing faults found while integrating

- The fixed-facing Stage 8 fleet controller no longer consumed `_stagger`, while
  its firing gate still rejected a positive delay. Delayed native partners could
  remain unarmed indefinitely. The Stage 8 dispatcher now consumes that timer.
- Mutator replacements retained the same delay but used another mover. That
  blocked their shared advanced attack gate. Their delay now expires before
  normal AI readiness, restoring Rifle Locust bursts and Hexpyre ring attacks.
- The generic age-based exit push moved new veteran hulls away from their own
  warning positions. They now declare ownership of their finite route.

All hurt feedback still uses `markHit`, owner/part flash timers and the native
renderer. No flash timer is suppressed for palette preservation.

## Art and verification

Only existing art is referenced. Native-canvas contact sheets were inspected
before selection, then all reused damage/idle cells were rendered together.
Source cells remain even: 256×256, 512×512, and Herald 192×256. Each bank keeps
one proportional scale and a fixed centre. Raptor's whole plate faces south by a
fixed 180-degree rotation. No atlas, raster or generated manifest was edited.
Brood's toxic rounds use the existing 256×256 cells of
`cfx_stage7_toxic_projectiles_v2`, avoiding the older odd-width loose crop.
Aircraft ordnance is explicitly preloaded for a fresh Stage 7 visit.

Checks and source hashes are recorded in `docs/qa/legacy_legion_1018.json`:

**196 native checks passed** (177 combat/roster, 19 review/geometry), with zero
page, console/draw or missing-asset errors. The core suite finished with
**8,791 passed, 0 failed, BUILD OK, exit 0**, matching its recorded baseline.

- `node --check assets/game.js` and the new runtime file.
- `node _BUILD_SOURCE/test_fl.js`, compared with the 8,791/0 baseline and checked
  for its final BUILD OK banner and process exit code.
- `_BUILD_SOURCE/probe_legacy_legion_1018.py`: actual Normal/Hard/Furious attacks,
  isolated J-gun damage, ordinary deaths/rewards, hit pixels and flash expiry for
  all restored units, launched fighters and all 18 native Stage 8 roster slots;
  native delayed-mutator advanced attacks; six stage-wave observations.
- `_BUILD_SOURCE/probe_legacy_review_1018.py`: real controls, full side-HUD field,
  exact committed beam geometry, glacial warning/impact pixels, fighter launches,
  bot toggle, isolated review saves and art-bank dimensions.

Wave observations use an invulnerable shooting bot with minibosses bypassed.
Isolated J-gun checks remove escorts so their interception does not hide direct
hull damage. Mixed-wave observations retain the escorts. These tests establish
behaviour and integration; they do not establish human survival balance or a new
complete campaign-clear result. Screenshots/logs are in
`_shots/late_legends_1018/`. Preview:
`docs/previews/legacy_legion_1018/index.html`.

Existing staged/unstaged/untracked work was retained. `assets/game.js` and
`_BUILD_SOURCE/test_fl.js` were not edited for this request; LF/CRLF respectively
remain intact. No commit or push was performed.
