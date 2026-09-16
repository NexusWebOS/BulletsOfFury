# Bullets of Fury — production roadmap

Updated 2026-09-16. This page is the GitHub entry point for the active production plan.

## Current tally

**151 tracked deliverables: 128 complete / 7 partial / 16 pending.**

**23 remain unfinished.** Ten currently depend on SpriteCook production assets. The full checklist
keeps the exact creative request, current status, dependency, and proof for every completed item.

| Work area | Complete | Partial | Pending | Total |
| --- | ---: | ---: | ---: | ---: |
| Earlier handoff, weapons, and Tempest | 9 | 1 | 0 | 10 |
| Shared combat, warnings, and targeting | 12 | 2 | 1 | 15 |
| Stage 1: fodder, Razorback, and jungle chopper | 12 | 0 | 0 | 12 |
| Stage 2: lava enemies, Inferno Reaver, and Furnace Tyrant | 7 | 1 | 3 | 11 |
| Stage 3: ice enemies, miniboss, and Rime Wall | 12 | 0 | 2 | 14 |
| Stage 4: Olive Warden and Sovereign | 14 | 0 | 4 | 18 |
| Stages 5–9: space and encounter cleanup | 18 | 2 | 4 | 24 |
| Manual missile tiers and supplies | 9 | 0 | 0 | 9 |
| Pause, saving, title, and pilot selection | 16 | 0 | 0 | 16 |
| Achievements, timers, and unlockable modes | 11 | 1 | 2 | 14 |
| Arcade and shared difficulty rewards | 8 | 0 | 0 | 8 |

## Work completed in the current production run

- Reworked Cole's Sonic Boom, Juggernaut's dash and wrecking balls, and Laser Mist with stronger
  authored graphics and sound feedback.
- Rebuilt the Tempest encounter around two independent fighter jets with readable turns, slides,
  charge thrusts, offscreen departures, returns, and per-ship damage behavior.
- Established shared green/yellow/red warning rules for dangerous boss attacks and migrated major
  attack families across Stages 2–9.
- Repaired Stage 1 enemies, Razorback, boss sound, jungle-chopper entrance and charge patterns,
  boss supplies, and Hard/Furious behavior.
- Repaired Stage 2 enemy shields, elemental damage rules, flame and projectile presentation,
  Furnace patterns, Inferno Reaver role routing, and the Reaver's warned nine-lane shotgun fan.
- Improved Stage 3 projectile visibility, removed active boats, rebuilt miniboss laser behavior,
  and expanded boss cannon, FOV, difficulty, and target-lock behavior.
- Rebuilt Stage 4 miniboss weapons and sounds, helper placement, shield-node interactions, boss
  flyovers, and Hard/Furious encounter pressure.
- Rebuilt the Stage 5 transition around the Furyship, fast cloud travel, solid component assembly,
  nine pilot palettes, somersault and roll frames, the SPCBOY legacy ship, and physical hazards.
- Added the Chrome Hammer Archmage fight, including the one-handed hammer spin, charged vertical
  boomerang throw, offscreen turn, and visible magnetic return at medium speed.
- Added manual Super, Ultra, and Uber missile tiers; boss supplies; ordinary-enemy missile drops;
  multi-target retina scanning; protected shield targeting; and passive Space Volley Missiles.
- Rebuilt the pause menu, save/return flow, pilot select presentation, dialogue system, Yuri art,
  input graphics, game fonts, stage fonts, and pilot-name visual treatment.
- Added the achievement registry, boss timers, difficulty achievements, Arcade rules, elite aces,
  Continue Up rewards, and locked Boss Rush and Time Attack menu presentation.
- Stored the three supplied boss tracks without replacing active music: `minderaser` (Boss 1),
  `Hazardous-Death` (Boss 2), and `Lie Down or Stay Down` (Boss 3).

## Active unfinished queue

The order below mirrors the current easiest-to-hardest tracker. Dependencies can be skipped while
ready work continues.

1. **S2-10 · Pending** — Build the accelerating screaming-head finale, two fire-ring X cycles,
   white flash, absent boss, and residual explosions after the Stage 2 boss identity is confirmed.
