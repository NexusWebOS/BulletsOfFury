# Stage 8 final boss patterns (September 25)

The four physical shells remain on the existing three-part music arc. The last shell is the final music phase. All eight new plates live in `assets/game/final_boss_0925_patterns/` and are lazily registered by `assets/game.js`.

- **Possessed shell:** Alternating hyper-cannon beams, a sweeping cannon pass, and shootable shadow interceptors join its rockets and orbs. The cannon arms are separate authored art. Each beam has a charge tell, a muzzle flash, a bounded active window, and recovery.
- **Ascendant/sealed shells:** Eclipse draws the pilot gently toward an orb ring, leaves an aimed escape sector, then fires a delayed laser.
- **Final shell, ghost prison:** Two one-third-screen authored walls close from the visible side edges with back rails. They push and constrain instead of damaging. A forward dash provokes an earlier claw strike, which is telegraphed; somersault avoids contact but cannot cross the walls.
- **Final shell, phantom:** Marked ground portals precede fast skull emergence. The visual burst is harmless; contact starts the existing dark-void ship-eradication animation.
- **Final shell, knight:** Marked sword leaps use an authored sword and shield body and a separate slash plate. There are two, three, or four leaps on Normal, Hard, or Furious.
- **Final shell, duplicate dimension:** A ball/portal transformation makes four shootable positions. Fake hits enrage and charge. Damaging the real copy by 7.5% of that shell's pool detonates the fakes and starts a bouncing ball with radial void orbs. The real copy is fully opaque; fakes are slightly translucent.

The attack rotation remains deterministic within each difficulty so players can learn the tells. Existing shield, module, form-transition, and death pipelines remain in place.
