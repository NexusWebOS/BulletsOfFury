module.exports=function testStage6CarrierCycloneFanWarning(vm,ctxv,ok){
  console.log('=== 348. Stage-6 Carrier twin-cyclone warning ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets,charge:Audio.SFX.bossWeaponCharge,cannon:Audio.SFX.enemyBossCannon};const o={};
    try{
      Audio.SFX.bossWeaponCharge=()=>{};Audio.SFX.enemyBossCannon=()=>{};camX=0;curStage=STAGES[5];run.stage=6;eBullets=[];player={x:360,y:410,dead:false,invuln:999,_hx:9,_hy:10};
      boss=null;spawnBoss('doomsdaycarriermk2');boss.enter=false;boss.x=240;boss.y=146;boss._drawY=146;carrierMegaInit(boss);boss._mega.phase=0;boss._mega.cd=0;boss._combatWarnings={};
      carrierMegaTick(boss,.01);const F=boss._mega.cycloneFan,angles=F.lanes.map(q=>q.a);o.start=!!F&&F.tell===.62&&F.cooldown===1.35&&F.lanes.length===6&&eBullets.length===0;
      carrierCycloneFanTick(boss,.10);let B=boss._combatWarnings[F.id];o.green=l23FovPhase(B.t/B.warm)==='green';
      player.x=40;player.y=250;boss.x=280;carrierCycloneFanTick(boss,.25);B=boss._combatWarnings[F.id];const moved=carrierCycloneFanPaths(boss,F);o.yellow=l23FovPhase(B.t/B.warm)==='yellow'&&F.lanes.every((q,i)=>q.a===angles[i])&&moved.some(p=>p.x!==240);
      carrierCycloneFanTick(boss,.20);B=boss._combatWarnings[F.id];o.red=l23FovPhase(B.t/B.warm)==='red'&&eBullets.length===0;
      carrierCycloneFanTick(boss,.08);const shots=eBullets.filter(q=>q.kind==='s6cyclone');o.release=B.released&&shots.length===6&&shots.every((q,i)=>Math.abs(q.ang-angles[i])<.000001&&q.spd===4.1);
      o.mirrored=F.lanes.slice(0,3).every(q=>q.slot==='MG_L')&&F.lanes.slice(3).every(q=>q.slot==='MG_R');
      carrierCycloneFanTick(boss,.75);o.cleanup=!boss._mega.cycloneFan;
      const draw=carrierCycloneFanDraw.toString();o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true');
      o.layered=carrierMegaDrawUnder.toString().includes('carrierCycloneFanDraw(b,false)')&&carrierMegaDrawOver.toString().includes('carrierCycloneFanDraw(b,true)');
      o.integrated=carrierMegaTick.toString().includes('carrierCycloneFanTick')&&carrierMegaTick.toString().includes('carrierCycloneFanStart');
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;Audio.SFX.bossWeaponCharge=save.charge;Audio.SFX.enemyBossCannon=save.cannon;}
  })()`,ctxv));
  for(const k of Object.keys(result))ok(result[k],'Carrier cyclone warning: '+k);
};
