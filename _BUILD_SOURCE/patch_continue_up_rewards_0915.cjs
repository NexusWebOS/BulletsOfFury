const fs=require('fs');
const path=require('path');

const root=path.resolve(__dirname,'..');
const file=path.join(root,'assets','game.js');
let src=fs.readFileSync(file,'utf8');
if(/\r\n/.test(src))throw new Error('assets/game.js must remain LF-only');

function once(from,to,label){
  const count=src.split(from).length-1;
  if(count!==1)throw new Error(label+': expected one anchor, found '+count);
  src=src.replace(from,to);
}

once(
"  stage:1, score:0, lives:3, bombs:2, missileTier:'standard', missileUpgrade:null, _missileWaveSerial:0, weapon:0, wlevel:1, wlevels:[1,1,1,1,1,1,1],",
"  stage:1, score:0, lives:3, bombs:2, missileTier:'standard', missileUpgrade:null, _missileWaveSerial:0, contUsed:0, contBonus:0, weapon:0, wlevel:1, wlevels:[1,1,1,1,1,1,1],",
'run state fields');

once(
`function continueCap(){
  return run.stage===9&&run.mode!=='arcade'
    ? (DIFF.continues>=0?Math.min(DIFF.continues, STAGE9_CONTINUES):STAGE9_CONTINUES)
    : DIFF.continues;
}`,
`function continueCap(){
  const base=run.stage===9&&run.mode!=='arcade'
    ? (DIFF.continues>=0?Math.min(DIFF.continues, STAGE9_CONTINUES):STAGE9_CONTINUES)
    : DIFF.continues;
  /* Continue Ups extend every finite bank, including the Stage-9 campaign reserve. Easy and
     Normal campaign retain their authored unlimited bank (-1), while still tracking collected
     rewards so they become useful if that run later enters the finite rift reserve. */
  return base<0?-1:base+Math.max(0,run.contBonus|0);
}`,
'continue cap');

once(
`// Shared Life Up probability boost for Hard/Furious in every run mode.
function lifeDropChance(base){return clamp(base*((diffKey==='hard'||diffKey==='furious')?1.25:1),0,1);}`,
`// Shared Life Up probability boost for Hard/Furious in every run mode.
function lifeDropChance(base){return clamp(base*((diffKey==='hard'||diffKey==='furious')?1.25:1),0,1);}

/* ============================================================
   CONTINUE UP REWARD BOUNDARY — MODE-07, 0915

   A Continue Up is earned at one of two explicit, auditable boundaries:
     1. clear a miniboss or boss encounter without either active seat losing a life;
     2. destroy an authored Hard/Furious difficulty ace carrying _continueEligible.

   The reward is a real falling pickup. The final SpriteCook replacement is tracked separately
   by MODE-08; until then this path composes the existing authored Life Up plate with a large C
   badge, so it cannot be mistaken for a Life Up and no placeholder sprite enters the manifest.
   ============================================================ */
function continueRewardDeathCount(){
  let n=(typeof stageStats!=='undefined'&&stageStats)?(stageStats.deaths|0):0;
  if(typeof coopActive==='function'&&coopActive()&&typeof stageStats2!=='undefined'&&stageStats2)n+=stageStats2.deaths|0;
  return n;
}
function continueRewardMark(o){
  if(o){o._continueDeathMark=continueRewardDeathCount();o._continueRewardResolved=false;}
  return o;
}
function continueRewardDrop(x,y,source){
  const p={x:clamp(x==null?worldWidth()/2:x,camLeftX()+28,camRightX()-28),y:y==null?-24:y,
    vy:.62,t:0,kind:'continueup',w:34,h:34,bob:rnd(0,TAU),_continueSource:String(source||'section')};
  powerups.push(p);
  try{if(typeof stageStats!=='undefined'&&stageStats.pickupsSeen!=null)stageStats.pickupsSeen++;}catch(_cuSeen){}
  return p;
}
function continueRewardResolve(o,x,y,source){
  if(!o||o._continueRewardResolved)return false;
  o._continueRewardResolved=true;
  if(o._continueDeathMark==null||continueRewardDeathCount()!==o._continueDeathMark)return false;
  continueRewardDrop(x,y,source);return true;
}
function continueRewardEliteKill(e){
  if(!e||e._continueRewardResolved||!e._continueEligible||!(diffKey==='hard'||diffKey==='furious'))return false;
  e._continueRewardResolved=true;continueRewardDrop(e.x,e.y,'elite');return true;
}
function continueRewardCollect(p){
  run.contBonus=Math.max(0,run.contBonus|0)+1;
  const cap=continueCap(),left=cap<0?'UNLIMITED':String(Math.max(0,cap-(run.contUsed||0)));
  floatText(p.x,p.y,'CONTINUE UP','#62e6ff');
  if(typeof arcadeBanner==='function')arcadeBanner(cap<0?'CONTINUE UP!':('CONTINUE UP - '+left+' READY'));
  if(Audio.SFX&&Audio.SFX.life)Audio.SFX.life();else if(Audio.SFX&&Audio.SFX.powerup)Audio.SFX.powerup();
  return run.contBonus;
}`,
'continue reward engine');

