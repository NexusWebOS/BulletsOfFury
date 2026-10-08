# Balance recovery continuation — October 7, 2026

This continues the open Stage 2/4/5 boss, Hard/Furious stage and complete-finale findings from [the maneuver safety pass](MANEUVER_SAFETY_1007.md). It ships targeted counterplay and recovery improvements. The results below are recorded controller attempts, not human win-rate estimates or certification that every encounter is balanced.

## Playable changes

- **Stage 2:** Furnace flame sweeps now visibly vent, leave a clear crossing interval and warn before reigniting. Drawing and damage use the same beam list. Breaking a body section or barrier grants an attack-free opening. A surviving arm starts a fresh warning afterward, rather than resuming a live flame. Environmental firewalls and mountain vents stop scheduling new events during the miniboss; already warned events finish normally. After the fight, at least three seconds pass before a new environmental warning begins.
- **Stage 4:** Destroying the shield generators grants a real recovery opening. The Sovereign retreats toward its station while its hull, generators and helpers remain solid and attached. Its ram, beam and helper pressure wait until recovery ends. The previous ram-warning footprint and fixed-clock corrections remain in place.
- **Stage 5:** Follow-up whirlwind passes reserve reaction plus travel time for the slowest unboosted pilot. The existing interrupted-heal stun stays intact.
- **Rotating crosses:** Sovereign, pursuit bombers and Herald retain six sectors and a complete revolution. Every reappearance gets a longer warning and a distinct harmless crossing interval.
- **Earned recovery:** Existing collectible weapon supplies drop once per Furnace body section, the Sovereign's first generator break, and the Archmage's first armor break. Easy/Normal add a shield at those milestones. Interrupting the first Archmage recharge gives a weapon and shield on every difficulty. Each genuinely defeated finale phase/form gives one weapon and shield when combat resumes. Regeneration, revisiting a form and donor proxies cannot farm these rewards. No equipment is granted automatically.
- **Fight length:** Stage 2/4/5 hull and corresponding armor/module/barrier budgets are reduced on Normal/Hard/Furious. Their attack books and phases remain. Easy health is unchanged. Stage 8 donor copies retain their own health budgets.

| Difficulty | Furnace HP budget | Sovereign HP budget | Archmage HP budget | Earned Furnace/Sovereign opening | Cross absent interval | Cross reappearance warning |
|---|---:|---:|---:|---:|---:|---:|
| Easy | 100% | 100% | 100% | 2.00 s | 0.75 s | 0.75 s |
| Normal | 68% | 76% | 76% | 1.65 s | 0.64 s | 0.66 s |
| Hard | 68% | 76% | 72% | 1.30 s | 0.56 s | 0.58 s |
| Furious | 72% | 80% | 70% | 1.10 s | 0.48 s | 0.52 s |

HP percentages multiply each encounter's previous difficulty/equipment-scaled budget; they are not percentages of Easy HP. Cross dissolution is a separate harmless 0.24 seconds. Furnace flames are damaging while shrinking through their 0.14-second fade; their hitbox shrinks with the visible width.

## What the tests establish

The real Chromium whirlwind comparison improved from **0/12 delayed-movement escapes to 12/12**, with a 400 ms response, the slowest pilot, four difficulties and three starting heights. All 12 stationary controls still took damage before and after. This is isolated attack evidence, not whole-fight survival.

The native probe checks live/fading/absent/warning flame phases, real cross-laser collision, preserved sector count, solid recovering Sovereign attachments, actual collectible drops and duplicate prevention, delayed whirlwind escapes, and environmental scheduling. Protected setup is used only for mechanical fixtures; full survival screens keep real deaths, resources and normal input.

The paired boss screen uses Juggernaut, Level III primary, zero speed pickups, 250 ms delayed observation, 10 Hz decisions and normal evasion/missile controls. Its 12 before and 12 after attempts share the controller and initial configuration. The after screen uses the first complete recovery candidate, before environmental pacing and the fresh-warning refinement after a Furnace arm break. Separate playable-build rows repeat the affected fights; the candidate and playable-build hashes remain distinct.

Complete-stage screens use a separate equipped profile: Yuri, Level V laser, one speed upgrade and passive missile Level III at stage entry. This is a synthetic equipped entry, not a fresh campaign playthrough. It loses equipment and speed normally on death. Starting-life runs and runs accepting real continues are reported separately. The Continue screen preserves damage and stage progress exactly as in the game. Hard starts with three continues and Furious with one; naturally collected Continue Ups can raise those limits and are included in the recorded limit.

Controller observations were corrected during this investigation: transparent sprite padding is not a bullet hitbox; a stationary shield model cannot predict a moving hull; firewalls, volcanic debris and geysers are visible hazards; an exposed Sovereign hull is a better target than endlessly regenerated helpers; short-range flames require closer positioning; Fusion overcharge must be released; manual missiles are ordinary offensive equipment. Different controller versions are never pooled as repeated trials of the same player. Audio playback is suppressed in the tactical/credit screens to isolate its random-number consumption, and their simulation, animation and Date clocks advance together. Native physics run at 60 Hz and rendering at 30 Hz. This is not a hardware FPS benchmark.

## Results and remaining acceptance work

<!-- RESULTS -->

Failures remain visible in [the result matrix](qa/balance_recovery_1007b_matrix.md). A failed controller attempt does not prove that a human cannot win. Conversely, one clear establishes an observed route for that configuration, not a population survival probability. The existing [human replay worksheet](qa/maneuver_human_trials_1007.csv) remains appropriate for measuring recognition, enjoyment and improvement over repeated attempts.

The additional helper-pause experiment (`sovereign_ram_budget`) is **not installed**: neither of its two Hard/Furious attempts cleared. Its evidence is retained without treating a slightly lower remaining HP value as a successful balance fix.

A full finale clear requires the actual exit plus all nine persistent form pools depleted; surviving a timed form visit does not qualify. Historical candidate evidence is labeled separately from fresh playable-build verification. Co-op, optional Stage X rematches, and repeated human learning curves are not certified here.

## Reproduction

From the game repository, use its installed Node and Python/Playwright:

```text
node --check assets/game.js
node --check assets/balance_recovery_1007b.js
node _BUILD_SOURCE/test_fl.js
python _BUILD_SOURCE/probe_balance_recovery_1007b.py --out release_probe
python _BUILD_SOURCE/probe_balance_recovery_1007b.py --browser firefox --out release_firefox
python _BUILD_SOURCE/probe_balance_recovery_1007b.py --browser webkit --out release_webkit
python _BUILD_SOURCE/maneuver_credit_1007b.py --cases _BUILD_SOURCE/maneuver_credit_remaining_1007b.json --out credit_bosses_release
python _BUILD_SOURCE/maneuver_world_1007b.py --cases _BUILD_SOURCE/maneuver_world_stage2_1007b.json --out world_stage2_release
python _BUILD_SOURCE/maneuver_cruise_1007b.py --cases _BUILD_SOURCE/maneuver_release_finale_1007b.json --out finale_release
```

Do not add a candidate overlay when testing the installed layer: that would load the same globals twice. Historical before/after overlays and case files remain in `_BUILD_SOURCE`; native captures and full traces remain under ignored `_shots/maneuver_safety_1007`. Portable summaries and runtime hashes are in [QA JSON](qa/balance_recovery_1007b.json) and [CSV](qa/balance_recovery_1007b.csv). Changes are local; no commit or push was performed for this continuation.
