# October 5, 2026 — paused Dracodia cinematic passover

Mike explicitly asked to pause implementation and publish the current game,
unfinished work, and this passover to GitHub. **Do not treat the draft cinematic
as a completed or verified feature.** Resume this document before implementing
the next pass. Read `HANDOFF_CODEX.md`, `CLAUDE.md`, and the project guide first.

## What is playable and verified

The published game loads the permanent password catalog (59 codes, nine pages),
complete fixed portrait frames for all nine Fury pilots, the alien arena and
modular ghost, and Stage 6 approaching-pellet/elite-turret warnings. These are
the finished local passes since the previous GitHub publication, `d2356b86`.

- `assets/password_catalog_1005.js`: pinned in-game catalog; D-pad/mouse pages,
  A fills a code, B returns; raw-keyboard duplication fixed.
- `assets/cole_portraits_1005.js` and `assets/pilot_portraits_1005.js`: complete,
  stable bezels; mouth-only speech, preserved facing and pilot proportions.
- `assets/alien_arena_art_1005.js`, `assets/alien_arena_1005.js`: almost-black
  central corridor, constant authored swirling void, twelve animated green code
  frames, rib parallax, drone engulfment, articulated modular ghost with its
  complete head, white hits and opaque breakup. Stronger host/ghost/Dracula
  attack books, actual copied campaign controllers, persistent HP and modules,
  forty-second Furious copied-form visits.
- `assets/pellet_warnings_1005.js`: predicted approaching-pellet glow and original
  impact asterisk, four nearest threats per living player; warned/staggered elite
  fighter gun rain, movement and difficulty-specific recovery.

The most recent completed full suite reached **7,292 assertions, zero errors,
exit 0**. Alien-arena native/pixel/review evidence contains **44 passing checks**
with zero browser errors. Earlier portrait evidence contains 236 all-pilot checks
and 46 Cole checks; the password catalog contains 89 native checks. See the
corresponding `docs/qa/*_1005.json` and drop documents. Publication-time rechecks
are recorded in the handoff publication note. Protected silent recordings are
not unassisted Furious clears or final balancing proof.

## What Mike wants next — exact encounter order

There are **three outer Stage 8 fights**. The original drone arrives, mutates and
becomes encounter 1; encounter 2 is the ghost; encounter 3 is the giant
Dracula-like alien, now named **Dracodia**, who owns the eight copied boss forms.
Do not move the copied forms into the first two fights or allocate a fourth outer
fight. Preserve each copied form's HP and broken equipment when switching.

After each of the first two defeats, the boss must visibly destroy, the player
must fly forward a little, then the entity reforms. Keep the world alive during
timed, protected dialogue; no incoming damage, player weapons, accidental skip,
extra loot or early campaign completion during these sequences.

1. First reform: **"What in the world is that.."**, then
   **"It's...Reforming?!"**
2. Second reform: **"......."**, then
   **"No amount of training could ever have prepared me for this."**
3. Final defeat: **"You. Are. Terminated!"**

The working interpretation puts the third line at the final kill, rather than
inventing another reform after Dracodia. Preserve Mike's exact dialogue above.

## Dracodia's reveal, portrait and speech

Generate/use his own complete animated portrait box; retain every frame edge,
keep the head/crown stable, animate speaking, and shake his box appropriately.
He must gesture with his arms and head in the live engine. A split-maw, The Thing
style alien scream must shake the whole screen and have a distinct audible cue.
Reveal him from the full-screen black symbiote void into the animated alien arena.
Keep the center dark and the green code moving; avoid download effects as a
substitute for organic mutation/reformation.

Mike's requested meaning and climactic lines:

- He does **not** know his true origins; he crossed from an unknown plane
  millennia ago. His knowledge and code make the entire universe comprehensible.
- Man will never triumph until he understands it. The virus exposed humanity's
  inferiority. He demands control and acceptance of his knowledge/code/power.
- **"Fear me!! I. Am. Machine. I am Man. I am EVERYTHING! THE WORLD WILL KNOW
  THE TRUE POWER OF I, DRACODIA! MASTER OF DESTRUCTION!!!!!!!!!"**

