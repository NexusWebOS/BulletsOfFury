# Herald six-slice storm ritual — October31

Mike requested scene darkening, the final red warning flash before any inscription, larger separated sword-like lines with loud slice sounds and lightning, then a1015 accelerating spinning circle/star, expansion and explosive shatter into tornadoes.

`assets/herald_ritual_1031.js` (HR92) owns only the Herald storm cast. It extends the existing native warmup and switches off HR87's earlier fast seal. It uses the original generated HS53 seal, the actual red HH69 lightning, the existing warning plate palette and native tornado arrival, flash, damage and recovery. The other attacks, parts, health, ordinary one-pass glass, desperation counters, rewards and global bullet-marker removal are untouched.

| Game time | Presentation/event |
|---|---|
|0–0.65s|Background darkens; green warning.|
|0.65–1.25s|Yellow warning.|
|1.25–1.65s|Held red warning.|
|1.65–2.15s|Final red/white authored warning flash; no seal.|
|2.20,3.20,4.20,5.20,6.20s|Five large strokes, each carved over0.20s and held; one blade sound and a three-lane lightning release per stroke.|
|7.20–7.80s|Sixth slice forms the circle/runes.|
|7.95–10.20s|1015 emission and authored clockwise rotation accelerate from0.16 to approximately2.5turn/s.|
|10.20–11.00s|Still-spinning seal expands approximately36%.|
|11.00–11.65s|The exact seal splits into18 sectors, with original ruby prism-glass glints, flash and blast/glass cues.|
|11.32s onward|Native tornado arrival follows the shatter.|
|11.65s onward|Native tornado collision and red-orb volleys release, followed by ordinary finite recovery.|

The circle pixels were explicitly separated from all five star strokes; the former source's partial cells leaked inner-circle material early. No line or rune is drawn before the official flash. A single native attack clock schedules visual selection and the six slice/thunder pairs, without host timers or render-driven events. Pausing freezes it, death/stage changes cancel it, and reduced-motion warning mode holds red rather than flashing white.

There are268 fixed authored cells across seven banks, all even dimensions with explicit central pivots, plus seven editable Aseprite sources. The seal grows from its actual source to roughly360px; the expansion reaches roughly490px. Shatter uses an832x832 canvas so every source fragment fits as it travels. Runtime uses fixed native source-over blits, with no runtime sprite scaling/turning, filters, animated alpha, generated lines or blend effects. The per-pose skull/arms stay with existing authored HH52/HS53 charge and raised poses; native damaged pixels and flash expiry were verified.

Sources/manifest/provenance: `assets/game/levels/stage_08/miniboss/herald_ritual_1031/`. Rebuild with `_BUILD_SOURCE/build_herald_ritual_1031.py`; exact PNG reproduction passed. Audio in `assets/game/shared/audio/herald_ritual_1031/` re-masters the existing approved chip slice into three small pitch/presence/short-echo variants. Lightning reuses the existing Dracodia-derived strike recording. Bounded native pools and shared volume/mute controls remain authoritative; music ducks during the ritual. Accepted decoded playback and recording levels were measured; user audition remains available through the movies.

Verification: 67 focused checks passed, including32 native timeline/renderer checks,5 native damage/reduced-flash checks,24 source/frame checks,1 reproducible export and5 browser-playback checks. Syntax passes. The mandatory full suite reaches its summary and exits1 with the same five baseline failures:

- and the flash is held long enough for a single hit to register
- dialogue ends with the opening jump warning
- opening jump lands and returns before chromium activation
- unchosen right route persists as the opposite Stage X fight
- Stage X right branch launches a full encounter

Core game.js remains `024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de`. No paid generation, commit or push.

[Current ritual review](http://127.0.0.1:51046/?herald=six-slice-ritual-1031#clip=stage8-herald-inscribed-storm). The focused video is explicitly labelled an attack checkpoint: full native4264HP, no firing and no HP/phase/timer writes during filming. All six slices and six lightning cues played, with zero game/render/asset/audio-tap errors. The full encounter uses native4264HP and an input-only GOD observer through real defeat; no recorder damage/phase/time writes. Movies fully decode, with negative output peaks. Exact performance/audio values and source recordings are in `docs/qa/herald_ritual_1031.json`. Earlier short-seal recordings remain archived in the gallery.
