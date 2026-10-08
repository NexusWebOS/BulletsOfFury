# BOF balance pass — October 7, 2026

Runtime: GitHub commit `2d5b72b`. No gameplay tuning is included in this measurement pass.

Completed **838 measurements**: 72 encounter baselines, 108 movement trials, 24 damage/simulation-step controls, 415 follow-ups (including 144 HP configuration checks), 36 stage slices, 124 confirmations, nine explicit MG selections and 50 fresh-browser confirmations. This is not a count of successful playthroughs. Zero recorded browser page/console/missing-file errors. Nine unsupported/locked Orb fixtures are excluded from weapon conclusions.

## Findings

### Co-op health scaling is inconsistent

The stated runtime rule is +50% HP for bosses/minibosses. Actual initialized Normal health:

| Encounter | Solo HP | Co-op HP | Ratio |
|---|---:|---:|---:|
| s4 | 3,872.0 | 5,808.0 | 1.500× |
| mini5 | 2,050.0 | 3,075.0 | 1.500× |
| mini6 | 2,255.0 | 3,385.0 | 1.501× |
| rebels | 4,040.0 | 4,040.0 | 1.000× |
| ace | 4,489.4 | 4,489.4 | 1.000× |
| herald | 2,796.0 | 4,194.0 | 1.500× |
| final-host | 2,600.0 | 2,600.0 | 1.000× |
| final-ghost | 2,990.0 | 2,990.0 | 1.000× |
| final-home | 3,380.0 | 3,380.0 | 1.000× |
| final-0 | 3,380.0 | 3,380.0 | 1.000× |
| final-1 | 2,744.0 | 2,744.0 | 1.000× |
| final-2 | 3,885.0 | 3,885.0 | 1.000× |
| final-3 | 4,752.0 | 4,752.0 | 1.000× |
| final-4 | 5,808.0 | 5,808.0 | 1.000× |
| final-5 | 6,435.0 | 6,435.0 | 1.000× |
| final-6 | 6,734.0 | 6,734.0 | 1.000× |
| final-7 | 5,574.0 | 5,574.0 | 1.000× |
| final-8 | 6,435.0 | 6,435.0 | 1.000× |

This is a configuration finding, independent of the test controller. Rebels, ace and finale phases/forms require an explicit co-op balance decision; simply increasing the global multiplier would also change encounters already applying it.

### Stage 5 has a steep equipment-dependent pacing curve

These trials use a new browser context per case, restore the real offscreen entrance, and use Juggernaut/Yuri with two seeds per row. Clear times include entrance time; failures stop on the first death.

| Difficulty | Level | Clears / trials | Median clear | Range | Saw rotating cross |
|---|---:|---:|---:|---:|---:|
| easy | 0 | 4/4 | 8.42s | 8.22–8.63s | 0/4 |
| easy | 3 | 4/4 | 4.52s | 4.40–4.65s | 0/4 |
| easy | 5 | 4/4 | 3.51s | 3.40–3.65s | 0/4 |
| normal | 0 | 0/4 | — | — | 4/4 |
| normal | 3 | 4/4 | 6.99s | 6.78–7.20s | 0/4 |
| normal | 5 | 4/4 | 5.39s | 5.03–5.55s | 0/4 |
| hard | 0 | 0/4 | — | — | 4/4 |
| hard | 3 | 4/4 | 7.86s | 7.57–8.15s | 0/4 |
| hard | 5 | 4/4 | 5.86s | 5.68–6.03s | 0/4 |
| furious | 0 | 0/4 | — | — | 4/4 |
| furious | 3 | 4/4 | 9.03s | 8.52–9.37s | 2/4 |
| furious | 5 | 4/4 | 6.49s | 6.27–6.72s | 0/4 |

Treat this as a pacing/recovery candidate, not a reason to multiply all enemy HP. Review the space-primary damage curve, core exposure and time available to teach the miniboss’s attack book.

### Isolated new attacks have usable movement escapes

Movement trials: 120/120 survived. Positive controls: 12/12 took damage. Juggernaut uses no shields, firing, rolls or specials. Reaction delays are 150/250/400 ms, with three starting positions and all four difficulties. Twelve additional movement trials use a 30 Hz simulation step.

The cross test measures one crossing during a dissipation interval, not an entire 360-degree attack. Rift and hook trials isolate their attack owners; they do not certify every possible overlapping hazard.

## Methods and interpretation

- Native Chromium runs the real game and renderer. No combat damage is faked or enemies force-killed. Online score submission is disabled in the isolated browser context.
- Encounter baselines use Yuri, Level III gear, one common seed, up to 60 seconds. The controller sees delayed geometric observations and has limited evasion logic.
- Mini5 follow-ups vary pilot, equipment and seed. Weapon screening covers all nine pilots; the close-range follow-up changes approach distance, and the Orb confirmation uses its actual Yuri unlock.
- Co-op configuration checks use actual initialized pools, followed by 48 active/mixed/missing-partner trials.
- Forty recovery trials pair ordinary starts with a recorded intentional death that invokes the real equipment-loss and respawn path.
- Updated finale trials record the nine persistent HP pools so a transition cannot masquerade as healing or a complete victory.
- The stage controller uses rolls and bombs and samples nine stages across four difficulties for up to 120 seconds. Its results must not be pooled with the newer encounter controller as one skill level.
- The initial shared-context repeat differed (5.050s / 4.767s); fresh-stage resets retain some player cooldowns. The final fresh-browser repeats **matched** (6.783s / 6.783s). The original timing sweep is therefore exploratory.

