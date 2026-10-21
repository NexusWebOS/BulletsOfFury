'use strict';
/* Password encounter: authored Chrome Heart acting and native combat/death/mixer owners. */
const CH21={store:'bof_chrome_heart_v1',unlocked:false,pending:false,notice:false,age:0,result:null,musicReady:false,
 base:{victory:triggerVictory,password:submitPassword,start:startRun,begin:beginStage,spawn:spawnBoss,update:updateBoss,draw:drawBoss,hit:hitBoss,at:bossHitTest,targets:retinaBossTargets,contact:target17BossContact,projectile:drawCombatFinalProjectile,leave:scLeaveStage,set:setState,scene:drawScene,load:stageLoadBegin,die:bossDie,music:Audio.startMusic,bar:drawHealthBarV2,shield:bossShieldFrac,rocks:l5RocksUpdate},draws:{},events:[]};
try{CH21.unlocked=JSON.parse(localStorage.getItem(CH21.store)||'null')?.unlocked===true;}catch(e){}
for(const a of Object.values(CH21_ART.sheets))XART._src[a.key]=a.path;
for(const B of Object.values(CH21_ART.banks))for(const a of B.frames)BOFX.cells[a.key]=[a.sheet,...a.cell];
const ch21Keys=()=>[...Object.values(CH21_ART.sheets).map(a=>a.key),...Object.values(CH21_ART.banks).flatMap(B=>B.frames.map(a=>a.key))];
function ch21Earn(){const winner=[run.pilot,...(coopActive()?[run2.pilot]:[])].find(p=>['falva','lizzie'].includes(p));if(CH21.unlocked||run.stage!==CAMPAIGN_STAGES||!bossDefeated||!winner||debugFight||_bmHost||run._heartMode)return false;
 CH21.unlocked=true;CH21.notice=true;try{localStorage.setItem(CH21.store,JSON.stringify({version:1,unlocked:true,pilot:winner,difficulty:diffKey,at:Date.now()}));}catch(e){}return true;}
triggerVictory=function(){ch21Earn();return CH21.base.victory.apply(this,arguments);};
submitPassword=function(){const code=String(pwInput).trim().toUpperCase();CH21.pending=false;if(code!=='BARBIE')return CH21.base.password.apply(this,arguments);
 pwInput='';if(!CH21.unlocked){CH21.result={locked:true,t:0};setState('chromeheart_result');b20Cue('blocked');return;}
 CH21.pending=true;PENDING_STAGE=5;_coleScene=0;run.mode='arcade';passwordDifficulty=true;menuIndex=Math.max(0,diffList().indexOf(diffKey||'normal'));setState(GS.DIFF);b20Cue('select');};
stageLoadBegin=function(n,keys){return CH21.base.load.call(this,n,[...(keys||[]),...(CH21.pending||run._heartMode?ch21Keys():[])]);};
function ch21Arena(){run._heartMode=true;CH21.result=null;CH21.age=0;debugFight=null;ht27Stop();BOFCinematicDirector.cancel();story=null;special=null;s6Wing=null;
 const entry={stage:5,role:'boss',kind:'chromehammer',name:'CHROME HEART'};debugJump(entry);floaters=floaters.filter(f=>f.txt!=='DEBUG: CHROME HEART');l5Rocks=[];l5RockT=Infinity;stageTimer=0;stagePlan=[];warnT=1.8;_bossCard=null;setState(GS.PLAY);for(const k of ch21Keys())XART.rdy(k);}
startRun=function(fromStage){const launch=CH21.pending;run._heartMode=false;const r=CH21.base.start.apply(this,arguments);CH21.pending=false;
 if(launch)ch21Arena();
 return r;};
