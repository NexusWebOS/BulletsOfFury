"use strict";
const SW28={base:{init:s7mInit,stage:s7mStage,next:s7mNext,set:s7mSet,tick:s7mTick,pose:s7mPose,move:s7mMove,
 at:s7mAt,hit:s7mHit,targets:s7mTargets,blit:s7mBlit,draw:s7mDraw,muzzle:s7mMuzzle,shot:s7mShot,cell:s7mCell,update:updatePlay,warnings:s7mWarnings,projectile:drawCombatFinalProjectile},actor:null,mortars:[],events:[]};
s7mCell=function(name,i,trim){if(typeof i==='string'&&i.startsWith('er28rear_')){const [,id,frame]=i.split('_'),a=ER28_ART[id],key='er28cell:'+i;let c=SW28[key];if(!c&&XART.rdy(a.key)){c=document.createElement('canvas');c.width=c.height=256;c.getContext('2d').drawImage(XART.get(a.key),+frame%a.cols*a.cw,Math.floor(+frame/a.cols)*a.ch,a.cw,a.ch,0,0,256,256);SW28[key]=c;}return c||null;}return SW28.base.cell.apply(this,arguments);};
function sw28Can(M){return(M.er28Canisters||[]).filter(p=>p.hp>0);}
s7mInit=function(b){const M=SW28.base.init.apply(this,arguments);if(!M.tank&&!M.er28Canisters){
 M.er28Canisters=['canL','canR'].map(id=>({id,hp:M.shield/2,max:M.shieldMax/2,flash:0,dead:false}));M.er28Serial=0;
 if(run.ngplus)for(const c of M.er28Canisters)NG27.scaled.set(c,{max:c.max});
 }return M;};
function sw28Limbs(M){return s7mLive(M,'front').length+s7mLive(M,'rear').length;}
s7mMove=function(b,tx,ty,speed,dt){const M=b._s7mod;if(!M.tank){tx=worldWidth()/2;ty=clamp(ty,235,Math.max(236,VH*.61));}return SW28.base.move.call(this,b,tx,ty,speed,dt);};
s7mSet=function(b,mode){const out=SW28.base.set.apply(this,arguments),M=b._s7mod;
 if(!M.tank&&M.mode==='jump'){M.target.x=worldWidth()/2;M.target.y=clamp(M.target.y,235,VH*.61);if(M.landing){M.landing.x=M.target.x;M.landing.y=M.target.y+55;}}
 if(mode.startsWith('er28-')){M.er28Serial=(M.er28Serial||0)+1;M.warn=mode==='er28-bounce'?.85:mode==='er28-mortar'?1.05:.9;M.live=mode==='er28-guns'?2.5:2.9;M.er28={t:0,cd:0,round:0,impact:-1,from:{x:b.x,y:b.y},angle:Math.atan2(player.y-b.y-60,player.x-b.x),target:{x:player.x,y:player.y}};}
 if(mode==='er23-surge'){M.warn=M.n===2?.80:1.05;M.er23Origin={x:b.x,y:b.y};M.er23Aim={x:player.x,y:player.y};M.er23Angle=Math.atan2(player.y-b.y,player.x-b.x);M.er23Pass=0;M.er23Shots=0;M.er23Hit=new Set();}
 return out;};
