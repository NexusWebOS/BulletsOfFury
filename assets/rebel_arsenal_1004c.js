'use strict';
/* October 4: pilot-attached readouts, survivor radio and personal dogfight arsenals. */
const RA4_BASE={init:rg4Init,warm:rg4Warm,attack:rg4Attack,attackTick:rg4AttackTick,tick:rebelSquadTick,
 ordTick:rg4OrdnanceTick,ordDraw:rg4OrdnanceDraw,ship:fr27RebelDrawShip,warning:rg4Warning,
 projectile:drawCombatFinalProjectile,wing:s6WingDraw,player:drawPlayer,scene:rg4RescueStart,world:drawWorld};
const RA4={bars:[],badges:[],events:[],cache:new Map()};
const RA4_ROLES={voss:'turbo',nyx:'cloak',rook:'slug',kaia:'rockets',jace:'helix'};
const RA4_COLORS={voss:'#ff48bd',nyx:'#69d9ff',rook:'#ffbd50',kaia:'#39e6c5',jace:'#ff792b'};
Object.assign(RG4_COLORS,RA4_COLORS);
const RA4_NAMES={turbo:'TURBO OVERDRIVE',cloak:'GHOSTKNIFE CLOAK',slug:'.50 CAL SLUGS',rockets:'TWIN ROCKET RACK',helix:'HELIX NOVA',ram:'CHARGE DASH',fusion:'FUSION CANNON',missiles:'MISSILE VOLLEY'};
for(const [n,s] of Object.entries(RA4_ART.sheets))XART._src['ra4_'+n]=s.path;
for(const p of Object.values(RA4_ART.palette))XART._src[p.key]=p.path;
function ra4Alive(q){return !!(q&&!q.dead&&q.hp>0);}
function ra4Image(name,white=false){const cacheKey=name+(white?'-white':'');if(RA4.cache.has(cacheKey))return RA4.cache.get(cacheKey);const r=RA4_ART.cells[name];if(!r||!XART.rdy('ra4_ui'))return null;
 const im=white?xartTint('ra4_ui','#ffffff',1):XART.get('ra4_ui');if(!im)return null;
 const c=document.createElement('canvas');c.width=r[2];c.height=r[3];c.getContext('2d').drawImage(im,...r,0,0,r[2],r[3]);RA4.cache.set(cacheKey,c);return c;}
function ra4Blit(im,x,y,w,h=w,rot=0,alpha=1){if(!im)return false;ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=alpha;ctx.translate(x,y);ctx.rotate(rot);ctx.drawImage(im,-w/2,-h/2,w,h);ctx.restore();return true;}
function ra4Reel(name,f,x,y,w,h=w,rot=0){if(!XART.rdy('ra4_fx'))return;const r=RA4_ART.reels[name][clamp(f|0,0,5)];ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(x,y);ctx.rotate(rot);ctx.drawImage(XART.get('ra4_fx'),...r,-w/2,-h/2,w,h);ctx.restore();}
function ra4Palette(key){return XART.rdy('ra4_'+key)?XART.get('ra4_'+key):null;}
rg4Warm=function(){RA4_BASE.warm();for(const n of ['ui','fx'])XART.rdy('ra4_'+n);for(const p of Object.values(RA4_ART.palette))XART.rdy(p.key);
 for(const k of S6_PILOTS){XART.rdy(specialArtKey('spicon_'+k));XART.rdy(specialArtKey('special_'+k));}for(let i=4;i<6;i++)XART.rdy('arch_blaster_fx_'+i);};
rg4Init=function(b){const G=RA4_BASE.init(b);if(G.arsenal1004c)return G;G.arsenal1004c=true;G.novaFx=[];G.rebelBoxes=[];
 for(const q of b._rebels.ships){const A=q.rg4;A.role=RA4_ROLES[q.key];A.gunCd=.65+q.i*.42;A.gunN=0;A.badge=0;A.serial=0;A.trace=[];A.cd=1.4+q.i*1.65;}
 return G;};
