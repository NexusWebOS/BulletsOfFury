/* Mike's stage 1–5 encounter corrections, 0914. Authored plates, one simulation owner. */
const STAGE5_SKY_LEAD=5.0;
const REGENT_COMBAT_GAIN=.40;
function regentCombatMixArm(){
  if(typeof Snd==='undefined'||!Snd||Snd._regentMix)return;
  const original=Snd.play;
  Snd.play=function(name,volume){
    const combat=run.stage===5&&boss&&boss._xenoRig&&!boss.dead,voice=Snd.VOICE_SET&&Snd.VOICE_SET[name];
    return original.call(this,name,(volume==null?1:volume)*(combat&&!voice?REGENT_COMBAT_GAIN:1));
  };
  Snd._regentMix=true;
}
function stageRevisionWarm(kind){
  const names=kind==='razorback'?['razorbackGun','razorbackPressure','razorbackCharge','razorbackRocket','razorbackRam']:
    kind==='damkeeper'?['overlordGun','overlordRocket','overlordLance','overlordWind','overlordCharge','overlordRotor']:
    ['wardenGun','wardenCenterGun','wardenRocket','wardenRackCharge','sovereignDive','sovereignFlyby','sovereignContact','sovereignIntercept','sovereignBreak','sovereignHelperGun','sovereignHeat','sovereignWindup','sovereignLaser'];
  if(typeof Snd!=='undefined'&&Snd.prepare)Snd.prepare(names);
  if(kind==='damkeeper'&&typeof Snd!=='undefined'&&Snd.loopPrepare)Snd.loopPrepare('overlordRotor');
  if(kind==='olivewarden')for(const key of ['mgcf_1_5','bpfx_proj_missile_0'])XART.rdy(key);
  if(kind==='razorback'||kind==='damkeeper')for(const fam of ['nsd_chim','nxp_upward'])for(let i=0;i<8;i++)XART.rdy(fam+'_'+i);
}
function stageRevisionCue(b,key,gate,vol){
  if(!b||b.dead)return false;
  const now=b.t||b._ovT||0,row=b._stageSound||(b._stageSound={});
  if(row[key]!=null&&now-row[key]<(gate||0))return false;
  row[key]=now;return weaponFeedbackSound(key,vol==null?1:vol);
}
function stage1Burning(e){return !!(e&&e._nef&&/^nef_s1_/.test(e._nef)&&!e.dead&&e._dyingT==null&&e.maxhp>0&&e.hp>0&&e.hp/e.maxhp<=.50);}
function stage1BurnDraw(e){
  if(!stage1Burning(e))return;
  const critical=e.hp/e.maxhp<=.25,t=e.t||0,w=e._drawW||e.w,h=e._drawH||e.h;
  const hard=/tank|apc|buggy|boat|corvette|craft/.test(e._nef),n=critical?2:1;
  ctx.save();ctx.translate(e.x,e.y+(e._navBob||0));if(e.spin)ctx.rotate(e.spin);if(e._navLean)ctx.rotate(e._navLean);
  for(let i=0;i<n;i++){
    const x=(n===1?-.08:(i?1:-1)*.16)*w,y=(hard?-.06:-.18)*h;
    const f=(Math.floor(t*12)+i*3)%8,fire=16+(critical?9:0),key='nxp_upward_'+f;
    weaponFeedbackArt(key,x,y-fire*.29,fire,null,.84,0,false);
    for(let k=0;k<2;k++){
      const u=(t*.90+k*.5+i*.27)%1,sz=(critical?27:21)*(1+u*.50);
      weaponFeedbackArt('nsd_chim_'+((Math.floor(t*9)+i*3+k*2)%8),x+u*4,y-8-u*24,sz,null,.57*(1-u),0,false);
    }
  }
  ctx.restore();
}
function stage2FlightFrame(kind){
  /* Rows are birth/growth examples, not onion aligned flight reels. Retain one full flight pose. */
  return /^s2/.test(kind)?1:null;
}
function stage3DroneShotDraw(b){
  if(!b._s3DroneShot)return false;
  const key='bpfx_proj_laser_0';if(!XART.rdy(key))return false;
  const im=XART.get(key),h=58,w=h*(im.width||im.naturalWidth)/(im.height||im.naturalHeight),a=Math.atan2(b.vy,b.vx)-Math.PI/2;
  const rim=xartTint(key,'#030611',1);ctx.save();ctx.translate(Math.round(b.x),Math.round(b.y));ctx.rotate(a);ctx.imageSmoothingEnabled=false;
  if(rim)for(const p of [[-2,0],[2,0],[0,-2],[0,2],[-1,-1],[1,-1],[-1,1],[1,1]])ctx.drawImage(rim,-w/2+p[0],-h/2+p[1],w,h);
  ctx.drawImage(im,-w/2,-h/2,w,h);
  ctx.save();ctx.beginPath();const y=-h/2+((b.t||0)*90%h);ctx.rect(-w/2,y,w,7);ctx.clip();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.50;ctx.drawImage(im,-w/2,-h/2,w,h);ctx.restore();ctx.restore();return true;
}
function spaceVolleyLaunchRack(level){
  const lv=clamp(level,1,5),hp=spaceShipHardpoints(player.x,player.y,SPACE_SHIP_SIZE),range=350+lv*18,
    seed={x:player.x,y:hp.nose.y},locks=spaceVolleyLocks(seed,range);
  const origins=[hp.laser[0],hp.nose,hp.laser[1]];
  for(let i=0;i<3;i++){
    const side=i-1,a=-Math.PI/2+side*.24,sp=6.2+lv*.32,p=origins[i];
    pBullets.push({kind:'spaceVolley',x:p.x,y:p.y,vx:Math.cos(a)*sp,vy:Math.sin(a)*sp,w:13,h:25,
      dmg:4+lv*1.4,lv,side,i,t:0,ang:a,spd:sp,_originX:p.x,_originY:p.y,_target:locks[i],_seekT:0,_lockRange:range,_hit:[]});
  }
  spaceWeaponCue('spaceVolleyLaunch','volleyLaunch');
}
function stage3WallLaserAttack(b,pat,step){
  const S=b&&b._s3boss;if(!S||S.role!=='wall')return false;
  const slots=['L','C','R'],angles=[Math.PI/2,Math.PI/2,Math.PI/2];let arc=[0,0,0],width=42,active=.72;
  if(pat==='s3wallgate'){angles[0]+=.72;angles[2]-=.72;arc=[.22,0,-.22];active=.95;}
  else if(pat==='s3wallhalo'){slots.splice(step&1?2:0,1);angles.splice(step&1?2:0,1);arc=[0,0];width=46;active=.88;}
  else if(pat==='s3walloverdrive'){angles[0]+=.95;angles[2]-=.95;arc=[.42,0,-.42];width=48;active=1.05;}
  else if(pat!=='s3wallcannons')return false;
  if(!l23BossBeamStart(b,'rime',slots,angles,L23_WARN_T,active,.24,width,{sweepArc:arc,sweepRate:2.6}))return true;
  S.volley=null;S.cannonSeq=null;S.charge={t:0,dur:L23_WARN_T,slot:'C',kind:'centerBeam'};
  S.lastPattern=pat;S.patternsSeen[pat]=(S.patternsSeen[pat]||0)+1;
  stage3BossBeginSlide(b,L23_WARN_T+active+1.05);b.fireCd=(L23_WARN_T+active+1.0)*1.35;
  return true;
}
function stage4GeneratorColumn(b,side){
  const left=camLeftX(),right=camRightX(),mid=(left+right)*.5,off=Math.min((right-left)*.5-29,b.w*.69+29);
  return {x:mid+side*off,y:(b._s4war.homeY||150)+78};
}
function stage4ShieldBeamNodes(b,x,halfW,top,bot){
  const H=b&&b._s4war&&b._s4war.shield;if(!H||!H.active)return [];
  return H.nodes.filter(n=>!n.dead&&n.y>=top-34&&n.y<=bot+34&&Math.abs(x-n.x)<=34+(halfW||0));
}
function stage4ContactFeedback(b,x,y,size,palette){
  explode(x,y,size,palette||'blue',null,null,null,null,true);
  stageRevisionCue(b,'sovereignContact',.10);
}
function stage4InterceptFeedback(q){
  explode(q.x,q.y,7,'red',null,null,null,null,true);
  const T=boss&&boss._s4war?boss:subBoss&&subBoss._s4war?subBoss:null;
  if(T)stageRevisionCue(T,'sovereignIntercept',.10);
}
function stage4PiercingBeam(b,shot){
  const nodes=stage4ShieldBeamNodes(b,shot.x,shot.w/2,shot.top,shot.bot),
    turrets=b&&b._s4war&&b._s4war.coreUnlocked?b._s4war.coreTurrets.filter(t=>!t.dead&&t.materialize>=.92&&
      t.y>=shot.top-S4H_HALF&&t.y<=shot.bot+S4H_HALF&&Math.abs(shot.x-t.x)<=58*S4H_SCALE+shot.w/2):[];
  if(!nodes.length&&!turrets.length)return false;
  /* Snapshot every intersection before either node is destroyed or the shield changes state. */
  for(const n of nodes){b._s4CoreHit=null;b._s4ShieldHit=n;_lastHitX=n.x;_lastHitY=n.y;hitBoss(shot.dmg);}
  for(const t of turrets){b._s4ShieldHit=null;b._s4CoreHit=t;_lastHitX=t.x;_lastHitY=t.y;hitBoss(shot.dmg);}
  weaponHitSfx('laser');return true;
}
function stage4MiniMachine(b,slot,a,spd){
  const p=typeof slot==='string'?shipBossMount(b,slot):slot;
  const q=eShootT(p.x,p.y,eAimDown(a),spd,'mg',{w:4,h:14,silent:true,szMul:1});
  q._s4wKind='machine';q._noArsenal=true;q._s4Mini=true;q._s4Slot=typeof slot==='string'?slot:null;
  return q;
}
function stage4MiniCenter(b){
  for(const slot of ['CL','CR']){stage4MiniMachine(b,slot,Math.PI/2,5.8);stage4WarfareMuzzle(b,slot,'mg',.58,.085);}
  stageRevisionCue(b,'wardenCenterGun',.10,.85);
}
function stage4MiniRocket(b,slot,a){
  const q=stage4WarfareShot(b,slot,a,1.7,'rocket',{accel:1.05,max:5.1,shootable:true,hp:2,szMul:.72});
  q._s4Mini=true;q._s4Slot=slot;
  stage4WarfareMuzzle(b,slot,'rocket',.85,.15);return q;
}
function stage4MiniDirector(b,dt){
  const S=b._s4war,W=worldWidth(),phase=shipBossPhase(b);S.t+=dt*(1+phase*.10);b.fireCd=999;
  const amp=Math.min(68,Math.max(24,W*.5-b.w*.62));b.y+=(S.homeY-b.y)*Math.min(1,dt*5.5);S.poseRot=0;S.scale=1;b._animKey=null;
  S.summoned=false;S.drones.length=0;
  if(S.mode==='burst'){
    b.x=W*.5+Math.sin(S.t*1.12)*amp;
    while(S.shot<=S.t){S.shot+=.145;const o=Math.sin(S.wave*.38)*.24;
      for(const slot of ['L','R']){
        stage4MiniMachine(b,slot,Math.PI/2+o+(slot==='L'?.12:-.12),5.20+phase*.20);
        stage4WarfareMuzzle(b,slot,'mg',.65,.10);
      }
      stageRevisionCue(b,'wardenGun',.12,.90);S.wave++;
    }
    if(S.t>=3.2)stage4WarfareSetMode(b,'center');
  }else if(S.mode==='center'){
    b.x+=(W*.5-b.x)*Math.min(1,dt*5);
    while(S.shot<=S.t){S.shot+=.11;stage4MiniCenter(b);S.wave++;}
    if(S.t>=1.45){stage4WarfareSetMode(b,'rockets');stageRevisionCue(b,'wardenRackCharge',0);}
  }else{
    b.x=W*.5+Math.sin(S.t*.65)*amp*.5;
    if(S.t>=.68&&S.event<4&&S.shot<=S.t){
      S.shot=S.t+.48;const a=Math.PI/2+(S.event&1?-.16:.16);
      stage4MiniRocket(b,'L',a+.12);stage4MiniRocket(b,'R',a-.12);
      stageRevisionCue(b,'wardenRocket',.20);S.event++;
    }
    if(S.t>=3.1)stage4WarfareSetMode(b,'burst');
  }
  return true;
}
function stage4RamStart(b){
  const S=b._s4war;if(!S||S.mini||S.shield.active||S.shield.rearming)return false;
  S.ram={t:0,lane:player.x,locked:false,speed:180,flyY:VH+210,shadowY:VH+210};stage4WarfareSetMode(b,'ramTell');
  stageRevisionCue(b,'sovereignDive',0);return true;
}
function stage4RamEnd(b){b._noHit=false;b._s4Airborne=false;b._s4war.ram=null;}
function stage4RamTick(b,dt){
  const S=b._s4war,R=S.ram;if(!R)return false;R.t+=dt;S.poseRot=0;S.scale=1;
  if(S.shield.active||S.shield.rearming||b.dead){stage4RamEnd(b);return false;}
  const frame=clamp(Math.floor(R.t*12),0,11);b._animKey='s4w_boss_charge_'+frame;
  if(S.mode==='ramTell'){
    if(R.t<.40)R.lane=clamp(player.x,72,worldWidth()-72);else R.locked=true;
    b.x+=(R.lane-b.x)*Math.min(1,dt*7);b.y+=(S.homeY-b.y)*Math.min(1,dt*6);
    if(R.t>=1.0){S.mode='ramDive';R.t=0;stageRevisionCue(b,'sovereignFlyby',0,.90);}
  }else if(S.mode==='ramDive'){
    R.speed=Math.min(740,R.speed+680*dt);b.x=R.lane;b.y+=R.speed*dt;
    b._animKey='s4w_boss_flight_'+(Math.floor(R.t*16)%12);
    if(b.y>VH+b.h*.65+72){S.mode='ramOff';R.t=0;b._noHit=true;}
  }else if(S.mode==='ramOff'){
    if(R.t>=.48){S.mode='ramOver';R.t=0;b._s4Airborne=true;stageRevisionCue(b,'sovereignFlyby',0,.72);}
  }else if(S.mode==='ramOver'){
    const u=clamp(R.t/1.25,0,1);R.flyY=lerp(VH+250,-250,u);R.shadowY=R.flyY+18;
    b.x=R.lane;b.y=R.flyY;b._animKey='s4w_boss_flight_'+(Math.floor(R.t*18)%12);
    if(u>=1){S.mode='ramReturn';R.t=0;b._s4Airborne=false;b.y=-b.h*.65-72;}
  }else{
    b.x+=(worldWidth()*.5-b.x)*Math.min(1,dt*3.0);b.y+=290*dt;b._animKey='s4w_boss_flight_'+(Math.floor(R.t*14)%12);
    if(b.y>=S.homeY){b.y=S.homeY;stage4RamEnd(b);stage4WarfareSetMode(b,'lightning');}
  }
  return true;
}
function stage4RamShadowDraw(b){
  const S=b&&b._s4war,R=S&&S.ram;if(!R)return;
  if(S.mode==='ramTell'){
    const p=shipBossMount(b,'C'),key='bmfx_fov_'+l23FovPhase(R.t)+'_tall';
    if(XART.rdy(key)){ctx.save();ctx.translate(R.lane,p.y);l23FovDraw(b,{family:'rime',angles:[Math.PI/2],t:R.t},0,p,R.t,38);ctx.restore();}
  }
  if(S.mode!=='ramOver')return;
  const key=b._animKey,im=xartTint(key,'#02040a',1);if(!im)return;
  ctx.save();ctx.globalAlpha=.38;ctx.imageSmoothingEnabled=false;ctx.drawImage(im,R.lane-b.w*.43,R.shadowY-b.h*.30,b.w*.86,b.h*.60);ctx.restore();
}
function stage4OverflightDraw(){
  if(!boss||boss.dead||!boss._s4Airborne||!boss._s4war.ram)return;
  const R=boss._s4war.ram,key=boss._animKey;
  weaponFeedbackArt(key,R.lane,R.flyY,boss.w*1.18,boss.h*1.18,1,0,false);
}
function xenoRegentFormationMove(b,dt){
  const R=b._xenoRig,left=camLeftX(),right=camRightX(),mid=(left+right)*.5;
  const x=mid+Math.sin(R.t*.48)*32,y=186+Math.sin(R.t*.63)*9;
  b.x+=(x-b.x)*Math.min(1,dt*3.0);b.y+=(y-b.y)*Math.min(1,dt*3.0);
}
function xenoRigAttackTick(b,part,dt){
  const Q=part.tell;if(!Q)return;Q.t+=dt;
  if(b._xenoGrid||part.dead){part.tell=null;return;}
  if(Q.t>=Q.dur){
    const offsets=part.role==='mother'?[-.16,0,.16]:[-.08,.08];
    for(let i=0;i<offsets.length;i++){
      const ox=part.role==='mother'?(i-1)*.23:0,p={x:part.x+ox*part.w,y:part.y+part.h*.30};
      spaceBossShot(p.x,p.y,Q.angle+offsets[i],part.role==='mother'?3.20:3.75,part.role==='mother'?'s5fracture':'s5null',{silent:true});
      xenoRegentMuzzle(part,ox);
    }
    stageRevisionCue(b,'bossfireXenoregent',.13,.70);part.anim=.42;part.tell=null;
  }
}
function xenoRigTell(part){part.tell={t:0,dur:part.role==='mother'?.75:.55,angle:aimPlayer(part.x,part.y+part.h*.3)};}
function xenoRigTellDraw(part){
  const Q=part&&part.tell;if(!Q||part.dead)return;
  const p=clamp(Q.t/Q.dur,0,1),h=part.role==='mother'?52:34;
  weaponFeedbackArt('bpfx_muzzle_void_'+(Math.floor(p*7)%8),part.x,part.y+part.h*.30,h*(.55+p*.50),null,.40+p*.40,0,true);
}