s7mNext=function(b){const M=b._s7mod;if(M.tank){
 if(M.n===2&&!M.od&&b.hp<=b.maxhp*.5)return SW28.base.next.apply(this,arguments);
 const armed=s7mLive(M,'gun').length>0,book=armed?['er28-guns','er28-mortar','er28-guns','er23-surge','er28-mortar']:['er28-mortar','er23-surge','er28-mortar'];
 const pool=book.filter(k=>k!==M.er28Last);if(Math.abs(player.x-b.x)<75&&M.er28Last!=='er23-surge')pool.push('er23-surge');const pick=pool[Math.floor(er23Random(M)*pool.length)];M.er28Last=pick;M.seq++;return s7mSet(b,pick);}
 const limbs=sw28Limbs(M),book=limbs?['chase','swipeL','er28-guns','er28-mortar','swipeX','swipeR']:
 sw28Can(M).length?['er28-guns','er28-mortar','orbs']:['er28-bounce','er28-core-burst','er28-bounce'];
 let mode=book[M.seq++%book.length];if(mode==='er28-guns'&&!s7mLive(M,'gun').length)mode='er28-core-burst';return s7mSet(b,mode);
};
s7mPose=function(b){const out=SW28.base.pose.apply(this,arguments),M=b._s7mod;
 for(const p of out){
  if(p.id==='gunL'||p.id==='gunR'){
   const sign=p.id==='gunL'?-1:1,active=M.mode==='er28-guns',A=M.er28;
   const angle=active&&A?A.angle+Math.sin(Math.max(0,M.t-M.warn)*2.4+sign)*.22:Math.atan2(player.y-b.y-50,player.x-b.x-sign*(M.tank?43:34));
   p.a=clamp(angle-Math.PI/2,-1.05,1.05);const forward=M.tank?43:38,hip={x:sign*(M.tank?43:34),y:M.tank?22:12};
   p.x=hip.x-Math.sin(p.a)*forward;p.y=hip.y+Math.cos(p.a)*forward;p.w=M.tank?67:38;p.h=M.tank?105:84;
  }
  if(!M.tank&&p.id.startsWith('can')){p.w=46;p.h=88;}
  if(!M.tank&&p.id==='mask'){const lift=M.mode==='er28-core-burst'||!sw28Limbs(M)?1:Math.min(1,M.mask||0);p.y=60-lift*43;}
  if(!M.tank&&p.id.startsWith('rear')){
   const row=R25_ART.legs[p.id],f=p.frame||0,meta=row.frames[f],k=row.worldScale,side=p.id==='rearL'?-1:1,a=side*.60,
    pivot={x:row.pivot[0],y:256-row.pivot[1]},hip={x:side*64,y:-50},dx=(128-pivot.x)*k,dy=(128-pivot.y)*k;
   p.a=a;p.x=hip.x+dx*Math.cos(a)-dy*Math.sin(a);p.y=hip.y+dx*Math.sin(a)+dy*Math.cos(a);p.cell='er28rear_'+p.id+'_'+f;p.frame=f;p.r25=true;
   const tx=(meta.target[0]-128)*k,ty=(256-meta.target[1]-128)*k;
   p.target={x:p.x+tx*Math.cos(a)-ty*Math.sin(a),y:p.y+tx*Math.sin(a)+ty*Math.cos(a)};
  }
 }
 return out;};
s7mMuzzle=function(b,id){const M=b._s7mod;if(id==='dorsal')return s7mWorld(b,{x:0,y:M.tank?-39:-77});
 if(id==='emitter')return{...s7mWorld(b,{x:0,y:26}),a:Math.PI/2};
 if(!['gunL','gunR'].includes(id))return SW28.base.muzzle.apply(this,arguments);
 const p=s7mPose(b).find(q=>q.id===id),q=s7mWorld(b,p),a=p.a+M.lean,reach=M.tank?46:37;
 return{x:q.x-Math.sin(a)*reach,y:q.y+Math.cos(a)*reach,a:Math.PI/2+a};};
function sw28Bank(b,p){const M=b._s7mod;if(p.id==='gunL'||p.id==='gunR')return{name:M.tank?'tank_gun':'warden_gun',f:er28Dir(p.a+M.lean)+(M.mode==='er28-guns'?Math.floor(M.clock*32)%4:0)*64};
 if(!M.tank&&p.id.startsWith('rear'))return{name:p.id+'_fixed',f:p.frame||0};
 if(!M.tank&&p.id.startsWith('front')&&p.r25)return{name:p.id+'_swat',f:(p.frame||0)*17+Math.round((clamp(p.a,-.8,.8)+.8)/.1)};
 if(!M.tank&&p.id.startsWith('can'))return{name:'canister',f:Math.floor(M.clock*20+(p.id==='canL'?0:8))%16};
 if(!M.tank&&['body','core'].includes(p.id))return{name:'core',f:Math.floor(M.clock*20)%16};return null;}
s7mAt=function(b,x,y){const M=b._s7mod;if(!M||['portal','entry','roar','dead','jump','overdrive'].includes(M.mode))return null;
 for(const p of s7mPose(b).slice().reverse()){
  const part=M.parts.find(q=>q.id===p.id)||M.er28Canisters?.find(q=>q.id===p.id);if(part&&part.hp<=0)continue;
  if(!part&&!['body','core'].includes(p.id))continue;const q=s7mWorld(b,p),bank=sw28Bank(b,p);
  if(bank){if(er28AlphaAt(bank.name,bank.f,x-q.x,y-q.y)){if(!part&&!M.tank&&(sw28Can(M).length||sw28Limbs(M)))continue;return part?part.id:'core';}}
  else{const a=p.a+M.lean,dx=(x-q.x)*Math.cos(a)+(y-q.y)*Math.sin(a),dy=-(x-q.x)*Math.sin(a)+(y-q.y)*Math.cos(a);if(Math.abs(dx)<p.w*.48&&Math.abs(dy)<p.h*.48)return part?part.id:'core';}
 }return null;};
