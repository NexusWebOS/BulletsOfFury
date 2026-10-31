"use strict";
/* Oct27 review. Encounter clocks, ordnance ownership and authored components. */
const ER28={events:[],rook:false,alpha:new Map(),base:{spawn:spawnBoss,mini:spawnSubBoss,opening:s6OpeningTick,wing:s6WingTick,
 onslaught:s6OnslaughtTick,rebelIntro:h3RebelTick,rebelDraw:fr27RebelDrawShip,socket:rr26Socket,enemyDraw:drawEnemy,
 rdy:XART.rdy,carrier:roster17Draw,muzzle:roster17Muzzle,weapon:roster17Weapon,turret:pf20TurretDraw,hive:hivewingTick,load:stageLoadBegin}};
function er28Log(event,data={}){ER28.events.push({event,t:efxClock,...data});if(ER28.events.length>1200)ER28.events.shift();}
for(const a of Object.values(ER28_ART))XART._src[a.key]=a.path;
function er28Blit(name,f,x,y,hit=false){const a=ER28_ART[name+(hit?'_hit':'')]||ER28_ART[name];if(!a||!XART.rdy(a.key))return false;
 f=((f|0)%a.frames+a.frames)%a.frames;ctx.drawImage(XART.get(a.key),(f%a.cols)*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);return true;}
function er28Dir(a){return((Math.round(a*64/TAU)%64)+64)%64;}
function er28AlphaAt(name,f,x,y){const a=ER28_ART[name];if(!a||!XART.rdy(a.key))return false;const px=Math.floor(x+a.pivot[0]),py=Math.floor(y+a.pivot[1]);if(px<0||py<0||px>=a.cw||py>=a.ch)return false;
 f=((f|0)%a.frames+a.frames)%a.frames;const id=name+':'+f;let alpha=ER28.alpha.get(id);if(!alpha){const c=document.createElement('canvas');c.width=a.cw;c.height=a.ch;const g=c.getContext('2d');g.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,0,0,a.cw,a.ch);const data=g.getImageData(0,0,a.cw,a.ch).data;alpha=Uint8Array.from({length:a.cw*a.ch},(_,i)=>data[i*4+3]);ER28.alpha.set(id,alpha);}return alpha[py*a.cw+px]>48;}
stageLoadBegin=function(n,keys){const names=Object.keys(ER28_ART).filter(k=>n===6?/rook|carrier|hull|clean/.test(k):n===7?/tank|warden|core|canister|rear|front|toxic/.test(k):n===8?/^(head_|herald_|death_ball|pentagram|tornado|nuke|lightning|code_round|dark|red_flash)/.test(k):false);
 return ER28.base.load.call(this,n,[...(keys||[]),...names.map(k=>ER28_ART[k].key)]);};
function er28Stage6Boss(){return run.stage===6&&!!(boss&&!boss.dead&&['warhive','rebelsquad'].includes(boss.kind));}
function er28WingReady(route){if(!s6Wing)s6WingInit();const W=s6Wing;
 s6Opening=null;fb2Talk=null;W.fake=null;W.fakeDone=true;W._fb2Talked=true;W.choice=false;W.beats=2;W.all=true;W.route=route;W.supplyIndex=3;W.postMiniT=99;W.line=null;
 s6WingLaunch(8,true);for(const q of W.ships){q.all=true;if(q.phase==='arrive'){q.phase='fight';q.t=1;q.x=camLeftX()+viewW()/2+(q.slot%2?1:-1)*(68+Math.floor(q.slot/2)*58);q.y=VH*.78+(q.slot%2)*26;}}
 W.er28Encounter=true;er28Log('stage6-encounter-entry',{route,allies:W.ships.length});
}
spawnBoss=function(kind){if(run.stage===6&&['warhive','rebelsquad'].includes(kind))er28WingReady(kind==='rebelsquad'?'right':'left');return ER28.base.spawn.apply(this,arguments);};
spawnSubBoss=function(){if(run.stage===6&&debugFight?.stage===6){if(!s6Wing)s6WingInit();s6Wing.er28Mini=true;}return ER28.base.mini.apply(this,arguments);};
s6OpeningTick=function(dt){if(er28Stage6Boss()||run.stage===6&&debugFight?.stage===6)return;return ER28.base.opening.apply(this,arguments);};
s6OnslaughtTick=function(){if(er28Stage6Boss()||s6Wing?.er28Encounter&&debugFight?.stage===6)return;return ER28.base.onslaught.apply(this,arguments);};
s6WingTick=function(dt){if(er28Stage6Boss()){
 const W=s6Wing;if(W){W.fakeDone=true;W.fake=null;W.beats=2;W.all=true;W.choice=false;W.postMiniT=99;W.supplyIndex=3;}
 }return ER28.base.wing.apply(this,arguments);};