## Recovery, loadouts and endurance

Twenty paired recovery scenarios invoke the real death/respawn path. The initial intentional death is excluded from subsequent-death counts. These are exploratory shared-context comparisons, and the controller does not deliberately route to supplies.

| Stage 6 miniboss | Fresh Level III clear | After intentional death | HP remaining at stop |
|---|---:|---:|---:|
| easy | 10.2s | 37.4s clear | 0.0% |
| normal | 25.0s | 45.0s cap | 48.3% |
| hard | 30.1s | 45.0s cap | 57.9% |
| furious | 37.7s | 45.0s cap | 61.3% |

The Normal/Hard/Furious recovery samples survived the cap but left substantial boss health. Review rebuild pickups and low-level damage before increasing those HP pools. A human pickup-route test remains necessary.

The Normal Stage 6 co-op miniboss cleared at 34.6–35.1 seconds with two active seats; one seat against the same initialized co-op pool had 26.8% HP remaining at the 40-second cap. These are different controllers, not a controlled measure of human co-op advantage.

The CSV preserves requested and effective weapons. Stage 6 intentionally upgrades the default primary to chaingun for all pilots, including Cole; nine explicit primary-selection trials confirm the actual MG separately. Close-range flame follow-ups change approach distance, so this screen is not a directly comparable DPS ranking.

Four attempts starting at the final host and preserving resources ended at Continue:

| Difficulty | Time | Last outer encounter reached |
|---|---:|---|
| easy | 124.9s | Dracula / copies |
| normal | 85.7s | Ghost |
| hard | 52.9s | Host |
| furious | 54.4s | Host |

The controller did not clear the complete finale. Timed form changes are transitions, never full-boss victories. Updated per-form pools prevent a fresh pool being mistaken for healing.

## Decisions by mode

| Mode | First validation target |
|---|---|
| Easy | Recovery after a death with base gear and a slow pilot. |
| Normal | Intended boss duration and whether upgraded builds see signature attacks. |
| Hard | Overlapping attacks, supply routes and the cost of one mistake. |
| Furious | Full-fight and full-finale clears using the actual limited resource budget. |

The blank human sheet covers BOSS4, MINI5, REBEL6, HARR6, MINI8 and HAMR8. Run three attempts at the same loadout per mode; distinguish first-sight from learned attempts. Record deaths, bombs, warning understanding, fairness and enjoyment. Include slow/fast pilots, stripped equipment and a mixed-experience co-op session before approving global tuning. No human results have been collected.

Rerun instructions: [_BUILD_SOURCE/balance_cases_1007/README.md](../_BUILD_SOURCE/balance_cases_1007/README.md).

## Review priorities

1. Resolve per-encounter co-op health scaling, including copied-form pools and module health.
2. Review the Stage 5 space-weapon damage/HP relationship at Levels 0, III and V. Preserve recovery while giving upgraded builds time to see signature attacks.
3. Review Stage 4 and Rebel attack combinations using the captured death causes. Individual escape tests pass; controller losses alone do not prove unavoidable attacks.
4. Use the paired recovery records to set a survivable path back from depleted equipment.
5. Run the human learning/readability sheet before approving global difficulty changes.

## Evidence

- Portable results: [JSON](qa/balance_1007.json), [CSV](qa/balance_1007.csv).
- Native screenshots and raw traces: `_shots/balance_1007/`; local dashboard `review.html`.
- Reusable harness: `_BUILD_SOURCE/balance_pass_1007.py`, `balance_lab_1007.js`, `balance_attacks_1007.js`, `balance_natural_entry_1007.js`, and `balance_stage_slices_1007.py`.
- Case vectors: `_BUILD_SOURCE/balance_cases_1007/`.
- Human session sheet: `docs/qa/balance_human_sessions_1007.csv`.

## Practical limits

- Controller results are not human clear rates.
- Most isolated encounters skip entry cinematics; native-entry groups include 48 shared-context cases and 48 fresh-context cases plus two fresh repeats.
- Baseline controller uses delayed visible geometry, not pixel recognition; most trials use primary fire and rolls, not a complete human arsenal.
- Nine invalid Lightning Orb weapon fixtures are excluded; owned-yuri-8 is the supported replacement.
- Rendering is sampled during accelerated simulations; 30 FPS checks concern simulation stepping, not hardware frame-rate certification.
- Stage slices run at most 120 simulated seconds and are not complete campaign clears.
- Complete finale attempts preserve damage/resources, but a failed attempt does not establish impossibility.
- Human warning readability, enjoyment and learning remain unmeasured.
- The broad sweep reused a browser context and can retain player cooldown/profile state; its same-seed repeat differed by 0.283 seconds. Treat its time/ranking/recovery/co-op combat results as exploratory. The headline Stage 5 timing table uses fresh contexts.
- Stage 6 automatically upgrades the default primary to chaingun, including Cole. Requested weapon 0 can therefore mean effective weapon 7; nine explicit MG-selection trials confirm the actual MG separately.
- Encounter fixtures zero initial adaptive threat, suppress ordinary waves/allied support, and do not deliberately route to supply pickups.
- This pass does not exhaustively sweep all seeds, Forge variants/tiers, attack overlaps, bombs/specials, pickup routes or deliberate cheese strategies.
- No complete campaign or finale clear is claimed. Local-server logs contain some cancelled-request connection-abort traces; zero browser page/console/missing-response errors were recorded.
