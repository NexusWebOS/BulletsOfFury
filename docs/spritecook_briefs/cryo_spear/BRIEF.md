# SpriteCook brief — CRYO SPEAR damaged + critical

Mike, 0905: *"run cryo spear through spritecook then to get them and ask spritecook to make a 1|1
replica to make sure we dont lose too much originality"*

**Two plates are needed. Nothing else about this unit changes.**

---

## Why

`rimewall` (the kind whose NAME is CRYO SPEAR — the names are crossed in `SHIPBOSS`, see below) is
stage 3's miniboss and ships with **one** plate. Every other ship boss and mini that degrades
declares a `dmg` array; this one has no entry, because the art does not exist. So the Cryo Spear
takes its whole fight at full visual health and never shows a scratch.

`shipBossDraw` picks the plate from HP, and the thresholds are already in the code:

| HP fraction | plate |
|---|---|
| above 0.62 | `nsb_cryo_spear` (exists) |
| 0.62 and below | `dmg[0]` — **damaged** (missing) |
| 0.30 and below | `dmg[1]` — **critical** (missing) |

---

## The reference — use it as a 1:1 identity lock

`REFERENCE_nsb_cryo_spear.png` in this folder. Extracted losslessly from `atlas/mini_s3.png`
(the repack verified every cell pixel-identical), so it is the exact art the game draws.

- **256 x 256**, transparent background
- ink occupies **(22, 11) to (233, 245)** — 211 x 234 inside the canvas
- 23,023 opaque pixels

⚠ **PASS IT AS `edit_asset_id`, NOT `reference_asset_id` — I had this wrong.** Read from the
installed plugin's own skill (`skills/spritecook-generate-sprites/SKILL.md`, "Reference Roles"),
the three slots are not interchangeable:

| slot | what it means | fit here |
|---|---|---|
| `style_asset_ids` | ambient style guides — palette, proportions, rendering | no: a NEW ship in the house style |
| `reference_asset_id` | *"make a building in a similar style to this one"* | **no: a lookalike, which is what Mike asked us not to produce** |
| `edit_asset_id` | *"make this roof red"*, *"remove the sign"* — a direct modification of ONE existing asset | **yes** |

Damaged and critical ARE the same plate with armour torn off. That is an edit, not a new
generation. `reference_asset_id` would have handed back a ship that resembles the Cryo Spear, and
Mike's words were *"a 1|1 replica to make sure we dont lose too much originality"*. The two must
read as **the same ship after taking hits**, not a new ship.

⚠ **AND THEY CANNOT BE COMBINED** — the skill states `reference_asset_id` and `edit_asset_id` are
mutually exclusive (`style_asset_ids` may accompany either). One choice, and it is the edit.

The upload route is `create_asset_upload` → HTTP PUT → `finalize_asset_upload`, which returns the
`asset_id` (the same bridge the BOF2 station panels used, recorded in
`BOFII-Lost-Conquest/docs/SPRITECOOK_STATION.md`). ⚠ The upload URL and token are short-lived
secrets — never echoed, never written to a manifest, never into a passover.

---

## The convention, with a worked example

`CONVENTION_damage_states.png` shows two units in this game that already have all three states —
the RIME WALL (stage 3 boss) and the MAGMA WARD (stage 2 mini). Read it before writing a prompt.
What the pack does, consistently:

- **The silhouette, pose and scale do not move.** All three plates are the same canvas, the same
  ship, dead-on from the same angle. Only the surface changes.
- **Damage is armour LOST, not dirt added.** Panels tear off, plates crack away, hull sections
  break open. The Rime Wall's ice armour chips back in wedges; the Magma Ward's outer panels strip
  to bare frame.
- **What is underneath gets exposed** — machinery, ribs, gears, cabling.
- **The energy core survives and intensifies.** Both examples keep their glowing heart lit through
  critical; on the Magma Ward the exposed right pod becomes a second lit core.
- Critical is *more of the same*, not a different idea: same wounds, deeper.

