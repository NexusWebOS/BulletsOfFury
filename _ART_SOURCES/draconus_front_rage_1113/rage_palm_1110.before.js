'use strict';
/* Authored GPT whole-body rage and palm gestures. Native Stage5 clocks, HP,
   sounds and collision remain authoritative. No play-time silhouette building. */
const RF1110={base:{image:b20Image,pose:ha21Blue,palm:c32Pose,hand:c30Hand,draw:hammerBossDraw,tick:hammerBossTick,active:cgActive,hit:bossHitTest,load:stageLoadBegin,warm:v18Warm,keys:v18Keys,start:hb20Start,donor:v19NativeTick,donorDraw:v19DonorDraw,donorPose:hb20Pose,rig:v19HammerRig,laser:hammerLaserDraw,clear:v18Clear,state:setState},events:[],draws:0};
function rf1110Log(type,data={}){RF1110.events.push({type,time:efxClock,...data});if(RF1110.events.length>1500)RF1110.events.shift();}
for(const [name,a]of Object.entries(RF1110_ART.banks))for(const mat of (name.includes('_charge_')?['power','hit','plain']:['power','hit']))XART._src['rf1110_'+name+'_'+mat]='assets/game/shared/combat/rage_palm_1110/'+name+'_'+mat+'.webp';
for(const color of ['red','purple'])for(const kind of ['lightning','gather'])XART._src['rf1110_'+color+'_'+kind]='assets/game/shared/combat/rage_palm_1110/fx_'+color+'_'+kind+'.webp';
function rf1110Keys(stage){const prefix=stage===5?'chronos_':'drac_';return[...Object.keys(RF1110_ART.banks).filter(n=>n.startsWith(prefix)).flatMap(n=>(n.includes('_charge_')?['power','hit','plain']:['power','hit']).map(m=>'rf1110_'+n+'_'+m)),...['lightning','gather'].map(n=>'rf1110_'+(stage===5?'red':'purple')+'_'+n)];}
function rf1110Warm(stage){return rf1110Keys(stage).map(k=>XART.rdy(k)).every(Boolean);}
stageLoadBegin=function(n,keys){return RF1110.base.load.call(this,n,[...(keys||[]),...([5,8].includes(n)?rf1110Keys(n):[])]);};
v18Keys=function(){return[...RF1110.base.keys.apply(this,arguments),...(run.stage===8?rf1110Keys(8):[])];};
v18Warm=function(){return RF1110.base.warm.apply(this,arguments)&&(run.stage!==8||rf1110Warm(8));};
function rf1110Row(unit,bank,frame,depth=1){const name=unit+'_'+bank+'_'+(depth<.7?'back':'fore'),a=RF1110_ART.banks[name];frame=clamp(frame|0,0,a.count-1);const m=a.meta[frame];return{...m,key:'rf1110_'+name+'_power',white:'rf1110_'+name+'_hit',w:a.cw,h:a.ch,pivot:a.pivot,bank:name,frame,_rf1110:true};}
function rf1110Blit(a,x,y,hit=false){const spec=RF1110_ART.banks[a.bank],key=hit?a.white:a.key;if(!spec||!XART.rdy(key))return false;const f=a.frame;ctx.drawImage(XART.get(key),f%4*a.w,Math.floor(f/4)*a.h,a.w,a.h,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.w,a.h);RF1110.draws++;return true;}
b20Image=function(a,x,y,k,rot,flash){return a?._rf1110?rf1110Blit(a,x,y,flash>0):RF1110.base.image.apply(this,arguments);};
function rf1110Fx(color,kind,f,x,y){const key='rf1110_'+color+'_'+kind;if(!XART.rdy(key))return;const bolt=kind==='lightning',w=bolt?40:80,h=bolt?768:80,n=bolt?8:16;f=clamp(f|0,0,n-1);ctx.drawImage(XART.get(key),f%4*w,Math.floor(f/4)*h,w,h,Math.round(x-w/2),Math.round(y-(bolt?h:h/2)),w,h);}
function rf1110Palms(b,a){return a.palms.map(p=>({x:b.x+p[0]-a.pivot[0],y:b.y+p[1]-a.pivot[1]}));}
function rf1110Side(beat){return beat===2||beat===5?2:beat%2;}
function rf1110Gesture(R){const V=R.volley;if(!V)return 0;const iv=diffKey==='furious'?.13:.16;
 if(R.phase==='volley_warn'){const dur=V.group?.58:.85;return R.t>dur-.06?Math.min(2,Math.floor((R.t-dur+.06)/.02)):0;}
 if(R.phase!=='volley_fire')return 0;
 const age=R.t-(V.shotAt??R.t),next=V.beat*iv-R.t;
 if(V.beat<6&&next<=.05&&next>0)return rf1110Side(V.beat)*8+Math.min(2,Math.floor((.05-next)/(.05/3)));
 return (V.dual?2:V.lastSide||0)*8+Math.min(7,3+Math.floor(Math.max(0,age)/.018));
}
c32Pose=function(b){if(!c32Own(b))return RF1110.base.palm.apply(this,arguments);const R=b._hammer.c30;return{a:rf1110Row('chronos','palms',rf1110Gesture(R),R.scale),k:1,rot:0,kind:'rf1110_palm'};};
function rf1110CastPose(unit,R){let f=0;const phase=R.phase.replace('kame_','');if(['charge','gather'].includes(phase))f=16+Math.min(2,Math.floor(R.t/.25));else if(phase==='thrust')f=16+Math.min(3,Math.floor(R.t/.09));else if(['fire','beam'].includes(phase))f=19+([0,0,1,0][Math.floor(R.t*12)%4]);else if(['recover','return'].includes(phase))f=20+Math.min(3,Math.floor(R.t/.14));return{a:rf1110Row(unit,'palms',f,R.scale),k:1,rot:0,kind:'rf1110_cast'};}
ha21Blue=function(b){if(c30Own(b)&&b._hammer.c30)return c32Own(b)?c32Pose(b):rf1110CastPose('chronos',b._hammer.c30);return RF1110.base.pose.apply(this,arguments);};
c30Hand=function(b,release=false){if(!c30Own(b)||!b._hammer.c30)return RF1110.base.hand.apply(this,arguments);const R=b._hammer.c30,a=release?rf1110Row('chronos','palms',19,R.scale):ha21Blue(b).a,p=rf1110Palms(b,a);return{x:(p[0].x+p[1].x)/2,y:(p[0].y+p[1].y)/2};};

