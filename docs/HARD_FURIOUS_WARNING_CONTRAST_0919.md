# Hard/Furious warning contrast — 2026-09-19

At the final red phase, the existing authored FOV cone and alert symbol now receive a narrow cool-cyan edge on Hard and Furious. Their red interiors, three-stage timing, footprint and collision remain unchanged. This creates a different value/hue boundary from the warm Furious projectiles and white/orange explosions. Normal and Easy retain the original rendering.

Focused Chromium check captured a Furious Razorback charge warning over its red hull with a projectile and nearby explosion. The authored FOV and alert assets decoded and rendered; there were no page errors. Screenshot: `C:\Users\Mike\Documents\New project\furious_readability_shots\furious_warning_overlap.png`. `node --check assets/game.js` passed. The full legacy suite repeated with 77 failures versus the prior 76-failure baseline; the sole extra assertion is the previously intermittent Stage 1 sand-tank spawn. An unrelated Maverick lance assertion appeared on the first pass and passed on the repeat.

Status: partial. Other Hard/Furious hazard families and multiple overlapping explosions still need a continuous playtest before claiming whole-game readability.
