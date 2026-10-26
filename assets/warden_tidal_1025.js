'use strict';
/* Oct25: the whole Tidal Sovereign, liquid reservoirs and a water arsenal.
   Native convergence, displayed HP budget, hits, death and rewards own the fight.
   One attack turn owns its complete warnings, ordnance and recovery. */
const WT25={events:[],owners:new Set(),frames:new Map(),serial:0,
 base:{load:stageLoadBegin,lateTick:late27Tick,lateDraw:late27Draw,hull:er26Hull,draw:shipBossDraw,mount:shipBossMount,fusionTick:s9FusionBossTick,
  update:updatePlay,intercept:enemyOrdnanceCanIntercept,element:enemyOrdnanceElement,rules:s3kOrdnanceRules,targetReady:target17Ready},
 book:['flood','geysers','mortars','mist','undertow','maelstrom'],
 cues:['bossfireTidalfusion','bossWeaponCharge','combatBeam0927','combatOrb0927','cfComboWater','missile']};
for(const a of Object.values(WT25_ART.sheets)){XART._src[a.key]=a.path;XART._src['nca_'+a.key]=a.path;}
for(const bank of Object.values(WT25_ART.banks))for(const f of bank.frames)BOFX.cells[f.key]=[bank.sheet,...f.rect];
function wt25Own(b){return !!(run.stage===9&&b?._ship==='tidalsovereign'&&(!b._s9fusion||b._s9fusion.phase==='tidal'));}
// The replacement water arsenal owns complete turns. The former supplemental
// targeter must not open a second, unrelated volley over flood/mortar recovery.
target17Ready=function(b,ports){return wt25Own(b)&&b._wt25?false:WT25.base.targetReady.apply(this,arguments);};
function wt25Log(b,event,data={}){WT25.events.push({event,time:b?._wt25?.clock||0,...data});if(WT25.events.length>500)WT25.events.shift();}
function wt25Keys(){return [...Object.values(WT25_ART.sheets).map(a=>a.key),S1W20_ART.key,'efx_geyser_water',
 ...['tidalpressurebeam','tidalpressurebeamtile','tidalgeyserimpact','tidalmaelstrom','tidalcutter','tidaltorpedo','tidalbubblemine'].flatMap(n=>Array.from({length:8},(_,i)=>n+'_'+i)),
 ...['bf22_water_muzzle','bf22_water_wave','bf22_water_orb'],...['green','yellow','red'].map(c=>'bmfx_fov_'+c+'_tall')];}
function wt25Warm(){return wt25Keys().map(k=>XART.rdy(k)).every(Boolean);}
stageLoadBegin=function(n,keys){if(n===9)for(const k of WT25.cues)Snd.prepare(k);return WT25.base.load.call(this,n,[...(keys||[]),...(n===9?wt25Keys():[])]);};
function wt25Point(b,x,y){const P=shipBossVisualPose(b),dx=(x-160)*b.w/320*P.sx,dy=(y-128)*b.h/256*P.sy,c=Math.cos(P.rot),s=Math.sin(P.rot);
 return{x:b.x+P.x+dx*c-dy*s,y:(b._drawY??b.y)+P.y+dx*s+dy*c};}
