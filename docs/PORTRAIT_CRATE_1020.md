# Framed Dracodia portrait and exclusive Hammer chaingun pickup — October 20

Mike requested an actual regenerated portrait box for Dracodia and an exclusive Hammer boss chaingun crate with a weapon pictogram instead of the I-marked generic treatment.

The built-in image_gen tool produced three assets: integrated Dracodia portrait/bezel, blue chromium Hammer crate with the rotary weapon emblem, and matching standalone chaingun emblem with no numeral. Portrait512x512; crate/icon128x128; common centered pivots and proportional exports. Masters, original native icon/crate/Hammer references and exact prompts are in `_ART_SOURCES/portrait_crate_1020`.

`assets/dracodia_dialogue_portrait_1020.js` keeps its existing DP20 key and dialogue aliases, now pointing to `assets/game/levels/stage_08/cinematics/dracodia_portrait_box_1020/portrait.webp`. The current concept portrait tab and expansion template kit were updated too; the old unframed master is retained as source history. This remains a single portrait expression, not a new lip-animation bank.

`assets/hammer_redesign_1020.js` owns two exclusive keys, `hb20_chaingun_crate_exclusive` and `hb20_chaingun_icon_exclusive`, under `assets/game/shared/pickups/hammer_chaingun_1020/`. Both Stage5 and Stage8 preload them. The boss draws the dedicated box directly, never drawScrate/player-pilot art; after the strike it draws the matching clean emblem along the existing pickup arc. Stage5 box56px, corrupted form62px; released icon36px. The weapon remains chaingun level1. Pickup logs preserve that semantic identity and separately record the exclusive art key. Strike1.78s, acquisition2.55s, transition2.85s, audio cues, hit flash and subsequent gun behavior are unchanged.

Native Edge27/27, no page/console/draw/asset errors. For each of Easy/Normal/Hard/Furious: Stage5 and corrupted Stage8 show the exclusive crate, retire it on impact, draw the exclusive released emblem and enter the native gun phase. Actual monologue and every Dracodia face/talk alias resolve to the new boxed portrait. Native screenshots inspected; see `docs/qa/portrait_crate_1020.json`. Owner JS syntax checks pass. No combat rules, game.js, tests, player pickup mappings or Overdrive edits; no commit/push.

Review: http://127.0.0.1:8794/docs/previews/portrait_crate_1020/index.html
