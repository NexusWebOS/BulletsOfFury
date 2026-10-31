# Dracodia Luminaire — October30

Dracodia's chest orb now charges an expanding rounded warning while a lower field rises like water. The release is a blinding violet-white void-light field. Escape slightly above the halfway mark and to either side of him. The existing claw combos remain; every third main-body decision is Luminaire, including the armless phase. First host and copied forms retain their owners.

The warning is fixed to the native680x512 world, centred on the actual chest socket at approximately340,160. Camera movement does not drag it. The final region is the rounded164px orb bloom united with the rising lower field, with its crest near y251. Two practical escape targets are166,226 and514,226. These are suggestions within clear side pockets, not teleport destinations or temporary player immunity. The exact last warning alpha and damage spans match pixel-for-pixel.

Charge lasts4.2s Normal /4.0s Hard /3.8s Furious. The fully expanded red warning holds for the final fraction of the charge, then the field is harmful for0.9s. One second of authored harmless recovery follows. Ordinary body contact is disabled while channeling, and the charge itself never deals damage. Foreground body/core damage stays native. Real chest destruction/boss defeat cancels the attack; severed arms disappear with complete source-position explosions while the chest can continue casting. Pause freezes the attack; cancellation, retry and stage changes stop its voices. Native playerHit, HP pools, protected earlier main bars, copy cursor, arena-return rebuild and final destruction/reward owners remain.

## Artwork and sound

Built-in image generation used Mike's chest crop to make original orb energy; the supplied GIF was a choreography reference. No Chrono Trigger frames were imported. The raw1426x1103 RGBA sheet, exact prompt, editable Aseprite source sheet, hashes and rebuild recipe are retained under _ART_SOURCES/dracodia_luminaire_1030. Runtime exports have even dimensions and fixed source rectangles:48 charge,12 release,48 growing warning,24 field and16 recovery frames (148 total). The existing raised-claw anatomy supplies same-frame body alpha and chest sockets. Image fades, glow/brightness, depth-like orb variation and flood texture are authored offline. Runtime renders ordinary fixed blits; no sprite rotation/scaling, generated masks, tint/filter or animated global alpha. The field stays behind actors/HUD, preserving visible escape pockets. Shared mixer cues reuse the approved charge/reverb wave sounds plus native boss charge/shadow release/impact; no new audio files were required.

Large field banks use small texture pages, retaining every authored pixel/frame. Same-frame ninja/casting hit rigs are reused only while world position, animation and live anatomy are identical; movement, pose and limb destruction invalidate them immediately. Cached claw alpha is checked against the original uncached rig across more than1000 arena points. Native part/flash references remain live.

Rebuild: _BUILD_SOURCE/build_dracodia_luminaire_1030.py. Native probes/recording helpers are saved alongside it. Generated source and PROMPT.md are project files, not dependencies on the generator cache.

## Evidence and limits

46 focused native checks pass, plus66 isolated claw/arena-return regression checks. Claw fixtures explicitly choose a melee decision so the new spell scheduler does not replace the move being examined; the normal two-claw-combos/third-spell rotation is tested separately. Both side pockets are reached with ordinary movement from the south and survive the real release with GOD off on Normal, Hard and Furious. Centre/lower-field fixtures die through native playerHit. Tests cover held final warning, matching world geometry, harmless charge, unchanged boss HP, pause, real mid-charge arm breakup, cancellation/audio, alternating attack book, retry, cache equivalence/invalidation and final-death cleanup. No browser/draw errors.

The updated full native Furious final-main-life checkpoint starts at5330HP with intact limbs; preceding copied lives are cleared before capture. An invulnerable input-only bot reacts to the field, alternates left/right escapes and resumes fighting. No recorder HP/phase/timer writes occur during footage. 5 releases are recorded; all sampled blast positions remain in the safe pockets and no Luminaire contact is logged. Native defeat occurs at99.83s, total film106.85s. Measured spell charge58.28 / blast57.79 nativeFPS; combat55.05FPS. Overall54.14FPS includes the slower native final-destruction interval at43.13FPS, which this pass does not rework. Decoded audio mean-21.0dB / peak-4.2dB; charge/fire playback verified. The film includes the opening of final destruction, not a whole-game run or a non-GOD boss-balance result. Player weapon pickups remain native.

Required full suite exits1 with the same five known failures and no new failures; core game.js is unchanged. Existing movie passes remain archived. No commit or GitHub push was requested.

Luminaire chapter: http://127.0.0.1:51046/?dracodia=luminaire-1030#clip=stage8-dracodia-luminaire

Updated full main-life fight: http://127.0.0.1:51046/?dracodia=luminaire-1030#clip=stage8-dracodia-ninja
