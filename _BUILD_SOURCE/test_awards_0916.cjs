module.exports=function testAwards(vm,ctxv,ok){
  console.log('=== 364. the awards gallery and the unlock toast (ACH-02) ===');
  /* The registry has been complete since 0915 - 66 definitions, the awards, the points, the
     persistence - and NOTHING DREW ANY OF IT: achievementUnlock set a variable and dispatched a
     window event nothing listened to, so a player could earn 1,630 points and never be told once.
     Driven end to end by probe_awards_0916.py (22/0). */

  /* ---- the seventh title button ---- */
  ok(vm.runInContext("TITLE_ITEMS.length===7&&TITLE_ITEMS.indexOf('ACHIEVEMENTS')>=0",ctxv),
     'the title carries an ACHIEVEMENTS button');
  ok(vm.runInContext("MENU_KEYS.length===TITLE_ITEMS.length&&MENU_KEYS.indexOf('btn_achievements_0916')===TITLE_ITEMS.indexOf('ACHIEVEMENTS')",ctxv),
     'its plate sits at its own index - the two tables cannot slip');
  ok(vm.runInContext("typeof XART!=='undefined'&&/title_0916\\/btn_achievements_lit\\.png$/.test(String(XART._src['btn_achievements_0916']||''))",ctxv),
     'and that plate is registered');

  /* ⚠ THE DISPATCH IS KEYED BY NAME. It was `m===0 .. m===4` with `else { tryExit(); }`, so
     inserting AWARDS before CREDITS would have repointed every row below it and made one of them
     quit the game. */
  ok(vm.runInContext("TITLE_ITEMS.every(function(t){return typeof TITLE_ACTION[t]==='function';})",ctxv),
     'every title row has its own action, by name');
  /* ⚠ COMMENTS STRIPPED. The note in the source that explains this fix contains the very string the
     next assertion looks for - "NO `else { tryExit() }`" - so an unstripped test FAILS on the fixed
     code, which is section 47's trap self-inflicted. CLAUDE.md: strip comments by default in any
     toString() assertion, not when you remember to. */
  const disp=vm.runInContext('drawTitle.toString()',ctxv).replace(/\/\*[\s\S]*?\*\//g,'').replace(/\/\/.*/g,'');
  ok(/TITLE_ACTION\[TITLE_ITEMS\[m\]\]/.test(disp.replace(/\s+/g,'')),
     'the dispatch looks the action up by label');
  ok(!/else\{tryExit\(\)\}/.test(disp.replace(/\s+/g,'')),
     'and an unrecognised row no longer quits the game');

  /* ---- the gallery ---- */
  ok(vm.runInContext("GS.ACHIEVEMENTS==='achievements'",ctxv), 'the gallery has its own state');
  ok(vm.runInContext('typeof drawAwards==="function"&&typeof awardsOpen==="function"',ctxv), 'and its own draw');
  ok(vm.runInContext('AWARDS_VIEW===8',ctxv), 'eight rows at a time');
  const rows=vm.runInContext('awardsRows()',ctxv);
  ok(rows.length===Object.keys(vm.runInContext('ACHIEVEMENT_DEFS',ctxv)).length,
     'it lists every definition ('+rows.length+')');
  ok(rows.length===66, 'which is 66');
  /* ⚠ SORTED, because ACHIEVEMENT_DEFS is built pilot-then-stage and its raw order interleaves
     100-point campaign clears with 10-point stage clears and reads as noise */
  ok(rows[0].family==='campaign_clear'&&rows[0].points>=rows[rows.length-1].points,
     'sorted by family and then by points (first '+rows[0].family+' '+rows[0].points+')');
  const da=vm.runInContext('drawAwards.toString()',ctxv).replace(/\/\*[\s\S]*?\*\//g,'').replace(/\/\/.*/g,'');
  ok(/unlocked\?/.test(da.replace(/\s+/g,'')), 'a locked row is dimmed, not hidden - the gallery is a list of things to go and do');
  /* up and down are each read once - they consume their tap */
  const inp=da.replace(/\s+/g,'');
  ok(/constup=\(Input\.menuUp/.test(inp)&&/dn=\(Input\.menuDown/.test(inp), 'up and down are read into locals');
  ok(inp.indexOf('dn=(Input.menuDown')<inp.indexOf('if(dn)'), 'before either is acted on');

  /* ---- the toast ---- */
  ok(vm.runInContext('typeof achToastPush==="function"&&Array.isArray(achToasts)',ctxv), 'the toast is a QUEUE');
  ok(/achToastPush/.test(vm.runInContext('achievementUnlock.toString()',ctxv)),
     'and every unlock pushes one');
  /* ⚠ A QUEUE AND NOT A SLOT: a stage clear can award seven at once, and one slot would show the
     last and silently drop six. */
  vm.runInContext("achToasts.length=0;['a','b','c'].forEach(function(t){achToastPush({title:t,points:10});});",ctxv);
  ok(vm.runInContext('achToasts.length===3',ctxv), 'three at once queue three');
  ok(vm.runInContext('ACH_TOAST.slide>0&&ACH_TOAST.hold>0&&ACH_TOAST.out>0',ctxv),
     'it rises, holds and leaves rather than blinking on and off');
  vm.runInContext('achToasts.length=0;',ctxv);

  /* ---- the tabs and filters (Mike, 0916) ---- */
  ok(vm.runInContext("AWARDS_TABS.map(function(t){return t.key;}).join(',')==='all,type,enemy,pilot,status'",ctxv),
     'the gallery carries a tab per axis Mike named - type, enemy, player, completion');

  /* \u26a0 THE VALUES ARE DERIVED FROM THE ROWS, NOT HAND-LISTED. This file's history is why:
     _selfPat, the edge-pin exemption list and the separation list were each a hand-written list
     that went stale the moment something new arrived. A family added later must appear on its own. */
  ok(vm.runInContext("awardsTabValues('type',achievementList()).length>=8",ctxv),
     'TYPE offers one value per family, derived from the rows');
  ok(vm.runInContext("(function(){var L=achievementList();var fams={};L.forEach(function(r){fams[r.family||'other']=1;});"+
                     "var vals=awardsTabValues('type',L).map(function(q){return q.v;});"+
                     "return Object.keys(fams).every(function(f){return vals.indexOf(f)>=0;});})()",ctxv),
     'and no family in the list is missing from the tab');

  /* \u26a0 "ENEMY" IS THE ENCOUNTER AXIS. Beating stage 4 without dying is about the STAGE; beating
     its boss on Furious is about the BOSS. Offering every row that carries a stage would just be
     STAGE CLEAR under a second name. */
  ok(vm.runInContext("achievementList().filter(awardsIsEnemyRow).every(function(r){return r.family==='boss_difficulty'||r.family==='boss_speed';})",ctxv),
     'ENEMY offers only the rows won against a unit');
  /* \u26a0 AND THE FOUR STAGE-1 SPEED AWARDS HAD NO `stage`, SO THE TAB COULD NOT SEE THEM. Their
     ids and titles said "Stage 1" and their definitions did not - the filter was right and the data
     was short a field. */
  ok(vm.runInContext("['stage1_boss_under_60','stage1_boss_under_120','stage1_miniboss_under_60','stage1_miniboss_under_120']"+
                     ".every(function(id){return ACHIEVEMENT_DEFS[id]&&ACHIEVEMENT_DEFS[id].stage===1;})",ctxv),
     'and the four stage-1 speed awards say which stage they belong to');
  ok(vm.runInContext("awardsTabValues('enemy',achievementList()).filter(function(q){return q.v===1;}).length===1",ctxv),
     'so stage 1 appears exactly once on the ENEMY axis');

  ok(vm.runInContext("(function(){var L=achievementList();var a=L.filter(function(r){return awardsMatch(r,'status','done');}).length;"+
                     "var b=L.filter(function(r){return awardsMatch(r,'status','todo');}).length;return a+b===L.length;})()",ctxv),
     'STATUS splits the gallery in two with nothing lost between them');
  ok(vm.runInContext("achievementList().every(function(r){return awardsMatch(r,'all',null);})",ctxv),
     'and ALL filters nothing out');

  /* \u26a0 EVERY GRANT RECORDS WHO WAS FLYING, AND ONLY ONE OF THEM USED TO. The only pilot anywhere
     in this system was the `pilot` field on the nine campaign-clear DEFINITIONS, so a pilot filter
     could only ever have shown one row per pilot. achievementMeta is the funnel. */
  ok(vm.runInContext("typeof achievementMeta==='function'&&!!achievementMeta({}).difficulty",ctxv),
     'one funnel builds every grant meta');
  ok(vm.runInContext("(function(){var p=run.pilot;run.pilot='cole';var m=achievementMeta({stage:3});run.pilot=p;"+
                     "return m.pilot==='cole'&&m.stage===3;})()",ctxv),
     'and it records the pilot, so the PILOT tab can attribute what gets earned from here on');
  var src=String(vm.runInContext("String(achievementStageComplete)+String(achievementEncounterDefeat)+String(achievementWeaponMax)",ctxv));
  ok(src.split('achievementMeta(').length-1>=3,
     'the stage, encounter and weapon grants all go through it');
};
