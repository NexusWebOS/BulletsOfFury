# Event Horizon assault — October25

Mike's faster spin, up/down flight and charged energy bomb are implemented for
the Stage9 miniboss. [Fresh45-second Furious review](previews/horizon_assault_1025/index.html).
The existing bullethell gallery's `9-mini` entry also uses the current film.

The old barrage stretched one complete spin bank over its firing duration.
`assets/horizon_assault_1025.js` gives the existing authored spin an independent
clock:1.75 rotations/s on Normal,2 on Hard and2.25 on Furious. Rotation brakes to
the upright source pose before the charge. The whole black drift/spin/charge
plates and their common eye pivot remain in use.

Flight has its own clock. In the Furious film the centre travels from170 to315
world pixels vertically, including during the barrage. The physical core,
rendered hull, warning origin and projectile launcher share that position.
Native horizontal manoeuvres remain. Charging pauses the vertical pass so the
large eye effect and committed firing lane are readable.

Every third native decision inserts an eye bomb, then resumes the native attack
book. The cyan energy visibly grows on the eye. Its green/yellow/red native
warning tracks briefly, locks with roughly one second remaining, then launches
a92px authored energy orb into a warned54px-radius impact. Furious charge lasts
1.65s and flight lasts1s. The shared targeted-ball owner supplies the line,
reticle, projectile travel and impact collision. Defensive clearing cancels the
bomb's splash; native defeat cancels a pending charge or flight.

The energy uses the existing animated cyan orb; no new hulls or generated assets
were needed. Charge, launch and impact use the shared `bossWeaponCharge`,
`combatOrb0927` and `warpBurst` cue routes and retrigger gates. Ordinary energy
rejects offensive interception from birth while preserving defensive clears.
Native complete HP, white damaged pixels, Retina/core ownership and defeat stay
authoritative. The final Stage9 Tidal encounter and warp remain separate.

Film checkpoints: fast barrage spin0:16.8; low vertical pass0:08.1; large charge
0:09.4; launched bomb0:10.0; impact0:10.9. The gallery also provides slow motion
and single-frame stepping. This is an invulnerable observation take with
weapons withheld, not a human difficulty verdict.

## Verification

- 34 native Chromium checks pass across Normal, Hard and Furious: complete bomb
  cycles, vertical range, eye/core alignment, at least eight authored spin poses
  in half a second, unchanged HP during observation, committed aim, actual white
  hit pixels/expiry, defensive-clear cancellation, native defeat cleanup and
  decoded charge/fire/impact audio.
- 11 browser review checks pass: all five checkpoints play and seek with audio,
  quarter/half speed, frame stepping, byte-range delivery and no page/console/
  asset errors. The45.22s film fully decodes at30fps; native rendering observed
  about59.6fps, with-8.5dB decoded audio and both complete bomb cycles audible.
- JavaScript syntax checks pass for game.js and the new encounter owner.
- Required `node _BUILD_SOURCE/test_fl.js` still exits1 at its first require:
  `_BUILD_SOURCE/retired_art_archive_1022.cjs` is missing. No assertions or final
  suite summary are reached; no full-suite pass is claimed.

Evidence: `docs/qa/horizon_assault_1025.json` and `_shots/horizon_assault_1025/`.
Reproduce with `_BUILD_SOURCE/probe_horizon_assault_1025.py`,
`record_horizon_assault_1025.py`, `publish_horizon_assault_1025.py` and
`check_horizon_review_1025.py`. No edits to game.js/test_fl.js, commit or push
were made by this pass.
