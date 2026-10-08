# Windstorm, the Machinists, and ally infiltration

Art and proposed systems for Bullets of Fury — Overdrive, 7 October 2026. This package adds graphics, review tools, and asset metadata. Gameplay has not been implemented.

## Niel — Windstorm

Niel is a Hispanic Italian man in his mid-30s: eccentric, composed, sophisticated, with slicked-back dark hair over a faded undercut and a groomed beard. His pearl-white, sea-green, charcoal, and antique-gold kit uses a spiral insignia. The user approved this design; it is retained unchanged.

His proposed ship name is **Sirocco**, an interceptor with two ducted wind turbines. The pack supplies idle, bank candidates, damage art, portraits, front/full-body poses, HUD avatar, and the Windstorm special icon and pickup box. Bank poses are art variants; do not treat them as a seamless animation without comparing their geometry.

**Windstorm** releases repeated three-funnel volleys. Use the single-tornado sequence for individual projectile entities; the three-tornado image is a formation preview or a single composite effect. Each volley has center/left/right launch offsets, heading, phase offset, lifetime, hit cooldown, and collision radius defined in data. The charge and impact strips are separate. Suggested behavior: gently diverging funnels sweep a broad lane, with a light pull on small enemies and resistance on heavy units. Pull strength, volley count, ammo/charge cost, damage, cooldown, and whether hostile projectiles are deflected remain balance decisions. Avoid applying damage every render frame or using translucent swirls as exact collision geometry. Anchor the funnel at its ground tip and author a clear cast/release event.

## The Machinists

The Machinists are the newly requested rebel tank squad. Their role does not reclassify Hotwire and Phoenix as rebels; those two keep their established independent motivations.

The selected **v2 designs** follow the user's request for less anime styling. Wren is a rugged industrial android, Rolf a weathered red-jacketed tanker with short dark hair, and Chaz a scruffy blond mechanic with orange equipment and goggles. Wren's android role, Rolf's red/cream/navy palette, and Chaz's orange/blond palette provide loose Phantasy Star III, II, and IV nods. Portraits, proportions, workwear, and weapons now follow the grounded Overdrive style. The rejected v1 sheet is retained as a source archive and is not used by the preview.

| Crew | Tank | Primary attack | Special proposal |
| --- | --- | --- | --- |
| Wren | **Foundry** | Alternating or simultaneous twin autocannon slugs; heat-limited suppression | **Bastion:** deploy a red-orange electromagnetic barrier around the vehicle; breaks or expires visibly |
| Rolf | **Vector** | Focused rail-cannon shot with clear charge/impact | **Vector Splitter:** fire three diverging lances to sweep multiple lanes |
| Chaz | **Redline** | Breach cannon with paired rocket pods | **Redline Breach:** short engine boost followed by a frontal pressure burst; collision and cancel rules need design |

Their abilities are original proposals for this expansion, not imported Phantasy Star combat mechanics. All tank names and balance details can be changed independently of art IDs.

### Actual module contract

Each tank has a bare central hull, separate left and right track pods, separate rotating turret, rear special module, damaged hull, wreck, and assembled concept. The package also supplies **assembled PNGs built from the exported parts** and transparent 256×256 layer canvases with the common pivot `(128,151)`. These are not just flattened concept pictures labeled modular. The original concept and reconstructed assembly may differ slightly because generated component shapes vary.

The renderer should compose left track → right track → hull → special module → turret. Hull heading and turret heading are independent. Tracks and the special module follow the hull transform; turret rotation uses the common turret socket. Barrel recoil should translate the normal turret temporarily along the aim vector. Use the muzzle sockets as initial calibration, with twin-barrel offsets for Wren and rocket pod offsets for Chaz. Do not scale every part independently at runtime. The prepared layer canvases already share their assembly geometry.

Six motion phases now exist for each left/right track, with calibrated 256×256 layers sharing the original assembly placement. The viewer demonstrates forward, reverse and pivot turns. For gameplay, advance each track phase by its signed travel distance; reverse the sequence for negative travel. A pivot turn drives opposite tracks in opposite directions. A stationary vehicle holds its phase. This avoids tracks cycling while the hull is stopped. Generated housing details and the final-to-first seam still need pixel cleanup. Track damage, detached debris, rotation-dependent lighting, exact turret collision, footprint size, and weapon sockets remain integration work. Damaged hull is a state swap. Wreck is a separate complete object. Collision is authored from the visible chassis footprint, never from the 256-pixel canvas.

