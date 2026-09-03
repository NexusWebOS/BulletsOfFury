# ATLAS REPACK 0903 — one named sheet per thing

Mike (0902/0903): *"all stage 1 enemies, stage 2, stage 3 get their own atlas's. every boss and
mini boss get their own atlas sheet. all fx's like clouds, lightning, rain get their own atlas. all
player weapon projectiles get their own atlas. all player boxes, pills, weapon pick up icons and
specials get their own atlas. all enemy projectiles per stage get their own atlas sheet... Then,
delete old atlas's that no longer serve purposes or graphics we're never going to use. Do not
confuse this with recent generations."* — and, after the failed first attempt: *"please do a full
atlas repack."*

Tool: `_BUILD_SOURCE/atlas_repack_0903.py` (`--plan` to see, `--write` to do). Everything below
was produced by it in ONE pass: sheets, cell table, img registrations, PRELOAD patch, then a
pixel-identity check of every live cell before the manifest was touched.

## What a sheet index is now

`BOFX.cells` rows are `[sheet, x, y, w, h]` and the loader resolves the sheet as `'nca_'+sheet`.
Since 0903 the sheet is a NAME: `['en_s1', 12, 40, 96, 96]` reads `assets/game/atlas/en_s1.png`
through the img key `nca_en_s1`. `nca_s1combatfx` and the stage runtime atlases already used
this route, so the loader did not change. **The only numeric sheets left are `nca_87/88/89`** —
the MG/spread projectile pack, which `P87_SHEET` indexes whole and which stays untouched.

## The sheets (58 files, 219.8 MB — was 85 numbered files, 271.1 MB)