---

## Prompts

Both generated at the reference's canvas, transparent background, top-down/dead-on to match.

**DAMAGED (shown from 62% HP down):**

> The same ice interceptor as the reference, one-to-one, after taking heavy fire. Identical
> silhouette, pose, scale and camera angle. Two or three of the cyan ice blades along the wings are
> cracked and partly broken away, leaving jagged stubs. Sections of the white hull plating are torn
> off along the left flank, exposing dark blue-grey mechanical framing and cabling underneath. Soot
> scorching around the torn edges. The central blue thruster core and the nose spear remain intact
> and still glowing. Same colour palette: white, pale cyan, ice blue, dark navy. Transparent
> background, no shadow, no ground.

**CRITICAL (shown from 30% HP down):**

> The same ice interceptor as the reference, one-to-one, critically damaged and barely flying.
> Identical silhouette, pose, scale and camera angle. Most of the ice blades are shattered to
> stumps; large sections of hull plating on both flanks are gone, exposing the internal frame,
> broken ribs and severed cabling. One thruster pod is blown open with its inner mechanism visible.
> Deep scorching and stress fractures across the remaining white plating. The central blue core
> burns brighter and more unstable than before, venting cyan light through the cracks. Same colour
> palette: white, pale cyan, ice blue, dark navy. Transparent background, no shadow, no ground.

---

## Output spec

- **256 x 256**, transparent (no baked background, no drop shadow — the game composites these)
- **Same pivot**: the ship must sit at the same place in the canvas as the reference, so the hull
  does not jump between states mid-fight. If SpriteCook returns a different crop, re-pad to 256x256
  with the ink centred on the reference's bbox (22, 11, 211 x 234) rather than rescaling the ship.
- Save as `nsb_cryo_spear_damaged.png` and `nsb_cryo_spear_critical.png` in this folder.

⚠ **`smart_crop` DEFAULTS TO TRUE AND MUST BE TURNED OFF HERE.** The plugin's own parameter table
gives `smart_crop: true, smart_crop_mode: "tightest"` as the default, and workflow-essentials says
to prefer `"tightest"` — correct for a standalone sprite, **wrong for a damage state**. Tightest
crops to the ink, so a plate that has lost a wing comes back cropped to what is LEFT and re-centred:
the ship then grows, shrinks or jumps the instant it takes a hit. The three plates are swapped in
place at one draw size, so the canvas must not move. Pass `smart_crop=false`.

## The exact call, once the tools are live

`get_credit_balance` first (workflow-essentials requires it before a multi-asset batch, and Mike
wants the cost said out loud). Then upload the reference once and edit it twice:

```
create_asset_upload(file_name="REFERENCE_nsb_cryo_spear.png",
                    content_type="image/png", pixel=true)
  -> PUT the bytes to upload_url   (short-lived secret: never echoed, never in a passover)
finalize_asset_upload(upload_token=...)  -> asset_id

generate_game_art(prompt=<DAMAGED or CRITICAL, below>,
                  edit_asset_id=<asset_id>,     # NOT reference_asset_id — see above
                  width=256, height=256,        # in range; the tool accepts 16-512
                  pixel=true, bg_mode="transparent",
                  smart_crop=false,             # ⚠ the pivot rule above
                  aspect_ratio="1:1", variations=1)
```

⚠ **`generate_game_art` IS ASYNCHRONOUS.** It returns a job, not art. Follow the returned
`poll.tool` with its exact `poll.arguments` — workflow-essentials says explicitly not to invent a
polling endpoint or fish through response fields. Take the plate from `sprite_url`, and record
`asset_id` + a `sha12` of the saved file in the project manifest so a later state edits the same
lineage instead of starting a new ship.

---

## Wiring, once the two files land

One line. `SHIPBOSS.rimewall` gains a `dmg` array, exactly like its siblings:

