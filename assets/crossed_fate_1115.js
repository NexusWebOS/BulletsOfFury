"use strict";
/* Stage6 routes keep their native combat/results owners. This layer records
   the terminal opponent, directs the map aftermath and extends the award bank. */
const FATE15={base:{create:fb112Create,defeat:achievementEncounterDefeat,begin:beginStage,
 leave:scLeaveStage,rows:c16Rows,open:openStageSelect,wing:s6WingTick,wingDraw:s6WingDraw,
 choice:s6WingChoiceDraw,say:s6WingSay,world:drawWorld,powerups:drawPowerups,
 mapDraw:Rival24.mapDraw,mapInput:Rival24.mapInput,mapBack:Rival24.mapBack,
 camera:cmap2CameraTick,save:Rival24.save,load:Rival24.load,toast:achToastTick,
 state:setState,menuBack:menuBackTick,brief:mapgBriefingDraw},last:null,events:[],toast:null};
for(const B of Object.values(FATE15_ART.banks))for(const p of B.pages)XART._src[p.key]=p.path+'?v='+p.sha256.slice(0,12);
for(const a of Object.values(FATE15_ART.icons))XART._src[a.key]=a.path+'?v='+a.sha256.slice(0,12);
const FATE15_MESSAGES={storm:'Play Stage 6 via password STRM on hard to face the harrier!',rebels:'You let the storm cannon get away! use password STRM on furious for a second chance at redemption!'};
const FATE15_NAMES={storm:'Storm Cannon',harrier:'Harrier',rebels:'Rough Riders'};
function fate15SkyReport(q){const down=q.defeated==='rebels'?'The Rough Riders are down.':FATE15_NAMES[q.defeated]+' is down.',incoming=q.target==='rebels'?'The Rough Riders are still heading for the city.':'The Harrier is still heading for the city.';return down+' '+incoming;}
const fate15Ease=v=>{v=clamp(v,0,1);return v*v*(3-2*v);};
function fate15Log(event,data={}){FATE15.events.push({event,...data});if(FATE15.events.length>256)FATE15.events.shift();}
function fate15Kind(b){return b?._fb112?.model==='thunder'||b?.kind==='thunderhead'?'storm':b?._rebels||b?.kind==='rebelsquad'?'rebels':b?._whv||b?.kind==='warhive'?'harrier':null;}
function fate15Outcome(defeated,difficulty=diffKey){const furious=difficulty==='furious',target=defeated==='rebels'?'harrier':'rebels';return{
 defeated,difficulty,target,route:target==='harrier'?'left':'right',furious,
 crash:furious&&defeated==='storm',escape:furious&&defeated==='rebels',
 award:furious&&defeated==='storm'?'crossed_fate':furious&&defeated==='rebels'?'road_not_taken':null,
 message:furious?FATE15_MESSAGES[defeated]||'':''};}
function fate15Current(route=s113Route()){
 const v=run._stage6FateDefeat;if(v&&v.difficulty===diffKey)return fate15Outcome(v.defeated,v.difficulty);
 const r=campaign.stage6Fate;if(r?.version===1&&r.difficulty===diffKey)return fate15Outcome(r.defeated,r.difficulty);
 return fate15Outcome(route==='right'?'rebels':diffKey==='furious'?'storm':'harrier');
}
function fate15Receipt(v){if(!v||v.version!==1||!['storm','harrier','rebels'].includes(v.defeated)||!DIFF_ORDER.includes(v.difficulty)||typeof v.id!=='string')return null;
 const q=fate15Outcome(v.defeated,v.difficulty);return {...q,version:1,id:v.id.slice(0,96),verified:v.verified===true,pilot:PILOTS.some(p=>p.key===v.pilot)?v.pilot:'cole',
 crew:Array.isArray(v.crew)?[...new Set(v.crew.filter(k=>PILOTS.some(p=>p.key===k)))].slice(0,5):['cole'],
 elapsed:clamp(Number(v.elapsed)||0,0,60),transitSeen:!!v.transitSeen,messageSeen:!!v.messageSeen,awardNotified:!!v.awardNotified};}
