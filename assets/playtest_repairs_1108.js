'use strict';
/* PR118: repairs from Mike's November 8 playtest of Windows Rev F. Loaded last.
   Each block names the defect it closes. Evidence: docs/PLAYTEST_REPAIRS_1108.md. */
const PR118={base:{free:cp22Free,opening:s6OpeningTick,live:ls112Live,cfg:_levelCfg,phase:bg6Phase,
 play:updatePlay,begin:beginStage,load:stageLoadBegin},cityT:0,events:[]};
function pr118Log(event,data={}){PR118.events.push({event,stage:run.stage,t:stageTimer,...data});if(PR118.events.length>200)PR118.events.shift();}

/* ---- STAGE 6 OPENING ----
   (1) cp22Free never checked the scripted opening, so Tempest Dashers and strays attacked during
   the radio scene. (2) updatePlayerLocks empties playerLocks when the pilot dies, so the opening's
   missile lock could never fire, phase 'lock' waited forever on launched===2, s6OpeningActive()
   stayed true and the stage clock, wave plan and miniboss were all frozen at 0. */
cp22Free=function(){return !s6OpeningActive()&&PR118.base.free.apply(this,arguments);};
function pr118OpeningSweep(){
 if(run.stage!==6||!s6OpeningActive())return;
 for(const e of enemies){if(e.dead||e._mission29)continue;
  e.dead=true;e.hp=0;e.shoots=false;if(typeof groundTargetingCancel==='function')groundTargetingCancel(e);pr118Log('opening-stray-removed',{type:e.type});}
}
/* Mike: shorten the opening (83 s before the stage clock). The radio buildup runs 1.7x with every line kept; the missile
   lock is rescaled to land on the same beat. The assault loses its repeated bombing pass and its long gaps; each lane's
   own warning is untouched. */
const PR118_S6_SPEED=1.7;
s6OpeningTick=function(dt){
 const O0=s6Opening,fast=O0&&(O0.phase==='cloak'||O0.phase==='reveal');
 PR118.base.opening.call(this,fast?dt*PR118_S6_SPEED:dt);
 const O=s6Opening;if(!O)return;
 if(O.threatLock&&!O._pr118Lock){O._pr118Lock=1;const L=O.threatLock;L.dur/=PR118_S6_SPEED;for(const q of L.launches||[])q.at/=PR118_S6_SPEED;if(L.maxT)L.maxT/=PR118_S6_SPEED;}
 if(O.phase==='lock'&&(player.dead||O.t>3||(O.threatLock&&!playerLocks.includes(O.threatLock)&&O.launched<2))){
  pr118Log('opening-lock-recovered',{dead:!!player.dead,t:O.t});O.launched=2;O.phase='intercept';O.t=0;s6OpeningEnd(false);
 }
 if(O.phase==='assault'&&O.t>O.finish+3){pr118Log('opening-assault-timeout');for(const e of enemies)if(e._mission29&&!e.dead){e.dead=true;e.hp=0;}s6Opening=null;run._mission29OpeningDone=true;Input.clearTaps();}
 pr118OpeningSweep();
};

PR118.base.assaultStart=missionAssaultStart;
missionAssaultStart=function(){const O=PR118.base.assaultStart.apply(this,arguments);if(!O?.events?.length)return O;
 const kept=O.events.filter(e=>!(e.kind==='bomb'&&e.direction==='west'));let prev=kept[0].at,at=prev;
 for(const e of kept){const gap=e.at-prev;prev=e.at;at+=gap>1.7?gap*.6:gap;e.at=at;}
 O.events=kept;O.finish=at+3;return O;};

/* ---- STAGE 6 SKY ----
   LS112 replaced the whole stage with the city plate, so there was no cloud sky at all. The storm
   sky master is restored; the city stays out until the miniboss is dead, then rises under the
   clouds, using the approved LS112 city art. */
const PR118_CITY_FADE=12;
ls112Live=function(n=run.stage){return Number(n)!==6&&PR118.base.live.apply(this,arguments);};
_levelCfg=function(stage=run.stage){const cfg=PR118.base.cfg.apply(this,arguments);return cfg&&Number(stage)===6?{...cfg,city:LS112_ART.levels['6'].key}:cfg;};
bg6Phase=function(){const p=PR118.base.phase.apply(this,arguments);if(run.stage!==6)return p;
 if(!subBossDone)return Math.min(p,BG6_CITY_FROM-.005);
 return Math.max(p,BG6_CITY_FROM+(BG6_CITY_TO-BG6_CITY_FROM)*clamp(PR118.cityT/PR118_CITY_FADE,0,1));};
/* The storm grade was painted over the finished city and clouds, turning them to murk. It lifts as the city arrives. */
PR118.base.grade=bg6WeatherGrade;
bg6WeatherGrade=function(){if(run.stage!==6||!subBossDone)return PR118.base.grade.apply(this,arguments);ctx.save();ctx.globalAlpha*=1-.92*clamp(PR118.cityT/PR118_CITY_FADE,0,1);try{return PR118.base.grade.apply(this,arguments);}finally{ctx.restore();}};
/* The city art leaves its rivers transparent, so the blue sky showed through as bright slabs. Its own night water goes under it. */
PR118.base.sky6=bg6SkyBaseDraw;
bg6SkyBaseDraw=function(img,key,sy,winH,drawW,dstY){const out=PR118.base.sky6.apply(this,arguments);if(run.stage===6&&subBossDone){const k=clamp((bg6Phase()-BG6_CITY_FROM)/(BG6_CITY_TO-BG6_CITY_FROM),0,1),a=k*k*(3-2*k);
 if(a>.002){ctx.save();ctx.beginPath();ctx.rect(0,dstY,drawW,winH);ctx.clip();ctx.globalAlpha*=a;ls112Bed(LS112_ART.levels['6'].material,drawW,dstY,winH);ctx.restore();}}return out;};
const PR118_MOOD=bg6Mood;bg6Mood=function(p){return PR118_MOOD.call(this,run.stage===6?Math.min(p,BG6_CITY_FROM-.005):p);};
stageLoadBegin=function(n,keys){return PR118.base.load.call(this,n,Number(n)===6?[...(keys||[]),LS112_ART.levels['6'].key,LS112_ART.materials[LS112_ART.levels['6'].material].key]:keys);};
beginStage=function(){PR118.cityT=0;return PR118.base.begin.apply(this,arguments);};
updatePlay=function(dt){const out=PR118.base.play.apply(this,arguments);if(run.stage===6&&subBossDone)PR118.cityT+=dt;pr118OpeningSweep();return out;};

/* ---- CINEMATIC CRASH ----
   story_campaign_1103 calls S113.base.start(stage,done) detached, so C22's this.play threw for every
   stage outside 2-6: "draw error in state supplies" after Stage 1 and a broken exit from 7, 8 and 9. */
S113.base.start=S113.base.start.bind(BOFCinematicDirector);

/* ---- OLD TALK SCENES ----
   Stages 7 and 8 were outside story_campaign_1103, so their beats had no scene art and fell back to the
   0930 layout: two full-body pilots standing in the empty Forge lab. Same story, on the current command
   bay and headset panels. The lost pilot never speaks from HQ, so Decker's Stage 7 lines pass to Lizzie. */
function pr118StoryScript(stage,p=run.pilot){const L=s113Line;
 if(stage===7){const hq=['decker','cole','lizzie'].filter(k=>k!==p).slice(0,2),who=p.toUpperCase(),desk=p==='decker'?{}:{actor:'panic'};
  return [L(hq[0],'The portal closed behind '+who+'. No beacon, no weapons telemetry. The sewer is gone.','command-bay',{frame:0,...desk}),
   L(hq[1],'Keep the last vector on the recorder. Leave every channel open. We are not giving up on them.','command-bay',{frame:0,...desk}),
   L('FURY RELAY','LAST TRANSMISSION LOST. UNKNOWN SPACE AHEAD.','command-bay',{frame:0,...(p==='decker'?{}:{actor:'shock'})})];}
 const c=p==='decker'?'cole':'decker';
 return [L(p,'The signal is breaking apart. Fury flight, can anyone hear me?','command-bay',{comic:true,portraitEmotion:'scared',listenerEmotion:'surprised'}),
  L(c,'We have you. Hold that channel. We are bringing you home.','command-bay',{comic:true,portraitEmotion:'happy',listenerEmotion:'surprised'}),
  L(p,'Copy. I have had enough of other dimensions for one day.','command-bay',{comic:true,portraitEmotion:'happy',listenerEmotion:'happy'})];}
PR118.base.storyStart=BOFCinematicDirector.start;PR118.base.storyScript=BOFCinematicDirector.script;
BOFCinematicDirector.start=function(stage,done){if(run.mode==='campaign'&&(stage===7||stage===8))return s113Play('post-'+stage,pr118StoryScript(stage),done);return PR118.base.storyStart.apply(this,arguments);};
BOFCinematicDirector.script=function(stage,p,route){if(stage===7||stage===8)return pr118StoryScript(stage,p||run.pilot);return PR118.base.storyScript.apply(this,arguments);};