function ra4Targets(){const out=[];for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out)out.push({key:_pilotKey(),ref:player,seat});});
 for(const q of s6Wing?.ships||[])if(q.hp>0&&q.phase!=='leave'&&!out.some(t=>t.key===q.key))out.push({key:q.key,ref:q});return out;}
function ra4Target(q,n=0){const targets=ra4Targets();return targets[(q.i+n)%Math.max(1,targets.length)]||{ref:player,key:_pilotKey()};}
function ra4Log(G,event,data={}){rg4Log(G,event,data);RA4.events.push({event,...data});if(RA4.events.length>150)RA4.events.shift();}
function ra4Gun(q,G,dt){const M=q.rg4;if(!ra4Alive(q)||G.scene||q.stun>0||['turbo','ram'].includes(M.act?.kind))return;
 M.gunCd-=dt;if(M.gunCd>0)return;M.gunCd=diffKey==='easy'?1.25:G.gang?.62:.9;
 const target=ra4Target(q,M.gunN++),a=Math.atan2(target.ref.y-q.y-28,target.ref.x-q.x),side=M.gunN%2?1:-1;
 const z=rg4Round({x:q.x+side*18,y:q.y},a,3.7,'s6tracer',{_ra4Gun:true,_ra4Slug:q.key==='rook',owner:q});q._ra4GunFlash=.1;
 wm26Emit?.(q,z.x,z.y-12,a,q.key==='rook'?'chaingun':'mg',null,{size:20,life:.1});
 (q.key==='rook'?Audio.SFX.enemyMachineGunHeavy:Audio.SFX.enemyShoot)?.();
}
function ra4AttackKind(q,G){const n=q.rg4.serial++;if(q.key==='voss')return n%3===1?'fusion':'turbo';if(q.key==='rook')return n%3===2?'ram':'slug';
 if(q.key==='jace')return n%3===2?'ram':'helix';return RA4_ROLES[q.key];}
function ra4Supply(q,G){const M=q.rg4;if(M.supply&&!M.supply.dead)return;
 const kind=ra4AttackKind(q,G),o={owner:q,key:q.key,kind,x:clamp(q.x+(q.i%2?42:-42),camLeftX()+30,camRightX()-30),y:clamp(q.y+70,PLAY.y+85,VH-170),w:34,h:34,r:17,hp:6,max:6,t:0,flash:0,dead:false};
 M.supply=o;G.rebelBoxes.push(o);M.cd=.5;ra4Log(G,'personalBoxDrop',{pilot:q.key,kind});}
function ra4BoxHit(G,o,dmg){if(o.dead||G.scene||!(dmg>0))return false;o.hp=Math.max(0,o.hp-dmg);o.flash=.14;
 if(o.hp<=0){o.dead=true;o.owner.rg4.supply=null;o.owner.rg4.cd=4.0;explode(o.x,o.y,32,'blue');Audio.SFX.expSmall?.();ra4Log(G,'personalBoxDestroyed',{pilot:o.key});}else av3Sound('impact_metal',.55,.1);return true;}
function ra4SupplyTick(G,dt){if(G.scene){for(const o of G.rebelBoxes)o.dead=true;G.rebelBoxes=[];for(const q of boss?._rebels?.ships||[])q.rg4.supply=null;return;}
 for(const o of G.rebelBoxes){if(o.dead)continue;if(!ra4Alive(o.owner)){o.dead=true;continue;}o.t+=dt;o.flash=Math.max(0,o.flash-dt);
  for(const p of pBullets){if(p.dead)continue;const beam=p.kind==='beam'?playerBeamRange(p):null,hit=p.kind==='firewhip'?fireWhipTouches(p,o,p.t/p.duration,p.t/p.duration):beam?o.y+o.r>=beam.top&&o.y-o.r<=beam.bot&&Math.abs(o.x-beam.x)<o.r+beam.half:Math.abs(p.x-o.x)<o.r+(p.w||4)/2&&Math.abs(p.y-o.y)<o.r+(p.h||8)/2;
   if(hit){if(beam&&G.age<(o.nextBeam||0))continue;if(beam)o.nextBeam=G.age+.12;ra4BoxHit(G,o,p.dmg||2);if(!beam&&!p.pierce)p.dead=true;if(o.dead)break;}}
  if(o.dead)continue;const q=o.owner;q.x+=clamp(o.x-q.x,-dt*240,dt*240);q.y+=clamp(o.y-q.y,-dt*240,dt*240);
  if(Math.hypot(q.x-o.x,q.y-o.y)<19){o.dead=true;q.rg4.supply=null;q.rg4.armed=o.kind;q.rg4.cd=0;Audio.SFX.powerup?.();ra4Log(G,'personalBoxCollected',{pilot:q.key,kind:o.kind});}
 }
 G.rebelBoxes=G.rebelBoxes.filter(o=>!o.dead);}