function fate15Keys(){return [...new Set([...Object.values(FATE15_ART.banks).flatMap(b=>b.pages.map(p=>p.key)),...Object.values(FATE15_ART.icons).map(a=>a.key),
 'mapg_briefing','statpanel_full_0916',MW21_ART.m.key,...Array.from({length:8},(_,i)=>'cinfx_airburst_'+i),...Array.from({length:8},(_,i)=>'nxp_smoke_'+i),...Array.from({length:6},(_,i)=>'ndk_scorch_'+i),
 ...PILOTS.flatMap(p=>['ship_'+p.key,'ship_'+p.key+'_g1','ship_'+p.key+'_g2'])])];}
function fate15Warm(){return fate15Keys().map(k=>XART.rdy(k)).every(Boolean);}
function fate15Blit(name,frame,x,y,width,alpha=1){const B=FATE15_ART.banks[name];if(!B)return false;const f=clamp(Math.floor(frame),0,B.frames-1),c=B.cells[f];if(!XART.rdy(c[0]))return false;
 const k=width/B.bodyWidth;ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(c[0]),c[1],c[2],B.w,B.h,x-B.pivot[0]*k,y-B.pivot[1]*k,B.w*k,B.h*k);ctx.restore();return true;}
const fate15Load=stageLoadBegin;stageLoadBegin=function(n,keys){if(n===6)Snd.prepare(['jetDash','expSmall','expBig','blip','enemyMachineGunLight']);return fate15Load.call(this,n,n===6?[...(keys||[]),...fate15Keys()]:keys);};
fb112Create=function(model,sub){const b=FATE15.base.create.apply(this,arguments);if(model==='thunder'&&!sub){b.name='STORM CANNON';b._stage6FateKind='storm';}return b;};
achievementEncounterDefeat=function(b,role){const fresh=b&&!b._achievementAwarded,kind=fate15Kind(b),r=FATE15.base.defeat.apply(this,arguments);
 if(fresh&&run.stage===6&&!run._gp4StageX&&role==='boss'&&kind&&b.hp<=0){run._stage6FateDefeat={defeated:kind,difficulty:diffKey,verified:true};fate15Log('native-defeat',{kind,difficulty:diffKey});}return r;};
beginStage=function(n){if(n===6)delete run._stage6FateDefeat;return FATE15.base.begin.apply(this,arguments);};

/* Native route text and the two passing aircraft use the existing split clock. */
const fate15RouteScript=BOFCinematicDirector.routeScript;
BOFCinematicDirector.routeScript=function(side,p=run.pilot){const rows=fate15RouteScript.apply(this,arguments);if(side!=='left'||diffKey!=='furious'||run._gp4StageX)return rows;
 const text=['The Storm Cannon is breaking left. Its batteries are still active. The Harrier is heading for the city.',
  'I am taking Storm Cannon. Keep the Harrier and the Rough Riders on radar.',
  'We will mark the surviving contacts at the city. Choose two wingmen if you pursue them.',
  'Fury Fighters, split formation. Left wing, on me.'];return rows.map((b,i)=>({...b,text:text[i]||b.text}));};
s6WingSay=function(who,line){if(run.stage===6&&diffKey==='furious'&&!run._gp4StageX){if(line==='HARRIER BREAKING LEFT. CONTACTS COMING THROUGH!')line='HARRIER HEADING FOR THE CITY! STORM CANNON BREAKING LEFT!';
 if(line==='FIVE-SHIP WING, TAKE THE HARRIER TOGETHER!')line='FIVE-SHIP WING, TAKE THE STORM CANNON TOGETHER!';}return FATE15.base.say.call(this,who,line);};
