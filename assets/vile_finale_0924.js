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
  b._vForm=idx;b.name=VILE24_NAMES[idx];b._v24={seq:0,pattern:null,shield:Math.ceil(phaseHp*(idx===2?.10:.16)),shieldMax:Math.ceil(phaseHp*(idx===2?.10:.16)),shards:[],muzzles:[],foes:[],shedCd:0};
  b._annihilation=null;b._vileWall=null;b._vileFan=null;b._vileSolar=null;b._vileMissiles=null;b._brk=null;
  b.flash=.22;shake=Math.max(shake,idx?12:6);
  for(const key of (idx===0?['vile24_form1_body','vile24_form1_rocket_arm']:idx===1?['vile24_form2_body','vile24_form2_cannon_arm','vile24_form2_rocket_arm']:idx===2?Array.from({length:6},(_,i)=>'vile24_ball_'+i):['vile24_alien_final']))XART.rdy(key);
  for(let i=0;i<6;i++)XART.rdy('vile24_ball_'+i);
  if(idx>=1)XART.rdy('vile24_alien_final');
  XART.rdy('vile24_shield_sheet');
  for(const key of ['vile25_ghost_claw','vile25_ghost_wall_left','vile25_phantom_skull','vile25_void_knight',
                    'vile25_shadow_interceptor','vile25_phantom_ground_portal','vile25_void_knight_slash','vile25_form1_hyper_cannon_arm'])XART.rdy(key);
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
function vile25CannonPoint(b,side){return {x:b.x+side*b.w*.255,y:b.y+b.h*.42};}
/* The last music phase owns several readable subforms. All visible bodies, tells and
   weapons use authored plates; these helpers only move them and test their hit boxes. */