## Phoenix and Hotwire as top-down allies

Both allies retain helmets. Phoenix uses ember-red/black/gold armor and his phoenix emblem; Hotwire uses charcoal/copper armor with cyan cables. Their new sheets include directional stance candidates, three-frame runs, crouch and prone poses, wall taps, door interaction, cover lean, crawl, aim/recoil, medkit use, and hand signals. A separate north-facing correction strip supplies explicit back-view idle/run art. The original north candidates remain marked as drafts and are excluded from normal preview selection.

The completion pass adds dedicated grenade throws, six-pose roll-to-prone and roll-to-stand, hit/stun, death, revive, powerup, assist-heal, duck-to-prone and recovery art for both allies. Six-pose north/south rifle cycles use fixed cell anchors so a larger muzzle flash does not shift the body. Hotwire's generated roll-to-stand row was primarily a get-up: the manifest instead uses the shoulder-roll entry from her roll-to-prone row followed by the standing exit. Phoenix's duck transition takes its final fully prone frame from the following recovery row. Source sheets remain intact and these selections are explicit in the manifest.

Animation events are proposals for later binding. Grenade release is frame 4 (zero-based index 3); consume inventory and spawn the projectile once at that event, with a separate hand/launch socket and ballistic arc. Stationary north/south rifle cycles fire at frames 2 and 4 (indices 1 and 3). Damage comes from the weapon system, not from whether a flash sprite is visible. Ally grenade AI must check blast clearance and friendly positions before committing. Powerup collection and healing also need exactly-once commit events.

Rolls require entry/exit states, a movement path, collision sweeps and an explicit decision about invulnerability. The last roll frame commits either prone or standing; input cannot silently choose a different exit after that event. Crawling begins only after the prone transition ends. Aim-lock preserves the actor's position while allowing target selection; run-and-gun uses movement and aim separately. Hit, stun, death and revive need interruption priorities. Death holds its final pose until removal or an authorized revive; revive returns to a valid unoccupied position and restores only the resources specified by the chosen mode. A looping art viewer does not imply death/revive loops in gameplay.

Later ally logic should support follow, hold position, take cover, focus target, interact, heal/support, and regroup. Reserve cover anchors so allies do not occupy the player's spot or push the player into visibility. They need pathfinding with formation offsets, door clearance, independent aim heading, fire discipline, friendly-fire rules, and explicit awareness of whether the player is sneaking. A hand signal can issue a silent command; shouting or gunfire should create noise. Do not automatically break stealth because an ally can see a distant enemy.

Phoenix's combat support and Hotwire's technical support can be defined through their existing identities: Phoenix provides covering fire; Hotwire handles powered doors and equipment. These are role proposals, not hard-coded features in this package. Their special ship abilities are not automatically copied to handheld weapons.

## Shared player interactions

Four new interaction sheets preserve the existing helmet/palette approach: regular male, heavy, athletic male, and female. Each adds three-frame candidates for east and north wall taps, east and north door operation, high-wall lean, low-crate peek, heal/medkit use, and a tossed-casing noise distraction. The prior on-foot package supplies aim, run-and-gun, crouch/prone transition, crawl, grenade throw, roll exits, hit/stun, recovery, death, revive, and powerup graphics. Use the manifests together rather than regenerating every pilot's entire body set.

Niel uses the regular family. Wren can use heavy, Rolf regular, and Chaz regular for shared on-foot silhouettes if later needed. Their detailed tank-crew portraits do not require four new infantry skeletons. Preview palette filtering is approximate; final paint masks must preserve visors, neutral metal, skin, medkits, and FX.

### Cover, doors, and noise

Define cover anchors with position, normal, height, allowed stance, peek side, and reservation owner. Align the body against the cover normal and keep its gameplay root stable during lean/peek. Tall crates and walls block sight and bullets according to height; low cover is stance dependent. Background artwork is not a collision source. Draw the actor behind cover with authored depth/occlusion masks.