s6WingChoiceDraw=function(){if(run.stage!==6||run._gp4StageX)return FATE15.base.choice.apply(this,arguments);const W=s6Wing;if(!W?.choice||W.route||BOFCinematicDirector.live)return;
 const C=W.frChoice||{side:'left'},furious=diffKey==='furious',x=12,y=VH*.30,w=VW-24;
 ctx.save();worldXformEscape();ctx.fillStyle='rgba(0,3,12,.72)';ctx.fillRect(0,0,VW,VH);const panel=mw21Window('m',x,y,w,200);
 if(panel){ui20Text(ctx,'CHOOSE YOUR PURSUIT',VW/2,y+25,17,w-70,'center','#fff0b0');
  fate15Blit(furious?'storm_nw':'harrier_north',0,VW*.28,VH*.42,50);
  for(let i=0;i<REBEL_SHIPS.length;i++){const key='rr_ship_'+REBEL_SHIPS[i];if(!XART.rdy(key))continue;const im=XART.get(key),h=17;ctx.drawImage(im,VW*.72+(i-2)*14-h*im.width/im.height/2,VH*.40+Math.abs(i-2)*4,h*im.width/im.height,h);}
  for(const [side,cx,label]of [['left',VW*.28,furious?'STORM CANNON':'HARRIER'],['right',VW*.72,'ROUGH RIDERS']]){const selected=C.side===side;ui20Text(ctx,label,cx,VH*.49,14,VW*.38,'center',selected?'#fff4b7':'#b0c8de');ui20Text(ctx,side.toUpperCase(),cx,VH*.54,11,VW*.38,'center','#83dbff');if(selected)drawSelArrow(cx-VW*.195,VH*.49,16,false,'g');}
  controlHintRow([['pad_dpad','CHOOSE'],['pad_a','CONFIRM']],VH*.615,VW/2,VW*.8,20);}
 ctx.restore();FATE15.lastChoice={left:furious?'STORM CANNON':'HARRIER',right:'ROUGH RIDERS',selected:C.side};};
function fate15Pass(){const W=s6Wing;if(run.stage!==6||diffKey!=='furious'||run._gp4StageX||!W?.fake)return [];
 const t=W.fake.t/1.35,frames=Math.floor(t*18)%16,out=[];
 for(const [name,start,dur,size]of [['harrier_nw',0,1.55,1.35],['storm_nw',.72,2.15,1.15]]){const u=(t-start)/dur;if(u<0||u>=1)continue;const e=.32*u+.68*u*u,w=viewW()*size;
  out.push({name,frame:name==='harrier_nw'?0:frames,u,x:lerp(camRightX()+w*.65,camLeftX()-w*.7,e),y:lerp(VH+w*.45,viewTopY()-w*.7,e),w});}return out;}
s6WingTick=function(dt){const f=s6Wing?.fake;if(run.stage===6&&diffKey==='furious'&&!run._gp4StageX&&f)f.t+=Math.max(0,dt)*.35;
 const r=FATE15.base.wing.apply(this,arguments),W=s6Wing;if(run.stage===6&&diffKey==='furious'&&W?.fake&&!run._gp4StageX){
  W.fake._fateCues??=new Set();for(const[name,at]of [['harrier',.04],['storm',.76]])if(W.fake.t/1.35>=at&&!W.fake._fateCues.has(name)){W.fake._fateCues.add(name);Snd.play('jetDash');fate15Log('overflight',{name});}}
 return r;};
s6WingDraw=function(){if(!fate15Pass().length&&!s6Wing?.fake)return FATE15.base.wingDraw.apply(this,arguments);
 if(run.stage!==6||diffKey!=='furious'||run._gp4StageX)return FATE15.base.wingDraw.apply(this,arguments);
 const ready=XART.rdy;XART.rdy=function(k){return k==='whv_closed'?false:ready.apply(this,arguments);};try{return FATE15.base.wingDraw.apply(this,arguments);}finally{XART.rdy=ready;}};
drawPowerups=function(){const r=FATE15.base.powerups.apply(this,arguments);for(const p of fate15Pass())fate15Blit(p.name+'_shadow',p.frame,p.x+22,p.y+64,p.w*.94);return r;};
drawWorld=function(){const r=FATE15.base.world.apply(this,arguments),passes=fate15Pass();if(!passes.length)return r;
 ctx.save();try{const z=viewZoom();if(z!==1){ctx.scale(z,z);ctx.translate(0,VH*(1-z)/z);}if(worldWidth()>viewW())ctx.translate(-camX,0);
  // The score and five-panel HUD live above/below the playfield now. Use the
  // full native world window; only real in-field dialogue apertures cut holes.
  ctx.beginPath();ctx.rect(camLeftX(),0,viewW(),VH);for(const p of RR66.panels||[])ctx.rect(camLeftX()+p.x,p.y,p.w,p.h);ctx.clip('evenodd');
  for(const p of passes)fate15Blit(p.name,p.frame,p.x,p.y,p.w);
 }finally{ctx.restore();}FATE15.last={kind:'overflight',passes};return r;};

