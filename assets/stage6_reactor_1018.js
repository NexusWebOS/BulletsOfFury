"use strict";
/* Stage6: Fortress reactor, carrier launch bays, attached turbine damage and
   the original continuous carrier -> Nightwing encounter. No Harrier reactor. */
const S6R18={events:[],draws:{reactor:0,shutter:0,smoke:0,burst:0,radio:0},base:{
 tick:warhiveTick,draw:warhiveDraw,die:bossDie,open:sc13Open,
 core:sc13Core,carrierDraw:whvDrawCarrier,aceDraw:whvDrawAce,
 load:stageLoadBegin,radioTick:s6WingRadioTick,radioDraw:s6WingRadioDraw,
 rec:debugRecFrame,refresh:SC12.refresh,play:updatePlay,launch:whvLaunchJet}};
function s6r18Owns(b){return run.stage===6&&!run._gp4StageX&&!!(b?._cargo17Mini||b?._carrier17||b?._s6CarrierFall);}
function s6r18State(b){return b._s6r18||(b._s6r18={open:0,opening:false,exposed:false,
 bay:{mode:'wait',t:0,open:0,launched:0,next:0},drift:{x:0,v:0},fanFx:new Map()});}
function s6r18Log(event,b,data={}){S6R18.events.push({event,mini:!!b?._cargo17Mini,t:b?.t,...data});if(S6R18.events.length>280)S6R18.events.shift();}
function s6r18PartsDown(b){return b?._cargo17Mini?b._cargo13.guns.every(g=>g.dead):b?._carrier17?.parts.every(p=>p.dead);}
function s6r18Warm(){for(const k of ['whv_closed_w','whv_open_w','mr27_corefx','efx_burst_fire',
 'xelite_hivewing_idle',...Array.from({length:8},(_,i)=>'nsd_chim_'+i),...Array.from({length:8},(_,i)=>'nxp_upward_'+i)])XART.rdy(k);
 gp4AceWarm();enc30Warm(6);}
stageLoadBegin=function(n,keys){if(n===6){s6r18Warm();Snd.prepare?.(['bossShieldStatic','bossShieldTeleport','impactMetal','expBoss','launch']);}
 return S6R18.base.load.call(this,n,n===6?[...(keys||[]),'mr27_corefx','whv_closed_w','whv_open_w','efx_burst_fire']:keys);};
sc13Core=function(b){if(!b?._cargo17Mini)return S6R18.base.core.apply(this,arguments);
 // The actual cyan vent at source(512,251), rather than an invisible point on
 // the closed nose armour. Art, primary hits, beams and Retina share this point.
 return{x:b._cargo13.x,y:b._cargo13.y-5*sc13Scale(b)};};
