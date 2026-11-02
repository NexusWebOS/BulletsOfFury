# Voss twin blasters and overhead turbo — October28

Mike replaced the charging sphere with 1015 outer/inner power and requested matching jet-color twin defensive-blaster rounds from the top, followed by safe south/north turbo flight with turning, scaling and shadows.

`assets/voss_turbo_1028.js` owns Voss's personal cycle after the existing rebel owners. Position at the top,1.35s paired-cannon warning, five pairs at0.30s,1.60s own-pixel turbo charge, two south/north cycles on Easy/Normal or three on Hard/Furious, then native recovery/cooldown. Turns are continuous35-unit U-curves below/above the screen; no offscreen teleport. Native health/module pools, damage/white flash, Retina, missile formations, defensive clears and final defeat remain.

`build_voss_turbo_1028.py` owns fixed192x192 whole-ship plates, common96,96 pivot, one1.15 proportional unit, own-mask outer/inner light and exact-alpha shadow/hit companions. The original72 RR33 frames are unchanged; eight south boost cells reverse the existing north boost at the same pivot. All flight uses authored headings/boost frames, never live static-image rotation. Actual wing mouths66,106 and126,106 own both FOVs, round release and muzzle effects. Native florb frames exported through XART are palette-swapped into eight fixed128 cells; alpha and Rec.709 luminance are preserved, with the white-hot core/outline structure retained. Native heavy-round2HP/damage/flash/destruction remain; ordinary enemy-bullet rules are unchanged.

The old center sphere/auxiliary frCast and ordinary Voss gun route are superseded. Outer silhouette light and inner emissive pixels power the charge; there is no charging ball. New attacks use shared bossWeaponCharge, enemyBossCannon, chargeDash and jetDash cues through retrigger gates. Broken cannons cancel their own release/rounds; native death cancels the new controller. No pending audio callbacks are scheduled.

High flight has no player/allied ram damage. Its ground shadow draws in the native boss pass; the elevated hull draws after players/allies and uses the same pose/pivot/scale. Shadow depth approaches smoothly on recovery. Only the explicit high Voss pass can fly over the central wall; players and ordinary ships retain the original physical wall block, as does Voss after recovery.

Verification: 19 native controller/render checks,8 export/rebuild checks and35 existing Jace/team regression checks pass. The two existing Voss regression time bounds increase450→1200 ticks to cover the requested longer finite sequence; other expectations remain. Actual native cannon pixels, outer/inner charge without a sphere, both FOV origins, orb damage, continuous turning, foreground/shadow order, multi-seat/allied harmless contact, wall clearance and real white hit pixels/expiry are verified.

Current focused native Furious film: 15.24s, 59.46fps, decoded peak-14.8dB, all11 recording checks pass, no game/browser/asset errors. Attack selected once in the native Stage6 scene with a labelled invulnerable observer, other special selections and allied autofire held for clarity; no Voss HP/phase/timer writes after selection. Source `_shots/voss_turbo_1028/video/141228/voss-turbo.mp4`. Replay `docs/previews/voss_turbo_1028/index.html`; evidence `docs/qa/voss_turbo_1028.json`.

Replay verification: all8 Chromium playback/layout checks pass, including every chapter seek, decoded stills and desktop/mobile fit. No video or browser errors.

Syntax passes. Required full suite exits1 before summary on the existing missing UNUSED_ASSETS/retired_art_1022/manifest.json, so no assertion comparison is available. No game.js/test_fl.js edits, commit or push.
