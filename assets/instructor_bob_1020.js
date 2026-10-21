'use strict';
/* Tutorial-only ownership: authored Cole portraits, B.O.B.'s live modules and dossier.
   Ordinary combat, controls, elements, targeting, audio and all campaign stages retain their owners. */
const BOB20_SPEC=Object.freeze({missile:Object.freeze({hp:90,element:null}),cannon:Object.freeze({hp:110,element:null}),core:Object.freeze({hp:240,element:'ice',missileMultiplier:2})});
const IC20={base:{keys:sg20Keys,warm:sg20Warm,ready:sg20LayersReady,ask:tutAskDraw,
 overlay:tutOverlayDraw,update:updatePlay,next:tutNext,cleanup:tutCleanup,hold:tutHold,start:tutStart,
 draw:drawEnemy,hit:hitEnemy,kill:killEnemy,wave:sg20ExamWave,strikeTick:s6StrikeMissileTick,jet:jetTick},draws:0,partDraws:0,hits:[]};
const IC20_KEYS=[...IC20_ART.portraits,IC20_ART.whole,IC20_ART.card,...Object.values(IC20_ART.parts),...Object.values(IC20_ART.views)].map(a=>a.key);
for(const a of [...IC20_ART.portraits,IC20_ART.whole,IC20_ART.card,...Object.values(IC20_ART.parts),...Object.values(IC20_ART.views)])XART._src[a.key]=a.path;
const IC20_MISSILES=[...Array.from({length:6},(_,i)=>'s1fx_jungle_missile_'+i),...Array.from({length:6},(_,i)=>S1_MUZZLE_MILITARY+'_'+i),...Array.from({length:8},(_,i)=>'laser_round_muzzle_'+i)];
sg20Keys=function(){return [...IC20.base.keys(),...IC20_KEYS,...IC20_MISSILES];};
sg20Warm=function(){IC20.base.warm();for(const k of [...IC20_KEYS,...IC20_MISSILES])XART.rdy(k);
 if(!IC20.audio){IC20.audio=true;Snd.prepare(['expSmall','expBig','shieldHitHeavy','powerup','enemyMachineGunLight','missileLaunch']);}};
sg20LayersReady=function(){return IC20.base.ready()&&IC20_KEYS.every(k=>XART.rdy(k))&&IC20_MISSILES.every(k=>XART.rdy(k));};
tutStart=function(){IC20.hits=[];IC20.labStats={};return IC20.base.start.apply(this,arguments);};
function ic20Port(smile=false){if(smile)return 'ic20_smile';
 const T=TUT,t=T?T._sg?.time||T.t:0,typing=T&&(T.typed||0)<(T.say||T.text||'').length;
 return typing?['ic20_neutral','ic20_talk-small','ic20_neutral','ic20_talk-open'][Math.floor(t*8)%4]:'ic20_neutral';}
tutAskDraw=function(dt){const prior=dlgBox;
 dlgBox=function(o){return prior({...o,who:'COLE',portraitKey:'ic20_neutral',tint:UI20.color('COLE')});};
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
 const F=tutField(),G={x:F.cx,y:tutTop()+55,y0:tutTop()+55,k:.88,t:0,mode,parts:{},cycle:null,next:.8,turn:0};
 for(const id of mode==='exam'?['missile','cannon','core']:mode==='warn'?['cannon']:mode==='strike'?['missile']:['core']){
  const a=IC20_ART.parts[id],off={x:(a.target[0]-128)*G.k,y:(a.target[1]-128)*G.k};
  const hp=mode==='exam'?BOB20_SPEC[id].hp:mode==='element'?150:9999;
  const e=tutSpawn('s1jetBomber',G.x+off.x,G.y+off.y,hp,{amp:0});if(!e)continue;
  e.w=id==='core'?66:id==='missile'?48:42;e.h=id==='core'?56:id==='missile'?94:108;
  e._bob20={id,G,off};e._esh=null;e._iceEnemy=id==='core';e.dropOk=false;
  G.parts[id]=e;
 }
 L.bob=G;L.units=Object.values(G.parts);return G;
}
function bob20Alive(e){return !!e&&!e.dead&&e.hp>0&&e._dyingT==null;}
// B.O.B. borrows the native enemy damage/target container, never the Stage1 jet AI or its elite HP multipliers.
jetTick=function(e,dt){if(e?._bob20)return;return IC20.base.jet.apply(this,arguments);};
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
 const p=rect(982,44,156,156);if(XART.rdy('ic20_neutral'))ui20Portrait(ctx,'ic20_neutral',p);
 text('B.O.B.',[278,80,644,43],39,'#ffd38b');
 text('BALLISTICS ORIENTATION BOT',[278,132,644,30],24,'#c0ebff');
 const names=['FULL UNIT','MISSILE POD','CANNON POD','CRYO REACTOR'];
 text(names[L.sel],[94,226,560,43],31,'#a5f5ff');
 if(a&&XART.rdy(a.key)){const f=Math.floor(L.yaw)%a.frames,c=a.cells[f],r=rect(92,278,564,315),sz=Math.min(r.w,r.h),mx=r.x+(r.w-sz)/2,my=r.y+(r.h-sz)/2;
  ctx.save();ctx.beginPath();ctx.rect(r.x,r.y,r.w,r.h);ctx.clip();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),...c,mx,my,sz,sz);ctx.restore();IC20.cardFrame={part:key,frame:f};IC20.cardLayout.model={x:mx,y:my,w:sz,h:sz};}
 const lines=key==='whole'?['440 TOTAL HP','TRAINING MECH / ICE','WEAK: FIRE X1.5','RESISTS ICE X0.5','PODS FIRST, THEN CORE','MISSILE CORE BONUS X2']:
 key==='core'?['240 HP / ICE','BLUE REACTOR TARGET','WEAK: FIRE X1.5','RESISTS ICE X0.5','RETINA MISSILE X2','SHUTTER: BOTH PODS']:
 key==='missile'?['90 HP / STEEL','GROUND MISSILE POD','NEUTRAL DAMAGE X1','NO ELEMENT BONUS','RETINA TARGET: POD','STOPS GROUND STRIKES']:
 ['110 HP / STEEL','FOV MACHINE CANNON','NEUTRAL DAMAGE X1','GREEN AIM / YELLOW SET','RED: LEAVE THE LANE','STOPS GUN VOLLEYS'];
 for(let i=0;i<lines.length;i++)text(lines[i],[735,234+i*56,364,42],27,i===2?'#ffd38b':'#e6f3f3');
 text('WHY HAVEN\'T I RETIRED YET?',[135,661,930,83],36,'#ffd38b');IC20.layoutCapture=null;
 if(typeof controlHintRow==='function')controlHintRow([['pad_dpad','PART / TURN'],['pad_a',L.age>3.8?'DEPLOY':'SCANNING'],['pad_b','FULL UNIT']]);
}
const IC20_CARD={id:'bob_card',good:'DOSSIER STUDIED',text:()=> 'MEET B.O.B.! INSPECT HIS PARTS. BREAK BOTH PODS TO EXPOSE THE ICE REACTOR. AIM RETINA MISSILES AT THE BLUE CORE.',
 start(L){L.age=0;L.yaw=0;L.sel=0;L.seen={0:true};},tick:ic20CardTick};
