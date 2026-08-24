# PASSOVER — 0823 handoff

Written to hand Bullets of Fury to another agent mid-stream. Read this top to bottom before
touching anything; the second half is the part that will save you a day.

---

## 0. READ THESE FIRST, IN THIS ORDER

1. **`CLAUDE.md`** in this repo — ~1,900 lines, the real instructions. Not the one in the parent
   folder, which is only a router.
2. **`docs/feedback/0823_video_walkthrough.txt`** — Mike's own 33-minute walkthrough, transcribed
   to 183 timestamped segments. **This is the live bug list.** It is his words, and the timestamps
   map straight to the video (`C:\Users\Mdogg\Videos\2026-08-23 16-19-57.mp4`).
3. **`docs/PASSOVER_0822A.md`** — the long running log. Sections `0822x` through `0822ag` are this
   session.

---

## 1. ⚠ THE WORKING TREE IS SHARED RIGHT NOW

**Another agent session is editing `assets/game.js` at the same time.** As of this writing the
working tree contains their in-progress work as well as mine:

- flamethrower / ice-breath audio (`flameSndStart(el)`, `iceBreathLoop`, `weaponHitSfx`)
- `pShard`, `flameFire`, `FUSE_DMG`, `pShoot`, `lizzieFire`

Two suite failures come from that work, not from anything in this handoff:

```
ASSERT FAIL: the flamethrower loops arc_flame_loop.wav     <- they renamed the loop
ASSERT FAIL: game/ holds music, sounds, fonts, ...         <- they added cinematic_* asset dirs
```

**Do not revert those and do not attribute them.** Either coordinate with that session or wait for
it to land. `git diff assets/game.js` shows both sets mixed.

---

## 2. SUITE BASELINE

```
node _BUILD_SOURCE/test_fl.js            2798 ok / 5 fail
node _BUILD_SOURCE/verify_atlas_0806z.js PASS
python _BUILD_SOURCE/shoot.py --state PLAY --stage N --out DIR
```

Of the 5 failures: **3 are long-standing and unrelated** (a preload bound that wants `<600` against
a set of 602; two about a `_superseded/` quarantine ledger). **2 are the other session's**, above.

⚠ **Rule 3 from CLAUDE.md, and it has bitten twice this week: `0 failures` can mean a crash.
Always check the assertion COUNT, not just the fail count.**

---

## 3. WHAT LANDED THIS SESSION

Commits `0aecdec` → `b728149`, plus uncommitted card work (§5).

| drop | what |
|---|---|
| 0822x | atlas halo sweep — 13,467px to a black edge on 21 **rendered and verified** sheets; repaired 861px 0822w had wrongly blackened on nebula/glow rims |
| 0822y | Doomsday Carrier Mk II on stage 6; fixed `shipBossDraw` drawing every ship boss **square** |
| 0822z | stage 7 on Mike's new 680×4716 sewer; **removed the L7 boss map teleport** |
| 0822aa | Furious Death — stage 8 modular sky + parallax scenery |
| 0822ab | **stage 9 made reachable** — it was absent from `STAGES[]` entirely |
| 0822ac | stage 7 ends by flying into the void portal |
| 0822ad | the stage-5 secret: nine gates, warp-out, campaign-map unlock |
| 0822ae | **killed the boss beeping**; transcribed the video |
| 0822af | **menu input** — the controller was locked out of half the game |
| 0822ag | campaign-hub screen flash; installed 25 missing weapon icons; Freezer's per-stage kit |

---

## 4. THE FOUR FINDINGS WORTH REMEMBERING

These are the ones that were invisible from the source and only fell out of measurement.

**1. `'up'` is not a key name.** `keyName()` returns `e.key.toLowerCase()`, so an arrow key is
`'arrowup'`. Four menus tested `Input.tap('up')` — a string that has never matched anything —
alongside `'w'`, which does. Mode select, campaign hub and the campaign map were **arrow-key and
d-pad dead**, measured by stashing the fix and re-running. Everything menu-shaped must go through
`Input.menuUp/menuDown/menuLeft/menuRight`, which read `keybind.*`.

**2. The beeping was `enemyShoot`, fired per BULLET.** `eMG` plays it for every machine-gun pellet
and the boss blast fan called it inside its own `k=-1..1` loop. The stage 6 boss asked for it
**124 times in 10 seconds**. Now throttled at the source (`ESHOOT_GAP=90ms`) → 11 tones. Dials:
`ESHOOT_GAP`, `UI_BLIP_REPEAT`, `UI_BLIP`.

