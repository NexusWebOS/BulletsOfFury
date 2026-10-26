"use strict";
/* Mike Oct26: four copies protect the final life; native bodies, weapons and
   health owners receive continuous code-fusion transitions and readable acting. */
const RD30={base:{hit:modularHit,rupture:v18Rupture,donorRupture:v19Rupture,break:r30Break,
 final:j3FinalDeath,enter:v18Enter,morph:j3Morph,tick:r30Tick,draw:r30DrawBoss,world:drawWorld,
 body:v19Body,paint:v19Paint,targets:retinaBossTargets,shield:bossShieldFrac,clear:v18Clear,
 start:v18StartAttack,attack:v18AttackTick,shot:v18Shot,projectile:drawCombatFinalProjectile,
 naval:navalFlash,brain:nb23Body,eyes:nb23Eyes,phoenix:bi24Draw,phoenixPose:bi24AttackPose,
 phoenixSocket:bi24PhoenixSocket,phShot:ph21Shot,load:stageLoadBegin,
 frame:v18Frame,swipe:v19BeginSwipe,intercept:enemyOrdnanceCanIntercept,update:updatePlay},events:[],last:null,
 glow:new Map(),mix:new Map(),active:null,serial:0};
function rd30Own(b){return v18Owned(b)&&j3State(b).encounter===2;}
function rd30State(b){return j3State(b).rd30??={cursor:0,visits:0,wardCue:-99,transition:null,muzzles:[],history:[],unlocked:false};}
function rd30Copies(b){return V18.forms.filter(i=>i!==0&&j3State(b).hp[i]>0);}
function rd30Locked(b){return rd30Own(b)&&b._r30.v18.form===0&&rd30Copies(b).length>0;}
function rd30Log(b,event,data={}){RD30.events.push({event,clock:b._r30.clock,form:b._r30.v18.form,...data});if(RD30.events.length>1600)RD30.events.shift();}
function rd30Cue(b,key,gain=1){Snd.play(key,gain);rd30Log(b,'cue',{key,gain});}
stageLoadBegin=function(n,keys){if(n===8)for(const key of ['combatEnergy0927','combatBeam0927','combatModule0927','shieldHitHeavy','shieldBreakCombat','bossWeaponCharge','expBig'])Snd.prepare(key);
 return RD30.base.load.call(this,n,keys);};
