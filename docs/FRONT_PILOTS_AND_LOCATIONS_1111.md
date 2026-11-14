# Headset-free Fury portraits and locations

Nine actual pilots now have new front-facing, headset-free cinematic portraits. Their flight colors, hair, skin tones and eyewear remain recognizable; Maverick stays teal. The direction combines the approved comic linework and 16-bit shapes with 1990s action-anime cel shadows and expressive faces.

Each pilot has seven generated mouth positions (closed, A, E, O, U, F, L), normalized against a stable 320-pixel master. Only the mouth region changes. One shared indexed palette per GIF prevents loop shimmer; ivory teeth and natural dark mouth colors exclude Maverick’s teal clothing palette.

The conference briefing uses the conference room; later demonstrations use Decker’s workshop. Homecoming uses the hangar and workshop, the final crew conversation returns to HQ, and the music-room exchange has its own lounge. Pilots in flight have sky, orbit or tunnel behind an authored cockpit. The tech contact remains at HQ. Locations are chosen per speaker and scene rather than assigning one generic background to each pilot.

The late FP5 owner selects the new portrait/background banks. CM3 retains its existing black starts, panel reveals, camera pans, scrolls, caption timing and controls. Non-strip dialogue retains the rectangular CX4 metal frames, with room-backed portrait cells. Native callbacks, mission rewards, maps and save ownership remain unchanged.

Sources include 63 native mouth cells, nine editable portrait Aseprite documents, generated high-resolution identity masters, seven room/environment backgrounds, 268 tagged derivative banks and 2,254 registered frame cells. Seven zoom poses and four small portrait sizes are exported directly from the native sources. Production frames are even, fixed and untrimmed.

Generation: built-in image generation supplied each pilot and room master using the actual native pilots and HQ architecture as references. PixelLab PixMiniMax supplied the mouth-position sets. Aseprite locks the body/eyes/hair, cleans oral colors, authors the GIF timelines and verifies exact editable-source round trips. Prompt direction and generation identifiers are preserved in source/art-brief.json and source/generation-provenance.json; raw generated mouth GIFs remain in masters.

This source update does not rebuild the installer or overwrite the earlier full-story movie. The new pilot preview and gallery show this revision.
