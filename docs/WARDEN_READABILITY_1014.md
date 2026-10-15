# Stage 4 Warden feedback and readability — October 14, 2026

Mike reported missing hit flashes, excessive/unpredictable pressure, small
helpers and missing attack sounds after the Stage 3–4 encounter update.

The SA14 renderer explicitly passed zero flash for the Warden's modular plates,
zeroed VP12 aircraft flash timers during drawing, and drew its new helpers with
no hit tint. Those suppressions are removed. Native `markHit`, hull/part timers,
authored frames and their cached hit tints now remain responsible for feedback.
Actual hull, gun-module and helper damage was compared pixel by pixel. The
normal camo/metal artwork returns when the native hit timer expires. This rule
is now explicit in `AGENTS.md`, including future bosses, modules and helpers.

The Warden's balancing is separate from the Stage 3 encounters and Sovereign.
Targets commit before the tell and remain fixed throughout a finite release.
There is no per-shot reacquisition. Main weapons and helpers take separate
turns, with a recovery before main weapons resume. Destroyed modules stop firing
through the existing mount/part ownership checks.

| Difficulty | Main warning | MG rounds | Missile waves | Recovery | Helpers | Helper warning | Helper rounds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Easy | 2.40 s | 4 | 1 | 1.90 s | 1 | 1.35 s | 3 |
| Normal | 2.15 s | 6 | 1 | 1.70 s | 2 | 1.20 s | 4 |
| Hard | 1.95 s | 8 | 2 | 1.50 s | 2 | 1.05 s | 5 |
| Furious | 1.80 s | 10 | 2 | 1.35 s | 2 | .95 s | 6 |

Main MG cadence is .24/.21/.18/.15 seconds; speed is 3.0/3.4/3.8/4.2 versus
the previous 4.5/5.2/5.7/6.2. Missiles travel at 2.6/2.9/3.2/3.5. Easy fires one
missile from each surviving box; other difficulties fire two per box per wave.
Each missile lane is shown before release. The gaps and finite round budgets
replace the previous 2.6-second rapid-fire stream and up to six rocket waves.

Helpers have a separate 1.8-second south-entry warning, 2.2-second harmless depth
entry and their own yellow/red aiming lane and warning sound before firing.
Their combat span is 96 rather than 64 pixels, retaining one proportional scale
and the existing authored camo heading frames, shadows and transparent padding.
They station outside the main hull, turn smoothly through authored headings,
fire one committed burst apiece in sequence, then leave. Maximum population is
one on Easy and two otherwise; the old Furious limit was five. They use the
regular aircraft family's HP instead of an extra minimum-eight-HP override.
If camera movement hides a helper, it cancels its attack and exits safely.

The MG calls previously used the player's `machineGun` function, which is
intentionally muted while Cole's upgraded gun owns that cue. Main weapons now
use `enemyMachineGunHeavy`, helpers use `enemyMachineGunLight`, and their real
barrels own authored muzzle flashes. `Audio.SFX.missileLaunch` did not exist;
volleys now call the approved `missile` chip launch cue. Entry uses the existing
jet-thrust cue and aiming uses the shared authored warning sound. These cues are
prepared during Stage 3–4 loading and honor the existing volume/mute controls.
No sounds or images were generated or replaced.

Verification uses the shipping page, actual update/collision/render owners and
actual media output. The focused probe checks all difficulties, finite releases,
aim commitment, entry timing, helper bounds, separate turns, damage pixels and
expiry. It also measures nonzero decoded output for both enemy guns and the
native chip missile cue with Cole's upgraded weapon equipped. The first meter
attempt did not sample the chip cue's native media route; the corrected probe
uses that route. Initial fixture/meter logs remain under ignored `_shots`.

Twelve 30-second steering samples use real keyboard events, no firing, shields,
roll, somersault or special, and ordinary half-second movement decisions. They
show surviving samples on each difficulty with three starting lives; they are
controlled observations, not a human campaign-clear percentage or hardware test.

Reproduce with `_BUILD_SOURCE/probe_warden_readability_1014.py`. Existing Stage
3–4 gameplay and visual probes now expect the revised helper schedule and
mandatory primary/fallback hit flashes. Source and screenshots remain under
`_shots/warden_readability_1014/`; portable evidence is in
`docs/qa/warden_readability_1014.json`.

Local changes only; no commit or push requested for this pass. Unrelated
Overdrive changes and existing project notes are preserved.

Final result: 55/55 focused native checks, zero browser errors. The existing
Stage 3–4 gameplay/visual probes pass 60/60 and 13/13. The final full suite ends
BUILD OK / 0 ERRORS, exit 0, with 8,700 passing assertions. Game and module syntax
and scoped whitespace checks pass; actual warning and hit screenshots inspected.