once(
`  if(typeof coopActive==='function' && coopActive() && b && b.maxhp>0){
    b.maxhp=Math.ceil(b.maxhp*COOP_BOSS_MUL); b.hp=b.maxhp;
  }
  boss=b; bossActive=true;`,
`  if(typeof coopActive==='function' && coopActive() && b && b.maxhp>0){
    b.maxhp=Math.ceil(b.maxhp*COOP_BOSS_MUL); b.hp=b.maxhp;
  }
  continueRewardMark(b);
  boss=b; bossActive=true;`,
'boss reward marker');

once(
`  if(typeof coopActive==='function' && coopActive() && b && b.maxhp>0){
    b.maxhp=Math.ceil(b.maxhp*COOP_BOSS_MUL); b.hp=b.maxhp;
  }
  subBoss=b; subBossActive=true;`,
`  if(typeof coopActive==='function' && coopActive() && b && b.maxhp>0){
    b.maxhp=Math.ceil(b.maxhp*COOP_BOSS_MUL); b.hp=b.maxhp;
  }
  continueRewardMark(b);
  subBoss=b; subBossActive=true;`,
'subboss reward marker');

once(
"    if(T>=1.9){ subBoss=null; subBossActive=false; subBossDone=true; if(typeof dropPowerup==='function') dropPowerup(b.x,b.y,'weapon'); }",
"    if(T>=1.9){ continueRewardResolve(b,b.x,b.y,'miniboss'); subBoss=null; subBossActive=false; subBossDone=true; if(typeof dropPowerup==='function') dropPowerup(b.x,b.y,'weapon'); }",
'subboss death reward');

once(
`function bossDie(){
  achievementEncounterDefeat(boss,'boss');`,
`function bossDie(){
  achievementEncounterDefeat(boss,'boss');
  continueRewardResolve(boss,boss&&boss.x,boss&&boss.y,'boss');`,
'boss death reward');

once(
`  enemyMissileDrop(e);
  if(e._waterRock){`,
`  enemyMissileDrop(e);
  continueRewardEliteKill(e);
  if(e._waterRock){`,
'elite death reward');

once(
`    case 'life':
      run.lives=clamp(run.lives+1,0,9); floatText(p.x,p.y,'1UP','#ff5a8a'); Audio.SFX.life(); break;`,
`    case 'life':
      run.lives=clamp(run.lives+1,0,9); floatText(p.x,p.y,'1UP','#ff5a8a'); Audio.SFX.life(); break;
    case 'continueup':
      continueRewardCollect(p); break;`,
'continue pickup collection');

