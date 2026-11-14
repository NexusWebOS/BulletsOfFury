'use strict';
/* Authored comic gutters and nine reference-driven space reels. The live
   Chronos clocks, missile impact, breakup, saves and rewards retain their owners. */
const CB1110={version:1,revision:2,styles:['vertical','slash','backslash','stack','triptych','impact'],last:null,
 base:{visual:d1110Visual,keys:d1110Keys,post:d1110Post,endingDraw:h3EndingDraw,warm:hf17Warm,load:stageLoadBegin},draws:{}};
for(const [name,a]of Object.entries(CB1110_ART.banks)){D1110_ART.banks[name]=a;XART._src[a.key]=a.path;}
function cb1110Space(pk){return 'space-'+pk+'-finisher';}
function cb1110Gutter(style,h){return 'comic-'+style+'-'+h;}
function cb1110Style(b,i=0){if(b.comic)return b.comic;return CB1110.styles[i%CB1110.styles.length];}
function cb1110Decorate(n,rows,p){return rows.map((raw,i)=>{const b={...raw,readings:[...(raw.readings||[])],people:[...(raw.people||[])]};
 b.comic=cb1110Style(b,i+n);if(b.readings.length&&b.comic==='triptych')b.comic='stack';b.chapter='AFTER STAGE '+n;
 if(n===5){
  if(b.id==='B501'){b.art='earth-approach';b.ship='return';b.text='Fury HQ, we have the salvage. Beginning our approach.';b.readings=['SPACE ARMOR: DISENGAGED','HQ APPROACH: CLEARED'];b.comic='slash';}
  if(b.id==='B502'){b.comic='stack';b.text='Bring it in. The hangar is clear.';}
  if(b.id==='B503'){b.comic='backslash';b.text='The rotary assembly survived. Set it on the bench; I can rebuild this.';}
  if(b.id==='B504')b.comic='triptych';
  if(b.id==='B505')b.comic='stack';
  if(b.id==='B506'){b.comic='impact';b.text=d1110Resolve('[Guard names], hold HQ. Flight wing, scramble for the city.',p);}
  if(b.id==='B507'){b.comic='slash';b.squad=true;
   if(nf100Ends()){b.ship='board';b.art='hangar';b.squad=false;b.who='COLE';b.text='Hold on standby. We have won this battle. The war is still out there.';b.cue=null;b.readings=['FLIGHT: ON STANDBY'];}
  }
 }
 if(n===9&&b.id==='Q02'){b.bank=cb1110Space(p);b.clip=[5];b.times=[100000];b.hold=5;b.ship=null;b.layout='panel';b.comic='vertical';b.spaceExit=true;}
 return b;});}
d1110Post=function(n,p=run.pilot,route=s113Route()){return cb1110Decorate(n,CB1110.base.post(n,p,route),p);};
s113Script=d1110Post;BOFCinematicDirector.script=d1110Post;BOFCampaignStory.script=d1110Post;D1110.script=d1110Post;
d1110Keys=function(rows,p=run.pilot){const keys=CB1110.base.keys(rows,p);
 for(const b of rows){if(!b.comic)continue;const h=b.text?398:484;keys.push(D1110_ART.banks[cb1110Gutter(b.comic,h)].key);
  if(CB1110_ART.banks[b.art])keys.push(CB1110_ART.banks[b.art].key);
  if(b.spaceExit)for(const pk of d1110Active(p))keys.push(D1110_ART.banks[cb1110Space(pk)].key);
  for(const pk of [...new Set([p,d1110Tech(p),...d1110People(b),...(b.squad?d1110Crew(p).flying:[])])])for(const name of ['face-'+pk,'native-'+pk+'-front','native-'+pk+'-rear'])keys.push(D1110_ART.banks[name].key);
  for(const name of ['command-work','radar-acquisition','cole-decker-homecoming','satellite-takeover','decker-reaction'])keys.push(D1110_ART.banks[name].key);
 }
 return [...new Set(keys)];};
