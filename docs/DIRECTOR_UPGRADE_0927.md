# September 27 director upgrade

Mike requested distinct muzzle flashes throughout the game, sustained destruction effects for modular parts, a red/black Furious Tempest and animated thrusters within every pilot's ship. This pass implements those systems locally. No commit or push; the older overnight automation remains paused.

## Muzzle art and routing

Four new transparent sheets provide **16 families, six frames each (96 frames)**: machine gun, chaingun, spreadfire, shotgun, fire, ice, lightning, toxic, laser, orb, sonic, void, missile ignition, roller, helix and exhaust. Built-in image generation only. The originals retain their actual RGBA; measured ignition-root anchors keep the effect attached to its barrel instead of centered over it.

The shared release path covers primary guns, manual/auto missiles, space weapons, enemy shots, boss mounts and naval emitters. Explicit draw routes cover fire/ice breath, infused held beams, Decker's shotgun, Yuri's lightning, Falva's charge/release, Maverick's laser charge and helix tap, Razorback, Furnace, Hammer and the Harrier missile/plasma/laser mounts. The bomber charge also uses the new laser reel. Stage 7's machine-gun barrels now use a ballistic flare while its toxic attacks retain toxic effects. Rival allies use the same muzzle drawing rather than a projectile sprite.

Source prompts: `docs/director_prompts_0927.json`. Owning build: `_BUILD_SOURCE/build_director_art_0927.py`. Measured metadata: `assets/director_art_0927.js` and `docs/director_art_0927.json`. Runtime: `assets/combat_director_0927.js`; sheet keys `d27_ballistic`, `d27_elemental`, `d27_energy`, `d27_specialist` are registered in the art taxonomy. Existing art is preserved.

## Modular destruction

Broken parts now schedule **12 or 18 staggered explosions** across roughly one to one-and-a-half seconds, using the engine's existing dense, barrage, radial and cluster explosion reels. The burst follows its owner's hardpoint, includes smoke and restrained impact shakes, and spreads sound transients rather than playing every explosion at full volume simultaneously.

Hooks cover the new modular roster and helpers, space/Earth bombers, toxic walker legs/turrets, Furnace parts, Hammer modules, Warhive, carrier bays/nodes, Xeno Regent, modular boats, Vile and legacy mech parts. Each part can trigger once; overlapping module queues cap at 144 and are discarded on stage changes. These cosmetic cascades do not add hidden player damage.

## Furious Tempest

Stage 5's space bomber becomes **Tempest Crimson Eclipse** on Furious: dark armor with red energy, quicker lateral passes and vertical bobbing, shorter charge/recovery beats, faster bomb cycles and paired missile lanes. Its five-lane bomb sequence skips one lane per phase. Warning timing remains readable; the laser charge lasts 1.65 seconds, compared with Hard's 2.7 seconds. Destroying engines reduces movement, and breaking a charging cannon interrupts its attack. Normal and Hard retain their existing behavior and palettes; Stage 6's Earth bomber does not inherit the Furious space behavior.

## Pilot thrusters

All nine pilots use six animated heat pulses within the exhaust already painted into their authored ship plates. The mask is measured from their existing glow variants. Idle, banking and supported perspective poses animate without moving the hull or adding a second star-shaped plume. Rapid roll poses keep their authored frames.

Native pixel comparisons find six distinct frames per pilot, **zero changed pixels outside the exhaust mask and zero alpha changes**. Generated exhaust also runs at the modular space bomber's engine outlets.

## Verification

- Incoming suite: **5,432 assertions / zero failures**. Final: **5,479 assertions / zero failures**, final success banner and exit 0. No failing names in either run. Runtime syntax passes; game.js LF and test files CRLF are preserved.
- Native Chromium: all 96 effect frames render; all nine pilot animations pass the pixel checks. Normal/Hard/Furious space Tempest each runs 35 simulated seconds with finite projectiles and zoom 1. Furious travels about four times Hard's lateral distance in that fixture; this is an aggression measurement, not a balance rating.
- The large-module check schedules 18 explosions, rejects duplicate retriggers, follows the owner, and drains completely. Four module breaks are staged in the destruction recording.
- Actual input/renderer checks observe Maverick's laser charge and helix tap, Falva roller, Decker shotgun, Freezer ice, Yuri lightning and ordinary fire. The first special probe held Maverick's trigger without tapping and correctly observed only the charge family; adding an actual short tap verifies the helix route too.
- Seven native clips total **145 nominal seconds**, including two silent animation galleries. Other clips capture real SFX with music muted. The special audition uses 65% SFX volume and 0.4 capture-only gain to leave headroom. Unattenuated special captures exceeded unity (peaks 1.112 and 1.776); the latter included the helix tap. Full-volume special mixing remains a separate audio follow-up. The recording adjustment does not change the game mixer or remaster those existing sounds.
- All native page and console error lists are empty. The review checks every video, poster and link.

Review: `http://127.0.0.1:8794/_shots/director_0927/review.html`. Durable evidence: `docs/qa/director_upgrade_0927.json`. Reproduce with the `probe_director`, `review_director`, `director_specials`, `build_director_review` and `check_director_review` scripts under `_BUILD_SOURCE/`.

These are selected encounters, controlled module breaks and weapon demonstrations. They are not uninterrupted campaign wins, physical-controller tests or certification that every difficulty is finally balanced. The previous campaign/hardware follow-ups remain open.
