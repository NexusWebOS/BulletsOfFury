# Passover 0809r — Decker/Freezer, and the attract reel becomes a demo

## 1. Decker and Freezer were swapped in the arcade intro pack

Mike: *"you made decker freezer and freezer decker. fix that."*

The plate labelled **DECKER** showed the dark-haired pilot with the fur collar and snowflake; the
one labelled **FREEZER** showed the blond in gold with glasses.

The game's own data settles which body owns which name, and it is not close:

| pilot | role | tint | `port_*_idle` |
|---|---|---|---|
| DECKER | TECH CONNOISSEUR | `#ffd24a` gold | blond, glasses, gold/black |
| FREEZER | FROSTBITE | `#6fd0ff` ice | dark hair, fur collar, snowflake |

**The extraction was not at fault** — `aintro_decker.png` is byte-identical to
`Decker/decker-arcade-intro-640x480.png`. The *pack's own folder names* are what lie. That is rule
1 one level further out than usual: this time the thing to distrust was the source directory.

Each plate's background and name panel were already correct — tech corridor + ORDER OF THE MATRIX
for Decker, ice hangar + AIRFORCE for Freezer. Only the character layers sat on the wrong plates,
and the pack ships those separately, so the fix recomposites entirely from authored art:

```
background  +  the correct pilot layer at (78,42)  +  authored panel art from x>=300
```

(78,42) was template-matched and lands on an exact pixel match for both.

**`x>=300` is the part that matters.** Copying every pixel where the composite differs from
`background + own layer` drags the OLD body's rim glow along with it, and you get a ghost
silhouette standing behind the new pilot. 300 clears the character column and its glow while
keeping both text panels whole.

All nine were then checked against `port_*_idle`. Only these two were swapped.

## 2. The attract reel is a demo now, not a slideshow

Mike: *"I told you not to make those basic ass windows or fonts for the cinematics. And you should
fade to their card, and then show their ship going off and actual gameplay with their special
abilities."*

Three beats per pilot:

| beat | what |
|---|---|
| PLATE (1.8s) | the authored `aintro_*` plate, **nothing drawn over it** |
| CARD (1.3s) | cross-fade to that pilot's card |
| DEMO (3.6s) | the real game |

The plate already carries its own PILOT DEPLOYED banner and name panel — my `PRESS START` was
sitting on top of finished art. It now blinks over the **demo** only, which is where a real cabinet
puts it.

The demo is live, not recorded: it sets `run.pilot`, calls `beginStage`, and drives `updatePlay` +
`drawWorld` directly — exactly what `test_fl.js` and `shoot.py` do. The ship rises into frame from
below the bottom edge (the "ship going off"), an autopilot flies and fires it, and
`startSpecial()` triggers the pilot's ability at 1.45s.

Live beats recorded on every axis that matters here: nothing is baked, so it costs no megabytes and
**cannot go stale** when a weapon, a pilot or a stage changes.

### ⚠ `beginStage` drives the state

First attempt came back `state=opening` with the reel frozen. `beginStage` runs the stage card and
launch sequence and hands the screen to `GS.OPENING`, so the attract dispatch was never reached
again. The demo now takes the screen straight back with `setState(GS.ATTRACT)` — the same move the
harness makes when it forces `GS.PLAY` after `beginStage`. `updatePlay` has no state gate of its
own, so it runs perfectly happily under `GS.ATTRACT`.

On the way out the demo empties the world arrays, so a live wave is not still running behind the
next pilot's plate.

## 3. Verified in the browser

- plate beat: authored Cole plate, clean, no overlay
- card beat: cross-fade to his card
- demo beat: real water stage, real enemies and explosions, bullets streaming
- Axel's demo shows the 5-orb aegis ring around his ship — the special genuinely fires

## 4. Note

`attractIdleTick` is defined and never called. The 12-second idle-to-attract trigger is dead code,
so nothing can launch a demo from a menu mid-session.