/* Post6 stays in the current cockpit/comic renderer. No vanished-order plot. */
c16Rows=function(id,p=run.pilot,route=s113Route()){const rows=FATE15.base.rows.apply(this,arguments);if(id!=='post-6'||run._gp4StageX)return rows;
 const q=fate15Current(route),name=c16Name(p),left=q.crash?'the Harrier and the Rough Riders':'the '+FATE15_NAMES[q.target],tech=d1110Tech(p).toUpperCase();
 const lines={B601:[tech,name+', looks like we toned down the chaos, but we still have '+left+' heading to the city.'],
 'POST6-02':['COLE','Good work, Fury Fighters. The skies are clearing. Keep those contacts in sight.'],
 'POST6-03':['FREEZER','Still on your wing. We are ready when you are.'],
 'POST6-04':[tech,q.escape?'The Storm Cannon is breaking away to the west. The Harrier is still heading for the city.':q.crash?'Storm Cannon is down. The Harrier is moving fast, and the Rough Riders are closing on the city too.':fate15SkyReport(q)],
 'POST6-05':[p.toUpperCase(),'Mark the city contact. What else is on the radar?'],
 'POST6-06':[tech,'A high-level threat under the city. Close to the riverbank. Let me narrow it down.'],
 'POST6-07':['YURI','An underground contact? Mark that too.'],
 'POST6-08':[tech,'The drains by the riverbank. I have both routes marked.'],
 'POST6-09':[p.toUpperCase(),'Keep the city contact marked. We will choose our next move once everyone is clear.'],
 'POST6-10':[tech,'We can pursue the city contacts or check underground. Recheck your gear first.'],
 'POST6-11':[p.toUpperCase(),'Fury Fighters, regroup. We will choose our next move together.']};
 for(const b of rows){const v=lines[b.id];if(!v)continue;b.who=v[0];b.text=v[1];b.people=[...new Set([b.who.toLowerCase(),p,tech.toLowerCase()])].filter(k=>PILOTS.some(v=>v.key===k)).slice(0,2);
  if(b.people.length<2)b.people.push(b.people[0]==='cole'?'decker':'cole');b.duration=Math.max(3,b.text.length*.055+1.15);b.speechEnd=b.text.length*.055+.12;
  if(b.id==='POST6-11'){b.kind='dialogue';b.bank=null;b.location='sky';b.layout='duo';b.page=0;}
  if(b.cm3)b.cm3.baseDuration=b.duration;for(const person of b.people){b.fpLocations??={};b.fpLocations[person]='cockpit-sky';}}
 return rows;};
C16.rows=CM3.rows=FP5.rows=c16Rows;

/* A single receipt accompanies native result settlement and the saved city. */
scLeaveStage=function(R){if(run.stage===6&&!run._gp4StageX&&!P2M.active&&!R?._beta24Settled&&!R?._s113Leaving){
 const v=run._stage6FateDefeat,kind=v?.defeated||fate15Kind(boss);if(kind){const q=fate15Outcome(kind,v?.difficulty||diffKey),crew=[...new Set([run.pilot,...(coopActive()?[p2Pilot().key]:[]),...gp4Allies()])].slice(0,5);
  campaign.stage6Fate=fate15Receipt({...q,version:1,id:'stage6-'+Date.now()+'-'+kind,verified:v?.verified===true,pilot:run.pilot,crew,elapsed:0});FATE15.toast=null;
  campaign.stageX1004={route:q.route,target:q.target,defeated:kind,difficulty:q.difficulty,done:false};campaign.rivalScattered=false;
  fate15Log('result-routed',{defeated:kind,target:q.target,verified:campaign.stage6Fate.verified});}}
 return FATE15.base.leave.apply(this,arguments);};
