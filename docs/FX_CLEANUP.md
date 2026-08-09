# FX CLEANUP — drop 0801d

    721 files quarantined · 39 relocated · manifest 7800 -> 7054 keys
    assets/fx: 47 MB (was ~100 MB)
    Everything reversible: python3 cleanup_fx_0801d.py --restore

## Your list

| ask | done |
|---|---|
| clear the leftover n6e sprites at the fx root | 129 files, 0 code references |
| one `lasers` folder: green, Falva's, laser beams | 37 files merged from greenlaser + falvalaser + laserbeam |
| delete old helix beams | 54 files — superseded by the nhxm_/nhxv_ modular pack |
| delete old chain lightning | 12 files — superseded by the nchp_ premium 12-frame bolt |
| delete the maverick folder | 4 files |
| race can go | 32 files |
| delete rot/, keep 1-2 green frames | 515 of 517 quarantined; eglR_00 and eglR_18 kept |

## The rot folder was the real win

517 keys of PRE-BAKED rotation — eglR, omsl, mroll, mtilt, dr0R/1R/2R, homR — 72 frames each, a
full 360 at 5 degree steps. You called it exactly: *"I dont think you need 100's of frames when we
can do this in game."*

Every one of those sets was the same sprite at a different angle, which is what `ctx.rotate` does
for free. The old comments argued *"no runtime rotation warp, no procedural shapes"* as if the
transform were lossy — it is not. Rotating a square sprite about its centre is exact at
0/90/180/270 and interpolated elsewhere, using the same interpolation that generated the baked
frames in the first place. Keeping them only moved the cost from the GPU to the disk.

Five callers converted to runtime transforms before anything was removed:

    eglR      green enemy laser    72 frames -> 1 + rotate
    mroll     player ship roll     72 frames -> the normal ship draw, which already rotates
    mtilt     player ship tilt     13 frames -> same
    omsl      enemy torpedo        72 frames -> the fallback below it ALREADY rotated the real art
    nchgM     Maverick charge ring  4 frames -> removed. The flat-plate guard was already
                                                measuring it as an 84% single-colour plate and
                                                SKIPPING the draw, so nothing was ever appearing.

## The green flyer

eglR_00 and eglR_18 are now in `assets/enemies/greenflyer`. Everything else is runtime:

    WING FLAP   the two frames alternate at 9Hz. Two frames IS a flap — that is how every 8-bit
                bird ever drawn worked, and more would not read as more.
    SPIN        a full 360 about the centre, which is exactly what the 72 deleted frames baked.
    TWIST       a 180 through a horizontal scale, so it turns edge-on and back. Different enough
                from the spin that a mixed formation does not read as one effect.

Each flyer picks spin OR twist at spawn and keeps it. LEVEL 1 ONLY.

## Honest note

The cull moved the harness from 42 to 44 failures. Two are assertions I updated to test the
post-cull truth. The other two are pre-existing and unrelated (`trt_t1/t3/t5` microturret art is
missing, and has been since before this drop — worth its own look).