rg4Attack=function(q,R,G,forced){if(!G.arsenal1004c)return RA4_BASE.attack.apply(this,arguments);
 if(!forced&&!q.rg4.armed){ra4Supply(q,G);return;}
 const kind=forced||q.rg4.armed;if(!Object.values(RA4_ROLES).includes(kind)&&kind!=='ram'){q.rg4.armed=null;return RA4_BASE.attack(q,R,G,kind);}
 if(['turbo','ram','helix'].includes(kind)&&R.ships.some(v=>v!==q&&ra4Alive(v)&&['turbo','ram','helix','fusion'].includes(v.rg4.act?.kind))){q.rg4.cd=.6;return;}
 const M=q.rg4,target=ra4Target(q,M.serial),ref=target.ref,warm=({turbo:1.35,ram:1.25,slug:1.0,rockets:1.75,helix:2.0,cloak:1.15})[kind]*(diffKey==='easy'?1.3:1);M.armed=null;
 M.n++;M.act={kind,phase:'charge',t:0,warm,target,tx:ref.x,ty:ref.y,a:Math.atan2(ref.y-q.y,ref.x-q.x),shot:0,cd:0,cycle:0};M.badge=1.35;q.evadeT=0;q.frSomersault=false;
 if(kind==='rockets')M.act.locked=M.serial%2===1;
 if(kind==='cloak'){q.frCloak=10;rg4FX(G,2,q.x,q.y,90,.55);av3Sound('teleport_out',.7);}
 combatWarningTick(q,'ra4-'+M.n,0,warm);av3Sound(kind==='helix'?'laser_charge':'target_acquire',.65,.3);
 G.releaseAt=G.age+(diffKey==='easy'?1.8:1.15);ra4Log(G,'specialStart',{pilot:q.key,kind});
};
function ra4DashSetup(q,A){const target=A.target.ref;
 A.tx=clamp(target.x,camLeftX()+30,camRightX()-30);A.ty=clamp(target.y,PLAY.y+80,VH-65);
 A.a=Math.atan2(A.ty-q.y,A.tx-q.x);A.ox=q.x;A.oy=q.y;A.distance=Math.min(620,Math.hypot(A.tx-q.x,A.ty-q.y)+125);A.travel=0;A.hit=new Set();q.rfHeading=A.a;
}
function ra4RamHit(q,A){for(const t of ra4Targets()){if(A.hit.has(t.ref)||Math.hypot(t.ref.x-q.x,t.ref.y-q.y)>35)continue;A.hit.add(t.ref);
 if(t.seat)withSeat(t.seat,()=>playerHit('rebel charge dash'));
 else if(t.ref.canBeHit&&!t.ref.hurtT){t.ref.hp=Math.max(0,t.ref.hp-1);t.ref.hurtT=1;explode(t.ref.x,t.ref.y,36,'blue');if(!t.ref.hp){t.ref.phase='leave';t.ref.t=0;}}
}}
function ra4Rocket(q,G,A){const side=A.shot%2?-1:1,x=q.x+side*27,y=q.y+42,target=A.target.ref;
 const a=A.locked?Math.atan2(target.y-y,target.x-x):Math.PI/2+Math.sin(A.shot*1.8+q.i)*.46;
 const z={x,y,vx:Math.cos(a)*3.0,vy:Math.sin(a)*3.0,ang:a,spd:3.0,w:14,h:32,kind:'emissile',hp:2,_shootable:true,homing:false,t:0,
 _rg4:true,_boss:true,_noArsenal:true,_ra4Rocket:true,owner:q,lock:A.locked?A.target:null,commit:false,side};eBullets.push(z);
 q.rg4.launchSide=side;q.rg4.launchFlash=.2;Audio.SFX.missile?.();av3Sound('laser_release',.45,.18);ra4Log(G,'rocketLaunch',{pilot:q.key,side,locked:A.locked});
}
function ra4Helix(q,G,A){G.ord.push({kind:'helix',owner:q,x:q.x,y:q.y+48,vx:Math.cos(A.a)*155,vy:Math.sin(A.a)*155,r:22,hp:14,max:14,t:0,life:1.35,burst:false,split:true,flash:0});
 (Audio.SFX.maverickHelixRelease||Audio.SFX.helixBurst)?.();ra4Log(G,'helixRelease',{pilot:q.key});}