beginStage=function(){const secret=run._heartMode,r=CH21.base.begin.apply(this,arguments);if(secret)ch21Arena();return r;};
l5RocksUpdate=function(dt){if(run._heartMode){l5Rocks=[];l5RockT=Infinity;return;}return CH21.base.rocks.apply(this,arguments);};
setState=function(s){if(CH21.pending&&![GS.DIFF,GS.PILOT,GS.PASSWORD].includes(s)&&state!==GS.PILOT)CH21.pending=false;
 if(run._heartMode&&s===GS.STAGECLEAR){CH21.result={t:0,score:run.score};run._heartMode=false;Audio.stopMusic();Audio.startMusic('stageclear');return CH21.base.set.call(this,'chromeheart_result');}
 if(s===GS.TITLE){run._heartMode=false;CH21.pending=false;for(const c of ['bossWeaponCharge','hammerImpact','shieldBossAbsorb'])Snd.stopCue(c);}
 return CH21.base.set.apply(this,arguments);};
function ch21Init(b){b._heart={age:0,seq:0,action:null,cool:1,shield:0,shieldMax:0,shieldFlash:0,cueCd:0};
 b.name='CHROME HEART';b.enter=false;b._noHit=false;b.hp=b.maxhp=[1050,1400,1750,2050][b20Rank()];b.w=184;b.h=220;b.x=worldWidth()/2;b.y=PLAY.y+130;
 // Keep only the native Hammer death owner; old action books/target modules never run.
 b._hammer.state='hammer';b._hammer.balance0922=true;b._hammer.hammerDestroyed=true;b._hammer.chainDestroyed=true;b._hammer.mode='hammer';b._hammer.throw=null;b._hammerTime=null;b._hama=null;b._mr27=null;b._be=null;b.modular=false;b.parts=[];
 Snd.prepare(['bossWeaponCharge','hammerImpact','shieldBossAbsorb','enemyBossCannon']);CH21.events.push({kind:'spawn',difficulty:diffKey,hp:b.hp});return b;}
spawnBoss=function(kind){const r=CH21.base.spawn.apply(this,arguments);if(run._heartMode&&boss?._hammer)ch21Init(boss);return r;};
function ch21Bank(name,t=0,d=1,loop=true){const B=CH21_ART.banks[name];if(!B)return null;const f=loop?Math.floor(t/d*B.frames.length)%B.frames.length:Math.floor(clamp(t/d,0,.9999)*B.frames.length);return B.frames[Math.max(0,f)];}
function ch21Blit(name,t,x,y,size,d=1,loop=true,flash=0){const a=ch21Bank(name,t,d,loop),B=CH21_ART.banks[name];if(!a)return false;return b20Image({...a,w:B.w,h:B.h,pivot:B.pivot},x,y,size/(B.scaleBase||Math.max(B.w,B.h)),0,flash);}
function ch21Pose(b){const Q=b._heart,A=Q.action,u=A?A.t-A.tell:0;let name='idle',t=Q.age,d=1.2,loop=true;
 if(A){name=A.type==='slam'?'slam':A.type==='waltz'?'spin':A.type==='shield'?'channel':'dance';d=A.type==='slam'?A.duration:A.type==='shield'?A.duration:1.6;t=A.type==='slam'||A.type==='shield'?A.t:Math.max(0,u);loop=!['slam','channel'].includes(name);}
 return{name,t,d,loop};}
function ch21Start(b,type){const Q=b._heart,R=b20Rank(),target=b20Target(b),book=['dance','slam','shield','waltz','bouquet'];
 const A=Q.action={type:type||book[Q.seq++%book.length],t:0,tell:[1.5,1.25,1.1,.95][R],origin:{x:b.x,y:b.y},target:{x:clamp(target.x,camLeftX()+75,camRightX()-75),y:clamp(target.y,PLAY.y+150,PLAY.y+PLAY.h-70)},n:0,hit:new Set()};
 A.duration=A.tell+(A.type==='slam'?1.7:A.type==='shield'?2.7:A.type==='waltz'?3.2:3.1);
 if(A.type==='shield')Q.shield=Q.shieldMax=[90,120,145,170][R];b20Cue('bossWeaponCharge');CH21.events.push({kind:'attack',type:A.type,tell:A.tell});return A;}