function cb1110WarmSpace(p=run.pilot){const keys=d1110Active(p).map(pk=>D1110_ART.banks[cb1110Space(pk)].key);
 for(const h of [398,484])for(const style of ['slash','impact','stack'])keys.push(D1110_ART.banks[cb1110Gutter(style,h)].key);
 keys.push('nbret_'+p);let ready=true;for(const k of keys)if(!XART.rdy(k))ready=false;return ready;}
hf17Warm=function(){const native=CB1110.base.warm.apply(this,arguments),comic=cb1110WarmSpace();return native&&comic;};
stageLoadBegin=function(n,keys){const added=n===5?d1110Active().map(pk=>D1110_ART.banks[cb1110Space(pk)].key):[];return CB1110.base.load.call(this,n,[...(keys||[]),...added]);};
function cb1110Panels(style,h){const M=h/2;
 const poly=(pts,box)=>({pts,box});
 if(style==='slash'||style==='backslash'||style==='impact'){
  const a=style==='backslash'?438:style==='impact'?600:566,b=style==='backslash'?566:style==='impact'?460:438;
  const left=poly([[0,0],[a,0],[b,h],[0,h]],[0,0,Math.max(a,b),h]);
  if(style==='impact'){const y0=h*.46,y1=h*.59,x0=a+(b-a)*.5;return[left,poly([[a,0],[912,0],[912,y1],[x0,y0]],[Math.min(a,b),0,912-Math.min(a,b),h*.59]),poly([[x0,y0],[912,y1],[912,h],[b,h]],[Math.min(a,b),h*.46,912-Math.min(a,b),h*.54])];}
  return[left,poly([[a,0],[912,0],[912,h],[b,h]],[Math.min(a,b),0,912-Math.min(a,b),h])];
 }
 if(style==='stack')return[poly([[0,0],[552,0],[552,h],[0,h]],[0,0,552,h]),poly([[552,0],[912,0],[912,M],[552,M]],[552,0,360,M]),poly([[552,M],[912,M],[912,h],[552,h]],[552,M,360,M])];
 if(style==='triptych')return[poly([[0,0],[314,0],[258,h],[0,h]],[0,0,314,h]),poly([[314,0],[648,0],[706,h],[258,h]],[258,0,448,h]),poly([[648,0],[912,0],[912,h],[706,h]],[648,0,264,h])];
 return[poly([[0,0],[514,0],[514,h],[0,h]],[0,0,514,h]),poly([[514,0],[912,0],[912,h],[514,h]],[514,0,398,h])];
}
function cb1110Clip(slot,fn){ctx.save();ctx.beginPath();slot.pts.forEach((q,i)=>i?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1]));ctx.closePath();ctx.clip();try{fn(slot.box);}finally{ctx.restore();}}
function cb1110Cover(name,frame,box,focus=.35){const a=D1110_ART.banks[name];if(!a||!XART.rdy(a.key))return;
 const [x,y,w,h]=box,k=Math.max(w/a.w,h/a.h),dw=a.w*k,dh=a.h*k;d1110Bank(name,frame,Math.round(x+(w-dw)/2),Math.round(y+(h-dh)*focus),Math.round(dw),Math.round(dh));}
