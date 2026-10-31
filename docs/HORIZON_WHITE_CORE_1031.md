# Event Horizon white core cannon and retired bullet markers — October 31

Mike requested removal of bullet-attached asterisks throughout the game, a 1015 white core charge and muzzle flash into level-4 white cannon beams, and continuous synchronized hull/core/spiral rotation.

The original PW5 predictor/collector/draw and the later Part2 collector/draw override are retired. Their public no-op API remains for downstream wrappers; Nightwing's remaining attack code is unchanged. Actual ground/attack warnings, rotation symbols, missile locks, interception and projectile collision remain independently owned.

`assets/horizon_symbiote_1029.js` integrates exactly one unwrapped angular clock at0.60turn/s during every live entry, charge, attack, recovery, half transition and dash/return. The32 hull poses and matching optic masks select from that angle; spiral and sweeping cannon geometry derive from the same angle, with an offset committed at release. Firing starts at the actual core including the existing world float. Pausing freezes the clock. No turn is reset at frame31/0 or at an attack boundary.

The new1288 fixed cells are1024 directional white shaft frames,256 pose-specific white core charge cells and8 white muzzle frames. They reuse the actual `laser_4_pulse_long` centre cross section and native `roundLaserMuzzleArt('#f5f7ff')`, with per-pose EH57 optic masks. Source cells, hashes, palette provenance, manifest and three editable Aseprite sources are in `assets/game/levels/stage_09/miniboss/horizon_white_optics_1031/`. Rebuild with `_BUILD_SOURCE/build_horizon_white_optics_1031.py`; exact PNG reproduction passed. Runtime renders ordinary fixed native frame blits, with no runtime turns/scaling, filters, opacity animation, generated decoration or blend modes added. A filled rotation warning now precedes the rotating straight cannon too.

Native health, alpha contact, hit flash, half-health gate, movement, damage dispatch, ordinary unshootable rounds, defeat and rewards stay with their original owners. Core game.js SHA256 remains `024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de`. The two old test modules now expect retired bullet warnings rather than dereferencing a removed prediction.

Verification:34 native browser checks,15 source/asset checks,1 reproducible export and4 browser playback checks passed (54 total). Syntax checks pass. The mandatory full suite reaches its final summary and exits1 with the same five baseline failures:

- and the flash is held long enough for a single hit to register
- dialogue ends with the opening jump warning
- opening jump lands and returns before chromium activation
- unchosen right route persists as the opposite Stage X fight
- Stage X right branch launches a full encounter

Current full Furious film: 163.034s, original10965HP, 58.91 nativefps, half transition and all six attacks through actual native defeat. Invulnerable input-only observer; no recorder HP/phase/timer writes. Zero bullet-marker draws, browser/render/asset errors or media decode errors. Charge/release/sustain/orb/boost/half audio played; decoded mean -19.0dB and peak -2.4dB. This validates native presentation/ownership, not a claim that every pattern has been human-beaten without GOD.

[Current fight](http://127.0.0.1:51046/?horizon=white-core-1031#clip=stage9-miniboss). Local full movie: `C:/Users/Mike/Documents/New project/BOF-Downloaded-Stage6-9-1028/videos/stage9-horizon-white-core-1031.mp4`. The previous movie remains archived in the manifest. The28s opening preview shows attacks before player firing. Existing enemy-showcase footage is a previous build snapshot; it was not re-recorded by this pass.

No paid generation, commit or GitHub push. Other bosses and their art are outside this change.
