# Passover for ChatGPT's image generator: more animation frames (Bullets of Fury)

**From:** Claude (Bullets of Fury engine), October 9, 2026
**For:** ChatGPT with image generation
**Owner of every creative decision:** Mike (ColeForge)

## 1. Why this exists

Mike wants Bullets of Fury to feel like **Shadow Gangs Zero** on the Neo Geo: smooth and alive.

The engine half is done. The game now runs exactly one logic tick per displayed frame
(`docs/FRAME_PACING_1009.md`).

The other half is **art**. Neo Geo-tier sprites carry many more frames than ours. Measured from the game's
manifest:

| group | frames today | target |
|---|---|---|
| Stage 1 enemies (tanks, jets, boats) | **1 still plate per damage state, no motion at all** | an 8-frame idle loop + a 4-frame fire reel |
| Stage 2 enemy reels (`nvl_*`) | 6 | 12 |
| Shared explosions (`nxp_dense`, `nxp_clus`) | 8 | 16 |

Every reference file you need is in `reference/` beside this README.

## 2. Ground rules

The engine depends on these. Break one and the art cannot be used.

1. **Same sprite, more frames.**
   - Match the reference exactly: silhouette, palette, line weight, panel detail, camo pattern, outline.
   - Do not redesign, restyle, "improve" or re-light the unit.
   - Every new frame must overlay the reference plate almost perfectly where nothing is supposed to move.
2. **Top-down, nose pointing straight UP.**
   - Every frame keeps the unit's centreline vertical, at the same position, at the same size.
   - **Never rotate the whole sprite** to fake motion. The game rotates sprites itself; a baked rotation fights it.
   - Banking and rolling are not part of this job.
3. **Motion comes from the moving parts, not the whole body.** Each frame changes only these:
   - treads cycling
   - rotor blades
   - wake or foam
   - engine glow and exhaust flicker
   - antenna sway
   - turret recoil
   - muzzle flash
   - hatch or radar spin
   - a small 1-pixel suspension bob
4. **Background.**
   - Fully transparent PNG, OR a flat pure magenta `#FF00FF` background.
   - No checkerboard, no shadows on the ground, no text, no grid lines, no frame numbers.
5. **No purple or pink halo around the sprite.** Its edge must be a clean dark outline. (The game converts
   halos to black edges, and stray magenta fringe is the most common rejection.)
6. **One horizontal strip per reel.**
   - Frames sit left to right, in playback order, on equal-width cells.
   - Leave generous empty space between frames, so frames can be cut apart without touching.
7. **Keep each reel to 8 frames or fewer per image.**
   - For a 12- or 16-frame reel, deliver it as two images, frames 1–8 then 9–16. Image generators are unreliable
     at long counts and silently drop or merge frames.
   - State the frame count in your reply, and count the frames yourself before sending.
8. **Pixel-art finish, matching the reference density.** Crisp edges, no blur, no painterly smoothing, no
   anti-aliased glow spilling outside the outline.
9. **Loops must loop.** The last frame of an idle loop should lead naturally back into frame 1, with no pop.

## 3. The work, in priority order

Sizes are the reference cell sizes. Produce at that size, or at an exact 2× or 4× of it.

### Batch A: Stage 1 enemies (highest priority, currently motionless)

Each reference strip `reference/s1_<unit>_states.png` shows three plates: **intact | damaged | critical**.

Animate the **intact** plate first. If time allows, repeat the idle loop for **damaged** and **critical**, keeping
their existing smoke, scorch and fire marks; the fire may flicker.