function vile25Special(k){return ['hyperlaser','spinlaser','shadowcall','eclipse','box','phantom','knight','mirror','mirrorball'].includes(k);}
function vile25Hard(){return diffKey==='hard'||diffKey==='furious'||diffKey==='insanity';}
function vile25Fury(){return diffKey==='furious'||diffKey==='insanity';}
function vile25Sprite(key,x,y,w,h,alpha,flip){
  if(!XART.rdy(key))return false;
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=alpha==null?1:alpha;
  if(flip){ctx.translate(x,0);ctx.scale(-1,1);x=0;}
  ctx.drawImage(XART.get(key),x-w/2,y-h/2,w,h);ctx.restore();return true;
}
function vile25Warn(b,k,x,y,ex,ey,progress,width){
  combatWarningDraw(b,{x,y,ex,ey,progress:clamp(progress,0,1),width,fieldOnly:true});
}
function vile25Start(b,P){
  P.duration=P.type==='box'?5.35:P.type==='phantom'?(vile25Fury()?5.8:vile25Hard()?4.8:3.8):
    P.type==='knight'?(vile25Fury()?5.6:vile25Hard()?4.6:3.7):P.type==='mirror'?7.2:
    P.type==='mirrorball'?4.3:P.type==='eclipse'?3.7:P.type==='shadowcall'?2.35:
    P.type==='spinlaser'?(vile25Fury()?4.45:3.65):P.type==='hyperlaser'?(vile25Fury()?4.1:3.65):3.2;
  P.fired={};P.tx=player.x;P.ty=player.y;
  if(P.type==='box'){P.left=0;P.right=0;P.strikeAt=3.85;P.strikeX=player.x;P.strikeY=player.y;}
  if(P.type==='phantom'||P.type==='knight')P.count=P.type==='phantom'?(vile25Fury()?4:vile25Hard()?3:2):(vile25Fury()?4:vile25Hard()?3:2);
  if(P.type==='hyperlaser'||P.type==='spinlaser'){P.legs=vile25Fury()?3:2;P.beam=null;}
  if(P.type==='mirror'){
    P.real=(Math.floor(Math.random()*4)+4)%4;P.realDamage=0;
    const left=camLeftX();
    P.clones=Array.from({length:4},(_,i)=>({x:left+VW*(.18+i*.21),y:PLAY.y+115+(i%2)*48,rage:0,alive:true}));
  }
  combatWarningTick(b,'stage8-vile25-'+P.type,0,.8,true);
}
function vile25FireBeam(b,x,y,tx,ty,span){
  if(!player.dead&&player.invuln<=0&&!(player.roll||player.somer)){
    const dx=tx-x,dy=ty-y,len=Math.max(1,Math.hypot(dx,dy));
    const t=clamp(((player.x-x)*dx+(player.y-y)*dy)/(len*len),0,1);
    if(t*len<span&&Math.hypot(player.x-x-t*dx,player.y-y-t*dy)<19)playerHit('laser');
  }
}
function vile25Eradicate(){
  if(player.dead||player.somer||specialActive('juggernaut'))return;
  player.invuln=0;run.shield=0;playerHit('darkVoid');
}
function vile25FoesTick(b,dt){
  const S=b._v24;if(!S||!S.foes.length)return;
  for(const f of S.foes){
    if(f.hp<=0)continue;
    f.t+=dt;f.x+=Math.sin(f.t*3+f.seed)*dt*33;f.y+=dt*(vile25Fury()?75:55);
    if(f.y>VH+40){f.hp=0;continue;}
    if(f.t>1.15&&!f.shot){f.shot=true;vile24Shot('orb',f.x,f.y,Math.atan2(player.y-f.y,player.x-f.x),2.8,true);}
    for(const q of pBullets){if(q.dead||q.y<f.y-24||q.y>f.y+24||Math.abs(q.x-f.x)>25)continue;
      q.dead=true;f.hp-=Math.max(1,q.dmg||1);if(f.hp<=0){unitDeathFX({x:f.x,y:f.y,w:46,h:46},'jet','red');break;}}
    if(f.hp>0&&!player.dead&&Math.abs(player.x-f.x)<23&&Math.abs(player.y-f.y)<25)playerHit('shadow');
  }
  S.foes=S.foes.filter(f=>f.hp>0);
}
function vile25FoesDraw(b){for(const f of b._v24.foes)vile25Sprite('vile25_shadow_interceptor',f.x,f.y,56,56);}
function vile25Tick(b,P,dt){
  P.t+=dt;const t=P.t,W=worldWidth(),id=P.type;
  combatWarningTick(b,'stage8-vile25-'+id,Math.min(t,.8),.8);
  if(id==='hyperlaser'||id==='spinlaser'){
    const sweep=id==='spinlaser',legTime=.94,age=t-.92;
    const leg=Math.floor(age/legTime),phase=age-leg*legTime;
    if(age>=0&&leg<P.legs){
      const side=leg%2?-1:1,at=vile25CannonPoint(b,side);
      const progress=clamp((phase-.17)/.69,0,1);
      const ex=sweep?W*(leg%2?.88-.76*progress:.12+.76*progress):
        clamp(P.tx+side*W*.12,30,W-30);
      // Each cannon changes hands on a visible charge beat. The beam and its
      // collision turn on together, leaving a short repeatable dodge window.
      if(phase<.17){P.beam=null;P.beamTell={x:at.x,y:at.y,ex:sweep?W*(leg%2?.88:.12):ex,ey:VH,p:phase/.17};}
      else if(phase<.86){P.beamTell=null;P.beam={x:at.x,y:at.y,ex,ey:VH,side};
        vile25FireBeam(b,at.x,at.y,ex,VH,Math.hypot(ex-at.x,VH-at.y));
        if(!P.fired[leg]){P.fired[leg]=true;vile24DrawMuzzle(at.x,at.y,48);
          if(Audio.SFX&&Audio.SFX.enemyBossCannon)Audio.SFX.enemyBossCannon();shake=Math.max(shake,4);}}
      else{P.beam=null;P.beamTell=null;}
    }else{P.beam=null;P.beamTell=null;}
  }else if(id==='shadowcall'){
    if(t>.82&&!P.fired.call){P.fired.call=true;const n=vile25Fury()?4:vile25Hard()?3:2;
      for(let i=0;i<n;i++)b._v24.foes.push({x:W*(i+1)/(n+1),y:b.y+b.h*.25,hp:18,t:0,seed:i*2,shot:false});}
  }else if(id==='eclipse'){
    if(t<1.45&&!player.dead){const dx=b.x-player.x,dy=b.y-player.y,d=Math.hypot(dx,dy);if(d<215&&d>1){player.x+=dx/d*12*dt;player.y+=dy/d*12*dt;}}
    if(t>1.55&&!P.fired.orbs){P.fired.orbs=true;const n=vile25Fury()?12:vile25Hard()?10:8;
      const safe=Math.atan2(player.y-b.y,player.x-b.x);
      for(let i=0;i<n;i++){const a=i*TAU/n;if(Math.abs(Math.atan2(Math.sin(a-safe),Math.cos(a-safe)))<.38)continue;
        vile24Shot('orb',b.x,b.y,a,2.4,i>0);}shake=Math.max(shake,6);}
    if(t>2.25&&!P.fired.laser){P.fired.laser=true;vile24Shot('laser',b.x,b.y+b.h*.20,Math.atan2(P.ty-b.y,P.tx-b.x),4.4);vile24DrawMuzzle(b.x,b.y+b.h*.2,46);}
  }else if(id==='box'){
    const wallW=VW/3,wallH=VH/3,backY=VH-37,left=camLeftX(),right=left+VW;
    P.left=clamp((t-.76)/1.55,0,1);P.right=clamp((t-1.45)/1.5,0,1);
    const lx=left-wallW*.60+P.left*(VW*.30+wallW*.60);
    const rx=right+wallW*.60-P.right*(VW*.30+wallW*.60);
    P.walls={lx,rx,w:wallW,h:wallH,y:VH-wallH*.56};
    if(t>1.2&&t<4.65&&!player.dead){
      const lo=lx+wallW*.35+12,hi=rx-wallW*.35-12;
      if(lo<hi)player.x=clamp(player.x,lo,hi);
      player.y=Math.min(player.y,backY);
      if(player.somer)player.y=Math.max(player.y,VH-wallH+18);
      if(t>2.65&&player.y<VH-wallH-28&&!P.fired.rush){P.fired.rush=true;P.strikeAt=Math.max(t+.42,3.05);}
    }
    if(t>P.strikeAt-.45&&!P.fired.lock){P.fired.lock=true;P.strikeX=player.x;P.strikeY=player.y;}
    if(t>=P.strikeAt&&!P.fired.strike){P.fired.strike=true;shake=Math.max(shake,9);
      if(!player.dead&&Math.hypot(player.x-P.strikeX,player.y-P.strikeY)<72)vile25Eradicate();}
  }else if(id==='phantom'||id==='knight'){
    const interval=id==='phantom'?1.12:1.14,base=.55,cycle=Math.floor(Math.max(0,t-base)/interval),local=t-base-cycle*interval;
    if(t>=base&&cycle<P.count){
      if(P.cycle!==cycle){P.cycle=cycle;P.tx=clamp(player.x,40,W-40);P.ty=clamp(player.y,PLAY.y+92,VH-58);P.emerged=false;P.hit=false;
        if(id==='knight'){P.leapFromX=b.x;P.leapFromY=b.y;}}
      if(local>.58&&!P.emerged){P.emerged=true;shake=Math.max(shake,id==='knight'?8:5);}
      if(local>.63&&local<.92&&!P.hit&&!player.dead){
        const radius=id==='knight'?58:49;
        if(Math.hypot(player.x-P.tx,player.y-P.ty)<radius){P.hit=true;if(id==='phantom')vile25Eradicate();else if(!player.somer)playerHit('blade');}
      }
    }
  }else if(id==='mirror'){
    for(let i=0;i<4;i++){const c=P.clones[i];if(!c.alive||c.rage<=0)continue;
      c.rage=Math.max(0,c.rage-dt);const dx=player.x-c.x,dy=player.y-c.y,d=Math.max(1,Math.hypot(dx,dy));
      c.x+=dx/d*dt*(vile25Fury()?245:185);c.y+=dy/d*dt*(vile25Fury()?245:185);
      if(d<39&&!player.dead)playerHit('shadow');}
  }else if(id==='mirrorball'){
    const r=Math.min(W*.38,170),v=vile25Fury()?4.8:3.9;
    b.x=W/2+Math.sin(t*v)*r;b.y=PLAY.y+165+Math.sin(t*v*1.37)*115;
    const beat=Math.floor(t*3);if(!P.fired[beat]){P.fired[beat]=true;for(let i=0;i<8;i++)vile24Shot('orb',b.x,b.y,i*TAU/8+t,2.9,i>0);shake=Math.max(shake,5);}
    if(!player.dead&&Math.hypot(player.x-b.x,player.y-b.y)<b.w*.31)playerHit('collision');
  }
  if(t>=P.duration){b._v24.pattern=null;b.fireCd=.48;b.x=W/2;b.y=b.ty;}
}
/* The luminous shell catches incoming ordnance while charged. Once it breaks, the
   knight's physical shield still protects its right flank, leaving the left open. */
