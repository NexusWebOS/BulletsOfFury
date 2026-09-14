# Green in-game pause menu — September 14, 2026

Pause now freezes combat while menu rows drop in with existing cues. The default
top selection is Resume. The main-menu cursor uses its existing flashing green
variant. Resume, Return to Main Menu, Restart Level, Options, Help and Quit Game
are reachable by keyboard/controller or mouse. Existing chrome drawing helpers
and authored fonts/cursor are used; new SpriteCook bitmap button production is
still pending.

The playfield renders to one reusable offscreen frame and is composited in
grayscale; menu/cursor remain colored. Music ducks to 28 percent independently of
the preference shown in Options. Resume removes that temporary reduction.
Options and Help reuse the real screens, return to pause and do not tick combat.
Backspace cannot abandon the level. Restart resets the same stage and pilot.

Return to Main Menu/quit verify campaign autosave before starting the real
anchored burning spin, crash/shock/explosions, game-over sound/over voice, and
fade. Saving failure keeps the menu open with an error. The latest successful
campaign record can recover Continue when the in-memory session is lost.
Manual save slots are preserved. Controls reset preserves autosaves as well.

Autosav01.json/02.json/03.json are rotating serialized JSON **records in browser
localStorage**, separate from manual slots. They are not Windows files downloaded
into the repository. A SAVED label is displayed only after the actual record
has been written and read back identically. Arcade exit does not write a campaign
autosave. Exit uses the existing game's exited state after the sequence.

Syntax passes. Full suite **3,756 passed / 61 failed, exit 1**, final summary
reached; all failure names match docs/qa/stage_1_5_0914.json. Eleven section-302
checks pass. Chromium **14 / 0**, zero page/console/loop errors. Music preference
and actual element volume, decoded background/grayscale pixels, Options/Help,
native death spin, restart, save readback and campaign recovery verified.
LF runtime/CRLF suite preserved.

Proof: docs/qa/pause_menu_0914.json.
Sources: _BUILD_SOURCE/pause_menu_0914/.
Screenshots: _shots/pause_menu_0914/.
Do not run older integration workflows over this runtime.
Nothing committed/pushed; no user-data deletion or atlas edits.