Rival24.save=function(){return {...FATE15.base.save(),stage6Fate:campaign.stage6Fate?{...campaign.stage6Fate,crew:campaign.stage6Fate.crew.slice()}:null};};
Rival24.load=function(v){const r=FATE15.base.load.apply(this,arguments);campaign.stage6Fate=fate15Receipt(v?.stage6Fate);FATE15.toast=null;return r;};
function fate15MotionEnd(r){return r.crash?8.4:4.8;}
function fate15Motion(){const r=campaign.stage6Fate;return state===GS.STAGESEL&&r&&!r.transitSeen;}
function fate15MapOpen(){const r=campaign.stage6Fate;if(!r||r.messageSeen&&(!r.award||r.awardNotified))return;
 CF4.focus=false;MAP4E.xPreview=false;cmap2.focus='map';MAP4E.focus=false;CF4.flight=3.3;FATE15.cameraReleased=false;FATE15.mapCursor=sselCursor;fate15Warm();}
openStageSelect=function(){const r=FATE15.base.open.apply(this,arguments);FATE15.cameraReleased=true;if(campaign.stage6Fate)fate15MapOpen();return r;};
const fate15Flying=Object.getOwnPropertyDescriptor(Rival24,'flying').get;
Object.defineProperty(Rival24,'flying',{get(){return !!fate15Motion()||fate15Flying.call(Rival24);}});
cmap2CameraTick=function(dt,cine,selected){const r=campaign.stage6Fate;
 if(!r||sselBoot>0)return FATE15.base.camera.apply(this,arguments);
 if(!r.transitSeen||sselUnlockCine){FATE15.mapCursor=sselCursor;if(!r.transitSeen){CF4.focus=false;MAP4E.xPreview=false;}}
 else if(sselCursor!==FATE15.mapCursor||CF4.focus||MAP4E.xPreview)FATE15.cameraReleased=true;
 if(!fate15Motion()&&FATE15.cameraReleased)return FATE15.base.camera.apply(this,arguments);
 map4eWarm();const t=fate15Motion()?(r.escape?map30Overview():cmap2Frame(6,'hub')):cmap2Frame(7,'hub'),k=1-Math.exp(-Math.max(0,dt)*2.6);for(const p of ['x','y','z'])cmap2.cam[p]+=(t[p]-cmap2.cam[p])*k;};
