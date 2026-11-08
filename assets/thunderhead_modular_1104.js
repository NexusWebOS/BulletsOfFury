"use strict";
/* TM115: regenerated disjoint Thunderhead assembly and cyclone-cannon charge.
   Native FB112 HP, part dependencies, hit flash and rewards remain authoritative. */
const TM115={base:{keys:fb112Keys,ready:fb112Ready,at:fb112At,bore:fb112Bore,opaque:fb112Opaque,
 blit:fb112Blit,draw:fb112Draw,start:fb112Start,tick:fb112Tick,cancel:fb112Cancel,
 targets:retinaBossTargets,load:stageLoadBegin},bits:null,load:null,owner:null,drawOwner:null,
 keys:Object.keys(TM115_ART.pages),events:[],beamWarm:1.7,beamGrow:.25,beamTail:.25};
for(const [k,p]of Object.entries(TM115_ART.pages))XART._src[k]=p.path;
FB112_ART.models.thunder=TM115_ART.model;
function tm115Own(b){return b?._fb112?.model==='thunder'&&b._fb112.M===TM115_ART.model;}
function tm115Warm(){if(!TM115.load)TM115.load=fetch(TM115_ART.maskPath).then(r=>{if(!r.ok)throw Error('Thunderhead modular collision '+r.status);return r.arrayBuffer();}).then(a=>{if(a.byteLength!==TM115_ART.maskBytes)throw Error('Thunderhead modular collision size');TM115.bits=new Uint8Array(a);}).catch(e=>console.error(e));}
fb112Keys=function(){tm115Warm();return [...TM115.base.keys(),...TM115.keys];};
fb112Ready=function(){return TM115.base.ready()&&!!TM115.bits&&TM115.keys.every(k=>XART.rdy(k));};
stageLoadBegin=function(n,keys){if(n===6&&fb112Rank())keys=[...(keys||[]),...fb112Keys()];return TM115.base.load.call(this,n,keys);};
function tm115State(b){return b._tm115||(b._tm115={clock:0,beams:[],serial:0,launched:false});}
function tm115Log(b,event,data={}){const row={event,t:b.t,attack:b._fb112.attack,...data};TM115.events.push(row);if(TM115.events.length>800)TM115.events.shift();fb112Log(b,'modular-'+event,data);}
function tm115Dir(a){return a<Math.PI/2-.12?1:a>Math.PI/2+.12?2:0;}
function tm115Bank(name,f,x,y){const B=TM115_ART.banks[name];if(!B)return false;f=clamp(f|0,0,B.frames-1);const c=B.cells[f];if(!XART.rdy(c[0]))return false;
 ctx.drawImage(XART.get(c[0]),c[1],c[2],B.cw,B.ch,Math.round(x-B.pivot[0]),Math.round(y-B.pivot[1]),B.cw,B.ch);return true;}
function tm115CoreOffset(){return{x:TM115_ART.model.core[0]-288,y:TM115_ART.model.core[1]-288};}
function tm115Charge(b){const q=b._fb112;return q.phase==='warn'?clamp(q.t/q.dur,0,1):q.phase==='attack'?1:0;}
function tm115Pulse(b,frames=8){const q=b._fb112,t=q.phase==='warn'?8*q.t+12*q.t*q.t/q.dur:q.phase==='attack'?20*q.dur+q.t*32:tm115State(b).clock*8;return THS114.reduced?1:Math.floor(t)%frames;}
function tm115Mask(name,f,cx,cy,x,y,pad=0){const B=TM115_ART.banks[name],m=TM115_ART.masks[name]?.[f];if(!B||!m||!TM115.bits)return false;
 const px=Math.floor(x-cx+B.pivot[0])-m[0],py=Math.floor(y-cy+B.pivot[1])-m[1];if(px<0||py<0||px>=m[2]||py>=m[3])return false;
 const bit=py*m[2]+px;return !!(TM115.bits[m[4]+(bit>>3)]&(1<<(bit&7)));}
fb112Opaque=function(name,f,a,k,cx,cy,x,y){if(!name.startsWith('thunder_'))return TM115.base.opaque.apply(this,arguments);
 if(name==='thunder_body'){const C=tm115CoreOffset();return tm115Mask('core',0,cx+C.x,cy+C.y,x,y);}
 if(/^thunder_gun[0-3]$/.test(name))return tm115Mask('gun',tm115Dir(a)+(f?3:0),cx,cy,x,y);
 if(/^thunder_pressure[01]$/.test(name))return tm115Mask('pod'+name.at(-1),0,cx,cy,x,y);
 return TM115.base.opaque.apply(this,arguments);};
