# Fusion and co-op combat integrity — October 5

Mike requested continued game improvements after the Cole/Rebel update. This pass fixes concrete collision and state defects in that update and keeps existing authored art and encounter timing.

Fusion impact sprites previously occupied `pBullets`. Rebel ability-crate and other bullet consumers could therefore treat a visual explosion as a damaging shot. Impacts now use a bounded private effects pool, advance in simulation, and render through `drawEffects` under the existing world camera. The authored reel finishes without a fade and clears at stage/new-game/load boundaries. Real beams, splash, ricochets and eight shards remain damaging; all descendants inherit the firing seat.

Cole's selected and earned laser tiers, plus the manual primary choice, now participate in the established co-op seat swap. Empty values are initialized for both seats to prevent fallback to P1. Input suppression checks the requested ship rather than whichever ship is temporarily active. A P1 equip chord cannot silence P2. Fresh games clear both seats' laser state. Campaign loads validate saved tiers/unlocks and fall back to earned weapon banks for malformed fields.

Fusion previously used only missile acquisition targets. A cloaked Rebel consequently had no Fusion collision body. A private, physical hull proxy now lets aimed Fusion and shards hit her while the global missile-lock list remains unchanged. Visible and cloaked proxies share their piercing-hit identity, preventing a second hit when cloak ends. Protected dialogue, warping/entry and dead hulls remain excluded. Phased enemies no longer trigger Fusion impacts or receive splash.

The Rebel formation controller centers a single-contact duel and uses individual slots when multiple pilots remain. The five-pilot Stage X rematch and centered legacy duel are verified separately; this does not convert the legacy single-contact mode into a squad fight.

## Verification

- Syntax checks: `node --check assets/game.js` and each of the three changed overlay scripts.
- `node _BUILD_SOURCE/test_fl.js`: 7,240 assertions, exit 0, final BUILD OK reached. Previous baseline was 7,223; seventeen new gameplay regressions pass.
- `_BUILD_SOURCE/probe_combat_integrity_1005.py`: nineteen Chromium gameplay/review checks pass, including actual simultaneous keyboard input, private impact lifetime, crate collision, P2 descendants, cloaked Nyx damage/white hit flash, and Stage X formation.
- Existing `_BUILD_SOURCE/probe_cole_rebel_1004l.py`: all twenty-five checks pass after the final changes, including overload death, real modular boss damage, all ten ships surviving the protected demonstrations, top HUD and playable review routes.
- Screenshots inspected through the game's real canvas: impact/shards, independent co-op fire, five Stage X ships with anchored bars, cloaked Nyx's white hit flash, and an impact over an undamaged ability crate. Both browser reports have zero page/console errors. Browser navigation/closing can reset the local HTTP server's unfinished asset sockets; that is distinct from browser errors.

Playable review: `_shots/combat_integrity_1005/review.html`. Portable evidence: `docs/qa/combat_integrity_1005.json`. The review blocks campaign-storage writes. No assets or atlases were replaced. `assets/game.js` was not edited and remains LF; the suite entry point remains CRLF. Unrelated untracked projects and scratch are preserved. Local only: no commit or push. These fixtures are not a full human campaign clear or a full balance audit.

Mike authorized publishing this verified combat-integrity pass together with the overnight upgrades on October 5. Scratch captures remain local.