Rival24.mapInput=function(){return fate15Motion()?true:FATE15.base.mapInput.apply(this,arguments);};
Rival24.mapBack=function(){return fate15Motion()?true:FATE15.base.mapBack.apply(this,arguments);};
menuBackTick=function(){if(fate15Motion()){Input.menuBack();return false;}return FATE15.base.menuBack.apply(this,arguments);};
const fate15MapPilot=sselShipDraw;sselShipDraw=function(){if(!fate15Motion())return fate15MapPilot.apply(this,arguments);};
setState=function(next){if(state===GS.STAGESEL&&next!==GS.STAGESEL&&campaign.stage6Fate)fate15Persist();return FATE15.base.state.apply(this,arguments);};
function fate15Persist(){if(state!==GS.STAGESEL)return;campSuspend();
 // Keep the native completed-stage checkpoint's stock/rank/next-stage fields.
 // Only add map-story progress to that existing autosave; explicit slots stay native.
 try{const s=campReadAuto();if(s?.v===CAMP_SAVE_VER&&s.rank?.[6]){s.rival24=Rival24.save();localStorage.setItem(CAMP_AUTO_KEY,JSON.stringify(s));}}catch(_){}
}
function fate15MapPoint(){const h=map4eHubPose();return cmap2ToScreen(h.x,h.y+30);}
cf4Hub=fate15MapPoint;
function fate15MapEffects(r,t,h){if(t<2.7)return;const age=t-2.7,z=Math.max(.5,Math.min(1.3,cmap2.cam.z/.31));
 for(let i=0;i<5;i++){const x=h.x+Math.sin(i*3.1)*49*z,y=h.y+Math.cos(i*2.4)*27*z,key='ndk_scorch_'+i;
  if(age>i*.26&&XART.rdy(key)){const im=XART.get(key);ctx.drawImage(im,x-11*z,y-7*z,22*z,14*z);}
  const a=age-i*.27;if(a>=0&&a<.6)cinFx('airburst',x,y,44*z,a);
  if(a>.3&&XART.rdy('nxp_smoke_'+(Math.floor(t*8+i)%8))){const im=XART.get('nxp_smoke_'+(Math.floor(t*8+i)%8)),s=27*z;ctx.save();ctx.globalAlpha=.65;ctx.drawImage(im,x-s/2,y-s,s,s);ctx.restore();}}
}
function fate15MapShips(r,t){const o=sselFlagScreenXY(6),h=fate15MapPoint(),k=fate15Ease(t/4.1),z=Math.max(.55,Math.min(1.2,cmap2.cam.z/.31));if(!o||!h)return;
 const ships=[];
 for(const [i,pk]of r.crew.entries()){const delay=i*.12,u=fate15Ease((t-delay)/4.1),x=lerp(o.x+(i-2)*8,h.x+(i-2)*23*z,u),y=lerp(o.y,h.y+45*z+Math.abs(i-2)*8*z,u)-Math.sin(u*Math.PI)*18;
  if(t<8.4){pt11OpeningShip(pk,t,x,y,26*z,.85);ships.push({pilot:pk,x,y});}
  if(r.crash&&t>3.4&&t<5.2){const a=(t-3.4+i*.1)%.32,p=a/.32;drawMfx('mgcf_1_5',lerp(x,h.x,p),lerp(y,h.y-12*z,p),0,8);}}
 if(r.crash||r.target==='harrier'){let x=lerp(o.x,h.x,k),y=lerp(o.y-34,h.y-18*z,k)-Math.sin(k*Math.PI)*22;
  if(r.crash&&t>=5.2){const age=t-5.2,u=clamp(age/2.5,0,1);x+=Math.sin(u*Math.PI)*42*z;y+=u*u*74*z;
   if(age<2.5){fate15Blit('harrier_crash',u*47,x,y,76*z);if(XART.rdy('nxp_smoke_'+(Math.floor(t*10)%8))){const im=XART.get('nxp_smoke_'+(Math.floor(t*10)%8));ctx.drawImage(im,x-22*z,y-40*z,44*z,44*z);}}
   if(age<.6)cinFx('airburst',x,y,75*z,age);if(age>=2.5&&age<3.1)cinFx('airburst',x,y,120*z,age-2.5);
   ships.push({kind:'harrier',x,y,crashing:true,age});
  }else{fate15Blit('harrier_north_shadow',0,x+6*z,y+9*z,74*z);fate15Blit('harrier_north',0,x,y,74*z);ships.push({kind:'harrier',x,y});}}
 if(r.target==='rebels')for(let i=0;i<REBEL_SHIPS.length;i++){const key='rr_ship_'+REBEL_SHIPS[i];if(!XART.rdy(key))continue;const im=XART.get(key),u=fate15Ease((t-.4-i*.1)/3.7),x=lerp(o.x+(i-2)*6,h.x+(i-2)*22*z,u),y=lerp(o.y+10,h.y-42*z+Math.abs(i-2)*8*z,u),s=24*z;ctx.drawImage(im,x-s*im.width/im.height/2,y-s/2,s*im.width/im.height,s);ships.push({kind:'rebel',pilot:REBEL_SHIPS[i],x,y});}
 if(r.escape){const u=clamp(t/3.8,0,1),x=lerp(o.x,-campaignViewOffset()-140,fate15Ease(u)),y=o.y-Math.sin(u*Math.PI)*38;
  if(u<1){fate15Blit('storm_w_shadow',Math.floor(t*18)%16,x+8,y+12,86*z);fate15Blit('storm_w',Math.floor(t*18)%16,x,y,86*z);ships.push({kind:'storm',x,y,escapedWest:u>.95});}}
 FATE15.last={kind:'map',time:t,defeated:r.defeated,target:r.target,ships,city:h};
}
function fate15Message(r){if(!r.message||r.messageSeen)return;const at=fate15MotionEnd(r),age=r.elapsed-at;if(age<0)return;const reveal=r.message.length/34,life=reveal+3.5+.65;
 if(age>=life){r.messageSeen=true;fate15Persist();return;}
 const a=age>life-.65?(life-age)/.65:Math.min(1,age/.2);ctx.save();ctx.globalAlpha*=a;const b=MAPG.rect,prior=_msgFace,count=Math.max(0,Math.floor(age*34));
 if(XART.rdy('mapg_briefing')){ctx.drawImage(XART.get('mapg_briefing'),...MAPG.panelSource,b.x,b.y,b.w,b.h);msgFaceUse('game');
  msgDrawBlock({text:'ALTERNATE ROUTE',budget:999,x:b.x+18,y:b.y+12,w:b.w-36,h:29,maxH:15,minH:10,color:'#ffe7a0',align:'center',stableCenter:true,valign:'middle',lineMul:1.15});msgFaceUse('dialogue');
  msgDrawBlock({text:r.message,budget:count,x:b.x+22,y:b.y+47,w:b.w-44,h:35,maxH:11,minH:9,lineMul:1.3,color:'#eef6ff',outline:false,align:'center',stableCenter:true,valign:'middle'});}
 msgFaceUse(prior);if(count<r.message.length&&count!==FATE15.messageCount&&count%3===0)Snd.play('blip');FATE15.messageCount=count;
 ctx.restore();FATE15.lastMessage={text:r.message,shown:Math.floor(age*34),alpha:a};
}
function fate15AwardDraw(r,dt){if(!r.award||!r.transitSeen||r.message&&!r.messageSeen)return;
 if(!achievementUnlocked(r.award)&&r.verified)achievementUnlock(r.award,{stage:6,difficulty:r.difficulty,pilot:r.pilot,defeated:r.defeated,receipt:r.id});
 if(r.awardNotified||!achievementUnlocked(r.award))return;const d=achievementDefinition(r.award);FATE15.toast??={id:r.award,t:0};const T=FATE15.toast;T.t+=Math.max(0,dt);
 if(T.t>=6.5){r.awardNotified=true;FATE15.toast=null;fate15Persist();return;}
 const a=Math.min(1,T.t/.3,(6.5-T.t)/.5),w=260,h=82,x=8-(1-fate15Ease(T.t/.3))*(w+8),y=36;ctx.save();ctx.globalAlpha*=a;
 if(XART.rdy('statpanel_full_0916')){unlockPanel(XART.get('statpanel_full_0916'),UNLOCK_ART.strip,x,y,w,h,true);ui20Text(ctx,'ACHIEVEMENT UNLOCKED',x+w/2,y+12,9,w-24,'center','#f6d883');
  const im=XART.get(d.plaque);if(im)ctx.drawImage(im,x+10,y+25,40,40);ui20Text(ctx,'+200 FP',x+30,y+72,8,52,'center','#8de23a');ui20Text(ctx,d.title,x+62,y+31,12,w-76,'left','#ffffff');
  msgDrawBlock({text:d.desc,budget:999,x:x+62,y:y+43,w:w-76,h:31,maxH:9,minH:8,lineMul:1.2,color:'#cbdce7',outline:false,align:'left',valign:'middle'});}
 ctx.restore();FATE15.lastAward={id:d.id,title:d.title,desc:d.desc,icon:d.plaque,time:T.t};
}
Rival24.mapDraw=function(dt){const r=campaign.stage6Fate;if(!r)return FATE15.base.mapDraw.apply(this,arguments);if(sselBoot>0)return FATE15.base.mapDraw.apply(this,arguments);
 if(FATE15.mapStarted!==r.id){FATE15.mapStarted=r.id;if(!r.transitSeen){CF4.focus=false;MAP4E.xPreview=false;FATE15.cameraReleased=false;FATE15.mapCursor=sselCursor;}}
 const ready=fate15Warm();if(!r.transitSeen&&!ready)return;const before=r.elapsed;r.elapsed=Math.min(60,r.elapsed+Math.max(0,dt||0));
 const h=fate15MapPoint();if(!r.transitSeen){fate15MapShips(r,r.elapsed);if(r.elapsed>=fate15MotionEnd(r)){r.transitSeen=true;if(!r.message)r.messageSeen=true;
   if(r.award&&r.verified)achievementUnlock(r.award,{stage:6,difficulty:r.difficulty,pilot:r.pilot,defeated:r.defeated,receipt:r.id});fate15Persist();fate15Log('map-transit-finished',{defeated:r.defeated,target:r.target});}}
 else FATE15.base.mapDraw.apply(this,arguments);
 fate15MapEffects(r,r.elapsed,h);
 if(before<2.8&&r.elapsed>=2.8)Snd.play('expSmall');if(r.crash&&before<7.7&&r.elapsed>=7.7)Snd.play('expBig');
 if(r.escape&&before<.1&&r.elapsed>=.1)Snd.play('jetDash');
 fate15Message(r);fate15AwardDraw(r,dt||0);
};
achToastTick=function(dt){if(state===GS.STAGESEL&&campaign.stage6Fate&&(!campaign.stage6Fate.transitSeen||!campaign.stage6Fate.messageSeen||FATE15.toast))return false;return FATE15.base.toast.apply(this,arguments);};

