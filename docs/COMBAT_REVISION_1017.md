# Combat revision — October 17

Mike requested a stronger Hammer destruction, protection against space-laser /
Volley cheese, stable camo aircraft colors, enhanced early aircraft, smaller
lightning escorts and the missing Stage 7 approach.

## Runtime changes

- `hammer_finale_1017.js`: all18 exact authored armor cuts keep alpha1 and
  their common proportional scale. Radial velocities150–246px/s carry every
  piece fully outside the playfield before the cutaway. Authored barrage/dense
  explosion reels follow the flying armor, starting with three bursts every75ms,
  then two every110ms while pieces remain in view. No new armor art or atlas.
- `hammer_counter_1017.js`: passive `spaceVolley` and auto-missile hits cannot
  increment the deliberate multi-missile heal counter. Native hit feedback stays.
- `combat_revision_1017.js`: normal Stage5 Hammer only, excluding music/password
  bosses and the Stage8 knight. Both laser barrels, their six pulses, Akimbo and
  passive volleys share one damage budget. Burst capacity is1.8%maxHP; refill is
 3.4/3.0/2.7/2.4%maxHP per second Easy/Normal/Hard/Furious. Existing punish states
 refill2.2x. Rejected armor still flashes. Ordinary enemies and other weapons
 retain their damage. The existing final HP floor now waits until a recovery
 actually finishes or the player completes its deliberate missile counter,
 alongside the pre-existing Furious twirl requirement. No additional HP pool.
- `air_motion_1013.js`: Stage4 motion no longer falls back to a different gray
  hull below50%HP. The same authored pose/palette remains through damage;
  real impact flashes still light the sprite briefly and expire.
- `storm_guard_1017.js`: Sovereign escorts shrink192→116px with matching gun
  mounts, body extents and Retina targets. Faster patrol/entry; alternating
  lightning gun bursts and shootable lightning missile salvos. Missiles use
  committed lanes and accelerate forward. Depth entry, broken guns, boss depth
  moves and shield rearming keep their attack/contact gates. The Warden's
  separate non-electric wing remains with its own owner.
- New early aircraft roles reuse the existing authored hulls: Stage1 small
  formations; Stage2 fire fighters / retired-golem replacement; Stage3 small
  ice interceptors and large ice fighters; Stage4 interceptors, rocket aircraft
  and small formations. Gunners fire finite twin bursts, ice fighters alternate
  split ice brackets, rocketeers fire committed interceptable missiles. Full
  warnings, limited simultaneous attackers, recovery and finite departures.
  Hard/Furious shorten recovery and add rounds/roles. Authored elemental reels
  render through the actual enemy bullet path, with proportional pivots.
- Stage7's approach was owned only by the post-Stage6 director. Paths bypassing
  that story could enter without it. Post6 now ends with the full city, river,
  bridge, sewer-bank and lower-tunnel approach. Stage7 entry catches an unseen
  approach without replaying it twice. It uses the exact selected `ship_<pilot>`
  gameplay hull and native animated thrusters for all nine pilots, then resumes
  the existing top-down sewer connector. Arcade retains its native connector.

## Review and verification

`docs/previews/combat_revision_1017/index.html` embeds the actual game at its
normal field of view, with isolated saves and an explicitly invulnerable review
flight. Select aircraft, guards, the Hammer fight/finale or the Stage7 intro.

Native checks, screenshots and logs: `_shots/combat_revision_1017`.
QA record: `docs/qa/combat_revision_1017.json`.
The probes use actual Chromium, collision/damage owners, XART keys and native
drawImage/pixels. These are controlled encounter checks, not a full human
campaign balance certification. Existing game.js/test_fl bytes and unrelated
local work are preserved. No commit or push by this pass.
