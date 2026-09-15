# Shared elemental weakness — September 15, 2026

Fire attacks now deal exactly double damage to ice-aligned enemies, minibosses
and bosses. Ice attacks do the same to fire-aligned targets. The multiplier runs
through the same three shared damage boundaries as elemental absorption, so it
also reaches authored component/helper routers and protected enemy or boss shield
pools before hull damage.

The existing opposing-element hit language is preserved: fire striking ice uses
the red silhouette and ice striking fire uses light blue. Fire-Ice counts as the
opposing element against either family. The Stage 8 final boss keeps its authored
elemental exemption.

Freezer already had two authored double-damage routes: Stage 2 Ice Breath and
Stage 3 Fire-Ice. `elementalAlreadyScaled` recognizes those paths so the shared
rule leaves them at 2x rather than multiplying them again to 4x. Other pilots use
the shared rule without gaining a pilot-specific bonus.

Verification:

- Complete-suite section 304c: **13 passed / 0 failed**. It covers fire-on-ice,
  ice-on-fire, exact 2x shield depletion, Freezer's no-4x guard, both 50%
  absorption paths, popup throttling, enemy/miniboss/boss boundaries and the
  Stage 8 exemption.
- Native Chromium combined combat pass: **19 passed / 0 failed**, with zero page,
  console or controlled-loop errors. Actual held primary-fire input struck an
  authored Stage 3 ice tank; Chromium independently resolved the same hit at
  exactly 2x.
- The rendered red opposing-element silhouette was inspected at
  `_shots/retina_audit_0915/stage3_fire_weakness.png`.
- Final syntax passed. The exact-runtime complete suite reached its final summary
  at **3,875 passed / 58 failed**, exit 1. All 58 failing names exactly match the
  recorded baseline; there are no new or missing names.

Proof: `docs/qa/elemental_weakness_0915.json`. Source:
`_BUILD_SOURCE/test_elemental_absorb_0915.cjs`,
`_BUILD_SOURCE/patch_elemental_weakness_0915.cjs`, and the combined native probe
in `_BUILD_SOURCE/retina_audit_0915/`. Runtime LF and suite CRLF are preserved.
No commit or push was performed.
