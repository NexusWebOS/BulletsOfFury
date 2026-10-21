'use strict';
/* Tutorial-only ownership: authored Cole portraits, B.O.B.'s live modules and dossier.
   Ordinary combat, controls, elements, targeting, audio and all campaign stages retain their owners. */
const BOB20_SPEC=Object.freeze({missile:Object.freeze({element:null}),cannon:Object.freeze({element:null}),core:Object.freeze({element:'ice',missileMultiplier:2})});
const IC21_TUNING={
 easy:{hp:[90,110,240],tell:1.6,gap:1,shots:4,speed:3.1,strike:5,strikeWarn:2.5,move:.09,escorts:0,jetTell:1.1,jetGap:2.5,jetShots:2,jetSpeed:3},
 normal:{hp:[120,145,300],tell:1.2,gap:.75,shots:5,speed:3.6,strike:4.6,strikeWarn:2,move:.14,escorts:0,jetTell:.95,jetGap:2.1,jetShots:3,jetSpeed:3.4},
 hard:{hp:[165,195,410],tell:.95,gap:.6,shots:7,speed:4,strike:3.5,strikeWarn:1.7,move:.18,escorts:1,jetTell:.75,jetGap:1.55,jetShots:4,jetSpeed:3.9},
 furious:{hp:[210,250,540],tell:.7,gap:.45,shots:9,speed:4.4,strike:2.6,strikeWarn:1.4,move:.22,escorts:2,jetTell:.6,jetGap:1.1,jetShots:5,jetSpeed:4.4}
};
function ic21Tuning(){return IC21_TUNING[diffKey]||IC21_TUNING.normal;}
const IC20={base:{keys:sg20Keys,warm:sg20Warm,ready:sg20LayersReady,ask:tutAskDraw,
 overlay:tutOverlayDraw,update:updatePlay,next:tutNext,cleanup:tutCleanup,hold:tutHold,start:tutStart,
 draw:drawEnemy,hit:hitEnemy,kill:killEnemy,wave:sg20ExamWave,strikeTick:s6StrikeMissileTick,jet:jetTick},draws:0,partDraws:0,hits:[]};
const IC20_KEYS=[...IC20_ART.portraits,IC20_ART.whole,IC20_ART.card,...Object.values(IC20_ART.parts),...Object.values(IC20_ART.views)].map(a=>a.key).concat(['idle','happy','talk-closed','talk-small','talk-medium','talk-wide','talk-o'].map(e=>'comm_cole_'+e));
for(const a of [...IC20_ART.portraits,IC20_ART.whole,IC20_ART.card,...Object.values(IC20_ART.parts),...Object.values(IC20_ART.views)])XART._src[a.key]=a.path;
const IC20_MISSILES=[...Array.from({length:6},(_,i)=>'s1fx_jungle_missile_'+i),...Array.from({length:6},(_,i)=>S1_MUZZLE_MILITARY+'_'+i),...Array.from({length:8},(_,i)=>'laser_round_muzzle_'+i)];
sg20Keys=function(){return [...IC20.base.keys(),...IC20_KEYS,...IC20_MISSILES];};
sg20Warm=function(){IC20.base.warm();for(const k of [...IC20_KEYS,...IC20_MISSILES])XART.rdy(k);
 if(!IC20.audio){IC20.audio=true;Snd.prepare(['expSmall','expBig','shieldHitHeavy','powerup','enemyMachineGunLight','missileLaunch']);}};
sg20LayersReady=function(){return IC20.base.ready()&&IC20_KEYS.every(k=>XART.rdy(k))&&IC20_MISSILES.every(k=>XART.rdy(k));};
tutStart=function(){IC20.hits=[];IC20.labStats={};return IC20.base.start.apply(this,arguments);};
function ic20Port(smile=false){if(smile)return 'comm_cole_happy';
 const T=TUT,t=T?T._sg?.time||T.t:0,typing=T&&(T.typed||0)<(T.say||T.text||'').length;
 return typing?['comm_cole_talk-closed','comm_cole_talk-small','comm_cole_talk-medium','comm_cole_talk-wide'][Math.floor(t*8)%4]:'comm_cole_idle';}
tutAskDraw=function(dt){const prior=dlgBox;
 dlgBox=function(o){return prior({...o,who:'COLE',portraitKey:'comm_cole_idle',tint:UI20.color('COLE')});};
 try{return IC20.base.ask(dt);}finally{dlgBox=prior;}};
