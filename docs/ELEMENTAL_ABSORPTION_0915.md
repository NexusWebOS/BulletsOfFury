# Shared elemental absorption — September 15, 2026

Fire-aligned enemies, minibosses and bosses now retain half damage from player
fire attacks. Ice-aligned targets do the same for ice attacks. The rule runs at
the three shared damage boundaries, so flame ticks, orbs, projectiles, targetable
parts and ordinary hull hits cannot drift into separate behavior.

The response uses `FIRE DMG ABSORBED!` and `ICE DMG ABSORBED!` in the existing
combat text renderer. Each target has a 0.55-second simulation-time gate so held
weapons show the rule without stacking unreadable text every damage tick. Matching
hits use warm orange or ice-white hit flashes. Existing opposite-element reactions
remain intact. Fire-Ice continues to count as the opposing element against either
family, and the authored Stage 8 final-boss exemption remains intact.

The real-browser visual pass uncovered a separate flamethrower renderer crash:
`flameDraw` selected its source with `_isIce` before that constant was initialized.
The element test now runs before source selection. The fix does not change the
chosen flame or ice art.

Verification:

- Complete-suite section 304c: **10 passed / 0 failed**. It covers exact half
  damage and stat accounting, both popup labels, held-hit throttling, enemy,
  miniboss and boss boundaries, opposite-element behavior, and the Stage 8
  exemption.
- Native Chromium combined combat pass: **16 passed / 0 failed**, with zero page,
  console or controlled-loop errors. A real held primary-fire mouse input created
  the fire flamethrower, displayed the absorption label, and reduced Furnace body
  health through its normal part router.
- The rendered frame was inspected at
  `_shots/retina_audit_0915/furnace_fire_absorbed.png`.
- Final syntax passed. The complete suite reached its final summary at **3,873
  passed / 57 failed**, exit 1. There are no new failure names against the recorded
  58-name baseline; the historical random sand-tank assertion passed this run.

Proof: `docs/qa/elemental_absorption_0915.json`. Source:
`_BUILD_SOURCE/test_elemental_absorb_0915.cjs`,
`_BUILD_SOURCE/patch_elemental_absorb_0915.cjs`, and the combined native probe in
`_BUILD_SOURCE/retina_audit_0915/`. Runtime LF and suite CRLF are preserved. No
commit or push was performed.
