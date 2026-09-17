# Overnight 0917 — what was built, what to look at first

Mike's brief: *"Go into auto work mode overnight and do not stop. continue improving my boss and
enemy AI, toy around with the weapon combination system and surprise me with some fun upgrades ...
Begin wiring up text for when you kill enemies ... I'll see you at 8am."*

Everything below is committed locally on `main` and **not pushed**. Every item has a Chromium probe
that drives the real game and a section in the suite; the failure names against the `9f64e731`
baseline were byte-identical on every full run (the two documented order-dependent flakes aside).

## Play this first

1. **NEW GAME +** — SELECT MODE shows a sixth row only after a real final campaign clear. Pick it:
   the campaign hub opens with `run.ngplus` set, and DARK MATTER infusions can drop.
   (`docs/NGPLUS_0917.md`)
2. **Infusions** — an element pickup (hex badge) layers on whatever gun you hold. Nine elements,
   three levels, level 3 named: FIREBURST, GLACIAL STRIKE, GODS WRATH, PRISM WAVE, ERADICATION,
   SONIC WAVE, MIRROR SHELL, GEYSER, VOID. Rounds wear the colour on the MG, spread, chaingun, laser,
   missiles and the orb. (`docs/INFUSIONS_0917.md`)
3. **GODS WRATH** — lightning level 3, a kill can strike every hostile from the sky. ⚠ This was
   invisible on the first build for a reason that was NOT the one I first wrote down — see §6 of the
   infusion doc. It shows now (`docs/proofs/infusion_0917/12_gods_wrath_bolts.png`).
4. **FUSION** — hold a level-3 element and pick a different one: THERMAL SHOCK, NAPALM, HYDRO VOLT,
   TESLA MIRROR ... the screen detonates once, then the new element takes the gun.
5. **Kill points** — every kill floats `+N` in the stage face, pops, and settles; 1,000+ is bigger
   and hotter. Kills within 1.2s chain: `+150 x3`, a quarter of the kill paid per chain step.
6. **HARD and up only:** ordinary jets sidestep your rounds (`EVADE_DIFF`), and the ship-boss lane
   patterns pick AGAINST where you are sitting (`BOSS_DENY_DIFF`). EASY/NORMAL are untouched.
   (`docs/ENEMY_EVADE_0917.md`)
7. **Giant beam** (kinetic on the laser), **sonic wave** (kinetic L3 on the MG), **water orb**
   (water on the orb), **void beam** (dark on the laser pulls hostiles into the column), **chromium**
   (mirrors enemy fire back), **cross-element geysers** (a soaked kill by fire/lightning).

## Things flagged for your call

- The NEW GAME + plate is wider than its family (5.23 against 3.4–4.5), so it reads shorter than
  its neighbours at the shared width. One SpriteCook job if you want it taller.
- The giant beam's muzzle orb scales with the beam and gets large at level 3.
- Infusion drop rate is `INFUSION_DROP_P` (0.14) of kill drops × `dropMul` — behind the 18% kill-drop
  gate that is about one infusion per 40 kills; it was one per 100 at first and the sweep showed it.
  Biased per stage (`INFUSION_STAGE_BIAS`); water needs the stage-9 signal, dark needs NEW GAME +.
- `EVADE_DIFF` / `BOSS_DENY_DIFF` numbers are first guesses: 0.30/0.55/0.80 and 0.50/0.75/1.0 for
  HARD/FURIOUS/INSANITY.

## Probes (all real Chromium)

| probe | result |
|---|---|
| `probe_ngplus_0917.py` | 15/0 |
| `probe_infusion_0917.py` | 31/0 |
| `probe_infusion_carriers_0917.py` | 14/0 |
| `probe_chrome_0917.py` | 10/0 |
| `probe_giantbeam_0917.py` | 10/0 |
| `probe_wrath_0917.py` | 5/0 |
| `probe_fusion_0917.py` | 9/0 |
| `probe_killpoints_0917.py` | 10/0 |
| `probe_evade_0917.py` | 11/0 |
| `probe_bossdeny_0917.py` | 8/0 |
| `probe_playtest_0917.py` | see below |

Suite sections 367 (infusions), 368 (NEW GAME +), 369 (evade + denial); 366 now also checks
`EVADE_DIFF` and `BOSS_DENY_DIFF` against every difficulty.

## The playtest sweep

`probe_playtest_0917.py`: every stage on HARD, a level-3 infusion held, trigger held, ship weaving,
45 simulated seconds each through the real stage loop, console read. Result recorded below when it
finished.

(filled in at the end of the night)
