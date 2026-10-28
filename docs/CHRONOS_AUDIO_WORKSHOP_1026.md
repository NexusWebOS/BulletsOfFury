# Chronos sound workshop — 26 October 2026

The first pass relied on very short fragments and large pitch drops. These 18 candidates retain longer forward passages, dry attacks and more upper-frequency detail.

- Clear: primary material at original pitch.
- Weight: primary material down two semitones; quiet low-frequency support underneath.
- Edge: primary material up one semitone with brighter detail.

## Listen

Open index.html through the local viewer. The comparison reel plays the previous treatment, Clear, Weight and Edge for each of three sound families. Individual charge, release, wave and tail/loop files are included as WAV masters and MP3 runtime candidates. These candidates have not replaced the production charge/wave sounds.

## Integrated lightning

Chronos now uses a dedicated eight-voice pool derived from the actual Dracodia formation beam cue. Pitch is unchanged. The 340 ms strike gets presence shaping and controlled dynamics, then plays once per strike with overlap-aware gain. User master/SFX settings and pause cleanup are preserved. Dracodia’s original file, gain and voice pool are unchanged.

The Kame opener reuses the existing authored eight-frame C42 lightning bolt behind the actor so its new strike sound accompanies a visible bolt. No damage, projectile, HP, attack timing or arena rules were changed.

Chronos-Lightning-Live.mp4 is a fresh, real-time native-engine checkpoint recording with game audio, not an offline sound overlay. It captured 26 rage strikes, one final strike and 12 Kame bolts; all accepted their cue. Decoded video peak: -6.0 dBFS.

## Verification and limits

- All 18 candidates decode to finite audio; oversampled peaks stay below -1 dBFS (loudest -3.52 dBFS).
- All 14 corrected focused native checks pass: once-per-strike, distinct next strike, bounded independent voices, mute, pause cleanup, ordinary wave and Kame opener, and unchanged health/score/projectiles/clock.
- The initial post-recording deduplication check reused a token already consumed in the film. The fresh-token probe corrects that fixture; original raw report retained.
- One known optional stop_empty.png asset is missing in this downloaded build. Recording/probe only use the existing native recovery fallback. No production art replacement was made.
- The full regression suite finishes with five failures. The same five assertions fail with this task’s backed-up pre-audio files loaded in memory.

- and the flash is held long enough for a single hit to register
- dialogue ends with the opening jump warning
- opening jump lands and returns before chromium activation
- unchosen right route persists as the opposite Stage X fight
- Stage X right branch launches a full encounter

## Sources and recipes

The user-supplied source files remain unchanged. No unmodified source files are bundled, and no files were uploaded to a cloud service. Recipes and source hashes are provided for reproduction. Source license metadata was not supplied. This workshop does not make a rights or copyright-free claim.

The lightning changes are local game changes. No GitHub upload or commit was performed in this audio workshop.
