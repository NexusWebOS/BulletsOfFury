'use strict';
/* DF55: protected hull, alternating twin slugs, roof mortar and wall collision. */
const DF55={base:{set:s7mSet,next:s7mNext,tick:s7mTick,at:s7mAt,hit:s7mHit,targets:s7mTargets,blit:s7mBlit,
 slug:sw28Slug,mortars:sw28Mortars,warnings:s7mWarnings,projectile:drawCombatFinalProjectile,update:updatePlay,
 effects:drawEffects,load:stageLoadBegin,ready:target17Ready},events:[],flights:[],fx:[],serial:0};
for(const a of Object.values(DF55_ART))XART._src[a.key]=a.path;
Audio.SFX.df55WallImpact=()=>weaponFeedbackSound('juggernautRamImpact',1);
function df55Own(b){return dc40Own(b);}
function df55Armed(b){return s7mLive(b._s7mod,'gun').length>0;}
function df55Log(event,data={}){DF55.events.push({event,time:efxClock,...data});if(DF55.events.length>1200)DF55.events.shift();}
function df55Blit(name,f,x,y){const a=DF55_ART[name];if(!a||!XART.rdy(a.key))return false;f=clamp(f|0,0,a.frames-1);ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);return true;}
stageLoadBegin=function(n,keys){if(n===7)Snd.prepare(['enemyMachineGunHeavy','combatToxic0927','bossWeaponCharge','juggernautRamImpact','combatServo0927','jetDash']);return DF55.base.load.call(this,n,n===7?[...(keys||[]),...Object.values(DF55_ART).map(a=>a.key)]:keys);};
target17Ready=function(b){return df55Own(b)?false:DF55.base.ready.apply(this,arguments);};
function df55Top(b){return s7mMuzzle(b,'dorsal');}
function df55Clear(b){for(const F of DF55.flights)if(F.b===b)F.dead=true;for(const q of eBullets)if(q._df55Owner===b)q.dead=true;}
s7mAt=function(b,x,y){if(!df55Own(b)||!df55Armed(b))return DF55.base.at.apply(this,arguments);const M=b._s7mod;
 if(['entry','portal','overdrive','dead'].includes(M.mode))return null;
 // Sealed hull pixels never eat rounds on their way to the live gun masks.
 for(const p of s7mPose(b).slice().reverse()){if(!p.id.startsWith('gun')||!s7mLive(M,'gun').some(q=>q.id===p.id))continue;
  const q=s7mWorld(b,p),bank=sw28Bank(b,p);if(bank&&er28AlphaAt(bank.name,bank.f,x-q.x,y-q.y))return p.id;}return null;};
s7mTargets=function(b){const r=DF55.base.targets.apply(this,arguments);return df55Own(b)&&df55Armed(b)?r.filter(q=>['gunL','gunR'].includes(q._retinaId)):r;};
s7mHit=function(b,dmg,x,y,id){if(!df55Own(b))return DF55.base.hit.apply(this,arguments);const M=b._s7mod;id=id||s7mAt(b,x,y);
 if(df55Armed(b)&&(!id||id==='core'||id==='body')){if(dmg>0&&id){M.shieldFlash=.12;weaponHitSfx('shield');df55Log('hull-protected',{core:M.core});}return true;}
 const armed=df55Armed(b),r=DF55.base.hit.call(this,b,dmg,x,y,id);
 if(armed&&!df55Armed(b)&&M.mode!=='dead'){M.od=true;M.df55Hull=true;df55Log('hull-unsealed',{core:M.core,hp:b.hp,maxhp:b.maxhp});s7mSet(b,'dc40-ram');}
 if(b.dead||M.mode==='dead')df55Clear(b);return r;};
