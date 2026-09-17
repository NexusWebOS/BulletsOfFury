module.exports=function testNgPlus(vm,ctxv,ok){
  console.log('=== 368. NEW GAME + - the sixth mode, hidden until the final clear (0917) ===');
  /* Mike, 0917: "Dark Matter ... can be only be used in New Game +, a new button you will create and
     unlock/make visible after we beat the campaign on any difficulty."

     Driven through the live screen in real Chromium by probe_ngplus_0917.py. This section pins the
     shape: one row in the table, ABSENT from the list the screen walks until the unlock, the campaign
     structure with one flag, and that flag carried by the save and dropped by a password. */
  var strip=function(s){return String(s).replace(/\/\*[\s\S]*?\*\//g,'').replace(/\/\/.*$/gm,'');};

  ok(vm.runInContext("MODE_ITEMS.some(function(it){return it.mode==='ngplus'&&it.requiresFinalClear&&it.hiddenUntilUnlocked&&it.pill==='mode_ngplus_0917';})",ctxv),
     'NEW GAME + is a MODE_ITEMS row: final-clear gated, hidden until then, on its own plate');
  ok(vm.runInContext("BONUS_MODE_PLAYABLE.ngplus===true",ctxv),
     'and it is PLAYABLE - not a development placeholder like BOSS RUSH / TIME ATTACK');
  ok(vm.runInContext("/modes_0917/.test(String(XART._src['mode_ngplus_0917']||''))",ctxv),
     'the plate is registered as a loose file under a NEW key (a cell beats the loose-file cache)');

  /* ⚠ ONE LIST, THREE CONSUMERS. The cursor, the draw loop and the confirm all read modeList(); a
     hidden row is absent from all three at once, the way INSANITY is absent from diffList(). */
  ok(vm.runInContext("(function(){var s=bonusModesUnlocked;bonusModesUnlocked=false;var a=modeList().length;bonusModesUnlocked=true;var b=modeList().length;bonusModesUnlocked=s;return a===MODE_ITEMS.length-1&&b===MODE_ITEMS.length&&modeList()[b-1]===undefined||a===MODE_ITEMS.length-1&&b===MODE_ITEMS.length;})()",ctxv),
     'modeList() drops the row while locked and carries it once unlocked');
  var src=strip(vm.runInContext("String(drawModeSelect)",ctxv));
  ok(src.indexOf('modeList()')>=0 && src.indexOf('MODE_ITEMS[')<0,
     'drawModeSelect walks modeList(), never MODE_ITEMS by index');
  ok(src.indexOf("run.ngplus = (_m==='ngplus')")>=0 || src.indexOf("run.ngplus=(_m==='ngplus')")>=0,
     'the confirm assigns run.ngplus on EVERY branch (a stale true is a Dark Matter drop in a plain run)');
  ok(/\(_m==='ngplus'\)\s*\?\s*'campaign'/.test(src) && /_m==='campaign'\|\|_m==='ngplus'/.test(src),
     'NEW GAME + is the CAMPAIGN structure - run.mode campaign, routed to the hub');
  ok(src.indexOf('modeRows(')>=0 && src.indexOf('_rows[i].y')>=0 && !/\bgap\b/.test(src),
     'the rows come from modeRows() - their own heights - and nothing reads a literal pitch');

  /* the flag is what the mode IS */
  ok(vm.runInContext("(function(){var s=String(infusionGateOpen);return s.indexOf('ngplus')>=0;})()",ctxv),
     'infusionGateOpen reads run.ngplus for DARK MATTER');
  ok(vm.runInContext("(function(){var o=run.ngplus;var st=run.stage;run.stage=2;run.ngplus=false;var a=infusionPool().indexOf('dark')<0;run.ngplus=true;var b=infusionPool().indexOf('dark')>=0;run.ngplus=o;run.stage=st;return a&&b;})()",ctxv),
     'and the drop pool carries dark only with the flag');
  ok(strip(vm.runInContext("String(campSnapshot)",ctxv)).indexOf('ngplus:!!run.ngplus')>=0 &&
     strip(vm.runInContext("String(campApply)",ctxv)).indexOf('run.ngplus=!!s.ngplus')>=0,
     'the campaign save carries it both ways');
  ok(/run\.ngplus=false/.test(strip(vm.runInContext("String(startRun)",ctxv))),
     'a password (arcade) start drops it');
};