The draft expands this into twelve readable dialogue beats. The narration is
already written in its `DR5.intro` array; Mike has not reviewed that expansion in
game yet. Restore his exact phrasing if a change weakens the intended delivery.

## Final death and portal-home requirements

Mike wants the most spectacular authored destruction in the game, with a clear
sequence, not a fade-out or an instant generic explosion:

1. Shriek and pause. Raise both arms fully, lower them, then thrash them around.
2. Head turns left, right, up, down, then shocked forward and about-to-explode.
   **Keep his entire head and crown in every frame.**
3. Bright sun-like beams rupture from two ends of his body. Crackle, flames and
   fire disintegration culminate in escalating explosions.
4. Smoke rings, charred decals, alien symbiote chips/tendrils, spinning body/arm
   debris, layered fire and shock effects. Fragments stay opaque while moving
   into authored explosions; no module or enemy fade-away.
5. Better animated portal home and return-to-engine arrival. Original reunion
   remains the sole owner of rewards/completion, exactly once.

## Current draft and generated assets — not integrated

`assets/dracodia_cinematic_1005.js` is an initial runtime draft. It parses, but is
**not included in `index.html` or the full test harness**, has never been run in
Chromium, and does not yet have every referenced art/audio family. Do not add its
script tag and call it finished. `assets/dracodia_art_1005.js` currently registers
only twelve component cells. The existing playable game remains on the verified
alien-arena layer because the draft is deliberately unloaded.

Draft hooks capture/wrap `r30Tick`, `r30DrawBoss`, `j3Encounter`, `r30Break`,
`j3FinalDeath`, `drawWorld`, `drawPlayer`, `beginStage`, protected controls and
`XART._touch`. It sketches opaque destruction/forward travel, two reform radio
beats, the twelve-line villain introduction, articulated intro/death rig, a
sixteen-second finale and a seven-second portal, then the existing reunion.
Read the actual code; its existence is not evidence of correct behavior.

Four imagegen sources are preserved under `_ART_SOURCES/dracodia_1005/`:

| File | Content and current status |
|---|---|
| `parts.png` | Headless torso, two arms, nine head views. Twelve measured native crops deployed; complete crown intended, crop/joints still need native engine inspection. |
| `portrait.png` | Nine complete chrome/green/red portrait frames: idle, speech, confidence, anger, split-maw scream, shock, burning, decoding. Source inspected; no deployed cells yet. |
| `effects.png` | Sixteen cells: eight major alien-reactor explosion stages, four sun ruptures, four smoke/fire rings. Source inspected; no deployed cells yet. |
| `portal.png` | Twelve portal opening/steady/closing stages. Generated during the pause request; archived intact, not inspected or integrated. |

`archive_manifest.json` records archived source filenames, native dimensions,
hashes, prompt briefs and provisional crop guidance. `manifest.json` belongs to
the current parts-only builder. Original generated files were copied, not moved
or deleted. **The sheets are not evenly spaced despite the generation prompts.**
Inspect native boundaries and preserve alpha/pixels; never blindly divide them
into equal cells or rely on their names.

`_BUILD_SOURCE/build_dracodia_1005.py` currently builds only `parts`. Extend it for
the remaining families and register source/deployed metadata together. Leave
shared atlases alone. Do not repaint generated source pixels with Python.

## Concrete resume checklist, in order

1. Inspect the archived portal and native source sheets. Finish measured crops
   for portrait/effects/portal, generate the registry, and render contact sheets.
   Check every head/crown, bezel edge, transparent center and neighboring cell
   boundary for clipping/bleed.
2. Create/register a distinct Dracodia scream. The draft currently calls
   `r30Sound('dracodiaShriek')`, but that key is **not registered** and can fall
   back to generic alien combat sound. Available authored source clips include
   `assets/game/sounds/mechScream.mp3`, `wardenScream.mp3`, and
   `symbiote_warcry_0924.wav`. These may be layered/mastered with ffmpeg; keep
   provenance and do not describe processing as provider-generated audio.
3. Fix portrait/body speech animation. The draft keeps a stable frame and uses a
   mouth-only overlay for the two base speech frames, but its other expressions
   do not yet animate their mouths, and the in-engine head currently stays in
   the speaking pose instead of cycling/resting. Inspect mouth crop alignment.
