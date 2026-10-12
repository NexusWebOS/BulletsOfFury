# Actual ship identity in cinematics

Mike's October 10 direction: use the actual ships as references for every
cinematic generated from now on. An old cinematic drawing or a filename alone
is not an identity reference.

Latest correction: Mike rejected the generated Cole return-flight likeness
and explicitly allowed static ship images. The homecoming now uses each
pilot's original `ship_<pilot>_so6` front and `ship_<pilot>_so2` rear images
directly, with animated translation/scale. See
[the current static-aircraft drop](STATIC_PILOT_SHIPS_1010.md).

Before generating a ship-bearing cinematic, export the active pilot, Furyship
or enemy aircraft from the current game's `XART.get` and its own `drawImage`
route. Inspect those pixels. Supply the export to built-in image generation
as an identity reference, label its exact role and preserve its silhouette,
cockpit, wings, engine layout, palette and ordnance colors. For scenes that
actually feature the Furyship, use its current design. The October 10
homecoming direction explicitly uses the selected pilot's own jet from the
return portal through Earth descent and HQ landing, including its space
shots. Never
substitute a generic jet or invent a matching-colored aircraft.

Prefer separate environment plates and the exact existing ship sprites when
the scene requires live movement or input. Match one proportional scale;
keep physical mounts registered. Generated perspective views must still be
checked against the identity references before acceptance. Every new frame
obeys [the even frame resolution rules](FRAME_RESOLUTION_RULES.md).

The current native reference pack is
[`_ART_SOURCES/hq_live_1010/references`](../_ART_SOURCES/hq_live_1010/references).
Its manifest records nine pilot ships, three authored stealth palettes and
the native radar bezel, all exported through real Chromium. The nine-ship
sheet uses row-major Cole, Axel, Freezer, Yuri, Maverick, Falva, Lizzie,
Decker and Juggernaut. Existing odd-sized source sprites are unchanged;
transparent padding makes the supporting 864 × 864 sheet even.

`_BUILD_SOURCE/export_hq_live_refs_1010.py` owns this export. Re-export current
art before a future generation if the ship designs have changed. The HQ live
generation includes this exact reference sheet in both prompts and renders
the actual in-game ships at runtime; no generated replacement ships ship
with the live HQ scene.

The homecoming references in
[`_ART_SOURCES/homecoming_1010/references`](../_ART_SOURCES/homecoming_1010/references)
are nine individual active `ship_<pilot>` exports plus the actual Dracodia
return-gate frames. `_BUILD_SOURCE/export_homecoming_refs_1010.py` exports
those native pixels. The separate generated front/rear/landing reels are now
archived candidates, not approved aircraft likenesses. Native composites of
those generated reels are also archived references. Use the original pilot
sheet images for the current ending, never those generated composites as a
new identity authority.