// The final life is held in reserve, including its actual arm HP and pixels.
modularHit=function(dmg){const b=boss;if(!rd30Locked(b))return RD30.base.hit.apply(this,arguments);
 if(!r30Live(b)||b._noHit||!Number.isFinite(dmg)||dmg<=0)return;const R=rd30State(b),p=b.parts.includes(b._lastPart)?b._lastPart:b.parts[0];
 markHit(b,.12);markHit(p,.12);R.wardFlash=.18;
 if(b._r30.clock-R.wardCue>.16){R.wardCue=b._r30.clock;Snd.play('shieldHitHeavy',.45);}
 rd30Log(b,'base-ward-hit',{part:p.id,hp:b.hp,copies:rd30Copies(b).length});
};
retinaBossTargets=function(b){return rd30Locked(b)?[]:RD30.base.targets.apply(this,arguments);};
bossShieldFrac=function(b){return rd30Locked(b)?1:RD30.base.shield.apply(this,arguments);};
r30Break=function(b){if(rd30Locked(b)){rd30Log(b,'base-death-blocked');return;}
 if(rd30Own(b))rd30Log(b,'form-exhausted',{remaining:rd30Copies(b),hp:b.hp});
 return RD30.base.break.apply(this,arguments);
};
j3FinalDeath=function(b){if(rd30Own(b)&&rd30Copies(b).length){rd30Log(b,'premature-finale-blocked');return;}return RD30.base.final.apply(this,arguments);};
function rd30Rupture(b,p,fallback,args){if(rd30Locked(b))return;
 if(rd30Own(b)&&b._r30.v18.form===0&&p.id!=='core'&&!p._rd30Shattered){
  const a=v18Frame(b)[p.id];if(a&&XART.rdy(a.key)){const c=document.createElement('canvas');c.width=c.height=320;c.getContext('2d').drawImage(XART.get(a.key),0,0);
   r25Shards(b,c,b.x,b.y,v18Size(b)/320,12,p.id==='left'?-70:70,-30);p._rd30Shattered=true;rd30Log(b,'final-arm-shatter',{part:p.id});}
 }
 return fallback.apply(null,args);
}
v18Rupture=function(b,p){return rd30Rupture(b,p,RD30.base.rupture,arguments);};
v19Rupture=function(b,p){return rd30Rupture(b,p,RD30.base.donorRupture,arguments);};
v18Enter=function(b,n,form=0){const R=v18Owned(b)?rd30State(b):null,out=RD30.base.enter.apply(this,arguments);
 if(n===2&&rd30Own(b)){const N=b._r30.v18;if(form===0){N.seq=R.cursor;R.visits++;}
  R.muzzles=[];R.history=[];rd30Log(b,'form-enter',{hp:b.hp,locked:rd30Locked(b),remaining:rd30Copies(b)});
  if(!R.unlocked&&!rd30Copies(b).length){R.unlocked=true;rd30Log(b,'final-life-unlocked',{hp:j3State(b).hp[0]});}
 }return out;
};
// Source-derived image mixing: common canvases/pivots, bounded cache, cyclic phase.
function rd30Mixed(a,z,mix,tag){if(!z||mix<=0)return a;mix=Math.round(clamp(mix,0,1)*24)/24;if(!mix)return a;
 const key=tag+':'+mix;let c=RD30.mix.get(key);if(c)return c;c=document.createElement('canvas');c.width=Math.ceil(a.width/2)*2;c.height=Math.ceil(a.height/2)*2;
 const g=c.getContext('2d');g.globalAlpha=1-mix;g.drawImage(a,0,0);g.globalCompositeOperation='lighter';g.globalAlpha=mix;g.drawImage(z,0,0);
 if(RD30.mix.size>=80)RD30.mix.delete(RD30.mix.keys().next().value);RD30.mix.set(key,c);return c;
}
function rd30Glow(image,key){let c=RD30.glow.get(key);if(c)return c;c=document.createElement('canvas');c.width=Math.ceil(image.width/2)*2;c.height=Math.ceil(image.height/2)*2;
 const g=c.getContext('2d',{willReadFrequently:true});g.drawImage(image,0,0);const q=g.getImageData(0,0,c.width,c.height),d=q.data;
 for(let i=0;i<d.length;i+=4){const r=d[i],green=d[i+1],blue=d[i+2],l=Math.max(r,blue);if(l<65||l<green*1.18){d[i+3]=0;continue;}
  d[i]=Math.min(255,r*1.35+24);d[i+1]=Math.min(255,green*1.12+12);d[i+2]=Math.min(255,blue*1.35+24);d[i+3]*=.65;}
 g.putImageData(q,0,0);if(RD30.glow.size>=48)RD30.glow.delete(RD30.glow.keys().next().value);RD30.glow.set(key,c);return c;
}
function rd30Phase(b){const N=b._r30.v18,P=N.attack;if(P){const u=P.t-P.tell;return u<0?clamp(P.t/Math.max(.1,P.tell),0,1):Math.max(.18,1-clamp(u/(P.active||2),0,1));}
 if(ph21Own(b)){const A=ph21State(b)?.action;return A?.tell?clamp(A.t/A.tell,0,1):A?.mode==='dive'?.85:.15;}
 if(N.form===8){const h=gd4Create(b,8).p._hammer;return /warn|charge|raise|recharge|spell|nova/.test(h.state)?clamp(h.t/.9,0,1):.15;}
 return .12;
}
function rd30GlowPose(v,amount){if(!v.a||v.spec?.hidden||!XART.rdy(v.key)||!amount)return;
 const im=XART.get(v.key),a=v.a,anchor=v.anchor||a.pivot;if(!anchor||im.width>a.w*1.5||im.height>a.h*1.5)return;
 ctx.save();ctx.translate(v.ax,v.ay);ctx.rotate(v.rot||0);ctx.globalCompositeOperation='lighter';ctx.globalAlpha*=pxgStep(amount);
 ctx.drawImage(rd30Glow(im,v.key),-anchor[0]*v.k,-anchor[1]*v.k,a.w*v.k,a.h*v.k);ctx.restore();
}
// Final main body uses the complete authored plate until the final-life breaks.
function rd30MainBody(b){const model=V18_ART.models.colossus,now=v18Frame(b),phase=b._r30.clock*model.fps,f=Math.floor(phase)%model.frames.length,
 next=model.frames[(f+1)%model.frames.length],mix=phase-Math.floor(phase),acting=!!v19Acting(b),k=bi24PlateScale(b);
 for(const id of ['left','core','right']){const p=b.parts.find(p=>p.id===id),a=now[id];if(!p||p.destroyed||!a||!XART.rdy(a.key))continue;
  const im=acting?XART.get(a.key):rd30Mixed(XART.get(a.key),XART.get(next[id].key),mix,a.key+'>'+next[id].key);
  ctx.drawImage(im,b.x-160*k,b.y-160*k,320*k,320*k);
  if(Math.max(p.flash||0,b.flash||0)>0){ctx.save();ctx.globalAlpha*=r25Pulse(b,Math.max(p.flash||0,b.flash||0),b._r30.clock);ctx.drawImage(xartTint(a.key,'#fff',1),b.x-160*k,b.y-160*k,320*k,320*k);ctx.restore();}
 }
}
v19Body=function(b){if(rd30Own(b)&&b._r30.v18.form===0&&b._r30.mode==='fight')return rd30MainBody(b);return RD30.base.body.apply(this,arguments);};
v19Paint=function(v,b){if(!hc22Own(b)||!v.a||!v.key.startsWith('v18_helicopter_'))return RD30.base.paint.apply(this,arguments);
 const model=V18_ART.models.helicopter,phase=b._r30.clock*model.fps,f=Math.floor(phase)%model.frames.length,next=model.frames[(f+1)%model.frames.length][v.p.id],a=v.a;
 const im=rd30Mixed(XART.get(v.key),XART.get(next.key),phase-Math.floor(phase),v.key+'>'+next.key);
 ctx.save();ctx.translate(v.ax,v.ay);ctx.rotate(v.rot||0);ctx.drawImage(im,-v.anchor[0]*v.k,-v.anchor[1]*v.k,a.w*v.k,a.h*v.k);
 if(Math.max(b.flash||0,v.p.flash||0)>0){ctx.globalAlpha*=.9;ctx.drawImage(xartTint(v.key,'#fff',1),-v.anchor[0]*v.k,-v.anchor[1]*v.k,a.w*v.k,a.h*v.k);}ctx.restore();
};
function rd30BrainBlend(b){const a=nb23Actor(b),P=b._r30.v18.attack,bank=P?._nb23&&P.type==='eyeExpansion'&&P.t>=P.tell&&P.t<P.tell+P.active?'focus':!P||P.type!=='eyeExpansion'?'brain':null;
 if(!bank)return{a,im:XART.get(a.key),mix:0};const rows=NB23_ART.banks[bank],phase=(bank==='focus'?P.t-P.tell:b._r30.v18.brainAge)*10,i=Math.floor(phase)%rows.length,z=rows[(i+1)%rows.length],mix=phase-Math.floor(phase);
 return{a,z,mix,im:rd30Mixed(XART.get(a.key),XART.get(z.key),mix,a.key+'>'+z.key)};
}
nb23Body=function(b){if(!rd30Own(b))return RD30.base.brain.apply(this,arguments);const q=rd30BrainBlend(b),hit=Math.max(b.flash||0,b.parts[0]?.flash||0)>0;
 if(hit)return RD30.base.brain.apply(this,arguments);ctx.drawImage(q.im,Math.round(b.x-q.a.pivot[0]),Math.round(b.y-q.a.pivot[1]));return true;};