function ra4Nova(G,o){if(o.burst)return;o.burst=true;o.dead=true;G.novaFx.push({x:o.x,y:o.y,t:0,dur:.55});
 for(let i=0;i<8;i++){const a=i*TAU/8;const z=eShootT(o.x+Math.cos(a)*18,o.y+Math.sin(a)*18,a,diffKey==='easy'?2.65:3.6,'s6orb',{w:14,h:14,silent:true});
  Object.assign(z,{_ra4MiniBall:true,_rg4:true,_noArsenal:true,_boss:true,owner:o.owner});}
 av3Sound('impact_energy',.9);Audio.SFX.helixBurst?.();ra4Log(G,'helixNova',{count:8});}
rg4AttackTick=function(q,R,G,dt){const M=q.rg4,A=M.act;if(!G.arsenal1004c||!A||!['turbo','ram','slug','rockets','helix','cloak'].includes(A.kind))return RA4_BASE.attackTick.apply(this,arguments);
 A.t+=dt;const kind=A.kind;if(A.phase==='charge'){
  if(A.t<A.warm*.65){const p=A.target.ref;A.tx=p.x;A.ty=p.y;A.a=Math.atan2(p.y-q.y,p.x-q.x);}
  combatWarningTick(q,'ra4-'+M.n,Math.min(A.t,A.warm-.001),A.warm);
  if(kind==='cloak')q.frCloak=10;
  if(A.t<A.warm)return;A.phase='fire';A.t=0;A.cd=0;ra4Log(G,'specialRelease',{pilot:q.key,kind});
  if(kind==='turbo'||kind==='ram'){ra4DashSetup(q,A);Audio.SFX.chargeDash?.();av3Sound('teleport_in',.8);}
  if(kind==='helix')ra4Helix(q,G,A);
 }
 if(A.phase==='fire'){
  if(kind==='turbo'||kind==='ram'){
   const speed=diffKey==='easy'?580:780,step=speed*dt;A.travel+=step;q.x=A.ox+Math.cos(A.a)*A.travel;q.y=A.oy+Math.sin(A.a)*A.travel;
   M.trace.push({x:q.x,y:q.y,a:A.a,t:0});if(M.trace.length>9)M.trace.shift();ra4RamHit(q,A);
   if(A.travel>=A.distance){A.cycle++;if(kind==='turbo'&&A.cycle<(G.gang?4:3)){
    const dir=A.cycle%2?1:-1;q.x=dir>0?camLeftX()-64:camRightX()+64;q.y=clamp(A.target.ref.y+(A.cycle%2?32:-32),PLAY.y+145,VH-80);
    A.tx=dir>0?camRightX()+80:camLeftX()-80;A.ty=q.y;A.a=dir>0?0:Math.PI;A.ox=q.x;A.oy=q.y;A.distance=viewW()+150;A.travel=0;A.phase='row';A.t=0;A.warm=diffKey==='easy'?1.3:1.0;A.hit=new Set();q.rfHeading=A.a;
   }else{A.phase='recover';A.t=0;}}
  }
  if(kind==='slug'){A.cd-=dt;if(A.cd<=0&&A.shot<(G.gang?20:14)){A.cd=G.gang?.10:.13;const side=A.shot++%2?1:-1,p={x:q.x+side*23,y:q.y+16};
   rg4Round(p,A.a+Math.sin(A.shot*.71)*.06,4.9,'s6tracer',{_ra4Slug:true,owner:q});q._rg4Muzzle=.11;Audio.SFX.enemyMachineGunHeavy?.();}}
  if(kind==='rockets'){A.cd-=dt;if(A.cd<=0&&A.shot<(G.gang?6:4)){A.cd=diffKey==='easy'?.6:.42;ra4Rocket(q,G,A);A.shot++;}}
  if(kind==='cloak'){q.frCloak=10;q.x=clamp(q.x+Math.sin(G.age*2.4+q.i)*dt*95,camLeftX()+52,camRightX()-52);
   A.cd-=dt;if(A.cd<=0){A.cd=.55+Math.random()*.25;const p=A.target.ref,a=Math.atan2(p.y-q.y,p.x-q.x);rg4Round(q,a+rnd(-.16,.16),3.8,'s6tracer',{_ra4Ghost:true,owner:q});Audio.SFX.enemyShoot?.();}}
  const end=({slug:G.gang?2.25:2.0,rockets:G.gang?2.7:1.95,helix:1.4,cloak:G.gang?6.5:5.2})[kind];if(end&&A.t>=end){A.phase='recover';A.t=0;if(kind==='cloak'){q.frCloak=0;rg4FX(G,2,q.x,q.y,90,.55);av3Sound('teleport_in',.7);}}
 }else if(A.phase==='row'){
  combatWarningTick(q,'ra4-row-'+A.cycle,Math.min(A.t,A.warm-.001),A.warm);if(A.t>=A.warm){A.phase='fire';A.t=0;Audio.SFX.chargeDash?.();}
 }else if(A.phase==='recover'){
  q.frCloak=0;q.rfHeading=null;const x=camLeftX()+viewW()/2+(q.i-2)*Math.min(82,(viewW()-112)/4),y=PLAY.y+83+(q.i%2)*46;
  q.x+=clamp(x-q.x,-dt*330,dt*330);q.y+=clamp(y-q.y,-dt*330,dt*330);
  if(A.t>.9){M.act=null;M.cd=({turbo:7.0,ram:5.2,slug:4.3,rockets:5.2,helix:5.4,cloak:3.0})[kind]*(G.gang?.82:diffKey==='easy'?1.2:1);}
 }
};
rebelSquadTick=function(b,dt){const r=RA4_BASE.tick.apply(this,arguments),G=b._rebels?.gang1004;if(!G?.arsenal1004c||b.dead)return r;
 for(const q of b._rebels.ships){const M=q.rg4;if(!M)continue;M.badge=Math.max(0,M.badge-dt);M.launchFlash=Math.max(0,(M.launchFlash||0)-dt);q._ra4GunFlash=Math.max(0,(q._ra4GunFlash||0)-dt);
  for(const t of M.trace)t.t+=dt;M.trace=M.trace.filter(t=>t.t<.2);ra4Gun(q,G,dt);
  if(!ra4Alive(q)){M.act=null;q.frCloak=0;q.rfHeading=null;}
 }
 ra4SupplyTick(G,dt);return r;};