/* ---- FLIGHT BEATS BETWEEN LEVELS NOW TRAVEL ----
   Mike: "your not vertically scrolling so I have no clue whats going on". Every airborne beat moved the
   ships over a backdrop fixed in place. The world now moves down the screen under them, as in play:
   arrivals scroll the plate in from above, departures drop it off the bottom into open sky, the sky
   battle is continuous sky. Existing art only; ship banks, clocks and cues are untouched. */
const PR118_SKY='stage6_blue_master',PR118_SPACE='bg_stage05_loop_0923';
function pr118TravelCfg(b){if(b.battle)return {bg:PR118_SKY,mode:'loop'};
 if(b.flight==='return')return {bg:b.s113==='earth'?PR118_SPACE:PR118_SKY,mode:'arrive'};
 if(b.flight==='launch'||b.flight==='squad')return {bg:PR118_SKY,mode:'depart'};return null;}
function pr118Loop(key,off){const im=XART.get(key),iw=im.naturalWidth||im.width,ih=im.naturalHeight||im.height,k=Math.ceil(912/iw),w=iw*k,h=ih*k,x=Math.round((912-w)/2);
 for(let y=((Math.round(off)%h)+h)%h-h;y<512;y+=h)if(y+h>0)ctx.drawImage(im,x,y,w,h);}
PR118.base.s113Bank=s113Bank;PR118.base.s113Visual=s113Visual;PR118.base.s113Keys=s113Keys;
s113Bank=function(name,f,x,y){const T=PR118.travel;
 if(T&&name===T.shot){if(T.mode==='loop'||T.y>=512||T.y<=-512)return true;return PR118.base.s113Bank.call(this,name,f,456,256+Math.round(T.y));}
 return PR118.base.s113Bank.apply(this,arguments);};
s113Keys=function(beats){const keys=PR118.base.s113Keys.apply(this,arguments);for(const b of beats){const c=pr118TravelCfg(b);if(c&&!keys.includes(c.bg))keys.push(c.bg);}return keys;};
s113Visual=function(b,t){const c=pr118TravelCfg(b);if(!c||!XART.rdy(c.bg)){const out=PR118.base.s113Visual.apply(this,arguments);if(b.s113Action&&b.s113?.startsWith('cable-'))pr118ChargeMeter(b,t);return out;}
 const d=b.duration||4,D=d*620;let s,y;
 if(c.mode==='loop'){s=t*760;y=0;}
 else if(c.mode==='arrive'){const u=clamp(t/(d*.8),0,1);s=D*(1-(1-u)*(1-u));y=s-D;}
 else{const u=clamp(t/d,0,1);s=D*u*u;y=s;}
 pr118Loop(c.bg,s);PR118.travel={shot:b.s113,mode:c.mode,y};
 try{return PR118.base.s113Visual.apply(this,arguments);}finally{PR118.travel=null;}};
/* The Stage 7 sewer approach: its five plates become one strip, each scrolling in from above the last. */
PR118.base.ce20Cover=ce20Cover;
ce20Cover=function(key,W,H){const s=BOFCinematicDirector.current,b=s?.beats?.[s.i];if(!b?._sewer17||key!==b.bg)return PR118.base.ce20Cover.apply(this,arguments);
 const prev=s.beats[s.i-1]?.bg||key,y=Math.round(H*clamp(s.t/(b.duration||5.2),0,1)),args=[...arguments];
 ctx.save();ctx.translate(0,y);PR118.base.ce20Cover.apply(this,[prev,...args.slice(1)]);ctx.restore();
 ctx.save();ctx.translate(0,y-H);const out=PR118.base.ce20Cover.apply(this,args);ctx.restore();return out;};

/* ---- STAGE 2 ENDING: THE RUN TO THE RADAR AND THE CHARGE ----
   The level met the dish art on a hard straight line, the world held 1 s then slid at a constant rate and
   stopped dead, the ship cut diagonally over the canyon walls, the radar's lava was baked still, and the
   cable beat showed no charging. Same art and shot; one-time prepared plate, no per-frame readback. */
const PR118_S2={band:120,T:8.6,plates:{},stages:{2:{name:'dish-exit',x:570,y:318,lava:true},4:{name:'pad-exit',x:566,y:246,lava:false}}};
function pr118Smooth(u){u=clamp(u,0,1);return u*u*(3-2*u);}
function pr118S2Plate(a,lava){if(PR118_S2.plates[a.key])return PR118_S2.plates[a.key];
 const c=document.createElement('canvas');c.width=a.w;c.height=a.h;const g=c.getContext('2d',{willReadFrequently:true});g.drawImage(XART.get(a.key),0,0);
 const W=a.w,H=a.h,im=g.getImageData(0,0,W,H),d=im.data,hot=new Uint8Array(W*H),stack=new Int32Array(W*H);
 for(let i=0;i<W*H;i++){const r=d[i*4],g2=d[i*4+1],b=d[i*4+2];if(r>190&&g2>50&&b<95)hot[i]=1;}
 /* Lava is the large connected glow; the dish's small amber lamps stay painted. */
 for(let i=0;i<W*H;i++){if(hot[i]!==1)continue;let n=0,sp=0;const list=[];stack[sp++]=i;hot[i]=2;
  while(sp){const p=stack[--sp];list.push(p);n++;const x=p%W;for(const q of [x>0?p-1:-1,x<W-1?p+1:-1,p-W,p+W])if(q>=0&&q<W*H&&hot[q]===1){hot[q]=2;stack[sp++]=q;}}
  if(lava&&n>=400)for(const p of list)d[p*4+3]=0;}
 /* Ordered 2px dither dissolves the plate's bottom edge into the level's ground. */
 const B=[0,8,2,10,12,4,14,6,3,11,1,9,15,7,13,5],top=H-PR118_S2.band;
 for(let y=top;y<H;y++)for(let x=0;x<W;x++){const v=(y-top)/PR118_S2.band,t=(B[((y>>1)&3)*4+((x>>1)&3)]+.5)/16;if(t<v)d[(y*W+x)*4+3]=0;}
 g.putImageData(im,0,0);return PR118_S2.plates[a.key]=c;}
function pr118S2Exit(dt){const C=PR118_S2.stages[run.stage],a=S113_ART.banks[C.name],mat=C.lava?LS112_ART.levels['2']?.material:null,matKey=LS112_ART.materials[mat]?.key,
  keys=[a.key,'s113_landing-'+run.pilot,...(coopActive()?['s113_landing-'+p2Pilot().key]:[]),'s113_fade',...(matKey?[matKey]:[])],band=PR118_S2.band,T=PR118_S2.T;
 if(!S113.exit){S113.exit={t:0,wait:0,startX:player.x,startY:player.y,cam:camX,done:false,snap:null};Audio.stopMusic();Audio.startMusic('stageclear');}
 const e=S113.exit;e.wait+=dt;const ready=s113Warm(keys);if(ready)e.t+=Math.max(0,dt);const t=e.t;
 if(dt>0)efxClock+=Math.min(dt,.1);try{updateFlyoverLiveFx(dt);}catch(_e){}
 if(!ready&&e.wait>12){S113.exit=null;return S113.base.flyover(dt);}
 if(t>.4&&Input.menuStart()){e.done=true;S113.exit=null;setState(GS.STAGECLEAR);return;}
 const travel=Math.round(a.h*pr118Smooth(t/T)),pan=pr118Smooth((travel-640)/(a.h-640)),targetX=C.x,targetY=C.y,
  camera=Math.round(e.cam+(clamp(targetX-VW/2,0,worldWidth()-VW)-e.cam)*pan),py=travel-a.h;camX=camera;
 ctx.save();ctx.fillStyle='#000';ctx.fillRect(0,0,VW,VH);
 if(travel<VH){ctx.save();ctx.translate(0,travel);_cinematicHidePlayer=true;try{drawWorld(0);}finally{_cinematicHidePlayer=false;ctx.restore();}}
 if(!e.snap&&ready){const m=ctx.getTransform(),s=document.createElement('canvas');s.width=VW;s.height=band;const g=s.getContext('2d');g.imageSmoothingEnabled=false;g.translate(0,band);g.scale(1,-1);
  g.drawImage(cv,m.e,m.f,VW*m.a,band*m.d,0,0,VW,band);e.snap=s;}
 ctx.imageSmoothingEnabled=false;
 if(ready&&py<VH){if(e.snap&&travel<VH+band)ctx.drawImage(e.snap,0,travel-band);
  if(mat&&py+a.h-band>0){ctx.save();ctx.translate(0,py);ctx.beginPath();ctx.rect(0,0,VW,a.h-band);ctx.clip();ls112Bed(mat,VW,0,a.h-band);ctx.restore();}
  ctx.drawImage(pr118S2Plate(a,C.lava),-camera,py);}
 const v=pr118Smooth(t/T),x=e.startX+(targetX-e.startX)*pan,y=e.startY+(targetY-e.startY)*v;
 s113Bank('landing-'+run.pilot,clamp((t-7.8)*12,0,31),Math.round(x-camera),Math.round(y));
 if(coopActive())s113Bank('landing-'+p2Pilot().key,clamp((t-7.8)*12,0,31),Math.round(x-camera-58),Math.round(y+18));
 if(t>10.8)s113Bank('fade',clamp(Math.floor((t-10.8)/.05),0,16),VW/2,VH/2);
 ctx.restore();S113.last={shot:C.name,time:t,travel,ship:[x,y],landed:t>=10.4,fade:t>10.8};
 if(t>=11.7&&!e.done){e.done=true;S113.events.push({event:'landed-to-stats',stage:run.stage});S113.exit=null;flyoverT=0;setState(GS.STAGECLEAR);}}
