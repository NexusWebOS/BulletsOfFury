# Level 1–9 enemy behavior pass — October 11, 2026

Mike requested a complete regular-enemy behavior pass: visible enemies must
participate in combat, Normal → Hard must increase pressure, and Hard → Furious
must make a larger change. This pass follows the actual authored wave roster,
including spawn options and separate weapon/route variants.

## Changes

- Seven native attack queues now wait for a visible, unstunned firing window.
  Their old clocks could finish an entire attack while the common offscreen
  safety gate discarded every projectile. Fast crossing craft brake during the
  warning, fire from their existing mounts, recover and resume their route.
- Queued aimed attacks commit to a target before release. Stun or camera departure
  before firing requires a fresh warning. Fixed-direction and radial attacks keep
  their original patterns and show a source charge instead of a misleading aim line.
- Stage 1 boats/tanks cannot spend their first burst offscreen. Their idle reloads,
  generic gun cooldowns, ground turrets and drone cadence now receive the difficulty
  step. Terrain restrictions and authored burst spacing remain intact.
- Stage 2/3 small flyers remain shieldless, gunless kamikazes. Their actual late
  controller uses speed caps of 260/300/400 for Normal/Hard/Furious; the existing
  orbit approach and committed target remain. Large elemental jets get faster
  recoveries and five burst pulses on Furious instead of three.
- Held Stage 4–9 native gunships have finite attack engagements and depart. The
  legacy age-based downward push no longer moves controllers that already own
  their route, scroll placement, ram or departure. Stationary ships abandoned
  outside the camera also time out.
- Stage 6 wave-authored `s6dart` dash routes now approach visibly, warn, release
  their native four-tracer nose burst, recover and dive through the committed
  target. Previously that separate controller never fired. Dive speeds are
  320/380/500, with a selected follow-up burst on Furious. Bombing routes retain
  their own rack/ground-warning controller.
- Stage 8 side-entry ships choose a home inside the viewport. The realm fleet
  holds its firing pocket and completes 2/3/5 attack cycles before leaving.
  It no longer receives both an old movement multiplier and a generic downward
  shove. Nearer live co-op pilots can be selected for its committed attacks.
- Stage 9 rim leeches fly into the visible camera edge instead of snapping to an
  often offscreen world edge. Chaos attacks wait for visibility, and authored
  staggered entries expire correctly for Prism Mine, Void Manta, Twin Splitter
  and Chrono Breaker instead of permanently blocking their weapons.

No art, atlas, biome, weapon damage or enemy HP replacements were needed.
The meteor/contact enemies, repair support and small kamikazes retain those roles.
Existing boss controllers and the previous Hammer Chromium pass are preserved.

## Difficulty settings

These are additional regular-enemy controls, alongside existing projectile speed,
HP and stage-specific difficulty rules. They are not global boss multipliers.

| Control | Normal | Hard | Furious |
| --- | ---: | ---: | ---: |
| Generic idle cooldown rate | 1.00 | 1.10 | 1.42 |
| Native queued cooldown multiplier | 1.00 | 0.90 | 0.70 |
| Minimum native queue warning | 0.62 s | 0.54 s | 0.46 s |
| Minimum queue recovery | 0.34 s | 0.30 s | 0.26 s |
| Concurrent native queue windups | 2 | 2 | 3 |
| Typical held native engagement | 3 cycles | 4 cycles | 5 cycles |
| Realm fleet engagement | 2 cycles | 3 cycles | 5 cycles |

Furious repeats selected narrow gun salvos on alternating engagements. Heavy
explosives, mine rings and spawners are excluded from that repeat rule. Warnings
and recovery gaps remain; higher difficulty is not implemented by removing tells.

## Ownership and verification

`assets/enemy_behaviour_1011.js` is loaded after the existing encounter overrides
and the Hammer pass. Native queue call sites remain in `assets/game.js` with
their original fallback when the late owner is absent. Related current owners
are `assets/feedback_1002.js`, `assets/arcade_combat_1010.js` and
`assets/audio_feedback_1010.js`.

Verification uses the real `index.html` in Chromium, `_BUILD_SOURCE/shoot.py`,
the native enemy loop and the game canvas. The roster fixture captures actual
wave spawn options, distinguishes weapon variants, resets terrain scroll caches
between fixtures, and follows terrain-bound units horizontally to exercise their
intended firing lane. It measures real projectiles, beams and ground hazards;
it does not infer successful firing from an animation state alone.

- `node --check assets/game.js`
- `node _BUILD_SOURCE/test_fl.js`: **8,631 assertions, zero errors, final summary,
  exit 0**. The old Gate Leech assertion was updated from an instantaneous world
  edge snap to a bounded approach to the visible edge, while retaining world-side
  selection. The new regressions cover entry gating, fixed aim, stuns, death,
  actual wave-authored dash routes, late stagger timers and difficulty output.
- `_BUILD_SOURCE/probe_enemy_behaviour_1011.py`: 139 wave/weapon/role variants on
  Normal, Hard and Furious (**417 cases**), plus warning caps and native recordings.
- `_BUILD_SOURCE/probe_enemy_commitments_1011.py`: real damage, successful dodge,
  both camera edges, co-op targeting, full realm engagements and their exits.

Final native measurements and source hashes are in
`docs/qa/enemy_behaviour_1011.json`. The ignored review at
`_shots/enemy_behaviour_1011/review.html` contains eighteen eight-second opening
wave clips plus one twelve-second late alien fleet clip. The recordings use an
invulnerable observer and no player firing to expose attacks. They are bounded
combat fixtures, not nine human-played campaign clears or a survival balance score.

Earlier diagnostics exposed—and then corrected—bad fixture scroll deltas,
the scripted dash route, a legacy snap assertion and Stage 9 stagger handling.
The final report supersedes those intermediate logs. No commit or push was made;
preexisting staged, unstaged and untracked work was preserved.
