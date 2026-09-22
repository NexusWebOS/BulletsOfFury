# Bullets of Fury download notes — September 22, 2026

This handoff travels with the repository so it is available immediately after
downloading or pulling the latest `main` branch.

## Download

```powershell
git pull origin main
```

The main September build is commit `652b6086`. The small documentation commit
that adds this checklist follows it.

## Successfully completed

- [x] Replaced enemy burn status art with eight animated, transparent flames
  that wrap around the enemy while leaving its hull readable.
- [x] Matched ordinary burns to the orange, yellow and white-hot palette of the
  player flamethrower and magma orb.
- [x] Forged flamethrower burns remember the element color that ignited them,
  even after the player changes weapons.
- [x] Anchored all four Level 4 boss electrical shield cores to the Storm
  Sovereign. Camera and background scrolling cannot move them independently;
  they move only when the boss moves.
- [x] Kept core artwork, electricity, targeting and collision positions on the
  same boss-relative coordinates.
- [x] Integrated Cole's supplied full-body overhaul and all eight supplied Cole
  portrait variations.
- [x] Added updated 12-expression portrait sets for all nine pilots. Dialogue
  portraits face into the dialogue window and legacy portrait callers resolve
  to the new artwork.
- [x] Created the five-member Roaming Rebels art roster: three men and two
  women, with Darius Voss included as the leader.
- [x] Created five distinct transparent Rebel ship masters, normalized for the
  game and facing the player.
- [x] Added the generated source art, full prompts, build scripts, visual
  catalog and provenance needed to rebuild the portrait and Rebel assets.
- [x] Included the wider September gameplay, menu, campaign, weapon, sound,
  boss, Stage 6 wingman, score-tally and Fury Supplies work in the uploaded
  `652b6086` build.

## Things for Mike to review after downloading

- [ ] Play a representative fire-heavy section and confirm the new enemy burn
  scale feels right on small jets, tanks and larger regular enemies.
- [ ] Fight the Level 4 boss while moving left and right. Confirm the four
  electrical cores stay locked around the boss and follow only his motion.
- [ ] Review the proposed Rebel names, roles and ship names in
  `assets/game/roaming_rebels_0922/roster.json`. They remain working names until
  Mike approves them.
- [ ] Decide where and how all five Roaming Rebels enter the campaign. Their
  portraits and ships are registered, but the existing Stage 6 three-ship Rebel
  encounter has not yet been replaced with a five-member encounter.
- [ ] Decide whether existing cinematic background plates containing baked-in
  older figures should be regenerated. Menus, dialogue and live portrait routes
  already use the new pilot art.

## Verification record

- Game syntax passed.
- Real Chromium checks passed for portraits, Rebel ships, enemy burns and the
  Level 4 electrical-core anchors, with no page or console errors.
- The latest full suite completed with 4,905 passing checks and 75 known failure
  names. The failure list was unchanged by the burn and core fixes; the suite
  exits nonzero because those existing failures remain recorded.

More detail:

- `docs/ENEMY_BURN_0922.md`
- `docs/STAGE4_CORE_ANCHORS_0922.md`
- `docs/PORTRAITS_REBELS_0922.md`
- `docs/PORTRAITS_REBELS_0922.html`
- `docs/REPAIR_0922.md`
