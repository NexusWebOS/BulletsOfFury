"use strict";
/* Final art pass: new authored banks, native combat ownership, bounded effects.
   Never replace the engine's hit/burn/spin/crash/shock-ring death sequence. */
const FV21={base:{touch:XART._touch,shield:drawEnemyShieldLayer,load:stageLoadBegin,
 pose:hb20Pose,carrier:carrierShieldDraw,final:j3FinalDeath,update:updatePlay,world:drawWorld,
 projectile:drawCombatFinalProjectile,get:XART.get,gates:s5RunDraw,gateOut:s5GateOutDraw,portal:wdPortalDraw,wall:hm10Blit,warTick:stage4WarfareTick},fx:[],next:0,clock:0,draws:{},aliases:new Map(),tags:new WeakMap()};
for(const [id,a] of Object.entries(FV21_ART.sheets))XART._src[a.key]=a.path;
for(const B of Object.values(FV21_ART.banks))for(const a of B.frames)BOFX.cells[a.key]=[a.sheet,...a.cell];
const fv21Bank=n=>FV21_ART.banks[n];
function fv21Key(n,t=0,once=false){const B=fv21Bank(n);if(!B)return null;const f=Math.floor(t*B.fps);return B.frames[once?Math.min(B.frames.length-1,f):((f%B.frames.length)+B.frames.length)%B.frames.length]?.key;}
function fv21Frame(n,t,x,y,size,alpha=1,once=false,angle=0,flash=0){const B=fv21Bank(n),key=fv21Key(n,t,once);if(!B||!key||!XART.rdy(key))return false;
 const im=XART.get(key),k=size/Math.max(B.w,B.h);ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(im,-B.pivot[0]*k,-B.pivot[1]*k,B.w*k,B.h*k);if(flash>0){ctx.globalAlpha*=clamp(flash/.12,0,1);ctx.drawImage(xartTint(key,'#ffffff',1),-B.pivot[0]*k,-B.pivot[1]*k,B.w*k,B.h*k);}ctx.restore();FV21.draws[n]=(FV21.draws[n]||0)+1;return true;}
function fv21Alias(key){let name=null,t=efxClock;
 if(/^nfx_s5gate96_\d+$/.test(key))name='portal';
 else if(/^nfx_warp_tunnel_\d+$/.test(key))name='portal_blue';
 else if(/^s4w_lightning_shield_\d+$/.test(key))name='shield_volt';
 else if(/^dr21_shield_main_\d+$/.test(key))name='shield_void';
 else if(/^dr21_shield_\d+$/.test(key))name='shield_code';
 else if(/^s4w_boss_flight_\d+$/.test(key)&&fv21Bank('boss4_drift')){name='boss4_drift';t=boss?._s4war?.t||efxClock;}
 return name?fv21Key(name,t):null;
}
XART._touch=function(key){const alias=fv21Alias(String(key));return FV21.base.touch.call(this,alias||key);};
XART.get=function(key){const im=FV21.base.get.apply(this,arguments);if(im)FV21.tags.set(im,key);return im;};
s5RunDraw=function(){if(!fv21Bank('portal'))return FV21.base.gates.apply(this,arguments);const draw=ctx.drawImage;
 function portalImage(im,...args){const key=FV21.tags.get(im)||'';if(!/^nfx_s5gate96_\d+$/.test(key))return draw.call(this,im,...args);
  const [x,y,w,h]=args.slice(-4),cx=x+w/2,cy=y+h/2,g=s5run?.gates.find(g=>Math.abs(g.x-cx)<1&&Math.abs(g.y-cy)<1),name=g?.i===S5R_N-1?'portal_blue':'portal';
  ctx.drawImage=draw;try{fv21Frame(name,efxClock,cx,cy,w*(224/96));}finally{ctx.drawImage=portalImage;}
 }
 ctx.drawImage=portalImage;try{return FV21.base.gates.apply(this,arguments);}finally{ctx.drawImage=draw;}};
