'use strict';
/* Mike's Oct25 review: planted spider gait and the first-host/download revision.
   HP, rewards, protected core, portal travel and final-arena owners stay native. */
const S78={events:[],frames:new Map(),pulses:new WeakMap(),debris:[],arenaClock:0,
 base:{load:stageLoadBegin,cell:s7mCell,pose:s7mPose,tick:s7mTick,set:s7mSet,next:s7mNext,blit:s7mBlit,draw:s7mDraw,at7:s7mAt,targets7:s7mTargets,world7:s7mWorld,muzzle7:s7mMuzzle,reverse7:s7WardenReverseScroll,warnings7:s7mWarnings,
  attack:v18StartAttack,attackTick:v18AttackTick,pose8:bi24AttackPose,eye:rb23Eye,point:rb23PartPoint,
  body:v18Body,draw24:bi24Draw,at:r30At,rupture:v18Rupture,break:r30Break,sceneTick:rb23SceneTick,sceneDraw:rb23SceneDraw,
  weapon:rb23DrawWeapon,bank:er23DrawBank,arena:v17ArenaDraw,bossTick:r30Tick,bossDraw:r30DrawBoss,
  mount:d20BossMount,plated:v19Body,update:updatePlay,finalDeath:j3FinalDeath}};
for(const a of Object.values(R25_ART.sheets)){XART._src[a.key]=a.path;XART._src['nca_'+a.key]=a.path;}
for(const [name,a]of Object.entries(R25_ART.legs))for(let f=0;f<a.count;f++)for(const hit of ['', '_hit'])
 BOFX.cells['r25_leg_'+name+hit+'_'+f]=['r25_leg_'+name+hit,(f%a.cols)*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h];
function r25Log(type,data={}){S78.events.push({type,time:efxClock,...data});if(S78.events.length>500)S78.events.shift();}
function r25Own7(b){return run.stage===7&&b?._s7mod&&!b._s7mod.tank;}
function r25Keys(n){return Object.entries(R25_ART.sheets).filter(([k])=>n===7?k.startsWith('leg_'):!k.startsWith('leg_')).map(([,a])=>a.key);}
function r25Warm(n){return r25Keys(n).map(k=>XART.rdy(k)).every(Boolean);}
stageLoadBegin=function(n,keys){if(n===8)for(const k of ['enemyBossCannon','combatBeam0927','bossWeaponCharge','combatModule0927','timedBombBeep','timedBombBlast'])Snd.prepare(k);
 return S78.base.load.call(this,n,[...(keys||[]),...([7,8].includes(n)?r25Keys(n):[]),...(n===8?Array.from({length:4},(_,i)=>'weapon_muzzle_rotary_'+i):[])]);};
function r25Pulse(owner,timer,clock){
 if(!owner)return 0;let q=S78.pulses.get(owner);
 if(!(timer>0)){if(q)q.active=false;return 0;}
 if(!q){q={active:false,start:clock};S78.pulses.set(owner,q);}
 if(!q.active||clock-q.start>=.24){q.start=clock;q.active=true;}
 const age=Math.max(0,clock-q.start);
 return Math.min(1,timer/.035)*(age<.055?1:age<.125?(1-(age-.055)/.07):0);
}
function r25Frame(name,f,white=false){
 const a=R25_ART.host[name]||R25_ART[name],sheet=R25_ART.sheets[name];if(!a||!sheet||!XART.rdy(sheet.key))return null;
 f=clamp(f|0,0,a.count-1);const id=name+':'+f+':'+white;let c=S78.frames.get(id);if(c)return c;
 c=document.createElement('canvas');c.width=a.w;c.height=a.h;const g=c.getContext('2d');g.drawImage(XART.get(sheet.key),(f%a.cols)*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,0,0,a.w,a.h);
 if(white){g.globalCompositeOperation='source-in';g.fillStyle='#fff';g.fillRect(0,0,c.width,c.height);}S78.frames.set(id,c);return c;
}
function r25Layer(name,id,f,white=false){
 const a=R25_ART.host[name],sheet=R25_ART.sheets[name+'_'+id];if(!a||!sheet||!XART.rdy(sheet.key))return null;
 const cache=name+':'+id+':'+f+':'+white;let c=S78.frames.get(cache);if(c)return c;
 c=document.createElement('canvas');c.width=c.height=512;const g=c.getContext('2d');g.drawImage(XART.get(sheet.key),(f%4)*512,Math.floor(f/4)*512,512,512,0,0,512,512);
 if(white){g.globalCompositeOperation='source-in';g.fillStyle='#fff';g.fillRect(0,0,512,512);}S78.frames.set(cache,c);return c;
}

/* Walking is driven by ground distance. Diagonal support pairs hold their toes
   in world space while the chassis travels over them; hips stay beneath it. */
s7mCell=function(name,i,trim){if(typeof i==='string'&&i.startsWith('r25_leg_'))return XART.rdy(i)?XART.get(i):null;return S78.base.cell.apply(this,arguments);};
function r25Gait(b){const M=b._s7mod;return M.r25Gait||(M.r25Gait={distance:0,x:b.x,y:b.y,yaw:0,speed:0,feet:{},walks:0});}
function r25GroundRate(b){const M=b._s7mod;if(b.dead||M.frExit||!s7mLive(M,'front').length&&!s7mLive(M,'rear').length)return 0;
 return M.mode==='chase'?[100,130,160][M.n]:M.mode==='crawl'?36:0;}
