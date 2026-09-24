"use strict";
/* Stage 3 elemental escalation. Whole authored plates and effect sprites live in
   assets/game/bosses/stage3_thermo; only their placement and timing are simulated. */
const S3_THERMO_STRIKE={mini:null,boss:null};
const S3_THERMO_ART='s3thermo_';
function s3ThermoReady(key){return typeof XART!=='undefined'&&XART.rdy(S3_THERMO_ART+key);}
function s3ThermoImage(key){return s3ThermoReady(key)?XART.get(S3_THERMO_ART+key):null;}
function s3ThermoSound(...names){
  try{for(const n of names){const f=Audio&&Audio.SFX&&Audio.SFX[n];if(f){f();return;}}}catch(_e){}
}
function s3ThermoWarm(){
  for(const k of ['strike_jet','thermocloud','therno_robonoid','nuclear_fire','ice_orb','thermo_orb','ice_shards','fire_disintegrate','nuclear_retina',
    'thermocloud_idle_sheet','thermocloud_attack_sheet','therno_attack_sheet','nuclear_fire_sheet'])s3ThermoReady(k);
}
function s3ThermoSheet(key,frame,x,y,w,h){
  const im=s3ThermoImage(key);if(!im)return false;
  const fw=im.width/8,fh=im.height;
  ctx.drawImage(im,(frame&7)*fw,0,fw,fh,x,y,w,h);return true;
}
function s3ThermoCloudInit(b){
  b.name='THERMOCLOUD EYE';b.w=184;b.h=184;b.ty=145;
  b.hp=b.maxhp=Math.ceil(1050*DIFF.eHp);
  b._s3Thermo={role:'mini',mode:'ice',clock:0,cycle:0,charge:null,shots:0,hitT:0,parts:null};
  b._s3ice=true;b._fireEnemy=false;s3ThermoWarm();
}
function s3ThernoInit(b){
  b.name='THERNO, THE SHOCKBRINGER';b.w=262;b.h=280;b.ty=145;
  b.hp=b.maxhp=Math.ceil(b.maxhp*1.55);
  b._s3Thermo={role:'boss',mode:'ice',clock:0,cycle:0,charge:null,shots:0,hitT:0,
    parts:{fireShoulder:1,iceShoulder:1,mace:1}};
  b._s3ice=true;b._fireEnemy=false;s3ThermoWarm();
}
function s3ThermoForm(b,mode){
  const T=b._s3Thermo;if(!T)return;
  T.mode=mode;b._s3ice=mode==='ice';b._fireEnemy=mode==='fire';
  b._hitFlashColor=mode==='fire'?'#ff743d':mode==='ice'?'#95e8ff':'#e5b8ff';
  s3ThermoSound('bossPhase','enemyElectricBolt');
}
function s3ThermoShoot(b,mode,x,y,a,speed,large){
  const kind=mode==='fire'?'magma':'s3mortar';
  const size=large?34:mode==='thermal'?22:15;
  const q=eShootT(x,y,a,speed,kind,{w:size,h:size,silent:true});
  q._boss=true;q._noArsenal=true;q._s3ThermoArt=mode;q._s3ThermoSpin=mode==='thermal'?7:4;
  q.dmg=large?2:1;q._shootable=!!large;q.hp=large?2:undefined;
  b._s3Thermo.shots++;return q;
}
function s3ThermoProjectileDraw(q){
  let key=q.kind==='s3shard'?'ice_shards':q._s3ThermoArt==='thermal'?'thermo_orb':q._s3ThermoArt==='ice'?'ice_orb':'nuclear_fire';
  const im=s3ThermoImage(key);if(!im)return false;
  const size=q.w*(q._s3Orb?2.15:1.65),angle=(q.t||0)*(q._s3ThermoSpin||4);
  ctx.save();ctx.translate(q.x,q.y);ctx.rotate(angle);ctx.imageSmoothingEnabled=false;
  ctx.drawImage(im,-size/2,-size/2,size,size);ctx.restore();return true;
}
function s3ThermoRadial(b,mode,n,speed,aimGap){
  const base=aimPlayer(b.x,b.y),gap=aimGap==null?0:aimGap;
  for(let i=0;i<n;i++){
    const a=i*TAU/n+base*.20;if(gap&&Math.abs(Math.atan2(Math.sin(a-base),Math.cos(a-base)))<gap)continue;
    s3ThermoShoot(b,mode,b.x,b.y+b.h*.25,a,speed,false);
  }
}
function s3ThermoStartOrb(b){
  const T=b._s3Thermo;if(!T)return;
  T.charge={t:0,mode:'ice',aim:null,released:false};
  if(diffKey==='hard'||diffKey==='furious'){
    try{enemyLockOn(b,.95,{fire:function(){}});}catch(_e){}
  }
  s3ThermoSound('cryoOrb','bossWeaponCharge');
}
function s3ThermoBurstOrb(q){
  if(!q||q._s3OrbBurst)return;q._s3OrbBurst=true;
  const n=12,base=(q.t||0)*.8;
  for(let i=0;i<n;i++){
    const a=base+i*TAU/n,p=eShootT(q.x,q.y,a,3.4,'s3shard',{w:11,h:17,silent:true});
    p._boss=true;p._noArsenal=true;p._s3ThermoArt='ice';p._s3ThermoSpin=5;
  }
  if(typeof explode==='function')explode(q.x,q.y,28,'blue');
  const qi=eBullets.indexOf(q);if(qi>=0)eBullets.splice(qi,1);
  s3ThermoSound('shatter','iceOrbImpact');
}
function s3ThernoModuleHit(b,dmg,x,y){
  const T=b&&b._s3Thermo;if(!T||T.role!=='boss'||!T.parts)return dmg;
  const rx=(x-b.x)/b.w,ry=(y-b.y)/b.h;
  const name=ry>.20?'mace':rx<-.18?'fireShoulder':rx>.18?'iceShoulder':null;
  if(!name||T.parts[name]<=0)return dmg;
  T.parts[name]=Math.max(0,T.parts[name]-dmg/(b.maxhp*.14));
  T.hitT=.22;
  if(T.parts[name]===0){
    const px=b.x+(name==='fireShoulder'?-b.w*.30:name==='iceShoulder'?b.w*.30:0);
    const py=b.y+(name==='mace'?b.h*.25:-b.h*.17);
    explode(px,py,54,name==='fireShoulder'?'orange':'blue');
    s3ThermoSound('shieldBreakCombat','expBig');shake=Math.max(shake,7);
  }
  return dmg*.72;
}
function s3ThermoOrbTick(b,dt){
  const T=b._s3Thermo,C=T&&T.charge;
  if(C){
    C.t+=dt;
    if(!C.released&&C.t>=.95){
      const target=targetShip(b.x,b.y),x=b.x,y=b.y+b.h*.35;
      const a=Math.atan2(target.y-y,target.x-x);
      const q=s3ThermoShoot(b,'ice',x,y,a,2.25,true);
      q._s3Orb=true;q._s3OrbAge=0;q._s3OrbTarget={x:target.x,y:target.y};
      T.orb=q;C.released=true;s3ThermoSound('enemyIceBolt','enemyBossCannon');
    }
    if(C.t>=1.55)T.charge=null;
  }
  const q=T&&T.orb;
  if(q&&!q._s3OrbBurst){
    q._s3OrbAge+=dt;
    const near=q._s3OrbTarget&&Math.hypot(q.x-q._s3OrbTarget.x,q.y-q._s3OrbTarget.y)<29;
    if(near||q._s3OrbAge>1.55||eBullets.indexOf(q)<0){s3ThermoBurstOrb(q);T.orb=null;}
  }
}
function s3ThermoAttack(b){
  const T=b._s3Thermo,mini=T.role==='mini',step=T.cycle++;
  if(mini&&step%4===3){
    const target=targetShip(b.x,b.y);
    T.dive={t:0,fromX:b.x,fromY:b.y,toX:clamp(target.x,b.w*.5+20,worldWidth()-b.w*.5-20),
      toY:clamp(target.y-100,245,Math.min(VH*.67,580))};
    T.clock=2.35;s3ThermoSound('bossWeaponCharge','dangerAlert');return;
  }
  const mode=['ice','fire','thermal'][step%3];s3ThermoForm(b,mode);
  if(mode==='ice'){
    if(mini||T.parts.iceShoulder>0)s3ThermoStartOrb(b);
    else {const a=aimPlayer(b.x,b.y),y=b.y+b.h*.3;
      for(let i=-2;i<=2;i++)s3ThermoShoot(b,'ice',b.x,y,a+i*.18,3.25,false);}
    T.clock=mini?2.65:2.25;
  }else if(mode==='fire'){
    const x=b.x,y=b.y+b.h*.36,a=aimPlayer(x,y),n=mini?5:7;
    if(mini||T.parts.fireShoulder>0)for(let i=0;i<n;i++)s3ThermoShoot(b,'fire',x,y,a+(i-(n-1)/2)*.16,mini?3.4:3.85,false);
    else for(let i=-1;i<=1;i++)s3ThermoShoot(b,'ice',x,y,a+i*.19,3.15,false);
    if(!mini&&T.parts.fireShoulder>0)s3ThermoRadial(b,'fire',12,2.65,.28);
    T.clock=mini?2.1:2.0;s3ThermoSound('magmaOrb','enemyFlameBolt');
  }else{
    const x=b.x,y=b.y+b.h*.32,a=aimPlayer(x,y);
    for(const off of (mini?[-.25,0,.25]:T.parts.mace>0?[-.36,-.18,0,.18,.36]:[-.2,0,.2]))
      s3ThermoShoot(b,'thermal',x,y,a+off,mini?3.25:3.75,true);
    if(!mini&&T.parts.mace>0)s3ThermoRadial(b,'thermal',10,2.8,.24);
    T.clock=mini?2.4:2.05;s3ThermoSound('enemyElectricBolt','bossWeaponCharge');
  }
}
function s3ThermoTick(b,dt){
  const T=b._s3Thermo;if(!T)return;
  if(T.role==='boss')b.t+=dt;
  b.flash=Math.max(0,(b.flash||0)-dt);
  if(b.dead){b.dying=(b.dying||0)+dt;return;}
  if(b.enter){
    b.y+=(b.ty-b.y)*Math.min(1,dt*3.5);
    if(Math.abs(b.y-b.ty)<2||b.t>3.5){b.y=b.ty;b.enter=false;T.clock=.7;}
    return;
  }
  T.hitT=Math.max(0,T.hitT-dt);
  if(T.dive){
    const D=T.dive;D.t+=dt;
    if(D.t<.65){b.x=D.fromX;b.y=D.fromY;}
    else if(D.t<1.17){const p=clamp((D.t-.65)/.52,0,1);b.x=D.fromX+(D.toX-D.fromX)*p;b.y=D.fromY+(D.toY-D.fromY)*p;}
    else if(D.t<1.85){const p=clamp((D.t-1.17)/.68,0,1);b.x=D.toX+(D.fromX-D.toX)*p;b.y=D.toY+(D.fromY-D.toY)*p;}
    else{T.dive=null;b.x=D.fromX;b.y=D.fromY;T.clock=.5;}
    if(D.t>=.65&&!D.launched){D.launched=true;s3ThermoRadial(b,T.mode,10,3.15,.20);s3ThermoSound('enemyElectricBolt','enemyBossCannon');}
    if(T.dive)return;
  }
  const target=targetShip(b.x,b.y),margin=b.w*.5+15;
  const wantX=T.role==='mini'?clamp(target.x+(Math.sin(b.t*1.8)*75),margin,worldWidth()-margin)
                              :clamp(worldWidth()*.5+Math.sin(b.t*.95)*75,margin,worldWidth()-margin);
  b.x+=(wantX-b.x)*Math.min(1,dt*(T.role==='mini'?2.9:1.5));
  b.y=b.ty+Math.sin(b.t*(T.role==='mini'?3.2:1.9))*(T.role==='mini'?13:8);
  s3ThermoOrbTick(b,dt);
  T.clock-=dt;
  if(T.clock<=0)s3ThermoAttack(b);
}
function s3ThermoDraw(b){
  const T=b._s3Thermo;if(!T)return;
  const key=T.role==='mini'?'thermocloud':'therno_robonoid',im=s3ThermoImage(key);
  if(im){
    const dy=b.y+Math.sin((b.t||0)*2.7)*3;
    ctx.save();ctx.imageSmoothingEnabled=false;
    const frame=Math.floor((b.t||0)*9)%8;
    const sheet=T.role==='mini'?(T.charge||T.clock<.75?'thermocloud_attack_sheet':'thermocloud_idle_sheet'):'therno_attack_sheet';
    if(!s3ThermoSheet(sheet,frame,b.x-b.w/2,dy-b.h/2,b.w,b.h))
      ctx.drawImage(im,b.x-b.w/2,dy-b.h/2,b.w,b.h);
    if(b.flash>0&&typeof xartTint==='function'){
      const tint=xartTint(S3_THERMO_ART+key,hitFlashColor(b,'#ffffff'),.85);
      if(tint){ctx.globalAlpha=Math.min(.75,b.flash*4);ctx.drawImage(tint,b.x-b.w/2,dy-b.h/2,b.w,b.h);}
    }
    if(T.parts&&T.hitT>0){
      const ret=s3ThermoImage('nuclear_retina');if(ret){ctx.globalAlpha=T.hitT*2;
        ctx.drawImage(ret,b.x-b.w*.34-20,dy-b.h*.22-20,40,40);
        ctx.drawImage(ret,b.x+b.w*.34-20,dy-b.h*.22-20,40,40);
        ctx.globalAlpha=1;}
    }
    if(T.parts){const wreck=s3ThermoImage('fire_disintegrate');if(wreck){
      ctx.globalAlpha=.53+.13*Math.sin((b.t||0)*8);
      if(T.parts.fireShoulder<=0)ctx.drawImage(wreck,b.x-b.w*.34-40,dy-b.h*.18-40,80,80);
      if(T.parts.iceShoulder<=0)ctx.drawImage(wreck,b.x+b.w*.34-40,dy-b.h*.18-40,80,80);
      if(T.parts.mace<=0){ctx.drawImage(wreck,b.x-b.w*.42-46,dy+b.h*.22-46,92,92);
        ctx.drawImage(wreck,b.x+b.w*.42-46,dy+b.h*.22-46,92,92);}
      ctx.globalAlpha=1;
    }}
    ctx.restore();
  }
  if(T.dive&&T.dive.t<.65){const ret=s3ThermoImage('nuclear_retina');if(ret){
    ctx.save();ctx.globalAlpha=.25+.5*T.dive.t/.65;
    ctx.drawImage(ret,T.dive.toX-50,T.dive.toY-50,100,100);ctx.restore();
  }}
  if(T.charge){const orb=s3ThermoImage('ice_orb');if(orb){
    const q=clamp(T.charge.t/.95,0,1),sz=20+q*45;
    ctx.save();ctx.globalAlpha=.45+.55*q;ctx.drawImage(orb,b.x-sz/2,b.y+b.h*.38-sz/2,sz,sz);ctx.restore();
  }}
}
function s3ThermoStrikeTick(role,b,dt){
  if(!b||run.stage!==3||diffKey!=='furious')return false;
  const expected=role==='mini'?'frostcruiser':'cryospear';
  if(b.kind!==expected||b.dead)return false;
  let S=S3_THERMO_STRIKE[role];
  if(!S){
    if((b.t||0)<2.25||b.enter)return false;
    s3ThermoWarm();S=S3_THERMO_STRIKE[role]={t:0,beat:-1,x:b.x,y:b.y,impact:false,old:b};
    b._noHit=true;b._jcGhost=true;
    if(b._s3boss){b._s3boss.volley=null;b._s3boss.cannonSeq=null;b._s3boss.charge=null;}
    b._l23Beam=null;
    s3ThermoSound('stage3AtomicSiren','atomicLaunch');
  }
  S.t+=dt;b.x=S.x;b.y=S.y;
  if(role==='boss')b.t+=dt;
  const beat=Math.floor(Math.max(0,S.t-.28)/.22);
  if(S.t>=.28&&beat>S.beat&&S.t<1.7){S.beat=beat;s3ThermoSound('alertLockon','dangerAlert','blip');}
  if(S.t>=1.72&&!S.impact){
    S.impact=true;shake=Math.max(shake,16);flashScreen=Math.max(flashScreen,.42);
    s3ThermoSound('atomicDetonate','expBig','bossExplosion');
    if(typeof explode==='function')explode(S.x,S.y,role==='boss'?230:125,'orange');
  }
  if(S.t>=3.65){
    S3_THERMO_STRIKE[role]=null;
    if(role==='mini')spawnSubBoss__inner('thermocloud');
    else spawnBoss('therno');
  }
  return true;
}
function s3ThermoStrikeDraw(role,b){
  const S=S3_THERMO_STRIKE[role];if(!S||S.old!==b)return false;
  if(b._ship&&typeof shipBossDraw==='function')shipBossDraw(b);
  const retina=s3ThermoImage('nuclear_retina'),jet=s3ThermoImage('strike_jet');
  if(S.t<1.75){
    const q=clamp((S.t-.15)/1.55,0,1),sz=role==='boss'?250:180;
    if(retina){ctx.save();ctx.globalAlpha=.35+.55*q;ctx.drawImage(retina,S.x-sz/2,S.y-sz/2,sz,sz);ctx.restore();}
    if(role==='mini'&&jet){const y=VH+80-S.t*410;ctx.drawImage(jet,worldWidth()*.5-65,y-75,130,150);}
  }else{
    const fire=s3ThermoImage(S.t<2.7?'nuclear_fire':'fire_disintegrate');
    if(fire){const q=clamp((S.t-1.72)/.72,0,1),size=(role==='boss'?440:255)*(S.t<2.6?.25+.75*q:1);
      if(S.t<2.7){if(!s3ThermoSheet('nuclear_fire_sheet',Math.floor(q*8),S.x-size/2,S.y-size/2,size,size))
        ctx.drawImage(fire,S.x-size/2,S.y-size/2,size,size);}
      else ctx.drawImage(fire,S.x-size/2,S.y-size/2,size,size);}
    const flash=(S.t<2.65?((Math.floor((S.t-1.72)*10)&1)?'#ff3b23':'#ffffff'):
      S.t<3.0?'#ffffff':null);
    if(flash){ctx.save();ctx.globalAlpha=S.t<2.45?.72:.26;ctx.fillStyle=flash;
      ctx.fillRect(camLeftX(),viewTopY(),viewW(),viewH());ctx.restore();}
  }
  return true;
}

