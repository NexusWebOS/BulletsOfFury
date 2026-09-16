module.exports=function testStage8VileCrescentWallWarning(vm,ctxv,ok){
  console.log('=== 344. Stage-8 Vile crescent-wall warning ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets,shake,charge:Audio.SFX.bossWeaponCharge,shoot:Audio.SFX.enemyShoot};const o={};
    try{
      Audio.SFX.bossWeaponCharge=()=>{};Audio.SFX.enemyShoot=()=>{};camX=0;curStage=STAGES[7];run.stage=8;eBullets=[];shake=0;
      player={x:360,y:410,dead:false,invuln:999,_hx:9,_hy:10};
      boss={x:240,y:140,w:236,h:236,hp:5000,maxhp:5000,dead:false,flash:0,fireCd:0,t:0,_vile:true,_vForm:0,_vAtk:0,_combatWarnings:{}};
      vileAttack(boss);const V=boss._vileWall,gap=V.gap,columns=V.columns.slice();
      o.start=!!V&&V.tell===.72&&columns.length===vileCrescentWallColumns(worldWidth(),gap).length&&eBullets.length===0&&boss.fireCd===1.35;
      vileCrescentWallTick(boss,.10);let B=boss._combatWarnings['stage8-vile-crescent-wall'];o.green=l23FovPhase(B.t/B.warm)==='green'&&eBullets.length===0;
      boss.t=9;player.x=40;vileCrescentWallTick(boss,.27);B=boss._combatWarnings['stage8-vile-crescent-wall'];o.yellow=l23FovPhase(B.t/B.warm)==='yellow'&&V.gap===gap&&V.columns.join(',')===columns.join(',');
      boss.t=18;player.x=230;vileCrescentWallTick(boss,.27);B=boss._combatWarnings['stage8-vile-crescent-wall'];o.red=l23FovPhase(B.t/B.warm)==='red'&&eBullets.length===0;
      vileCrescentWallTick(boss,.07);o.noEarly=eBullets.length===0&&!V.released;
      vileCrescentWallTick(boss,.02);B=boss._combatWarnings['stage8-vile-crescent-wall'];const shots=eBullets.filter(q=>q._bfam==='vile');
      o.release=B.released&&V.released&&shots.length===columns.length&&shots.every((q,i)=>q.kind==='s8nf_crescent'&&q.x===columns[i]&&Math.abs(q.vx)<1e-8&&q.vy>0)&&shake===5;
      o.safeGap=!columns.some(x=>Math.abs(x-gap)<70);
      const draw=vileCrescentWallDraw.toString(),body=drawModularBoss.toString();o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true')&&body.includes('vileCrescentWallDraw(b,false)')&&body.includes('vileCrescentWallDraw(b,true)');
      o.singleAnnihilationState=(vileAnnihilationStart.toString().match(/b\\._annihilation=/g)||[]).length===1;
      vileCrescentWallTick(boss,.33);o.cleanup=!boss._vileWall;
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;shake=save.shake;Audio.SFX.bossWeaponCharge=save.charge;Audio.SFX.enemyShoot=save.shoot;}
  })()`,ctxv));
  for(const k of Object.keys(result))ok(result[k],'Vile crescent wall warning: '+k);
};
