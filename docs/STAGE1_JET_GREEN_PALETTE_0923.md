# Stage 1 jet green palette — 2026-09-23

The four authored Stage 1 jet variants now recolor their red paint and cockpit accents at draw time. Black-hull variants use neon green; silver/light-hull variants use forest green. The mask retains the source's luminance and alpha, so hull detail and silhouettes remain intact. Projectile art and boat variants are unchanged. Recolored canvases are cached per flight frame.

`_BUILD_SOURCE/probe_stage1_jet_green_0923.py` verified all four variants in Chromium and captured `_shots/stage1_jet_palette_0923/four_jets.png`; there were no page or console errors. The full suite before the symbiote work reached its final summary with 80 baseline failing assertions and no new assertion names relative to the previous 81-failure run.