s7mSet=function(b,mode){if(!df55Own(b))return DF55.base.set.apply(this,arguments);const M=b._s7mod;
 if(mode==='dc40-circle'||mode==='er28-mortar')mode='df55-roof';
 if(!df55Armed(b)&&!['entry','recover','dead','dc40-ram','df55-roof','stun'].includes(mode))mode='dc40-ram';
 const r=DF55.base.set.call(this,b,mode);
 if(['dc40-guns','dc40-ram','df55-roof'].includes(mode)){
  M.df55=true;M.dc40=M.dc40||{mode,angle:Math.atan2(player.y-b.y-60,player.x-b.x)};const A=M.dc40;
  Object.assign(A,{mode,from:{x:b.x,y:b.y},phase:'warn',cd:0,round:0,guns:{gunL:0,gunR:.028},barrels:{gunL:0,gunR:1},hits:new Set()});
  M.warn=mode==='dc40-guns'?1.15:mode==='df55-roof'?.40:1.25;M.df55TopAge=99;
  if(mode==='dc40-ram'){
   Object.assign(A,{end:{x:clamp(player.x,camLeftX()+100,camRightX()-100),y:VH-124},back:{x:camLeftX()+viewW()/2,y:Math.min(VH*.43,VH-245)},dash:.55});
   b._s4MiniSafe=true;combatAudio0927(b,'bossWeaponCharge',.20);
  }else b._s4MiniSafe=false;
  df55Log('attack-start',{mode,armed:df55Armed(b),x:b.x,y:b.y});
 }
 if(mode==='dead')df55Clear(b);return r;};
s7mNext=function(b){if(!df55Own(b))return DF55.base.next.apply(this,arguments);const M=b._s7mod;M.df55Choice=(M.df55Choice||0)+1;
 const book=['dc40-guns','df55-roof','dc40-ram','dc40-guns','df55-roof'];M.seq++;return s7mSet(b,df55Armed(b)?book[(M.df55Choice-1)%book.length]:'dc40-ram');};
sw28Slug=function(b,id){if(!df55Own(b))return DF55.base.slug.apply(this,arguments);if(!dc40Live(b,id)||!sw28Budget(b))return;const M=b._s7mod,A=M.dc40;
 const barrel=A.barrels[id]++%2,p=dc40Barrel(b,id,barrel),q=dc40Shot(b,p,id);if(!q)return;
 q._df55Owner=b;q._df55Gun=id;q._df55Barrel=barrel;M.dc40Recoil[id]=.11;
 navalFlash(null,p,.55,'weapon_muzzle_toxic',{n:4,hpx:20,life:.065,follow:()=>dc40Live(b,id)?dc40Barrel(b,id,barrel):null});
 combatAudio0927(b,'enemyMachineGunHeavy',.11);df55Log('slug',{id,barrel,x:p.x,y:p.y,a:p.a});};
