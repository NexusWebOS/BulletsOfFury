'use strict';
/* Wind omega: one native life, non-destructible visual guns, measured emitters. */
const NW30={base:{get:XART.get,touch:XART._touch,load:stageLoadBegin,tick:whvAceTick,body:nw28DrawBody,draw:whvDrawAce,guns:whvAceGuns,missiles:whvAceFireMissiles,bg:drawBG,projectile:drawCombatFinalProjectile,intercept:enemyOrdnanceCanIntercept,element:enemyOrdnanceElement},events:[],last:null,dim:0};
for(const b of Object.values(NW30_ART.banks))XART._src[b.key]=b.path;
function nw30Own(b){return nw28Own(b);}
function nw30Palette(){return run.stage===6&&!run._gp4StageX;}
XART._touch=function(k){const n=nw30Palette()&&NW30_ART.aliases[k];return NW30.base.touch.call(this,n?NW30_ART.banks[n].key:k);};
XART.get=function(k){const n=nw30Palette()&&NW30_ART.aliases[k];return NW30.base.get.call(this,n?NW30_ART.banks[n].key:k);};
stageLoadBegin=function(n,keys){if(n===6)Snd.prepare?.(["bossWeaponCharge","combatOrb0927"]);return NW30.base.load.call(this,n,n===6?[...(keys||[]),...Object.values(NW30_ART.banks).map(b=>b.key),...Array.from({length:8},(_,i)=>'laser_round_muzzle_'+i),'cf50_scenery_dim']:keys);};
function nw30Log(b,event,data={}){NW30.events.push({event,time:efxClock,...data});if(NW30.events.length>500)NW30.events.shift();}
function nw30State(b){return b._nw30||(b._nw30={gunCd:1.8,windCd:6,action:null,angles:[Math.PI/2,Math.PI/2],recoil:[0,0],rings:[],ringCd:0,serial:0});}
function nw30Blit(name,f,x,y,g=ctx){const a=NW30_ART.banks[name];if(!a||!XART.rdy(a.key))return;f=Math.max(0,Math.min(a.frames-1,f));g.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x)-a.pivot[0],Math.round(y)-a.pivot[1],a.cw,a.ch);}
function nw30Pose(b){const A=b._whv.ace,p=A._nf29Pose;return p?{bank:p.bank,frame:p.frame,meta:NW30_ART.sockets[p.bank][p.frame]}:{bank:'whole',frame:nw28Frame(b),meta:NW30_ART.sockets.whole[nw28Frame(b)]};}
function nw30Gun(b,side,angle=null){const A=b._whv.ace,S=nw30State(b),a=(angle??S.angles[side])-Math.PI/2,dir=((Math.round(a/TAU*32)%32)+32)%32,r=Math.min(3,Math.floor((.12-S.recoil[side])/.12*4)),f=dir*4+Math.max(0,r),socket=NW30_ART.sockets['gun_'+(side?'right':'left')][f],x=A.x+(side?58:-58),y=A.y+6;return{x,y,mx:x+socket[0],my:y+socket[1],angle:Math.PI/2+dir*TAU/32,frame:f};}
function nw30Aim(b,tx,ty){const S=nw30State(b);for(let i=0;i<2;i++){const g=nw30Gun(b,i);S.angles[i]=clamp(Math.atan2(ty-g.y,tx-g.x),Math.PI/2-.65,Math.PI/2+.65);}}
function nw30Cancel(b){const S=nw30State(b),A=b._whv.ace;S.action=null;A._pw5Gun=A._ra7Gate=null;A.burst=A._pw5Missiles=0;for(const L of playerLocks)if(L.src===b)L.launches=L.launches.filter(q=>q.done);}
function nw30Ready(b){const A=b._whv.ace;return b._whv.mode==='ace'&&A.st==='fight'&&!nw28Intro(A)&&!A.roll&&!A.somer&&!A.dash&&(!A.desp||A.desp.st==='done')&&!nf29Hidden(A);}
function nw30Start(b,kind){const A=b._whv.ace,S=nw30State(b);nw30Cancel(b);const C=S.action={kind,phase:kind==='wind'?'charge':'warn',t:0,n:0,next:0,x:A.x,y:A.y,tx:player.x,ty:player.y,warn:diffKey==='easy'?1.25:diffKey==='normal'?1.05:.95,id:++S.serial};A.vx=A.vy=0;nw30Aim(b,C.tx,C.ty);
 if(kind==='gun'){enemyLockOn(b,C.warn,{fire:()=>{if(b.dead||S.action!==C||!nw30Ready(b))return;C.phase='fire';C.t=C.next=0;nw30Log(b,'dual-gun-release',{id:C.id});}});}
 else{combatAudio0927(b,'bossWeaponCharge',.65);S.windCd=diffKey==='furious'?12:15;}
 nw30Log(b,kind+'-warning',{id:C.id,tx:C.tx,ty:C.ty});
}
function nw30Shoot(b,C){const S=nw30State(b),wind=C.kind==='wind';
 for(let i=0;i<2;i++){
  const spread=wind?[-.24,0,.24]:[0];S.angles[i]=Math.atan2(C.ty-(b._whv.ace.y+6),C.tx-(b._whv.ace.x+(i?58:-58)));S.angles[i]=clamp(S.angles[i],Math.PI/2-.65,Math.PI/2+.65);S.recoil[i]=.12;
  // The posed barrel and every emitted round use one quantized firing angle.
  const g=nw30Gun(b,i);for(const off of spread){const p=eShootT(g.mx,g.my,g.angle+off,wind?4.0:5.3,'s6tracer',{owner:b,silent:wind||i>0||off!==0,w:wind?18:7,h:wind?18:14});p.owner=b;p._nw30Owner=b;p._nw30Wind=wind;p._shootable=false;p._weaponProof=false;}
  wm26Emit(b,g.mx,g.my,g.angle,wind?'nw30wind':'mg',null,{size:wind?32:20,life:wind?.18:.13,follow:wind?()=>{const p=nw30Gun(b,i);return{x:p.mx,y:p.my,angle:p.angle};}:undefined});nw30Log(b,'turret-shot',{id:C.id,kind:C.kind,side:i,x:g.mx,y:g.my,angle:g.angle,frame:g.frame});
 }
 if(wind)combatAudio0927(b,'combatOrb0927',.20);C.n++;
}
whvAceGuns=function(b){if(nw30Own(b))return;return NW30.base.guns.apply(this,arguments);};
whvAceFireMissiles=function(b){if(nw30Own(b))return;return NW30.base.missiles.apply(this,arguments);};
whvAceTick=function(b,dt){if(!nw30Own(b)||b.dead)return NW30.base.tick.apply(this,arguments);const A=b._whv.ace,S=nw30State(b);dt=Math.min(.05,dt);S.recoil=S.recoil.map(t=>Math.max(0,t-dt));S.rings=S.rings.filter(r=>efxClock-r.at<.56);S.ringCd-=dt;
 // Retire the overlapping legacy volley/orb; the single dual-gun owner below
 // provides committed tells and all new rounds. Native flight/evasions remain.
 A._ra7Cd=999;A._ra7Gate=A._pw5Gun=null;A.burst=A._pw5Missiles=0;if(b.hp<=b.maxhp*.5)A.orb={a:0,cd:999};
 if(S.action&&!nw30Ready(b))nw30Cancel(b);
 const C=S.action;
 if(C){C.t+=dt;A.t+=dt;A.x=C.x;A.y=C.y+Math.sin(C.t*2.4)*1.5;A.vx=A.vy=0;b.x=A.x;b.y=A.y;b._drawY=A.y;
  if(C.phase==='charge'){combatWarningTick(b,'nw30-wind',C.t,2.1);if(C.t>=2.1){C.phase='fire';C.t=C.next=0;nw30Log(b,'wind-release',{id:C.id});}}
  else if(C.phase==='warn')combatWarningTick(b,'nw30-gun',C.t,C.warn);
  else if(C.phase==='fire'){
   if(C.t>=C.next&&C.n<(C.kind==='wind'?5:diffKey==='furious'?10:8)){C.next+=C.kind==='wind'?.24:.105;nw30Shoot(b,C);}
   if(C.t>(C.kind==='wind'?1.35:1.3)){C.phase='recover';C.t=0;nw30Log(b,'turret-recovery',{kind:C.kind,id:C.id});}
  }else if(C.t>.9){S.action=null;S.gunCd=2.3;A.gunCd=1;A.mslCd=4;nw30Log(b,'attack-complete',{kind:C.kind,id:C.id});}
 }else{
  const out=NW30.base.tick.apply(this,arguments);S.gunCd-=dt;S.windCd-=dt;
  if(nw30Ready(b)){if(S.windCd<=0)nw30Start(b,'wind');else if(S.gunCd<=0)nw30Start(b,'gun');}
  const fast=A.dash&&['go','flyover'].includes(A.dash.st)||A.desp&&['south','cross'].includes(A.desp.st);
  if(fast&&S.ringCd<=0&&!nw28Intro(A)){const p=nw30Pose(b),m=p.meta,ex=m.engines.reduce((s,p)=>s+p[0],0)/2,ey=m.engines.reduce((s,p)=>s+p[1],0)/2;S.rings.push({x:A.x+ex,y:A.y+ey,angle:m.angle,at:efxClock});if(S.rings.length>6)S.rings.shift();S.ringCd=.12;nw30Log(b,'dash-wind-ring');}
  return out;
 }
};
function nw30Modular(b){const A=b._whv.ace;return !b.dead&&!nw28Intro(A)&&!A._nf29Pose&&!A.roll&&!A.somer&&(!A.desp||A.desp.st==='done')&&(!!nw30State(b).action||Math.abs(A.vx)<=170||A.inverted);}
function nw30Shadow(b,p){const A=b._whv.ace;if(b.dead||A.dash?._nf29&&['offscreen','flyover_warn'].includes(A.dash.st))return;const scale=p.meta.scale||1,dx=Math.round(NW30_ART.flight.shadowOffset[0]*scale),dy=Math.round(NW30_ART.flight.shadowOffset[1]*scale);if(nw30Modular(b)){const f=A.inverted?16:(b.hp<b.maxhp*.5?8:0)+Math.floor(efxClock*14)%8;nw30Blit('clean_shadow',f,A.x+dx,A.y+dy);for(let i=0;i<2;i++){const g=nw30Gun(b,i);nw30Blit('gun_'+(i?'right':'left')+'_shadow',g.frame,g.x+dx,g.y+dy);}}else nw30Blit(p.bank+'_shadow',p.frame,A.x+dx,A.y+dy);}
nw28DrawBody=function(b){if(!nw30Own(b))return NW30.base.body.apply(this,arguments);const A=b._whv.ace,S=nw30State(b),p=nw30Pose(b),m=p.meta;if(!b.dead&&A.dash?._nf29&&['offscreen','flyover_warn'].includes(A.dash.st))return;
 nw30Shadow(b,p);
 for(const r of S.rings){if(efxClock-r.at>=.56)continue;const a=((Math.round(r.angle/TAU*16)%16)+16)%16,f=Math.min(7,Math.floor((efxClock-r.at)/.56*8));nw30Blit('wind_ring',a*8+f,r.x,r.y);}
 if(!b.dead&&!(A.dash?._nf29&&['offscreen','flyover_warn'].includes(A.dash.st))){
  const fast=A.dash&&['go','flyover','drift'].includes(A.dash.st)||A.desp&&['south','cross'].includes(A.desp.st),large=m.scale>1.35,dir=((Math.round(m.angle/TAU*32)%32)+32)%32,mode=large?'large_'+(dir>=16?'b':'a'):m.scale<.85?'small':fast?'boost':'cruise',f=(large?dir%16:dir)*NW30_ART.exhaustFrames+Math.floor(efxClock*22)%NW30_ART.exhaustFrames;
  const visible=[];for(const [x,y]of m.engines){if(visible.some(q=>Math.hypot(q[0]-x,q[1]-y)<7))continue;visible.push([x,y]);nw30Blit('exhaust_'+mode,f,A.x+x,A.y+y);}NW30.last={pose:p.bank,frame:p.frame,engines:visible.map(([x,y])=>[A.x+x,A.y+y]),throttle:mode,modular:nw30Modular(b)};
 }
 if(nw30Modular(b)){
  const idx=A.inverted?16:(b.hp<b.maxhp*.5?8:0)+Math.floor(efxClock*14)%8;nw30Blit(b.flash>0?'clean_hit':'clean',idx,A.x,A.y);
  for(let i=0;i<2;i++){const g=nw30Gun(b,i);nw30Blit('gun_'+(i?'right':'left')+(b.flash>0?'_hit':''),g.frame,g.x,g.y);}
 }else{nw30Blit(p.bank+(b.flash>0&&!b.dead?'_hit':''),p.frame,A.x,A.y);NW28.draws++;NW28.last={frame:p.frame,key:NW30_ART.banks[p.bank].key,x:A.x,y:A.y,whole:true};if(A._nf29Pose)NF29.last={bank:p.bank,frame:p.frame,key:NW30_ART.banks[p.bank].key,x:A.x,y:A.y,scale:m.scale,whole:true};}
 if(S.action?.kind==='wind'&&S.action.phase==='charge')nw30Blit('wind_charge',Math.floor(efxClock*18)%NW30_ART.banks.wind_charge.frames,A.x,A.y);
};
whvDrawAce=function(b){const r=NW30.base.draw.apply(this,arguments);if(!nw30Own(b)||b.dead)return r;const S=nw30State(b),C=S.action;if(!C||!['warn','charge'].includes(C.phase))return r;
 const progress=C.t/(C.kind==='wind'?2.1:C.warn);for(let i=0;i<2;i++){const g=nw30Gun(b,i);for(const off of C.kind==='wind'?[-.24,0,.24]:[0])combatWarningDraw(b,{x:g.mx,y:g.my,ex:g.mx+Math.cos(g.angle+off)*900,ey:g.my+Math.sin(g.angle+off)*900,width:C.kind==='wind'?24:16,progress,fieldOnly:true});}return r;};
