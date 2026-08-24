# Top-Down Cinematic Transition Backgrounds

Nine full-resolution environment plates for interactive transitions into the eight campaign stages and the Stage 9 bonus route.

- Native master size: `1672x941` RGB PNG
- Camera: true overhead, near-orthographic, approximately 85-90 degrees down
- Scene flow: bottom entry to top exit
- Content: environment only, with no baked ships, aircraft, vehicles, pilots, enemies, creatures, projectiles, explosions, text, logos or UI
- Intended use: place all moving actors and interactive objects over these backgrounds at runtime

## Included routes

1. Rumble in the Jungle - river islands, causeway and dam
2. It's Hot in Here - desert highway and volcanic zone
3. Ice Still Can't See - frozen research route
4. Crouching Missiles, Hidden Death - coastal checkpoint and airbase threshold
5. All for One, None for All - orbital causeway and transit gate
6. Heavy Turbulence - weather deck and supercell route
7. Not Another Sewer Level - toxic canal and maintenance intake
8. Furious Death - obsidian path and gravitational abyss
9. The Velocity Void - bonus transit-gate corridor

## Integration files

- `manifest.json` records stage mappings, hashes, source references and constraints.
- `interaction_zones.json` supplies shared placement suggestions for entry, traversal, side interactions and exit.
- `GENERATION_PROMPTS.md` records the common art contract and stage-specific direction.
- `previews/topdown_transitions_contact.jpg` is the 3x3 review sheet.

Rebuild metadata and the contact sheet with `_BUILD_SOURCE/build_topdown_transition_pack.py`; verify the complete pack with `_BUILD_SOURCE/verify_topdown_transition_pack.py`.
