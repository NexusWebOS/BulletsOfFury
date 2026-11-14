'use strict';
/* Team-room, recovered rotor and private prototype acting. Earned loadouts,
   ranks, saves, difficulty completion, alarms and launches stay native. */
const HQ1110={version:1,base:{post:d1110Post,keys:d1110Keys,primary:cb1110Primary,secondary:cb1110Secondary,readings:cb1110Readings,visual:d1110Visual,tick:BOFCinematicDirector.tick,preview:D1110.preview},last:null,events:[]};
for(const[n,a]of Object.entries(HQ1110_ART.banks)){D1110_ART.banks[n]=a;XART._src[a.key]=a.path;}
Snd.prepare(['blip','av3_cole_laser6','av3_cole_laser7']);
function hq1110Beat(id,duration,who,text,bank,extra={}){return{id,duration,who,text,bank,hq1110:true,d1110:true,art:'comic',layout:'panel',comic:'vertical',people:['cole','decker'],readings:[],delay:.25,times:HQ1110_ART.banks[bank].durations.map((n,i,a)=>i===a.length-1?100000:n),_cueSet:new Set(),...extra};}
function hq1110Conference(){return[
 hq1110Beat('HQ301',5.5,'COLE','All wings accounted for. Everyone around the table. Bring the recorder in.','hq-conference',{hqWide:true}),
 hq1110Beat('HQ302',4.8,'COLE','The airbase is our lead. We recover its launch records and bring that power cell home.','hq-conference',{hqWide:true,clip:[3],times:[100000]})
 ];}
function hq1110Prototypes(){return[
 hq1110Beat('HQ303',5,'COLE','Decker. Before we launch—show me the prototypes.','hq-laser-reveal',{context:'cole'}),
 hq1110Beat('HQ304',5.8,'DECKER','Level Six laser array. Then the Level Seven photon emitter. Both are still in bench trials.','hq-laser-reveal',{clip:[4,5],times:[650,100000],context:'decker',readings:['VI: YELLOW LASER ARRAY','VII: PHOTON EMITTER']}),
 hq1110Beat('HQ305',5.6,'SYSTEM','','hq-laser-demo',{comic:'stack',context:'hq-laser-reveal',contextFrame:5,hqDemo:true,readings:['LAB: ISOLATED TEST','FIELD CLEARANCE: PENDING'],hqCues:[{name:'av3_cole_laser6',at:.91},{name:'av3_cole_laser7',at:2.86}]}),
 hq1110Beat('HQ306',5,'COLE','You built the Photon Cannon? I knew you were hiding something good.','hq-cole-decker-hug',{context:'cole'}),
 hq1110Beat('HQ307',5,'DECKER','Easy, Cole. I still need both hands to finish it.','hq-cole-decker-hug',{clip:[5],times:[100000],context:'decker'}),
 hq1110Beat('HQ308',5.2,'COLE','Clear the mount tests. Keep my prototype line separate from the squad conversions.','hq-laser-reveal',{clip:[5],times:[100000],context:'hq-laser-demo',contextFrame:5,readings:['LAB PROTOTYPES: SECURED','FIELD CLEARANCE: PENDING']})
 ];}
function hq1110Workshop(){return[
 hq1110Beat('HQ501',4.5,'COLE','That gun nearly cut us in half. Show me what you can recover.','hq-chaingun-inspection',{clip:[5],times:[100000],context:'cole'}),
 hq1110Beat('HQ502',3,'FURY HQ','LATER THAT NIGHT','hq-chaingun-inspection',{clip:[5],times:[100000],context:'decker'}),
 hq1110Beat('HQ503',5.6,'DECKER','The rotor checks out. Paired feeds, balanced mounts. We can make this work.','hq-salvage-diagnostics',{context:'hq-chaingun-inspection',contextFrame:5,hqDiagnostic:true,readings:['RECOVERED ROTOR: INTACT','FEED TEST: STABLE'],cue:'blip',cueAt:3.5})
 ];}
d1110Post=function(n,p=run.pilot,route=s113Route()){const rows=HQ1110.base.post(n,p,route);if(n===3){const conference=hq1110Conference(),out=[];for(const b of rows){if(b.id==='B307')out.push(...hq1110Prototypes());out.push(b);if(b.id==='B301')out.push(conference[0]);if(b.id==='B305')out.push(conference[1]);}return out;}
 if(n===5){const out=[];for(const b of rows){if(b.id==='B503'){out.push({...b,hq1110:true,bank:'hq-chaingun-inspection',clip:undefined,times:[650,650,650,650,650,100000],delay:.25,comic:'vertical',context:'decker',people:['decker'],readings:['SALVAGE: CHRONOS ROTOR','SAFETY: FEED DISCONNECTED']},...hq1110Workshop());}
  else if(b.id==='B504')out.push({...b,hq1110:true,bank:'hq-heavy-metal',clip:undefined,times:[600,600,650,650,650,100000],delay:.25,comic:'backslash',context:'juggernaut',people:['juggernaut','decker']});else out.push(b);}return out;}
 return rows;};
