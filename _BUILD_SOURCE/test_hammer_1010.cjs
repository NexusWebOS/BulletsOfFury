module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path'),crypto=require('crypto'),root=path.resolve(__dirname,'..');
 console.log('=== Hammer 1010: physical depth, committed impact and absorptive Chromium ===');
 for(const [name,symbol]of [['boss_motion_art_1009.js','BM9_ART'],['boss_motion_1009.js','BM9'],['hammer_art_1010.js','HM10_ART'],['hammer_1010.js','HM10']])
  if(vm.runInContext('typeof '+symbol,c)==='undefined')vm.runInContext(fs.readFileSync(path.join(root,'assets',name),'utf8'),c,{filename:name});
 const banks=JSON.parse(vm.runInContext('JSON.stringify(HM10_ART)',c));let files=true,geometry=true,hashes=true;
 for(const bank of Object.values(banks))for(const a of bank){const p=path.join(root,a.path);if(!fs.existsSync(p)){files=false;continue;}const bytes=fs.readFileSync(p);
  geometry&&=a.w%2===0&&a.h%2===0&&a.w===bytes.readUInt32BE(16)&&a.h===bytes.readUInt32BE(20)&&a.w===bank[0].w&&a.h===bank[0].h&&String(a.pivot)===String(bank[0].pivot);
  hashes&&=crypto.createHash('sha256').update(bytes).digest('hex')===a.sha256;
 }
 ok(files,'All 96 shipped Hammer frames exist');ok(geometry,'PNG dimensions and fixed physical pivots match the even bank registrations');ok(hashes,'Registered hashes match the approved frame pixels');
 ok(Object.values(banks).every(b=>b.length===16&&new Set(b.map(a=>a.sha256)).size===16),'Each of the six banks contains 16 distinct authored frames');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={},old={hit:playerHit,bullet:_dmgBullet,source:_dmgSrc};
  function fight(diff='furious'){
   ht27Stop();coopOn=false;diffKey=diff;DIFF=difficultyForRun('arcade',diff);run.mode='arcade';run.pilot='yuri';
   beginStage(5);setState(GS.PLAY);player.reset();player.invuln=999;story=special=fb2Talk=null;BOFCinematicDirector.cancel();
   enemies=[];pBullets=[];eBullets=[];powerups=[];l5Rocks=[];l5RockT=9999;spawnBoss(curStage.boss);bossActive=true;
   const b=boss,h=b._hammer;b.enter=b.dead=b._noHit=false;b.hp=b.maxhp=6000;b.x=worldWidth()/2;b.y=180;camX=b.x-VW/2;
   b._fb2IntroSeen=b._cin30Spoke=true;h.balance0922=h.gp4FailsafeSeen=h._fb2RageDone=h.intro1002=true;
   h.frRecovery=h.phasePending=h.openingJump1003=false;h.recovery=null;h.mode='hammer';
   h.frArmor={hp:3000,max:3000,t:0,active:true,activated:true,half:true,barrier:0,checkpoints:[.75,.5,.35,.15],rage:false};
   hammerState(b,'hammer');return b;
  }
  try{
   playerHit=()=>{};_dmgSrc='bullet';
   const b=fight(),h=b._hammer;hammerState(b,'giant_warn');h.t=.4;
   o['Background warning is targetable but cannot make player-plane contact']=bossHitTest(b.x,b.y)&&!hammerOnPlayerPlane(b);
   o['Small background body uses its visible silhouette']=!bossHitTest(b.x+35,b.y)&&bossHitTest(b.x+12,b.y);
   for(const t of [.10,.26,.30,.52]){hammerState(b,'giant_dive');h.t=t;o['Orbital contact at '+t+' seconds follows apparent depth']=hammerOnPlayerPlane(b)===(t>=.30);
    const head=hammerHeadPoint(b),r=HAMMER_STRIKE_REEL[6],scale=.70*(.25+1.4*Math.min(1,t/.52));
    o['Visible orbital hammer tip and hit point agree at '+t+' seconds']=Math.abs(head.x-(b.x+(r[6]-r[4])*scale))<1e-8&&Math.abs(head.y-(b.y+(r[7]-r[5])*scale))<1e-8;
   }
   for(const diff of ['easy','normal','hard','furious'])for(const kind of ['mg','laser','gmiss','retinaMissile']){
    const b=fight(diff),h=b._hammer;hammerState(b,'giant_dive');h.t=.20;h.giantLeft=1;h.giantFromX=h.tx=b.x;h.giantFromY=b.y;h.ty=310;
    const shot={kind,x:b.x,y:b.y,vx:0,vy:-9,dmg:12},hp=h.frArmor.hp;
    const reflected=hammerDiveReflect(b,shot);_dmgBullet=shot;_lastHitX=b.x;_lastHitY=b.y;b._hammerModuleHit=null;hitBoss(12);_dmgBullet=null;
    const held=h.state==='giant_dive';for(let i=0;i<40&&h.state==='giant_dive';i++)hammerBossTick(b,1/60);
    o[diff+' '+kind+': armor damage, no reflection, committed dive through impact']=!reflected&&shot.vy===-9&&!shot._enemyReflected&&held&&h.state==='giant_sweep'&&h.frArmor.hp<hp;
   }
   for(const diff of ['hard','furious']){
    const b=fight(diff),h=b._hammer,A=h.frArmor;A.barrier=6;h.recovery={status:'charging'};hammerState(b,'storm_raise');
    const head=hammerHeadPoint(b),y=b.y+85,lane={kind:'mg',x:head.x,y,vy:-9},body={kind:'mg',x:b.x+(head.x>b.x?-95:95),y,vy:-9};
    pBullets=[lane,body];eBullets=[];fr27Reflect(b,A,1/60);
    o[diff+': wall absorbs body shots without emitting any returned pellet']=body.dead&&eBullets.length===0&&A.flash>0;
    o[diff+': recovery hammer remains reachable and has an independent shield impact']=!lane.dead&&hm10Data(b).hits.length===1;
   }
   const w=fight(),hw=w._hammer;hammerState(w,'warn');hw.t=.25;hammerTarget(w);hw.hammerHP=1;w._hammerModuleHit='hammer';_dmgBullet={kind:'mg'};hitBoss(5);_dmgBullet=null;
   o['Weapon depletion holds the jump warning rather than disarming immediately']=hw.hm10BreakPending&&hw.state==='warn'&&!hw.hammerDestroyed;
   for(let i=0;i<120&&hw.state!=='hammer_exposed';i++)hammerBossTick(w,1/60);
   o['The jump lands before the depleted weapon breaks']=hw.hammerDestroyed&&hw.state==='hammer_exposed'&&hw.leapFx>0;
   const e=fight(),he=e._hammer;he.gp4FailsafeSeen=false;he.frArmor.hp=0;e.hp=e.maxhp*.08;
   hammerState(e,'giant_dive');he.t=.20;he.giantLeft=1;he.giantFromX=he.tx=e.x;he.giantFromY=e.y;he.ty=310;
   hammerBossTick(e,.1);o['8% emergency reserve waits for the committed dive']=he.state==='giant_dive'&&!he.gp4Emergency;
   for(let i=0;i<100&&!he.gp4Emergency;i++)hammerBossTick(e,1/60);
   o['Emergency reserve starts after the full orbital impact']=!!he.gp4Emergency;
   for(let i=0;i<185&&he.gp4Emergency;i++)hammerBossTick(e,1/60);
   o['Deferred emergency reserve still restores 38% and resumes rage']=Math.abs(e.hp/e.maxhp-.38)<.001&&!he.gp4Emergency&&he.frArmor.rage;
   for(const side of [-1,1]){
    const C={side,tell:1.35,t:1.36},b={x:390,y:180};
    const expected=HM10_ART[side>0?'swing_right':'swing_left'][7],p=bm9CounterHead(b,C,(side>0?0:4)+1);
    o['Side '+side+': warning starts at the same mounted hammer head as the authored backswing']=Math.abs(p.x-b.x-(expected.tip[0]-expected.pivot[0])*.70)<1e-8&&Math.abs(p.y-b.y-(expected.tip[1]-expected.pivot[1])*.70)<1e-8;
    C.t=C.tell+.15;const q=bm9CounterHead(b,C),a=HM10_ART[hm10CounterBank(C)][hm10CounterFrame(C)];
    o['Side '+side+': damage path follows the current released swing frame']=Math.abs(q.x-b.x-(a.tip[0]-a.pivot[0])*.70)<1e-8&&Math.abs(q.y-b.y-(a.tip[1]-a.pivot[1])*.70)<1e-8;
    const L=hm10CounterLane(b,C);o['Side '+side+': warning contains the whole curved release and its impact width']=[7,8,9,10,11].every(f=>{const p=hm10CounterPoint(b,C,f);return s81003Distance(p.x,p.y,L)+19<=L.width/2+1e-8;});
   }
   const spike={t:0,split:0,delay:0,warm:0,riseRate:1,height:180,x:390,y:480};const frames=[];
   for(const t of [.02,.36,.40,.61,.64,1.20]){spike.t=t;const s=hammerStormSpikeShape(spike);frames.push(s.f);
    o['Spike at '+t+' seconds shares visible and hittable shaft height']=s.hm10&&s.height>=0&&s.height<=180&&s.kx===s.ky;
   }
   o['Spikes use distinct rise, sustain and authored shatter stages']=frames[0]<8&&frames[2]>=8&&frames[2]<12&&frames.at(-1)===15;
   spike.t=1.23;o['Shattered spike has no hidden collision or drawing']=hammerStormSpikeShape(spike)===null&&!hammerStormSpikeHits(spike,spike.x,spike.y-40);
  }finally{playerHit=old.hit;_dmgBullet=old.bullet;_dmgSrc=old.source;}
  return o;
 })())`,c));
 for(const [name,pass]of Object.entries(out))ok(pass,name);
};
