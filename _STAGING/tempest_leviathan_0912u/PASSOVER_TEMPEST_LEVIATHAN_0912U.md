# PASSOVER 0912u — Tempest Leviathan, black/dark gray: the new Stage 6 miniboss (STAGED, NOT WIRED)

Mike, 2026-09-12: *"now snag the new tempest levithan, palette swap the red to black/dark gray. this is our
new mini-boss and fighting style for level 6's miniboss. upload this to the github as a seperate zip and
file set with a passover so my main pc can understadn waht to do"*

## 1. What state this is in — read first

- **The game is unchanged.** `assets/game.js` does not know this unit exists. Stage 6's miniboss is still
  `SUBBOSS[6] = blacksteel` (BLACKSTEEL RAPTOR, `stage6MiniInit/Tick/DrawOver`). Stage 6's boss is still
  `doomsdaycarriermk2`. ⚠ The comment on the `SUBBOSS[6]` row ("STORM SOVEREIGN … Leviathan keeps the boss
  slot") is stale — read the row, not the comment.
- **What IS done:** the encounter is copied into the repo as a playable file set, the red paint is
  palette-swapped to black/dark gray and verified, and this document says how to wire it in.
- Repo HEAD this was staged on top of: `694e84ae` (Furnace Tyrant). Suite baseline there:
  **3,488 ok / 64 fail** (the one name beyond a clean worktree is the flaky stage-1 sand-tank fixture).

## 2. Files

| path | what |
|---|---|
| `_STAGING/tempest_leviathan_0912u/encounter/` | the complete standalone encounter, **byte-identical to Mike's approved pack except the two ship plates** (now black) and the two manifest hash entries |
| `…/encounter/sources/red_originals/` | the untouched red `interceptor.png` / `interceptor-damaged.png` — re-run the swap from THESE, never from the black output (CLAUDE.md 0906o) |
| `_STAGING/tempest_leviathan_0912u/blackswap_proof.png` | red vs black on a dark field and on the live Stage 6 field (the purple night storm) |
| `_STAGING/tempest_leviathan_0912u.zip` | the same folder, zipped (the repo ignores `*.zip`; `.gitignore` carries `!_STAGING/*.zip` for this) |
| `_BUILD_SOURCE/tempest_blackswap_0912u.py` | the swap tool, with its measurements in its docstring |
| `docs/PASSOVER_TEMPEST_LEVIATHAN_0912U.md` | this file (a copy is inside the zip) |

Play it standalone:

```bash
cd "_STAGING/tempest_leviathan_0912u/encounter" && node serve.cjs
```

then open http://127.0.0.1:8783/ — **ENGAGE BOSS**, or **WATCH SHOWCASE** to see every phase. Its own
regression test: `node interceptor-test.cjs` (also `test.cjs` / `rig-test.cjs`). `engine.js` is the live
simulation and `game.js` its renderer; `engine-v3.js` is an older snapshot and is NOT loaded.

## 3. The palette swap — what changed and what did not

Measured on the two live plates (807×700; the pack renders only these — `jet*.png`, `turret*.png` and
`player.png` are unrendered history / the standalone's stand-in player ship, and were not touched):

- **Wing paint** at hue 350°–15° (sat p50 0.79, val p50 0.42) → **dark gray**: saturation ×0.14, value
  ×0.66 + 0.018. Lands at val p50 ≈0.30 — darker than the paint, **lighter than the black titanium body
  (0.13)**, so the wings still read as their own panels. Feathered: full effect within ±10° of red, none past
  24°, so the damaged plate's **orange scorch (damage glow) stays**.
- **Kept exactly:** the violet reactor, the cyan laser apertures, the blue engines, alpha (0 delta).
- **Ordnance keeps its colour** (CLAUDE.md standing rule): laser beam, charge corona, plasma bolt, the
  needle missile (including its small red fins), fire, smoke and explosions are untouched. If Mike wants the
  missile fins black too, that is one more plate through the same tool.
- ⚠ **The usual 20%-palette-loss guard does not apply to this kind of swap, and why is measured.** RGB colour
  count went 66,226 → 42,877 (0.65) intact and 75,647 → 49,893 (0.66) damaged — and a five-setting sweep
  (sat ×0.10–0.22, value ×0.52–0.66, with and without a hue rotation) gave 0.63–0.67 every time. A ratio that
  does not move with the parameters is intrinsic to removing chroma from ~72k saturated pixels. So the tool
  guards on **distinct value levels** in the painted band (kept 182/255 and 200/255), zero alpha change and
  zero saturated red left — and the proof was read at full size on the real Stage 6 field before accepting.
- On the live Stage 6 field (purple storm clouds, rain) the black jet reads clearly — the current Blacksteel
  Raptor is also dark gunmetal and reads fine there.

Re-run: `python3 _BUILD_SOURCE/tempest_blackswap_0912u.py --src <red_originals> --out <assets> --proof <png> --field <stage-6 capture> --write`

## 4. The fighting style being adopted (from the pack's README, verified against `engine.js`)

- **Fixed nose-up. No yaw, rotate, flip or diagonal.** Every simulation step moves the boss on **exactly one
  axis** (x OR y). This is the defining look of the fight — do not "smooth" it with diagonal easing.
- Two integrated laser housings, each with a **front and a rear aperture** — **four apertures, 300 HP each**,
  each independently silenced when destroyed (destroying one also costs the hull 90).
- Hull 8,000 HP in four gated phases (thresholds cannot be skipped):
  - **100–75% `chase`**: fast horizontal strafes firing rear plasma bolts; warned twin **rear** laser lanes that
    track then stop tracking before they fire; vertical dive/climb.
  - **→ `overtake`** (1.5s): the boss drops below the player.
  - **75–50% `pursuit`**: tracks beneath the player (560 px/s), drives forward behind twin **front** lasers, then
    **three side rams**: park at a random left/right edge, capture the player's ROW, 0.4s warning band, ram
    horizontally at 1,200 px/s, short vertical recovery above the player = a 1-second counterattack window (its
    rear lasers still threaten).
  - **→ `return`** (1.5s).
  - **50–25% `hell`**: faster rear assault, shorter beam warnings, faster bolts, **needle missiles** from the rear
    apertures on each dive.
  - **→ `falsecrash`** (1.3s, burning).
  - **25–0% `frenzy`**: 660 px/s pursuit, 0.35s beam warning, **four** 1,450 px/s rams, 0.28s ram warning, 0.72s
    counterattack windows.
  - **0% `death`**: falling reactor explosion, then a bottom-to-top escape cinematic.
- Standalone damage model: lasers 20, rams 32, bolts 10, needle missiles 18 (missiles take 2 hits to shoot down).

## 5. How to wire it in as Stage 6's miniboss — step by step

Follow the **Razorback port (0912r)** exactly; it is the same shape (a standalone pack → a sub-boss rig).
Its code sits beside `jungleCruiserInit` in `assets/game.js` and its CLAUDE.md section lists every trap.

1. **Pick a kind id that is not taken: `tempestleviathan`.** ⚠ `leviathan` is a legacy `spawnBoss` case
   (`LEVIATHAN CORE`), and RUST / CESSPOOL / TOXIC / RUNWAY / ABYSSAL LEVIATHAN all exist. Display name
   `TEMPEST LEVIATHAN`; in `DEBUG_BOSS_NAMES` give it a name that is **not** its kind in capitals
   (`debugFightList` rejects that by construction — 0912r).
2. **Art.** Copy the two black plates + `laser-beam`, `laser-charge`, `plasma-bolt`, `needle-missile` into
   `assets/game/bosses/tempest/` as `tlv_*.png` and register them in the top-of-file loose-art block (beside
   `rzb_` and `fzt_`). **Do not copy** the pack's `explosion-0..7` — they ARE the game's `nxp_barrage_0..7`
   (manifest says so); use the game's own FX, smoke and fire.
3. **Hooks — the Razorback set, one each:** `case 'tempestleviathan': tempestInit(b); break;` in
   `spawnSubBoss__inner`; `if(b._tlv){ tempestUpdate(b,dt); return; }` in `updateSubBoss` next to `_rzb`;
   `if(b._tlv){ tempestDraw(b); return; }` in `drawSubBoss`; per-part geometry in `subBossHitPart` (the four
   apertures + hull, **only live parts stop a shot**); damage routing in `hitSubBoss`; a projectile draw hook
   at the head of the `eBullets` loop in `drawBullets` + `PROJ` rows for every new bullet kind (§ PROJ
   coverage assertion); `_PACKOF` warm prefix.
4. ⚠ **HP floor sync.** The engine raises a miniboss to its stage's HP floor AFTER spawn. Size the aperture
   pools and the four phase thresholds as SHARES of whatever `maxhp` settles (the Razorback's `hpSync`), or
   the last phase empties with hp still on the bar and it cannot die.
5. ⚠ **The needle missiles go through the retina lock (0912q header rule).** Queue them with
   `enemyLockOn(b, delay, {fire})` — one retina per unit, launches 1-by-1 — never direct spawns.
6. **Conversions.** The pack arena is 900×1000 in px/s. The game world is 680 wide (480 camera), `VH` 512,
   and enemy bullets move **per frame** (`b.x += b.vx`). Convert sizes and distances by a scale factor,
   speeds to px/frame, and apply the house ×1.35 "faster projectiles" convention. Keep the pack's ratio of
   boss to player (108×118 against a 48×59 player ≈ 2×).
7. ⚠ **Screen-space hazards — these are where a straight port goes wrong:**
   - The top **77 world px are the BOSS gauge band** (0912t `FZT_YOFF`): nothing the player must hit may park there.
   - The side rams span the SCREEN, so compute edges from the **camera** (`camLeftX/camRightX`), not the
     world — a world-edge ram on a panning stage starts off-camera and arrives unreadable (0811s/0813x).
   - Rams and "tracks beneath the player" put a 1,200–1,450 px/s hull through the player's space: keep the
     warning band, and keep contact damage on the ram only (the ordinary sub-boss body contact rules apply).
8. ⚠ **Two pack beats cannot be ported as-is — Mike's call:**
   - `overtake` / `return` **move the PLAYER'S y** (`p.y += …`) to swap who is on whose six. In the campaign
     that takes the controls away. Options: move only the boss across the player with a warning, or keep it.
   - The 0% **escape cinematic** is a whole-screen sequence; a miniboss death in the campaign must hand back to
     the stage (`unitDeathFX` + the sub-boss death branch), not play a victory escape.
9. **Sound** (all six pack WAVs already exist in `assets/game/sounds/`, and `reviewed_enemy_laser.wav` is
   byte-identical): lasers → `enemyPulseLaserBlue`; rams → `maverickHelixRelease` (the pack's `ram-boost.wav` is
   that file); impacts → `explosionAirSmall01`; break-up → `explosionJetBreakup`; death → `explosionBossCore`.
   ⚠ `enemy_machine_shot_heavy.wav` has **no key** yet — register it in the code-owned `Object.assign(BOFA.sfx,…)`
   block **with a `Snd.TAME` row** (0912j: a key with no row plays unthrottled).
10. **The Blacksteel Raptor:** store it as `ALTBOSS[6]` exactly like `ALTBOSS[3]` (keep its row and art, do
    NOT add it to `DEAD_SUBBOSS`) — recommended, Mike's call. Then repoint the suite assertions that pin
    `SUBBOSS[6]` / "stage 6 is the BLACKSTEEL" (grep `test_fl.js` for `blacksteel` and `SUBBOSS[6]`).
11. **Verify like 0912r:** a `probe_tempest_*.py` that starts `BOSSMODE.start(6,'mini',…)`, identifies draws by
    the KEY `XART.get` is asked for (never by size/`src`), asserts axis-only movement and fixed orientation,
    one-at-a-time retina-locked missiles, aperture silencing, phase gating, death — and **looks at screenshots
    over the purple Stage 6 field**. Then the full suite, comparing failure NAMES against a clean worktree.

## 6. Open for Mike

- The two pack beats in step 8 (player-moving overtake; escape cinematic).
- Whether the needle missile's small red fins should also go black (ordnance rule keeps them red).
- Whether the Blacksteel Raptor becomes `ALTBOSS[6]`.
