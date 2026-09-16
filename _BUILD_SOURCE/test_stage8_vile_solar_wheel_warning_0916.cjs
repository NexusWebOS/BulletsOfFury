module.exports=function testStage8VileSolarWheelWarning(vm,ctxv,ok){
  console.log('=== 346. Stage-8 Vile solar-wheel warning ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets,charge:Audio.SFX.bossWeaponCharge,shoot:Audio.SFX.enemyShoot};const o={};
    try{
      Audio.SFX.bossWeaponCharge=()=>{};Audio.SFX.enemyShoot=()=>{};camX=0;curStage=STAGES[7];run.stage=8;eBullets=[];player={x:360,y:410,dead:false,invuln:999,_hx:9,_hy:10};
      boss={x:240,y:140,w:236,h:236,hp:5000,maxhp:5000,dead:false,flash:0,fireCd:0,t:0,_vile:true,_vForm:2,_vAtk:0,_vRot:0,_combatWarnings:{}};
      vileAttack(boss);let V=boss._vileSolar,paths=vileSolarWheelPaths(boss,V),aims=paths.map(p=>p.a);o.start=V&&V.tell===.62&&V.cooldown===.95&&paths.length===9&&eBullets.length===0&&Math.abs(aims[0]-.19)<1e-9&&Math.abs((aims[1]-aims[0])-TAU/9)<1e-9;
      vileSolarWheelTick(boss,.10);let B=boss._combatWarnings[V.id];o.green=l23FovPhase(B.t/B.warm)==='green';
      boss.x=330;boss.y=155;vileSolarWheelTick(boss,.24);B=boss._combatWarnings[V.id];o.yellow=l23FovPhase(B.t/B.warm)==='yellow'&&vileSolarWheelPaths(boss,V).every((p,i)=>p.a===aims[i]);
      vileSolarWheelTick(boss,.23);B=boss._combatWarnings[V.id];o.red=l23FovPhase(B.t/B.warm)==='red'&&eBullets.length===0;
      vileSolarWheelTick(boss,.06);const shots=eBullets.filter(q=>q._bfam==='vile');o.release=B.released&&shots.length===9&&shots.every((q,i)=>{const d=Math.atan2(q.vy,q.vx)-aims[i];return q.kind==='s8nf_solar'&&Math.abs(Math.atan2(Math.sin(d),Math.cos(d)))<1e-8;});
      vileSolarWheelTick(boss,.34);o.cleanup=!boss._vileSolar;
      const draw=vileSolarWheelDraw.toString(),body=drawModularBoss.toString();o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true')&&body.includes('vileSolarWheelDraw(b,false)')&&body.includes('vileSolarWheelDraw(b,true)');
      o.integrated=updateBoss.toString().includes('vileSolarWheelTick(b,dt)')&&vileBuildForm.toString().includes('b._vileSolar=null');
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;Audio.SFX.bossWeaponCharge=save.charge;Audio.SFX.enemyShoot=save.shoot;}
  })()`,ctxv));
  for(const k of Object.keys(result))ok(result[k],'Vile solar wheel warning: '+k);
};
