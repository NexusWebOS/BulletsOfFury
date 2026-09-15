module.exports=function testStage9HorizonSharedVolleyWarning(vm,ctxv,ok){
  console.log('=== 339. Stage-9 Horizon/Sentinel shared volley warning ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    const save={boss,player,run:{...run},camX,curStage,eBullets};const o={};
    try{
      camX=0;curStage=STAGES[8];run.stage=9;eBullets=[];player={x:360,y:400,dead:false,invuln:999,_hx:9,_hy:10};
      boss={x:240,y:130,w:196,h:238,hp:5000,maxhp:5000,dead:false,flash:0,fireCd:999};const w={side:null,x:240,y:130,w:196,h:238,hp:500,maxhp:500,disabled:false};
      s9FusionWardenWarningStart(boss,w,.10,'stage9-event-horizon');let A=w._s9VolleyWarn,angles=s9FusionWardenWarningAngles(w);o.radial=!!A.radial&&angles.length===8;
      A.t=.10;s9FusionWardenWarningTick(boss,w,0);let B=boss._combatWarnings['stage9-event-horizon'];o.green=l23FovPhase(B.t/B.warm)==='green';
      A.t=.31;s9FusionWardenWarningTick(boss,w,0);B=boss._combatWarnings['stage9-event-horizon'];o.yellow=l23FovPhase(B.t/B.warm)==='yellow';
      A.t=.558;s9FusionWardenWarningTick(boss,w,0);B=boss._combatWarnings['stage9-event-horizon'];o.red=l23FovPhase(B.t/B.warm)==='red';
      A.t=.63;s9FusionWardenWarningTick(boss,w,0);B=boss._combatWarnings['stage9-event-horizon'];o.radialRelease=B.released&&!w._s9VolleyWarn&&eBullets.filter(q=>q.kind==='s9warp').length===8;
      eBullets=[];player.x=360;player.y=400;s9FusionWardenWarningStart(boss,w,.60,'stage9-event-horizon');A=w._s9VolleyWarn;const aim=A.aim,fan=s9FusionWardenWarningAngles(w);player.x=40;player.y=250;A.t=.63;s9FusionWardenWarningTick(boss,w,0);const needles=eBullets.filter(q=>q.kind==='s9needle');o.aimed=fan.length===5&&needles.length===5&&needles.every((q,i)=>Math.abs(Math.atan2(q.vy,q.vx)-fan[i])<.0001)&&A.aim===aim;
      eBullets=[];const eventBoss={x:240,y:130,w:196,h:238,hp:500,maxhp:500,dead:false,t:0};s9VoidHorizonInit(eventBoss);eventBoss._s9rift.t=2;eventBoss.enter=false;eventBoss._s9rift.core._fire=0;s9VoidHorizonTick(eventBoss,0);o.noInstant=!!eventBoss._s9rift.core._s9VolleyWarn&&eBullets.length===0;
      const owner={_combatWarnings:{}} ,L={side:'L',x:170,y:130,disabled:false},R={side:'R',x:310,y:130,disabled:false};s9FusionWardenWarningStart(owner,L,.1,'stage9-warp-sentinel-L');s9FusionWardenWarningStart(owner,R,.6,'stage9-warp-sentinel-R');o.independent=!!owner._combatWarnings['stage9-warp-sentinel-L']&&!!owner._combatWarnings['stage9-warp-sentinel-R']&&s9FusionWardenWarningAngles(L).length===8&&s9FusionWardenWarningAngles(R).length===5;
      const draw=s9FusionWardenWarningDraw.toString(),eventDraw=s9VoidHorizonDraw.toString(),pairDraw=s9FusionBossDraw.toString();o.shared=draw.includes('fieldOnly:true')&&draw.includes('alertOnly:true')&&eventDraw.includes('s9FusionWardenWarningDraw(b,w,false)')&&eventDraw.includes('s9FusionWardenWarningDraw(b,w,true)')&&pairDraw.includes('s9FusionWardenWarningDraw(b,w,false)')&&pairDraw.includes('s9FusionWardenWarningDraw(b,w,true)');
      return JSON.stringify(o);
    }finally{boss=save.boss;player=save.player;Object.assign(run,save.run);camX=save.camX;curStage=save.curStage;eBullets=save.eBullets;}
  })()`,ctxv));
  for(const k of Object.keys(result))ok(result[k],'Stage-9 volley warning: '+k);
};