s5GateOutDraw=function(){if(!s5GateOut||!fv21Bank('portal_blue'))return FV21.base.gateOut.apply(this,arguments);const t=s5GateOut.t,u=clamp(t/S5GO_DUR,0,1),open=Math.sin(Math.min(1,u*1.15)*Math.PI);
 ctx.save();ctx.globalCompositeOperation='lighter';fv21Frame('portal_blue',t,s5GateOut.x,s5GateOut.y,210+open*120,.35+.65*open);ctx.restore();};
wdPortalDraw=function(x,y,size,t){if(fv21Bank('portal_blue')){
  if(run.stage===5&&s5run?.gates.some(g=>g.i===S5R_N-1&&!g.passed&&Math.abs(g.x-x)<1&&Math.abs(g.y-y)<1))return;
  return fv21Frame('portal_blue',t,x,y,size*2.4);}
 return FV21.base.portal.apply(this,arguments);};
hm10Blit=function(name,f,x,y,k=1,flash=0){if(name==='shield_wall'&&fv21Bank('shield_wall')){const alpha=f<8?Math.max(.2,f/7):f>=12?Math.max(0,1-(f-12)/4):1;return fv21Frame('shield_wall',efxClock,x,y,k*512,alpha,false,0,flash);}return FV21.base.wall.apply(this,arguments);};
stage4WarfareTick=function(b,dt){const H=b?._s4war?.shield;if(H?.rearming){const center=(camLeftX()+camRightX())/2;b.x=lerp(b.x,center,Math.min(1,dt*6));}return FV21.base.warTick.apply(this,arguments);};
const FV21_SHIELDS={bubble_hex:'shield_hex',bubble_volt:'shield_volt',bubble_fire:'shield_fire',bubble_toxic:'shield_toxic',bubble_ice:'shield_ice',bubble_void:'shield_void'};
drawEnemyShieldLayer=function(e,front){const s=e?._esh,name=FV21_SHIELDS[s?.family];if(!name)return FV21.base.shield.apply(this,arguments);if(!front||e._dyingT!=null)return;
 const t=s.animT||0,energy=clamp(s.energy/Math.max(1,s.max),0,1),size=Math.max(e._drawW||e.w||30,e._drawH||e.h||30)*1.40;
 let alpha=.40+.40*energy;if(s.phase==='deploy')alpha*=clamp(t/.34,0,1);if(s.phase==='broken')alpha*=clamp(1-t/.30,0,1);
 fv21Frame(name,efxClock+(e.t||0)*.1,e.x,e.y,size,alpha,false,0,s.hitT||0);
};
// The ordinary spawn warmer touches eight old shell keys. Redirect these
// registrations to the new atlas to avoid decoding the retired512px stills.
for(const [family,name]of Object.entries(FV21_SHIELDS)){const F=ENEMY_SHIELD_FAMILY[family],B=fv21Bank(name);if(!F||!B)continue;
 if(family==='bubble_toxic')continue;
 for(let i=0;i<8;i++)FV21.aliases.set(F.prefix+'_'+i,name);
}
const fv21AliasTouch=XART._touch;
XART._touch=function(key){const n=FV21.aliases.get(key);return fv21AliasTouch.call(this,n?fv21Key(n,efxClock):key);};
carrierShieldDraw=function(b){const S=b?._bayShield;if(!S?.up)return;const size=Math.max(b.w*1.24,b.h*1.5),alpha=S.flash>0?.78:.55;
 if(!fv21Frame('shield_volt',b.t||0,b.x,b._drawY??b.y,size,alpha,false,0,S.flash||0))return FV21.base.carrier.apply(this,arguments);};
