# Matched roster motion studies â€” October 25

Mike approved the matched modular art, then requested an animated preview.
art-packs/raiden-components-1024/animation.html is the live motion study for
all 24 machines, with a six-machine opening showcase, tier pages and individual
focus. Play/pause, idle/travel/firing/full-cycle modes, speed, lifted track belts
and visible hit feedback can be inspected independently.

The renderer uses the exact approved normal and hit PNGs. One complete hull
and its matching modules share the same parent transform. Airframes turn and
drift as rigid assembled aircraft; this is articulated 2D motion, not a new bank
of painted roll/somersault poses. Ground rolling surfaces scroll their own
existing tread/roller pixels inside measured local apertures; casings and
mounting arms stay fixed. Radar dishes rotate over their fixed supports.

Turret housings remain mounted while barrel pixels recoil behind them at a
measured joint. The per-part alpha silhouette supplies actual barrel endpoints,
including separate twin/triple barrels. Red missile nose pixels supply launch
origins and directions. North-facing racks retain their north-facing launch;
south-facing aircraft pods launch south. Moving rounds keep their launch-time
world pose instead of curving with the current turret angle.

Existing authored stage1_motion_1009 banks supply eight exhaust, eight muzzle
and eight water-wake frames, copied with their registered even canvases and
native pivots. Four original Raiden armory ordnance images are retained with
RGB-preserving solid-alpha cleanup. No procedural replacement sprites, new
painted hulls, palette changes or generation jobs. The preview is silent.

Owner: _BUILD_SOURCE/build_raiden_animation_1025.py exports animation-data.json,
animation-data.js and animation-fx/ with source hashes, fixed pivots, measured
barrel tips and rolling apertures. The approved main catalog is read-only.
animation.js owns the runtime clock and analytic shot timing. Eight-second
motion cycle, independent FX clocks, bounded RAF delta and deterministic
renderAt(t) for capture. The ordinary component builder remains available.

Chromium owner: _BUILD_SOURCE/probe_raiden_animation_1025.py. Checks actual
idle/travel/firing pixels, pause/resume, all 24 animated units, separate rolling
wheels under lifted belts, actual white hit pixels and palette recovery, tier
navigation, mobile layout and page/console errors. Captures use the actual
Chromium canvas, never a Python redraw of the renderer.

With --video, the probe pipes actual native canvas frames directly to ffmpeg:
28-second 1280x800 / 24fps MP4, covering the overview and every roster tier;
eight-second 768x480 / 12fps looping GIF from the opening showcase. No frame
directory or full repository copy. Independently decode the complete MP4 and
inspect decoded frames before delivery. Evidence: _shots/raiden_animation_1025/.

Build order: matched component builder, animation builder, native probe --video,
then the component builder's package() function. ZIP registration includes every
animation FX dependency. Existing shipping game files are untouched; this is
an art/animation preview, not live encounter or attack/audio integration.

Final native verification: 39 passed / 0 failed, no page or console errors.
Full MP4 decode passed; final GIF has 96 frames, infinite loop and eight-second
duration. Desktop, mobile and decoded video frames inspected. No shipping
gameplay changes, generation spend, commit or push.
