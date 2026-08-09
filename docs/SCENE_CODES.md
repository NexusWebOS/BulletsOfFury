# SCENE CODES + WHERE THE TRANSITIONS STAND

## COLE1 .. COLE9

Type at the password screen. Each drops you into stage N with its boss **already up and on its
last sliver of HP** — the kill, the death, and the handoff to the next stage are one shot away.

    COLE1   stage 1        COLE4   stage 4        COLE7   stage 7
    COLE2   stage 2        COLE5   stage 5        COLE8   stage 8
    COLE3   stage 3        COLE6   stage 6        COLE9   stage 8 finale

What each code sets up:

    boss spawned, active, entrance skipped   you are AT the fight, not watching it arrive
    boss at ~4% HP                           a sliver, not zero, so you land the kill and see
                                             the death animation and the transition
    mech bosses skip the genesis haul        straight into phase 'fight', limbs at 15%
    modular bosses drop to 15% per component
    wave script and sub-boss already spent   nothing else is on screen
    6s of player invulnerability             enough to line the shot up

Applied at the END of beginStage, after the stage is fully built underneath it — same placement
as the opening cinematic, and for the same reason.

**A bug found while adding these:** the password field was capped at 4 characters. There is
already a 6-character unlock in `submitPassword` — `COLE4U` — which meant it could never be
typed. Raised to 6, so that one works now too.

The scene codes are kept OUT of the `PASSWORDS` table on purpose. Those set a starting stage;
these set up a situation. Separating them means the normal codes behave exactly as before.

## The transitions themselves

They are still OFF, at your instruction from the earlier session:

    DBG.transitions = false
    /* TRANSITIONS TEMPORARILY OFF (drop 0724do). Mike asked to disable them to rule them out.
       One flag, checked here and in the outbound, so it is a single line to put back. */

Two places read it — `beginStage` for the stage-1 opening, and `TRANS[fromStage].via` for the
outbound terrain routes. Flipping the flag restores both.

**I could not recover your original spec.** I searched the previous session for it and the
transcript has the transition ART (`03-stage-transitions` in the megapack, 96 `ntr_*` keys
registered) and the fact that the system broke and was disabled — but not what you actually
described wanting it to DO. That detail did not survive into the summaries.

So rather than guess at it and rebuild the thing that broke the game, tell me the stage-1-to-2
handoff as you picture it and I will build that one, alone, and you can check it with COLE1
before we go near stage 2.