nb23Eyes=function(b){if(!nb23Own(b))return RD30.base.eyes.apply(this,arguments);const q=rd30BrainBlend(b);return(q.a.eyes||NB23_ART.eyes).map((p,i)=>({x:Math.round(b.x-q.a.pivot[0])+lerp(p[0],q.z?.eyes?.[i]?.[0]??p[0],q.mix),y:Math.round(b.y-q.a.pivot[1])+lerp(p[1],q.z?.eyes?.[i]?.[1]??p[1],q.mix)}));};
bi24AttackPose=function(b,actor){const q=RD30.base.phoenixPose.apply(this,arguments);if(actor!=='phoenix'||!ph21Own(b))return q;const A=ph21State(b).action;
 if(!A){const phase=(ph21State(b).age*3)%(2*(q.a.count-1)),f=phase<q.a.count-1?phase:2*(q.a.count-1)-phase;return{...q,f:Math.floor(f),next:Math.min(q.a.count-1,Math.floor(f)+1),blend:f-Math.floor(f)};}
 // Native attack pose timing remains authoritative; interpolate within its measured cells.
 const u=['volley','fan','lance'].includes(A.mode)?A.t<A.tell?A.t/A.tell:(A.t-A.tell)/.36:['recede','corner'].includes(A.mode)?clamp(A.t/.6,0,1):A.mode==='dive'?A.t/A.duration:(1+Math.sin(ph21State(b).age*3))*.5,
 phase=clamp(u,0,1)*(q.a.count-1);return{...q,f:Math.floor(phase),next:Math.min(q.a.count-1,Math.floor(phase)+1),blend:phase-Math.floor(phase)};};
