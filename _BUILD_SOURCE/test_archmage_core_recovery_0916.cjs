module.exports=function testArchmageCoreRecovery(vm,ctxv,ok){
  console.log('=== 358. Archmage Easy/Normal core recovery ===');
  const out=JSON.parse(vm.runInContext(`(function(){
    const save={boss:boss,player:player,diff:diffKey,DIFF:DIFF,blit:archBlit,effect:archEffectBlit,atmos:hammerBossAtmosphereDraw,warn:combatWarningDraw,charge:Audio.SFX.bossWeaponCharge,phase:Audio.SFX.bossPhase,enemy:Audio.SFX.enemyShoot};
    const o={},calls={body:[],fx:[],warn:[]};let chargeCues=0,phaseCues=0;
    try{
      Audio.SFX.bossWeaponCharge=()=>{chargeCues++;};Audio.SFX.bossPhase=()=>{phaseCues++;};Audio.SFX.enemyShoot=()=>{};
      player={x:360,y:430,dead:false,invuln:999};diffKey='normal';DIFF=DIFFS.normal;
      boss={x:104,y:286,w:158,h:176,hp:500,maxhp:1000,flash:0,enter:false,dead:false,_noHit:false};hammerBossInit(boss);boss.x=104;boss.y=286;boss.enter=false;boss._noHit=false;const h=boss._hammer;h.state='chaingun';h.mode='chaingun';h.chainHP=1;boss._hammerModuleHit='chaingun';
      hammerBossDamage(boss,2);o.route=h.chainDestroyed&&h.hammerDestroyed&&h.mode==='core'&&h.state==='core_orbit'&&h.t===0&&h.coreAngle===0&&chargeCues===1;
      const x0=boss.x,y0=boss.y;hammerBossTick(boss,.65);o.active=h.state==='core_orbit'&&h.coreAngle>0&&boss.x>x0&&boss.y<y0;
      archBlit=function(key,frame,x,y,z,tint){calls.body.push({key:key,frame:frame,tint:tint,z:z});return true;};archEffectBlit=function(cell,x,y,size,rot,alpha){calls.fx.push({cell:cell,x:x,y:y,size:size,alpha:alpha});return true;};hammerBossAtmosphereDraw=function(){};hammerBossDraw(boss);
      o.authored=calls.body.length===1&&calls.body[0].key==='chaingun_break_enrage'&&calls.body[0].tint==='blue'&&calls.fx.map(q=>q.cell).join(',')==='0,3,4,6'&&calls.fx.every(q=>q.size>=32&&q.alpha>=.55);
      hammerBossTick(boss,1.51);o.release=h.state==='uzi'&&h.mode==='core'&&h.shotCd===.18&&phaseCues===1;
      h.t=4.39;h.shotCd=.5;hammerBossTick(boss,.02);o.megaCharge=h.state==='mega_charge';hammerBossTick(boss,.40);const W=boss._combatWarnings&&boss._combatWarnings['archmage-fused-wave'];o.warning=!!W&&W.t===.4&&W.warm===1.65&&!W.released;combatWarningDraw=function(owner,q){calls.warn.push(q);};hammerBossDraw(boss);o.warningDraw=calls.warn.length===1&&calls.warn[0].progress===.4/1.65&&calls.warn[0].width===VW*.24&&calls.warn[0].ey===VH;
      hammerBossTick(boss,1.30);o.megaBeam=h.state==='mega_beam'&&boss._combatWarnings['archmage-fused-wave'].released;
      h.t=6.99;hammerBossTick(boss,.02);o.loop=h.state==='uzi'&&h.mode==='core';
      diffKey='hard';DIFF=DIFFS.hard;const hard={x:240,y:168,w:158,h:176,hp:500,maxhp:1000,flash:0,enter:false,dead:false,_noHit:false};hammerBossInit(hard);hard.x=240;hard.y=168;hard.enter=false;hard._noHit=false;hard._hammer.state='chaingun';hard._hammer.chainHP=1;hard._hammerModuleHit='chaingun';hammerBossDamage(hard,2);o.hard=hard._hammer.state==='enrage'&&hard._hammer.mode==='enraged'&&hard._hammer.hammerDestroyed&&!('coreAngle' in hard._hammer);
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;diffKey=save.diff;DIFF=save.DIFF;archBlit=save.blit;archEffectBlit=save.effect;hammerBossAtmosphereDraw=save.atmos;combatWarningDraw=save.warn;Audio.SFX.bossWeaponCharge=save.charge;Audio.SFX.bossPhase=save.phase;Audio.SFX.enemyShoot=save.enemy;}
  })()`,ctxv));
  for(const k of Object.keys(out))ok(out[k],'Archmage core recovery: '+k);
};