for(const [n,B]of Object.entries(FV21_ART.banks))if(n.startsWith('hammer_'))HB20_ART.banks['corrupt_'+n.slice(7)]=B.frames;
hb20Pose=function(b){const q=FV21.base.pose.apply(this,arguments);if(q?.kind?.startsWith('corrupt_')){q.k=1.1*(hb20State(b)?.scale||1);if(q.kind==='corrupt_ball')q.k=1.45*(hb20State(b)?.scale||1);}return q;};
function fv21Burst(name,x,y,size,owner){const B=fv21Bank(name);if(!B)return;FV21.fx.push({name,x,y,size,t:0,dur:B.frames.length/B.fps,owner});if(FV21.fx.length>12)FV21.fx.shift();}
j3FinalDeath=function(b){const r=FV21.base.final.apply(this,arguments);b._fv21Final??={t:0,next:0,n:0};return r;};
updatePlay=function(dt){const r=FV21.base.update.apply(this,arguments);dt=Math.min(.05,Math.max(0,dt));FV21.clock+=dt;
 for(const e of FV21.fx)e.t+=dt;FV21.fx=FV21.fx.filter(e=>e.t<e.dur&&(!e.owner||e.owner===boss));
 const b=boss,Q=b?._fv21Final;if(Q&&['finalFall','dr5Death'].includes(b._r30?.mode)){Q.t+=dt;if(Q.t>=Q.next&&Q.n<10){const i=Q.n++,a=i*2.39996,radius=32+i*5;Q.next=Q.t+.32;
  const name=['explosion_chain_burst','pack_fuel_tank_rupture','explosion_star_burst','pack_standard_eexplosions_04_smoke_core_blast','pack_implosion_collapse'][i%5];
  fv21Burst(name,b.x+Math.cos(a)*radius,b.y+Math.sin(a)*radius,110+(i%3)*45,b);}}
 return r;};
drawWorld=function(dt){const r=FV21.base.world.apply(this,arguments);if(FV21.fx.length){ctx.save();ctx.translate(-camLeftX(),0);for(const e of FV21.fx)fv21Frame(e.name,e.t,e.x,e.y,e.size,1,true);ctx.restore();}return r;};
drawCombatFinalProjectile=function(p){if(p._rd21Wind||p._rd21Shadow){const name=p._rd21Shadow?'nyx_orb':'wind_round';
 if(fv21Bank(name)&&fv21Frame(name,p.t||0,p.x,p.y,p._rd21Shadow?31:24))return true;
 const key='ra4_nhxsb_g_'+(1+Math.floor((p.t||0)*16)%2),im=xartPalette(key,p._rd21Shadow?'#6723a5':'#35e1c4');if(im){const s=p._rd21Shadow?29:23;ctx.drawImage(im,p.x-s/2,p.y-s/2,s,s);return true;}}
 return FV21.base.projectile.apply(this,arguments);};
stageLoadBegin=function(n,keys){const names=({1:[],2:['shield_hex','shield_fire','shield_volt'],3:['shield_ice'],4:['shield_volt'],5:['shield_hex','shield_void','shield_volt'],6:['shield_ice','shield_volt','shield_void'],7:['shield_hex','shield_toxic'],8:['shield_fire','shield_void','shield_code'],9:['shield_hex','shield_ice','shield_void','shield_volt']})[n]?.slice()||[];
 if(n===5)names.push('portal');if(n===8)names.push('explosion_star_burst','explosion_chain_burst','pack_fuel_tank_rupture','pack_standard_eexplosions_04_smoke_core_blast','pack_implosion_collapse');
 if([5,8].includes(n)&&fv21Bank('shield_wall'))names.push('shield_wall');if(n===4&&fv21Bank('boss4_drift'))names.push('boss4_drift');
 if(n===5&&fv21Bank('portal_blue'))names.push('portal_blue');
 for(const name of ['nyx_orb','wind_round'])if([6,8].includes(n)&&fv21Bank(name))names.push(name);
 const extra=names.flatMap(name=>{const B=fv21Bank(name);return B?[FV21_ART.sheets[B.frames[0].sheet].key]:[];});
 if(n===8)for(const [id,a] of Object.entries(FV21_ART.sheets))if(id.startsWith('fv21_hammer_'))extra.push(a.key);
 return FV21.base.load.call(this,n,[...(keys||[]),...extra]);};
globalThis.BOF_FINAL21={art:FV21_ART,state:FV21,draw:fv21Frame,burst:fv21Burst};