rg4OrdnanceTick=function(b,G,dt){if(!G.arsenal1004c)return RA4_BASE.ordTick.apply(this,arguments);
 for(const o of G.ord)if(o.kind==='helix'&&!o.dead){if(o.owner.dead){o.dead=true;continue;}
  if(o.t+dt>=o.life||ra4Targets().some(q=>Math.hypot(q.ref.x-o.x,q.ref.y-o.y)<o.r+12)){ra4Nova(G,o);}
 }
 const r=RA4_BASE.ordTick.apply(this,arguments);for(const f of G.novaFx)f.t+=dt;G.novaFx=G.novaFx.filter(f=>f.t<f.dur);return r;
};
const RA4_UPDATE=updatePlay;
updatePlay=function(dt){const G=rg4State();if(G?.arsenal1004c&&!G.scene)for(const p of eBullets){if(p.dead||!p._ra4Rocket)continue;
 if(p.t>4.2){p.dead=true;continue;}if(p.lock&&!p.commit){const target=p.lock.ref,dx=target.x-p.x,dy=target.y-p.y;
  if(Math.hypot(dx,dy)<115||p.t>.9)p.commit=true;else{const a=Math.atan2(p.vy,p.vx),goal=Math.atan2(dy,dx),da=((goal-a+Math.PI*3)%TAU)-Math.PI,next=a+clamp(da,-dt*1.25,dt*1.25);p.spd=Math.min(5.0,p.spd+dt*2);p.vx=Math.cos(next)*p.spd;p.vy=Math.sin(next)*p.spd;p.ang=next;}}
 }return RA4_UPDATE.apply(this,arguments);};
