'use strict';
/* Event-bound campaign cinema. Native results, unlocks, saves and combat remain owners.
   Authored fixed cells only: no runtime rotation, image scaling, alpha or FX synthesis. */
const S113={base:{script:BOFCinematicDirector.script,start:BOFCinematicDirector.start,
 draw:BOFCinematicDirector.draw,tick:BOFCinematicDirector.tick,preview:C22.preview,
 flyover:drawFlyover,begin:beginStage,load:stageLoadBegin,leave:scLeaveStage,normalOpen:nf100Open},
 W:912,H:512,revision:9,events:[],last:null,exit:null,guard:null,casts:S113_ART.pilots};
for(const a of Object.values(S113_ART.banks))XART._src[a.key]=a.path;
Snd.prepare?.(['stage3AtomicSiren','crackle','jetDash','expBig','blip','dracodiaShriek']);
function s113Bank(name,f=0,x=456,y=256){const a=S113_ART.banks[name];if(!a||!XART.rdy(a.key))return false;
 f=clamp(Math.floor(f),0,a.frames-1);ctx.drawImage(XART.get(a.key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,
 Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.w,a.h);return true;}
function s113Line(who,text,shot,extra={}){const bank=S113_ART.banks[shot];return {who:who.toUpperCase(),text,s113:shot,bg:bank?.key,...extra};}
function s113Action(shot,duration,extra={}){return s113Line('FURY FLIGHT','',shot,{duration,s113Action:true,...extra});}
function s113Crew(p=run.pilot){const leads=[p,...(coopActive()?[p2Pilot().key]:[])];
 const guards=['decker','axel','juggernaut','freezer','lizzie'].filter(k=>!leads.includes(k)&&k!=='cole').slice(0,2);
 const flying=[...new Set([...leads,'cole','yuri','maverick','freezer','lizzie','falva','juggernaut','axel','decker'])].filter(k=>!guards.includes(k)).slice(0,5);
 return {guards,flying};}
function s113Route(){return run._gp4StageX||s6Wing?.route||'left';}
function s113Script(stage,p=run.pilot,route=s113Route()){
 const L=s113Line,A=s113Action,c=p==='decker'?'cole':'decker',crew=s113Crew(p),g=crew.guards.map(k=>k.toUpperCase()).join(' and ');
 if(stage===2)return [
 L(p,'That dish still has power. If its service connection fits my ship, I might get comms and maps back.','cockpit-'+p),
 L(p,'A compatible cable. Finally, something out here is working in our favor.','volcanic-dish',{frame:3}),
 A('cable-'+p,7.2,{sequence:[0,1,2,3],step:1.8,cue:'crackle'}),
 L(p,'Power is stable. Navigation online... squad transponders! There you are.','cable-'+p,{frame:3}),
 L(c,'We have your signal! The others are just ahead, near that base. We are heading there now.','command-bay',{frame:0,actor:'typing'}),
 L(p,'Wait. That ground was bare a second ago. Is that snow?','freeze',{frame:1}),
 A('freeze',5.6,{sequence:[0,1,2,3],step:1.4}),
 L(p,'The whole area is freezing over. First the volcano, now this? Those anomalies are connected.','freeze',{frame:3}),
 ...BOFCinematicDirector.upgrade(2,p).map(b=>L(b.who,b.text,'freeze',{frame:3})),
 L(p,'I am going in. Keep my beacon marked. I will find out what is causing this.','freeze',{frame:3})];
 if(stage===3)return [
 A('hangar',4.6,{flight:'return',cue:'jetDash'}),
 L('cole','Everyone made it back. Good. Get clear of the flight line and check in.','lounge',{group:'happy'}),
 L('decker','I am overriding the safety locks until we know what is happening. I am also disabling every auto-flight system. Nobody gets hacked in midflight.','command-bay',{frame:0,group:'neutral'}),
 L('cole','Join Decker and me in the Command Bay. All of you. We need a plan.','command-bay',{frame:0,group:'neutral'}),
 A('command-bay',2.8,{frame:0,actor:'typing'}),
 L('decker','I am enhancing these satellite images. Abandoned airbase, about twenty miles east of Fury HQ. Look at this power reading.','command-bay',{frame:1,actor:'typing'}),
 L('decker','That is a launch pad. Something left this base and went into space. The launch was shortly before everything went to hell.','command-bay',{frame:2,actor:'typing'}),
 L('cole','Then that airbase is our next stop. Recover the records and find out what they launched.','command-bay',{frame:1,group:'neutral'}),
 ...BOFCinematicDirector.upgrade(3,p).map(b=>L(b.who,b.text,'forge',{group:'neutral'})),
 L(p,'We have our heading. Fury flight, move out.','launch-pad',{frame:0})];
 if(stage===4)return [
 A('launch-pad',2,{frame:2,actor:'onsite'}),
 L(c,'You are inside the hangar. Find the mainframe terminal and open the launch archive. Search for the last satellite uplink.','launch-pad',{frame:2,comic:true,actor:'onsite',portraitEmotion:'determined'}),
 L(p,'At the terminal. Launch logs, telemetry, security recordings... I have the uplink file.','launch-pad',{frame:2,comic:true,actor:'onsite'}),
 L(c,'Wait! That is it! Quick, upload that file to our network! Let me see... What in the world... Everyone, you are going to want to see this.','command-bay',{frame:1,actor:'ecstatic'}),
 A('symbiote-jump',6.2,{sequence:[0,1,2],step:2.1}),
 A('symbiote-jump',.65,{frame:3,cue:'dracodiaShriek'}),
 A('command-bay',1.5,{frame:0,actor:'shock',cue:'crackle'}),
 L('decker','What the...! Give me a second. That damn thing came from space. It took over the satellite and used it to reach our network.','command-bay',{frame:0,comic:true,portraitEmotion:'scared',listenerEmotion:'scared'}),
 L('decker','During the upload I got into their terminal and downloaded classified intel. Earth\'s Space Federation Division left a prototype here.','launch-pad',{frame:2,comic:true,portraitEmotion:'surprised'}),
 L(c,'A spacecraft armor suit that attaches to your jet. Orbital life support and an entire arsenal. For defense purposes, of course.','launch-pad',{frame:2,comic:true,portraitEmotion:'happy'}),
 ...BOFCinematicDirector.upgrade(4,p).map(b=>L(b.who,b.text,'launch-pad',{frame:3,comic:true})),
 L('cole','We have no choice. If the answers are up there, that is where we go.','command-bay',{frame:2,group:'neutral'}),
 L('decker','Fit the Federation suit. We will guide you as far as the signal holds.','launch-pad',{frame:3,comic:true,portraitEmotion:'determined'}),
 A('launch-pad',4.5,{frame:3,flight:'launch',cue:'jetDash'})];
 if(stage===5)return [
 A('earth',4,{flight:'return',cue:'jetDash'}),A('hangar',4,{flight:'return'}),
 L('cole','Welcome home! That is how you bring a Fury pilot back in one piece!','lounge',{group:'jump_cheer'}),
 L('decker','Is that the chaingun from Chronos? Oh, I can work with this. Everyone, go relax in the lounge. Leave the salvage to me.','forge',{group:'happy',actor:'ecstatic'}),
 L(p,'You heard him. Try to get some rest while we still can.','lounge',{group:'happy'}),
 L('FURY HQ','LATER THAT NIGHT','forge',{actor:'typing',duration:3}),
 A('forge',3.2,{actor:'typing',cue:'crackle'}),
 ...BOFCinematicDirector.upgrade(5,p).map(b=>L(b.who,b.text,'forge',{actor:'ecstatic'})),
 L('decker','Paired chaingun turrets installed on our jets. Talk about heavy metal!','forge',{actor:'ecstatic'}),
 A('alarm',2.3,{frame:0,cue:'stage3AtomicSiren',group:'angry'}),
 L('FURY COMMAND','RED ALERT! ALL PERSONNEL TO BATTLE STATIONS!','alarm',{frame:1,group:'angry'}),
 L('decker','Those are not glitches. Every red contact is hostile... They are covering the entire sky!','alarm',{radar:true,actor:'panic'}),
 A('alarm',1.3,{frame:3,actor:'duck',cue:'expBig'}),
 L('cole',g+', stay behind and defend HQ! Everyone else, TO THE SKIES. NOW!','alarm',{frame:3,group:'angry'}),
 A('hangar',3.2,{group:'run',cue:'jetDash'}),
 A('hangar',6.4,{flight:'squad',crew:crew.flying,cue:'jetDash'}),
 A('alien-descent',6.4,{sequence:[0,1,2,3],step:1.6,cue:'stage3AtomicSiren'})];
 if(stage===6){const harrierDefeated=route==='left';return [
 A('sky',harrierDefeated?4.8:8,{battle:harrierDefeated?'harrier':'rebels',cue:'expBig'}),
 A('hangar',3.8,{flight:'return',cue:'jetDash'}),
 L('decker',harrierDefeated?'The Rebel Fighters have reached the city. If we do not stop them, casualties could be massive.':'The Harrier is heading into the city. We have to stop it before the casualties become massive.','command-bay',{frame:0,actor:'panic'}),
 L('cole','Keep that remaining threat marked for Stage X. What else are you seeing?','command-bay',{frame:0,group:'neutral'}),
 L('decker','Something underground. A strange alien signal... almost like it wants us to find it. Let me narrow the scan.','command-bay',{frame:0,actor:'typing'}),
 A('command-bay',2.8,{frame:1,actor:'typing'}),
 L('decker','Under the city itself. Inside the sewers. That is where the signal is coming from.','command-bay',{frame:3,actor:'typing'}),
 L(p,'Keep the channel open. We are heading down to check it out.','sewer'),
 ...BOFCinematicDirector.upgrade(6,p).map(b=>L(b.who,b.text,'sewer'))];}
 return S113.base.script(stage,p,route);
}
function s113Keys(beats){const names=new Set(['fade']),portraits=new Set(['dlg_window']);for(const b of beats){if(b.s113)names.add(b.s113);
 const who=String(b.who).toLowerCase();if(S113.casts.includes(who))for(const pose of ['idle','talk'])portraits.add(commPortrait(who,pose));
 if(b.comic){names.add('comic-backdrop');names.add('comic-border');names.add('comic-scroll-'+run.pilot);names.add('headset-panel-'+run.pilot);names.add('headset-panel-'+(run.pilot==='decker'?'cole':'decker'));}
 if(b.group)for(const p of S113.casts)names.add('actor-'+p);
 if(b.actor){names.add(['command-bay','alarm'].includes(b.s113)?'decker-room':'decker-shock');names.add('actor-'+run.pilot);}
 if(b.flight)for(const p of b.crew||[run.pilot]){names.add('launch-'+p);names.add('return-'+p);names.add('flight-'+p);}
 if(b.battle){for(const p of s113Crew().flying)names.add('flight-'+p);for(const p of ['voss','nyx','rook','kaia','jace'])names.add('rebel-'+p);names.add('harrier');}}
 return [...names].map(n=>S113_ART.banks[n]?.key).concat([...portraits],beats.some(b=>b.battle)?[C22_ART.banks.data_blast.key]:[]).filter(Boolean);}
function s113Warm(keys){let ok=true;for(const k of keys)if(!XART.rdy(k))ok=false;return ok;}
function s113Viewport(){if(CINEMA_VW!==912||cv.width!==912*SS||cv.height!==VH*SS){CINEMA_VW=912;cv.width=912*SS;cv.height=VH*SS;ctx.setTransform(SS,0,0,SS,0,0);window.__bofFit?.();}}
function s113Play(id,beats,done){const keys=s113Keys(beats);s113Warm(keys);const ok=BOFCinematicDirector.play(id,beats,done);
 if(ok){const s=BOFCinematicDirector.current;s.s113Keys=keys;s.s113Loading=0;S113.events.push({event:'start',id,pilot:run.pilot});s113Viewport();}return ok;}
BOFCinematicDirector.script=s113Script;
BOFCinematicDirector.start=function(stage,done){if(run.mode!=='campaign')return false;if(![2,3,4,5,6].includes(stage))return S113.base.start(stage,done);
 return s113Play('post-'+stage,s113Script(stage),stage===5?()=>{Input.clearTaps();beginStage(6);}:done);};
BOFCampaignStory.script=s113Script;BOFCampaignStory.start=(n,done)=>BOFCinematicDirector.start(n,done);
// Easy/Normal settle and archive their Chronos clear before calling this owner.
// Show the same homecoming, then retain their native difficulty-choice ending.
nf100Open=function(flight=true,preview=false){
 if(flight&&!preview&&run.mode==='campaign'&&run.stage===5&&!debugFight){
  if(S113.guard?.kind==='normal-homecoming')return;
  const guard={kind:'normal-homecoming',done:false};S113.guard=guard;
  if(s113Play('post-5',s113Script(5),()=>{if(guard.done)return;guard.done=true;
   S113.guard=null;S113.events.push({event:'homecoming-to-completion',difficulty:diffKey});
   S113.base.normalOpen(false,false);}))return;
  S113.guard=null;
 }
 return S113.base.normalOpen.apply(this,arguments);
};
function s113Actor(p,pose,x,y){return s113Bank('actor-'+p,S113_ART.actorPoses.indexOf(pose),x,y);}
function s113Group(kind,t,omit){for(let i=0;i<S113.casts.length;i++){const p=S113.casts[i],moving=kind==='run';if(p===omit)continue;
 const pose=moving?'run_'+Math.floor(t*10)%4:kind==='jump_cheer'?(Math.floor(t*3)%2?'jump_cheer':'happy'):kind;
 s113Actor(p,pose,moving?80+i*90+t*125:72+i*96,365-(i%2)*20);}}
function s113Battle(kind,t){const allies=s113Crew().flying;
 for(let i=0;i<5;i++){const u=clamp(t/6,0,1),x=100+i*168+Math.sin(t*1.3+i)*65,y=380-u*200+Math.sin(t*1.7+i)*32;
 s113Bank('flight-'+allies[i],t<2?1:t<4?2:3,x,y);}
 if(kind==='harrier'){s113Bank('harrier',0,456,130+t*19);if(t>1.1)s113Explosions(t,[[390,170],[500,215],[440,100]]);}
 else for(let i=0;i<5;i++){const fall=Math.max(0,t-2-i*.52),x=100+i*168+Math.sin(t+i)*40,y=95+fall*fall*60;
 if(fall<1.8)s113Bank('rebel-'+['voss','nyx','rook','kaia','jace'][i],fall?72+Math.floor(fall*9)%16:48+Math.floor(t*24)%8,x,y);
 if(fall>.5&&fall<2.4)s113Explosions(fall-.5,[[x,y]]);}}
function s113Explosions(t,points){const a=C22_ART.banks.data_blast;if(!a||!XART.rdy(a.key))return;
 const f=clamp(Math.floor(t*12)%a.frames,0,a.frames-1);for(const [x,y]of points)ctx.drawImage(XART.get(a.key),f%a.columns*a.w,Math.floor(f/a.columns)*a.h,a.w,a.h,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.w,a.h);}
function s113PortraitFrame(side,b,t,active,talking){
 const inward=side==='left'?8:4,clips=S113_ART.headsetMotion.clips;
 if(active&&b.portraitClip&&clips[b.portraitClip]){const c=clips[b.portraitClip];return c.frames[Math.floor(t*1000/c.ms)%c.frames.length];}
 const emotion=active?b.portraitEmotion:b.listenerEmotion;
 const first={happy:12,sad:14,angry:16,scared:18,surprised:20,determined:22}[emotion];
 if(!active)return first??inward;
 if(t<.18)return inward;if(t<.32)return 0;
 if(first!==undefined)return first+(talking&&Math.floor((t-.32)*8)%3!==0?1:0);
 return talking?[0,1,2,1,3,1][Math.floor((t-.32)*9)%6]:0;
}
function s113Comic(b,t){const p=run.pilot,contact=p==='decker'?'cole':'decker',who=String(b.who).toLowerCase(),leftActive=who===contact;
 const s=BOFCinematicDirector.current,talking=!!s&&s.shown<b.text.length;
 const left=s113PortraitFrame('left',b,t,leftActive,talking),right=s113PortraitFrame('right',b,t,!leftActive,talking);
 const scroll=S113_ART.comicScroll,scrollTime=s?.age??t,scrollFrame=Math.floor(scrollTime*scroll.fps)%scroll.phases;
 s113Bank('comic-backdrop');s113Bank('comic-scroll-'+p,scrollFrame,456,196);s113Bank('headset-panel-'+contact,left,214,398);s113Bank('headset-panel-'+p,right,698,398);s113Bank('comic-border');
 S113.last={shot:b.s113,frame:0,pilot:p,comic:true,actor:null,time:t,contact,leftFrame:left,rightFrame:right,speaker:leftActive?'left':'right',talking,emotion:b.portraitEmotion||'neutral',clip:b.portraitClip||null,scrollFrame,scrollTime,leftColor:scroll.colors[contact],rightColor:scroll.colors[p]};
}
function s113Visual(b,t){let f=b.frame??0;if(b.sequence)f=b.sequence[Math.min(b.sequence.length-1,Math.floor(t/(b.step||1)))];
 if(b.comic){s113Comic(b,t);return;}
 if(b.radar)f=t<1.4?0:t<2.7?1:2;s113Bank(b.s113,f);
 if(b.group)s113Group(b.group,t,b.actor?'decker':null);
 if(b.actor==='onsite'){if(!b.comic)s113Actor(run.pilot,'dispatch_typing',290,370);}
 else if(b.actor){const f=b.radar&&t>2.7?2:({typing:0,ecstatic:1,shock:2,recover:3,panic:4,duck:5}[b.actor]??0);
  if(['command-bay','alarm'].includes(b.s113))s113Bank('decker-room',f,190,406);
  else s113Bank('decker-shock',f,b.actor==='typing'?270:456,410);}
 if(b.flight==='return')s113Bank('return-'+run.pilot,Math.min(31,t*8),456,180+t*21);
 if(b.flight==='launch')s113Bank('launch-'+run.pilot,Math.min(47,t*12),456,310-t*55);
 if(b.flight==='squad')for(let i=0;i<b.crew.length;i++){const q=Math.max(0,t-i*.38);s113Bank('launch-'+b.crew[i],Math.min(47,q*12),150+i*150,340-q*70);}
 if(b.battle)s113Battle(b.battle,t);
 S113.last={shot:b.s113,frame:f,pilot:run.pilot,actor:b.actor,flight:b.flight,battle:b.battle,time:t};}
BOFCinematicDirector.tick=function(dt){const s=this.current,b=s?.beats[s.i];if(!b?.s113||s.live)return S113.base.tick.call(this,dt);
 s.s113Keys??=s113Keys(s.beats);s.s113Loading+=dt;
 if(!s113Warm(s.s113Keys)&&s.s113Loading<12){if(s.age>.15&&Input.menuStart()){this.finish();return;}s.age+=dt;return;}
 if(!b._s113Cue){b._s113Cue=true;if(b.cue)Snd.play(b.cue);S113.events.push({event:'beat',id:s.id,index:s.i,shot:b.s113});}
 if(b.radar){const n=Math.min(35,Math.floor((Math.exp(Math.min(s.t,5)*.65)-1)*2));if(n>(b._beeps||0)){b._beeps=n;Snd.play('blip');}}
 if(b.battle){const n=b.battle==='harrier'?(s.t>1.1?1:0):clamp(Math.floor((s.t-2.5)/.52)+1,0,5);if(n>(b._s113Blasts||0)){b._s113Blasts=n;Snd.play('expBig');}}
 const out=S113.base.tick.call(this,dt);if(this.current===s&&s.beats[s.i]===b&&(b.s113Action||b.portraitClip)&&s.t>=b.duration){s.shown=b.text.length;this.advance();}return out;};
BOFCinematicDirector.draw=function(){const s=this.current,b=s?.beats[s.i];if(!b?.s113||s.live)return S113.base.draw.apply(this,arguments);
 s113Viewport();ctx.save();ctx.imageSmoothingEnabled=false;ctx.fillStyle='#000';ctx.fillRect(0,0,912,512);s113Visual(b,s.t);
 if(!b.s113Action){dlgBox._tw={key:String(state)+'|'+b.who+'|'+b.text,count:s.shown,at:performance.now(),auto:false};
 dlgBox({who:b.who,portrait:S113.casts.includes(b.who.toLowerCase())?b.who.toLowerCase():false,full:b.text,shown:b.text.slice(0,s.shown),forceShown:true,fade:1,pw:840,ph:84,y:406,maxBottom:490,screenSpace:false});}
 msgFaceUse('dialogue');controlHintRow([['pad_a',s.shown<b.text.length?'REVEAL':'NEXT'],['pad_start','SKIP SCENE']],500,456,860,14);msgFaceUse(null);ctx.restore();};
stageLoadBegin=function(n,keys){
 const campaignCinema=run.mode==='campaign'&&!debugFight&&[2,3,4,5,6].includes(n);
 const story=campaignCinema?s113Keys(s113Script(n)):[];
 const more=campaignCinema&&[2,4].includes(n)?['s113_'+(n===2?'dish-exit':'pad-exit'),'s113_landing-'+run.pilot,...(coopActive()?['s113_landing-'+p2Pilot().key]:[]),'s113_fade']:[];
 return S113.base.load.call(this,n,[...new Set([...(keys||[]),...story,...more])]);};
beginStage=function(){S113.exit=null;S113.guard=null;return S113.base.begin.apply(this,arguments);};
drawFlyover=function(dt){if(run.mode!=='campaign'||![2,4].includes(run.stage)||debugFight)return S113.base.flyover.apply(this,arguments);
 const name=run.stage===2?'dish-exit':'pad-exit',a=S113_ART.banks[name],keys=[a.key,'s113_landing-'+run.pilot,...(coopActive()?['s113_landing-'+p2Pilot().key]:[]),'s113_fade'];
 if(!S113.exit){S113.exit={t:0,wait:0,startX:player.x,startY:player.y,cam:camX,done:false};Audio.stopMusic();Audio.startMusic('stageclear');}
 const e=S113.exit;e.wait+=dt;const ready=s113Warm(keys);if(ready)e.t+=Math.max(0,dt);const t=e.t;
 if(!ready&&e.wait>12){S113.events.push({event:'exit-art-timeout',stage:run.stage});S113.exit=null;return S113.base.flyover(dt);}
 if(t>.4&&Input.menuStart()){e.done=true;S113.exit=null;setState(GS.STAGECLEAR);return;}
 const u=clamp((t-1)/7.5,0,1),travel=Math.round(a.h*u),targetX=run.stage===2?570:566,targetY=run.stage===2?318:246;
 const camera=Math.round(e.cam+(clamp(targetX-VW/2,0,worldWidth()-VW)-e.cam)*u);camX=camera;
 ctx.save();ctx.fillStyle='#000';ctx.fillRect(0,0,VW,VH);
 if(travel<VH){ctx.save();ctx.translate(0,travel);_cinematicHidePlayer=true;try{drawWorld(0);}finally{_cinematicHidePlayer=false;ctx.restore();}}
 ctx.save();ctx.translate(-camera,travel-a.h);s113Bank(name,0,340,a.h/2);ctx.restore();
 const x=e.startX+(targetX-e.startX)*u,y=e.startY+(targetY-e.startY)*u;
 s113Bank('landing-'+run.pilot,clamp((t-7.5)*12,0,31),Math.round(x-camera),Math.round(y));
 if(coopActive())s113Bank('landing-'+p2Pilot().key,clamp((t-7.5)*12,0,31),Math.round(x-camera-58),Math.round(y+18));
 if(t>10.5){const f=clamp(Math.floor((t-10.5)/.05),0,16);s113Bank('fade',f,VW/2,VH/2);}
 ctx.restore();S113.last={shot:name,time:t,travel,ship:[x,y],landed:t>=10.2,fade:t>10.5};
 if(t>=11.4&&!e.done){e.done=true;S113.events.push({event:'landed-to-stats',stage:run.stage});S113.exit=null;flyoverT=0;setState(GS.STAGECLEAR);}};
scLeaveStage=function(result){
 if(result._s113Leaving)return;
 if(run.mode==='campaign'&&[2,3,4,5,6].includes(run.stage))result._s113Leaving=true;
 if(run.mode==='campaign'&&run._gp4StageX){
  const route=run._gp4StageX,kind=route==='left'?'harrier':'rebels';
  if(s113Play('stage-x-'+kind,[s113Action('sky',kind==='harrier'?5:8,{battle:kind,cue:'expBig'})],()=>{
   S113.events.push({event:'stage-x-to-map',route});S113.base.leave(result);
  }))return;
 }
 return S113.base.leave.apply(this,arguments);};
S113.preview=async function(id,p=run.pilot,route='left'){BOFCinematicDirector.cancel();run.mode='campaign';run.pilot=S113.casts.includes(p)?p:'cole';coopOn=false;Input.clearTaps();Input.mouse.down=false;
 const beats=id.startsWith('post-')?s113Script(Number(id.slice(5)),run.pilot,route):[s113Action('sky',8,{battle:id.includes('harrier')?'harrier':'rebels',cue:'expBig'})];
 const keys=s113Keys(beats),start=performance.now();while(!s113Warm(keys)){if(performance.now()-start>60000)throw Error('Cutscene art failed to load');await new Promise(r=>setTimeout(r,50));}
 return s113Play('review-'+id,beats,()=>setState(GS.TITLE));};
S113.previewHeadsets=async function(p=run.pilot,clip='all'){
 BOFCinematicDirector.cancel();run.mode='campaign';run.pilot=S113.casts.includes(p)?p:'cole';coopOn=false;Input.clearTaps();Input.mouse.down=false;
 const clips=S113_ART.headsetMotion.clips,names=clip==='all'?Object.keys(clips):[clip];
 if(names.some(n=>!clips[n]))throw Error('Unknown headset animation');
 const beats=names.map(n=>s113Line(run.pilot,n.replace(/-/g,' ').toUpperCase(),'comic-backdrop',{comic:true,portraitClip:n,duration:5}));
 const keys=s113Keys(beats),start=performance.now();while(!s113Warm(keys)){if(performance.now()-start>60000)throw Error('Headset art failed to load');await new Promise(r=>setTimeout(r,50));}
 return s113Play('review-headsets',beats,()=>setState(GS.TITLE));
};
C22.preview=function(id,p){if(id.startsWith('post-')&&[2,3,4,5,6].includes(Number(id.slice(5))))return S113.preview(id,p);return S113.base.preview.apply(this,arguments);};
window.BOF_STORY_1103=S113;
