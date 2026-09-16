module.exports=function testStage6CarrierLastRunSlide(vm,ctxv,ok){
  console.log('=== 352. Stage-6 Carrier Last Run continuous slide ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets};const o={};
    try{camX=0;curStage=STAGES[5];run.stage=6;eBullets=[];player={x:340,y:440,dead:false,invuln:999,_hx:9,_hy:10};boss=null;spawnBoss('doomsdaycarriermk2');boss.enter=false;boss.x=340;boss.y=146;boss._drawY=146;carrierInit(boss);carrierMegaInit(boss);boss._mega.phase=5;boss._mega.cd=99;boss.hp=boss.maxhp*.20;boss._mega.t=0;boss._lc.playing=false;boss._cn=null;
      const center=worldWidth()*.5,amp=Math.max(60,worldWidth()*.5-Math.max(150,boss.w*.5)),cd0=boss._mega.cd;carrierMegaTick(boss,.20);const x1=boss.x;o.cooldownFrame=Math.abs(x1-center)>1&&boss._mega.cd<cd0;o.formula=Math.abs(x1-(center+Math.sin(boss._mega.t*.85)*amp))<.000001;
      boss._lc.playing=true;carrierMegaTick(boss,.20);const x2=boss.x;o.beamFrame=Math.abs(x2-x1)>1&&boss._mega.cd===cd0-.20*bossCadencePressure(boss);boss._lc.playing=false;boss._cn={playing:true};carrierMegaTick(boss,.20);const x3=boss.x;o.cannonFrame=Math.abs(x3-x2)>1;boss._cn=null;
      boss._lc.playing=true;let lo=Infinity,hi=-Infinity;for(let i=0;i<480;i++){carrierMegaTick(boss,1/60);lo=Math.min(lo,boss.x);hi=Math.max(hi,boss.x);}boss._lc.playing=false;o.bounds=lo>=center-amp-.001&&hi<=center+amp+.001&&hi-lo>amp*1.9;
      const sx=boss.x;boss._mega.phase=4;boss._mega.cd=99;boss.hp=boss.maxhp*.32;carrierMegaTick(boss,.20);o.phaseScoped=boss._mega.phase===4&&boss.x===sx;
      const src=carrierMegaTick.toString(),slideAt=src.indexOf('PHASE 6 "CONSTANTLY SLIDES"');o.order=slideAt>=0&&slideAt<src.indexOf('carrierThunderheadTick')&&slideAt<src.indexOf('M.cd-=dt');return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;}
  })()`,ctxv));for(const k of Object.keys(result))ok(result[k],'Carrier Last Run slide: '+k);
};