PR118.base.flyover=drawFlyover;
drawFlyover=function(dt){if(run.mode==='campaign'&&PR118_S2.stages[run.stage]&&!debugFight&&!tutLive())return pr118S2Exit(dt);return PR118.base.flyover.apply(this,arguments);};
/* The cable beat: the plug goes in at 3.6 s, the meter fills, and the ship lights up exactly when it is full. */
function pr118ChargeMeter(b,t){const u=clamp((t-3.6)/3.6,0,1),n=20,lit=Math.floor(u*n),W=240,x=456-W/2,y=34;
 if(t<3.4)return;
 ctx.fillStyle='#05090e';ctx.fillRect(x-8,y-22,W+16,44);ctx.fillStyle='#3a4652';ctx.fillRect(x-6,y-20,W+12,2);ctx.fillRect(x-6,y+18,W+12,2);
 for(let i=0;i<n;i++){ctx.fillStyle=i<lit?(u>=1&&Math.floor(t*8)%2?'#ffffff':'#46e6ff'):'#16303c';ctx.fillRect(x+i*12,y+2,10,12);}
 const prior=_msgFace;msgFaceUse('game');msgDrawBlock({text:u>=1?'CHARGE COMPLETE':'CHARGING SHIP SYSTEMS',budget:99,x,y:y-18,w:W,h:18,maxH:12,minH:8,color:u>=1?'#ffffff':'#9ff2ff',align:'center',stableCenter:true,valign:'middle',lineMul:1});msgFaceUse(prior);
 if(lit>(b._pr118Lit||0)){b._pr118Lit=lit;if(lit>=n)Snd.play('crackle');else if(lit%2===0)Snd.play('blip');}}
PR118.base.s113Script=s113Script;
s113Script=function(stage){const rows=PR118.base.s113Script.apply(this,arguments);if(stage===2)for(const b of rows)if(b.s113Action&&b.s113?.startsWith('cable-')){b.duration=9;b.sequence=[0,1,2,2,3];b.step=1.8;}return rows;};

/* ---- STAGE 4 BOSS: CHARGED ON THE TESLA PAD ----
   Mike: he is already at the pad as we approach it; do not stop the game or the wave. So this is a scene on the
   moving road: a stand-in of the boss sits on the pad as it scrolls in, the six coils charge him, the shield forms and
   he launches away. It cannot be hit and touches no clock, wave or enemy. The real boss then arrives on the stage's own
   schedule. window.PR118_PAD_OFF=1 removes it. */
const PR118_PAD={x:338,cy:2354,startY:-30,small:.38};
PR118.padGuy=null;PR118.padLine=null;PR118.padDone=false;
function pr118PadOn(){return !window.PR118_PAD_OFF&&run.stage===4&&!debugFight&&ls112Live(4);}
function pr118PadY(){const T=LS112.clock.terrain;return T&&T.stage===4?PR118_PAD.cy-T.source+viewTopY():null;}
function pr118PadMake(y){const sb=boss,sa=bossActive,sub=subBoss;let g=null;
 try{PR118.base.spawnBoss.call(null,'stormsovereign');g=boss;}catch(_e){g=null;}boss=sb;bossActive=sa;subBoss=sub;
 PR118.padDone=true;if(!g)return;const A=sa14State(g);g.enter=false;g.x=PR118_PAD.x;g.y=y;g._noHit=true;A.angle=0;A.scale=PR118_PAD.small;A.depth=false;
 for(let i=0;i<12;i++)XART.rdy('s4w_lightning_shield_'+i);XART.rdy('cfx_stage4_chain_lightning');
 g._pr118Pad={t:0,launch:5,fly:1.2,shieldAt:3.3,done:false,lit:0,cued:{}};PR118.padGuy=g;}
function pr118PadUpdate(dt){if(!pr118PadOn()||state!==GS.PLAY)return;
 const L=PR118.padLine;if(L){L.age+=dt;if(L.age>=L.duration)PR118.padLine=null;}
 let g=PR118.padGuy;
 if(!g){if(!PR118.padDone&&!boss&&!bossActive&&!subBossActive){const y=pr118PadY();if(y!=null&&y>=PR118_PAD.startY&&y<VH)pr118PadMake(y);}return;}
 if(boss&&bossActive){PR118.padGuy=null;return;}
 const P=g._pr118Pad,A=sa14State(g),y=pr118PadY();P.t+=dt;const t=P.t,cue=(k,f)=>{if(!P.cued[k]){P.cued[k]=1;f();}};
 const lit=clamp(Math.floor((t-.6)/.3)+1,0,6);if(lit>P.lit){P.lit=lit;Snd.play('crackle');}
 if(t>=P.shieldAt)cue('shield',()=>{Audio.SFX.bossPhase?.();});
 if(t<P.launch){A.scale=PR118_PAD.small;if(y!=null)g.y=y;return;}
 cue('launch',()=>{Snd.play('jetDash');shake=Math.max(shake,5);P.from=g.y;const text="I guess that's the signal we found. Don't let it get away!";PR118.padLine={who:run.pilot==='decker'?'COLE':'DECKER',text,age:0,duration:text.length/38+2.7};});
 const u=clamp((t-P.launch)/P.fly,0,1),e=u*u;A.scale=lerp(PR118_PAD.small,1,e);g.y=lerp(P.from,-220,e);if(u>=1){P.done=true;PR118.padGuy=null;}}
PR118.base.spawnBoss=spawnBoss;
PR118.base.padBegin=beginStage;beginStage=function(){PR118.padGuy=null;PR118.padLine=null;PR118.padDone=false;return PR118.base.padBegin.apply(this,arguments);};
/* All authored art: the fight's own chain lightning from the coils, the lightning-wrap swirl, then his real shield. */
function pr118PadSwirl(b,bank){const P=b._pr118Pad,A=sa14State(b),u=clamp((P.t-2.2)/1,0,1);if(u<=0)return;
 const alpha=u*(P.t>=P.shieldAt?Math.max(.45,1-(P.t-P.shieldAt)/1.4):1)*(bank==='wrap_back'?.6:1);l21Wrap(bank,P.t,b,b.w*A.scale*(1.2+u*.5),0,alpha);}
function pr118PadDraw(b){const P=b._pr118Pad,T=LS112.clock.tesla,t=P.t,A=sa14State(b);
 if(T&&t<P.launch)for(let i=0;i<Math.min(P.lit,T.sockets.length);i++){const s=T.sockets[i],d=Math.hypot(b.x-s.x,b.y-s.y);sa14BlueArc(s.x,s.y,Math.atan2(b.y-s.y,b.x-s.x),d,t+i*.13,lerp(.85,.2,clamp((t-2.2)/.7,0,1)));}
 pr118PadSwirl(b,'wrap_front');
 const u=clamp((t-P.shieldAt)/1.4,0,1),key='s4w_lightning_shield_'+Math.floor(t*12)%12;
 if(u>0&&XART.rdy(key)){const size=b.w*1.34*A.scale*(.7+.3*u);ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.40*u;ctx.drawImage(XART.get(key),b.x-size/2,b.y-size/2,size,size);ctx.restore();}}
/* The line rides the Command HUD radio, so nothing stops for it. */
PR118.base.ui20Radio=ui20Radio;
ui20Radio=function(){const L=PR118.padLine;if(state===GS.PLAY&&L)return L;return PR118.base.ui20Radio.apply(this,arguments);};
PR118.base.updateBossLine=updatePlay;
updatePlay=function(dt){const out=PR118.base.updateBossLine.apply(this,arguments);pr118PadUpdate(Math.max(0,dt||0));return out;};
PR118.base.mr27Draw=mr27Draw;PR118.base.mr27Over=mr27Over;
mr27Draw=function(b){const on=b?._pr118Pad&&!b._pr118Pad.done;if(on)pr118PadSwirl(b,'wrap_back');const out=PR118.base.mr27Draw.apply(this,arguments);if(on)pr118PadDraw(b);return out;};
/* His shield emitters and glow belong to the fight; the coils are building that shield here. */
mr27Over=function(b){if(b?._pr118Pad&&!b._pr118Pad.done)return;return PR118.base.mr27Over.apply(this,arguments);};
PR118.base.drawBulletsPad=drawBullets;
drawBullets=function(){const g=PR118.padGuy;if(g&&run.stage===4&&state===GS.PLAY)mr27Draw(g);return PR118.base.drawBulletsPad.apply(this,arguments);};

