# Cinematic Ship Generation Prompt Record

## Workflow

Built with the built-in ImageGen reference workflow. The runtime ship atlas `assets/game/atlas/nca_4.png` and `assets/manifest.js` were used to reconstruct six canonical source poses for each pilot in `_BUILD_SOURCE/cinematic_ship_inputs/`.

Each pilot was generated as one complete six-view sheet to keep its proportions and design coherent. The generated chroma masters are retained in `_BUILD_SOURCE/cinematic_ship_chroma/`; deterministic extraction then removed and decontaminated the key color, produced true RGBA, split the fixed frames and created tight cutouts.

## Shared generation contract

- Production cinematic multi-view ship sheet for a Neo-Geo-style arcade shooter
- Exact 1536x1024 canvas with an invisible 3-column by 2-row layout
- Exactly six complete views, one ship centered in each 512x512 slot
- Preserve the canonical silhouette, fuselage proportions, wing/pod placement, cockpit, engines, palette, markings and surface motifs
- Render as luxurious late-1990s arcade sprite art with hand-painted pixel clusters and pseudo-3D mechanical depth
- No pilot, people, other ships, scenery, sky, stars, ground, panels, labels, text, UI, smoke, contrails, projectiles, damage or long exhaust trails
- Uniform green key for non-green ships; uniform magenta key for Maverick and Cole

## View order

1. Strict top-down neutral, nose upward
2. Front-left three-quarter pseudo-3D hero
3. Front-right three-quarter pseudo-3D hero
4. Rear-left three-quarter with engines visible
5. Rear-right three-quarter with engines visible
6. Dramatic hard-bank upper-side view

## Ship identity locks

- **Axel:** cobalt-blue and black angular command interceptor with cyan edge lights and layered swept wings.
- **Freezer:** white-chrome and violet biomechanical manta with hooked crescent wing blades and a purple core.
- **Falva:** hot-magenta needle fighter with a long dark canopy and slim wing-mounted pods.
- **Lizzie:** golden retro single-propeller warbird with blue canopy and star roundels.
- **Yuri:** red-silver spearhead delta interceptor with cyan-blue engine core.
- **Maverick:** neon-green and gunmetal many-bladed stealth interceptor.
- **Juggernaut:** charcoal flying fortress with dense cylindrical pods and orange engine details.
- **Decker:** black and antique-gold prototype needle interceptor with fine technical accents.
- **Cole:** military-green and black command fighter with broad wings, side booms and clustered engines.

## Targeted continuity repair pass

Built-in ImageGen was run once per affected frame using the current frame as the edit target and the corresponding canonical ship reconstruction as the second reference. The shared instruction locked camera, scale, palette, cockpit, wings and surface detail while replacing only the invalid rear geometry.

- **Falva 02, 03, 06:** remove every solid rear cone, spear or second nose; terminate in the canonical compact nozzle with only a short soft purple gaseous exhaust.
- **Decker 02, 03, 06:** remove every solid rear cone, spear or second nose; terminate in the canonical compact engine assembly with only a short soft orange gaseous exhaust.
- **Lizzie 04, 05:** remove the invented glowing tail bulb; retain a plain gold vertical fin, rudder and horizontal tailplane, with the sole engine and propeller at the front.

Each repair was generated against uniform green chroma, resized before dekeying, decontaminated into transparent RGBA, and inserted only into its original 512x512 master slot.
