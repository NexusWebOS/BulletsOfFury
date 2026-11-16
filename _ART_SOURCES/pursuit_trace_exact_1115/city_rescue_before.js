"use strict";
/* CITY16: rural split, physical exhaust and the mandatory city rescue.
   Native encounter, damage, terminal defeat, result rewards and saves remain owners. */
const CITY16={base:{draw:fb112Draw,blit:tc119Blit,cfg:_levelCfg,load:stageLoadBegin,team:fb2TeamScript,rows:c16Rows,
 choice:s6WingChoiceDraw,routeInput:fr27RouteInput,defeat:achievementEncounterDefeat,leave:scLeaveStage,
 open:openStageSelect,begin:beginStage,auto:campAutoAfterClear,apply:campApply,save:Rival24.save,restore:Rival24.load,
 map:Rival24.mapDraw,input:Rival24.mapInput,back:Rival24.mapBack,camera:cmap2CameraTick,ship:sselShipUpdate,
 keys:d1110Keys,visual:d1110Visual,deploy:sselDeploy,menuBack:menuBackTick,brief:mapgBriefingDraw,storyPlay:s113Play},events:[],holding:false,scene:null,lastThrust:[],travel:null};
for(const a of Object.values(CITY16_TRACE_ART.banks))XART._src[a.key]=a.path+'?v='+a.sha256.slice(0,12);
for(const a of Object.values(CITY16_ART.images))XART._src[a.key]=a.path+'?v='+a.sha256.slice(0,12);
for(const B of Object.values(CITY16_ART.banks))for(const p of B.pages)XART._src[p.key]=p.path+'?v='+p.sha256.slice(0,12);
for(const name of ['storm_nw','storm_nw_shadow','storm_w','storm_w_shadow'])if(CITY16_ART.banks[name])FATE15_ART.banks[name]=CITY16_ART.banks[name];
function city16Log(event,data={}){CITY16.events.push({event,...data});if(CITY16.events.length>256)CITY16.events.shift();}
function city16Keys(){return [...new Set([...Object.values(CITY16_ART.images).map(a=>a.key),...Object.values(CITY16_ART.banks).flatMap(b=>b.pages.map(p=>p.key)),PM27_ART.arrows.g.key,...Object.values(CITY16_TRACE_ART.banks).map(b=>b.key)])];}
function city16Warm(){return city16Keys().map(k=>XART.rdy(k)).every(Boolean);}
function city16Bank(name,f,x,y){const B=CITY16_ART.banks[name];if(!B)return false;const c=B.cells[((f|0)%B.frames+B.frames)%B.frames];if(!XART.rdy(c[0]))return false;
 ctx.drawImage(XART.get(c[0]),c[1],c[2],B.w,B.h,Math.round(x)-B.pivot[0],Math.round(y)-B.pivot[1],B.w,B.h);return true;}
function city16Image(name,x,y){const a=CITY16_ART.images[name];if(!a||!XART.rdy(a.key))return false;ctx.drawImage(XART.get(a.key),Math.round(x),Math.round(y));return true;}

/* Exhaust is painted behind the real hull, registered to the four visible
   nozzle rims. Old model engine positions are never used for these pixels. */
tc119Blit=function(n){if(CITY16.drawing&&n.startsWith('thrust_'))return true;return CITY16.base.blit.apply(this,arguments);};
fb112Draw=function(b){const prior=CITY16.drawing;if(tc119Own(b)&&fb112Ready()){
 CITY16.drawing=b;CITY16.lastThrust=[];const C=b._tc119,dir=fb112Dir(b._fb112.heading,16),f=Math.floor(C.clock*16)%16;
 if(!b.dead&&b._fb112.death<3)for(let i=0;i<CITY16_ART.sockets.length;i++){const at=fb112Point(b,CITY16_ART.sockets[i]),frame=(f+i*3)%16,key='thrust-d'+C.di+'-r'+dir;
  if(city16Bank(key,frame,at.x,at.y))CITY16.lastThrust.push({engine:i,x:at.x,y:at.y,frame,bank:key,di:C.di,dir});}
 }
 try{return CITY16.base.draw.apply(this,arguments);}finally{CITY16.drawing=prior;}};