```js
  rimewall:      {key:'nsb_cryo_spear',         name:'CRYO SPEAR',       w:195,h:195, hp:390, pat:'s3spearburst', cd:0.88, mini:true, proj:'cryo',
                  ...
                  pats:['s3spearburst','s3spearcross','s3spearcore'],
                  dmg:['nsb_cryo_spear_damaged','nsb_cryo_spear_critical']},
```

Then register the two plates and pack them onto `mini_s3` with
`_BUILD_SOURCE/atlas_repack_0903.py`, and warm them — `warmStage` already walks `SHIPBOSS[kind].dmg`
for every ship mini, so no new warming code is needed.

⚠ **Register the art BEFORE adding the `dmg` entry.** A `dmg` key that does not resolve is the
0812c bug: the fight opens on the hull silhouette fallback instead of the plate, silently.

---

## ⚠ The names are crossed, and this is not a typo

In `SHIPBOSS`, the kind `rimewall` is named **CRYO SPEAR** and draws `nsb_cryo_spear`; the kind
`cryospear` is named **RIME WALL** and draws `nsb_rimewall_*`. Stage 3 fields `cryospear` as its
boss and `rimewall` as its miniboss. This brief is about the **miniboss** — the slim ice
interceptor in the reference image — whatever the kind string says.

---

# ✅ RUN AND LANDED — 0905

**32 credits** (2 x `gemini-3-pro-image` at 16), 346 → 314. Both plates shipped and verified in
real Chromium. Lineage and hashes: `spritecook-assets.json` beside this file.

## What Mike decided

The first damaged plate came back reading as **soot added rather than armour lost** — the opposite
of the convention above, and the ice blades the prompt asked to be "cracked and partly broken away"
were still intact. That was put to him with the render. **"looks great to me"** — so the damage
LEVEL is his call and stands. It was not re-run. Do not "fix" it later on the strength of the
convention section above; he has seen it and overruled it.

## What was wrong and was NOT a design question

Both fixed by `_BUILD_SOURCE/normalize_spritecook_plate_0905.py`, which every future SpriteCook
plate should go through:

| | generated | after normalize | authored reference |
|---|---|---|---|
| canvas | 257x274 / 266x263 | **256x256** | 256x256 |
| colours (opaque px) | 19,063 / 17,347 | **61** | 61 |
| semi-alpha px | 0 | 0 | 0 |
| ink bbox | (22,12,234,262) | (21,6,233,256) | (22,11,233,245) |

Alignment was solved by **silhouette IoU**, not bbox edges: damaged dx=-1 dy=-6 at **IoU 0.919**,
critical dx=-6 dy=-5 at **0.872** (lower because more armour is gone — the right direction), **0 px
clipped** on both. The ship was NOT rescaled; see the script's header for why forcing the height to
match would have made the boss narrower at 62% HP.

## How it is wired

Registered as **loose files** in `BOFX.img` (`assets/game/nsb_cryo_spear_{damaged,critical}.png`),
alongside `nsb_spawncarrier_*` — the repack doc records recent generations as deliberately left
loose. Folding them onto `mini_s3` is a later `atlas_repack_0903.py` pass, not required to ship.
`SHIPBOSS.rimewall` gained `dmg:['nsb_cryo_spear_damaged','nsb_cryo_spear_critical']` **after** the
art was registered, per the 0812c warning above.

## Verified, in real Chromium

`_BUILD_SOURCE/probe_cryospear_dmg.py` — proof frames in `docs/proofs/cryospear_dmg_0905/`.
It records **the art key the DRAW asked for**, because `XART.get` returns a canvas with no `.src`:

    100% hp -> nsb_cryo_spear            OK
     50% hp -> nsb_cryo_spear_damaged    OK
     20% hp -> nsb_cryo_spear_critical   OK      0 page errors

⚠ The probe polls `XART.rdy` against real elapsed time rather than checking once, because
`shipBossDraw` reads `if(_dk && XART.rdy(_dk)) _hk=_dk;` — **an unready plate silently keeps the
intact hull**, so a one-shot check reports a working swap as broken (and a missing plate as fine).
