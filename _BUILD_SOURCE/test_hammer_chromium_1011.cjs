module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path');
 if(vm.runInContext('typeof HC11',c)==='undefined')vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/hammer_chromium_1011.js'),'utf8'),c,{filename:'hammer_chromium_1011.js'});
 console.log('=== Hammer 1011: half-screen beams and anchored slide counter ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const out={},oldHit=playerHit;let hits=0;
  function fight(diff='normal'){
   ht27Stop();coopOn=false;diffKey=diff;DIFF=difficultyForRun('arcade',diff);run.mode='arcade';run.pilot='yuri';
   beginStage(5);setState(GS.PLAY);player.reset();player.invuln=999;story=special=fb2Talk=null;BOFCinematicDirector.cancel();
   enemies=[];pBullets=[];eBullets=[];powerups=[];l5Rocks=[];l5RockT=9999;spawnBoss(curStage.boss);bossActive=true;
   const b=boss,h=b._hammer;b.enter=b.dead=b._noHit=false;b.hp=b.maxhp=6000;b.x=worldWidth()/2;b.y=180;camX=b.x-VW/2;
   b._fb2IntroSeen=b._cin30Spoke=true;h.balance0922=h.gp4FailsafeSeen=h._fb2RageDone=h.intro1002=true;
   h.frRecovery=h.phasePending=h.openingJump1003=false;h.recovery=null;h.mode='storm';
   h.frArmor={hp:3000,max:3000,t:0,active:true,activated:true,half:true,barrier:0,checkpoints:[.75,.5,.35,.15],rage:false};
   h.stormHome={x:b.x,y:b.y};player.x=b.x;player.y=hammerStormFloorY()-60;
   hammerStormTarget(b);hammerStormImpact(b);return b;
  }
  try{
   playerHit=()=>{hits++;};
   for(const diff of ['easy','normal','hard','furious']){
    const b=fight(diff),h=b._hammer,q=h.stormWaves[2];
    out[diff+': all real storm lanes stop exactly at the screen midpoint']=h.stormWaves.every(q=>q.hc11Beam&&q.top===hc11MidY()&&q.y-q.height===q.top);
    out[diff+': every column retains a full lane warning and gaps']=q.warm>=1.2&&q.retinaWidth>=q.radius*2&&h.stormWaves[1].x-h.stormWaves[0].x>q.radius*2+24;
    q.t=q.split+q.delay+q.warm+.08;out[diff+': ignition glow cannot damage the player']=!hammerStormSpikeHits(q,q.x,q.y-20);
    q.t=q.split+q.delay+q.warm+.35;
    out[diff+': straight beam hits near its top and bottom equally']=hammerStormSpikeHits(q,q.x+14,q.top+1)&&hammerStormSpikeHits(q,q.x+14,q.y-1);
    out[diff+': beam collision never crosses the midpoint or side margin']=!hammerStormSpikeHits(q,q.x,q.top-.01)&&!hammerStormSpikeHits(q,q.x+18,q.top+30);
    q.t=q.split+q.delay+q.warm+q.active;
    out[diff+': expired beam has neither sprite nor hidden collision']=hammerStormSpikeShape(q)===null&&!hammerStormSpikeHits(q,q.x,q.y-30);
    h.t=1;player.y=hc11MidY();hammerStormTick(b,0);out[diff+': the midpoint itself does not trigger an upper counter']=!h.hc11Counter;
    player.y=hc11MidY()-1;hammerStormTick(b,0);
    out[diff+': crossing above halfway starts a committed side slide']=!!h.hc11Counter&&hammerStrikeCommitted(b);
   }
   for(const camera of ['left','right'])for(const side of [-1,1]){
    const b=fight('furious'),h=b._hammer;camX=camera==='left'?0:Math.max(0,worldWidth()-viewW());
    const anchor={x:side<0?camLeftX()+20:camRightX()-20,y:PLAY.y+14,seat:1},C=hc11BeginCounter(b,anchor),land=C.land;
    const tip=hc11Tip(C,11,land.x,land.y,land.scale,land.angle),L=hc11StrikeLane(C);
    out[camera+' '+side+': orbit puts the authored head on the locked player position']=Math.hypot(tip.x-anchor.x,tip.y-anchor.y)<1e-7;
    out[camera+' '+side+': warning covers the complete curved hammer release']=[7,8,9,10,11].every(f=>{const p=hc11Tip(C,f,land.x,land.y,land.scale,land.angle);return s81003Distance(p.x,p.y,L)+19<=L.width/2+1e-7;});
    const lock=JSON.stringify(C.anchor);player.x+=170;player.y+=100;camX+=25;hc11CounterTick(b,C,C.lockAt+.1);
    out[camera+' '+side+': camera motion and dodging cannot drag the world anchor']=JSON.stringify(C.anchor)===lock;
    out[camera+' '+side+': sliding boss stays full-size and cannot make unwarned body contact']=C.scale>=1&&C.scale<=1.1&&!hammerOnPlayerPlane(b)&&hammerStrikeCommitted(b);
    player.invuln=0;player.x=anchor.x;player.y=anchor.y;hits=0;
    hc11CounterTick(b,C,C.tell-C.t-.01);out[camera+' '+side+': full locked warning and slide remain harmless']=hits===0;
    hc11CounterTick(b,C,.35);out[camera+' '+side+': held position is hit by the anchored head sweep']=hits===1;
    hc11CounterTick(b,C,.1);out[camera+' '+side+': one swing cannot hit a seat repeatedly']=hits===1;
    hc11CounterTick(b,C,C.end-C.t+.01);out[camera+' '+side+': recovery releases the attack and restores storm movement']=!h.hc11Counter&&h.hc11CounterDone&&!!h.stormRecovery;
   }
   const b=fight(),h=b._hammer,C=hc11BeginCounter(b,{x:b.x+85,y:hc11MidY()-30,seat:1});
   player.x=worldWidth()+200;player.y=hc11MidY()-50;player.invuln=0;hits=0;
   for(let i=0;i<220&&h.hc11Counter;i++)hc11CounterTick(b,C,1/60);
   out['Leaving the warned anchor avoids the full slide and side strike']=hits===0;
   const d=fight(),hd=d._hammer,D=hc11BeginCounter(d,{x:d.x+100,y:hc11MidY()-35,seat:1});
   hammerBossModuleBreak(d,'hammer');out['Hammer depletion queues the break through the side slide']=hd.hm10BreakPending&&!hd.hammerDestroyed&&hammerStrikeCommitted(d);
   player.invuln=999;for(let i=0;i<240&&hd.hm10BreakPending;i++)hammerBossTick(d,1/60);
   out['The committed strike lands before the depleted hammer breaks']=!hd.hm10BreakPending&&hd.hammerDestroyed&&D.impact;
   out['Legacy orbital jump commitment remains active']=(()=>{const b=fight();hammerState(b,'giant_dive');return hammerStrikeCommitted(b);})();
  }finally{playerHit=oldHit;}
  return out;
 })())`,c));
 for(const [name,pass]of Object.entries(out))ok(pass,name);
};
