# Chronos hammer return alignment

The recall previously targeted a guessed hand offset and ended on a vertical flight view. It now targets the actual H22 held frame hammer-head socket through hb20World and finishes on authored flight view5. Ordinary returning throws settle to the same orientation and scale over the final150 world pixels. Knocked-away and armor-break recall use the same final scale.

Measured cyan energy head: original held source31x36 at1.75 =54.25x63 world pixels. Authored flight view5 source83x88 uses one uniform0.687 scale, giving57.02x60.46. No nonuniform stretching or held-body reconstruction. Native last recall position differs from final target by under0.2px. Original held pose remains intact.

Focused Chromium6/6 passed; last recall and caught screenshots inspected. Syntax passed. Required test_fl still exits1 before assertions/final summary because retired_art_archive_1022.cjs is missing.

Full recording and review findings are in docs/CHRONOS_FIGHT_REVIEW_1025.md after completion. No commit/push.
