# DROP 0814E — THE "HITBOX SQUARE" MINIBOSS IS STAGE 8, AND IT WAS WEARING ITS OWN PROJECTILE

> Tester, standing item: "the miniboss that is still a hitbox square (stage not identified)."

## 1. IDENTIFIED BY SPAWNING ALL EIGHT AND READING THE PIXELS

`_BUILD_SOURCE/probe_minibosshull_0814e.html` (`?stage=<n>`) spawns each stage's own `SUBBOSS` kind,
parks it in frame for ~6 simulated seconds — past any lazy decode, the 0812c trap — and screenshots.
Stages 1–7 all draw full authored hulls. **Stage 8's HERALD OF DEATH drew two giant green blobs.**

## 2. THE HERALD NEVER HAD A BODY

Three measurements, all on main @ cbffa29:

- **`mba_vr_*` — 0 registered keys.** The plates `buildModularBoss` asks for exist nowhere: not the
  manifest, not `assets/game/`, not `_ART_SOURCES`. 0812c's "routed around, not resolved"
  understated it; there is nothing to resolve.
- **`nvr_*` — 0 keys.** The flight reels were never built; `heraldAnimKey`'s own 0801ga comment
  admits it.
- **`nev_venom_0_0..10`, rendered** (`probe_heraldart_0814e.html`): NOT a flight loop. It is the
  venom ATTACK stream — twin droplets (frames 0–3) twisting into a helix (4–7) into 203x314 spray
  columns (8–9), then a 14x18 residue speck (10). The herald's idle body was frames 0–3 of its own
  projectile at 165px.

⚠ **AN IoU AGAINST NOTHING PROVES NOTHING.** The code claimed "silhouette IoU 1.0000 against the
composited clean components" — the composited clean components are EMPTY, so any overlay scores
1.0000 against them. A verification whose reference set can be empty is not a verification.

⚠ **RULE 1 WOULD HAVE CAUGHT THIS IN ONE RENDER.** The family is named nev_VENOM and the enemy fire
table's comment upstream correctly calls it "the Herald's attack reel". The name was believed over
the pixels in the one place it happened to be accurate.

## 3. THE FIX WAS SITTING IN THE LOCK PACK

`CF_BOFFinalArtLock-Vol.2/Enemies/Stage08/spawn_carrier_miniboss/` — 256px canvas, facing down,
intact/damaged/critical, ellipse hitbox in `enemy.json`. The SAME triplet convention magmaward,
rimewall and olivewarden were already integrated from: **stage 8 was the last miniboss not yet
migrated from the lock, which is exactly why it was the last one broken.**

Wired identically to its siblings — three PNGs as `nsb_spawncarrier_*`, three manifest entries, one
`SHIPBOSS` row (`mini:true`, absolute hp, `dmg[]`), one line in the spawn-arm case list, and
`SUBBOSS[8]` repointed. `warmStage` warms it through `SHIPBOSS[kind].key` with no new code — the
0812f table-driven warm doing its job for a unit added two drops later.

**Verified in pixels**: the probe re-run on stage 8 shows the full purple hull, the SPAWN CARRIER
name banner, the health bar, and its `void` volley in flight. Parse: game.js and test_fl.js both OK.

## 4. DECISIONS TAKEN, AND WHOSE THEY ARE

- **hp 340** — above blacksteel's 327 (stage 6); ratking measures 456 effective. The mini HP curve
  across stages is Mike's to retune.
- **`pat:'void'`, `pats:['void','mslfan']` — MY pick** for stage-8 flavour. The herald's venom
  stream is authored attack art and could become a spawncarrier pattern later; nothing here uses it.
- **The herald code stays, unassigned** — spawn arm, `heraldAnimTick/Key`, all of it — the
  magma/cryo precedent. Retiring it via `DEAD_SUBBOSS` would be wrong: that clears the gate and
  skips the fight entirely.
- **Name per the pack** ("SPAWN CARRIER"). If Mike wants the HERALD OF DEATH name kept on the new
  hull, it is one string in the SHIPBOSS row.

## 5. WHAT THE PACKS CHANGE ABOUT THE OPEN LIST — INVENTORIED, NOT INTEGRATED

Seven packs were delivered this session. Beyond this drop's miniboss:

- **`CF_BOFFinalArtLock-Vol.2`** (829 entries, 90MB) is a full stages-4–9 art lock: 104 enemies
  with damage triplets, boss rebuilds for 4–9 (**stage 8's boss has 4 authored forms** — bears
  directly on "stage 8 boss: 4 forms, same pattern, very tanky"), stage 9's boss chain, the stage-6
  M.A.D. Sky Citadel with an 11-section damage contract, and the complete Shadow Blast weapon
  family. Its README declares itself the authoritative metadata layer.
- **`CF_Stage9BonusPack-Lvl9`** — Velocity Gate Core boss, Twin Portal Warden minibosses, comet
  debris: the stage-9 roster.
- **`CF_Stage9PortalCombatPickups-Lvl9`** — warp rings/portal fills: the level-9-through-level-5
  mechanism's art.
- **`CF_StoryCutscenes-Vol.1`** — six prologue masters + Runtime-640x480 + a CLAUDE_HANDOFF.md.
- **`CF_FuryHQCutscenes-Vol.1`** — per-pilot HQ room masters.
- **`CF_FreezerThermoshockAttack-Vol.1`** — thermoshock charge/components with its own handoff;
  overlaps the `nts_` family 0814a wired, so integrating it must start by diffing against what is
  already in.
- **`CF_BOFFinalArtSources-Vol.2`** — FF00FF source boards, including the Blacksite Overlord and a
  legacy Shadow Blast archive.

Each is its own drop or several. Read each pack's own CLAUDE_HANDOFF/README before integrating.
