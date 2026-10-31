# Kaia faster four-edge rollers — 2026-10-29

Stage 6 Rough Riders Kaia now releases her existing ten-round roller burst every .14s instead of .20s (43% higher release rate). Travel speeds are 235/260/280/300px per second on Easy/Normal/Hard/Furious, about one third faster than 175/195/210/225.

Each roller ricochets at the left, right, top and bottom of the current viewport. Edge insets contain the complete 48px authored roller cell. Overshoot is reflected, including simultaneous corner impacts, keeping speed and remaining travel continuous. The moving camera cannot leave a ball outside its visible edge. Native ordnance still owns its 16px collision radius, three HP, four-second lifetime, weapon collision, gold-shield reflection and owner-defeat cleanup. The existing animated teal roller art, attack windup, ten-shot count and recovery remain.

The changes are scoped to Stage 6 Kaia's five-ship Rough Riders encounter. Stage X, Voss's parallel orb rows, other projectiles and Kaia's noncombat intro demonstration retain their prior owners. The native launcher marks only those rollers; native ordnance invokes the new movement for that marker. No second projectile loop or duplicate collision owner.

15 native checks pass, covering release cadence/count and speed at all four difficulties, every wall and corner at 144/60/20fps, overshoot, multiple same-step rebounds, viewport movement, lifetime, native weapon damage, owner defeat and Stage X exclusion. No native page errors.

Required syntax checks pass. Full suite completes with the same five baseline failures, exit 1: single-hit flash duration; opening-jump warning dialogue; opening jump return before Chromium; opposite Stage X route persistence; Stage X right full encounter. assets/game.js and _BUILD_SOURCE/test_fl.js are unchanged.

Fresh 301.03s complete native Furious fight at 59.23fps contains the actual ten-shot roller burst, repeated native rebounds and 118 sampled live roller positions inside the viewport. Audio mean -18.8dB, peak -3.0dB. Player control only: native GOD and real inputs; weapons withheld for 240s to allow the existing squad schedule to reach Kaia, then native defeat. No enemy HP, phase or timer writes. The first shorter recording ended before her attack and was preserved without publishing.

34 film/player checks pass. One additional long-run fighter-spacing check fails: a brief Kaia/Jace conservative-footprint overlap of 13.60px (including reserved margins), first present before Kaia fires. No flight/spacing code was changed here; this observation is retained in the report for a separate airspace pass. Do not describe the long film as a clean spacing pass. Prior Nyx concealment/turret origins, gold shield, correct music, steady camera, real defeat and roller speed/bounds remain verified.

Full fight and all related local chapters now use the new movie. The Kaia chapter starts immediately before her actual burst: http://127.0.0.1:51046/?riders=kaia-ricochet-1029#clip=rough-riders-kaia . Prior media is retained. Evidence: C:/Users/Mike/Documents/New project/BOF-Kaia-Ricochet-1029/. No commit or GitHub upload.
