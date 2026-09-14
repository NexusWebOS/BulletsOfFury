# Stage 3 enemy action-reel prompt set

Mode: built-in ImageGen edit workflow, using one exact shipped seed silhouette per unit. Every
request asked for one horizontal eight-frame Neo-Geo action strip on a neutral removable backdrop,
with no projectile baked into the hull, no halo, no crop, no new appendages, and stable mass,
palette, perspective, lighting, and center anchor across all frames.

- **Shard Mine:** sealed hover mine -> iris plates open -> cyan core swells -> peak release flash -> plates recover.
- **Elite Ice Interceptor:** stable top-down ice fighter -> engine emitters charge -> thrusters flare for a committed ram -> recover; preserve the exact tail.
- **AA Sled:** stable twin-barrel sled -> both physical barrels charge -> simultaneous muzzle flash and recoil -> center follow-through -> recover.
- **Snowmobile Gunner:** stable tracked snow vehicle -> compact forward gun winds up -> short machine-gun flash/recoil -> recover; no chassis deformation.
- **Ice Crawler:** stable multi-legged crawler -> claws brace -> center mortar core charges -> forward release flash/recoil -> recover.
- **Snow Tank:** stable heavy tracked tank -> turret/cannon charges -> one large barrel flash and chassis recoil -> recover; no extra weapons.
- **Cryo Barge:** stable broad ice carrier -> paired side launchers illuminate -> symmetrical release flashes -> recoil settles -> recover.
- **Tracked Frost Artillery:** stable long-barrel artillery -> chassis braces -> bore glow grows -> heavy muzzle flash and barrel recoil -> recover.

The generated strips were then cleaned to hard alpha and normalized as whole sequences with the
sprite-pipeline tool before their frames were copied into `assets/game/stage3_enemy_attacks/`.
