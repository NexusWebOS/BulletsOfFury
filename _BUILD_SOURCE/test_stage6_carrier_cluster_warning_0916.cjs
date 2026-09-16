module.exports=function testStage6CarrierClusterWarning(vm,ctxv,ok){
  console.log('=== 354. Stage-6 Carrier cluster-fan warning ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets,charge:Audio.SFX.bossWeaponCharge,cannon:Audio.SFX.enemyBossCannon};const o={};
    try{Audio.SFX.bossWeaponCharge=()=>{};Audio.SFX.enemyBossCannon=()=>{};camX=0;curStage=STAGES[5];run.stage=6;eBullets=[];player={x:340,y:440,dead:false,invuln:999,_hx:9,_hy:10};boss=null;spawnBoss('doomsdaycarriermk2');boss.enter=false;boss.x=340;boss.y=146;boss._drawY=146;carrierInit(boss);carrierMegaInit(boss);boss._mega.phase=5;boss._mega.step=0;boss._mega.cd=0;boss.hp=boss.maxhp*.20;boss._mega.t=0;boss._lc.playing=false;boss._cn=null;boss._combatWarnings={};
      carrierMegaTick(boss,.01);const F=boss._mega.clusterFan,angles=F.lanes.map(q=>q.a);o.start=!!F&&F.tell===.62&&F.cooldown===1.18&&F.lanes.length===6&&eBullets.length===0;
      carrierClusterFanTick(boss,.12);let B=boss._combatWarnings[F.id];o.green=l23FovPhase(B.t/B.warm)==='green';boss.x+=34;carrierClusterFanTick(boss,.27);B=boss._combatWarnings[F.id];const moved=carrierClusterFanPaths(boss,F);o.yellow=l23FovPhase(B.t/B.warm)==='yellow'&&F.lanes.every((q,i)=>q.a===angles[i])&&moved[0].x!==340;
      carrierClusterFanTick(boss,.18);B=boss._combatWarnings[F.id];o.red=l23FovPhase(B.t/B.warm)==='red'&&eBullets.length===0;carrierClusterFanTick(boss,.06);const shots=eBullets.filter(q=>q.kind==='s6cluster');o.release=B.released&&shots.length===6&&shots.every((q,i)=>q.spd===3.35&&Math.abs(q.ang-angles[i])<.000001);
      o.geometry=F.lanes.slice(0,3).every(q=>q.slot==='L'&&q.a<Math.PI/2)&&F.lanes.slice(3).every(q=>q.slot==='R'&&q.a>Math.PI/2);
      carrierClusterFanTick(boss,1);o.cleanup=!boss._mega.clusterFan;
      boss._mega.phase=4;boss.hp=boss.maxhp*.32;carrierClusterFanStart(boss);const G=boss._mega.clusterFan,gid=G.id;boss.hp=boss.maxhp*.20;carrierMegaTick(boss,.01);o.phaseCancel=boss._mega.phase===5&&!boss._mega.clusterFan&&boss._combatWarnings[gid].released;
      const draw=carrierClusterFanDraw.toString();o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true');o.layered=carrierMegaDrawUnder.toString().includes('carrierClusterFanDraw(b,false)')&&carrierMegaDrawOver.toString().includes('carrierClusterFanDraw(b,true)');o.integrated=carrierMegaTick.toString().includes('carrierClusterFanTick')&&carrierMegaTick.toString().includes('carrierClusterFanStart');return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;Audio.SFX.bossWeaponCharge=save.charge;Audio.SFX.enemyBossCannon=save.cannon;}
  })()`,ctxv));for(const k of Object.keys(result))ok(result[k],'Carrier cluster warning: '+k);
};