fb112At=function(b,x,y,pad=0){if(!tm115Own(b))return TM115.base.at.apply(this,arguments);if(!fb112Visible(b))return null;const q=b._fb112;let best=null,score=Infinity;
 for(const p of fb112LiveParts(b)){const at=fb112PartPoint(b,p),box=p===q.core?q.M.coreBox:p.hitBox,rx=box[0]/2+pad,ry=box[1]/2+pad,v=((x-at.x)/rx)**2+((y-at.y)/ry)**2;
  const name=p===q.core?'core':p.type==='gun'?'gun':'pod'+p.index,f=p.type==='gun'?tm115Dir(p.angle)+(p.recoil>.035?3:0):0;
  if(v<=1&&v<score&&tm115Mask(name,f,at.x,at.y,x,y)){best=p;score=v;}}
 return best;};
fb112Bore=function(b,p){if(!tm115Own(b))return TM115.base.bore.apply(this,arguments);const at=fb112PartPoint(b,p),bore=p.type==='gun'?TM115_ART.model.turretBores[tm115Dir(p.angle)]:p.bore;
 return{x:at.x+bore[0],y:at.y+bore[1]+(p.type==='gun'&&p.recoil>.035?-2.24:0)};};
retinaBossTargets=function(b){if(!tm115Own(b))return TM115.base.targets.apply(this,arguments);if(!fb112Visible(b))return[];
 return fb112LiveParts(b).map(p=>{const box=p===b._fb112.core?b._fb112.M.coreBox:p.hitBox;return retinaDynamicPiece(b,'fb112-'+p.id,p.type,()=>({...fb112PartPoint(b,p),hp:p.hp,dead:!fb112Visible(b)||p.hp<=0||p===b._fb112.core&&!b._fb112.open}),d=>fb112Damage(b,d,null,null,p),box[0],box[1]);});};
fb112Blit=function(name,f,x,y,k=1,a=Math.PI/2){if(!name.startsWith('thunder_'))return TM115.base.blit.apply(this,arguments);
 const b=TM115.drawOwner||boss,q=tm115Own(b)?b._fb112:null;
 if(name==='thunder_body'){
  const level=q&&!b.dead?Math.min(3,Math.floor(tm115Charge(b)*4)):0;tm115Bank('hull',level*4+(q?tm115Pulse(b,4):0),x,y);if(q){const C=tm115CoreOffset(),frame=level*8+tm115Pulse(b);tm115Bank(q.core.hp<=0?'core_wreck':'core',q.core.hp<=0?0:frame,x+C.x,y+C.y);}return true;
 }
 if(name==='thunder_hit'){const C=tm115CoreOffset();return tm115Bank('core_hit',0,x+C.x,y+C.y);}
 const gun=/^thunder_gun([0-3])(_hit|_wreck)?$/.exec(name);if(gun){const pose=tm115Dir(a),bank=gun[2]==='_hit'?'gun_hit':gun[2]==='_wreck'?'gun_wreck':'gun',level=q?Math.min(3,Math.floor(tm115Charge(b)*4)):0,offset=bank==='gun'&&level>0?(1+(level-1)*4+tm115Pulse(b,4))*6:0;return tm115Bank(bank,offset+pose+(bank!=='gun_wreck'&&f?3:0),x,y);}
 const pod=/^thunder_pressure([01])(_hit|_wreck)?$/.exec(name);if(pod){const bank='pod'+pod[1]+(pod[2]||''),frame=pod[2]?0:q?Math.min(3,Math.floor(tm115Charge(b)*4))*8+tm115Pulse(b):0;return tm115Bank(bank,frame,x,y);}
 return true;
};
function tm115Aura(b){const q=b._fb112,p=tm115Charge(b),level=Math.min(3,Math.floor(p*4)),f=level*4+tm115Pulse(b,4),C=fb112PartPoint(b,q.core);
 tm115Bank('hull_aura',f,b.x,b.y);tm115Bank('core_aura',f,C.x,C.y);
 for(const part of q.parts)if(part.hp>0){const at=fb112PartPoint(b,part);tm115Bank(part.type==='gun'?'gun_aura':'pod'+part.index+'_aura',f,at.x,at.y);}
}
fb112Start=function(b){const out=TM115.base.start.apply(this,arguments);if(!tm115Own(b))return out;const q=b._fb112,S=tm115State(b);S.serial=q.seq;S.launched=false;
 if(q.parts.some(p=>p.type==='pressure'&&p.hp>0))q.dur+=2.2;
 tm115Log(b,'core-charge',{duration:q.dur,beamWarning:TM115.beamWarm});return out;};