shipBossMount=function(b,slot){const p=wt25Own(b)&&WT25_ART.sockets[slot];return p?wt25Point(b,...p):WT25.base.mount.apply(this,arguments);};
function wt25Frame(key,t){const bank=WT25_ART.banks[key];if(!bank)return null;const f=Math.floor(Math.max(0,t)*WT25_ART.fps)%32,id=bank.frames[f].key;return XART.rdy(id)?XART.get(id):null;}
er26Hull=function(b,key){return wt25Own(b)&&!b.dead?wt25Frame(key,b._wt25?.clock||0)||WT25.base.hull.apply(this,arguments):WT25.base.hull.apply(this,arguments);};
function wt25Cue(b,key,gap=.18){combatAudio0927(b,key,gap);}
function wt25Init(b){if(b._wt25)return b._wt25;
 // Retain the existing encounter's native pool initialization exactly once.
 const A=late27Init(b,'tidal');A.suspended=true;A.mode='water25';A.paths=[];
 if(b._target17){b._target17.phase='recover';b._target17.t=0;}
 for(const q of eBullets)if(q._target17Owner===b)q.dead=true;
 const T=b._wt25={clock:0,seq:0,rest:1.10,attack:null,walls:[],geysers:[],mortars:[],flashes:[],history:[],home:{x:worldWidth()/2,y:Math.max(viewTopY()+136,b.h*.5+16)}};
 WT25.owners.add(b);wt25Log(b,'water-arsenal-ready',{hp:b.hp,maxhp:b.maxhp});return T;
}
s9FusionBossTick=function(b,dt){const before=b?._s9fusion?.phase,r=WT25.base.fusionTick.apply(this,arguments);
 // Initialize the established 5000*DIFF pool before the first live water frame.
 // Previously the generic fusion seed appeared for one frame, accepted hits,
 // then the late director reset it to its real pool on the following update.
 if(before==='fuse'&&b._s9fusion.phase==='tidal')wt25Init(b);return r;};