s7WardenReverseScroll=function(){return r25Own7(boss)?r25GroundRate(boss):S78.base.reverse7.apply(this,arguments);};
s7mWorld=function(b,p){if(!r25Own7(b))return S78.base.world7.apply(this,arguments);const M=b._s7mod,a=r25Gait(b).yaw,c=Math.cos(a),s=Math.sin(a);return{x:b.x+p.x*c-p.y*s,y:b.y+M.drop-M.height+p.x*s+p.y*c};};
s7mMuzzle=function(b,id){if(!r25Own7(b))return S78.base.muzzle7.apply(this,arguments);const M=b._s7mod,yaw=r25Gait(b).yaw;
 if(id==='emitter')return{...s7mWorld(b,{x:0,y:59}),a:Math.PI/2+yaw};
 const pose=s7mPose(b),p=pose.find(p=>p.id===id)||pose.find(p=>p.id==='body'),a=p.a+yaw,q=s7mWorld(b,p);return{x:q.x-Math.sin(a)*p.h*.47,y:q.y+Math.cos(a)*p.h*.47,a:Math.PI/2+a};};
s7mNext=function(b){const M=b?._s7mod;if(r25Own7(b)&&!M.frExit&&s7mLive(M,'front').length+s7mLive(M,'rear').length>0){
 const G=r25Gait(b);G.walks++;if(G.walks%2===1){M.r25Walk=true;s7mSet(b,s7mLive(M,'front').length?'chase':'crawl');return;}}
 return S78.base.next.apply(this,arguments);};
s7mSet=function(b,mode){if(r25Own7(b)){
 const M=b._s7mod;if(mode==='jump'&&M.mode==='swipeX'&&(s7mLive(M,'front').length||s7mLive(M,'rear').length)){
  M.r25Jump=(M.r25Jump||0)+1;if(M.r25Jump%3!==0)mode='recover';}
 if(!['chase','crawl'].includes(mode))M.r25Walk=false;
 }return S78.base.set.call(this,b,mode);};
