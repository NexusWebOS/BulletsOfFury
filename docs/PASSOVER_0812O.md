0812o: the finale fights four ways

Mike, on the stage-8 boss: "4 forms, very tanky, attack pattern is the same through all 4 forms."
He was exactly right, and it was worse than untidy: measured, the LAST fight of the campaign was
the least threatening unit in the game - 0.44 rounds per second reaching the player, with
4.2-second silences. All four forms ran the single `case 8:` branch in bossAttack.

FOUR IDENTITIES, ESCALATING, each built from a primitive that already exists:

  APOSTLE COCOON      a shell. Slow wall volleys with ONE moving gap - the stage-7 flood idiom,
                      because a cocoon should read as something you break, not something that
                      hunts you. Lowest pressure on purpose: it is the opener.
  VENOM ASCENDANT     it has hatched. Aimed bursts plus homing pairs from both flanks.
  NECROTIC LEVIATHAN  area denial. The rotating rake with a bullet spiral to thread between.
  FURIOUS DEATH       all of it, faster: five-spoke rake, missile fans and aimed fire.

                    shots/s   threat/s   worst silence   rake
  APOSTLE COCOON      12.31       0.64        1.1s         -
  VENOM ASCENDANT      6.78       4.44        0.9s         -
  NECROTIC LEVIATHAN   9.20       0.53        1.6s       23.1s
  FURIOUS DEATH        7.69       4.84        1.3s       22.3s

The 4.2-second silence is gone - worst is now 1.6s. The low threat/s on forms 0 and 2 is the
metric, not the fight: it counts AIMED rounds reaching the player's row, and a wall-with-a-gap is
not aimed while a rake fires no bullets at all. Those two forms pressure you by geometry.

A STEP GATE IS NOT A COOLDOWN, and that nearly ruined the rake. Volleys keep counting while a rake
sweeps, so "arm every third volley" let the next one begin the instant the last retracted -
measured 34.6 seconds of rake in a 45-second sample, 77% of the fight. At that density it stops
being a hazard you survive and becomes the room you live in, which is the exact failure the retract
was meant to prevent. A real cooldown now starts when the rake ENDS: 23.1s of 45, sweep then open
floor.

AND I WROTE A BUG FIXING IT: the cooldown decrements inside beamRakeTick, and both call sites only
called that function while a rake existed - so the cooldown would have frozen the moment the sweep
ended and no rake would ever have armed again for the rest of the fight. Both sites now tick while
either is live. Caught in the same pass, asserted so it cannot come back.

TWO MORE PROBE FAULTS, both reporting working code as dead:
  Pinning the boss's HP to keep the fight alive means it NEVER MORPHS past form 0 - and form 0 is
  deliberately the gentlest of the four, so "the finale at full health" measures the opener as if
  it were the whole fight. Each form is built explicitly now.
  And buildModularBoss RE-ARMS THE POWER-ON (`_be`), which makes updateBoss return early - so
  every form measured as firing NOTHING, 0 shots in 45 seconds, four times over.

Suite 2,600 / 232 / 5 - the same five long-standing failures.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
