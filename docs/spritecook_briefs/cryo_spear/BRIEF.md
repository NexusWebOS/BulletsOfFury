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

**Pass this as the reference asset** (`reference_asset_id` in SpriteCook's API — the plugin's own
skills describe generating a hero asset first and referencing it for everything after; the same
route the BOF2 station panels used, recorded in `BOFII-Lost-Conquest/docs/SPRITECOOK_STATION.md`).
Mike's instruction is explicit: a 1:1 replica, so the ship's identity survives. The damaged and
critical plates must read as **the same ship after taking hits**, not a new ship.

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

⚠ **Do not let a smart-crop resize the ship.** The three plates are swapped in place at the same
draw size; a re-cropped plate reads as the boss growing or shrinking when it takes a hit.

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