s7mTick=function(b,dt){if(!r25Own7(b))return S78.base.tick.apply(this,arguments);
 const M=b._s7mod,G=r25Gait(b),x=b.x,y=b.y,grounded=!['portal','entry','jump','stomp','bounce','dead'].includes(M.mode);
 const previousDistance=Math.hypot(G.lastDX||0,G.lastDY||0),target=grounded&&previousDistance>.04?clamp(G.lastDX/previousDistance*.19,-.19,.19):0;
 G.yaw+=clamp(target-G.yaw,-dt*.33,dt*.33);M.lean=G.yaw;
 let r;if(M.r25Walk&&['chase','crawl'].includes(M.mode)){
  bm9S7Common(b,dt);const rear=M.mode==='crawl',side=Math.sin((G.walks+1)*2.39996),tx=clamp(player.x+side*80,145,worldWidth()-145),ty=clamp(player.y-(rear?180:145),150,VH*.55);
  s7mMove(b,tx,ty,rear?62:98,dt);M.height=0;
  if(M.t>3.2){M.r25Walk=false;s7mSet(b,'recover');}r=true;
 }else r=S78.base.tick.apply(this,arguments);
 // The scrolling floor is movement too: holding a screen position while the
 // pilot retreats still requires planted feet, carried with that same floor.
 const floor=grounded?r25GroundRate(b)*dt:0,dx=b.x-x,dy=b.y-y+floor;
 for(const p of Object.values(G.feet))if(p.stance)p.y-=floor;
 const d=grounded?Math.hypot(dx,dy):0;G.speed=dt>0?d/dt:0;G.distance+=d;G.floorRate=dt>0?floor/dt:0;
 M.lean=G.yaw;G.x=b.x;G.y=b.y;G.lastDX=b.x-x;G.lastDY=b.y-y;
 if(!grounded)G.feet={};
 if(d>0){const beat=Math.floor(G.distance/36);if(beat!==G.footBeat){G.footBeat=beat;if(G.speed>20)s7WardenMechSound('foot');}}
 return r;
};
s7mPose=function(b){const out=S78.base.pose.apply(this,arguments);if(!r25Own7(b))return out;
 const M=b._s7mod,G=r25Gait(b);
 // The trunnions stay seated during takeoff/landing and portal assembly too.
 for(let i=0;i<out.length;i++){const p=out[i];if(p.id!=='gunL'&&p.id!=='gunR')continue;const side=p.id==='gunL'?-1:1,a=p.a,reach=37;
  out[i]={...p,x:side*34-Math.sin(a)*reach,y:12+Math.cos(a)*reach,w:34,h:84,mount:{x:side*34,y:12}};}
 if(['portal','entry'].includes(M.mode))return out;
 const airborne=['jump','stomp','bounce'].includes(M.mode);
 const active=G.speed>.01,cycle=G.distance/72;
 for(let i=0;i<out.length;i++){
  const p=out[i],side=p.id.endsWith('L')?-1:1;
  // One rigid gun rotates about its rear trunnion. Neither the battery's
  // convergence pose nor the chaingun's extension may translate its mounting.
  if(p.id==='gunL'||p.id==='gunR')continue;
  const a=R25_ART.legs[p.id];if(!a)continue;
  const rear=p.id.startsWith('rear'),offset=(p.id==='frontR'||p.id==='rearL')?.5:0,phase=(cycle+offset)%1;
  const swipe=!rear&&M.mode.startsWith('swipe'),striking=swipe&&(M.mode==='swipeX'||M.mode===(side<0?'swipeL':'swipeR')),u=M.t-M.warn;
  let f=active?Math.floor(phase*8)%8:0,angle=rear?-side*.60:0;
  if(airborne)f=M.height>0||M.mode==='jump'&&M.t<.26?4:0;
  if(striking){const wind=clamp(M.t/Math.max(.01,M.warn),0,1),strike=clamp(u/.38,0,1),back=clamp((u-.38)/.65,0,1);
   // Use the same connected claw and pivot throughout. The retired attack bank
   // folded both live forearms across the face and made them appear to vanish.
   angle=u<0?-side*.50*wind:u<.38?side*(-.50+.80*strike):side*.30*(1-back);
   f=u<0?Math.min(4,Math.floor(wind*5)):u<.38?4+Math.min(3,Math.floor(strike*4)):Math.max(0,7-Math.floor(back*8));}
  const row=a.frames[f],k=a.worldScale;
  const hip={x:side*64,y:rear?-72:-11},c=Math.cos(angle),s=Math.sin(angle);
  const center={x:hip.x+(128-a.pivot[0])*k*c-(128-a.pivot[1])*k*s,y:hip.y+(128-a.pivot[0])*k*s+(128-a.pivot[1])*k*c};
  const toe={x:hip.x+(row.foot[0]-a.pivot[0])*k*c-(row.foot[1]-a.pivot[1])*k*s,y:hip.y+(row.foot[0]-a.pivot[0])*k*s+(row.foot[1]-a.pivot[1])*k*c};
  const world=s7mWorld(b,toe),stance=active&&!airborne&&!striking&&phase<.50,foot=G.feet[p.id];let dx=0,dy=0;
  if(stance){if(!foot||!foot.stance||phase<foot.phase)G.feet[p.id]={x:world.x,y:world.y,stance:true,phase};
   const pin=G.feet[p.id],wx=pin.x-world.x,wy=pin.y-world.y;dx=wx*Math.cos(G.yaw)+wy*Math.sin(G.yaw);dy=-wx*Math.sin(G.yaw)+wy*Math.cos(G.yaw);pin.phase=phase;
  }else G.feet[p.id]={x:world.x,y:world.y,stance:false,phase};
  const tx=(row.target[0]-128)*k,ty=(row.target[1]-128)*k;
  out[i]={...p,cell:row.key,x:center.x+dx,y:center.y+dy,w:256*k,h:256*k,a:angle,r25:true,frame:f,stance,toe:{x:toe.x+dx,y:toe.y+dy},bm9Tip:{x:toe.x+dx,y:toe.y+dy},target:{x:center.x+dx+tx*c-ty*s,y:center.y+dy+tx*s+ty*c}};
 }
 return out;
};
s7mAt=function(b,x,y){if(!r25Own7(b))return S78.base.at7.apply(this,arguments);const M=b._s7mod;
 if(['portal','entry','roar','dead','jump','overdrive'].includes(M.mode))return null;
 for(const p of s7mPose(b).slice().reverse()){
  const part=M.parts.find(q=>q.id===p.id);if(part&&part.hp<=0)continue;if(!part&&!['body','core','canL','canR'].includes(p.id))continue;
  const q=s7mWorld(b,p),a=p.a+M.lean,c=Math.cos(a),s=Math.sin(a),dx=(x-q.x)*c+(y-q.y)*s,dy=-(x-q.x)*s+(y-q.y)*c;
  if(p.r25){const px=Math.floor((dx/p.w+.5)*256),py=Math.floor((dy/p.h+.5)*256);if(px<0||py<0||px>=256||py>=256)continue;
   const key=p.cell+':alpha';let mask=S78.frames.get(key);if(!mask){const im=XART.get(p.cell);if(!im)continue;const g=document.createElement('canvas');g.width=g.height=256;g.getContext('2d').drawImage(im,0,0);mask=g.getContext('2d').getImageData(0,0,256,256).data;S78.frames.set(key,mask);}if(mask[(py*256+px)*4+3]>48)return p.id;
  }else if(Math.abs(dx)<p.w*.48&&Math.abs(dy)<p.h*.48)return part?part.id:p.id.startsWith('can')?'canister':'core';
 }return null;
};
s7mTargets=function(b){if(!r25Own7(b))return S78.base.targets7.apply(this,arguments);const M=b._s7mod;if(['portal','entry','roar','jump','dead'].includes(M.mode))return [];
 const ids=M.parts.filter(p=>s7mVulnerable(M,p)).map(p=>p.id);if(!s7mLive(M,'front').length&&!s7mLive(M,'rear').length)ids.push('core');
 return ids.map(id=>retinaDynamicPiece(b,id,'toxic module',()=>{const pose=s7mPose(b),p=pose.find(p=>p.id===id)||pose.find(p=>p.id==='body'),q=s7mWorld(b,p.r25?p.target:p),part=M.parts.find(p=>p.id===id);return{...q,hp:part?part.hp:M.shield>0?M.shield:M.core,dead:b.dead||M.mode==='dead'||!!(part&&!s7mVulnerable(M,part))};},d=>s7mHit(b,d,0,0,id),id==='core'?92:48,id==='core'?102:68));
};
s7mBlit=function(name,i,x,y,w,h,rot,alpha,flash){if(S78.s7Actor&&flash>0)flash*=r25Pulse(S78.s7Actor._s7mod,flash,S78.s7Actor._s7mod.clock);
 return S78.base.blit.call(this,name,i,x,y,w,h,rot,alpha,flash);};
s7mDraw=function(b){const old=S78.s7Actor;if(r25Own7(b))S78.s7Actor=b;try{return S78.base.draw.apply(this,arguments);}finally{S78.s7Actor=old;}};
s7mWarnings=function(front){const M=boss?._s7mod;
 if(!r25Own7(boss)||!M.mode.startsWith('swipe'))return S78.base.warnings7.apply(this,arguments);
 // Suppress only the former claw envelopes. All other owners keep their tells.
 const mode=M.mode;M.mode='r25-claw-warning';try{S78.base.warnings7.apply(this,arguments);}finally{M.mode=mode;}
 if(M.t>=M.warn)return;
 for(const p of s7mPose(boss).filter(p=>p.id.startsWith('front')&&s7mLive(M,'front').some(q=>q.id===p.id)&&(mode==='swipeX'||mode===(p.id==='frontL'?'swipeL':'swipeR')))){
  const a=s7mWorld(boss,p.toe),side=p.id.endsWith('L')?-1:1,bank=R25_ART.legs[p.id],row=bank.frames[7],ang=side*.30,k=bank.worldScale,dx=(row.foot[0]-bank.pivot[0])*k,dy=(row.foot[1]-bank.pivot[1])*k;
  const z=s7mWorld(boss,{x:side*64+dx*Math.cos(ang)-dy*Math.sin(ang),y:-11+dx*Math.sin(ang)+dy*Math.cos(ang)});
  combatWarningDraw(boss,{x:a.x,y:a.y,ex:z.x,ey:z.y,width:26,progress:M.t/M.warn,laneShape:'line',fieldOnly:!front,alertOnly:front});
 }
};

