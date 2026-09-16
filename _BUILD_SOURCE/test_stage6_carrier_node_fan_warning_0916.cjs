module.exports=function testStage6CarrierNodeFanWarning(vm,ctxv,ok){
  console.log('=== 349. Stage-6 Carrier storm-node fan warning ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets,charge:Audio.SFX.bossWeaponCharge,cannon:Audio.SFX.enemyBossCannon};const o={};
    try{Audio.SFX.bossWeaponCharge=()=>{};Audio.SFX.enemyBossCannon=()=>{};camX=0;curStage=STAGES[5];run.stage=6;eBullets=[];player={x:360,y:410,dead:false,invuln:999,_hx:9,_hy:10};
      boss=null;spawnBoss('doomsdaycarriermk2');boss.enter=false;boss.x=240;boss.y=146;boss._drawY=146;carrierMegaInit(boss);boss._mega.phase=1;boss._mega.step=0;boss._mega.cd=0;boss._combatWarnings={};
      carrierMegaTick(boss,.01);const F=boss._mega.nodeFan,angles=F.lanes.map(q=>q.a);o.start=!!F&&F.tell===.62&&F.cooldown===1.55&&F.lanes.length===6&&F.lanes.every(q=>q.node==='L2'||q.node==='R1')&&eBullets.length===0;
      carrierNodeFanTick(boss,.10);let B=boss._combatWarnings[F.id];o.green=l23FovPhase(B.t/B.warm)==='green';player.x=40;player.y=250;boss.x=270;carrierNodeFanTick(boss,.25);B=boss._combatWarnings[F.id];o.yellow=l23FovPhase(B.t/B.warm)==='yellow'&&F.lanes.every((q,i)=>q.a===angles[i]);
      carrierNodeFanTick(boss,.20);B=boss._combatWarnings[F.id];o.red=l23FovPhase(B.t/B.warm)==='red'&&eBullets.length===0;carrierNodeFanTick(boss,.08);let shots=eBullets.filter(q=>q.kind==='s6cyclone');o.release=B.released&&shots.length===6&&shots.every((q,i)=>q.ang===angles[i]&&q.spd===3.15);
      boss._mega.nodeFan=null;eBullets=[];boss._mega.phase=3;boss._mega.step=0;carrierNodeFanStart(boss);const W=boss._mega.nodeFan;o.wide=W.lanes.length===10&&W.cooldown===1.12&&W.lanes.every(q=>q.node==='L1'||q.node==='R2');
      const doomed=boss._mega.nodes.find(n=>n.id===W.lanes[0].node);doomed.dead=true;const before=carrierNodeFanPaths(boss,W).length;o.destroyedDisarms=before===5;const wid=W.id;boss._mega.nodes.forEach(n=>n.dead=true);carrierMegaTick(boss,.01);o.phaseCancel=boss._mega.phase===4&&!boss._mega.nodeFan&&boss._combatWarnings[wid].released;
      const draw=carrierNodeFanDraw.toString();o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true');o.layered=carrierMegaDrawUnder.toString().includes('carrierNodeFanDraw(b,false)')&&carrierMegaDrawOver.toString().includes('carrierNodeFanDraw(b,true)');o.integrated=carrierMegaTick.toString().includes('carrierNodeFanTick')&&carrierMegaTick.toString().includes('carrierNodeFanStart');return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;Audio.SFX.bossWeaponCharge=save.charge;Audio.SFX.enemyBossCannon=save.cannon;}
  })()`,ctxv));for(const k of Object.keys(result))ok(result[k],'Carrier node fan warning: '+k);
};
