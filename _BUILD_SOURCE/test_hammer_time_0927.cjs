module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 for(const f of ['hammer_time_art_0927.js','hammer_time_0927.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv,{filename:f});
 console.log('=== HAMMER password fight, soundtrack cue and protected dance break ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={};diffKey='normal';DIFF=DIFFS.normal;debugFight=null;coopOn=false;setState(GS.PASSWORD);pwInput='hammer';submitPassword();
  o['HAMMER routes through difficulty selection to Stage 5']=ht27Pending&&PENDING_STAGE===5&&state===GS.DIFF;
  setState(GS.PASSWORD);o['backing out cancels the secret route']=!ht27Pending;
  pwInput='HAMMER';submitPassword();pilotIndex=PILOTS.findIndex(p=>p.key==='cole');startRun(PENDING_STAGE);
  const b=boss,d=b._hammerTime,m=Snd.music.hammerTime;m.readyState=0;m.paused=true;m.currentTime=0;
  updatePlay(1);o['entrance waits for audio readiness without running ahead']=!d.musicStarted&&d.clock===0&&d.mode==='intro'&&Snd.cur!==m;
  m.readyState=4;const ready=XART.rdy;XART.rdy=function(k){return k==='arch_ship_transform'?false:ready.call(XART,k);};updatePlay(1);XART.rdy=ready;
  o['music waits for the actual ship art']=!d.musicStarted&&d.clock===0&&Snd.cur!==m;
  updatePlay(1/60);m.paused=false;
  o['secret starts a complete space encounter with its own theme']=ht27Active&&state===GS.PLAY&&spaceShipActive()&&b.kind==='chromehammer'&&b.hp===6800&&Snd.cur===m&&d.musicStarted;
  const origin={x:player.x,y:player.y,ammo:run.bombs};for(const a of ['up','fire','bomb'])for(const k of keybind[a])Input.keys[k]=true;
  function advance(to){while(m.currentTime<to){m.currentTime=Math.min(to,m.currentTime+1/60);updatePlay(1/60);}}
  advance(1);o['boss enters in his ship before transforming']=d.shipFrame===15&&b.y>VH*.34&&b.y<VH+50;
  advance(3);o['ship unfolds before the hammer animation']=d.shipFrame>=6&&d.shipFrame<15&&!d.slammed;
  m.paused=true;const held=d.clock;updatePlay(1);o['intro remains on the audio clock during a playback stall']=d.clock===held;m.paused=false;
  advance(6);pShoot();useBomb();startSpecial();setState('paused');hitBoss(999);
  o['entrance blocks movement firing specials pause and boss damage']=ht27Locked()&&state===GS.PLAY&&pBullets.length===0&&special===null&&player.x===origin.x&&player.y===origin.y&&run.bombs===origin.ammo&&b.hp===6800;
  o['friends are not summoned before the hammer impact']=!d.slammed&&d.helpers.length===0;
  advance(6.65);
  o['hammer slam summons exactly four staged arrivals']=d.slammed&&d.helpers.length===4&&d.helpers.some(q=>q.spawn<1)&&ht27Locked();
  for(const k of Object.keys(Input.keys))Input.keys[k]=false;advance(8.5);
  o['four arrivals stay locked throughout the musical lead-in']=ht27Locked()&&d.mode==='intro'&&d.helpers.every(q=>q.spawn===1)&&d.shield;
  const wallEarly=ht27WallBounds(d);advance(12);const wallLate=ht27WallBounds(d);
  o['one half-transparent wall rises toward the dance cue']=wallEarly.y>wallLate.y&&wallEarly.rise>0&&wallLate.rise<1&&wallLate.alpha===.5;
  advance(15.99);
  o['sixteen-second cue has no premature combat gap']=HAMMER_TIME_ART.audio.breakStart===16&&ht27Locked()&&d.mode==='intro'&&player.x===origin.x&&player.y===origin.y&&run.bombs===origin.ammo&&pBullets.length===0;
  m.currentTime=16;o['pause is blocked even before the first break tick']=ht27Locked();setState('paused');o['break cannot enter the in-game pause state']=state===GS.PLAY;
  special={pilot:'cole',t:8,dur:8,strikes:3};const saved=special;
  const before={x:player.x,y:player.y,ammo:run.bombs,lives:run.lives,hp:b.hp};
  updatePlay(1/60);for(const a of ['up','fire','bomb'])for(const k of keybind[a])Input.keys[k]=true;
  for(let i=0;i<90;i++)updatePlay(1/60);
  pShoot();useBomb();autoFireMissiles(1/60);spaceLaserFire();spaceVolleyLaunchRack(3);spaceShadowRelease();startSpecial();hitBoss(500);
  o['locked break freezes movement and consumes no ammunition or lives']=player.x===before.x&&player.y===before.y&&run.bombs===before.ammo&&run.lives===before.lives;
  o['shielded break suppresses every release path and boss damage']=pBullets.length===0&&b.hp===before.hp&&special===null;
  o['wall finishes rising as the dance begins']=ht27WallBounds(d).rise===1&&d.mode==='break';
  o['four backup dancers assemble behind the shield']=d.helpers.length===4&&d.helpers.every(q=>q.spawn===1)&&d.shield;
  o['helper arrival explosions expire while controls stay frozen']=explosions.length===0;
  m.currentTime=24.01;for(const k of Object.keys(Input.keys))Input.keys[k]=false;updatePlay(1/60);
  o['break releases control with the previous special intact']=!ht27Locked()&&!d.shield&&special===saved&&player.invuln>=47;
  special=null;b._noHit=false;hitBoss(10);o['boss takes damage again after the shield lowers']=b.hp<before.hp;
  setState('paused');o['ordinary combat can still pause']=state==='paused';setState(GS.PLAY);
  const states=[];for(let i=0;i<4;i++){b.hp=b.maxhp*.5;ht27Attack(b,d);states.push(b._hammer.state);}
  o['dance fight retains jump throw whirlwind and spiked-ball attacks']=states[0]==='warn'&&states[1]==='spin'&&states[2].includes('whirl')&&states[3]==='curl';
  ht27Attack(b,d);hammerWhirlStart(b);hammerState(b,'whirlwind');b._noHit=false;for(let i=0;i<4;i++){b._hammer.whirlHitCd=0;hammerBossDamage(b,1);}
  o['whirlwind still supports the real disarm counter']=b._hammer.state==='hammer_stun';b._hammer.ballSeen=true;b._hammer.t=4.99;ht27Tick(b,.02);
  o['disarm recovers back into the dance encounter']=d.mode==='dance'&&!b._hammer.hammerDestroyed;
  setState(GS.TITLE);o['leaving cleans up music and the global lock']=!ht27Active&&!ht27Pending&&!ht27Locked()&&Snd.cur!==m;
  startRun(5);o['ordinary Stage 5 does not launch the secret encounter']=!ht27Active&&!(boss&&boss._hammerTime);
  for(const diff of ['easy','normal','hard','furious','insanity']){diffKey=diff;DIFF=DIFFS[diff];pwInput='HAMMER';submitPassword();startRun(5);o[diff+' secret health pool is explicit']=boss.hp===({easy:4800,normal:6800,hard:8400,furious:9800,insanity:9800})[diff];const D=boss._hammerTime;ht27Summon(D,true);for(const q of D.helpers){q.spawn=1;q.arrived=true;q.shotCd=0;}boss.y=VH*.34;ht27DanceStart(boss,D,100);D.clock=30;m.currentTime=30;eBullets=[];pBullets=[];
   for(let i=0;i<300;i++)ht27Helpers(boss,D,1/60);
   const armed=['hard','furious','insanity'].includes(diff);o[diff+' helper attack eligibility']=eBullets.some(q=>q._ht27Helper)===armed;
   o[diff+' helper missile targeting eligibility']=D.helpers.every(q=>_lockTargets().includes(q)===armed&&spaceTargets().includes(q)===armed);
   const q=D.helpers[0],hp=q.hp;hitEnemy(q,5);o[diff+' helper damage follows combat eligibility']=q.hp===(armed?hp-5:hp);
   if(armed){hitEnemy(q,999);o[diff+' helper death removes it from target lists']=q.dead&&!_lockTargets().includes(q)&&!spaceTargets().includes(q);}
   setState(GS.TITLE);}
  const wall=ht27WallBounds();o['one flat wall spans the world at half opacity']=wall.x<=0&&wall.x+wall.w>=worldWidth()&&wall.alpha===.5&&HAMMER_TIME_ART.sheets.wall.frames.length===8;
  return o;
 })())`,ctxv));
 for(const [name,value]of Object.entries(out))ok(value,name);
};
