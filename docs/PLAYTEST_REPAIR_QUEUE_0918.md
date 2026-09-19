# Recorded playtest repair queue — 0918

Source review: the three latest September 18 gameplay recordings in `C:\Users\Mike\Videos`, including Hard and Furious Stage 1 play, Stats, Loadout, and Pilot Select.

## Confirmed repair targets

- Hard Razorback Duo pressure: extended 0919. Sonic, missile and nova attacks take turns with shared recovery that waits for prior waves, Retina locks and missiles to clear; machine guns keep firing. Focused browser simulation passed.
- Furious Razorback: 0919 partial fix inserts a five-second suppression beat between Retina salvos and adds pale contrast to sonic rings and projectiles. Dense warning/explosion overlap still needs a continuous playtest. [Proof](RAZORBACK_FURIOUS_READABILITY_0919.md).
- Achievement notifications and Fury Point conversion compete with the lower Stats sign-off and Continue area.
- Loadout needs controller/D-pad arsenal paging and stronger selected combination feedback alongside its mouse browsing.
- Pilot Select needs its identity typing and one-by-one bar-fill presentation restored before the clean GOOD LUCK launch card.
- Respawn projectile safety: extended 0919. Life-loss respawns clear the incoming lane for the full two-second invulnerability window; distant shots and boss beams remain. The ship stays visibly lit during grace. Focused browser check passed.
- Hard/Furious warning colors need stronger value separation from hostile rounds, explosions, and red enemy palettes.

These are recorded observations; each item retains its own implementation and browser-verification status.

## Additional faults found during browser review

- Early central-turret hits are accepted during Razorback's gun phase, but the turret flash is still gated to the later turret phase.
- The Hard duo exposes one combined health bar without a clear per-tank condition readout.
- Tank-roll cue: dedicated tread and motor loop added 0919 and loaded through the Razorback movement route; browser audio-pool check passed.
- Stats labels `BULLETS FIRED` while formatting `hits / shots`, which describes accuracy counts rather than bullets fired.
- The dense Loadout matrix needs a selected-name/state readout and larger paging; dim opacity alone is weak feedback.
- Pilot Select can briefly show blank ship cells during lazy decode and still omits callsign, special and biography detail from the restored selection view.