2. **S2-11 · Pending** — Continue scrolling after that defeat and play randomized other-pilot
   dialogue about the assimilated military mech.
3. **S4-16 · Pending** — Add authored left/right escape arrows with synchronized flashes and
   warning sounds for the giant Stage 4 strike. Requires SpriteCook.
4. **ACH-02 · Pending** — Add the Achievement button/menu and bottom-center unlock notification
   that slides and fades downward. Requires SpriteCook.
5. **ACH-06 · Partial** — Finish the 1,000-point no-continue achievement with its trophy avatar.
   The award logic already works; the avatar requires SpriteCook.
6. **ENG-15 · Pending** — Add the gray-to-red incoming-lock HUD indicator and distance-accelerated
   beeps above Equipped. Requires SpriteCook.
7. **ENG-02 · Partial** — Finish auditing and migrating every dangerous non-laser boss and
   miniboss attack to the shared warning rule.
8. **S2-09 · Pending** — Produce improved Furnace giant-beam art that also supports the Stage 3
   Furious palette. Requires SpriteCook.
9. **S3-10 · Pending** — Add the Hard Rime Wall charge dash, authored charge effects, circular
   return flight, and persistent hull shadow. Requires SpriteCook.
10. **S3-12 · Pending** — Add the Furious black/blue Rime Wall, all Hard patterns, and the improved
    giant beam. Requires SpriteCook.
11. **S2-08 · Partial** — Build the missile-sequence head fight and connect its distinct Super
    Missile Box encounter sequence.
12. **SPACE-12 · Partial** — Correct Furyship flight-reel silhouette and wingspan consistency and
    finish exact component fit during transformation.
13. **PRE-10 · Partial** — Finish the complete replacement-ship frame set beyond the already
    verified palette, transformation, death, roll, and space integration.
14. **ENG-14 · Partial** — Complete the nine-pilot barrel-roll and somersault regression with the
    final replacement-ship frames.
15. **S4-08 · Pending** — Build the Furious third black-camo helper and its opaque black/white,
    blue-glowing Maverick-style charge ball. Requires SpriteCook.
16. **S4-09 · Pending** — Build the Dark Chromium shatter and dual rotating energy-flame attack
    with its sounds. Requires SpriteCook.
17. **S4-10 · Pending** — Add the Dark Chromium ship-disintegration death while preserving the
    standard burning spin and crash elsewhere. Requires SpriteCook.
18. **ACH-14 · Pending** — Implement playable Boss Rush and Time Attack behind the real campaign
    completion unlock.
19. **SPACE-06 · Partial** — Complete the Stage 5 natural-play enemy, projectile, and boss balance
    review with Mike; the first readability fixes are verified.
20. **SPACE-07 · Pending** — Complete the Stage 6 enemy and projectile cleanup round.
21. **SPACE-08 · Pending** — Complete the Stage 7 enemy and projectile cleanup round.
22. **SPACE-09 · Pending** — Complete the Stage 8 enemy and projectile cleanup round.
23. **SPACE-10 · Pending** — Complete the Stage 9 enemy and projectile cleanup round.

## Source documents and verification

- [Full 151-item request checklist](docs/REQUEST_CHECKLIST_0914.md)
- [Generated easiest-to-hardest work order](docs/WORK_ORDER_0914.md)
- [Canonical editable checklist JSON](docs/REQUEST_CHECKLIST_0914.json)
- [Detailed original request ledger](docs/OVERNIGHT_REQUESTS_0914.md)
- [Latest Stage 2 Reaver proof](docs/STAGE2_REAVER_SHARED_WARNING_0916.md)
- [Historical full design roadmap](docs/BOF_ROADMAP.md)

Gameplay work is accepted only after syntax checks, the complete test suite, and visible inspection
in real Chromium. Browser probes record page errors, console errors, game-loop errors, state checks,
and screenshots. Existing suite failures remain reported by exact name so a higher pass count cannot
hide a new regression.

The tracker grows when Mike adds requests. New work receives a stable ID, a dependency and work
order, and an evidence record when completed; superseded variants are folded into the latest design
instead of being counted twice.