/* Extensible award family, persisted separately like the existing general bank. */
const FATE15_STORE='bof_stage6_fates_1115';
const FATE15_DEFS=[{id:'crossed_fate',title:'Crossed Fate',desc:'Defeated the Storm Cannon Boss on Furious Difficulty',icon:'crossed_fate'},
 {id:'road_not_taken',title:'Road Not Taken',desc:'Defeated the Rough Riders on Furious Difficulty',icon:'road_not_taken'}].map(d=>Object.freeze({...d,points:200,family:'stage6_route',steamKey:'BOF_'+d.id.toUpperCase(),plaque:FATE15_ART.icons[d.icon].key}));
const fate15Definitions=Object.fromEntries(FATE15_DEFS.map(d=>[d.id,d]));
function fate15AwardLoad(){try{const d=JSON.parse(localStorage.getItem(FATE15_STORE));if(d&&typeof d==='object')return Object.fromEntries(FATE15_DEFS.filter(v=>d[v.id]&&Number.isFinite(d[v.id].at)).map(v=>[v.id,d[v.id]]));}catch(_){}return {};}
let fate15Awards=fate15AwardLoad();
const FATE15_ACH={list:achievementList,definition:achievementDefinition,points:achievementPoints,unlocked:achievementUnlocked,unlock:achievementUnlock,profile:achievementProfileSnapshot,reload:achievementReload,rows:awardsRows};
achievementList=function(){return FATE15_ACH.list().concat(FATE15_DEFS.map(d=>({...d,unlocked:!!fate15Awards[d.id],unlockedAt:fate15Awards[d.id]?.at||null,meta:fate15Awards[d.id]?.meta||null})));};
achievementDefinition=function(id){return fate15Definitions[id]||FATE15_ACH.definition(id);};
achievementPoints=function(){return FATE15_ACH.points()+FATE15_DEFS.reduce((s,d)=>s+(fate15Awards[d.id]?d.points:0),0);};
achievementUnlocked=function(id){return fate15Definitions[id]?!!fate15Awards[id]:FATE15_ACH.unlocked(id);};
achievementUnlock=function(id,meta){const d=fate15Definitions[id];if(!d)return FATE15_ACH.unlock.apply(this,arguments);if(fate15Awards[id])return false;
 fate15Awards[id]={at:Date.now(),meta:meta?JSON.parse(JSON.stringify(meta)):{}};let persisted=true;try{localStorage.setItem(FATE15_STORE,JSON.stringify(fate15Awards));}catch(_){persisted=false;}
 Snd.play('select');window.dispatchEvent(new CustomEvent('bof-achievement',{detail:{...d,persisted}}));fate15Log('achievement-unlocked',{id,persisted});return true;};
achievementProfileSnapshot=function(){const p=FATE15_ACH.profile();Object.assign(p.unlocked,fate15Awards);return p;};
achievementReload=function(){fate15Awards=fate15AwardLoad();return FATE15_ACH.reload.apply(this,arguments);};
awardsRows=function(){const rows=FATE15_ACH.rows();for(const d of achievementList().filter(d=>d.family==='stage6_route'))if(!rows.some(r=>r.id===d.id))rows.push(d);return rows;};
PASSWORDS.STRM=6;PASSWORDS.BASE4=4;
const fate15Pages=pc5Pages;pc5Pages=function(){return fate15Pages().map(p=>({...p,rows:p.rows.map(r=>r[0]==='STRM'?['STRM','STAGE 6 - SKY PURSUIT']:r)}));};
window.BOF_STAGE6_FATES={state:FATE15,outcome:fate15Outcome,current:fate15Current,receipt:fate15Receipt,definitions:FATE15_DEFS,warm:fate15Warm,keys:fate15Keys};
for(const a of Object.values(FATE15_ART.icons))XART.rdy(a.key);