// The pre-rage throw uses the same rigid hammer plates as his real attack.
function rf1110Plain(unit,f){const a=rf1110Row(unit,'charge',f);a.key=a.key.replace('_power','_plain');return{a,k:1,rot:0,kind:'rf1110_empty'};}
const rf1110Reel=c45ReelDraw,rf1110ReelHead=c45ReelHead,rf1110StopDraw=c45StopDraw;
c45ReelDraw=function(b,u){if(!c25Own(b))return rf1110Reel.apply(this,arguments);if(u>=C45_THROW.release){const q=rf1110Plain('chronos',15-Math.min(3,Math.floor((u-C45_THROW.release)/.035*3)));ha21Body(b,q);return true;}const h=b._hammer,m=h.frArmor?.activated?'chrome':'regular';const q=ba119Pose('blue-overhead',Math.min(8,Math.floor(u/C45_THROW.release*9)),m,1);if(q){ha21Body(b,q);return true;}return false;};
function rf1110HammerCentre(b,a){return ba119At(b,{...a,tip:a.headCenter||a.tip});}
c45ReelHead=function(b,f,k){if(c25Own(b))return rf1110HammerCentre(b,ba119Row('blue-overhead',8,'regular'));return rf1110ReelHead.apply(this,arguments);};
c45StopDraw=function(b,u){if(!c25Own(b))return rf1110StopDraw.apply(this,arguments);ha21Body(b,rf1110Plain('chronos',Math.max(0,12-Math.floor((u-.17)/.13*13))));return true;};