function wt25Flash(b,slot,size=44){const T=b._wt25;T.flashes.push({slot,t:0,size});if(T.flashes.length>12)T.flashes.shift();}
function wt25Angle(p,q){return Math.atan2(q.y-p.y,q.x-p.x);}
function wt25Line(b,slot,angle,width=20){const p=shipBossMount(b,slot);return{slot,...p,a:angle,ex:p.x+Math.cos(angle)*900,ey:p.y+Math.sin(angle)*900,width};}
function wt25Ordinary(q,b){if(!q)return q;Object.assign(q,{_wt25Owner:b,_wt25Born:b._wt25.clock,_weaponProof:true,_shootable:false,_s3kOriginalProof:false,_noArsenal:true,homing:false});delete q.hp;return q;}
function wt25Shot(b,slot,a,sp,kind='tidalcut',physical=false){const p=shipBossMount(b,slot);
 const q=physical?eShootT(p.x,p.y,a,sp,'emissile',{owner:b,noMuzzle:true,silent:true,w:12,h:28}):s9aShot(p.x,p.y,a,sp,kind,{owner:b,noMuzzle:true,silent:true,...(kind==='tidalmine'?{w:16,h:16}:{})});
 if(physical)Object.assign(q,{_wt25Owner:b,_wt25Physical:true,_wt25Born:b._wt25.clock,_s9a:'tidaltorp',_noArsenal:true,_shootable:true,_weaponProof:false,hp:3,homing:true,turn:.012,spd:sp});else wt25Ordinary(q,b);
 wt25Log(b,'water-shot',{kind:physical?'torpedo':kind,slot,x:p.x,y:p.y,a,physical});return q;
}
enemyOrdnanceElement=function(q){return q?._wt25Owner&&!q._wt25Physical?null:WT25.base.element.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){return q?._wt25Owner&&!q._wt25Physical?false:WT25.base.intercept.apply(this,arguments);};
s3kOrdnanceRules=function(q){const r=WT25.base.rules.apply(this,arguments);if(q?._wt25Owner&&!q._wt25Physical){q._weaponProof=true;q._shootable=false;q._s3kOriginalProof=false;delete q.hp;}return r;};
function wt25Start(b,kind){const T=b._wt25,n=late27Level(),phase=b.hp<b.maxhp*.5?1:0,left=camLeftX(),right=camRightX(),W=right-left;
 const P=T.attack={id:++WT25.serial,kind,t:0,n,phase,lanes:[],plans:[],fired:0,waves:0,done:false,tail:0};T.rest=0;
 const px=clamp(player.x,left+85,right-85),py=clamp(player.y,viewTopY()+260,VH-72);
 if(kind==='flood'){
  P.waves=n===2?3:2;P.gap=150+(n===0?30:0);P.spacing=1.55;P.warm=n===2?1.25:1.50;
  P.centers=Array.from({length:P.waves},(_,i)=>clamp(px+Math.sin(i*1.05+T.seq)*62,left+P.gap*.5+20,right-P.gap*.5-20));
  P.next=P.warm;P.tellAt=0;P.end=P.warm+(P.waves-1)*P.spacing;
 }else if(kind==='geysers'){
  const count=4+n,tell=n===2?1.35:1.60;
  for(let i=0;i<count;i++){const col=(i*3+T.seq)%7,x=left+55+col*(W-110)/6,y=clamp(py-25-(i%3)*62,viewTopY()+300,VH-48);
   P.plans.push({at:i*.58,tell,live:.78,x,y,slot:i%2?'circleR':'circleL',fired:false});}
  P.end=P.plans.at(-1).at+tell+.85;
 }else if(kind==='mortars'){
  const count=4+n,tell=n===2?1.12:1.35;
  for(let i=0;i<count;i++){const side=i%2?-1:1,x=clamp(px+side*(55+Math.floor(i/2)*38),left+55,right-55),y=clamp(py-((i%3)===2?95:0),viewTopY()+300,VH-45);
   P.plans.push({at:Math.floor(i/2)*1.0,tell,flight:1.0,x,y,slot:i%2?'circleR':'circleL',fired:false,active:.82});}
  P.end=P.plans.at(-1).at+tell+1.85;
 }else if(kind==='mist'){
  const warm=n===2?1.25:1.50,aim=clamp((px-worldWidth()/2)/W,-.30,.30);
  for(let i=0;i<4+phase;i++){const slot=i%2?'R':'L',p=shipBossMount(b,slot),a=Math.PI/2+aim+(i%2?-.13:.13)+(Math.floor(i/2)-.5)*.10;
   P.plans.push({at:i*.85,tell:warm,live:.48,slot,a,width:21,line:wt25Line(b,slot,a,21),fired:false});}
  P.end=P.plans.at(-1).at+warm+.58;
 }else if(kind==='undertow'){
  P.warm=n===2?1.25:1.50;P.spacing=.72;P.waves=3+n;P.next=P.warm;
  for(const slot of ['circleL','circleR'])for(const off of [-.34,0,.34])P.lanes.push(wt25Line(b,slot,Math.PI/2+off,24));
  for(const slot of ['L','R']){const p=shipBossMount(b,slot);P.lanes.push(wt25Line(b,slot,wt25Angle(p,{x:px,y:py}),18));}
  P.end=P.warm+(P.waves-1)*P.spacing+1.5;
 }else{
  P.warm=n===2?1.25:1.50;P.spacing=.82;P.waves=4+n;P.next=P.warm;P.gapX=px;wt25RingPlan(b,P);
  P.end=P.warm+(P.waves-1)*P.spacing+1.7;
 }
 T.history.push(kind);if(T.history.length>30)T.history.shift();wt25Cue(b,'bossWeaponCharge',.25);wt25Log(b,'water-attack-start',{kind,seq:T.seq,n,phase,plans:P.plans.length,waves:P.waves});return P;
}
function wt25RingPlan(b,P){P.lanes=[];const slot=P.fired%2?'circleR':'circleL',p=shipBossMount(b,slot),count=16+P.n*2,base=P.fired*.18,aim=wt25Angle(p,{x:P.gapX,y:VH-38}),half=Math.max(.22,Math.atan2(50,Math.max(120,VH-p.y)));
 for(let i=0;i<count;i++){const a=base+i*TAU/count,d=Math.abs(Math.atan2(Math.sin(a-aim),Math.cos(a-aim)));if(d>half)P.lanes.push(wt25Line(b,slot,a,16));}
 P.tellAt=P.t;P.tell=P.fired===0?P.warm:P.spacing;P.next=P.t+P.tell;
}
function wt25HitBox(b,x,y,w,h,label){for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.abs(player.x-x)<w*.5+3&&Math.abs(player.y-y)<h*.5+3)playerHit(label);});}
function wt25Geyser(b,Q,mortar=false){const T=b._wt25;T.geysers.push({x:Q.x,y:Q.y,t:0,life:Q.active||Q.live||.78,height:mortar?180:196,width:mortar?34:36});
 wt25Cue(b,mortar?'bossfireTidalfusion':'cfComboWater',.22);wt25Flash(b,Q.slot,46);wt25Log(b,'geyser-erupt',{x:Q.x,y:Q.y,mortar});}
