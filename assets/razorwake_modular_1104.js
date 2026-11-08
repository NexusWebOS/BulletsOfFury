'use strict';
/* RW117: intact hinged wings, disjoint rotary guns and authored wind arsenal. */
const RW117={base:{create:fb112Create,keys:fb112Keys,ready:fb112Ready,at:fb112At,opaque:fb112Opaque,bore:fb112Bore,start:fb112Start,tick:fb112Tick,draw:fb112Draw,damage:fb112Damage,cancel:fb112Cancel,projectile:drawCombatFinalProjectile,early:ovSonicProjectileDraw,load:stageLoadBegin,weather:bg6Draw,grade:bg6WeatherGrade,begin:beginStage},bits:null,load:null,owner:null,tickOwner:null,artReady:false,ready:false,loadKeys:null,images:{},events:[],draws:{},keys:Object.keys(RW117_ART.pages)};
for(const[k,p]of Object.entries(RW117_ART.pages))XART._src[k]=p.path;
RW117.keys.push(CF114_ART.banks.small_64.key,CF114_ART.banks.smoke_40.key,RD72_ART.asterisk.key);
FB112_ART.models.razor=RW117_ART.model;
function rw117Own(b){return b?._fb112?.model==='razor'&&b._fb112.M===RW117_ART.model;}
function rw117Warm(){if(!RW117.load)RW117.load=fetch(RW117_ART.maskPath).then(r=>{if(!r.ok)throw Error('Razorwake modular collision '+r.status);return r.arrayBuffer();}).then(a=>{if(a.byteLength!==RW117_ART.maskBytes)throw Error('Razorwake collision size');RW117.bits=new Uint8Array(a);}).catch(e=>console.error(e));}
function rw117Ready(){if(RW117.artReady)return true;if(!RW117.bits||!RW117.keys.every(k=>XART.rdy(k)))return false;for(const k of RW117.keys)RW117.images[k]=XART.get(k);RW117.artReady=true;return true;}
fb112Keys=function(){rw117Warm();return RW117.loadKeys||(RW117.loadKeys=[...RW117.base.keys(),...RW117.keys]);};
fb112Ready=function(){return RW117.ready||(RW117.ready=RW117.base.ready()&&rw117Ready());};
stageLoadBegin=function(n,keys){RW117.ready=RW117.artReady=false;RW117.images={};if(n===6&&fb112Rank())keys=[...(keys||[]),...fb112Keys()];return RW117.base.load.call(this,n,keys);};
function rw117State(b){return b._rw117||(b._rw117={clock:0,wing:0,spin:0,spinRate:0,next:0,pulses:0,release:-1,weather:.3,tornadoes:[],detached:[],open:false,serial:0});}
function rw117Log(b,event,data={}){RW117.events.push({event,t:b.t,id:b._fb112.id,attack:b._fb112.attack,seq:b._fb112.seq,...data});if(RW117.events.length>1500)RW117.events.shift();fb112Log(b,'razor-'+event,data);}
fb112Create=function(model,sub){const b=RW117.base.create.apply(this,arguments);if(model==='razor'){b._fb112.scale=1;rw117State(b);RW117.owner=b;Snd.prepare(['enemyMachineGunHeavy','bossWeaponCharge','overlordWind','combatEnergy0927','combatModule0927','jetDash','expBig']);l23FovWarm();rw117Log(b,'assembly',{hp:b.hp,parts:b._fb112.parts.map(p=>({id:p.id,hp:p.hp}))});}return b;};
function rw117Dir(a){return fb112Dir(a,32);}
function rw117Blit(name,f,x,y){const B=RW117_ART.banks[name];if(!B)return false;f=clamp(f|0,0,B.frames-1);const c=B.cells[f];if(!c||!RW117.images[c[0]])return false;ctx.drawImage(RW117.images[c[0]],c[1],c[2],c[3],c[4],Math.round(x)-B.pivot[0]+c[5],Math.round(y)-B.pivot[1]+c[6],c[3],c[4]);RW117.draws[name]=(RW117.draws[name]||0)+1;return true;}
function rw117Mask(name,f,cx,cy,x,y){const B=RW117_ART.banks[name],m=RW117_ART.masks[name]?.[f];if(!B||!m||!RW117.bits)return false;const px=Math.floor(x-cx+B.pivot[0])-m[0],py=Math.floor(y-cy+B.pivot[1])-m[1];if(px<0||py<0||px>=m[2]||py>=m[3])return false;const bit=py*m[2]+px;return !!(RW117.bits[m[4]+(bit>>3)]&(1<<(bit&7)));}
function rw117GunFrame(b,p){return(p.recoil>.035?8:0)*32+(Math.floor(rw117State(b).spin)%8)*32+rw117Dir(p.angle);}
fb112At=function(b,x,y,pad=0){if(!rw117Own(b))return RW117.base.at.apply(this,arguments);if(!fb112Visible(b))return null;const q=b._fb112;let best=null,score=Infinity;for(const p of fb112LiveParts(b)){const at=fb112PartPoint(b,p),core=p===q.core,rx=(core?26:20)+pad,ry=(core?38:45)+pad,v=((x-at.x)/rx)**2+((y-at.y)/ry)**2;const mask=core?rw117Mask('hull',rw117Dir(q.heading),b.x,b.y,x,y):rw117Mask('gun',rw117GunFrame(b,p),at.x,at.y,x,y);if(v<=1&&v<score&&mask){best=p;score=v;}}return best;};
// The retained real-depth whole-craft roll uses its original fixed world scale.
fb112Opaque=function(name,f,a,k,cx,cy,x,y){if(name==='razor_roll'&&rw117Own(RW117.tickOwner))k=250/384;return RW117.base.opaque.call(this,name,f,a,k,cx,cy,x,y);};
fb112Bore=function(b,p){if(!rw117Own(b))return RW117.base.bore.apply(this,arguments);const at=fb112PartPoint(b,p),a=fb112Angle(p.angle??b._fb112.heading)-Math.PI/2,x=p.bore[0],y=p.bore[1]+(p.recoil>.035?-3:0);return{x:at.x+x*Math.cos(a)-y*Math.sin(a),y:at.y+x*Math.sin(a)+y*Math.cos(a)};};
fb112Damage=function(b){if(!rw117Own(b))return RW117.base.damage.apply(this,arguments);const q=b._fb112,S=rw117State(b),hp=q.parts.map(p=>p.hp),open=q.open,out=RW117.base.damage.apply(this,arguments);q.parts.forEach((p,i)=>{if(hp[i]>0&&p.hp<=0){const at=fb112PartPoint(b,p);S.detached.push({x:at.x,y:at.y,vx:p.index?85:-85,vy:30,t:0,angle:p.angle,spin:Math.floor(S.spin)%8,part:p.id});rw117Log(b,'gun-detach',{part:p.id,x:at.x,y:at.y});if(q.attack==='pass'&&!b.dead){fb112Set(b,'recover');q.wait=2.4;q.attack=null;}}});if(!open&&q.open){S.tornadoes=[];for(const r of eBullets)if(r._rw117Owner===b)r.dead=true;rw117Log(b,'core-exposed',{hp:q.core.hp});}return out;};
function rw117Charge(b){if(b.dead)return 0;const q=b._fb112;return q.phase==='warn'&&['wind-cyclone','wing-storm'].includes(q.attack)?clamp(q.t/q.dur,0,1):q.phase==='attack'&&['wind-cyclone','wing-storm'].includes(q.attack)?Math.max(0,1-q.t/1.25):0;}
function rw117Glow(b){const q=b._fb112,p=rw117Charge(b),phase=q.phase==='warn'?8*q.t+18*q.t*q.t/Math.max(.01,q.dur):rw117State(b).clock*20;return p>0?Math.min(5,1+Math.floor(p*3)+(Math.floor(phase)%2)):0;}
fb112Start=function(b){if(!rw117Own(b))return RW117.base.start.apply(this,arguments);const q=b._fb112,S=rw117State(b),both=q.parts.every(p=>p.hp>0);q.seq++;const book=q.open?['wind-cyclone','wing-storm']:both?['rotary','pass','wind-cyclone','wing-storm']:['rotary','wind-cyclone','wing-storm'];q.attack=book[(q.seq-1)%book.length];fb112Set(b,q.attack==='pass'?'depart':'warn');q.dur=q.attack==='wing-storm'?3.6:q.attack==='wind-cyclone'?1.9:1.05;
 const T=targetShip(b.x,b.y);q.target={x:clamp(T.x,camLeftX()+55,camRightX()-55),y:clamp(T.y,245,VH-45)};q.dir=q.seq%2?1:-1;q.passFrom={x:q.dir>0?camLeftX()-155:camRightX()+155,y:clamp(T.y-35,145,VH-115)};q.passTo={x:q.dir>0?camRightX()+155:camLeftX()-155,y:clamp(T.y+35,200,VH-70)};q.parts.forEach(p=>p.angle=q.heading);S.next=0;S.pulses=0;S.release=-1;combatAudio0927(b,q.attack==='pass'?'jetDash':'bossWeaponCharge',.4);rw117Log(b,'charge',{duration:q.dur,target:q.target});};