sc13Open=function(b){return b?._cargo17Mini?b._cargo13.guns.every(g=>g.dead)&&s6r18State(b).open>=.999:S6R18.base.open.apply(this,arguments);};
function s6r18Opening(b,dt){if(!b?._cargo17Mini)return;const S=s6r18State(b);if(b.dead||!s6r18PartsDown(b))return;
 if(!S.opening){S.opening=true;S.bay.mode='reactor';S.bay.open=0;
  s6r18Log('reactor-opening',b);Snd.play('bossShieldStatic',1);s6WingSay('COLE','ALL WEAPONS DOWN. THE REACTOR HATCH IS OPENING!');}
 S.open=clamp(S.open+dt/.85,0,1);
 if(S.open>=.999&&!S.exposed){S.exposed=true;showCallout('shoot',1.6);Snd.play('bossShieldTeleport',1);
  s6WingSay('COLE','ENERGY CORE EXPOSED! PUT EVERYTHING INTO IT!');s6r18Log('reactor-exposed',b);}
}
function s6r18Bay(b,dt){const C=b._carrier17,W=b._whv,S=s6r18State(b),D=S.bay;
 if(C.phase!=='fight'){
  D.open=Math.max(0,D.open-dt/.6);D.mode='wait';D.t=0;D.launched=0;C.bayOpen=D.open>0;return;
 }
 D.t+=dt;
 if(D.mode==='wait'&&D.t>=.65){D.mode='opening';D.t=0;D.launched=0;D.next=0;
  s6WingSay('DECKER','HARRIER BAYS OPENING. ELITE FIGHTERS INBOUND!');Snd.play('impactMetal',.8);s6r18Log('bay-opening',b);}
 else if(D.mode==='opening'){
  D.open=clamp(D.t/.65,0,1);if(D.open>=1){D.mode='launch';D.t=0;}
 }else if(D.mode==='launch'){
  D.next-=dt;const alive=whvJetsAlive(W),cap=W.jetN||4;
  if(D.next<=0&&D.launched<cap){
   if(alive<cap){const before=W.jets.length;whvLaunchJet(b);if(W.jets.length>before){D.launched++;s6r18Log('jet-launch',b,{count:D.launched,alive:W.jets.length});}}
   else D.launched=cap;D.next=W.hard?.5:.55;
  }
  if(D.launched>=cap){D.mode='hold';D.t=0;}
 }else if(D.mode==='hold'&&D.t>=1.4){D.mode='closing';D.t=0;Snd.play('impactMetal',.65);s6r18Log('bay-closing',b);}
 else if(D.mode==='closing'){D.open=1-clamp(D.t/.65,0,1);if(D.open<=0){D.mode='cool';D.t=0;}}
 else if(D.mode==='cool'&&D.t>7&&whvJetsAlive(W)<(W.jetN||4)){D.mode='wait';D.t=0;}
 C.bayOpen=D.open>0;
}
whvLaunchJet=function(b){if(roster17Active(b)){
 const W=b._whv,used=new Set(W.jets.filter(e=>e&&!e.dead&&e._dyingT==null&&enemies.includes(e)).map(e=>e._hwSlot));
 const free=Array.from({length:W.jetN||4},(_,i)=>i).find(i=>!used.has(i));if(free==null)return;
 // Refill a real vacant squadron slot, rather than letting later bay cycles
 // count beyond the formation and send replacements outside the playfield.
 W.launched=free;
 }return S6R18.base.launch.apply(this,arguments);};
function s6r18FanTick(b,C,dt){const S=s6r18State(b);let down=0,side=0;
 for(const p of C.parts.filter(p=>p.kind==='fan')){
  let F=S.fanFx.get(p.id);
  if(!F){F={t:0,next:0,broken:false,bursts:[]};S.fanFx.set(p.id,F);}
  if(p.dead){down++;side+=p.id==='L'?1:-1;
   if(!F.broken){F.broken=true;F.t=0;F.bursts=[0,.10,.21].map((delay,i)=>({t:-delay,life:.55,dx:(i-1)*9,dy:i%2?8:-7,size:42+i*8}));s6r18Log('fan-destroyed',b,{id:p.id});}
   F.t+=dt;F.next-=dt;
   if(F.next<=0){F.next=F.t<1.6?.18:.55;F.bursts.push({t:0,life:.55,dx:rnd(-13,13),dy:rnd(-10,10),size:F.t<1.6?48:32});}
  }
  for(const q of F.bursts)q.t+=dt;F.bursts=F.bursts.filter(q=>q.t<q.life);
 }
 if(down&&C.phase==='fight'){
  // Relative spring drift: the pilot tries to counter the missing thrust.
  // Apply after the nominal path is set, so offsets never accumulate on a
  // departure and every hitbox/muzzle follows the same translated whole hull.
  const D=S.drift;D.v+=(side*13+Math.sin(C.age*3.1)*8-D.x*2.8-D.v*2.9)*dt;D.x+=D.v*dt;
  const jitter=(.55+down*.45)*Math.sin(C.age*29);
  b.x+=D.x+jitter;b.y+=Math.sin(C.age*7.8)*(1+down*.6);shake=Math.max(shake,.25+down*.25);
 }
}
warhiveTick=function(b,dt){const out=S6R18.base.tick.apply(this,arguments);if(!s6r18Owns(b))return out;
 if(b._carrier17&&!b.dead){s6r18Bay(b,dt);s6r18FanTick(b,b._carrier17,dt);roster17Sync(b);}
 else if(b._cargo17Mini&&!b.dead)s6r18Opening(b,dt);
 else if(b._s6CarrierFall&&b._whv.mode!=='ace'){roster17FlashTick(b._s6CarrierFall,dt);s6r18FanTick(b,b._s6CarrierFall,dt);}
 return out;};
