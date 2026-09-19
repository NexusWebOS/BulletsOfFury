const fs=require('fs');
module.exports=function testWeaponRepair0918(vm,ctxv,ok){
  console.log('=== 373. BOSS ELEMENTS, SELECTABLE FORMS, FURIOUS RAZORBACK (0918) ===');
  const R=js=>vm.runInContext(js,ctxv);
  ok(R("JSON.stringify(BOSS_ELEMENT_BY_STAGE)==='{"+"\\\"1\\\":\\\"kinetic\\\",\\\"2\\\":\\\"fire\\\",\\\"3\\\":\\\"ice\\\",\\\"4\\\":\\\"lightning\\\",\\\"5\\\":\\\"chrome\\\",\\\"6\\\":\\\"dark\\\",\\\"7\\\":\\\"toxic\\\",\\\"8\\\":\\\"prism\\\",\\\"9\\\":\\\"water\\\"}'"),
    'stages 1-9 award Sonic, Fire, Ice, Lightning, Chromium, Dark Matter, Toxic, Prism and Water in order');
  R("var __wrOwn=achievementState.owned;achievementState.owned={};run.forge={};run.forgeForms={};run.forgeElems={};run.forgeCombos=4;run.forgeRespecs=2;run.weapon=0;run.infusion=null;");
  ok(R("forgeComboGrant('fire')==='ok' && FORGE_WEAPONS.every(function(w){return forgeElemsFor(w).indexOf('fire')>=0;})"),
    'the Fire boss reward unlocks Fire for every weapon, not one random pairing');
  ok(R("forgeCombine(0,'fire')==='ok' && forgeCombine(3,'fire')==='ok' && run.forgeForms[0].fire && run.forgeForms[3].fire"),
    'the same obtained element forges both machine gun and laser');
  ok(R("forgeSelect(0,null)==='ok' && !run.forge[0] && run.forgeForms[0].fire && forgeSelect(0,'fire')==='ok' && run.forge[0].elem==='fire'"),
    'switching to bare and back preserves the crafted form');
  R("forgeComboGrant('ice');");
  ok(R("weaponBaseForms(4).some(function(x){return x.id==='icebreath';}) && weaponBaseForms(5).some(function(x){return x.id==='fireorb';}) && weaponBaseForms(5).some(function(x){return x.id==='fireice';})"),
    'loadout offers Ice Breath, Fire Orb and Thermoshock once their elements are obtained');
  ok(R("weaponFormSelect(5,{kind:'variant',id:'fireice'})==='ok' && run.wvars[5]==='fireice'"),
    'the loadout form selector equips Thermoshock');
  ok(R("(run.stage=5,run.spaceMode=true,forgeComboGrant('chrome'),forgeVisible())"),
    'the Stage-5 Chromium Forge opens after the space boss');
  ok(R("(run.stage=9,forgeComboGrant('dark'),infusionGateOpen('dark'))"),
    'a boss-earned gated element is usable immediately');
  ok(R("(run.stage=1,forgeComboRoll().elem==='kinetic') && (run.stage=5,forgeComboRoll().elem==='chrome') && (run.stage=9,forgeComboRoll().elem==='water')"),
    'boss element rewards are deterministic, never a lottery');
  ok(R("XART._src.magma_orb_0918 && XART._src.forge_loadout_0918 && XART._src.weapon_found_0918"),
    'the Magma Orb, Forge/loadout and Weapon Found plates are registered');
  ok(R("(function(){var q=rzbFuriousSegments(1.05,5);return q.length===5&&q.every(function(x,i){return x[0]<x[1]&&(i===0||q[i-1][1]<x[0]);});})()"),
    'Furious sonic pressure is five separated decibel lobes with real openings');
  ok(R("(function(){var q=rzbFuriousSegments(1.05,5),w={arc:1.05,segments:q};return rzbWaveAngleHit(w,(q[0][1]+q[1][0])/2)===false&&rzbWaveAngleHit(w,(q[0][0]+q[0][1])/2)===true;})()"),
    'wave collision respects the visible openings');
  const src=fs.readFileSync(require('path').join(__dirname,'..','assets','game.js'),'utf8');
  ok(R("!!BOFX.img.rzbf_hull_0 && !!BOFX.img.rzbf_turret && String(rzbSprite).indexOf('xartPalette')<0"),
    'Furious Razorback uses authored red-panel plates instead of a full-sprite color overlay');
  ok(/forgeForms:JSON\.parse/.test(src)&&/run\.forgeForms=/.test(src),'campaign saves preserve every crafted form');
  ok(/POWER ACQUIRED/.test(src)&&!/NEW COMBINATION  -/.test(src),'the boss pickup announces an element power, not a weapon pair');
  ok(/stageRevisionCue\(b,'razorbackCharge'/.test(src)&&/stageRevisionCue\(b,'razorbackPressure'/.test(src),'Razorback charge and release both have audible gameplay cues');
  R("achievementState.owned=__wrOwn;run.spaceMode=false;");
};
