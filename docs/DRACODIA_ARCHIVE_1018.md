> Latest extension: [moving hover, core missiles and charged arm lasers](DRACODIA_HOVER_1018.md).

# Dracodia: code storms and archive downloads — 18 October 2026

Dracodia's main Colossus form now alternates downloads, physical scythes,
spiraling lightning, code bombs, its arm-raising roar and core spores. The
existing Hammer, helicopter, Harrier and volcano copies keep their distinct
controllers and finite health pools. Downloaded enemies are separate actors;
they do not add transformations or campaign rewards.

The supplied [Dracula fight](https://youtu.be/0YvOl8PQrhI?t=55) informed the
depth changes, curling electrical lanes and background activity. The supplied
[Smithy fight](https://youtu.be/qBmdxtSSvuU?t=301) reinforces the existing
distinct copied forms. These are adaptations to the authored BOF encounter.

## Combat

- **Spiral lightning:** two, three or four outward spirals on Normal, Hard and
  Furious. Each release keeps its origin and follows its own curved trajectory.
  Contact follows the moving projectile. Charge warnings precede release;
  the canonical lightning charge/release/impact sounds remain active.
- **Code bombs:** Dracodia uniformly recedes to 53% size in the background,
  throws five shootable bombs at committed locations, then returns to the
  player plane. Each target has a ground warning and timed detonation. Bomb
  bodies cannot kill before detonation. Shooting one produces a harmless
  smaller burst; the native player damage function owns dodge protection.
- **Archive formation:** one former miniboss on Normal, with an ice escort on
  Hard and a second toxic escort on Furious. Downloads assemble harmlessly,
  settle, warn, then fire. The owner cap is one/two/three live actors, including
  surviving downloads. Phase changes erase the formation and its ordnance.
- **Physical weapons:** every downloaded hull has independent core and side
  weapon pools, corresponding real-pixel render plates and Retina targets.
  Destroyed batteries stop firing and leave the target list. All cached locks
  retire immediately when the hull dies. The blue gunship
  retains its central cannon. Native `markHit` owner/part flashes remain visible
  and expire; authored palettes return between hits.

Bastion alternates gun bursts and artillery fans; Camo fires shootable,
non-homing missiles; the blue gunship fires its side guns and heavy central
cannon. Cryo Spear fires ice fans, while Brood fires toxic bursts. Reused escort
barrels were inspected through the native renderer before measuring muzzles.

The source maxima of the supplied BZ0 **Iron Bastion** and BZ4 **Camo Colossus**
use their old Stage 8 spawn formula and original multipliers (1.10 and 1.15).
The supplied blue gunship has a new, unscaled full-strength budget of 1,060;
it is not the unrelated old Blue Halberd sprite. Difficulty and co-op scaling
apply once, then each miniboss starts at `ceil(sourceMaximum * .5)`. Tough
escorts retain their original full enemy pools.

The native boss clock still owns dialogue, persistent hazards, transitions and
defeats. Only the main form's attack dispatcher is extended. The one new core
collision flag, `_noBodyContact`, separates shootable timed ordnance from body
ram damage. Other enemy collision behaviour is unchanged.

## Art ownership

Mike explicitly approved uploading only BZ0, BZ4 and the supplied blue gunship
screenshot to PixelLab, using existing credits up to $7.68 with no top-up.
Those were the only local references uploaded. Additional effects used text
descriptions and subsequent PixelLab-generated images. The measured balance
changed from $7.68 to $5.03: **$2.65 used; no top-up**.

Owner: `_BUILD_SOURCE/build_dracodia_archive_1018.py`. Raw responses, prompts,
original returns and pose selections remain under
`_ART_SOURCES/dracodia_archive_1018/`. The first flat star-shaped detonation is
archived and excluded. Blank holds, early reverse-breaking download poses and
the blue gunship's faulty grey tail are excluded. The standalone transfer VFX
needed neutral-grey segmentation-matte removal. Source pixels otherwise keep
their proportions; there is no per-frame fitting, interpolation or duplicate
frame padding.

| Shipping bank | Poses | Canvas and pivot |
| --- | ---: | --- |
| Bastion download | 18 | 320 × 320; 160,160 |
| Camo download | 18 | 320 × 320; 160,160 |
| Blue gunship download | 22 | 320 × 320; 160,160 |
| Code bomb charge | 16 | 160 × 160; 80,80 |
| Code bomb detonation | 22 | 160 × 160; 80,80 |
| Spiral lightning | 18 | 128 × 128; 64,64 |
| Void storm and escort transfer | 32 each | 320 × 320; 160,160 |

Each bank uses one scale and a shared pivot. Padding is common across each
bank, with world-size compensation preserving the physical footprint. Three
full hulls and their nine exact source-pixel plates complete **190 PNGs,
2.94 MiB**. Module reassembly is RGBA-identical in the builder and pixel-identical
through Chromium. No shared atlas was changed. The two old escort ships retain
their actual XART sprites and use the generated transfer effect during reveal.

## Review and verification

Live full-field review: `docs/previews/dracodia_archive_1018/index.html`.
Every selected pose can be scrubbed, played and onion-viewed in `frames.html`.
The review pilot is invulnerable and saves use an isolated prefix. Production
does not inherit the review's protection. Selected attacks repeat without changing to another attack or copy; the full
book option uses the natural sequence. The older Stage 8 review's Roar
selector is updated for the extended attack book.

**248 native checks passed**, with no page, console, drawing or missing-asset
errors. The core suite finished at **8,784 passed, 0 failed, BUILD OK, exit 0**,
matching its measured baseline. Authoritative counts, source hashes and final exits are in
`docs/qa/dracodia_archive_1018.json`. Evidence is under
`_shots/dracodia_archive_1018/`. Tests exercise real XART cells and the game
context's `drawImage`, actual machine-gun and Retina damage, all three
difficulties, native unprotected player damage and dodge protection, physical
swipes, blackout transitions, the new avatar, armor breakup and the single red
portal campaign ending. This is encounter verification with controlled scenes;
it is not a new human survival-balance or complete campaign-clear claim.

Existing work is retained. `assets/game.js` keeps LF; `test_fl.js` keeps CRLF
and was not edited. No commit or push was performed.
