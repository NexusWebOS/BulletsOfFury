# Trailer v10 - the Gasline cut (Stage 6 rebel-fight / Stage X track)

Mike, 2026-10-08: a bot that actually plays, footage across Easy/Normal, Hard and Furious where the game changes,
the 9 pilots, 10 stages, 1 hell of a campaign, minibosses, bosses, specials, the Rebel fight and its cutscene, the
alternate path choice, the Harrier, the final boss transforming into its forms in the void, missile volley galore -
fast, action paced, cut to the rebel boss fight music (`assets/game/music/LevelX.mp3`, Gasline, 88.4 s).

Output (gitignored): `_shots/trailer_v10/BulletsOfFury_Trailer_v10.mp4` - 92.4 s, 1920x1080, 60 fps, AAC 320k,
final -13.1 LUFS / -1.0 dBFS peak. 103 clips, 0 footage claimed twice, 0 back-to-back same pilot.

## Pipeline (same tools as v9, retargeted)

    python brand9.py                                            # brand/ from the game's own atlases
    python beatmap9.py ../../assets/game/music/LevelX.mp3 --out beatmap10.json   # 163.1 BPM, 1.471 s bars
    python capture10.py --all --missing --workers 3 --quality 0.82   # takes10/ (~7 GB, plan in plan10.py)
    python whiteness9.py --all                                  # per-frame white hit-flash share
    python render_audio.py --all                                # each take's sfx.wav through the game's Snd code
    python edit10.py                                            # edl10.json + shot report (cut lives in cut10.py)
    python compose.py edl10.json video.mp4 --workers 3
    python mix9.py edl10.json mix10.wav && python mix9.py mux video.mp4 mix10.wav BulletsOfFury_Trailer_v10.mp4

## The bot

Every take is real play (real9.py): the game's own `playerHit` is live - shields pop, ships spin out and respawn
("SHIP DESTROYED" is in the footage), only GAME OVER is held off. The autopilot predicts every enemy round, hull,
beam and hazard 2-26 frames ahead and steers/rolls to dodge while firing; boss takes use burst fire so bosses are not
held in their white hit flash. Encounters are reached the way a player reaches them: stage starts, the debug fight
list, or their own passwords (FINAL1/2/3, MINI8, XREBEL). Stage 6 is flown end to end on both routes; the route
choice is made with real key taps on CHOOSE YOUR PURSUIT. The finale's eight copied forms are entered through the
game's own `j3Morph` transformation, and Dracodia's death through its real last-pool `modularHit`.

## Findings

* The campaign map's deploy keys changed since v9: the v9 X_rival tap script now lands in SAVE GAME. Stage X is
  filmed through XREBEL instead; the map shot still comes from the walk.
* The Stage 6 ECLIPSE SIEGE BOMBER miniboss did not enter within 960 frames of a debug fight (two attempts) - only
  stealth fighters and lightning. Worth a look; it is swapped out of the montage.
* The Sovereign's Furious giant lightning did not fire inside 25 s of the Furious fight, so it is not in the cut.
* Pilot screen time is uneven (yuri 4.0 s, freezer 3.9 s ... lizzie 9.9 s); reported, not forced.