function ic20Panel(full,shown,y=PLAY.y+5,h=100,smile=false){
 const r=ui20Panel('COLE',12,y,VW-24,h,true);if(!r)return;
 r.text={x:r.text.x+5,y:r.text.y+2,w:r.text.w-10,h:r.text.h-4};
 msgFaceUse('dialogue');const q=ui20PanelContents('COLE',full,shown,ic20Port(smile),r,12,14);msgFaceUse(null);
 UI20.dialogue={who:'COLE',x:12,y,w:VW-24,h,full:full.length,shown,...q};IC20.draws++;
}
function ic20Text(s,x,y,h,w,color='#e6f3f3',align='center'){ui20Text(ctx,String(s),x,y,h,w,align,color);}
function ic20BoxText(s,r,maxH,color='#e6f3f3'){
 ctx.save();ctx.beginPath();ctx.rect(r.x,r.y,r.w,r.h);ctx.clip();
 ic20Text(s,r.x+r.w/2,r.y+r.h/2,Math.min(maxH,r.h),r.w,color);ctx.restore();
 if(IC20.layoutCapture)IC20.layoutCapture.push({text:String(s),rect:{...r}});
}
function ic20Meter(x,y,w,h,ratio,color){ctx.fillStyle='#03080e';ctx.fillRect(x,y,w,h);ctx.fillStyle='#526776';ctx.fillRect(x+1,y+1,w-2,h-2);
 ctx.fillStyle='#0a131b';ctx.fillRect(x+2,y+2,w-4,h-4);ctx.fillStyle=color;ctx.fillRect(x+2,y+2,Math.max(0,w-4)*clamp(ratio,0,1),h-4);}
function bob20Spawn(L,mode='exam'){
 const F=tutField(),G={x:F.cx,cx:F.cx,y:tutTop()+55,y0:tutTop()+55,k:.88,t:0,mode,parts:{},cycle:null,next:.4,missileNext:1.1,turn:0,tuning:ic21Tuning()};
 for(const id of mode==='exam'?['missile','cannon','core']:mode==='warn'?['cannon']:mode==='strike'?['missile']:['core']){
  const a=IC20_ART.parts[id],off={x:(a.target[0]-128)*G.k,y:(a.target[1]-128)*G.k};
  const hp=mode==='exam'?G.tuning.hp[['missile','cannon','core'].indexOf(id)]:mode==='element'?150:9999;
  const e=tutSpawn('s1jetBomber',G.x+off.x,G.y+off.y,hp,{amp:0});if(!e)continue;
  e.w=id==='core'?66:id==='missile'?48:42;e.h=id==='core'?56:id==='missile'?94:108;
  e._bob20={id,G,off};e._esh=null;e._iceEnemy=id==='core';e.dropOk=false;
  G.parts[id]=e;
 }
 L.bob=G;L.units=Object.values(G.parts);return G;
}
function bob20Alive(e){return !!e&&!e.dead&&e.hp>0&&e._dyingT==null;}
// B.O.B. borrows the native enemy damage/target container, never the Stage1 jet AI or its elite HP multipliers.
jetTick=function(e,dt){if(e?._tut)return;return IC20.base.jet.apply(this,arguments);};
function bob20Pods(G){return ['missile','cannon'].some(id=>bob20Alive(G.parts[id]));}
tutHold=function(dt){IC20.base.hold(dt);if(!tutLive())return;
 for(const e of enemies)if(e._bob20&&!e.dead){const {G,off}=e._bob20;
  G.y=G.y0+Math.sin(G.t*1.4)*3;e.x=G.x+off.x;e.y=G.y+off.y;e._tutHold.x=e.x;e._tutHold.y=e.y;e.vx=e.vy=0;e._drawY=e.y;}
};
drawEnemy=function(e){if(!e?._bob20)return IC20.base.draw.apply(this,arguments);if(e.dead||e.hp<=0)return;
 const {id,G,off}=e._bob20,key=IC20_ART.parts[id].key;
 if(!XART.rdy(key))return;const active=e.flash>0;
 const im=active?xartTint(key,hitFlashColor(e),.72):e._fireEnemy?xartTint(key,'#ff6b29',.42):XART.get(key);
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,Math.round(e.x-off.x-128*G.k),Math.round(e.y-off.y-128*G.k),256*G.k,256*G.k);ctx.restore();IC20.partDraws++;
};
hitEnemy=function(e,dmg){if(!e?._bob20)return IC20.base.hit.apply(this,arguments);
 if(e.dead)return;markHit(e,.16);const {id,G}=e._bob20;
 if(G.mode==='warn'||G.mode==='strike'||id==='core'&&G.mode==='exam'&&bob20Pods(G)){
  if((G.shieldCue||0)<=G.t){Snd.play('shieldHitHeavy',.6);G.shieldCue=G.t+.25;}
  G.absorbed=(G.absorbed||0)+1;return true;
 }
 const missile=_dmgSrc==='missile'||_dmgBullet?.kind==='missile',before=e.hp;
 const scale=id==='core'&&G.mode==='exam'&&missile?BOB20_SPEC.core.missileMultiplier:1;
 if(G.mode==='element'&&TUT?.L?.phase===0)dmg=Math.min(dmg,10);
 const r=IC20.base.hit.call(this,e,dmg*scale);markHit(e,.16);
 const L=TUT?.L,loss=Math.max(0,before-e.hp);
 if(loss>0){const ev={lesson:L?.def.id,part:id,loss,element:damageProjectileElement(_dmgBullet),missile,weakspot:scale,time:TUT?.t};
  IC20.hits.push(ev);if(IC20.hits.length>120)IC20.hits.shift();G.last=ev;
  if(G.mode==='element'&&L){L.hitCount=(L.hitCount||0)+1;if(ev.element)L.last=ev;
   const stats=IC20.labStats||(IC20.labStats={});const k=L.def.id+':'+L.phase,old=stats[k],elements={...old?.elements};
   if(ev.element)elements[ev.element]=(elements[ev.element]||0)+1;
   stats[k]={...ev,hits:(old?.hits||0)+1,elements};}
 }
 return r;
};
killEnemy=function(e){if(!e?._bob20)return IC20.base.kill.apply(this,arguments);if(e.dead)return;
 e.hp=0;e.dead=true;e.shoots=false;groundTargetingCancel(e);
 explode(e.x,e.y,e._bob20.id==='core'?56:32,'red','fireball');Snd.play(e._bob20.id==='core'?'expBig':'expSmall');
 const G=e._bob20.G;if(G.mode==='exam')TUT.say=e._bob20.id==='core'?'B.O.B.: I AM FILING FOR RETIREMENT. NICE SHOOTING, PILOT!':bob20Pods(G)?'ONE POD DOWN. DISABLE THE OTHER, THEN HIT THE BLUE REACTOR.':'REACTOR EXPOSED! FIRE BEATS ICE. A RETINA MISSILE HITS THIS CORE FOR DOUBLE DAMAGE.';
};
function bob20Port(e){const a=IC20_ART.parts[e._bob20.id],k=e._bob20.G.k;
 return {x:e.x+(a.muzzle[0]-a.target[0])*k,y:e.y+(a.muzzle[1]-a.target[1])*k};}
