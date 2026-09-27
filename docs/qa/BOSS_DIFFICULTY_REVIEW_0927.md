# Boss and miniboss review — September 27

Current evidence supersedes the September 25 roster notes. The opening inspection covers 17 configured encounters on Normal, Hard and Furious (51 native Chromium cases). A second 17-case inspection covers Furnace core/head, Warden shield/guns/laser, and both Furious Stage 3 transformations. These are immunity fixtures, not clears. Current audio/video clips are in `_shots/overnight_0927/review.html`.

The finite-life probes use stage scripts in arcade mode, selected starting equipment, a control bot, ordinary collision and normal defensive cooldowns. They do not establish uninterrupted campaign completion or human difficulty balance. V5 adds two-axis movement and boss-body/beam avoidance; it still misunderstands several bespoke attacks.

| Stage | Current encounter assessment | Normal | Hard | Furious |
|---|---|---|---|---|
| 1 — Razorback / helicopter | Keep as the timing and readability reference. Helicopter inspection reaches sweep, charge, sonic, missiles and zone rush. Razorback's Hard configuration differs from Furious; opening HP alone is not a useful ranking. | Verify the third sweep remains survivable with ordinary movement after defensive cooldowns are spent. | Preserve warning time while increasing execution pressure. | Check the three-pass sequence followed by charge with an actual player; avoid overlapping lethal zones. |
| 2 — Magma Ward / Furnace Tyrant | Ward now has hunt, strafe, mortar, lance and bombard attacks; Furious uses the black/charred attack book. Furnace later-phase inspection reaches its core and head attacks with repeated charge/release audio. | Compare Ward clear time to Razorback using the same acquired loadout, not maximum weapons. | Prioritize attack handoffs and a real recovery opening after mortar/lance. | Keep the distinct charred patterns. Confirm repeated shield breaks interrupt active attacks without skipping the entire fight. |
| 3 — Frost Cruiser / Cryo Spear | Same authored actors enter once, settle, take the nuclear strike, then change form. Native long samples show neutral → Fire → Ice without re-entry. | Crosscuts, icebreaker, pincer and mortar should build on Stage 2's movement questions. | Check cannon-relay and gate overlap while the player is displaced to the side. | Keep opposite-element weakness readable. Verify normal damage/white flash in the neutral opening and element swaps under actual sustained fire. |
| 4 — Olive Warden / Storm Sovereign | Framing stays at normal zoom. Helpers, batteries, siege rockets, scissors and mortars are active. | Keep one prominent warning at a time around the helpers. | Test whether helper fire hides the main turret warning. | Increase coordinated sequences rather than adding unrelated elite hulls. No resolution changes. |
| 5 — Eclipse Siege Bomber / Chrome Hammer | Bomber has engines, cannons, rear bombs, lane missiles and a forward beam. Hammer retains ball before the cannon transition, has higher durability, and faster Hard/Furious slam lasers. V5 clears the bomber and reaches Hammer on all three settings, then loses lives. | Human-test Hammer recovery windows with a mid-level space weapon. Do not reduce HP solely because the bot dies to contact. | Confirm faster strike rays remain readable and countering the hammer gives a useful stun window. | Check ball, whirlwind, throw counter and Chromium in a natural damage progression. Current forced-phase clips prove operation, not full-fight pacing. |
| 6 — Tempest Brothers / Harrier or Rival route | Allies now acquire miniboss modules and their weapon clock advances while the stage timer is frozen. Tempest uses authored cones/signs/retinas for charge, beam and inbound warnings. Harrier fighters launch north and grow before turning. | Committed thrust hold is .42s; two-ally audio clip is below clipping. Tempest contact remains the main playtest difficulty. | Committed hold is .32s. Review body-contact escapes rather than simply reducing projectile count. | Committed hold is .22s. Preserve the existing one-committed-pass-at-a-time rule; check the optional Rival route separately from Harrier. |
| 7 — Caustic Siege Tank / Toxic Portal Warden | Tank is constrained by its complete footprint on solid floor. Warden parts, shield counterattack and both final branches run. New body removes the baked duplicate face; one mask rises to reveal its actual laser emitter. | Maintain a clear charge/recovery contrast, especially when rear legs collapse. | Check that faster reactions still leave space around the landing retina. | Prioritize leg/turret target choice and counter volleys over extra unrelated enemies. Verify the full destruction order in a naturally played fight. |
| 8 — Vile Existence | Fleet has lower simultaneous pressure, visible charge delays and spaced volleys; automatic Furious elite helpers are gone. V5 reaches the boss on all difficulties with its first death occurring there. Cannon, ghost-wall and final-form fixtures remain separate evidence. | Next human check: cannon release and shadow foes together, then the first morph. | Assess beam/body overlap while the player changes altitude. | Test final-form fake targets, box escape timing and portal grabs with spent cooldowns. Do not call a fixture recording a final-boss victory. |
| 9 — Void Horizon / Sentinels → Tidal fusion | Horizon has relay, gates, orbit and sweep. Fusion retains one world-space portal location; disabled sentinels clear pending warnings. Earlier finite-life bot cleared Normal/Hard. | Preserve committed lanes and readable gaps; verify the win with a human and ordinary acquired gear. | Check the fusion handoff while bullets are present. | Main remaining check is later-health projectile overlap with a moving player; no balance approval from the opening matrix alone. |

