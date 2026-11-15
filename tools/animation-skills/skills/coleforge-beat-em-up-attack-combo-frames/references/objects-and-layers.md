# Objects and layers

Manifest: material/identity, native cell/root, carry eligibility, HP, intact/damage/airborne/break/debris/cleanup frames, bounds, hand offsets and release pose/time. Keep dimensions/shape consistent; retain editable Aseprite sources and independent exports.

- Corrugated steel trash can: dent ribs, pop lid, crumple shell/scraps; no glass-like fracture.
- Wooden barrel: split staves, spring hoops, falling/settled wood. Steel drums instead buckle sheet metal and shed lids/rims.
- Newspaper dispenser: buckle metal box, glass fragments, open door and paper sheets.
- Car: dents, broken windows, sagging chassis, metal/glass debris; heavy fixed obstacle unless designed otherwise.

Break progression: contact/deformation → separation → pieces spread/fall → remnant → short visible/blank authored-frame cadence → removal. Stage gates must not wait for cleanup. Avoid large-screen strobes. No runtime fades, rotation, tints or generic explosion replacement; draw orientations if spinning is wanted.

Carry: eligible nearby object + grounded available player + input edge → exclusive reservation → lift → hold/walk → attack edge → windup → one release pose → arc/contact → break/settle. Hit/death/disconnect/exit clears ownership and drops safely. Resolve simultaneous pickup once. No duplication/stealing/infinite overlap damage. Validate lane/height, co-op friendly-fire policy and offscreen cleanup.

Native OpenBOR obstacles are stationary damageable entities, not automatically liftable. Inspect the exact engine revision and test script/weapon hooks. [Type](https://chronocrash.com/obor/wiki/type/), [weapon models](https://chronocrash.com/obor/wiki/weapons/). Carry weapon models must preserve identity/stats/scripts/controls and safe HUD name mapping. Direct script HP assignment does not synthesize native damage events.

Keep collision/route separate from art. Use a logical pixel grid, finite palette, clear clusters/stepped edges, restrained dithering and stable lighting. Separate sky/clouds/skyline/middle buildings/facade/floor/objects/foreground. Match horizon, floor and seams street → stairs → subway. Train is a timed layer behind near platform and in front of opposite wall. Combine slow camera parallax with independent cloud drift; facade follows the world.

Vents, neon, water/drips, flags and lamps use authored timed banks/anchors. Do not obscure combat targets. Check repeated seams at several camera positions, route transitions and a two-player prop encounter in the actual engine.