function bob20Muzzle(e){if(!bob20Alive(e))return;navalFlash(null,bob20Port(e),.7,S1_MUZZLE_MILITARY,{n:6,hpx:30,life:.16});}
function bob20Ground(e,warn=2.5){
 const q=groundTargetingSpawn({kind:'missile',owner:e,x:player.x,y:player.y,track:true,trackFor:.5,lane:false,warn,active:.48,radius:30,size:78,sound:'expBig',shake:3,
  onImpact:g=>explode(g.x,g.y,48,'red','fireball')});
 q._strikeMissile={...bob20Port(e),launched:false};q._late27=true;return q;
}
s6StrikeMissileTick=function(q){if(!q.owner?._bob20)return IC20.base.strikeTick(q);
 const M=q._strikeMissile,e=q.owner;if(!M||M.launched)return;
 if(!bob20Alive(e)){q.dead=true;return;}
 if(q.t>=q.warn*.52){M.launched=true;Object.assign(M,bob20Port(e));Audio.SFX.missile();
  navalFlash(null,{x:M.x,y:M.y},.7,S1_MUZZLE_MILITARY,{n:6,hpx:30,life:.16});}
};
function bob20Bar(G){if(!G||G.mode!=='exam')return;const parts=Object.values(G.parts),hp=parts.reduce((n,e)=>n+Math.max(0,e.hp),0),max=parts.reduce((n,e)=>n+e.maxhp,0);
 const y=VH-35;ic20Text('B.O.B. - BALLISTICS ORIENTATION BOT',VW/2,y-12,10,VW-50,'#ffd58b');
 ic20Meter(24,y,VW-48,13,hp/max,'#f0a549');
 ic20Text(bob20Pods(G)?'ARMORED REACTOR - PODS FIRST':'CRYO CORE - FIRE X1.5 / MISSILES X2',VW/2,y+22,9,VW-40,'#a9ecff');}
