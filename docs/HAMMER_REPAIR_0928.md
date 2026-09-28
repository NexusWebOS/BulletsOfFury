# Chromium activation and hammer recovery counter

HAMMER's soundtrack cue previously reset an unfinished Chromium activation to the idle hammer pose. The cue now waits for activation, stun, final twirl and protected restoration counterplay to finish. Chromium activation records completion before normal combat or the musical break can resume.

The armor barrier previously swallowed a hit on the exposed healing hammer before the recovery damage handler ran. A guided rocket striking the selected hammer now immediately cancels the heal, revokes the healing already granted and enters the existing stun response. Passive weapons can still damage the exposed hammer core while the body wall remains active. Front-facing body hits remain blocked.

Guided rockets and space volley missiles retain their selected boss/body/hammer target while taking a path outside the energy wall, clearing its upper edge and then turning inward. Rockets arriving by this path can damage the boss through the protected body phase. Volley missiles locked to the hammer do not detonate on the boss body before reaching that hammer. Ordinary encounters keep their existing missile movement.

## Verification

Native Chromium reproduction before the change confirmed that a 24-damage rocket left the healing hammer's 24 HP unchanged; the musical cue also reset activation at 1.21 seconds. `_BUILD_SOURCE/probe_hammer_repair_0928.py` subsequently verified regular Stage 5 and HAMMER on Furious, both ordinary and critical healing, body hits after flanking, passive volley core damage, and full activation across the soundtrack cue. Four guided healing shots cancelled their respective heal, both body shots dealt 24 armor damage, volley shots reached the core without reflection, and no page errors occurred. Flight screenshots and reports are under `_shots/hammer_fix_0928`.

Regression coverage also checks that the wall still rejects front-facing body rockets. Local game and the playable ZIP include these changes; no GitHub push is included.

The full regression suite finished with **0 errors**. The same native scenarios passed against the compressed release. Updated ZIP: **498,534,304 bytes**; archive CRC and runtime-script checks passed.
