# Stage 5 hammer consistency and strike recovery — September 26

Mike rejected the double-ended hammer and the repeated overhead pose. The active strike and whirlwind reels now use the canonical single blue cylindrical hammer head from `leap_strike_0922.png`.

The new twelve-pose strike reel covers lowered idle, lifting, wind-up, crouch, jump, apex, downward strike, impact, lateral follow-through, lowering, settling and idle. Regular strikes and Furious orbital strikes share it. The eight-pose whirlwind replacement uses the same weapon. Both PNGs retain the generated RGBA unchanged; explicitly measured source rectangles isolate poses without cutting across the generator's uneven gutters. Superseded PNGs remain on disk but are no longer the active XART sources.

The repeated-strike controller previously entered `warn` immediately whenever `comboPending` was true. It now holds lowered idle for 0.55 seconds on Normal, 0.40 on Hard and 0.30 on Furious before beginning a new wind-up. Impact recovery actually lowers the weapon; the return flight also keeps it lowered. Existing difficulty-owned strike counts remain two, four and six respectively.

Furious orbital strikes now go through lowered idle (0.46 seconds), wind-up (0.48 seconds), rise, warning, dive, impact/sweep, and lowering recovery. Recovery brings the boss back to the upper arena so his next lowered pose is visible above the HUD. Both orbital strikes follow this sequence. The existing missile counter and shared warnings remain active. Hammer lock targets, direct module hits and break explosions follow the animated head position.

Assets and exact built-in image-generation prompts: `docs/hammer_consistency_art_0926.json`. The active files are `assets/game/stage5_archmage_0916/combat_0926/hammer_strike_v2.png` and `whirlwind_v2.png`.

Verification:

- `node --check assets/game.js` passed; game LF and suite CRLF preserved.
- `_BUILD_SOURCE/probe_hammer_consistency_0926.py --record` passed in real Chromium: all Normal/Hard/Furious repeated cycles, lowered idle holds, ordered wind-up/jump/recovery poses, aligned module hits and lock targets, both orbital repeats, return to the upper arena, and missile counter. All twelve strike source rectangles have clear edges. Zero page or console errors.
- `_BUILD_SOURCE/probe_hammer_authored_0926.py` passed the existing beam collision, safe-lane and locked-spell regressions.
- Reviewed actual game-canvas pose sheets and sampled recordings. `_shots/hammer_consistency_0926/review.html` presents nine seconds of Normal, fourteen seconds of Furious repeated strikes, and fourteen seconds of Furious whirlwind/orbital strikes. These are invulnerable attack-inspection fixtures with muted audio, not complete campaign playthroughs.
- First complete suite run: 4,957 passed, zero failed, exit 0 (`_shots/test_fl_hammer_consistency_0926.log`). After the recovery-position adjustment, a complete run exited 1 with two jet-table failures: `s1jetbomber_b strafes when a tracking round closes (0 frames)` and `s1jetbomber_b actually leaves its lane to do it (0px)`. Both differ from the zero-failure baseline. Section 210 uses an unseeded live-world fixture; Stage 1 gameplay and that fixture were not modified by this hammer correction. The failing log is preserved at `_shots/test_fl_hammer_consistency_0926_final.log`.

- An unchanged-code full-suite recheck then completed with **4,957 passed, zero failed, exit 0**, including both jet-dodge assertions (`_shots/test_fl_hammer_consistency_0926_recheck.log`). The intermittent failed run above is retained, not discarded or represented as passing.

Nothing committed or pushed.