function wt25Mortar(b,Q){const T=b._wt25,p=shipBossMount(b,Q.slot),a=wt25Angle(p,Q),q=wt25Ordinary(s9aShot(p.x,p.y,a,0,'tidalorb',{owner:b,noMuzzle:true,silent:true,w:18,h:18}),b);
 const m={q,start:{...p},x:Q.x,y:Q.y,t:0,flight:Q.flight,active:Q.active,slot:Q.slot};q._wt25Mortar=m;T.mortars.push(m);wt25Cue(b,'bossfireTidalfusion',.30);wt25Flash(b,Q.slot,52);
 wt25Log(b,'circle-mortar-launch',{slot:Q.slot,x:p.x,y:p.y,target:{x:Q.x,y:Q.y},flight:Q.flight});}
function wt25DangerTick(b,dt){const T=b._wt25;
 for(const F of T.flashes)F.t+=dt;T.flashes=T.flashes.filter(F=>F.t<.30);
 for(const m of T.mortars){m.t+=dt;if(m.q.dead){m.cancelled=true;continue;}const u=clamp(m.t/m.flight,0,1);
  m.q.x=lerp(m.start.x,m.x,u);m.q.y=lerp(m.start.y,m.y,u)-Math.sin(u*Math.PI)*105;m.q.vx=m.q.vy=0;
  if(u>=1){m.q.dead=true;m.impact=true;wt25Geyser(b,m,true);}}
 T.mortars=T.mortars.filter(m=>!m.impact&&!m.cancelled);
 for(const G of T.geysers){G.t+=dt;const k=wt25GeyserScale(G);if(G.t>.10&&G.t<G.life-.10)wt25HitBox(b,G.x,G.y-G.height*k*.50,G.width*k*.68,G.height*k*.87,'Tidal water geyser');}
 T.geysers=T.geysers.filter(G=>G.t<G.life);
 for(const F of T.walls){F.t+=dt;F.y+=F.speed*dt;
  for(const seat of seatList())withSeat(seat,()=>{if(player.dead||Math.abs(player.x-F.gapX)<F.gap*.5-4)return;if(player.y>=F.y-57&&player.y<=F.y+16)playerHit('Tidal flood wall');});}
 T.walls=T.walls.filter(F=>F.y-64<VH+35&&F.t<7);
 for(const q of eBullets)if(q._wt25Owner===b&&T.clock-q._wt25Born>6.8)q.dead=true;
}
function wt25GeyserScale(G){return Math.min(1,G.t/.13,(G.life-G.t)/.16);}
function wt25Tick(b,dt){const T=wt25Init(b);T.clock+=dt;b.fireCd=999;b._sba=null;b._s9Beam=null;b._s9Cascade=null;
 wt25DangerTick(b,dt);
 // Slow, visible watercraft drift. The committed warning and each native socket
 // share this same current pose, with no banking or generic charge underneath.
 const left=camLeftX(),right=camRightX(),margin=Math.min(b.w*.5+16,(right-left)*.5-4),cx=(left+right)*.5;
 const tx=clamp(cx+Math.sin(T.clock*.32)*Math.min(56,Math.max(0,(right-left)*.5-margin)),left+margin,right-margin),ty=T.home.y+Math.sin(T.clock*.53)*10;
 b.x=clamp(b.x+clamp(tx-b.x,-32*dt,32*dt),left+margin,right-margin);b.y+=clamp(ty-b.y,-22*dt,22*dt);b._drawY=b.y;
 let P=T.attack;
 if(!P){T.rest-=dt;if(T.rest<=0){P=wt25Start(b,WT25.book[T.seq++%WT25.book.length]);}else return true;}
 P.t+=dt;
 for(const Q of P.plans){const t=P.t-Q.at;if(t<0)continue;
  if(t<Q.tell)combatWarningTick(P,'tidal-'+P.id+'-'+P.plans.indexOf(Q),t,Q.tell);
  if(!Q.fired&&t>=Q.tell){Q.fired=true;P.fired++;if(P.kind==='geysers')wt25Geyser(b,Q);else if(P.kind==='mortars')wt25Mortar(b,Q);else if(P.kind==='mist'){wt25Cue(b,'combatBeam0927',.28);wt25Flash(b,Q.slot,38);wt25Log(b,'turret-mist-fire',{slot:Q.slot,...shipBossMount(b,Q.slot),a:Q.a});}}
  if(P.kind==='mist'&&t>=Q.tell&&t<Q.tell+Q.live)chaosHarrierBeamRay(b,shipBossMount(b,Q.slot),Q.a,Q.width*.42);
 }
 if(P.kind==='flood'&&P.fired<P.waves){
  const tell=P.fired===0?P.warm:P.spacing;combatWarningTick(P,'tidal-flood-'+P.id+'-'+P.fired,P.t-P.tellAt,tell);
  if(P.t>=P.next){const gapX=P.centers[P.fired],p=shipBossMount(b,'C');T.walls.push({t:0,y:p.y+14,gapX,gap:P.gap,speed:110+P.n*8+P.phase*12});
   wt25Flash(b,'circleL',60);wt25Flash(b,'circleR',60);wt25Cue(b,'bossfireTidalfusion',.4);wt25Log(b,'flood-release',{wave:P.fired,gapX,gap:P.gap,y:p.y+14});
   P.fired++;P.tellAt=P.t;P.next=P.t+P.spacing;}
 }else if(P.kind==='undertow'&&P.fired<P.waves){
  if(P.t<P.warm)combatWarningTick(P,'tidal-undertow-'+P.id,P.t,P.warm);
  if(P.t>=P.next){for(const L of P.lanes){const physical=['L','R'].includes(L.slot);if(physical&&P.fired%2)continue;wt25Shot(b,L.slot,L.a,physical?1.8:2.45+P.n*.12,'tidalcut',physical);}
   wt25Flash(b,'circleL');wt25Flash(b,'circleR');wt25Flash(b,'L',32);wt25Flash(b,'R',32);wt25Cue(b,'bossfireTidalfusion',.30);P.fired++;P.next=P.t+P.spacing;}
 }else if(P.kind==='maelstrom'&&P.fired<P.waves){
  combatWarningTick(P,'tidal-maelstrom-'+P.id+'-'+P.fired,P.t-P.tellAt,P.tell);
  if(P.t>=P.next&&eBullets.filter(q=>q._wt25Owner===b&&!q.dead).length+P.lanes.length<=110){for(const L of P.lanes)wt25Shot(b,L.slot,L.a,2.05+P.n*.12,'tidalmine');
   wt25Flash(b,P.lanes[0]?.slot||'circleL',56);wt25Cue(b,'combatOrb0927',.30);wt25Log(b,'maelstrom-wave',{wave:P.fired,count:P.lanes.length,gapX:P.gapX});P.fired++;
   if(P.fired<P.waves){P.gapX=clamp(P.gapX+Math.sin(P.fired*.7)*28,camLeftX()+70,camRightX()-70);wt25RingPlan(b,P);}}
 }
 if(P.t>P.end&&!T.walls.length&&!T.geysers.length&&!T.mortars.length){const live=eBullets.some(q=>q._wt25Owner===b&&!q.dead);P.tail+=dt;
  if(!live||P.tail>6.9){wt25Log(b,'water-attack-complete',{kind:P.kind,duration:P.t});T.attack=null;T.rest=1.0;}}
 return true;
}
late27Tick=function(b,dt){return wt25Own(b)&&!b.dead&&!b.enter&&!b._scene?wt25Tick(b,Math.min(.05,Math.max(0,dt))):WT25.base.lateTick.apply(this,arguments);};
function wt25Cancel(b,reason){const T=b._wt25;if(!T)return;T.attack=null;T.walls=[];T.geysers=[];T.mortars=[];T.flashes=[];
 for(const q of eBullets)if(q._wt25Owner===b)q.dead=true;WT25.owners.delete(b);wt25Log(b,'water-cancel',{reason});}
