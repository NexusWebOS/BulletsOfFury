# Pilot name flair — 0914

Names now use a shared cached bitmap treatment in dialogue, cinematic dialogue, pilot comms and the unlocked pilot-selection heading. Each name has a white highlight, its pilot color, a one-pixel colored rim, a dark keyline and a slow three-second glow pulse. Locked selection text keeps its existing neutral appearance. Spoken text retains its white font.

The old luminance-preserving font tint left pure-white glyphs white. The new name-only renderer builds masks from the current Command Signal glyph sheet and colors those masks directly. Portraits and other authored art are untouched. The cache is capped at 64 entries; glow is applied to the whole name rather than every glyph. Canvas alpha, shadow and smoothing state are restored after drawing.

Native verification extends the existing readable-type probe through `_BUILD_SOURCE/readable_type_0914/probe_name_flair.py`: eleven checks pass, including exact pilot-color pixels and drawing-state restoration, with no page, console or game errors. Visually inspected all nine names, real Yuri PLAY dialogue and pilot selection. A four-second silent capture is `_shots/pilot_name_flair_0914/Pilot_Name_Glow_0914.mp4`; the contact sheet is `all_pilot_names.png` in that folder.

Syntax and full-suite results are recorded in `qa/pilot_name_flair_0914.json`. One source-level assertion was updated from the former msgText call to the shared bitmap nameplate route; no gameplay expectation was removed. Existing working changes are preserved. No commit or push.
