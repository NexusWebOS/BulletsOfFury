# THE HARNESS WAS TESTING THE WRONG TREE

Found while wiring the boss fight system. Worth reading before trusting any earlier green run.

## What happened

Both harnesses had a hardcoded root:

    const ROOT = '/tmp/build/BulletsOfFury';

That was the CODE-ONLY tree from the start of the session, before the full game with assets
arrived. Once work moved to the real tree, `test_fl.js` and `verify_0730a.js` kept loading the
old `assets/game.js` — a build from 04:39 — while the live one was hours newer.

So every "1335 assertions, 0 errors" I reported after that point was green against stale code. The
number was real. What it was testing was not.

Fixed: `const ROOT = require('path').resolve(__dirname, '..')`. The harness can now only test the
tree it lives in.

## What it was hiding

Pointed at the live tree, the suite immediately found a **real crash**:

    assets/game.js:2964
    const door = b.parts.find(p => p.role === 'door');
                        ^
    TypeError: Cannot read properties of undefined (reading 'find')

Culling boss art means `_bossArtOK` correctly declines to build that boss — so `b.parts` is
undefined, and three separate `.find()` calls downstream assumed it existed. That would have
hard-crashed the game the moment a culled boss spawned. Guarded all three.

## Where it stands

    before (stale tree)   1335 assertions,  0 failures  — meaningless
    after  (live tree)    1755 assertions, 41 failures  — real

The 420 extra assertions are ones the old tree never reached, because it had no art to test
against.

The 41 remaining failures are almost entirely STALE ASSERTIONS rather than broken code — they
test art and systems that were deliberately removed or replaced this session:

    the L2 boss is modular and carries the magma profile   <- it is a mech now
    the cryo behemoth draws its phase body                 <- replaced by the mech system
    stage 5/6 master ... is loaded                         <- culled
    rival jet top-down 4f registered                       <- race content culled

Each needs rewriting to assert the behaviour that replaced it, the way the cesspool, magma
entrance and probe assertions already were. That is a session of its own and it should be done
deliberately, not by deleting whatever is red.

## verify_0730a.js: 46 passed, 0 failed

Including the boss design rules, which are asserted against live values through `bossRules()`
rather than by string-matching source — because matching source only proves the rule was typed.
