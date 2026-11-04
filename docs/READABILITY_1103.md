# Readability layer (November 3)

`assets/readability_1103.js` (RD13), loaded after `difficulty_assist_1103.js`. All difficulties.
`window.RD13_OFF=1` disables it. Renderer only.

- **Threat pips.** drawWorld draws rounds before effects, so explosions cover the rounds inside them.
  Explosion size stays (Mike's rule: death frame = unit frame +25%, COVER_TARGET). After drawEffects,
  every live enemy round inside an explosion with r>14 gets a 6x6 pip: dark seat, a ring in the round's
  hue (`PFX13._hue`, fallback by kind) stepped on the 1015 ladder, and a white 2x2 core.
- **Warning lanes.** combatWarningDraw is wrapped. Each frame the two owners with the highest warning
  progress (ranked from the previous frame) draw normally; when more than two are live, the others draw
  at 35% via `q.alpha`. Nothing is removed and no timing changes.
- `window.RD13={state:{stat:{pips,dimmed}},version}`.

Verification: `_BUILD_SOURCE/probe_readability_1103.py` 4/4 on Stage 9 Furious natural pacing: pips
stamped, lanes dimmed, the same frame drawn leaves rounds and enemies identical, zero page errors.
Frame: `_shots/waves_1103/readability_pips.png`.