function rf1110ChargeFrame(u){return u<.38?Math.floor(clamp((u-.30)/.08,0,1)*3):u<.8?3+Math.floor(clamp((u-.38)/.42,0,1)*9):12+Math.min(3,Math.floor((u-.8)/.05));}
function rf1110ChargeTick(b,C,u,dt,color){C.rf1110??={n:0,bolts:[],done:false};const P=C.rf1110;for(const q of P.bolts)q.age+=dt;P.bolts=P.bolts.filter(q=>q.age<.18);const n=c45StrikeCount(u);
 while(P.n<n){const i=++P.n,side=i%2?-1:1,x=clamp(b.x+side*Math.max(0,145-i*5),camLeftX()+20,camRightX()-20),y=b.y+105;P.bolts.push({x,y,age:0});shake=Math.max(shake,Math.min(8,2+i*.2));if(color==='red')c45Log('strike',{n:i});else Snd.play(CF48.key,.63);if(i%4===0)explode(x,y,23,'red');rf1110Log('charge-strike',{color,index:i});}
 if(u>=.8&&!P.done){P.done=true;P.bolts.push({x:b.x,y:b.y+30,age:0});flashScreen=Math.max(flashScreen||0,.18);shake=Math.max(shake,12);if(color==='red'){C.c45Final=true;b._hammer._c45AfterDone=true;chronosRageRings(b);c45Log('final');}if(color==='purple')hb20State(b).rf1110Rings={x:b.x,y:b.y,start:efxClock};rf1110Log('charge-release',{color});}
}
function rf1110Bolts(C,color){for(const q of C.rf1110?.bolts||[])rf1110Fx(color,'lightning',Math.floor(q.age/.18*8),q.x,q.y);}
function rf1110ChargeDraw(b,C,u,unit){rf1110Bolts(C,'red');const a=rf1110Row(unit,'charge',rf1110ChargeFrame(u));rf1110Blit(a,b.x,b.y,(b.flash||0)>0);RF1110.last={unit,phase:'rage-charge',frame:a.frame,charge:u};}
const rf1110OldTrace=c27TraceAura;c27TraceAura=function(b,q){if(q?.a?._rf1110||c25Own(b)&&b._hammer?._hf22Charge)return;return rf1110OldTrace.apply(this,arguments);};
function rf1110Stage5(b){return c25Own(b)&&!b.dead&&(b._hammer._hf22Charge&&cgChargeU(b)>=.30||c30Own(b)&&b._hammer.c30);}
cgActive=function(b){return rf1110Stage5(b)?false:RF1110.base.active.apply(this,arguments);};
hammerBossTick=function(b,dt){const charge=c25Own(b)&&b._hammer?._hf22Charge,r=RF1110.base.tick.apply(this,arguments);if(charge&&b._hammer._hf22Charge===charge&&cgChargeU(b)>=.30)rf1110ChargeTick(b,charge,cgChargeU(b),dt,'red');return r;};
function rf1110BeamLightning(b,R,color){const phase=R.phase.replace('kame_','');if(!['charge','thrust','fire','gather','beam'].includes(phase))return;const off={charge:0,gather:0,thrust:2.6,fire:2.96,beam:2.96}[phase],elapsed=off+R.t,beat=Math.floor(elapsed/.38),age=elapsed% .38;if(age>.18)return;const x=lerp(camLeftX(),camRightX(),[.18,.76,.39,.89,.58,.09,.68,.30][beat%8]);rf1110Fx('red','lightning',Math.floor(age/.18*8),x,VH-15);if(color==='red')chronosLightningStrike(b,R,'rf1110-wave-'+(R.cycle||0),beat);}
function rf1110DrawStage5(b){const h=b._hammer,C=h._hf22Charge;if(C){rf1110ChargeDraw(b,C,cgChargeU(b),'chronos');c45Line(b,C45_LINE_RAGE,(cgChargeU(b)-.38)*CG_SSJ,'#ff5030');return;}
 const R=h.c30,V=R.volley;rf1110BeamLightning(b,R,'red');ha21Body(b,ha21Blue(b));
 if(c32Own(b)){if(R.phase==='volley_warn')for(let i=0;i<2;i++){const L=c32Lane(b,i);C25.base.warning(b,{x:L.from.x,y:L.from.y,ex:L.to.x,ey:L.to.y,width:L.width,progress:clamp(R.t/(V.group?.58:.85),0,1),fieldOnly:true});}
  const hands=c32Hands(b);for(let i=0;i<2;i++)if(V.flash[i]>0)rf1110Fx('red','gather',12+Math.min(3,Math.floor((.1-V.flash[i])*40)),hands[i].x,hands[i].y);
 }else{const opener=R.phase.startsWith('kame_'),gather=R.phase==='gather'||R.phase==='kame_charge',thrust=R.phase==='thrust'||R.phase==='kame_thrust',fire=R.phase==='beam'||R.phase==='kame_fire';
  if(gather||thrust){const L=opener?c46Line(b):c30Line(b),dur=opener?C46_T.charge:1.7;C25.base.warning(b,{x:L.from.x,y:L.from.y,ex:L.to.x,ey:L.to.y,width:76,progress:clamp(R.t/dur,0,1),fieldOnly:true});const p=c30Hand(b);rf1110Fx('red','gather',thrust?15:Math.floor(clamp(R.t/dur,0,1)*15),p.x,p.y);}
  if(fire){const L=opener?c46Line(b):c30Line(b);c41Draw(L.from,L.to,R.t,opener?C46_T.fire:1.35,true);const p=c30Hand(b);rf1110Fx('red','gather',12+Math.floor(R.t*20)%4,p.x,p.y);}
 }
 RF1110.last={unit:'chronos',phase:R.phase,frame:ha21Blue(b).a.frame,palms:c32Own(b)?c32Hands(b):null};
}
hammerBossDraw=function(b){if(!rf1110Stage5(b))return RF1110.base.draw.apply(this,arguments);return rf1110DrawStage5(b);};
bossHitTest=function(x,y){const b=boss;if(!c30Own(b)||!b._hammer.c30)return RF1110.base.hit.apply(this,arguments);if(b._noHit||hammerDepthScale(b)<.95)return false;const a=ha21Blue(b).a,px=Math.floor(x-b.x+a.pivot[0]),py=Math.floor(y-b.y+a.pivot[1]),row=a.spans[py];b._hammerModuleHit=null;return !!row&&row.some((v,i)=>i%2===0&&px>=v&&px<row[i+1]);};
/* Dracodia keeps RD74's body/HP owner. Shared choreography, not a fake Stage5 boss. */
function rf1110Drac(b){return rd74Own(b)&&!b.dead&&!!hb20State(b).rf1110;}
function rf1110Phase(b,R,p){R.phase=p;R.t=0;rf1110Log('phase',{unit:'drac',phase:p,scale:R.scale});}
function rf1110DracMove(b,R,p,to){R.from={x:b.x,y:b.y,scale:R.scale};R.to=to;rf1110Phase(b,R,p);}
function rf1110DracStart(b){const Q=hb20State(b);Q.pendingRecall=Q.pendingGun=Q.pendingArsenal=false;Q.hammerHP=Q.gunHP=0;Q.hammerDestroyed=true;Q.parts[1].hp=Q.parts[2].hp=0;Q.parts[1].destroyed=Q.parts[2].destroyed=true;Q.shield=0;Q.action={type:'rf1110_rage',t:0,tell:0,duration:999,hit:new Set(),hits:new Map(),serial:++RD74.serial};
 const R=Q.rf1110={phase:'kame_up',t:0,scale:1,cycle:0,hit:new Set(),sfx:new Set()};rf1110DracMove(b,R,'kame_up',{x:c46Centre(),y:c46Sky(),scale:.42});rd74Log('rage-hammer-discarded-permanently');return Q.action;}