TUT_LESSONS.splice(TUT_LESSONS.findIndex(d=>d.id==='exam'),0,IC20_CARD);
const ic20ExamStart=SG20_EXAM.start,ic20ExamTick=SG20_EXAM.tick,ic20ExamDraw=SG20_EXAM.draw;
sg20ExamWave=function(L){if(L.wave!==2)return IC20.base.wave(L);
 tutClearField();L.wave=3;L.gap=0;L.age=0;L.c=null;bob20Spawn(L,'exam');};
SG20_EXAM.text=()=> 'GRADUATION: TWO ESCORT WAVES, THEN B.O.B. HIS PODS ARE REAL TARGETS. WATCH THE FOV AND GROUND WARNINGS. BREAK BOTH PODS, THEN HIT HIS EXPOSED BLUE CORE.';
SG20_EXAM.obj=L=>L.wave<3?'ESCORT WAVE '+L.wave+' / 2':bob20Pods(L.bob)?'DISABLE BOTH WEAPON PODS':'REACTOR OPEN - RETINA + MISSILE';
SG20_EXAM.tick=function(L,dt){if(L.wave<3)return ic20ExamTick(L,dt);
 const G=L.bob;if(!G)return false;G.t+=dt;if(!Object.values(G.parts).some(bob20Alive)){L.gap+=dt;return L.gap>1.3;}
 if(!G.cycle){G.next-=dt;if(G.next<=0){const cannon=bob20Alive(G.parts.cannon),launcher=bob20Alive(G.parts.missile);
  const type=cannon&&launcher?(G.turn++%2?'strike':'lane'):cannon?'lane':launcher?'strike':'core';
  if(type==='strike'){G.q=bob20Ground(G.parts.missile);G.next=3.9;}
  else G.cycle={type,t:0,x:player.x,fired:0};}}
 const C=G.cycle;if(!C)return false;C.t+=dt;
 const gun=C.type==='core'?G.parts.core:G.parts.cannon;if(!bob20Alive(gun)){G.cycle=null;G.next=.8;return false;}
 if(C.t<1)C.x+=clamp(player.x-C.x,-110*dt,110*dt);
 if(C.t<3){combatWarningTick(gun,'bob20-lane',C.t,3);return false;}
 if(C.fired<6&&C.t>=3+C.fired*.16){const m=bob20Port(gun),a=Math.atan2(PLAY.y+PLAY.h-m.y,C.x-m.x);
  for(const o of [-.08,0,.08])tutShoot(m.x,m.y,a+o,3);bob20Muzzle(gun);C.fired++;}
 if(C.t>5){G.cycle=null;G.next=1;}return false;
};
SG20_EXAM.draw=function(L){if(L.wave<3)return ic20ExamDraw(L);const G=L.bob,C=G?.cycle;
 if(C&&C.t<3){const e=C.type==='core'?G.parts.core:G.parts.cannon;if(bob20Alive(e))combatWarningDraw(e,{...bob20Port(e),ex:C.x,ey:PLAY.y+PLAY.h+20,progress:C.t/3,width:48});}
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