// The same authored pods teach the two warning systems before the graduation fight.
const IC20_WARN=TUT_LESSONS.find(d=>d.id==='warn'),IC20_STRIKE=TUT_LESSONS.find(d=>d.id==='strike');
IC20_WARN.start=function(L){const G=bob20Spawn(L,'warn');L.gun=G.parts.cannon;L.clean=0;L.cycles=0;L.c=null;};
IC20_WARN.tick=function(L,dt){L.bob.t+=dt;
 if(!L.c)L.c={t:-.8,x:player.x,hit0:TUT.hits,fired:0};const C=L.c,DUR=2.4;C.t+=dt;
 if(C.t<0)return false;if(C.t<DUR/3)C.x+=clamp(player.x-C.x,-160*dt,160*dt);
 if(C.t<DUR){combatWarningTick(L.gun,'bob20-practice',C.t,DUR);return false;}
 if(C.fired<6&&C.t>=DUR+C.fired*.14){const m=bob20Port(L.gun),a=Math.atan2(PLAY.y+PLAY.h-m.y,C.x-m.x);
  for(const o of [-.035,0,.035])tutShoot(m.x,m.y,a+o,3.5);bob20Muzzle(L.gun);C.fired++;}
 if(C.t>DUR+2){L.cycles++;if(TUT.hits===C.hit0)L.clean++;else TUT.say='LEAVE THE YELLOW LANE BEFORE RED. TRY AGAIN - YOUR LIVES ARE SAFE.';L.c=null;}
 return L.clean>=2||L.cycles>=5;
};
IC20_WARN.draw=function(L){const C=L.c,e=L.gun;if(C&&C.t>=0&&C.t<2.4)
 combatWarningDraw(e,{...bob20Port(e),ex:C.x,ey:PLAY.y+PLAY.h+20,progress:C.t/2.4,width:40});};
IC20_STRIKE.start=function(L){bob20Spawn(L,'strike');L.n=0;L.next=.6;L.clean=0;L.cur=null;};
IC20_STRIKE.tick=function(L,dt){L.bob.t+=dt;
 if(L.cur){if(L.cur.dead||!groundTargetingFx.includes(L.cur)){if(TUT.hits===L.h0)L.clean++;else TUT.say='LEAVE THE CIRCLE AT YELLOW. RED IS THE BLAST. YOU CAN ROLL OR SOMERSAULT TO ESCAPE.';L.cur=null;L.next=.65;}return L.clean>=3||L.n>=6;}
 L.next-=dt;if(L.next<=0){L.n++;L.h0=TUT.hits;L.cur=bob20Ground(L.bob.parts.missile);}return false;
};
// Borrow a level-I common gun only for the element lab; never write the forge or armory save.
const IC20_LOAN_FIELDS=['weapon','wlevel','wlevels','wvars','infusion','forge','forgeForms','_wbag','_kinN'];
function ic20Loan(){if(TUT._icLoan)return;TUT._icLoan={};for(const k of IC20_LOAN_FIELDS)TUT._icLoan[k]=run[k]===undefined?undefined:JSON.parse(JSON.stringify(run[k]));
 if(typeof endSpecial==='function')endSpecial();run.weapon=0;run.wlevel=1;
 run.wlevels=Array.isArray(run.wlevels)?run.wlevels.slice():{...run.wlevels};run.wlevels[0]=1;
 run.wvars={...run.wvars};delete run.wvars[0];run.forge={...run.forge};delete run.forge[0];run.infusion=null;}
function ic20Return(){const loan=TUT?._icLoan;if(!loan)return;for(const k of IC20_LOAN_FIELDS){if(loan[k]===undefined)delete run[k];else run[k]=loan[k];}delete TUT._icLoan;}
function ic20LabStart(L,enemyElement){ic20Loan();const G=bob20Spawn(L,'element'),e=G.parts.core;
 e._iceEnemy=enemyElement==='ice';e._fireEnemy=enemyElement==='fire';L.element=enemyElement;L.phase=0;L.hitCount=0;L.ready=0;
 run.infusion={elem:enemyElement,lv:1,hits:0};L.baseline=0;}