hb20Start=function(b,type){if(rd74Own(b)){const Q=hb20State(b);if(Q.rage&&(Q.pendingRecall==='rage'||Q.rf1110||type==='recall'))return rf1110DracStart(b);}return RF1110.base.start.apply(this,arguments);};
function rf1110DracRetreat(b,R){const kind=R.cycle%3;R.lock=null;R.hit=new Set();R.sfx=new Set();R.volley=kind===2?null:{depth:kind===0?'foreground':'background',group:0,beat:0,flash:[0,0],angles:[Math.PI/2,Math.PI/2]};rf1110DracMove(b,R,kind===2?'retreat':'volley_move',{x:kind===0?c46Centre():lerp(camLeftX(),camRightX(),R.cycle%2?.73:.27),y:viewTopY()+(kind===0?190:135),scale:kind===0?1:.42});}
function rf1110DracWarn(b,R){const p=targetShip(b.x,b.y);R.volley.target={x:p.x,y:Math.max(p.y,b.y+200)};R.volley.beat=0;rf1110Phase(b,R,'volley_warn');Snd.play('rd74WaveCharge',.7);}
function rf1110DracShot(b,R){const V=R.volley,beat=V.beat,side=rf1110Side(beat);V.dual=side===2;V.lastSide=side%2;V.shotAt=R.t;const a=rf1110Row('drac','palms',side*8+3,R.scale),hands=rf1110Palms(b,a),slots=side===2?[0,1]:[side];for(const i of slots){const p=hands[i],offset=[-36,0,36,36,0,-36][beat],ang=Math.atan2(V.target.y-p.y,V.target.x+offset-p.x),before=eBullets.length;hammerLaser(p.x,p.y,ang,diffKey==='furious'?7.4:6.7,i>0);for(const q of eBullets.slice(before)){q._rf1110Purple=true;q._c32Palm=true;q._c32Depth=V.depth;q._c32Start={x:p.x,y:p.y};q._c32Owner=b;q._weaponProof=true;q.w=10;q.h=54;}
 V.flash[i]=.10;V.angles[i]=ang;rf1110Log('palm-shot',{unit:'drac',phase:R.phase,beat,hand:i,x:p.x,y:p.y,pose:a.frame,depth:V.depth});}V.beat++;}