/* The complete connected host is retained. Per-pixel layer masks only remove
   the arm Mike now explicitly wants to break away; no moving rectangle crops. */
bi24AttackPose=function(b,actor){if(actor==='dracodia'&&rb23Host(b)){
 const P=b._r30.v18.attack;if(P?.type==='rb23-pincer'){
  const u=P.t-P.tell;return u<0?bi24Sample('dracodia_wind',P.t/P.tell):u<1.6?bi24Sample('dracodia_wind',1):bi24Sample('dracodia_wind',1-clamp((u-1.6)/.7,0,1));
 }}return S78.base.pose8.apply(this,arguments);};
function r25HostSample(b){const q=bi24AttackPose(b,'dracodia'),name=q.a.key.replace('nca_bi24_','');return{...q,name,data:R25_ART.host[name]?.frames[q.f]};}
rb23Eye=function(b){if(rb23Host(b)&&!b._r30.v18.bi24Rolled){const q=r25HostSample(b),p=q.data?.eye;if(p)return{...bi24World(b,p[0],p[1]),w:p[2]*360/512,h:p[3]*360/512};}return S78.base.eye.apply(this,arguments);};
rb23PartPoint=function(b,p,muzzle=false){if(rb23Host(b)&&!b._r30.v18.bi24Rolled&&p.id!=='core'){
 const q=r25HostSample(b),a=muzzle?q.data?.muzzles[p.id]:(q.data?.targets?.[p.id]||q.a.arms[q.f]?.[p.id]?.map(v=>v*2));if(a)return bi24World(b,a[0],a[1]);
 }return S78.base.point.apply(this,arguments);};
bi24Draw=function(q,b,size,rot=0){if(!v18Owned(b))return S78.base.draw24.apply(this,arguments);
 const host=rb23Host(b),k=size/q.a.w,name=q.a.key.replace('nca_bi24_','');
 if(host&&R25_ART.host[name]){
  ctx.save();ctx.translate(b.x,b.y);ctx.rotate(rot);ctx.imageSmoothingEnabled=false;
  for(const id of ['left','right','core']){const p=b.parts.find(p=>p.id===id);if(!p||p.destroyed||p.hp<=0&&id!=='core')continue;const im=r25Layer(name,id,q.f);if(!im)continue;
   ctx.drawImage(im,-256*k,-256*k,512*k,512*k);const pulse=r25Pulse(p,Math.max(p.flash||0,id==='core'?b.flash||0:0),b._r30.clock);
   if(pulse>0){ctx.save();ctx.globalAlpha*=pulse;ctx.drawImage(r25Layer(name,id,q.f,true),-256*k,-256*k,512*k,512*k);ctx.restore();}}
  ctx.restore();BI24.current.set(b,{...q,size,k,rot,x:b.x,y:b.y,key:q.a.key});return true;
 }
 const flash=Math.max(b.flash||0,...b.parts.map(p=>p.flash||0)),pulse=r25Pulse(b,flash,b._r30.clock),im=bi24DamagePlate(q,b),a=q.a;
 if(!XART.rdy(a.key)||!XART.rdy(a.white))return false;ctx.save();ctx.translate(b.x,b.y);ctx.rotate(rot);ctx.imageSmoothingEnabled=false;
 if(im)ctx.drawImage(im,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);else ctx.drawImage(XART.get(a.key),q.f%a.cols*a.w,Math.floor(q.f/a.cols)*a.h,a.w,a.h,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);
 if(pulse>0){ctx.globalAlpha*=pulse;ctx.drawImage(XART.get(a.white),q.f%a.cols*a.w,Math.floor(q.f/a.cols)*a.h,a.w,a.h,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);}ctx.restore();BI24.current.set(b,{...q,size,k,rot,x:b.x,y:b.y,key:a.key});return true;
};
v19Body=function(b){if(!bi24Plated(b))return S78.base.plated.apply(this,arguments);
 const frame=v18Frame(b),rows=['left','core','right'].map(id=>frame[id]).filter(Boolean);if(!rows.every(a=>XART.rdy(a.key)))return;
 const key=rows.map(a=>a.key).join('|');let plate=BI24.plates.get(key);
 if(!plate){const c=document.createElement('canvas');c.width=c.height=320;const g=c.getContext('2d');for(const a of rows)g.drawImage(XART.get(a.key),0,0);const white=document.createElement('canvas');white.width=white.height=320;const w=white.getContext('2d');w.drawImage(c,0,0);w.globalCompositeOperation='source-in';w.fillStyle='#fff';w.fillRect(0,0,320,320);plate={c,white};BI24.plates.set(key,plate);}
 const k=bi24PlateScale(b),pulse=r25Pulse(b,Math.max(b.flash||0,...b.parts.map(p=>p.flash||0)),b._r30.clock);ctx.drawImage(plate.c,b.x-160*k,b.y-160*k,320*k,320*k);
 if(pulse>0){ctx.save();ctx.globalAlpha*=pulse;ctx.drawImage(plate.white,b.x-160*k,b.y-160*k,320*k,320*k);ctx.restore();}
};
r30At=function(b,x,y){if(rb23Host(b)&&!b._r30.v18.bi24Rolled&&b._r30.mode==='fight'){
 if(!r30Live(b)||b._noHit)return null;const q=r25HostSample(b),k=360/512,px=Math.floor((x-b.x)/k+256),py=Math.floor((y-b.y)/k+256);if(px<0||py<0||px>=512||py>=512)return null;
 for(const id of ['left','right','core']){const p=b.parts.find(p=>p.id===id);if(!p||p.destroyed||p.hp<=0)continue;const im=r25Layer(q.name,id,q.f);if(!im)continue;
  const cache=q.name+':'+id+':'+q.f+':alpha';let data=S78.frames.get(cache);if(!data){data=im.getContext('2d').getImageData(0,0,512,512).data;S78.frames.set(cache,data);}if(data[(py*512+px)*4+3]>48)return p;}
 return null;
 }return S78.base.at.apply(this,arguments);};