/* ---- SPREAD LASER / PLASMA CANNON BOXES ----
   coleforge_fx_1104 painted these two containers as the bare weapon icon, so an unbroken box looked like a
   loose powerup. The box now draws as the stage's plain spinning crate; the weapon icon only appears once it breaks. */
cfx114NewPickup=function(p){return spaceWeaponsActive()&&p.kind==='weapon'&&[3,4].includes(p.spaceType);};

/* ---- FORGE: EARNED ELEMENTS AND PREVIEW TARGET ----
   A run that begins part-way through (level select, password) starts with an empty element list, so the Forge
   offered only the boss just beaten: Chromium after Stage 5, Tidal after Stage 9. Every stage already cleared
   now counts. Chromium and Tidal only do anything on contact and the preview had nothing to hit, so they
   looked inert; their rounds now burst at a fixed point in the preview, with Chromium's real mirror shard. Nothing is drawn there. */
function pr118ForgeEarned(){if(!run)return;const st=run.stage|0,ranks=typeof hf23RankStages==='function'?hf23RankStages():[];
 for(let n=1;n<=9;n++){const implied=st===9?n<=5:(n<st||(n===st&&state!==GS.STAGESEL));if((ranks.includes(n)||implied)&&BOSS_ELEMENT_BY_STAGE[n]){forgeDiscover(BOSS_ELEMENT_BY_STAGE[n]);if(implied&&typeof hf23Grant==='function')hf23Grant(n);}}}
PR118.base.forgeStart=forgeStart;
forgeStart=function(){pr118ForgeEarned();return PR118.base.forgeStart.apply(this,arguments);};
/* The Forge has six bays but a run can own more guns. The bays become a window on every owned weapon: LEFT/RIGHT
   past either end slides it. The chosen loadout itself is put back after every frame and never changes here. */
PR118.base.drawForge=drawForge;
drawForge=function(dt){const F=forge,real=run?.loadout;if(!F||state!==GS.FORGE||!Array.isArray(real))return PR118.base.drawForge.apply(this,arguments);
 const all=[...new Set([...real,...(F.pool||[])])];if(all.length<=FORGE_LOADOUT_MAX)return PR118.base.drawForge.apply(this,arguments);
 const max=all.length-FORGE_LOADOUT_MAX;F.first=clamp(F.first|0,0,max);const win=all.slice(F.first,F.first+FORGE_LOADOUT_MAX),was=F.sel|0,row=F.row;
 for(const w of win)XART.rdy(weaponIconKey(w,Math.max(1,(run.wlevels&&run.wlevels[w])|0),{bare:1}));
 run.loadout=win;let out;try{out=PR118.base.drawForge.apply(this,arguments);}finally{if(run.loadout===win)run.loadout=real;}
 if(forge===F&&row===0&&F.row===0){const last=FORGE_LOADOUT_MAX-1;
  if(was===0&&F.sel===last){if(F.first>0){F.first--;F.sel=0;}else F.first=max;}
  else if(was===last&&F.sel===0){if(F.first<max){F.first++;F.sel=last;}else F.first=0;}}
 if(state===GS.FORGE&&forge===F&&F.row===0){const W=typeof cutsceneViewWidth==='function'?cutsceneViewWidth():VW,y=VH*.40;
  if(F.first>0)drawSelArrow(W*.045,y,14,true,'y');if(F.first<max)drawSelArrow(W*.955,y,14,false,'y');}
 return out;};
PR118.base.previewTick=forgePreviewTick;
function pr118PreviewTarget(P){return P&&(P.elem==='chrome'||P.elem==='water')&&P.space==null;}
forgePreviewTick=function(P,VWp,VHp,dt){const out=PR118.base.previewTick.apply(this,arguments);if(!pr118PreviewTarget(P)||P.err)return out;
 const T=P.dummy||(P.dummy={x:VW/2,y:VH-250,flash:0,cd:0}),step=Math.min(dt,.05);T.flash=Math.max(0,T.flash-step);T.cd-=step;
 forgePreviewSwap(P,VW,VH,function(){const hit=y=>{efxBurst(P.elem,T.x,y,40);T.flash=.1;
   if(P.elem==='chrome')pBullets.push({x:T.x,y:T.y-34,vx:0,vy:-9,w:4,h:10,dmg:2,kind:'spread',lv:1,t:0,_inf:'chrome',_infLv:1,_el:'chrome',_child:true,_mirror:true});};
  for(const b of pBullets.slice()){if(b._mirror)continue;
   if(['beam','flame','firewhip'].includes(b.kind)){if(T.cd<=0){T.cd=.22;hit(T.y+16);}continue;}
   if(Math.abs(b.x-T.x)<40&&Math.abs(b.y-T.y)<30){b.dead=true;hit(b.y);}}
  pBullets=pBullets.filter(b=>!b.dead);});
 return out;};

/* ---- NOV 9 LIST ---- */
/* Approach alert: half size, three on/off flashes across its own duration. */
drawApproachAlert=function(elapsed,remaining,cy=VH*.42){if(!XART.rdy('alert_critical_1024'))return;const im=XART.get('alert_critical_1024'),iw=im.naturalWidth||im.width,ih=im.naturalHeight||im.height;if(!iw||!ih)return;
 const period=Math.max(.05,(elapsed+remaining)/6);if(Math.floor(elapsed/period)%2)return;
 const w=Math.min(360,VW*.74)*.5,h=w*ih/iw;ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,Math.round(VW/2-w/2),Math.round(cy-h/2),w,h);ctx.restore();};
/* One avatar for every pilot's onboard computer. */
XART._src.system_avatar_1109='assets/game/shared/ui/system_avatar_1109/system.png';XART.rdy('system_avatar_1109');
PR118.base.dlgSys=dlgBox;
dlgBox=function(o){if(o&&/^(SHIP )?SYSTEMS?$/i.test(String(o.who||'')))return PR118.base.dlgSys.call(this,{...o,portrait:false,portraitKey:'system_avatar_1109'});return PR118.base.dlgSys.apply(this,arguments);};
/* Razorback half-circle: it left the hull centre along the hull's heading. It now leaves the main gun along the turret, which tracks the player. */
function pr118RzbWaves(){for(const b of [subBoss,boss]){const R=b?._rzb;if(!R||b.dead)continue;for(const w of R.waves||[]){if(w._pr118||!(w.arc>2))continue;w._pr118=1;const m=rzbFwd(b,R.turret,(142-(R.recoil||0))*rzbScale(b));w.x=m.x;w.y=m.y;w.a=R.turret;}}}
/* Stage 1 delta jets: faster, on a corkscrew. Applied as an offset so it rides on whichever flight owner moves them. */
function pr118S1Jets(dt){if(run.stage!==1||!(dt>0))return;for(const e of enemies){if(!/^s1jetdelta/.test(e.type||''))continue;const S=e._pr118Sp||(e._pr118Sp={t:0,ox:0,oy:0,dir:e.x<(camLeftX()+camRightX())/2?1:-1,ph:(e.x*7+e.y)%6.28,px:e.x,py:e.y});
  if(e.dead||e._dyingT!=null||e._fb9Swoop||e._s1Kamikaze||e._s1Rush)continue;S.t+=dt;
  const R=Math.min(1,S.t/.7)*38,a=S.ph+S.t*5.2*S.dir,nx=Math.cos(a)*R,ny=Math.sin(a)*R+S.t*72;
  e.x=clamp(e.x-S.ox+nx,camLeftX()+18,camRightX()-18);e.y+=ny-S.oy;S.ox=nx;S.oy=ny;
  const dx=e.x-S.px,dy=e.y-S.py;S.px=e.x;S.py=e.y;if(Math.hypot(dx,dy)>.4&&typeof gf113SetHead==='function')gf113SetHead(e,Math.atan2(dy,dx));}}