| unit (reference file) | cell | IDLE loop, 8 frames | FIRE reel, 4 frames |
|---|---|---|---|
| `s1_jungle_tank_states.png` | 167×228 | treads cycle (tread links advance 1–2 px per frame), 1 px hull bob, engine-deck heat shimmer | barrel recoils 3–4 px back then returns; muzzle flash on frames 1–2 only |
| `s1_jungle_mini_tank_states.png` | 167×228 | same as the tank, smaller, faster tread cycle | same as the tank |
| `s1_jungle_apc_states.png` | 145×228 | treads or wheels cycle, roof hatch light blinks on frames 1–4 | roof gun recoil + flash |
| `s1_rocket_buggy_states.png` | 153×228 | wheels spin, chassis bounces 1 px on alternate frames | rocket rack: one tube flashes and its rocket leaves |
| `s1_river_patrol_boat_states.png` | 145×228 | **bow wake and side foam animate** (the main motion); a small wave bob | deck gun recoil + flash |
| `s1_missile_gunboat_states.png` | 145×228 | wake and foam as the patrol boat | launcher hatch opens, missile exhaust flare |
| `s1_river_corvette_states.png` | 145×228 | wake and foam, radar dish rotates through 8 positions | twin deck guns alternate flashes |
| `s1_landing_craft_states.png` | 145×228 | wake and foam, ramp vibrates 1 px | none needed |
| `s1_camo_attack_jet_states.png` | 205×228 | engine exhaust flame flickers (length and brightness vary), wingtip light blink | twin cannon flashes at the gun ports |
| `s1_jungle_bomber_states.png` | 228×200 | engine exhaust flicker on every engine (no propellers - the game has none on enemies) | bomb bay doors open over frames 1–2 and close over 3–4 |

**Skip** the crates, barrels, fuel tank and river mine. They are props and stay still.

### Batch B: shared explosions (seen constantly)

| reference | cell | today | deliver |
|---|---|---|---|
| `nxp_dense_strip.png` | 256×256 | 8 frames | **16 frames**: an in-between drawn between each existing pair, so the fireball grows, peaks and breaks into smoke more gradually. Keep the first and last frames identical to the existing first and last. |
| `nxp_clus_strip.png` | 256×256 | 8 frames | **16 frames**, same method |

Explosions must stay **centred in the cell**, and must not touch the cell edge on any frame.

### Batch C: Stage 2 volcanic enemies

| reference | cell | today | deliver |
|---|---|---|---|
| `nvl_skim_strip.png` | 245×222 | 6 | 12 (an in-between for each pair, loop closes back to frame 1) |
| `nvl_lance_strip.png` | 200×235 | 6 | 12 |
| `nvl_eye_strip.png` | 232×220 | 6 | 12 |
| `nvl_golem_strip.png` | 274×249 | 6 | 12 |

These reels already animate. You are only adding the frames between them, so every new frame is a true halfway
pose between its two neighbours. Copy no existing frame twice.

## 4. Prompt template (adapt per row)

> Using the attached sprite as the exact reference, create a horizontal sprite strip of **8 frames** of the SAME
> unit for a 16-bit top-down vertical shoot-em-up. The unit faces straight up in every frame, centred, the same
> size and position in every frame, identical design, palette, outline and detail to the reference.
>
> Animate only: **[moving parts from the table]**. Frame 8 must loop seamlessly back to frame 1.
>
> Crisp pixel art, dark clean outline, no glow outside the outline, no ground shadow. Flat pure magenta #FF00FF
> background (or transparent). Frames evenly spaced left to right with empty space between them. No text, no
> numbers, no grid.

For in-betweens, attach two frames:

> Draw the single frame exactly halfway between these two frames of the same sprite.

## 5. Delivery

- File names: `<reference-name>__<reel>__<firstframe>-<lastframe>.png`
  - `s1_jungle_tank__idle_intact__01-08.png`
  - `s1_jungle_tank__fire_intact__01-04.png`
  - `nxp_dense__16__01-08.png` and `nxp_dense__16__09-16.png`
- Put them in a folder named `returned/` next to this README. A zip works too.
- With the files, list for each one:
  - the frame count you actually drew
  - the background used (transparent or magenta)
  - anything you were unsure about

## 6. Self-check before sending

- [ ] The frame count in the image equals the frame count in the file name, counted by eye.
- [ ] Overlay frame 1 on the reference: the body lines up and only the listed parts differ.
- [ ] The nose points straight up in every frame; nothing is rotated.
- [ ] No checkerboard, no magenta or purple fringe on the outline, no text.
- [ ] The loop plays back without a jump from the last frame to the first.
- [ ] Explosions never touch the cell edge.

## 7. What happens next (Claude's side)

Claude will:

1. Cut the strips.
2. Key the magenta and convert any fringe to a black edge.
3. Register each frame against the reference plate by silhouette overlap, so frames that drift are re-seated, not
   stretched.
4. Wire the reels into the game's tick clock.
5. Verify them in real Chromium.

Anything that fails rule 1 or 2 will come back to you with the exact frames named.