function vile25ShieldContact(b,q){
  const S=b&&b._v24;if(!S||!q||q.dead||q._enemyReflected||b.enter)return false;
  const pose=vile25KnightPose(b)||b,dx=q.x-pose.x,dy=q.y-pose.y;
  const bubble=S.shield>0&&(dx*dx/(b.w*.58*b.w*.58)+dy*dy/(b.h*.58*b.h*.58)<=1);
  const knight=S.pattern&&S.pattern.type==='knight'&&
    dx>=b.w*.13&&dx<=b.w*.57&&dy>=-b.h*.26&&dy<=b.h*.38;
  return !!(bubble||knight);
}
function vile25ShieldDeflect(b,q){
  if(!vile25ShieldContact(b,q))return false;
  const S=b._v24,pose=vile25KnightPose(b)||b;
  const missile=['gmiss','nukem','missile','retinaMissile','spaceVolley'].includes(q.kind);
  if(S.shield>0){
    S.shield=Math.max(0,S.shield-Math.max(1,q._bossDmg||q.dmg||1));
    if(S.shield===0){shake=Math.max(shake,10);
      if(Audio.SFX&&Audio.SFX.shieldBreakCombat)Audio.SFX.shieldBreakCombat();}
  }
  S.reflections=(S.reflections||0)+1;
  const aimed=S.reflections%3!==0,tx=aimed?player.x:clamp(q.x+(S.reflections%2?-160:160),28,worldWidth()-28);
  const ty=aimed?player.y:VH+24,ang=Math.atan2(ty-q.y,tx-q.x);
  const shot=vile24Shot(missile?'rocket':'laser',q.x,q.y,ang,missile?4.5:5.7,true);
  shot._v25Reflected=true;shot._shootable=missile;shot.hp=missile?1:undefined;
  q.dead=true;b.flash=Math.max(b.flash||0,.11);
  S.shards.push({x:q.x,y:q.y,vx:Math.cos(ang)*55,vy:Math.sin(ang)*55,t:0});
  vile24DrawMuzzle(q.x,q.y,missile?35:25);
  if(Audio.SFX&&(Audio.SFX.projectileRicochet||Audio.SFX.shieldDeflect))
    (Audio.SFX.projectileRicochet||Audio.SFX.shieldDeflect)();
  return true;
}
function vile25KnightPose(b){
  const P=b&&b._v24&&b._v24.pattern;if(!P||P.type!=='knight')return null;
  const local=P.t-.55-Math.floor(Math.max(0,P.t-.55)/1.14)*1.14;
  let x=b.x,y=b.y;
  if(P.cycle!=null&&P.cycle<P.count){
    if(local>=.46&&local<.72){const q=clamp((local-.46)/.26,0,1),e=q*q*(3-2*q);
      x=lerp(P.leapFromX??b.x,P.tx,e);y=lerp(P.leapFromY??b.y,P.ty,e)-Math.sin(q*Math.PI)*34;}
    else if(local>=.72&&local<.98){x=P.tx;y=P.ty;}
    else if(local>=.98){const q=clamp((local-.98)/.16,0,1);x=lerp(P.tx,b.x,q);y=lerp(P.ty,b.y,q);}
  }
  return {x,y};
}
function vile25MirrorActive(b){return !!(b&&b._v24&&b._v24.pattern&&b._v24.pattern.type==='mirror'&&b._v24.pattern.t>=.9&&b._v24.pattern.clones);}
function vile25MirrorHitTest(b,x,y){
  const P=b._v24.pattern;b._vCloneHit=null;
  for(let i=P.clones.length-1;i>=0;i--){const c=P.clones[i];if(c.alive&&Math.hypot(x-c.x,y-c.y)<b.w*.16){
    b._vCloneHit=i;if(i===P.real)b._lastPart=vile24Part(b,'central_core');return true;}}
  return false;
}
function vile25FakeHit(b,i){const P=b._v24&&b._v24.pattern;if(!P||!P.clones[i])return;
  P.clones[i].rage=Math.max(P.clones[i].rage,1.7);P.clones[i].x+=Math.sign(player.x-P.clones[i].x)*4;
  vile24DrawMuzzle(P.clones[i].x,P.clones[i].y,26);
}
function vile25OnDamage(b,dmg){const P=b._v24&&b._v24.pattern;if(!P||P.type!=='mirror'||!(dmg>0))return;
  P.realDamage+=dmg;const threshold=(b._vPhaseHp||b.maxhp||1000)*.075;
  if(P.realDamage<threshold)return;
  for(let i=0;i<P.clones.length;i++)if(i!==P.real){const c=P.clones[i];c.alive=false;explode(c.x,c.y,42,'red','fireball');}
  const B={type:'mirrorball',t:0,tell:.5,tx:player.x,ty:player.y,released:false,second:false};
  b._v24.pattern=B;vile25Start(b,B);shake=Math.max(shake,13);
}
function vile24Attack(b){
  const S=b&&b._v24;if(!S)return;
  if(S.pattern){b.fireCd=.18;return;}
  const form=b._vForm|0,sets=(diffKey==='furious'||diffKey==='insanity')?
    [['laser','hyperlaser','spinlaser','shadowcall','rockets','orb'],['eclipse','laser','rockets','void'],
     ['eclipse','ball','void','orb'],['void','box','phantom','knight','mirror','laser']]:
    diffKey==='hard'?
    [['rockets','hyperlaser','spinlaser','shadowcall','orb'],['laser','eclipse','void','rockets','orb'],
     ['ball','eclipse','orb','void'],['void','box','phantom','knight','mirror','laser']]:
    [['rockets','hyperlaser','shadowcall','spinlaser','orb','laser'],['laser','rockets','eclipse','void','orb'],
     ['ball','orb','eclipse','void'],['void','box','phantom','knight','mirror','laser']];
  const type=sets[form][S.seq++%sets[form].length],tell=type==='void'?1.0:type==='laser'?.80:type==='ball'?.75:.70;
  S.pattern={type,t:0,tell,tx:clamp(player.x,42,worldWidth()-42),ty:clamp(player.y,PLAY.y+45,VH-54),released:false,second:false};
  if(vile25Special(type))vile25Start(b,S.pattern);
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
  vile25FoesTick(b,dt);
  if(b._vForm===2&&!b.enter){b.x=worldWidth()/2+Math.sin(b.t*1.52)*Math.min(105,worldWidth()*.23);b.y=b.ty+Math.abs(Math.sin(b.t*1.92))*23;}
  const P=S.pattern;if(!P||b.enter)return;
  if(vile25Special(P.type)){vile25Tick(b,P,dt);return;}
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
function vile25DrawSubform(b,P){
  const t=P.t,W=worldWidth(),id=P.type,trans=clamp(t/.58,0,1);
  if(id==='box'){
    const wall=P.walls;
    if(wall){vile25Sprite('vile25_ghost_wall_left',wall.lx,wall.y,wall.w,wall.h,.80);
      vile25Sprite('vile25_ghost_wall_left',wall.rx,wall.y,wall.w,wall.h,.80,true);}
    if(P.fired.lock&&!P.fired.strike)vile25Warn(b,'claw',b.x,b.y,P.strikeX,P.strikeY,clamp((t-P.strikeAt+.45)/.45,0,1),95);
    if(P.fired.strike&&t<P.strikeAt+.37)
      vile25Sprite('vile25_ghost_claw',P.strikeX,P.strikeY-34,b.w*1.15,b.h*1.15,1);
    else vile25Sprite('vile25_ghost_claw',b.x,b.y,b.w*1.13,b.h*1.13,trans);
    return true;
  }
  if(id==='phantom'){
    const local=t-.55-Math.floor(Math.max(0,t-.55)/1.12)*1.12;
    if(P.cycle!=null&&P.cycle<P.count){
      vile25Sprite('vile25_phantom_ground_portal',P.tx,P.ty,132,78,local<.58?.6:.95);
      if(local<.58)vile25Warn(b,'phantom',b.x,b.y,P.tx,P.ty,local/.58,102);
      else if(local<.98)vile25Sprite('vile25_phantom_skull',P.tx,P.ty-25,b.w*.92,b.h*.92,1);
    }
    if(t<.55||t>.55+P.count*1.12)vile25Sprite('vile25_phantom_skull',b.x,b.y,b.w,b.h,trans);
    return true;
  }
  if(id==='knight'){
    const local=t-.55-Math.floor(Math.max(0,t-.55)/1.14)*1.14;
    const pose=vile25KnightPose(b);
    if(P.cycle!=null&&P.cycle<P.count){
      if(local<.58)vile25Warn(b,'knight',b.x,b.y,P.tx,P.ty,local/.58,100);
      if(local>.58&&local<.98)vile25Sprite('vile25_void_knight_slash',P.tx,P.ty,155,125,1);
    }
    vile25Sprite('vile25_void_knight',pose.x,pose.y,b.w*1.07,b.h*1.07,trans);return true;
  }
  if(id==='mirror'){
    if(t<.58){vile24Plate('vile24_ball_'+Math.min(5,Math.floor(t/.10)),b);return true;}
    if(t<.90)vile25Sprite('vile25_phantom_ground_portal',b.x,b.y,b.w*1.25,b.h*.7,1);
    for(let i=0;i<4;i++){const c=P.clones[i];if(!c.alive)continue;
      vile25Sprite('vile24_alien_final',c.x,c.y,b.w*.34,b.h*.34,i===P.real?1:.75);
      if(c.rage>0)vile24Cell('vile24_shield_sheet',2,2,1,c.x-b.w*.23,c.y-b.h*.23,b.w*.46,b.h*.46,.78);}
    return true;
  }
  if(id==='mirrorball'){
    vile24Plate('vile24_ball_'+(Math.floor(t*11)%6),b,0,0,b.w*.91,b.h*.91);return true;
  }
  if(id==='eclipse'){
    vile24Plate(b._vForm===1?'vile24_form2_body':'vile24_ball_'+(Math.floor(t*7)%6),b);
    if(t<1.65){vile25Sprite('vile25_phantom_ground_portal',b.x,b.y,b.w*1.28,b.h*.78,.8);
      for(let i=0;i<5;i++){const a=t*2+i*TAU/5;vile24Cell('vile24_weapons_sheet',2,2,0,b.x+Math.cos(a)*b.w*.6-15,b.y+Math.sin(a)*b.h*.48-15,30,30,.85);}}
    return true;
  }
  return false;
}
function vile25DrawWeaponTell(b,P){
  if(P.type!=='hyperlaser'&&P.type!=='spinlaser')return;
  if(P.t<.92){for(const s of [-1,1]){const at=vile25CannonPoint(b,s);
    vile25Warn(b,P.type,at.x,at.y,P.type==='spinlaser'?worldWidth()*(s<0?.15:.85):P.tx+s*worldWidth()*.12,VH,Math.min(1,P.t/.92),34);
    vile24Cell('vile24_weapons_sheet',2,2,3,at.x-21,at.y-21,42,42,Math.min(1,P.t/.92));}}
  if(P.beamTell){const Q=P.beamTell;vile25Warn(b,'cannon-followup',Q.x,Q.y,Q.ex,Q.ey,Q.p,35);}
  if(P.beam){const Q=P.beam,ang=Math.atan2(Q.ey-Q.y,Q.ex-Q.x)-Math.PI/2,len=Math.hypot(Q.ex-Q.x,Q.ey-Q.y);
    ctx.save();ctx.translate(Q.x,Q.y);ctx.rotate(ang);
    vile24Cell('vile24_weapons_sheet',2,2,2,-36,0,72,len);
    vile24Cell('vile24_weapons_sheet',2,2,3,-23,-23,46,46);ctx.restore();}
}
function vile24DrawBoss(b){
  if(b._symEntry){vile24EntryDraw(b);return;}
  if(b._morphT!=null){const from=b._morphFrom|0,fi=Math.min(5,Math.floor(b._morphT/.55*6));
    vile24Plate('vile24_ball_'+fi,b,0,0,b.w*1.08,b.h*1.08,false,1-b._morphT*.42);return;}
  const S=b._v24;if(!S)return;
  vile24DrawWarning(b,S.pattern);
  const f=b._vForm|0,flash=b.flash>0?Math.min(.32,b.flash*2):0;
  const sub=S.pattern&&vile25DrawSubform(b,S.pattern);
  if(!sub&&f===0){
    vile24Plate('vile24_form1_body',b);
    const cannon=S.pattern&&['hyperlaser','spinlaser'].includes(S.pattern.type);
    const arm=cannon?'vile25_form1_hyper_cannon_arm':'vile24_form1_rocket_arm';
    if(vile24Part(b,'right_systems'))vile24Plate(arm,b,Math.sin(b.t*2)*2,0,b.w,b.h);
    if(vile24Part(b,'left_systems'))vile24Plate(arm,b,-Math.sin(b.t*2)*2,0,b.w,b.h,true);
  }else if(!sub&&f===1){
    vile24Plate('vile24_form2_body',b);
    if(vile24Part(b,'left_systems'))vile24Plate('vile24_form2_cannon_arm',b,Math.sin(b.t*2.2)*2,0,b.w,b.h);
    if(vile24Part(b,'right_systems'))vile24Plate('vile24_form2_rocket_arm',b,-Math.sin(b.t*2.2)*2,0,b.w,b.h);
  }else if(!sub&&f===2){
    const frame=Math.floor((b.t||0)*7)%6,key='vile24_ball_'+frame;
    if(XART.rdy(key))S.ballReady=key;
    vile24Plate(S.ballReady||'vile24_ball_0',b);
  }
  else if(!sub)vile24Plate('vile24_alien_final',b);
  if(S.pattern)vile25DrawWeaponTell(b,S.pattern);
  vile25FoesDraw(b);
  const fxPose=vile25KnightPose(b)||b;
  if(flash){ctx.save();ctx.globalCompositeOperation='screen';ctx.globalAlpha=flash;ctx.fillStyle='#fff';ctx.beginPath();ctx.ellipse(fxPose.x,fxPose.y,b.w*.42,b.h*.42,0,0,TAU);ctx.fill();ctx.restore();}
  if(S.shield>0){const ratio=S.shield/S.shieldMax,cell=ratio>.66?0:ratio>.33?1:2;
    vile24Cell('vile24_shield_sheet',2,2,cell,fxPose.x-b.w*.59,fxPose.y-b.h*.59,b.w*1.18,b.h*1.18,.48);
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
