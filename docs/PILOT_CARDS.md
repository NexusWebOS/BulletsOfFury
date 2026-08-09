# PILOT CARDS + NEW STAGE FONTS — 0801j

    verify 104 passed / 0 failed · 52 pack keys + 288 sliced glyphs registered

## The reveal

Mike: *"the card pops up, and the text all forms letter by 1 letter, stat bar by star like a Mega
Man X menu screen ... fill the stat bars simulatinously 1 by 1 1 bar at a time with sounds."*

    in       0.45s  the card slides up
    type            name, title, callsign, affiliation and bio type out at 42 chars/sec
    bars            one bar at a time, ONE SEGMENT at a time, 46ms per segment
    special         the ability icon lands with a white flash
    hold            done

**The pack made this possible on purpose.** From its own passover: *"The cards are now visual
shells... Names, callsigns, affiliations, biographies, labels, and stat values are intentionally
not baked into the card art."* A card with baked text can only ever pop in whole. An empty data
window can be filled a character at a time — that IS the effect.

**Three details from the real thing**, because the charm is in the timing, not the layout:

1. the bar fills one segment at a time, each with its own tick. Not a smooth sweep.
2. each bar completes before the next starts, so the eye follows a single moving edge down the
   screen rather than four bars racing.
3. **the tick PITCHES UP as the bar fills** — 0.6 to 1.3 across 20 segments. A long bar sounds
   different from a short one, and you hear the stat before you finish reading it. This is the
   one people remember without knowing why.

All three are asserted.

**Any input skips it.** Same rule as the cinematics: a flourish must never trap the player.

## Specials

    cole        WARHEAD             falva     ROLLER-BALL
    maverick    HELIX BEAM          yuri      CHAIN LIGHTNING
    decker      CLOAKING SYSTEM     lizzie    TIME-DISTORTION
    axel        AFTERBURNER         freezer   ICE ORB
    juggernaut  SIEGE MODE

Each draws a real icon beside the name, pulled from that pilot's actual weapon art.

## Stats stay in game data

The pack asks for this explicitly: *"Keep numerical values in game data so balance changes never
require repainting a card."* Values come from `PILOTS[p]` at runtime and are mapped to 0-20
segments, so retuning a pilot never touches art.

The affiliation typo is fixed at the source too — the pack notes the old art read PRINCESS'S OF
THE SKY, and pulling from the profile means PRINCESSES OF THE SKY is what renders.

## Fonts

Stages 2, 5, 6, 7, 8, 9 replaced. 48 glyphs each — the new sets carry punctuation the old ones
did not: `.,!?-:+/%'()`

    184 old glyphs retired to _quarantine/font0801j
    288 new glyphs sliced from the magenta-source atlases

De-keyed by flood fill from the border with the rim despilled, not deleted — the standing rule.
Glyph order comes from each map's own `glyphs` string rather than an assumed A-Z.

**Stage 1 is untouched.** It is the UI font and the fallback for any character the others lack,
so replacing it would have reached into every menu in the game.
