module.exports=function testHammerThrowVisual(vm,ctxv,ok){
 console.log('=== 342. Canonical hammer wind-ups without warning overlays ===');
 const out=JSON.parse(vm.runInContext(`(function(){
  const save={boss,draw:combatWarningDraw,ret:hammerGroundReticleDraw,reel:hammerReelDraw,flight:hammerFlightDraw,frame:hammerFrame};const o={},calls={warn:[],ret:[],reel:[],flight:[]};
  try{
   combatWarningDraw=(b,q)=>calls.warn.push(q);hammerGroundReticleDraw=(im,x,y,w,a)=>calls.ret.push({tint:im.tint,x,y,w,a});hammerFrame=(key,f,tint)=>({tint:tint||'green'});
   hammerReelDraw=(b,key,reel,f)=>{calls.reel.push({key,f});return true;};hammerFlightDraw=(T,a)=>calls.flight.push({x:T.x,y:T.y,a});
   boss={x:240,y:168,w:158,h:176,hp:1000,maxhp:1000,flash:0,dead:false};hammerBossInit(boss);boss.x=240;boss.y=168;boss.enter=false;boss._noHit=false;const h=boss._hammer;
   h.state='spin';h.throwX=326;h.throwY=392;
   for(const t of [.18,.80,1.4]){h.t=t;h.spinAngle=t*25;hammerBossDraw(boss);}
   o.noThrowWarning=calls.warn.length===0;
   o.noThrowReticles=calls.ret.length===0;
   o.reels=calls.reel[0].key==='arch_hammer_throw_0926'&&calls.reel.slice(1).every(q=>q.key==='arch_hammer_overhead_0926');
   hammerSpiralArm(boss);h.t=1.3;hammerBossDraw(boss);
   o.noRetaliationWarning=calls.warn.length===0&&calls.ret.length===0;
   h.state='throw';h.t=.4;h.throw={x:326,y:360,angle:2,trail:Array.from({length:5},(_,i)=>({x:320-i*12,y:350-i*20,angle:2-i*.2}))};hammerBossDraw(boss);
   o.afterimages=calls.flight.length===3&&calls.flight.slice(0,-1).every(q=>q.a===.09)&&calls.flight[2].a===1;
   o.emptyHand=calls.reel[calls.reel.length-1].key==='arch_hammer_throw_0926'&&calls.reel[calls.reel.length-1].f===0;
   o.assets=['hammer_throw','hammer_overhead','hammer_flight','storm_charge','hammer_lightning','chromium_spike'].every(k=>XART._src['arch_'+k+'_0926']==='assets/game/stage5_archmage_0916/combat_0926/'+(k==='chromium_spike'?'chromium_spike_tall_v2':k)+'.png');
   return JSON.stringify(o);
  }finally{boss=save.boss;combatWarningDraw=save.draw;hammerGroundReticleDraw=save.ret;hammerReelDraw=save.reel;hammerFlightDraw=save.flight;hammerFrame=save.frame;}
 })()`,ctxv));for(const[k,v]of Object.entries(out))ok(v,'Hammer throw visuals: '+k);
};