function cb1110Face(pk,box,t,speaking){const[x,y,w,h]=box,size=Math.min(384,Math.max(180,Math.min(w,h+30)));d1110Face(pk,Math.round(x+w/2-size/2),Math.round(y+Math.max(-12,(h-size)/2)),t,speaking,size);}
function cb1110Jet(pk,view,box,size=256){const[x,y,w,h]=box;d1110Native(pk,view,Math.round(x+w/2),Math.round(y+h*.48),Math.min(size,w*.86,h*1.3));}
function cb1110Flight(b,s,box){const t=s.t,u=D1110.static?.6:clamp(t/(b.duration||6),0,1),[x,y,w,h]=box;
 const active=d1110Active(),ground=b.ship==='land'||b.ship==='board',takeoff=b.ship==='launch';
 active.forEach((p,i)=>{const off=(i-(active.length-1)/2)*(active.length>1?150:0),cx=x+w/2+off,cy=y+(ground?.56:takeoff?lerp(.75,.10,u):lerp(.70,.40,u))*h;
  if(ground)d1110Plane(p,b.ship==='board'?5:Math.min(5,Math.floor(u*6)),cx,cy,Math.min(290,w*.66));
  else if(takeoff)d1110Native(p,'rear',cx,cy,Math.min(250,w*.52));else d1110Native(p,'front',cx,cy,Math.min(280,w*.58));
 });
}
function cb1110Primary(b,s,box){const t=s.t,people=d1110People(b);
 if(b.bank){cb1110Cover(b.bank,d1110Frame(b,t),box,.22);return;}
 if(b.layout==='duo'||b.layout==='trio'){d1110Plate({...b,art:'comic'},t);cb1110Face(people[0]||run.pilot,box,t,b.who===(people[0]||'').toUpperCase()&&s.shown<b.text.length);return;}
 if(CB1110_ART.banks[b.art])cb1110Cover(b.art,0,box,.4);else d1110Plate(b,t);if(b.layout==='flight'||b.ship)cb1110Flight(b,s,box);
 if(b.portal){const a=C22_ART.banks.blue_portal,f=Math.floor(t*a.fps)%a.frames;if(XART.rdy(a.key))ctx.drawImage(XART.get(a.key),f%a.columns*a.w,Math.floor(f/a.columns)*a.h,a.w,a.h,110,18,344,344);}
}
function cb1110Secondary(b,s,box,index=1){const t=s.t,people=d1110People(b),p=run.pilot;
 if(b.spaceExit){const pk=d1110Active().find(k=>k!==p);if(pk){const[x,y,w]=box;d1110Bank(cb1110Space(pk),5,x+(w-300)/2,y+4,300,300);}else cb1110Face(p,box,t,false);return;}
 if(b.squad){const flying=d1110Crew().flying.filter(pk=>!d1110Active().includes(pk)),[x,y,w,h]=box;flying.forEach((pk,i)=>{const cx=x+w*(.47+(i%2)*.35),cy=y+h*(i<2?.31:.70);d1110Native(pk,'rear',cx,cy,Math.min(126,h*.36));msgFaceUse('dialogue');msgText(pk.toUpperCase(),cx,cy+43,10,'#e1e4d6',1,1,.04);msgFaceUse(null);});return;}
 if(b.layout==='duo'||b.layout==='trio'){
  if(people[index]){cb1110Face(people[index],box,t,b.who===people[index].toUpperCase()&&s.shown<b.text.length);return;}
  cb1110Jet(p,'front',box);return;
 }
 if(index===2){if(b.bank==='radar-acquisition'||b.bank==='command-work')cb1110Face(d1110Tech(),box,t,false);else cb1110Jet(p,'front',box);return;}
 const context={'command-work':'radar-acquisition','radar-acquisition':'command-work','satellite-takeover':'decker-reaction','decker-reaction':'satellite-takeover','service-connector':'command-work','cole-decker-homecoming':'command-work'}[b.bank];
 if(context){cb1110Cover(context,context==='satellite-takeover'?5:0,box,.15);return;}
 if(b.ship||b.layout==='flight'){const pk=index===2?d1110Tech():p;if(index===2||b.readings?.length)cb1110Face(pk,box,t,false);else cb1110Jet(pk,'front',box);return;}
 if(index===2){cb1110Jet(p,'front',box);return;}
 const who=(b.who||'').toLowerCase();cb1110Face(D1110.pilots.includes(who)?who:d1110Tech(),box,t,false);
}
function cb1110Caption(b,s){if(b.text){msgFaceUse('dialogue');const r=ui20Panel(b.who,20,402,872,90,false);if(r){const content=ui20PanelContents(b.who,b.text,s.shown,null,r,14,13);D1110.caption={text:b.text,shown:s.shown,frame:r,content};}msgFaceUse(null);}
 msgFaceUse('dialogue');controlHintRow([['pad_a',s.shown<b.text.length?'REVEAL':'NEXT'],['pad_start','SKIP SCENE']],500,456,870,14);msgFaceUse(null);}
