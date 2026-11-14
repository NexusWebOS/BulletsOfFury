# Maverick's teal identity and the full story movie

Mike corrected the requested color from neon green to teal. Teal is the final authority: Maverick's native ship/name tint is `#3ad6c8`. His clothing, headset acting and personal portrait frames now use matching teal shades. His aircraft, skin, hair, dark harness, silhouette, poses, transparency and timing retain their existing source owners.

## Palette production

The deterministic Aseprite palette edit replaces the olive/neon-green material ramp with a teal ramp. Explicit regions isolate Maverick in the Yuri/Maverick preflight sheet, nine-person conference, two-person comic and shared native atlases. No other pilot receives a palette change. Metal and outlines keep their neutral values; the original shading order remains. Source dimensions, atlas cells and alpha are unchanged, including existing older odd-sized native assets. No new runtime filter or recoloring effect is added.

The pass covers81 native/runtime image files and two whole-pose master sheets. This includes full-body/emotion/seated/movement poses, individual radio portraits and their boxes, both cockpit views, the invasion reporting poses, both headset sizes, the legacy19-pose actor bank, cable inspection, the comic portrait and its personal background, four compact personal frame sizes, the newer dialogue portrait, preflight and all four conference poses. Ship-only images are excluded. `source-art/maverick-teal/` preserves the originals, exact masks/jobs,83 editable palette canvases and exported PNGs. `source/palette_maverick_teal.lua` owns the material mapping. The final editor/production checks are in `verification/maverick-teal/`.

The two original cinema banks and seven HQ timelines are rebuilt through the existing timeline author. The affected atlas hashes are updated with the artwork. Existing bank dimensions, pivots, frame counts and durations remain. The historical generation prompts retain their original submitted wording; the teal revision is an explicit palette post-process recorded here.

## Movie edit

`Bullets-of-Fury-Full-Story.mp4` is a chaptered movie of the current cinematic story. It retains the native dialogue boxes, text reveals, authored comic transitions, instrument readings, actual pilot/ship identities and timed effects. The picture is captured and exported at the native912×512 logical canvas,24fps, without resampling individual sprites. It uses the game's existing music and sound recordings; no voice acting is synthesized.

The main cut follows Cole's campaign perspective with the whole crew: intro; evidence after Stages1–3; conference/prototype lab; Stage4 approach and satellite recording; the earned Stage5→9 jump, bonus arrival and return; Chronos's actual final words and missile sequence; recovered-cannon workshop; the Stage6 signal/pursuit; river approach; Warden breach; actual native Dracodia disintegration; homecoming ending, crew roll and final transmission. Combat intervals are omitted and native-font chapter cards mark the gap. The optional bonus/pursuit scenes are included as chosen events, not simultaneous alternatives. The other Stage6 outcome/pursuit and Easy/Normal standby are clearly labelled after the main ending.

`Watch Story Movie.html` provides playback and chapter jumps; the MP4 also contains chapter markers. `Story-Movie-Chapters.md` lists timestamps, and the recording ledger preserves every scene/shot's dialogue and duration. This is a story review cut from controlled native cinematic fixtures, not a claim that a complete combat campaign was played. Gameplay, rewards, saves and the published Windows installer are unchanged. No commit or push is made.