PR118.base.playNov9=updatePlay;
updatePlay=function(dt){const out=PR118.base.playNov9.apply(this,arguments);if(state===GS.PLAY){pr118RzbWaves();pr118S1Jets(dt);}return out;};
/* Campaign map: decode its art during the stage-clear flow and hold black until it can draw, so it never opens on empty ocean. */
function pr118MapKeys(){return Object.keys(XART._src).filter(k=>/^cm2_/.test(k));}
PR118.base.setStateMap=setState;
setState=function(s){if(s===GS.FLYOVER||s===GS.STAGECLEAR||s===GS.FORGE||s===GS.LOADOUT)for(const k of pr118MapKeys())XART.rdy(k);if(s===GS.STAGESEL)PR118.mapT=0;return PR118.base.setStateMap.apply(this,arguments);};
PR118.base.drawMap=drawStageSelect;
/* "LEVEL N UNLOCKED" sat under the ship in faint green: moved clear of it, with a dark outline. */
function pr118MapDraw(self,args){const f=ctx.fillText;ctx.fillText=function(s,x,y,...r){if(/^LEVEL \d+ UNLOCKED$/.test(String(s))){const lw=ctx.lineWidth,sc=ctx.strokeStyle;ctx.lineWidth=4;ctx.strokeStyle='#04101c';ctx.strokeText(s,x,y+24);ctx.lineWidth=lw;ctx.strokeStyle=sc;return f.call(ctx,s,x,y+24,...r);}return f.call(ctx,s,x,y,...r);};try{return PR118.base.drawMap.apply(self,args);}finally{delete ctx.fillText;}}
drawStageSelect=function(dt){const out=pr118MapDraw(this,arguments);if(cmap2On()&&(PR118.mapT||0)<3&&state===GS.STAGESEL){PR118.mapT=(PR118.mapT||0)+(dt>0?dt:0);if(!pr118MapKeys().every(k=>XART.rdy(k))){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,cv.width,cv.height);ctx.restore();}else PR118.mapT=3;}return out;};

/* ---- SHIELDED ENEMIES STAY READABLE ----
   The November 4 blue and green shells were painted solid at 2.5x the hull, hiding who was inside. Enemies now use the
   existing translucent hull-sized shell; the player's own Axel shield keeps the big one. */
PR118.base.shieldLayer=drawEnemyShieldLayer;
drawEnemyShieldLayer=function(){const big=cfx114Shield;cfx114Shield=function(){return false;};try{return PR118.base.shieldLayer.apply(this,arguments);}finally{cfx114Shield=big;}};

/* ---- BOSS HIT FLASH ----
   Mike: enemies flash every few seconds instead of on every hit. Each boss has its own damage route and many never set a
   flash: measured 2 of 281 hits on Stage 7's boss and about half on Tidal Sovereign. Any health drop on a boss or miniboss,
   by any route, now flashes it, unless one of its pieces is already showing that hit. window.PR118_FLASH_OFF=1 disables. */
const PR118_FLASH_T=.07;
function pr118PartLists(b){const out=[];for(const k of Object.keys(b)){const v=b[k];if(!v||typeof v!=='object')continue;if(Array.isArray(v)){if(v.length&&v[0]&&typeof v[0]==='object'&&'hp' in v[0])out.push(v);continue;}
  if(k[0]==='_'&&!(v instanceof Set)&&!(v instanceof Map))for(const j of Object.keys(v)){const w=v[j];if(Array.isArray(w)&&w.length&&w[0]&&typeof w[0]==='object'&&'hp' in w[0])out.push(w);}}return out;}
/* Under sustained fire a flash on every hit is one solid white boss, so it strobes: 0.05 s on, at most every 0.14 s, while damage continues. */
const PR118_FLASH_ON=.05,PR118_FLASH_EVERY=.14;
function pr118Strobe(o,hit,now){if(hit)o._pr118LastHit=now;if(!(now-(o._pr118LastHit??-9)<.25))return;
 if(hit&&now>=(o._pr118Next||0)){o._pr118Next=now+PR118_FLASH_EVERY;o._pr118On=now+PR118_FLASH_ON;o.flash=PR118_FLASH_ON;return;}
 if(now<(o._pr118On||0))return;if('flash' in o)o.flash=0;}
function pr118BossFlash(){if(window.PR118_FLASH_OFF)return;const now=efxClock;for(const b of [subBoss,boss]){if(!b||b.dead||b.enter||b._pr118Pad)continue;
  const L=pr118PartLists(b);let t=+b.hp||0,shown=false;
  for(const a of L)for(const q of a){const h=Math.max(0,+q.hp||0),w=q._pr118Hp;q._pr118Hp=h;t+=h;const hit=w!=null&&h<w-.001;if(!('flash' in q))continue;pr118Strobe(q,hit,now);if(hit)shown=true;}
  const was=b._pr118Hp;b._pr118Hp=t;pr118Strobe(b,was!=null&&t<was-.001&&!shown,now);}}
PR118.base.playFlash=updatePlay;
updatePlay=function(dt){const out=PR118.base.playFlash.apply(this,arguments);if(state===GS.PLAY)pr118BossFlash();return out;};

/* ---- DRACODIA: RETINAS ON THE FINAL BODY ----
   Her final body offered no Retina targets at all while any copied form was alive, so the Retina looked broken. It can now
   always be locked. Her ward still holds: those hits flash and ring off without damage until the copies are dead. */
PR118.base.rdTargets=retinaBossTargets;
retinaBossTargets=function(b){if(b&&typeof rd30Locked==='function'&&rd30Locked(b))return RD30.base.targets.call(this,b);return PR118.base.rdTargets.apply(this,arguments);};

/* ---- FURIOUS, STAGES 5-9 ----
   Mike: enemies are too easy even on Furious. First pass on regular enemies only: 35% more health and 10% faster rounds.
   Warning times, bosses, minibosses and every other difficulty are untouched. window.PR118_FURY_OFF=1 disables. */
const PR118_FURY={hp:1.35,speed:1.10};
function pr118FuryOn(){return !window.PR118_FURY_OFF&&diffKey==='furious'&&(run.stage|0)>=5&&(run.stage|0)<=9;}
PR118.base.furySpawn=spawnEnemy;
spawnEnemy=function(){const out=PR118.base.furySpawn.apply(this,arguments);if(out&&pr118FuryOn()&&!out._pr118Fury&&!out._boss&&!out._prop&&!out.prop){out._pr118Fury=1;out.hp=Math.ceil(out.hp*PR118_FURY.hp);for(const k of ['maxhp','_maxhp'])if(out[k]>0)out[k]=Math.ceil(out[k]*PR118_FURY.hp);}return out;};
PR118.base.furyShot=eShootT;
eShootT=function(x,y,a,spd){if(pr118FuryOn()&&!boss&&!subBossActive&&Number.isFinite(spd)){const args=[...arguments];args[3]=spd*PR118_FURY.speed;return PR118.base.furyShot.apply(this,args);}return PR118.base.furyShot.apply(this,arguments);};

/* ---- THUNDERHEAD (FURIOUS STAGE 6) ----
   Beams: the cannon's lip was painted after the beam and covered its start. Lip and coupling go first and the beam overlays
   the cannon, starting inside its mouth. Hit lanes are unchanged.
   Background attack: one giant tornado becomes a staggered volley of five. They stop growing at 160 px so a volley can be
   dodged. window.PR118_TH_OFF=1 restores one tornado. */
tc119Beams=function(b){for(const B of tm115State(b).beams){const f=B.recovery?22+Math.min(5,Math.floor(B.tail*24)):B.age<TM115.beamGrow?Math.min(5,Math.floor(B.age*24)):6+Math.floor((B.age-TM115.beamGrow)*24)%16,at=fb112PartPoint(b,B.part);
  if(B.part.hp>0)tc119Blit('pod'+B.part.index+'_lip',0,at.x,at.y);
  tc119Blit(B.recovery?'beam_coupling_tail':'beam_coupling',B.recovery?Math.min(5,Math.floor(B.tail*24)):Math.floor(B.age*24)%16,B.x,B.y);
  tm115Bank('wind_beam',f,B.x,B.y-(B.y-at.y)*.55);}};
const PR118_TH={lanes:[0,-130,130,-65,65],gap:.4,sizes:7};
if(TC119_ART.cycloneSizes.length>PR118_TH.sizes)TC119_ART.cycloneSizes.length=PR118_TH.sizes;
PR118.base.tcLaunch=tc119Launch;
tc119Launch=function(b){if(window.PR118_TH_OFF)return PR118.base.tcLaunch.apply(this,arguments);const C=b._tc119;C.pr118Aim={...C.aim};C.pr118Next=1;C.pr118At=efxClock+PR118_TH.gap;return PR118.base.tcLaunch.apply(this,arguments);};
function pr118ThDrain(){const b=boss,C=b?._tc119;if(!C?.pr118Aim||!C.pr118Next)return;if(b.dead||!C.flow){C.pr118Next=0;return;}
 while(C.pr118Next<PR118_TH.lanes.length&&efxClock>=C.pr118At){const keep=C.aim;C.aim={x:clamp(C.pr118Aim.x+PR118_TH.lanes[C.pr118Next],camLeftX()+60,camRightX()-60),y:C.pr118Aim.y};PR118.base.tcLaunch.call(null,b);C.aim=keep;C.pr118Next++;C.pr118At+=PR118_TH.gap;}
 if(C.pr118Next>=PR118_TH.lanes.length)C.pr118Next=0;}
PR118.base.playTh=updatePlay;
updatePlay=function(dt){const out=PR118.base.playTh.apply(this,arguments);if(state===GS.PLAY&&run.stage===6)pr118ThDrain();return out;};

