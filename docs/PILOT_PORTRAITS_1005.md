# All nine pilots: complete frames and stable speech

Mike requested Cole's portrait correction for every pilot. The complete Fury
roster now retains its own authored frame and idle head/shoulders while talking.
Only the aligned authored mouth region changes. Every expression uses one stable
intrinsic size and the same complete bezel. Falva retains her repaired 256×244
aspect rather than stretching it to square. Comm faces mirror toward the text.

`assets/pilot_portraits_1005.js` composes the approved Axel, Decker, Falva, Freezer,
Juggernaut, Lizzie, Maverick and Yuri cells at the XART boundary. Lizzie uses her
existing source-sheet/full-bezel composition as the source and now protects every
rail for all emotional poses too. Cole retains `cole_portraits_1005.js`, including
the Stage 6 fixed shouting head. Legacy portrait/face keys and Yuri's alternate
avatar routes resolve to the same repairs. The original art and manifests remain
intact; no atlas changes or substitute portraits were introduced.

Verification: `node --check assets/game.js` and the new runtime script pass.
The full suite reaches its final summary with 7,274 passing assertions, exit 0.
`_BUILD_SOURCE/probe_pilot_portraits_1005.py` passes 236 native Chromium checks
with zero page/console errors. It inspects real XART pixels for both menu and
comm versions, all twelve expressions, mouth-only changes, fixed rails, aliases,
and idle return. The browser clock advances by one authored mouth interval while
rendering all nine dialogue callers so PNG encoding cannot skip poses for later
speakers. Pose contacts and in-game dialogue captures were visually inspected.

An initial native run caught Lizzie's emotional poses changing a thin inner rail;
the full-bezel composition was tightened. The animation probe also needed to
preserve its recorded keys across speakers and step the clock instead of relying
on capture wall time. The final native run passes all checks. A temporary account
usage limit blocked one automatic approval review; the later authorized browser
run completed successfully.

Review with nine native speech animations: `_shots/pilot_portraits_1005/review.html`.
Portable QA: `docs/qa/pilot_portraits_1005.json`. Local follow-up, no commit or push.
