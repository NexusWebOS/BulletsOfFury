# Maneuverability QA

The production fixes are in assets/maneuver_safety_1007.js and the two owning ram/warning controllers. Use ../maneuver_release_1007.json with ../maneuver_safety_v2_1007.py for the final affected-build screen. Use ../maneuver_tactics_1007.json with ../maneuver_tactics_1007.py for the separate targeting profile. Keep these profiles distinct.

The three JS files here preserve the final experimental ram overlay and helper source. Candidate runners use local HTTP interception; their historical datasets remain experimental evidence. Shipped-build probes need no overlay arguments. Re-running an old case on current code does not recreate the old build. Runtime hashes and source groups accompany the portable QA; some early experimental captures predate the warning-render fix.

See ../../docs/MANEUVER_SAFETY_1007.md for all commands, caveats and open findings. Do not interpret protected fixtures, form transitions, or zero-HP carrier transitions as complete unassisted clears. No human trial data has been fabricated.
