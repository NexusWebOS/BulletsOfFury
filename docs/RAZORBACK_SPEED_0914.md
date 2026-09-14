# Razorback speed tuning — 0914

S1-04 is implemented. Razorback cruise and ram movement are 30% faster, hull turning is 20% faster, and the approach slowdown scales with travel speed. Machine-gun and sonic-shot launch speeds are 20% faster. Missile launch, acceleration and speed cap are also increased by 20%. Sonic Hammer and Resonance Nova pressure rings expand 25% faster.

The 1.2-second Sonic Hammer charge, 1.55-second Nova charge, missile queue spacing, attack order, recovery times, hit sizes, part HP pools, authored rig and sound routes are unchanged. This is the requested baseline tuning; Hard double-Razorback and Furious tank variants remain separate pending work.

## Verification

`_BUILD_SOURCE/razorback_speed_0914/probe.py` boots the real game with shoot's RAF trap and the established capture clock. Twelve native checks pass: actual movement distance, projectile launch speeds, pressure-wave radius through the update loop, preserved warning/release counts, player-hit routing, keyboard sidestep after release, accelerating shootable missiles, sound routes, pressure art and zero page/console/game-loop errors.

Staying in the sonic lane reaches the player-hit callback; a normal keyboard sidestep after release moves outside the faster fan and wave without reaching it. Hit callbacks are counted for this comparison rather than spending lives. This proves a concrete escape route, not balance across every pilot/difficulty or encounter phase.

The real-game screenshots of moving gunfire, full sonic charge, release and sidestep were visually inspected. Silent recordings are `_shots/razorback_speed_0914/Razorback_Faster_Guns_0914.mp4` (6 seconds) and `Razorback_Sonic_Dodge_0914.mp4` (3 seconds). Both decode successfully. Captures use debug fight selection, controlled attack phases and capture-only damage interception.

Syntax passed. Full suite: 3,852 passing assertions / 58 inherited failures; final summary reached, exit 1. No new names against recorded baselines. Proof: `qa/razorback_speed_0914.json`. No atlas, test-harness or source-art edits. No commit or push.