**3. Ice breath never appeared because the ICON did not exist.** The drop table was innocent —
120 crates as Freezer on stage 2 produce `icebreath ×20`. But `WVAR_ICON` named five icon families
and **none of them were registered**. The art was authored and sitting in `_ART_SOURCES` the whole
time. 25 icons installed. A code comment claimed they "already existed and were simply
unreachable" — they existed, in a folder, never in the build.

**4. `PEMB_INK` had drifted on all nine emblems.** It is the source rect cropped out of each
256×256 affiliation emblem, "measured offline" once. Axel's said `x:28 w:200` while the ink runs
`23..233` — the crop sliced **5px off each wing**, which is exactly the "cut off on the left wing
side" Mike reported. Decker's and Juggernaut's were the opposite: a rect **larger** than their ink,
so they drew shrunken and off-centre. Re-derived from each emblem's alpha bounding box.

> The pattern in all four: **a table describing art, maintained by hand, drifting from the art.**
> When something looks wrong on screen, measure the asset before reading the logic.

---

## 5. UNCOMMITTED WORK IN `assets/game.js` (finish or keep)

Small and self-contained. All verified in a browser.

- **`PC_SPECIAL`** — `axel: 'MEGA SHIELD'` (was `AFTERBURNER`; the code has always given him
  `special.orbs=5` and `run.shield=5`), `lizzie: 'ATOM BOMB + HEAVY TURRET'`,
  `cole: 'SONIC BOOM / WARHEAD'`. Axel keeps his winged-A emblem — Mike: *"you could probably take
  his afterburner symbol that you have."*
- **`SPECIAL_INFO.axel`** → `MEGA SHIELD` too. That table and `PC_SPECIAL` **disagreed on almost
  every pilot**; only Axel's is reconciled, because only his was a flat contradiction. The other
  six still disagree — see §7.
- **`PEMB_INK`** — all nine re-measured.
- **`_BUILD_SOURCE/test_fl.js`** — 9 new assertions covering the above.