4. Inspect raised/lowered/thrashing arm angles and head attachment in the actual
   context. Anchor the two sun-rupture beam origins to the body correctly. Add
   an actual authored charred decal; the draft's fire/smoke is not that decal.
5. Improve the portal arrival as well as departure. The draft hands off to the
   existing reunion, whose early arrival still draws the old portal FX. Replace
   that particular arrival with the new reel without duplicating rewards.
6. Check state cleanup, all player seats, timed protection, charged weapons and
   missile controls, music handoffs, pause behavior, boss HUD, practice-copy
   shortcuts, and non-Stage-8 behavior. Do not let draft radio/state leak into a
   fresh run. Intro runs once for the real third encounter; copied-form practice
   shortcuts must not repeat the monologue.
7. Only then load the art registry and cinematic script after the existing
   arena/pellet layer. Add meaningful regression checks; preserve `game.js` LF
   and `_BUILD_SOURCE/test_fl.js` CRLF. One writer for `game.js`; no edits to it
   have been needed for these October 5 layers.
8. Run `node --check assets/game.js`, syntax checks for new layers, and the entire
   test suite through its final summary. Compare assertion names, not historical
   counts. Report nonzero exits even if a failure predates the change.
9. Run real Chromium through `shoot.py`/native probes. Damage actual boss pools
   and observe both inter-phase breaks, flight, exact dialogue, monologue, all
   death poses, rupture/fire/debris, portal and exactly-one reunion award. Poll
   lazy XART assets with timers, yield between simulation batches, and inspect
   screenshots plus page/console errors. Verify sound actually plays.
10. Produce a playable review and short captured timelines; inspect visible
    head/arm continuity, explosions and portraits before marking complete.

## Continuing improvements and Mike's priorities

Keep Stage 6 and Stage 8 as the priority. Stage 6 and elite/Rebel bullet rain
needs fair readable gaps on Hard/Furious, meaningful original FOV warnings and
high-speed committed attacks. Test sustained lasers and Fusion against actual
Rebel hulls. Preserve five-versus-five teams, whole Rebel hulls, anchored pilot
HP, cloaked Nyx's hidden HP/Retina immunity, survivor counter-scan priority and
live protected dialogue. Voss must stay fast; Jace's ball and Rook's slugs go
south. Bombers must be true red/green swaps of the approved blue stealth fighter,
and the giant ace stays blue with white hit flashes.

Stage 8's first two fights must remain threatening, with distinct modular attacks
and cinematic transitions. Dracula/Dracodia must use the actual earlier boss
controllers and upgraded patterns, preserve all eight HP pools with no healing
on switches, and retain targetable knight sword/shield and exact-zero code
shatter. Keep Flash/Time Bomb assistance. Improve balance by recording real
gameplay rather than only protected probes. The Contra reference was sampled;
do not claim its whole 55-minute video was watched. The supplied long gameplay
recordings were sampled, not fully experienced as unassisted human runs.

Broader earlier requests and evidence live in their drop documents: campaign
map/HQ/islands/Stage X/navigation/save slots, Stage 7 direct portal to Stage 8,
Prism on Stage 6/Dark Matter on Stage 8, distinct boss/miniboss music, Hammer
reserve and in-engine destruction/homecoming, shootable balls/missiles only,
aligned spread muzzle flashes, weapon targeting, complete sounds and arcade
module deaths. Preserve these while improving the finale; don't reset them to
older designs. Mike explicitly values authored graphics, ambitious cinematic
presentation, fun aggressive battles and original warning conventions.

## Publication and workspace boundaries

Publish game-related finished files, source art/builders/probes/portable QA, and
this explicit unfinished draft. No unrelated projects, `.claude`/stopresisting
scratch, trailer source FLACs, or user recordings belong in this commit. Keep
them locally untouched. `_shots/` recordings/reviews are ignored and do not travel
with the repository; committed QA/documents record their evidence. Recreate
reviews from the included probes if needed. Inspect incoming GitHub commits
before integrating; do not force-push. Implementation is paused at Mike's request;
resume only when he asks.
