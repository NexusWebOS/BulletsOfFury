# Official FURY HQ — Earth Division generation prompts

Mode: built-in ImageGen reference workflow.

These are the final production prompt specifications used for the approved generated identity pass. In every asset, the lettering is part of the generated illustrated object rather than a separately composited font layer.

## Master insignia

```text
Use case: logo-brand
Asset type: official faction logo master for a premium Neo-Geo / 1990s arcade military science-fiction game
Primary request: create a single unified, fully illustrated official insignia and wordmark for the Earth headquarters of an elite fighter-pilot division. Integrate a heraldic Earth globe, swept mechanical wings, nine-aircraft formation, orbital ring, stars and lightning into engraved gunmetal, aged silver, dark navy enamel, military green enamel, gold trim, restrained cyan lights and amber status lights. Use monumental embossed arcade title lettering and an engraved lower command ribbon. The emblem, title lettering, ribbon, metalwork, shadows, wear, lighting and ornament must all be part of the same generated artwork.
Text (verbatim): exactly two lines only: "FURY HQ" and "EARTH DIVISION". Render both exactly once. Spell FURY as F-U-R-Y, HQ as H-Q, EARTH as E-A-R-T-H and DIVISION as D-I-V-I-S-I-O-N.
Constraints: one centered production-ready logo lockup; transparent background; no flat web banner, typed overlay, corporate logo, generic UI panel, extra words, initials, slogans, numbers, scenery, mockup wall or watermark; clean silhouette with no glow halo.
```

## Horizontal headquarters sign

```text
Use case: logo-brand
Input: approved master insignia
Primary request: derive a fully generated ultra-wide physical command sign preserving the master globe, mechanical wings, nine-aircraft formation, enamel palette, metalwork and title treatment. Add sculpted armored endcaps, inset badge, engraved backing plate, dimensional title, integrated lower ribbon, bolts, seams, wear, grime and internal illumination. Generate the words as physical raised lettering on the object itself.
Text (verbatim): exactly "FURY HQ" and "EARTH DIVISION", once each, with exact spelling.
Constraints: front-facing approximately 4:1 sign; no generic rectangular UI panel, plain typography, modern corporate layout, extra copy, mockup scenery or watermark.
```

## Vertical hangar standard

```text
Use case: logo-brand
Input: approved master insignia
Primary request: derive a fully generated tall armored ceremonial aerospace standard preserving the master identity. Use a sculpted crest, stacked monumental title, engraved division ribbon, armored borders, rivets, seams, subtle battle wear and pointed lower finial. The lettering and crest must be inherent parts of the illustrated object.
Text (verbatim): exactly "FURY HQ" and "EARTH DIVISION", once each, with exact spelling.
Constraints: front-facing approximately 2:3 standard; no generic UI, plain typed subtitle, extra copy, mockup environment, country flags or watermark.
```

## Exterior architectural signage

```text
Use case: precise-object-edit
Inputs: exterior edit target plus approved generated horizontal identity
Primary request: remove the flat rectangular first-pass text panel and replace it with a newly generated, physically integrated headquarters insignia above the entrance. Reinterpret the approved identity as sculpted architecture with gunmetal, silver, navy and green enamel, gold trim, inset cyan/amber lighting, Earth globe, mechanical wings, nine-aircraft formation, deeply embossed lettering, engraved division ribbon, structural mounts, realistic wear, grime, shadows and reflections. Match the original perspective, distance, weather and lighting.
Text (verbatim): exactly "FURY HQ" and "EARTH DIVISION", once each, with exact spelling.
Constraints: preserve the exterior composition, jungle, beach, ocean, runway, buildings, water, camera and grade; do not paste a flat sign or use generic text; no extra wording, people, vehicles, flags or watermark.
```

## Ending cinematic — restored FURY HQ

```text
Use case: lighting-weather
Input: the approved digital-night FURY HQ runway plate
Primary request: preserve the exact base, runway, radar dishes, mountains, jungle coastline and ocean while changing the scene to first light after the final battle. Remove the virus corruption; restore coordinated cyan, green and amber indicators; add restrained welding sparks, steam and radar pulses. Keep the central runway open for a separately composited top-down pilot ship and the lower quarter dark for dialogue.
Style: premium 1990s arcade pixel art with crisp hard-pixel clusters.
Constraints: no aircraft, characters, text, UI, blur or redesigned architecture.
```

## Ending cinematic — damaged satellite dish

```text
Use case: stylized-concept
Primary request: a dramatic close, low-oblique view of a huge damaged FURY HQ deep-space satellite dish after the battle, looking upward toward the stars. The cracked concave bowl must remain readable as a launch surface, with scorched armor, sparking cables, smoke wisps and one overlooked red infected indicator. Leave open space for the separately animated survivor fragment.
Style: premium 1990s arcade pixel art; wide 16:9, center-safe 4:3; dialogue-safe lower quarter.
Constraints: do not draw the survivor, aircraft, characters, text, UI or malformed dish geometry.
```

## Ending cinematic — symbiote survivor

```text
Use case: precise-object-edit
Inputs: approved black BOF2 shadow mech and the retired red survivor
Primary request: replace the armored projectile form with one compact living black ooze-virus fragment. Use a low wet tar mass, curling/dripping gripping tendrils, a few embedded blackened mechanical shards and one tiny sickly-green internal eye. The silhouette must work both crawling over a satellite bowl and contracting into launch.
Output: genuine transparent-background PNG with the full horizontal ooze mass inside generous margins.
Constraints: at least 90 percent black, near-black and charcoal; no red veins, red core, missile silhouette, spacecraft, scenery, crop, baked checkerboard, blur or halo.
```

## Ending cinematic — BOF2 shadow mech

```text
Use case: style-transfer plus background-extraction
Input: supplied gold-and-brown round mechanical model on magenta
Primary request: preserve that model's exact recognizable geometry: large round spiked armored hull, pointed lower nose, one horizontal green slit-eye, exactly two long symmetrical segmented arms and two three-prong claws. Re-render it as a heavily shadowed black/charcoal teaser with minimal edge light, one dim green eye and only subtle black-virus ooze in its armor seams.
Output: genuine transparent-background PNG designed to scale from distant contact to larger than screen.
Constraints: no gold or red palette, demon head, mouth, teeth, wings, legs, tentacle wings, extra limbs, scenery, crop, baked checkerboard, blur or halo.
```

## Ending cinematic — deep-space starfield

```text
Use case: stylized-concept
Asset type: wide ending-cinematic background plate
Primary request: true outer space far beyond Earth's atmosphere, with an overwhelmingly black field, hundreds of crisp stars at varied depth, restrained white/cyan/violet points, subtle distant violet-black haze and a faint central approach corridor.
Style: premium 1990s arcade pixel art; wide 16:9 with a center-safe 4:3 crop.
Constraints: no Earth, planet, horizon, atmosphere, clouds, blue sky gradient, ships, enemies, text, UI or watermark.
```