updatePlay=function(dt){for(const b of WT25.owners)if(b!==boss||b.dead||!wt25Own(b))wt25Cancel(b,'native-owner-change');const r=WT25.base.update.apply(this,arguments);
 for(const b of WT25.owners)if(b!==boss||b.dead||!wt25Own(b))wt25Cancel(b,'native-owner-change');return r;};
function wt25Blit(key,x,y,w,h,angle=0,alpha=1){if(!XART.rdy(key))return false;ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(key),-w*.5,-h*.5,w,h);ctx.restore();return true;}
function wt25Fx(name,t,x,y,size,angle=0,alpha=1){const D=BF22_ART.effects['water_'+name];if(!D||!XART.rdy(D.key))return;const f=Math.floor(Math.max(0,t)*D.fps)%D.frames;
 ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(D.key),...D.cells[f],-size/2,-size/2,size,size);ctx.restore();}
function wt25Beam(b,Q,t){const p=shipBossMount(b,Q.slot),f=Math.floor(t*16)%8,w=Q.width,len=Math.max(0,(VH+30-p.y)/Math.max(.3,Math.sin(Q.a))),head='tidalpressurebeam_'+f,tile='tidalpressurebeamtile_'+f;
 ctx.save();ctx.translate(p.x,p.y);ctx.rotate(Q.a-Math.PI/2);ctx.imageSmoothingEnabled=false;ctx.globalCompositeOperation='lighter';
 if(XART.rdy(head)){const im=XART.get(head);ctx.drawImage(im,-w/2,-w*.25,w,w*128/56);}
 if(XART.rdy(tile)){const im=XART.get(tile),h=w*2;for(let y=w*1.3;y<len;y+=h){const dh=Math.min(h,len-y);ctx.drawImage(im,0,0,32,64*dh/h,-w/2,y,w,dh);}}
 // The authored water splash supplies drifting mist along the pressure ray.
 for(let i=1;i<=4;i++){const y=(i/5*len+t*42)%len,side=i%2?1:-1;wt25Blit('tidalgeyserimpact_'+((f+i)%8),side*w*.4,y,42,33.6,side*.4,.34);}
 ctx.restore();
}
function wt25FloodDraw(b,F){const left=camLeftX(),right=camRightX(),a=S1W20_ART,f=Math.floor(b._wt25.clock*a.fps)%a.frames;
 for(const [x,r]of [[left,F.gapX-F.gap/2],[F.gapX+F.gap/2,right]]){if(r<=x)continue;
  ctx.save();ctx.beginPath();ctx.rect(x,F.y-60,r-x,82);ctx.clip();ctx.imageSmoothingEnabled=false;
  if(XART.rdy(a.key)){ctx.save();ctx.beginPath();ctx.rect(x,F.y-60,r-x,64);ctx.clip();ctx.globalAlpha=.68;for(let xx=x-20;xx<r;xx+=112)ctx.drawImage(XART.get(a.key),...a.cells[f],xx,F.y-60,112,112);ctx.restore();}
  for(let xx=x;xx<r;xx+=80)wt25Fx('wave',b._wt25.clock,xx+40,F.y-3,90);
  ctx.restore();
 }
}
function wt25Tell(b,P,Q,t,front){const p=shipBossMount(b,Q.slot),k=clamp(t/Q.tell,0,1);
 if(front)return;
 if(P.kind==='mist'){const L=wt25Line(b,Q.slot,Q.a,Q.width);combatWarningDraw(P,{...L,progress:k,fieldOnly:true,alpha:.38});}
 else if(P.kind==='mortars'){combatWarningDraw(P,{x:p.x,y:p.y,ex:Q.x,ey:Q.y,width:20,progress:k,fieldOnly:true,alpha:.30,laneShape:'line'});groundTargetReticleDraw(Q.x,Q.y,70,k,.85);}
 else if(P.kind==='geysers'){combatWarningDraw(P,{x:Q.x,y:Q.y,ex:Q.x,ey:Q.y-190,width:35,progress:k,fieldOnly:true,alpha:.35,laneShape:'line'});groundTargetReticleDraw(Q.x,Q.y,64,k,.85);}
 wt25Fx('muzzle',t,p.x,p.y,28+22*k,0,.38+.52*k);
}
function wt25Draw(b,front){const T=b?._wt25;if(!T||b.dead||!wt25Own(b))return;
 const P=T.attack;
 if(!front){
  for(const F of T.walls)wt25FloodDraw(b,F);
  for(const G of T.geysers){const k=Math.max(0,wt25GeyserScale(G)),f=Math.floor(G.t*16)%8,h=G.height*k,w=h*43/250;
   efxFrame('efx_geyser_water',f,G.x-w/2,G.y-h,w,h,1);wt25Blit('tidalgeyserimpact_'+f,G.x,G.y-12,86,68.8,0,Math.min(1,k*1.5));}
  for(const m of T.mortars){const k=clamp(m.t/m.flight,0,1);groundTargetReticleDraw(m.x,m.y,70,.55+k*.45,.85);
   combatWarningDraw(m,{x:m.x,y:m.y,ex:m.x,ey:m.y-180,width:34,progress:k,fieldOnly:true,alpha:.28,laneShape:'line'});}
 }
 if(P){for(const Q of P.plans){const t=P.t-Q.at;if(t>=0&&t<Q.tell)wt25Tell(b,P,Q,t,front);else if(!front&&P.kind==='mist'&&t>=Q.tell&&t<Q.tell+Q.live)wt25Beam(b,Q,t-Q.tell);}
  if(!front&&P.kind==='flood'&&P.fired<P.waves){const gapX=P.centers[P.fired],k=clamp((P.t-P.tellAt)/(P.fired===0?P.warm:P.spacing),0,1),y=shipBossMount(b,'C').y+14;
   for(const [x,r]of [[camLeftX(),gapX-P.gap/2],[gapX+P.gap/2,camRightX()]])if(r>x)combatWarningDraw(P,{x:(x+r)/2,y,ex:(x+r)/2,ey:VH+24,width:r-x,progress:k,fieldOnly:true,alpha:.28,laneShape:'line'});}
  if(!front&&((P.kind==='undertow'&&P.t<P.warm)||(P.kind==='maelstrom'&&P.fired<P.waves))){const k=P.kind==='undertow'?P.t/P.warm:(P.t-P.tellAt)/P.tell;
   for(const q of P.lanes){const L=wt25Line(b,q.slot,q.a,q.width);combatWarningDraw(P,{...L,progress:clamp(k,0,1),fieldOnly:true,alpha:P.fired?.10:.27});}}
 }
 if(front)for(const F of T.flashes){const p=shipBossMount(b,F.slot);wt25Fx('muzzle',F.t,p.x,p.y,F.size,0,1-F.t/.30);}
}
late27Draw=function(front){const r=WT25.base.lateDraw.apply(this,arguments);wt25Draw(boss,front);return r;};
shipBossDraw=function(b){const r=WT25.base.draw.apply(this,arguments);if(!wt25Own(b)||b.dead||!(b.flash>0))return r;
 const T=b._wt25,key=b.hp/b.maxhp<=.30?'ns9_tidal_critical':b.hp/b.maxhp<=.62?'ns9_tidal_damaged':'ns9_tidal_intact',im=wt25Frame(key,T?.clock||0);if(!im)return r;
 const pulse=r25Pulse(b,b.flash,T?.clock||0);if(pulse<=0)return r;
 const id=key+':'+Math.floor((T?.clock||0)*12)%32+':white';let white=WT25.frames.get(id);
 if(!white){white=document.createElement('canvas');white.width=320;white.height=256;const g=white.getContext('2d');g.drawImage(im,0,0);g.globalCompositeOperation='source-in';g.fillStyle='#fff';g.fillRect(0,0,320,256);WT25.frames.set(id,white);}
 const P=shipBossVisualPose(b);ctx.save();ctx.translate(b.x+P.x,(b._drawY??b.y)+P.y);ctx.rotate(P.rot);ctx.scale(P.sx,P.sy);ctx.globalAlpha*=pulse;ctx.drawImage(white,-b.w/2,-b.h/2,b.w,b.h);ctx.restore();return r;
};
window.BOF_WARDEN_TIDAL=WT25;
