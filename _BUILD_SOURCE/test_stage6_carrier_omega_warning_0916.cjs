module.exports=function testStage6CarrierOmegaWarning(vm,ctxv,ok){
  console.log('=== 353. Stage-6 Carrier omega-bomb warning ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets,charge:Audio.SFX.bossWeaponCharge,cannon:Audio.SFX.enemyBossCannon};const o={};
    try{Audio.SFX.bossWeaponCharge=()=>{};Audio.SFX.enemyBossCannon=()=>{};camX=0;curStage=STAGES[5];run.stage=6;eBullets=[];player={x:340,y:440,dead:false,invuln:999,_hx:9,_hy:10};boss=null;spawnBoss('doomsdaycarriermk2');boss.enter=false;boss.x=340;boss.y=146;boss._drawY=146;carrierInit(boss);carrierMegaInit(boss);boss._mega.phase=5;boss._mega.step=3;boss._mega.cd=0;boss.hp=boss.maxhp*.20;boss._mega.t=0;boss._lc.playing=false;boss._cn=null;boss._combatWarnings={};
      carrierMegaTick(boss,.01);const F=boss._mega.omegaBomb,a=F.a;o.start=!!F&&F.tell===.66&&F.cooldown===1.45&&F.sp===1.1&&eBullets.length===0;
      carrierOmegaTick(boss,.12);let B=boss._combatWarnings[F.id];o.green=l23FovPhase(B.t/B.warm)==='green';boss.x+=34;carrierOmegaTick(boss,.27);B=boss._combatWarnings[F.id];const moved=carrierOmegaPath(boss,F);o.yellow=l23FovPhase(B.t/B.warm)==='yellow'&&F.a===a&&moved.x!==340;
      carrierOmegaTick(boss,.22);B=boss._combatWarnings[F.id];o.red=l23FovPhase(B.t/B.warm)==='red'&&eBullets.length===0;carrierOmegaTick(boss,.06);const shots=eBullets.filter(q=>q.kind==='s6omega');o.release=B.released&&shots.length===1&&shots[0].spd===1.1&&shots[0]._s6Accel===1.05&&shots[0]._s6Max===5.2&&Math.abs(shots[0].ang-a)<.000001;
      carrierOmegaTick(boss,1);o.cleanup=!boss._mega.omegaBomb;
      eBullets=[];boss._mega.phase=5;boss._mega.step=10;boss._mega.cd=0;boss._lc.playing=false;boss._cn=null;carrierMegaTick(boss,.01);o.alt=!!boss._mega.omegaBomb&&boss._mega.omegaBomb.sp===1.25&&boss._mega.omegaBomb.cooldown===1.20;
      boss._mega.omegaBomb=null;boss._mega.phase=4;boss.hp=boss.maxhp*.32;carrierOmegaStart(boss,1.1,1.45);const G=boss._mega.omegaBomb,gid=G.id;boss.hp=boss.maxhp*.20;carrierMegaTick(boss,.01);o.phaseCancel=boss._mega.phase===5&&!boss._mega.omegaBomb&&boss._combatWarnings[gid].released;
      const draw=carrierOmegaDraw.toString();o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true');o.layered=carrierMegaDrawUnder.toString().includes('carrierOmegaDraw(b,false)')&&carrierMegaDrawOver.toString().includes('carrierOmegaDraw(b,true)');o.integrated=carrierMegaTick.toString().includes('carrierOmegaTick')&&carrierMegaTick.toString().includes('carrierOmegaStart');return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;Audio.SFX.bossWeaponCharge=save.charge;Audio.SFX.enemyBossCannon=save.cannon;}
  })()`,ctxv));for(const k of Object.keys(result))ok(result[k],'Carrier omega warning: '+k);
};