⚠ I reverted my edits to `SPECIAL_INFO.cole` and `SPECIAL_INFO.lizzie`: those had their own
recorded decisions with assertions behind them (*"NUKE STRIKE is still his special — art changed,
mechanic did not"*). Mike was looking at the **card**, so only the card changed. If he wants the
select-screen blurbs to match too, repoint those assertions rather than deleting them.

`+` and `/` both resolve as glyphs (`sfont1_p43` / `sfont1_p47`) — verified, every font family 1–8
carries them.

---

## 6. THE OUTSTANDING LIST, FROM MIKE'S VIDEO

Timestamps are into `docs/feedback/0823_video_walkthrough.txt`. He asked for menu input first;
that is done. **Next up was the rest of the pilot cards.**

### Pilot cards — partly done
- [x] Axel's special is Mega Shield, not afterburner `[03:23]`
- [x] Lizzie: Atom Bomb **and** Heavy Turret `[02:49]`
- [x] Cole: add Sonic Boom / Warhead `[23:55]`
- [x] Icons cut off / off-centre in the bottom-right socket `[02:49, 03:23]`
- [ ] **Move the text up** on Falva, Decker, Maverick and Cole's right-hand card so everything
      fits `[03:09, 03:46, 23:55]` — on Axel the `SPEED` label collides with the last line of the
      description; that is the bug to chase
- [ ] Maverick's avatar is cut off at the top `[06:18]`
- [ ] Use the dialogue-font zip on the cards; palette-swap per pilot `[02:32]`

### Menus — done, except
- [ ] Music should stop when returning to the main menu `[01:48]`
- [ ] Softlock pilot re-select while a campaign is in progress `[11:12]`
- [ ] Pilots must face the player, never away `[11:30, 13:46]`
- [ ] Fury HQ: **all** pilots on screen behind the console, not one at a time `[13:54]` — he says
      he has asked five times

### Weapons
- [ ] **Revert the laser for everyone; only Maverick keeps the helix beam** `[08:36, 13:13]` — he
      says it twice and calls it a good change *for Maverick only*
- [ ] Helix laser should cross the whole screen `[05:34]`
- [ ] Level 2 weapon shows a level 1 bullet icon `[05:20]`
- [ ] Change the upgrade colour per level `[09:25]`
- [ ] Decker shoots far too fast `[20:22]`
- [ ] Fire wave sound is missing `[14:26]`
- [ ] After level 3, Fire Orb and Ice Orb as separate pickups `[18:50]`

### Things that must not move
- [ ] Ships twist while moving `[04:20]`; projectiles spin `[15:19]`; barrels wobble and scroll
      in `[12:32]`; clouds animate `[08:23]`

### Bosses
- [ ] **No boss fades out — they blow up** `[16:38]`, said "like sometimes" before
- [ ] Patterns don't read; missiles should be real projectiles that return `[09:49]`
- [ ] Homing that cannot be escaped even with a barrel roll `[16:06]`
- [ ] Ice boss should fire ice `[18:38]`

### Stages
- [ ] Stage 6 background: own art, blended, fading through the level `[08:06]`
- [ ] Space background: same at start and here; drop the objects enemies hide behind `[06:28]`
- [ ] Stage 3 should extend into lava, not cut to it `[15:46]`
- [ ] Stage transition: the ship should keep moving, the stage should keep scrolling `[11:55]`
- [ ] The flyover **should not pause the screen** — live time as you fly out `[13:42]`

### Freezer — spec captured, one part open
Implemented and asserted: stage 2 ice breath only (never flamethrower); stage 3 flamethrower +
fireice only; stage 4+ all four; **never fireorb, ever**. Everyone else gets fireorb from 3.
- [ ] Ice breath still was not appearing in his level-3 run `[29:42]` — worth a second look now
      that the icons exist

---

## 7. OPEN QUESTIONS FOR MIKE — do not guess these

1. **`SPECIAL_INFO` and `PC_SPECIAL` disagree on six pilots** (decker OVERCLOCK/CLOAKING SYSTEM,
   maverick VENOM STRIKE/HELIX BEAM, freezer TIME FREEZE/ICE ORB, juggernaut WRECKING
   BALL/SIEGE MODE, falva ROLLER BALL/ROLLER-BALL, yuri agrees). Renaming an ability is his call.
2. **`SHIPBOSS.dmg` is dead data** — nothing reads it, confirmed by him. Every ship boss declares
   damaged/critical plates that have never drawn. Wiring it is a real feature.
3. **Stage 9 has no card art** (`nss_panel_9` / `nss_label_9`). A text fallback stands in; drop the
   art in and that branch stops running on its own.
4. **Stage 9 has no background** — still the Water World plate. The packs shipped no void backdrop.
5. **Stage 9 is the only 800-wide plate.** Rescale to 680 or keep it deliberately?
6. **~2,829 vivid magenta px remain across 21 atlas sheets**, plus ~97 on stage 1's hull edges.
   Everything else flagged is authored art — fire bursts, pink ribbons, purple beams. See
   `docs/proofs/halo/contact_1..4.png` before touching any of it.

---

## 8. HOUSE RULES THAT WILL BITE YOU

- **Never invent placeholder or procedural sprites.** Search `_ART_SOURCES` first — that is where
  the 25 weapon icons had been sitting. If unsure which art fits, render candidates and ask.
- **Purple halos are converted to a black edge, never deleted.** Alpha is preserved.
- **Palette/luminance swaps, not draw-time overlays.**
- **No boss splits. At all.** Asked and answered twice.
- **`XART.rdy(k)` returns false on the FIRST call** — that call starts the load. A synchronous
  frame burst never yields, so lazy art never decodes. Warm anything a cutscene needs.
- **`e.art` is a NAME, not a cell key.** It needs an `ENEMY_ART` entry *and* an `<base>_idle` alias
  or the unit spawns, moves, shoots and never draws. This trap reappeared twice in one week.
- **`assets/game.js` is CRLF** (~42,000). `manifest.js` and `test_fl.js` are LF. Edit in binary and
  check the CRLF count before and after — a universal-newline read once converted 40,776 lines.
- **Find the branch that OWNS the object.** Two spawners, two switches; editing the wrong table
  changes nothing and looks like the fix failed.
- **When an assertion fails after a deliberate change, read it before fixing it.** Several encode
  Mike's earlier rulings verbatim. Repoint them at the rule and keep both quotes — 0822ag reverses
  0812l on Freezer's ice orb and says so in the file.
- **Verify with pixels.** `test_fl.js` proves state; `shoot.py` proves what is on screen. Eight
  probes were invalid earlier this week because they compared animated frames, rounded their own
  numbers, or read a world coordinate as a screen one.
