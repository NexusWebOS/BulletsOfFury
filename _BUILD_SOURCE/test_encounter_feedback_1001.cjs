module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 for(const f of ['spread_art_1001.js','spread_1001.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv,{filename:f});
 console.log('=== 385. October 1 encounter feedback ===');
 const rows=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();debugFight=null;coopOn=false;run.mode='campaign';run.pilot='yuri';
 function reset(stage,diff){diffKey=diff;DIFF=DIFFS[diff];beginStage(stage);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;s6Opening=null;s6Wing=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];groundTargetingReset();player.x=worldWidth()/2;player.y=VH-100;player.invuln=999;}
 for(const diff of ['easy','normal','hard','furious']){
  reset(8,diff);spawnBoss('vileexistence');const b=boss,S=b._r30;let previous=0;
  for(let n=0;n<3;n++){r30Form(b,n);S.mode='fight';b.enter=false;
   out[diff+' form '+n+' has a bounded, increasing health pool']=b.maxhp>previous&&b.maxhp<6000;previous=b.maxhp;
   b.hp=b.maxhp*.5;out[diff+' form '+n+' bar shows its actual remaining half']=Math.abs(bossHealthFraction(b)-.5)<.001;
  }
  r30Form(b,1);S.mode='fight';b.enter=false;r30Attack(b);const P=S.attack;
  out[diff+' ghost has at least a full readable second before contact']=P.strikeAt>=1&&P.cycleTime-P.strikeAt>=.6;
  for(const [stage,kind] of [[5,'spacebomber'],[6,'siegebomber']]){reset(stage,diff);spawnSubBoss__inner(kind);const b=subBoss,B=b._bomber;
   out[diff+' Stage '+stage+' bomber uses its lower private pool']=b.maxhp<3400&&b.hp===B.core+B.parts.reduce((s,p)=>s+p.hp,0)&&b.maxhp===B.coreMax+B.parts.reduce((s,p)=>s+p.max,0);
  }
 }
 reset(3,'furious');spawnBoss('cryospear');let b=boss;b.enter=false;b._noHit=false;b._er26.neutralOpening=false;b._er26.form='fire';er26Set(b,'cannon-relay');er26Combat(b,.01);
 out['Fire-form Rime Wall still fires four cold barrel beams']=b._l23Beam.family==='rime'&&b._l23Beam.slots.join()==='L0,L1,R0,R1';
 out['paired barrel tips are distinct']=Math.hypot(shipBossMount(b,'L0').x-shipBossMount(b,'L1').x,shipBossMount(b,'L0').y-shipBossMount(b,'L1').y)>3;
 mr27Part(b,'gunL').dead=true;out['destroying the left turret removes both barrel grants']=!mr27CanFire(b,'L0')&&!mr27CanFire(b,'L1')&&mr27CanFire(b,'R0');
 reset(5,'furious');spawnBoss(curStage.boss);b=boss;b.enter=false;b._noHit=false;const h=b._hammer;h.balance0922=true;hammerState(b,'hammer');hammerBossTick(b,.016);hammerBossTick(b,3.5);const A=fr27Armor(b);A.rage=true;A.hp=0;A.checkpoints=[.75,.5,.35,.15];h.frRecovery=false;h.recovery=null;h.mode='hammer';b.hp=b.maxhp*.14;
 hammerTarget(b);hammerState(b,'warn');hammerBossTick(b,.1);out['rage warning runs once per simulation tick']=h.state==='warn'&&Math.abs(h.t-.1)<.001;
 b.x-=100;b.y+=90;hammerState(b,'leap_reset');const before={x:b.x,y:b.y};for(let i=0;i<30;i++)hammerBossTick(b,1/60);
 out['rage holds recovery for at least half a second']=h.state==='leap_reset';
 out['rage recovery travels back instead of snapping']=Math.hypot(b.x-before.x,b.y-before.y)>10&&b.y>VH*.34;
 for(let i=0;i<32;i++)hammerBossTick(b,1/60);out['rage exits recovery into a fresh warning']=h.state==='warn'&&h.t<.2;
 out['all Spreadfire combinations own four real frames']=Object.keys(SPREAD1001_ART).length===10&&Object.values(SPREAD1001_ART).every(a=>a.frames.length===4&&a.fps===16);
 return out;
})())`,ctxv));
 for(const [name,pass] of Object.entries(rows))ok(pass,name);
 for(const a of JSON.parse(vm.runInContext('JSON.stringify(Object.values(SPREAD1001_ART))',ctxv)))ok(fs.existsSync(path.join(__dirname,'..',a.path)),a.key+' exists');
};