_levelCfg=function(n=run.stage){const q=CITY16.base.cfg.apply(this,arguments);return q&&Number(n)===6&&!run._gp4StageX?{...q,city:CITY16_ART.images.rural.key}:q;};
stageLoadBegin=function(n,keys){return CITY16.base.load.call(this,n,Number(n)===6?[...(keys||[]),...city16Keys()]:keys);};
fb2TeamScript=function(){const rows=CITY16.base.team.apply(this,arguments),stop=rows.findIndex(b=>['callisto','demo'].includes(b.kind)||/PRIVATE FIELD TESTS|ALLOW ME TO DEMONSTRATE/i.test(b.text||''));return stop<0?rows:rows.slice(0,stop);};

/* All headline, aircraft and route-name pixels belong to the generated menu.
   Keep logical native menu edges and its campaign briefing callback. */
function city16Selection(x,y,t){const a=PM27_ART.arrows.g;if(!XART.rdy(a.key))return false;const f=Math.floor(Math.max(0,t)*16)%16;ctx.save();ctx.shadowBlur=0;ctx.filter='none';ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x)-a.pivot[0],Math.round(y)-a.pivot[1],a.cw,a.ch);ctx.restore();CITY16.lastSelection={key:a.key,frame:f,x,y};return true;}
function city16Trace(side,x,y,t){const difficulty=diffKey==='furious'?'furious':'hard',B=CITY16_TRACE_ART.banks[difficulty+'-'+side];if(!B||!XART.rdy(B.key))return false;const f=Math.floor(Math.max(0,t)*16)%16;ctx.save();ctx.globalAlpha=1;ctx.shadowBlur=0;ctx.filter='none';ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(B.key),f%B.cols*B.w,Math.floor(f/B.cols)*B.h,B.w,B.h,Math.round(x)+B.origin[0],Math.round(y)+B.origin[1],B.w,B.h);ctx.restore();CITY16.lastTrace={difficulty,side,key:B.key,frame:f,origin:B.origin};return true;}
function city16MenuRect(){const w=VW-24,h=w*512/912,x=12,y=Math.round((VH-h)/2);return{x,y,w,h};}
s6WingChoiceDraw=function(){if(run.stage!==6||run._gp4StageX)return CITY16.base.choice.apply(this,arguments);const W=s6Wing;if(!W?.choice||W.route||BOFCinematicDirector.live)return;
 const C=W.frChoice||{side:'left'},r=city16MenuRect(),name=diffKey==='furious'?'pursuit-furious':'pursuit-hard',a=CITY16_ART.images[name];if(!XART.rdy(a.key))return;
 ctx.save();worldXformEscape();city16Image('shade',0,0);ctx.drawImage(XART.get(a.key),r.x,r.y,r.w,r.h);
 city16Trace(C.side,r.x,r.y,C.t||0);
 const cx=r.x+r.w*(C.side==='left'?.06:.52),cy=r.y+r.h*.45;city16Selection(cx,cy,C.t||0);
 controlHintRow([['pad_dpad','CHOOSE'],['pad_a','CONFIRM']],r.y+r.h*.895,VW/2,r.w*.85,20);ctx.restore();
 FATE15.lastChoice={left:diffKey==='furious'?'STORM CANNON':'HARRIER',right:'ROUGH RIDERS',selected:C.side,generated:true,rect:r};};
fr27RouteInput=function(W){if(run.stage!==6||run._gp4StageX)return CITY16.base.routeInput.apply(this,arguments);const C=W.frChoice||(W.frChoice={side:'left',t:0,mouse:false});C.t+=1/60;
 if(Input.menuLeft()){C.side='left';Audio.SFX.blip();}if(Input.menuRight()){C.side='right';Audio.SFX.blip();}
 const m=Input.mouse||{},r=city16MenuRect(),inside=m.y>r.y+r.h*.21&&m.y<r.y+r.h*.78&&m.x>r.x+r.w*.055&&m.x<r.x+r.w*.945;
 if(m.down&&!C.mouse&&inside&&C.t>.2){C.side=m.x<VW/2?'left':'right';fr27ChooseRoute(W,C.side);}C.mouse=!!m.down;
 if(C.t>.2&&Input.menuConfirm())fr27ChooseRoute(W,C.side);};