s7mHit=function(b,dmg,x,y,id){const M=b._s7mod;id=id||s7mAt(b,x,y);if(!M.tank&&M.er28Canisters){
 const part=M.er28Canisters.find(p=>p.id===id);
 if(part){if(!Number.isFinite(dmg)||dmg<=0||['portal','entry','dead'].includes(M.mode))return true;
  part.hp=Math.max(0,part.hp-dmg);markHit(part,.16);markHit(b,.10);M.shield=M.er28Canisters.reduce((s,p)=>s+p.hp,0);
  if(part.hp===0&&!part.dead){part.dead=true;const pose=s7mPose(b).find(p=>p.id===id),q=s7mWorld(b,pose);s7mFX(q.x,q.y,110,true);s7mSound('expBig');er28Log('toxic-canister-destroyed',{id});}
  s7mSyncHP(b);return true;
 }
 if(id==='core'&&sw28Can(M).length){M.shieldFlash=.16;markHit(b,.1);weaponHitSfx('shield');er28Log('toxic-core-protected',{remaining:sw28Can(M).map(p=>p.id)});return true;}
 }return SW28.base.hit.call(this,b,dmg,x,y,id);};
s7mTargets=function(b){const M=b._s7mod,base=SW28.base.targets.apply(this,arguments);if(M.tank||!M.er28Canisters)return base;
 const ids=new Set(base.filter(q=>!/core/.test(String(q._retinaId||q.id))).map(q=>q));
 if(!sw28Limbs(M))for(const c of sw28Can(M))ids.add(retinaDynamicPiece(b,c.id,'toxic canister',()=>{
  const p=s7mPose(b).find(p=>p.id===c.id);return{...s7mWorld(b,p),hp:c.hp,dead:b.dead||c.hp<=0};
 },d=>s7mHit(b,d,0,0,c.id),46,88));
 if(!sw28Can(M).length)for(const q of base)ids.add(q);return [...ids];};
s7mBlit=function(name,i,x,y,w,h,rot,alpha,flash){const b=SW28.actor;if(!b)return SW28.base.blit.apply(this,arguments);const M=b._s7mod;
 if(!M.tank&&alpha!==1&&(name==='body'||name==='warden'&&i===6))return true;
 if(name==='tank'&&i===1||name==='warden'&&i===5){const f=er28Dir(rot)+(M.mode==='er28-guns'?Math.floor(M.clock*32)%4:0)*64,p=M.parts.find(p=>p.id===(x<b.x?'gunL':'gunR'));return er28Blit(M.tank?'tank_gun':'warden_gun',f,x,y,p?.flash>0);}
 if(!M.tank&&typeof i==='string'&&i.startsWith('er28rear_')){const a=i.split('_'),id=a[1],f=+a[2];return er28Blit(id+'_fixed',f,x,y,M.parts.find(p=>p.id===id)?.flash>0);}
 if(!M.tank&&typeof i==='string'&&/r25_leg_front/.test(i)){const id=i.includes('frontL')?'frontL':'frontR',frame=+(i.match(/_(\d+)$/)?.[1]||0),angle=Math.round((clamp(rot,-.8,.8)+.8)/.1);return er28Blit(id+'_swat',frame*17+angle,x,y,M.parts.find(p=>p.id===id)?.flash>0);}
 if(!M.tank&&name==='body'&&i===0)return er28Blit('core',Math.floor(M.clock*20)%16,x,y,M.coreFlash>0);
 if(!M.tank&&name==='warden'&&i===6){const id=x<b.x?'canL':'canR',p=M.er28Canisters?.find(p=>p.id===id);if(p?.hp<=0)return true;return er28Blit('canister',Math.floor(M.clock*20+(id==='canL'?0:8))%16,x,y,p?.flash>0);}
 return SW28.base.blit.apply(this,arguments);};