function ch21Shot(b,angle,speed=2.3,size=25,origin){const m=origin||{x:b.x+13,y:b.y-18};eShoot(m.x,m.y,angle,speed,'heartchrome');const q=eBullets.at(-1);if(q){q._chromeHeart=true;q._boss=true;q._noArsenal=true;q._heartSize=size;q.w=q.h=size*.55;q.r=size*.27;q.homing=false;q._committed=true;q._heartOwner=b;}return q;}
function ch21Volley(b,A){const R=b20Rank(),aim=Math.atan2(A.target.y-(b.y-18),A.target.x-(b.x+13)),n=[3,5,5,7][R],spread=A.type==='bouquet'?.34:.19;
 if(A.type==='waltz'){const gap=Math.PI/2+Math.sin(A.n*.6)*.35;for(let i=0;i<12+R*2;i++){const a=i*TAU/(12+R*2)+A.n*.17;if(Math.abs(Math.atan2(Math.sin(a-gap),Math.cos(a-gap)))<.28)continue;ch21Shot(b,a,1.6+R*.18,23);}}
 else for(let i=0;i<n;i++)ch21Shot(b,aim+(i-(n-1)/2)*spread,2.1+R*.23,A.type==='bouquet'?32:25);
 b20Cue('enemyBossCannon');A.n++;}
function ch21Tick(b,dt){const Q=b._heart;Q.age+=dt;Q.cool-=dt;Q.shieldFlash=Math.max(0,Q.shieldFlash-dt);Q.cueCd=Math.max(0,Q.cueCd-dt);b.flash=Math.max(0,b.flash-dt);b.t+=dt;
 if(!Q.action&&Q.cool<=0)ch21Start(b);const A=Q.action;if(!A){b.x+=clamp(worldWidth()/2-b.x,-60*dt,60*dt);b.y+=clamp(PLAY.y+130-b.y,-65*dt,65*dt);return;}
 A.t+=dt;const u=A.t-A.tell,R=b20Rank();combatWarningTick(b,'chromeheart-'+A.type,A.t,A.tell,A.t>A.tell);
 if(A.type==='slam'&&u>=0){const p=clamp(u/.48,0,1),back=clamp((u-.65)/.8,0,1),k=p*(1-back);b.x=lerp(A.origin.x,A.target.x-21,k);b.y=lerp(A.origin.y,A.target.y-122,k);
  if(!A.n&&u>=.48){A.n++;b20Cue('hammerImpact');b20HitSegment(b,A.target,A.target,45,'Chrome Heart hammer slam',A.hit);explode(A.target.x,A.target.y,65,'purple');for(let i=0;i<7+R*2;i++)ch21Shot(b,Math.PI*i/(6+R*2),1.6+R*.2,26,A.target);}}
 else if(A.type==='waltz'){b.x=clamp(A.origin.x+Math.sin(Math.max(0,u)*2)*100,camLeftX()+90,camRightX()-90);if(u>=A.n*.7&&A.n<4)ch21Volley(b,A);}
 else if(['dance','bouquet'].includes(A.type)&&u>=A.n*.8&&A.n<[3,3,4,4][R])ch21Volley(b,A);
 if(A.type==='shield'&&u>=0&&u<1.9&&u>=A.n*.65&&A.n<3)ch21Volley(b,A);
 if(A.t>=A.duration){Q.action=null;Q.shield=0;Q.cool=[1.15,.95,.8,.65][R];CH21.events.push({kind:'recovery',type:A.type});}
}
updateBoss=function(dt){if(!boss?._heart)return CH21.base.update.apply(this,arguments);const b=boss;if(b.dead){b.flash=Math.max(0,b.flash-dt);hammerBossDeathTick(b,dt);return;}ch21Tick(b,dt);};
drawBoss=function(){const b=boss;if(!b?._heart)return CH21.base.draw.apply(this,arguments);if(b.dead&&b.dying>=5.8)return;
 const Q=b._heart,A=Q.action,p=ch21Pose(b);ch21Blit(p.name,p.t,b.x,b.y,280,p.d,p.loop,b.flash||0);CH21.draws[p.name]=(CH21.draws[p.name]||0)+1;
 if(b.dead){drawSmokeRings(true);return;}
 if(Q.shield>0)ch21Blit('shield',Q.age,b.x,b.y,300,1,true,Q.shieldFlash);
 if(A&&A.t<A.tell){const u=A.t/A.tell;if(A.type==='slam')b20Reticle(A.target.x,A.target.y,68,u);else ch21Fov(b,A,u);}
 const caption=A?{dance:'LOVE CHROMIUM - LET’S DANCE!',shield:'HEART SHIELD, ACTIVATE!',slam:'HEAD OVER HEELS!',bouquet:'A LITTLE LOVE FOR EVERYONE!',waltz:'CHROME HEART WALTZ!'}[A.type]:'CHROME HEART';ui20Text(ctx,caption,b.x,b.y-125,12,310,'center','#ff9bd5');
};
function ch21Fov(b,A,u){const R=b20Rank(),o={x:b.x+13,y:b.y-18},aim=Math.atan2(A.target.y-o.y,A.target.x-o.x),distance=Math.max(VH,Math.hypot(A.target.x-o.x,A.target.y-o.y));
 let angles=[];if(A.type==='waltz'){const gap=Math.PI/2;for(let i=0;i<12+R*2;i++){const a=i*TAU/(12+R*2);if(Math.abs(Math.atan2(Math.sin(a-gap),Math.cos(a-gap)))>=.28)angles.push(a);}}
 else{const n=[3,5,5,7][R],spread=A.type==='bouquet'?.34:.19;for(let i=0;i<n;i++)angles.push(aim+(i-(n-1)/2)*spread);}
 for(const a of angles)b20Field(b,o,{x:o.x+Math.cos(a)*distance,y:o.y+Math.sin(a)*distance},A.type==='bouquet'?36:28,u);
}
bossHitTest=function(x,y){const b=boss;if(!b?._heart)return CH21.base.at.apply(this,arguments);if(b.dead)return false;
 const p=ch21Pose(b),a=ch21Bank(p.name,p.t,p.d,p.loop),B=CH21_ART.banks[p.name],px=Math.floor((x-b.x)/(280/256)+B.pivot[0]),py=Math.floor((y-b.y)/(280/256)+B.pivot[1]),m=v18Mask({...a,w:B.w,h:B.h});
 return !!(m&&px>=0&&py>=0&&px<B.w&&py<B.h&&m[py*B.w+px]>48);};
