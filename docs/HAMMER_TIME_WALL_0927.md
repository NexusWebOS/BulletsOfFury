# HAMMER entrance, flat wall and fighting helpers — September 27

This follow-up supersedes the opening and helper behavior in `HAMMER_TIME_0927.md`.

## Current behavior

- **One giant flat wall, 50% opacity.** Generated eight animation frames here, with straight horizontal rails. Exactly one frame is drawn once at `ctx.globalAlpha = 0.5`, spanning the whole 680px world plus 8px overscan at each edge. No cylinder, separate bubbles or stacked walls. The dancers remain visible through the wall.
- **Locked boss entrance.** The boss descends, raises the existing canonical single-headed hammer, slams it down with the engine's explosions, shock ring and impact sound, then summons four robots in staggered bursts. Controls, weapons, specials, evasion and in-game pause remain locked until all four have arrived. The entrance takes approximately 5.6 simulation seconds. Authored strike/recovery frames are reused; no replacement boss identity.
- **Difficulty-gated helpers.** All four appear on every difficulty. Easy/Normal helpers only dance and are excluded from damage and target lists. Hard/Furious/Insanity helpers fight and can be destroyed. They alternate aimed three-shot pulse bursts and three-round fans; Insanity fan helpers fire five rounds. Existing green/yellow/red FOV warnings, warning signs, muzzle effects, laser audio, white hit flashes, explosions and shock rings are used. A shared attack scheduler permits only one active helper tell/burst at a time, during quieter boss beats. Helpers have 44/64/76 HP on Hard/Furious/Insanity respectively.
- **Real target integration.** Armed helpers participate in Retina scans, space target selection, missiles, direct lasers and shadow area damage. Custom helper damage routes prevent ordinary enemy death handlers from treating them as unrelated aircraft. Death immediately removes them from target lists.
- **Music break preserved.** At 0:16 the group regathers behind the wall, lost helpers are replaced, all combat stops, and the group dances until 0:24. Automatic release restores the previous special and grants 48 frames of protection. The entrance grants 60 frames. The engine uses frames for this field; the prior fractional values were corrected after the expanded test exposed the short grace period.

All changes are isolated to the HAMMER password encounter. The normal campaign Hammer is unaffected; no `assets/game.js` edit was needed.

## Art and integration

New raw RGBA sheet: `assets/game/hammer_time_0927/wall.png`. Generated with the built-in image tool, not SpriteCook. Original alpha and pixels preserved. The owning build `_BUILD_SOURCE/build_hammer_time_0927.py` registers eight cells and measures rail centers to prevent vertical jumping between frames. Original cylindrical sheet is retained on disk but no longer drawn. Prompt/source provenance: `docs/hammer_time_wall_art_0927.json` and `docs/hammer_time_prompts_0927.json`.

Runtime: `assets/hammer_time_0927.js`. Metadata: `assets/hammer_time_art_0927.js`. Existing strike plate: `arch_orbital_sweep_0926`, inspected before reuse.

## Evidence

- Full suite: **5538 passing, zero failures**, final success banner, exit 0; incoming 5513/0. The one intermediate failure caught the frame-versus-seconds protection bug; fixed and retested. Failing-name baseline and final list both empty.
- Syntax checks pass for `game.js`, the encounter and its metadata. `game.js`/runtime LF and tests CRLF preserved.
- Native Chromium probe: frozen entrance position/ammo/HP, no shots or pause; slam occurs before summons; exactly four arrive before unlock. Existing music lock/release and victory-to-title cleanup pass. Easy, Normal, Hard, Furious and Insanity simulated combat remains finite with zoom 1 and reaches the ball attack. Native helper checks prove no Normal attacks/targets/damage, working Hard/Insanity attacks and missile damage, and at most one active helper attack.
- Native draw audit: exactly one wall draw, alpha 0.5, destination `[-8,81.92,696,245.76]`. Screenshots of the actual XART rendering inspected.
- Approximately 36-second real-time Hard recording with supplied music: entrance released at 5.749s with four robots and all 12 missiles intact; no movement/shots/pause during entrance. Dance lock observed at 16.003–23.991s over 500 frames, with zero movement/shot/ammo/pause violations. Audio remained present, sampled capture peak 0.457. Player invulnerability was a recording aid, not a completed gameplay win or balance claim.
- Original and seek-indexed video decode; review images, seek buttons and playback pass. Zero native page/console errors. Review screenshot inspected.

Evidence: `_shots/hammer_time_wall_0927/`. Durable summary: `docs/qa/hammer_time_wall_0927.json`. Review: `http://127.0.0.1:8794/_shots/hammer_time_wall_0927/review.html`.

Remaining: human difficulty/feel and physical controller playtesting. No commit/push. Earlier overnight automation remains paused.
