# Chronos: protected minigun and depth flight — October 25

The gun damage owner rejects module damage until five seconds of committed firing have elapsed. Pickup and warning time do not consume protection. Hits still flash; ordinary damage resumes at the boundary. The existing HP bar and Retina targeting remain active.

C35 changes rage depth transitions into a northward exit, an offscreen depth change, and a southward entry. Return travel uses the same choreography with foreground scale restored beyond the screen. Same-depth repositioning remains continuous. The existing hammer depth attack already has its own northward exit/background drop.

Gun body and hand rendering remaps saturated violet accents to blue, preserving alpha, dark outlines, neutral metal and hit-white images. Detached throws, discard, recall, pickup release and knocked-away hammer use the original eight-view arch_hammer_flight_0926 sheet and measured HAMMER_FLIGHT_HEADS. Whole held boss plates remain intact.

The red wave now plays authored terminal frames 6 and 7. Storm lightning plays its authored terminal frames at full opacity, then retires; no opacity fade is used for the red bolts. The background darkness recovers separately.

Verification: native Chromium focused probe passes 12/12 with screenshots, real gun damage boundaries, flash expiry, both depth scales, terminal wave frames and no browser errors. Syntax checks pass. Required test_fl exits 1 before assertions or final summary: missing _BUILD_SOURCE/retired_art_archive_1022.cjs (existing blocker).

Evidence: _shots/chronos_flight_1025/probe. Full recording and delivery results are recorded in docs/qa/chronos_flight_video_1025.json after capture. No commit or push.

Final delivery: 337.8-second full fight, 8/8 playback/audio checks, no game/browser errors. Recorded protection lasts 5.1164 seconds before first HP loss. Main preview revision flight-protection-1025; chapter controls include background flight and foreground return.
