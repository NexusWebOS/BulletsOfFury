module.exports=function testHammerBoomerang(vm,ctxv,ok){
  console.log('=== 304e. Chrome Hammer one-hand boomerang ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,hit:playerHit,run:{...run},powerups,camX,curStage,
      sounds:{spin:Audio.SFX.hammerSpin,throw:Audio.SFX.hammerThrow,magnet:Audio.SFX.hammerMagnet,catch:Audio.SFX.hammerCatch}};const o={},sounds={spin:0,throw:0,magnet:0,catch:0};
    try{
      Audio.SFX.hammerSpin=()=>sounds.spin++;Audio.SFX.hammerThrow=()=>sounds.throw++;
      Audio.SFX.hammerMagnet=()=>sounds.magnet++;Audio.SFX.hammerCatch=()=>sounds.catch++;
      camX=0;curStage=STAGES[4];run.stage=5;run.lives=9;powerups=[];
      player={x:326,y:392,dead:false,invuln:999,_hx:9,_hy:10};
      boss={x:240,y:168,w:154,h:168,hp:1000,maxhp:1000,dead:false,flash:0};hammerBossInit(boss);
      boss.x=240;boss.y=168;boss.enter=false;boss._noHit=false;boss._hammer.state='hammer';boss._hammer.t=1.61;
      hammerBoomerangStart(boss);o.starts=boss._hammer.state==='spin'&&boss._hammer.throwX===326;
      player.x=95;hammerBossTick(boss,.20);o.commits=boss._hammer.throwX===326&&boss._hammer.state==='spin';
      const spin0=boss._hammer.spinAngle;hammerBossTick(boss,.35);const spin1=boss._hammer.spinAngle;
      hammerBossTick(boss,.35);const spin2=boss._hammer.spinAngle;o.accelerates=(spin2-spin1)>(spin1-spin0);
      hammerBossTick(boss,.66);o.releases=boss._hammer.state==='throw'&&boss._hammer.throw&&boss._hammer.throw.phase==='out';
      const y0=boss._hammer.throw.y;hammerBossTick(boss,.10);o.fastOutbound=boss._hammer.throw.y-y0>45;
      while(boss._hammer.throw&&boss._hammer.throw.phase==='out')hammerBossTick(boss,.05);
      const T=boss._hammer.throw,d0=Math.hypot(hammerGripPoint(boss).x-T.x,hammerGripPoint(boss).y-T.y),x0=T.x,y1=T.y;
      hammerBossTick(boss,.10);const d1=Math.hypot(hammerGripPoint(boss).x-T.x,hammerGripPoint(boss).y-T.y);
      o.mediumReturn=d1<d0&&Math.hypot(T.x-x0,T.y-y1)<=HAMMER_RETURN_SPEED*.10+.001;
      let guard=0;while(boss._hammer.state==='throw'&&guard++<100)hammerBossTick(boss,.05);
      o.catches=boss._hammer.state==='hammer'&&!boss._hammer.throw&&boss._hammer.attackCycle===1;
      boss._hammer.t=1.61;hammerBossTick(boss,.01);o.alternates=boss._hammer.state==='warn';
      let hits=0;playerHit=function(){hits++;player.invuln=40;};player.dead=false;player.invuln=0;player.x=220;player.y=300;
      const q={x:220,y:300,hitCd:0};o.hazard=hammerBoomerangHit(q,.016)&&hits===1&&q.hitCd===.82;
      o.assets=XART._src.hammer_boomerang_body==='assets/game/stage5_hammer/boomerang_body.png'&&
        XART._src.hammer_boomerang_hammer==='assets/game/stage5_hammer/boomerang_hammer.png';
      o.timing=HAMMER_SPIN_TIME===1.55&&HAMMER_OUT_TIME===.70&&HAMMER_RETURN_SPEED===315;
      o.soundBeats=Object.values(sounds).every(n=>n===1);
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;playerHit=save.hit;Object.assign(run,save.run);powerups=save.powerups;camX=save.camX;curStage=save.curStage;Object.assign(Audio.SFX,save.sounds);}
  })()`,ctxv));
  for(const k of Object.keys(result))ok(result[k],'Chrome Hammer boomerang: '+k);
};