function rw117Shot(b,p,angle,kind='slug'){if(p?.hp<=0)return;const at=p?fb112Bore(b,p):fb112PartPoint(b,b._fb112.core),a=fb112Angle(angle),r=eShootT(at.x,at.y,a,kind==='slug'?5.0:2.8,'l6bolt',{owner:b,silent:true,noMuzzle:true,w:kind==='slug'?26:140,h:kind==='slug'?50:160});Object.assign(r,{_rw117Owner:b,_rw117Kind:kind,_rw117Born:b.t,_rw117Angle:a,_fb112Owner:b,_fb112Part:p,_fb112Born:b.t,_weaponProof:true,_shootable:false,_noArsenal:true,_boss:true});if(p){p.recoil=.07;p._rwMuzzle=.07;}rw117Log(b,'round',{part:p?.id,kind,x:at.x,y:at.y,angle:a});}
function rw117Release(b){const q=b._fb112,S=rw117State(b);S.release=q.seq;rw117Log(b,'release');if(q.attack==='wing-storm'){const at=fb112PartPoint(b,q.core),sign=q.target.x<at.x?-1:q.target.x>at.x?1:q.dir;S.tornadoes.push({x:at.x,y:at.y+60,vx:sign*215,vy:148,t:0,life:5.4,bounces:0,hits:new Set()});combatAudio0927(b,'overlordWind',.3);rw117Log(b,'tornado-launch',{x:at.x,y:at.y+60});}}
fb112Cancel=function(b){const out=RW117.base.cancel.apply(this,arguments);if(rw117Own(b)){const S=rw117State(b);S.tornadoes=[];S.spinRate=0;for(const p of b._fb112.parts){p._rwMuzzle=0;}for(const r of eBullets)if(r._rw117Owner===b)r.dead=true;}return out;};
beginStage=function(){if(RW117.owner)fb112Cancel(RW117.owner);RW117.owner=null;return RW117.base.begin.apply(this,arguments);};
function rw117Fields(b,dt){const S=rw117State(b);for(const f of S.tornadoes){f.t+=dt;if(b.dead){f.dead=true;continue;}if(f.t<f.life-.35){f.x+=f.vx*dt;f.y+=f.vy*dt;const l=camLeftX()+70,r=camRightX()-70,top=viewTopY()+95,bot=VH-70;if(f.x<l||f.x>r){f.x=clamp(f.x,l,r);f.vx=-f.vx;f.bounces++;}if(f.y<top||f.y>bot){f.y=clamp(f.y,top,bot);f.vy=-f.vy;f.bounces++;}if(f.t>.2)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&player.invuln<=0&&f.t-((f.hitAt&&f.hitAt.get(seat))??-99)>.7&&((player.x-f.x)/40)**2+((player.y-f.y)/62)**2<1){f.hits.add(seat);if(!f.hitAt)f.hitAt=new Map();f.hitAt.set(seat,f.t);playerHit('Razorwake wing tornado');rw117Log(b,'tornado-contact',{seat});}});}if(f.t>=f.life){f.dead=true;rw117Log(b,'tornado-expired',{bounces:f.bounces});}}S.tornadoes=S.tornadoes.filter(f=>!f.dead);}
fb112Tick=function(b,dt){if(!rw117Own(b))return RW117.base.tick.apply(this,arguments);if(!rw117Ready()){stageLoadTick();return;}const q=b._fb112,S=rw117State(b),before=b.t;RW117.tickOwner=b;let out;try{out=RW117.base.tick.apply(this,arguments);}finally{RW117.tickOwner=null;}if(b.t===before)return out;RW117.owner=b;S.clock+=dt;
 for(const f of S.detached){f.t+=dt;f.x+=f.vx*dt;f.y+=f.vy*dt;f.vy+=140*dt;f.angle+=dt*3.2;}S.detached=S.detached.filter(f=>f.t<1.7&&f.y<VH+120);
 const rotor=q.attack==='rotary'&&['warn','attack'].includes(q.phase),targetSpin=rotor?(q.phase==='warn'?12+q.t/q.dur*60:90):0;S.spinRate+=clamp(targetSpin-S.spinRate,-dt*150,dt*140);S.spin+=S.spinRate*dt;
 for(const p of q.parts)p._rwMuzzle=Math.max(0,(p._rwMuzzle||0)-dt);
 const flapping=q.attack==='wing-storm'&&['warn','attack'].includes(q.phase);if(flapping)S.wing+=dt*(q.phase==='warn'?10+56*clamp(q.t/q.dur,0,1):30);else S.wing+=Math.min(1,dt*9)*(Math.ceil(S.wing/24)*24-S.wing);
 const weather=b.dead?0:rw117Charge(b)>0?.95:q.phase==='attack'&&q.attack==='wing-storm'?.8:.32;S.weather+=clamp(weather-S.weather,-dt*.45,dt*.65);
 if(b.dead){S.tornadoes=[];return out;}rw117Fields(b,dt);
 if(q.phase==='warn'&&q.attack==='rotary'&&q.t<q.dur*.82)for(const p of q.parts.filter(p=>p.hp>0)){const at=fb112PartPoint(b,p),target=Math.PI/2+clamp(Math.atan2(q.target.y-at.y,q.target.x-at.x)-Math.PI/2,-.55,.55);p.angle=fb112Angle(target);}
 if(q.phase!=='attack')return out;if(S.release!==q.seq)rw117Release(b);
 if(q.attack==='rotary'){
  if(q.t>=S.next&&q.t<1.75){for(const p of q.parts.filter(p=>p.hp>0))rw117Shot(b,p,p.angle);combatAudio0927(b,'enemyMachineGunHeavy',.09);S.next+=turretInterval15(.095);}
  if(q.t>2.1){fb112Set(b,'recover');q.wait=1.0;}
 }else if(q.attack==='wind-cyclone'){
  if(q.t>=S.next&&S.pulses<3){for(const d of[-.22,.22])rw117Shot(b,null,Math.PI/2+d,'cyclone');S.pulses++;S.next+=.6;combatAudio0927(b,'overlordWind',.3);}
  if(q.t>3.2){fb112Set(b,'recover');q.wait=1.1;}
 }else if(q.attack==='wing-storm'&&q.t>5.5&&S.tornadoes.length===0){fb112Set(b,'recover');q.wait=1.2;}
 return out;
};
function rw117RoundDraw(r){if(!r?._rw117Owner)return false;if(r.dead)return true;const age=r._rw117Owner.t-r._rw117Born;if(r._rw117Kind==='cyclone')return rw117Blit('cyclone',Math.floor(age*24)%16,r.x,r.y);return rw117Blit('slug',(1+Math.floor(age*22)%3)*32+rw117Dir(r._rw117Angle),r.x,r.y);}
drawCombatFinalProjectile=function(r){return r?._rw117Owner?rw117RoundDraw(r):RW117.base.projectile.apply(this,arguments);};
ovSonicProjectileDraw=function(r){return r?._rw117Owner?rw117RoundDraw(r):RW117.base.early.apply(this,arguments);};
function rw117Wings(b,mode='normal'){const q=b._fb112,S=rw117State(b),dir=rw117Dir(q.heading),south=dir===0,pose=Math.floor(S.wing)%24,hot=rw117Charge(b)>0&&south,level=rw117Glow(b);for(const side of['left','right'])rw117Blit(side+(mode==='shadow'?'_shadow':mode==='hit'?'_hit':hot?'_charge':''),hot&&mode==='normal'?level*24+pose:south?32+pose:dir,b.x,b.y+(mode==='shadow'?28:0));}
function rw117Warnings(b){const q=b._fb112;if(b.dead||q.phase!=='warn')return;const progress=q.t/q.dur,at=fb112PartPoint(b,q.core);if(q.attack==='rotary')for(const p of q.parts.filter(p=>p.hp>0))fb112Warn(b,p,p.angle,q.t,q.dur,22);
 else if(q.attack==='wind-cyclone')for(const d of[-.22,.22])combatWarningDraw(b,{x:at.x,y:at.y,ex:at.x+Math.cos(Math.PI/2+d)*640,ey:at.y+Math.sin(Math.PI/2+d)*640,width:50,progress,fieldOnly:true});
 else if(q.attack==='pass')combatWarningDraw(b,{x:q.passFrom.x,y:q.passFrom.y,ex:q.passTo.x,ey:q.passTo.y,width:250,progress,fieldOnly:true});
 if(q.attack==='wing-storm'||q.attack==='wind-cyclone'){const red=progress>=2/3,visible=!red||Math.floor(q.t*12)%2===0;if(visible){const y=Math.max(viewTopY()+70,b.y-115);rd72Blit('asterisk',red?1:0,b.x,y);RW117.draws.warning=(RW117.draws.warning||0)+1;RW117.warning={x:b.x,y,red};}}
}
fb112Draw=function(b){if(!rw117Own(b))return RW117.base.draw.apply(this,arguments);if(!rw117Ready())return;const q=b._fb112,S=rw117State(b),dir=rw117Dir(q.heading),level=rw117Glow(b),hot=rw117Charge(b)>0&&dir===0,rolling=fb112Rolling(b);
 if(!b.dead&&rw117Charge(b)>0){rw117Blit('swirl',Math.floor(S.clock*24)%16,b.x,b.y-38);rw117Blit('swirl',(Math.floor(S.clock*24)+8)%16,b.x,b.y+35);}
 if(!b.dead&&q.phase==='warn'&&q.attack==='wing-storm'&&q.t>q.dur-.95){const at=fb112PartPoint(b,q.core);rw117Blit('tornado_grow',Math.min(7,Math.floor((q.t-(q.dur-.95))/.95*8)),at.x,at.y+60);}
 if(q.death<3){
  if(rolling){fb112Shadow('razor_roll',fb112RollFrame(b),b.x,b.y+42,250/384*.9,q.heading);fb112Blit('razor_roll',fb112RollFrame(b),b.x,b.y,250/384,q.heading);}
  else{rw117Blit('hull_shadow',dir,b.x,b.y+28);rw117Wings(b,'shadow');rw117Blit(hot?'hull_charge':'hull',hot?level:dir,b.x,b.y);rw117Wings(b);if(q.open&&q.core.flash>0){rw117Blit('hull_hit',dir,b.x,b.y);rw117Wings(b,'hit');}
   for(const p of q.parts){const at=fb112PartPoint(b,p),d=rw117Dir(p.angle);rw117Blit(p.hp<=0?'gun_wreck':p.flash>0?'gun_hit':hot?'gun_charge':'gun',p.hp<=0?d:hot&&p.flash<=0?level:rw117GunFrame(b,p),at.x,at.y);if(p.hp<=0){const B=CF114_ART.banks.smoke_40;cf114Blit(ctx,'smoke_40',cf114Frame(B,S.clock%.9,.9),at.x,at.y-12);}if(p.hp>0&&p._rwMuzzle>0){const m=fb112Bore(b,p);rw117Blit('muzzle',(1+Math.floor(S.clock*48)%3)*32+d,m.x,m.y);}}
  }
  if(!b.dead)for(const e of q.M.engines){const roll=rolling?Math.cos(Math.max(0,q.M.clips.roll.indexOf(q.pose))*TAU/8):1,at=fb112Point(b,[192+(e[0]-192)*roll,e[1]]),throttle=['depart','attack'].includes(q.phase)&&q.attack==='pass';rw117Blit(throttle?'thrust_throttle':'thrust_cruise',(1+Math.floor(S.clock*20)%5)*32+dir,at.x,at.y);}
 }
 for(const f of S.detached)rw117Blit('gun',f.spin*32+rw117Dir(f.angle),f.x,f.y);

 for(const f of S.tornadoes)rw117Blit(f.t>f.life-.35?'tornado_tail':'tornado',f.t>f.life-.35?Math.min(7,Math.floor((f.t-f.life+.35)/.35*8)):Math.floor(f.t*24)%16,f.x,f.y);
 for(const f of q.fx){const B=CF114_ART.banks.small_64;cf114Blit(ctx,'small_64',cf114Frame(B,f.t,.6),f.x,f.y);}
 rw117Warnings(b);if(b.sub&&!b.dead)drawSubBossBar(b);
};
function rw117Weather(){const b=RW117.owner;if(run.stage!==6||b!==subBoss||!rw117Own(b)||b._fb112.death>3)return false;const S=rw117State(b),t=S.clock,grade=clamp(Math.round(S.weather*6),1,6);for(let y=128;y<650;y+=256)for(let x=170;x<worldWidth()+340;x+=340)th114Blit('grade',grade,x,y);for(let i=0;i<3;i++){th114Blit('cloud_far',Math.floor(t*3+i)%6,((i*265+t*9)%(worldWidth()+288))-144,65+i*185);th114Blit('cloud_near',Math.floor(t*4+i*2)%6,((i*435-t*17)%(worldWidth()+384)+worldWidth()+384)%(worldWidth()+384)-192,150+i*135);}for(let y=128;y<650;y+=256)for(let x=170;x<worldWidth()+340;x+=340)th114Blit('rain',(S.weather>.65?8:0)+Math.floor(t*24)%8,x,y);return true;}
bg6Draw=function(){return rw117Weather()?undefined:RW117.base.weather.apply(this,arguments);};
bg6WeatherGrade=function(){if(run.stage===6&&rw117Own(subBoss)&&!subBoss.dead)return;return RW117.base.grade.apply(this,arguments);};
globalThis.BOF_RAZORWAKE_MODULAR_1104={state:RW117,owns:rw117Own};
