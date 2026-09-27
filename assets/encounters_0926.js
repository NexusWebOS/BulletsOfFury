"use strict";
/* Stage 2ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“4 encounter revision. Whole authored hulls, shared warning plates and
   engine ordnance; one director owns each attack channel. Mike, 2026-09-26. */
const ER26_STAGE={magmaward:2,frostcruiser:3,cryospear:3,olivewarden:4,stormsovereign:4};
const ER26_PALETTES=new Map();
function er26Owns(b){return !!(b&&ER26_STAGE[b._ship]===run.stage&&!b._scene);}
function er26Level(){return diffKey==='furious'?2:diffKey==='hard'?1:0;}
function er26Sound(...names){s3ThermoSound(...names);}
function er26Warm(){
  for(const prefix of ['mwfx_fireball_','mwfx_fireball_charge_','l23fx_cryo_ball_','l23fx_rime_orb_'])
    for(let i=0;i<8;i++)XART.rdy(prefix+i);
  for(let i=0;i<8;i++)XART.rdy('l23fx_inferno_mg_'+i);
  for(let i=0;i<12;i++){XART.rdy('l23fx_inferno_laser_'+i);XART.rdy('l23fx_rime_laser_'+i);}
  XART.rdy('lz_bomb');l23FovWarm();
}
function er26Init(b){
  if(!er26Owns(b)||b._er26)return;
  const hp={magmaward:1800,frostcruiser:2050,cryospear:3600,olivewarden:2050,stormsovereign:4400};
  b.hp=b.maxhp=Math.ceil(hp[b._ship]*DIFF.eHp);
  const R=b._er26={level:er26Level(),clock:0,t:0,serial:0,index:-1,phase:0,mode:'recover',
    dur:1.15,shot:0,wave:0,shots:0,side:-1,home:Math.max(b.ty||150,b.h*.5+32),
    from:{x:b.x,y:b.y},to:{x:worldWidth()/2,y:Math.max(b.ty||150,b.h*.5+32)},
    warnings:[],history:[],seeds:[],helperShots:0,bodyShots:0,form:'neutral',formBeats:0,completed:0,
    neutralOpening:run.stage===3&&er26Level()===2};
  if(b._ship==='frostcruiser'){
    b.w=202;b.h=202;R.home=Math.max(b.ty||150,150);R.to.y=R.home;
    // Keep the original Frost Cruiser, including its authored mounts, at every difficulty.
    b._jc.hardVariant=false;b._jc.mode='idle';b._jc.poseRot=0;
  }
  if(b._ship==='magmaward'&&R.level===2)b.name='CHARRED INFERNO REAVER';
  if(b._s4war){b._s4war.homeY=R.home;b._s4war.poseRot=0;}
  b.fireCd=999;er26Warm();
}
function er26Move(b,R,t){
  const q=clamp(t,0,1),u=q*q*(3-2*q);
  b.x=lerp(R.from.x,R.to.x,u);b.y=lerp(R.from.y,R.to.y,u);b._drawY=b.y;
}
function er26Station(b,side){
  const L=camLeftX(),W=camRightX()-L,H=b._s4war&&b._s4war.shield;
  const span=H&&(H.active||H.rearming)?(H.anchorX||204)+34:b.w*.53+18;
  const pad=Math.min(W*.5,Math.max(Math.min(W*.42,b.w*.53+18),span));
  return clamp(L+W*(side<0?.24:side>0?.76:.5),L+pad,L+W-pad);
}
function er26Book(b){
  const R=b._er26;
  if(b._ship==='magmaward')return R.level===2?
    ['charred-battery','ash-pursuit','charcoal-wheel','blackout-pass','charred-mortar','cinder-scissors','ash-eruption']:
    ['ember-hunt','furnace-strafe','ember-mortar','furnace-lance','ember-bombard'];
  if(b._ship==='frostcruiser')return ['cryo-crosscut','icebreaker','shatter-wheel','pincer-lance','cryo-mortar','cryo-crosscut'];
  if(b._ship==='cryospear')return ['bastion-gates','cannon-relay','orb-siege','glacier-press','cryo-mortar','cannon-relay'];
  if(b._ship==='olivewarden')return ['warden-suppress','escort-crossfire','rocket-feint','warden-drive','center-break'];
  return ['sovereign-battery','escort-crossfire','siege-rockets','ion-scissors','siege-mortar','siege-drive','core-barrage'];
}
function er26Set(b,mode){
  const R=b._er26;
  if(mode==='recover'&&!['recover','form-change','nuclear'].includes(R.mode)){
    R.completed++;if(b._s3Nuclear)R.formBeats++;
  }
  R.mode=mode;R.t=0;R.shot=0;R.wave=0;R.warnings=[];R.beamStarted=false;R.groundCast=false;R.laneCast=false;R.serial++;
  R.from={x:b.x,y:b.y};R.side=-R.side;
  R.to={x:er26Station(b,R.side),y:R.home};
  R.target={x:clamp(player.x,camLeftX()+30,camRightX()-30),y:player.y};
  R.history.push({mode,phase:R.phase,form:R.form,time:R.clock});if(R.history.length>48)R.history.shift();
  const n=R.level;
  R.warm=[1.05,.90,.78][n];R.live=[2.65,2.70,3.0][n];R.gap=[.34,.25,.18][n];
  if(mode==='recover'){R.dur=[1.10,.84,.68][n];R.to={x:er26Station(b,0),y:R.home};return;}
  if(mode==='form-change'){
    R.dur=1.55;R.to={x:er26Station(b,0),y:R.home};b._noHit=true;R.formApplied=false;R.formNext=R.form==='fire'?'ice':'fire';
    er26Sound('bossPhase','bossWeaponCharge');return;
  }
  if(/lance|cannon-relay/.test(mode)){R.warm=3;R.live=1.2+n*.18;}
  if(/pass|strafe|icebreaker|drive/.test(mode)){R.warm=1.25-n*.12;R.live=2.2-n*.25;}
  if(mode==='escort-crossfire'){R.warm=1;R.live=5.4;R.to.x=er26Station(b,0);}
  if(mode==='orb-siege'||mode==='charcoal-wheel'){R.live=2.9;R.gap=.82-n*.12;}
  if(mode==='glacier-press'){R.live=3.2;R.gap=.72-n*.1;R.to.y=R.home+62;}
  R.dur=R.warm+R.live;
  if(b._s3Nuclear&&R.form==='fire')R.gap*=.82;
  if(diffKey==='easy'){R.gap*=1.65;if(R.warm){R.warm*=1.3;R.dur=R.warm+R.live;}if(mode==='recover')R.dur*=1.4;}
  R.angles=['L','C','R'].map(slot=>{const p=shipBossMount(b,slot);return Math.atan2(R.target.y-p.y,R.target.x-p.x);});
  er26Sound('bossWeaponCharge','enemyBossCannon');
}
function er26Next(b){
  const R=b._er26;
  if(b._s3Nuclear&&R.formBeats>=2){R.formBeats=0;er26Set(b,'form-change');return;}
  const book=er26Book(b);R.index=(R.index+1)%book.length;er26Set(b,book[R.index]);
}
function er26Warning(b,slot,angle,width=38){
  const R=b._er26,p=typeof slot==='string'?shipBossMount(b,slot):slot;
  R.warnings.push({slot,x:p.x,y:p.y,angle,width});
}
function er26Shot(b,slot,a,speed,opt={}){
  if(typeof mr27CanFire==='function'&&!mr27CanFire(b,slot))return {dead:true};
  if(typeof mr27Fire==='function')mr27Fire(b,slot,a);
  const R=b._er26,p=typeof slot==='string'?shipBossMount(b,slot):slot;
  const fire=b._ship==='magmaward'||b._s3Nuclear&&R.form==='fire',charred=b._ship==='magmaward'&&R.level===2;
  const size=opt.large?24:12;
  const q=eShootT(p.x,p.y,a,speed,fire?'magma':'s3mortar',{w:size,h:size,silent:true,curve:opt.curve||0,noMuzzle:typeof slot!=='string'});
  q._boss=true;q._noArsenal=true;q._er26Art=fire?'fire':'ice';q._er26Charred=charred;q._er26Large=!!opt.large;
  q._er26Source=b._ship;q._er26Serial=R.serial;q._er26Draw=opt.large?52:26;
  q._weaponProof=!opt.large;q._shootable=!!opt.large;if(opt.large)q.hp=3;
  R.shots++;if(typeof combatAudio0927==='function')combatAudio0927(b,fire?'combatOrb0927':'combatIce0927',.24);
  if(opt.burst)R.seeds.push({q,t:0,form:q._er26Art,charred,at:1.35,gap:R.target.x});
  return q;
}
function er26Muzzle(b,slot){
  const fire=b._ship==='magmaward'||b._er26.form==='fire';
  shipBossMuzzleStart(b,[slot],{life:.16,hpx:44,fam:fire?'magma':'cryo'});
}
function er26Fan(b,slot,a,n,spread,speed,opt){
  for(let j=0;j<n;j++)er26Shot(b,slot,a+(j-(n-1)/2)*spread,speed,opt);
  er26Muzzle(b,slot);
}
function er26Seeds(b,dt){
  const R=b._er26;
  for(const s of R.seeds){
    s.t+=dt;if(s.q.dead||!eBullets.includes(s.q)){s.done=true;continue;}
    if(s.t<s.at)continue;
    const q=s.q,n=8+R.level*2,aim=Math.atan2(player.y-q.y,player.x-q.x);
    for(let j=0;j<n;j++){
      const a=j*TAU/n+Math.PI/2;
      // Always leave a two-round-wide escape sector toward the player's side.
      if(Math.abs(Math.atan2(Math.sin(a-aim),Math.cos(a-aim)))<.38)continue;
      const p=er26Shot(b,q,a,2.5+R.level*.3);p._er26Art=s.form;p._er26Charred=s.charred;
    }
    explode(q.x,q.y,28,s.form==='fire'?'red':'blue');q.dead=true;s.done=true;
    er26Sound('iceOrbImpact','expSmall');
  }
  R.seeds=R.seeds.filter(s=>!s.done);
}
function er26Combat(b,dt){
  const R=b._er26,n=R.level,t=R.t,live=t-R.warm,speed=3.4+n*.48+R.phase*.18+(R.form==='fire'?.35:0),mode=R.mode;
  if(typeof polishEncounterAttack==='function'&&polishEncounterAttack(b,dt))return;
  const moving=/pass|strafe|icebreaker/.test(mode);
  R.warnings=[];
  if(moving){
    // Stage on one flank before the crossing run; the active pass interpolates from
    // that actual position. No center/edge teleport at either boundary.
    if(t<R.warm){b.x+=(er26Station(b,-R.side)-b.x)*Math.min(1,dt*5);b.y+=(R.home-b.y)*Math.min(1,dt*5);}
    else {if(!R.passFrom)R.passFrom={x:b.x,y:b.y};const u=clamp(live/R.live,0,1);b.x=lerp(R.passFrom.x,R.to.x,u*u*(3-2*u));}
  }else if(mode==='glacier-press')er26Move(b,R,t/R.dur);
  else {b.x+=(R.to.x-b.x)*Math.min(1,dt*1.7);b.y+=(R.home-b.y)*Math.min(1,dt*3);}
  b._drawY=b.y;
  if(/lance|cannon-relay/.test(mode)){
    if(!R.beamStarted){
      const slots=(mode==='cannon-relay'?[(R.index&1)?'R':'L','C']:['L','R']).filter(s=>typeof mr27CanFire!=='function'||mr27CanFire(b,s));
      const angles=slots.map(s=>s==='L'?Math.PI/2+.30:s==='R'?Math.PI/2-.30:Math.PI/2);
      const family=b._ship==='magmaward'||R.form==='fire'?'inferno':'rime';
      l23BossBeamStart(b,family,slots,angles,3,R.live,.24,mode==='cannon-relay'?32:25);R.beamStarted=true;
      R.dur=3+R.live+.24;
    }
    if(b._l23Beam)l23BossBeamTick(b,dt);
    if(b._smz)b._smz.fam=b._ship==='magmaward'||R.form==='fire'?'magma':'cryo';
    return;
  }
  const aimed=/hunt|pursuit|crosscut|bombard/.test(mode);
  for(const slot of ['L','R'])er26Warning(b,slot,aimed?R.angles[slot==='L'?0:2]:Math.PI/2,mode==='blackout-pass'?52:36);
  if(t<R.warm){combatWarningTick(b,'er26-'+R.serial,t,R.warm,true);return;}
  R.shot-=dt;if(R.shot>0)return;
  R.shot+=R.gap;const wave=R.wave++,side=(wave&1)?'R':'L',a=R.angles[side==='L'?0:2];
  if(mode==='ember-hunt'||mode==='ash-pursuit'){
    // Four committed rounds, then reacquire visibly on the next attack; no late steering.
    er26Fan(b,side,a+(wave%3-1)*.11,mode==='ash-pursuit'?5:3,.13,speed+.50);R.shot+=wave%4===3?.32:0;
  }else if(mode==='furnace-strafe'||mode==='blackout-pass'||mode==='icebreaker'){
    const band=Math.floor((b.x-camLeftX())/viewW()*5),safe=R.index%5;
    if(band!==safe)er26Fan(b,'C',Math.PI/2,mode==='blackout-pass'?3:2,.12,speed-.3);
    if(wave%3===0)er26Shot(b,side,Math.PI/2+((wave&1)?-.3:.3),speed-.8,{large:true});
  }else if(mode==='ash-eruption'){
    if(wave<4){for(const off of [-.22,.22])er26Shot(b,'C',R.angles[1]+off,2.3,{large:true,burst:true});er26Muzzle(b,'C');}
    R.shot+=.58;
  }else if(mode==='ember-bombard'||mode==='orb-siege'){
    if(wave<3+n)er26Shot(b,side,a,2.25,{large:true,burst:true});R.shot+=.35;er26Muzzle(b,side);
  }else if(mode==='cinder-scissors'){
    // Alternating shutters. Left and right never seal at once.
    const off=(wave%4)*.09;
    er26Fan(b,side,Math.PI/2+(side==='L'?-.28+off:.28-off),4,.13,speed);
    R.shot+=.12;
  }else if(mode==='charcoal-wheel'||mode==='shatter-wheel'){
    const p=shipBossMount(b,'C'),count=10+n*2,gapAngle=Math.atan2(player.y-p.y,player.x-p.x);
    for(let j=0;j<count;j++){
      const angle=j*TAU/count+wave*.21;
      if(Math.abs(Math.atan2(Math.sin(angle-gapAngle),Math.cos(angle-gapAngle)))<.34)continue;
      er26Shot(b,p,angle,2.6+n*.25,{curve:mode==='charcoal-wheel'?(wave&1?-.12:.12):0});
    }er26Muzzle(b,'C');
  }else if(mode==='cryo-crosscut'){
    er26Fan(b,side,a,3+n,.115,speed+.4);R.shot+=.12;
  }else if(mode==='bastion-gates'||mode==='glacier-press'){
    const count=9+n*2,gap=2+(wave+R.index*2)%(count-4),p=shipBossMount(b,'C');
    for(let j=0;j<count;j++){
      if(Math.abs(j-gap)<=1)continue;
      er26Shot(b,p,Math.PI/2+(j-(count-1)/2)*.13,speed-.45);
    }R.shot+=.24;er26Muzzle(b,'C');
  }
  er26Sound(b._ship==='magmaward'?'enemyFlameBolt':'enemyIceBolt','enemyBossCannon');
}
function er26Palette(key,mode){
  if(!mode||!XART.rdy(key))return null;
  const cache=key+'|er26|'+mode;if(ER26_PALETTES.has(cache))return ER26_PALETTES.get(cache);
  const im=XART.get(key),c=document.createElement('canvas');c.width=im.width||im.naturalWidth;c.height=im.height||im.naturalHeight;
  const x=c.getContext('2d');x.drawImage(im,0,0);const data=x.getImageData(0,0,c.width,c.height),d=data.data;
  for(let i=0;i<d.length;i+=4){
    if(!d[i+3])continue;const r=d[i],g=d[i+1],b=d[i+2],lum=.2126*r+.7152*g+.0722*b;
    if(mode==='charred'||mode==='charred-shot'){
      const hot=r>g*1.45&&r>b*1.7;
      if(mode==='charred-shot'&&lum>178){d[i]=Math.min(255,lum*1.13);d[i+1]=lum*.91;d[i+2]=lum*.88;}
      else if(hot&&lum>65){d[i]=Math.min(250,115+lum*.76);d[i+1]=Math.round(lum*.17);d[i+2]=Math.round(lum*.09);}
      else {const v=lum<24?lum*.65:Math.pow(lum/255,1.05)*(mode==='charred-shot'?144:138);d[i]=v*.90;d[i+1]=v*.95;d[i+2]=v;}
    }else if(mode==='fire'){
      if(lum<26)continue;d[i]=Math.min(255,lum*1.25+24);d[i+1]=lum*.52;d[i+2]=lum*.19;
    }else if(mode==='ice'){
      if(lum<26)continue;d[i]=lum*.58;d[i+1]=Math.min(255,lum*.94+16);d[i+2]=Math.min(255,lum*1.18+22);
    }else {d[i]=lum*.72;d[i+1]=lum*.77;d[i+2]=lum*.84;}
  }
  x.putImageData(data,0,0);ER26_PALETTES.set(cache,c);return c;
}
function er26Hull(b,key){
  const R=b._er26;if(!R)return null;
  if(b._ship==='magmaward'&&R.level===2)return er26Palette(key,'charred');
  if(b._s3Nuclear||R.nuclearRevealed)return er26Palette(key,R.form);
  return null;
}
function er26DamageClamp(b,dmg){
  if(!b||!b._er26)return dmg;
  if(b._noHit)return 0;
  // Preserve the required neutral -> missile -> elemental sequence under burst
  // damage. The missile arrives after two complete attacks, not during entry.
  if(b._er26.neutralOpening)return Math.max(0,Math.min(dmg,b.hp-b.maxhp*.75));
  return dmg;
}
function er26ProjectileDraw(q){
  if(!q._er26Art)return false;
  const frame=Math.floor((q.t||0)*12)%8;
  const key=(q._er26Art==='fire'?'mwfx_fireball_':q._er26Large?'l23fx_rime_orb_':'l23fx_cryo_ball_')+frame;
  if(!XART.rdy(key))return true; // warmed at encounter spawn, never fall through to generic darts
  const im=q._er26Charred?er26Palette(key,'charred-shot'):XART.get(key),s=q._er26Draw||26;
  ctx.save();ctx.translate(Math.round(q.x),Math.round(q.y));ctx.rotate((q.t||0)*2.7);ctx.imageSmoothingEnabled=false;
  ctx.drawImage(im,-s/2,-s/2,s,s);ctx.restore();return true;
}
function er26Draw(b){
  const R=b._er26;if(!R||b.dead||b.enter)return;
  if(R.mode!=='recover'&&R.mode!=='form-change'){
    let alert=null;
    for(const w of R.warnings){
      if(w.progress==null&&R.t>=R.warm)continue;
      const p=typeof w.slot==='string'?shipBossMount(b,w.slot):w;
      const tell={x:p.x,y:p.y,ex:p.x+Math.cos(w.angle)*VH,ey:p.y+Math.sin(w.angle)*VH,
        progress:w.progress==null?clamp(R.t/R.warm,0,1):w.progress,width:w.width};
      combatWarningDraw(b,{...tell,fieldOnly:true});
      if(!alert||tell.progress>alert.progress)alert=tell;
    }
    // One sign per attack, below the Sovereign's separate shield gauge.
    if(alert)combatWarningDraw(b,{...alert,alertOnly:true,alertY:b._s4war&&!b._s4war.mini?82:undefined});
  }
  if(R.mode==='form-change'){
    const key='mwfx_fireball_charge_'+Math.min(7,Math.floor(R.t/1.55*8));
    const im=er26Palette(key,R.formNext||'ice');if(im){const s=60+R.t*48;ctx.save();ctx.globalAlpha=.7;
      ctx.globalCompositeOperation='lighter';ctx.drawImage(im,b.x-s/2,b.y-s/2,s,s);ctx.restore();}
  }
}
function er26Tick(b,dt){
  if(!er26Owns(b))return false;
  er26Init(b);if(typeof mr27Tick==='function')mr27Tick(b,dt);const R=b._er26;
  // Entry owns the hull first. Start combat recovery at the actual arrival position,
  // not the offscreen coordinates saved when its controller was constructed.
  if(!R.engaged){R.engaged=true;if(R.mode==='recover'){R.from={x:b.x,y:b.y};R.t=0;}}
  R.t+=dt;R.clock+=dt;R.phase=b.hp/b.maxhp<=.30?2:b.hp/b.maxhp<=.65?1:0;
  b.fireCd=999;b._sba=null;b._sbaHitT=Math.max(0,(b._sbaHitT||0)-dt);b._sbaKick=0;
  if(b._s4war)return er26WarTick(b,dt);
  er26Seeds(b,dt);
  if(R.mode==='recover'){
    er26Move(b,R,R.t/R.dur);if(R.t>=R.dur){R.passFrom=null;er26Next(b);}return true;
  }
  if(R.mode==='form-change'){
    er26Move(b,R,R.t/R.dur);
    if(R.t>=.75&&!R.formApplied){R.form=R.formNext;b._s3Nuclear.mode=R.form;R.formApplied=true;b.flash=.18;b._hitFlashColor='#ffffff';}
    if(R.t>=R.dur){b._noHit=false;er26Next(b);}return true;
  }
  er26Combat(b,dt);
  if(R.t>=R.dur&&!b._l23Beam)er26Set(b,'recover');
  return true;
}