function ic20LabTick(L,dt){L.bob.t+=dt;L.ready+=dt;const e=L.bob.parts.core;
 // Three actual native hits demonstrate resistance, then the player destroys the same target with its counter element.
 if(L.phase===0){e.hp=Math.max(e.hp,90);if(L.hitCount>=3&&L.ready>2){
  pBullets.length=0;L.phase=1;L.ready=0;L.hitCount=0;e.hp=e.maxhp=90;
  run.infusion={elem:L.element==='ice'?'fire':'ice',lv:1,hits:0};Audio.SFX.powerup();
  TUT.say=(L.element==='ice'?'FIRE':'ICE')+' INFUSION ONLINE. NOW YOUR SHOTS DEAL 1.5X DAMAGE. DESTROY THE '+L.element.toUpperCase()+' REACTOR.';
 }return false;}return !bob20Alive(e);
}
function ic20LabObj(L){const mode=L.phase?'COUNTER ELEMENT X1.5':'MATCHING ELEMENT X0.5';return mode+' - '+(L.last?'LAST HIT '+L.last.loss.toFixed(1)+' DMG':'HOLD FIRE AT THE REACTOR');}
const IC20_ELEMENT={id:'elements_ice',good:'THERMAL ADVANTAGE',
 text:()=> 'STAGE 3: ICE RESISTS ICE. TRY YOUR LOANED ICE GUN: HALF DAMAGE. AFTER THREE HITS, TRY FIRE FOR 1.5X DAMAGE.',
 start:L=>ic20LabStart(L,'ice'),tick:ic20LabTick,obj:ic20LabObj};
const IC20_FIRE={...IC20_ELEMENT,id:'elements_fire',good:'COUNTERS MASTERED',
 text:()=> 'STAGE 2: FIRE RESISTS FIRE. SHOOT THE HEATED REACTOR. THEN TRY ICE FOR 1.5X DAMAGE. THESE RULES APPLY TO BOSSES TOO.',start:L=>ic20LabStart(L,'fire')};
TUT_LESSONS.splice(TUT_LESSONS.findIndex(d=>d.id==='brief1'),1);
TUT_LESSONS.splice(TUT_LESSONS.findIndex(d=>d.id==='special'),0,IC20_ELEMENT,IC20_FIRE);
tutNext=function(){if(TUT?.L&&/^elements_/.test(TUT.L.def.id))ic20Return();return IC20.base.next.apply(this,arguments);};
tutCleanup=function(){ic20Return();return IC20.base.cleanup.apply(this,arguments);};
// A combat-free dossier. Frames are authored 3D turntable views, not a flat canvas rotation.
const IC20_PARTS=['whole','missile','cannon','core'];
function ic20CardTick(L,dt){L.age+=dt;L.yaw=(L.yaw+dt*10)%32;
 const up=Input.menuUp(),down=Input.menuDown(),left=Input.menuLeft(),right=Input.menuRight(),back=Input.menuBack(),go=Input.menuConfirm()||!!L._hsConfirm;L._hsConfirm=false;
 if(up||down){L.sel=(L.sel+(up?-1:1)+4)%4;L.seen[L.sel]=true;Audio.SFX.blip();}
 if(left||right)L.yaw=(L.yaw+(left?-2:2)+32)%32;
 if(back){L.sel=0;Audio.SFX.blip();}
 return L.age>3.8&&go;
}
function ic20CardDraw(L){
 const y=PLAY.y+107,bottom=Math.min(VH-30,PLAY.y+PLAY.h-6),k=Math.min((VW-20)/1200,Math.max(100,bottom-y)/832),w=1200*k,h=832*k,x=(VW-w)/2,key=IC20_PARTS[L.sel],a=IC20_ART.views[key],
  rect=(a,b,c,d)=>({x:x+a*k,y:y+b*k,w:c*k,h:d*k}),text=(s,r,sz,color)=>ic20BoxText(s,rect(...r),sz*k,color);
 IC20.cardLayout={x,y,w,h,k,regions:[],model:null};IC20.layoutCapture=IC20.cardLayout.regions;
 ctx.fillStyle='#030a13ed';ctx.fillRect(0,PLAY.y+105,VW,PLAY.h-105);
 if(XART.rdy(IC20_ART.card.key))ctx.drawImage(XART.get(IC20_ART.card.key),x,y,w,h);
 // Hide the Overdrive template's old insignia beneath the actual instructor's framed portrait.
 const p=rect(982,44,156,156);if(XART.rdy('comm_cole_idle'))ui20Portrait(ctx,'comm_cole_idle',p);
 text('B.O.B.',[278,80,644,43],39,'#ffd38b');
 text('BALLISTICS ORIENTATION BOT',[278,132,644,30],24,'#c0ebff');
 const names=['FULL UNIT','MISSILE POD','CANNON POD','CRYO REACTOR'];
 text(names[L.sel],[94,226,560,43],31,'#a5f5ff');
 if(a&&XART.rdy(a.key)){const f=Math.floor(L.yaw)%a.frames,c=a.cells[f],r=rect(92,278,564,315),sz=Math.min(r.w,r.h),mx=r.x+(r.w-sz)/2,my=r.y+(r.h-sz)/2;
  ctx.save();ctx.beginPath();ctx.rect(r.x,r.y,r.w,r.h);ctx.clip();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),...c,mx,my,sz,sz);ctx.restore();IC20.cardFrame={part:key,frame:f};IC20.cardLayout.model={x:mx,y:my,w:sz,h:sz};}
 const hp=ic21Tuning().hp,lines=key==='whole'?[hp.reduce((a,b)=>a+b,0)+' TOTAL HP',diffKey.toUpperCase()+' / ICE','WEAK: FIRE X1.5','RESISTS ICE X0.5','PODS FIRST, THEN CORE','MISSILE CORE BONUS X2']:
 key==='core'?[hp[2]+' HP / ICE','BLUE REACTOR TARGET','WEAK: FIRE X1.5','RESISTS ICE X0.5','RETINA MISSILE X2','SHUTTER: BOTH PODS']:
 key==='missile'?[hp[0]+' HP / STEEL','GROUND MISSILE POD','NEUTRAL DAMAGE X1','NO ELEMENT BONUS','RETINA TARGET: POD','STOPS GROUND STRIKES']:
 [hp[1]+' HP / STEEL','FOV MACHINE CANNON','NEUTRAL DAMAGE X1','GREEN AIM / YELLOW SET','RED: LEAVE THE LANE','STOPS GUN VOLLEYS'];
 for(let i=0;i<lines.length;i++)text(lines[i],[735,234+i*56,364,42],27,i===2?'#ffd38b':'#e6f3f3');
 text('WHY HAVEN\'T I RETIRED YET?',[135,661,930,83],36,'#ffd38b');IC20.layoutCapture=null;
 if(typeof controlHintRow==='function')controlHintRow([['pad_dpad','PART / TURN'],['pad_a',L.age>3.8?'DEPLOY':'SCANNING'],['pad_b','FULL UNIT']]);
}
const IC20_CARD={id:'bob_card',good:'DOSSIER STUDIED',text:()=> 'MEET B.O.B.! INSPECT HIS PARTS. BREAK BOTH PODS TO EXPOSE THE ICE REACTOR. AIM RETINA MISSILES AT THE BLUE CORE.',
 start(L){L.age=0;L.yaw=0;L.sel=0;L.seen={0:true};},tick:ic20CardTick};