## Current priorities

1. Play the two Tempest hulls and the Hammer recovery/counter loop with real input, including failure/retry. The bot is insufficient to certify these.
2. Measure damage windows and total fight duration with representative mid-level loadouts. Raw HP comparisons are misleading for shields, multiple hulls, gated forms and modular parts.
3. Check the new compact Stage6 HUD radio during a human fight. Native coverage confirms it preserves every word and yields to active specials; it no longer uses the large left-side panel.
4. Keep warning geometry and damage geometry together. Stage 7's final laser warning and muzzle now share the same physical emitter; apply that standard to any remaining mismatch found in play.
5. Verify real 8BitDo hardware. Chromium reload/disconnect tests pass for simulated raw buttons 2 and 5, but cannot establish the physical pad's mapping or feel.

No commit or push was made. Full-campaign wins and final balance approval remain outstanding.


## 05:50 damage-window checkpoint

Native Chromium now has 33 sustained-fire samples: 11 encounters on all three difficulties. Cole uses Machine Gun III (Space Laser III in space), auto missiles II, no elements, manual ammo, allies or specials. The aiming bot uses ordinary movement; damage immunity removes survival from the measurement. These times are **not human clear times, campaign wins, or difficulty rankings**. Failed aim, defensive movement, different weapons, and lost lives will change them. Stage 8 full-form damage progression is not in this matrix.

| Encounter | Normal, seconds | Hard, seconds | Furious, seconds |
|---|---:|---:|---:|
| 1 — Razorback | 26.7 | 58.2 | 31.4 |
| 2 — Magma Ward | 24.4 | 30.6 | 36.0 |
| 3 — Frost Cruiser | 26.9 | 33.5 | 49.8 |
| 3 — Cryo Spear | 35.5 | 44.3 | 63.9 |
| 4 — Storm Sovereign | 87.3 | 103.7 | 121.1 |
| 5 — Eclipse Siege Bomber | 18.6 | 22.6 | 26.6 |
| 5 — Chrome Hammer | 55.3 | 76.6 | 104.3 |
| 6 — Tempest Brothers | 50.7 | 51.3 | 61.4 |
| 7 — Toxic Portal Warden | 59.0 | 75.2 | 87.0 |
| 9 — Event Horizon | 34.5 | 43.0 | 50.7 |
| 9 — Sentinels / Tidal fusion | 67.0 | 76.5 | 89.7 |

All 33 samples reached the encounter's defeat state with finite projectiles and no page/console errors. This caught two real problems:

- Sovereign initially stalled at full hull HP for 180s on every setting. Its 176.88px shield intercepted shots toward generators at 160px horizontal offset. Upper/lower rows were also tied to the 317px helpers, putting nodes near the gauges/HUD. Generator spacing is now independent: 204px columns, 46px center offset, 78px row spacing. The shield phase holds a station that fits both columns; all four generators take ordinary projectiles. Large helpers keep their approved size and clamp to world bounds. Shield warnings draw once beneath the shield gauge.
- Horizon's first tick silently replaced its scaled spawn pool with 2200 times difficulty HP. Removed that reset and increased its base hull budget so all four attacks can play. Before: 10.5/12.9/15.0s. After: 34.5/43.0/50.7s. Its health gauge now uses the shared authored miniboss art.