/* ---- EVENT HORIZON (STAGE 9 MINIBOSS) ----
   Mike: shooting the spinning laser made it disappear. Traced: no gun touches those rounds. Damage that crossed 50% started the
   half-health phase, which erased the active beam and every round in flight. The phase now waits for the attack to finish, and
   rounds already fired keep flying. Bombs and reflectors no longer erase them either. */
PR118.base.ehRound=eh57Round;
eh57Round=function(){const q=PR118.base.ehRound.apply(this,arguments);if(q)q._s3kOriginalProof=true;return q;};
PR118.base.ehHalf=eh57Half;
eh57Half=function(b){const H=eh57State(b);if(['spiral','sweep','beam','spin'].includes(H.mode)&&H.phase==='fire'){H.pr118Half=true;return;}
 H.pr118Half=false;const keep=eBullets.filter(q=>q._eh57Owner===b&&!q.dead);for(const q of keep)q._eh57Owner=null;const out=PR118.base.ehHalf.apply(this,arguments);for(const q of keep)q._eh57Owner=b;return out;};
PR118.base.playEh=updatePlay;
updatePlay=function(dt){const out=PR118.base.playEh.apply(this,arguments);const b=subBoss,H=b?._eh57;if(H?.pr118Half&&!b.dead&&H.phase!=='fire')eh57Half(b);return out;};

/* ---- FORGE: NORMAL LASER PREVIEW ----
   The preview reuses one beam and never ages it, so the six-frame reel sat on frame 0. */
PR118.base.forgeTick=forgePreviewTick;
forgePreviewTick=function(P,VWp,VHp,dt){const out=PR118.base.forgeTick.apply(this,arguments);if(P?.bullets)for(const q of P.bullets)if(q.kind==='beam')q._visualAge=(q._visualAge||0)+(Number.isFinite(dt)?dt:1/60);return out;};

/* ---- DRACODIA CLAW WIND-UPS (DRONE AND FINAL FORM) ----
   Mike: compare to Stage 5. The arm now cocks back, whips and returns to guard on authored frames instead of only the warning lanes
   doing the telling. Display only: strike paths, contact, hitboxes and timers are untouched. Right arms are the left bank mirrored
   per cell. window.PR118_CLAW_OFF=1 restores the old draw. */
const PR118_CLAW={cell:320,cols:4,dir:'assets/game/levels/stage_08/boss/claw_anim_1109/',drone:[245,85],final:[235,70],draws:{}};
PR118_CLAW.keys=[];for(const n of ['drone','final'])for(const s of ['L','R'])for(const h of ['','_hit']){const k='pr118_'+n+'_'+s+h;XART._src[k]=PR118_CLAW.dir+n+'_'+s+h+'.webp';PR118_CLAW.keys.push(k);}
function pr118ClawBlit(kind,side,f,x,y,hit){const s=side==='left'?'L':'R',key='pr118_'+kind+'_'+s+(hit?'_hit':'');if(window.PR118_CLAW_OFF||!XART.rdy(key))return false;const C=PR118_CLAW.cell,P=PR118_CLAW[kind],px=side==='left'?P[0]:C-P[0];
 ctx.drawImage(XART.get(key),f%PR118_CLAW.cols*C,Math.floor(f/PR118_CLAW.cols)*C,C,C,Math.round(x-px),Math.round(y-P[1]),C,C);PR118_CLAW.draws[kind]=(PR118_CLAW.draws[kind]||0)+1;return true;}
PR118.base.clawKeys=v18Keys;
v18Keys=function(){return [...PR118.base.clawKeys.apply(this,arguments),...PR118_CLAW.keys];};
PR118.base.clawLoad=stageLoadBegin;
stageLoadBegin=function(n,keys){return PR118.base.clawLoad.call(this,n,n===8?[...(keys||[]),...PR118_CLAW.keys]:keys);};
/* host_whole_arms_1031 owns the drone's arm draw; the new frames replace only its 16 wind-up poses, so the authored strike and recovery stay. */
function pr118DroneFrame(P){const u=P.t-P.tell;if(u<0)return Math.min(3,Math.floor(clamp(P.t/P.tell,0,1)/.6*4));return u<.18?4+Math.min(2,Math.floor(u/.06)):-1;}
PR118.base.clawArm=rd96Blit;
rd96Blit=function(n,f,x,y,hit=false){const P=(n==='arm_left'||n==='arm_right')?rd96Physical(boss):null;if(P&&n==='arm_'+P.side){XART.rdy(RD96_ART[n].key);if(RD96_ART[n+'_hit'])XART.rdy(RD96_ART[n+'_hit'].key);const g=pr118DroneFrame(P);if(g>=0){const v=RD96_ART[n].poses[0],late=P.t>P.tell*.75,j=late?(Math.floor(efxClock*30)%2?1:-1):0;if(pr118ClawBlit('drone',P.side,g,x+v.root[0]+j,y+v.root[1],hit))return true;}}return PR118.base.clawArm.apply(this,arguments);};
function pr118FinalFrame(S,u){if(S.kind==='side-tell'||S.kind==='jump-tell')return Math.min(3,Math.floor(Math.min(1,u/.7)*4));if((S.kind==='side-rake'||S.kind==='jump-strike')&&u<.3)return 4+Math.min(2,Math.floor(u/.1));return -1;}
PR118.base.clawBlit=rd88Blit;
rd88Blit=function(a,b,hit=false){const P=rd88Act(b),S=P?.steps?.[P.step];if(S&&S.index!=null){const side=P.order[S.index],q=rd88Frame(b),f=q?.parts[side]===a?pr118FinalFrame(S,clamp(P.local/S.duration,0,1)):-1;if(f>=0){const J=q.joints[side].shoulder;if(pr118ClawBlit('final',side,f,b.x+J[0]-RD88_ART.pivot[0],b.y+J[1]-RD88_ART.pivot[1],hit))return;}}return PR118.base.clawBlit.apply(this,arguments);};

/* ---- CHRONOS FURIOUS COMBO JOINS ----
   Mike: the Stage 5 swings are janky. Each move of the combo began in an unrelated pose, so the hammer head teleported 110-280 px, and a
   takeoff frame stood in at the end. Existing whole-body frames, chosen for the smallest head travel, now bridge every gap. Display only:
   impacts, sweep windows and all hit positions keep their clocks, and each swing still reaches its final frame at its original hit time.
   window.PR118_JOIN_OFF=1 restores the old poses. */
const PR118_JOIN={spans:[[0,.22,[['retract',3],['retract',9]]],[.70,.86,[['retract',3],['left',1]]],[1.34,1.46,[['right',3],['windup',1]]],[1.90,2.18,[['left',3],['left',1],['retract',3],['retract',0]]]],wind:[.22,.46],left:.86,right:1.46};
PR118.base.joinPose=hf22FuriousPose;
hf22FuriousPose=function(b,P){if(window.PR118_JOIN_OFF||!c25Own(b))return PR118.base.joinPose.apply(this,arguments);const t=P.clock,T=HF22_FURIOUS_COMBO,k=P.scale||1,J=PR118_JOIN,row=(n,f)=>c27Pose(b,n,(f+.01)/16,k);let q=null;
 for(const [a,z,L]of J.spans)if(t>=a&&t<z){const e=L[Math.min(L.length-1,Math.floor((t-a)/(z-a)*L.length))];q=row(e[0],e[1]);break;}
 if(!q&&t>=J.wind[0]&&t<J.wind[1])q=c27Pose(b,'windup',(t-J.wind[0])/(J.wind[1]-J.wind[0]),k);
 if(!q&&t>=J.left&&t<T.left.hit)q=c27Pose(b,'left',(t-J.left)/(T.left.hit-J.left),k);
 if(!q&&t>=J.right&&t<T.right.hit)q=c27Pose(b,'right',(t-J.right)/(T.right.hit-J.right),k);
 return q||PR118.base.joinPose.apply(this,arguments);};

/* Hard runs the shorter double strike: same pull-back bridge, and the strike holds at impact so the following return starts from the pose it needs. */
PR118.base.joinPair=hf22PairPose;
hf22PairPose=function(b,P){if(window.PR118_JOIN_OFF||P.furiousMelee24||P.kind!=='blue'||P.difficulty==='furious'||!c25Own(b))return PR118.base.joinPair.apply(this,arguments);const t=P.clock,k=P.scale||1;let q=null;
 if(t<.30)q=c27Pose(b,'retract',((t<.15?3:9)+.01)/16,k);else if(t<.85)q=c27Pose(b,'windup',(t-.30)/.55,k);else if(t>=1.2)q=c27Pose(b,'strike',1,k);
 return q||PR118.base.joinPair.apply(this,arguments);};

/* ---- CHRONOS BALL FORM ----
   Mike: smaller, faster, and ordinary projectiles make it flash red and fire lasers back; missiles do not. Supersedes the 1025 no-ball-lasers
   rule. Red and white hit colours stay with the existing ball paint owner. window.PR118_BALL_OFF=1 restores the old ball. */
