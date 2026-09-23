# September 22 flight, boss and arsenal repair pass

Base: `22a4e5f3` (the downloaded build). Changes are local and uncommitted.

## Implemented

- Stage 6 uses the same continuously scrolling world for its opening, stealth reveal, combat, route selection and boss. Cruise speed is 740; the opening and Freezer special no longer slow this stage. Stealth aircraft face north throughout their fade-in. The route choice allows 30 seconds while combat continues, followed by the Harrier crossing and rival introduction.
- Allies use their native bank, roll and somersault frames, predictive evasion, aimed fire, missiles and pilot-specific attacks. Each arriving ally has a 0.0001 probability of being susceptible to a hit; an actual hit then makes that ally withdraw. This is a per-arrival probability, not a per-frame damage roll. Primary aim uses the exact lead solution 99% of the time; that is not a guaranteed hit rate against moving enemies.
- Active ally count scales the enemy cap, wave cadence and supply cadence by 2/3/4. Additional onslaught waves are bounded. Per-pilot special supplies are separate from ordinary crates and reject other pilots' shots and collection, including child lightning bolts and orb fragments.
- Five Roaming Rebels have no shields, physical movement and finite dodge windows. Forty generated roll frames replace flat rotated aircraft. Their shared navigation/evasion behavior is paired with tracer, lightning/missile and warned charge roles.
- Stage 1 sonic attacks center the helicopter without tilting its hull. Horizontal waves span 75% of the view. Normal sends one, Hard three, Furious six: straight, angled, two vertical quarter-screen lanes, straight, opposite angle.
- Stage 4 main-boss helpers are three times their former size, positioned between their side's core pair. The view fits the full boss width. Furious adds the right helper's vertical hover and inward side fire. Miniboss escorts steer clear of the hull's target area; native weapon paths continue to hit them.
- Stage 3 mini/main bosses and Stage 5 receive difficulty-scaled durability and shorter attack recovery. Stage 5 favors chained hammer leaps, including actual landing damage. New overhead strike and cleaned twirl art replace the old poses. Back-mounted-gun poses are excluded from transition reels; hand-held chaingun attacks remain. Separate hammer/gun health bars are hidden. The Harrier assembly uses its formed ship art at the completed merge.
- Fire Whip is selectable, remains anchored to the ship, sweeps left/right along a flexible curve, and uses the same curve for hits and rendering. Its damage is 25% above the corresponding laser calculation. It hits exposed modules as well as hulls and containers. The oversized infusion halo is removed.
- Gameplay and previews share orb updates, including magma bursts, shards, spin and dark collapse. Native lightning orb previews now fire. All 405 existing element/weapon tier-icon files were found on disk; this pass reuses that artwork rather than duplicating it.
- New generated frame art is integrated into loadout, weapon-form selection, weapon unlocks and life/continue supplies. Previews, honest unlock counts, bitmap text and controller prompts remain functional.

## Generated artwork

Tool: built-in image generation. Sources retained beside normalized assets. No reference/source images were deleted.

- `assets/game/stage5_archmage_0916/leap_strike_0922.png`: eight 320x384 cells; source `exec-995ea07d-5bcd-479e-bba8-a287bb3a1b31.png`. Components normalized around the energy core.
- `assets/game/stage5_archmage_0916/twirl_throw_0922.png`: sixteen 176x160 cells; source `exec-3c884014-ae1c-4f8e-ba81-2ed53211876a.png`. Edited from the existing twirl reel to remove the back gun, then isolated and padded into uniform cells.
- `assets/game/ui/arsenal_0922/frame.png`: source `exec-96748f56-6f10-491b-9533-f62aea24fad6.png`.
- `assets/game/roaming_rebels_0922/roll/`: five eight-frame 256x256 sets with preserved source images and manifest. Sources: Voss `97ca02ee-14dc-4b1d-b44e-745ff9464bc7`; Nyx `7cff224e-0f7f-48fb-9b1d-c9fc93681610`; Rook `84b0be65-ca16-4e52-b634-1874a63f63dc`; Kaia `d7f08400-7e40-4d35-8491-dcff583a7483`; Jace `2ff4322c-fe7f-4736-b36c-10c753ade7e3` (all `exec-*.png`).

## Verification

- `node --check assets/game.js` passed.
- `_BUILD_SOURCE/probe_focus_0922.py`: continuous scrolling, ownership, five rivals and decoded roll frames, sonic wave counts, helper placement, hammer landing damage, whip selection/anchor/sweep, 81 preview combinations, screenshots and browser error capture.
- `_BUILD_SOURCE/probe_stage6_wingmen_0922.py`: independent navigation, eight native-size allies, dodge, real projectile damage, warning timing, bomber racks and live route selection. Passed with zero browser errors.
- `_BUILD_SOURCE/probe_stage4_targets_0922.py`: real weapon/module interception checks passed.
- Full-suite result is recorded below after the final run. Downloaded baseline had 79 failed assertions. Existing failures include outdated roster/weapon expectations, audio harness issues and other unrelated contracts. Do not describe the suite as green.
- Focused screenshots and JSON evidence are under ignored `_shots/focus_0922/`; wingman evidence under `_shots/wing_0922/`. Art and actual rendered menus/bosses were visually inspected.
- Game LF and test_fl CRLF are preserved. Use `git -c core.whitespace=cr-at-eol diff --check` for the mixed repository conventions.

## Limits / follow-up

This was focused browser verification with controlled/invulnerable player fixtures, not a full campaign victory on each difficulty. The new Stage 3/5 difficulty and maximum Stage 6 onslaught need human balance feedback and longer performance sessions. The legacy suite failures remain repair work. Rival attacks share agile movement principles but are deliberately hittable; they do not inherit the allies' near-invulnerability.

### Final verification result

Final full run: `_shots/focus_suite_final_complete_0922.log`, **75 failures**, compared with 79 in `_shots/focus_baseline_suite.log`. The final failed-assertion names are a subset of the baseline: **no newly failing assertion names**. The four baseline-only failures concern randomized enemy movement/spawning; their absence is not claimed as a repair. The suite remains nonzero.

The final focused Chromium probe completed successfully with no page/console errors. The separate wingman probe also passed. Screenshot review included actual gun-free twirl, hammer overhead strike, five rival roll attitudes, fixed helper sockets, live Fire Whip selection, unlocks and supplies. The 0.01% ally hit eligibility is a per-arrival design setting and was not statistically validated by millions of runs.
