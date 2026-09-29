# Hama graphics pack — 2026-09-28

128 transparent authored frames, 15 reels. Correct current compact hammer-only robot: black steel, cyan visor/reactor, cylindrical blue energy hammer. No back-mounted chaingun. All images generated with the built-in image_gen tool; Python only slices, scales with nearest-neighbor, pads, packs atlases and makes review composites.

The original generation pass was an **art-only handoff**. It adds no password, music, lyrics/captions, AI, hitboxes or game-engine code. Existing Hammer mode remains unchanged. No song recording was supplied for this art request, so preview FPS and event frame numbers are animation cues, not verified music timestamps. Synchronize against the chosen recording in the gameplay pass.

## Reels

| Reel | Frames | Purpose |
|---|---:|---|
| boss_moonwalk_left / right | 8 each | Backward heel/toe glide in both directions, black steel body |
| armored_moonwalk_left / right | 8 each | Silver/chromium body variant for armor activation and shield rise |
| boss_lasso_360 | 12 | Raised-hand lasso gesture with hopping poses and authored front, side and back views |
| helper_lasso_360 | 12 | Matching full-turn helper breakdown |
| double_hammer_slam | 12 | Two distinct overhead-to-floor impacts |
| hammer_toss_helper_throw | 16 | Hammer toss, reach/grab/carry, helper throw, beckon and replacement summon |
| helper_airborne_tumble | 8 | Full helper turning in flight, including back and upside-down views |
| boss_speaker_sing / chant | 4 each | Modular helmet with animated cyan vocal grille |
| helper_speaker_sing / chant | 4 each | Modular helper head with vocal grille and eye expressions |
| hammer_airborne_spin | 8 | Detached cylindrical hammer, full end-over-end turn with drum-centered pivot |
| boss_vocal_leap | 12 | Crouch, airborne hammer windup, strike, landing and recovery; torso vocal grille |

## Attachment and frame cues

All event numbers below are **zero based**. Each reel.json and manifest.json supplies canvas size, anchor, atlas rectangle, individual PNG path, source crop and scale. Use the supplied fixed anchor and authored view changes. Do not independently fit each sprite or CSS-rotate a finished frame.

- Moonwalk: translate the boss opposite its facing direction. The first pair faces right while sliding left; the second faces left while sliding right. Match root movement to heel/toe contact, rather than treating this as a walking cycle.
- Lasso: one 12-frame cycle passes through front, right, back and left views. Small hop displacements are retained in the normalized offsets. Beat cadence can change independently of the body turn.
- Double slam: trigger separate impacts at frames **2** and **7**. Set those cue times to the two-word musical hit. Hold the overhead poses if needed; use existing ground explosion/shockwave graphics, sounds and shake as separate layers.
- Toss: detach the airborne hammer at **3**, attach/hide the independent helper at **6**, release the helper at **10**, beckon at **13**, summon at **14**. Frames 0–5 already include the nearby helper; frames 6–9 include the carried helper. Do not draw a duplicate helper over those composites. A replacement may enter independently at frame 14. The separate hammer and helper reels follow their own flight trajectories.
- Singing heads replace the visible front-facing helmet, with neck anchor at bottom center. Mount and scale them to the body's helmet rather than drawing a second floating head. Use only on compatible front views; preserve the authored side/back helmet during the full turn. Captions stay above the actor in the game's graphical font, separate from sprites.
- Vocal leap: takeoff **3**, apex **5**, ground impact **8**, recovered **11**. Preserve the supplied airborne offsets. The body has a torso grille; the modular helmet can provide additional mouth movement on front-facing frames.
- Armor/shield: use the armored moonwalk after the existing hammer-only chromium transformation. Keep the existing shield/wall on its own layer so it can rise around the moving boss. The two moonwalk variants are authored versions and need a short transition or cut on the beat, not a per-pixel morph.

## Review and validation

Serve this folder locally and open preview.html. Filters separate boss, helpers, heads and hammer; pause/speed controls and per-reel sliders allow frame review. Double-click a reel or press Play to resume it. GIFs and contact sheets are in review/.

All 128 source cuts and padded frame edges were checked for clipping. All 15 canvases render and animate, filter/scrub controls pass, and the isolated browser viewer has no page errors. This does not certify gameplay integration or song synchronization.

Original selected sources and prompts are in _ART_SOURCES/hama_art_0928. Rebuild tools are in _BUILD_SOURCE/hama_art_0928. The original handoff left files unregistered. They are now registered through the dedicated HAMA runtime registry; the large generated engine manifest remains unchanged.


## Runtime integration — 2026-09-29

The HAMA password now uses this pack via `assets/hama_frames_art_0929.js` and
`assets/hama_frames_0929.js`. The previously supplied instrumental and measured
cue sheet are wired by the incoming engine changes. The deterministic real-game
probe verified all 128 frames, both contacts within one frame of their cues, and
the authored flight views. See `docs/HAMA_FRAMES_0929.md` for the current behavior
and tests. The original art-only notes above describe generation provenance.


## Moonwalk appearance correction — 2026-09-29

The introductory dance shield must not switch the boss to the silver armor
moonwalk. Both directions now retain the regular black-steel/cyan appearance.
The 16 silver frames remain in this original art pack as unused variants; they
are omitted by the runtime registry and are not preloaded. The current live
pack is 13 reels / 112 frames. This supersedes the armored-moonwalk integration
suggestion in the original generation notes above.
