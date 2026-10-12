# Hammer: Chromium columns and anchored jump strike

Mike's October 11 direction replaces the bottom storm's spikes with Chromium
energy beams extending from the bottom to the screen's halfway line. Crossing
above that line provokes a jump and side strike at the pilot's locked position.

The late runtime owner is `assets/hammer_chromium_1011.js`, loaded after the
part-two encounter overrides. It replaces the earlier full-height spike volume
and bypasses the global Chromium-to-ice art substitution for this attack.
The original authored Chromium sheet supplies the complete beam and both caps
at one proportional scale. Each column retains its separate lane warning,
ignition grace, straight collision volume and expiry. No beam pixel or collision
extends above the halfway line, computed through the actual world zoom.

The side counter uses the existing intact sixteen-pose left/right swing banks.
Hammer winds up, arcs into the background at 30% size, pauses on a warned target,
dives, sweeps through it, and recovers. The target is committed in world space;
player movement and camera scrolling cannot drag it. At the upper and side
edges, the chest position and rotation keep the measured hammer head on that
target. The warning follows each segment of the authored head arc. Only the
active head sweep can hurt a pilot during this counter; its airborne/recovering
body creates no additional collision. Each seat can be hit once per swing.

Hammer damage still counts during the jump. Depleting the weapon queues its
break until the committed strike lands. Existing armor, healing, stun and
ordinary orbital-jump behavior retain their owners. Both co-op pilots can
trigger the upper-half counter. Musical intros/dance breaks remain outside it.

No new art, atlas edits, combat HP changes or Git publication in this pass.
The prior generated sprite sheets and their original sources remain intact.

Verification is recorded in `docs/qa/hammer_chromium_1011.json`. The full gameplay
suite reaches its final success summary with exit 0. Native Chromium checks
cover four difficulties, both side edges, actual player damage, co-op target
selection, authored source-key draw calls, pixel bounds, and browser errors.
The first test run caught a floating-point expiry boundary; comparing absolute
end times corrected it. The first native capture caught the old ice-art alias;
the direct authored Chromium route corrected it. Final native checks: 22 passed,
0 failed, with zero page, console or asset errors.

Review: `_shots/hammer_chromium_1011/review.html`. It contains two eight-second
fixed-step native gameplay recordings and screenshots. The recordings use
protected fixtures to inspect choreography and graphics; they are not complete
campaign clears or human difficulty ratings. Use **BOSS5** to play the regular
Hammer encounter with these changes.
