# Pilot fire and acceleration — September 27

Implemented Mike’s follow-up locally; no commit or push.

- **One physical emitter.** Ground projectile fans share one centered nose flare. Rapid volleys refresh that flare rather than accumulating copies. Space launches map to the authored cannon/nose positions; missile rack flashes do not stack on a live cannon flash. Native checks measured exactly two cannon flashes at the two hardpoints, plus the separate nose launcher when fired.
- **Homing lance colors.** Acquired laser tiers I–V now give orange, blue, green, white and red lances and matching muzzle energy. The ordinary homing variant keeps three tier-I lances at .62 damage each. Its launch staggering previously suppressed the entire muzzle; the volley now gets one centered flash. Native pShoot/updatePlay/drawWorld checks cover all five tiers.
- **Generated ice breath.** Twelve new RGBA frames of rolling cold vapor and moving ice shards, generated here with the built-in image tool. The 4×3 sheet uses measured per-frame root anchors and simulation-time playback at18fps. Freezer’s established damage envelope and reach remain. No duplicate root flare. Owning build: `_BUILD_SOURCE/build_pilot_feedback_0927.py`; prompt/source: `docs/pilot_feedback_art_0927.json`; registered in ART_TAXONOMY.
- **Acceleration exhaust.** Real movement input ramps forward thrust rapidly and releases smoothly. The renderer extends and brightens the authored exhaust from fixed nozzle roots on all nine pilots. Lateral/backward input and evasions use lower intensity. Ground full-forward flame length reaches4.2× the existing flame; space reaches2.45×. Normal/banked poses and space plume transforms stay aligned; quick-roll plates retain their authored poses. No hull, collision or camera scaling changes.

## Verification

Syntax passes for all four changed/new runtime scripts. Full suite reaches its final success banner and exits0: **5,492 assertions /0 failures**, versus incoming5,479/0. An intermediate run exited1 with five new lance-muzzle assertions; the staggered-launch fix resolved all five. Final failing-name comparison is empty. `assets/game.js` remainsLF; test_fl and the new contract test remainCRLF.

Native Chromium verified one ground muzzle across five weapon tiers, real space hardpoints, five distinct lance palettes and their real firing path, twelve ice animation frames, nine pilots’ flame masks, acceleration/release input and zoom1. Screenshots inspected. Page and console errors empty.

Review contains three real-time clips:12s single muzzle sequence,8s ice breath,16s ground/space acceleration. These are empty combat fixtures, not campaign runs. Actual SFX captured with music muted and0.4 capture-only gain; peaks .403/.594/.490. All videos decode; posters, game link and idle/boost toggle checked in Chromium. Evidence, recordings and review page live under `_shots/pilot_feedback_0927`; durable results: `docs/qa/pilot_feedback_0927.json`.

[Open review](http://127.0.0.1:8794/_shots/pilot_feedback_0927/review.html)

Previous full-volume special mixing, physical controller and human campaign balance follow-ups remain unchanged. Prior overnight automation remains paused.
