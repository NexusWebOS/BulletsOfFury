module.exports=function testStage8VileMissileSalvoWarning(vm,ctxv,ok){
  console.log('=== 347. Stage-8 Vile straight-missile warning ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets,allow:_eMslAllow,charge:Audio.SFX.bossWeaponCharge,missile:Audio.SFX.missile};const o={};
    try{
      Audio.SFX.bossWeaponCharge=()=>{};Audio.SFX.missile=()=>{};_eMslAllow=()=>true;camX=0;curStage=STAGES[7];run.stage=8;eBullets=[];player={x:360,y:410,dead:false,invuln:999,_hx:9,_hy:10};
      boss={x:240,y:140,w:236,h:236,hp:5000,maxhp:5000,dead:false,flash:0,fireCd:0,t:0,_vile:true,_vForm:3,_vAtk:2,_annihilationUsed:true,_combatWarnings:{}};
      vileAttack(boss);let V=boss._vileMissiles,paths=vileMissileSalvoPaths(boss,V),xs=paths.map(p=>p.x);o.start=V&&V.tell===.58&&V.cooldown===.78&&paths.length===4&&eBullets.length===0&&V.offsets.join(',')==='-0.3,-0.1,0.1,0.3';
      vileMissileSalvoTick(boss,.10);let B=boss._combatWarnings[V.id];o.green=l23FovPhase(B.t/B.warm)==='green';
      player.x=40;player.y=250;vileMissileSalvoTick(boss,.22);B=boss._combatWarnings[V.id];o.yellow=l23FovPhase(B.t/B.warm)==='yellow'&&vileMissileSalvoPaths(boss,V).every((p,i)=>p.x===xs[i]);
      vileMissileSalvoTick(boss,.20);B=boss._combatWarnings[V.id];o.red=l23FovPhase(B.t/B.warm)==='red'&&eBullets.length===0;
      vileMissileSalvoTick(boss,.07);const shots=eBullets.filter(q=>q.kind==='emissile');o.release=B.released&&shots.length===4&&shots.every((q,i)=>q.x===xs[i]&&q.vx===0&&q.vy===2.3&&!q.homing&&!q._lockId);
      vileMissileSalvoTick(boss,.21);o.cleanup=!boss._vileMissiles;
      const draw=vileMissileSalvoDraw.toString(),body=drawModularBoss.toString();o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true')&&body.includes('vileMissileSalvoDraw(b,false)')&&body.includes('vileMissileSalvoDraw(b,true)');
      o.noHoming=!vileMissileSalvoTick.toString().includes('enemyLockOn')&&!vileMissileSalvoTick.toString().includes('eMissileHoming');
      o.integrated=updateBoss.toString().includes('vileMissileSalvoTick(b,dt)')&&vileBuildForm.toString().includes('b._vileMissiles=null');
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;_eMslAllow=save.allow;Audio.SFX.bossWeaponCharge=save.charge;Audio.SFX.missile=save.missile;}
  })()`,ctxv));
  for(const k of Object.keys(result))ok(result[k],'Vile missile salvo warning: '+k);
};
