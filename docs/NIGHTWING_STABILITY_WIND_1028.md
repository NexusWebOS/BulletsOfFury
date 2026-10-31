> October30 visual revision: vortex diameter reduced12.5%; teal-green exterior charge remains visible around real hit flashes. See NIGHTWING_TEAL_CHARGE_1030.md.

# Nightwing flight and wind readability — October28

The Stage6 Carrier/Nightwing preview card previously used the downloaded194.77s full-fight movie. It now uses a fresh native full encounter from the current local source, and all five related chapters have been remapped to the new actual entrance, drift and wind timing. Older downloaded, solo, and first revision movies are preserved.

Flight: north curve lasts2.1s and return1.9s. Both use the one64-heading level-attitude family through their tangent, eliminating threshold switches between bank silhouettes at8% and90%. The return has eased travel into the fight position. Dash windup now turns progressively from its prior facing into the committed lane; the existing48-frame banked drift, depth approach, shadows, sockets and collision continue unchanged. Player-velocity prediction is reset across held attacks/returns so a stale sample cannot kick the next flight decision. Native health, attack cadence, hit flashes, barrel rolls/somersaults, allies and rewards remain.

Charge: six own-pixel illumination steps brighten the actual teal armor before both Retina machine-gun bursts and wind release. Royal-blue cockpit and silhouette remain. Real accepted white hit frames take priority. PixelLab's new24-frame mint-white wind vortex is authored at384px around the aircraft, with a clear center and separate front/rear layers. The existing background dim and native FOV stay. The aura ends with the charge owner; it grants no shield or collision.

Wind rounds: same generated16-frame airflow design and32 directions, now96px fixed cells with1.5x the visible size, bright mint-white cores, stronger authored opacity and dark outlines. Shot speeds, spreads,18px hitboxes, twin real-barrel sockets and unshootable policy stay. No attached marker or disc replaces the wind. New runtime owner is assets/nightwing_stability_1028.js, last in index.html; art sources/exports/receipts live in assets/game/levels/stage_06/boss/nightwing_stability_1028/. No existing hull or atlas was repacked.

## Observed verification

16 checks pass: exact glow alpha against all17canonical clean frames; stronger visible area/highlights in every wind phase; stable64-heading arrival family; visible per-frame arrival translation8.42px maximum and at most one5.625degree heading step; native target/HP; gradual dash yaw; flyover/drift/approach completion; actual front/rear vortex and armor glow in native renderer; accepted white hit priority/expiry; machine-gun charge cue; six native wind rounds from the real two barrels; fixed96px projectile blits; non-interception; owner cancellation and no browser/asset/draw errors. Native screenshots and decoded footage were visually reviewed.

The initial candidate full capture averaged36.64nativefps. Equivalent-pose packing and transparent-padding reduction lowered new decoded atlas memory to50.08MiB, and the final **196.93s** native Furious capture averages **54.44nativefps**. It reaches actual Carrier and Nightwing defeat with the invulnerable input-only bot and actual enemy HP/phases/timers. No enemy state writes after native spawn. Player fire is withheld for32seconds of the ace form to show the real entry and attacks; ordinary allies remain active. Both charge cues, visible gusts, repeated drifts and real accepted hit flashes are observed. Audio mean-18.3dB / peak-1.3dB. 21 film/player checks pass across all six refreshed cards.

Required node syntax checks pass. Full _BUILD_SOURCE/test_fl.js reaches its summary and exits1 with the same five known failures: single-hit flash duration; opening-jump dialogue warning; opening jump return before Chromium; opposite StageX route persistence; StageX right full encounter. No changes to assets/game.js or _BUILD_SOURCE/test_fl.js.

Arrival: http://127.0.0.1:51046/?nightwing=stable-wind#clip=stage6-nightwing-flight
Wind: http://127.0.0.1:51046/?nightwing=stable-wind#clip=stage6-nightwing-wind
Full fight: http://127.0.0.1:51046/?nightwing=stable-wind#clip=stage6-carrier-nightwing
Evidence: C:/Users/Mike/Documents/New project/BOF-Nightwing-Stability-1028/

Local build and preview updated. No commit or GitHub push.
