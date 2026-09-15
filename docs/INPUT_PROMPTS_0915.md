# UI-16 — Mouse and keyboard prompt art

Six new Bullets of Fury input prompts match the existing Help-screen cabinet controls: a neutral mouse, red left-click mouse, red right-click mouse, wheel, Spacebar and R key. Each production icon is an independently trimmed transparent PNG under `assets/game/ui/input_prompts_0915/`; the preserved magenta source and extraction manifest sit beside them.

The runtime registers every icon without modifying generated `manifest.js`. The Help controls page now replaces its text-only mouse explanation with the neutral, left, right and wheel graphics. Options uses the corresponding generated icon whenever a binding is left mouse, middle/wheel, right mouse, Spacebar or R, while every other binding keeps its existing live text label.

## Verification

- `_BUILD_SOURCE/test_input_prompts_0915.cjs` validates six files, six runtime registrations, input mapping and both consuming UI paths.
- `node --check assets/game.js` passes.
- All six runtime images are distinct RGBA files with real transparency.
- Native Chromium review decodes and displays all six production files against the game UI background.
- Full `_BUILD_SOURCE/test_fl.js`: 4,337 passing assertions and 57 existing unrelated failures; no input-prompt assertion failed.
