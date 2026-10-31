/* Large authored infantry. Movement and aiming remain independent; pose banks
 * contain real drawings for eight facings, never rotated standing billboards. */
(function(root){
  'use strict';
  const TD=root.TD,M=TD.M,W=TD.World,I=TD.Input,A=TD.Audio,FX=TD.FX,PACK=root.TD_ASSAULT_ART;
  const DIR=['south','southwest','west','northwest','north','northeast','east','southeast'];
  const direction=a=>DIR[(Math.round(a/(Math.PI/4))%8+8)%8];
  const wrap=v=>(v%1+1)%1;
  function facing(p,a){
    const prev=p.motionFacing;
    if(prev!=null){const delta=Math.atan2(Math.sin(a-prev*Math.PI/4),Math.cos(a-prev*Math.PI/4));if(Math.abs(delta)<Math.PI/8+.065)return prev;}
    return (Math.round(a/(Math.PI/4))%8+8)%8;
  }
  TD.AssaultArt={
    draw(ctx,key,x,y,o){const m=PACK.assets[key];if(m)ART.draw(ctx,key,x,y,Object.assign({ax:m.anchor[0],ay:m.anchor[1]},o));},
    frame(bank,t,loop=true){const q=PACK.sequences[bank];if(!q)return null;const n=Math.floor(t*q.fps);return q.frames[loop?n%q.frames.length:Math.min(n,q.frames.length-1)];},
    direction,
  };
  const art=TD.AssaultArt;
  const oldShot=TD.drawShot;
  TD.projectileLift=s=>s.liftStart!=null?M.lerp(s.liftStart,s.liftEnd,M.clamp(Math.hypot(s.x-s.spawnX,s.y-s.spawnY)/Math.max(1,s.flightDist),0,1)):(s.drawLift||0);
  TD.drawShot=function(ctx,s,enemy){const lift=TD.projectileLift(s);if(lift){ctx.save();ctx.translate(0,-lift);oldShot(ctx,s,enemy);ctx.restore();}else oldShot(ctx,s,enemy);};
  TD.footLift=p=>p.blindfire?43:p.stance==='prone'&&!p.peekExposed?15:p.stance==='crouch'&&!p.peekExposed?28:45;
  TD.FOOT_GUNS.assault_rifle={name:'ASSAULT RIFLE',cap:Infinity,reserve:0,cd:7,damage:2,k:'vulcan',speed:10};
  const oldMake=TD.makeFootPlayer,oldPose=TD.footPose,oldDraw=TD.drawFoot,oldSocket=TD.footSocket,oldPickupDraw=TD.drawFootPickup,oldHurt=TD.hurtPlayer;
  const rifle=()=>({id:'assault_rifle',lv:1,ammo:Infinity,reserve:0});
  if(!TD.FOOT_EXTRA.includes('repair'))TD.FOOT_EXTRA.push('repair');
  TD.makeFootPlayer=(x,y)=>Object.assign(oldMake(x,y),{hp:3,max:3,r:10,modernFoot:true,weapons:[rifle()],wi:0,stance:'stand',jump:0,roll:0,rollCd:0,rollProne:false,stamina:1,cover:null,peek:0,peekExposed:false,prone:false,poseT:0,walkT:0,gaitPhase:0,gaitSettle:0,motionFacing:null});
  TD.hurtPlayer=function(G,dmg,x,y,source){
    const p=G.player;if(!p.modernFoot)return oldHurt(G,dmg,x,y);
    if(source&&p.prone&&!p.peekExposed&&!source.hitsProne)return;
    if(p.dead||p.inv>0||G.state!=='play'||p.jump>.16&&p.jump<.52||p.roll>.08&&p.roll<.42)return;
    p.hp-=Math.max(1,dmg*(TD.DIFFICULTIES?.[TD.difficulty||'normal']?.damage||1));p.inv=65;p.flash=.18;TD.Cam.kick(4);A.play('hit');
    if(p.hp<=0){p.deathAim=p.aim;p.deathFrom={x:p.x,y:p.y};G.playerDied();}
  };
  function nearestCover(p,G){
    let best=null,dist=30;
    for(const s of G.structures)if(s.assault&&!s.dead&&s.cover){const r=s.rect,d=Math.hypot(p.x-M.clamp(p.x,r.x0,r.x1),p.y-M.clamp(p.y,r.y0,r.y1));if(d<dist){dist=d;best=s;}}
    return best;
  }
  // The peek socket exits only the player's own cover. Every other wall and
  // destructible object still participates in the ordinary swept shot query.
  TD.footAimOrigin=function(p){
    if(p.cover&&!p.cover.dead&&(p.peekExposed||p.blindfire)){
      const q=p.cover.rect,f=M.fwd(p.aim),x=p.x,y=p.y,steps=Math.max(q.x1-q.x0,q.y1-q.y0)+45;
      let entered=false;
      for(let d=1;d<steps;d+=2){const px=x+f[0]*d,py=y+f[1]*d,inside=px>=q.x0-5&&px<=q.x1+5&&py>=q.y0-5&&py<=q.y1+5;
        if(inside)entered=true;else if(entered)return{x:px,y:py};}
    }
    const f=M.fwd(p.aim);return{x:p.x+f[0]*20,y:p.y+f[1]*20};
  };
  // Ground collision starts outside our cover; the visual height is measured
  // from the very pose drawn, so shot and flash share the same barrel pixel.
  TD.footVisualSocket=function(p){const pose=TD.footPose(p),m=PACK.assets[pose.key];if(m?.muzzle){const x=(m.muzzle[0]-m.anchor[0])*pose.scale,y=(m.muzzle[1]-m.anchor[1])*pose.scale,c=Math.cos(pose.angle||0),s=Math.sin(pose.angle||0);return{x:p.x+x*c-y*s,y:p.y-(p.jumpZ||0)+x*s+y*c};}const q=TD.footAimOrigin(p);return{x:q.x,y:q.y-TD.footLift(p)};};
  TD.footSocket=function(p){if(!p.modernFoot)return oldSocket(p);const visual=TD.footVisualSocket(p),ground=TD.footAimOrigin(p);return{x:visual.x,y:ground.y,drawLift:ground.y-visual.y,key:TD.footPose(p).key};};
  TD.footSightOrigin=function(p,target){
    const aim=M.angTo(p.x,p.y,target.x,target.y);
    return TD.footAimOrigin({...p,aim,peekExposed:true});
  };
  TD.footBriefKeys=()=>I.padStyle()==='standard'?[['a','FIRE / PEEK'],['b','JUMP'],['x','ROLL'],['y','GRENADE'],['dpad','MOVE'],['start','PAUSE']]:[['x','FIRE NORTH'],['y','FIRE WEST'],['z','GRENADE'],['a','FIRE SOUTH'],['b','FIRE EAST'],['c','ROLL']];
  function fire(p,G){
    let w=p.weapons[p.wi],d=TD.FOOT_GUNS[w.id];
    if(!d||w.ammo<=0){p.weapons=p.weapons.filter(q=>q.id==='assault_rifle'||q.ammo>0);p.wi=0;w=p.weapons[0];d=TD.FOOT_GUNS[w.id];}
    if(TD.Combat39&&(p.fireAge39??99)>=TD.Combat39.fireDuration(p))p.fireAge39=0;
    p.firing=.13;p.shotAge=0;const socket=TD.footSocket(p);
    if(p.blindfire){const pose=TD.footPose(p),meta=PACK.assets[pose.key];if(meta?.muzzle){socket.x=p.x+(meta.muzzle[0]-meta.anchor[0])*pose.scale;socket.drawLift=socket.y-(p.y+(meta.muzzle[1]-meta.anchor[1])*pose.scale);}}
    if(!p.peekExposed&&!p.blindfire&&W.rayBlock(p.x,p.y,socket.x,socket.y)){p.fireCd=8;A.play('blocked',.3);return;}
    const target=p.retina?.locked&&p.retina.target?.valid()?p.retina.target.point():null;
    const pointer=I.pointer,point=pointer.active&&!p.blindfire?{x:pointer.x/TD.Cam.zoom+TD.Cam.x,y:pointer.y/TD.Cam.zoom+TD.Cam.y}:null;
    const aim=target?M.angTo(socket.x,socket.y,target.x,target.y):point?M.angTo(socket.x,socket.y-(socket.drawLift??TD.footLift(p)),point.x,point.y):p.aim;
    const lv=w.lv||1,lift=socket.drawLift??TD.footLift(p);p.fireCd=Math.max(3,d.cd-(lv-1));p.firing=.13;
    const blindSpread=p.blindfire?Math.sin(p.footTime*37)*.14:0;
    for(const delta of d.fan||[0]){const a=aim+delta+blindSpread,f=M.fwd(a);G.shots.push({k:d.k,x:socket.x,y:socket.y,a,vx:f[0]*d.speed,vy:f[1]*d.speed,dmg:d.damage*(1+(lv-1)*.35),life:d.life||65,r:d.radius||3,weapon39:w.id,pierce:d.pierce||0,splash:d.splash,sdmg:5,lv:1,t:0,drawLift:lift,homing:w.id==='rocket_launcher',napalm:w.id==='napalm_launcher',blindfire:p.blindfire});}
    if(w.id!=='assault_rifle'&&--w.ammo<=0){p.weapons.splice(p.wi,1);p.wi=0;G.say('ASSAULT RIFLE - UNLIMITED',p);}
    FX.attachedFlash(p,TD.footVisualSocket,aim,.10);A.play(d.cue||(d.k==='laser'?'laser':d.k==='homing'?'missileLaunch':'gd_soldierRifle'),.55);
    TD.Stealth.noise(p.x,p.y,200,.6,G.units);
  }
  TD.footTick=function(p,G,dt){
    if(!p.modernFoot||p.dead||p.scripted)return;
    p.rollCd=Math.max(0,(p.rollCd||0)-dt);const rollWas=p.roll;
    if(I.tap('prone')&&p.roll>0)p.rollProne=!p.rollProne;
    p.footTime+=dt;p.poseT+=dt;p.shotAge=(p.shotAge||0)+dt;if(p.stanceTransition)p.stanceTransition.t+=dt;p.inv=Math.max(0,p.inv-1);p.flash=Math.max(0,p.flash-dt);p.fireCd=Math.max(0,p.fireCd-1);p.firing=Math.max(0,(p.firing||0)-dt);p.stamina=Math.min(1,p.stamina+dt*.6);
    const [dx,dy]=I.dir(),len=Math.hypot(dx,dy)||1,aim=I.aim({x:p.x,y:p.y-TD.footLift(p)});
    TD.Retina.tick(p,G,dt);
    if(p.retina?.locked){const q=p.retina.target.point();p.aim=M.angTo(p.x,p.y,q.x,q.y);}
    else if(aim!=null){p.aim=aim;p.manualAim=90;}
    else if(I.down('aimLeft')||I.down('aimRight')){p.aim+=(I.down('aimRight')?1:-1)*.09;p.manualAim=90;}
    else if(p.manualAim>0)p.manualAim--;else if(dx||dy)p.aim=M.angTo(0,0,dx,dy);
    if(dx||dy)p.a=M.angTo(0,0,dx,dy);
    if(I.tap('prone')&&p.jump<=0&&p.roll<=0){p.prone=!p.prone;p.poseT=0;p.stanceTransition={from:p.stance,to:p.prone?'prone':'stand',t:0};A.play('gd_coverEnter',.5);}
    if((I.tap('jump')||I.tap('reload')||I.tap('B')&&!I.state.directionalFire)&&p.jump<=0&&p.roll<=0&&p.stamina>=.35){p.jump=.65;p.stamina-=.35;p.prone=false;p.poseT=0;A.play('stylishDodge',.4);}
    if(I.tap('X')&&p.jump<=0&&p.roll<=0&&p.rollCd<=0){p.rollFromProne39=!!p.prone;p.rollProne=p.prone||I.down('prone')||I.down('cover');p.prone=false;p.rollCd=5;p.roll=.5;p.rollAim=(dx||dy)?p.a:p.aim;p.stamina-=.45;p.poseT=0;A.play('stylishDodge',.5);}
    const low=I.down('C')||I.down('cover')||p.prone;
    const oldCover=p.cover;
    p.cover=low&&p.jump<=0&&p.roll<=0?nearestCover(p,G):null;
    if(p.cover!==oldCover){p.peek=0;p.coverT=0;}p.coverAnchor=null;
    const wasBlind=p.blindfire;p.blindfire=!!p.cover&&I.down('A')&&I.down('retina');if(p.blindfire&&!wasBlind)p.coverT=0;
    const expose=!!p.cover&&I.down('A')&&!p.blindfire;
    p.peek=M.clamp((p.peek||0)+(expose?dt:-dt*1.5),0,.24);
    p.coverT=(p.coverT||0)+dt;p.peekExposed=!!p.cover&&p.peek>=.24&&!p.blindfire;
    const stance=p.prone?'prone':low?'crouch':'stand';if(stance!==p.stance){p.stance=stance;p.poseT=0;}
    const speed=p.roll>0?5.2:p.stance==='prone'?1.05:p.stance==='crouch'?1.55:2.75;
    const v=p.roll>0?M.fwd(p.rollAim):[dx/len,dy/len];p.vx=v[0]*speed;p.vy=v[1]*speed;
    const wasMoving=p.moving,fromX=p.x,fromY=p.y;
    p.x+=p.vx;p.y+=p.vy;for(let pass=0;pass<3;pass++){W.collide(p,p.r,false);for(const q of G.props)if(!q.dead)TD.pushOut(p,q);}
    const distance=Math.min(speed,Math.hypot(p.x-fromX,p.y-fromY));
    p.moving=!!(dx||dy||p.roll>0)&&distance>.025;
    // Advance a complete gait by ground distance, with a shorter crawl stride.
    // Firing and facing changes share this phase. Airborne/roll motion and a
    // blocked wall cannot advance the walking feet underneath another pose.
    if(p.moving&&p.jump<=0&&p.roll<=0&&!p.action){
      const stride=p.stance==='prone'?48:p.stance==='crouch'?60:96;
      const f=M.fwd(p.aim),back=(p.x-fromX)*f[0]+(p.y-fromY)*f[1]<-distance*.55;
      p.gaitPhase=wrap((p.gaitPhase||0)+distance/stride*(back?-1:1));
      p.walkT+=distance/165;p.gaitSettle=0;
    }else if(!p.moving&&!p.jump&&!p.roll){
      if(wasMoving){p.gaitRest=Math.round((p.gaitPhase||0)*2)/2;p.gaitSettle=.08;}
      if(p.gaitSettle>0){const delta=wrap(p.gaitRest-p.gaitPhase+.5)-.5;p.gaitPhase=wrap(p.gaitPhase+delta*Math.min(1,dt/p.gaitSettle));p.gaitSettle=Math.max(0,p.gaitSettle-dt);}
    }
    p.motionFacing=facing(p,p.roll>0?p.rollAim:p.aim);
    p.hidden=!!W.inType(p.x,p.y,'h')||!!W.inType(p.x,p.y,'d')||!!p.cover&&!p.peekExposed;
    if(I.tap('tapWall')){const f=M.fwd(p.aim),x=p.x+f[0]*20,y=p.y+f[1]*20;if(W.solidAt(x,y)){TD.Stealth.noise(x,y,180,.25,G.units);G.say('TAP',p);A.play('blip',.2);}}
    if(I.tap('Y')&&p.smoke>0&&p.roll<=0&&!p.action)p.action={kind:'grenade',t:0,aim:p.aim,committed:false};
    if(p.action){p.action.t+=dt;if(!p.action.committed&&p.action.t>=.375){p.action.committed=true;p.smoke--;const f=M.fwd(p.action.aim);G.footGrenades.push({x:p.x,y:p.y,tx:p.x+f[0]*125,ty:p.y+f[1]*125,t:0,done:false});A.play('bombDrop',.5);}if(p.action.t>=.6)p.action=null;}
    const blindFrame=Math.floor((p.coverT||0)*14)%8,blindReady=!p.blindfire||blindFrame>=2&&blindFrame<=4;
    if(I.down('A')&&p.fireCd<=0&&p.roll<=0&&!p.action&&blindReady&&(!p.cover||p.peekExposed||p.blindfire))fire(p,G);
    p.roll=Math.max(0,p.roll-dt);if(rollWas>0&&p.roll<=0){p.prone=!!p.rollProne;p.stance=p.prone?'prone':'stand';p.stanceTransition=null;p.poseT=0;}p.jump=Math.max(0,p.jump-dt);p.jumpZ=p.jump>0?Math.sin((.65-p.jump)/.65*Math.PI)*28:0;
  };
  TD.footPose=function(p){
    if(p.pilot!=='yuri')return oldPose(p);
    if(p.stanceTransition?.t<.46&&!p.cover&&!p.roll&&!p.jump){const dir=direction(p.aim),d=dir,bank='pb19_yuri_'+d+'_prone_transition',q=PACK.sequences[bank];if(q){let n=Math.min(q.frames.length-1,Math.floor(p.stanceTransition.t/.46*q.frames.length));if(p.stanceTransition.to==='stand')n=q.frames.length-1-n;return{key:q.frames[n],scale:1,angle:0,action:'prone_transition',dir:d};}}
    if(p.dead)return{key:art.frame(PACK.sequences.yuri_north_knockback?'yuri_north_knockback':'yuri_death',p.deadT||0,false),angle:0,scale:1,action:'death',dir:'north'};
    if(p.action){const dir=direction(p.action.aim),bank='yuri_'+dir+'_grenade',k=art.frame(bank,p.action.t,false)||art.frame('yuri_'+dir+'_walk',0);return{key:k,angle:0,scale:PACK.assets[k]?.drawScale??.42,action:'grenade',dir};}
    const dir=DIR[facing(p,p.roll>0?p.rollAim:p.aim)];let action=p.moving?(p.firing>0?'run_fire':'walk'):(p.firing>0?'fire':'idle'),t=p.moving?p.walkT:p.firing>0?(p.shotAge||0):p.footTime,loop=true;
    if(p.stance==='crouch'){action='crouch';t=Math.min(.5,p.poseT);loop=false;}
    if(p.stance==='prone'){action=p.moving?'crawl':'prone_fire';t=p.moving?p.walkT:p.firing>0?p.footTime:.1;}
    if(p.cover&&p.peek>0){action='peek';t=p.peek/.24*.5;loop=false;}
    if(p.cover&&p.peekExposed&&!p.blindfire){action=p.firing>0?'fire':'idle';t=p.shotAge||0;loop=true;}
    if(p.cover&&p.blindfire){action='blindfire';t=p.coverT;}
    if(p.jump>0){action='jump';t=(.65-p.jump)/.65*.6;loop=false;}
    if(p.roll>0){action='roll';t=(.5-p.roll)/.5*.6;loop=false;}
    // New motion banks use the same cycle phase even when frame counts differ.
    // Idle/prone hold the planted frame instead of changing body banks.
    const travel=M.fwd(p.a),look=M.fwd(p.aim),lateral=Math.abs(travel[0]*look[1]-travel[1]*look[0])>.72;
    if(p.moving&&p.stance==='stand'&&p.roll<=0&&p.jump<=0&&lateral&&dir==='north'&&PACK.sequences.yuri_north_sidestep)action='sidestep';
    const coverNorth=action==='blindfire'||action==='peek'&&PACK.sequences.yuri_north_peek;
    let bank='yuri_'+(coverNorth?'north':dir)+'_'+action;
    if(!PACK.sequences[bank])bank='yuri_'+(coverNorth?'north':dir)+'_'+(action==='prone_fire'?'crawl':action==='fire'?'run_fire':action==='idle'?'walk':action);
    const seq=PACK.sequences[bank];
    if(seq?.motion){let phase=p.gaitPhase??wrap(p.walkT*165/(seq.stride||96));if(action==='sidestep'&&p.vx<0)phase=wrap(-phase);const index=Math.floor(wrap(phase)*seq.frames.length+1e-8)%seq.frames.length;return{key:seq.frames[index],angle:0,scale:PACK.assets[seq.frames[index]]?.drawScale??.42,action,dir,phase,index};}
    const k=art.frame(bank,t,loop);return{key:k,angle:0,scale:PACK.assets[k]?.drawScale??.42,action,dir};
  };
  TD.drawFoot=function(ctx,p,o){
    if(p.pilot!=='yuri')return oldDraw(ctx,p,o);
    const pose=TD.footPose(p),z=p.jumpZ||0;
    art.draw(ctx,pose.key,p.x+3,p.y+3,{s:pose.scale,tint:'#000000',alpha:.3});
    art.draw(ctx,pose.key,p.x,p.y-z,{s:pose.scale,flash:o?.flash||0,alpha:p.dead?.65:1});
  };
  TD.footPickups=function(G,dt){
    const p=G.player;
    for(const k of G.pickups){k.t+=dt;if(p.dead||M.dist(k.x,k.y,p.x,p.y)>28)continue;k.dead=true;const d=TD.FOOT_GUNS[k.kind];
      if(d&&k.kind!=='assault_rifle'){let w=p.weapons.find(w=>w.id===k.kind)||{id:k.kind,lv:1,ammo:0,reserve:0};w.ammo+=d.cap+d.reserve;p.weapons=[rifle(),w];p.wi=1;G.say(d.name,p);A.play('weaponFound');}
      else if(k.kind==='grenades'){p.smoke=Math.min(9,p.smoke+3);G.say('GRENADES +3',p);}
      else if(k.kind==='life'){G.lives++;A.play('extraLife');}
      else if(k.kind==='repair'){p.hp=Math.min(p.max,p.hp+1);G.say('ARMOR +1',p);}
      else if(k.kind==='pow'){const w=p.weapons[p.wi];w.lv=Math.min(3,(w.lv||1)+1);G.say('FIREPOWER UP',p);}
      else if(k.kind==='crash'){G.crash=Math.min(5,(G.crash||0)+1);}
      else if(k.kind==='score'){G.score+=1000;}
      else{for(const w of p.weapons)if(w.id!=='assault_rifle')w.ammo+=TD.FOOT_GUNS[w.id].cap;G.score+=100;G.say('SUPPLY RECOVERED',p);}
      A.play('gd_ammoPickup',.4);
    }G.pickups=G.pickups.filter(k=>!k.dead);
  };
  TD.drawFootPickup=function(ctx,k){if(k.kind==='ammo'||k.kind==='repair'){ART.draw(ctx,'of_desert_eagle_ammo',k.x,k.y,{s:.3});return;}oldPickupDraw(ctx,k);};
  TD.infantryHUD=function(ctx,text,G){
    const p=G.player;if(!p.onfoot)return false;const w=p.weapons[p.wi],d=TD.FOOT_GUNS[w.id];
    ctx.fillStyle='rgba(3,10,18,.83)';ctx.fillRect(8,7,TD.VW-16,48);
    ART.draw(ctx,'pav_'+p.pilot,31,31,{s:.12});text(d.name,57,23,12,'#ffcf72');text(w.id==='assault_rifle'?'UNLIMITED':String(w.ammo)+' ROUNDS',57,42,10,'#c8f7ff');
    text('ARMOR '+Math.max(0,Math.ceil(p.hp))+'/'+p.max,TD.VW-15,21,11,'#7dffa0','right');text('GRENADES '+p.smoke+'  LIVES '+G.lives,TD.VW-15,42,9,'#fff','right');
    const label=p.cover?(p.blindfire?'BLINDFIRE / PROTECTED':p.peekExposed?'EXPOSED - FIRING':'IN COVER'):p.jump>0?'JUMP':p.roll>0?'ROLL':p.stance.toUpperCase();text(label,12,TD.VH-16,10,p.peekExposed?'#ffa763':'#8ceaff');
    if(p.retina?.phase)text('RETINA '+(p.retina.locked?'LOCKED':'SEEKING'),TD.VW-12,TD.VH-16,10,'#ffd566','right');
    else if(p.cover)text(I.padId?(I.padStyle()==='standard'?'L + R + FIRE: BLINDFIRE':'MODE + Z: BLINDFIRE'):(I.keyLabel('retina')+' + FIRE: BLINDFIRE'),TD.VW-12,TD.VH-16,9,'#c8f7ff','right');
    if(!p.cover&&!p.retina?.phase)text(I.padId?(I.padStyle()==='six'?'MODE + X: PRONE / D-PAD: CRAWL':'MODE + X: PRONE / D-PAD: CRAWL'):(I.keyLabel('prone')+': PRONE / WASD: CRAWL'),TD.VW-12,TD.VH-16,9,'#c8f7ff','right');
    if(G.boss?.alive()){const b=G.boss,w=Math.min(240,TD.VW*.38),x=(TD.VW-w)/2,y=34,fill=b.state==='enter'?b.gauge:b.hpFrac();ctx.fillStyle='rgba(3,10,18,.9)';ctx.fillRect(x-5,y-24,w+10,43);text(b.name+' / 40 WATT EXECUTIONER',TD.VW/2,y-8,11,'#ffd060','center');ctx.fillStyle='#17202c';ctx.fillRect(x,y,w,12);ctx.fillStyle='#ffba54';ctx.fillRect(x+1,y+1,(w-2)*M.clamp(fill,0,1),3);ctx.fillStyle='#e63b42';ctx.fillRect(x+1,y+4,(w-2)*M.clamp(fill,0,1),7);}
    return true;
  };
})(window);