c16Rows=function(id,p=run.pilot,route=s113Route()){const rows=CITY16.base.rows.apply(this,arguments);if(id!=='post-6'||run._gp4StageX)return rows;
 const tech=d1110Tech(p).toUpperCase(),lines={
 'POST6-05':['COLE','Route us for the city. If anyone is still alive, we have to save them! Is there anything else on the radar? We have to find out what is causing this!'],
 'POST6-06':[tech,'I am detecting a high-level threat underground, close to the riverbank.'],
 'POST6-07':['COLE','Underground? After we save those people, we have to check it out.'],
 'POST6-08':[tech,"As you wish. Alright team, let's do this!"]};
 return rows.filter(b=>!['POST6-09','POST6-10','POST6-11'].includes(b.id)).map(b=>{const v=lines[b.id];if(!v)return b;
  return {...b,who:v[0],text:v[1],people:[v[0].toLowerCase(),v[0]==='COLE'?tech.toLowerCase():'cole'],duration:Math.max(3,v[1].length/30+1.6),speechEnd:v[1].length/30+.12,fpLocations:{cole:'cockpit-sky',[tech.toLowerCase()]:'cockpit-sky'},cm3:{...b.cm3,baseDuration:Math.max(3,v[1].length/30+1.6)}};});};
C16.rows=CM3.rows=FP5.rows=c16Rows;

function city16CompleteRank7(){return campaign.rank?.[7]&&campaign.rank[7]!=='incomplete';}
function city16NeedsCity(){return run.mode==='campaign'&&!!campaign.stageX1004?.route&&!campaign.stageX1004.done&&!city16CompleteRank7();}
function city16NeedsDebrief(){return run.mode==='campaign'&&campaign.cityRescue16?.completed&&!campaign.cityRescue16.debriefSeen;}
function city16Gate(){return city16NeedsCity()||city16NeedsDebrief();}
mapgBriefingDraw=function(info){if(state===GS.STAGESEL&&city16NeedsCity()&&!campPause&&cmap2.focus!=='bar'){
 const harrier=campaign.stageX1004.route==='left';info={key:'city16-required-'+harrier,title:'STAGE X - CITY RESCUE',body:(harrier?'THE HARRIER IS':'THE ROUGH RIDERS ARE')+' ATTACKING THE CITY. SAVE THE PEOPLE BEFORE HEADING TO THE RIVERBANK.'};}return CITY16.base.brief.call(this,info);};
function city16TravelLive(){return state===GS.STAGESEL&&!!CITY16.travel&&!CITY16.travel.done;}
function city16Lock(){if(!city16Gate())return;campaign.unlockedMax=Math.min(campaign.unlockedMax||6,6);campaign.justUnlocked=0;sselMax=Math.min(sselMax||6,6);sselUnlockCine=null;}
function city16Receipt(v){if(!v||v.version!==1)return null;const completed=!!v.completed&&v.verified===true;return{version:1,completed,debriefSeen:completed&&!!v.debriefSeen,travelSeen:completed&&!!v.travelSeen,travelT:clamp(Number(v.travelT)||0,0,3.2),target:['harrier','rebels'].includes(v.target)?v.target:'harrier',
 pilot:PILOTS.some(p=>p.key===v.pilot)?v.pilot:'cole',allies:Array.isArray(v.allies)?[...new Set(v.allies.filter(k=>PILOTS.some(p=>p.key===k)))].slice(0,4):[],verified:!!v.verified,legacy:!!v.legacy};}
