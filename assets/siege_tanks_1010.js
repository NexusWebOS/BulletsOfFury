"use strict";
/* Authored modular Level 1 encounters. SONIC / ORDOS / HARK select them through
   the existing difficulty/pilot password flow. Default campaign roster is kept.
   Canvas policy: even frame dimensions, shared pivots and proportional scales. */
const SG10={clock:0,launchUnit:null,fx:[],debris:[],decals:[],masks:new Map(),events:[],
 kinds:{siegesonic:'sonic',siegedeviator:'deviator',siegedevastator:'devastator'},
 specs:{sonic:{name:'SONIC SIEGE TANK',width:240,hp:1.15,color:'#65e6ff'},
  deviator:{name:'DEVIATOR MISSILE TANK',width:200,hp:1.03,color:'#90ed75'},
  devastator:{name:'DEVASTATOR ASSAULT TANK',width:154.5,hp:.95,color:'#ff6452'}},
 routes:{SONIC:'siegesonic',ORDOS:'siegedeviator',HARK:'siegedevastator'},
 base:{spawn:spawnSubBoss__inner,tick:updateSubBoss,draw:drawSubBoss,hit:hitSubBoss,
  at:subBossHitPart,solid:subBossSolidAt,beam:subBossBeamImpact,targets:retinaBossTargets,
  play:updatePlay,bullets:drawBullets,effects:drawEffects,begin:beginStage,start:startRun,
  load:stageLoadBegin,submit:submitPassword,pages:pc5Pages,break:ordnanceBreak1002,
  damageDraw:encounterDamageOverlay,retire:bofDerivedCachesRetire}};
const SG10_RIG=[
 {id:'trackL',part:'track_left',x:-134,y:12,hp:.18},
 {id:'trackR',part:'track_right',x:134,y:12,hp:.18},
 {id:'hull',part:'hull',x:0,y:0,hp:1},
 {id:'reactor',part:'reactor',x:0,y:-137,hp:.16},
 {id:'podL',part:'pod',x:-98,y:50,hp:.14},
 {id:'podR',part:'pod',x:98,y:50,hp:.14},
 {id:'sensor',part:'sensor',x:0,y:-196,hp:.12},
 {id:'weapon',part:'weapon',x:0,y:0,hp:.25}];
