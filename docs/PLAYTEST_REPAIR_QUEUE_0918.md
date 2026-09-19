# Recorded playtest repair queue — 0918

Source review: the three latest September 18 gameplay recordings in `C:\Users\Mike\Videos`, including Hard and Furious Stage 1 play, Stats, Loadout, and Pilot Select.

## Confirmed repair targets

- Hard Razorback Duo attack scheduling can stack sonic releases and missile locks without enough shared recovery.
- Furious Razorback rocket pressure and red-on-red effect density reduce both survival space and visual readability.
- Achievement notifications and Fury Point conversion compete with the lower Stats sign-off and Continue area.
- Loadout needs controller/D-pad arsenal paging and stronger selected combination feedback alongside its mouse browsing.
- Pilot Select needs its identity typing and one-by-one bar-fill presentation restored before the clean GOOD LUCK launch card.
- Respawns can return into hostile lower-screen patterns; the safety window needs projectile handling as well as invulnerability.
- Hard/Furious warning colors need stronger value separation from hostile rounds, explosions, and red enemy palettes.

These are recorded observations and remain pending until implemented and re-recorded in the native browser.

## Additional faults found during browser review

- Early central-turret hits are accepted during Razorback's gun phase, but the turret flash is still gated to the later turret phase.
- The Hard duo exposes one combined health bar without a clear per-tank condition readout.
- The tank-roll cue currently reuses a low-passed aircraft engine loop; a purpose-built tread/roller loop remains required.
- Stats labels `BULLETS FIRED` while formatting `hits / shots`, which describes accuracy counts rather than bullets fired.
- The dense Loadout matrix needs a selected-name/state readout and larger paging; dim opacity alone is weak feedback.
- Pilot Select can briefly show blank ship cells during lazy decode and still omits callsign, special and biography detail from the restored selection view.