function rd30PhoenixCell(q,b,f){const a=q.a,key=a.key+':'+f+':'+b.parts.filter(p=>p.destroyed).map(p=>p.id).join();let c=RD30.mix.get(key);if(c)return c;
 const damaged=bi24DamagePlate({...q,f},b);if(damaged)return damaged;c=document.createElement('canvas');c.width=a.w;c.height=a.h;c.getContext('2d').drawImage(XART.get(a.key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,0,0,a.w,a.h);if(RD30.mix.size>=80)RD30.mix.delete(RD30.mix.keys().next().value);RD30.mix.set(key,c);return c;}
bi24Draw=function(q,b,size,rot=0){if(!ph21Own(b)||q.next==null||Math.max(b.flash||0,...b.parts.map(p=>p.flash||0))>0)return RD30.base.phoenix.apply(this,arguments);
 const im=rd30Mixed(rd30PhoenixCell(q,b,q.f),rd30PhoenixCell(q,b,q.next),q.blend,q.a.key+':ph:'+q.f+':'+b.parts.filter(p=>p.destroyed).map(p=>p.id).join()),k=size/q.a.w;
 ctx.save();ctx.translate(b.x,b.y);ctx.rotate(rot);ctx.drawImage(im,-q.a.pivot[0]*k,-q.a.pivot[1]*k,q.a.w*k,q.a.h*k);ctx.restore();BI24.current.set(b,{...q,size,k,rot,x:b.x,y:b.y,key:q.a.key});return true;};
bi24PhoenixSocket=function(b,side,barrel=0){const q=bi24AttackPose(b,'phoenix');if(q.next==null)return RD30.base.phoenixSocket.apply(this,arguments);
 const a=q.a.sockets[q.f][side],z=q.a.sockets[q.next][side],Q=ph21State(b),k=360/256*Q.scale,c=Math.cos(Q.angle),s=Math.sin(Q.angle),dx=(lerp(a[0],z[0],q.blend)-128+(barrel%2?4:-4))*k,dy=(lerp(a[1],z[1],q.blend)-128)*k;return{x:b.x+dx*c-dy*s,y:b.y+dx*s+dy*c};};
// Snapshot native authored pixels using their same rig transforms. No actor substitutes.
function rd30Plate(b){const c=document.createElement('canvas');c.width=c.height=768;const g=c.getContext('2d');g.translate(384-b.x,384-b.y);g.imageSmoothingEnabled=false;
 if(ph21Own(b)){const q=bi24AttackPose(b,'phoenix'),Q=ph21State(b),a=q.a,k=360/512*Q.scale;g.translate(b.x,b.y);g.rotate(Q.angle);g.drawImage(rd30PhoenixCell(q,b,q.f),-256*k,-256*k,512*k,512*k);return c;}
 const drawn=new Set();for(const v of v18Rig(b)){if(v.p.destroyed||v.spec?.hidden||!v.a||!XART.rdy(v.key))continue;const a=v.a,anchor=v.anchor||a.pivot,tag=v.key+':'+v.ax+':'+v.ay+':'+v.rot;if(drawn.has(tag))continue;drawn.add(tag);
  g.save();g.translate(v.ax,v.ay);g.rotate(v.rot||0);g.drawImage(XART.get(v.key),-anchor[0]*v.k,-anchor[1]*v.k,a.w*v.k,a.h*v.k);g.restore();}return c;
}
j3Morph=function(b,to){if(!rd30Own(b))return RD30.base.morph.apply(this,arguments);const R=rd30State(b),N=b._r30.v18,J=j3State(b);
 if(R.transition)return;if(N.form===0&&b._r30.mode==='fight'){
  if(N.attack||N.swipe)return;if(J.attacks<3){v18StartAttack(b);return;}if(!bh25DrClear(b)){b._r30.cd=.35;return;}R.cursor=N.seq;
 }
 const target=to==='home'?v18Next(b):V18.forms.includes(to)&&J.hp[to]>0?to:v18Next(b);if(target<0)return j3FinalDeath(b);if(target===N.form)return;
 const x=b.x,y=b.y,from=b.hp>0?rd30Plate(b):null;j3Save(b);v18Clear(b);b.x=x;b.y=y;
 R.transition={id:++RD30.serial,from:N.form,to:target,x,y,start:{x,y},home:{x:worldWidth()/2,y:viewTopY()+viewH()*.40},age:0,source:from,incoming:null,impact:false};N.from=N.form;N.to=target;
 DR21.base.setMode(b,'v18formOut');rd30Cue(b,'combatEnergy0927',.7);rd30Log(b,'fusion-start',{from:N.form,to:target});
};
function rd30Code(b,t,alpha,height=330){const S=rd28State(b,b.x,b.y,6.2+t);return{...S,y:b.y,phase:t*3+t*t*.35,flow:t*.35,absorb:0,alpha,height};}
function rd30TransitionWhite(b){const R=rd30State(b),t=b._r30.t;if(!R.transition||b._r30.mode!=='v18formIn'||t<1.45)return 0;return t<1.65?Math.floor((t-1.45)/.2*16):t<1.85?16:16-Math.floor(clamp((t-1.85)/.6,0,1)*16);}
function rd30TransitionDraw(b){const R=rd30State(b),T=R.transition,S=b._r30,t=S.t,incoming=S.mode==='v18formIn',u=clamp(t/(incoming?1.65:1.4),0,1),size=v18Size(b),k=size/320,
 code=rd30Code(b,T.age,.85*Math.sin(Math.min(1,T.age/3.9)*Math.PI)+.1,330);
 rd28Begin(code);rd28Strands(code,false);
 if(!incoming&&T.source){ctx.save();ctx.beginPath();for(let y=0;y<768;y+=4)if(((y/4)*.61803398875)%1>u)ctx.rect(b.x-384,b.y-384+y,768,4.1);ctx.clip();ctx.drawImage(T.source,b.x-384,b.y-384);ctx.restore();}
 const carrier=ER23_ART.banks.symbiote,phase=T.age*.85+T.age*T.age*.09,Q={rotationTurns:phase,yaw:phase*TAU,frame:Math.floor(phase*24)%24};
 if(!incoming||t<1.65){ctx.save();ctx.globalAlpha*=incoming?.55:clamp(u*2,0,1);const im=rd27Carrier(Q);ctx.drawImage(im,b.x-128*k,b.y-128*k,256*k,256*k);ctx.restore();}
 const complete=incoming&&t>=1.65;
 if(incoming&&T.incoming){const progress=complete?1:Math.min(.86,.08+.78*v19Ease(u));ctx.save();ctx.beginPath();for(let y=0;y<768;y+=4)if(((y/4)*.61803398875)%1<=progress)ctx.rect(b.x-384,b.y-384+y,768,4.1);ctx.clip();ctx.drawImage(T.incoming,b.x-384,b.y-384);ctx.restore();}
 rd28Strands(code,true);
 if(incoming&&t>1.05&&t<1.85){const strike=Math.floor((t-1.05)*14),x=b.x+[-75,52,0,90,-35][strike%5];if(((t-1.05)*14)%1<.6)r25Bolt(x,viewTopY()-35,b.x+(x-b.x)*.2,b.y+125,T.age,.8);}
 RD30.last={kind:'fusion',from:T.from,to:T.to,time:T.age,incoming,complete,white:rd30TransitionWhite(b),phase,x:b.x,y:b.y};
}
// Any flash following a donor socket expires with that exact donor generation.
navalFlash=function(e,mz,scale,fam,opts){if(!RD30.active||!opts?.follow)return RD30.base.naval.apply(this,arguments);
 const b=RD30.active,form=b._r30.v18.form,N=b._r30.v18,generation=N._hc22,follow=opts.follow;
 const out=RD30.base.naval.call(this,e,mz,scale,fam,{...opts,follow:()=>!b.dead&&rd30Own(b)&&N.form===form&&b._r30.mode==='fight'&&(!generation||N._hc22===generation)?follow():null});
 const f=_navalFlashes[_navalFlashes.length-1];if(f)f._rd30Owner=b;return out;};
v18Clear=function(b){if(v18Owned(b)){for(let i=_navalFlashes.length-1;i>=0;i--)if(_navalFlashes[i]._rd30Owner===b)_navalFlashes.splice(i,1);const R=j3State(b).rd30;if(R){R.muzzles=[];R.history=[];}}
 return RD30.base.clear.apply(this,arguments);};
function rd30Muzzle(b,port,angle,size=30){if(!rd30Own(b))return;const R=rd30State(b);R.muzzles.push({at:b._r30.clock,form:b._r30.v18.form,id:port.module||'core',x:port.x,y:port.y,angle,size});if(R.muzzles.length>28)R.muzzles.shift();}
v18Shot=function(b,p,a){const q=RD30.base.shot.apply(this,arguments);if(q&&rd30Own(b)){rd30Muzzle(b,p,a,Math.max(22,(q.w||10)*1.5));if(q._v19Symbiote){q._rd30Energy=true;q._rd30Form=b._r30.v18.form;q._rd30Module=p.module||'core';q._rd30Owner=b;q._weaponProof=true;q._shootable=false;}}
 return q;};
ph21Shot=function(b,id,a){const before=eBullets.length,out=RD30.base.phShot.apply(this,arguments);if(eBullets.length>before){const p=ph21Muzzle(b,id,arguments[4]);if(p)rd30Muzzle(b,{...p,module:id},a,36);}return out;};
drawCombatFinalProjectile=function(q){if(q?._rd30Energy){dr21Art('ball',q.t||0,q.x,q.y,Math.max(26,(q.w||12)*1.7));return true;}return RD30.base.projectile.apply(this,arguments);};

// Whole authored scythe poses own the collision, not an invisible rotated limb.
function rd30ScythePose(b){const P=b._r30.v18.attack,c=V19_ART.clips.colossus_scythe,u=P.t-P.tell,
 phase=u<0?.24*v19Ease(P.t/P.tell):u<P.active?.24+.52*clamp(u/P.active,0,1):.76+.24*v19Ease((u-P.active)/P.recover);
 return c.frames[Math.min(c.frames.length-1,Math.floor(phase*(c.frames.length-1)))];}
v18Frame=function(b){return rd30Own(b)&&b._r30.v18.attack?._rd30Scythe?rd30ScythePose(b).layers:RD30.base.frame.apply(this,arguments);};
v19BeginSwipe=function(b,type){if(!rd30Own(b)||b._r30.v18.form!==0||type!=='scytheReap')return RD30.base.swipe.apply(this,arguments);
 const N=b._r30.v18,ports=['left','right'].map(id=>d20BossMount(b,id)).filter(Boolean);if(!ports.length)return false;
 const P=N.attack={_rd30Scythe:true,type,t:0,tell:diffKey==='furious'?1.08:1.3,active:.78,recover:.80,origin:{x:b.x,y:b.y},
  target:{x:clamp(player.x,camLeftX()+100,camRightX()-100),y:clamp(player.y,viewTopY()+220,VH-65)},ports,targets:[],lanes:[],hit:new Set()};
 P.lanes=ports.map(p=>({...p,ex:P.target.x,ey:P.target.y,width:100,module:p.module}));N.swipe=null;N.acting='colossus_scythe';b._r30.attack=P;
 combatWarningTick(b,'rd30-scythe-'+N.seq,0,P.tell,true);rd30Cue(b,'bossWeaponCharge',.8);rd30Log(b,'scythe-tell',{target:P.target,tell:P.tell});return true;
};
function rd30ScytheTick(b,dt){const N=b._r30.v18,P=N.attack;P.t+=dt;const u=P.t-P.tell;
 combatWarningTick(b,'rd30-scythe-'+N.seq,Math.min(P.t,P.tell),P.tell);
 const advance=u<0?v19Ease(P.t/P.tell)*.25:u<P.active?.25+.75*v19Ease(u/P.active):1-v19Ease((u-P.active)/P.recover);
 b.x=lerp(P.origin.x,P.target.x,advance);b.y=lerp(P.origin.y,P.target.y-115,advance);
 if(u>=0&&!P.released){P.released=true;rd30Cue(b,'slice',.9);rd30Log(b,'scythe-release');}
 if(u>=0&&u<P.active)for(const seat of seatList())withSeat(seat,()=>{if(player.dead||P.hit.has(seat))return;
  const hit=[[-4,0],[4,0],[0,4],[0,-4],[0,0]].some(([x,y])=>{const p=r30At(b,player.x+x,player.y+y);return p&&p.id!=='core';});
  if(hit){P.hit.add(seat);playerHit('Dracodia authored scythe slash');}});
 if(u>=P.active+P.recover){b.x=P.origin.x;b.y=P.origin.y;N.home={...P.origin};N.attack=null;N.acting=null;b._r30.attack=null;b._r30.cd=.75;j3State(b).attacks++;}
}
enemyOrdnanceCanIntercept=function(q){return q?._rd30Energy?false:RD30.base.intercept.apply(this,arguments);};
updatePlay=function(){for(const q of eBullets)if(q._rd30Energy){const b=q._rd30Owner;if(!rd30Own(b)||b.dead||b._r30.v18.form!==q._rd30Form||!b.parts.some(p=>p.id===q._rd30Module&&!p.destroyed))q.dead=true;}return RD30.base.update.apply(this,arguments);};

// The old ghost-hop attack now travels continuously between its committed points.
v18AttackTick=function(b,dt){const P=b?._r30?.v18?.attack;if(rd30Own(b)&&P?._rd30Scythe)return rd30ScytheTick(b,dt);if(!rd30Own(b)||P?.type!=='ghostTeleport')return RD30.base.attack.apply(this,arguments);
 const u=P.t+dt-P.tell,hops=P.hops*P.hop;if(u>=0&&u<hops){P.t+=clamp(dt||0,0,.05);const i=Math.floor(u/P.hop),f=clamp((u-i*P.hop)/P.hop,0,1),from=i?P.positions[i-1]:P.origin,to=P.positions[i];
  b.x=lerp(from.x,to.x,v19Ease(f));b.y=lerp(from.y,to.y,v19Ease(f));P.opacity=1;P.depth=1;P.ghostAt=f*P.hop;b._noHit=f>.12&&f<.88;
  if(P.lastHop!==i){P.lastHop=i;rd30Cue(b,'combatEnergy0927',.45);rd30Log(b,'continuous-code-dash',{i,from,to});}return;
 }return RD30.base.attack.apply(this,arguments);
};
function rd30CombatEffects(b,front){const N=b._r30.v18,R=rd30State(b),P=N.attack,t=b._r30.clock,power=rd30Phase(b),locked=rd30Locked(b);
 if(N.form===0&&(locked||P?.type==='downloadRitual')){const code=rd30Code(b,t,.13+(R.wardFlash||0)*1.6,310);rd28Begin(code);rd28Strands(code,front);}
 if(!front)return;
 const seen=new Set();if(N.form!==2)for(const v of v18Rig(b)){if(seen.has(v.key))continue;seen.add(v.key);rd30GlowPose(v,.2+power*.65);}
 if(N.form===6&&P?.type==='eyeExpansion'){const u=P.t-P.tell;if(u<0||u<P.active)for(const eye of nb23Eyes(b))av3Muzzle(ctx,eye.x,eye.y,u<0?12+32*power:52,'void',t,u<0?.35+.5*power:.9);}
 if(N.form===8){const v=v18Rig(b).find(v=>v.p.id==='hammer');if(v&&power>.3){d20Fx('lightning_loop',t,v.x,v.y,28+power*38,0,.35+power*.45);}}
 if(N.form===1){const Q=hc22Proxy(b),p=Q.p;if(['chargeTell','charge','rush'].includes(p._ovState))for(const side of [-1,1]){const m=hc22Mount(b,side);if(b.parts.some(q=>q.id===(side<0?'left':'right')&&!q.destroyed))av3Muzzle(ctx,m.x,m.y,26+power*26,'void',t,.65);}}
 if(N.form===2){const A=ph21State(b)?.action;if(A?.mode==='dive')for(const v of v19VolcanoRig(b).filter(v=>v.p.id.startsWith('claw'))){const p=ph21TalonPoint(v);d20Fx('lightning_loop',t,p.x,p.y,28,0,.7);}
  if(A?.tell&&A.t<A.tell)for(const id of ['cannonL','cannonR'])if(ph21Alive(b,id)){const p=ph21Muzzle(b,id);av3Muzzle(ctx,p.x,p.y,12+power*25,'fire',t,.3+power*.5);}}
 for(const m of R.muzzles){const age=t-m.at;if(age<0||age>.2||m.form!==N.form||!b.parts.some(p=>p.id===m.id&&!p.destroyed))continue;
  let at=m;if(N.form===2&&m.id.startsWith('cannon'))at=ph21Muzzle(b,m.id)||m;else if(N.form===0)at=d20BossMount(b,m.id)||m;
  av3Muzzle(ctx,at.x,at.y,m.size*(1-age*2),'void',age,1-age/.2);}
 RD30.last={kind:'combat',form:N.form,locked,power,muzzles:R.muzzles.length};
}
r30Tick=function(b,dt){if(!rd30Own(b))return RD30.base.tick.apply(this,arguments);const R=rd30State(b),S=b._r30,N=S.v18;dt=clamp(dt||0,0,.05);
 if(R.transition&&['v18formOut','v18formIn'].includes(S.mode)){
  dr5Protect(b,dt);b._noHit=b.enter=true;R.transition.age+=dt;const T=R.transition;if(S.mode==='v18formOut'){const u=v19Ease(S.t/1.4);T.x=lerp(T.start.x,T.home.x,u);T.y=lerp(T.start.y,T.home.y,u);}b.x=T.x;b.y=T.y;
  if(S.mode==='v18formOut'&&S.t>=1.4){v18Enter(b,2,T.to);b.x=T.x;b.y=T.y;N.home={x:b.x,y:b.y};
   if(hc22Own(b)){const p=hc22Proxy(b).p;p.x=b.x;p.y=b.y;}if(v19Native(b)){const p=gd4Create(b,N.form).p;p.x=b.x;p.y=b.y;}
   DR21.base.setMode(b,'v18formIn');T.incoming=rd30Plate(b);rd30Log(b,'fusion-assembly',{x:b.x,y:b.y});
  }else if(S.mode==='v18formIn'){
   if(S.t>=1.65&&!T.impact){T.impact=true;rd30Cue(b,'combatBeam0927',.7);shake=Math.max(shake,4);}
   if(S.t>=2.5){R.transition=null;v18Fight(b);N.home={x:b.x,y:b.y};rd30Log(b,'fusion-complete',{x:b.x,y:b.y,hp:b.hp});}
  }return;
 }
 R.wardFlash=Math.max(0,(R.wardFlash||0)-dt);R.muzzles=R.muzzles.filter(q=>S.clock-q.at<.25);
 const previous=RD30.active,P=N.attack;RD30.active=b;let out;try{out=P?._rd30Scythe?D20.base.tick.apply(this,arguments):RD30.base.tick.apply(this,arguments);}finally{RD30.active=previous;}
 if(P?.type==='bh25'&&!N.attack&&S.mode==='fight')j3State(b).attacks++;
 if(S.mode==='fight'&&N.attack?.type==='ghostTeleport'){R.history.push({x:b.x,y:b.y,t:S.clock});if(R.history.length>12)R.history.shift();}else R.history=[];
 return out;
};
r30DrawBoss=function(b){if(!rd30Own(b))return RD30.base.draw.apply(this,arguments);const R=rd30State(b),S=b._r30,P=S.v18.attack;
 if(R.transition&&['v18formOut','v18formIn'].includes(S.mode))return rd30TransitionDraw(b);
 if(S.mode!=='fight')return RD30.base.draw.apply(this,arguments);
 rd30CombatEffects(b,false);let out;
 if(P?.type==='ghostTeleport'){
  for(const q of R.history.filter((_,i)=>i%4===0)){const code=rd30Code(b,S.clock,.14,220);code.x=q.x;code.y=q.y;rd28Begin(code);rd28Strands(code,false);}
  v19Body(b);v18Warnings(b);if(P.slamAge>=0&&P.slamAge<.7)dr21Art('erase',P.slamAge,P.target.x,P.target.y,150,1,true);
 }else out=RD30.base.draw.apply(this,arguments);rd30CombatEffects(b,true);return out;
};
drawWorld=function(){const out=RD30.base.world.apply(this,arguments),b=boss;if(rd30Own(b)&&rd30State(b).transition){const white=rd30TransitionWhite(b);if(white){ctx.save();ctx.setTransform(SS,0,0,SS,0,0);const z=viewZoom();ctx.scale(z,z);ctx.translate(-camLeftX(),VH*(1-z)/z);er23Curtain('whiteout',white);ctx.restore();}}return out;};
globalThis.BOF_DRACODIA_FORMS_1026=RD30;