for(const bank of Object.values(SG10_ART))for(const a of bank){BOFX.img[a.key]=a.path;XART._src[a.key]=a.path;}
for(const [code,kind]of Object.entries(SG10.routes)){PASSWORDS[code]=1;ON5_CODES[code]={stage:1,role:'mini',kind,name:SG10.specs[SG10.kinds[kind]].name};}
function sg10Log(name,data={}){SG10.events.push({name,t:SG10.clock,...data});if(SG10.events.length>160)SG10.events.shift();}
function sg10Keys(unit){return Object.entries(SG10_ART).filter(([k])=>k.startsWith(unit+'_')||k==='decals').flatMap(([,a])=>a.map(q=>q.key));}
function sg10Ready(b){return !!b?._sg10&&sg10Keys(b._sg10.unit).every(k=>XART.rdy(k));}
function sg10Reset(){SG10.fx=[];SG10.debris=[];SG10.decals=[];SG10.masks.clear();}
function sg10Sfx(b,cue,gap=.12){stageRevisionCue(b,cue,gap);}
function sg10Cell(bank,index,x,y,k,angle=0,white=false){
 const list=SG10_ART[bank],a=list?.[((index%list.length)+list.length)%list.length];if(!a||!XART.rdy(a.key))return;
 const im=white?xartTint(a.key,'#ffffff',1):XART.get(a.key);if(!im)return;
 ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();
}
function sg10Mask(a){
 if(SG10.masks.has(a.key))return SG10.masks.get(a.key);if(!XART.rdy(a.key))return null;
 const cv=document.createElement('canvas');cv.width=a.w;cv.height=a.h;const g=cv.getContext('2d');
 g.drawImage(XART.get(a.key),0,0,a.w,a.h);const data=g.getImageData(0,0,a.w,a.h).data;
 // The state harness has no real image pixels; Chromium always takes the full
 // authored mask. Bounds remain available to the state harness's geometry checks.
 if(data.length!==a.w*a.h*4)return null;
 const mask=new Uint8Array(a.w*a.h);for(let i=0;i<mask.length;i++)mask[i]=data[i*4+3];SG10.masks.set(a.key,mask);return mask;
}
function sg10PartCell(b,m){
 const S=b._sg10,p=S.parts[m.id],ratio=m.id==='hull'?b.hp/b.maxhp:p.hp/p.maxhp;
 let bank=S.unit+'_'+m.part,index=['pod','reactor','sensor'].includes(m.part)?0:Math.floor(S.time*16)%16;
 if(m.id==='weapon')index=S.attack?Math.min(15,Math.floor(S.attack.t/S.attack.life*16)):0;
 if(ratio<.67){bank+='_damage';index=ratio<.34?1:0;}
 return {bank,index,a:SG10_ART[bank][index]};
}
function sg10Box(b,m){
 const S=b._sg10,q=sg10PartCell(b,m),a=q.a,k=S.k,ox=b.x+m.x*k-a.pivot[0]*k,oy=b.y+m.y*k-a.pivot[1]*k;
 return {...q,m,k,ox,oy,l:ox+a.bounds[0]*k,r:ox+a.bounds[2]*k,top:oy+a.bounds[1]*k,bot:oy+a.bounds[3]*k};
}
function sg10At(b,x,y,pad=0){
 if(!b?._sg10||b.dead||b.enter)return null;
 for(let i=SG10_RIG.length-1;i>=0;i--){const m=SG10_RIG[i],p=b._sg10.parts[m.id];if(p.gone)continue;const q=sg10Box(b,m);
  if(x<q.l-pad||x>q.r+pad||y<q.top-pad||y>q.bot+pad)continue;
  const mask=sg10Mask(q.a);if(!mask)return m.id;
  for(const [dx,dy]of [[0,0],[-pad,0],[pad,0],[0,-pad],[0,pad]]){
   const px=Math.floor((x+dx-q.ox)/q.k),py=Math.floor((y+dy-q.oy)/q.k);
   if(px>=0&&py>=0&&px<q.a.w&&py<q.a.h&&mask[py*q.a.w+px]>=96)return m.id;
  }
 }return null;
}
function sg10Beam(b,beam){
 if(!b?._sg10||b.dead||b.enter)return null;const r=playerBeamRange(beam);if(!r)return null;let best=null;
 for(const m of SG10_RIG){if(b._sg10.parts[m.id].gone)continue;const q=sg10Box(b,m);
  const l=Math.max(q.l,r.x-r.half),right=Math.min(q.r,r.x+r.half),top=Math.max(q.top,r.top),bot=Math.min(q.bot,r.bot);
  if(right<=l||bot<=top)continue;let x=clamp(r.x,l,right),y=bot-.1;const mask=sg10Mask(q.a);
  if(mask){let found=false;
   const x0=Math.max(0,Math.floor((l-q.ox)/q.k)),x1=Math.min(q.a.w-1,Math.floor((right-q.ox)/q.k));
   const y0=Math.max(0,Math.floor((top-q.oy)/q.k)),y1=Math.min(q.a.h-1,Math.floor((bot-q.oy)/q.k));
   for(let py=y1;py>=y0&&!found;py--)for(let px=x0;px<=x1;px++)if(mask[py*q.a.w+px]>=96){x=q.ox+(px+.5)*q.k;y=q.oy+(py+.5)*q.k;found=true;break;}
   if(!found)continue;
  }
  if(!best||y>=best.entry)best={x,y,entry:y,key:m.id};
 }return best;
}
function sg10Point(b,m){
 const S=b._sg10,a=SG10_ART[S.unit+'_'+m.part][0],mask=sg10Mask(a);
 const points=S.lockPixels||(S.lockPixels={}),point=points[m.part];
 let px=point?.x??Math.floor((a.bounds[0]+a.bounds[2])/2),py=point?.y??Math.floor((a.bounds[1]+a.bounds[3])/2);
 if(!point&&mask&&mask[py*a.w+px]<160){let best=Infinity,bestPoint=null;
  for(let y=a.bounds[1];y<a.bounds[3];y++)for(let x=a.bounds[0];x<a.bounds[2];x++)if(mask[y*a.w+x]>=160){
   const d=(x-px)**2+(y-py)**2;if(d<best){best=d;bestPoint={x,y};}}
  if(bestPoint){px=bestPoint.x;py=bestPoint.y;}
 }
 if(mask&&!point)points[m.part]={x:px,y:py};
 return {x:b.x+(m.x+px+.5-a.pivot[0])*S.k,y:b.y+(m.y+py+.5-a.pivot[1])*S.k};
}
function sg10Sync(b){const S=b._sg10;b._drawY=b.y+S.centerY;b._drawW=b.w;b._drawH=b.h;S.parts.hull.hp=Math.max(0,b.hp);}
function sg10Init(b,unit){
 const spec=SG10.specs[unit],base=Math.max(300,b.maxhp||900);b.name=spec.name;b.mini=true;
 b.hp=b.maxhp=Math.ceil(base*spec.hp);b.flash=0;b.fireCd=999;b.enter=true;b._deathFxStarted=true;
 const parts=Object.fromEntries(SG10_RIG.map(m=>[m.id,{hp:Math.ceil(b.maxhp*m.hp),maxhp:Math.ceil(b.maxhp*m.hp),gone:false,flash:0}]));
 let l=Infinity,r=-Infinity,top=Infinity,bot=-Infinity;
 for(const m of SG10_RIG){const a=SG10_ART[unit+'_'+m.part][0];l=Math.min(l,m.x+a.bounds[0]-a.pivot[0]);r=Math.max(r,m.x+a.bounds[2]-a.pivot[0]);}
 const k=spec.width/(r-l);
 for(const m of SG10_RIG)for(const a of [...SG10_ART[unit+'_'+m.part],...SG10_ART[unit+'_'+m.part+'_damage'].slice(0,2)]){
  top=Math.min(top,(m.y+a.bounds[1]-a.pivot[1])*k);bot=Math.max(bot,(m.y+a.bounds[3]-a.pivot[1])*k);}
 b.w=spec.width;b.h=bot-top;b.x=camLeftX()+viewW()/2;b.y=PLAY.y-top-b.h-30;
 b.ty=Math.max(PLAY.y+34-top,PLAY.y+PLAY.h*.22);
 b._sg10={unit,k,parts,time:0,arrival:0,centerY:(top+bot)/2,top,bot,idx:0,attack:null,rest:1.1,side:1};
 sg10Sync(b);stageLoadBegin(1,sg10Keys(unit).concat(['nbret_'+_pilotKey(),'bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall']));
 stageRevisionWarm('razorback');Audio.SFX.bossAlarm?.();sg10Log('spawn',{unit,hp:b.maxhp});return b;
}
function sg10Burst(unit,bank,x,y,k,life=.65,extra={}){
 const q={unit,bank,x,y,k,t:0,life,...extra};SG10.fx.push(q);if(SG10.fx.length>80)SG10.fx.shift();return q;
}
function sg10Decal(unit,x,y,k){const row=unit==='sonic'?0:unit==='devastator'?4:8;
 SG10.decals.push({f:row+(SG10.decals.length%4),x,y,k,scroll:mapScroll});if(SG10.decals.length>24)SG10.decals.shift();}
