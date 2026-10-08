# Maneuverability and safety pass — October 7, 2026

The mechanical corrections are verified separately from completion attempts. **This is not an all-green balance sign-off.** Several encounter and stage screens still have zero clears, and human survival, learning and enjoyment have not been measured. The exact difficulty-by-encounter results are in [the matrix](qa/maneuver_safety_1007_matrix.md), [CSV](qa/maneuver_safety_1007_matrix.csv) and [portable evidence](qa/maneuver_safety_1007.json).

## Corrections

### Combat speed no longer depends on display refresh

Ship movement and many projectiles were advanced in pixels per frame, but attack clocks used seconds. At 30 updates per second, the pilot covered less distance before a second-based strike. The low-rate ground-warning candidate initially lost 18 of 180 moving trials despite a calculated escape allowance.

The browser loop now runs combat at fixed 60 Hz, preserving its existing 60 Hz feel. Rendering stays on the display clock. Catch-up is capped at three simulation ticks, long background intervals discard accumulated time, state transitions stop catch-up, and input taps on 120/144 Hz displays remain pending until a simulation tick consumes them.

The native main-loop audit made 176 movement/projectile measurements across all nine pilots and all four difficulties in Chromium, plus the slowest pilot in Firefox and WebKit, at 30/60/120/144 Hz. Its 47 movement/timing/input assertions passed. These are timing-equivalence tests, not claims of sustained frame rate on every computer.

### Yellow ground reticles commit their aim

Previously the reticle became yellow halfway through the warning but could keep tracking until 56%. A 400 ms response to the yellow lightning cue was hit on all four difficulties in the original center-position audit.

Yellow now coincides with the actual end of tracking. Tracked ground attacks reserve reaction time, travel distance, a spatial margin and simulation-step slack for the slowest unboosted pilot. Easy/Normal get larger allowances; linked fixed-position Furnace eye-beam clocks stay unchanged.

| Difficulty | Reaction allowance used by ground budget | Additional spatial margin |
|---|---:|---:|
| Easy | 450 ms | 18 px |
| Normal | 380 ms | 16 px |
| Hard | 320 ms | 14 px |
| Furious | 280 ms | 12 px |

The native after-check has 180/180 surviving moving trials: five strike types, four difficulties, three starting positions and 30/60/120 Hz display clocks. All 20 centered stationary controls were hit. The smallest measured impact margin was 33.58 world pixels. These isolate one attack; overlapping hazards remain a separate concern.

### Sovereign's damaged-weapon ram gets a visible, honest warning

The Stage 4 ram could begin while the outer director still reported `recover`. The warning renderer suppressed that state, so the ram's warning data existed without its visible corridor. Its old 145.2 px warning was also narrower than the 353.76 px shield diameter, and the live generators extended the assembly still farther.

The renderer now shows an active ram tell even during outer recovery. It forwards the constant-width lane style through the existing authored warning renderer. Warning width includes the hull, active shield and live attached generators/helpers; destroyed generators no longer enlarge it. Charge time accounts for the slowest pilot's reaction, the assembly footprint and horizontal distance swept toward a target near an edge. The attack still commits to its recorded target.

The initial centered 400 ms response was hit by the shielded ram on Normal, Hard and Furious. The final shipped build survives 24/24 moving trials over all difficulties, shielded/unshielded rigs and left/center/right starts. Sixteen stationary cases take real damage; eight unshielded edge positions are already outside the collision path. The native warning screenshot was inspected. Full-fight outcomes are listed separately and are not replaced by these isolated passes.

## Encounter coverage and interpretation

The broad baseline contains 160 cases. The improved screen adds 164 cases: every numbered stage, every miniboss and alternate slot, the current main bosses, all finale phases and nine forms, and four attempts at the complete finale. Stage 6 carrier hull and blue ace get separate two-seed checks. Additional runs compare legal upgraded equipment and Stage 4 targeting tactics.

The broad screen ran after the clock and ground-warning corrections, before the final ram change. Twelve affected cases repeat Stage 4, its boss and the Sovereign copy using the same profile on the final build; those replace the corresponding matrix cells. Twelve additional whole-fight Stage 4 attempts use the separate targeting profile (three seeds per difficulty). Complete Stage 8/finale observations retain their earlier ram-build label; they are not presented as fresh complete-finale verification.

The principal screen uses Juggernaut, Level III primary, zero speed pickups, a 250 ms observation delay and 10 Hz decisions. It fires normally, uses genuine evasion cooldowns, loses real stock and weapons on death, and can collect actual pickups. It never grants invulnerability, force-kills an enemy or inserts damage. Rendering is sampled at 10 Hz while physics advances at 60 Hz; the dedicated browser-clock audit uses the shipped main loop and real display intervals.

The controller has limitations: approximate body geometry, incomplete understanding of older attack families, no full use of pilot abilities, and limited strategic aiming. The separately labeled tactics profile targets live Stage 4 generators and estimates visible beam rotation. The equipped profile uses Yuri, Level V laser and one speed upgrade; its results are not pooled with the slow-pilot profile as if they were repeated trials of the same player.

