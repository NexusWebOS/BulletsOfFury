"use strict";
/* Two warned strafing axes, reversing gun/missile orbits and a top bomber pass.
   Existing helicopter modules and authored projectiles retain their owners. */
const H21={base:{start:v18StartAttack,tick:v18AttackTick,warn:v18Warnings,rig:v18Rig,ports:v18Ports,draw:r30DrawBoss,contact:target17BossContact,clear:v18Clear,load:stageLoadBegin},events:[]};
stageLoadBegin=function(n,keys){if(n===8)for(const cue of ['atomicLaunch','atomicDetonate','enemyMachineGunLight','bossWeaponCharge'])Snd.prepare(cue);return H21.base.load.call(this,n,n===8?[...(keys||[]),'hm17_missile']:keys);};
function h21Own(b){return v18Owned(b)&&j3State(b).encounter===2&&b._r30.v18.form===1;}
function h21Action(b){const p=b?._r30?.v18?.attack;return p?._h21?p:null;}
function h21Point(u,v){return{x:camLeftX()+viewW()*u,y:viewTopY()+viewH()*v};}
function h21Start(b,type){const N=b._r30.v18,rank=b20Rank(),tell=[1.40,1.2,1.05,.92][rank],choice=type||['cross','plus','orbit','atomicPass'][N.seq++%4],P={_h21:true,type:choice,t:0,tell,active:0,next:0,msl:0,n:0,origin:{x:b.x,y:b.y},target:b20Target(b),scale:1,bank:0,hit:new Set(),dir:Math.random()<.5?-1:1};
 if(choice==='cross'||choice==='plus'){P.segment=[2.10,1.90,1.70,1.55][rank];P.active=P.segment*2+1.05;P.routes=choice==='cross'?[[h21Point(-.3,-.25),h21Point(1.3,1.2)],[h21Point(1.3,-.25),h21Point(-.3,1.2)]]:[[h21Point(-.3,.40),h21Point(1.3,.40)],[h21Point(.5,-.3),h21Point(.5,1.25)]];}
 if(choice==='orbit'){P.orbitTime=[3.4,3.0,2.7,2.4][rank];P.active=P.orbitTime*2+.85;P.center=h21Point(.5,.38);P.rx=viewW()*.32;P.ry=viewH()*.23;}
 if(choice==='atomicPass'){P.active=2.7+[2.6,2.4,2.2,2.0][rank]*[2,2,3,3][rank];P.bombs=[];P.dropped=0;P.radius=Math.max(220,viewW()*.46);P.spacing=[2.6,2.4,2.2,2.0][rank];}
 if(P.routes&&P.dir<0)P.routes=P.routes.slice().reverse().map(([a,z])=>[z,a]);
 N.attack=P;b._r30.attack=P;b20Cue(choice==='atomicPass'?'atomicLaunch':'bossWeaponCharge');b20Log('heli-tell',{type:choice,tell,dir:P.dir});return P;}
v18StartAttack=function(b){if(h21Own(b))return h21Start(b);return H21.base.start.apply(this,arguments);};
function h21Fire(b,P,u,missiles=false){const rank=b20Rank(),ports=v18Ports(b);if(u>=P.next){P.next=u+[.30,.24,.20,.17][rank];P.muzzleUntil=P.t+.075;for(const p of ports){const angle=Math.atan2(P.target.y-p.y,P.target.x-p.x);const q=eShootT(p.x,p.y,angle,4.1+rank*.25,'mg',{w:5,h:12});if(q){q._v18Owner=b;q._h21=true;}b._r30.v18.shots=(b._r30.v18.shots||0)+1;}b20Cue('enemyGun');}
 if(missiles&&u>=P.msl){P.msl=u+[1.05,.95,.85,.75][rank];for(const p of ports){v18Shot(b,p,Math.atan2(P.target.y-p.y,P.target.x-p.x),2.5+rank*.15,'missile',true);}b20Cue('missile');}}