/* Stage 4: alternating helpers, committed aim and overheat opportunities.
   Existing shield generators / module damage / Retina targets stay authoritative. */
function er26EscortTick(b,dt){
  const R=b._er26,S=b._s4war,list=stage4MiniEscortEnsure(b),L=camLeftX(),W=viewW();
  for(const d of list){
    if(b._mr27)d._mrOwner=b;
    if(d.dead)continue;
    if(!d._erArrival){d._erArrival=true;d.x=L+W*(d.side<0?.16:.84);d.y=-100;d.active=0;d.t=0;d.fireCd=0;}
    d.t+=dt;d.active=clamp(d.t/1.2,0,1);d.flash=Math.max(0,d.flash-dt);
    const x=L+W*(d.side<0?.15:.85),y=Math.min(245,R.home+46);
    d.x+=(x-d.x)*Math.min(1,dt*2.8);d.y+=(y-d.y)*Math.min(1,dt*2.8);
    const allowed=R.mode==='escort-crossfire'&&R.t>=R.warm&&R.t<R.dur;
    const slot=Math.floor(Math.max(0,R.t-R.warm)/2.65)%2;
    const turn=allowed&&slot===d.index&&d.active===1&&!(b._mr27&&mr27HelperState(d).dead);
    const local=(R.t-R.warm)%2.65;
    if(!turn){d._erLock=null;d.ang+=stage4AngleDelta(d.ang,Math.PI/2)*Math.min(1,dt*4);continue;}
    if(!d._erLock){d._erLock={x:player.x,y:player.y};d.fireCd=0;d._erBurst=0;}
    const a=Math.atan2(d._erLock.y-d.y,d._erLock.x-d.x);
    d.ang+=stage4AngleDelta(d.ang,a)*Math.min(1,dt*6);
    if(local<.72){combatWarningTick(d,'er26-escort',local,.72,true);
      R.warnings.push({slot:null,x:d.x,y:d.y,angle:a,width:32,progress:local/.72});continue;}
    d.fireCd-=dt;if(d.fireCd>0||local>2.0)continue;
    const tip={x:d.x+Math.cos(a)*d.size*.43,y:d.y+Math.sin(a)*d.size*.43};let q;
    if(d.role==='gunner'){
      q=stage4MiniMachine(b,tip,a+(d._erBurst%3-1)*.045,4.3+R.level*.5);
      d.fireCd=.115;d._erBurst++;if(d._erBurst%5===0)d.fireCd=.38;
    }else{q=stage4WarfareShot(b,tip,a,2.2,'rocket',{accel:.6,max:4.7,shootable:true,hp:2,szMul:.74});d.fireCd=.56;}
    q._s4EscortRole=d.role;q._er26Source='escort';d.shots++;R.helperShots++;stage4WarfareDroneMuzzle(b,d);
  }
  S.summoned=list.some(d=>!d.dead);
}
function er26CoreTick(b,dt){
  const R=b._er26,S=b._s4war;if(!S.coreUnlocked)return;
  if(S.coreEnrage)stage4CoreEnrageEnd(b);
  stage4CoreFormationTick(b,dt);
  const enabled=R.mode==='escort-crossfire'&&R.t>=R.warm;
  for(const d of S.coreTurrets){
    if(b._mr27)d._mrOwner=b;
    if(d.dead)continue;const p=stage4CoreTurretTarget(b,d.side);
    d.spawnT+=dt;d.materialize=clamp(d.spawnT/.8,0,1);d.flash=Math.max(0,d.flash-dt);
    d.deflectFlash=Math.max(0,d.deflectFlash-dt);d.deflectSfx=Math.max(0,d.deflectSfx-dt);
    d.x+=(p.x-d.x)*Math.min(1,dt*5);d.y+=(p.y-d.y)*Math.min(1,dt*5);
    const side=(Math.floor(Math.max(0,R.t-R.warm)/2.7)&1)?1:-1,owns=enabled&&d.side===side&&!(b._mr27&&mr27HelperState(d).dead);
    const local=(R.t-R.warm)%2.7;
    const state=owns?(local<.8?'windup':local<1.9?'fire':'overheat'):'overheat';
    if(d.state!==state){d.state=state;d.stateT=0;d.fireShot=0;
      if(state==='windup')d._erAim=Math.atan2(player.y-d.y,player.x-d.x);
      if(state==='fire')er26Sound('enemyLightningChaingun','enemyShoot');}
    d.stateT+=dt;d.vulnerable=state==='overheat';S.coreCycleSeen[state]=true;
    d.heat=state==='overheat'?.8:state==='fire'?.48:.15;d.reelSpeed=state==='fire'?38:state==='windup'?22:6;d.spin=(d.spin+dt*d.reelSpeed)%8;
    if(!owns||d.materialize<1)continue;
    const a=clamp(d._erAim||Math.PI/2,Math.PI*.22,Math.PI*.78);
    d.ang+=stage4AngleDelta(d.ang,a)*Math.min(1,dt*5);
    if(state==='windup'){combatWarningTick(d,'er26-core',local,.8,true);R.warnings.push({slot:null,x:d.x,y:d.y,angle:a,width:36,progress:local/.8});}
    if(state!=='fire')continue;
    d.fireShot-=dt;if(d.fireShot>0)continue;d.fireShot=[.12,.095,.075][R.level];
    const sideBarrel=d.barrelNext;d.barrelNext=-d.barrelNext;const tip=stage4CoreTurretTip(d,sideBarrel);
    const q=stage4WarfareShot(b,tip,a,4.9+R.level*.4,'lightningmg',{szMul:1.2});
    q._s4CoreSide=d.side;q._s4CoreBarrel=sideBarrel;q._er26Source='core';
    S.coreShots++;S.coreBarrelShots[sideBarrel]++;R.helperShots++;stage4CoreTurretMuzzle(b,d,sideBarrel);
  }
}
function er26WarShot(b,slot,a,speed,kind,opt){
  if(typeof mr27CanFire==='function'&&!mr27CanFire(b,kind==='rocket'?'ROCKET_'+slot:slot))return {dead:true};
  if(kind==='rocket'&&(slot==='L'||slot==='R'))slot='ROCKET_'+slot;
  if(typeof mr27Fire==='function')mr27Fire(b,slot,a);
  const q=stage4WarfareShot(b,slot,a,speed,kind,opt);q._er26Source=b._ship;b._er26.bodyShots++;
  stage4WarfareMuzzle(b,slot,kind==='rocket'?'rocket':kind==='orb'?'orb':/^lightning/.test(kind)?'lightning':'mg',.85,.14);
  return q;
}
function er26WarTick(b,dt){
  const R=b._er26,S=b._s4war,mini=S.mini,n=R.level;R.warnings=[];S.poseRot=0;S.scale=1;
  if(!mini){
    stage4ShieldTick(b,dt);stage4ShieldSyncNodes(b);
    if(S.shield.rearming){
      b.x+=(er26Station(b,0)-b.x)*Math.min(1,dt*3);b.y+=(R.home-b.y)*Math.min(1,dt*3);b._drawY=b.y;
      b._animKey='s4w_boss_charge_'+Math.min(11,Math.floor(S.shield.rearmT/1.08*12));
      stage4ShieldSyncNodes(b);R.wasRearming=true;return true;
    }
    if(R.wasRearming){R.wasRearming=false;er26Set(b,'recover');}
    er26CoreTick(b,dt);
    // The late twin guns remain visible and aim while cooling. They only fire
    // during core-barrage, never under helper salvos, rams or the nuclear lances.
    if(S.finalGuns!=='off'){
      S.finalGunSpin=(S.finalGunSpin+dt*(R.mode==='core-barrage'?28:5))%8;
      for(const side of [-1,1]){const p=stage4FinalGunMount(b,side),a=Math.atan2(R.target?R.target.y-p.y:VH,R.target?R.target.x-p.x:0),k=side<0?'finalGunAimL':'finalGunAimR';S[k]+=stage4AngleDelta(S[k],a)*Math.min(1,dt*4);}
    }
  }else er26EscortTick(b,dt);
  if(R.mode==='recover'){
    er26Move(b,R,R.t/R.dur);if(R.t>=R.dur)er26Next(b);
  }else{
    const mode=R.mode,t=R.t,live=t-R.warm;
    if(typeof polishEncounterAttack==='function'&&polishEncounterAttack(b,dt)){if(t>=R.dur)er26Set(b,'recover');return true;}
    const drive=mode==='warden-drive'||mode==='siege-drive';
    if(drive){
      if(!R.drive){R.drive={x:clamp(R.target.x,camLeftX()+b.w*.52,camRightX()-b.w*.52),y:Math.min(VH*.65,player.y-82),fromX:b.x,fromY:b.y};R.live=2.2;R.dur=R.warm+R.live;}
      const D=R.drive;
      if(live<0){b.x+=(D.x-b.x)*Math.min(1,dt*4);b.y+=(R.home-b.y)*Math.min(1,dt*4);er26Warning(b,'C',Math.PI/2,b.w*.62);}
      else {if(D.startY==null)D.startY=b.y;const q=clamp(live/R.live,0,1),reach=Math.sin(q*Math.PI);b.x+=(D.x-b.x)*Math.min(1,dt*4);b.y=D.startY+(D.y-D.startY)*reach;}
    }else {b.x+=(er26Station(b,0)-b.x)*Math.min(1,dt*3);b.y+=(R.home-b.y)*Math.min(1,dt*3);}
    b._drawY=b.y;
    if(mode==='escort-crossfire'){
      if(mini&&!S.summoned||!mini&&!S.coreUnlocked){
        // Early/Normal variant: the hull's alternating barrels teach the helper rhythm.
        if(live>=0){R.shot-=dt;if(R.shot<=0){const slot=(Math.floor(live/1.5)&1)?'R':'L';
          er26WarShot(b,slot,R.angles[slot==='L'?0:2],4.1+n*.45,'mg');R.shot=.17;}}
      }
    }else if(t<R.warm){
      if(!drive)for(const slot of ['L','R'])er26Warning(b,slot,R.angles[slot==='L'?0:2],42);
      combatWarningTick(b,'er26-'+R.serial,t,R.warm,true);
    }else if(!drive){
      R.shot-=dt;
      if(R.shot<=0){
        const wave=R.wave++,slot=(wave&1)?'R':'L',a=R.angles[slot==='L'?0:2];R.shot=diffKey==='easy'?.44:[.26,.20,.16][n];
        if(mode==='warden-suppress'||mode==='sovereign-battery'){
          const sweep=(wave%9-4)*.075;
          for(const off of [-.075,.075])er26WarShot(b,slot,Math.PI/2+sweep+off,4.3+n*.4,mini?'mg':'lightningmg');
          R.shot=diffKey==='easy'?.32:[.18,.135,.105][n];if(wave%8===7)R.shot+=.42;
        }else if(mode==='rocket-feint'||mode==='siege-rockets'){
          for(let j=0;j<1+n;j++)er26WarShot(b,slot,a+(j-n/2)*.16+(wave%3-1)*.07,2.0,'rocket',{accel:.75,max:5,shootable:true,hp:2,szMul:.82});R.shot=.48-n*.07;
        }else if(mode==='ion-scissors'){
          const off=wave%2?-.23:.23;
          for(const port of ['L','R'])er26WarShot(b,port,Math.PI/2+(port==='L'?off:-off),4.3+n*.4,'lightning',{szMul:1.5});R.shot=.42-n*.05;
        }else if(mode==='center-break'){
          for(const port of ['CL','CR'])er26WarShot(b,port,R.angles[1]+(wave%5-2)*.055,4.9+n*.4,'mg');
          R.shot=diffKey==='easy'?.28:[.16,.12,.09][n];if(wave%7===6)R.shot+=.38;
        }else if(mode==='core-barrage'&&S.finalGuns==='active'){
          const side=(wave&1)?1:-1,p=stage4FinalGunTip(b,side,stage4FinalGunAngle(b,side));
          if(b._mr27&&!mr27CanFire(b,side<0?'L':'R')){R.shot=.2;return true;}
          const q=stage4WarfareShot(b,p,stage4FinalGunAngle(b,side)+(wave%5-2)*.035,5.3+n*.35,'lightningmg',{szMul:1.12});
          q._er26Source=b._ship;R.bodyShots++;stage4FinalGunMuzzle(b,side,0);R.shot=.12-n*.017;
        }else{
          for(const off of [-.22,0,.22])er26WarShot(b,slot,a+off,4.5+n*.4,mini?'mg':'lightning',{szMul:mini?1:1.25});R.shot=.55-n*.07;
        }
        er26Sound('enemyMachineGunHeavy','enemyBossCannon');
      }
    }
    if(t>=R.dur){R.drive=null;er26Set(b,'recover');}
  }
  if(!mini){stage4ShieldSyncNodes(b);b._animKey='s4w_boss_'+(R.t<R.warm&&R.mode!=='recover'?'charge_':'energized_')+(Math.floor((b.t||0)*10)%12);}
  return true;
}
