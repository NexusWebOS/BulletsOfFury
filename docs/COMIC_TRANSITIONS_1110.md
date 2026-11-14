# Comic mission bridges and nine Chronos finishing reels

Mike requested straight/angled comic dividers throughout the between-level scenes, a stronger Stage5→6 transition, and nine spacecraft-specific versions of the Chronos missile shot.

## Production owners

`assets/cinema_comic_art_1110.js` registers the new banks; `assets/cinema_comic_1110.js` loads after the existing `cinema_direction_1110.js`. The original symbiote-code satellite correction remains active. Core combat, missile simulation, Chronos death phases, rewards, saves and campaign continuation retain their native owners.

The complete durable production pack is `C:\Users\Mike\Documents\Codex\2026-11-10\you-are-a-cinematic-director-for-3\outputs\BOF-Cinema-1110`.

## Presentation

All main mission bridges after Stages1–7 and the bonus mission use authored comic gutters: straight vertical, forward slash, reverse slash, stacked panels, angled triptych and impact split. Twelve transparent 912×512 plates cover captioned/silent heights. They were authored offline in Aseprite and reopened pixel-exact. Runtime polygon clipping places the animation in the matching apertures; the rules and effects are raster artwork, not generated browser strokes.

Panels pair actions with a different useful view: instruments, a listener, the actual aircraft or the flight wing. Compact portrait sizing preserves faces in short panels. Readings use an authored window rather than lying over a face. The primary and co-op pilot indices are synchronized in the review so its selected partner is the one rendered.

## Stage5→6

The native Chronos finale already owns the orbital return. The revised debrief therefore starts on approach to HQ, using a new clear coastal atmosphere plate and the pilot's actual ordinary jet. It continues through the overhead hangar landing, rotary salvage, crew exchange, increasing radar contacts, alarm, guard assignment and the flight-wing launch. Active pilots stay out of the base guard roster. The squad insert shows the native five-ship flight wing, excluding duplicate active-player thumbnails.

Hard/Furious retain the actual Stage6 launch. Easy/Normal show a standby order before their native completion/difficulty menu; they no longer depict a Stage6 sortie they cannot enter.

## Nine space-ship reels

Fresh current-game `furyShipCanvas` exports supplied top, bank and end-on identity references for all nine pilots. These are the actual space armor kit, not the ordinary atmospheric fighter. Native accent identities are Cole green, Axel blue, Freezer violet, Yuri red, Maverick teal, Falva pink, Lizzie bronze/ochre, Decker bright yellow and Juggernaut orange.

Nine independently generated 1536×1024 masters contain six equal 512×512 frames each: ready, release, travel, impact flash, expanding fire/debris and banked escape. They preserve the common kit geometry, silver armor planes and each pilot's color distribution. These 54 new frames accompany the actual current Chronos in a separate panel. The native core flash, swelling, cookoff, explosions and armor-piece breakup continue to render from their existing authored banks, driven by `h3EndingTick`/HF17/CE110/CO110. One real missile impact remains the sole destruction trigger. The cinematic uses a fixed screen transform so combat camera zoom cannot distort its comic layout.

The space bonus mission's return also uses the matching space-armor reel rather than an ordinary jet. Its co-op insert loads and displays the partner's own palette. All nine orbital and bonus return selections are covered by the scene checks.

## Sources and verification

`source-art/references/space-current/` contains27 fresh native exports and their hashes. `source-art/comic/masters/` contains nine spacecraft sheets and one coastal environment. `source-art/comic/generation-prompts.json` records built-in image-generation prompts and reference roles. `source-art/comic/aseprite/` contains nine editable six-frame reels and one twelve-frame divider source; all66 frames reopen unchanged. Production images are lossless WebP with fixed even cells and shared pivots. `source/build_comic_assets.py` owns the exports and registry. `source/author_comic_dividers.lua` owns the divider source.

The focused review passed144/144 scene/identity/layout checks,50/50 native campaign continuation checks,8/8 real bossDie→missile→return→tally→Stage6 checks, and13/13 replay-control checks. Installed verification is recorded under `verification/comic/`. The live check used the actual game display route, not just a preview callback. This is focused cinematic and continuation verification rather than a full combat campaign playthrough.

The full game suite retains its existing missing `difficultyHealthBaseline15` failure. The core game and test files remain unchanged; the Windows installer is not rebuilt. No commit or push is made.

Open `Start Review.vbs` in the pack and choose **Chronos · Missile / core impact / escape** or **After Stage5**. Every pilot and co-op combination can be selected. The Chronos review replays the artwork against native boss rendering without changing progression.
