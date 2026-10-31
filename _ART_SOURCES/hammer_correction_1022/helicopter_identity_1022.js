"use strict";
/* The corrupted helicopter uses Overlord-X's real controller: hunt/orbit,
   gun sweeps, missile locks, sonic attacks and committed warning/charge runs.
   Its existing breakable corrupted modules remain the visible body. */
const HC22={base:{enter:v18Enter,start:v18StartAttack,tick:v18AttackTick,warn:v18Warnings,rig:v18Rig,clear:v18Clear,mount:ovMount,facing:ovFacingMount,rocket:ovRocketSide,sonic:ovSonicMissileVolley,rotor:ovRotorTempest,canFire:mr27CanFire,green:ovGreenVolley,contact:target17BossContact},events:[]};
function hc22Own(b){return v18Owned(b)&&j3State(b).encounter===2&&b._r30.v18.form===1;}
function hc22Proxy(b){const N=b._r30.v18;if(N._hc22)return N._hc22;
 const D=gd4Create(b,1),p=D.p;p.kind='damkeeper';p._ovInit=null;p._ovFlight='hunt';p.x=b.x;p.y=b.y;p.enter=false;p.dead=false;
 return N._hc22={p,age:0,last:null,states:[],bank:0};
}
v18Enter=function(b,n,form){const r=HC22.base.enter.apply(this,arguments);if(n===2&&form===1){delete b._r30.v18._hc22;hc22Proxy(b);}return r;};
v18StartAttack=function(b){if(!hc22Own(b))return HC22.base.start.apply(this,arguments);
 hc22Proxy(b);const P={type:'native-overlord',t:0,tell:0,active:999};b._r30.v18.attack=P;b._r30.attack=P;return P;
};
v18AttackTick=function(b,dt){if(!hc22Own(b))return HC22.base.tick.apply(this,arguments);const N=b._r30.v18,Q=hc22Proxy(b),p=Q.p;
 Q.age+=dt;p.t+=dt;p.hp=b.hp;p.maxhp=b.maxhp;p.dead=false;p.enter=false;p.flash=b.flash||0;
 const oldX=p.x,first=eBullets.length;updateOverlordX(p,dt);b.x=p.x;b.y=p.y;b._drawY=b.y;b._noHit=!!p._noHit;
 for(let i=first;i<eBullets.length;i++){const q=eBullets[i];q._v18Owner=b;q._hc22Owner=b;}
 Q.bank=clamp((p.x-oldX)/Math.max(.001,dt)/1500,-.20,.20)+(p._pivot||0);
 if(p._ovState!==Q.last){Q.last=p._ovState;Q.states.push(Q.last);HC22.events.push({event:'native-state',state:Q.last,time:Q.age});if(HC22.events.length>120)HC22.events.shift();}
 if(Q.age>42&&p._ovState==='fight'&&V18.forms.filter(i=>j3State(b).hp[i]>0).length>1){N.attack=null;b._r30.attack=null;j3Save(b);j3Morph(b,'home');}
};
v18Warnings=function(b){if(!hc22Own(b))return HC22.base.warn.apply(this,arguments);const p=hc22Proxy(b).p;
 ovRushWarningDraw(p,false);ovSweepSafeDraw(p);if(p._ovSonic)ovSonicWarningDraw(p);
 if(p._ovState==='chargeTell'&&p._chargeTell){const T=p._chargeTell,hub=ovChargeOrigin(p,T),progress=ovChargeWarningProgress(T);combatWarningDraw(b,{x:hub.x,y:hub.y,ex:T.lane,ey:T.dir<0?0:VH,progress,width:42,fieldOnly:true});sx21HeliCharge(p,progress);}
};
v18Rig=function(b){const rig=HC22.base.rig.apply(this,arguments);if(!hc22Own(b))return rig;
 const a=hc22Proxy(b).bank||0,c=Math.cos(a),s=Math.sin(a);return rig.map(v=>{
  const dx=v.ax-b.x,dy=v.ay-b.y;return b20Piece(v.p,v.a,{x:b.x+dx*c-dy*s,y:b.y+dx*s+dy*c},(v.rot||0)+a,v.k,v.layer||v.p.id,v.z||1);
 });
};
v18Clear=function(b){if(hc22Own(b)){const Q=b._r30.v18._hc22;if(Q)Q.p.dead=true;delete b._r30.v18._hc22;}
 return HC22.base.clear.apply(this,arguments);};