s113Script=d1110Post;BOFCinematicDirector.script=d1110Post;BOFCampaignStory.script=d1110Post;D1110.script=d1110Post;
d1110Keys=function(rows,p=run.pilot){const keys=HQ1110.base.keys(rows,p);for(const b of rows){if(!b.hq1110)continue;if(HQ1110_ART.banks[b.context])keys.push(HQ1110_ART.banks[b.context].key);if(D1110.pilots.includes(b.context))keys.push(D1110_ART.banks['face-'+b.context].key);for(const pk of b.people||[])if(D1110.pilots.includes(pk))keys.push(D1110_ART.banks['face-'+pk].key);}return[...new Set(keys)];};
function hq1110Fit(name,f,box){const a=D1110_ART.banks[name],[x,y,w,h]=box,k=Math.min(w/a.w,h/a.h);d1110Bank(name,f,Math.round(x+(w-a.w*k)/2),Math.round(y+(h-a.h*k)/2),Math.round(a.w*k),Math.round(a.h*k));}
cb1110Primary=function(b,s,box){if(!b.hq1110)return HQ1110.base.primary(b,s,box);d1110Plate({art:'comic'},s.t);hq1110Fit(b.bank,d1110Frame(b,s.t),box);HQ1110.last={shot:b.id,bank:b.bank,frame:d1110Frame(b,s.t),pilot:run.pilot,wide:false};};
cb1110Secondary=function(b,s,box,index=1){if(!b.hq1110)return HQ1110.base.secondary(b,s,box,index);
 if(index===1&&HQ1110_ART.banks[b.context]){hq1110Fit(b.context,b.contextFrame||0,box);return;}
 const face=index===2?'cole':D1110.pilots.includes(b.context)?b.context:(b.who==='COLE'?'cole':'decker');cb1110Face(face,box,s.t,b.who===face.toUpperCase()&&s.shown<b.text.length);
};
cb1110Readings=function(b,t){if(!b.hq1110)return HQ1110.base.readings(b,t);let rows=b.readings;if(b.hqDemo){const f=d1110Frame(b,t);rows=[['VI: YELLOW ARRAY','INTERLOCK: CLOSED'],['VI: TEST PULSE','COIL OUTPUT: STABLE'],['VI: TEST COMPLETE','EMITTER: STANDBY'],['VII: PHOTON EMITTER','INTERLOCK: CLOSED'],['VII: TEST PULSE','COIL OUTPUT: STABLE'],['LAB PROTOTYPES: SECURED','FIELD CLEARANCE: PENDING']][f];}
 if(b.hqDiagnostic)rows=[['SALVAGE TEST: BASELINE','READER: ISOLATED'],['ROTOR RESPONSE: FOUND','PICKUP: TRACKED'],['FEED RESPONSE: MATCHED','SIGNAL: STABLE'],['PAIRED MOUNTS: TESTING','LOAD: BALANCED'],['PAIRED MOUNTS: MATCHED','FEED: STABLE'],['SALVAGE: VERIFIED','CONVERSION: READY']][d1110Frame(b,t)];
 if(!rows?.length)return;const x=b.comic==='stack'?552:532,y=b.comic==='stack'?144:300,w=b.comic==='stack'?352:368;ui20Panel('',x,y,w,90,false);msgFaceUse('dialogue');rows.forEach((text,i)=>msgText(text,x+w/2,y+38+i*22,11,'#c6f5ea',1,1,.04));msgFaceUse(null);
};
function hq1110Perimeter(h){const a=D1110_ART.banks[cb1110Gutter('vertical',h)];if(!XART.rdy(a.key))return;const im=XART.get(a.key);for(const q of [[0,0,912,16],[0,h-16,912,16],[0,16,16,h-32],[896,16,16,h-32]])ctx.drawImage(im,...q,...q);}
d1110Visual=function(b,s){if(!b.hqWide)return HQ1110.base.visual(b,s);const h=b.text?398:484;ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#03070d';ctx.fillRect(0,0,912,512);
 cb1110Clip({pts:[[12,12],[900,12],[900,h-12],[12,h-12]],box:[12,12,888,h-24]},box=>cb1110Cover(b.bank,d1110Frame(b,s.t),box,.08));hq1110Perimeter(h);cb1110Caption(b,s);ctx.restore();
 D1110.last={id:s.id,shot:b.id,pilot:run.pilot,coOp:d1110Active(),bank:b.bank,frame:d1110Frame(b,s.t),time:s.t,who:b.who,comic:'wide'};CB1110.last={...D1110.last,panels:1};HQ1110.last={...D1110.last,wide:true,cast:HQ1110_ART.cast};
};
BOFCinematicDirector.tick=function(dt){const s=this.current,b=s?.beats[s.i],previous=s?.t;const result=HQ1110.base.tick.apply(this,arguments);if(b?.hqCues&&this.current===s&&s.beats[s.i]===b)for(const q of b.hqCues)d1110Cue(s,b,q.name,q.at,previous);return result;};
function hq1110PreviewRows(id,p){const n=id==='hq-workshop'?5:3,rows=d1110Post(n,p);return rows.filter(b=>id==='hq-briefing'?['HQ301','B302','B303','B304','B305','HQ302'].includes(b.id):id==='hq-prototypes'?['HQ303','HQ304','HQ305','HQ306','HQ307','HQ308'].includes(b.id):['B503','HQ501','HQ502','HQ503','B504'].includes(b.id)||String(b.id).startsWith('upgrade-5-'));}
D1110.preview=S113.preview=async function(id,p='cole',route='left',partner=null){if(['hq-briefing','hq-prototypes','hq-workshop'].includes(id)){
 BOFCinematicDirector.cancel();run.pilot=p;pilotIndex=PILOTS.findIndex(q=>q.key===p);run.mode='campaign';coopOn=D1110.pilots.includes(partner)&&partner!==p;if(coopOn){run2.pilot=partner;p2Index=PILOTS.findIndex(q=>q.key===partner);}Input.clearTaps();return d1110Play('review-'+id,hq1110PreviewRows(id,p),()=>setState(GS.TITLE));}
 return HQ1110.base.preview(id,p,route,partner);};
HQ1110.conference=hq1110Conference;HQ1110.prototypes=hq1110Prototypes;HQ1110.workshop=hq1110Workshop;window.BOF_HQ_CINEMA_1110=HQ1110;