h3RebelTick=function(b,dt){const out=ER28.base.rebelIntro.apply(this,arguments);if(b?._rebels&&!b._rebels.frIntro?.done&&s6Wing){
 for(const q of s6Wing.ships){q.t+=dt;q.phase='fight';q.x=camLeftX()+viewW()/2+(q.slot%2?1:-1)*(68+Math.floor(q.slot/2)*56);q.y=VH*.78+(q.slot%2)*24;q.vx=q.vy=0;}
 }return out;};
// Carrier helpers stay in the upper half and weave across each other. Their
// own warning commits the downward burst; no charging through the player.
hivewingTick=function(e,dt,X){if(!e?._whvEscort||!er28Stage6Boss())return ER28.base.hive.apply(this,arguments);
 const W=boss._whv;if(e.dead||e._dyingT!=null)return ER28.base.hive.apply(this,arguments);
 e._er28Weave??={t:0,cd:1.1+(e._hwSlot%3)*.4,phase:'weave',birth:{x:e.x,y:e.y}};const A=e._er28Weave;A.t+=dt;
 e._hwLaunch=e._hwPeel=e._hwD=e._fb2Tac=null;e._noHit=false;e._scale=1;e._et=(e._et||0)+dt;
 const left=camLeftX()+46,right=camRightX()-46,band=viewTopY()+viewH()*.27,side=e._hwSlot%2?1:-1,
 u=Math.sin(A.t*.82+Math.floor(e._hwSlot/2)*.78)*side,tx=(left+right)/2+u*(right-left)*.43,ty=band+(e._hwSlot%3)*24+Math.sin(A.t*1.64+e._hwSlot)*23;
 const old={x:e.x,y:e.y};e.x+=clamp(tx-e.x,-150*dt,150*dt);e.y+=clamp(ty-e.y,-170*dt,170*dt);e.y=clamp(e.y,viewTopY()+65,viewTopY()+viewH()*.47);
 fb2HwFace(e,Math.PI/2+clamp((e.x-old.x)*.025,-.65,.65));
 if(A.phase==='weave'){A.cd-=dt;if(A.cd<=0){A.phase='tell';A.clock=0;A.aim=aimPlayer(e.x,e.y);A.round=0;A.shot=0;}}
 else if(A.phase==='tell'){A.clock+=dt;combatWarningTick(A,'er28-helper-'+e._hwSlot,A.clock,.85);if(A.clock>=.85){A.phase='fire';A.clock=0;}}
 else{A.shot-=dt;if(A.shot<=0&&A.round<4){A.shot=.11;A.round++;eShootT(e.x,e.y+e.h*.35,A.aim,3.5,'s6tracer',{owner:e});e._muz=.1;}
 if(A.round>=4){A.phase='weave';A.cd=1.6+(e._hwSlot%3)*.25;}}
};
drawEnemy=function(e){const A=e?._er28Weave;if(A?.phase==='tell'&&!e.dead&&er28Stage6Boss())combatWarningDraw(e,{x:e.x,y:e.y+e.h*.35,ex:e.x+Math.cos(A.aim)*VH*1.4,ey:e.y+Math.sin(A.aim)*VH*1.4,width:16,progress:A.clock/.85,fieldOnly:true});return ER28.base.enemyDraw.apply(this,arguments);};
// Suppress the old fixed player pods only while Rook's native hull renders.
XART.rdy=function(k){if(ER28.rook&&String(k).startsWith(CHAINGUN_POD_KEY))return false;return ER28.base.rdy.apply(this,arguments);};
fr27RebelDrawShip=function(q){if(q.key!=='rook'||q.dead)return ER28.base.rebelDraw.apply(this,arguments);
 let out;ER28.rook=true;try{out=ER28.base.rebelDraw.apply(this,arguments);}finally{ER28.rook=false;}
 const a=q.rfHeading??Math.PI/2,c=Math.cos(a),s=Math.sin(a),phase=q.rg4?.act?.phase,f=Math.floor((q.t||0)*(phase==='fire'?26:phase==='charge'?14:4))%4;
 const kick=q._rr26Kick?Math.sin(q._rr26Kick/.12*Math.PI)*2.5:0;
 for(const side of[-1,1]){const x=q.x+c*13-s*side*23,y=q.y+s*13+c*side*23-kick;er28Blit('rook_pod',er28Dir(a-Math.PI/2)+f*64,x,y,q.flash>0);}
 return out;};