function hc22Host(p){const b=p?._gp4Host;return b&&hc22Own(b)?b:null;}
function hc22Mount(b,side,core=false){const v=v18Rig(b).find(v=>v.p.id===(core?'core':side<0?'left':'right')&&!v.p.destroyed);
 return v?v19WorldPoint(v,core?[160,95]:side<0?[52,212]:[268,212]):{x:b.x,y:b.y+45};
}
ovMount=function(p,x,y){const b=hc22Host(p);if(!b)return HC22.base.mount.apply(this,arguments);const q=hc22Mount(b,x<0?-1:1,Math.abs(x)<15);return[q.x,q.y];};
ovFacingMount=function(p,x,y){const b=hc22Host(p);return b?hc22Mount(b,x<0?-1:1,x===0):HC22.base.facing.apply(this,arguments);};
mr27CanFire=function(p,slot){const b=hc22Host(p);if(!b)return HC22.base.canFire.apply(this,arguments);const side=String(slot).includes('L')?'left':'right';return !!b.parts.find(q=>q.id===side&&!q.destroyed);};
ovRocketSide=function(p,side,fan){const b=hc22Host(p);if(!b)return HC22.base.rocket.apply(this,arguments);if(b.parts.find(q=>q.id===(side<0?'left':'right'))?.destroyed)return;return GD4_BASE.ovRocket.apply(this,arguments);};
ovSonicMissileVolley=function(p,index){const b=hc22Host(p);if(!b)return HC22.base.sonic.apply(this,arguments);if(p.dead||diffKey!=='furious')return;
 for(const side of [-1,1])if(b.parts.some(q=>q.id===(side<0?'left':'right')&&!q.destroyed))for(const spread of [-.12,.12]){
  const m=hc22Mount(b,side),a=Math.PI/2+(p._pivot||0)+side*.18+spread;
  eBullets.push({kind:'s1jungleMissile',_ovSonicMissile:true,_shootable:true,_volley:index,x:m.x,y:m.y,vx:Math.cos(a)*2.3,vy:Math.sin(a)*2.3,ang:a,w:14,h:26,t:0,hp:1,homing:true,turn:.028,spd:2.3,_accel:.045,_maxspd:4.8,_v18Owner:b});
  navalFlash(null,m,.9,S1_MUZZLE_MILITARY,{n:6,hpx:42,life:.2,follow:()=>b.dead||b.parts.find(q=>q.id===(side<0?'left':'right'))?.destroyed?null:hc22Mount(b,side)});
 }stageRevisionCue(p,'overlordRocket',.1);weaponFeedbackSound('colePressureRelease',.45);
};
ovGreenVolley=function(p){const b=hc22Host(p);if(!b)return HC22.base.green.apply(this,arguments);stageRevisionCue(p,'overlordLance',.1);
 for(const [side,offset]of [[-1,-.22],[-1,-.09],[0,0],[1,.09],[1,.22]]){
  if(side&&b.parts.find(q=>q.id===(side<0?'left':'right'))?.destroyed)continue;const m=hc22Mount(b,side,side===0),a=eAimDown(aimPlayer(m.x,m.y)+offset);
  eShootT(m.x,m.y,a,5.65,'s1greenLaser',{owner:b,w:7,h:22,silent:true,impact:'green'});
 }
};
ovRotorTempest=function(p){return hc22Host(p)?GD4_BASE.ovRotor.apply(this,arguments):HC22.base.rotor.apply(this,arguments);};
target17BossContact=function(b,x,y){if(!hc22Own(b))return HC22.base.contact.apply(this,arguments);if(b.dead||b.enter||b._noHit||b._r30.mode!=='fight')return false;return v18Rig(b).some(v=>!v.p.destroyed&&v19AtRect(v,x,y));};
globalThis.BOF_HELICOPTER_IDENTITY=HC22;