v18AttackTick=function(b,dt){const P=h21Action(b);if(!h21Own(b)||!P)return H21.base.tick.apply(this,arguments);P.t+=dt;const u=P.t-P.tell,N=b._r30.v18;b._noHit=false;combatWarningTick(b,'h21-'+N.seq,Math.min(P.t,P.tell),P.tell);if(u<0)return;
 if(P.type==='cross'||P.type==='plus'){let index=u<P.segment?0:u<P.segment+1.05?-1:1;if(index<0){const w=clamp((u-P.segment)/1.05,0,1),from=P.routes[0][1],to=P.routes[1][0];b.x=lerp(from.x,to.x,w);b.y=lerp(from.y,to.y,w);P.scale=.28;b._noHit=true;}else{const t=index?u-P.segment-1.05:u,v=clamp(t/P.segment,0,1),[from,to]=P.routes[index];b.x=lerp(from.x,to.x,v);b.y=lerp(from.y,to.y,v);P.scale=.8+Math.sin(v*Math.PI)*.25;P.bank=Math.sin(v*TAU)*.13;if(v>.1&&v<.90)h21Fire(b,P,u);}}
 else if(P.type==='orbit'){const gap=.85,second=u>=P.orbitTime+gap,phase=second?u-P.orbitTime-gap:u;
  if(u>=P.orbitTime&&u<P.orbitTime+gap){P.scale=.48;b._noHit=true;if(!P.reversal){P.reversal=true;P.target=b20Target(b);b20Cue('bossWeaponCharge');b20Log('heli-orbit-reverse',{from:P.dir,to:-P.dir});}}
  else{const sign=second?-P.dir:P.dir,a=-Math.PI/2+sign*clamp(phase/P.orbitTime,0,1)*TAU;b.x=P.center.x+Math.cos(a)*P.rx;b.y=P.center.y+Math.sin(a)*P.ry;P.scale=1;P.bank=sign*.14;h21Fire(b,P,u,true);}}
 else if(P.type==='atomicPass'){if(u<.65){const v=clamp(u/.65,0,1);b.x=P.origin.x;b.y=lerp(P.origin.y,viewTopY()-170,v);P.scale=lerp(1,.25,v);b._noHit=true;}
  else if(u<2.25){const v=(u-.65)/1.6;b.x=lerp(P.dir>0?camLeftX()-180:camRightX()+180,P.dir>0?camRightX()+180:camLeftX()-180,v);b.y=viewTopY()+56;P.scale=1.1;P.bank=P.dir*.13;const count=[2,2,3,3][b20Rank()];
   while(P.dropped<count&&v>=(P.dropped+.35)/count){const i=P.dropped++,target=h21Point(i%2?.72:.28,.66),warn=P.spacing*(i+1),q=groundTargetingSpawn({kind:'missile',x:target.x,y:target.y,warn,active:.45,radius:P.radius,size:P.radius*2,track:false,lane:false,owner:b,sound:'atomicDetonate',shake:12,onImpact:q=>{explode(q.x,q.y,q.radius*2,'purple');b20Log('heli-atomic-impact',{radius:q.radius});}});q._h21Atomic=true;q._h21Origin={x:b.x,y:b.y+35};P.bombs.push(q);b20Cue('atomicLaunch');b20Log('heli-atomic-drop',{radius:P.radius,target,warn});}}
  else{const v=clamp((u-2.25)/.8,0,1);b.x=lerp(P.dir>0?camRightX()+160:camLeftX()-160,worldWidth()/2,v);b.y=lerp(viewTopY()-160,viewTopY()+viewH()*.26,v);P.scale=lerp(.28,1,v);P.bank=0;b._noHit=v<.75;}
 }
 b._drawY=b.y;if(u>=P.active){b.x=P.origin.x;b.y=P.origin.y;b._drawY=b.y;b._noHit=false;N.attack=null;b._r30.attack=null;b._r30.cd=[1.0,.8,.65,.5][b20Rank()];j3State(b).attacks++;b20Log('heli-complete',{type:P.type});}
};
v18Rig=function(b){const rig=H21.base.rig.apply(this,arguments),P=h21Action(b);if(!h21Own(b)||!P)return rig;const scale=P.scale??1,a=P.bank||0,c=Math.cos(a),s=Math.sin(a);
 return rig.map(v=>{const dx=v.ax-b.x,dy=v.ay-b.y,k=v.k*scale,at={x:b.x+(dx*c-dy*s)*scale,y:b.y+(dx*s+dy*c)*scale};return b20Piece(v.p,v.a,at,(v.rot||0)+a,k,v.layer||v.p.id,v.z||1);});};
v18Ports=function(b){if(!h21Own(b))return H21.base.ports.apply(this,arguments);const rig=v18Rig(b),out=[];for(const side of ['left','right']){const v=rig.find(v=>v.p.id===side);if(v&&!v.p.destroyed)for(const xy of side==='left'?[[52,212],[72,212]]:[[248,212],[268,212]])out.push({...v19WorldPoint(v,xy),module:side});}return out;};
v18Warnings=function(b){const P=h21Action(b);if(!h21Own(b)||!P)return H21.base.warn.apply(this,arguments);const u=P.t-P.tell;if(u<0){if(P.routes)for(const [a,z]of P.routes)b20Field(b,a,z,80,P.t/P.tell);else if(P.type==='orbit')b20Reticle(P.center.x,P.center.y,viewW()*.34,P.t/P.tell);else b20Field(b,h21Point(0,.12),h21Point(1,.12),78,P.t/P.tell);}else if(P.type==='orbit'&&u>=P.orbitTime&&u<P.orbitTime+.85)b20Reticle(P.center.x,P.center.y,viewW()*.34,(u-P.orbitTime)/.85);};
target17BossContact=function(b){if(h21Own(b))return false;return H21.base.contact.apply(this,arguments);};
r30DrawBoss=function(b){const result=H21.base.draw.apply(this,arguments),P=h21Action(b);if(!h21Own(b)||!P)return result;
 if(P.t<(P.muzzleUntil||0))for(const m of v18Ports(b))wm26Draw(ctx,'chaingun',m.x,m.y,Math.atan2(P.target.y-m.y,P.target.x-m.x),1-(P.muzzleUntil-P.t)/.075,42);
 for(const q of P.bombs||[])if(!q.dead&&!q.impact){const u=clamp(q.t/q.warn,0,1),x=lerp(q._h21Origin.x,q.x,u),y=lerp(q._h21Origin.y,q.y,u);if(XART.rdy('hm17_missile')){const a=HM17_ART.missile,k=(.34+u*.18);ctx.save();ctx.translate(x,y);ctx.rotate(Math.PI);ctx.imageSmoothingEnabled=false;ctx.drawImage(xartTint(a.key,'#9b53df',.42),-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();}}return result;};
v18Clear=function(b){if(h21Own(b))groundTargetingCancel(b);return H21.base.clear.apply(this,arguments);};
globalThis.BOF_HELICOPTER_ASSAULT={state:H21,start:h21Start};