function df55Roof(b,magma=false){const M=b._s7mod,A=M.dc40,p=df55Top(b),count=magma?5+M.n:3+M.n;
 M.df55TopAge=0;M.df55Hot=magma;DF55.fx.push({b,kind:magma?'magma_spew':'ooze',t:0,anchor:true});
 for(let i=0;i<count;i++){
  if(DF55.flights.filter(F=>!F.dead&&F.b===b).length>=24)break;
  // A spread of committed landing points, not a circular pre-fire warning.
  const wave=A.round||0,u=(i+.5)/count,x=camLeftX()+42+u*(viewW()-84),row=(i+wave)%3;
  const target={x:clamp(x+(wave%2?14:-14),camLeftX()+38,camRightX()-38),y:viewTopY()+viewH()*(.53+row*.16)},flight=1.20+i*.065;
  const F={id:++DF55.serial,b,magma,from:{x:p.x,y:p.y},target,x:p.x,y:p.y,t:0,flight,arc:82+i%2*25,dead:false};DF55.flights.push(F);
  df55Log('roof-orb',{id:F.id,magma,x:p.x,y:p.y,target,flight});
 }
 combatAudio0927(b,'combatToxic0927',.18);df55Log('roof-volley',{magma,count});
}
sw28Mortars=function(b){if(df55Own(b))return df55Roof(b,!df55Armed(b));return DF55.base.mortars.apply(this,arguments);};
function df55Impact(b,A){if(A.collided)return;A.collided=true;A.phase='impact';shake=Math.max(shake,9);
 combatAudio0927(b,'df55WallImpact',.25);s7mFX(A.end.x,A.end.y+98,110,false);
 df55Log('wall-impact',{x:A.end.x,y:A.end.y+98,core:b._s7mod.core});
}
function df55Ram(b,dt){const M=b._s7mod,A=M.dc40,u=M.t-M.warn;
 if(u<0){combatWarningTick(b,'df55-ram',M.t,M.warn);return;}
 if(u<A.dash){const v=u/A.dash;b.x=lerp(A.from.x,A.end.x,v*v);b.y=lerp(A.from.y,A.end.y,v*v);
  if(A.phase!=='dash'){A.phase='dash';combatAudio0927(b,'jetDash',.5);df55Log('ram-release',{from:A.from,to:A.end});}
  for(const seat of seatList())withSeat(seat,()=>{if(!A.hits.has(seat)&&!player.dead&&Math.abs(player.x-b.x)<76&&Math.abs(player.y-(b.y+55))<86){A.hits.add(seat);playerHit('Dredger wall ram');}});
 }else if(u<A.dash+.60){b.x=A.end.x;b.y=A.end.y;df55Impact(b,A);shake=Math.max(shake,4*(1-(u-A.dash)/.60));}
 else if(u<A.dash+3.55){if(A.phase!=='reverse'){A.phase='reverse';combatAudio0927(b,'combatServo0927',.2);df55Log('reverse-start',{from:A.end,to:A.back,duration:2.95});}
  const v=clamp((u-A.dash-.60)/2.95,0,1),k=v*v*(3-2*v);b.x=lerp(A.end.x,A.back.x,k);b.y=lerp(A.end.y,A.back.y,k);b._s4MiniSafe=false;
 }else{b.x=A.back.x;b.y=A.back.y;b._s4MiniSafe=false;df55Log('reverse-complete',{y:b.y});s7mSet(b,'df55-roof');}
}
s7mTick=function(b,dt){if(!df55Own(b))return DF55.base.tick.apply(this,arguments);const M=b._s7mod;
 if(!['dc40-guns','dc40-ram','df55-roof'].includes(M.mode)||!M.dc40)return DF55.base.tick.apply(this,arguments);
 const oldY=b.y;sw28Common(b,dt);M.lean=0;M.dc40Track??=0;M.df55TopAge=(M.df55TopAge??99)+dt;
 for(const id of ['gunL','gunR'])M.dc40Recoil[id]=Math.max(0,(M.dc40Recoil[id]||0)-dt);
 const A=M.dc40,u=M.t-M.warn;
 if(M.mode==='dc40-ram')df55Ram(b,dt);
 else if(M.mode==='dc40-guns'){
  if(u<0){if(M.t<M.warn*.42)A.angle=Math.atan2(player.y-b.y-60,player.x-b.x);combatWarningTick(b,'df55-guns',M.t,M.warn);}
  else{const interval=M.n===2?.055:M.n===1?.07:.085;
   for(const p of s7mLive(M,'gun')){A.guns[p.id]-=dt;if(A.guns[p.id]<=0){A.guns[p.id]+=interval;sw28Slug(b,p.id);}}
   if(u>2.35||!df55Armed(b))s7mSet(b,'recover');}
 }else if(u>=0){A.cd-=dt;if(A.cd<=0&&A.round<3){A.cd=.62;df55Roof(b,!df55Armed(b));A.round++;}if(u>2.05)s7mSet(b,'recover');}
 M.dc40Track=(M.dc40Track+(b.y-oldY)/1.5+8000)%8;M.lean=0;b._drawY=b.y+M.drop-M.height;return true;
};
s7mBlit=function(name,i,x,y,w,h,rot,alpha,flash){const b=SW28.actor;if(name==='tank'&&df55Own(b)){const M=b._s7mod,A=M.dc40;
 if(i===2&&!(flash>0)){const charge=A?.mode==='df55-roof'||A?.mode==='dc40-ram'&&M.t<M.warn,frame=charge?Math.floor(M.clock*24)%16:Math.floor(M.clock*10)%16;
  return df55Blit(!df55Armed(b)?'top_magma':'top_green',frame,x,y);}
 if(i===0&&A?.mode==='dc40-ram'&&M.t<M.warn&&!(flash>0))return df55Blit('body_charge',Math.floor(M.dc40Track||0)*16+Math.floor(M.clock*(10+14*M.t/M.warn))%16,x,y);
 }return DF55.base.blit.apply(this,arguments);};