/* Committed claw socket owns its FOV, physical rocket and ordinary round. */
function r25ClawLanes(b,P){P.lanes=[];for(const p of rb23Arms(b)){
 const q=rb23PartPoint(b,p,true),a=Math.atan2(P.ty-q.y,P.tx-q.x);for(const off of [-.18,0,.18])P.lanes.push({...q,ex:q.x+Math.cos(a+off)*VH,ey:q.y+Math.sin(a+off)*VH,width:20,module:p.id,angle:a+off});}}
v18StartAttack=function(b){const r=S78.base.attack.apply(this,arguments);if(!rb23Host(b))return r;const P=b._r30.v18.attack;
 if(P?.type==='rb23-pincer'){P.committed=false;r25ClawLanes(b,P);}
 if(P?.type==='rb23-roll'){P.active=9.6;P.beamPhase='travel';P.drop=0;P.path=[{...P.origin},...rb23Path(b,b._r30.v18.rb23Seq)];r25Log('ball-route',{points:P.path.length});}
 return r;};
function r25FinishAttack(b,P){const N=b._r30.v18;N.attack=null;b._r30.attack=null;b._r30.cd=.8;N.home={x:clamp(b.x,camLeftX()+100,camRightX()-100),y:clamp(b.y,viewTopY()+140,viewTopY()+260)};j3State(b).attacks++;}
function r25Route(P,u){const a=P.path,v=clamp(u,0,.999999)*(a.length-1),i=Math.floor(v),t=v-i,p0=a[Math.max(0,i-1)],p1=a[i],p2=a[i+1],p3=a[Math.min(a.length-1,i+2)];
 const value=key=>.5*((2*p1[key])+(-p0[key]+p2[key])*t+(2*p0[key]-5*p1[key]+4*p2[key]-p3[key])*t*t+(-p0[key]+3*p1[key]-3*p2[key]+p3[key])*t*t*t);
 return{x:clamp(value('x'),camLeftX()+100,camRightX()-100),y:clamp(value('y'),viewTopY()+135,VH-112)};}
d20BossMount=function(b,id){if(rb23Host(b)&&b._r30.v18.bi24Rolled)return{x:b.x,y:b.y+22,module:id};return S78.base.mount.apply(this,arguments);};
function r25DropBomb(b,P){const live=enemies.filter(e=>!e.dead&&e._d20?.owner===b&&e._d20.kind==='bomb'&&e._d20.phase!=='erase');if(live.length>=4)return;
 let target={x:clamp(b.x,camLeftX()+70,camRightX()-70),y:clamp(b.y+110,viewTopY()+240,VH-62)};
 if(live.some(e=>Math.hypot(e._d20.target.x-target.x,e._d20.target.y-target.y)<112)){
  const sign=b.x<(camLeftX()+camRightX())/2?1:-1;target.x=clamp(target.x+sign*132,camLeftX()+70,camRightX()-70);
  if(live.some(e=>Math.hypot(e._d20.target.x-target.x,e._d20.target.y-target.y)<112))return;}
 const e=d20Bomb(b,target);if(e){e.x=b.x;e.y=b.y+22;e._d20.start={x:e.x,y:e.y};r25Log('ball-code-drop',{x:e.x,y:e.y,target,warning:e._d20.flight+e._d20.warm});}}
v18AttackTick=function(b,dt){const P=b?._r30?.v18?.attack;if(!rb23Host(b)||!['rb23-roll','rb23-pincer'].includes(P?.type))return S78.base.attackTick.apply(this,arguments);
 P.t+=dt;const u=P.t-P.tell;
 if(P.type==='rb23-pincer'){
  if(P.committed)for(const L of P.lanes){const p=b.parts.find(p=>p.id===L.module);if(!p||p.destroyed)continue;const q=rb23PartPoint(b,p,true);Object.assign(L,q,{ex:q.x+Math.cos(L.angle)*VH,ey:q.y+Math.sin(L.angle)*VH});}
  if(u<0){if(!P.committed){r25ClawLanes(b,P);if(P.t>=P.tell-.30)P.committed=true;}else for(const L of P.lanes){const p=b.parts.find(p=>p.id===L.module),q=rb23PartPoint(b,p,true);Object.assign(L,q,{ex:q.x+Math.cos(L.angle)*VH,ey:q.y+Math.sin(L.angle)*VH});}
   combatWarningTick(b,'dracodia-claws-'+b._r30.v18.rb23Seq,P.t,P.tell);return;}
  if(u>=P.next&&P.n<4){P.next+=.4;const missile=P.n++%2===1;
   for(const p of rb23Arms(b)){
    const q=rb23PartPoint(b,p,true),lanes=P.lanes.filter(L=>L.module===p.id),selected=missile?lanes.filter((_,i)=>i===1):lanes;
    for(const L of selected){const shot=missile?eShootT(q.x,q.y,L.angle,3.4,'emissile',{owner:b,noMuzzle:true,silent:true,w:10,h:20}):v18Shot(b,q,L.angle,3.4,'code');
     if(shot){shot._v18Owner=b;shot._noArsenal=true;if(missile){shot._shootable=true;shot._weaponProof=false;shot.hp=3;shot.homing=false;}r25Log('claw-shot',{part:p.id,x:q.x,y:q.y,angle:L.angle,missile});}}
    navalFlash(null,q,.75,'weapon_muzzle_rotary',{n:4,hpx:42,life:.16,angle:(lanes[1]?.angle||Math.PI/2)-Math.PI/2,follow:()=>p.destroyed||b.dead||!r30Live(b)?null:rb23PartPoint(b,p,true)});
   }r30Sound('enemyBossCannon');}
 }else{
  if(u<0){combatWarningTick(b,'dracodia-fold-'+b._r30.v18.rb23Seq,P.t,P.tell);return;}
  const q=r25Route(P,u/P.active);b.x=q.x;b.y=q.y;P.eye={x:b.x,y:b.y};P.beamPhase='travel';
  P.drop-=dt;if(P.drop<=0){P.drop=[1.15,1,.85][Math.min(2,target17Rank())];r25DropBomb(b,P);}
  for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(player.x-b.x,player.y-b.y)<62)playerHit('Dracodia rolling core');});
 }
 if(u>=P.active)r25FinishAttack(b,P);b._drawY=b.y;
};
er23DrawBank=function(name,f,x,y,flash=false){if(flash&&rb23Host(boss)&&['fold','roll'].includes(name)){
 const r=S78.base.bank.call(this,name,f,x,y,false),pulse=r25Pulse(boss.parts[0],boss.parts[0].flash,boss._r30.clock);
 if(pulse>0){ctx.save();ctx.globalAlpha*=pulse;S78.base.bank.call(this,name,f,x,y,true);ctx.restore();}return r;}
 return S78.base.bank.apply(this,arguments);};
