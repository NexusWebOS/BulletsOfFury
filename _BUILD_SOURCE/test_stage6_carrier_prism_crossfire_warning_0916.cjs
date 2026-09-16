module.exports=function testStage6CarrierPrismCrossfireWarning(vm,ctxv,ok){
  console.log('=== 350. Stage-6 Carrier prism-crossfire warning ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets,charge:Audio.SFX.bossWeaponCharge,cannon:Audio.SFX.enemyBossCannon};const o={};
    try{Audio.SFX.bossWeaponCharge=()=>{};Audio.SFX.enemyBossCannon=()=>{};camX=0;curStage=STAGES[5];run.stage=6;eBullets=[];player={x:360,y:410,dead:false,invuln:999,_hx:9,_hy:10};
      boss=null;spawnBoss('doomsdaycarriermk2');boss.enter=false;boss.x=240;boss.y=146;boss._drawY=146;carrierMegaInit(boss);boss._mega.phase=4;boss._mega.step=0;boss._mega.cd=0;boss.hp=boss.maxhp*.32;boss._combatWarnings={};
      carrierMegaTick(boss,.01);const F=boss._mega.prismFan,angles=F.lanes.map(q=>q.a);o.start=!!F&&F.tell===.62&&F.cooldown===1.25&&F.lanes.length===4&&eBullets.length===0;
      carrierPrismFanTick(boss,.10);let B=boss._combatWarnings[F.id];o.green=l23FovPhase(B.t/B.warm)==='green';player.x=40;player.y=250;boss.x=280;carrierPrismFanTick(boss,.25);B=boss._combatWarnings[F.id];const moved=carrierPrismFanPaths(boss,F);o.yellow=l23FovPhase(B.t/B.warm)==='yellow'&&F.lanes.every((q,i)=>q.a===angles[i])&&moved.some(p=>p.x!==240);
      carrierPrismFanTick(boss,.20);B=boss._combatWarnings[F.id];o.red=l23FovPhase(B.t/B.warm)==='red'&&eBullets.length===0;carrierPrismFanTick(boss,.08);const shots=eBullets.filter(q=>q.kind==='s6prism');o.release=B.released&&shots.length===4&&shots.every((q,i)=>Math.abs(q.ang-angles[i])<.000001&&q.spd===4.3);
      o.barrels=F.lanes.map(q=>q.slot).join(',')==='upper_left_outer,upper_left_inner,upper_right_inner,upper_right_outer';
      carrierPrismFanTick(boss,.70);o.cleanup=!boss._mega.prismFan;
      eBullets=[];boss._mega.phase=4;boss._mega.step=2;boss._mega.cd=0;boss.hp=boss.maxhp*.32;carrierMegaTick(boss,.01);const R=boss._mega.prismFan;o.reverse=R.lanes.every((q,i)=>Math.abs(q.a-(Math.PI/2+[-22,-8,8,22][i]*Math.PI/180))<.000001);
      boss.hp=boss.maxhp*.20;const rid=R.id;carrierMegaTick(boss,.01);o.phaseCancel=boss._mega.phase===5&&!boss._mega.prismFan&&boss._combatWarnings[rid].released;
      const draw=carrierPrismFanDraw.toString();o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true');o.layered=carrierMegaDrawUnder.toString().includes('carrierPrismFanDraw(b,false)')&&carrierMegaDrawOver.toString().includes('carrierPrismFanDraw(b,true)');o.integrated=carrierMegaTick.toString().includes('carrierPrismFanTick')&&carrierMegaTick.toString().includes('carrierPrismFanStart');return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;Audio.SFX.bossWeaponCharge=save.charge;Audio.SFX.enemyBossCannon=save.cannon;}
  })()`,ctxv));for(const k of Object.keys(result))ok(result[k],'Carrier prism warning: '+k);
};
