# Overdrive menu, controls and Warrior revision — October 11, 2026

Entry: `expansion/topdown/index.html`. Current work is local and uncommitted.

## Startup and original presentation

Start → BOF/Overdrive intro → title → difficulty → pilot select → briefing.
New Game begins Iron Infiltration. The authored campaign continues through
Machinists: Rebel Siege and Museum of Violence. Continue resumes the saved
campaign position; a successful password restores a position through pilot
select. There is no opening mission-selection menu. The shelved Level 3 remains
intact and hidden.

The title uses the original BOF logo, cover, bitmap alphabet and Title music,
with the existing Overdrive wordmark and newly generated expansion buttons.
Selection has the original arrow graphics, glow and confirmation flash. The
pilot screen restores the body/aircraft/biography/stat card arrangement, framed
avatars, two rows of six portrait/ship pairs, card flip, text reveal and stat reveal. The original nine
pilots retain their actual authored portraits, bodies, aircraft, affiliations,
special labels and original stat values. Hotwire, Phoenix and Niel join that
roster. PilotSelect music plays on that screen.

The pilot menu is 640 × 512 logical pixels; all twelve avatars fit two rows of six.
Left/right moves within a row, up/down moves to the matching column in the
other row, and clicking either portrait or ship selects that pilot. Options
uses the original BOF 480 × 512 viewport. Smaller
browser panes use one proportional display scale without cropping. Gameplay
uses the requested closer 640 × 480 field and proportional fullscreen fitting.
The new [Warrior introduction](OVERDRIVE_BOSS_INTRO_1011.md) rolls in from above,
tracks and pulls out with the camera, displays a generated rotating dossier,
then slides away and restores normal 1:1 combat zoom. The canvas never resizes
at arena entry. The previous 800 × 600 view is superseded.

Mike's difficulty-art correction restores the exact original purple Insanity
skull plate. Furious uses a new chaotic melting skull in the Overdrive frame
with its red label. Both exports are 768 × 224 with center pivot (384,112),
proportional scaling and transparent padding. Their active filenames are
`od_diff_insanity_original_1011.png` and `od_diff_furious_melting_1011.png` under
`expansion/topdown/art/menu_1011/`. Sources and generation prompt are preserved;
the owning `build_menu_art_1011.py` registers the revisions on every build.
The targeted native Chromium check passes 12/12 with zero browser/media errors;
both selected states and the narrow view were inspected. It compares decoded
opaque artwork pixels and traces the game context's actual `drawImage` calls.
Evidence: `docs/qa/overdrive_difficulty_1011.json`; exact built-in imagegen prompt:
`expansion/topdown/_research/difficulty_generation_1011.json`.

Insanity is visibly locked until the campaign is completed. Keyboard/controller
confirmation, password load and direct launch all enforce the gate. The unlock
persists across future runs and reloads. The original purple plate is retained.

## Options and controls

- Original BOF Options renderer: original panel, font, cursor animation,
  scrollbar, key caps, volume segments and Apply/Cancel controls. Thirteen
  renderer helpers are copied verbatim; the main renderer receives Overdrive
  action data and its canonical input/save adapters. There are no custom tabs.
- Sound: original Master, Music, SFX and Voice strips; changes preview immediately.
- Keyboard: every existing gameplay/menu action can be rebound or reset.
- Controller: Six Button and Standard Pad presets, individual physical-button
  binding, reset, and full learning with neutral separation between inputs.
- Apply saves; Cancel restores the previous settings and bindings.
- B is Back; Backspace only deletes password text. Escape cancels key capture.
  Controller learning has a generated Cancel plate for pointer cancellation.
- Help includes six-button tank, standard-pad tank and on-foot schemes.

| Input | Tank action |
| --- | --- |
| L shoulder | Cruise in the previous drive direction; D-pad freely aims the turret. Fire remains independent. |
| R shoulder | Hold Retina; fire/release the cannon after lock to launch a tank missile. |
| Six-button Mode + C | Speed boost; ordinary C still charges/releases the cannon. |
| Standard left trigger | Speed boost; right stick aims independently. |
| Keyboard F / R / I | Cruise / boost / Retina, all rebindable in Options. |

Learning records all 14 six-button controls or all 13 standard-pad controls,
including L/R. Profiles persist by controller ID. Default physical button
numbers are examples; learning is the way to match Mike's actual controller.
Cruise releases into braking and uses the normal solid-cover collision pass.

The approved engine sample is unchanged. Its cue gain is **0.08**, previously
0.22 (36% of the previous amplitude), and boost playback rate is 1.12, previously
1.22. The separate Engine slider further scales actual engine voices. Idle
still uses 65% of the moving gain; treads and traverse keep their own cues.

## Overdrive passwords and saves

New checkpoint codes have the form `OD-xxxx-xxxx`, with a checksum and an
Overdrive-specific alphabet. A code carries campaign position, pilot,
difficulty and companion. Results display the next checkpoint code. Legacy
BOF codes and malformed codes reject. The menu supports controller keypad
entry or Type with a keyboard; Backspace deletes while typing.

Stores: `bof_od_campaign`, `bof_od_options`, `bof_od_keys`, `bof_od_pad_style`,
`bof_td_controllers`, `bof_od_achievements`. These do not replace base-game saves.

## Generated achievements

