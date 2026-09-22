module.exports=function testInfusion(vm,ctxv,ok){
  var _fs=require('fs'), _path=require('path');
  var _SRC=_fs.readFileSync(_path.join(__dirname,'..','assets','game.js'),'utf8');
  vm.runInContext("var require_src;",ctxv);
  ctxv.require_src=function(){return _SRC;};
  console.log('=== 367. weapon infusions - the combination system (0917) ===');
  /* Mike, 0917: "toy around with being able to toy around with the orbs, lasers, missiles and pellet
     based weapons. Combinations could be incendiary bullets, lightning bullets, ice bullets or lasers
     or missiles. This does not apply to level 5 or level 9, space levels are in-eligible."

     Driven end to end in real Chromium by probe_infusion_0917.py (31/0) - every element through the
     live hit path, asserted on the TARGET. This section pins the table, the gates and the seams that
     have to hold for that to keep being true. */

  ok(vm.runInContext("typeof INFUSIONS==='object'&&Object.keys(INFUSIONS).length===9",ctxv),
     'nine elements in the table (chromium joined on 0917)');
  ok(vm.runInContext("['fire','ice','lightning','prism','toxic','kinetic','water','dark','chrome'].every(function(k){return INFUSIONS[k]&&INFUSIONS[k].body&&INFUSIONS[k].glow;})",ctxv),
     'each with a body colour for the round and a glow for its halo');
  ok(vm.runInContext("INFUSIONS.fire.el==='fire'&&INFUSIONS.ice.el==='ice'",ctxv),
     'fire and ice carry the ELEMENT, so the existing 2x / absorb rules apply to an infused round');

  /* ⚠ THE GATE IS THE WEAPON SET, NOT THE WALLPAPER - AND THIS ASSERTION USED TO PASS WHILE THE
     GAME DISAGREED. It moved `run.stage` alone, so the `curStage.bg==='space'` branch it was meant
     to cover never ran and stage 8 read eligible here while the real stage 8 dropped nothing
     (probe_infusion_rate_0917.py: 0 pickups in 4,000 calls). curStage MOVES WITH run.stage now.
     Three stages wear the space backdrop; only 5 and 9 hand out the space guns. */
  ok(vm.runInContext("(function(){var s=run.stage,c=curStage;var r=[];for(var i=1;i<=9;i++){run.stage=i;curStage=STAGES[i-1];r.push(infusionEligible());}run.stage=s;curStage=c;return r[4]===false&&r[8]===false&&r[0]&&r[1]&&r[2]&&r[3]&&r[5]&&r[6]&&r[7];})()",ctxv),
     'stages 5 and 9 are ineligible, every other stage is - with curStage set, so stage 8 (bg space, ordinary guns) counts');
  ok(vm.runInContext("(function(){var s=run.stage,c=curStage;run.stage=8;curStage=STAGES[7];var r=curStage.bg==='space'&&!spaceWeaponsActive()&&infusionEligible()&&INFUSION_STAGE_BIAS[8]==='prism';run.stage=s;curStage=c;return r;})()",ctxv),
     'stage 8 keeps the prism bias INFUSION_STAGE_BIAS reserves for it - a bias on an ineligible stage can never fire');
  ok(vm.runInContext("infusionPool().indexOf('water')<0&&infusionPool().indexOf('dark')<0",ctxv),
     'water and dark matter are gated off until earned');
  ok(vm.runInContext("(function(){var s=String(infusionGateOpen);return s.indexOf('laserMistIsUnlocked')>=0&&s.indexOf('ngplus')>=0;})()",ctxv),
     'water opens on the stage-9 signal LASER MIST already uses; dark matter on New Game +');

  /* ⚠ EVERY EFFECT REUSES A MECHANISM THE GAME ALREADY HAD - a second burn beside the first is
     how two flags end up sharing a name (0810q). */
  var src=String(vm.runInContext("String(infusionOnHit)",ctxv)).replace(/\/\*[\s\S]*?\*\//g,'').replace(/\/\/.*$/gm,'');
  ok(vm.runInContext("(function(){var e={x:100,y:100,hp:100};infusionOnHit(e,{_inf:'fire',_infLv:1},1);return e._burn>0&&e._burnPalette===INFUSIONS.fire.body;})()",ctxv), 'fire is the incendiary shotgun\'s own burn');
  ok(src.indexOf('_frozen')>=0, 'ice stacks the ice weapon\'s own freeze counter');
  ok(src.indexOf('chainZap(')>=0, 'lightning is Yuri\'s own arc');
  ok(src.indexOf('chromeMirror(')>=0 && String(vm.runInContext('String(chromeMirror)',ctxv)).indexOf('eBullets')>=0,
     'chromium mirrors ENEMY rounds (reads eBullets) back as the player\'s own');
  ok(/_soaked>0 && e\.hp<=0[^\n]*geyserSpawn\(e\.x,e\.y,b\._inf\)/.test(src),
     'a soaked kill by fire or lightning raises THAT element\'s geyser (Mike\'s fire / water / lightning geysers)');

  /* ⚠ THE HOOK MUST NOT RE-ENTER ITSELF. chainZap calls hitEnemy while _dmgBullet is still the
     infused round; without the busy flag a lightning hit arcs, the arc hits, the hit arcs again. */
  ok(src.indexOf('_infBusy')>=0 && src.indexOf('finally')>=0, 'the on-hit hook guards against re-entry and always releases');
  var core=String(vm.runInContext("String(_hitEnemyCore)",ctxv)).replace(/\/\*[\s\S]*?\*\//g,'').replace(/\/\/.*$/gm,'');
  ok(core.indexOf('infusionOnHit(e,_dmgBullet,dmg)')>=0, 'and it fires from the ONE place every player hit lands');

  /* the ladder */
  ok(vm.runInContext("(function(){run.infusion=null;var o=[];for(var i=0;i<4;i++){infusionGrant('fire');o.push(run.infusion.lv);}run.infusion=null;return o.join(',')==='1,2,3,3';})()",ctxv),
     'the same element levels 1 -> 2 -> 3 and caps');
  ok(vm.runInContext("(function(){run.infusion=null;infusionGrant('fire');infusionGrant('ice');var r=run.infusion.elem==='ice'&&run.infusion.lv===1;run.infusion=null;return r;})()",ctxv),
     'a different element replaces it at level 1');
  ok(vm.runInContext("infusionLabel('fire',3)==='FIREBURST'&&infusionLabel('ice',3)==='GLACIAL STRIKE'&&infusionLabel('lightning',3)==='GODS WRATH'&&infusionLabel('prism',2)==='LUMINAIRE'&&infusionLabel('prism',3)==='PRISM WAVE'&&infusionLabel('toxic',3)==='ERADICATION'",ctxv),
     'level 3 is the NAMED combination from Mike\'s list');

  /* the round wears it */
  ok(vm.runInContext("String(p87Draw).indexOf('inf')>=0&&String(p87Body).indexOf('INFUSIONS')>=0",ctxv),
     'an infused round goes through the pack with its element\'s palette');
  ok(vm.runInContext("['fire','ice','lightning','prism','toxic','kinetic','water','dark','chrome'].every(function(e){return /infusion_0917/.test(String(XART._src['inf_'+e]||''));})",ctxv),
     'all nine badges registered as loose files');

  ok(vm.runInContext("INFUSION_CARRIERS.orb===1&&INFUSION_CARRIERS.shard===1&&INFUSION_CARRIERS.beam===1&&INFUSION_CARRIERS.missile===1",ctxv),
     'the orb and its shards are carriers beside the mg, spread, beam and missiles (the WATER ORB)');
  ok(vm.runInContext("(function(){var s=String(drawBullets);return s.indexOf(\"infPal('fx0825_ice_orb',_oi.body)\")>=0;})()",ctxv),
     'an infused orb is the authored ice wheel through infPal (xartPalette with the achromatic fix) - a palette swap, never an overlay');
  /* the GIANT BEAM: kinetic on the laser widens the column, and the hit test reads the same width */
  ok(vm.runInContext("(function(){var s=String(pShoot);return s.indexOf(\"elem==='kinetic') beam.w*=1+0.5*\")>=0;})()",ctxv),
     'KINETIC on the laser widens beam.w x1.5/x2.0/x2.5 - the giant beam (probe_giantbeam_0917.py 7/0)');

  ok(vm.runInContext("(function(){var s=require_src();return s.indexOf(\"(run._kinN=(run._kinN|0)+1)%24===0)) sonicRelease(0.45)\")>=0;})()",ctxv),
     'KINETIC L3 on the mg / spread releases the sonic wave of Cole every 24th ROUND (counted on rounds, never the wall clock)');

  /* ⚠ THE PER-FRAME ZAP HARD-CLEAR MUST KEEP INFUSION BOLTS. `if(!specialActive('yuri')) zaps.length=0`
     deleted every lightning arc and every GODS WRATH bolt the frame it was born, for every pilot but Yuri. */
  ok(vm.runInContext("(function(){var s=require_src();return s.indexOf(\"if(!specialActive('yuri')) zaps=zaps.filter(z=>z._inf);\")>=0 && s.indexOf('zaps.length=0;   // hard-clear')<0;})()",ctxv),
     'the per-frame zap hard-clear keeps INFUSION bolts (tagged _inf) and clears only the zaps of Yuri');
  ok(vm.runInContext("String(godsWrath).indexOf('_inf:true')>=0 && String(chainZap).indexOf('_inf:!!_infBusy')>=0",ctxv),
     'godsWrath and an infusion chainZap tag their zaps');

  /* FUSION: a level-3 element replaced by a different one detonates once (probe_fusion_0917.py 9/0) */
  ok(vm.runInContext("infusionFusionName('fire','ice')==='THERMAL SHOCK'&&infusionFusionName('ice','fire')==='THERMAL SHOCK'&&infusionFusionName('toxic','kinetic')==='FUSION'",ctxv),
     'fusion pairs are named both ways round; an unnamed pair is a plain FUSION');
  ok(vm.runInContext("(function(){var s=String(infusionGrant);return s.indexOf('(run.infusion.lv|0)>=INFUSION_PICKUP_MAX')>=0&&s.indexOf('infusionFusion(run.infusion.elem, elem)')>=0&&INFUSION_PICKUP_MAX===3;})()",ctxv),
     'the fusion fires from infusionGrant only when a LEVEL-3 (the pickup ceiling, INFUSION_PICKUP_MAX) element is replaced by a different one');

  ok(vm.runInContext("(function(){var s=String(_newWeaponTick);return s.indexOf('_voidBeam')>=0&&s.indexOf(\"b._inf==='dark'\")>=0;})()",ctxv),
     'the VOID BEAM: a dark beam draws hostiles toward its column from the one enemy loop (carrier probe 14/0)');

  /* ARCADE KILL CHAIN: kills within KILL_CHAIN_T of each other on the STAGE clock (probe_killpoints_0917.py) */
  ok(vm.runInContext("(function(){var s=String(killChainStep);return KILL_CHAIN_T===1.2&&s.indexOf('stageTimer')>=0&&s.indexOf('performance.now')<0;})()",ctxv),
     'the kill chain runs on the STAGE clock, never the wall clock');
  ok(vm.runInContext("(function(){var s=String(killFeedback);return s.indexOf('killChainStep()')>=0&&s.indexOf(\"' x'+chain\")>=0;})()",ctxv),
     'and the floater carries the multiplier');

  /* ⚠ THE DROP ROLL IS MADE AT THE KILL SITE, NOT INSIDE dropPowerup. Behind the ordinary 18% loot
     gate the infusion landed 2.4% of drop-eligible kills - one per ~44 - and a nine-stage sweep
     measured ZERO across 229 kills. killDrop gives it its own roll, so INFUSION_DROP_P is the real
     per-eligible-kill rate and an infusion never competes with ammo / shield / life. */
  ok(vm.runInContext("(function(){var s=String(killDrop);return s.indexOf('INFUSION_DROP_P')>=0&&s.indexOf(\"dropPowerup(e.x,e.y,'infuse')\")>=0&&s.indexOf('chance(0.18*DIFF.dropMul)')>=0;})()",ctxv),
     'killDrop rolls the infusion on its own, then the unchanged 18% loot gate underneath it');
  ok(vm.runInContext("(function(){var src=require_src();return src.indexOf('if(e.dropOk && chance(0.18*DIFF.dropMul)) dropPowerup(e.x,e.y);')<0;})()",ctxv),
     'and both ordinary death paths go through that one funnel');
  /* 0917b, Mike: element badges "shouldnt ... generate in-game. they are meant for the forge screen, and when
     the boss dies as a drop." A forced 'infuse' now puts NOTHING on the field - which also means it can never
     be a pickup with nothing on it, the claim this assertion was written for. */
  ok(vm.runInContext("(function(){var st=run.stage;run.stage=1;var n0=powerups.length;dropPowerup(10,10,'infuse');dropPowerup(10,10);run.stage=st;var any=powerups.slice(n0).some(function(p){return p.kind==='infuse';});powerups.length=n0;return INFUSION_FIELD_DROPS===false && !any;})()",ctxv),
     "no element badge ever reaches the field from an ordinary drop - only the boss drops one (0917b)");

  /* death drops the element with the gun - the reset line that zeroes the weapon zeroes this too */
  ok(vm.runInContext("(function(){var src=require_src();var i=src.indexOf('manualMissileResetOnDeath(run);');return i>=0&&src.slice(i,i+400).indexOf('run.infusion=null')>=0;})()",ctxv),
     'death clears the infusion on the same line that drops the gun');
};
