# Stage 6/7, campaign and beam repair — September 29

Mike's request: upright toxic doorway, anomaly introduction and jammed radar,
ground-anchored Warden wreck, conditional comms, fast warned opening jet gates,
animated elemental lasers, and strict per-campaign collected upgrades.

`assets/mission_repair_0929.js` loads after HAMA's current art/encounter owners.
The shared `drawBullets` renderer delegates infused held beams to the nine
September 28 authored reels. Fire Whip keeps its distinct existing attack.
Both the live weapon and Forge preview use this renderer; collision, widths,
damage, element mechanics and base beam tiers remain owned by the engine.

The Stage 6 live opening transitions from the existing enemy-free cloak dialogue,
shootable intercept and Harrier flyover into an independent assault sequence.
It occupies `s6Opening` with `phase: 'assault'`: ordinary waves and stage progress
wait, while the sky, missiles, rolls, somersaults, weapons and collisions run.
Right-to-left and left-to-right row gates leave one row safe; bomber passes
use only committed ground retinas; descending gates leave two or more lanes safe.
Normal/Hard gate jets do not fire. Furious adds selected paired guns and bombs.
Numbers/speeds/warnings scale by difficulty; the normal director resumes after
the authored jets and their blast warnings have cleared.

Comms prefer Decker, substituting Cole when Decker is the solo pilot; other
Cole/Maverick calls similarly avoid solo self-warning. Co-op allows the named
pilot to speak naturally, including a Decker/Cole pairing.

Stage 7 has a seven-second darkened anomaly beat with authored green explosion
reels and explosion audio, shared comm window and generated animated radar static.
The Warden emerges from its original upright 16-frame toxic doorway. That same
doorway is used for escape and the Stage 8 arrival; no ground seal or circular
warp substitutes. The death pose is frozen, moves with terrain source coordinates,
and leaves the viewport as the pilot advances rather than chasing the pilot.

Campaign Forge no longer imports profile recipes/elements. Profile records remain
available to the Armory and arcade. Fresh campaign state clears infusion,
forms, discovery, pending element rewards, loadout, NG+, seed flags and rival state.
Mist/chaingun/Yuri Orb unlocks are saved on the campaign. Old saves infer these
only from their own completed Stage 5/9 and Yuri Stage 4 rank records. Yuri in
co-op seat two retains the shared campaign-earned Orb gate; preview permissions
are isolated from the actual run. Existing collected forms/elements in
a save remain valid. Manual slots and global achievement/profile records are not
erased. Cole's session password behavior is retained.

Generated source provenance is in `_ART_SOURCES/mission_repair_0929/`.
The owning builder creates eleven lazy families / 43 frames: radar (4), blue jet
cardinal views (3), and nine beam reels (36). It slices/packs authored pixels and
derives beam ink bounds from the original animation-pack metadata.

Verification:
- `node --check assets/game.js` and addon syntax passed.
- Full `_BUILD_SOURCE/test_fl.js`: 5,817 passing checks, zero errors.
- Real Chromium `_BUILD_SOURCE/probe_mission_0929.py`: 45 passing, zero failures;
  natural launch/cloak/Harrier/assault, Normal/Hard unarmed gates, Furious mixed
  pressure, correct solo comms, all four radar frames, three authored jet views,
  upright portal frames, ground-anchored escape, nine four-frame beams, actual
  held firing, real Forge previews with unchanged campaign state, and co-op Orb.
- Captures and structured results: `_shots/mission_0929/qa.json`; suite/native
  logs in `_shots/mission_0929_suite.log` and `_shots/mission_0929_native.log`.
- Final diff checked for whitespace and UTF-8 preservation. Prior HAMA art,
  cue timing, regular moonwalk appearance, and its existing edits are preserved.
The native probe uses immunity only to observe complete patterns, not as evidence
that Furious is easy or that every player can survive the sequence.
