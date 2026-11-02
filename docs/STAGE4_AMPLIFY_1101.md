# Stage4 highway art and combat corrections

Mike requested seven specific corrections after reviewing the Stage4 guide. Current owner is `assets/stage4_amplify_1101.js`, loaded after R46. Original atlases and source art are retained.

- Highway Tank: same whole authored armor and native hull/turret/rack health budget, with its original road lane retained before/after AI and frenzy movement. It advances south without side-to-side chassis motion; its native weapon aiming and attack ownership remain.
- Missile Launcher Truck: new six-wheel olive/bronze armor with two visible rails. Fired cream/silver missiles retain the orange bands, red warheads and dark fins shown on the truck. Launch/reload frames empty and replenish the actual rails.
- Command Fighter: new black/burnt-orange camouflage whole aircraft and fixed twin machine guns. No modular turrets. Uses16 authored direction poses, full roll, somersault and attack/boost banks through a turning sortie and committed forward bursts.
- Fuel Tanker: new unarmed truck,114px/s forward drive. No shooting controller. A real native defeat owns its existing shock ring, fireball chain, smoke and debris, plus exactly one155px splash through normal `hitEnemy` to nearby regular enemies/objects. It never awards a second death or bypasses native hit feedback.
- Armored Tractor: new tracked hull and fixed front twin guns. Real source tread/recoil poses and only south-facing machine-gun rounds. Its native stagger delay is consumed rather than stranding it offscreen.
- Heavy Jet: current gray identity retained in a new complete authored motion bank, with integrated parallel fixed missile rails. It strafes/turns, commits a Retina warning, and launches along its current displayed heading. No independently rotating launchers.
- Mobile SAM: new three-rail hull, matching rack missiles, visible depletion/reload, native Retina and beeps. The three launch callbacks are separated by0.18s. Native launcher defeat cancels queued launches and warnings.

All full native hull HP is retained. The old coupled modular jet bookkeeping is removed only for the two explicitly whole-airframe replacements; the existing live hull budget is unchanged. Shields, white hit flash/expiry, native missile HP/interception, ordinary bullet immunity, shared mixer and reward/death owners remain. New ground traffic uses full visible footprints and the shared `ground_traffic_1018.js` entry placement/reservation owner. Crowded vehicles queue upstream rather than overlap.

## Art, generation and rebuilding

Nine built-in `image_gen` source PNGs are copied into `_BUILD_SOURCE/stage4_amplify_1101/`. Style reference is the actual `encounters_0930/tank_hull.png`; the actual live heavy-jet seed is exported as `heavyjet_identity.png`. Original source files, prompts and generation identifiers are retained in `generation.json` and the source manifest.

`_BUILD_SOURCE/build_stage4_amplify_1101.py` exports six models, a matching missile bank and134 frames in19 registered banks under `assets/game/levels/stage_04/enemies/amplify_1101/`. Final hull cells are192×192; missile cells128×128, with a shared pivot and one proportional scale per source bank. Direction cells are actually authored views; the runtime never rotates a static aircraft/vehicle/projectile image. Native effects retain their existing registered reels. The exporter removes disconnected edge debris, preserves source colors, aligns physical pivots and records the original odd source crops separately from the final even canvases.

`update_stage4_metadata_1101.py` registers the taxonomy and current atlas descriptions/banks. It preserves unrelated entries. No original atlas repack was required.

## Verification

`probe_stage4_amplify_1101.py`:32 native checks pass, including real shot releases, zero tank x drift, changing authored jet headings, no modular guns on replacements, forward firing, sequential SAM timing, actual damaged pixels/expiry, real fuel splash and launcher defeat cancellation. `probe_stage4_edges_1101.py`:8 checks pass for crowded full-hull clearance/fixed lanes on Normal/Hard/Furious, actual gun-mount alpha on all32 aircraft heading poses, and browser errors. No page/console errors.

Required JavaScript syntax checks pass. The required full `test_fl.js` suite exits1 **before assertions/final summary**, because this checkout lacks ignored `UNUSED_ASSETS/retired_art_1022/manifest.json`. This is reported separately from browser checks.

`record_stage4_amplify_1101.py` records native inputs and actual game audio without enemy HP/phase/timer writes. The tanker is killed by ordinary player primary-fire input, and native telemetry records nearby barrels damaged by its fuel splash. Other cases use a movement-only invulnerable pilot; the Highway Tank take keeps the pilot/camera still to expose any true lane drift. A first-frame capture-configuration lookup was fixed and the first take replaced; the remaining six had no game or media errors. Original capture receipts remain in the ignored evidence directory.

`publish_stage4_amplify_1101.py` replaces only the seven requested cards in the current164-card local guide, preserving all other films and archived routes. New seven-clip review page: `http://127.0.0.1:8805/current/stage4-highway-1101.html`. Current complete guide starts at `http://127.0.0.1:8805/enemy-showcase-1031.html?revision=stage4-highway-1101#enemy=stage4-s4sam`.

All local native evidence, source calibration sheets, recordings and playback receipts live under ignored `_shots/stage4_amplify_1101/`. No commit or push was performed.

Final publication checks pass: all19 exported bank dimensions/checksums, full H.264/AAC decoding of all seven films, and actual Chromium video/audio decoding, seeking, poster/route resolution, seven-clip page and selected SAM card in the complete guide. No page/console errors. Every other card in the164-card guide was preserved.
