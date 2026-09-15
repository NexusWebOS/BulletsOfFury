# Sovereign Hard/Furious chain lightning — September 15, 2026

## Result

S4-14 is complete. The Storm Sovereign's lightning phase now has explicit Normal, Hard, and Furious profiles:

- Normal preserves the original two outer bolts, two crossing bolts, one heavy center bolt, and one center lightning ball.
- Hard doubles both side-cannon volleys to eight distinct lanes, widens their outer reach, slightly increases travel speed and size, and retains the heavy center bolt for nine total chain bolts.
- Furious keeps nine bolts, widens the outer lanes again, accelerates every release beat, and finishes the phase sooner.
- Furious launches three shootable lightning balls instead of one. They alternate left, right, left from the authored orb racks and commit from separately timed launches.
- All traveling bolts and balls use existing authored Stage 4 combat art and retain fixed post-launch vectors.

## Verification

- `node --check assets/game.js` and the CRLF suite file pass.
- Focused suite section 328: **10/10** assertions pass for Normal preservation, Hard count/width/speed, Furious timing/width, three shootable balls, alternating racks, phase exit, and projectile tagging.
- The complete suite reaches its final summary with the exact established **57 failure names** and no new failures.
- Real Chromium through `_BUILD_SOURCE/sovereign_chain_lightning_0915/probe.py`: **13 passed / 0 failed**, with zero page or console errors.
- Pixel-reviewed native frames show the nine-bolt Hard fan and three spatially distinct Furious lightning balls on natural frame timing.

Machine-readable Chromium evidence: [qa/sovereign_chain_lightning_0915.json](qa/sovereign_chain_lightning_0915.json).