function ra4BarPose(q){const im=XART.rdy('rr_ship_'+REBEL_SHIPS[q.i])?XART.get('rr_ship_'+REBEL_SHIPS[q.i]):null,h=im?SHIP_DRAW_H*1.5*im.height/im.width:85;
 return{x:q.x,y:q.y-h*.5-14,w:62,visible:ra4Alive(q)&&!q.frCloak&&q.x>camLeftX()-25&&q.x<camRightX()+25&&q.y>PLAY.y+15&&q.y<VH+20};}
rg4HealthBars=function(b){RA4.bars=[];for(const q of b._rebels.ships){const P=ra4BarPose(q);if(!P.visible)continue;RA4.bars.push({pilot:q.key,...P,hp:q.hp,max:q.max});
 const im=ra4Image('icon_'+q.key);ra4Blit(im,P.x-P.w/2-9,P.y,16,16);
 ctx.save();ctx.fillStyle='#030810';ctx.fillRect(P.x-P.w/2-1,P.y-1,P.w+2,7);ctx.fillStyle='#34404d';ctx.fillRect(P.x-P.w/2,P.y,P.w,5);ctx.fillStyle=RA4_COLORS[q.key];ctx.fillRect(P.x-P.w/2,P.y,P.w*clamp(q.hp/q.max,0,1),5);ctx.restore();campText(q.key.toUpperCase(),P.x,P.y-7,7,'#edf6ff');
 }};
function ra4LockWarning(A){if(!A.locked)return;const p=A.target.ref,f=Math.floor(A.t*11)%4,im=retinaTinted(A.t/A.warm>.8?'retB':'retA',f,'yuri');
 ra4Blit(im,p.x,p.y,46,46);}