Wall tap has one impact event at the hand-contact frame. It creates a hearing event at the actual wall position, not the player's target or the enemy's location. A tossed casing creates a landing noise at the casing's final location. Sound events need category, intensity/radius, lifetime, obstruction/attenuation, owner, and whether they can escalate squad alarms. Sound-ring sprites are UI cues, not damaging blasts.

Door states are locked, unlocked/closed, opening/ajar, open, and optionally blocked. Set collision and sight occlusion at the correct opening event. Hand-to-handle sockets and hinge geometry require alignment. Decide whether the player can quietly open, force, tap, or hack a door; a failed locked-door attempt should not silently open it. Include interruption and re-entry behavior if an actor is attacked while operating the door.

Enemies hearing a tap turn toward or investigate the sound source; they do not receive perfect knowledge of the player. Perception uses clipped FOV plus ray-tested visibility, suspicion accumulation/decay, last-known position, hearing events, and patrol/investigate/alert/search/return states. The existing green/amber/red FOV art in `../onfoot/stealth/` can be reused. Prone reduces exposure where appropriate; it is not unconditional invisibility. Aim and firing can remain stationary while movement input is locked, and firing from cover needs muzzle obstruction checks to avoid shooting through the wall.

### Healing and the established lethal-hit rule

The request now includes heal graphics, so medkits, application poses, and healing pulses are supplied for players and allies. The previously requested normal on-foot player rule is still one damaging hit = death. These graphics do not silently introduce a player health bar. Use healing for allies with health, scripted recovery, or a separately chosen player mode with health; choose that rule explicitly during implementation. A medkit animation cannot revive a dead actor unless a revive rule authorizes it. Consume a kit on its committed use event and specify cancellation/refund behavior.

## Art readiness and next integration checks

The manifest records source bounds, canvases, provisional pivots, checksums, sequences, and modular tank placements. Original RGBA sources are preserved. Crops remove empty/very faint outer margins while retaining the pixels inside their recorded bounds. The portraits intentionally fill framed image borders; sprite canvases have clear margins.

These are generated motion candidates. Three-frame movements can have silhouette, gait, hand, and weapon drift. Stabilize roots and sockets, inspect onion skins at engine resolution, and expand missing south/west interaction poses as needed. West mirror is a useful candidate but may reverse badges and handedness. Door art is a standing doorway kit; map orientation and collision need authoring. The Windstorm and tank effect sequences should use gameplay-defined timing instead of letting image phase determine damage.

One low-alpha connection between tank shield/rail effect cells is recorded by the extraction checks; separated output frames were visually inspected. Technical checks verify nonempty PNGs, dimensions, transparent margins for sprite exports, and sequence references. They do not certify motion quality or gameplay correctness.

## Reference research

- [SEGA Phantasy Star II manual](https://www.sega.jp/mdmini2/en/assets/manual/pdf/EU_Phantasy-Star-II.pdf)
- [SEGA Phantasy Star IV manual](https://manuals.sega.com/genesismini/pdf/PHANTASY_STAR_IV.pdf)
- [Phantasy Star III Wren character reference](https://phantasystar.fandom.com/wiki/Wren_%28Phantasy_Star_III%29)

These references established the requested character associations. The selected redesign prioritizes the user's later grounded-style correction. Complete prompts and generation provenance are in `generation.json` and `completion-generation.json`; `prompts.json` is an older snapshot.

## Directional and enemy continuation — 7 October 2026

The [second art pass](PASS_2.md) adds four-direction crouch locomotion and prone firing for six actors, west runs and two alien biped patrol sets. Selected north enemy animation uses corrected rear views. New exports use fixed source-cell anchors; source body drift still needs cleanup. Separate movement heading, aim heading and stance in the engine; trigger weapon and hearing events independently of sprite bounds.

Each enemy now has an east hit-to-destruction strip. An ordinary hit on a beefy enemy must return to combat after its nonlethal reaction; only zero health commits the death segment and wreck state. All four patrol headings have motion, but directed attack poses beyond east are still needed. Match weapon sockets before wiring projectiles, and keep sound investigation separate from visual confirmation.

Wren, Rolf and Chaz now use canonical 256-square portrait frames, 112-square hex badges and 360×400 pickup canvases. Use consistent ability IDs for Bastion, Vector Splitter and Redline Breach across tank modules, pickup behavior and HUD display. No gameplay code is registered by this art pass.