once(
`    const yb=p.y+Math.sin(p.t*4)*2;
    if(p.kind==='crate'){ drawCrate(p.x,yb,p.t,p.flash||0); continue; }`,
`    const yb=p.y+Math.sin(p.t*4)*2;
    if(p.kind==='continueup'){
      /* MODE-08 will replace this composed presentation with its dedicated SpriteCook plate.
         Every pixel of the current base still comes from the shipped Life Up artwork. */
      if(ASSETS.ready&&ASSETS.has('pu_life')){
        const d=ASSETS.dims('pu_life'),s=46/Math.max(d.w,d.h),pulse=.5+.5*Math.sin((p.t||0)*8);
        ctx.save();ctx.translate(p.x,yb);ctx.shadowColor='#62e6ff';ctx.shadowBlur=10+pulse*8;
        ASSETS.blit('pu_life',0,0,d.w*s,d.h*s);ctx.globalCompositeOperation='lighter';
        ctx.strokeStyle='rgba(98,230,255,'+(.55+pulse*.35)+')';ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,0,25+pulse*2,0,TAU);ctx.stroke();
        ctx.globalCompositeOperation='source-over';ctx.fillStyle='#071326';ctx.strokeStyle='#e9ffff';ctx.lineWidth=3;
        ctx.font='bold 18px "BOFmil", monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.strokeText('C',0,1);ctx.fillText('C',0,1);ctx.restore();
        continue;
      }
    }
    if(p.kind==='crate'){ drawCrate(p.x,yb,p.t,p.flash||0); continue; }`,
'continue pickup draw');

once(
`  run.contUsed=0;   // continue counter resets per RUN, not per stage (drop 0805b)
  run._s5Resume=null;`,
`  run.contUsed=0; run.contBonus=0;   // spent credits and earned Continue Ups reset per run
  run._s5Resume=null;`,
'run continue reset');

once(
`    stage:run.stage, score:run.score, lives:run.lives, bombs:clampManualMissiles(run.bombs),missileTier:manualMissileSpec(run.missileTier).id,
    missileUpgrade:run.missileUpgrade?Object.assign({},run.missileUpgrade):null,missileWaveSerial:run._missileWaveSerial||0,retinaScan:!!run.retinaScan,`,
`    stage:run.stage, score:run.score, lives:run.lives, bombs:clampManualMissiles(run.bombs),missileTier:manualMissileSpec(run.missileTier).id,
    missileUpgrade:run.missileUpgrade?Object.assign({},run.missileUpgrade):null,missileWaveSerial:run._missileWaveSerial||0,retinaScan:!!run.retinaScan,
    contUsed:Math.max(0,run.contUsed|0),contBonus:Math.max(0,run.contBonus|0),`,
'campaign snapshot');

once(
`  run.missileTier=manualMissileSpec(s.missileTier).id;run.missileUpgrade=s.missileUpgrade?Object.assign({},s.missileUpgrade):null;run._missileWaveSerial=Math.max(0,s.missileWaveSerial|0);run.bombs=clampManualMissiles(s.bombs==null?2:s.bombs);run.retinaScan=!!s.retinaScan;player._retinaScan=null;`,
`  run.missileTier=manualMissileSpec(s.missileTier).id;run.missileUpgrade=s.missileUpgrade?Object.assign({},s.missileUpgrade):null;run._missileWaveSerial=Math.max(0,s.missileWaveSerial|0);run.bombs=clampManualMissiles(s.bombs==null?2:s.bombs);run.retinaScan=!!s.retinaScan;player._retinaScan=null;
  run.contUsed=Math.max(0,s.contUsed|0);run.contBonus=Math.max(0,s.contBonus|0);`,
'campaign restore');

once(
`  if(run.mode==='arcade'){
    const left=Math.max(0,continueCap()-(run.contUsed||0));`,
`  if(continueCap()>=0){
    const left=Math.max(0,continueCap()-(run.contUsed||0));`,
'continue prompt finite bank display');

const backup=path.join(root,'_shots','backups','game_pre_continue_up_rewards_0915.js');
fs.mkdirSync(path.dirname(backup),{recursive:true});
if(!fs.existsSync(backup))fs.copyFileSync(file,backup);
fs.writeFileSync(file,src,'utf8');
console.log('PATCHED_CONTINUE_UP_REWARDS_0915');