function rf1110DracHands(b,R,release=false){const a=release?rf1110Row('drac','palms',19,R.scale):rf1110CastPose('drac',R).a,p=rf1110Palms(b,a);return{x:(p[0].x+p[1].x)/2,y:(p[0].y+p[1].y)/2};}
function rf1110DracLine(b,R){const from=rf1110DracHands(b,R,true);return{from,to:R.lock||{x:from.x,y:VH+90}};}
function rf1110DracLock(b,R){const p=targetShip(b.x,b.y),m=rf1110DracHands(b,R,true);R.lock={x:m.x,y:VH+90};R.lockTarget={x:p.x,y:p.y};}
function rf1110DracTick(b,dt){const Q=hb20State(b),R=Q.rf1110;R.t+=dt;Q.scale=R.scale;Q.shield=0;Q.parts[1].destroyed=Q.parts[2].destroyed=true;Q.parts[1].hp=Q.parts[2].hp=0;b._noHit=R.scale<.95||['kame_up','kame_return','volley_move','retreat'].includes(R.phase);const V=R.volley;if(V)V.flash=V.flash.map(t=>Math.max(0,t-dt));
 const once=(id,key)=>{if(!R.sfx.has(id)){R.sfx.add(id);Snd.play(key,1);}};
 if(R.phase==='kame_up'){if(c35DepthFlight(b,R,.42)){R.scale=.42;R.x0=b.x;R.y0=b.y;rf1110Phase(b,R,'kame_strafe');}}
 else if(R.phase==='kame_strafe'){b.x=R.x0+Math.sin(R.t*C46_W)*(camRightX()-camLeftX())*.34;b.y=R.y0+Math.sin(R.t*2.7)*10-Math.abs(Math.sin(R.t*C46_W))*8;if(R.t>=C46_T.strafe){b.x=R.x0;rf1110Phase(b,R,'kame_charge');}}
 else if(R.phase==='kame_charge'||R.phase==='gather'){const opener=R.phase==='kame_charge',dur=opener?C46_T.charge:1.7;once('charge','rd74WaveCharge');const target=targetShip(b.x,b.y);if(!R.lock)b.x+=clamp(target.x-b.x,-80*dt,80*dt);b.y=(R.y0||viewTopY()+135)+Math.sin(R.t*2.7)*4;if(!R.lock&&R.t>=(opener?C46_T.lock:.65))rf1110DracLock(b,R);if(R.t>=dur)rf1110Phase(b,R,opener?'kame_thrust':'thrust');}
 else if(R.phase==='kame_thrust'||R.phase==='thrust'){if(R.t>=.36){const opener=R.phase==='kame_thrust';rf1110Phase(b,R,opener?'kame_fire':'beam');once('fire','rd74WaveFire');Snd.stopCue('rd74WaveCharge');shake=Math.max(shake,9);}}
 else if(R.phase==='kame_fire'||R.phase==='beam'){const opener=R.phase==='kame_fire',dur=opener?C46_T.fire:1.35,L=rf1110DracLine(b,R);if(R.t>.05&&R.t<dur-.2)b20HitSegment(b,L.from,L.to,36,'Corrupted Chronos purple wave',R.hit);if(R.t>=dur)rf1110Phase(b,R,opener?'kame_recover':'recover');}
 else if(R.phase==='kame_recover'){if(R.t>=C46_T.recover)rf1110DracMove(b,R,'kame_return',{x:c46Centre(),y:viewTopY()+190,scale:1});}
 else if(R.phase==='kame_return'){if(c35DepthFlight(b,R,1)){R.scale=1;R.cycle=0;rf1110DracRetreat(b,R);}}
 else if(R.phase==='volley_move'){if(c35DepthFlight(b,R,R.to.scale)){R.scale=R.to.scale;rf1110DracWarn(b,R);}}
 else if(R.phase==='volley_warn'){if(R.t>=(V.group?.58:.85)){rf1110Phase(b,R,'volley_fire');rf1110DracShot(b,R);}}
 else if(R.phase==='volley_fire'){const iv=diffKey==='furious'?.13:.16;if(V.beat<6&&R.t>=V.beat*iv)rf1110DracShot(b,R);if(R.t>=iv*6+.18){V.group++;if(V.group<3)rf1110DracWarn(b,R);else rf1110Phase(b,R,'volley_recover');}}
 else if(R.phase==='volley_recover'||R.phase==='recover'){if(R.t>=(R.phase==='recover'?.7:.55)){R.cycle++;if(b._r30.v18.donorAge>52){Q.rf1110=null;Q.action=null;Q.cool=.8;}else rf1110DracRetreat(b,R);}}
 else if(R.phase==='retreat'){if(c35DepthFlight(b,R,.42)){R.scale=.42;R.y0=b.y;rf1110Phase(b,R,'gather');}}
 // Match the shared visible bolt schedule through the native audio mixer.
 const wp=R.phase.replace('kame_','');if(['charge','gather','thrust','fire','beam'].includes(wp)){const off={charge:0,gather:0,thrust:2.6,fire:2.96,beam:2.96}[wp],elapsed=off+R.t,beat=Math.floor(elapsed/.38),id=(R.cycle||0)+':'+(R.phase.startsWith('kame_')?'opener':'wave')+':'+beat;R.lightningSeen??=new Set();if(elapsed% .38<.18&&!R.lightningSeen.has(id)){R.lightningSeen.add(id);Snd.play(CF48.key,.63);}}
 Q.scale=R.scale;b._drawY=b.y;
}
v19NativeTick=function(b,dt){const active=rf1110Drac(b),C=rd74Own(b)&&hb20State(b).action?.type==='rage'?hb20State(b).action:null;const r=RF1110.base.donor.apply(this,arguments);if(C&&hb20State(b).action===C&&C.t>=.95&&!C.rf1110Launch){C.rf1110Launch=true;C.launch=rf1110HammerCentre(b,ba119Row('corrupt-overhead',8,hb20State(b).chrome?'chrome':'regular'));}if(C&&hb20State(b).action===C&&C.t>=2.16)rf1110ChargeTick(b,C,C.t/7.2,dt,'purple');if(active&&rf1110Drac(b))rf1110DracTick(b,clamp(dt,0,.05));if(rf1110Drac(b)){const Q=hb20State(b);Q.parts[1].destroyed=Q.parts[2].destroyed=true;Q.parts[1].hp=Q.parts[2].hp=0;if(Q.rf1110.scale<.95)b._noHit=true;}return r;};
hb20Pose=function(b){if(rf1110Drac(b)){const R=hb20State(b).rf1110;return R.volley&&R.phase.startsWith('volley_')?{a:rf1110Row('drac','palms',rf1110Gesture(R),R.scale),k:1,rot:0,kind:'rf1110_drac'}:rf1110CastPose('drac',R);}if(rd74Own(b)){const A=hb20State(b).action;if(A?.type==='rage'&&A.t<.95)return ba119Pose('corrupt-overhead',Math.min(8,Math.floor(A.t/.95*9)),hb20State(b).chrome?'chrome':'regular',1);if(A?.type==='rage'&&A.t>=.95&&A.t<2.16)return rf1110Plain('drac',15-Math.min(15,Math.floor((A.t-.95)/1.21*16)));if(A?.type==='rage'&&A.t>=2.16)return{a:rf1110Row('drac','charge',rf1110ChargeFrame(A.t/7.2)),k:1,rot:0,kind:'rf1110_drac_charge'};}return RF1110.base.donorPose.apply(this,arguments);};
v19HammerRig=function(b){if(rf1110Drac(b)){const Q=hb20State(b),q=hb20Pose(b),core=b20Piece(Q.parts[0],q.a,b,0,1,'core',1);core._rd74=true;return[core];}return RF1110.base.rig.apply(this,arguments);};
v19DonorDraw=function(b){const Q=rd74Own(b)&&hb20State(b);if(!Q)return RF1110.base.donorDraw.apply(this,arguments);const C=Q.action;
 if(!rf1110Drac(b)){if(C?.type==='rage'){if(C.t>=2.16)rf1110ChargeDraw(b,C,C.t/7.2,'drac');else{const q=hb20Pose(b);if(q.a._rf1110)rf1110Blit(q.a,b.x,b.y);else b20Image(q.a,b.x,b.y,1,0,0);rd74DrawTool(b,C);}}else return RF1110.base.donorDraw.apply(this,arguments);}
 else{const R=Q.rf1110,q=hb20Pose(b);rf1110BeamLightning(b,R,'purple');rf1110Blit(q.a,b.x,b.y,Math.max(b.flash||0,Q.parts[0].flash||0)>0);
  if(R.phase==='volley_warn'){const hands=rf1110Palms(b,q.a),dur=R.volley.group?.58:.85;for(const p of hands)b20Field(b,p,R.volley.target,110,clamp(R.t/dur,0,1));}
  if(R.phase==='volley_fire'){const hands=rf1110Palms(b,q.a);for(let i=0;i<2;i++)if(R.volley.flash[i]>0)rf1110Fx('purple','gather',12+Math.min(3,Math.floor((.10-R.volley.flash[i])*40)),hands[i].x,hands[i].y);}
  if(['kame_charge','gather','kame_thrust','thrust','kame_fire','beam'].includes(R.phase)){const p=rf1110DracHands(b,R),fire=['kame_fire','beam'].includes(R.phase),dur=R.phase==='gather'?1.7:C46_T.charge;rf1110Fx('purple','gather',fire?12+Math.floor(R.t*20)%4:Math.floor(clamp(R.t/dur,0,1)*15),p.x,p.y);const L=rf1110DracLine(b,R);if(!fire)b20Field(b,L.from,L.to,76,clamp(R.t/dur,0,1));else rd74Fx('wave_purple',c41Frame(R.t,R.phase==='beam'?1.35:C46_T.fire),L.from.x,L.from.y);}
  RF1110.last={unit:'drac',phase:R.phase,frame:q.a.frame};
 }
 // The announcement remains live, and never pauses combat.
 rf1110DracRings(b,Q);if(Q.speech){const S=Q.speech,w=cd27Width(VW-20),x=(VW-w)/2,y=48;ctx.save();worldXformEscape();CD27.inDlg++;msgFaceUse('dialogue');try{const r=ui20Panel('DRACODIA',x,y,w,CD27.height,true);if(r)ui20PanelContents('DRACODIA',S.text,S.shown||0,'rd74_portrait',r);}finally{msgFaceUse(null);CD27.inDlg--;ctx.restore();}}
};
function rf1110DracRings(b,Q){const ring=Q.rf1110Rings;if(!ring)return;for(const name of ['small','large']){const bank=CF50_ART.banks[name],age=efxClock-ring.start;if(age<0||age>=bank.life)continue;const frame=bank.frames[Math.min(bank.frames.length-1,Math.floor(age/bank.life*bank.frames.length))];if(XART.rdy(frame.key))ctx.drawImage(XART.get(frame.key),Math.round(ring.x-frame.pivot[0]),Math.round(ring.y-frame.pivot[1]));}}
// Purple projectiles use the same native shot/collision, with a prepared palette.
hammerLaserDraw=function(q){if(!q._rf1110Purple)return RF1110.base.laser.apply(this,arguments);const key='rf1110_purple_projectiles';if(!XART.rdy(key))return;const a=((Math.round((Math.atan2(q.vy,q.vx)-Math.PI/2)/TAU*32)%32)+32)%32,depth=clamp(Math.round((q.w/10-.6)/.4*7),0,7),f=depth*32+a;ctx.drawImage(XART.get(key),f%16*64,Math.floor(f/16)*64,64,64,Math.round(q.x-32),Math.round(q.y-32),64,64);};
XART._src.rf1110_purple_projectiles='assets/game/shared/combat/rage_palm_1110/fx_purple_projectiles.webp';
const rf1110OriginalKeys=rf1110Keys;rf1110Keys=function(stage){return[...rf1110OriginalKeys(stage),...(stage===8?['rf1110_purple_projectiles','rf1110_red_lightning',...['small','large'].flatMap(n=>CF50_ART.banks[n].frames.map(f=>f.key))]:[])];};
const rf1110BG=drawBG;drawBG=function(){const r=rf1110BG.apply(this,arguments),b=boss;if(rf1110Drac(b)){const R=hb20State(b).rf1110;if(['kame_charge','gather','kame_thrust','thrust','kame_fire','beam'].includes(R.phase))cf50DimDraw(Math.round(clamp(R.t/.7,0,1)*11));}return r;};
v18Clear=function(b){if(rd74Own(b)){hb20State(b).rf1110=null;Snd.stopCue('rd74WaveCharge');}return RF1110.base.clear.apply(this,arguments);};
setState=function(s){if(s!==GS.PLAY&&s!==GS.PAUSED&&rd74Own(boss)){Snd.stopCue('rd74WaveCharge');Snd.stopCue('rd74WaveFire');}return RF1110.base.state.apply(this,arguments);};
// The shared simulation schedule owns all 26 visible charge strikes exactly once.
const rf1110LegacyBolts=rd74BoltTick;rd74BoltTick=function(b,A,dt){if(A?.type==='rage'&&A.t>=2.16)return;return rf1110LegacyBolts.apply(this,arguments);};
// Decode and prepare the small pre-rage throw cells behind the native loading
// gate. The first charge must not pay the old lazy atlas/cell decoding cost.
const rf1110NativeReady=stageLoadReady,rf1110Decoded=new WeakMap(),rf1110Uploaded=new Set();
function rf1110Prepared(stage){
 if(stage!==5&&stage!==8)return true;const bank=stage===5?'blue-overhead':'corrupt-overhead',cells=[];
 for(let f=0;f<=8;f++)for(const mat of ['regular','chrome','hit'])cells.push('ba119_'+bank+'_'+mat+'_'+f);
 let ready=true,uploadBudget=1;for(const k of cells)if(!XART.rdy(k))ready=false;
 for(const k of [...rf1110Keys(stage),...cells,...(stage===5?['rh1110_flight','rh1110_flight_hit']:[])]){
  if(!XART.rdy(k)){ready=false;continue;}const im=XART.get(k);if(im&&typeof im.decode==='function'){
   if(!rf1110Decoded.has(im)){rf1110Decoded.set(im,false);im.decode().then(()=>rf1110Decoded.set(im,true)).catch(()=>rf1110Decoded.set(im,true));}
   if(!rf1110Decoded.get(im)){ready=false;continue;}
  }
  if(im&&!rf1110Uploaded.has(k)){
   ready=false;if(uploadBudget>0){
    // Force the first raster/texture preparation under the loading overlay,
    // one resource per tick. These pixels are never used as game artwork.
    ctx.save();try{ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.imageSmoothingEnabled=false;const saved=ctx.getImageData(0,0,16,16);ctx.drawImage(im,0,0,Math.min(im.width,384),Math.min(im.height,448),0,0,16,16);ctx.getImageData(0,0,1,1);ctx.putImageData(saved,0,0);}finally{ctx.restore();}
    rf1110Uploaded.add(k);uploadBudget--;
   }
  }
 }
 return ready;
}
stageLoadReady=function(stage=run.stage){return rf1110NativeReady.apply(this,arguments)&&rf1110Prepared(stage);};
globalThis.BOF_RAGE_PALM_1110=RF1110;
