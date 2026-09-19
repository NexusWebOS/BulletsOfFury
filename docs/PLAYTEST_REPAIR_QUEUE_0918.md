# Recorded playtest repair queue — 0918

Source review: the three latest September 18 gameplay recordings in `C:\Users\Mike\Videos`, including Hard and Furious Stage 1 play, Stats, Loadout, and Pilot Select.

## Confirmed repair targets

- Hard Razorback Duo pressure: extended 0919. Sonic, missile and nova attacks take turns with shared recovery that waits for prior waves, Retina locks and missiles to clear; machine guns keep firing. Focused browser simulation passed.
- Furious Razorback: 0919 partial fix inserts a five-second suppression beat between Retina salvos and adds pale contrast to sonic rings and projectiles. Dense warning/explosion overlap still needs a continuous playtest. [Proof](RAZORBACK_FURIOUS_READABILITY_0919.md).
- Achievement notifications and Fury Point conversion compete with the lower Stats sign-off and Continue area.
- Loadout needs controller/D-pad arsenal paging and stronger selected combination feedback alongside its mouse browsing.
- Pilot Select: role, callsign, affiliation, biography, sequential stat bars and boxed special icon restored 0919; GOOD LUCK retains only the pilot and ship. [Proof](PILOT_SELECT_DETAILS_0919.md).
- Respawn projectile safety: extended 0919. Life-loss respawns clear the incoming lane for the full two-second invulnerability window; distant shots and boss beams remain. The ship stays visibly lit during grace. Focused browser check passed.
- Hard/Furious warning colors: 0919 partial fix gives the final red FOV/alert a cool-cyan edge. Dense overlap in other encounters remains to be tested. [Proof](HARD_FURIOUS_WARNING_CONTRAST_0919.md).

These are recorded observations; each item retains its own implementation and browser-verification status.

## Additional faults found during browser review

- Early central-turret targeting: fixed 0919. Point hits already damaged/flashed it; laser beams and Retina targets now include it while the front guns remain. The authored white turret overlay was inspected in Chromium. [Proof](RAZORBACK_EARLY_TURRET_0919.md).
- The Hard duo now exposes two individual miniboss health bars, one per tank; the earlier combined-bar observation predates the current build.
- Tank-roll cue: CC0 recorded rolling texture blended into the motor loop 0919; Chromium verified the Hard duo keeps the loop alive while either tank moves. [Proof](RAZORBACK_TREAD_RECORDING_0919.md).
- Stats `BULLETS FIRED` now formats the shot count directly; `WEAPON ACCURACY` separately formats hits / shots. The earlier label mismatch predates the current build.
- The dense Loadout matrix needs a selected-name/state readout and larger paging; dim opacity alone is weak feedback.
- Pilot Select can briefly show blank ship cells during lazy decode and still omits callsign, special and biography detail from the restored selection view.
