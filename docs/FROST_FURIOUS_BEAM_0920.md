# Stage-3 Furious blue beam — 2026-09-20

The Furious Rime Wall's Simon-Says cannon sequence now commits to one 62-world-pixel beam after its yellow/red FOV beats. The release uses `assets/game/bosses/frost/frost_furious_beam_0920.png`, a dark-navy, royal-blue and pale-ice palette swap of the regenerated Furnace laser plate. `_BUILD_SOURCE/palette_frost_furious_beam_0920.py` preserves the source pixels and alpha. The warning receives the same width as the active hit corridor. The beam still originates at the selected authored cannon mount and uses the existing commitment timing.

The Furious Frost Cruiser miniboss reuses that plate for its nose sweep, replacing the green-looking reel on that difficulty alone. Normal and Hard retain their existing beam art. Neither attack changes its movement or damage calculation.

`_BUILD_SOURCE/probe_frost_furious_beams_0920.py` captured the real Chromium canvas in `_shots/frost_furious_beams_0920/`: the Rime Wall warning, enlarged blue cannon beam and Frost Cruiser nose sweep all rendered with decoded hull and plate assets. The warning lane visibly points down from the cannon that later fires. The probe recorded no page or console errors. `node --check assets/game.js` passed. The complete assertion suite exits nonzero against its legacy baseline: first run had 77 failing names including the intermittent Stage-1 three-drone lance fixture; the repeat had exactly the recorded 76 failing names and no added name (`test_fl.log`, `test_fl_repeat.log`).

The remaining Furious Rime Wall pass includes the requested black/blue hull plate and Hard-pattern parity; those have not been marked complete by this beam work.
