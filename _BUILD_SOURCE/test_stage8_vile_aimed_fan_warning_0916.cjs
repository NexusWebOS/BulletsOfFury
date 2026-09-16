module.exports=function testStage8VileAimedFanWarning(vm,ctxv,ok){
  console.log('=== 345. Stage-8 Vile aimed-fan warnings ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets,lock:enemyLockOn,charge:Audio.SFX.bossWeaponCharge,shoot:Audio.SFX.enemyShoot};const o={};
    try{
      Audio.SFX.bossWeaponCharge=()=>{};Audio.SFX.enemyShoot=()=>{};camX=0;curStage=STAGES[7];run.stage=8;eBullets=[];player={x:360,y:410,dead:false,invuln:999,_hx:9,_hy:10};const locks=[];enemyLockOn=(src,delay,opt)=>{locks.push({src:src,delay:delay,opt:opt});return{};};
      boss={x:240,y:140,w:236,h:236,hp:5000,maxhp:5000,dead:false,flash:0,fireCd:0,t:0,_vile:true,_vForm:1,_vAtk:1,_combatWarnings:{}};
      vileAttack(boss);let V=boss._vileFan,paths=vileAimedFanPaths(boss,V),aims=paths.map(p=>p.a);o.needleStart=V.kind==='needle'&&V.tell===.62&&paths.length===5&&V.homing&&eBullets.length===0&&locks.length===0;
      vileAimedFanTick(boss,.10);let B=boss._combatWarnings[V.id];o.needleGreen=l23FovPhase(B.t/B.warm)==='green';
      player.x=40;player.y=250;vileAimedFanTick(boss,.22);B=boss._combatWarnings[V.id];o.needleYellow=l23FovPhase(B.t/B.warm)==='yellow'&&vileAimedFanPaths(boss,V).every((p,i)=>p.a===aims[i]);
      player.x=230;player.y=470;vileAimedFanTick(boss,.24);B=boss._combatWarnings[V.id];o.needleRed=l23FovPhase(B.t/B.warm)==='red'&&eBullets.length===0;
      vileAimedFanTick(boss,.07);const needle=eBullets.filter(q=>q._bfam==='vile');o.needleRelease=B.released&&needle.length===5&&locks.length===1&&locks[0].delay===.55&&needle.every((q,i)=>q.kind==='s8nf_needle'&&Math.abs(Math.atan2(q.vy,q.vx)-aims[i])<1e-8);
      vileAimedFanTick(boss,.44);o.needleCleanup=!boss._vileFan;
      eBullets=[];locks.length=0;player.x=330;player.y=420;boss._vForm=3;boss._annihilationUsed=true;boss._vAtk=0;boss._combatWarnings={};vileAttack(boss);V=boss._vileFan;paths=vileAimedFanPaths(boss,V);aims=paths.map(p=>p.a);o.gunStart=V.kind==='gunship'&&V.tell===.58&&V.cooldown===.78&&paths.length===7&&!V.homing;
      vileAimedFanTick(boss,.59);B=boss._combatWarnings[V.id];const guns=eBullets.filter(q=>q._bfam==='vile');o.gunRelease=B.released&&guns.length===7&&locks.length===0&&guns.every((q,i)=>q.kind==='s8nf_gunship'&&Math.abs(Math.atan2(q.vy,q.vx)-aims[i])<1e-8);
      const draw=vileAimedFanDraw.toString(),body=drawModularBoss.toString();o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true')&&body.includes('vileAimedFanDraw(b,false)')&&body.includes('vileAimedFanDraw(b,true)');
      o.integrated=updateBoss.toString().includes('vileAimedFanTick(b,dt)')&&vileBuildForm.toString().includes('b._vileFan=null');
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;enemyLockOn=save.lock;Audio.SFX.bossWeaponCharge=save.charge;Audio.SFX.enemyShoot=save.shoot;}
  })()`,ctxv));
  for(const k of Object.keys(result))ok(result[k],'Vile aimed fan warning: '+k);
};
