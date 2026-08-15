0812p: a 5-second roll cooldown you can see, and the EQUIPPED box that was never drawn

Mike settled the tester's barrel-roll complaint himself: "lets do a 5 second cooldown on barrel
rolling. make a little charge bar that appears in the bottom left corner, and also I've noticed our
equipment box doesnt appear in-game in my hud. Place that on the lower right corner of the game."

THE COOLDOWN WAS 0.18 SECONDS
Not a cooldown - a lockout that only stopped two rolls in the same instant, which is exactly why
the roll kept firing on micro-adjustments. Now 5s, verified end to end: a roll starts, arms the
full 5s when it completes, a second roll during it is refused, and it re-arms after.

AND A 5-SECOND COOLDOWN HAS TO BE VISIBLE. At 0.18s the player never needed to know; at 5s an
invisible timer is just an input that sometimes does nothing, so the bar is not decoration - it is
the half of this change that keeps it fair. Bottom-left, and the READY moment is what changes
colour rather than just filling, because ready is the thing the player is waiting for.

nequipbox WAS IN THE BUILD AND DRAWN BY NOTHING
`nequipbox` is a registered key - a hand-authored 777x731 "EQUIPPED" panel with an empty interior
socket - and grep found ZERO references to it in game.js. Not misplaced, not mis-sized: never
called. The same shape as the systems CLAUDE.md already lists as declared-and-never-fired. It is
drawn lower-right now with the weapon you are actually holding in its socket, and the interior was
MEASURED off the plate (x 0.218..0.785, y 0.244..0.855) rather than eyeballed, so the icon sits in
the frame's own window at any scale.

AND IT IS NOT THE SHIELD/SPEED/WEAP PIP STRIP. My first cut built those pips into a corner panel.
Mike: "no not that weapon box. the Equip box." Those pips are a different readout that already
exists on the HUD strip; this is the authored frame.

micon_ IS THE THIRD ART STORE AND THE OTHER TWO CANNOT SEE IT
The icon socket came out empty at first and I nearly called it unwired. Measured: `micon_mg_1` is
absent from XART._src, from BOFX.cells AND from ASSETS, so XART.rdy() on it is false forever -
which is what an unreachable key looks like. It lives in BOFX.icons and draws through
iconDraw/iconBlit, exactly as CLAUDE.md's three-store note says. Asking the wrong store paints an
empty socket and reads as a missing feature.

Why the strip version was invisible in his screenshot, for the record: drawHUDStrip puts the
equipment pips at 0.757..0.913 of VW on a SEPARATE canvas - the far right of the strip - and his
narrower window crops exactly there. Both new readouts anchor to the PLAY rect instead, inside the
frame the game actually renders.

Suite 2,613 / 233 / 5 - the same five long-standing failures.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
