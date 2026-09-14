/* BULLETS OF FURY ENGINE RULES — Mike 0914.
 * Dangerous boss/miniboss attacks: green acquisition, yellow commitment, red release warning.
 * Aim must lock before red and cannot chase the player during a released laser.
 * FOV and the overhead alert share the same progress; render does not advance simulation.
 * Impact decoration is bounded independently of damage. Pausing never quits via Backspace.
 */
const COMBAT_WARNING_SECONDS=3.0;
const PLAYER_FLAME_SCALE=.75;
function combatWarningDraw(owner,q){
  if(!owner||!q||q.progress==null)return;
  const k=clamp(q.progress,0,1),a=Math.atan2(q.ey-q.y,q.ex-q.x),p={x:q.x,y:q.y},
    B={family:'rime',angles:[a],t:(owner.t||stateT||0),warm:1,released:false};
  ctx.save();ctx.translate(p.x,p.y);ctx.rotate(a-Math.PI/2);
  l23FovDraw(owner,B,0,p,k,q.width||20);ctx.restore();
  B.t=k;l23WarnSymbolDraw(owner,B);
}
function combatWarningTick(owner,id,elapsed,duration){
  if(!owner)return;const warnings=owner._combatWarnings||(owner._combatWarnings={});
  let B=warnings[id];
  if(!B||elapsed<B.t)B=warnings[id]={t:0,warm:duration,released:false};
  B.t=elapsed;B.warm=duration;l23WarnSound(B);
}
function enemyGlideTick(e,dt,opt){
  if(!e||e.dead)return;opt=opt||{};
  const left=camLeftX()+Math.max(24,e.w*.5),right=camRightX()-Math.max(24,e.w*.5),
    speed=opt.speed||85,aim=opt.follow?clamp(player.x,left,right):
      (e._glideSide===-1?left:right);
  e.x+=clamp(aim-e.x,-speed*dt,speed*dt);
  if(!opt.follow&&Math.abs(e.x-aim)<2)e._glideSide=e._glideSide===-1?1:-1;
}
function stage3CentralPulse(b,C){
  if(C.kind!=='centerPulse'||C.released||C.t<C.dur)return;
  C.released=true;const p=shipBossMount(b,'C'),q=stage3BossShot(b,'C',Math.PI/2,3.2,'s3mortar',{w:30,h:36,silent:true});
  /* The core charges inside the hull; released ordnance starts at its forward exit. */
  q.x=p.x;q.y=(b._drawY!=null?b._drawY:b.y)+b.h*.46;
  q._l23fx='rime_orb';q._s3StaticSpin=true;q._s3CorePulse=true;q.szMul=1.1;
  stage3BossMuzzle(b,'C','s3mortar',.8,.16);
  if(Audio.SFX.enemyHeavyLaser)Audio.SFX.enemyHeavyLaser();
}
function stage3CoreWarningDraw(b){
  const C=b&&b._s3boss&&b._s3boss.charge;if(!C||C.kind!=='centerPulse'||C.t>=C.dur)return;
  const p=shipBossMount(b,'C');combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x,ey:VH,progress:C.t/C.dur,width:22});
}
function xenoRigAnyTell(b){const R=b&&b._xenoRig;return !!(R&&(R.mother.tell||R.helpers.some(h=>!h.dead&&h.tell)));}
function xenoRegentGridStart(b,step){
  if(!b||b._xenoGrid)return false;
  const left=camLeftX(),right=camRightX(),cols=8,gapW=3,cw=(right-left)/cols,
    gap=clamp(Math.floor((player.x-left)/cw)-1,0,cols-gapW);
  b._xenoGrid={t:0,tell:COMBAT_WARNING_SECONDS,wave:0,waves:3,next:COMBAT_WARNING_SECONDS,
    gap,gapW,dir:(step&1)?1:-1,cols,left,right,warnAt:0,rowTell:COMBAT_WARNING_SECONDS,
    slots:(step&1)?['R','L','C']:['L','R','C'],angles:[Math.PI/2,Math.PI/2,Math.PI/2]};
  if(b._xenoRig){b._xenoRig.mother.tell=null;for(const h of b._xenoRig.helpers)h.tell=null;}
  b.fireCd=Math.max(b.fireCd||0,7.0);
  if(Audio.SFX.bossWeaponCharge)Audio.SFX.bossWeaponCharge();return true;
}
function xenoRegentGridTick(b,dt){
  const G=b&&b._xenoGrid;if(!G)return false;G.t+=dt;
  if(G.wave<G.waves){
    combatWarningTick(b,'regent-port-'+G.wave,G.t-G.warnAt,G.rowTell);
    if(G.t>=G.next){
      const slot=G.slots[G.wave],p=shipBossMount(b,slot);
      for(const off of [-.14,.14])spaceBossShot(p.x,p.y,G.angles[G.wave]+off,2.8,'s5fracture',
        {silent:off>0,noArsenal:true,forceStageArt:true});
      shipBossMuzzleStart(b,[slot],{fam:'bpfx_muzzle_void',n:8,life:.15,hpx:36});
      G.wave++;G.gap=clamp(G.gap+G.dir,0,G.cols-G.gapW);
      G.warnAt=G.t;G.rowTell=COMBAT_WARNING_SECONDS;G.next=G.t+G.rowTell;
    }
  }
  if(G.wave>=G.waves&&G.t>G.warnAt+.7){b._xenoGrid=null;b.fireCd=1.5;return false;}
  return true;
}
function xenoRegentGridDraw(b){
  const G=b&&b._xenoGrid;if(!G||G.wave>=G.waves)return;
  const p=shipBossMount(b,G.slots[G.wave]),a=G.angles[G.wave],k=clamp((G.t-G.warnAt)/G.rowTell,0,1);
  combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(a)*650,ey:p.y+Math.sin(a)*650,progress:k,width:18});
  weaponFeedbackArt('bpfx_muzzle_void_'+Math.min(7,Math.floor(k*8)),p.x,p.y,24+k*12,null,.55,0,false);
}
function spaceImpact(b,family,lv,size){
  b.kind='spaceImpact';b.family=family;b.lv=lv||1;b.t=0;b.vx=0;b.vy=0;
  b.life=family==='shadow'?.40:.20;
  b.w=b.h=family==='shadow'?Math.min(110,size||70):family==='volley'?30+(b.lv||1)*2:20+(b.lv||1)*2;
  const live=pBullets.filter(q=>q!==b&&!q.dead&&q.kind==='spaceImpact'&&!q._quietVisual),
    nearby=live.some(q=>q.t<.09&&Math.hypot(q.x-b.x,q.y-b.y)<28);
  b._quietVisual=family!=='shadow'&&(live.length>=6||nearby);
  /* One authored impact reel per accepted hit decoration, no extra explosion stacks or screen flash. */
  if(family==='shadow')shake=Math.max(shake,3);
  try{const S=Audio&&Audio.SFX,fn=S&&(family==='shadow'?S.spaceShadowHit:family==='volley'?S.spaceVolleyHit:S.spaceLaserHit);if(fn)fn();}catch(_){}
}
function spaceImpactDraw(b){
  if(b._quietVisual)return true;
  const p=clamp(b.t/b.life,0,.999),lv=clamp(b.lv||1,1,5),fam=b.family||'laser',n=fam==='laser'?4:6,
    key=fam+'_'+lv+'_impact_'+Math.floor(p*n),s=b.w*(.82+p*.18);
  ctx.save();ctx.globalAlpha=(1-p)*.88;ctx.imageSmoothingEnabled=false;
  spaceAtlasDraw(ctx,key,b.x,b.y,s,s,true,null);ctx.restore();return true;
}
function furnaceHeadCombat(b,dt){
  const F=b._fz,t=F.at,P=player,W=worldWidth(),period=2.55,warm=1.65,lock=.70,
    cycle=t%period,beat=Math.floor(t/period);F.a=0;
  if(cycle<lock||cycle>warm+.32){b.x=W/2+Math.sin(F.t*.65)*160*FZT_S;b.y=fztPy(180)+Math.sin(F.t*.8)*20*FZT_S;}
  F.charge=clamp(cycle/warm,0,1);
  for(const side of [-1,1]){
    const p={x:b.x+side*19*FZT_S,y:b.y};
    if(cycle<lock)F.eye[side]+=clamp(fztWrap(fztAim(p,P)-F.eye[side]),-2.0*dt,2.0*dt);
    if(cycle<warm){fztTell(F,p.x,p.y,F.eye[side],1100,cycle/warm);}
    else if(cycle<warm+.32){
      const sweep=F.attack==='eyeSweep'?(cycle-warm)*F.dir*.20:0;
      fztBeam(F,p.x,p.y,F.eye[side]+sweep,1150,12,'eye');
      if(side===1&&beat>F.shotBeat){F.shotBeat=beat;fztSfx('furnaceLaserStart');}
    }
  }
  if(cycle<warm)combatWarningTick(b,'furnace-eyes',cycle,warm);
  if(F.attack==='eyeSweep'&&t>7.65||F.attack!=='eyeSweep'&&t>8.0)furnaceNext(b);
}