function s6r18CarrierFall(b){const C=b._carrier17,W=b._whv;
 C.depth=false;C.scale=1;C.phase='fall';b._s6CarrierFall=C;delete b._carrier17;
 b.hp=1;b.dead=false;b._noHit=false;W.parts.door.hp=0;W.parts.door.dead=true;W.doorOpen=true;
 // Continue the existing owner without awarding stage clear or boss loot.
 // Its falling carrier spawns the authored giant blue Nightwing, with the
 // original evasions, attacks, hit feedback and eventual native defeat path.
 whvDeathStart(b);s6r18Warm();s6WingSay('DECKER','CARRIER GOING DOWN! GIANT BLUE FIGHTER LEAVING THE BAY!');s6r18Log('carrier-fall',b);
}
bossDie=function(){if(roster17Active(boss)&&s6r18PartsDown(boss))return s6r18CarrierFall(boss);
 return S6R18.base.die.apply(this,arguments);};

function s6r18Shutters(key,sourceRect,x,y,k,open){if(!XART.rdy(key))return;
 const im=XART.get(key),[sx,sy,w,h]=sourceRect,half=w/2,shift=half*clamp(open,0,1);
 ctx.save();ctx.beginPath();ctx.rect(x-w*k/2,y-h*k/2,w*k,h*k);ctx.clip();ctx.imageSmoothingEnabled=false;
 for(const side of [-1,1]){const from=side<0?sx:sx+half,dx=x+(side<0?-half:0)*k+side*shift*k;
  ctx.drawImage(im,from,sy,half,h,dx,y-h*k/2,half*k,h*k);}
 ctx.restore();S6R18.draws.shutter++;
}
function s6r18CoreDraw(b,x,y,height,open,flash){if(open<=0)return;
 const im=mr27Cell('corefx',5+Math.floor(b.t*10)%3);if(!im)return;
 const k=height/im.height;ctx.save();ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,x-im.width*k/2,y-height/2,im.width*k,height);
 // Keep visible blue energy under sustained fire. Timers and markHit remain
 // native; only the core silhouette brightens, and inherited fade is retained.
 if(flash>0){const white=mr27Cell('corefx',5+Math.floor(b.t*10)%3,'#ffffff');ctx.globalAlpha*=clamp(flash*4,0,.55);ctx.drawImage(white,x-im.width*k/2,y-height/2,im.width*k,height);}
 ctx.restore();S6R18.draws.reactor++;
}
function s6r18FanDraw(b,C){const S=s6r18State(b),W=b._whv,cy=W.cy+(W.dy||0);
 for(const p of C.parts.filter(p=>p.kind==='fan')){
  const F=S.fanFx.get(p.id),ratio=p.hp/p.maxhp;if(!F||ratio>.75&&!p.dead)continue;
  const x=W.cx+p.dx*WHV_S,y=cy+p.dy*WHV_S,level=p.dead?3:ratio<.4?2:1,n=p.dead?3:level;
  for(let i=0;i<n;i++){const u=((b.t+i*.37)*.62)%1,size=(22+level*9)*(1+u*.6);
   if(weaponFeedbackArt('nsd_chim_'+(Math.floor(b.t*10)+i*2)%8,x+(i-(n-1)/2)*9+u*4,y-12-u*58,size,null,.72*(1-u),0,false))S6R18.draws.smoke++;
  }
  if(p.dead||ratio<.4)weaponFeedbackArt('nxp_upward_'+Math.floor(b.t*14)%8,x,y-6,p.dead?40:26,null,.95,0,false);
  for(const q of F.bursts)if(q.t>=0){efxFrame('efx_burst_fire',clamp(Math.floor(q.t/q.life*8),0,7),x+q.dx-q.size/2,y+q.dy-q.size/2,q.size,q.size,1);S6R18.draws.burst++;}
 }
}
function s6r18CarrierOverlay(b,C){const S=s6r18State(b),W=b._whv,x=W.cx,y=W.cy+(W.dy||0),unit=roster17HullScale(b),k=(C.scale||1)*unit;
 ctx.save();ctx.translate(x,y);ctx.scale(k,k);ctx.translate(-x,-y);
 const p={x,y:y+WHV_DOOR.y*WHV_S},open=b._s6CarrierFall?1:S.bay.open;
 s6r18Shutters('whv_closed_w',[214.5,148,83,82],p.x,p.y,WHV_S,open);
 s6r18FanDraw(b,C);ctx.restore();
 // Spawned fighters must emerge above the bay plate, never be painted under it.
 for(const e of W.jets)if(e&&!e.dead&&e._dyingT==null&&e.y<y+WHV_PLATE.h*WHV_S*unit*.55)drawEnemy(e);
}
warhiveDraw=function(b){const out=S6R18.base.draw.apply(this,arguments);if(!s6r18Owns(b)||b.dead)return out;
 if(b._carrier17)s6r18CarrierOverlay(b,b._carrier17);
 if(b._cargo17Mini&&b._cargo13.ready){const S=s6r18State(b),p=sc13Core(b),k=sc13Scale(b);
  s6r18CoreDraw(b,p.x,p.y,108*k,S.open,Math.max(b._cargo13.coreFl,b.flash||0));
  // Approved miniboss aperture: slide the actual original vent leaves while
  // the whole authored hull remains intact. No fitted or procedural sprites.
  s6r18Shutters('s6cargo13_hull',[477,192,70,118],p.x,p.y,k,S.open);
 }return out;};
