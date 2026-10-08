# Boss bars and Dracodia's knight / Code Hammer forms — October 8, 2026

Mike: "bosses got upgraded boss bars. the shields no longer get a seperate giant bar, but instead can be the sub
bar of a boss bar of our generations. #2, hammer boss still gets 2x boss bar. It fills and then fills over in Gray.
Stage 8 3rd phase boss, same deal. Should stack Red first, then dark gray, then green, then light gray, then
yellow, then black, then orange, red/purple mix. if any enemies utilize a shield, use the boss bar with the shield
version. When we switch forms, he gets a full hp bar per form, but that is 1 of his 8 health bars. The sword knight
and hammer forms he has, are very very underwhelming compared to the actual hammer boss. Also, he was stuck on the
knight form after i destroyed all other forms and unbeatable."

Two new layers, loaded last (after `player_hud_1008.js`). `assets/game.js` is untouched.

## `assets/boss_bars_1008.js`

- **Shields** use only the generated stage frames' `bossShield` / `miniShield` sub-bar (enemy_hud_1007c). The old
  separate shield plate (`drawShieldBarArt`) is retired; Dracodia's code-wall/knight barrier (`_r30.shield`) now
  reports through `bossShieldFrac`, so his third encounter wears the shield frame for the whole fight.
- **Hammer (Stage 5) 2× bar**: the chromium armour is painted as a grey second fill over the live HP — it fills in
  during the activation and drains first. The generated frame had bypassed the old overlay, so it had been missing.
- **Dracodia's stacked bar**: one layer per pool still alive, the active one draining on top, the next colour
  showing beneath, and an `X n` count of bars left. Stack bottom→top: red, dark gray, green, light gray, yellow,
  black, orange, red/purple mix — plus his own body pool on top in the Stage 8 purple. The game carries **nine**
  pools (Dracodia + eight copied forms: chopper, furnace, cryo, storm, knight, harrier, warden, Code Hammer), so the
  ninth layer is his own; each form switch shows that form's full bar as one of the stack.
  Greys and black are the authored grey plate darkened/lightened in the well — `xartPalette` keeps the plate's
  luminosity, so '#202020' and '#d0d0d0' would otherwise render as the same mid grey.

## `assets/finale_forms_1008.js`

Measured on the live game before the change: the knight and Code Hammer drew at 0.68 / 0.76 of their cells (about
half the real Hammer on screen) and spent most of a fight as solid white hit-flash silhouettes; the Code Hammer
took **0 damage in 38 s** of continuous Normal fire (armour = its whole pool, plus the source Hammer's heal), and
every copy rotates home on a 38/44 s timer — so a Code Hammer left as the last pool could only loop back into itself.

- Knight ×1.42, Code Hammer ×1.38, scaling the whole rig so hit boxes, blade lines and muzzles match the picture.
- The white hit flash on the third encounter is a flicker capped at 58% instead of a solid silhouette.
- Knight: shorter recovery between moves (0.8 / 0.6 / 0.45 s), a radial code shockwave where every leap lands
  and every shield smite finishes (a gap is left away from the player), and a new **Blade Tempest** every third
  move — a committed, colour-stepped lane warning, then a spinning sweep across the whole arena spilling code
  rounds, ending in a shockwave.
- Code Hammer armour is 35 / 40 / 45% of its pool (Normal / Hard / Furious) instead of 100%.
- A copied form may heal once per fight; the last pool alive never heals and never rotates away.

## Verification (native Chromium, real damage routing, invulnerable test pilot)

- Lone Code Hammer, Normal, level-5 machine gun, no damage multiplier: dies in 35 s (was 0 damage in 38 s).
- Lone Code Hammer, Furious: dies in 110 s, 0 heals. Lone knight, Furious: dies in 40 s.
- Full finale Normal and Hard runs (3× damage) reach the death sequence through every pool.
- Bar captures: the stack draining red/purple → orange → black → yellow → light gray, the shield sub-bar on the
  knight, the Hammer's grey fill-over during activation, and Stage 2/4 boss and miniboss frames unchanged.
- Zero page or console errors. These are protected fixtures, not human balance sign-off.

Not reproduced: a knight that could not be damaged. Every knight scenario tried (direct, after rotation, with sword
and shield broken, Normal and Furious) died normally; the reproducible unbeatable loop was the Code Hammer as the
last pool, which is what this fixes. If the knight lock recurs, the difficulty and the forms killed before it will
pin it down.