function df55Burst(F){if(F.dead)return;F.dead=true;const b=F.b;if(!dc40Live(b))return;DF55.fx.push({b,kind:F.magma?'magma_spew':'ooze',t:0,x:F.target.x,y:F.target.y,anchor:false});
 for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(player.x-F.target.x,player.y-F.target.y)<25)playerHit(F.magma?'Dredger magma mortar':'Dredger toxic mortar');});
 for(let i=0;i<(F.magma?8:5);i++){if(!sw28Budget(b))break;const a=i*TAU/(F.magma?8:5)+F.id*.23,q=sw28Orb(b,F.target.x,F.target.y,a,F.magma?2.6:2.25);if(q)Object.assign(q,{_df55Owner:b,_df55Born:efxClock,_df55Magma:F.magma});}
 combatAudio0927(b,'combatToxic0927',.12);df55Log('roof-impact',{id:F.id,magma:F.magma,x:F.target.x,y:F.target.y});
}
s7mWarnings=function(front){const out=DF55.base.warnings.apply(this,arguments);if(!front)for(const F of DF55.flights)if(!F.dead&&dc40Live(F.b)){const k=F.t/F.flight;df55Blit('ground_'+(k<.5?'green':k<.8?'yellow':'red'),0,F.target.x,F.target.y);}return out;};
drawCombatFinalProjectile=function(q){if(q?._df55Magma)return df55Blit('magma_ball',Math.floor((efxClock-q._df55Born)*24)%16,q.x,q.y);return DF55.base.projectile.apply(this,arguments);};
updatePlay=function(dt){const out=DF55.base.update.apply(this,arguments);
 for(const F of DF55.flights){if(!dc40Live(F.b)){F.dead=true;continue;}F.t+=dt;const u=clamp(F.t/F.flight,0,1);F.x=lerp(F.from.x,F.target.x,u);F.y=lerp(F.from.y,F.target.y,u)-Math.sin(u*Math.PI)*F.arc;if(u>=1)df55Burst(F);}
 DF55.flights=DF55.flights.filter(F=>!F.dead);for(const F of DF55.fx)F.t+=dt;DF55.fx=DF55.fx.filter(F=>F.t<.50&&dc40Live(F.b));
 for(const q of eBullets)if(q._df55Owner&&(!dc40Live(q._df55Owner,q._df55Gun)||q._df55Born!=null&&efxClock-q._df55Born>2.7))q.dead=true;
 return out;
};
drawEffects=function(){const out=DF55.base.effects.apply(this,arguments);for(const F of DF55.flights){if(F.magma)df55Blit('magma_ball',Math.floor(F.t*24)%16,F.x,F.y);else er28Blit('toxic_orb',Math.floor(F.t*24)%16,F.x,F.y);}
 for(const F of DF55.fx){const p=F.anchor?df55Top(F.b):F;df55Blit(F.kind,Math.min(15,Math.floor(F.t/.5*16)),p.x,p.y);}return out;};
globalThis.BOF_DREDGER_FINAL_1029={state:DF55};
