# Retina component targeting — 0914

Retina taps cycle among live electrical nodes and independent helpers instead of a shielded boss hull. Stage-6 missile bays become targets during shield-down windows; the core becomes selectable after the bays are destroyed. Destroyed components, shield reformation and arrivals invalidate existing locks. Target wrappers preserve component identity and follow current drawn coordinates without replacing authored boss plates.

Manual missiles route damage to the chosen node, bay or helper. Seeking missiles and space weapons share the eligibility list. Ordinary shots can still strike and weaken shields; protected hulls are excluded from lock selection.

Verified in real Chromium: Stage-6 cycling across four nodes, a launched missile spending one ammo and reducing selected-node HP while leaving carrier HP unchanged, open-bay eligibility, exposed hull and shield reformation. Stage-4 selection includes all four nodes and both mounted helpers. Authored Retina frames were inspected through XART and the game context's drawImage. Native probe: 12 passed, zero page/console/controlled-loop errors.

Full suite reached its final summary: 3,771 passed, 60 failures, exit 1. No new failing assertion names compared with the recorded 61-failure baseline; the historical random sand-tank assertion passed this run and is not claimed as fixed. Runtime LF and suite CRLF preserved; sources reproduce the runtime. Proof: docs/qa/retina_targets_0914.json.

The combined 19-second blue-laser/pause video contains 570 decoded frames with native effects and voice audio. Overlapping death explosions originally clipped; the live sound engine now applies explosion gain and retrigger limits. Corrected peaks are 0.676 and 0.774 without export normalization. Green pause cursor, grayscale playfield and actual Autosav01.json SAVED record were visually reviewed. Autosave records remain browser localStorage data, separate from manual slots.

Directional multi-lock upgrade, its five-second expiry and sequential firing, the universal no-one-shot rule, Hard/Furious encounters, missile tier assets and achievements remain pending. New SpriteCook assets cannot be produced until its authenticated tools are available.