rr26Socket=function(q,side=0){if(q.key!=='rook')return ER28.base.socket.apply(this,arguments);const a=q.rfHeading??Math.PI/2;
 return{x:q.x+Math.cos(a)*46.5-Math.sin(a)*side*23,y:q.y+Math.sin(a)*46.5+Math.cos(a)*side*23,angle:a};};
roster17Weapon=function(b,p,dt){const count=b._carrier17?.shots||0,out=ER28.base.weapon.apply(this,arguments);
 p.er28Bearing??=Math.PI/2;const target=p.angle??Math.PI/2,d=Math.atan2(Math.sin(target-p.er28Bearing),Math.cos(target-p.er28Bearing));p.er28Bearing+=clamp(d,-dt*1.8,dt*1.8);
 if(p.phase==='fire')p.er28Bearing=target;
 if(p.kind==='gun'&&(b._carrier17?.shots||0)>count){const m=roster17Muzzle(b,p);wm26Emit(b,m.x,m.y,p.muzzleAngle??target,'chaingun',null,{size:30,life:.12});}
 return out;};
roster17Muzzle=function(b,p){if(!p||!['laser','gun'].includes(p.kind))return ER28.base.muzzle.apply(this,arguments);
 const q=roster17Mount(b,p),a=p.muzzleAge<.14?p.muzzleAngle:p.er28Bearing??p.angle??Math.PI/2,k=roster17HullScale(b),reach=p.kind==='laser'?29.6875*k:15*k;
 return{x:q.x+Math.cos(a)*reach,y:q.y-(p.kind==='laser'?4.1875*k:0)+Math.sin(a)*reach};};
roster17Draw=function(b,C=b._carrier17){if(C.depth||C.scale!==1)return ER28.base.carrier.apply(this,arguments);
 const parts=C.parts,get=XART.get;C.parts=parts.filter(p=>!['gun','laser'].includes(p.kind));
 XART.get=function(k){const key='clean_'+k,a=ER28_ART[key];return a&&get.call(XART,a.key)?get.call(XART,a.key):get.apply(XART,arguments);};
 try{ER28.base.carrier.call(this,b,C);}finally{C.parts=parts;XART.get=get;}
 for(const p of parts.filter(p=>['gun','laser'].includes(p.kind))){const q=roster17Mount(b,p);if(p.dead)continue;
 const a=p.muzzleAge<.14?p.muzzleAngle:p.er28Bearing??p.angle??Math.PI/2,f=er28Dir(a-Math.PI/2)+(p.phase==='fire'?Math.floor((p.t||0)*30)%4:0)*64;
 if(p.kind==='laser')er28Blit('carrier_turret',f,q.x,q.y-4.1875*1.45,p.flash>0);
 else er28Blit('hull_gun_'+p.hullGun,f,q.x,q.y,p.flash>0);
 if(p.phase==='tell'){const m=roster17Muzzle(b,p);combatWarningDraw(p,{...m,ex:m.x+Math.cos(a)*VH*1.4,ey:m.y+Math.sin(a)*VH*1.4,width:p.kind==='laser'?30:20,progress:p.t/(p.kind==='laser'?1.12:roster17GunConfig().warm),fieldOnly:true});}
 if(p.kind==='laser'&&p.phase==='fire'){const m=roster17Muzzle(b,p),open=clamp(Math.min(p.t/.1,(.62-p.t)/.12),0,1);if(open>0)av3Beam(ctx,m.x,m.y,a,900,(14+target17Rank()*2)*1.45*open,'ice',b.t);}
 }
};