Rival24.save=function(){return {...CITY16.base.save(),cityRescue16:campaign.cityRescue16?{...campaign.cityRescue16,allies:campaign.cityRescue16.allies.slice()}:null};};
Rival24.load=function(s){const r=CITY16.base.restore.apply(this,arguments);campaign.cityRescue16=city16Receipt(s?.cityRescue16);CITY16.travel=null;CITY16.scene=null;
 if(!campaign.cityRescue16&&s?.stageX1004?.done&&!city16CompleteRank7())campaign.cityRescue16=city16Receipt({version:1,completed:true,verified:true,legacy:true,pilot:run.pilot,target:s.stageX1004.route==='left'?'harrier':'rebels',allies:gp4Allies()});city16Lock();return r;};
const city16Flying=Object.getOwnPropertyDescriptor(Rival24,'flying').get;
Object.defineProperty(Rival24,'flying',{get(){return city16TravelLive()||city16Flying.call(Rival24);}});
campAutoAfterClear=function(n,next,rank){city16Lock();return CITY16.base.auto.call(this,n,city16Gate()&&next>=7?6:next,rank);};
beginStage=function(n){if(n===7&&city16Gate()){city16Log('stage7-blocked');if(city16NeedsDebrief())city16StartDebrief();else openStageSelect(6,{});return false;}
 if(n===6)delete run._city16Defeat;return CITY16.base.begin.apply(this,arguments);};
sselDeploy=function(n){if(n>=7&&city16Gate()){CF4.focus=true;MAP4E.xPreview=false;cmap2.focus='map';city16Log('deployment-blocked',{stage:n});return;}return CITY16.base.deploy.apply(this,arguments);};
campApply=function(s){const ok=CITY16.base.apply.apply(this,arguments);if(ok){city16Lock();if(city16NeedsDebrief()){if(BOFCinematicDirector.current?.id==='post-city16')setState(GS.CUTSCENE);else city16StartDebrief();}}return ok;};

achievementEncounterDefeat=function(b,role){const fresh=b&&!b._achievementAwarded,city=run.stage===6&&run._gp4StageX,kind=fate15Kind(b),r=CITY16.base.defeat.apply(this,arguments);
 if(fresh&&city&&role==='boss'&&['harrier','rebels'].includes(kind)&&b.hp<=0){run._city16Defeat={target:kind,verified:true};city16Log('native-city-defeat',{target:kind});}return r;};
/* The requested debrief replaces S113's obsolete staged battle insert.
   Invoke that insert's native settlement callback, never a second reward path. */
s113Play=function(id,rows,done){if(CITY16.holding&&/^stage-x-(harrier|rebels)$/.test(id)){city16Log('legacy-city-insert-replaced',{id});if(typeof done==='function')done();return true;}return CITY16.base.storyPlay.apply(this,arguments);};
scLeaveStage=function(R){if(run.stage!==6||!run._gp4StageX){if(run.stage===6&&!R?._beta24Settled&&!R?._s113Leaving&&run._stage6FateDefeat?.verified){campaign.cityRescue16=null;CITY16.travel=null;}return CITY16.base.leave.apply(this,arguments);}
 if(R?._city16Settled||CITY16.holding||campaign.cityRescue16?.completed)return false;
 if(!run._city16Defeat?.verified){city16Log('unverified-city-result-rejected');return false;}
 R._city16Settled=true;const target=run._city16Defeat.target,allies=[...new Set([...(s6Wing?.ships||[]).filter(q=>q.hp>0).map(q=>q.key),...gp4Allies()])].filter(k=>k!==run.pilot).slice(0,4);
 campaign.cityRescue16=city16Receipt({version:1,completed:true,verified:true,target,pilot:run.pilot,allies});CITY16.holding=true;
 try{CITY16.base.leave.apply(this,arguments);}finally{CITY16.holding=false;}
 city16Lock();campAutoAfterClear(6,6,campaign.rank?.[6]||R.rank);campSuspend();city16Log('native-city-settlement',{target});return city16StartDebrief();};

