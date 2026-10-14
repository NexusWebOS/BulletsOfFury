# FURYBOT — a Furious autopilot that plays by the rules (1014)

Mike: *"Make a strong BOT capable of playing on Furious Difficulty and able to live and win without cheating."*

Code: `_BUILD_SOURCE/bot/furybot.js` (the bot, injected into the real game) and `_BUILD_SOURCE/bot/furybot.py`
(the driver: real Chromium, the real index.html, a synthetic 60 Hz clock with the rAF chain trapped).

    python _BUILD_SOURCE/bot/furybot.py --full --pilot cole             # stage 1 to the end, Furious, arcade
    python _BUILD_SOURCE/bot/furybot.py --stage 8 --tag f8              # one stage
    python _BUILD_SOURCE/bot/furybot.py --stage 6 --shots 4             # a frame every 4 game seconds

Report: `_shots/furybot/<tag>/report.json` (per-stage results, every death with the stack of the fatal
`playerHit`, the last 24 planner frames, the boss and hazards in view) and `death*.jpg` frames.

## The rule: inputs only

The bot presses keys through `Input.keys` (held) and `Input.injectTap` (edges) — the same two doors a
keyboard uses. It READS state the way a player reads the screen and never WRITES a life, an i-frame, a
weapon, a shield or a game state. Menus are advanced by key taps. The run starts the way a password
start does (arcade, Furious, `startRun`). A game over is a loss.

Two non-gameplay stubs: the achievement toast is silenced, and `bossHitTest`'s hit-routing notes
(`_s4CoreHit`, `_hammerModuleHit`, `_carrierBayHit`, `_lastPart`…) are saved and restored around the bot's
own probing (`FB.playSafe`), because asking the boss's shape a question must not change which part the
next real round hits.

## The brain, per PLAY frame

1. **Threats** — every enemy round with the engine's own swept-box rule (half-sizes hx+w·0.15, hy+h·0.15),
   hulls with the ram box (e.w/2 + hx − 1). The player's box shrinks with bank, so the bot plans with the
   un-banked maximum (9 x 10).
2. **Hazards** — read from what the game draws and owns: warned beams (`_l23Beam`, the `av3Beam` draw),
   the shared green/yellow/red FOV cones (soft costs), hostile geysers and zone columns, ground strikes
   (lethal only once they stop tracking), lobbed tb28 balls, the Stage-2 firewall and vents, the Chrome
   Hammer's throw / whirlwind / ball / dives / eradication beam / spell pillars, Stage-5 rocks, the
   Razorback hull and pressure waves, the Furnace fire wave, the Overlord sonic ellipse, and (1014, late)
   the final boss's Warhive-copy rounds and its chromium rift (core, pull zone, forked lightning).
3. **Plan** — a space-time grid (cell = speed/√2) with a backward DP over a 30-frame horizon: `V[k][c]`
   is cost-to-go, `D[k][c]` how long a cell stays survivable. The first move is re-checked exactly
   against the real hit rules. A first hit dominates every other cost (60000 + earliness).
4. **Escape** — when the best path survives fewer than 10 frames: barrel roll toward the safer side, else
   somersault (both are real double taps with their real cooldowns). I-frames are planned as ending 45
   frames early except during a roll or somersault.
5. **Offence** — fire held; the attack spot sits under the boss's hittable mass (probed with
   `bossHitTest`), else under the miniboss, else under the nearest air target. Fusion is released at
   minimum charge (0.42 s — best damage per second; it overloads at 3.10 s). The Chrome Hammer's Furious
   armour heals unless the hammer column is hit or missiles break the heal, so the bot targets it then.
   The Storm Sovereign takes damage only on its shield nodes and core turrets. Retina locks the boss and
   manual missiles are tapped (every 16 frames during a heal break, otherwise 50).

## Results (Furious, Cole, arcade, no assistance)

- Stages 1–7: cleared with **0 deaths** on two full runs (A1, A3) carrying the weapons they picked up.
- Final boss (Stage 8, Vile Existence and its eight copied forms): A1, A2 and A3 all ended in game over
  there. The deaths were the Warhive-copy rounds, the Hammer-copy chromium rift (its pull drags the ship
  into the core and the forked lightning), and hull contact when a form appears over the ship — none of
  which the bot could see. Those hazards were added afterwards; see the follow-up runs below.

- Follow-up, same day, with those hazards added: two stage-8 runs started fresh on Stage 8 (base weapons,
  3 lives). **f8a reached the game's own VICTORY state with 0 deaths** (11 hits taken on shields, 905 s
  wall). f8b lost all lives (enemy rounds and miniboss contact). So the bot can win the final stage, but
  not every time yet. A full stage-1-to-victory run (fullA4) was in progress at commit time.

<!-- FOLLOWUP -->

## Traps found on the way

- Cost lines patched into the wrong function (`rzbHit`) threw `c is not defined` only on stage 1.
- A near-miss cost could outweigh hit avoidance; the first hit is now lexicographically dominant.
- Treating warned cones as lethal froze the bot in place; they are soft costs.
- `Z.rects` / `Z.mcirc` were re-initialised AFTER the zone columns and ground strikes were pushed,
  silently erasing them; the lists are created once in the Z literal.
- After a respawn with no surviving path the bot sat in a corner; it now moves away from the hull or the
  nearest round.
- Killer rounds sat inside the real hitbox but outside the banked `_hx` the bot read.
- Holding Fusion overloaded it at 3.1 s.
