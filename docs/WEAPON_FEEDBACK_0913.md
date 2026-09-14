# Cole, Juggernaut and Laser Mist feedback — 2026-09-13

Mike requested graphical and sound improvements to Cole's Sonic Boom, Juggernaut's
charge dash and wrecking balls, and the Laser Mist weapon. This pass uses the
existing authored art and layers recordings from the existing game sound bank.
No atlases or generated manifests were edited.

## Result

- **Sonic Boom:** inward compression rings show the held charge. The moving
  crescent, pressure edge, muzzle pulse and distortion wake reflect charge
  strength. Animation advances on the simulation clock rather than in the draw.
  Dedicated pressure build, loop, release and contact cues replace borrowed
  feedback for Cole. Short releases are audibly weaker. Holding still emits
  nothing; releasing emits exactly one piercing, finite-range wave.
- **Charge dash:** two animated authored aft exhausts, a compressed nose plate,
  orange hull afterimages and launch/landing plates show the committed ram.
  The hull no longer blinks out during dash invulnerability. Mechanical wind-up,
  ignition, boost, metal contact and landing each own their sound. Ram contact
  replaces redundant generic explosion cues. Full charge remains 360px over
  0.40s and completes when the special expires mid-dash.
- **Wrecking balls:** the two opposite flails retain their radii, orbit speeds,
  ship anchors and contact rules. Their 34px steel art matches the unchanged
  17px contact radius. Brief visual recoil and hot metal show a strike; authored
  impact bursts remain at the contact point rather than chasing the moving ball.
  Quiet chain movement, short deflections and heavy metal impacts have separate
  gated cues. Chain and ball drawing still occur in their original passes around
  the crisp aircraft. An offset introduced during enlargement was caught by the
  existing chain probe and corrected before the final footage.
- **Laser Mist:** all three emitters have blue authored launch flashes, replacing
  the borrowed MG flash. Small split pulses and dim lance echoes show the two
  split beats without a glowing wall. Each wave owns one first-split sound and
  one final-bloom sound. Wet contacts retain authored splashes, decals and capped
  bubbles. The 3 → 9 → 27 pattern, damage ledger and three-wave ceiling remain.

## Bugs found in combat verification

Laser Mist had its own broad miniboss collision route, bypassing the exposed-part
predicate used by ordinary rounds. Sealed Razorback armor produced wet impacts
and consumed lances without damage. It now uses `subBossSolidAt` before consuming
the shared hit budget. Shots pass inactive armor; a live rotated gun receives
damage and the corresponding splash. This also honors rotated Tempest geometry.

Dead pilots skip the movement pass that owns charge updates. Their abandoned
charge/ram state is now cleared before that pass, with its loops released.
Sound loops also stop on pause and fade out on release and expiry.

## Sound and movie proof

Sixteen WAV mixes are built from authored recordings, registered as seventeen
explicit sound routes in the runtime. Every route has a gain, filter and gate.
Original sounds remain available to unrelated encounters.

The final native combat footage is
`_shots/weapon_feedback_0913/video/BulletsOfFury_Weapon_Feedback_0913.mp4`.
It has 1,200 decoded video frames at 30fps, 960×1024, approximately forty seconds,
with frame-aligned game effects and held beds. The capture protects the demo
pilot and grants the demonstrated weapons; target health and attack gates run
normally. There are no added title cards. The four sections are:

| Time | Native encounter | Demonstration | Mixer peak |
| --- | --- | --- | --- |
| 0–10s | Stage 1 Damkeeper | Cole pressure build, partial/full releases, contacts | 0.7124 |
| 10–20s | Stage 4 Olive Warden | Juggernaut charge, thrust, contact, landing | 0.8543 |
| 20–28s | Stage 4 Olive Warden | Flail orbits, interceptions and steel strikes | 0.6810 |
| 28–40s | Stage 1 Razorback | Laser Mist splits and exposed-part wet impacts | 0.7900 |

All four game-mixer renders are non-silent, below clipping, with zero cut voices
and zero replay errors. Audio is replayed from actual accepted `Snd.play` events
and per-frame loop levels through the game's filters and volume settings.

## Validation and continued work

- `node --check assets/game.js` passes.
- All twenty-three new section-298 assertions pass. The full suite reaches its
  final summary: **3,703 passes / 61 failures**, exit 1. There are **zero new
  failing assertion names** against `docs/qa/game_bugfix_0913.json`.
- Focused real Chromium: **27 / 0**, including real drawImage calls, hold/release,
  contacts, split counts, armor/gun geometry, expiry, death and pause. Zero page,
  console or loop errors. Screenshots from the canvas were inspected.
- Existing live wreck/dash probe: **23 / 0**, including exact two-ball counts,
  links pointing at balls, chain endpoints, movement/dash alignment, afterimages
  and cleanup when changing pilots. Its prior proof directory was preserved.
- Readable sources reproduce `assets/game.js` byte-for-byte. Runtime LF and
  suite CRLF are preserved. Hashes, complete failure names and media evidence:
  `docs/qa/weapon_feedback_0913.json`.

Readable sources and commands are under `_BUILD_SOURCE/weapon_feedback_0913/`:
`feedback.js`, `charge_draw.js`, `sonic_draw.js`, `mist_draw.js`, `tests.js`;
`build_audio.py`, `integrate.py`, `refine.py`, `probe.py`, `probe_legacy.py`,
`record.py`, `validate.py`.

Use `probe.py` and `probe_legacy.py` for browser checks. `record.py` records the
native scenes; `--resume` reuses completed takes. The integration refuses an
already integrated runtime. `integrate.py --source-before --dry-run` reconstructs
only the expected comparison artifact from the archived pre-pass runtime; compare
it rather than overwriting subsequent work. `validate.py` collects all proof after
the suite, probes and capture complete.

Existing dirty work and previous recordings are preserved. Nothing committed or
pushed.
