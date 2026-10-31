# Stage7: fast sewer collapse and last-moment rescue

SR93 keeps northward travel at400px/s during the Warden's post-defeat escape. The original stone chamber scrolls into view continuously; the green PixelLab metal gate opens automatically while the collapse is still chasing the aircraft. Decker's dialogue reads `WHAT IS THAT? <SELECTED PILOT>, NOOOO!` using the current pilot's display name. There is no waiting wreck, approach prompt or deceleration before intake.

The gate forms over0.60s, takes the ship in over0.70s, closes over0.48s and whites out over0.38s. Its anchor remains the measured original stone aperture, x343/y310 in source art. The aircraft remains full-sized until it reaches the mouth, then uses existing authored shrinking north-view frames; both co-op seats enter together. The ship disappears22px ahead of the advancing blast front. Native Forge reward, campaign ledger and direct Stage8 WARPENTRY remain owned by the existing finish function, called once after rescue.

## Art and implementation

- `assets/sewer_rescue_1031.js` wraps only the Stage7 Warden exit, portal, player intake and supplementary collapse rendering. Tank miniboss and other boss routes retain their owners.
- `assets/sewer_rescue_art_1031.js` registers56 authored frames: dense192px, barrage288px, radial288px, engulf352px and smoke-ring448px banks. Every bank has even fixed cells and one centre pivot.
- `assets/game/levels/stage_07/effects/escape_rescue_1031/` contains PNGs, five editable Aseprite sources, manifest, provenance, authoring Lua and32 exact native source frames.
- `_BUILD_SOURCE/build_sewer_rescue_1031.py` reproduces the PNGs exactly from those saved inputs. The source is actual ColeForge explosion/smoke art; toxic palette and ring expansion/fade are baked offline. No new paid generation or external upload.
- Runtime only advances fixed frame blits. No runtime rotation/scaling/opacity, filter glow, procedural replacement explosions or shader effects. The original game explosion system is retained. Supplementary effects are bounded to76 and cancelled on restart/handoff.
- Native `jetDash`, `warpCharge`, `warpGate`, `warpBurst`, `expSmall`, `expBig` and dialogue-letter sounds use the existing shared mixer and retrigger gates. The warning is text dialogue, without generated speech.

## Verification and review

47 targeted native/pilot/co-op/source/rebuild/playback checks pass. These cover400px/s movement, steering, pause, automatic opening, all9 selected names, aperture anchoring, both co-op seats, frame ownership,22px rescue timing, original reward/ledger/Stage8 entry, cleanup, exact source rebuild and browser playback. No page, rendering, asset or audio-tap errors were recorded.

The real live engine film starts at a prepared Warden final-hit checkpoint (core12HP, modules/canisters already destroyed), then player fire triggers defeat. Once filming starts, the recorder only supplies input; it never writes boss HP, phases or timers. It includes native Stage8 handoff. Invulnerable Cole observer, Furious,30fps film, 15.847s. Active escape simulation averages58.67fps; whole-recording average44.06fps includes the existing startup/Stage8 load stalls. Audio mean-24.8dB, peak-6.6dB; full decode has no errors.

[Watch current local rescue](http://127.0.0.1:51046/?escape=nick-of-time-1031#clip=stage7-portal-chamber). The `stage7-portal-chamber` gallery entry now selects this film. The older take is preserved as `stage7-portal-chamber-before-rescue`. No Git upload was made.

`node --check assets/game.js` and the new runtime pass. The complete `_BUILD_SOURCE/test_fl.js` suite still exits1 with exactly the same five pre-existing failures:

- and the flash is held long enough for a single hit to register
- dialogue ends with the opening jump warning
- opening jump lands and returns before chromium activation
- unchosen right route persists as the opposite Stage X fight
- Stage X right branch launches a full encounter

Core `assets/game.js` remains unchanged: `024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de`. Full evidence is in `docs/qa/sewer_rescue_1031.json`. Focused native fixtures and recorder are archived in `_BUILD_SOURCE/` and write ignored `_shots/sewer_rescue_1031/` output. The film is a final-hit route review, not a full Warden balance test.
