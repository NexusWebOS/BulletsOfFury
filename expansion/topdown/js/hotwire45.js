/* Player-grade Hotwire plates shared by the pilot and the story companion. */
(function(root){
 'use strict';
 const TD=root.TD,M=TD.M,I=TD.Input,A=TD.Audio,P=root.TD_GOSFAR45_ART,art=TD.AssaultArt;
 const api=TD.Hotwire45={};
 const DIR=['south','south-west','west','north-west','north','north-east','east','south-east'];
 const direction=a=>DIR[(Math.round((a||0)/(Math.PI/4))%8+8)%8];
 const cardinal=a=>Math.abs(Math.sin(a||0))>Math.abs(Math.cos(a||0))?(Math.sin(a)<0?'east':'west'):(Math.cos(a)<0?'north':'south');
 const weapon=p=>p.weapon||(p.weapons?.[p.wi||0]?.id==='desert_eagle'?'eagle':'rifle');
 function bank(w,a,d){return P.banks['hotwire/'+w+'/'+a+'/'+d];}
 function choose(w,a,d,angle){const c=cardinal(angle),fallback=a==='crouch_walk'?'crouch':a==='run_fire'?'fire':a==='prone_roll'?'roll':null;return bank(w,a,d)||bank(w,a,c)||(fallback&&(bank(w,fallback,d)||bank(w,fallback,c)))||(['jump','death','roll','prone_roll','grenade'].includes(a)&&(bank(w,a,'south')||bank(w,a,'north')))||bank(w,'ready',d)||bank(w,'ready',c);}
 api.pose=function(p){const aim=p.roll>0?p.rollAim:p.aim||0,d=direction(aim),w=weapon(p);let action=p.action||'ready',clock=p.actionT||0,loop=false,phase=null;
  if(typeof action==='object')action='grenade';
  if(p.pilot==='hotwire'){
   action=p.dead?'death':p.roll>0?(p.rollFromProne39?'prone_roll':'roll'):p.jump>0?'jump':p.action?'grenade':p.reload45>0?'reload':p.prone?(p.moving?'crawl':p.firing>0?'prone_fire':'prone'):p.stance==='crouch'||p.cover?(p.firing>0?'crouch_fire':p.moving?'crouch_walk':'crouch'):p.firing>0?(p.moving?'run_fire':'fire'):p.moving?'walk':'ready';
   if(p.dead)clock=p.deadT||0;else if(p.roll>0)clock=.5-p.roll;else if(p.jump>0)clock=.65-p.jump;else if(p.action)clock=p.action.t||0;else if(p.reload45>0)clock=1.1-p.reload45;else if(p.firing>0)clock=p.hotFire45||0;else clock=p.footTime||0;
  }
  if(action==='cover')action='crouch';
  if(action==='hack'){const b=P.banks['hotwire/hack'];return{key:b.frames[Math.floor((p.t||0)*b.fps)%b.frames.length],scale:1,angle:0,dir:'north',action:'hack',bank:'hotwire/hack'};}
  if(action==='throw')action='grenade';
  if(action==='prone_fire'&&!bank(w,action,d)&&!bank(w,action,cardinal(aim)))action='prone';
  if(action==='crouch_fire'&&!bank(w,action,d)&&!bank(w,action,cardinal(aim)))action='crouch';
  let b=choose(w,action,d,aim);if(['roll','prone_roll','grenade','jump','death'].includes(action))b=choose('rifle',action,d,aim)||b;
  if(!b)return null;
  if(['walk','run','crawl','crouch_walk','run_fire'].includes(action)&&p.moving){phase=((p.gaitPhase||0)%1+1)%1;const key=b.frames[Math.floor(phase*b.frames.length)%b.frames.length];return{key,scale:1,angle:0,dir:d,action,bank:'hotwire/'+w+'/'+action+'/'+d,phase};}
  if(['fire','prone_fire','crouch_fire'].includes(action))loop=true;
  if(['crouch','prone','ready'].includes(action)){clock=0;loop=false;}
  const n=loop?Math.floor(clock*b.fps)%b.frames.length:Math.min(b.frames.length-1,Math.floor(clock*b.fps));return{key:b.frames[Math.max(0,n)],scale:1,angle:0,dir:d,action,bank:'hotwire/'+w+'/'+action+'/'+d};
 };
 api.socket=function(p){const z=api.pose(p),m=z&&P.assets[z.key];if(!m)return{x:p.x,y:p.y-45};const u=m.muzzle||[m.anchor[0],m.anchor[1]-45];return{x:p.x+u[0]-m.anchor[0],y:p.y+u[1]-m.anchor[1]};};
 api.draw=function(ctx,p,o={}){const z=api.pose(p);if(!z)return;art.draw(ctx,z.key,p.x,p.y-(p.jumpZ||0),{s:1,flash:o.flash??((p.flash||0)>0?.8:0),alpha:p.dead?.65:1});};
 const pose=TD.footPose;TD.footPose=function(p){if(p.pilot==='hotwire'&&!p.pseudo3D&&!p.sideScroll){const z=api.pose(p);if(z)return z;}return pose(p);};
 const draw=TD.drawFoot;TD.drawFoot=function(ctx,p,o){if(p.pilot==='hotwire'&&!p.pseudo3D&&!p.sideScroll)return api.draw(ctx,p,o);return draw(ctx,p,o);};
 const make=TD.makeFootPlayer;TD.makeFootPlayer=function(...args){const p=make(...args);if(p.pilot==='hotwire'){p.weapons.push({id:'desert_eagle',lv:1,ammo:84,reserve:0});p.mag45={assault_rifle:30,desert_eagle:7};p.reload45=0;}return p;};
 TD.FOOT_GUNS.desert_eagle={...TD.FOOT_GUNS.desert_eagle,name:'DESERT EAGLE',damage:4,cd:17,speed:11,cue:'od75_sniper'};
 const hudModel=TD.CornerHUD26.model;TD.CornerHUD26.model=function(G,pseudo){const v=hudModel(G,pseudo),p=G.player,w=p.weapons?.[p.wi||0];if(p.pilot==='hotwire'&&!pseudo&&p.mag45&&p.mag45[w?.id]!=null){v.ammo=p.mag45[w.id]+'/'+(w.ammo===Infinity?'INF':Math.max(0,w.ammo-p.mag45[w.id]));if(p.reload45>0)v.status='RELOADING';}return v;};
 const tick=TD.footTick;TD.footTick=function(p,G,dt){if(p.pilot!=='hotwire'||p.pseudo3D||p.sideScroll||p.dead||p.scripted)return tick(p,G,dt);
  p.mag45??={assault_rifle:30,desert_eagle:7};
  if((I.tap('swap')||I.state.wheel)&&p.weapons.length>1&&!(p.reload45>0)){p.wi=(p.wi+1)%p.weapons.length;A.play('loadoutSelect',.5);}
  const id=p.weapons[p.wi||0]?.id;
  if((I.tap('reload')||p.mag45[id]===0)&&!(p.reload45>0)&&p.roll<=0&&['assault_rifle','desert_eagle'].includes(id)){p.reload45=1.1;p.reloadWeapon45=id;A.play('loadoutEquip',.6);}
  if(p.reload45>0){p.fireCd=Math.max(p.fireCd||0,2);p.reload45=Math.max(0,p.reload45-dt);if(!p.reload45){p.mag45[p.reloadWeapon45]=p.reloadWeapon45==='desert_eagle'?7:30;A.play('gd_ammoPickup',.5);}}
  const tap=I.tap,old=G.shots.length;I.tap=function(k){return k==='reload'?false:tap.call(this,k);};try{tick(p,G,dt);}finally{I.tap=tap;}
  p.hotFire45=p.firing>0?(p.hotFire45||0)+dt:0;
  if(G.shots.length>old&&p.mag45[id]!=null)p.mag45[id]=Math.max(0,p.mag45[id]-1);
 };
})(window);
