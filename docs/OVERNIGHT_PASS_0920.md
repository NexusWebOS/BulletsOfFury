# Overnight development pass — 2026-09-20

This pass addresses Mike's latest Stage 2, 5, 6, and 7 requests. It is uncommitted and unpushed. Stage 8 boss work is reserved for Mike's separate design session.

## Implemented

- Stage 2 Furnace Tyrant core laser uses new transparent pixel art at `assets/game/bosses/furnace/fzt_fire_laser_0920.png`. The core beam keeps the encounter's existing hit geometry and timing. Eye beams retain their separate art. The rectangular shield bar now draws both frame and fill at their source aspect ratios instead of stretching either vertically.
- Stage 5 warp gates derive their position from the same background scroll as the starfield. They no longer travel on an independent timer. The background keeps moving through the route.
- Stage 5 Chrome Hammer Archmage has three new authored stun poses at `assets/game/stage5_archmage_0916/stun_0920.png`. Five distinct player missiles within 1.2 seconds during the hammer windup interrupt the throw. The hammer drops as a targetable object; the boss throws up his arms, kneels, pulls it back magnetically, and recovers. Its module gauge follows the dropped hammer. Every third leap has a stronger upward arc, shadow, landing shock, and slightly longer tell.
- Stage 6 starts with two black Tempest fighters climbing from behind the player. Each puts an independent Retina lock on the player and releases a shootable missile. Their launch invokes the existing SHOOT! art and a brief slow-motion interception window. Both rounds can be selected with Retina and destroyed with manual missiles or the primary weapon. An unanswered attack consumes a life. Regular waves wait until the opener resolves.
- Stage 7 Toxic Portal Warden's hyper rotation now adds a warned 20-round toxic chaingun burst and a warned leg-strike leap. The leap moves the authored boss plate, lands with an impact, spreads five toxic shells, and retreats to its normal patrol. The chaingun now uses a dedicated casing-and-green-tip plate cropped from existing projectile art; the full Stage 7 natural-play balance review remains open.

## Verification

`node --check assets/game.js` and `git diff --check -- assets/game.js` passed. The full `_BUILD_SOURCE/test_fl.js` reached its final summary with **75 failures** on the first run and **76 failures** on the final run (nonzero exit both times). The recorded baseline had 76; comparing assertion names shows **no new failing names**. The intermittent extra failure is the existing Stage-1 sand-tank spawn fixture. These legacy failures still require separate triage.

Real Chromium probes through `_BUILD_SOURCE/shoot.py` passed: first-pass Furnace/gate checks 5/5; Stage 5 hammer stun and heavy leap 6/6; Stage 6 opener including Retina interception and loss-of-life path 10/10; Stage 7 new attacks 5/5. No page or console errors were reported. Screenshots and logs are under `_shots/qa_0920_overnight/`.

## Next work

The focused Forge reward, two-combine, loadout, death and save routes are now checked in Chromium; broader natural-play combinations remain. Stage 3 Furious has a blue-palette version of the Furnace beam, and the Stage-7 chaingun has a dedicated toxic bullet plate. Stage 1 Campaign clear now has one two-ship flight bridge; later transitions and cockpit/POV beats remain. Stage 5–7 natural playthroughs still need difficulty and visual tuning with Mike; leave the Stage 8 boss untouched. Details and evidence are in `FORGE_REWARD_AUDIT_0920.md`, `FROST_FURIOUS_BEAM_0920.md`, `STAGE7_MACHINE_ROUND_0920.md`, and `CAMPAIGN_BRIDGE_0920.md`.