- A `form-transition` means the pilot survived that form's visit. It does **not** mean its persistent health pool or the full finale was cleared.
- `phase-depleted` is a phase/pool result, except a full-sequence result must also empty all saved pools or reach the genuine finale exit.
- The standalone carrier check stops at the hull's zero-HP transition and is labeled **carrier phase**; the ace check is separate. Full Stage 6 attempts include the normal route and continuation.
- Original Stage 6 timeouts were invalid combat results: the scripted pilot did not confirm the pursuit menu. The final controller confirms it through ordinary input.
- Complete-stage exits and isolated encounter clears are separate rows. A pre-boss wave sample is not a complete stage.
- Stage 7's `warpentry` is its successful handoff after Warden's death and portal sequence into Stage 8. Its retained one-point cinematic boss stub is not an undefeated combat boss.
- Each percentage shows its denominator. One success in one replay is not a 100% human survival probability. A failed controller attempt is not proof of human impossibility.
- Optional Stage X campaign rematch progression, co-op and human replay improvement have not been certified by this pass.

## Open balance findings

**October 7 continuation:** [Installed recovery changes and new completion evidence](BALANCE_RECOVERY_1007B.md) supersede some zero-clear findings below. The earlier observations remain historical evidence; unresolved Hard/Furious and human-learning acceptance items are still open.

1. **Whole-fight viability remains unproven for several early encounters.** Stage 2, Stage 4 and Stage 5 bosses have no clears with the slow-pilot screening profile on any difficulty. Whole Stage 1/2/4 attempts also need follow-up. These are priorities before certifying a forgiving Easy mode; a geometry controller can fail because of aiming or strategy, so these failures alone do not justify arbitrary HP reductions.
2. **Hard and Furious need actual repeated-player trials.** Their complete-stage screen has no clears. Only two standalone encounters in the main Furious screen clear; some finale forms are survived until they rotate out. That is insufficient evidence for the requested learning-and-reward curve.
3. **The complete finale has no confirmed scripted clear.** Successful phase or form visits remain separate. The user permits tighter precision here, but that does not replace the need to prove a full sequence can be won.
4. **Isolated safety does not prove overlap safety.** Ground warnings and the damaged-weapon ram now have measured delayed escape paths. Other simultaneous body contact, beams and projectile patterns can still defeat the test pilot. Stage 4's targeting profile still needs a demonstrated complete clear after the ram fix.

No human win rates, enjoyment ratings or learning gains are available. The report deliberately leaves these acceptance items open.

## What should count as balance acceptance

Keep a fixed pilot/loadout when measuring learning. Have the same person play each encounter three times, then compare clear rate, avoidable hits, warning comprehension and perceived fairness. Record gear progression separately so extra damage does not masquerade as learning.

For stages before the finale, require a repeatable ordinary-movement escape with reaction slack, no invisible damage region, a safe re-entry after death, and a noticeable opening after a correctly avoided attack. A viable full-fight route must survive the overlapping attack book, not just a single hazard in isolation. Hard/Furious can demand recognition and retries while preserving clear commitment cues and recovery beats. The final level can demand more precision, as requested, while retaining accurate warnings and hitboxes.

Use [the human replay worksheet](qa/maneuver_human_trials_1007.csv) to record first and repeated attempts. The zero-clear rows in the automated matrix remain investigation priorities. No human observations or success percentages have been invented.

## Reproduction and build integrity

Run from the repository using its installed Python/Playwright and Node:

```text
node --check assets/game.js
node _BUILD_SOURCE/test_fl.js
python _BUILD_SOURCE/probe_maneuver_clock_1007.py
python _BUILD_SOURCE/probe_maneuver_commit_1007.py --out warning_final
python _BUILD_SOURCE/probe_maneuver_ram_1007.py --matrix --out ram_after
python _BUILD_SOURCE/maneuver_safety_v2_1007.py --cases _BUILD_SOURCE/maneuver_final_a_1007.json --out final_a
python _BUILD_SOURCE/maneuver_safety_v2_1007.py --cases _BUILD_SOURCE/maneuver_final_b_1007.json --out final_b
python _BUILD_SOURCE/maneuver_safety_v2_1007.py --cases _BUILD_SOURCE/maneuver_release_1007.json --out release_affected
python _BUILD_SOURCE/maneuver_tactics_1007.py --cases _BUILD_SOURCE/maneuver_tactics_1007.json --out tactics_after
python _BUILD_SOURCE/summarize_maneuver_1007.py
```

Native logs and screenshots are under `_shots/maneuver_safety_1007/`; the interactive review is `review.html` there. Portable results live under `docs/qa/`. Local HTTP cancellation traces from closing browser contexts are retained in logs; page/console/missing-file errors are recorded separately.

A deployment-script text-encoding error was caught during diff review and repaired. Removing only the two intended loop edits from the repaired game source reproduces the exact pre-change SHA-256, `812e40144f9ee3b82d1e325cc1ab6e7dad0283234ce3be4101db357bdc71b58c`. Earlier asset/layout/projectile work is preserved. The full suite is rerun against the corrected source and final ram patch; final results and runtime hashes are recorded with the portable QA.

The final regression suite completed **7,840 assertions, zero errors, final success banner and exit 0**. Fresh final-build probes repeat all 200 ground-warning cases and all 48 ram cases, plus a 48-measurement / 15-assertion timing smoke check across Chromium, Firefox and WebKit. No page or console errors were recorded by those probes. The larger earlier timing audit remains 176 measurements / 47 assertions. Neither timing audit is a hardware FPS benchmark.

No HP, damage, life-stock, reward or global difficulty multipliers were changed. Changes remain local; no commit or GitHub push was performed.
