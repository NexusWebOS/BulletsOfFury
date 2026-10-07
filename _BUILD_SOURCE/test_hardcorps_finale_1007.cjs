module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path');
 for(const [sym,file] of [['HC7_ART','hardcorps_finale_art_1007'],['HC7','hardcorps_finale_1007']])if(vm.runInContext('typeof '+sym,c)==='undefined')vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/'+file+'.js'),'utf8'),c,{filename:file+'.js'});
 console.log('=== Chromium void spell ownership and authored cast ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();coopOn=false;run.mode='arcade';run.pilot='juggernaut';diffKey='normal';DIFF=DIFFS.normal;
 function fresh(){beginStage(8);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;fb2Talk=null;boss=null;bossActive=false;subBoss=null;subBossActive=false;
  enemies=[];eBullets=[];pBullets=[];powerups=[];player.reset();player.invuln=0;run.shield=0;run._megaShield=false;spawnBoss('vileexistence');
  const b=boss;j3Encounter(b,2);dr5State(b).introSeen=true;dr5State(b).introWanted=false;j3Mimic(b,8);on5FightStart(b);b.x=worldWidth()/2;b.y=213;b._drawY=b.y;
  const D=gd4Create(b,8);D.p.x=b.x;D.p.y=b.y;D.p._hammer.state='hammer';D.p._hammer.hammerDestroyed=false;b.parts.find(p=>p.id==='hammer').destroyed=false;return b;}
 let b=fresh(),C=hc7RiftStart(b),D=gd4Create(b,8);
 out['new cast pauses original donor in a named spell state']=D.p._hammer.state==='hc7Rift'&&C.phase==='raise';
 out['raise has a complete 2.6 second escape tell']=C.tell>=2.6;
 out['safe edge corridors lie outside pull and lightning reach']=C.edgeLeft<C.x-C.radius-7&&C.edgeRight>C.x+C.radius+7;
 const stages=[.1,.3,.55,.9,1.6,2.45].map(t=>{C.t=t;return hc7CastFrame(C);});
 out['raise uses six different authored anticipation cells']=new Set(stages).size===6;
 C.t=1.6;const palm=hc7CastPalm(b),rig=fmcRig(b),weapon=rig.find(v=>v.p.id==='hammer');
 out['overhead spell originates above the actual helmet']=palm.y<b.y-73;
 out['cast keeps an independently targetable measured Hammer head']=weapon&&hammerWeaponTargetable(D.p)&&weapon.x>b.x+75;
 out['physical cast modules remain opaque']=rig.every(v=>v.alpha===1);
 const a=HC7_ART.cast[4];out['cast frame has measured reactor hand and head pivots']=a.px>0&&a.py>0&&a.hand.length===2&&a.head.length===2;
 out['new energy loops have sixteen frames each']=HC7_ART.void.length===16&&HC7_ART.helix.length===16;
 const saved=[...j3State(b).hp];C.phase='active';C.t=.8;C.pulse=0;player.x=C.x+C.radius+25;player.y=C.y;
 const outside=player.x;hc7RiftStep(b,1/60);out['outside player receives zero pull']=player.x===outside;
 player.x=C.x+100;player.y=C.y;const close=player.x;hc7RiftStep(b,1/60);out['near player is drawn toward fixed center']=player.x<close;
 const center=[C.x,C.y];player.x+=30;camX+=20;hc7RiftStep(b,1/60);out['rift does not chase pilot or camera']=C.x===center[0]&&C.y===center[1];
 out['cast simulation cannot heal any of nine persistent pools']=JSON.stringify(saved)===JSON.stringify(j3State(b).hp);
 C.phase='recover';C.t=.1;player.x=C.x+90;player.y=C.y;const rx=player.x;hc7RiftStep(b,1/60);out['dissipating recovery has no pull']=player.x===rx;
 C.t=1.19;hc7RiftStep(b,.02);out['recovery resumes original Hammer controller']=!b._r30.hc7Rift&&D.p._hammer.state==='recover'&&D.hc7Cd>0;
 b=fresh();C=hc7RiftStart(b);D=gd4Create(b,8);const oldHit=playerHit,hits=[];playerHit=function(reason){hits.push(reason);};
 try{
  C.phase='active';C.t=.82;C.pulse=0;hc7RiftPlan(b,C);const L=C.lanes[1];L.age=.5;player.x=lerp(L.x,L.ex,.75);player.y=lerp(L.y,L.ey,.75);hc7RiftStep(b,.01);
  out['warned lightning is harmless before active beat']=hits.length===0;
  L.age=1;player.x=lerp(L.x,L.ex,.75);player.y=lerp(L.y,L.ey,.75);hc7RiftStep(b,.01);out['active lightning dispatches real damage route']=hits.includes('evil chromium lightning');
  hits.length=0;L.age=1.2;player.x=lerp(L.x,L.ex,.75);player.y=lerp(L.y,L.ey,.75);hc7RiftStep(b,.01);out['dissipated lightning is harmless']=hits.length===0;
  player.x=C.x;player.y=C.y;hc7RiftStep(b,.01);out['void core dispatches separate damage reason']=hits.includes('evil chromium void');
 }finally{playerHit=oldHit;}
 D.p._hammer.hammerDestroyed=true;hc7RiftStep(b,.01);out['lost emitting Hammer cancels immediately']=!b._r30.hc7Rift;
 out['disarmed body cannot start another rift']=hc7RiftStart(b)===false;
 b=fresh();C=hc7RiftStart(b);D=gd4Create(b,8);const hp=[...j3State(b).hp];j3Clear(b);
 out['form clear removes spell state and lanes']=!b._r30.hc7Rift;
 out['clear leaves persistent form health unchanged']=JSON.stringify(hp)===JSON.stringify(j3State(b).hp);
 b=fresh();C=hc7RiftStart(b);const clock=hc7Clock(b);hc7RiftStep(b,0);out['zero simulation step does not advance spell age']=C.age===0&&hc7Clock(b)===clock;
 j3Clear(b);beginStage(1);return out;
 })())`,c));for(const [name,value]of Object.entries(out))ok(value,name);
};
