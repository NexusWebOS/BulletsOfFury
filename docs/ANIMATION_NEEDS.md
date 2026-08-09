# BULLETS OF FURY — Enemy / Boss Animation Needs

Source: MegaPack v5.2 (`src/incoming_megapack_v5_2/07-bosses-and-sub-bosses/`).
Classification of how each boss's moving parts are authored, and what animation work each needs.

## The core principle (per Mike)
Prefer a **separate moving part** (rotor / blade / turret) that we rotate/pivot at runtime and
**overlay + anchor** onto the body. That gives smooth motion (e.g. a rotor spun in 5–15° steps over a
full 360°) instead of a small number of pre-baked frames that look choppy. Bosses whose only motion is
locked inside a handful of pre-rendered frames ("baked frames only") **cannot** be smoothed this way —
they need either (a) a separate moving-part asset authored, or (b) acceptance of the choppy baked loop.

## READY — SEPARATE ROTOR (build smooth rotation)
These ship a discrete spinning part on the same canvas as the body, already center-anchored.
- **jungle-overlord-x-helicopter** — `body-intact-192` + `rotor-f01..f12` (12 frames = 30° each), both 192×192,
  co-centered. PLAN: generate a fine 360° rotation set from the blade in 5–15° steps (24–72 frames),
  overlay on the body, anchored at the shared 192×192 center. Also fully componentized (core-cockpit,
  nose-chainguns, left/right weapon-wings, tail-engine — each intact/damaged/critical) for damage states.
  => This is the Level-1 helicopter boss to use for the smooth-blade treatment.

## NEEDS WORK — BAKED FRAMES ONLY (moving parts locked in pre-rendered frames; cannot smooth-rotate)
Motion is baked into idle/movement frame strips; no separate spinning part to rotate. To get smooth
rotation on any of these, a separate rotor/turret asset must be authored. Otherwise use the baked loop.
- **dam-breaker** — chopper; rotor spin is baked into `idle-f01..f06` (only 6 frames → choppy). No separate blade. *(This is why dam-breaker won't work for the smooth-blade request.)*
- battlefield-command-carrier
- bio-sludge-abomination
- cryo-behemoth
- cyclone-interceptor-carrier
- furious-death-normal / -super / -ultra
- glacier-rail-fortress
- hellwing-death-carrier
- jungle-siege-crawler
- magma-colossus
- obsidian-drill-tank
- rampart-zero
- toxic-dredger

## COMPONENTIZED (separate wings/turrets/cockpit — parts can be pivoted/rotated if a design calls for it)
Body + separately-authored parts (wings, turrets, cockpit, engines, guns), each with intact/damaged/critical.
Good for damage states and for pivoting individual turrets/wings; not rotors, but the parts are separable.
(48 bosses — full list in the sheet.) Examples: continental-crusher (24 parts), jungle-hornet,
jungle-thorn-predator, dreadnought-vanguard, ice-colossus-form1/2, storm-sovereign, the rival jets
(f16/f22/su57/mig29/etc.), the furious-death forms, and more.

## STATIC / STATES ONLY
No frame animation supplied (single sprite or damage-states only): bone-shard, death-implosion,
existence-core-pulse, furious-death-morph-transitions, tendril-slash, venom-orb.

---
## Rotor-overlay implementation note (for Overlord-X and any future separate-rotor part)
1. Pre-render the blade rotation set at build time (like `gen_rot.py` does for other art): rotate the
   single rotor sprite in N steps over 360° (N=24 → 15°, N=48 → 7.5°, N=72 → 5°), fixed square canvas,
   store as PNG frames + register in manifest. NO runtime canvas rotation/warp.
2. Draw order: body first, then pick `rotorFrame = round(spinAngle / step) % N` and blit it centered on
   the body's anchor (both share the 192×192 canvas, so anchor = body center).
3. Spin speed independent of frame count; advance spinAngle by degrees/second.
4. On damage-state change, swap the BODY art (intact/damaged/critical); the rotor overlay is unchanged.
