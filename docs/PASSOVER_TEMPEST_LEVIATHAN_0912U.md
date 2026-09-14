# PASSOVER 0912u/v/w — The Tempest Leviathan brothers: BOTH on Stage 6, fighting together (STAGED, NOT WIRED)

> **0913 — Mike's decisions, read these first:**
> - *"yes they fight together. they are meant to fight together on stage 6 only. not used on stage 8 at all."*
>   → the black ship and its light-gray brother are **ONE Stage 6 miniboss encounter**. Wire it per **§8**.
> - *"store the hod."* → the HERALD OF DEATH is **stored in the game as `ALTBOSS[8]`** (done, see §1). **Stage 8 now
>   has NO miniboss** until Mike picks one.
> - §1–§6 describe the black ship and still apply to it. §7 describes the gray ship on its own — **its Stage 8 plan is VOID**.

Mike, 2026-09-12: *"now snag the new tempest levithan, palette swap the red to black/dark gray. this is our
new mini-boss and fighting style for level 6's miniboss. upload this to the github as a seperate zip and
file set with a passover so my main pc can understadn waht to do"*

## 1. What state this is in — read first

- **The Leviathans are not in the game yet.** `assets/game.js` does not know either ship exists. Stage 6's miniboss is still
  `SUBBOSS[6] = blacksteel` (BLACKSTEEL RAPTOR, `stage6MiniInit/Tick/DrawOver`). Stage 6's boss is still
  `doomsdaycarriermk2`. ⚠ The comment on the `SUBBOSS[6]` row ("STORM SOVEREIGN … Leviathan keeps the boss
  slot") is stale — read the row, not the comment.
- **The ONE game change in this drop — Stage 8's miniboss is stored (0913).** `SUBBOSS[8]` is now empty and the HERALD
  OF DEATH (`heralddeath`, the "giant reaper") is `ALTBOSS[8]` — exactly like `ALTBOSS[3]`: its SHIPBOSS row, art,
  custom reels and death reel are kept, it still spawns by kind, and it is NOT in `DEAD_SUBBOSS`. Stage 8 still
  reaches its boss (VILE EXISTENCE): the boss gate is the stage clock (`stageTimer>=curStage.length`), not
  `subBossDone`, and the suite's 140-second Stage 8 soak asserts the boss arrives. The debug menu now lists 17
  fights. Putting the Herald back is one line: copy `ALTBOSS[8]` into `SUBBOSS[8]`.
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
| `…/encounter/brother.html` | **the light-gray brother's playable page** (same server, `http://127.0.0.1:8783/brother.html`) |
| `…/encounter/engine-brother.js` | the brother's flight: `class Brother extends Jet` — `engine.js` itself is unchanged |
| `…/encounter/brother-test.cjs` | the brother's regression test (`node brother-test.cjs`) |
| `…/encounter/assets/brother.png`, `brother-damaged.png` | the light-gray plates (from `sources/red_originals`) |
| `_STAGING/tempest_leviathan_0912u/grayswap_proof.png` | red / black / light gray, and both ships on the live Stage 8 field |
| `_BUILD_SOURCE/tempest_grayswap_0912v.py` | the light-gray swap tool |
| `…/encounter/duo.html` | **BOTH brothers in one fight — the Stage 6 miniboss as Mike wants it** (`http://127.0.0.1:8783/duo.html`) |
| `…/encounter/engine-duo.js` | `Duo` (shared player, fire, collisions, ending) + `DuoBlack` / `DuoBrother` (the tag-team rules); the two ship engines are unchanged |
| `…/encounter/duo-test.cjs` | the duo's regression test (`node duo-test.cjs`) |
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
- ~~Brother: whether the two brothers should ever appear together~~ — **answered 0913: together, Stage 6 only.**
- ~~Brother: whether the Herald of Death is kept or deleted~~ — **answered 0913: stored (`ALTBOSS[8]`, done).**
- **NEW: Stage 8 has no miniboss now.** Leave it empty, or pick a replacement.

## 7. The light-gray brother on its own (0912v) — ⚠ its Stage 8 plan is VOID since 0913; see §8

Mike, 2026-09-12: *"remove the giant reaper mini boss, and add another levithan ship in there, but palette swap
that one ot be more light gray then black. this will be its brother ship that does diagonal motions and
vertical motions and horizontal motions, but overall flys across the screen up and down, side to side off
screen and returning to flake you out."*

### 7.1 Which miniboss is "the giant reaper"
`heralddeath` — **HERALD OF DEATH**, Stage 8's miniboss (`SUBBOSS[8]`, a bone-winged skull carrier). Nothing in
the stage tables is literally named "reaper" (GRAY REAPER is only a mega-boss form name), so the four
candidates were rendered side by side before deciding: the Blacksteel Raptor (Stage 6) is an F-22-style jet,
the Inferno Reaver (Stage 2) is a lava ship, and the Herald is the reaper. Stage 8 is **FURIOUS DEATH**, a dark
space field; its boss is `vileexistence` (BLACK COCOON).

### 7.2 The art
`assets/brother.png` / `brother-damaged.png`, built from the **red originals** by
`_BUILD_SOURCE/tempest_grayswap_0912v.py`:
- red wing paint → light gray; the black titanium hull → mid/light gray (body value median 0.13 → 0.47);
- the outer **2px outline stays dark** (black-edge rule) so the silhouette holds on any field;
- violet reactor, cyan apertures, blue engines and the damaged plate's orange scorch are untouched; alpha 0 delta;
- guards: 221/256 and 227/256 value levels kept, 0 saturated red left (the first run was refused for a red
  rim left in the outline ring). The lift is an offset plus a ~1.3 gain, not a stretch (CLAUDE.md 0906o).
- On the live Stage 8 field it reads clearly — see `grayswap_proof.png`.

### 7.3 The flight style (what makes it the brother, not a copy)
The black ship moves on exactly ONE axis per step and stays in the arena. The brother does the opposite:
- **Any-line flight** — diagonal, horizontal and vertical runs (`glide`). It still never yaws, rotates or flips.
- **It leaves the screen and comes back from another edge**: every run starts off-screen, crosses, and exits.
- **Runs per phase** (same HP gates as the black ship):
  - `chase` 100–75%: corner-to-corner DIAGONAL crossing · SIDE PASS with a mid-screen braking laser stop ·
    VERTICAL PLUNGE down the player's column.
  - `pursuit` 75–50%: FEINT (dives at the player's row on a diagonal, then V-turns up and out the far top
    corner) · side pass · diagonal · plunge (can come UP from the bottom now).
  - `hell` 50–25%: ZIGZAG — diagonal bounces between the walls with needle missiles at every apex · plunge · diagonal.
  - `frenzy` 25–0%: all of them, 1.22× faster, shorter warnings.
- **Flaking you out, fairly:** each return is announced by a red **entry marker at the exact edge point it will
  come through, with the line it will fly** (0.6s, 0.38s when hard; the marker is kept clear of the top HUD strip - in the game that band is the 77px boss gauge). The feint is a V-turn AFTER it has
  entered — never a warning at the wrong edge. It is **invulnerable while off-screen** and **hovers high for a
  counterattack window** after each run, firing rear lasers.
- It **never uses the black ship's overtake/return beats** (which move the player); those phase changes become
  an off-screen regroup.

Measured by `node brother-test.cjs` over three seeded full showcase runs (all reach victory in ~130 s):
~4,100–4,400 diagonal frames, ~1,900–2,100 horizontal-only and ~3,650–3,800 vertical-only; 62–63 screen exits,
off every edge (x −170..1070, y −180..1180); 62–65 returns, **every one warned**; 4–5 feints; 0 hittable frames
off-screen; 0 rotation; all positions finite; apertures still silence. The same run asserts the black ship
still has **0** diagonal frames.

### 7.4 ⚠ VOID (0913): the brother is not used on Stage 8. Kept only for its engine-level notes, which §8 reuses
Follow §5 for everything shared (Razorback pattern, art registration, hooks, HP floor sync, retina lock for the
needle missiles, sound keys). The differences:
1. **Kind id `tempestbrother`** (display `TEMPEST LEVIATHAN II` or Mike's choice; the debug name must not equal
   the kind in capitals). Replace `SUBBOSS[8].kind` (`heralddeath`) with it.
2. **The Herald of Death:** remove it from the slot, keep its code and art on disk unless Mike says delete
   (recommend `ALTBOSS[8]`, exactly like `ALTBOSS[3]`; do NOT add it to `DEAD_SUBBOSS` if it may return).
   Repoint suite assertions that pin `SUBBOSS[8]` / `heralddeath` (grep `test_fl.js`).
3. **Diagonal movement is correct for THIS unit** — do not carry the black ship's axis-only rule onto it.
4. ⚠ **Exits and entries are screen edges, i.e. CAMERA edges** (`camLeftX()/camRightX()`, the 480 camera on the
   680 world), not world edges — an off-world entry on a panning stage arrives unwarned (0811s/0813x).
5. ⚠ **The entry marker is drawn in screen space**, so it must carry the camera translate exactly like every
   other overlay (the world-vs-screen trap CLAUDE.md records five times).
6. ⚠ **Off-screen means unhittable**: `subBossHitPart` must return null while it is off-camera, and the hittable
   flag is decided AFTER the move (the brother's own test caught it one frame late on every exit).
7. The top 77 world px are the boss gauge band — the counterattack hover (pack y 210) must land below it.
8. Verify with a `probe_tempestbrother_*.py` (BOSSMODE `start(8,'mini',…)`): diagonal + axis-only frames, exits
   off camera edges, warned returns, 0 off-camera hits, key-identified draws of `tlvb_*` plates, screenshots
   over the Stage 8 field; then the full suite with a failure-name diff.

## 8. The brothers together — Stage 6's miniboss (0912w, STAGED, NOT WIRED)

Mike, 2026-09-13: *"store the hod. and yes they fight together. they are meant to fight together on stage 6
only. not used on stage 8 at all.."*

### 8.1 What the duo is
`duo.html` / `engine-duo.js`. Both ships fly the SAME fight on one screen against one player:
- **BLACK** (engine.js `Jet`, unchanged) holds the arena: one-axis strafes, twin laser lanes, side rams.
- **GRAY** (engine-brother.js `Brother`, unchanged) crosses from anywhere: diagonal / horizontal / vertical runs off
  every edge and back, feints, zigzag missiles, counterattack hovers.
- Each keeps its **own 8,000 HP, its own four 300-HP apertures and its own four phase gates**. `Duo` owns the player,
  the player's fire, every collision and the ending. The HUD bar shows the pair's average integrity.

### 8.2 The tag-team rules (they are what keep two dangerous ships readable — port them, do not drop them)
1. **The black ship never STARTS a side ram while its brother is warning in or crossing** — including a run still
   flying in from off-screen (`DuoBlack.change` defers `ram-warn` and keeps lining up on the row).
2. **The brother waits OFF-SCREEN, unwarned and unhittable, while the black ship lines up, rams or changes phase**
   (`DuoBrother.fly` replaces its regroup with a hold).
3. **PINCER** — while the black ship burns its twin rear laser lanes from the top, the brother's next run is a side
   pass UNDERNEATH it, between the black ship and the player.
4. **VENGEANCE** — when one brother goes down its falling reactor plays, it leaves the fight, and the survivor fights
   on alone: no more waiting, and the gray one flies 15% faster.
5. **One escape**, after BOTH are down.
6. **The duo never moves the player** — the black ship's overtake/return still move the black SHIP, but not the player.

⚠ Two of these rules failed on their first cut and the fixes are recorded in `engine-duo.js`: the hold ran BEFORE the
regroup (which leaves the screen and plans in the same call, so it never caught the brother waiting — 0 held frames),
and a run still inbound from off-screen did not count as a crossing (310 frames of ram-during-crossing on one seed).

### 8.3 Measured
`node duo-test.cjs`, three seeded full showcase runs — every one ends in **victory** (141–151 s):
- both ships on screen together ~8,200–8,400 frames; **0** frames of the black ship ramming during a crossing;
- brother held off-screen 528–811 frames; black ram deferrals 509–735; pincers 10–11;
- the black ship keeps **0** diagonal steps inside the duo; the gray keeps its diagonal, horizontal and vertical runs
  and 67–73 screen exits; **0** player jumps (nothing but input moves the player);
- one brother falls first (the black, ~120 s, in all three) and the survivor fights on alone; one escape after both;
- no rotation, all positions finite. `node brother-test.cjs` and `node interceptor-test.cjs` still pass.
Chromium: `duo.html` builds `Duo` with `DuoBlack` + `DuoBrother`, loads both plate sets, shows both ships on screen
and the entry marker, **0 console errors**; `index.html` and `brother.html` still load their single ship.

### 8.4 Wiring it in as Stage 6's miniboss
Everything in §5 (Razorback pattern, art registration, hooks, HP-floor sync, retina lock for the needle missiles,
sound keys) and the engine notes in §7.4 (diagonal flight is correct for the gray ship, camera-edge exits,
screen-space entry marker, off-camera unhittable, the 77px gauge band) still applies. On top of that:
1. **One kind for the pair: `tempestbrothers`** in `SUBBOSS[6]`, replacing `blacksteel`. `subBoss` is a single global,
   so the sub-boss owns BOTH ship states (the `Duo` shape): `b._tlv={black:{…}, gray:{…}}`.
2. **Hit routing per ship and aperture** — `subBossHitPart` returns part keys like `B0..B3` / `Bhull` / `G0..G3` / `Ghull`
   (null for an off-camera gray ship); `hitSubBoss` routes damage into that ship's pools.
3. **The HP bar is the PAIR** (sum of both pools, re-proportioned to the engine's HP floor). The sub-boss dies only when
   BOTH ships are down; the first ship's fall is an explosion and a removal, not the sub-boss death branch.
4. **Port the tag-team rules as written** — they depend on the black ship's state names (`edge`, `row`, `ram-warn`,
   `ram`, `punish-rise`, `laser-track`), so keep those names if the state machine is ported.
5. This is **two ships, not a boss splitting** — NO BOSS SPLITS does not apply (and it is a miniboss).
6. The Blacksteel Raptor: store as `ALTBOSS[6]` like `ALTBOSS[3]`/`ALTBOSS[8]` if Mike agrees (still open), and repoint
   the suite assertions that pin `SUBBOSS[6]` / "stage 6 is the BLACKSTEEL".
7. Verify with a `probe_tempestbrothers_*.py` (`BOSSMODE.start(6,'mini',…)`) porting duo-test's assertions — both on
   screen, 0 ram-during-crossing, holds, pincers, survivor alone, one death — with key-identified draws of both plate
   sets and screenshots over the purple Stage 6 field; then the full suite with a failure-name diff.