/* The existing Stage-3 ships use the same authored orb/shard sprites. The orb
   commits its target at release; Hard can track through the charge warning. */
function s3FrostOrbBegin(b){
  const J=b&&b._jc;if(!J)return;
  J.iceOrbCharge={t:0,released:false,target:null};
  s3ThermoReady('ice_orb');s3ThermoReady('ice_shards');
  if(diffKey==='hard'&&typeof enemyLockOn==='function')enemyLockOn(b,.92,{fire:function(){}});
  s3ThermoSound('cryoOrb','bossWeaponCharge');
}
function s3FrostOrbTick(b,dt){
  const J=b&&b._jc;if(!J)return;
  const C=J.iceOrbCharge;
  if(C){
    C.t+=dt;
    if(!C.released&&C.t>=.92){
      const m=shipBossMount(b,'C'),target=targetShip(m.x,m.y),a=Math.atan2(target.y-m.y,target.x-m.x);
      const q=eShootT(m.x,m.y,a,diffKey==='hard'?2.8:2.35,'s3mortar',{w:38,h:38,silent:true});
      q._boss=true;q._noArsenal=true;q._s3ThermoArt='ice';q._s3Orb=true;
      q._s3OrbAge=0;q._s3OrbTarget={x:target.x,y:target.y};J.iceOrb=q;
      C.released=true;s3ThermoSound('enemyIceBolt','enemyBossCannon');
    }
    if(C.t>1.5)J.iceOrbCharge=null;
  }
  const q=J.iceOrb;
  if(q&&!q._s3OrbBurst){
    q._s3OrbAge+=dt;
    const near=q._s3OrbTarget&&Math.hypot(q.x-q._s3OrbTarget.x,q.y-q._s3OrbTarget.y)<30;
    if(near||q._s3OrbAge>1.6||eBullets.indexOf(q)<0){s3ThermoBurstOrb(q);J.iceOrb=null;}
  }
}
function s3FrostOrbDraw(b){
  const C=b&&b._jc&&b._jc.iceOrbCharge,im=C&&s3ThermoImage('ice_orb');
  if(!im||C.released)return;
  const m=shipBossMount(b,'C'),q=clamp(C.t/.92,0,1),size=18+q*53;
  ctx.save();ctx.globalAlpha=.4+.6*q;ctx.imageSmoothingEnabled=false;
  ctx.drawImage(im,m.x-size/2,m.y-size/2,size,size);ctx.restore();
}
function s3WallOrbTick(b,dt){
  const S=b&&b._s3boss;if(!S||S.role!=='wall')return;
  for(const q of eBullets){
    if(!q._s3BurstIce||q._s3OrbBurst)continue;
    q._s3OrbAge=(q._s3OrbAge||0)+dt;
    if(q.y>=player.y-22||q._s3OrbAge>2.25)s3ThermoBurstOrb(q);
  }
}
function s3HardWallTrack(b,pat){
  if(diffKey!=='hard'||!b||b.dead||typeof enemyLockOn!=='function')return;
  const S=b._s3boss;if(!S||S.role!=='wall')return;
  const serial=S._earlyTrackSerial=(S._earlyTrackSerial||0)+1;
  enemyLockOn(b,.72,{fire:function(){
    if(!boss||boss!==b||b.dead||!b._s3boss||b._s3boss._earlyTrackSerial!==serial)return;
    const p=shipBossMount(b,'C'),a=aimPlayer(p.x,p.y);
    for(const off of [-.12,0,.12]){
      const q=stage3BossShot(b,'C',a+off,2.55,'s3lance',{w:17,h:25,accel:.65,max:5.2,shootable:true,silent:off!==0});
      q._threatBullet=1.05;
    }
    stage3BossMuzzle(b,'C','s3lance',1.1,.18);
  }});
}
