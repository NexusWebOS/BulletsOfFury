# Herald restoration and original enemy warnings — October 3

Mike asked to apply the original warnings and Retinas to all affected enemies,
then confirmed: restore Herald of Death, regenerate it at higher quality and make
it modular. This explicitly extends the modular-art exception to this miniboss.

## What happened to the miniboss

The September 13 change stored `heralddeath` in `ALTBOSS[8]` and left `SUBBOSS[8]`
empty. The September 14 integration retained that choice. The original art and
encounter were never deleted. See `docs/PASSOVER_TEMPEST_LEVIATHAN_0912U.md` and
`docs/GITHUB_BUILD_0914.md` for the historical decision.

`assets/herald_1003f.js` now assigns that identity to the existing Stage 8 halfway
gate (45% clock, scroll 1201). The alternate entry and historical art remain on
disk. Stage 8's normal moving backdrop continues, while its wave clock pauses
during the miniboss. Defeat resumes the stage and leads into the eight-form
modular finale without changing that fight.

## Original warnings everywhere

The mutants called `s81003Fov` without passing their emitter. The adapter defaulted
to `boss`, which is null during ordinary waves: some lanes disappeared. With a
boss present, they could take the boss-art path instead of the enemy-band path.

- Every mutant and alien passes its actual enemy owner.
- The shared implementation in `stage8_1003.js` uses `combatWarningDraw` and
  `groundTargetReticleDraw` directly. It no longer needs a late finale override.
- Stage 7/8 enemy preloading includes the original warning and reticle assets.
- The custom sheet's warning cells 0–7 have no live callers. Its separate
  projectile cells 8–11 remain in use.
- Enemy bands, boss FOV/alerts, committed aim and original warning colors remain
  distinct according to the established system. Code walls and beam art remain.

## Regenerated modular Herald

Built-in image generation produced a transparent six-component kit. Source and
exact prompt: `_ART_SOURCES/herald_1003f/parts.png` and `generation.json`.
Runtime copy: `assets/game/herald_1003f/parts.png`. Source pixels and alpha are
unchanged; `build_herald_1003f.py` owns measured rectangles, pivots and registrations.

- Separate core, skull, left/right wings and left/right cannon arms.
- Upright body, articulated wings, aimed cannons and independent recoil/flashes.
- One geometry definition drives drawing, component collisions, Retina targets
  and weapon origins. Empty gaps do not consume normal shots or hurt the pilot.
- Cannon destruction removes its volleys; wing destruction removes its beam and
  reduces lateral movement. The skull receives 20% extra damage; the core stays
  vulnerable, so remaining attachments never prevent finishing the encounter.
- Skull fans, sequential skull salvos and paired wing beams use original warning
  art. Easy omits wing beams. Hard/Furious increase volley density with committed
  targeting and recovery windows.
- Existing authored projectiles, sounds and explosion effects are reused. Defeat
  ejects the actual components in timed beats before the native miniboss reward
  and stage-resume path completes.
- Existing Stage 8 HP floors and co-op scaling apply before module pools are set.

## Verification

- Syntax checks passed, including `node --check assets/game.js`.
- Full suite: **6,952 passing assertions**, final build banner, **exit 0**.
  Previous baseline: 6,917; this pass adds 35 assertions.
- `probe_enemy_warnings_1003f.py`: **25 passing native Chromium checks**. All seven
  mutants and all three aliens, all warning phases, Normal/Furious, with and
  without a live boss; actual game-context pixels and real wave rosters.
- `probe_herald_1003f.py`: **27 passing native checks**. Natural scheduler on all
  four difficulties, six rendered components, live attacks, moving Retina missile
  impact, normal-shot module damage, disabled weapons, skull damage, gap/contact
  collision, modular destruction and transition to the existing finale.
- Original-warning/Stage X regression: **13 passing native checks**, including
  actual Gasline playback. Zero page/console errors in these runs and the replay.
- Screenshots inspected. Local review includes an actual-engine video, captures,
  component sheet, warning examples and a playable isolated Furious miniboss.
  Desktop/mobile layout, 27.8-second video metadata and actual playable launch
  verified with no page/console errors. The first review launch check exposed an
  obsolete BOFGAME readiness flag; it now waits for the real BOFDEBUG API.
- LF in `game.js`, CRLF in `test_fl.js` and `index.html` preserved. Whitespace
  check passes with `cr-at-eol`, respecting the existing CRLF files.

The first Herald probe incorrectly required the flying backdrop to stop, even
though the wave clock correctly paused; four assertions failed. The test was
corrected to the existing Stage 8 behavior and rerun. A subsequent visual/collision
review found the inherited broad player-contact rectangle; the runtime now checks
the live modular shapes, verified with both empty-gap and real-core contact.

These are controlled fixtures, not a full campaign clear or final balance rating.
Review: `http://127.0.0.1:8794/_shots/herald_1003f/review.html`.
Portable evidence: `docs/qa/herald_warnings_1003f.json`.
No commit, push or external publication; all earlier dirty work retained.