| sheet | holds |
|---|---|
| `en_s1` … `en_s7`, `en_s9` | enemy hulls per stage — from `ENEMY_ART` × each stage's plan, `VAULT_AIR_STAGE`, `'n6x_'+kind` (stage 6), `'nvl_'+art` (stage 2), `JUNGLE_TANKS`/`STAGE4_TANKS`, the stage-1 roster camo. Stages 6/8 field mostly runtime-atlas art already (`stage_runtime/`), so their sheets are small or absent |
| `en_shared` | the arsenal drones (`ndr_`, `ndt_`, `tnkG_`, `tk4_`) that several stages field |
| `boss_s1/2/3/5/6/9`, `mini_s2/3/4/6/9` | the LIVE boss and miniboss hulls, from `SHIPBOSS[kind].key/dmg` for the kinds `STAGES`/`SUBBOSS` name, plus stage 1's legacy chopper set and stage 6's carrier frames. Stages 4/7/8 bosses and minis 1/5/7/8 are code-registered loose packs (recent generations) and were left alone |
| `eproj_s1…s9`, `eproj_shared` | enemy projectiles: `bfx_<fam>_` by the stage whose boss fires that family (`SHIPBOSS.proj` + `bossVisualFamily`'s fallback); `mfx_`, `waf_`, `nio_`, `nbk_`, `ndc_` shared |
| `player_weapons` | every player projectile / special / charge / muzzle family (helix, flamethrower, laser, chain, orbs, shards, rollers, helix bomb, Decker, Axel) |
| `pickups` | crates, pills, powerups, missile boxes |
| `fx_weather` (3) | clouds, rain, snow, bolts, the stage-6 cloud plates, liquids' surface fx |
| `fx_explosions`, `fx_misc`, `fx_debris` | blasts, smoke, rings, shock rings, sparks, chunks; the 1,024-key debris library (built as `ramp+type+chunk+'_r'+rot+'_'+tier`, which no grep can see) |
| `terrain_liquids`, `terrain_masters` (3), `terrain_props` (2) | liquid reels, stage masters/uppers/planets, props, connectors |
| `ui_menu` (2), `ui_hud`, `ui_dialogue`, `ui_map` (2), `pilots` (2), `cinematic`, `misc` | the rest, by surface |
| `retired_rigs` (3) | **kept for Mike's decision, loaded by nothing at boot**: the sectional packs (`nsx_`, `nobd_`, `nglr_`, `nlgt_`, `nmrv_`, `nslc_`, `nrmp_`, `ntxl_`, `ncyc_`), the unassigned quad-laser (`nqx_`/`nql_`), the megaboss hulls `bz0-6`, the `esB_` minibosses, the ironrev/vault modular sets (`mbp_`, `mbv_`). No stage can spawn any of them; the suite still pins their registration (sections 104/105/136/160/190/202) and CLAUDE.md says the sectional rig stays on disk. 36 Mpx. One line in `atlas_repack_0903.py` moves them to the quarantine |

Boot download: **34 atlas files / 134.3 MB → 17 files / 101.9 MB** (`scratchpad/bootsheets.py`,
same measurement both times). The boot sheets are now exactly the surfaces the opening draws.

## Folded loose files

286 manifest-registered loose PNGs became cells (live boss hulls `nsb_*`, `ndam_*`, the stage-9
pack `ns9*`, the pilot intro plates, the stage-6 cloud and stage-5 planet plates, the warp portal
reel, the three campaign buttons). **262 of those files were then unreferenced by anything and were
deleted (23.3 MB)** — two stage-6 cloud plates stay because game.js names them as the fallback for its `cincloud_*` aliases — list in `docs/proofs/atlas_repack_0903/folded_loose_deleted.json`. Plates
over 2048px on a side (masters, uppers, the neon city, the starfield) stay loose.

## Quarantine — 2,345 keys in 51 families, out of the shipped manifest

`docs/ATLAS_QUARANTINE_0903.json` carries every removed key's old cell row and the commit the
sheets can be restored from (`0c964ee3`). Contact sheets of the largest families are in
`docs/proofs/atlas_repack_0903/quarantine_<family>.jpg` — rendered, not inferred (rule 1).

Two kinds of evidence, and only two:

- **Retired mech rigs (unreachable).** `spawnBoss`/`spawnSubBoss` are table-driven; the only kinds
  that can reach them are `STAGES[].boss` and `SUBBOSS[].kind`. None of those route to `mechInit`
  (`_SXMAP` names only `magmacolossus`, `cryobehemoth`, `leviathan`). So the twelve `mb*` mech rigs
  (Magma Colossus, Cryo Behemoth, Glacier Fortress, Obsidian Drill, Warhawk, MIRV Stalker, Rampart
  Zero, Legion Tank, Cyclone Escort, Storm Sovereign's old rig, Sludge Crawler, Toxic Leviathan),
  the Colossus arena pieces `nqm_`/`nqv_`, the loose mech gun set `mgx_`, their `nfx_<boss>_` fx and
  gravity mode's four pre-atlas weapon reels went. **~215 Mpx of the 316 MB was mech art no stage
  can spawn.** Mike scrapped the Colossus and the Behemoth himself (0810q); the rest were never
  assigned. Without their art `mechInit` refuses and the spawn falls to the generic hull — the suite
  fixtures that spawn those kinds now assert that instead of reading `boss._mech`.
- **Nothing names it.** No quoted family prefix in game.js in any quote style, no manifest-table
  mention, no exact key literal, not drawn in either live-run audit. `sfontA` (a font in seven
  palettes — the live faces are `sfontnew`/`sfontv3`/`bof_font`), `nhxm` (an older helix mesh),
  `nbm`, `nsf`, `nab`, `ncl6` (its own comment says the keys "were never registered under" the
  names the code uses), `nchl`, the `nbb1-8`/`nmb1-8` per-stage bar fills, `trt` (turrets Mike
  removed), and the rest of the list in the JSON.
  Families under 40,000 px and 12 keys were KEPT in `misc` even with no evidence — a blank costs
  more than the bytes.
- **Kept despite no code reference (`KEEP` in the script):** the stage-6 sky units and Tempest
  Missile Wall (`n6e_`/`n6w_`, now on `en_s6`), the alternate liquid falls (`nlqf_`), the vile
  morph fx (`nvx_`), Falva's fade-in frame sets Mike asked for (`nhxfi_`/`nrbfi_`, suite section
  184), the 60 spread-fire frames (`nsf_`), the six thruster types (`nthr0-5`) and the helix laser plate (`nmvh`). The suite asserts each is registered; they are authored
  art awaiting wiring, not scrapped art. The first pass quarantined them and section 184 crashed on
  `nrbfi_0` — the cross-check that caught it is now part of the procedure (grep the suite for every
  quarantined family before writing).

**Restore recipe:** `git checkout 0c964ee3 -- assets/game/atlas/nca_<N>.png`, then put the cell row
from the JSON back into `BOFX.cells` (its `[0]` is `<N>`) and `"nca_<N>"` back into `BOFX.img`.

## Verified

- `atlas_repack_0903.py --write`: **6,839 cells checked, 0 pixel mismatches** between old and new
  sheets, before the manifest moved.
- `node _BUILD_SOURCE/verify_atlas_0806z.js`: all 6,990 cells resolve, true sizes, no bleed; all
  eight stages play 100 s with **0 blank fallthroughs**. (VICTORY "drew nothing" is the same
  pre-existing result the tool gave before the repack.)
- `node --check assets/game.js` clean. PRELOAD's roster clause is `nca_(?:s1combatfx|en_s1|8[7-9])`.
- Real Chromium (`scratchpad/verify_repack.py`): screens in `docs/proofs/atlas_repack_0903/v*.png`,
  blank/error report in `verify_report.json` — see the commit message for the numbers.

## Traps this cost

- **Sheet 79 was `stage1roster.png`, not `nca_79.png`.** Resolve a numeric sheet through its
  `img['nca_N']` registration, never by building the filename. The first cut would have crashed
  on it — or worse, silently skipped 38 stage-1 cells.
- **A quoted heredoc is not safe from the harness's shell.** A regex character class containing a
  backtick broke a 400-line script write at line 117. Keep backticks out of source that passes
  through a shell (`'\x60'`), or write the file with the Write tool.
- **`n6x_`/`nvl_`/`s1_`/`tk*` are built by the code, not named by the tables**, so the table-driven
  pass put 471 stage-owned keys in `misc`. Rule 1 on the residue (render, read the draw function)
  moved them home; `misc` is 114 keys now.
- **The live-run audit wedges the renderer if a stage is stepped in long synchronous bursts.** The
  0903 audit ran 45 minutes with zero output and had to be killed; the 0902 audit (short bursts)
  was used instead. Pace with `wait_for_timeout` between bursts of ≤150 frames.
