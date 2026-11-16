'use strict';
/* Dedicated 3->4 and 6->7 story/arrival sequences. Native map, optional pursuit,
   rewards, save and stage-launch owners remain in charge of continuation. */
const BR1110={version:1,base:{post:d1110Post,keys:d1110Keys,primary:cb1110Primary,secondary:cb1110Secondary,readings:cb1110Readings,play:BOFCinematicDirector.play,launch:drawLaunch,load:stageLoadBegin,startRun,preview:D1110.preview},last:null,events:[],intercepting:false};
for(const[n,a]of Object.entries(BR1110_ART.banks)){D1110_ART.banks[n]=a;CB1110_ART.banks[n]=a;XART._src[a.key]=a.path;}
function br1110Beat(p,id,duration,who,text,extra={}){return{id,duration,who:d1110Who(who,p),text:d1110Resolve(text,p,s113Route()),d1110:true,bridge:true,art:'comic',layout:'panel',people:[],readings:[],comic:'slash',_cueSet:new Set(),...extra};}
function br1110Anim(name,extra={}){return{bank:'bridge-'+name,times:BR1110_ART.banks['bridge-'+name].durations.map((v,i)=>i===5?100000:v),...extra};}
function br1110Post3(p){const L=(...v)=>br1110Beat(p,...v);return[
 L('B301',5.5,'PILOT','HQ, the ice relay is silent. We have its recorder. Clear the bay.',{art:'hangar',layout:'flight',ship:'land',comic:'stack',context:'pilot'}),
 L('B302',5.6,'SYSTEM','',{...br1110Anim('relay-recorder'),comic:'vertical',context:'bridge-launch-correlation',contextFrame:0}),
 L('B303',5.5,'DECKER','A cached routing header. Local reader only; nothing goes back onto the network.',{...br1110Anim('relay-recorder',{clip:[5],times:[100000]}),readings:['READER: ISOLATED','RELAY CACHE: RECOVERED'],context:'bridge-launch-correlation',contextFrame:1}),
 L('B304',6.5,'COLE','Compare that launch marker with the first outages.',{...br1110Anim('launch-correlation'),comic:'stack',context:'bridge-relay-recorder',contextFrame:5,scan:'launch',cue:'blip',cueAt:2.4,readings:['LAUNCH MARKER: FOUND','FIRST OUTAGE: LATER']}),
 L('B305',5.5,'DECKER','The airbase is twenty miles east. Its independent power cell is still feeding the pad.',{...br1110Anim('airbase-recon'),comic:'backslash',context:'bridge-launch-correlation',contextFrame:5,readings:['AIRBASE: 20 MILES EAST','LOCAL POWER: PRESENT']}),
 L('B306',5.5,'DECKER','Bring that cell back intact. We need it for the launch generator.',{...br1110Anim('relay-recorder',{clip:[5],times:[100000]}),comic:'vertical',context:'bridge-airbase-recon',contextFrame:5}),
 L('B307',6,'COLE','We recover the launch records, secure the cell, and find out what left that pad.',{...br1110Anim('airbase-recon',{clip:[5],times:[100000]}),comic:'slash',context:'pilot',plan:true,readings:['NEXT SORTIE: AIRBASE','FLIGHT PLAN: COMPILED']})
];}
function br1110Post6(p,route){const L=(...v)=>br1110Beat(p,...v),report=route==='left'?'The Harrier is down. The remaining Rough Rider contacts are marked.':'The Rough Riders are down. The remaining Harrier threat is marked.';return[
 L('B601',6,'TECH',report,{art:'earth-approach',ship:'return',layout:'flight',comic:'slash',context:'remaining',route,readings:['ROUTE THREAT: CLEARED','REMAINING CONTACTS: MARKED']}),
 L('B602',5.5,'COLE','All wings, check in. Bring the recorders to the analysis bench.',{art:'hangar',ship:'land',layout:'flight',comic:'stack',context:'pilot'}),
 L('B603',6,'COLE','Keep the remaining contact on the board. Decker, show me the signal that never left.',{...br1110Anim('subsurface-analysis'),comic:'backslash',context:'bridge-subsurface-scan',contextFrame:0}),
 L('B604',5.5,'DECKER','Nothing at flying altitude. Run the lower band.',{...br1110Anim('subsurface-scan',{clip:[0,1,2],times:[700,700,100000]}),comic:'vertical',context:'bridge-subsurface-analysis',contextFrame:2,readings:['AIR SCAN: NO MATCH','SEARCH PLANE: SUBSURFACE']}),
 L('B605',6.5,'DECKER','There. Below the riverbed. The pulse repeats inside a drainage line beneath the bridge.',{...br1110Anim('subsurface-scan',{clip:[2,3,4,5],times:[800,900,950,100000]}),comic:'stack',context:'bridge-subsurface-analysis',contextFrame:5,scan:'subsurface',cue:'blip',cueAt:3,readings:['SIGNAL: REPEATING','ORIGIN: BELOW RIVERBED']}),
 L('B606',5.5,'COLE','An air search was never going to find it. Mark the lower access.',{...br1110Anim('river-recon'),comic:'slash',context:'bridge-subsurface-scan',contextFrame:5,readings:['ACCESS: NORTH OF BRIDGE','APPROACH: RIVER CORRIDOR']}),
 L('B607',5.5,'TECH','The surviving air threat stays marked for pursuit. The underground source is a separate lead.',{...br1110Anim('subsurface-analysis',{clip:[5],times:[100000]}),comic:'vertical',context:'remaining',route}),
 L('B608',5.5,'PILOT','River approach loaded. Keep the channel open until we go under.',{...br1110Anim('river-recon',{clip:[5],times:[100000]}),comic:'slash',context:'pilot',readings:['NEXT SORTIE: LOWER ACCESS','LOCAL NAVIGATION: READY']})
];}
function br1110Arrival(n,p=run.pilot){const L=(...v)=>br1110Beat(p,...v);return n===4?[
 L('A401',4.8,'TECH','Airbase ahead. Local power is still active.',{...br1110Anim('airbase-recon'),comic:'slash',context:'pilot',flight:'airbase',readings:['AIRBASE: VISUAL CONFIRMED','PAD: INDEPENDENT POWER']}),
 L('A402',4.8,'PILOT','Hangars to the left. The launch pad is on the right.',{...br1110Anim('airbase-recon',{clip:[5],times:[100000]}),comic:'stack',context:'bridge-launch-correlation',contextFrame:5,flight:'airbase-close',readings:['OBJECTIVE: LAUNCH ARCHIVE','RECOVERY: ELECTRICAL CELL']}),
 L('A403',4.5,'COLE','Stay on your local controls. Clear the defenses and recover those records.',{...br1110Anim('airbase-recon',{clip:[5],times:[100000]}),comic:'vertical',context:'pilot',flight:'airbase-close',readings:['REMOTE AUTHORITY: ISOLATED','AIRFRAME: LOCAL CONTROL']})
 ]:[
 L('A701',4.8,'TECH','Follow the river. The signal is on the far side of the iron bridge.',{...br1110Anim('river-recon'),comic:'slash',context:'bridge-subsurface-scan',contextFrame:5,flight:'river-approach',readings:['RIVER CORRIDOR: CONFIRMED','SOURCE: LOWER ACCESS']}),
 L('A702',5.5,'SYSTEM','',{...br1110Anim('river-recon'),comic:'vertical',context:'pilot',flight:'river-bridge',readings:['LOW APPROACH: BRIDGE CLEAR','FORMATION: MAINTAIN SEPARATION']}),
 L('A703',4.5,'PILOT','Taking the lower access. Local navigation stays on. Keep listening for us.',{...br1110Anim('river-recon',{clip:[5],times:[100000]}),comic:'slash',context:'pilot',flight:'river-hold',readings:['LOCAL NAV: ACTIVE','NETWORK RECONNECT: BLOCKED']})
 ];}
