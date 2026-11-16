"use strict";
/* Revised satellite discovery, six-panel workshop, and moving cinematic terrain. */
const CW16={base:{keys:d1110Keys,rows:c16Rows,visual:d1110Visual,top:sl14TopDown,bed:ls112Bed,connector:connectorSurface,launch:drawLaunch,begin:beginStage},last:null,water:{elapsed:0,motion:0,hadLaunch:false,settled:false},events:[]};
for(const a of Object.values(CW16_ART.banks))XART._src[a.key]=a.path;
function cw16Row(id,who,text,extra={}){return{id,who,text,kind:'dialogue',people:['cole','decker'],style:0,duration:Math.max(3.4,String(text).length/30+2.8),...extra};}
C16_STORY.scenes['post-3']=[
 cw16Row('B301','COLE',"All right. We're home. What did we find?",{tag:'briefing'}),
 cw16Row('CW3-02','DECKER','We were able to access the network at the base, despite cooling levels being below freezing.',{tag:'briefing'}),
 cw16Row('CW3-03','DECKER','Something sent a distress-signal virus from one of our own satellites.',{tag:'briefing'}),
 cw16Row('CW3-04','DECKER',"I can't even understand the code either. It's almost like it's alien. I've never seen any language like this. Ever.",{tag:'briefing'}),
 cw16Row('CW3-05','COLE',"You're saying we may be dealing with something outside of our own world?!",{tag:'briefing'}),
 cw16Row('CW3-06','DECKER',"Seems so. If we want answers, we're going to have to head to space, where it last came from, and trace the signal back to its source.",{tag:'briefing'}),
 cw16Row('CW3-07','DECKER',"There's an airbase about 500 km to the east. Last I heard, there was supposed to be a space shuttle launch, but it never went through.",{tag:'briefing'}),
 cw16Row('CW3-08','DECKER','I also know the Federation was testing prototype attachment suits for domestic aircraft. We may be in luck.',{tag:'briefing',upgrade:3}),
 cw16Row('CW3-09','AXEL','A shuttle launch facility. That gives us a destination.',{people:['axel','freezer'],tag:'briefing'}),
 cw16Row('CW3-10','FREEZER',"And a way up. I'll take those odds.",{people:['axel','freezer'],tag:'briefing'}),
 cw16Row('CW3-11','FALVA','Prototype space attachments? Now that I want to see.',{people:['falva','lizzie'],tag:'briefing'}),
 cw16Row('CW3-12','LIZZIE','First we get there. Then we test anything.',{people:['falva','lizzie'],tag:'briefing'}),
 cw16Row('CW3-13','YURI','If that signal came from orbit, we follow it.',{people:['yuri','maverick'],tag:'briefing'}),
 cw16Row('CW3-14','MAVERICK',"Alien trouble. Just when I thought this couldn't get stranger.",{people:['yuri','maverick'],tag:'briefing'}),
 cw16Row('CW3-15','JUGGERNAUT','As long as we go together.',{people:['juggernaut','cole'],tag:'briefing'}),
 cw16Row('CW3-16','COLE',"Then we go. Better than sitting around twiddling our thumbs. Let's go!",{tag:'briefing',duration:6.8}),
 cw16Row('CW3-W01','DECKER',"There's one more thing I wanted to show you.",{tag:'prototypes',cw16:'workshop',panel:0}),
 cw16Row('CW3-DEMO','SYSTEM','',{tag:'prototypes',kind:'insert',cw16:'photon',duration:7.2,c16Cues:[{name:'bossWeaponCharge',at:.55},{name:'av3_cole_laser7',at:2.5}]}),
 cw16Row('CW3-W02','COLE',"That's your Photon Cannon? Decker, this is incredible!",{tag:'prototypes',cw16:'workshop',panel:0}),
 cw16Row('CW3-W03','COLE','Come here, you genius!',{tag:'prototypes',cw16:'workshop',panel:1}),
 cw16Row('CW3-W04','DECKER',"Easy now, I'm not trying to file a restraining order these days!",{tag:'prototypes',cw16:'workshop',panel:2}),
 cw16Row('CW3-W05','COLE','When can I test it out?',{tag:'prototypes',cw16:'workshop',panel:3}),
 cw16Row('CW3-W06','DECKER',"When we find out what caused all of this mayhem. It's still not quite ready yet.",{tag:'prototypes',cw16:'workshop',panel:4}),
 cw16Row('CW3-W07','DECKER',"There's something missing, and I just can't for the life of me figure out what. Or, more importantly, why. I'm usually good at this.",{tag:'prototypes',cw16:'workshop',panel:4}),
 cw16Row('CW3-W08','COLE',"We all trust you, you know? It'll come in time, I'm sure. Anyway, let's get a move on it!",{tag:'prototypes',cw16:'workshop',panel:5})
];
C16_STORY.scenes['post-4']=[
 cw16Row('B401','PILOT',"We found the Federation's prototype attachment suits at the airbase. The launch systems are still intact.",{people:['$pilot','$tech']}),
 cw16Row('POST4-02','TECH',"Good. Those hulls were built to take ordinary aircraft beyond the atmosphere. I've adapted the mounts for our ships.",{people:['$pilot','$tech']}),
 cw16Row('CW4-03','TECH',"The airbase's last uplink confirms it. That distress virus was broadcast from our satellite. Look at the last camera feed.",{people:['$pilot','$tech']}),
 cw16Row('B403','SYSTEM','',{kind:'wide',bank:'satellite-takeover',duration:5.2,action:'satellite',cue:'crackle',cueAt:.4,people:['$pilot','$tech']}),
 cw16Row('POST4-04','PILOT',"So that's what's been sending the orders.",{people:['$pilot','$tech']}),
 cw16Row('POST4-05','TECH',"And its signal is still up there. We have to trace it before it moves again.",{people:['$pilot','$tech']}),
 cw16Row('POST4-06','PILOT','Then we follow it to the source.',{people:['$pilot','$tech']}),
 cw16Row('POST4-07','TECH',"The Federation kits are ready. I'll stay here and keep our relay open. Bring back answers.",{upgrade:4,people:['$pilot','$tech']}),
 cw16Row('POST4-08','FALVA',"We got Granddad's bomber flying. We can handle this.",{people:['falva','lizzie']}),
 cw16Row('POST4-09','LIZZIE',"Granddad's bomber had air outside it.",{people:['falva','lizzie']}),
 cw16Row('POST4-10','PILOT',"One last check. Then we're going up.",{kind:'travel',art:'earth',people:['$pilot','$tech']})
];
C16_STORY.continuity=C16_STORY.continuity.map(t=>/backup power cell|recovered recorder points/i.test(t)?'The restored ice-base network exposes an alien distress virus from a Fury satellite. A launch airbase 500 km east holds the Federation prototype aircraft attachments needed to trace it in orbit.':t);
c16Rows=function(id,p=run.pilot,route=s113Route()){
 const rows=CW16.base.rows.apply(this,arguments);
 for(const b of rows){
  if(id==='post-3')for(const pk of b.people||[])b.fpLocations[pk]=b.tag==='prototypes'?'workshop':'conference';
  if(id==='post-3'&&b.id==='CW3-08'&&p==='maverick')b.text=C16_STORY.scenes['post-3'].find(q=>q.id==='CW3-08').text;
  if(id==='post-4'&&b.upgrade===4&&p==='maverick')b.text="Your Federation space kit is ready. Your homing lasers stay as they are. I'll keep our relay open down here.";
  if(b.service14==='alert')b.c16Cues=[...(b.c16Cues||[]),{name:'groundBombImpact',at:.15}];
  if(b.service14==='takeoff')b.c16Cues=[...(b.c16Cues||[]),{name:'firewallLaunch',at:.12}];
  if(b.cw16){b.duration=Math.max(b.duration,b.text.length/30+3.0+(b.cm3?.readAt||0));b.speechEnd=b.text.length/30+(b.cm3?.readAt||0);}
 }return rows;
};
C16.rows=CM3.rows=FP5.rows=c16Rows;
d1110Keys=function(rows,p=run.pilot){const keys=CW16.base.keys.apply(this,arguments);if(rows.some(b=>b.service14))keys.push(CW16_ART.banks.firewave.key);for(const b of rows)if(b.cw16)keys.push(CW16_ART.banks[b.cw16].key,CM3_ART.banks['caption-0'].key);return[...new Set(keys)];};
function cw16Blit(name,f,box,cover=false){const a=CW16_ART.banks[name];if(!a||!XART.rdy(a.key))return false;f=clamp(Math.floor(f),0,a.frames-1);const[x,y,w,h]=box,k=(cover?Math.max:Math.min)(w/a.w,h/a.h),dw=Math.round(a.w*k),dh=Math.round(a.h*k);ctx.drawImage(XART.get(a.key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,Math.round(x+(w-dw)/2),Math.round(y+(h-dh)/2),dw,dh);return true;}
function cw16PanelTarget(n){return{x:clamp(n%3*490+236-444,0,564),y:Math.floor(n/3)*378};}
function cw16Workshop(b,s){
 const box=[12,12,888,354],n=b.panel||0,prior=s.beats[s.i-1],old=prior?.cw16==='workshop'?prior.panel:n,to=cw16PanelTarget(n),from=cw16PanelTarget(old),t=D1110.static?1:clamp(s.t/1.25,0,1),e=t*t*(3-2*t),camera={x:lerp(from.x,to.x,e),y:lerp(from.y,to.y,e)};
 c16Clip(box,()=>{ctx.fillStyle='#f0d9a5';ctx.fillRect(...box);ctx.save();ctx.translate(-Math.round(camera.x),-Math.round(camera.y));for(let i=0;i<6;i++){const slot=[12+i%3*490,12+Math.floor(i/3)*378,472,354];cw16Blit('workshop',i,slot);const focus=(i===n?e:0)+(i===old?1-e:0);ctx.fillStyle='rgba(8,13,21,'+(Math.max(0,1-focus)*.5)+')';ctx.fillRect(...slot);ctx.strokeStyle='#090b0e';ctx.lineWidth=5;ctx.strokeRect(...slot);}ctx.restore();});sl14Frame(box);
 CW16.last={mode:'workshop',panel:n,previousPanel:old,camera,boardOrder:[0,1,2,3,4,5],wholePanel:true,shot:b.id};
}
function cw16Photon(b,s){const t=Math.max(0,s.t-(b.cm3?.readAt||0)),bounds=[0,.7,1.5,2.5,3.1,4.2,5.3,6.2],f=Math.max(0,bounds.findLastIndex(v=>t>=v)),box=[12,12,888,488];c16Clip(box,()=>{ctx.fillStyle='#171e29';ctx.fillRect(...box);cw16Blit('photon',f,box,true);});sl14Frame(box);CW16.last={mode:'photon',frame:f,shot:b.id,topDown:true,wholeEmitter:true};}
d1110Visual=function(b,s){if(!b.cw16)return CW16.base.visual.apply(this,arguments);ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#080d14';ctx.fillRect(0,0,912,512);if(b.cw16==='photon')cw16Photon(b,s);else{cw16Workshop(b,s);sl14Caption(b,s);}msgFaceUse('dialogue');controlHintRow([['pad_a',s.shown<b.text.length?'READ':'NEXT'],['pad_start','SKIP']],505,723,887,9);msgFaceUse(null);ctx.restore();CW16.last={...CW16.last,text:b.text,who:b.who,time:s.t};D1110.last=CW16.last;};

// The escape is a ground event. The ship has no attached fire/heat ring.
sl14TopDown=function(b,s){
 const box=[12,12,888,354],mode=b.service14,age=sl14HeatAge(s),heat=clamp(age/6,0,1),u=clamp((s.t-.2)/3.8,0,1),e=u*u*(3-2*u),afterHeat=mode!=='heat',settle=mode==='alert'?clamp(s.t/1.3,0,1):afterHeat?1:0;
 const world={x:Number.isFinite(player.x)?player.x:worldWidth()/2,y:Number.isFinite(player.y)?player.y:VH*.78},actors=d1110Active(),terrainW=Math.min(worldWidth(),LS112_ART.levels['2'].w),terrainH=VH,inset=7,anchor={x:456,y:184};
 const zoom=Math.max(afterHeat?lerp(1.9,1.18,settle):lerp(1.18,1.9,clamp(age/4,0,1)),box[2]/(terrainW-inset*2),box[3]/(terrainH-inset*2));
 const left=(anchor.x-box[0])/zoom,right=(box[0]+box[2]-anchor.x)/zoom,top=(anchor.y-box[1])/zoom,bottom=(box[1]+box[3]-anchor.y)/zoom,endShipY=box[1]+box[3]-64*zoom*.5-18-(actors.length-1)*12;
 const viewX=clamp(world.x,left+inset,terrainW-right-inset),viewY=clamp(lerp(world.y,world.y-(endShipY-anchor.y)/zoom,settle),top+inset,terrainH-bottom-inset),shipX=anchor.x+(world.x-viewX)*zoom,shipY=anchor.y+(world.y-viewY)*zoom;
 const danger=mode==='alert'||mode==='takeoff'||mode==='fade',rumble=danger?(mode==='alert'?clamp(s.t/.8,0,1)*3.2:mode==='takeoff'?3.2*(1-.6*u):1.1):0,jitter={x:Math.sin(age*43)*rumble,y:Math.sin(age*61+.8)*rumble*.8};
 const waveProgress=mode==='alert'?clamp(s.t/b.duration,0,1)*.3:mode==='takeoff'?.3+.7*clamp(s.t/4,0,1):mode==='fade'?1:0,waveY=lerp(-54,382,waveProgress),waveFrame=Math.floor(age*12)%8;
 c16Clip(box,()=>{ctx.save();ctx.translate(anchor.x-viewX*zoom+jitter.x,anchor.y-viewY*zoom+jitter.y);ctx.scale(zoom,zoom);drawBG(0);ctx.restore();
  if(danger)cw16Blit('firewave',waveFrame,[box[0]-4,waveY-600,box[2]+8,600]);
  for(let i=0;i<actors.length;i++){const pk=actors[i],x=shipX+(i-(actors.length-1)/2)*94,y=(mode==='takeoff'?lerp(shipY,-160,e):mode==='fade'?-170:shipY)+i*12,size=Math.round(64*zoom*(mode==='takeoff'?1+.12*Math.sin(Math.PI*u):1)),burn=mode==='takeoff'||mode==='fade'?1:mode==='alert'?.7:.28+.18*heat;pt11OpeningShip(pk,age,x,y,size,burn);SL14.last={mode,pilot:run.pilot,actors,world,zoom,heat,ship:{x,y,size,burn},topDown:true,backgroundStage:run.stage,framing:{zoom,viewX,viewY,terrainW,terrainH,inset,visible:{left:viewX-left,right:viewX+right,top:viewY-top,bottom:viewY+bottom},box},groundRumble:{amplitude:rumble,...jitter},fireWave:danger?{frame:waveFrame,y:waveY,progress:waveProgress}:null,shipFireRing:false};}
 });sl14Frame(box);
};

// Give the Stage3 connector and incoming lake the same moving tile phase.
beginStage=function(n){CW16.water={elapsed:0,motion:0,hadLaunch:false,settled:false};return CW16.base.begin.apply(this,arguments);};
drawLaunch=function(dt){if(run.stage===3&&state===GS.LAUNCH){const d=Math.max(0,Math.min(.1,dt||0));CW16.water.elapsed+=d;CW16.water.motion+=Math.max(12,drawLaunch._spd||110)*d*.45;CW16.water.hadLaunch=true;}return CW16.base.launch.apply(this,arguments);};
ls112Bed=function(name,width=worldWidth(),top=viewTopY(),height=viewH(),travel){
 if(run.stage!==3||name!=='water')return CW16.base.bed.apply(this,arguments);
 const a=LS112_ART.materials.water;if(!XART.rdy(a.key))return false;const w=CW16.water;
 if(state!==GS.LAUNCH&&w.hadLaunch&&!w.settled){w.offset=w.motion-efxClock*12;w.timeOffset=w.elapsed-efxClock;w.settled=true;}
 const time=state===GS.LAUNCH&&w.hadLaunch?w.elapsed:Math.max(0,efxClock+(w.timeOffset||0)),f=Math.floor(time*a.fps)%a.frames,motion=Number.isFinite(travel)?travel:state===GS.LAUNCH&&w.hadLaunch?w.motion:efxClock*12+(w.offset||0),x0=Math.floor((camLeftX()*.68)%a.w)-a.w,y0=Math.floor(top+((motion%a.h)+a.h)%a.h)-a.h;
 for(let y=y0;y<top+height;y+=a.h)for(let x=x0;x<width;x+=a.w)ls112Frame(a,f,x,y);
 LS112.clock.bed={name,time,frame:f,x:x0,y:y0,travel:motion};CW16.water.last={time,frame:f,travel:motion,phase:drawLaunch._phase};ls112Count('bed-'+name);return true;
};
connectorSurface=function(stage,joinY,width){if(stage===3&&state===GS.LAUNCH&&ls112Live(3))return ls112Bed('water',Math.max(width||0,VW),0,VH,joinY-VH+CW16.water.motion);return CW16.base.connector.apply(this,arguments);};
Snd.prepare?.(['groundBombImpact','firewallLaunch','bossWeaponCharge','av3_cole_laser7']);
CW16.rows=c16Rows;CW16.preview=(id='post-3',p='cole')=>D1110.preview(id,p);window.BOF_CINEMATIC_REWORK_1114=CW16;
