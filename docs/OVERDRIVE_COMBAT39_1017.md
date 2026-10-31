# Overdrive combat39 and Night Run — local update, 2026-10-17

Build `overdrive1017-combat39-r1`. This pass did not edit assets/game.js and did not commit or push. Existing local changes are retained.

## Playable changes

Level 3 keeps directional top-down Yuri and enemy banks throughout attacks, cover and reloads. Clean crouch/peek/fire poses replace scenery-bearing cover clips. One body unit owns each actor through walking and firing. Ground minigun/fire loops continue throughout their bursts. The new bat drone uses PixelLab directional hover, flight and firing banks. Existing compatible roller fold/ball/unfold behavior is retained.

Enemy perception uses an obstructed sight cone, six-second last-known-position memory, nearby squad sharing and firing noise. Existing cover/flank/search tactics consume that perception. A lost visual during windup cancels the attack; a committed ground burst retains its release schedule and target. BOF authored green/yellow/red FOV cones originate at the weapon socket. Dead owners cannot launch further rounds.

F toggles prone in keyboard defaults. Generated prone-body rolls are used in level 3, rear-view base combat, the side-view service corridor and Night Run. Every bank keeps its padded canvas, fixed root and body scale. The corrected north roll stays oriented along its head-to-feet axis; the earlier heading-spin candidate is excluded.

Gosfer uses the new whole-body movement, firing, jump, roll, claymore-throw and death plates. His native pose owner and weapon socket share the same selector. Action clocks traverse their complete generated banks. At unshielded 50% HP he throws charges onto the visible left/right wall panels; they arm, explode, remove those collision panels and admit four flamethrower reinforcements. His existing shield/dialogue/transformation encounter remains intact.

The player can obtain finite travelling flamethrower attacks and a segmented cryogenic lance projectile in levels 3 and 4. Cryo hits slow enemies. The base offers flamethrower/cryo/minigun elite drops on waves 2/3/4. Its four regular waves each require both turrets to be destroyed before their door core can take any damage. Destroying that core advances even if infantry remain alive. The fourth breach enters the boss encounter.

## Level 5: Night Run

The new mission starts with Yuri, Phoenix, Hotwire and Niel on foot. Shoot supply crates, collect missiles, reach the vehicles and board. Phoenix drives the black/red S-10-inspired truck, Hotwire rides passenger, and Yuri operates its separate mounted weapon. Niel and his pale green/teal/white Mustang sit in the foreground with the window open. Both vehicles use strict side elevation. Body, wheels, doors, turret parts and sockets are registered separately; runtime wheels and the rigid turret move independently.

The chase has PixelLab parallax scenery, road and gate, original armored robot runners and an alien hunter drone. Yuri has generated level/up/down mounted poses with recoil, mirrored as complete banks. Reticle aiming turns the mechanical turret; the exact same transform locates its projectile muzzle. Niel fires support shots at runners. Enemy shots travel to locked hull positions. A bullet costs exactly 1% hull; a drone missile costs 5%, at every difficulty. Incoming missiles can be intercepted. The 150-second encounter ends with the gate ram, explosion, black fade and the native clear signal. A wreck regroups all four at the on-foot start.

The debrief is a new Overdrive backplate using the actual BOF logo, rank artwork, pilot portrait, score/time/death bonuses, password and original pad prompt. Night Run contributes hull integrity, interceptions and restart counts through the existing scoring owner.

Campaign order is display 2/internal2 tank, display3/internal3 fortress, display4/internal7 base, display5/internal6 Night Run, display6/internal4 Machinists, display7/internal5 desert.

## Art, review and provenance

Combat package: 431 playback banks / 4087 frames / 27 stills. Night package: 53 banks / 280 frames. Counts include aliases and complete-bank mirrors; they are not counts of new AI generations. PixelLab supplies actor/effect/environment work; the image generator supplies the vehicles, crates/pickups and debrief plate. Only selected strict side-on vehicle sources are used.

The hardware repairs use PixelLab exact pixel operations. Camera-turning west clips are replaced by complete-bank east mirrors. North weapons retain their original rigid geometry; native muzzle VFX and projectile events remain separate owners. Unwanted body/backpack flashes are removed or rejected; normal hit flashes and Gosfer's existing energized transformation are preserved. No animation frame is individually resized to its bounding box.

`art/combat39/source/generation39.json`, `source/receipts/`, `source/references/` and the source vehicle/supply/debrief PNGs retain provider IDs, prompts/receipts, fixed-keyframe references and exact repair provenance. Host generation/rebuild workspace: `C:\Users\Mike\Documents\Codex\2026-10-15\fo\work\overdrive39`. Owners there are build_assets.py, build_night.py and quality39.py. The earlier curated PixelLab library remains in the Codex workspace under outputs/bof-pixellab-rebuild. Those sources are deliberately retained rather than copied wholesale into this disk-limited repository.

Fixed-root +/-1 and +/-2 onion sheets cover 108 combat/locomotion banks, with representative sheets visually inspected. All exported frame dimensions and bank roots pass structural checks. Whole actor scale is preserved across state changes. Rejected drafts remain in the generation workspace and are not selected by runtime selectors.

## Verification and limits

- `node --check assets/game.js` and syntax checks on the 12 edited runtime modules pass.
- Required `node _BUILD_SOURCE/test_fl.js` reaches BUILD OK / 0 ERRORS, exit0. Log: `_shots/combat39/required-suite.log`.
- 54/54 focused checks pass through the production modules and actual native Canvas2D/PNG rendering. They exercise crate projectile collisions, collection, boarding, exact hull damage at all difficulties, missile interception, ram/fade/clear, every core wave with live infantry, blocked sight and search memory, directional/size continuity, rear prone rolls, Gosfer's four reinforcements, even dimensions and fixed roots, actual white hit pixels and exact restoration, and approved sound routes.
- All 12 new-route cue files decode to non-silent PCM through FFmpeg. This is a file-decoding check, not a claim of browser audio playback.
- Evidence is in `_shots/combat39/`; JSON copies are under docs/qa. `node expansion/topdown/_research/verify_combat39.cjs` reruns the native module/render check on this host.
- Live Chromium playtesting and audible browser playback remain outstanding. The browser tool still reports local browser use disabled in Work settings. No browser restriction was bypassed and no full live-input route clear is claimed. The native screenshots are rendered test scenarios, not proof of a browser playthrough.