function sg10Break(b,id,delay=0){
 const S=b._sg10,p=S.parts[id],m=SG10_RIG.find(q=>q.id===id);if(!p||p.gone)return;
 const ratio=id==='hull'?b.hp/b.maxhp:p.hp/p.maxhp;p.gone=true;p.hp=0;
 SG10.debris.push({unit:S.unit,part:m.part,x:b.x+m.x*S.k,y:b.y+m.y*S.k,k:S.k,
  t:-delay,life:.75,vx:m.x<0?-84:m.x>0?84:25,vy:-64,spin:0,held:ratio<.34?1:ratio<.67?0:-1});
 sg10Burst(S.unit,'impact',b.x+m.x*S.k,b.y+m.y*S.k,.20,.6,{t:-delay});
 if(id==='weapon'){S.attack=null;S.rest=.6;}sg10Sfx(b,'razorbackRocket',.14);av3Sound?.('module_break');
 shake=Math.max(shake,4);sg10Log('moduleBreak',{unit:S.unit,id});
}
function sg10Death(b){
 if(b.dead)return;b.hp=0;b.dead=true;b.dying=0;b._sg10.attack=null;
 for(const [i,m]of SG10_RIG.entries())sg10Break(b,m.id,i*.08);
 for(const q of eBullets)if(q._sg10Owner===b){q.dead=true;q._sg10Done=true;}
 sg10Burst(b._sg10.unit,'explosion',b.x,b._drawY,.40,1.6,{t:-.50});
 sg10Decal(b._sg10.unit,b.x,b._drawY,.65);achievementEncounterDefeat(b,'miniboss');Audio.SFX.expBig?.();shake=Math.max(shake,9);sg10Log('defeat',{unit:b._sg10.unit});
}
function sg10Damage(b,dmg,hx,hy,id=null){
 if(!b?._sg10||b.dead||b.enter||!(dmg>0))return 0;
 if(typeof er26DamageClamp==='function')dmg=er26DamageClamp(b,dmg);if(!(dmg>0))return 0;
 const S=b._sg10;let beam=null;
 if(!id&&_dmgBullet?.kind==='beam'){beam=sg10Beam(b,_dmgBullet);if(!beam)return 0;id=beam.key;hx=beam.x;hy=beam.y;}
 if(!id&&Number.isFinite(hx)&&Number.isFinite(hy))id=sg10At(b,hx,hy,Math.min(4,(_dmgBullet?.w||0)*.25));
 if(!id&&Number.isFinite(hx)&&Number.isFinite(hy))return 0;
 const before=b.hp,amount=enemyPoolDamage(b,'hp',dmg,'siege:'+S.unit,'maxhp');b.flash=.13;markHit(b);weaponHitSfx('normal');
 const targets=id?[id]:SG10_RIG.filter(m=>m.id!=='hull'&&!S.parts[m.id].gone).map(m=>m.id);
 for(const key of targets){const p=S.parts[key];if(!p||p.gone)continue;p.flash=.16;
  if(key!=='hull'){p.hp=Math.max(0,p.hp-amount/(id?1:Math.max(1,targets.length)));if(p.hp<=0)sg10Break(b,key);}}
 sg10Sync(b);const point=Number.isFinite(hx)?{x:hx,y:hy}:{x:b.x,y:b._drawY};sg10Burst(S.unit,'impact',point.x,point.y,.10,.35);
 if(typeof stageStats!=='undefined')stageStats.dmgDealt+=amount;if(b.hp<=0)sg10Death(b);return before-b.hp;
}
function sg10Muzzle(b,slot=0,pod=false){const S=b._sg10;
 if(pod){const m=SG10_RIG.find(q=>q.id===(slot?'podR':'podL'));const a=SG10_ART[S.unit+'_pod'][0];return{x:b.x+m.x*S.k,y:b.y+(m.y+a.bounds[3]-a.pivot[1])*S.k};}
 const a=SG10_ART[S.unit+'_weapon'][0];return{x:b.x+(slot?1:-1)*(S.unit==='sonic'?40:S.unit==='devastator'?39:35)*S.k,y:b.y+(a.bounds[3]-a.pivot[1]-4)*S.k};
}
function sg10StartAttack(b){
 const S=b._sg10,rank=['easy','normal','hard','furious'].indexOf(diffKey),book=S.unit==='sonic'?['pulse','charge','sweep']:S.unit==='devastator'?['cannons','fan','cannons']:['missiles','fan','lock'];
 let kind=book[S.idx++%book.length];if(S.parts.weapon.gone)kind='pods';
 const p=targetShip(b.x,b.y),charged=kind==='charge',warn=charged?1.8:rank>=2?.72:.92;
 const count=kind==='charge'?1:kind==='pods'?4:kind==='cannons'?6+Math.max(0,rank)*2:kind==='missiles'||kind==='lock'?6+Math.max(0,rank-1)*2:4+Math.max(0,rank)*2;
 const spacing=kind==='charge'?.25:kind==='cannons'?.16:kind==='missiles'||kind==='lock'?.17:.25;
 S.attack={kind,charged,t:0,warn,life:warn+count*spacing+.55,count,spacing,emitted:0,target:{x:p.x,y:Math.max(p.y,b._drawY+b.h*.5+36)}};
 sg10Sfx(b,'razorbackCharge',.2);sg10Log('attack',{unit:S.unit,kind});
}
function sg10Release(b,A,i){
 const S=b._sg10,unit=S.unit,slot=i%2,pod=A.kind==='pods',p=sg10Muzzle(b,slot,pod);
 if(pod&&S.parts[slot?'podR':'podL'].gone&&S.parts[slot?'podL':'podR'].gone)return;
 if(pod&&S.parts[slot?'podR':'podL'].gone)return;
 const speed=(unit==='sonic'?245:unit==='devastator'?300:220)*Math.min(1.16,DIFF.ebSpeed||1),fan=A.kind==='fan'||A.kind==='sweep';
 const tx=A.target.x+(fan?(i-(A.count-1)/2)*27:0),ty=Math.max(A.target.y,p.y+55),angle=clamp(Math.atan2(ty-p.y,tx-p.x),.35,Math.PI-.35);
 const missile=unit==='deviator',k=unit==='sonic'?(A.charged?.66:.28):unit==='devastator'?.27:.28;
 const q={kind:missile?'sg10missile':'sg10pressure',x:p.x,y:p.y,vx:Math.cos(angle)*speed/60,vy:Math.sin(angle)*speed/60,
  spd:speed/60,ang:angle,w:A.charged?22:missile?10:14,h:A.charged?28:missile?18:18,t:0,dmg:1,
  hp:missile?(diffKey==='furious'?3:2):undefined,_shootable:missile,_weaponProof:!missile,_s3kOriginalProof:!missile,_energyOrdnance:missile,homing:false,
  _sg10Owner:b,_sg10Unit:unit,_sg10K:k,_sg10Charged:A.charged,_sg10Target:{x:p.x+Math.cos(angle)*Math.hypot(tx-p.x,ty-p.y),y:p.y+Math.sin(angle)*Math.hypot(tx-p.x,ty-p.y)},_sg10Done:false};
 eBullets.push(q);sg10Burst(unit,'impact',p.x,p.y,.10,.30);sg10Sfx(b,missile?'razorbackRocket':'razorbackPressure',.11);sg10Log('shot',{unit,charged:A.charged});
}
function sg10Detonate(q,hazard=true){
 if(q._sg10Done)return;q._sg10Done=true;q.dead=true;const unit=q._sg10Unit,charged=q._sg10Charged&&hazard,bank=unit+'_explosion';
 const k=charged?Math.sqrt(viewW()*PLAY.h*.33/SG10_METRICS[bank].peakInk):unit==='sonic'?.24:unit==='devastator'?.24:.20;
 let x=q.x,y=q.y;if(charged){const a=SG10_ART[bank][0];
  x=clamp(x,camLeftX()+a.pivot[0]*k+4,camRightX()-(a.w-a.pivot[0])*k-4);
  y=clamp(y,PLAY.y+a.pivot[1]*k+4,PLAY.y+PLAY.h-(a.h-a.pivot[1])*k-4);}
 sg10Burst(unit,'explosion',x,y,k,charged?1.6:1.15,{hazard,charged,hitSeats:[],warm:charged?.22:.06,owner:q._sg10Owner});
 sg10Burst(unit,'impact',q.x,q.y,.18,.5);sg10Decal(unit,q.x,q.y,charged?.9:.3);
 sg10Sfx(q._sg10Owner,'razorbackPressure',.1);shake=Math.max(shake,charged?6:2);sg10Log('detonation',{unit,charged,hazard});
}
function sg10Tick(b,dt){
 const S=b._sg10;b.t+=dt;S.time+=dt;b.flash=Math.max(0,b.flash-dt);for(const p of Object.values(S.parts))p.flash=Math.max(0,p.flash-dt);
 if(b.dead){b.dying+=dt;if(b.dying>=2.5){continueRewardResolve(b,b.x,b._drawY,'miniboss');dropPowerup(b.x,b._drawY,'weapon');subBoss=null;subBossActive=false;subBossDone=true;}return;}
 if(!sg10Ready(b))return;
 if(b.enter){S.arrival+=dt;b.y=Math.min(b.ty,b.y+135*dt);sg10Sync(b);if(b.y>=b.ty){b.enter=false;S.rest=1.15;}return;}
 const crippled=(S.parts.trackL.gone?1:0)+(S.parts.trackR.gone?1:0),span=Math.max(0,(viewW()-b.w)/2-20),mid=camLeftX()+viewW()/2;
 const goal=mid+Math.sin(S.time*.65)*span*.75,move=(crippled===2?0:crippled?24:48)*dt;
 if(!S.attack||S.attack.t<S.attack.warn*.6)b.x+=clamp(goal-b.x,-move,move);sg10Sync(b);
 S.rest-=dt;if(!S.attack&&S.rest<=0)sg10StartAttack(b);
 const A=S.attack;if(A){A.t+=dt;
  while(A.emitted<A.count&&A.t>=A.warn+A.emitted*A.spacing){sg10Release(b,A,A.emitted);A.emitted++;}
  if(A.t>=A.life){S.attack=null;S.rest=diffKey==='furious'?.60:diffKey==='hard'?.85:1.15;}}
}
function sg10Draw(b,tells=true){
 const S=b._sg10;if(!S)return;
 for(const m of SG10_RIG){const p=S.parts[m.id];if(p.gone)continue;const q=sg10PartCell(b,m);
  sg10Cell(q.bank,q.index,b.x+m.x*S.k,b.y+m.y*S.k,S.k,0,b.flash>0||p.flash>0);}
 const A=S.attack;if(!tells||!A||A.t>=A.warn||b.enter)return;const p=sg10Muzzle(b,0),other=sg10Muzzle(b,1),progress=A.t/A.warn;
 sg10Cell(S.unit+'_charge',Math.min(15,Math.floor(progress*16)),(p.x+other.x)/2,p.y,S.unit==='sonic'?.46:.28);
 drawBossRetina(S.time,A.target.x,A.target.y,S.time*2,.95);
 const angle=Math.atan2(A.target.y-p.y,A.target.x-p.x);ctx.save();ctx.translate(p.x,p.y);ctx.rotate(angle-Math.PI/2);
 l23FovDraw(b,{family:'inferno',angles:[angle],t:A.t,len:Math.hypot(A.target.x-p.x,A.target.y-p.y),alpha:.55},0,p,progress,22);ctx.restore();
}
function sg10FXTick(dt){
 SG10.clock+=dt;
 for(const d of SG10.debris){d.t+=dt;if(d.t<0)continue;d.x+=d.vx*dt;d.y+=d.vy*dt;d.vy+=160*dt;d.spin+=dt*(d.vx<0?-5:5);
  if(d.t>=d.life){sg10Burst(d.unit,'explosion',d.x,d.y,.20,1.25);sg10Decal(d.unit,d.x,d.y,.27);d.dead=true;}}
 SG10.debris=SG10.debris.filter(d=>!d.dead);
 for(const q of SG10.fx){q.t+=dt;if(!q.hazard||q.t<q.warm||q.t>.65||q.owner?.dead)continue;
  const a=SG10_ART[q.unit+'_explosion'][0],rx=a.w*q.k*(q.charged?.39:.32),ry=a.h*q.k*(q.charged?.39:.32);
  for(const seat of seatList())withSeat(seat,()=>{if(q.hitSeats.includes(seat)||player.dead||player.out||player.invuln>0)return;
   if(((player.x-q.x)/rx)**2+((player.y-q.y)/ry)**2<=1){q.hitSeats.push(seat);playerHit('Siege blast');}});
 }
 SG10.fx=SG10.fx.filter(q=>q.t<q.life);SG10.decals=SG10.decals.filter(d=>d.y+mapScroll-d.scroll<VH+100);
}
function sg10FXDraw(){
 for(const d of SG10.decals)sg10Cell('decals',d.f,d.x,d.y+mapScroll-d.scroll,d.k);
 for(const d of SG10.debris)sg10Cell(d.unit+'_'+d.part+(d.t>=0||d.held>=0?'_damage':''),d.t>=0?2:d.held>=0?d.held:0,d.x,d.y,d.k,d.t>=0?d.spin:0);
 for(const q of SG10.fx)if(q.t>=0){const n=SG10_ART[q.unit+'_'+q.bank].length;sg10Cell(q.unit+'_'+q.bank,Math.min(n-1,Math.floor(q.t/q.life*n)),q.x,q.y,q.k);}
}
spawnSubBoss__inner=function(kind){const r=SG10.base.spawn.apply(this,arguments),unit=SG10.kinds[kind];if(unit&&subBoss)sg10Init(subBoss,unit);return unit?subBoss:r;};
updateSubBoss=function(dt){if(subBoss?._sg10)return sg10Tick(subBoss,dt);return SG10.base.tick.apply(this,arguments);};
drawSubBoss=function(){if(subBoss?._sg10){drawSubBossBar(subBoss);sg10Draw(subBoss);return;}return SG10.base.draw.apply(this,arguments);};
hitSubBoss=function(dmg,hx,hy){if(subBoss?._sg10)return sg10Damage(subBoss,dmg,hx,hy);return SG10.base.hit.apply(this,arguments);};
subBossHitPart=function(x,y){return subBoss?._sg10?sg10At(subBoss,x,y):SG10.base.at.apply(this,arguments);};
subBossSolidAt=function(x,y){return subBoss?._sg10?sg10At(subBoss,x,y,Math.min(4,(_dmgBullet?.w||0)*.25))!==null:SG10.base.solid.apply(this,arguments);};
subBossBeamImpact=function(b,beam){return b?._sg10?sg10Beam(b,beam):SG10.base.beam.apply(this,arguments);};
retinaBossTargets=function(b){if(!b?._sg10)return SG10.base.targets.apply(this,arguments);if(b.dead||b.enter)return [];
 return SG10_RIG.filter(m=>!b._sg10.parts[m.id].gone).map(m=>retinaDynamicPiece(b,m.id,'siege module',()=>({...sg10Point(b,m),hp:b._sg10.parts[m.id].hp,dead:b.dead||b.enter||b._sg10.parts[m.id].gone}),dmg=>sg10Damage(b,dmg,null,null,m.id),28,30));};
