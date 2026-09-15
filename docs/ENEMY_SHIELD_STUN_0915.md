# Shared enemy shield-break stun — September 15, 2026

Breaking an ordinary enemy shield now starts one shared 1.15-second punish
window. The hull stops moving and firing, lifts 14 pixels, completes a smooth
rotation and returns to its exact movement anchor. One-way shields enter their
existing red frenzy only after the stun ends, which keeps the break and frenzy
states visually separate.

The break reuses the registered shield-contact plates as four outward impact
bursts and three orbiting dizzy markers. It also keeps the existing shield-break
sound and combat burst. The sound plays once at the break; the delayed frenzy
handoff is silent.

Shield discharge damages nearby ordinary enemies within a hull-scaled radius
clamped to 78–124 world pixels. Damage is distance-weighted, capped at 16, and
limited to the six nearest valid enemies. Minibosses, bosses and other set pieces
are excluded. A secondary shield may break and stun, but the tagged splash cannot
start another splash, preventing formation-wide chain reactions.

Verification:

- Complete-suite section 304d: **8 passed / 0 failed**. It covers shield-only
  absorption, delayed frenzy, bounded radius/damage/target count, anchored lift
  and rotation, exact restoration, authored impact routing and chain prevention.
- Native Chromium: **9 passed / 0 failed**, with zero page, console or controlled
  loop errors. A real held primary-fire input using Freezer's authored Ice Breath
  broke a Stage 2 enemy shield, left its hull intact on the breaking contact,
  damaged a nearby authored unit, displayed the rotating/lifted stun and played
  one break cue before the existing frenzy resumed.
- The rendered frame was inspected at
  `_shots/enemy_shield_stun_0915/shield_break_stun.png`; the hull remains visible
  inside the impact orbit and the nearby unit remains readable.
- Final syntax passed. The complete suite reached its final summary at **3,884
  passed / 57 failed**, exit 1. There are no new failure names against the
  recorded 58-name baseline; the historical random sand-tank assertion passed.

Proof: `docs/qa/enemy_shield_stun_0915.json`. Source:
`_BUILD_SOURCE/test_enemy_shield_stun_0915.cjs`, the three guarded shield-stun
patch scripts, and `_BUILD_SOURCE/enemy_shield_stun_0915/probe.py`. Runtime LF
and suite CRLF are preserved. No commit or push was performed.
