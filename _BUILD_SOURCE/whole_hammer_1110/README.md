# Whole hammer runtime/native review

Production owners: assets/boss_animation_1109.js (size-aware atlas/attack timelines) and assets/whole_hammer_1110.js (whole-held alpha, release and catch). Art ownership: _ART_SOURCES/whole_hammer_1110/.

Run verify_combat.py for38 native combat/hit checks. Run record_hammers.py for the held/released/catch contract and real RAF/audio previews of both regular and chromium Furious attacks, then actual thrown-weapon flight. The god observer does not fire. Fixtures are review-only and never loaded by index.html. Normal/Hard/Furious contact counts remain1/2/4 with one initial jump and planted follow-ups. Existing HP, difficulty, audio, death/reward and charged-counter ownership are retained.

The full suite remains blocked by the existing missing difficultyHealthBaseline15 helper in combat_polish_0927b.js:151; see docs/qa/whole_hammer_full_suite_1110.txt. No full-suite-green claim. No new installer, archive, commit or push.
