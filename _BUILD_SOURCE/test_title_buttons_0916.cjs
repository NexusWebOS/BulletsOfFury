module.exports=function testTitleButtons(vm,ctxv,ok){
  console.log('=== 365. the title buttons, one generated sheet ===');
  /* Mike, 0916: "Regenerate all my other buttons here to match the current style of Bullets of
     Fury and proper reference of ships and pilots please. The help button also is too large
     compared to the rest."

     ⚠ "TOO LARGE" WAS AN ASPECT PROBLEM. titleMenuLayout measures ONE width and takes each
     row's height from its own plate, so a plate whose native aspect differs is drawn taller than
     every bar around it at the same width. Measured: the authored bars were 4.7-4.9:1 and btn_help
     was 446x112 = 3.98:1, so it drew ~23% taller. Nothing about it was big; it was the wrong
     shape, and no size tweak could have fixed it. Seven bars cut from ONE sheet share an aspect by
     construction. Driven in real Chromium by the 0916 title probe (12/0), which reads the blits
     back off the context by KEY. */

  ok(vm.runInContext("TITLE_ITEMS.length===7&&MENU_KEYS.length===7&&TITLE_ICONS.length===7",ctxv),
     'seven rows, seven plates, seven fallback icons');

  /* ⚠ TITLE_ICONS EXISTS BECAUSE THE FALLBACK WAS A FIFTH PLACE THAT KNEW THE MENU LENGTH.
     It was an inline six-entry array against a seven-row menu, so EXIT GAME drew with icon
     undefined - 0912a's "four places knew how long this menu was", one button over. */
  ok(vm.runInContext("TITLE_ICONS.every(function(i){return typeof i==='string'&&i.length>0;})",ctxv),
     'and every fallback row has an icon, EXIT GAME included');

  ok(vm.runInContext("MENU_KEYS.every(function(k){return /_0916$/.test(k);})",ctxv),
     'every row points at the 0916 sheet');

  /* ⚠ THEY SHIP UNDER NEW KEYS ON PURPOSE. btn_newgame and friends are ATLAS CELLS, and cells
     are checked BEFORE the loose-file cache (0912m), so a loose file registered under the same key
     would be silently ignored and the title would go on drawing the old plates. */
  ok(vm.runInContext("MENU_KEYS.every(function(k){return /title_0916/.test(String(XART._src[k]||''));})",ctxv),
     'each one registered as a loose file under a key no atlas cell owns');

  /* ⚠ THE LIT CUT IS WHAT SHIPS (Mike, 0916: "the lights should be palette swapped to
     different colors on the left and right sides of the button ... You also palette swap the text
     in each button to match the color of the lights"). The sheet's own cuts stay on disk
     un-recoloured so title_lights_0916.py can always re-run from a clean source - a script that
     consumes its own output is not idempotent (0907u). Pointing the keys back at the plain cut
     would silently ship the amber lamps again, with nothing else failing. The COLOURS themselves
     are canvas work and live in probe_title_0916.py, which reads them off the pixels the game
     serves; this only pins which file the game is asked for. */
  ok(vm.runInContext("MENU_KEYS.every(function(k){return /_lit\.png$/.test(String(XART._src[k]||''));})",ctxv),
     'and every row ships the RECOLOURED cut, not the sheet plate');
  ok(vm.runInContext("MENU_KEYS.every(function(k){return !(XART.cells&&XART.cells[k]);})",ctxv),
     'and no cell shadows any of them');

  /* the atlas rows stay - the pause menu and the campaign hub draw their own */
  ok(vm.runInContext("CAMP_PAUSE_BTN.some(function(b){return b.key==='btn_exit';})",ctxv),
     'the authored atlas buttons stay for the surfaces that use them');

  /* ⚠ THE GATE READS MENU_KEYS[0], NOT A KEY NAME. A hard-coded 'btn_newgame' there tests a
     plate the title no longer draws - true for ever, keeping the real art off the screen. */
  var src=String(vm.runInContext("String(drawMenuButtons)",ctxv)).replace(/\/\*[\s\S]*?\*\//g,'').replace(/\/\/.*$/gm,'');
  ok(/XART\.rdy\(MENU_KEYS\[0\]\)/.test(src),
     'the pre-decode gate asks MENU_KEYS[0], not a written-out key name');
  ok(!/rdy\('btn_newgame'\)/.test(src),
     'and no longer gates the whole menu on an atlas cell it stopped drawing');

  /* the layout is still derived, so the count lives in exactly one place */
  var lay=String(vm.runInContext("String(titleMenuLayout)",ctxv)).replace(/\/\*[\s\S]*?\*\//g,'').replace(/\/\/.*$/gm,'');
  ok(/TITLE_ITEMS\.length/.test(lay),
     'titleMenuLayout still derives its row count rather than carrying its own copy');
};