d1110Post=function(n,p=run.pilot,route=s113Route()){if(n!==3&&n!==6)return BR1110.base.post(n,p,route);const rows=n===3?br1110Post3(p):br1110Post6(p,route),upgrades=BR1110.base.post(n,p,route).filter(b=>String(b.id).startsWith('upgrade-'));rows.splice(n===3?6:7,0,...upgrades);return rows;};
s113Script=d1110Post;BOFCinematicDirector.script=d1110Post;BOFCampaignStory.script=d1110Post;D1110.script=d1110Post;
d1110Keys=function(rows,p=run.pilot){const keys=BR1110.base.keys(rows,p);for(const b of rows){if(!b.bridge)continue;
 if(D1110_ART.banks[b.context])keys.push(D1110_ART.banks[b.context].key);
 for(const pk of d1110Active(p))keys.push('ship_'+pk);
 if(b.context==='remaining')keys.push(b.route==='left'?null:'whv_closed',...(b.route==='left'?REBEL_SHIPS.map(k=>'rr_ship_'+k):[]));
 }return [...new Set(keys.filter(Boolean))];};
function br1110Rect(a,box,focus=.15){const[x,y,w,h]=box,k=Math.max(w/a.w,h/a.h);return{x:Math.round(x+(w-a.w*k)/2),y:Math.round(y+(h-a.h*k)*focus),k,w:Math.round(a.w*k),h:Math.round(a.h*k)};}
function br1110Jet(pk,x,y,size){const key='ship_'+pk;if(!XART.rdy(key))return;const im=XART.get(key),k=size/Math.max(im.width,im.height);ctx.drawImage(im,Math.round(x-im.width*k/2),Math.round(y-im.height*k/2),Math.round(im.width*k),Math.round(im.height*k));}
cb1110Primary=function(b,s,box){if(!b.bridge||!b.bank)return BR1110.base.primary(b,s,box);
 const f=d1110Frame(b,s.t),a=D1110_ART.banks[b.bank],r=br1110Rect(a,box,b.flight==='river-approach'?1:b.flight?0:.15);d1110Bank(b.bank,f,r.x,r.y,r.w,r.h);
 if(b.flight||b.plan){const active=d1110Active(),duration=b.duration||5;
  active.forEach((pk,i)=>{const u=clamp((s.t-i*.55)/Math.max(1,duration-i*.55),0,1),river=b.bank==='bridge-river-recon';let y;
   if(b.plan)y=250+i*65;
   else if(b.flight==='river-bridge')y=lerp(355+i*65,130+i*60,u);
   else if(b.flight==='river-hold')y=lerp(154+i*70,78+i*70,u);
   else if(b.flight==='river-approach')y=lerp(440+i*65,350+i*65,u);
   else y=lerp(b.flight==='airbase-close'?280:360,b.flight==='airbase-close'?180:200,u)+i*65;
   br1110Jet(pk,r.x+256*r.k,r.y+y*r.k,112*r.k);
  });
  if(b.bank==='bridge-river-recon'){const im=XART.get(a.key),sx=f%a.cols*a.w,sy=Math.floor(f/a.cols)*a.h;
   for(const q of [[0,190,512,115],[0,0,512,55]])ctx.drawImage(im,sx+q[0],sy+q[1],q[2],q[3],r.x+q[0]*r.k,r.y+q[1]*r.k,q[2]*r.k,q[3]*r.k);
  }
 }
 BR1110.last={shot:b.id,bank:b.bank,frame:f,pilots:d1110Active(),flight:b.flight||null,plan:!!b.plan,bridgeOcclusion:b.bank==='bridge-river-recon'&&!!b.flight};
};
cb1110Secondary=function(b,s,box,index=1){if(!b.bridge)return BR1110.base.secondary(b,s,box,index);
 const[x,y,w,h]=box;
 if(index===2){cb1110Face(d1110Tech(),box,s.t,false);return;}
 if(b.context==='remaining'){
  const keys=b.route==='left'?REBEL_SHIPS.map(k=>'rr_ship_'+k):['whv_closed'];
  keys.forEach((key,i)=>{if(!XART.rdy(key))return;const im=XART.get(key),size=keys.length===1?Math.min(250,w*.72,h*.7):Math.min(92,w*.24),k=size/Math.max(im.width,im.height),cx=keys.length===1?x+w/2:x+w*(.18+i%3*.32),cy=keys.length===1?y+h*.43:y+h*(i<3?.24:.55);ctx.drawImage(im,Math.round(cx-im.width*k/2),Math.round(cy-im.height*k/2),Math.round(im.width*k),Math.round(im.height*k));});
  msgFaceUse('dialogue');msgText('REMAINING AIR CONTACT',x+w/2,y+22,11,'#e5d3a6',1,1,.04);msgFaceUse(null);return;
 }
 if(D1110_ART.banks[b.context]){cb1110Cover(b.context,b.contextFrame||0,box,.15);return;}
 const pk=index===1?run.pilot:d1110Tech();cb1110Face(pk,box,s.t,b.who===pk.toUpperCase()&&s.shown<b.text.length);
};
cb1110Readings=function(b,t){if(!b.bridge)return BR1110.base.readings(b,t);const f=b.bank?d1110Frame(b,t):0,rows=!b.scan?b.readings:b.scan==='launch'?[['RELAY CACHE: OPEN','TIMELINE: LOADING'],['LAUNCH: EARLIER','FIRST OUTAGE: LATER'],['LAUNCH: EARLIER','FIRST OUTAGE: LATER'],['AIRBASE: IDENTIFIED','VECTOR: EAST'],['LOCAL POWER: PRESENT','AIRBASE: 20 MILES EAST'],['FLIGHT PLAN: READY','AIRBASE: 20 MILES EAST']][f]:f<3?['LOWER BAND: SCANNING','AIR SCAN: NO MATCH']:f<5?['SUBSURFACE PULSE: REPEATING','ORIGIN: BELOW RIVERBED']:['SOURCE: LOWER DRAIN','ACCESS: NORTH OF BRIDGE'];
 if(!rows?.length)return;ui20Panel('',532,300,368,90,false);msgFaceUse('dialogue');rows.forEach((text,i)=>msgText(text,716,338+i*23,11,'#c6f5ea',1,1,.04));msgFaceUse(null);
};
BOFCinematicDirector.play=function(id,rows,done,live=false){if(id==='stage7-approach'&&!BR1110.intercepting&&run.mode==='campaign'){
 BR1110.intercepting=true;try{return d1110Play(id,br1110Arrival(7),done);}finally{BR1110.intercepting=false;}
 }return BR1110.base.play.call(this,id,rows,done,live);};
