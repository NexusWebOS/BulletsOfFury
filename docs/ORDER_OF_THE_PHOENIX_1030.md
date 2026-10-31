# Order of the Phoenix — October 30

PH83 replaces only the cannon-destroyed corner-rush stage of Dracodia's Phoenix copy. After four randomized corner rushes, he continues along the last exit vector, banks around the outside of the arena and approaches from a randomly selected north or south edge at background depth. A true authored front/quarter/profile/rear turn and roll ends facing the player. His wings accelerate through a fire-wind charge, then he casts **Order of the Phoenix**:8–12 animated digital-fire outlines of his exact body grow toward the foreground. He winds down, turns away, actually exits the screen, twists back into the foreground and exposes a4.2s recovery.

## Flight and combat

Each cycle shuffles all four corners with a private per-encounter random seed; the first corner cannot repeat the previous cycle's last corner. All routes are continuous world paths. Each diagonal is committed before its metal warning/coloured corridor; no target follows the player's input after commitment. Rush direction, source silhouette, part alpha and claw contact share one authored pose. Background/in-transit/casting/returning poses cannot take ordinary damage. Existing native parts, current-life HP, pod gate, damage flash, score, later copies, return download and final destruction remain owners. Destroyed claws lose their corresponding contact attack. The cannon station retains PH82's straight turbo gun streams and single chest-core beam.

| Sequence | Timing / behaviour | Readable counter |
|---|---|---|
| Four corner rushes | Tell1.50/1.30/1.10/0.95s and travel0.98/0.90/0.82/0.74s Easy/Normal/Hard/Furious; each rush continues0.22s past its exit | Read the committed diagonal and move between paths; foreground portions alone are hittable |
| Background charge |4.2s; wing clock accelerates8→48frames/s, six authored fire-material/outer-light levels; fire-wind grows160→250px; scenery darkens | Metal warning and bitmap attack title identify the cast; move to a flank |
| Phoenix copies |8–12 per cycle, intervals0.74/0.64/0.56/0.50s;2.2/2.05/1.90/1.80s depth flight; maximum four alive together | Ground Retinas arrive green/yellow/red at committed landing x; read the growing body silhouette; both edge routes survive without GOD |
| Release and return |1.15s charge-down,0.6s turn-away,0.8s exit,1.7s depth-growing return,4.2s vulnerable recovery | Reposition, then punish the foreground recovery |

Copies contain the approved Phoenix silhouette, moving authored fire texture and digital code, an ivory/gold outline and orange outer light. They use sixteen authored depth sizes and eight wing/fire phases plus a four-step stored-alpha birth. Actual solid body spans own collision; decorative outer glow does not. Copies are local attack objects, cannot be targeted/intercepted and disappear only after their complete body travels offscreen. They commit their destination once, stop following lateral player movement and become harmful only at foreground depth. Pause freezes all clocks; exit/death/retry cancels copies, warning ownership, sound and scenery dim. Cast position is the world centre, with a250px fire-wind and10px hover that remain inside both camera extremes. It is energy around a casting body, with no shield mechanic.

The combo now finishes before the native46s donor-return deadline is acted on. This can extend that single copy visit beyond46s; it does not refill HP or force an unfinished cast to disappear. Normal copied-life defeat still interrupts/cancels immediately. The prior PH82 last-copy final-anatomy repair is preserved.

## Authored art and sources

702 fixed authored frames across38 banks and30 normal texture pages, plus white-hit pages: original whole-body wing loop, four directional depth rush banks and shadows, eighteen-step recede, sixteen flight headings, two24-frame depth turns, two32-frame return rolls, six charge intensities,160 fire-copy frames,128 fire-wind frames and twelve corridor warnings. Common512px logical canvases and256px pivots; even unrotated tight crops reconstruct their original frame. No new runtime rotation/scaling/tint, glow construction, animated alpha or generated decoration. All rotation, perspective sizes, palettes, fire fill, light and source alpha were baked offline.

The eight-volume reference uses GPT image generation against the approved current Phoenix; the original front remains canonical. Raw generation, exact prompt, connected-component extraction, seven complete generated non-front views, normalized turn strip, hashes, builder, manifest and seven named editable Aseprite documents are in `_ART_SOURCES/order_phoenix_1030/`. SpriteCook's four available credits were checked; no upload/job or paid credits were used. Existing PixelLab-authored fire and wind sources supply the moving fill/spirals.

Native visual inspection exposed a row-flush fault inherited from the PH82 atlas packer: a new row could skip flushing, leaving some cropped plates. The packer now flushes previous rows even when the new row height is zero. PH82's467 plates were rebuilt into61 complete pages, with unchanged runtime cannon logic; all normal/white banks and seven editable source documents were refreshed. The new packer also zeroes transparent RGB and checks source rectangle bounds. Every complete source body is now retained through the new wing/copy frames.

## Verification and review

46 focused checks pass, including four unique corner origins/no boundary repeat across2000 shuffle bags, continuous frame-to-frame paths, both north/south returns,8/12-echo ordinary-movement escape paths on Normal/Hard/Furious without GOD, exact source-pixel danger, harmless distant copies, committed landing points, native post-pod2624HP without healing, white-hit feedback/expiry, pause/cancellation, actual foreground/background target gating, both camera extremes, native live-copy return, last-copy zero-HP anatomy/final destruction, preserved brain/helicopter owners, all702 new/all467 predecessor atlas bounds and unchanged core bytes. The full required suite completes with the same five baseline failures, no new failures, exit1.

Fresh native Furious4100HP checkpoint footage: other life pools were cleared before capture, with an invulnerable input-only observer using normal weapons/Retina. The first complete new cast is observed before attacking again. No recorder HP/phase/timer writes during capture. This is a checkpoint review, not a whole-game or non-GOD full-fight victory claim. Duration199.84s; native defeat192.41s. Overall57.55FPS, combat58.11FPS, active new attack59.41FPS. First volley12 copies;43 launches in the film. Decoded audio mean-21.9dB, peak-4.6dB. No page, console, missing-asset or audio-tap errors. Prior film remains archived.

[Order of the Phoenix](http://127.0.0.1:51046/?phoenix=order-1030#clip=stage8-order-of-the-phoenix)

[Four shuffled corner rushes and return](http://127.0.0.1:51046/?phoenix=order-1030#clip=stage8-phoenix-corner-return)

[Full updated Phoenix fight](http://127.0.0.1:51046/?phoenix=order-1030#clip=s8-phoenix-volcano)

Core engine unchanged: `024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de`. No commit/push requested. Rebuild `_BUILD_SOURCE/build_order_phoenix_1030.py`, validate `probe_order_phoenix_1030.py`/`verify_order_phoenix_1030.py`, record `record_order_phoenix_1030.py`.
