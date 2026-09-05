# Stage 3 native ice-fleet AI previews

These GIFs are direct recordings of the production game canvas. The capture disables the normal
wave director and story panel so each reel shows one live enemy, its authored movement, its action
animation, its measured muzzle hardpoint, and the projectile family that the player will face.

| Unit | Arcade role | Preview |
|---|---|---|
| Shard Mine | Opens and casts a 12-way shard crown with a three-slot player-facing escape gate. | [GIF](Stage3_s3mine_Enemy_AI.gif) |
| Elite Ice Interceptor | Completes one readable circle, tells with its engines, then commits to a silent body ram. | [GIF](Stage3_s3interceptor_Enemy_AI.gif) |
| AA Sled | Fires from both visible barrels, then places the smaller center lance a beat later. | [GIF](Stage3_s3sled_Enemy_AI.gif) |
| Snowmobile Gunner | Makes one fast lateral pass and lays a short three-tracer burst; it never loops or homes. | [GIF](Stage3_s3snowmobile_Enemy_AI.gif) |
| Ice Crawler | Pursues slowly, plants its claws, and lobs a fixed three-shell mortar fan. | [GIF](Stage3_s3crawler_Enemy_AI.gif) |
| Snow Tank | Terrain-bound heavy cannon with one accelerating shell and two slower crystal escorts. | [GIF](Stage3_s3tank_Enemy_AI.gif) |
| Cryo Barge | Alternating six-round brackets pressure both sides while deliberately leaving the center open. | [GIF](Stage3_s3barge_Enemy_AI.gif) |
| Tracked Frost Artillery | Long cannon tell followed by a fixed three-lane accelerating mortar barrage. | [GIF](Stage3_s3artillery_Enemy_AI.gif) |
| Frostbite | Arsenal mini cycles a fast lance, shard fan, and slower mortar deployment from its animated center emitter. | [GIF](Stage3_Frostbite_Arsenal_Mini_AI.gif) |
| Rime Wall | Miniboss changes from dark-edged mortar spirals to broad cryo-wave columns at low health. | [GIF](Stage3_Rime_Wall_Miniboss_AI.gif) |
| Cryo Spear | Main boss progresses through lance lanes, shard rime, charge waves, and a final three-emitter beam fan. | [GIF](Stage3_Cryo_Spear_Boss_AI.gif) |

Projectile readability is shared across the fleet and all three boss tiers: a dark navy silhouette and violet edge separate
the ordnance from the bright ice, while a white/gold core makes its center and velocity readable.
Accelerating rounds preserve their launch heading and never mirror, home, or flip after release.

Each unit also owns eight action frames, eight damaged frames with moving smoke, and eight critical
frames with moving fire. Those damage reels remain fully opaque; enemies finish by entering their
explosion animation instead of fading out.