const PR118_BALL={scale:.45,speed:300,spin:6,radius:48,gap:{furious:.3,hard:.4},gapDefault:.55,fan:[-.22,0,.22],laser:5.2,lasers:0};
function pr118BallOn(b){return !window.PR118_BALL_OFF&&!!b&&c25Own(b)&&!b.dead&&['curl','ball','uncurl'].includes(b._hammer?.state);}
PR118.base.ballPose=ha21Blue;
ha21Blue=function(b){const q=PR118.base.ballPose.apply(this,arguments);if(q&&pr118BallOn(b)){const h=b._hammer,u=h.state==='ball'?1:h.state==='curl'?clamp(h.t/HAMMER_BALL_WARN,0,1):1-clamp(h.t/1.65,0,1);return{...q,k:q.k*lerp(1,PR118_BALL.scale,u*u*(3-2*u))};}return q;};
PR118.base.ballHit=bossHitTest;
bossHitTest=function(x,y){const r=PR118.base.ballHit.apply(this,arguments),b=boss;if(r&&pr118BallOn(b)&&b._hammer.state==='ball'&&Math.hypot(x-b.x,y-b.y)>PR118_BALL.radius)return false;return r;};
PR118.base.ballTick=hammerBossTick;
hammerBossTick=function(b,dt){if(pr118BallOn(b)&&b._hammer.state==='ball'){const h=b._hammer,v=Math.hypot(h.vx||0,h.vy||0)||1,k=PR118_BALL.speed/v;h.vx=(h.vx||150)*k;h.vy=(h.vy||165)*k;h.angle=(h.angle||0)+dt*PR118_BALL.spin;}return PR118.base.ballTick.apply(this,arguments);};
PR118.base.ballPaint=b20Image;
b20Image=function(a,x,y,k=1,rot=0,flash=0,pivot=a?.pivot){if(flash>0&&a&&pr118BallOn(boss)&&boss._hammer.state==='ball'&&!boss._hammer.c27BallMissile&&!a._c26&&XART.rdy(a.key)){const r=PR118.base.ballPaint.call(this,a,x,y,k,rot,0,pivot);ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.imageSmoothingEnabled=false;ctx.drawImage(xartTint(a.key,'#ff3030',1),-pivot[0]*k,-pivot[1]*k,a.w*k,a.h*k);ctx.restore();return r;}return PR118.base.ballPaint.apply(this,arguments);};
PR118.base.ballDamage=hammerBossDamage;
hammerBossDamage=function(b,dmg){const shot=_dmgBullet,out=PR118.base.ballDamage.apply(this,arguments);if(dmg>0&&pr118BallOn(b)&&b._hammer.state==='ball'){const h=b._hammer,missile=hammerMissile(shot);h.c27BallMissile=missile;
  if(efxClock>=(h.pr118BallFlash||0)){h.pr118BallFlash=efxClock+.14;b.flash=.06;}else if(b.flash>.06)b.flash=.06;
  if(!missile&&efxClock>=(h.pr118BallNext||0)){h.pr118BallNext=efxClock+(PR118_BALL.gap[diffKey]??PR118_BALL.gapDefault);const T=targetShip(b.x,b.y),a=Math.atan2(T.y-b.y,T.x-b.x);PR118_BALL.fan.forEach((o,i)=>{c26BallLaser(b.x+Math.cos(a+o)*PR118_BALL.radius,b.y+Math.sin(a+o)*PR118_BALL.radius,a+o,PR118_BALL.laser,i>0);PR118_BALL.lasers++;});}}return out;};

/* ---- ANIMATED TILES IN LEVEL INTRODUCTIONS ----
   Mike: "all animated tiles must animate during each levels introductions". The Stage 1 water, Stage 2
   lava, every LS112 material bed and the Stage 4 tesla take their frame from efxClock, and only efxTick
   advances it - in PLAY. Every intro drew them on one frozen frame. window.PR118_EFX_OFF=1 restores that. */
function pr118IntroClock(fn){return function(dt){if(!window.PR118_EFX_OFF&&dt>0)efxClock+=Math.min(dt,.1);return fn.apply(this,arguments);};}
drawIntro=pr118IntroClock(drawIntro);drawLaunch=pr118IntroClock(drawLaunch);drawL78Entry=pr118IntroClock(drawL78Entry);

/* ---- OFFSCREEN GROUND UNITS (Stage 5-8 slowdown, missing minibosses) ----
   Ground vehicles, pipes and turrets whose update branch skips the native bottom cull kept living
   thousands of pixels below the screen: one s7tank reached y=5551. They kept burning AI, collision and
   draw-loop time for the rest of the stage, and they counted toward the _sbLive<=9 miniboss crowd gate,
   so a level could never call its miniboss or boss. Anything that has been on screen and has since left
   it by more than the sweep margin is retired without kills, drops or score. */
const PR118_BELOW=260;
function pr118OffscreenSweep(){
 for(const e of enemies){if(e.dead||e._boss||e._amini||e._mini||e.boss)continue;
  if(e.y<VH+40&&e.y>viewTopY())e._pr118Seen=true;
  if(e._pr118Seen&&e.y>VH+PR118_BELOW){e.dead=true;e.hp=0;e.shoots=false;if(typeof groundTargetingCancel==='function')groundTargetingCancel(e);PR118.swept=(PR118.swept|0)+1;}}
}
const PR118_PLAY_A=updatePlay;
updatePlay=function(dt){const out=PR118_PLAY_A.apply(this,arguments);if(state===GS.PLAY)pr118OffscreenSweep();return out;};

/* ---- STAGE 4 LAST STAND ----
   The two core turrets stayed live and firing through the Storm Sovereign's final panic. Mike: remove them. */
function pr118Stage4Final(){const b=boss;if(run.stage!==4||!b?._p4Final||!Array.isArray(b._s4war?.coreTurrets))return;
 for(const t of b._s4war.coreTurrets)if(!t.dead||t.hp>0){if(Number.isFinite(t.x+t.y)&&typeof unitDeathFX==='function')unitDeathFX({x:t.x,y:t.y,w:t.w||40,h:t.h||40},'tank','red');t.dead=true;t.hp=0;pr118Log('s4-turret-removed');}
}
const PR118_PLAY_B=updatePlay;
updatePlay=function(dt){const out=PR118_PLAY_B.apply(this,arguments);if(state===GS.PLAY)pr118Stage4Final();return out;};

/* ---- STAGE 1 WARNING ORIGINS ----
   Flying drones and boat guns drew their cones from the hull's centre (measured offset 0-10 px), so the
   warning sat in the middle of the craft. Centred warnings now start at the nose, along the aimed line. */
const PR118_WARN=combatWarningDraw;
combatWarningDraw=function(owner,q){
 if(run.stage===1&&owner&&q&&!q.alertOnly&&/^s1boat(gun|patrol)$/.test(owner.type||'')&&Math.abs(q.x-owner.x)<=4&&Number.isFinite(q.ex+q.ey)){
  /* Mike: "he fires from the middle". A boat's rounds leave its two side guns, so its warning does too. */
  const M=(furyBoatModules(owner)||[]).filter(m=>m.hp>0);
  if(M.length){M.forEach((m,i)=>{const p=furyBoatPoint(owner,m),y=p.y+17;PR118_WARN.call(this,owner,{...q,x:p.x,y,ex:q.ex+p.x-q.x,ey:q.ey+y-q.y,width:(q.width||20)*.6,fieldOnly:q.fieldOnly||i>0});});return;}
 }
 if(run.stage===1&&owner&&q&&!q.alertOnly&&!owner._boss&&!owner._amini&&owner!==boss&&owner!==subBoss&&Number.isFinite(q.ex+q.ey)&&Number.isFinite(owner.x)){
  const oy=Number.isFinite(owner._drawY)?owner._drawY:owner.y,off=Math.hypot(q.x-owner.x,q.y-oy),L=Math.hypot(q.ex-q.x,q.ey-q.y);
  if(off<=12&&L>1){const r=Math.max(owner.w||0,owner.h||0)*.46;return PR118_WARN.call(this,owner,{...q,x:owner.x+(q.ex-q.x)/L*r,y:oy+(q.ey-q.y)/L*r});}
 }
 return PR118_WARN.apply(this,arguments);
};