v18Body=function(b){if(rb23Host(b)&&b._r30.mode==='fight'&&!rb23Arms(b).length){const N=b._r30.v18,P=N.attack;
 if(N.bi24Rolled||P?.type==='rb23-roll'){N.bi24Rolled=true;const folding=!N.r25BallReady&&P?.type==='rb23-roll'&&P.t<P.tell;
  if(!folding)N.r25BallReady=true;return er23DrawBank(folding?'fold':'roll',folding?Math.min(8,Math.floor(P.t/P.tell*9)):Math.floor(b._r30.clock*30)%24,b.x,b.y,b.parts[0].flash>0);}}
 return S78.base.body.apply(this,arguments);};
rb23DrawWeapon=function(b){const P=b._r30.v18.attack;if(P?.type==='rb23-roll')return;
 if(P?.type==='rb23-pincer'){
  if(P.t<P.tell)for(const L of P.lanes)if(b.parts.some(p=>p.id===L.module&&!p.destroyed))combatWarningDraw(b,{...L,progress:P.t/P.tell,fieldOnly:true});return;}
 const r=S78.base.weapon.apply(this,arguments);if(P?.type==='rb23-eye'){
  const eye=rb23Eye(b),u=P.t-P.tell;if(u<P.active){
   const a=R25_ART.eye_flare,im=a&&r25Frame('eye_flare',Math.floor(P.t*24)%a.count),fire=u>=0;
   if(im){const k=(fire?Math.max(eye.w||24,26)*1.85:Math.max(eye.w||24,26)*(1+P.t/P.tell*.6))/a.visibleWidth;
    ctx.save();ctx.globalAlpha*=fire?1:.35+.65*clamp(P.t/P.tell,0,1);ctx.drawImage(im,eye.x-a.pivot[0]*k,eye.y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();}
   else if(fire){const root=r25Frame('eye_root',Math.floor(P.t*24)%16);if(root)ctx.drawImage(root,eye.x-52,eye.y-12,104,80);}
  }}return r;};

/* Bounded debris made from the actual alpha-bearing arm/body pixels. Wrecks
   remain opaque, break into irregular shards, and leave the screen physically. */
function r25Shards(owner,im,x,y,k,count=14,baseVX=0,baseVY=0,rotation=0){if(!im)return;const seeds=Array.from({length:count},(_,i)=>({x:im.width*(.08+.84*((i*.61803398875+.17)%1)),y:im.height*(.08+.84*((i*.38196601125+.23)%1))}));
 const g=im.getContext('2d',{willReadFrequently:true}),src=g.getImageData(0,0,im.width,im.height),groups=seeds.map(()=>new Uint8ClampedArray(src.data.length));
 for(let py=0;py<im.height;py++)for(let px=0;px<im.width;px++){const at=(py*im.width+px)*4;if(src.data[at+3]<16)continue;let best=Infinity,id=0;for(let i=0;i<seeds.length;i++){const d=(px-seeds[i].x)**2+(py-seeds[i].y)**2;if(d<best){best=d;id=i;}}groups[id].set(src.data.subarray(at,at+4),at);}
 for(let i=0;i<groups.length;i++){
  const data=groups[i];let l=im.width,r=0,t=im.height,b=0;for(let py=0;py<im.height;py++)for(let px=0;px<im.width;px++)if(data[(py*im.width+px)*4+3]){l=Math.min(l,px);r=Math.max(r,px);t=Math.min(t,py);b=Math.max(b,py);}
  if(r<l)continue;const full=document.createElement('canvas');full.width=im.width;full.height=im.height;full.getContext('2d').putImageData(new ImageData(data,im.width,im.height),0,0);
  const c=document.createElement('canvas');c.width=Math.ceil((r-l+1)/2)*2;c.height=Math.ceil((b-t+1)/2)*2;c.getContext('2d').drawImage(full,l,t,r-l+1,b-t+1,0,0,r-l+1,b-t+1);
  const dx=(l+r)/2-im.width/2,dy=(t+b)/2-im.height/2,a=Math.atan2(dy,dx)+rotation,speed=110+(i*53%170),cr=Math.cos(rotation),sr=Math.sin(rotation);
  S78.debris.push({owner,stage:run.stage,im:c,x:x+(dx*cr-dy*sr)*k,y:y+(dx*sr+dy*cr)*k,k,vx:baseVX+Math.cos(a)*speed,vy:baseVY+Math.sin(a)*speed-70,rot:rotation,spin:(i%2?1:-1)*(1.1+i*.19),age:0});
 }
 if(S78.debris.length>100)S78.debris.splice(0,S78.debris.length-100);r25Log('authored-shatter',{count:groups.length});
}
v18Rupture=function(b,p){if(rb23Host(b)&&['left','right'].includes(p.id)){
 const q=r25HostSample(b),im=r25Layer(q.name,p.id,q.f),at=rb23PartPoint(b,p,true),side=p.id==='left'?-1:1;
 S78.debris.push({owner:b,stage:8,im,x:b.x,y:b.y,k:360/512,vx:side*100,vy:65,rot:0,spin:side*1.25,age:0,split:.28});
 explode(at.x,at.y,85,'purple');r30Sound('expBig');shake=Math.max(shake,8);r25Log('arm-detached',{part:p.id});return;
 }return S78.base.rupture.apply(this,arguments);};
function r25BodySnapshot(b){const c=document.createElement('canvas');c.width=c.height=320;const g=c.getContext('2d'),N=b._r30.v18;
 if(N.bi24Rolled){const a=ER23_ART.banks.roll,f=Math.floor(b._r30.clock*24)%a.count;g.drawImage(XART.get(a.key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,32,32,256,256);}
 else {const frame=v18Frame(b);for(const a of Object.values(frame))if(XART.rdy(a.key))g.drawImage(XART.get(a.key),0,0,320,320);}return c;}
r30Break=function(b){if(rb23Host(b)&&!rb23Arms(b).length&&b._r30.mode==='fight'){
 const im=r25BodySnapshot(b),r=S78.base.break.apply(this,arguments);r25Shards(b,im,b.x,b.y,.9,28,0,100);return r;}
 return S78.base.break.apply(this,arguments);};
j3FinalDeath=function(b){const im=v18Owned(b)?r25BodySnapshot(b):null,r=S78.base.finalDeath.apply(this,arguments);if(im)r25Shards(b,im,b.x,b.y,1.1,36,0,-65);return r;};
function r25DebrisTick(dt){for(let i=S78.debris.length-1;i>=0;i--){const d=S78.debris[i];d.age+=dt;d.x+=d.vx*dt;d.y+=d.vy*dt;d.vy+=190*dt;d.rot+=d.spin*dt;
 if(d.split&&d.age>=d.split){S78.debris.splice(i,1);r25Shards(d.owner,d.im,d.x,d.y,d.k,14,d.vx,d.vy,d.rot);continue;}
 if(d.stage!==run.stage||d.owner!==boss||d.age>6||d.y>VH+500||d.x<camLeftX()-500||d.x>camRightX()+500)S78.debris.splice(i,1);}}
function r25DebrisDraw(b){for(const d of S78.debris)if(d.owner===b&&d.im){ctx.save();ctx.translate(d.x,d.y);ctx.rotate(d.rot);ctx.imageSmoothingEnabled=false;ctx.drawImage(d.im,-d.im.width*d.k/2,-d.im.height*d.k/2,d.im.width*d.k,d.im.height*d.k);ctx.restore();}}

/* Living veins retain the complete original artwork and its authored colors. */
v17ArenaDraw=function(b){if(!v18Owned(b)||b._r30.v18.arenaPhase!==0||b._r30.mode==='dr5er23entry'&&b._r30.t<1.25)return S78.base.arena.apply(this,arguments);
 const a=PXV17_ART.arenas[0];if(!XART.rdy(a.key))return false;const t=S78.arenaClock,left=camLeftX(),top=viewTopY(),w=viewW(),h=viewH(),k=Math.max((worldWidth()+100)/a.w,(h+100)/a.h),im=XART.get(a.key),cx=worldWidth()/2,cy=top+h/2;
 ctx.save();ctx.beginPath();ctx.rect(left-24,top-24,w+48,h+48);ctx.clip();ctx.fillStyle='#000';ctx.fillRect(left-24,top-24,w+48,h+48);ctx.imageSmoothingEnabled=false;
 const band=4;for(let y=0;y<a.h;y+=band){const wave=Math.sin(y*.027+t*1.25)*2.4+Math.sin(y*.061-t*.73)*1.1;
  ctx.globalAlpha=.56+.055*Math.sin(t*1.7-y*.025);ctx.drawImage(im,0,y,a.w,band,cx-a.w*k/2+wave,cy+(y-a.h/2)*k,a.w*k,band*k+.5);}
 ctx.globalAlpha=1;for(let i=0;i<8;i++){const size=[104,142,180][i%3],x=worldWidth()*((i*.381966+.12)%1),y=top+((i*.173*h+t*(i%2?-1:1)*(9+i*2)+size)%(h+size*2)+(h+size*2))%(h+size*2)-size;
  v17Code(t*15+i*4,x,y,size,.065+.028*Math.sin(t*1.1+i));}
 ctx.restore();j3State(b).aa5ArenaDrawn=true;S78.arenaLast={t,bands:128};return true;
};aa5ArenaDraw=v17ArenaDraw;
updatePlay=function(dt){if(run.stage===8){S78.arenaClock+=clamp(dt||0,0,.05);r25DebrisTick(clamp(dt||0,0,.05));}else if(S78.debris.length)S78.debris=[];return S78.base.update.apply(this,arguments);};

/* Native 24 accelerating sound beats now strike real authored branching bolts.
   Data bands reconstruct the actual fusion plate; reveal remains at 25.6s. */
function r25Bolt(x1,y1,x2,y2,t,alpha=1){const a=R25_ART.lightning,im=r25Frame('lightning',Math.floor(t*22)%a.count);if(!im)return;
 const len=Math.hypot(x2-x1,y2-y1),angle=Math.atan2(y2-y1,x2-x1)-Math.PI/2,k=len/416;
 ctx.save();ctx.translate((x1+x2)/2,(y1+y2)/2);ctx.rotate(angle);ctx.globalCompositeOperation='screen';ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(im,-a.w*k/2,-a.h*k/2,a.w*k,a.h*k);ctx.restore();}
rb23SceneDraw=function(b){const S=b._r30,N=S.v18,t=S.t;if(S.mode==='dr5er23entry'||t<14||t>=25.6)return S78.base.sceneDraw.apply(this,arguments);
 const cx=(camLeftX()+camRightX())/2,cy=viewTopY()+viewH()*.38,R=N.rb23Rebirth,progress=clamp((t-14)/11.2,0,1),a=ER23_ART.banks.fusion,f=t<17?Math.min(8,Math.floor((t-14)/3*9)):8;
 er23Curtain('blackout',15);let c=S78.frames.get('fusion:'+f);
 if(!c&&XART.rdy(a.key)){c=document.createElement('canvas');c.width=c.height=256;c.getContext('2d').drawImage(XART.get(a.key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,0,0,256,256);S78.frames.set('fusion:'+f,c);}
 const spin=(t-14)*(1.8+progress*2.2),settle=clamp((t-24.2)/1.0,0,1),a0=10.2*(1.8+10.2/11.2*2.2),end=TAU*Math.ceil((a0+2)/TAU),u=settle;
 const angle=t<24.2?spin:(2*u*u*u-3*u*u+1)*a0+(u*u*u-2*u*u+u)*5.8+(-2*u*u*u+3*u*u)*end;
 if(c){ctx.save();ctx.translate(cx,cy);ctx.rotate(angle);ctx.imageSmoothingEnabled=false;
  for(let y=0;y<256;y+=4){const order=((y/4)*.61803398875)%1,complete=order<=progress,shift=complete?0:Math.sin(y*.7+t*19)*(7+14*(1-progress));
   ctx.globalAlpha=complete?.35+.65*progress:.06;ctx.drawImage(c,0,y,256,4,-128+shift,y-128,256,4);
   if(complete&&Math.abs(order-progress)<.075){ctx.globalAlpha=.7;ctx.globalCompositeOperation='screen';ctx.drawImage(c,0,y,256,4,-128,y-128,256,4);ctx.globalCompositeOperation='source-over';}}
  ctx.restore();}
 for(let i=0;i<7;i++){const side=i%2?-1:1,x=cx+side*(120+i%3*34),y=cy-180+((t*80+i*73)%350);v17Code(t*20+i*3,x,y,90,.23+progress*.20);}
 if(t>=17){const n=R?.bolts||0,phase=R?.boltPhase||0,beats=t<23?Math.min(3,1+Math.floor(progress*3)):6;
  for(let i=0;i<beats;i++){const theta=(n-i)*2.399963,rx=viewW()*.46,ry=viewH()*.43,x=cx+Math.cos(theta)*rx,y=cy+Math.sin(theta)*ry;
   r25Bolt(x,y,cx+Math.cos(theta+.7)*25,cy+Math.sin(theta+.7)*25,t+i*.15,t<23?(.95-phase*.65)/(1+i*.4):.78);}}
 ctx.save();ctx.font='bold 13px monospace';ctx.textAlign='center';ctx.fillStyle=progress>=1?'#fff':'#aaf6ff';ctx.fillText(progress>=1?'DOWNLOAD COMPLETE':'DOWNLOADING  '+Math.floor(progress*100).toString().padStart(2,'0')+'%',cx,cy+157);ctx.restore();
 if(t>=25.3)er23Curtain('whiteout',Math.floor((t-25.3)/.3*16));S78.downloadLast={progress,angle,bolts:R?.bolts||0,t};
};
rb23SceneTick=function(b,dt){const r=S78.base.sceneTick.apply(this,arguments);if(b._r30.mode==='dr5er23rebirth'&&b._r30.t>=25.2&&!b._r30.v18.rb23Rebirth?.r25Complete){const R=b._r30.v18.rb23Rebirth;if(R){R.r25Complete=true;r25Log('download-complete',{bolts:R.bolts});}}return r;};
r30DrawBoss=function(b){const r=S78.base.bossDraw.apply(this,arguments);if(v18Owned(b))r25DebrisDraw(b);return r;};
window.BOF_STAGE78_REVIEW=S78;

/* Review's small Stage9 bug: the native blue hit plate must share the hull's
   actual rotation, fusion scale and disabled opacity. Mystery HP is unchanged. */
const r25FusionDraw=s9FusionBossDraw;
s9FusionBossDraw=function(b){const F=b?._s9fusion;if(!F||F.phase==='tidal')return r25FusionDraw.apply(this,arguments);
 s9FusionRing(b);for(const w of [F.left,F.right])s9FusionWardenWarningDraw(b,w,false);
 for(const w of [F.left,F.right]){const q=F.phase==='fuse'?clamp(F.t/1.85,0,1):0,scale=F.phase==='fuse'?Math.pow(1-q,1.30):1;if(scale<.03)continue;
  const ratio=w.hp/w.maxhp,key=ratio>.58?'ns9_warpsen_intact':ratio>.24?'ns9_warpsen_damaged':'ns9_warpsen_critical';if(!XART.rdy(key))continue;
  ctx.save();ctx.translate(w.x,w.y);ctx.rotate(w.spin||0);ctx.globalAlpha*=w.disabled&&F.phase==='twins'?.62:1;ctx.imageSmoothingEnabled=false;
  ctx.drawImage(XART.get(key),-w.w*scale/2,-w.h*scale/2,w.w*scale,w.h*scale);
  if(w.flash>0){const hi=xartTint(key,'#8caeff',.60);if(hi){ctx.globalAlpha*=.38*clamp(w.flash/.10,0,1);ctx.drawImage(hi,-w.w*scale/2,-w.h*scale/2,w.w*scale,w.h*scale);}}
  ctx.restore();}
 if(F.phase==='fuse'&&F.t>1.70&&XART.rdy('ns9_tidal_intact')){const r=clamp((F.t-1.70)/.70,0,1),w=320*(.66+.34*r),h=256*(.66+.34*r);ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=r;ctx.drawImage(XART.get('ns9_tidal_intact'),worldWidth()/2-w/2,132-h/2,w,h);ctx.restore();}
 for(const w of [F.left,F.right])s9FusionWardenWarningDraw(b,w,true);return true;
};
