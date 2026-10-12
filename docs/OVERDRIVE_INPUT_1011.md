# Overdrive controller and aiming correction — October 11, 2026

Mike reported that controller bindings, mouse aiming and directional fire had
stopped working. The native regression probe reproduced ten failing cases.

## Corrections

- Saved D-pad assignments now override their default physical button and stick
  fallbacks, including intentionally unbound directions. Reassigned face buttons
  no longer also move the tank. Bindings survive reconnect and reload.
- Movement, cruise and Retina do not claim turret aim. Real mouse movement can
  aim while a controller or keyboard drives. A new right-stick deflection takes
  control, and Q/E can turn the turret with an idle mouse over the playfield.
- Six-button firing aims independently in all eight directions. Cruise uses
  explicit mouse/stick aim before its D-pad aiming fallback.
- The boss dossier uses menu controls, so physical B returns to its overview.
- Only physical fire inputs held when the introduction ends wait for release.
  Holding Retina cannot suppress another fire button, and a new mouse press
  can fire while an old inspection button remains held.

The user's saved controls are retained. The original Options renderer, tank
movement speeds, shot cooldowns, authored sprites and close camera view remain
as previously implemented. Launcher/module cache stamp: `overdrive1011-input-r1`.

## Verification

Real Chromium via `_BUILD_SOURCE/shoot.py`, using isolated saves, real keyboard
and pointer events, and synthetic standard/six-button Gamepad reports:

- Input regression probe: **28/28**, including actual projectile vectors,
  nondefault bindings, reconnect/reload, and fire release at introduction exit.
- Existing original frontend probe: **55/55**.
- Existing Warrior introduction probe: **42/42**.
- **125 native checks pass**, with no page, console or asset errors.
- Captured the actual authored tank driving north while its turret and shots
  point east; inspected the rendered screenshot.
- Syntax checks pass for the base game and edited runtime modules.
- Required base suite: **8,700 passing assertions, zero errors, exit 0**;
  reached `==== FALVA/LIZZIE BUILD OK, 0 ERRORS ====`.

Physical hardware was not connected to these tests. Fixtures use the same browser
Gamepad polling path as hardware. Results: `docs/qa/overdrive_input_1011.json`.
Ignored captures/logs: `_shots/overdrive_input_1011/`.

Local changes only; no commit or push.
