# Corrected modular encounter roster — September 27

Mike corrected the requested new modular boss to Stage 3 and the Earth bomber to Stage 6. Stage 4 also receives a modular remake of its existing boss/warship and helpers. The previous Stage 6 Tempest silhouettes become space spacecraft for Stage 5. These instructions authorize the modular exception to the older whole-plate art rule.

## Implemented

| Encounter | Current implementation |
|---|---|
| Stage 3 boss | Generated Rime Wall hull with two independently destroyable rotating cannon assemblies and two rocket racks. Existing neutral arrival → nuclear transformation → alternating Fire/Ice mechanics remain on Furious. Fire/Ice weak-element rules remain. Stage 3 miniboss is unchanged by this roster correction. |
| Stage 4 miniboss | Generated black/brown Iron Warden based on the current warship. Separate round cannon assemblies, rocket racks, reactor and modular escorts. |
| Stage 4 boss | Generated blue Storm Sovereign based on the current hull, independent guns/racks, animated eight-frame lightning reactor, retained shield-node mechanics and new modular helper art. |
| Stage 4 helpers | Separate hull and gun. Shield protects the gun; an exposed gun can be destroyed while the hull survives. Boss helpers use 96px art with matching collision/Retina dimensions, replacing the oversized inherited 316.8px rig. |
| Stage 5 miniboss | Tempest Void Eclipse (black) and Silver Eclipse (Hard/Insanity) space variants. Half-viewport span, separate engines/forward laser cannons, cyan/purple authored beams and visible bomb bay. |
| Stage 6 miniboss | Existing generated Eclipse Siege Bomber moved to its intended Earth stage. Separate engines/lasers, rearward bombs, northbound giant beams, charge interruptions. Existing alternate Blacksteel encounter remains. |

The mounted weapons share one geometry definition for drawing, rotation, muzzle origins, collisions and Retina targets. Breaking a weapon interrupts the current attack, cancels its beam/warnings, uses the existing explosion system and gives a recovery opening. Destroyed weapons stop firing. The new rigs retain the authored encounter attack books rather than resetting progression to basic aim/fire behavior.

All new image generation used the built-in image generator, not SpriteCook. Source references are the actual authored Rime Wall, Sovereign, Olive Warden and two Tempest hulls. Five generated RGBA sheets live in `assets/game/modular_roster_0927/`. The owning crop/registration workflow is `_BUILD_SOURCE/build_modular_roster_0927.py`, with measured cells in `assets/modular_roster_art_0927.js` and provenance in `docs/modular_roster_art_0927.json`. Crop bounds use alpha to isolate parts; genuine generated alpha is retained. Eight core FX frames share a common anchor/bounds. A rejected overlapping Tempest layout was replaced before integration. Art is registered in `ART_TAXONOMY.json`.

## Difficulty changes

- Easy: enemy HP multiplier .48, projectile speed .65, fire rate .52 and density .62. The encounter HP floor now respects Easy rather than forcing a minimum multiplier of 1. Equipment/life adaptive pressure no longer erases the handicap. New encounter warnings and recovery openings are longer.
- Normal: standard HP, readable pauses and weapon-break recovery. It remains the baseline for player testing.
- Hard: higher encounter durability and faster timing. The silver space-bomber skin appears here.
- Furious: Stage 3 nuclear/elemental mechanics remain. The Stage 8 shapeshifting final form and the full true-ending continuation require Furious (or the legacy higher Insanity mode). Easy/Normal/Hard finish the boss after the preceding form; campaign restoration and the result card remain available.

Measured full encounter HP with the fixture loadout (adaptive threat can change these in an actual campaign):

| Encounter | Easy | Normal | Hard | Furious |
|---|---:|---:|---:|---:|
| Rime Wall | 1,728 | 3,168 | 3,961 | 4,680 |
| Iron Warden | 1,558 | 2,875 | 3,594 | 4,247 |
| Storm Sovereign | 2,112 | 3,872 | 4,840 | 5,720 |
| Space Eclipse | 3,522 | 6,779 | 8,004 | 9,150 |
| Earth Eclipse | 4,300 | 8,326 | 9,825 | 11,237 |

Different encounter mechanics make these HP values unsuitable as a difficulty ranking by themselves.

## Verification

- Final syntax checks passed for `game.js`, both roster files, `encounters_0926.js` and `combat_polish_0927b.js`.
- Full suite: **5,432 passing assertions, 0 failures, final FALVA/LIZZIE success banner, exit 0**. Incoming checkpoint: 5,351/0. Updated obsolete Stage 5/6 roster assertions while retaining legacy Tempest AI tests; added 81 checks for modules, shield protection, compact helper collision, bomber pools, interrupts, Easy scaling and final-form routing. Intermediate stale-roster failures, a malformed new test fixture and the fixture's interaction with the existing no-one-shot rule were resolved; no final failures are hidden.
- Native Chromium: 20 encounter fixtures (five encounters × four difficulties), 42 simulated seconds each, lazy assets yielded/decoded, finite motion, empty page/console error lists. Native hitBoss/hitSubBoss checks independently confirm cannon destruction. Final-form checks confirm Easy/Normal/Hard stop at form index 2 while Furious reaches index 3.
- Six real-time 26-second Chromium canvas recordings: Rime/Furious, Iron/Hard, Sovereign/Hard, space/Normal, space/Hard and Earth/Normal. All retain zoom 1. These are **silent inspection clips with immunity and staged damage/helper activation**, not campaign victories. Source screenshots were inspected; this caught oversized Stage 4 helpers, which were then corrected and re-recorded.
- 36 ordinary-damage automated stage samples, one for each of nine stages × Easy/Normal/Hard/Furious, bounded to 180 simulated seconds. Fresh Yuri MG III / Space Laser III / auto-missile II equipment, independent Arcade stage starts, opening cinematics skipped. Final Stage 4 geometry was rerun across all four modes. No page/console errors and finite projectiles. The large maximum per-frame movements in this sampler include deaths/respawns/rolls; they are not proof of movement jumps or their absence.
- The review page decoded all six videos and its three damage screenshots; every linked resource returned HTTP 200. Native ending checks confirm the standard route skips the true-ending continuation while the Furious-cleared route retains it. Page/console errors remain empty.
- `assets/game.js` remains LF. Both the primary suite and new CJS test remain CRLF.

Local review: http://127.0.0.1:8794/_shots/modular_roster_0927/review.html

Durable machine-readable results: `docs/qa/modular_roster_0927.json`. Temporary logs, screenshots, recordings and reports are under `_shots/modular_roster_0927/`. Reproducible scripts: `probe_modular_roster_0927.py`, `focused_modular_roster_0927.py`, `balance_modular_roster_0927.py`, `review_modular_roster_0927.py` and `build_modular_review_0927.py` in `_BUILD_SOURCE/`.

## Balance findings still requiring play

The sampler frequently lost all lives on Stages 1–2 and 7–8, even on Easy. Stage 7 losses included sluice hazards; Stage 8 losses included lasers and shadow attacks. The controller does not reason about all boss mechanics, so these outcomes are review priorities, not an automatic justification for indiscriminate nerfs. Stage 6 frequently outlasted the three-minute sample; the ordinary-damage bomber clear time needs longer player testing. Stage 3 and 9 clears by this controller do not establish that later stages are correctly harder.

This pass does **not** certify uninterrupted human campaign clears, strict stage-by-stage difficulty progression, every weapon/loadout, physical 8BitDo input, or final balance. Earlier overnight review limits still apply. No commit or push; the previous overnight automation remains paused.