target17BossContact=function(b,x,y){return b?._heart?Math.hypot(x-b.x,y-b.y)<56:CH21.base.contact.apply(this,arguments);};
retinaBossTargets=function(b){if(!b?._heart)return CH21.base.targets.apply(this,arguments);if(b.dead)return[];return[retinaDynamicPiece(b,'heart-core','core',()=>({x:b.x+13,y:b.y-18,hp:b.hp,dead:b.dead}),d=>hitBoss(d),150,176)];};
hitBoss=function(dmg){const b=boss;if(!b?._heart)return CH21.base.hit.apply(this,arguments);if(b.dead||!(dmg>0))return;const Q=b._heart;markHit(b);weaponHitSfx('normal');
 if(Q.shield>0){Q.shield=Math.max(0,Q.shield-dmg);Q.shieldFlash=.15;if(Q.cueCd<=0){Q.cueCd=.1;b20Cue('shieldBossAbsorb');}return;}
 b.hp=Math.max(0,b.hp-dmg);if(typeof stageStats!=='undefined')stageStats.dmgDealt+=dmg;if(b.hp<=0)bossDie();};
bossDie=function(){if(!boss?._heart)return CH21.base.die.apply(this,arguments);if(boss.dead)return;const h=boss._hammer;boss._heart.shield=0;boss._heart.action=null;for(const q of eBullets)if(q._heartOwner===boss)q.dead=true;
 boss._hammer=null;try{return CH21.base.die.apply(this,arguments);}finally{boss._hammer=h;}};
