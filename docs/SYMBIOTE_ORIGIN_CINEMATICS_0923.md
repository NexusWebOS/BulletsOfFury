# Symbiote origin and Fury HQ art — 2026-09-23

The campaign prologue now shows the black-hole arrival, the organism attaching to Earth's satellite, its corrupted relay signal, radio dispatch seeing aircraft turn hostile, a harbor tower seeing aircraft and watercraft turn, ground dispatch seeing tanks/trucks/cars turn, and the new isometric Fury HQ. The existing chosen-pilot return scene follows. Dialogue uses the game's bottom-centered frame and holds for 4.3–4.8 seconds per beat. The full skippable intro lasts 53.8 seconds.

The new reusable source art lives in `assets/game/cinematic_campaign/symbiote_origin_0923/`:

| File | Use |
| --- | --- |
| `black_symbiote.png` | Transparent master of the alien organism for later encounters and composites. |
| `orbital_arrival.png` | Black-hole arrival and satellite attachment. |
| `satellite_infection.png` | Hostile satellite broadcast toward Earth. |
| `radio_dispatch.png` | Air-control radio dispatch. |
| `tower_dispatch.png` | Coastal air and watercraft control tower. |
| `land_takeover.png` | Tanks, trucks, and cars under the signal. |
| `fury_hq_isometric.png` | Reusable Fury HQ establishing shot; replaces the older HQ cinematic keys. |
| `fighter_cockpit_front.png` | Transparent front-facing fighter cockpit frame, used in the pilot intro. |
| `space_cockpit_front.png` | Transparent front-facing space cockpit frame, registered for future space scenes. |
| `pilot_pov_magenta.png` | Pilot-eye interior with joystick and controls; magenta windshield is keyed at runtime so a live scene can show through. |

The art was generated with the built-in image-generation model, using the existing game's dense 16-bit pixel-art, metallic cockpit framing, and cinematic palette as references. Prompt directions: a black tendril symbiote on transparent ground; a black hole ejecting that organism toward an Earth defense satellite; a corrupted satellite broadcasting toward Earth; radio operators discovering hijacked fighters; a coastal control tower discovering hijacked jets and vessels; hostile land vehicles; a permanently reusable isometric jungle-coast Fury HQ; transparent frontal fighter and space cockpits; and a pilot-eye control panel with a solid magenta windshield for chroma keying. Each is a separate source file rather than a cropped section of a contact sheet.

Browser verification: `_BUILD_SOURCE/probe_symbiote_origin_0923.py` captures nine real Chromium beats into ignored `_shots/symbiote_origin_0923/`, including the keyed POV and chosen-pilot cockpit, and checks page/console errors. The first-person view was visually inspected after capture. The magenta source remains available for later pseudo-3D scene composition; this change does not add the future late-game pseudo-3D level itself.