function tm115Stop(B){if(!B.recovery){B.recovery=true;B.tail=0;}}
fb112Cancel=function(b){const out=TM115.base.cancel.apply(this,arguments);if(tm115Own(b)){const S=tm115State(b);S.beams.length=0;S.launched=false;tm115Log(b,'cancel');}return out;};
fb112Tick=function(b,dt){const before=b.t,out=TM115.base.tick.apply(this,arguments);if(!tm115Own(b)||b.t===before)return out;
 const q=b._fb112,S=tm115State(b);S.clock+=dt;TM115.owner=b;if(b.dead){S.beams.length=0;return out;}
 if(q.phase==='warn'){
  for(const p of q.parts.filter(p=>p.type==='pressure'&&p.hp>0))if(q.t<TM115.beamWarm)combatWarningTick(p,'wind-beam-'+q.seq,q.t,TM115.beamWarm);
  if(q.t>=TM115.beamWarm&&!S.launched&&q.parts.some(p=>p.type==='pressure'&&p.hp>0)){
   S.launched=true;
   for(const part of q.parts.filter(p=>p.type==='pressure'&&p.hp>0)){const at=fb112Bore(b,part);S.beams.push({part,age:0,recovery:false,tail:0,hits:new Set(),x:at.x,y:at.y});tm115Log(b,'wind-beam',{part:part.id,x:at.x,y:at.y,warning:q.t});}
   combatAudio0927(b,'overlordWind',.4);combatAudio0927(b,'combatBeam0927',.4);
  }
 }
 for(const B of S.beams){B.age+=dt;const at=fb112Bore(b,B.part);B.x=at.x;B.y=at.y;
  if(q.phase!=='warn'||B.part.hp<=0)tm115Stop(B);
  if(B.recovery){B.tail+=dt;continue;}
  if(B.age>=TM115.beamGrow&&B.part.hp>0)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&player.invuln<=0&&!B.hits.has(seat)&&Math.abs(player.x-B.x)<42&&player.y>B.y+8&&player.y<VH+20){B.hits.add(seat);playerHit('Thunderhead cyclone cannon');tm115Log(b,'wind-beam-hit',{part:B.part.id,seat});}});
 }
 S.beams=S.beams.filter(B=>!B.recovery||B.tail<TM115.beamTail);if(S.beams.some(B=>!B.recovery))combatAudio0927(b,'overlordWind',1.2);return out;
};
function tm115DrawBeams(b){for(const B of tm115State(b).beams){const frame=B.recovery?22+Math.min(5,Math.floor(B.tail*24)):B.age<TM115.beamGrow?Math.min(5,Math.floor(B.age*24)):6+Math.floor((B.age-TM115.beamGrow)*24)%16;
 tm115Bank('wind_beam',frame,B.x,B.y);}}
function tm115Warnings(b){const q=b._fb112;if(q.phase!=='warn')return;
 const warm=TM115.beamWarm,coreWarm=q.attack==='storm-tempest'?2.8:q.attack==='storm-thunder'?1.9:1.6,progress=clamp((q.t-(q.dur-coreWarm))/coreWarm,0,1),at=th114Core(b);
 if(q.t<warm)for(const p of q.parts.filter(p=>p.type==='pressure'&&p.hp>0)){const m=fb112Bore(b,p);combatWarningDraw(p,{x:m.x,y:m.y,ex:m.x,ey:VH+100,width:90,progress:q.t/warm,fieldOnly:true});}
 l23WarnSymbolDraw(b,{family:'rime',t:clamp(q.t/q.dur,0,1),warm:1,released:false,blinkT:q.t,alertX:at.x,alertY:at.y+60});
 if(progress<=0)return;
 if(q.attack==='storm-cyclone')for(const d of[-.4,0,.4])combatWarningDraw(b,{x:at.x,y:at.y,ex:at.x+Math.sin(d)*600,ey:at.y+Math.cos(d)*600,width:42,progress,fieldOnly:true});
 if(q.attack==='storm-tornado')for(const p of q.parts.filter(p=>p.type==='pressure'&&p.hp>0)){const m=fb112Bore(b,p);combatWarningDraw(b,{x:m.x,y:m.y,ex:m.x+(p.index===0?50:-50),ey:VH+50,width:72,progress,fieldOnly:true});}
 if(q.attack==='storm-tempest')combatWarningDraw(b,{x:at.x,y:at.y,ex:th114State(b).stormLane,ey:VH+100,width:200,progress,fieldOnly:true});
}
fb112Draw=function(b){if(!tm115Own(b))return TM115.base.draw.apply(this,arguments);if(!fb112Ready())return;const q=b._fb112,S=th114State(b);TM115.drawOwner=b;
 try{
  if(!b.dead)tm115Aura(b);
  // The base assembly uses the new hull/core/weapon banks through fb112Blit.
  // Keep the storm's actual front/ground-impact owners without its old core art.
  THS114.base.draw(b);
  if(b.dead)return;
  for(const f of S.muzzle)th114Blit('muzzle',Math.min(3,Math.floor(f.age*24)),f.x,f.y);
  for(const f of S.fields)th114RoundDraw(f);
  tm115DrawBeams(b);
  for(const P of S.marks)th114Retina(P);
  for(const P of S.impacts){if(P.age<(THS114.reduced?.09:.24))th114Blit('bolt',Math.floor(P.age*24)%8,P.x,P.y-256);th114Blit('impact',Math.min(13,Math.floor(P.age*24)),P.x,P.y);}
  tm115Warnings(b);
 }finally{TM115.drawOwner=null;}
};
globalThis.BOF_THUNDERHEAD_MODULAR_1104={state:TM115,art:TM115_ART,owns:tm115Own};