ordnanceBreak1002=function(q){if(q?._sg10Unit){q._intercepted=true;sg10Detonate(q,false);return;}return SG10.base.break.apply(this,arguments);};
updatePlay=function(dt){
 sg10FXTick(dt);const old=eBullets.filter(q=>q._sg10Unit);
 for(const q of old)if(!q.dead&&!q._sg10Done){const p=q._sg10Target,step=Math.hypot(q.vx,q.vy)*dt*60;
  if(Math.hypot(p.x-q.x,p.y-q.y)<=step+3){q.x=p.x;q.y=p.y;sg10Detonate(q,true);}}
 const r=SG10.base.play.apply(this,arguments);
 for(const q of old)if((q.dead||!eBullets.includes(q))&&!q._sg10Done&&q.x>camLeftX()-20&&q.x<camRightX()+20&&q.y>PLAY.y-10&&q.y<VH+10)sg10Detonate(q,false);
 return r;
};
drawBullets=function(){const all=eBullets;try{eBullets=all.filter(q=>!q._sg10Unit);SG10.base.bullets.apply(this,arguments);}finally{eBullets=all;}
 for(const q of all)if(q._sg10Unit&&!q.dead)sg10Cell(q._sg10Unit+'_projectile',Math.floor((q.t||0)*24)%16,q.x,q.y,q._sg10K,q.ang-Math.PI/2);};