const CITY16_PAIRS={axel:'freezer',freezer:'axel',cole:'decker',decker:'cole',falva:'lizzie',lizzie:'falva'};
function city16AlbumPilot(p,allies){return CITY16_PAIRS[p]&&allies.includes(CITY16_PAIRS[p])?CITY16_PAIRS[p]:'juggernaut';}
function city16Rows(p=run.pilot,allies=campaign.cityRescue16?.allies||[]){const dj=city16AlbumPilot(p,allies),reply=p==='cole'?'decker':'cole',lines=[
 ['cole','Wa-hoo! Another win for us team!'],['decker',"I think that's enough distractions for one day. Shall we embark to the riverbank now?"],
 [p,'Is it going to smell bad?'],[reply,'Very funny, '+c16Name(p)+'.'],[dj,'Is this a good time to put on one of my favorite albums?'],['cole',"Only if it's sad but true."]];
 let previous='',ordered=[],group=-1;
 const rows=lines.map(([who,text],i)=>{const pair=[who,i===3?p:i===5?(dj==='cole'?'decker':dj):who==='cole'?'decker':'cole'],key=pair.slice().sort().join('|'),fresh=key!==previous;
  if(fresh){previous=key;ordered=pair;group++;}const people=ordered.slice(),readAt=fresh?.42:.26;return {id:'CITY16-'+String(i+1).padStart(2,'0'),who:who.toUpperCase(),text,c16:true,d1110:true,kind:'dialogue',art:'comic',layout:'duo',page:0,people,
  fpScene:'post-city16',fpPilot:p,fpLocations:Object.fromEntries(people.map(k=>[k,'cockpit-sky'])),duration:Math.max(3,text.length/30+1.6),speechEnd:text.length/30+.12,readings:[],_cueSet:new Set(),cm3:{group:'city16:'+group,readAt,newStrip:fresh,baseDuration:Math.max(3,text.length/30+1.6)}};});
 rows.push({id:'CITY16-ALBUM',who:'JUGGERNAUT',text:'',c16:true,d1110:true,kind:'wide',art:'comic',layout:'plate',page:2,people:[],readings:[],_cueSet:new Set(),duration:5,city16Album:true});return rows;}
d1110Keys=function(rows){const keys=CITY16.base.keys.apply(this,arguments);if(rows.some(b=>b.city16Album))keys.push(CITY16_ART.images.album.key,CM3_ART.banks['ink-fade'].key);return [...new Set(keys)];};
d1110Visual=function(b,s){if(!b.city16Album)return CITY16.base.visual.apply(this,arguments);
 ctx.save();ctx.setTransform(SS,0,0,SS,0,0);city16Image('album',0,0);cm3Cover([0,0,912,512],Math.floor(clamp(s.t/.4,0,1)*8));if(s.t>b.duration-.3)cm3Cover([0,0,912,512],Math.floor(clamp((b.duration-s.t)/.3,0,1)*8));ctx.restore();
 CITY16.lastAlbum={shot:b.id,time:s.t,smiling:true,key:CITY16_ART.images.album.key};return true;};
function city16StartDebrief(){const q=campaign.cityRescue16;if(!q?.completed||q.debriefSeen||BOFCinematicDirector.current?.id==='post-city16')return false;
 const rows=city16Rows(q.pilot,q.allies),done=()=>{if(q!==campaign.cityRescue16||q.debriefSeen)return;q.debriefSeen=true;campaign.unlockedMax=Math.max(7,campaign.unlockedMax||6);campaign.justUnlocked=7;
  city16Log('city-debrief-finished');openStageSelect(7,{unlock:7});campAutoAfterClear(6,7,campaign.rank?.[6]);campSuspend();};
 const ok=d1110Play('post-city16',rows,done);if(ok){CITY16.scene=BOFCinematicDirector.current;city16Log('city-debrief-started',{pilot:q.pilot,dj:city16AlbumPilot(q.pilot,q.allies)});}return ok;}

