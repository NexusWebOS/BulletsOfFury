# Chronos foreground audio correction — 26 October 2026

Mike still could not hear rage charging and could barely hear the wave. The previous short proof omitted rage; the production SFX default0.40 and full-volume music also left foreground energy too quiet.

This pass retains pitch and re-masters the Clear source bodies with presence EQ, compression and a bounded limiter. Native energy gain is1.8 before the user's SFX/master mix (release/tail1.25 with their role gains). Live SFX/master changes, mute, pause/death/owner cleanup and user preferences are preserved. Charge voices use seam-treated looping files until their actual native release. Music temporarily uses0.22 of its configured gain; lightning keeps every native strike at0.24 backing gain during foreground energy. Music restores when energy ends, is muted, or leaves its owner.

The new proof includes actual rage and wave excerpts from one native checkpoint capture, with original captured game audio. It has no replacement audio overlay. Native average frame rate and decoded peak are recorded in verification.json; no60fps claim. Recording uses the previously disclosed native recovery fallback for a missing optional stop_empty.png, only in the browser session. Production art/combat timing/HP/projectiles were not edited.

Actual per-cue audio is measured against BOTH music and lightning.21 focused checks cover looping, once-per-cycle, music duck/restore, live mute, saved preferences, cleanup, bounded voices and unchanged combat state. See verification.json for the completed required suite and unchanged baseline failure names. The first attempted ducking change failed on a private helper reference; a local helper corrected it before the delivered film. Failed raw take retained.

Lossless pre-masters, masters, exact filters and source hashes: _ART_SOURCES/chronos_energy_mix_1026. Owning encoder: _BUILD_SOURCE/build_chronos_energy_mix_1026.py. Original user-provided sources and earlier audio packs remain unchanged. No cloud upload, commit or GitHub push. No physical speaker/headphone listening claim; Mike reviews the delivered sound.