rg4Warning=function(q,A){if(!['turbo','ram','slug','rockets','helix','cloak'].includes(A.kind))return RA4_BASE.warning.apply(this,arguments);
 if(!['charge','row'].includes(A.phase)||A.kind==='cloak')return;const p=clamp(A.t/A.warm,0,1);
 const row=A.phase==='row',x=row?A.ox:q.x,y=row?A.oy:q.y,ex=row?A.tx:x+Math.cos(A.a)*600,ey=row?A.ty:y+Math.sin(A.a)*600;
 if(row){ctx.save();ctx.beginPath();ctx.rect(camLeftX(),y-31,viewW(),62);ctx.clip();}
 combatWarningDraw(q,{x,y,ex,ey,len:row?Math.abs(ex-x):undefined,width:['turbo','ram'].includes(A.kind)?55:A.kind==='helix'?48:26,progress:p,fieldOnly:true});
 if(row)ctx.restore();
 const key='bmfx_alert_'+l23FovPhase(p)+'_impact_imminent';if(XART.rdy(key))ra4Blit(XART.get(key),row?camLeftX()+viewW()/2:q.x,row?y:q.y+40,30,30);
 if(A.kind==='rockets')ra4LockWarning(A);
};
fr27RebelDrawShip=function(q){const G=rg4State(),A=q.rg4?.act;if(!G?.arsenal1004c)return RA4_BASE.ship.apply(this,arguments);
 const cloak=q.frCloak>0;if(cloak){const key='rr_ship_'+REBEL_SHIPS[q.i],im=XART.rdy(key)?XART.get(key):null,w=SHIP_DRAW_H*1.5,h=im?w*im.height/im.width:80;
  ra4Blit(im,q.x,q.y,w,h,0,.055+.035*Math.sin(G.age*9));rg4Cell(1,Math.floor(G.age*10)%6,q.x,q.y,w*.95,h,.12);
  if(q.flash>0)ra4Blit(xartTint(key,'#ffffff',1),q.x,q.y,w,h,0,Math.min(1,q.flash*9));
 }else RA4_BASE.ship.apply(this,arguments);
 if(q.dead)return;
 for(const t of q.rg4.trace)ra4Reel('dash',Math.floor(G.age*20)%6,t.x-Math.cos(t.a)*40,t.y-Math.sin(t.a)*40,115,34,t.a);
 if(q.key==='kaia')for(const side of [-1,1]){const f=q.rg4.launchFlash>0&&q.rg4.launchSide===side?3:q.rg4.act?.phase==='charge'?1:0;
  ra4Reel('launcher',f,q.x+side*27,q.y+19,22,54);}
 if(A?.kind==='helix'&&A.phase==='charge'){
  const p=clamp(A.t/A.warm,0,1),im=ra4Palette('fchgc_'+Math.min(3,Math.floor(p*4)));ra4Blit(im,q.x,q.y,102,130);
  ra4Blit(ra4Palette('nhxsb_g_'+Math.min(2,Math.floor(p*3))),q.x,q.y+42,24+p*28,24+p*28);}
 if(A&&!cloak&&A.phase!=='recover')ra4Blit(ra4Image('box_'+q.key),q.x+46,q.y-24,30,30);
};
rg4OrdnanceDraw=function(o,G){if(o.kind!=='helix')return RA4_BASE.ordDraw.apply(this,arguments);
 const im=ra4Palette('nhxsb_g_'+(1+Math.floor(G.age*12)%2));ra4Blit(im,o.x,o.y,o.r*2.25,o.r*2.25,G.age*2);
 if(o.flash>0){const key='ra4_nhxsb_g_2',hot=xartTint(key,'#ffffff',1);ra4Blit(hot,o.x,o.y,o.r*2.25,o.r*2.25,0,Math.min(1,o.flash*7));}
};
drawCombatFinalProjectile=function(p){if(p._ra4Slug)return chaingunRoundDraw(p);if(p._ra4Rocket){ra4Reel('rocket',Math.floor((p.t||0)*18)%6,p.x,p.y,14,40,Math.atan2(p.vy,p.vx)-Math.PI/2);return true;}
 if(p._ra4MiniBall){ra4Blit(ra4Palette('nhxsb_g_'+(1+Math.floor((p.t||0)*16)%2)),p.x,p.y,19,19,(p.t||0)*4);return true;}return RA4_BASE.projectile.apply(this,arguments);};
function ra4FriendlyBadge(key,q,active=false){if(q.dead||q.out||q.hp<=0||q.phase==='leave')return;
 // Existing pilot badges can be atlas cells or loose plates; iconDraw owns both paths.
 if(iconDraw((active?'special_':'spicon_')+key,q.x+22,q.y+34,active?22:16,true))RA4.badges.push({key,x:q.x,y:q.y});}
s6WingDraw=function(){const r=RA4_BASE.wing.apply(this,arguments),G=rg4State();if(!G?.arsenal1004c||G.scene)return r;RA4.badges=[];
 for(const q of s6Wing?.ships||[])ra4FriendlyBadge(q.key,q,q.boostT>0||q.specialT>0);return r;};