drawBG=function(){const r=NW30.base.bg.apply(this,arguments);const S=boss?._nw30,C=S?.action;NW30.dim=state===GS.PLAY&&boss&&!boss.dead&&nw30Own(boss)&&C?.kind==='wind'&&C.phase==='charge'?Math.round(clamp(C.t/1.6,0,1)*12):0;if(NW30.dim)cf50DimDraw(NW30.dim);return r;};
function nw30GustFrame(name,angle,t){const a=NW30_ART.banks[name],d=((Math.round((angle-Math.PI/2)/TAU*a.directions)%a.directions)+a.directions)%a.directions;return d*a.phaseFrames+(Math.floor(t*a.phaseFrames)%a.phaseFrames);}
WM26_REELS.nw30wind={key:NW30_ART.banks.wind_muzzle.key,n:NW30_ART.banks.wind_muzzle.phaseFrames,size:32,pivot:.5};
const nw30WindMuzzleDraw=wm26Draw;
wm26Draw=function(g,family,x,y,angle,progress){if(family!=='nw30wind')return nw30WindMuzzleDraw.apply(this,arguments);nw30Blit('wind_muzzle',nw30GustFrame('wind_muzzle',angle,clamp(progress,0,.999)),x,y,g);return true;};
drawCombatFinalProjectile=function(q){if(!q?._nw30Wind)return NW30.base.projectile.apply(this,arguments);const angle=Math.atan2(q.vy,q.vx);nw30Blit('wind_bullet',nw30GustFrame('wind_bullet',angle,(q.t||0)*24/NW30_ART.banks.wind_bullet.phaseFrames),q.x,q.y);return true;};
enemyOrdnanceCanIntercept=function(q){return q?._nw30Owner?false:NW30.base.intercept.apply(this,arguments);};
enemyOrdnanceElement=function(q){return q?._nw30Wind?'wind':NW30.base.element.apply(this,arguments);};
globalThis.BOF_NIGHTWING_WIND_1028=NW30;
