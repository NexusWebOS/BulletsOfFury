# Stage 2 volcanic enemy overhaul

Live-canvas GIFs were captured over the end-of-stage lava region. All projectiles use a near-black
silhouette, cyan separation edge, and white/yellow core so they remain readable over white-hot lava.
None home, flip, or reacquire the player after release.

| Enemy | Attack identity | Projectile | Counterplay | Preview |
|---|---|---|---|---|
| Ash / Ember Wasp | Sine dive with synchronized twin gun release | Needle pair | Slip between the narrow vertical lanes | [GIF](Stage2_ash_Enemy_AI.gif) |
| Magma Skimmer | One crossing pass with a three-prong belly rake | Rake bolts | Move through the fan after the fixed snapshot | [GIF](Stage2_skim_Enemy_AI.gif) |
| Eruption Eye | Long iris charge, heavy core, two fast escorts | Slag orb + needles | Read the charge, dodge the slow core, then the escorts | [GIF](Stage2_eye_Enemy_AI.gif) |
| Volcanic Mine | Rotating radial wheel with a three-round safe gap | Mine rings | Follow the rotating opening | [GIF](Stage2_disc_Enemy_AI.gif) |
| Volcanic Lancer | Nose bay opens, fires one accelerating rocket, then commits to a dive | Rocket | Break the launch line; it cannot turn afterward | [GIF](Stage2_lance_Enemy_AI.gif) |
| Crucible Bomber | Alternating physical left/right bomb racks | Heavy bomb | Cross beneath the inactive wing between drops | [GIF](Stage2_cruc_Enemy_AI.gif) |
| Magma Carrier | Bay-open sequence, deploys two Ash units, launches bracket rockets, retreats | Rocket pair | Clear the deployed pair, then occupy the bracket centre | [GIF](Stage2_carrier_Enemy_AI.gif) |
| Drill Miner | Braces, spins its drill, tears three fissures downward | Shock crescents | Stand between the widening fissure lanes | [GIF](Stage2_miner_Enemy_AI.gif) |
| Lava Maw | Large inhale tell followed by five-way furnace breath | Breath clusters | Use the long wind-up to cross outside the fan | [GIF](Stage2_lavamaw_Enemy_AI.gif) |
| Lava Crawler | Low pursuit followed by a fixed double jaw shot | Heavy slugs | Change direction after the mouth flashes | [GIF](Stage2_crawl_Enemy_AI.gif) |
| Eruption Pod | Petals open and emit a radial bloom with a safe gate | Mine rings | Enter the deliberately missing three-round wedge | [GIF](Stage2_pod_Enemy_AI.gif) |
| Magma Golem | Full-body fist raise and slam with an open centre lane | Shock crescents | Hold the centre through the split shockwave | [GIF](Stage2_golem_Enemy_AI.gif) |

Each enemy also owns a normalized eight-frame action reel under
`assets/game/stage2_enemy_attacks/<enemy>/01.png..08.png`.
