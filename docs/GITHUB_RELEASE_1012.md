# GitHub release — October 12, 2026

Mike requested publishing the current Bullets of Fury build to GitHub.
The release retains upstream commit `7539951c` and includes the accumulated
local campaign, boss, weapon, animation, sound and cinematic passes.

- Approved Siege Console side HUD, consistent gameplay/intro/continue field,
  live per-seat readouts and compact/co-op layouts.
- Modular password siege minibosses, Hammer chromium attacks and animation,
  Furnace/stealth animation repairs, Stage 1–9 enemy behavior and difficulty,
  signature specials, wind and elemental weapon families.
- Pilot-referenced HQ/homecoming/survivor cinematics, dark Stage 8 void arena,
  and centered 32-frame portal forming/loop/closing banks with formation spin.
- Approved BOF chip sound pass and Overdrive audio, controller, Retina,
  shoulder aim, Warrior introduction and 640 × 480 display updates.
- Authored graphics, owning builders, review pages and portable QA records
  required by these builds are included.

The remote was fetched and reviewed before publication; it matched local
`main`, so no additional upstream integration was required.

Verification: all 144 changed/new JavaScript files pass `node --check`.
Native QA records report 51 Siege Console checks, 144 portal lifecycle checks,
14 finale checks and 187 Overdrive Retina/input/introduction/frontend/Warrior
checks passing, with no recorded browser errors. The base regression suite
is rerun for publication; its final result is recorded in the release drop.
Shipping asset references resolve and the complete release dependency set is
included. The historical research catalog and mocked test paths are outside
runtime dependency validation. Game/test LF/CRLF line endings are retained.

Unrelated local game projects, private configuration, raw sound-library imports
and temporary capture output remain local. No user files are removed.
