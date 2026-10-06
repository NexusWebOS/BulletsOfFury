# October 6 — Stage 8 form animation and AI completion pass

The copied Code Hammer now shows the approved black/chrome/crimson robot in its actual curl, spiked ball, unfold, giant slam, whirlwind turn and weapon-loss states. Sixteen additional authored cells fill those gaps; throwing or losing the hammer no longer leaves another hammer baked into the body. Giant poses follow the source controller's approach/impact scale, and the curled ball follows its rotation.

The knight chooses its move book by distance and remaining equipment, avoids immediate repeats, and cancels a sword/shield attack when that weapon breaks. Furious adds a fresh warned shield smite after the downward/rising sword combo, or a sword followup if the shield is gone. Its charged code fire alternates three-way aimed and four-way split volleys; each of the three bursts has a full 1.15-second warning. Aim is committed per warning. The original side-edge Armageddon retinas, direction glyphs and collapsing eruptions remain.

## Copied-form coverage

| Identity | Authored graphics used | New followup / behavior |
| --- | --- | --- |
| Colossus / host, pool 0 | Existing modular colossus, code/void and claw effects | Furious adds one separately warned claw echo during each existing signature; committed target, same five-signature book. |
| Code Chopper, pool 1 | Existing core, tail, gun arms, racks and spinning rotor | Crossgun fan with an open central gap. Native sonic/rush/sweep sequences defer extra volleys. |
| Code Furnace, pool 2 | Existing modular chrome/crimson Furnace and authored magma ordnance | Alternating magma relay from actual surviving arm emitters. Cannon telegraphs allow it; beam tells/active beams defer it. |
| Code Cryo, pool 3 | Existing modular ice ship, racks/cannons and shootable ice rounds | Open-center ice gates. Broken emitters stop contributing shots. |
| Code Storm, pool 4 | Existing modular storm ship, racks and lightning barrel | Alternating raking code fans from the live mounted weapons. |
| Code Knight, pool 5 | Prior 12 intact body poses, four separate sword/shield states, eight eruption and eight code/impact cells | Distance/equipment choices, warned Furious followup, three independently warned code bursts, immediate disarm cancellation. Shield remains non-reflective. |
| Code Carrier, pool 6 | Existing fans, racks, beam emitter and authored targetable missiles | Split missile pincers. Native beams, dash and desperation defer additional casts. |
| Code Warden, pool 7 | Existing modular legs/claws/turrets and toxic ordnance | Alternating left/right claw relay. |
| Code Hammer, pool 8 | Prior approved Hammer plates, detached red hammer and 16 new motion cells | Full source armor, restoration counter, ball, whirlwind, giant strikes, throws and emergency reserve preserved. Furious returns the sideways swing after another warning, then recovers. |

Normal has one donor followup burst, Hard two and Furious/Insanity up to three. Each burst is separately telegraphed. Busy source attacks defer these additions to avoid overlapping beam phases. Native controllers retain their own animation clocks; this pass removes the old blanket 1.08 time multiplier. No new HP budget, outer encounter, reward or campaign unlock was added.

The first mutated-vessel and ghost encounters keep their authored attacks and cinematic reforms. Furious changes their attack order to introduce the physical roll, warp, rail and claw sequences earlier, then revisits those sequences. Final copied health and destroyed equipment stay in nine independent pools. Form changes clear pending casts and owned shots. Co-op snapshots alternate live players and restore the active seat.

## Generation and integration

- Built-in `image_gen`, using `_ART_SOURCES/hammer_knight_1005/hammer.png` as the identity/style reference. No back-mounted chaingun.
- Exact prompt, reference and output recorded in `_ART_SOURCES/finale_motion_1006/generation_manifest.json`; selected native source is `hammer-motion.png` in that folder.
- `_BUILD_SOURCE/build_finale_motion_1006.py` extracts measured source rectangles with transparent padding. All visible RGB pixels and alpha values are preserved; RGB under completely transparent pixels normalizes during compositing. No repaint, palette changes, resampling or broad atlas edits.
- Deployed cells: `assets/game/finale_motion_1006/hammer_motion_0.png` through `hammer_motion_15.png`. `assets/finale_motion_art_1006.js` registers dimensions, measured reactor pivots and hammer-head anchors. Existing 49 Hammer/knight/effect cells remain intact.
- Runtime: `assets/finale_ai_1006.js`, loaded after the prior Hammer/knight layer. `assets/game.js` has no new edits from this pass.

## Verification and limits

Final verification: 7,407 regression assertions, final success banner, exit 0; 42 native Chromium checks pass with zero browser/renderer errors. All 16 extracted cells preserve their visible source RGB and alpha and match the recorded hashes. Syntax and whitespace checks pass. Verification results are finalized in `docs/qa/finale_ai_1006.json`, `docs/qa/finale_followups_1006.json` and `docs/qa/finale_completion_1006.json`. The required full suite and syntax checks accompany protected native Chromium checks, actual projectile release for every donor family, equipment cancellation, co-op targeting, visible animation contacts and error capture. The native pass caught and repaired Furnace relay starvation; state-only plan assertions had missed it.

Review: `_shots/finale_ai_1006/review.html`. New motion contact includes all 16 poses; silent native clips show the Furious Hammer chain and knight code volleys. Passwords remain `HAMR8`, `KNIGHT` and `FINAL3`.

These are protected fixtures, not unassisted Furious clears or proof of final human balance. Full encounter pacing and creative approval still benefit from Mike's playtest. Earlier dirty work, unrelated staging, stash and source art were preserved. Local only; not committed or pushed.
