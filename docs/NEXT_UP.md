# BULLETS OF FURY — state at 0801az

    verify_0730a  327 passed / 0 FAILED
    test_fl       1710 assertions / 88 stale failures (see the honest note at the bottom)
    manifest      7024 keys, 0 broken paths
    assets        478 MB

## Landed since the last status

**Boss health bars** — CF_BossHealthBars wired. Four health states with CRITICAL reserved for the
last 12%. Fill CLIPS as it drains rather than squashing, with a leading segment at the edge. And
bosses 02/03 get PER-LIMB bars — head, arms, torso core, lower body — which is exactly the 5-limb
model already in the fight, so you can see which limb you are killing.

**Wide liquid flats** — 800x256 fully opaque surfaces, preferred over the old families wherever
they exist. This is what the keyed magenta holes actually needed.

**Wide liquid falls, PLACED** — not hand-positioned. A drop crest is geometrically the row where a
hole begins, so I scanned each master's alpha for exactly that:

    stage 1   y 798, 1042, 3198     dam + two river shelves
    stage 4   y 2934                coastal edge
    stage 7   y 283, 666            sewer outfalls
    stage 2   none                  correct: its lava is a flow, not a fall

Each crest carries its own x span, so a 189px shelf gets a 189px curtain. The fall tracks the SAME
srcY the terrain uses — a curtain on its own scroll drifts against the hole it covers.

**Radio / dialogue** — 304 lines lifted VERBATIM from the passovers into BOFX.story. 103 scenes,
13 speakers. The delivery rules drive the design:

    SAFE   21 scenes   full radio panel, player not flying
    COMBAT 82 scenes   ONE subtitle line, nothing over the playfield

Plus: any input clears a line (rule 4), lines duck when a boss goes live (rule 5), and a line whose
speaker IS the selected pilot is dropped so nobody talks to themselves (rule 7).

**Arcade presentation** — 82 cards. Stage intro / mid / boss warning / complete per stage, and
GAME OVER banded by how far you got (1-3, 4-5, 6-7, 8, bonus), because dying early and dying at
the finale should not read the same. Cards are stored as arrays of lines and rendered exactly as
authored — the line breaks are the layout.

**Attract mode** — arms after 12s idle on the title, 3.4s per card inside the doc's 3-5s band,
Start/Fire advances, any input dismisses and resets.

## Two namespace collisions, both mine

    nmb_   mini bosses vs missile pickups   -> minis moved to nab_
    nwf_   liquid falls vs weather          -> falls moved to nlf_

Same mistake twice: claiming a prefix without checking it was free. Worth a grep before the next
pack goes in.

## Honest note on the 88 harness failures

They are almost entirely STALE ASSERTIONS, not broken code — they test art and systems that were
deliberately replaced or culled at your instruction:

    26  art keys that were renamed or culled
    16  stage art replaced by the stacked pack
    11  boss systems reworked into the mech/component model
     3  fonts replaced by Vol.3
    32  other, mostly enemy families whose art was removed

verify_0730a is the harness carrying the current work and it is 327/0. Bringing test_fl back to
green means rewriting each assertion to test what replaced it — a real session of work, and it
should NOT be done by deleting whatever is red.

## Open, unresolved

- Helicopter boss vanishing mid-HP and reappearing. Never diagnosed.
- Stage 4 wants two connector sections that do not exist as art.
- Stage 4's coastal opening wants naval enemies; the boat art was culled.
- The stock enemy art table points at keys that no longer exist — same class as the turrets.
- `thruster_rig.html` is waiting for your rigging pass (147 units, ships included).
