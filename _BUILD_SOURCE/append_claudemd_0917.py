#!/usr/bin/env python3
"""append_claudemd_0917.py - the 0917 economy section, in the line ending the file's tail uses.

CLAUDE.md has MIXED line endings on main (0912u measured 3265 CRLF / 374 bare LF) and .gitattributes
gives it no contract, so an append that assumes one is wrong half the time. This matches the ending
of the section it follows, which is what that note prescribes.
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, 'CLAUDE.md')
raw = open(p, 'rb').read()
tail = raw[-600:]
nl = '\r\n' if tail.count(b'\r\n') >= max(1, tail.count(b'\n') - tail.count(b'\r\n')) else '\n'
assert raw.endswith(b'\n'), 'the file should end on a newline'
if b'THE COMBINATION COMES OFF THE BOSS' in raw:
    print('already appended'); raise SystemExit(0)

TEXT = """
## 0917 - the economy Mike actually asked for, and a guaranteed reward nobody could catch

Two messages replaced the run-end score bank: 1,000 score = 1 FURIOUS PT converted at the end of
EVERY level with the remainder carrying; achievement points land in the same balance; a pickup is
250 and a STYLISH dodge 500; one upgrade ladder from 1,000 at x1.25; and combinations are earned
from bosses, not discovered in the field. Full writeup: `docs/FORGE_ECONOMY_0917.md`.

**THE COMBINATION COMES OFF THE BOSS.** A combination is ELEMENT x WEAPON SLOT - fire on the machine
gun is a different thing from fire on the laser - and it lives in the profile beside the Armory's
levels as `forge_<elem>_<slot>_C`, written with NO `cost`. The Armory sells only the LEVELS of a pair
you already own; an unearned row is dim, says BOSS DROP and shows no price.
[!] **A FIELD PICKUP USED TO LICENSE AN ELEMENT ON ALL NINE SLOTS AT ONCE** - one crate on stage 1
opening nine combinations, which is exactly the "you dont unlock all these weapon combination
upgrades" he ruled out. `forgeDiscover` still records what has been SEEN and grants nothing;
`forgeElemsFor(w)` is what may be combined, and the Forge's element strip is now per SLOT (a global
list would offer what the screen behind it refuses).

[!][!] **"THE PICKUP EXISTS" AND "THE PICKUP IS CATCHABLE" ARE DIFFERENT CLAIMS, AND THE FIRST ONE
PASSED FOR TWENTY MINUTES WHILE THE REWARD WAS UNOBTAINABLE.** The drop was spawned at `boss.y`, and
the stage-1 helicopter reports **618.6 on a 512-tall playfield** - its DRAWN position is `boss._drawY`
- so the cull killed it on the frame it was born. Measured: **0 frames alive**. Every assertion about
it was green: it existed, it named an unowned pair, it was at the boss's position. The probe that
found it asks how long the thing stays reachable. It now spawns clamped into the field, descends to a
hover line and then closes on the player: collected at frame 107 of a fight that stays in PLAY until
346. [!] And that probe's own first cut could not tell COLLECTED from CULLED - both leave `powerups` -
so it reads the profile to say which.

[!] **A REWARD MUST NOT ADVANCE A PRICE LADDER.** The ladder counts purchases that carry a `cost`,
which `furiousBuy` writes and nothing else does, so earning a combination cannot raise the price of
everything else. And each purchase records the price it PAID, so re-tuning the base or the step later
cannot re-price what an existing profile already bought.

[!] **THE STYLISH AWARD IS MEASURABLE BECAUSE THE MANOEUVRE'S I-FRAMES ARE WHAT SPARE YOU.** A roll
and a somersault both set `player.invuln`, and the enemy-bullet loop returns on `invuln>0` BEFORE it
tests the hitbox - so "a projectile that would've impacted you" is exactly a round overlapping the
hitbox during those frames, and the check has to sit IN FRONT of that return. Gated on a live
manoeuvre, so ordinary post-hit i-frames pay nothing. One award per manoeuvre (flagged on the
manoeuvre object) - a roll through twenty rounds would otherwise pay more than the level converts.
[!] **Its glow is offset copies at the SAME SIZE**: a 1.14x pass centred on the same point puts every
glyph's edge somewhere different from its core and reads as ghosting, which only the render showed.
[!] **And it is drawn through `worldXformEscape`** - the first cut passed `player.x`, a WORLD x, into
a screen-space draw. Sixth time in this file.

[!] **THE PICKUP SCORE MOVED INTO `applyPowerup`.** The old 50 was written at the one touch collision
that awards it, and that collision excludes the crate, the capsule and the missile boxes BY NAME
while those reach `applyPowerup` from elsewhere - so some collections paid and some did not.

[!] **A TRIPLE-QUOTED PYTHON ANCHOR CANNOT END IN A QUOTE CHARACTER**, and several of these .cjs
lines do; build those anchors from pieces. [!] And an apostrophe inside a single-quoted JS assertion
message is a syntax error - this face has no usable apostrophe anyway (0912b).

Probes: `probe_bossdrop_0917.py` 34/0, `probe_armory_0917.py` 32/0, `probe_dropreach_0917.py` (the
reachability window), all real Chromium with 0 page or console errors. Proof frames in
`docs/proofs/bossdrop_0917/`. Suite section 372.
"""
TEXT = TEXT.replace('[!]', '⚠').replace('\n', nl)
open(p, 'ab').write(TEXT.encode('utf-8'))
print('appended the 0917 economy section using %r' % nl)