s7mDraw=function(b){const prev=SW28.actor;SW28.actor=b;try{return SW28.base.draw.apply(this,arguments);}finally{SW28.actor=prev;}};
function sw28Common(b,dt){const M=b._s7mod;M.t+=dt;M.clock+=dt;M.shotCD-=dt;M.counter=Math.max(0,M.counter-dt);b.flash=Math.max(0,b.flash-dt);
 M.coreFlash=Math.max(0,(M.coreFlash||0)-dt);M.shieldFlash=Math.max(0,(M.shieldFlash||0)-dt);for(const p of [...M.parts,...(M.er28Canisters||[])])p.flash=Math.max(0,(p.flash||0)-dt);
 if(!M.tank){b._s7warden.noHit=false;b._s7warden.final.phase='fight';b._s7FinalNoBar=false;b._s7warden.final.t=M.t;}
}
function sw28Budget(b){return eBullets.filter(q=>q._s7modOwner===b&&!q.dead).length<128;}
function sw28Slug(b,id){if(!sw28Budget(b))return;const q=s7mMuzzle(b,id),shot=eShootT(q.x,q.y,q.a,4.7+b._s7mod.n*.2,'s7shard',{owner:b,noMuzzle:true,silent:true,w:7,h:14});
 Object.assign(shot,{_er28Slug:true,_s7modOwner:b,_weaponProof:true,_shootable:false,_noArsenal:true,_boss:true});
 navalFlash(null,q,.6,'weapon_muzzle_toxic',{n:4,hpx:28,life:.09,follow:()=>s7mLive(b._s7mod,'gun').some(p=>p.id===id)?s7mMuzzle(b,id):null});}
function sw28Orb(b,x,y,a,speed=2.7){if(!sw28Budget(b))return null;const q=eShootT(x,y,a,speed,'s7acid',{owner:b,noMuzzle:true,silent:true,w:18,h:18});Object.assign(q,{_er28Orb:true,_s7modOwner:b,_weaponProof:true,_shootable:false,_noArsenal:true,_boss:true});return q;}
function sw28Mortars(b){const M=b._s7mod,A=M.er28,count=3+M.n,p=s7mMuzzle(b,'dorsal'),l=camLeftX()+52,r=camRightX()-52;
 for(let i=0;i<count;i++){const x=lerp(l,r,(i+.5)/count),target={x,y:clamp(A.target.y+(i%2?25:-25),viewTopY()+230,VH-70)},flight=1.05+i*.08,
 q=sw28Orb(b,p.x,p.y,Math.PI/2,0);if(!q)continue;q.vx=q.vy=0;q._er28Mortar=true;
 SW28.mortars.push({q,b,t:0,flight,start:{...p},target,arc:95+(i%2)*30});
 const mark=groundTargetingSpawn({kind:'missile',owner:b,x,y:target.y,warn:flight,active:.2,radius:27,size:62,track:false,shake:0,onImpact:()=>{}});mark._late27=true;
 }combatAudio0927(b,'combatToxic0927',.4);er28Log('dorsal-mortar-volley',{count,x:p.x,y:p.y});
}
s7mTick=function(b,dt){const M=b?._s7mod;if(!M)return SW28.base.tick.apply(this,arguments);const custom=M.mode.startsWith('er28-');
 let result;if(!custom)result=SW28.base.tick.apply(this,arguments);else{
  sw28Common(b,dt);const A=M.er28,u=M.t-M.warn;M.lean=0;
  if(M.t<M.warn){combatWarningTick(b,'er28-'+M.mode+'-'+M.er28Serial,M.t,M.warn);}
  else if(M.mode==='er28-guns'){
   A.cd-=dt;if(A.cd<=0){A.cd+=(M.n===2?.075:.095);for(const p of s7mLive(M,'gun'))sw28Slug(b,p.id);A.round++;if(A.round%3===1)combatAudio0927(b,'enemyMachineGunHeavy',.22);}
   if(u>2.5)s7mSet(b,'recover');
  }else if(M.mode==='er28-mortar'){
   A.cd-=dt;if(A.cd<=0&&A.round<3){A.cd=.62;A.round++;sw28Mortars(b);}if(u>2.7)s7mSet(b,'recover');
  }else if(M.mode==='er28-core-burst'){
   M.mask=Math.min(1,(M.mask||0)+dt*3);A.cd-=dt;if(A.cd<=0&&A.round<4){A.cd=.4;A.round++;const p=s7mMuzzle(b,'emitter');
    for(let i=0;i<5+M.n*2;i++)sw28Orb(b,p.x,p.y,Math.PI/2+(i-(4+M.n*2)/2)*.19,2.7);combatAudio0927(b,'combatToxic0927',.3);}
   if(u>2.4)s7mSet(b,'recover');
  }else if(M.mode==='er28-bounce'){
   const period=.82,cycle=Math.floor(u/period),v=(u%period)/period,landing=i=>clamp(260+Math.sin(i*2.39)*32,235,VH-145);
   b.x=worldWidth()/2+Math.sin(v*TAU)*(viewW()*.20);b.y=lerp(cycle?landing(cycle-1):A.from.y,landing(cycle),v);M.height=Math.sin(v*Math.PI)*150;b._s4MiniSafe=M.height>35;
   if(cycle>A.impact){if(A.impact>=0){const count=8+M.n*2,iy=landing(cycle-1)+54;for(let i=0;i<count;i++)sw28Orb(b,worldWidth()/2,iy,i*TAU/count+cycle*.19,2.5);s7mFX(worldWidth()/2,iy,125,true);combatAudio0927(b,'expBig',.35);er28Log('warden-bounce-impact',{x:worldWidth()/2,y:iy,count});}A.impact=cycle;A.landing={x:worldWidth()/2,y:landing(cycle)+54};}
   if(u>period*4){M.height=0;b.x=worldWidth()/2;b.y=landing(3);b._s4MiniSafe=false;s7mSet(b,'recover');}
  }result=true;
 }
 if(!custom)for(const p of M.er28Canisters||[])p.flash=Math.max(0,(p.flash||0)-dt);
 if(!M.tank){const G=r25Gait(b);G.yaw=0;M.lean=0;if(M.mode!=='er28-bounce'){b.x=worldWidth()/2;b.y=clamp(b.y,235,VH*.64);}
  b._drawY=b.y+M.drop-M.height;}
 return result;};