drawLaunch=function(dt){if(run.mode==='campaign'&&run.stage===4&&state===GS.LAUNCH&&!run._bridgeArrival4&&!debugFight&&!tutLive()){
 run._bridgeArrival4=true;if(d1110Play('stage4-approach',br1110Arrival(4),()=>{setState(GS.LAUNCH);})) {BR1110.events.push({event:'stage4-approach'});return;}run._bridgeArrival4=false;
 }return BR1110.base.launch.apply(this,arguments);};
startRun=function(){run._bridgeArrival4=false;return BR1110.base.startRun.apply(this,arguments);};
stageLoadBegin=function(n,keys){const extra=[4,7].includes(n)?d1110Keys(br1110Arrival(n)):[];return BR1110.base.load.call(this,n,[...(keys||[]),...extra]);};
D1110.preview=S113.preview=async function(id,p='cole',route='left',partner=null){if(id==='arrival-4'||id==='arrival-7'){
 BOFCinematicDirector.cancel();run.pilot=p;pilotIndex=PILOTS.findIndex(q=>q.key===p);run.mode='campaign';coopOn=D1110.pilots.includes(partner)&&partner!==p;if(coopOn){run2.pilot=partner;p2Index=PILOTS.findIndex(q=>q.key===partner);}Input.clearTaps();return d1110Play('review-'+id,br1110Arrival(Number(id.slice(-1)),p),()=>setState(GS.TITLE));
 }return BR1110.base.preview(id,p,route,partner);};
BR1110.post3=br1110Post3;BR1110.post6=br1110Post6;BR1110.arrival=br1110Arrival;window.BOF_BRIDGES_1110=BR1110;
