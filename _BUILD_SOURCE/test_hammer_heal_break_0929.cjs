module.exports=function(vm,ctxv,ok){
 /* 0929 - Mike: "when I shoot the hammer when he charges it to restore his energy it is still not breaking and
    bringing him to his stun state and he just keeps the shield up and keeps doing it. This is bad."
    The Hard/Furious armor layer (furious_review_0927.js) and HAMMER (hammer_time_0927.js). Behaviour only;
    nothing reads a function's source. The real-Chromium proof is _BUILD_SOURCE/probe_hammer_heal_break_0929.py,
    which also runs the pre-fix file as its busted arm (--old). */
 console.log('=== 378. Hammer heal break: the wall lets the hammer be shot, the stun, no second heal ===');
 const result=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={};const realHit=playerHit;playerHit=function(){};
  function fight(diff){ht27Stop();diffKey=diff;DIFF=DIFFS[diff];run.mode='arcade';run.pilot='maverick';coopOn=false;
    beginStage(5);setState(GS.PLAY);story=null;special=null;enemies=[];eBullets=[];pBullets=[];l5Rocks=[];l5RockT=9999;
    spawnBoss(curStage.boss);bossActive=true;const b=boss;b.enter=false;b._noHit=false;b._hammer.balance0922=true;
    hammerState(b,'hammer');hammerBossTick(b,.016);if(b._hammer.state==='fr_activation')hammerBossTick(b,3);return b;}
  /* the checkpoint heal exactly as the Hard/Furious tick fires it (the half-armor / threshold is marked used first) */
  function checkpoint(b){const A=b._hammer.frArmor;
    if(A.hp>0){A.hp=A.max*.4;A.half=true;}else{const r=b.hp/b.maxhp,th=[.75,.50,.35,.15].find(v=>r<=v&&!A.checkpoints.includes(v));if(th!=null)A.checkpoints.push(th);}
    fr27Restore(b,.10,false,true);}
  for(const diff of ['hard','furious']){
    const b=fight(diff),h=b._hammer,A=h.frArmor;
    b.hp=b.maxhp*.6;hammerState(b,'hammer');checkpoint(b);hammerBossTick(b,.5);
    o[diff+': the checkpoint heal still comes with its energy wall']=h.frRecovery&&A.barrier>0&&h.recovery.status==='charging';
    const hd=hammerHeadPoint(b),wallY=b.y+85;
    const lane={x:hd.x,y:wallY,vx:0,vy:-12,w:4,h:10,dmg:3,kind:'mg'},body={x:b.x-(hd.x>b.x?60:-60),y:wallY,vx:0,vy:-12,w:4,h:10,dmg:3,kind:'mg'};
    pBullets=[lane,body];fr27Reflect(b,A,1/60);
    o[diff+': while he heals, a round aimed at the raised hammer passes the wall']=!lane.dead;
    o[diff+': a round at his body beside it is still turned back']=!!body.dead;
    pBullets=[];
    const R=h.recovery;let n=0;
    while(R.status==='charging'&&n<200){_dmgBullet={kind:'mg',x:hd.x,y:hd.y};bossHitTest(hd.x,hd.y);b._hammerModuleHit='hammer';_lastHitX=hd.x;_lastHitY=hd.y;hitBoss(3);n++;}
    _dmgBullet=null;
    o[diff+': ordinary rounds on the hammer break the heal']=R.status==='cancelled'&&h.state==='fr_stun';
    o[diff+': the break takes his charge and drops the shield']=A.barrier===0&&!h.empowered;
    hammerBossTick(b,.5);
    o[diff+': the shield stays down through the stun']=A.barrier===0&&h.state==='fr_stun';
    const a0=A.hp;b._hammerModuleHit=null;_dmgBullet={kind:'mg'};const got=hammerBossDamage(b,10);_dmgBullet=null;
    o[diff+': a body hit in the stun does double damage']=(a0-A.hp)+got===20;
    const keys=[],ab=archBlit;archBlit=function(k){keys.push(String(k));return ab.apply(this,arguments);};
    try{hammerBossDraw(b);}catch(e){keys.push('THREW '+e.message);}archBlit=ab;
    o[diff+': the stun is drawn as his authored stun, not his idle pose']=keys.includes('stun_0920')&&!keys.includes('leap_strike_0922');
    hammerBossTick(b,FR27_STUN_T);
    o[diff+': after the stun he does not start another heal']=!h.frRecovery&&h.recovery===R&&R.status==='cancelled'&&h.state!=='storm_raise';
    o[diff+': he gets back up into the fight he left, hammer back in hand']=h.mode==='hammer'&&h.state==='leap_reset'&&!h.hammerDestroyed&&A.barrier===0;
    let healed=false;for(let i=0;i<180;i++){hammerBossTick(b,1/60);if(h.recovery!==R&&h.recovery&&h.recovery.status==='charging')healed=true;}
    o[diff+': three seconds on, still no second heal']=!healed;
    const b2=fight(diff),h2=b2._hammer;b2.hp=b2.maxhp*.6;h2.mode='storm';hammerState(b2,'storm_idle');checkpoint(b2);
    hammerRecoveryBreak(b2);hammerBossTick(b2,FR27_STUN_T+.01);
    o[diff+': from the storm phase he gets up the base way (the hammer re-forms)']=h2.state==='storm_rebuild'&&h2.mode==='storm'&&!h2.frRecovery;
    const b3=fight(diff),h3=b3._hammer,A3=h3.frArmor;b3.hp=b3.maxhp*.8;A3.barrier=2;hammerState(b3,'hammer_stun');hammerBossTick(b3,.1);
    o[diff+': the disarm stun stays his stun, shield down (no longer turned into fr_stun)']=h3.state==='hammer_stun'&&A3.barrier===0;
    hammerBossTick(b3,5);
    o[diff+': ... and it ends in the fight, not in a heal']=!h3.frRecovery&&h3.state!=='storm_raise'&&h3.state!=='fr_stun';
  }
  const R0=fight('furious'),hr=R0._hammer,AR=hr.frArmor;AR.hp=0;AR.rage=true;R0.hp=R0.maxhp*.1;hammerState(R0,'hammer_stun');hammerBossTick(R0,5.1);
  o['in the red rage the disarm stun gets up into the rage jumps, not the phase-two hand-off']=hr.state==='warn'&&hr.mode==='hammer';
  diffKey='furious';DIFF=DIFFS.furious;ht27Pending=true;startRun(5);const S=boss,D=S._hammerTime,hs=S._hammer;
  D.mode='attack';D.locked=false;D.shield=false;S._noHit=false;S.enter=false;hs.balance0922=true;
  hammerState(S,'hammer');hammerBossTick(S,.016);if(hs.state==='fr_activation')hammerBossTick(S,3);
  ht27DanceStart(S,D,1.9);S.hp=S.maxhp*.6;checkpoint(S);
  o['HAMMER: a heal that starts mid-dance hands the fight back to attack, so the charge and stun are drawn']=D.mode==='attack'&&hs.frRecovery;
  hs.frRecovery=false;hammerState(S,'hammer_stun');
  o['HAMMER: its music cue waits for a stun as it waits for the armor sequences']=ht27CombatSequence(S);
  /* a REAL music break (ht27LockStart sets the fields its tick reads), with a threshold crossed and unused */
  hammerState(S,'hammer');ht27LockStart(S,D);hs.frArmor.hp=0;hs.frArmor.checkpoints=[];S.hp=S.maxhp*.7;hammerBossTick(S,.016);
  o['HAMMER: no checkpoint heal starts inside a music break']=D.mode==='break'&&!hs.frRecovery;
  ht27Stop();playerHit=realHit;
  return o;
 })())`,ctxv));
 for(const [label,passed]of Object.entries(result))ok(passed,label);
};
