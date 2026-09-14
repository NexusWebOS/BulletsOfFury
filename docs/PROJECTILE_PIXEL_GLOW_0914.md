# Stable projectile sprites and pixel glow — 0914

Mike identified the diagonal purple Stage-5 projectiles and asked for a static frame animated through pixel glow, with the same treatment for Stage-2 lava saw blades.

The native XART sheet inspection confirmed that `cfx_stage5_alien_projectiles_v2` contains progressively larger charge/size variants, not an onion-aligned animation reel. All seven Stage-5 projectile rows now retain column 1 (the second cell) throughout flight. This covers the screenshot's `s5fracture` diagonal spears and `s5null` thin lances as well as split, prism, missile, chaos and halo rounds.

Stage 2 already used column 1 through `stage2FlightFrame`; its `s2slag` and `s2mine` saws remain on that stable authored sprite. Fixed-frame Stage-2 and Stage-5 shots now use four discrete brightness levels and a hard-edged six-pixel light band at 12 ticks/sec. Both lighting passes reuse the same source cell. No blur, new sprite, size animation, projectile speed, collision, damage or trajectory changes. Existing spin remains on radial/saw families; directional projectiles retain velocity alignment. The glow uses projectile simulation age, not wall-clock time.

Real Chromium loaded the actual game and XART sheets using `_BUILD_SOURCE/shoot.py`'s frame trap and the existing capture clock. The focused probe checks nine relevant projectile types across eight ages: each uses one source cell and constant dimensions, with visible pixel-light changes. All 19 native checks passed, with no page/console/game-loop errors. The source sheets, glow comparison, Stage-5 firing scene and Stage-2 saw screenshot were visually inspected. The six-second MP4 uses the actual PLAY loop and scripted shot spawns, with capture-only invincibility; it is silent and fully decodes. This does not certify full-stage encounter balance.

Sources: `_BUILD_SOURCE/projectile_glow_0914/`. Native output and preview: `_shots/projectile_glow_0914/`. Final verification record: `qa/projectile_glow_0914.json`. No atlas or test-file edits. Existing staged/unstaged work is preserved; no commit or push.

Final full suite: **3853 passed / 57 inherited failures, exit 1**. Final summary reached; no new failure names relative to the immediately preceding dialogue/hazards baseline. Syntax check exited 0.
