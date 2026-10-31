# Nightwing smaller wind vortex and teal 1015 charge — October 30

[Watch the updated wind attack](http://127.0.0.1:51046/?nightwing=teal-charge-1030#clip=stage6-nightwing-wind). [Full Carrier-to-Nightwing fight](http://127.0.0.1:51046/?nightwing=teal-charge-1030#clip=stage6-carrier-nightwing).

The existing 24-frame front/rear wind swirl is 12.5% smaller: 384px source cells are proportionally baked to 336px cells, keeping the exact center and timing. The original PixelLab strokes remain the source. Wind projectiles, hitboxes, warning lanes and gun sockets are unchanged.

Nightwing now builds a teal-green 1015 energy outline before the wind attack, alongside the existing armor-pixel charge. Its six authored strength levels follow the native 2.1-second windup and brief release accent. Three actual clean hull poses cover normal, damaged and inverted states. The energy occupies exterior pixels around the real armor contour; it never covers original body or hit pixels. Therefore the green cue stays visible while the real white hit flash still plays, without suppressing or extending hit feedback. The royal-blue cockpit and aircraft identity remain unchanged. Death/cancellation/recovery remove the effect with its attack owner.

The current NW32 owner registers the three new banks and blits fixed authored cells at their shared pivots. No runtime tint, glow, blend, scale or opacity animation was added. Sources and editable Aseprite files live in _ART_SOURCES/nightwing_teal_charge_1030; runtime images/metadata are in the matching boss folder. Rebuild with _BUILD_SOURCE/build_nightwing_teal_charge_1030.py --aseprite <installed executable>.

24 art/native checks pass, including inherited entry/turn/drift/target/HP tests, exact original body/hit alpha, all24 swirl phases, six growing energy levels across three poses, real smaller blits, visible outline during an accepted hit, hit expiry, wind round sockets/interception and cancellation. Native charge and hit screenshots were inspected.

The new 205.57s real-engine Furious GOD-observer movie reaches native Carrier and Nightwing defeat at 54.95 native FPS. It includes the actual charge, outline, wind release, hits, stable entrance and drift. 22 recording/player checks pass; decoded audio mean -18.4dB and peak -2.6dB. No game/draw/HTTP/audio/input exceptions. No enemy HP, attack phase or timer injections; ordinary input bot with labeled invulnerability. All six Carrier/Nightwing gallery cards now use this movie; earlier media remains.

Syntax passes. Required full suite completes with the same five existing failures and exit1: single-hit flash hold; opening-jump dialogue; jump/chromium order; opposite StageX route persistence; StageX right encounter. Core game.js and test_fl.js unchanged. No commit or GitHub push. Evidence: docs/qa/nightwing_teal_charge_1030.json.
