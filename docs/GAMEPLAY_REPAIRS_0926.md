# Stage 5–9 repair pass — September 26, 2026

## Implemented

- **Bottom HUD:** one shared layout anchors EQUIP in the right rail, LOCK immediately above it, and radar touching LOCK. Radar positions use the camera's world bounds. The active special draws after the rail at alpha 1, with its icon, timer, charges and pilot-specific labels inside the middle section.
- **Controller boot:** removed the startup bypass of saved button assignments. Both players' validated bindings now reload from storage. This preserves raw button numbers used by Genesis-style 8BitDo pads instead of assuming their printed A is standard XInput button 0.
- **Firewhip:** the Laser forms page exposes Fire Whip after Fire is discovered. First selection forges it once using one available combine credit; subsequent selection is free. Forging and selecting synchronize the actual weapon variant. Removed the duplicate fire entry.
- **Elemental previews:** all previews run the real level-1 firing path with isolated run, forge, special and space-mode state. Corrected orb/flame/Firewhip variant selection and level-1 icons. Capped lightning orbs are retired after leaving the preview glass, so new demonstrations continue. Their child bolts retain their launch element, and their release burst uses the matching elemental effect.
- **Missiles and retina:** exposed Stage 5 hammer and chaingun modules have stable moving lock targets. Missile context survives the space/retina damage routers and is restored afterward. A space volley can interrupt the giant dive. Existing no-lock missile damage, Stage 9 target routing and camera/turret fixes from the video review were preserved and rechecked.
- **Stage 5 animation:** eight authored front/profile/back whirlwind frames replace rotation of one flat plate. Eight orbital frames cover raised hammer, crouch, rise, tuck, descent, sweep, follow-through and recovery. Recovery scale eases back instead of snapping. New poses retain shaded blue hit feedback. The impact shock is now drawn even when a combat pose takes over rendering.
- **Chromium attacks:** eight new energy-only frames replace the stretched legacy column and flat spell pillars. Warning/damage lanes retain side escape routes. Beam damage is limited to the space below its origin. Spell targets keep their 72-pixel separation while tracking, then hold their positions for the final warning interval. Removed the random lightning scribbles over the entire screen and the forced solid-red spell pose.
- **Late-stage projectile fallback art:** 32 new frames cover blue laser, toxic laser, slime glob, black/red void needle, cyan water bolt, missile, gold tracer and chrome plasma. The late-stage fallback routes use these sheets; existing encounter-specific authored art still takes precedence.

## Art source and saved files

Generated with the built-in image tool in this conversation, not SpriteCook. RGBA files were copied into the project unchanged; there was no atlas repack.

- [Whirlwind — 8 frames](../assets/game/stage5_archmage_0916/combat_0926/whirlwind.png)
- [Orbital strike — 8 frames](../assets/game/stage5_archmage_0916/combat_0926/orbital_sweep.png)
- [Chromium beam — 8 frames](../assets/game/stage5_archmage_0916/combat_0926/chromium_beam.png)
- [Projectile families — 32 frames](../assets/game/projectiles_0926/late_campaign_flight.png)
- [Exact prompts, source filenames, XART keys and grid metadata](generated_combat_art_0926.json)

## Verification

- `node --check assets/game.js`: passed.
- Full `node _BUILD_SOURCE/test_fl.js`: **4,957 passing assertions, zero failures, exit 0**, reached its final summary. Final log: `_shots/test_fl_0926_final_verified.log`.
- Baseline comparison: the preceding video-repair build also had 4,957 passing / zero failing. This pass's first full run found two obsolete HUD source-string assertions. They now check actual joined layout geometry and all nine special icons at full opacity. No assertions were deleted.
- `probe_hud_forms_pad_0926.py`: 90 combinations (nine weapons × base plus nine elements), all level 1, all firing, no preview errors or persistent-state mutation. Saved raw fire assignment survives a page reload and fires before opening Settings, including a controller in slot 2 with earlier slots empty. This is a **synthetic Gamepad API test**, not a physical-pad test.
- `probe_late_combat_0926.py`: 15 real Chromium encounter smoke runs, 30 seconds of simulated combat each: Stages 5–9 × Normal/Hard/Furious. Captured screenshots inspected. No page/console errors. These runs cover opening boss phases, not complete fights.
- `probe_hammer_authored_0926.py`: above-beam immunity, center-lane damage, both side escapes, fixed spell spacing and final target commitment; rendered all orbital poses, beam widths for all difficulties and upward pillars. No browser errors.
- `probe_missile_turret_regressions_0926.py`: manual missile damage without a retina, distant Stage 9 volley acquisition/damage, map-anchored turret position and balanced canvas transform. No browser errors.
- `record_hammer_review_0926.py`: [23-second Chromium attack review](../_shots/hammer_authored_0926/stage5_attack_review.webm). This is an invulnerable visual-inspection fixture: the whirlwind is started explicitly and the chromium charge is queued at ten seconds. It is not an unassisted campaign playthrough.
- Line endings verified: `assets/game.js` remains LF; `_BUILD_SOURCE/test_fl.js` remains CRLF. `git -c core.whitespace=cr-at-eol diff --check` passed.

## Review captures

- [Joined HUD with an active special](../_shots/hud_forms_pad_0926/hud.png)
- [Fire weapon previews](../_shots/hud_forms_pad_0926/preview_fire.png)
- [Dark weapon previews](../_shots/hud_forms_pad_0926/preview_dark.png)
- [Orbital pose contact sheet](../_shots/hammer_authored_0926/orbital_frames.png)
- [Projectile contact sheet](../_shots/late_combat_0926/projectiles.png)
- Other difficulty/stage captures: `_shots/late_combat_0926/`.

## Remaining work and limits

- Verify the saved A assignment on Mike's actual 8BitDo wireless pad after a fresh launch. This session cannot establish its physical connection mode or driver mapping.
- Full unassisted Normal/Hard/Furious campaign and complete multi-phase boss/miniboss runs are still needed for difficulty, pacing and enjoyment. The automated checks above do not establish those.
- Stage 6 still shows crowded overlap between squadron deaths and allies; Stage 7 still has an oversized plain closed-portal seal. These need a focused encounter/art pass.
- The broader cinematic continuity/white-character complaint and full late-stage encounter polish are still open; see [the earlier video review](VIDEO_REVIEW_0926.md).
- No commit or push was made. Pre-existing tracked and untracked work was preserved.