s7mWarnings=function(front){const out=SW28.base.warnings.apply(this,arguments);
 for(const b of[boss,subBoss]){const M=b?._s7mod;if(M?.mode==='er28-bounce'){const q=M.er28?.landing||{x:worldWidth()/2,y:b.y+54};groundTargetReticleDraw(q.x,q.y,100,M.t<M.warn?M.t/M.warn:((M.t-M.warn)%.82)/.82,.7);}}
 for(const b of[boss,subBoss]){const M=b?._s7mod;if(!M||M.mode!=='er28-guns'||M.t>=M.warn)continue;
  for(const p of s7mLive(M,'gun')){const q=s7mMuzzle(b,p.id);for(const off of[-.22,0,.22]){const a=M.er28.angle+off;combatWarningDraw(b,{x:q.x,y:q.y,ex:q.x+Math.cos(a)*VH*1.4,ey:q.y+Math.sin(a)*VH*1.4,width:16,progress:M.t/M.warn,fieldOnly:!front,alertOnly:false});}}
 }return out;};
drawCombatFinalProjectile=function(q){if(q._er28Slug)return er28Blit('toxic_slug',Math.floor(projectileVisualAge(q)*24)%16*64+er28Dir(Math.atan2(q.vy,q.vx)+Math.PI/2),q.x,q.y);
 if(q._er28Orb)return er28Blit('toxic_orb',Math.floor(projectileVisualAge(q)*24)%16,q.x,q.y);
 return SW28.base.projectile.apply(this,arguments);};
updatePlay=function(dt){const out=SW28.base.update.apply(this,arguments);
 for(const m of SW28.mortars){const q=m.q;if(q.dead||m.b.dead||m.b!==boss&&m.b!==subBoss){q.dead=true;continue;}
  m.t+=dt;const u=clamp(m.t/m.flight,0,1);q.x=lerp(m.start.x,m.target.x,u);q.y=lerp(m.start.y,m.target.y,u)-Math.sin(u*Math.PI)*m.arc;
  if(u>=1){q.dead=true;s7mFX(m.target.x,m.target.y,85,true);for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(player.x-q.x,player.y-q.y)<27)playerHit('toxic mortar');});
   for(let i=0;i<6;i++)sw28Orb(m.b,q.x,q.y,i*TAU/6+m.target.x*.01,2.25);}
 }SW28.mortars=SW28.mortars.filter(m=>!m.q.dead);return out;};