Bomber core destruction now empties the gauge even when engines survive. Hammer naturally reached ball and Chromium on all three settings in these samples. Furious also reached the counter/catch/revenge throw sequence.

Remaining pacing questions: Hard Razorback's two bodies took substantially longer than the single Furious variant; Magma Ward is therefore shorter than Hard Razorback despite reaching its full attack book. Compare dodge pressure with a player before changing that authored Stage 1 reference. Stage 4 repeated shield objectives take longer than Hammer under ideal aiming. Do not solve these comparisons with HP increases alone.

Stage 6 radio now uses the reserved bottom HUD with two-line pages at 34 letters/s plus 2.2s reading time. It pauses for active specials or scripted dialogue. Native checks preserve all words, verify pause/resume and inspect screenshots. Tempest's offscreen return now telegraphs for .80/.65/.50s N/H/F; the sign remains above the HUD. Actual keyboard-event play was sampled with ordinary lives, paused between observations: two deaths followed by movement-only charge avoidance. This is not uninterrupted real-time play.

Evidence: `_shots/overnight_0927/damage-windows/{baseline,report}.json`, `sovereign-access.json`, `radio/report.json`, `tempest-return/report.json`, `manual-tempest/report.json`. Updated review includes 14 real-time clips with audio.


## 07:45 follow-up — what Mike should test first

1. **Normal Tempest, without permanent Retina hold.** The existing controls intentionally block lateral rolls while Retina is held. Release the scan before double-tapping. Actual keyboard checks verified both defensive moves and their5s/7s recharge; the19.80s retry still lost three lives. Review the combination of one brother's pass and the other brother's firing line. Proposed next adjustment if it remains oppressive: a short partner recovery window around committed charge/return passes, preserving each brother's attack book instead of simply lowering HP. This is a recommendation, not a change applied to the current build.
2. **Hammer with equipment acquired in a normal run.** Counter the thrown hammer, spend one defensive move, then attempt the next strike/Chromium attack. Immunity progression reaches ball and Chromium; it does not establish a fair survival window after a mistake. Review red recovery interruption and the faster Hard/Furious strike rays.
3. **Portal Warden after losing a life.** Native actual-keyboard play showed the one-front-leg balance pose and a readable jump target, but two toxic-volley deaths and reduced post-death firepower. Finish all four legs, weakened shield, then both surviving-gun and destroyed-gun branches. Consider a recovery opening if the reduced weapon tier makes the leg phase drag, rather than making the front legs cosmetic.
4. **Stage3 opposite-element rules during sustained damage.** New ice ammunition is generated and wired. Neutral arrival → nuclear strike → alternating forms works without a second entrance. Verify the player can read the form swap while firing and understand why the damage bonus changes.
5. **Final boss with spent defensive cooldowns.** All four forms complete under ordinary damage routing with immunity:274.63/333.07/384.58s N/H/F. Fake/real echo and moving phantom/knight target checks pass. Human decisions, grabs and box pressure remain unapproved.

Stage4 generator access is now proven with ordinary projectiles at fixed zoom. Stage9 opening Sentinels intentionally have no conventional boss gauge; the shared gauge appears after Tidal fusion, preserving its authored reveal. Disabled hulls cancel warnings, and the fusion shares one world-space position.

New current review:29 clips with audio, covering all17 configured encounters plus later branches across9stages. This does not mean every clip exists on every difficulty or that any immunity clip is a campaign win. Native state/entry matrix covers all three difficulties, with additional later-phase samples. Full suite5351/0, final banner/exit0 (`suite-30.log`). Generated24 ice +24 military projectile frames inspected through the game's own renderer, including the actual bullet routing.

Remaining broader work: sustained human1–9 difficulty progression; physical8BitDo connection and mappings; systematic review of remaining legacy projectile families and attack-sound coverage; title/cinematic consistency beyond the specific fixes already recorded. No claim that all prior creative requests are complete.


Final Normal Horizon actual-keyboard check: defeated by51.1simseconds, two lives lost, resumed play alive at53.1s. Paused between observations, selected equipment, no forced kill or immunity beyond initial2frame grace. Manual missiles launched without Retina. This is an encounter sample, not a campaign win; see `manual-horizon-normal/report.json`. The contrast with the19.8s/three-death Tempest sample reinforces the need for a human progression review before claiming later stages are harder.
