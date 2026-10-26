# October25 barrage readability and Herald flights

Review: [current clips](previews/barrage_revision_1025/index.html). Eight chapters,
six new audible native films. The three Herald chapters share one continuous
52-second film. Earlier recordings remain available; they predate these fixes.

| Encounter | Current behavior |
|---|---|
| Stage3 | Scenery-only black lighting at0.46 strength, after the background pass. The original ice terrain, water clocks and outlines remain. Projectiles, warnings, aircraft and HUD retain their native brightness. Same-frame before/after comparison is included. |
| Stage6 Siege Fortress | Removed the added battery barrage scheduler. All six laser batteries keep their native attacks. Only the exposed reactor receives the added barrage, between complete battery/missile turns. The native all-six-batteries gate, complete HP pool, reactor attacks and miniboss defeat remain. |
| Stage7 Caustic Dredger | Fans use the actual four barrel apertures in each authored gun assembly, with attached toxic muzzle flashes. The previous centre-bottom socket was between barrel mouths. Successive barrage turns alternate with sludge from the top liquid opening: warned arcing lobs, splash, then outward toxic rounds with committed dodge sectors. |
| Stage8 Herald | Round animated red chaos replaces the faint feather rounds. Claws emit the barrage and energy flashes. New warned corner swoops change heading/depth and animate the existing wings. Two Furious bomber passes release red bombs from surviving claws; warned bursts retain a dodge sector. Broken claws cancel their pending bombs, shots and flashes. Native core/head last stand, damage, Retina, white hit feedback and breakup remain. |

Herald's faster bomber revision is documented in
[Herald speed](HERALD_SPEED_1025.md): roughly 4.7 times faster passes,
rapid paired-claw drops and a newly recorded film. Current bomber checkpoints:
warning 0:17.1, fast pass 0:18.6, red burst
0:19.2, return 0:23.5. Gallery buttons use the
current film. The Dredger top-lob film retains its complete four-shell Furious turn.

## Ownership and art

`assets/bullethell_1025.js` owns the reactor interlock, measured Dredger sockets,
turret flashes and bounded dorsal lob turn. Native `tb28` owns its arcs/reticles.
`assets/herald_bomber_1025.js` owns the new Herald flight book, claw sockets,
ordinary red energy, muzzle attachment and Stage3 scenery lighting. Existing
module HP, hit detection and death owners remain authoritative.

The red orb is a palette variant of the eight existing authored
`bpfx_proj_void` frames. All source alpha, neutral armor/outline pixels and bright
glints are preserved. The whole bank uses128×128 cells and a64,64 pivot. Builder:
`_BUILD_SOURCE/build_herald_chaos_1025.py`; registry:
`assets/herald_chaos_art_1025.js`; provenance:
`assets/game/levels/stage_08/miniboss/herald_chaos_1025/manifest.json`.
No generated replacement hulls or paid asset jobs were needed.

Every new launch uses the shared mixer/retrigger gate. Dredger uses
`bossfireSludgeemperor` and `combatToxic0927` (the existing toxic-spit alias);
Herald uses `bossfireVileexistence`, `combatOrb0927`, `jetDash` and the native
charge cue. Fans have one audible launcher. Cancelled launchers retain no delayed
release. Ordinary energy is unshootable from birth and keeps defensive clears.
Projectile budgets are capped at128; warnings commit their openings before fire.

## Verification

- The preceding readability pass had 48 native Chromium checks pass, including actual scenery/projectile pixels,
  measured opaque barrel mouths and liquid opening, visible muzzle and hit
  flashes, native flash expiry, decoded attack audio, short return rotations,
  native reactor gate and destroyed-launcher cancellation.
- 34 review-browser checks pass: eight chapters, play/decode/seek with audio,
  frame stepping, slow motion and byte-range requests. No page, console or asset
  errors. Six films fully decode, with sound peaks between-8.5 and-6.7dB and
  observed native rendering near60fps.
- `node --check` passes for game.js and all three affected/new runtime registries.
- Required `node _BUILD_SOURCE/test_fl.js` exits1 before assertions or final
  summary: `_BUILD_SOURCE/retired_art_archive_1022.cjs` is missing. This is the
  recorded pre-existing suite blocker; no full-suite pass is claimed.

Observation films retain native enemy HP/phases and use an invulnerable movement
bot; Stage6 companions attack normally. Explicit native-damage/cancellation
fixtures are separate. Human difficulty still needs player review.

Evidence: `docs/qa/barrage_revision_1025.json` and
`_shots/barrage_revision_1025/`. Reproduce with `probe_barrage_revision_1025.py`,
`probe_barrage_sockets_1025.py`, `record_barrage_revision_1025.py`,
`publish_barrage_revision_1025.py` and `check_barrage_revision_1025.py` under
`_BUILD_SOURCE/`. This pass did not edit game.js or test_fl.js, commit or push.