/* Stage 1's delta jets opened fire with no warning. Each nose gun now shows a cone for the 0.6 s before a burst. */
const PR118_JET_TELL=.6;PR118.base.drawBulletsJet=drawBullets;
drawBullets=function(){if(run.stage===1&&state===GS.PLAY)for(const e of enemies){
  if(e.dead||e._dyingT!=null||!/^s1jetdelta/.test(e.type||'')||e._atk!=='mg'||e._furyMove||e._burst>0||!(e._burstCd>0&&e._burstCd<=PR118_JET_TELL))continue;
  const T=targetShip(e.x,e.y);if(!(T.y>e.y+8&&Math.abs(T.x-e.x)<150))continue;
  const nx=(e.w||60)*JET_GUN_OFF,ny=e.y+(e.h||60)*.44,a=e._s1Elite?s1JetAim(e,e.x,ny,4.6):Math.PI/2;
  [-1,1].forEach((d,i)=>{const x=e.x+d*nx;combatWarningDraw(e,{x,y:ny,ex:x+Math.cos(a)*700,ey:ny+Math.sin(a)*700,progress:1-e._burstCd/PR118_JET_TELL,width:18,fieldOnly:i>0});});}
 return PR118.base.drawBulletsJet.apply(this,arguments);};

/* ---- STAGE 1 GROUND TRAFFIC ON WATER ----
   Tank files were placed by lane fraction with no terrain test, then rode the scroll on whatever was
   underneath: sampled on water, the dam face and the reservoir. Before a unit comes into view it moves to the
   nearest drivable lane on its row. If there is none, or it ends up illegal on screen, it is retired
   without a kill or a reward. */
function pr118GroundLegal(e){const sy=levelSrcY()+e.y,F=groundTrafficFootprint(e),h=F.w*.35;return tankDrivable(e.x,sy,false)&&tankDrivable(e.x-h,sy,false)&&tankDrivable(e.x+h,sy,false);}
function pr118GroundSweep(dt){if(run.stage!==1||bossDefeated)return;const top=viewTopY();
 for(const e of enemies){if(e.dead||e._dyingT!=null||!groundTrafficVehicle(e)||e._boss||e._amini)continue;
  if(e.y<top-140)continue;
  if(pr118GroundLegal(e)){e._pr118Bad=0;continue;}
  if(e.y<top+6){let moved=false;const x0=e.x;for(let d=20;d<=320&&!moved;d+=20)for(const s of[-1,1]){e.x=x0+s*d;if(e.x>40&&e.x<worldWidth()-40&&pr118GroundLegal(e)){moved=true;break;}}
   if(moved){pr118Log('ground-relane',{type:e.type,from:x0|0,to:e.x|0});continue;}e.x=x0;e.dead=true;e.hp=0;pr118Log('ground-removed',{type:e.type});continue;}
  e._pr118Bad=(e._pr118Bad||0)+dt;
  if(e._pr118Bad>.35){e.dead=true;e.hp=0;e.shoots=false;if(typeof groundTargetingCancel==='function')groundTargetingCancel(e);if(typeof unitDeathFX==='function')unitDeathFX(e,'tank','red');pr118Log('ground-retired',{type:e.type,x:e.x|0,y:e.y|0});}
 }
}
const PR118_PLAY_C=updatePlay;
updatePlay=function(dt){const out=PR118_PLAY_C.apply(this,arguments);if(state===GS.PLAY)pr118GroundSweep(dt);return out;};

/* ---- FURIOUS SUMPJAW: GUNS MUST CONNECT ----
   Damage only registered inside small moving ellipses (gills 15x20, heart 17) so ordinary rounds went through
   the body and only Retina-locked missiles reliably connected: 7% of 14000 HP in 220 s of gun-only play.
   A round that strikes the body now lands on the pool that is currently open: gills first, then the heart. */
const PR118_SJ_AT=sj98At,PR118_SJ_BEAM=sj98Beam,PR118_SJ_R=62;
function pr118SjPool(a){return a.pools.find(p=>p.hp>0&&p.id!=='heart')||(sj98State(a)===3?a.pools.find(p=>p.hp>0&&p.id==='heart'):null);}
sj98At=function(b,x,y,pad=0){const hit=PR118_SJ_AT.apply(this,arguments);if(hit||!sj98Own(b)||b.dead)return hit;let best=null,dist=PR118_SJ_R+pad;
 for(const a of b._sj98.actors){if(a.dead||!sj98Foreground(a))continue;const p=pr118SjPool(a);if(!p)continue;const q=sj98Socket(a,'heart'),d=Math.hypot(x-q.x,y-q.y);if(d<dist){dist=d;best={a,p};}}return best;};
sj98Beam=function(b,beam){const hit=PR118_SJ_BEAM.apply(this,arguments);if(hit)return hit;const range=playerBeamRange(beam);if(!range)return null;let best=null;
 for(const a of b._sj98.actors){if(a.dead||!sj98Foreground(a))continue;const p=pr118SjPool(a);if(!p)continue;const q=sj98Socket(a,'heart');
  if(q.y+PR118_SJ_R<range.top||q.y-PR118_SJ_R>range.bot||Math.abs(q.x-range.x)>PR118_SJ_R+range.half)continue;const y=Math.min(range.bot,q.y+PR118_SJ_R-1);if(!best||y>best.entry)best={x:q.x,y,entry:y,key:'sump'+a.i+'-'+p.id};}
 return best;};

/* ---- WARP-OUT AFTER GATE EIGHT ----
   Passing the last gate drew a portal and then three seconds of full-screen swirling vortex. Mike wants no
   swirl after the gates: the jump is now the native streaked warp-drive frame climbing into the white. */
function pr118WarpStreaks(t,c){const cx=VW/2,cy=VH*.46,maxR=Math.hypot(VW,VH)*.62;ctx.save();ctx.fillStyle='rgba(2,4,18,'+(.45+.5*c).toFixed(3)+')';ctx.fillRect(0,0,VW,VH);ctx.lineCap='butt';
 for(let i=0;i<120;i++){const a=i*2.39996,speed=.7+((i*37)%50)/50,u=((t*speed*(1+2.4*c)+i*.137)%1),r=18+u*u*maxR,len=(14+150*c)*(.3+u);
  ctx.strokeStyle=i%5===0?'#9fe8ff':i%3===0?'#dff6ff':'#ffffff';ctx.globalAlpha=Math.min(1,.3+u);ctx.lineWidth=i%7===0?3:2;ctx.beginPath();ctx.moveTo(cx+Math.cos(a)*r,cy+Math.sin(a)*r);ctx.lineTo(cx+Math.cos(a)*(r+len),cy+Math.sin(a)*(r+len));ctx.stroke();}
 ctx.restore();}
s9WarpTick=S5924.base.warpTick;
s9WarpDraw=function(){const W=s9warp;if(!W)return;s5924HideWarp();
 if(W.ph==='draw'){const t=W.t,c=clamp(t/S9W_DRAW,0,1);pr118WarpStreaks(t,c);
  const white=clamp((t-(S9W_DRAW-.30))/.30,0,1);if(white>0){ctx.save();ctx.fillStyle='rgba(255,255,255,'+white.toFixed(3)+')';ctx.fillRect(0,0,VW,VH);ctx.restore();}
 }else{ctx.save();ctx.fillStyle='#ffffff';ctx.fillRect(0,0,VW,VH);ctx.restore();}};

/* ---- STAGE 6/8 SPRITE CELL CACHE (slowdown) ----
   Profiled on Furious: Stage 8 spent about a third of CPU drawing cells straight from giant sheets, with frames at
   68 ms median and 292 ms peaks as the decoded sheets were evicted and re-decoded. Each cell is copied once, pixel for
   pixel, into its own small canvas, the same approach Stage 5 and 7 already use. Stage 7's cache was too small
   for its roster: its churn also forced the projectile layer to re-read pixels every frame. */
S7P113.budget=192*1024*1024;
const PR118_CELLS={map:new Map(),bytes:0,budget:256*1024*1024,draws:0,misses:0};
const PR118_V31=v31Blit;
v31Blit=function(B,f,a,x,y,size,tint=null,alpha=1){
 if(window.PR118_CELL_OFF||![6,8].includes(run.stage)||!B)return PR118_V31.apply(this,arguments);
 if(!XART.rdy(B.key))return false;
 const c=B.cell,d=v31Dir(a,B.dirs),cols=B.cols||B.dirs,col=d%cols,row=clamp(f|0,0,B.frames-1)*(B.dirRows||1)+Math.floor(d/cols),id=B.key+':'+col+':'+row+':'+(tint||''),M=PR118_CELLS;
 let im=M.map.get(id);
 if(im){M.map.delete(id);M.map.set(id,im);}
 else{im=document.createElement('canvas');im.width=im.height=c;const g=im.getContext('2d');g.imageSmoothingEnabled=false;
  g.drawImage(tint?xartTint(B.key,tint,1):XART.get(B.key),col*c,row*c,c,c,0,0,c,c);M.map.set(id,im);M.bytes+=c*c*4;M.misses++;
  while(M.bytes>M.budget&&M.map.size>1){const [k,old]=M.map.entries().next().value;M.map.delete(k);M.bytes-=old.width*old.height*4;}}
 ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(im,0,0,c,c,x-size/2,y-size/2,size,size);ctx.restore();M.draws++;return true;
};
const PR118_BEGIN_B=beginStage;
beginStage=function(){PR118_CELLS.map.clear();PR118_CELLS.bytes=0;return PR118_BEGIN_B.apply(this,arguments);};
