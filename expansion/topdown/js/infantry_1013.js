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
  TD.drawShot=function(ctx,s,enemy){if(s.drawLift){ctx.save();ctx.translate(0,-s.drawLift);oldShot(ctx,s,enemy);ctx.restore();}else oldShot(ctx,s,enemy);};
  TD.footLift=p=>p.stance==='prone'&&!p.peekExposed?15:p.stance==='crouch'&&!p.peekExposed?28:45;
  TD.FOOT_GUNS.assault_rifle={name:'ASSAULT RIFLE',cap:Infinity,reserve:0,cd:7,damage:2,k:'vulcan',speed:10};
  const oldMake=TD.makeFootPlayer,oldPose=TD.footPose,oldDraw=TD.drawFoot,oldSocket=TD.footSocket,oldPickupDraw=TD.drawFootPickup,oldHurt=TD.hurtPlayer;
  const rifle=()=>({id:'assault_rifle',lv:1,ammo:Infinity,reserve:0});
  if(!TD.FOOT_EXTRA.includes('repair'))TD.FOOT_EXTRA.push('repair');
  TD.makeFootPlayer=(x,y)=>Object.assign(oldMake(x,y),{hp:3,max:3,r:10,modernFoot:true,weapons:[rifle()],wi:0,stance:'stand',jump:0,roll:0,stamina:1,cover:null,peek:0,peekExposed:false,prone:false,poseT:0,walkT:0,gaitPhase:0,gaitSettle:0,motionFacing:null});
  TD.hurtPlayer=function(G,dmg,x,y){
    const p=G.player;if(!p.modernFoot)return oldHurt(G,dmg,x,y);
    if(p.dead||p.inv>0||G.state!=='play'||p.jump>.16&&p.jump<.52||p.roll>.08&&p.roll<.42)return;
    p.hp-=Math.max(1,dmg*(TD.DIFFICULTIES?.[TD.difficulty||'normal']?.damage||1));p.inv=65;p.flash=.18;TD.Cam.kick(4);A.play('hit');
    if(p.hp<=0)G.playerDied();
  };
  function nearestCover(p,G){
    let best=null,dist=30;
    for(const s of G.structures)if(s.assault&&!s.dead&&s.cover){const r=s.rect,d=Math.hypot(p.x-M.clamp(p.x,r.x0,r.x1),p.y-M.clamp(p.y,r.y0,r.y1));if(d<dist){dist=d;best=s;}}
    return best;
  }
  // The peek socket exits only the player's own cover. Every other wall and
  // destructible object still participates in the ordinary swept shot query.
  TD.footAimOrigin=function(p){
    if(p.cover&&!p.cover.dead&&p.peekExposed&&p.cover.type.art!=='wall'){
      const q=p.cover.rect,f=M.fwd(p.aim),x=p.x,y=p.y,steps=Math.max(q.x1-q.x0,q.y1-q.y0)+45;
      let entered=false;
      for(let d=1;d<steps;d+=2){const px=x+f[0]*d,py=y+f[1]*d,inside=px>=q.x0-5&&px<=q.x1+5&&py>=q.y0-5&&py<=q.y1+5;
        if(inside)entered=true;else if(entered)return{x:px,y:py};}
    }
    const f=M.fwd(p.aim);return{x:p.x+f[0]*20,y:p.y+f[1]*20};
  };
  TD.footSocket=function(p){return p.modernFoot?TD.footAimOrigin(p):oldSocket(p);};
  TD.footSightOrigin=function(p,target){
    const aim=M.angTo(p.x,p.y,target.x,target.y);
    if(p.cover?.type.art==='wall'&&!p.cover.dead){const q=p.cover.rect,anchor=p.coverAnchor||p;return{x:anchor.x,y:target.y<p.cover.y?q.y0-p.r-8:q.y1+p.r+8};}
    return TD.footAimOrigin({...p,aim,peekExposed:true});
  };
  TD.footBriefKeys=()=>I.padStyle()==='standard'?[['a','FIRE / PEEK'],['b','JUMP'],['x','ROLL'],['y','GRENADE'],['dpad','MOVE'],['start','PAUSE']]:[['x','FIRE NORTH'],['y','FIRE WEST'],['z','GRENADE'],['a','FIRE SOUTH'],['b','FIRE EAST'],['c','ROLL']];
  function fire(p,G){
    let w=p.weapons[p.wi],d=TD.FOOT_GUNS[w.id];
    if(!d||w.ammo<=0){p.weapons=p.weapons.filter(q=>q.id==='assault_rifle'||q.ammo>0);p.wi=0;w=p.weapons[0];d=TD.FOOT_GUNS[w.id];}
    const socket=TD.footSocket(p);
    if(!p.peekExposed&&W.rayBlock(p.x,p.y,socket.x,socket.y)){p.fireCd=8;A.play('blocked',.3);return;}
    const target=p.retina?.locked&&p.retina.target?.valid()?p.retina.target.point():null;
    const aim=target?M.angTo(socket.x,socket.y,target.x,target.y):p.aim;
    const lv=w.lv||1,lift=TD.footLift(p);p.fireCd=Math.max(3,d.cd-(lv-1));p.firing=.13;
    for(const delta of d.fan||[0]){const a=aim+delta,f=M.fwd(a);G.shots.push({k:d.k,x:socket.x,y:socket.y,a,vx:f[0]*d.speed,vy:f[1]*d.speed,dmg:d.damage*(1+(lv-1)*.35),life:65,r:3,pierce:d.pierce||0,splash:d.splash,sdmg:5,lv:1,t:0,drawLift:lift,homing:w.id==='rocket_launcher',napalm:w.id==='napalm_launcher'});}
    if(w.id!=='assault_rifle'&&--w.ammo<=0){p.weapons.splice(p.wi,1);p.wi=0;G.say('ASSAULT RIFLE - UNLIMITED',p);}
    FX.flash(socket.x,socket.y-lift,aim,.12);A.play(d.k==='laser'?'laser':d.k==='homing'?'missileLaunch':'gd_soldierRifle',.55);
    TD.Stealth.noise(p.x,p.y,200,.6,G.units);
  }
  TD.footTick=function(p,G,dt){
    if(!p.modernFoot||p.dead||p.scripted)return;
    p.footTime+=dt;p.poseT+=dt;p.inv=Math.max(0,p.inv-1);p.flash=Math.max(0,p.flash-dt);p.fireCd=Math.max(0,p.fireCd-1);p.firing=Math.max(0,(p.firing||0)-dt);p.stamina=Math.min(1,p.stamina+dt*.6);
    const [dx,dy]=I.dir(),len=Math.hypot(dx,dy)||1,aim=I.aim({x:p.x,y:p.y-TD.footLift(p)});
    TD.Retina.tick(p,G,dt);
    if(p.retina?.locked){const q=p.retina.target.point();p.aim=M.angTo(p.x,p.y,q.x,q.y);}
    else if(aim!=null){p.aim=aim;p.manualAim=90;}
    else if(I.down('aimLeft')||I.down('aimRight')){p.aim+=(I.down('aimRight')?1:-1)*.09;p.manualAim=90;}
    else if(p.manualAim>0)p.manualAim--;else if(dx||dy)p.aim=M.angTo(0,0,dx,dy);
    if(dx||dy)p.a=M.angTo(0,0,dx,dy);
    if(I.tap('prone')){p.prone=!p.prone;p.poseT=0;A.play('gd_coverEnter',.5);}
    if((I.tap('jump')||I.tap('reload')||I.tap('B')&&!I.state.directionalFire)&&p.jump<=0&&p.roll<=0&&p.stamina>=.35){p.jump=.65;p.stamina-=.35;p.prone=false;p.poseT=0;A.play('stylishDodge',.4);}
    if(I.tap('X')&&p.jump<=0&&p.roll<=0&&p.stamina>=.45){p.roll=.5;p.rollAim=(dx||dy)?p.a:p.aim;p.stamina-=.45;p.poseT=0;A.play('stylishDodge',.5);}
    const low=I.down('C')||I.down('cover')||p.prone;
    const oldCover=p.cover;
    p.cover=low&&p.jump<=0&&p.roll<=0?nearestCover(p.coverAnchor||p,G):null;
    if(!p.cover||p.cover!==oldCover||dx||dy){if(p.coverAnchor){p.x=p.coverAnchor.x;p.y=p.coverAnchor.y;}p.coverAnchor=null;}
    if(p.cover?.type.art==='wall'&&!dx&&!dy&&!p.coverAnchor)p.coverAnchor={x:p.x,y:p.y};
    p.peek=p.cover&&I.down('A')?(p.peek+dt)% .72:0;p.peekExposed=!!p.cover&&p.peek>=.24&&p.peek<.48;
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
    if(p.coverAnchor){const q=p.cover.rect,anchor=p.coverAnchor,t=p.peek,edge=t<.24?t/.24:t<.48?1:(.72-t)/.24;
      const y=Math.cos(p.aim)<0?q.y0-p.r-8:q.y1+p.r+8;p.x=anchor.x;p.y=M.lerp(anchor.y,y,Math.max(0,edge));W.collide(p,p.r,false);}
    p.hidden=!!W.inType(p.x,p.y,'h')||!!W.inType(p.x,p.y,'d')||!!p.cover&&!p.peekExposed;
    if((I.tap('swap')||I.state.wheel)&&p.weapons.length>1){p.wi=(p.wi+1)%p.weapons.length;A.play('loadoutSelect');}
    if(I.tap('tapWall')){const f=M.fwd(p.aim),x=p.x+f[0]*20,y=p.y+f[1]*20;if(W.solidAt(x,y)){TD.Stealth.noise(x,y,180,.25,G.units);G.say('TAP',p);A.play('blip',.2);}}
    if(I.tap('Y')&&p.smoke>0&&p.roll<=0&&!p.action)p.action={kind:'grenade',t:0,aim:p.aim,committed:false};
    if(p.action){p.action.t+=dt;if(!p.action.committed&&p.action.t>=.3){p.action.committed=true;p.smoke--;const f=M.fwd(p.action.aim);G.footGrenades.push({x:p.x,y:p.y,tx:p.x+f[0]*125,ty:p.y+f[1]*125,t:0,done:false});A.play('bombDrop',.5);}if(p.action.t>=.6)p.action=null;}
    if(I.down('A')&&p.fireCd<=0&&p.roll<=0&&!p.action&&(!p.cover||p.peekExposed))fire(p,G);
    p.roll=Math.max(0,p.roll-dt);p.jump=Math.max(0,p.jump-dt);p.jumpZ=p.jump>0?Math.sin((.65-p.jump)/.65*Math.PI)*28:0;
  };
  TD.footPose=function(p){
    if(p.pilot!=='yuri')return oldPose(p);
    if(p.dead)return{key:art.frame('yuri_death',p.deadT||0,false),angle:0,scale:.42,action:'death',dir:'south'};
    if(p.action)return{key:art.frame('yuri_grenade',p.action.t,false),angle:0,scale:.42,action:'grenade',dir:'south'};
    const dir=DIR[facing(p,p.roll>0?p.rollAim:p.aim)];let action=p.firing>0?'run_fire':'walk',t=p.moving?p.walkT:0,loop=true;
    if(p.stance==='crouch'){action='crouch';t=Math.min(.5,p.poseT);loop=false;}
    if(p.stance==='prone'){action=p.moving?'crawl':'prone_fire';t=p.moving?p.walkT:p.firing>0?p.footTime:.1;}
    if(p.cover&&p.peek>0){action='peek';t=p.peek/.72*.6;loop=false;}
    if(p.jump>0){action='jump';t=(.65-p.jump)/.65*.6;loop=false;}
    if(p.roll>0){action='roll';t=(.5-p.roll)/.5*.6;loop=false;}
    // New motion banks use the same cycle phase even when frame counts differ.
    // Idle/prone hold the planted frame instead of changing body banks.
    const bank='yuri_'+dir+'_'+(action==='prone_fire'?'crawl':action),seq=PACK.sequences[bank];
    if(seq?.motion){const phase=p.gaitPhase??wrap(p.walkT*165/(seq.stride||96)),index=Math.floor(wrap(phase)*seq.frames.length+1e-8)%seq.frames.length;return{key:seq.frames[index],angle:0,scale:.42,action,dir,phase,index};}
    return{key:art.frame(bank,t,loop),angle:0,scale:.42,action,dir};
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
      if(d&&k.kind!=='assault_rifle'){let w=p.weapons.find(w=>w.id===k.kind);if(!w){w={id:k.kind,lv:1,ammo:0,reserve:0};if(p.weapons.length>=4)p.weapons.splice(p.wi||1,1);p.weapons.push(w);}w.ammo+=d.cap+d.reserve;p.wi=p.weapons.indexOf(w);G.say(d.name,p);A.play('weaponFound');}
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
    const label=p.cover?(p.peekExposed?'EXPOSED - FIRING':'IN COVER'):p.jump>0?'JUMP':p.roll>0?'ROLL':p.stance.toUpperCase();text(label,12,TD.VH-16,10,p.peekExposed?'#ffa763':'#8ceaff');
    if(p.retina?.phase)text('RETINA '+(p.retina.locked?'LOCKED':'SEEKING'),TD.VW-12,TD.VH-16,10,'#ffd566','right');
    if(G.boss?.alive()){const b=G.boss,x=160,y=TD.VH-24;ctx.fillStyle='#17202c';ctx.fillRect(x,y,TD.VW-320,9);ctx.fillStyle='#e63b42';ctx.fillRect(x+1,y+1,(TD.VW-322)*b.hpFrac(),7);text(b.name,TD.VW/2,y-11,11,'#ffd060','center');}
    return true;
  };
  // Museum keeps its encounter and vehicle systems; rifle fallback survives a death.
  const museum=TD.MISSIONS.find(m=>m.id===5);
  if(museum){const respawn=museum.respawn;museum.respawn=(G,p,f)=>{respawn?.(G,p,f);f.weapons=f.weapons.filter(w=>w.id!=='desert_eagle');if(!f.weapons.some(w=>w.id==='assault_rifle'))f.weapons.unshift(rifle());f.wi=0;};const hud=museum.hud;museum.hud=(ctx,text,G)=>G.player.onfoot?TD.infantryHUD(ctx,text,G):hud(ctx,text,G);}
})(window);