TUT_LESSONS.splice(TUT_LESSONS.findIndex(d=>d.id==='exam'),0,IC20_CARD);
sg20ExamWave=function(L){if(L.wave!==2){
 IC20.base.wave(L);const D=ic21Tuning(),F=tutField(),n=L.units.length+D.escorts;
 while(L.units.length<n)L.units.push(tutSpawn('s1jetDelta',F.cx,tutTop()+35,45,{amp:0}));
 L.units=L.units.filter(Boolean);L.units.forEach((e,i)=>{
  e.hp=e.maxhp=(L.wave===1?40:55)*(1+D.escorts*.25);e._entry=0;
  const x=F.L+F.W*(.16+.68*(i/(L.units.length-1||1)));
  Object.assign(e._tutHold,{x,y:tutTop()+24+(i%2)*24,amp:0});
  e._ic21Escort={home:x,wait:.25+i*.24,cycle:null,releases:0};
 });return;
}
 tutClearField();L.wave=3;L.gap=0;L.age=0;L.c=null;bob20Spawn(L,'exam');};
SG20_EXAM.text=()=> 'GRADUATION: TWO ESCORT WAVES, THEN B.O.B. HIS PODS ARE REAL TARGETS. WATCH THE FOV AND GROUND WARNINGS. BREAK BOTH PODS, THEN HIT HIS EXPOSED BLUE CORE.';
SG20_EXAM.obj=L=>L.wave<3?'ESCORT WAVE '+L.wave+' / 2':bob20Pods(L.bob)?'DISABLE BOTH WEAPON PODS':'REACTOR OPEN - RETINA + MISSILE';
function ic21JetRelease(e,C,D){
 const y=e.y+e.h*.3,angle=Math.atan2(C.y-y,C.x-e.x);
 for(const side of [-1,1]){const x=e.x+side*e.w*.22,before=eBullets.length;
  tutShoot(x,y,angle,D.jetSpeed);
  if(eBullets.length>before){wm26Emit(e,x,y,angle,'mg',null,{size:20,life:.12});e._af21FireAt=efxClock;}
 }
 C.fired++;e._ic21Escort.releases++;
}
function ic21EscortTick(L,dt){
 const alive=tutAlive(L.units);if(!alive.length){L.gap+=dt;if(L.gap>1.3)sg20ExamWave(L);return false;}
 const D=ic21Tuning(),F=tutField();L.age+=dt;
 for(const [i,e]of alive.entries()){
  const A=e._ic21Escort;if(!A)continue;
  e._tutHold.x=clamp(A.home+Math.sin(L.age*(.75+D.escorts*.18)+i)*F.W*(.045+D.escorts*.018),F.L+32,F.R-32);
  if(!A.cycle){A.wait-=dt;if(A.wait<=0)A.cycle={t:0,x:player.x,y:player.y,fired:0,warn:D.jetTell};}
  const C=A.cycle;if(!C)continue;C.t+=dt;
  if(C.t<C.warn*.65){C.x=player.x;C.y=player.y;}
  if(C.t<C.warn){combatWarningTick(e,'ic21-escort',C.t,C.warn);continue;}
  if(C.fired<D.jetShots&&C.t>=C.warn+C.fired*.10)ic21JetRelease(e,C,D);
  if(C.t>C.warn+D.jetShots*.10){A.cycle=null;A.wait=D.jetGap;}
 }return false;
}
SG20_EXAM.tick=function(L,dt){if(L.wave<3)return ic21EscortTick(L,dt);
 const G=L.bob;if(!G)return false;G.t+=dt;if(!Object.values(G.parts).some(bob20Alive)){L.gap+=dt;return L.gap>1.3;}
 const D=G.tuning,F=tutField(),exposed=!bob20Pods(G);
 G.x=G.cx+Math.sin(G.t*(exposed?1.15:.8))*F.W*D.move;
 if(bob20Alive(G.parts.missile)){G.missileNext-=dt;if(G.missileNext<=0){G.q=bob20Ground(G.parts.missile,D.strikeWarn);G.missileNext=D.strike;}}
 if(!G.cycle){G.next-=dt;if(G.next<=0){
  const type=bob20Alive(G.parts.cannon)?'lane':exposed?'core':null;
  if(type)G.cycle={type,t:0,x:player.x,fired:0,warn:D.tell*(exposed?.78:1)};
 }}
 const C=G.cycle;if(!C)return false;C.t+=dt;
 const gun=C.type==='core'?G.parts.core:G.parts.cannon;if(!bob20Alive(gun)){G.cycle=null;G.next=.2;return false;}
 if(C.t<C.warn*.65)C.x+=clamp(player.x-C.x,-240*dt,240*dt);
 if(C.t<C.warn){combatWarningTick(gun,'bob20-lane',C.t,C.warn);return false;}
 if(C.fired<D.shots&&C.t>=C.warn+C.fired*.10){const m=bob20Port(gun),a=Math.atan2(PLAY.y+PLAY.h-m.y,C.x-m.x);
  for(const o of C.type==='core'?[-.16,-.08,0,.08,.16]:[-.065,0,.065])tutShoot(m.x,m.y,a+o,D.speed);
  bob20Muzzle(gun);C.fired++;}
 if(C.t>C.warn+D.shots*.10){G.cycle=null;G.next=D.gap;}return false;
};
SG20_EXAM.draw=function(L){if(L.wave<3){
 for(const e of tutAlive(L.units)){const C=e._ic21Escort?.cycle;if(C&&C.t<C.warn)combatWarningDraw(e,{x:e.x,y:e.y+e.h*.3,ex:C.x,ey:C.y,progress:C.t/C.warn,width:26});}return;
}const G=L.bob,C=G?.cycle;
 if(C&&C.t<C.warn){const e=C.type==='core'?G.parts.core:G.parts.cannon;if(bob20Alive(e))combatWarningDraw(e,{...bob20Port(e),ex:C.x,ey:PLAY.y+PLAY.h+20,progress:C.t/C.warn,width:C.type==='core'?72:48});}
};
updatePlay=function(dt){if(!tutLive()||TUT.L?.def.id!=='bob_card')return IC20.base.update.apply(this,arguments);
 if(pauseTapped()){setState('paused');return;}
 const T=TUT,S=sg20State();tutHoldStage();T.t+=dt;T.lt+=dt;T.typed=(T.typed||0)+dt*TUT_TYPE;
 if(S){S.time+=dt;S.travel+=dt*SG20.speed;}
 if(T.done){T.done+=dt;if(T.done>1.5)tutNext();}
 else if(ic20CardTick(T.L,dt)){T.done=.01;Audio.SFX.select();}
};
tutOverlayDraw=function(){const T=TUT;if(!T?.L)return;const D=T.L.def,full=T.say||T.text;
 if(T._fullKey!==full){T._fullKey=full;T.typed=0;}
 if(D.draw)tutWorldDraw(()=>D.draw(T.L));
 ic20Panel(full,Math.min(full.length,Math.floor(T.typed||0)),PLAY.y+5,100,T.done>0||D.id==='debrief');
 if(D.id==='bob_card'){ic20CardDraw(T.L);return;}
 const y=PLAY.y+107;ctx.fillStyle='#02111ef0';ctx.fillRect(12,y,VW-24,43);
 const label=T.done>0&&D.good?D.good:D.info?'PRESS FIRE TO CONTINUE':D.obj?D.obj(T.L):'';
 ic20BoxText(label,{x:20,y:y+3,w:VW-40,h:18},11,T.done?'#9dffac':'#ffe5a0');
 ic20BoxText('INSTRUCTOR COLE - '+(T.i+1)+' / '+TUT_LESSONS.length+' - PAUSE TO SKIP',{x:20,y:y+23,w:VW-40,h:17},9,'#a5c9d0');
 if(T.flash)helpLabel('TRAINING HIT - LIVES PROTECTED',VW/2,PLAY.y+PLAY.h*.78,11,'#ffb799');
 if(D.id==='exam')bob20Bar(T.L.bob);
};
BOFTUTORIAL.lessons=TUT_LESSONS.map(d=>d.id);
window.BOFINSTRUCTOR={name:'Instructor Cole',boss:'B.O.B. - Ballistics Orientation Bot',get artReady(){return sg20LayersReady();},get hits(){return IC20.hits;},get bossState(){return TUT?.L?.bob;},get card(){return IC20.cardFrame;}};
// Mike's red/black formal portrait belongs to the author credits. Flight training
// uses the actual green-uniform Cole comm bank above.
drawCredits=function(dt){
 scrollSpaceBG(dt);const logo='cf_logo';
 if(XART.rdy(logo)){const im=XART.get(logo),w=250,h=w*im.height/im.width;ctx.drawImage(im,VW/2-w/2,55-h/2,w,h);}
 ['cfic_shield','cfic_star','cfic_wings','cfic_radar'].forEach((key,i)=>{
  if(XART.rdy(key)){const im=XART.get(key),w=32,h=w*im.height/im.width;ctx.drawImage(im,VW/2-82+i*44,97-h/2,w,h);}
 });
 if(XART.rdy('cfui_panel')){const im=XART.get('cfui_panel'),w=VW-40,h=w*im.height/(im.width-110);ctx.drawImage(im,110,0,im.width-110,im.height,20,160,w,h);}
 ui20Portrait(ctx,'ic20_neutral',{x:50,y:201,w:96,h:96});
 msgFaceUse('dialogue');
 IC20.creditsLayout=[];
 const text=(value,x,y,w,h,maxH=14,color='#eaf2ff')=>{const layout=msgDrawBlock({text:value,budget:value.length,x,y,w,h,maxH,minH:8,lineMul:1.25,color,align:'center',valign:'middle',stableCenter:true,outline:false});IC20.creditsLayout.push({text:value,x,y,w,h,layout});return layout;};
 text('CREDITS',24,133,VW-48,22,18,'#ffd58b');
 text('MICHAEL\n"FORGE MASTER"\nCOLE',165,206,VW-211,78,16,'#ffd58b');
 text('DIRECTOR / DESIGNER / CODER\nMUSIC / SOUNDS',48,302,VW-96,30,12);
 text('ART',48,342,VW-96,16,12,'#a7cce5');
 text('GPT IMAGES, NANO BANANA PRO\n& SPRITECOOK',48,361,VW-96,30,12);
 text('WRITTEN, CODED AND DESIGNED BY\nMICHAEL "FORGE MASTER" COLE',48,408,VW-96,22,9);
 text('COLEFORGE PHOENIX ENGINE',28,470,VW-56,15,10,'#a7cce5');
 msgFaceUse(null);controlHintRow([['pad_b','BACK']]);
 if(Input.mouse.down&&!drawCredits._md)Input.injectTap('enter');drawCredits._md=Input.mouse.down;
 if(Input.menuConfirm()||Input.menuBack()||backButton()){setState(GS.TITLE);menuIndex=3;}
};
