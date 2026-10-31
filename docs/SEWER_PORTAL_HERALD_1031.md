# Stage 7 stone portal route and Herald readable shatter

Mike's October 31 corrections are installed locally. This pass spends no generation credits: it reuses the existing PixelLab gated portals and HS53 authored spell seal.

## Herald of Death

The skull-bomb glass leaves the burst point once, keeps its outgoing velocity and expires beyond the screen. The former HH52 edge-reflection/clamping code is removed. HG70 depth-orb glass and HS53 spell glass also receive bounded offscreen cleanup. Ordinary glass remains dangerous and unshootable; the explicit skull-bomb and missile-return interactions remain with their original owners.

Before a tornado cast, the existing seal draws its five strokes and circle, spins, pulses, then bursts as the funnels arrive. The committed warmup is 5.4 seconds: initial caster pose for 0.6s; line/circle build to 3.35s; spin to 4.55s; pulse to 5.4s; burst through 6.05s. The existing metal warning, growing red lightning, tornado arrival/departure frames, internal lightning flashes, audio and finite recovery remain authoritative. No large FOV was added.

Runtime: `assets/herald_clear_shards_1031.js` (HR87), plus the narrowly scoped removal in `assets/herald_chaos_1029.js`. The seal banks stay in their existing HS53 source/builder; no duplicated generation or runtime rotation/glow.

## Stage 7 chamber and green gate

The original `nst7_master_v3.png` stone chamber replaces the prior connector cap. After the real Warden core defeat, the wreck sequence completes, then the camera and floor travel continuously north into the chamber. The pilot can steer while approaching. The green gate activates when a live pilot reaches the stone aperture; authored entry shrink, gate close and flash lead into the original campaign exit owner.

Stone aperture center: (343,310), approximately 198x200 source pixels. Green source frames are exported proportionally into fixed 384x384 cells so the visible metal rim fits the stone opening. The interior seal covers the otherwise visible floor. Source travel, wreck and gate all share one camera/source coordinate; there is no cinematic zoom or map teleport.

Native completion still owns the Forge reward, stage ledger, results bonus and direct Stage 8 WARPENTRY. Pausing freezes the route; activation/entry protect the pilot and guide all live seats. The dialogue uses the existing fixed bottom portrait frame.

## Correct blue gate

Dracodia's terminal exit and outdoor reunion now use the actual PixelLab `pixellab_void_1017` blue metal-rimmed form/loop/close frames. The earlier `portal_lifecycle_1011` energy-only swirl was the wrong source. This patch uses the blue bank directly, avoiding the Stage 8 portal router's color substitution.

Runtime: `assets/sewer_portal_chamber_1031.js` (SC86). Art manifest: `assets/sewer_portal_chamber_art_1031.js`. Seven banks, 177 fixed-cell frames; editable Aseprite sources are in `_ART_SOURCES/sewer_portal_chamber_1031`. Original PixelLab inputs, SHA256 provenance and export recipe are archived in `assets/game/levels/stage_07/effects/portal_chamber_1031`.

Rebuild from repository root:

    python _BUILD_SOURCE/build_sewer_portal_chamber_1031.py --aseprite PATH_TO_ASEPRITE

## Verification

21 native route checks, 14 native Herald checks and 19 source/provenance checks pass. Native renderer screenshots inspect partial seal strokes, the completed spinning seal, pulse/release, snug green gate, entry and direct Stage 8 handoff. Tests cover steering, pause, approach gate, all four shard exit directions, non-interception, unchanged HP and preserved reward/progression.

`node --check assets/game.js` passes. The complete `node _BUILD_SOURCE/test_fl.js` run still exits 1 with exactly the same five pre-existing assertion failures:

- and the flash is held long enough for a single hit to register
- dialogue ends with the opening jump warning
- opening jump lands and returns before chromium activation
- unchosen right route persists as the opposite Stage X fight
- Stage X right branch launches a full encounter

Core engine SHA256 remains `024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de`. No commit or push was performed.

Native footage, playback verification and measured audio/performance are recorded in the accompanying `SEWER_PORTAL_HERALD_1031_MEDIA.json`. Focused portal/attack clips explicitly use pre-recording checkpoints; the complete Herald film uses native full health and input-only GOD assistance.

## Recorded media results

All five revised gallery entries load, decode and advance at1280x800 with no page errors. The full Herald fight completes natively in88.5s, averaging57.06 game frames/s; final-hit portal clips are explicitly labelled checkpoints. The storm, skull shatter, chamber and blue return clips average57.65,56.60,53.14 and58.49 game frames/s respectively. The chamber average includes a brief native Stage8 handoff hitch; no source/camera reversal occurred. Recorded mixes have audio and negative measured peaks (no output clipping).

Local review: http://127.0.0.1:51046/?herald=straight-glass-seal-1031#clip=stage8-herald-inscribed-storm

The current `stage8-miniboss` entry points to the revised complete fight. Older full fights and the previous portal footage are preserved as archive entries. Focused proof/report files are under `_shots/portal_herald_1031`; original movies are retained in the working capture folder and published local gallery. These new changes and movies are local, not pushed to GitHub.