whvDrawCarrier=function(b){if(!b._s6CarrierFall)return S6R18.base.carrierDraw.apply(this,arguments);
 const W=b._whv,alpha=W.t<3.6?1:Math.max(0,1-(W.t-3.6)/.8);if(alpha<=0)return;
 ctx.save();ctx.globalAlpha=alpha;roster17Draw(b,b._s6CarrierFall);s6r18CarrierOverlay(b,b._s6CarrierFall);ctx.restore();};
whvDrawAce=function(b){const A=b?._whv?.ace;
 if(!b?._s6CarrierFall||A?.st!=='emerge')return S6R18.base.aceDraw.apply(this,arguments);
 // The fighter begins inside the hangar, then approaches the player's plane.
 // One proportional depth scale keeps its actual authored pose intact.
 const u=clamp(A.t/.7,0,1),k=lerp(.48,1,u*u*(3-2*u));
 ctx.save();ctx.translate(A.x,A.y);ctx.scale(k,k);ctx.translate(-A.x,-A.y);
 const out=S6R18.base.aceDraw.apply(this,arguments);ctx.restore();return out;};

// Combat radio is independent of the allied-wing actor controller. In the
// side HUD its captions age and draw while the wing continues fighting.
function s6r18Lines(text,width,size){const out=[];let line='';for(const word of String(text).toUpperCase().split(' ')){
 const next=line?line+' '+word:word;if(line&&bmfMeasure('dialogue',next,size)>width){out.push(line);line=word;}else line=next;
 }if(line)out.push(line);return out;}
