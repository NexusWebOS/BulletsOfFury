# Trailer v9 - the City in the Sky cut

Mike, 2026-09-30:

> make a revised trailer thats inspired by this, but uses our city in the sky track. now its 10 levels, 9 pilots,
> 20 bosses and 1 hell of a campaign. now you may showcase the entire game, the normal, hard and furious variants,
> the level 6 awesome intro sequence, stage 7's awesome boss fight, stage 6 with the allies, the chocie to go left ot
> right, the harrier fight there, the fury/dog fight at the center of the map, plenty of the level 1 and 2 boss,
> plenty of level 5 boss, and then as the song is ending we can fade it out, and fade into Last but not least. Stop?
> Hammertime? And then cut to the hama password fight where its at the part where they all do the break down, and
> he does the Stop! Hammertime! and then cut to our game logo, 11.1.26. Steam/PC/Mac/Linux. 2026 ColeForge Productions.

"Inspired by this" is read as the v7/v8 trailer (`_BUILD_SOURCE/trailer_v7/`): the same shape - brand plate, logo
slam, claims, pilots, bosses, the arsenal, the climax, the end card - and the same pipeline, rebuilt so it runs on a
Linux container from the repo alone (v7's scratch folder, fonts and brand art lived on Mike's desktop and are gone).

## Pipeline

    python brand9.py                                   # brand/: ColeForge plate, wordmark, the nine pilot bodies + portraits, (c) line
    python beatmap9.py ../../assets/game/music/stage6_city_in_the_sky.mp3    # beatmap9.json: 158.4 BPM, 74 bars
    python capture9.py --all --missing --workers 3     # takes9/: live 60 fps frames + the game's own sound log
    python fix_sfx_arrays.py                           # files for the five variation-array cues (see below)
    python render_audio.py --all                       # takes9/<id>/sfx.wav, rendered through the game's own Snd code
    python edit9.py                                    # edl9.json + the shot report (claims, pilot time, back-to-back)
    python compose.py edl9.json trailer_v9_video.mp4 --workers 4
    python mix9.py edl9.json mix9.wav
    python mix9.py mux trailer_v9_video.mp4 mix9.wav BulletsOfFury_Trailer_v9.mp4

`survey9.py` flies a stage headless and logs when things happen without saving frames - every long take's windows were
found with it first. `inspect9.py` evaluates one expression in a booted game. `frames9.py` renders chosen EDL frames as
a contact sheet with compose.py's own renderer.

## What capture9.py adds to capture3.py

* **diff** - `debugStartFight` and `startRun` both assign `DIFF` from `diffKey`, so setting it first films the real
  Normal / Hard / Furious encounter.
* **when** - conditional events (`{COND: JS}`), fired once on the first chunk boundary COND holds: the stage-6 route
  choice, the miniboss kill, the carrier's death branch, the Stage X intro-done flag.
* **windows** - one long run saved as several takes, each with its own `rec0`, so render_audio.py aligns each window's
  sound on its own. Stage 6 is a 76 s opening + 75 s of stage + a miniboss + a route + a boss; saving all of it was ~5 GB.
* **the HAMA clock** - `Snd.music.hama.currentTime` is pinned to a value the harness advances 1/60 s per frame (as
  `probe_hama_0928.py` does), so every STOP / HAMMER / TIME lands on a known frame; metrics carry it as `hc` and mix9.py
  lays the real instrumental under the take at exactly the song time it shows.
* **burst fire** on boss takes - a gun on a boss every frame re-arms its 0.16 s hit flash every frame, and a laser or an
  orb stream kept whole bosses white for entire takes (Olive Warden, Rime Wall, the Furnace's core shield). `bf` in the
  metrics marks flash frames and the edit's scoring avoids them.
* achievement toasts stubbed.

## Things found on the way

* **A game bug, fixed (assets/game.js `drawLaunch`)**: a STAGE X rival duel runs on stage 6's neutral setup with
  `s6Opening` deliberately null, and `drawLaunch` re-initialised it - the whole stage-6 opening (cloaked lock-on, its
  26 s input lock, the radio) replayed over the duel. Two radios typing at once also re-ticked every letter each frame:
  16,987 letter blips in one 40 s take, 504 after the fix.
* **capture3's sound dump dropped variation arrays**: `missile`, `enemyMissile`, `nuclearLaunch`, `spaceVolleyLaunch`
  and `volleyLaunch` are arrays at runtime, so every one was logged as played and rendered silent. Fixed in the dump;
  `fix_sfx_arrays.py` repairs takes recorded before the fix.
* **v7's Furnace script no longer fits the fight** (it has been rebalanced): measured on the default gun, assembly to
  ~780, ARMS to 1740, CORE to 2880, HEAD to its kill at 3620. A levelled gun kills the head before a 2900 window opens.
* **the no-one-shot rule floors a forced kill at 1 hp** - capture3's KILL (which also stops the gun) left the stage-7
  Warden at 1 hp for 20 s. The Warden is dropped to 2 hp and finished by the player's own rounds instead.
* the Stage X duel opens on the squad's 29 s radio intro; its window opens on `frIntro.done`.

## Mike's standing trailer rules (HANDOFF_CODEX.md), and how v9 keeps them

live footage only; the game's own sounds under every shot; no footage shown twice (every pane claims its frames and
edit9.py reports conflicts); no pilot on screen twice in a row (reported); pilots' screen time reported; no boss name
cards; full-size view, zooms only on intense moments. His 0930 request overrides "no stage-6 bosses except the Tempest
duel" - he asked for the Harrier fight and the stage-6 allies by name.

## The cut (edl9.json)

135.13 s, 8108 frames at 60 fps, 1920x1080; 88 clips, 0 claim conflicts, 0 back-to-back pilots. Song -13.2 LUFS,
game bus trimmed to sit under it, final -12.8 LUFS / -0.6 dBFS peak. Pilot screen time 7.6-13.7 s (juggernaut lowest,
maverick highest) - not equal, reported rather than forced.

`whiteness9.py` scores each boss/pilot take's white-silhouette share per frame from the pixels (modular bosses flash
per PART, which the `bf` metric cannot see); edit9.py subtracts each take's median and penalises the rest. Lizzie's
special is exempt - her atom bomb IS a white flash.

The stage-8 card is its own take (`F_card_s8b`, `setState(GS.INTRO)` on stage 8): a real stage-8 arrival comes
through the stage-7 portal, whose first frames are a slit, not the card.

## Licensing caveat

The HAMA segment plays `hama_instrumental_0928.mp3`. `docs/HAMA_0928.md` records that a public or Steam release needs
a sync licence for that track, or the track swapped. The trailer carries the same caveat.