drawCombatFinalProjectile=function(q){if(q?._chromeHeart){ch21Blit('heart',q.t||0,q.x,q.y,q._heartSize||25,.7);return true;}return CH21.base.projectile.apply(this,arguments);};
scLeaveStage=function(R){if(!run._heartMode)return CH21.base.leave.apply(this,arguments);run.score+=(R?.bonus||0);drawStageClear._init=false;drawStageClear._res=null;CH21.result={t:0,score:run.score};run._heartMode=false;Audio.stopMusic();Audio.startMusic('stageclear');setState('chromeheart_result');};
drawScene=function(dt){if(state!=='chromeheart_result'){const r=CH21.base.scene.apply(this,arguments);if(state===GS.TITLE&&CH21.notice){const q=mw21Window('s',20,76,VW-40,100);if(q){mw21Text('PASSWORD UNLOCKED',q.header,12,'#ff8fcf');mw21Text('BARBIE - CHROME HEART CHALLENGE',q.body,14,'#ffffff');}}return r;}
 const Q=CH21.result||{locked:true,t:0};Q.t+=dt;ctx.fillStyle='#090710';ctx.fillRect(0,0,VW,VH);const r=mw21Window('m',12,120,VW-24,220);
 if(r){mw21Text(Q.locked?'SECRET ENCOUNTER LOCKED':'CHROME HEART DEFEATED',r.header,14,'#ff8fcf');mw21Text(Q.locked?'WIN THE FINAL FIGHT AS FALVA OR LIZZIE TO UNLOCK THE BARBIE PASSWORD.':'LOVE HURTS. CHROMIUM BREAKS. CHALLENGE CLEARED! SCORE '+String(Q.score||0),r.body,17);}
 controlHintRow([['pad_a',Q.locked?'PASSWORD':'TITLE'],['pad_b','BACK']]);if(Q.t>.35&&(Input.menuConfirm()||Input.menuBack())){CH21.result=null;setState(Q.locked?GS.PASSWORD:GS.TITLE);}};
// Optional licensed local music uses the game's existing music gain and mute controls.
if(typeof CH21_MUSIC==='string'&&CH21_MUSIC){const m=new window.Audio();m.preload='none';m.src=CH21_MUSIC;m.loop=true;Snd.music.chromeheart=m;CH21.musicReady=true;}
Audio.startMusic=function(name){return CH21.base.music.call(this,run._heartMode&&CH21.musicReady?'chromeheart':name);};
bossShieldFrac=function(b){return b?._heart?b._heart.shield/Math.max(1,b._heart.shieldMax):CH21.base.shield.apply(this,arguments);};
drawHealthBarV2=function(kind,frac,cx,cy,w,inWorld){const b=boss;if(kind!=='boss'||!b?._heart)return CH21.base.bar.apply(this,arguments);
 const f=eh7Frame('stage_05','bossShield',w);if(!f)return CH21.base.bar.apply(this,arguments);const x=Math.round(cx-f.w/2),y=Math.max(2,Math.round(cy-f.h/2));ctx.save();if(inWorld===true)ctx.translate(camX,0);
 eh7Paint(f,x,y,0,0);bb8Paint({hex:'#ff339f',glow:'#fff0f8'},x+f.hp[0],y+f.hp[1],f.hp[2],f.hp[3],b.hp/Math.max(1,b.maxhp));
 if(f.shield)bb8Paint({hex:'#ffb2dd'},x+f.shield[0],y+f.shield[1],f.shield[2],f.shield[3],bossShieldFrac(b));
 ctx.restore();EH7.lastBoss={theme:'stage_05',variant:'bossShield',frac:b.hp/b.maxhp,shield:bossShieldFrac(b),x,y,w:f.w,h:f.h};return true;};
globalThis.BOF_CHROME_HEART=CH21;