function s6r18Pages(L){const lines=s6r18Lines(L.full,314,24),pages=[];
 for(let i=0;i<lines.length;i+=4){const rows=lines.slice(i,i+4);pages.push({rows,dur:Math.max(4.5,rows.join(' ').length/25+1.4)});}return pages;}
s6WingRadioTick=function(W,dt){if(run.stage!==6||!SC12.active())return S6R18.base.radioTick.apply(this,arguments);
 if(!W?.line||!s6WingRadioVisible())return;const pages=s6r18Pages(W.line);W.line.t+=dt;
 if(W.line.t>=pages.reduce((n,p)=>n+p.dur,0)){W.line=null;SC12.invalidate();}};
s6WingRadioDraw=function(){if(run.stage===6&&SC12.active())return;return S6R18.base.radioDraw.apply(this,arguments);};
function s6r18RadioDraw(){if(run.stage!==6||!SC12.active()||!s6WingRadioVisible()||!bmfReady('dialogue'))return;
 const L=s6Wing.line,pages=s6r18Pages(L);let age=L.t,i=0;while(i<pages.length-1&&age>=pages[i].dur)age-=pages[i++].dur;
 if(SC12.mode!=='sides')return s6r18CompactRadio(L,pages[i]);
 const r=SC12_ART.wells.pilot,g=SC12.panels[0].getContext('2d'),source=XART.get(SC12_ART.key);if(!source)return;
 for(let seat=0;seat<seatList().length;seat++){g.save();g.translate(0,seat*1536);g.imageSmoothingEnabled=false;g.clearRect(...r);g.drawImage(source,...r,...r);
  g.beginPath();g.rect(r[0]+3,r[1]+3,r[2]-6,r[3]-6);g.clip();
  const pilot=L.who.toLowerCase(),key=REBEL_KEYS.includes(pilot)?'rr_portrait_'+pilot:commPortrait(pilot,'talk');
  if(XART.rdy(key)){const im=XART.get(key),k=Math.min(58/im.width,58/im.height);g.drawImage(im,r[0]+8,r[1]+4,im.width*k,im.height*k);}
  bmfDrawOn(g,'dialogue',L.who.toUpperCase(),r[0]+80,r[1]+20,29,'left');bmfDrawOn(g,'dialogue','FURY COMMS',r[0]+80,r[1]+47,20,'left');
  for(let j=0;j<pages[i].rows.length;j++)bmfDrawOn(g,'dialogue',pages[i].rows[j],r[0]+10,r[1]+78+j*28,24,'left');g.restore();
 }S6R18.draws.radio++;
}
function s6r18CompactRadio(L,page){const g=SC12.compact.getContext('2d');g.save();g.imageSmoothingEnabled=false;
 for(let seat=0;seat<seatList().length;seat++){const x=13,y=seat*SC12_ART.compactHeight*2+10,w=372;g.clearRect(x,y,w,132);g.fillStyle='#031421';g.fillRect(x,y,w,132);
  bmfDrawOn(g,'dialogue',L.who.toUpperCase(),x+8,y+7,22,'left');const rows=s6r18Lines(page.rows.join(' '),w-16,21);
  for(let i=0;i<Math.min(4,rows.length);i++)bmfDrawOn(g,'dialogue',rows[i],x+8,y+35+i*24,21,'left');}
 g.restore();S6R18.draws.radio++;
}
debugRecFrame=function(){const r=S6R18.base.rec.apply(this,arguments);s6r18RadioDraw();return r;};
SC12.refresh=function(){const r=S6R18.base.refresh.apply(this,arguments);s6r18RadioDraw();return r;};
updatePlay=function(dt){const W=s6Wing,L=W?.line,t=L?.t,out=S6R18.base.play.apply(this,arguments);
 if(run.stage===6&&W===s6Wing&&L&&W.line===L&&L.t===t)s6WingRadioTick(W,dt);return out;};
window.BOF_STAGE6_REPAIR={state:S6R18,opening:s6r18Opening,bay:s6r18Bay};