function cb1110Readings(b,t){if(!b.readings?.length)return;ui20Panel('',532,300,368,90,false);d1110Readings(b,t);}
d1110Visual=function(b,s){if(b.cbFinisher){const t=b.cbFinisher==='missile'?s.t*.5:s.t;cb1110ChronosDraw(CB1110.makePreview(b.cbFinisher,t));cb1110Caption(b,s);D1110.last={...CB1110.last,shot:b.id,id:s.id};return;}if(!b.comic)return CB1110.base.visual(b,s);
 const h=b.text?398:484,slots=cb1110Panels(b.comic,h);D1110.visualH=h;
 ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#03070d';ctx.fillRect(0,0,912,512);
 slots.forEach((slot,i)=>cb1110Clip(slot,box=>i===0?cb1110Primary(b,s,box):cb1110Secondary(b,s,box,i)));
 d1110Bank(cb1110Gutter(b.comic,h),0,0,0);cb1110Readings(b,s.t);cb1110Caption(b,s);ctx.restore();
 D1110.last={id:s.id,shot:b.id,pilot:run.pilot,coOp:d1110Active(),bank:b.bank||null,frame:b.bank?d1110Frame(b,s.t):null,time:s.t,who:b.who,readings:b.readings,ship:b.ship||b.layout==='flight',comic:b.comic};
 CB1110.last={...D1110.last,panels:slots.length};CB1110.draws[b.comic]=(CB1110.draws[b.comic]||0)+1;
};
function cb1110FinisherFrame(F){if(['drain','pulse','lock'].includes(F.phase))return 0;if(F.phase==='missile')return F.t/F.flight<.5?1:2;if(F.phase==='engulf')return F.t<.28?3:4;if(F.phase==='burst')return F.t<.8?4:5;return 5;}
function cb1110ChronosDraw(e){const F=e.hf17,pk=run.pilot,frame=cb1110FinisherFrame(F),line=F.phase==='drain'?SM10_LAST_WORDS[F.line]:'',h=line?398:484,style=['engulf','burst'].includes(F.phase)?'impact':'slash',slots=cb1110Panels(style,h);
 d1110Viewport();ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#03070d';ctx.fillRect(0,0,912,512);
 cb1110Clip(slots[0],box=>cb1110Cover(cb1110Space(pk),frame,box,.25));
 cb1110Clip(slots[1],()=>{ctx.save();ctx.translate(724,190);ctx.scale(1.4,1.4);ctx.translate(-F.core.x,-F.core.y);hf17Actor(e);if(['lock','missile'].includes(F.phase))drawBossRetina(e.boss,F.core.x,F.core.y,F.phase==='lock'?(1-clamp(F.t/1.15,0,1))*TAU:0,1);if(F.phase==='missile')hf17Missile(F);ctx.restore();});
 if(slots[2])cb1110Clip(slots[2],box=>{const partners=d1110Active().filter(p=>p!==pk);if(partners.length)cb1110Cover(cb1110Space(partners[0]),frame,box,.15);else cb1110Face(pk,box,F.age,false);});
 d1110Bank(cb1110Gutter(style,h),0,0,0);
 ui20Panel('',560,h-70,334,58,false);msgFaceUse('dialogue');msgText('CHRONOS / FINAL SHOT',230,30,13,'#e6e4cf',1,1,.04);msgText({drain:'CORE POWER: DRAINING',pulse:'ENERGY SIGNATURE: RISING',lock:'RETINA: CORE LOCK',missile:'MISSILE AWAY',engulf:'CORE IMPACT',burst:'CORE SIGNAL: ZERO'}[F.phase]||'EARTHBOUND',727,h-40,12,'#bdeee3',1,1,.04);msgFaceUse(null);
 if(line)cb1110Caption({who:'CHRONOS',text:line},{shown:F.shown});ctx.restore();
 CB1110.last={id:'chronos-finisher',pilot:pk,bank:cb1110Space(pk),frame,phase:F.phase,comic:style,impacts:F.impacts,coOp:d1110Active()};
}
h3EndingDraw=function(){const e=H3.ending,F=e?.hf17;if(!F)return CB1110.base.endingDraw.apply(this,arguments);
 if(F.phase!=='after')return cb1110ChronosDraw(e);
 if(['welcome','descent'].includes(e.phase)){
  d1110Viewport();const slots=cb1110Panels('slash',484);ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#03070d';ctx.fillRect(0,0,912,512);cb1110Clip(slots[0],box=>cb1110Cover(cb1110Space(run.pilot),5,box));
  cb1110Clip(slots[1],box=>{const im=XART.get('h3_earth');if(im){const[x,y,w,h]=box;ctx.drawImage(im,x+12,y+45,w-24,(w-24)*im.height/im.width);}cb1110Jet(run.pilot,'front',[box[0],260,box[2],200],150);});
  d1110Bank(cb1110Gutter('slash',484),0,0,0);msgFaceUse('dialogue');msgText('EARTHBOUND / SPACE ARMOR RELEASE',456,464,13,'#bdeee3',1,1,.04);msgFaceUse(null);ctx.restore();CB1110.last={id:'chronos-return',pilot:run.pilot,bank:cb1110Space(run.pilot),frame:5,phase:e.phase,comic:'slash'};return;
 }
 return CB1110.base.endingDraw.apply(this,arguments);
};
CB1110.makePreview=function(phase='missile',t=.2){const F={phase,t,age:20+t,flight:.8,from:{x:240,y:350},anchor:{x:240,y:170},core:{x:240,y:170},ship:{x:240,y:400},camX:0,impacts:['engulf','burst'].includes(phase)?1:0,line:0,shown:SM10_LAST_WORDS[0].length,blasts:[],blastSerial:0};return {hf17:F,boss:{flash:0,dying:0},sm10:{phase},phase:'hammerFinale'};};
CB1110.previewFinisher=function(p='cole',phase='missile',t=.2,partner=null){run.pilot=p;pilotIndex=PILOTS.findIndex(q=>q.key===p);run.mode='campaign';coopOn=D1110.pilots.includes(partner)&&partner!==p;if(coopOn){run2.pilot=partner;p2Index=PILOTS.findIndex(q=>q.key===partner);}H3.ending=CB1110.makePreview(phase,t);cb1110WarmSpace(p);hf17Warm();return H3.ending;};
const cb1110BasePreview=D1110.preview;
D1110.preview=S113.preview=async function(id,p='cole',route='left',partner=null){pilotIndex=PILOTS.findIndex(q=>q.key===p);if(partner){p2Index=PILOTS.findIndex(q=>q.key===partner);run2.pilot=partner;}
 if(id==='chronos-finisher'){BOFCinematicDirector.cancel();H3.ending=null;run.pilot=p;run.mode='campaign';coopOn=D1110.pilots.includes(partner)&&partner!==p;Input.clearTaps();
  Snd.prepare?.(['retinaCharge','missile','expBig']);
  const rows=[['lock',1.6],['missile',1.6],['engulf',5.2],['burst',5.1]].map(([phase,duration])=>({id:'CHRONOS-'+phase,d1110:true,cbFinisher:phase,art:'comic',bank:cb1110Space(p),duration,text:'',who:'',readings:[],people:[p],comic:phase==='lock'||phase==='missile'?'slash':'impact',cue:{lock:'retinaCharge',missile:'missile',engulf:'expBig',burst:'expBig'}[phase],cueAt:.08,_cueSet:new Set()}));
  const start=performance.now();while(!hf17Warm()){if(performance.now()-start>90000)throw Error('Chronos art is still loading');await new Promise(r=>setTimeout(r,40));}return d1110Play('review-chronos-finisher',rows,()=>setState(GS.TITLE));
 }
 return cb1110BasePreview(id,p,route,partner);};
window.BOF_COMIC_1110=CB1110;