drawEffects=function(){const r=SG10.base.effects.apply(this,arguments);sg10FXDraw();return r;};
encounterDamageOverlay=function(b){if(b?._sg10)return;return SG10.base.damageDraw.apply(this,arguments);};
beginStage=function(){sg10Reset();return SG10.base.begin.apply(this,arguments);};
bofDerivedCachesRetire=function(){SG10.masks.clear();return SG10.base.retire.apply(this,arguments);};
stageLoadBegin=function(n,keys){const unit=SG10.launchUnit;return SG10.base.load.call(this,n,[...(keys||[]),...(n===1&&unit?sg10Keys(unit):[])]);};
startRun=function(){SG10.launchUnit=SG10.kinds[ON5.pending?.kind]||null;try{return SG10.base.start.apply(this,arguments);}finally{SG10.launchUnit=null;}};
submitPassword=function(){const code=String(pwInput).trim().toUpperCase();if(SG10.routes[code])pwInput=code;return SG10.base.submit.apply(this,arguments);};
pc5Pages=function(){return SG10.base.pages().map(page=>({...page,rows:page.rows.map(([code,label])=>[code,SG10.routes[code]?SG10.specs[SG10.kinds[SG10.routes[code]]].name:label])}));};
window.BOFSiegeTanks=SG10;
