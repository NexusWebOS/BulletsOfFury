/* Stage 8 symbiote finale. Authored plates and readable attack/recovery timing live here;
   game.js owns the engine hooks and HP/collision pipeline. */
const VILE24_NAMES=['THE POSSESSED','THE ASCENDANT','THE SEALED MASS','THE VILE EXISTENCE'];
const VILE24_SCALE=[1.06,1.12,.90,1.12];
function vile24Cell(key,cols,rows,frame,x,y,w,h,alpha){
  if(!XART.rdy(key))return false;
  const im=XART.get(key),cw=im.width/cols,ch=im.height/rows;
  if(!cw||!ch)return false;
  const i=Math.max(0,Math.min(cols*rows-1,frame|0));
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=alpha==null?1:alpha;
  ctx.drawImage(im,(i%cols)*cw+2,Math.floor(i/cols)*ch+2,cw-4,ch-4,x,y,w,h);
  ctx.restore();return true;
}
function vile24Plate(key,b,dx,dy,w,h,flip,alpha){
  if(!XART.rdy(key))return false;
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=alpha==null?1:alpha;
  if(flip){ctx.translate(b.x,b.y);ctx.scale(-1,1);ctx.translate(-b.x,-b.y);}
  ctx.drawImage(XART.get(key),b.x+(dx||0)-(w||b.w)/2,b.y+(dy||0)-(h||b.h)/2,w||b.w,h||b.h);
  ctx.restore();return true;
}
function vile24Part(b,name){return b.parts&&b.parts.find(p=>p.rc===name&&!p.destroyed);}
function vile24BuildForm(b,idx){
  const sc=VILE24_SCALE[idx],phaseHp=b._vPhaseHp||Math.ceil(b._vBase/4);
  const modules=idx<2?[
    {c:'left_systems',rect:[4,44,78,250],hp:900,role:'systems'},
    {c:'central_core',rect:[64,12,192,245],hp:2000,role:'core'},
    {c:'right_systems',rect:[178,44,252,250],hp:900,role:'systems'}
  ]:[{c:'central_core',rect:[24,10,232,250],hp:1000,role:'core'}];
  buildModularBoss(b,{mw:256,mh:256,scale:sc,overlay:true,named:true,modules},'vile24',phaseHp);
  b._vForm=idx;b.name=VILE24_NAMES[idx];b._v24={seq:0,pattern:null,shield:Math.ceil(phaseHp*(idx===2?.10:.16)),shieldMax:Math.ceil(phaseHp*(idx===2?.10:.16)),shards:[],muzzles:[],shedCd:0};
  b._annihilation=null;b._vileWall=null;b._vileFan=null;b._vileSolar=null;b._vileMissiles=null;b._brk=null;
  b.flash=.22;shake=Math.max(shake,idx?12:6);
  for(const key of (idx===0?['vile24_form1_body','vile24_form1_rocket_arm']:idx===1?['vile24_form2_body','vile24_form2_cannon_arm','vile24_form2_rocket_arm']:idx===2?Array.from({length:6},(_,i)=>'vile24_ball_'+i):['vile24_alien_final']))XART.rdy(key);
  for(let i=0;i<6;i++)XART.rdy('vile24_ball_'+i);
  if(idx>=1)XART.rdy('vile24_alien_final');
  XART.rdy('vile24_shield_sheet');
}
function vile24EntryTick(b,dt){
  const E=b&&b._symEntry;if(!E)return false;
  E.t=Math.min(E.dur,E.t+dt);b.x=worldWidth()/2;b.y=b.ty;
  const beat=Math.floor(E.t/.68);
  if(beat!==E.beat){E.beat=beat;if(beat===4||beat===6){shake=Math.max(shake,7);if(Audio.SFX&&Audio.SFX.bossPhase)Audio.SFX.bossPhase();}}
  if(E.t>=E.dur){b._symEntry=null;b.enter=false;b.fireCd=1.25;b.flash=.18;return false;}
  return true;
}
function vile24EntryDraw(b){
  const E=b&&b._symEntry;if(!E)return false;
  const p=E.t/E.dur,d=b.w*1.55,portalFrame=p<.22?0:p<.44?1:p<.76?2:3;
  vile24Cell('vile24_portal_sheet',2,2,portalFrame,b.x-d/2,b.y-d*.50,d,d,p<.95?1:1-p);
  const robotFrame=p<.22?0:p<.39?1:p<.54?2:3;
  if(p<.76){vile24Cell('vile24_robot_takeover_sheet',2,2,robotFrame,b.x-b.w*.48,b.y-b.h*.48,b.w*.96,b.h*.96,p<.60?1:Math.max(0,(.76-p)/.16));}
  if(p>.68)vile24Plate('vile24_form1_body',b,0,0,b.w,b.h,false,Math.min(1,(p-.68)/.22));
  return true;
}
function vile24DrawMuzzle(x,y,size){if(boss&&boss._v24)boss._v24.muzzles.push({x,y,size,t:0});}
function vile24Shot(kind,x,y,a,sp,silent){
  const sz=kind==='rocket'?[16,27]:kind==='laser'?[11,25]:[20,20];
  const q=eShootT(x,y,a,sp,'vile24'+kind,{w:sz[0],h:sz[1],silent:!!silent});
  q._boss=true;q._bfam='vile';q._noArsenal=true;q._v24Kind=kind;
  if(kind==='rocket'){q.hp=2;q._shootable=true;}
  return q;
}
function vile24DrawProjectile(q){
  if(!q._v24Kind)return false;
  const cell=q._v24Kind==='rocket'?1:q._v24Kind==='laser'?2:0;
  const w=cell===1?29:cell===2?20:32,h=cell===1?42:cell===2?38:32;
  ctx.save();ctx.translate(q.x,q.y);ctx.rotate(cell===0?0:(Math.atan2(q.vy,q.vx)-Math.PI/2));
  vile24Cell('vile24_weapons_sheet',2,2,cell,-w/2,-h/2,w,h);
  ctx.restore();return true;
}
function vile24ArmPoint(b,side){return {x:b.x+side*b.w*.33,y:b.y+b.h*.27};}
function vile24Attack(b){
  const S=b&&b._v24;if(!S)return;
  if(S.pattern){b.fireCd=.18;return;}
  const form=b._vForm|0,sets=(diffKey==='furious'||diffKey==='insanity')?
    [['laser','rockets','orb','rockets'],['void','laser','rockets','orb'],['ball','void','orb','void'],['void','rockets','laser','orb','void']]:
    diffKey==='hard'?
    [['rockets','laser','orb'],['laser','void','rockets','orb'],['ball','orb','void'],['void','laser','rockets','orb']]:
    [['rockets','orb','laser'],['laser','rockets','void','orb'],['ball','orb','void'],['void','laser','orb','rockets']];
  const type=sets[form][S.seq++%sets[form].length],tell=type==='void'?1.0:type==='laser'?.80:type==='ball'?.75:.70;
  S.pattern={type,t:0,tell,tx:clamp(player.x,42,worldWidth()-42),ty:clamp(player.y,PLAY.y+45,VH-54),released:false,second:false};
  b.fireCd=tell+1.3;
  combatWarningTick(b,'stage8-vile24-'+type,0,tell,true);
  if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.enemyBossCannon))(Audio.SFX.bossWeaponCharge||Audio.SFX.enemyBossCannon)();
}
function vile24Release(b,P){
  const L=vile24Part(b,'left_systems'),R=vile24Part(b,'right_systems');
  const aim=(x,y)=>Math.atan2(P.ty-y,P.tx-x);
  if(P.type==='rockets'){
    const live=[];for(const side of [-1,1]){if(b._vForm<2&&!(side<0?L:R))continue;live.push(side);}
    P.rockets=[];const repeats=(diffKey==='furious'||diffKey==='insanity')?3:diffKey==='hard'?2:1;
    for(let wave=0;wave<repeats;wave++)P.rockets.push(...live);
    P.nextRocket=P.tell;P.second=false;
  }else if(P.type==='laser'){
    const side=b._vForm===1&&L?-1:0,at=side?vile24ArmPoint(b,side):{x:b.x,y:b.y+b.h*.23};
    vile24Shot('laser',at.x,at.y,aim(at.x,at.y),5.2);vile24DrawMuzzle(at.x,at.y,42);
    if(typeof navalFlash==='function')navalFlash(null,at,1,'s8nf_solar_corvette_muzzle',{n:4,hpx:56,life:.16,anchor:.45});
  }else if(P.type==='orb'||P.type==='ball'){
    const n=P.type==='ball'?14:12,base=Math.atan2(P.ty-b.y,P.tx-b.x),gap=base;
    for(let i=0;i<n;i++){const a=i*TAU/n+(b.t||0)*.24,delta=Math.abs(Math.atan2(Math.sin(a-gap),Math.cos(a-gap)));
      if(delta<.30)continue;vile24Shot('orb',b.x,b.y+b.h*.18,a,P.type==='ball'?2.45:2.8,i>0);}
    vile24DrawMuzzle(b.x,b.y+b.h*.18,48);
  }else if(P.type==='void'){
    P.activeUntil=P.tell+1.12;P.beamStart=P.tell+.62;P.beamEnd=P.beamStart+.78;
    vile24Shot('orb',b.x,b.y+b.h*.20,aim(b.x,b.y+b.h*.20),2.6,true);
    vile24DrawMuzzle(b.x,b.y+b.h*.20,52);
  }
  shake=Math.max(shake,P.type==='void'?8:4);
}
function vile24Tick(b,dt){
  const S=b._v24;if(!S)return;
  S.shedCd=Math.max(0,S.shedCd-dt);
  for(const q of S.shards){q.t+=dt;q.x+=q.vx*dt;q.y+=q.vy*dt;}S.shards=S.shards.filter(q=>q.t<.55);
  for(const m of S.muzzles)m.t+=dt;S.muzzles=S.muzzles.filter(m=>m.t<.20);
  if(b._vForm===2&&!b.enter){b.x=worldWidth()/2+Math.sin(b.t*1.52)*Math.min(105,worldWidth()*.23);b.y=b.ty+Math.abs(Math.sin(b.t*1.92))*23;}
  const P=S.pattern;if(!P||b.enter)return;
  P.t+=dt;combatWarningTick(b,'stage8-vile24-'+P.type,Math.min(P.t,P.tell),P.tell);
  /* The higher difficulties actively follow the pilot during the early tell, then commit to a
     fixed target. The last slice of the warning and every projectile keep that shown position. */
  if((diffKey==='hard'||diffKey==='furious'||diffKey==='insanity')&&!P.released&&!P.locked&&!player.dead){
    const fast=diffKey==='furious'||diffKey==='insanity',commit=P.tell*(fast?.70:.60);
    if(P.t<commit){const rate=Math.min(1,dt*(fast?5.8:3.6));
      P.tx=lerp(P.tx,clamp(player.x,42,worldWidth()-42),rate);
      P.ty=lerp(P.ty,clamp(player.y,PLAY.y+45,VH-54),rate);
    }else P.locked=true;
  }
  if(!P.released&&P.t>=P.tell){P.released=true;vile24Release(b,P);}
  if(P.type==='rockets'&&P.released&&P.rockets&&P.rockets.length&&P.t>=P.nextRocket){
    const side=P.rockets.shift(),at=vile24ArmPoint(b,side);
    vile24Shot('rocket',at.x,at.y,Math.atan2(P.ty-at.y,P.tx-at.x),3.55,P.rockets.length>0);
    vile24DrawMuzzle(at.x,at.y,40);P.nextRocket+=(diffKey==='furious'||diffKey==='insanity')?.25:.31;
  }
  if(P.type==='void'&&P.released&&P.t<P.activeUntil&&!player.dead){
    const dx=P.tx-player.x,dy=P.ty-player.y,d=Math.hypot(dx,dy);
    if(d<122&&d>1){const pull=34*(1-d/122)*dt;player.x+=dx/d*pull;player.y+=dy/d*pull;}
    if(d<28&&player.invuln<=0)playerHit('darkVoid');
  }
  if(P.type==='void'&&P.beamStart!=null&&P.t>=P.beamStart+.18&&P.t<P.beamEnd&&!player.dead){
    const height=Math.min(400,P.ty-PLAY.y-8),grown=height*clamp((P.t-P.beamStart)/.23,0,1);
    if(Math.abs(player.x-P.tx)<18+(player._hx||9)&&player.y<P.ty+6&&player.y>P.ty-grown)playerHit('darkVoid');
  }
  const recovery=P.type==='void'?1.55:P.type==='rockets'?.95:.64;
  if(P.t>=P.tell+recovery){S.pattern=null;b.fireCd=Math.max(b.fireCd,.42);}
}
function vile24ShieldHit(b,dmg){
  const S=b._v24;if(!S)return dmg;
  if(S.shedCd<=0){S.shedCd=.06;for(let i=0;i<2;i++)S.shards.push({x:b.x+rnd(-b.w*.45,b.w*.45),y:b.y+rnd(-b.h*.35,b.h*.35),vx:rnd(-46,46),vy:rnd(-22,55),t:0});}
  if(S.shield<=0)return dmg;
  S.shield=Math.max(0,S.shield-dmg);if(S.shield===0){shake=Math.max(shake,10);if(Audio.SFX&&Audio.SFX.shieldBreakCombat)Audio.SFX.shieldBreakCombat();}
  return dmg*.52;
}
function vile24DrawWarning(b,P){
  if(!P)return;
  const k=clamp(P.t/P.tell,0,1),under=!P.released;
  if(P.type==='void'){
    const f=P.released?clamp(4+Math.floor((P.t-P.tell)*10),4,15):Math.floor(k*4);
    vile24Cell('vile24_ground_portal_rise_sheet',4,4,f,P.tx-76,P.ty-54,152,114,P.released?1:.70);
    if(under){ctx.save();ctx.strokeStyle='#ff3939';ctx.lineWidth=2+2*k;ctx.beginPath();ctx.arc(P.tx,P.ty,28+10*(1-k),0,TAU);ctx.stroke();ctx.restore();}
    if(P.beamStart!=null){
      if(P.t>=P.tell+.30&&P.t<P.beamStart){const v=clamp((P.t-(P.tell+.30))/(P.beamStart-P.tell-.30),0,1);combatWarningDraw(b,{x:P.tx,y:P.ty,ex:P.tx,ey:PLAY.y+8,progress:v,width:48,fieldOnly:true});}
      if(P.t>=P.beamStart&&P.t<P.beamEnd){const age=P.t-P.beamStart,height=Math.min(400,P.ty-PLAY.y-8)*clamp(age/.23,0,1),fi=clamp(Math.floor(age/.10),0,7);
        vile24Cell('vile24_ground_portal_beam_sheet',4,2,fi,P.tx-31,P.ty-height,62,height);}
    }
    return;
  }
  if(!under)return;
  if(P.type==='laser'){
    const at=b._vForm===1&&vile24Part(b,'left_systems')?vile24ArmPoint(b,-1):{x:b.x,y:b.y+b.h*.23};
    combatWarningDraw(b,{x:at.x,y:at.y,ex:P.tx,ey:P.ty,progress:k,width:17,fieldOnly:true});
  }else if(P.type==='rockets')for(const side of [-1,1]){
    if(b._vForm<2&&!vile24Part(b,side<0?'left_systems':'right_systems'))continue;
    const at=vile24ArmPoint(b,side);combatWarningDraw(b,{x:at.x,y:at.y,ex:P.tx,ey:P.ty,progress:k,width:16,fieldOnly:true});
  }else if(P.type==='orb'||P.type==='ball'){
    combatWarningDraw(b,{x:b.x,y:b.y,ex:P.tx,ey:P.ty,progress:k,width:16,fieldOnly:true});
  }
}
function vile24DrawBoss(b){
  if(b._symEntry){vile24EntryDraw(b);return;}
  if(b._morphT!=null){const from=b._morphFrom|0,fi=Math.min(5,Math.floor(b._morphT/.55*6));
    vile24Plate('vile24_ball_'+fi,b,0,0,b.w*1.08,b.h*1.08,false,1-b._morphT*.42);return;}
  const S=b._v24;if(!S)return;
  vile24DrawWarning(b,S.pattern);
  const f=b._vForm|0,flash=b.flash>0?Math.min(.32,b.flash*2):0;
  if(f===0){
    vile24Plate('vile24_form1_body',b);
    if(vile24Part(b,'right_systems'))vile24Plate('vile24_form1_rocket_arm',b,Math.sin(b.t*2)*2,0,b.w,b.h);
    if(vile24Part(b,'left_systems'))vile24Plate('vile24_form1_rocket_arm',b,-Math.sin(b.t*2)*2,0,b.w,b.h,true);
  }else if(f===1){
    vile24Plate('vile24_form2_body',b);
    if(vile24Part(b,'left_systems'))vile24Plate('vile24_form2_cannon_arm',b,Math.sin(b.t*2.2)*2,0,b.w,b.h);
    if(vile24Part(b,'right_systems'))vile24Plate('vile24_form2_rocket_arm',b,-Math.sin(b.t*2.2)*2,0,b.w,b.h);
  }else if(f===2){
    const frame=Math.floor((b.t||0)*7)%6,key='vile24_ball_'+frame;
    if(XART.rdy(key))S.ballReady=key;
    vile24Plate(S.ballReady||'vile24_ball_0',b);
  }
  else vile24Plate('vile24_alien_final',b);
  if(flash){ctx.save();ctx.globalCompositeOperation='screen';ctx.globalAlpha=flash;ctx.fillStyle='#fff';ctx.beginPath();ctx.ellipse(b.x,b.y,b.w*.42,b.h*.42,0,0,TAU);ctx.fill();ctx.restore();}
  if(S.shield>0){const ratio=S.shield/S.shieldMax,cell=ratio>.66?0:ratio>.33?1:2;
    vile24Cell('vile24_shield_sheet',2,2,cell,b.x-b.w*.59,b.y-b.h*.59,b.w*1.18,b.h*1.18,.48);
  }
  for(const q of S.shards)vile24Cell('vile24_shield_sheet',2,2,3,q.x-12,q.y-12,24,24,1-q.t/.55);
  for(const m of S.muzzles)vile24Cell('vile24_weapons_sheet',2,2,3,m.x-m.size/2,m.y-m.size/2,m.size,m.size,1-m.t/.20);
}
function vile24StartVoidDeath(){
  player._spin=null;player._voidDeath={t:0,dur:2.4,cx:player.x,cy:player.y,burst:false};player.deathT=2.4;
  if(Audio.SFX&&Audio.SFX.bossPhase)Audio.SFX.bossPhase();
}
function vile24UpdateVoidDeath(dt){
  const D=player._voidDeath;if(!D)return;D.t=Math.min(D.dur,D.t+dt);
  const k=clamp(D.t/D.dur,0,1);if(k<.70){player.x+=(D.cx-player.x)*Math.min(1,dt*3);player.y+=(D.cy-player.y)*Math.min(1,dt*3);}
  if(!D.burst&&k>=.63){D.burst=true;shake=Math.max(shake,17);flashScreen=Math.max(flashScreen,.7);if(Audio.SFX&&Audio.SFX.death)Audio.SFX.death();}
}
function vile24DrawVoidDeath(){
  const D=player._voidDeath;if(!D)return;const f=clamp(Math.floor(D.t/.15),0,15),k=D.t/D.dur;
  /* Composite the selected pilot's live ship; no generic craft exists in the FX sheet. */
  if(f<10){const pk=_pilotKey(),im=spaceAtlasCanvas('ship_base',pk);if(im){
    const size=SPACE_SHIP_SIZE*(1-.72*clamp(k/.63,0,1)),w=size*im.width/im.height;
    ctx.save();ctx.translate(player.x,player.y);ctx.rotate(k*TAU*1.5);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,-w/2,-size/2,w,size);ctx.restore();
  }else if(XART.rdy('ship_'+pk)){const sh=XART.get('ship_'+pk),size=SHIP_DRAW_H*(1-.72*clamp(k/.63,0,1)),w=size*sh.width/sh.height;
    ctx.save();ctx.translate(player.x,player.y);ctx.rotate(k*TAU*1.5);ctx.imageSmoothingEnabled=false;ctx.drawImage(sh,-w/2,-size/2,w,size);ctx.restore();}}
  const d=125*(f<4?.65+f*.12:f>11?1.2-(f-11)*.18:1.18);
  vile24Cell('vile24_void_death_sheet',4,4,f,player.x-d/2,player.y-d*.38,d,d*.76);
}