drawPlayer=function(){const r=RA4_BASE.player.apply(this,arguments),G=rg4State();if(G?.arsenal1004c&&!G.scene&&!player.dead)ra4FriendlyBadge(_pilotKey(),{...player,hp:1},!!special);return r;};
function ra4Scanner(R){return ['kaia','nyx','jace','rook','voss'].map(k=>R.ships.find(q=>q.key===k&&ra4Alive(q))).find(Boolean);}
rg4RescueStart=function(b,G){if(!G.arsenal1004c)return RA4_BASE.scene.apply(this,arguments);if(G.rescueDone||G.scene||b.dead)return false;const scanner=ra4Scanner(b._rebels);if(!scanner)return false;
 const started=RA4_BASE.scene(b,G);if(!started)return false;G.scanner=scanner.key;
 const alive=b._rebels.ships.filter(ra4Alive),other=alive.find(q=>q!==scanner)||scanner,leader=alive.find(q=>q.key==='voss')||other;
 const scanText={kaia:'LEAVE IT TO THE LADIES TO FIGURE THINGS OUT, YOU SILLY BOYS.',nyx:'LEAVE IT TO THE LADIES TO FIGURE THINGS OUT, YOU SILLY BOYS.',jace:"LEAVE IT TO THE NEW RECRUIT TO SHOW THEM HOW IT'S DONE.",rook:'LET ME SHOW YOU HOW THE BIG BOSS GETS IT DONE.',voss:'JEEZ, DO I GOTTA TEACH YOU GUYS HOW TO DO EVERYTHING AROUND HERE? LOCK ON AND USE THE RADAR HACK!'};
 const revealText={kaia:"WHY IS IT THAT GEEKS NEVER CAN DO THINGS RIGHT?",nyx:"WHY IS IT THAT GEEKS NEVER CAN DO THINGS RIGHT?",jace:'RADAR HACK LOCKED. THERE YOU ARE, DECKER!',rook:'LOCK IS GOOD. INVISIBILITY JUST RAN OUT!',voss:'THERE YOU ARE. THAT IS HOW YOU BREAK A CLOAK!'};
 const lines=G.scene.lines;lines[2].who=leader.key;lines[3].who=other.key;lines[4]={who:scanner.key,text:scanText[scanner.key],event:'scan'};lines[5]={who:scanner.key,text:revealText[scanner.key],event:'reveal'};
 if(scanner.key==='rook'&&alive.some(q=>q.key==='voss'))lines.splice(5,0,{who:'voss',text:'REMEMBER WHO THE ACTUAL BIG BOSS IS HERE, BIG GUY.'});
 if(!['kaia','nyx'].includes(scanner.key)){lines[lines.length-2].text='DECKER, I THINK YOUR EXPERIMENTAL TECH JUST MET ITS MATCH.';lines[lines.length-1].text="IT WORKED UNTIL THEY STARTED TRYING TO KILL ME. THAT COUNTS AS A SUCCESS!";}
 const log=G.events.findLast(e=>e.event==='rescueStart');if(log)log.scanner=scanner.key;ra4Log(G,'scannerChosen',{pilot:scanner.key});return true;
};
const RA4_REBEL_DRAW=rebelSquadDraw;
rebelSquadDraw=function(b){const r=RA4_REBEL_DRAW.apply(this,arguments),G=b._rebels?.gang1004;if(G?.arsenal1004c){for(const f of G.novaFx)ra4Reel('nova',Math.floor(f.t/f.dur*6),f.x,f.y,105,105);
 for(const o of G.rebelBoxes)if(!o.dead){const im=ra4Image('box_'+o.key),y=o.y+Math.sin(o.t*4)*3;ra4Blit(im,o.x,y,34,34);if(o.flash>0)ra4Blit(ra4Image('box_'+o.key,true),o.x,y,34,34,0,Math.min(1,o.flash*9));}}return r;};
const RA4_TARGETS=retinaBossTargets;
retinaBossTargets=function(b){const out=RA4_TARGETS.apply(this,arguments),G=b?._rebels?.gang1004;if(!G?.arsenal1004c||G.scene)return out;
 for(const o of G.rebelBoxes)if(!o.dead){o.id??='ra4-box-'+o.key+'-'+G.age;out.push(retinaDynamicPiece(b,o.id,'support',()=>({x:o.x,y:o.y,hp:o.hp,dead:o.dead}),d=>ra4BoxHit(G,o,d),34,34));}return out;};
rg4Warm();
