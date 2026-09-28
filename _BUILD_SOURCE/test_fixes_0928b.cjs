module.exports=function(vm,ctxv,ok){
 /* 0928b - Mike's bug list: the Stage-6 wind bed, the Hammer's heal counter, the Chromium activation and
    the chaingun taking over the machine gun from Stage 6. Behaviour only; nothing reads a function's source. */
 console.log('=== 376. Wind bed, Hammer heal counter, Chromium activation, chaingun takeover ===');
 const result=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={};const realHit=playerHit;playerHit=function(){};
  function stage(n,diff){diffKey=diff||'normal';DIFF=DIFFS[diffKey];run.mode='arcade';run.pilot='maverick';coopOn=false;
    beginStage(n);setState(GS.PLAY);story=null;special=null;s6Opening=null;s6Wing=null;enemies=[];eBullets=[];pBullets=[];
    boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;player.dead=false;player.invuln=0;}

  /* ---- the Hammer: a missile into the raised hammer breaks the heal ---- */
  for(const diff of ['normal','hard']){
    stage(5,diff);spawnBoss(curStage.boss);bossActive=true;const b=boss;b.enter=false;b._noHit=false;
    if(b._hammerTime){b._hammerTime.mode='attack';b._hammerTime.shield=false;}
    b.hp=b.maxhp*.6;hammerStormStart(b);hammerBossTick(b,1.2);
    const hd=hammerHeadPoint(b);
    const col=bossHitTest(hd.x,b.y+30);
    o[diff+': during the heal, rounds under the raised hammer pass the body']=col===false;
    o[diff+': the hammer itself is the hit, not the body in front of it']=bossHitTest(hd.x,hd.y+10)===true&&b._hammerModuleHit==='hammer';
    const shot={kind:'gmiss',x:hd.x,y:hd.y+10,dmg:24};
    retinaMissileDamage(b,24,shot);
    o[diff+': an unguided missile into the hammer cancels the heal and stuns him']=b._hammer.recovery.status==='cancelled'&&['storm_stun','fr_stun'].includes(b._hammer.state);
    stage(5,diff);spawnBoss(curStage.boss);bossActive=true;const c=boss;c.enter=false;c._noHit=false;
    if(c._hammerTime){c._hammerTime.mode='attack';c._hammerTime.shield=false;}
    c.hp=c.maxhp*.6;hammerStormStart(c);hammerBossTick(c,1.2);const hd2=hammerHeadPoint(c);
    _dmgBullet={kind:'mg',x:hd2.x,y:hd2.y};bossHitTest(hd2.x,hd2.y);const core=c._hammer.recovery.coreHP;c._hammerModuleHit='hammer';
    const d=hammerBossDamage(c,5);_dmgBullet=null;
    o[diff+': ordinary rounds on the hammer still drain the core, they do not break it outright']=c._hammer.recovery.status==='charging'&&c._hammer.recovery.coreHP===core-5&&d===0;
  }

  /* ---- the Chromium activation (Furious) ---- */
  stage(5,'furious');spawnBoss(curStage.boss);bossActive=true;const F=boss;F.enter=false;F._noHit=false;
  if(F._hammerTime){F._hammerTime.mode='attack';F._hammerTime.shield=false;}
  const h=F._hammer;h.balance0922=true;hammerState(F,'hammer');hammerBossTick(F,.016);
  const hp0=F.hp;
  o['Furious begins the activation on the real boss, armor spreading from the core']=h.state==='fr_activation'&&h.empowered===true;
  o['the HP bar does not empty and refill during it']=bossHealthFraction(F)===FR27_BASE.health(F);
  let steps=0;while(h.state==='fr_activation'&&steps<400){hammerBossTick(F,1/60);steps++;}
  o['it is over in about two seconds and hands back to the fight, armor full']=steps>=120&&steps<=140&&h.frArmor.activated&&h.frArmor.hp===h.frArmor.max&&!F._noHit&&!h.empowered;
  o['nothing about the activation touches his HP']=F.hp===hp0;

  /* ---- the chaingun takes over the machine gun from Stage 6 ---- */
  const was=chaingunUnlocked;chaingunUnlocked=true;
  stage(6);run.weapon=0;run.wlevels=WEAPONS.map(()=>0);run.wlevels[0]=3;run.wlevel=3;run.forge={};run.infusion=null;
  chaingunMGSync();
  o['Stage 6: the MG slot becomes the chaingun at the MG level']=run.weapon===7&&run.wlevels[7]===3&&run.wlevel===3;
  run.weapon=0;run.wlevels=WEAPONS.map(()=>0);run.wlevel=0;chaingunMGSync();
  o['a death drops you to the chaingun']=run.weapon===7;
  run.wlevels[0]+=1;run.weapon=0;chaingunMGSync();
  o['an MG level raises the chaingun']=run.weapon===7&&run.wlevels[7]===run.wlevels[0]&&run.wlevels[7]===1;
  run.forge={0:{elem:'ice',lv:1}};o['the MG forged element applies to the chaingun']=(forgeEntry(7)||{}).elem==='ice';
  run.forge={};player.x=300;player.y=400;run._chainOverheat=0;const n=pBullets.length;chaingunPlayerFire(3);
  const q=pBullets.slice(n),M=chaingunMountPoints();
  o['chaingun rounds are faster, heavier .50-cal rounds from both wing pods at L3']=q.length===2&&q.every(b=>b._cal50&&b.kind==='mg'&&Math.hypot(b.vx,b.vy)>=16&&b.dmg>3)&&
    q.some(b=>Math.abs(b.x-M[0].x)<2)&&q.some(b=>Math.abs(b.x-M[1].x)<2);
  stage(5);run.weapon=0;chaingunMGSync();o['Stage 5 keeps the machine gun']=run.weapon===0;
  chaingunUnlocked=false;stage(7);run.weapon=0;chaingunMGSync();o['before the unlock, Stage 7 keeps the machine gun']=run.weapon===0;
  chaingunUnlocked=was;
  o['every pilot has a measured pod mount']=['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri'].every(k=>Array.isArray(CHAINGUN_MOUNTS[k]));

  /* ---- the Stage-6 wind bed is owned by the main loop ---- */
  let stopped=0;const stop=ambStop;ambStop=function(){stopped++;return stop.apply(this,arguments);};
  try{_ambEl={pause(){},volume:1};_ambStage=6;run.stage=6;setState(GS.GAMEOVER);ambTick();
    o['leaving the stage (game over, title, map) stops the wind bed']=stopped>0&&_ambEl===null;}
  finally{ambStop=stop;}
  playerHit=realHit;
  return o;
 })())`,ctxv));
 for(const k in result)ok(result[k],'Fixes 0928b: '+k);
};
