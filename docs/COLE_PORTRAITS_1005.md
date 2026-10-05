# Cole's fixed portrait frame and talking anchor

Mike reported jumpy dialogue portraits with clipped frame sides. The supplied
neutral portrait and generated talking cells used different head positions and
different bezel crops. Playing those entire plates as mouth poses moved both
the head and its enclosure.

`assets/cole_portraits_1005.js` keeps Cole's complete authored neutral bezel for
every expression. Ordinary speech retains the neutral head and shoulders and
replaces only the aligned authored lip patch. Stage 6's shouting animation uses
one shouting head/body anchor and its three mouth poses. Comm portraits mirror
the composed plate toward the text; menus retain their original facing. Both use
the same 256-pixel source size, with an unchanged destination bay. Other emotions
retain their authored faces inside the fixed bezel. Completed ordinary dialogue
returns to neutral through the existing typing/idle logic.

This is an authored-art composition fix at the XART boundary, following the
existing Lizzie fixed-bezel approach. Original PNGs, sheets and manifests remain
preserved. No atlas repack or new generated artwork was needed. The script loads
after the existing runtime overlays and is included in the full-suite VM.

`_BUILD_SOURCE/probe_cole_portraits_1005.py` runs the actual game in Chromium via
`shoot.py`. It compares all pixels outside the mouth regions for normal and rage
talk reels, checks every expression's frame rails, verifies mirrored comm pixels,
captures actual dialogue animation and renders the Stage 6 shouting caller.
Native poses and in-game dialogue screenshots were inspected. Review and animation:
`_shots/cole_portraits_1005/review.html`. Portable QA:
`docs/qa/cole_portraits_1005.json`.

Verification: 7,274 full-suite assertions passed, exit 0; 46 native Chromium
checks passed with zero browser errors.

Local follow-up; no commit or push requested.