Sixteen new Overdrive medals are connected to play events: deployment, moving
boost, cruising while turning the turret, Retina launch, six destroyed
structures, Warrior defeat, no-death Warrior defeat, Machinists defeat, a clear
as each of Hotwire/Phoenix/Niel, five CQC takedowns, complete hostage rescue,
no-alarm clear, the three-mission campaign, and a full Furious/Insanity campaign.
The gallery shows points, locked/earned state, an earned filter and toasts.

Four general-game badges also work in the original game:

| Award | Requirement | Points |
| --- | --- | --- |
| Ace Squadron | Clear missions as three different pilots | 100 |
| Battle Hardened | Clear ten missions | 100 |
| Flawless Fury | Three consecutive mission clears without a death | 150 |
| Combined Arms | Maximum level in three different weapon families | 100 |

`assets/general_achievements_1011.js` extends the original public achievement
functions and XART gallery, with its own persisted store. Existing awards keep
their order; the new General family sits after the original 200-point families.
Original weapon maxima are level 5; Overdrive's actual ground maximum is level
3 and its completion event feeds the same general award. Re-reporting one
original stage-stats object does not duplicate a clear. Original `assets/game.js`
was not edited by this pass.

## The new Warrior

`art/warrior_mk2_1011/` is the active bank. It contains a new navy/silver siege
chassis, triangular ram prow, warrior helmet with a red visor, two long artillery
arms, matching damage state and wreck. It is inspired by the supplied HK
reference and our authored tanks. The old olive Warrior bank remains intact.

Hull/damaged/wreck canvases are 640 × 512 with one pivot and scale. Torso/arms
use 512 × 512 canvases with explicit physical mounts. The chassis canvas draws
at 332.8 pixels; the assembled front spans about 437.6 world pixels. Modules
keep their original art, angle, pivot and proportional scale when detaching,
then rotate, fall and settle. The existing bullets, lasers, missile salvos,
sideways lower-body turning, cover-breaking ram and supplied boss music remain
the encounter. No boss charge orb is added.

## Startup recording

The original `assets/game/shared/audio/sounds/announce.mp3` BOF call plays first.
Mike's supplied `overdrive.wav` follows with a short room reverb and arcade echo,
matched to the original call's measured loudness (-16.31 LUFS reference,
-16.30 LUFS processed). Natural pitch is retained. The source WAV is preserved byte for byte
at `expansion/topdown/audio/source/overdrive.wav`; the browser copy is
`expansion/topdown/audio/overdrive-reverb_1011.mp3` (256 kbps, stereo, 44.1 kHz).
The earlier dry MP3 remains stored. The processed call includes its echo tail.

The intro waits for actual media completion. Start/B skip and stop playback,
including physical controller buttons; saved Master/Voice gains apply. Leaving
for another menu also releases the recording. See
[the recording verification](OVERDRIVE_STARTUP_1011.md). The current module
stamp is `overdrive1011-restored`. Fullscreen is the server launch default;
native Fullscreen/Windowed controls and Alt+Enter are available. The missing
Return to Main Menu, Fullscreen, Windowed and Locked plates are generated and
registered through the menu builder. Current verification for this correction
is in `docs/qa/overdrive_restored_1011.json`.

## Owners and reproduction

- `build_menu_art_1011.py`: 46 menu exports and six Warrior module exports;
  fixed even canvases, uniform proportional scale per bank and source hashes.
- `export_original_pilot_1011.py`: read-only original-runtime export of pilot
  presentation metadata; records the current original game source hash.
- Generation prompts: `menu_generation_1011.json`,
  `menu_generation_revisions_1011.json`, `general_generation_1011.json`.
- Generated masters live under each bank's `source/`; rejected drafts are
  preserved. The builder registers the actual sheet order, not its filenames.
- Base atlas/manifest cells were not repacked. Original assets are referenced.

```powershell
python expansion/topdown/_research/build_menu_art_1011.py
python expansion/topdown/_research/build_original_options_1011.py
python expansion/topdown/_research/build_startup_audio_1011.py
python expansion/topdown/_research/export_original_pilot_1011.py
python expansion/topdown/_research/probe_restored_frontend_1011.py
python expansion/topdown/_research/probe_chip_audio_1011.py
python expansion/topdown/_research/probe_warrior_1011.py
node --check assets/game.js
node _BUILD_SOURCE/test_fl.js
```

Native verification uses `_BUILD_SOURCE/shoot.py`'s real Chromium server and
renderer, real keyboard/pointer events, browser Gamepad polling with test
hardware, decoded media and actual pixels. Protected combat and completion
fixtures verify event integration; they do not claim an unassisted campaign
clear or final difficulty balance. Screenshots and both page/console errors
were inspected. Current correction evidence is in
`docs/qa/overdrive_restored_1011.json` and ignored
`_shots/overdrive_restored_1011/`. The earlier custom-tab menu checkpoint is
preserved in `docs/qa/overdrive_menu_1011.json` for history.

Current correction: **55/55 restored frontend + 44/44 sound = 99/99 native checks**,
zero browser errors; **8,700 base assertions, zero errors, final summary and exit 0**.

Initial menu checkpoint: **53/53 menu + 43/43 sound + 22/22 Warrior = 118/118 native checks**,
zero browser/media errors. The base suite reaches **8,696 passing assertions,
zero errors, exit 0**, including its final summary. Earlier five chip-pass
failures are absent in the current shared checkout.
