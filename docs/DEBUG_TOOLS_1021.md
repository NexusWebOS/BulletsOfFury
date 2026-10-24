# Debug toolkit (1021) — Boss Mode and debug-mode upgrades

Mike: *"can you improve and upgrade my boss mode and debug modes please?"*

Owner: `assets/debug_tools_1021.js` (loaded last in `index.html`). Active only where debug is armed:
the title code (UP UP DOWN DOWN A B C), `index.html?debug=1`, or the Boss Mode host
(`index.html?bossmode=1`). A normal game is untouched — suite section 388 asserts the speed scale
does nothing outside debug.

## In a fight (title-code DEBUG mode, or the Boss Mode stage with the engine focused)

| key | what |
|---|---|
| **F8** | debug HUD: fight clock, boss HP + phase bar (75/50/25 ticks), pattern, DPS (3 s window), damage dealt, hits taken, deaths, lives, enemy / enemy-round / player-round / particle counts, peak rounds, speed, FPS |
| **F9** | GOD — `playerHit` refuses every hit. Not a pinned invuln timer, so the ship never blinks |
| **F10** | restart the current fight, same pilot and difficulty |
| **[** / **]** | freeze the combat clock / step exactly one 60 Hz tick while frozen |
| **-** / **=** / **0** | combat speed 0.10x … 2.00x / back to 1.00x |
| **1 2 3 4** | boss HP to 75 / 50 / 25 / 5 % (phase jumps) |
| **5** | kill the boss (the death branch) |
| **6** | current weapon to level V |
| R / F6 | record / scene overlay (unchanged) |

With the HUD off, a small `GOD 0.50x FROZEN` tag stays top-right whenever an assist is on.

## The debug menu

- **Difficulty cycles all five**, INSANITY included (it was hard-coded to four).
- **Best time per fight**, per difficulty, in each cell (gold, right side), saved in
  `localStorage.bof_debug_best_v1`.
- **LAST:** line — the last fight's result: win/lost, time, deaths, hits, NEW BEST.
- F8 / F9 toggle the HUD and GOD from the menu too; both are remembered.

**Best times count only unassisted wins.** A run that used GOD, a speed other than 1.00x, freeze,
an HP jump, kill or a weapon grant is recorded and marked ASSISTED, and never becomes a best — the
best time is a balance number and an assisted clear would make it lie.

## Boss Mode editor (`bossmode.html`)

STAGE toolbar: **GOD** (was INVULN, which blinked the ship), **SPEED** now 0.1–2.0 and actually
works, **FREEZE**, **STEP**, **RESTART**, phase-jump buttons **75 / 50 / 25 / 5**, and an
**ENGINE HUD** checkbox. Editor keys (with focus outside the game): F9 GOD, F10 restart, `[` `]`
freeze/step.

Footer: live `T 1:23.4  DPS 45.2  HITS 2  DEATHS 0  BEST 1:10.2  ASSISTED`.

CLIPS tab: a **RUN LOG** — every fight played, newest first, with result, time, difficulty, pilot,
hits, deaths, damage dealt, NEW BEST and the assists used. The engine reports each result through
`window.BOSSMODE_ONRESULT` on the editor window.

Engine surface: `BOSSMODE.tools` — `god`, `speed`/`setSpeed`, `frozen`/`freeze`/`step`, `ticks`,
`hud`/`setHud`, `restart`, `setHpFrac`, `kill`, `maxWeapon`, `stats()`, `last()`, `best()`,
`clearBest()`. `BOSSMODE.setInvuln` / `setTimeScale` now route to GOD and the speed scale.

## Bugs fixed on the way

- **The editor's SPEED slider never worked.** It set `timeScale`, which `updatePlay` resets to 1
  every frame unless Freezer's special is live; and `timeScale<1` only ever meant "skip odd frames"
  (a fixed half speed). Speed is now a scale on the dt handed to the fixed 60 Hz combat clock
  (`maneuver_safety_1007.js`), so 0.25x runs exactly 15 ticks a second.
- **INVULN blinked the ship** — `player.invuln=1e9` drives the damage blink.
- ⚠ **Hotkeys read after the combat clock are eaten at 2.00x.** A frame that runs two ticks calls
  `Input.clearTaps()` between them. The toolkit reads its keys at the top of `combatFrame`.
- ⚠ `BOF_COMBAT_CLOCK`, `state`, `boss`, `bossActive` are lexical — not on `window`. From the
  editor, read them through `BOSSMODE.snapshot()` / `BOSSMODE.tools.ticks`.

## Verification

`python3 _BUILD_SOURCE/probe_debug_tools_1021.py` — 45/0 in real Chromium with real keys, zero
page/console errors. Busted arms: with GOD off the same `playerHit` costs a life; at 1.00x the clock
runs 120 ticks in 120 frames (0.25x → 30, 2.00x → 240). Proof frames in
`docs/proofs/debug_tools_1021/`. Suite section 388 (`test_debug_tools_1021.cjs`).
