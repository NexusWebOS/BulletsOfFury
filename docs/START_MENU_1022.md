# The game-mode START menu, and no BACK out of a game mode (2026-10-22)

Mike: *"we need a start menu system similar to the in-game start menu, but it allows you to select Return to Menu,
Save Game, Load Game, Options, Forge/Loadout, Quit Game. Only those options when you've entered a game mode. you can
no longer press back or your assigned B button to exit a menu or screen like pilot select, or being in the arcade or
campaign game mode itself. Ive noticed I could press back on the pilot select screen, that should be disabled. When I
selected Campaign and then was in the map, I pressed back and went to selecting the game mode, no good."*

Runtime: `assets/start_menu_1022.js`, loaded last in `index.html`. `window.SM22_OFF=1` turns all of it off.

## What changed for the player

**Game-mode screens** are difficulty (except the password route), the campaign hub, pilot select, the co-op roster,
the campaign map, and the stage-1 opening / outbound cinematics. On those:

- **B, Escape and K do nothing.** They are swallowed, so no screen can be left that way. The hint rows that said
  `B BACK` now say `START MENU`.
- **START (P on the keyboard, the pad's START) opens the menu.** Enter does not: Enter is the confirm on all of these
  screens (on the map it is DEPLOY, 0917d).
- Presses that move *inside* a screen still work: the co-op seat rewind (P2 back to P1), the campaign hub's slot
  picker cancel, the map's button bar and its Stage X focus.

**The menu** draws over a greyed, frozen copy of the screen, on the same plate as the in-game pause:

| row | does |
|---|---|
| RETURN TO MENU | ends the campaign (if any) and goes to the title |
| SAVE GAME | campaign slot list, from the live campaign map. Arcade and other screens say why not |
| LOAD GAME | campaign slot list (auto save first) from any game-mode screen; opens the map |
| OPTIONS | the options page; APPLY / CANCEL / B come back to the menu, not to the title |
| FORGE / LOADOUT | from the campaign map: the Forge, then the loadout, then back to the map |
| QUIT GAME | exits |

B or START closes the menu. Unavailable rows are dimmed and the reason shows under the list.

The in-game pause during play is unchanged.

## Traps found

- **`menuBackTick` routed game-mode screens before the screen saw the press.** `MENU_BACK` still maps
  PILOT -> DIFF and STAGESEL -> MODESEL, and the router runs first, so the co-op seat rewind never worked: Escape on
  P2's pick dropped both players to difficulty (measured). On a locked screen the router now only lets the map's
  Stage X focus use it.
- **The Forge refills the stage's budget on every open.** `forgeStart` hands out a fresh `FORGE_COMBOS_PER_STAGE` and
  `FORGE_RESPECS_PER_STAGE` each time; from the map that would be unlimited upgrades. The menu puts the counts back.
- **`optApply` / `optCancel` both end on `setState(GS.TITLE)`.** While the menu owns the options page that call is
  swallowed.
- **The frozen frame carries the screen's own hint row**, which read as one garbled line with the menu's hints until
  a dark strip went under them.

## Verification

`_BUILD_SOURCE/probe_start_menu_1022.py` (real Chromium, real key/pad presses): **31/0, 0 page or console errors**,
with a busted arm (`SM22_OFF=1` lets B leave pilot select again). `probe_menu_confirm_0918f.py` 9/0 after its back
check moved from difficulty to credits. Proof frames: `docs/proofs/start_menu_1022/`.
