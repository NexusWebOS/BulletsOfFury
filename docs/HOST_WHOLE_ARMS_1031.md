# First host: whole-arm strikes and torso-to-ball closure

RD96 replaces the long segmented ligament and separate distal claw in the first host's physical attacks. The original complete shoulder, upper arm, forearm and claw now coil, advance and sweep as one authored limb. The body leans and advances toward the committed target, then returns home. Arm reach stays within the original anatomy (about83–158px from shoulder to contact through coiling/extension); body advance is capped175px. It never stretches a wrist or grows repeated arm sections.

The complete current torso stays visible after the last arm is destroyed. A1.50s/40-frame sequence curls the torso, draws the same synthetic code around it and closes curved source armor plates into the native sphere. Its first frame is pixel-identical to the complete current armless torso; its last frame is pixel-identical to native roll frame9. The spin begins at that exact frame and continues at30fps while the existing RD73 ricochet/bomb owner runs. The old9-frame cut-body `fold` reel is not used. Native core HP, damage after arm removal, bomb cap/cadence/warnings and first-host defeat remain.

## Runtime and sources

- `assets/host_whole_arms_1031.js` owns only first-host complete physical limbs and exposed-core rendering/closure. It delegates other attacks, both portals, possession, copied forms and final-life combat. Existing inset missile/optic owners are retained.
- `assets/host_whole_arms_art_1031.js` registers466 authored normal/hit frames in16 banks: two64-frame whole arms,16-frame torso/passive arm lean banks, complete armless torso and40-frame fold. Each bank has one even fixed cell, common padding/pivot and original360px host unit. No runtime transforms, animated alpha or synthesized graphics.
- `assets/game/levels/stage_08/boss/whole_arms_ball_1031/` contains PNGs, sixteen editable Aseprite sources, exact source hashes, metadata, authoring Lua and provenance. `_ART_SOURCES/host_whole_arms_1031/` retains the editable sources and review plates.
- `_BUILD_SOURCE/build_host_whole_arms_1031.py` reproduces all PNGs exactly from current approved whole-host, inset-tube and native ball artwork using offline nearest-neighbor authoring and the local Aseprite installation. No new paid art or external upload.
- Same-frame arm masks own projectile collision, part damage and Retina anchors. Native hit-white frames retain exactly the normal alpha and expire through the normal timer. The committed contact point belongs to the complete visible claw. Native capture, lift, fatal-throw owner and safe stage/arm-break release remain; GOD survival and arm-break release were exercised in this pass.
- Whole-arm break effects use the current shoulder/elbow/claw coordinates with the original bounded RD71 breakup owner. Shared `combatModule0927` cues accompany the strike; `combatEnergy0927`/`combatOrb0927` accompany fold/closure. Original robotic screams, warnings and bomb audio remain.

## Verification and footage

44 focused native/source/rebuild/playback checks pass: both arm sides, complete finite limbs, body advance and return, actual damaged pixels/expiry, moving collision/Retina anchors, capture/lift/release, native HP gate, complete armless frame, exact fold endpoints, pause, transition-before-bombing, core damage, absence of old tendon/claw/fold draws and browser chapter playback. No native rendering/browser/asset/audio-tap errors. Actual native and decoded film frames were inspected.

Fresh full5945HP first-host Furious fight: 148.056s,1280x800,30fps recording, 58.11 average native simulation fps. Cole uses actual player weapons and native GOD; health, arm destruction, exposed core, ricochet bombing and first-host defeat run normally. The bot withholds fire to display attacks and the exposed-core sequence; it never writes HP, phases or timers during filming. The inherited natural attack book uses its existing side selection; both sides are separately verified in native fixtures. Audio mean-18.6dB / peak-2.6dB; complete movie decodes without errors.

- [Whole-arm strike chapter](http://127.0.0.1:51046/?host=whole-arms-ball-1031#clip=stage8-host-whole-arm-strike)
- [Both arms destroyed and ball transformation chapter](http://127.0.0.1:51046/?host=whole-arms-ball-1031#clip=stage8-host-ball-transformation)
- [Current full first-host fight](http://127.0.0.1:51046/?host=whole-arms-ball-1031#clip=stage8-firsthost-whole-arms)

The older complete-run movie is retained and labelled as predating these first-host corrections. This new film does not claim to re-record the copied forms or final life.

Syntax checks pass for `assets/game.js` and the new owner. The required full gameplay suite completes and exits1 with the same five pre-existing failures:

- and the flash is held long enough for a single hit to register
- dialogue ends with the opening jump warning
- opening jump lands and returns before chromium activation
- unchosen right route persists as the opposite Stage X fight
- Stage X right branch launches a full encounter

Core `assets/game.js` remains unchanged: `024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de`. Complete evidence: `docs/qa/host_whole_arms_1031.json`. No commit/push.
