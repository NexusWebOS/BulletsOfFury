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

  ok(vm.runInContext("typeof INFUSIONS==='object'&&Object.keys(INFUSIONS).length===8",ctxv),
     'eight elements in the table');
  ok(vm.runInContext("['fire','ice','lightning','prism','toxic','kinetic','water','dark'].every(function(k){return INFUSIONS[k]&&INFUSIONS[k].body&&INFUSIONS[k].glow;})",ctxv),
     'each with a body colour for the round and a glow for its halo');
  ok(vm.runInContext("INFUSIONS.fire.el==='fire'&&INFUSIONS.ice.el==='ice'",ctxv),
     'fire and ice carry the ELEMENT, so the existing 2x / absorb rules apply to an infused round');

  /* ⚠ THE GATES ARE STAGE RULES, NOT A LIST OF STAGES. run.stage 5 and 9 and any space stage. */
  ok(vm.runInContext("(function(){var s=run.stage;var r=[];for(var i=1;i<=9;i++){run.stage=i;r.push(infusionEligible());}run.stage=s;return r[4]===false&&r[8]===false&&r[0]&&r[1]&&r[2]&&r[3]&&r[5]&&r[6]&&r[7];})()",ctxv),
     'stages 5 and 9 are ineligible, every other stage is');
  ok(vm.runInContext("infusionPool().indexOf('water')<0&&infusionPool().indexOf('dark')<0",ctxv),
     'water and dark matter are gated off until earned');
  ok(vm.runInContext("(function(){var s=String(infusionGateOpen);return s.indexOf('laserMistIsUnlocked')>=0&&s.indexOf('ngplus')>=0;})()",ctxv),
     'water opens on the stage-9 signal LASER MIST already uses; dark matter on New Game +');

  /* ⚠ EVERY EFFECT REUSES A MECHANISM THE GAME ALREADY HAD - a second burn beside the first is
     how two flags end up sharing a name (0810q). */
  var src=String(vm.runInContext("String(infusionOnHit)",ctxv)).replace(/\/\*[\s\S]*?\*\//g,'').replace(/\/\/.*$/gm,'');
  ok(src.indexOf('_burn')>=0&&src.indexOf('DK_BURN_TIME')>=0, 'fire is the incendiary shotgun\'s own burn');
  ok(src.indexOf('_frozen')>=0, 'ice stacks the ice weapon\'s own freeze counter');
  ok(src.indexOf('chainZap(')>=0, 'lightning is Yuri\'s own arc');

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
  ok(vm.runInContext("['fire','ice','lightning','prism','toxic','kinetic','water','dark'].every(function(e){return /infusion_0917/.test(String(XART._src['inf_'+e]||''));})",ctxv),
     'all eight badges registered as loose files');

  /* death drops the element with the gun - the reset line that zeroes the weapon zeroes this too */
  ok(vm.runInContext("(function(){var src=require_src();var i=src.indexOf('manualMissileResetOnDeath(run);');return i>=0&&src.slice(i,i+400).indexOf('run.infusion=null')>=0;})()",ctxv),
     'death clears the infusion on the same line that drops the gun');
};
