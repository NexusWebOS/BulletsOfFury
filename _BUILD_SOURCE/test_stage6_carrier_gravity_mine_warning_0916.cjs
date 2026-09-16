module.exports=function testStage6CarrierGravityMineWarning(vm,ctxv,ok){
  console.log('=== 351. Stage-6 Carrier gravity-mine warning ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets,charge:Audio.SFX.bossWeaponCharge,cannon:Audio.SFX.enemyBossCannon};const o={};
    try{Audio.SFX.bossWeaponCharge=()=>{};Audio.SFX.enemyBossCannon=()=>{};camX=0;curStage=STAGES[5];run.stage=6;eBullets=[];player={x:360,y:410,dead:false,invuln:999,_hx:9,_hy:10};
      boss=null;spawnBoss('doomsdaycarriermk2');boss.enter=false;boss.x=240;boss.y=146;boss._drawY=146;carrierMegaInit(boss);boss._mega.phase=4;boss._mega.step=1;boss._mega.cd=0;boss.hp=boss.maxhp*.32;boss._combatWarnings={};
      carrierMegaTick(boss,.01);const F=boss._mega.gravityFan,angles=F.lanes.map(q=>q.a);o.start=!!F&&F.tell===.72&&F.cooldown===1.72&&F.lanes.length===2&&eBullets.length===0;
      carrierGravityFanTick(boss,.12);let B=boss._combatWarnings[F.id];o.green=l23FovPhase(B.t/B.warm)==='green';player.x=40;player.y=250;boss.x=280;carrierGravityFanTick(boss,.27);B=boss._combatWarnings[F.id];const moved=carrierGravityFanPaths(boss,F);o.yellow=l23FovPhase(B.t/B.warm)==='yellow'&&F.lanes.every((q,i)=>q.a===angles[i])&&moved.some(p=>p.x!==240);
      carrierGravityFanTick(boss,.27);B=boss._combatWarnings[F.id];o.red=l23FovPhase(B.t/B.warm)==='red'&&eBullets.length===0;carrierGravityFanTick(boss,.08);const shots=eBullets.filter(q=>q.kind==='s6gravity');o.release=B.released&&shots.length===2&&shots.every((q,i)=>Math.abs(q.ang-angles[i])<.000001&&q.spd===1.35&&q._s6Accel===.16&&q._s6Max===2.15);
      o.geometry=F.lanes[0].slot==='L'&&F.lanes[1].slot==='R'&&Math.abs(F.lanes[0].a-(Math.PI/2-.20))<.000001&&Math.abs(F.lanes[1].a-(Math.PI/2+.20))<.000001;
      carrierGravityFanTick(boss,1.0);o.cleanup=!boss._mega.gravityFan;
      eBullets=[];boss._mega.phase=4;boss._mega.step=1;boss._mega.cd=0;boss.hp=boss.maxhp*.32;carrierMegaTick(boss,.01);const G=boss._mega.gravityFan,gid=G.id;boss.hp=boss.maxhp*.20;carrierMegaTick(boss,.01);o.phaseCancel=boss._mega.phase===5&&!boss._mega.gravityFan&&boss._combatWarnings[gid].released;
      const draw=carrierGravityFanDraw.toString();o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true');o.layered=carrierMegaDrawUnder.toString().includes('carrierGravityFanDraw(b,false)')&&carrierMegaDrawOver.toString().includes('carrierGravityFanDraw(b,true)');o.integrated=carrierMegaTick.toString().includes('carrierGravityFanTick')&&carrierMegaTick.toString().includes('carrierGravityFanStart');return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;Audio.SFX.bossWeaponCharge=save.charge;Audio.SFX.enemyBossCannon=save.cannon;}
  })()`,ctxv));for(const k of Object.keys(result))ok(result[k],'Carrier gravity warning: '+k);
};
