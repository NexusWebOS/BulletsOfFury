# Boss Mode — the boss fight editor (drop 0910a)

Open `bossmode.html` from the same folder as `index.html` (over http; `python -m http.server` in the
repo root is enough). The editor hosts the **real game** in an iframe (`index.html?bossmode=1`) and
drives it through `window.BOSSMODE`, so PLAY TEST is the shipping boss loop with your edits laid on.

```
bossmode.html                 the page
assets/bossmode/bossmode.js   the editor
assets/bossmode/bossmode.css  layout; the atlas-backed rules are generated at boot from the maps
assets/bossmode/ui/           CF_BossModeAssets-Vol.1: atlases + maps, boot/cover plates, 32px cursors
```

## The layout (0911b — theater)

```
 RAIL   |                 THEATER  (~75-80% of the width)                 |   DOCK (340px)
 stage  |  the view: stage / plate / scene / art / json / clips           |   INSPECTOR, or the
 plate  |                                                                 |   SCENE inspector on
 scene  |  [BOSS LIST]  a drawer that slides over the theater (L)         |   the SCENE tab
 ...    |                                                                 |
```

| key | what |
|---|---|
| **L** | the BOSS LIST drawer (also the LIST tab at the bottom of the rail); picking a fight closes it |
| **Tab** | fold / unfold the inspector dock (the `‹` pull tab on the right edge brings it back) |
| **T** / **F11** | THEATER — the dock and the drawer drop, the view has everything but the rail |
| F5 / F6 / Ctrl+S | play test / stop test / save |

The dock and theater state are remembered in `localStorage.bof_bm_layout`. The viewport reads
76% of a 1600px window and 80% of 1920px with the dock open, 97% folded. Under 1750px the header's
BOSSES / INSPECTOR / THEATER buttons drop to icons.

`assets/bossmode/scene.js` builds the SCENE pane and puts its inspector into `#dock-scene`;
`body[data-tab]` (set by `selectTab`) decides which inspector the dock shows.

## The document (`bof-bossmode/1`)

One fight, as `bossmode_<kind>.json`:

| field | live in the engine? | what it maps to |
|---|---|---|
| `name` | yes | `SHIPBOSS[kind].name` |
| `states[0..2].key` | yes | `key`, `dmg[0]`, `dmg[1]` — intact / damaged / critical plates, swapped at 66% / 33% |
| `states[].at` | data | the HP fraction you *intend* each state at (engine rule is even thirds) |
| `size.w/h` | yes | the hull hit box AND the drawn size |
| `size.ty/drawW/drawH` | yes | hover height, drawn size overrides |
| `hp.hp` / `hp.hpMul` | yes | absolute HP × `DIFF.eHp`, or a multiplier of the stage seed |
| `move` | yes | `ampX / ampY / period / orbit` patrol |
| `anchors` | yes | `mounts` — hull fractions from the plate centre, +Y toward the nose (south) |
| `actions.pat/cd/proj` | yes | fallback pattern, cooldown, `bfx_<proj>` family |
| `actions.pats[]` | yes | the phase list; the fight walks it as the bar drains (`shipBossPhase`) |
| `phases` | derived | shown from `pats`, not stored |
| `hitboxes[hull]` | yes | = `size.w/h`; extra boxes are **data only** |
| `parts[]` | data | planned sub-parts — the engine draws ONE plate (Mike's no-splits rule) |
| `orientation` | data | facing / rotation for the design record; every ship boss draws nose-south |
| `notes` | data | free text |
| `scene` | yes | the SCENE tab: `{grid:{cell,w,h}, ownFire, tracks:[...], zones:[...]}` - consumed by the scene director in `assets/game.js` |

`SAVE` applies the live subset as an override (`localStorage.bof_bossmode`) and keeps the whole
document (`localStorage.bof_bossmode_docs`). `EXPORT` / `SAVE AS` download the document;
`EXPORT ALL OVERRIDES` (JSON tab) bundles every override for hand-off. `IMPORT` takes either.

**A normal boot never applies overrides** — blank game state. The host applies them itself; in the
game, the debug menu's **F4 EDITOR OVERRIDES** arms them for the session.

## The engine surface (`window.BOSSMODE`, in `assets/game.js`)

`fights()`, `tables()`, `start(stage, role, pilot, record)`, `stop()`, `pause(on)`, `snapshot()`,
`kill()`, `setBossHp(v)`, `setInvuln(on)`, `setTimeScale(v)`, `patternSlots(pat, step)`,
`override.{apply,reset,arm,get,all,stock,live}`, `art.{rdy,raw,keysFor,cell,img}`,
`rec.{start,stop,active,last}`. `BOSSMODE_ONREC(clip)` on the host window is called when a
recording finishes.

## Debug mode in the game

Title screen: **UP UP DOWN DOWN A B C** (keyboard) → the DEBUG button (top-right; F2 also opens
it). Pick any mini / boss; the fight ends back on the menu. **R** records to a `.webm` in Downloads;
**F3** records every fight; **P** replays the last clip; **E** opens this editor.
`index.html?debug=1` unlocks it for a harness.

The clip is the **whole cabinet** — the score/lives/bombs strip and the EQUIPPED box composited
above the play field, in shoot.py's own layout, with the REC clock burnt in. Video only: the music
plays through HTMLAudio elements that are not all routed through one `AudioContext`, so there is no
single node to tap for the audio track.

Probes: `_BUILD_SOURCE/probe_debugmode.py`, `probe_bossmode_editor.py`, `probe_scene_editor_0911a.py`,
`probe_theater_0911b.py` (the layout: shares, drawer, dock, theater, persistence).