openStageSelect=function(n,opts){if(CITY16.holding){CITY16.heldMap=[n,opts];return;}if(city16NeedsDebrief()){city16StartDebrief();return;}
 if(city16NeedsCity()){n=6;opts={...(opts||{})};delete opts.unlock;city16Lock();}
 const out=CITY16.base.open.call(this,n,opts);city16Lock();if(city16NeedsCity()){CF4.focus=true;CF4.flight=3.3;MAP4E.xPreview=false;cmap2.focus='map';}
 const q=campaign.cityRescue16;if(q?.completed&&q.debriefSeen&&!q.travelSeen){CITY16.travel={t:q.travelT||0,done:false};sselCursor=7;sselUnlockCine=sselUnlockCine||null;map4eWarm();city16TravelShip();city16Log('chibi-flight-started');}return out;};
function city16TravelShip(){const T=CITY16.travel;if(!T||T.done)return;const from=map4eStageXPoint(),to=sselFlagXY(7);if(!from||!to)return;const u=fate15Ease(T.t/3.2),x=lerp(from.x,to.x,u),y=lerp(from.y,to.y,u);
 sselShip={...(sselShip||{}),x,y,tx:to.x,ty:to.y,t:T.t,phase:'idle',bank:0,trail:999,cur:7,face:to.x<from.x?-1:1,head:to.x<from.x?-Math.PI/2:Math.PI/2,moving:u<1};}
sselShipUpdate=function(){if(city16TravelLive()){city16TravelShip();return;}return CITY16.base.ship.apply(this,arguments);};
cmap2CameraTick=function(dt,cine,selected){const r=campaign.stage6Fate,T=CITY16.travel;if(city16TravelLive()){
 city16TravelShip();const t=cmap2Frame('hub',7),k=1-Math.exp(-Math.max(0,dt)*3.8);for(const key of ['x','y','z'])cmap2.cam[key]+=(t[key]-cmap2.cam[key])*k;return;}
 if(state===GS.STAGESEL&&r&&(!r.transitSeen||city16NeedsCity())&&sselBoot<=0&&!campPause&&cmap2.focus!=='bar'){
  FATE15.mapCursor=sselCursor;FATE15.cameraReleased=false;const h=map4eHubPose(),close={x:h.x,y:h.y+55,z:.34},wide=r.escape?map30Overview():cmap2Frame(6,'hub'),u=fate15Ease((r.elapsed-(r.escape?3.2:1.7))/1.7),t={x:lerp(wide.x,close.x,u),y:lerp(wide.y,close.y,u),z:lerp(wide.z,close.z,u)},k=1-Math.exp(-Math.max(0,dt)*3.8);
  for(const key of ['x','y','z'])cmap2.cam[key]+=(t[key]-cmap2.cam[key])*k;return;}
 return CITY16.base.camera.apply(this,arguments);};
Rival24.mapDraw=function(dt){const out=CITY16.base.map.apply(this,arguments);city16Lock();if(city16NeedsCity()&&!fate15Motion()&&!campPause&&cmap2.focus!=='bar')CF4.focus=true;
 const T=CITY16.travel,q=campaign.cityRescue16;if(city16TravelLive()&&sselBoot<=0&&!campPause){T.t=Math.min(3.2,T.t+Math.max(0,dt||0));q.travelT=T.t;city16TravelShip();if(T.t>=3.2){T.done=true;q.travelSeen=true;FATE15.cameraReleased=true;fate15Persist();city16Log('chibi-flight-finished');}}return out;};
Rival24.mapInput=function(){if(city16TravelLive()){Input.menuConfirm();return true;}if(city16NeedsCity()&&!fate15Motion()&&!campPause&&cmap2.focus!=='bar'&&!sselBoot){CF4.focus=true;MAP4E.xPreview=false;}
 return CITY16.base.input.apply(this,arguments);};
Rival24.mapBack=function(){return city16TravelLive()?true:CITY16.base.back.apply(this,arguments);};
menuBackTick=function(){if(city16TravelLive()){Input.menuBack();return false;}return CITY16.base.menuBack.apply(this,arguments);};
window.BOF_CITY_RESCUE_1115={state:CITY16,required:city16Gate,rows:city16Rows,albumPilot:city16AlbumPilot,warm:city16Warm,keys:city16Keys,receipt:city16Receipt};
