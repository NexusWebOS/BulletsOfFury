'use strict';
/* Illustrated 16-bit pages, fixed authored mouth cells, human campaign script.
   Native combat, earned equipment, score, saves and continuation retain their owners. */
const C16_STORY=__STORY__;
const C16={version:1,revision:2,last:null,base:{post:d1110Post,clone:d1110Clone,keys:d1110Keys,visual:d1110Visual,step:d1110Step,play:d1110Play,directPlay:BOFCinematicDirector.play,preview:D1110.preview,face:d1110Face,bank:s113Bank},events:[]};
for(const a of Object.values(C16_ART.banks))XART._src[a.key]=a.path+'?v='+a.sha256.slice(0,12);
Snd.prepare(['blip','stage3AtomicSiren','av3_cole_laser6','av3_cole_laser7','warpCharge','warpBurst','jetDash']);
function c16Name(pk){return pk==='juggernaut'?'Juggernaut':pk.charAt(0).toUpperCase()+pk.slice(1);}
function c16Resolve(text,p,route){return String(text||'').replaceAll('$techName',c16Name(d1110Tech(p))).replace('[Guard names]',d1110Crew(p).guards.map(c16Name).join(' and ')).replace('$routeReport',route==='left'?"Harrier's down. But the other contacts are still out there.":"The formation's down. Harrier's still out there.");}
function c16Rows(id,p=run.pilot,route=s113Route()){
 const source=C16_STORY.scenes[id];if(!source)return [];
 let rows=source.map(raw=>{
  const b={...raw,c16:true,d1110:true,layout:'duo',art:'comic',who:d1110Who(raw.who,p),text:c16Resolve(raw.text,p,route),readings:[],_cueSet:new Set()};
  b.location=raw.art;b.kind=raw.kind;b.bank=raw.bank?(C16_ART.aliases[raw.bank]||raw.bank):null;
  b.people=[...new Set((raw.people||['$pilot','$tech']).map(k=>k==='$pilot'?p:k==='$tech'?d1110Tech(p):k).filter(k=>C16_ART.pilots.includes(k)))];
  const speaker=b.who.toLowerCase();if(C16_ART.pilots.includes(speaker)&&!b.people.includes(speaker))b.people.push(speaker);
  if(b.people.length<2)b.people.push(b.people[0]==='cole'?'decker':'cole');
  // Group conversations stay at HQ; technical contact substitutions only affect radio exchanges.
  if(id==='post-4'&&b.id==='POST4-02'){b.kind='dialogue';b.bank=null;}
  if(id==='opening'&&b.id==='OPENING-16'&&p==='cole')b.text='Fury flight. Get those people clear.';
  if(id==='post-5'&&b.id==='B507'&&p==='cole')b.text='Everyone. Go.';
  if(p==='maverick'&&raw.upgrade){const lines={2:"Your homing lasers are holding up. I'm leaving them alone.",3:"The ice core's safe. I'll work on the squad's rigs. Yours stays as it is.",4:"Your space kit's ready. Same guns, sealed for orbit. Don't make me come get you.",5:"It works. I can fit the squad with these. Maverick, I'm leaving your guns alone.",6:"Check your gear before you go under. Your homing lasers are still as you left them.",9:"The recorder caught something useful. Your homing rig stays as it is."};b.text=lines[raw.upgrade]||b.text;}
  b.duration=Math.max(raw.duration||0,b.text.length*.055+.75);b.speechEnd=b.text.length*.055+.12;
  b.page=b.kind==='dialogue'?(b.style%2):b.bank==='hq-conference'||b.id==='OPENING-01'?2:b.kind==='wide'?0:3;
  if(b.bank==='satellite-takeover')b.page=0;
  if(b.bank==='hq-laser-demo')b.c16Cues=[{name:'av3_cole_laser6',at:.35},{name:'av3_cole_laser7',at:1.15}];
  if(b.id==='W5901')b.cue='warpCharge';if(b.id==='W5903')b.cue='warpBurst';
  if(b.bank==='radar-acquisition'||b.bank==='bridge-subsurface-scan')b.c16Cues=[{name:'blip',at:.35},{name:'blip',at:1.05},{name:'blip',at:1.75}];
  return b;
 });
 // Easy/Normal complete at Chronos. Keep the native completion menu's quiet pause.
 if(id==='post-5'&&['easy','normal'].includes(diffKey)){
  rows=rows.filter(b=>!['B505','POST5-14','POST5-15','POST5-16','B507'].includes(b.id));
  rows.push(...[
   {id:'B505',who:'DECKER',text:"Cole. We've got people calling from the city.",people:['cole','decker']},
   {id:'POST5-STANDBY',who:'COLE',text:"We'll be ready. First, get everybody patched up.",people:['cole','decker']},
   {id:'B507',who:p.toUpperCase(),text:"One quiet minute. That's all I'm asking.",people:[p,d1110Tech(p)]}
  ].map((b,i)=>({...b,c16:true,d1110:true,kind:'dialogue',layout:'duo',art:'comic',page:i%2,duration:Math.max(2,b.text.length*.055+.75),speechEnd:b.text.length*.055+.12,readings:[],_cueSet:new Set()})));
 }
 return rows;
}
d1110Post=function(n,p=run.pilot,route=s113Route()){return C16_STORY.scenes['post-'+n]?c16Rows('post-'+n,p,route):C16.base.post.apply(this,arguments);};
s113Script=d1110Post;BOFCinematicDirector.script=d1110Post;BOFCampaignStory.script=d1110Post;D1110.script=d1110Post;
d1110Clone=function(id,p=run.pilot,route=s113Route()){return C16_STORY.scenes[id]?c16Rows(id,p,route):C16.base.clone.apply(this,arguments);};
function c16ArtName(b){return b.bank?'art-'+b.bank:b.kind==='portal'?'portal':b.kind==='warp'?'art-warp-arrival':'location-'+(b.location==='river-arrival'?'sewer':b.location||'sky');}
function c16Keys(rows,p=run.pilot){const keys=[];
 for(const b of rows){
  for(const layer of ['bg','fg'])keys.push(C16_ART.banks['page-'+b.page+'-'+layer].key);
  const pk=b.who.toLowerCase(),name=C16_ART.banks['name-'+b.page+'-'+pk];if(name)keys.push(name.key);
  for(const person of b.people||[])keys.push(C16_ART.banks['talk-'+person].key,C16_ART.banks['backdrop-'+person].key);
  if(b.kind!=='dialogue'){const a=C16_ART.banks[c16ArtName(b)];if(a)keys.push(a.key);}
  if(['travel','warp'].includes(b.kind))for(const person of d1110Active(p))keys.push(C16_ART.banks['ship-'+(b.location==='space'||b.location==='earth'||b.kind==='warp'?'space':'earth')+'-'+person].key);
 }
 // Credits and the final card use small authored display variants.
 for(const pk of C16_ART.pilots)for(const prefix of ['icon-','credit-','card-','marker-'])keys.push(C16_ART.banks[prefix+pk].key);
 return [...new Set(keys)];
}
function c16LegacyKeys(){return C16_ART.pilots.flatMap(pk=>['talk-','talk-small-','talk-mini-','backdrop-'].map(prefix=>C16_ART.banks[prefix+pk].key));}
d1110Keys=function(rows,p=run.pilot){return rows.some(b=>b.c16)?[...new Set([...c16Keys(rows.filter(b=>b.c16),p),...(rows.some(b=>!b.c16)?[...C16.base.keys(rows.filter(b=>!b.c16),p),...c16LegacyKeys()]:[])])]:[...new Set([...C16.base.keys.apply(this,arguments),...(rows.length?c16LegacyKeys():[])])];};
function c16LiveId(id){return {'stage4-approach':'arrival-4','stage7-approach':'arrival-7','stage9-approach':'arrival-9','stage5-9-warp':'warp-5-9'}[id];}
// Adapt rows at the existing entry point. All supplied native callbacks are retained.
BOFCinematicDirector.play=function(id,rows,done,live=false){const scene=c16LiveId(id);if(scene)rows=c16Rows(scene);return C16.base.directPlay.call(this,id,rows,done,live);};
d1110Play=function(id,rows,done){const target=c16LiveId(id);return C16.base.play.call(this,id,target?c16Rows(target):rows,done);};
// The prior Stage7 adapter delegates through a stored play function; provide its new rows too.
br1110Arrival=function(n,p=run.pilot){return c16Rows('arrival-'+n,p);};BR1110.arrival=br1110Arrival;
wp1110Rows=function(kind,p=run.pilot){return c16Rows(kind==='departure'?'warp-5-9':'arrival-9',p);};WP1110.rows=wp1110Rows;
function c16Blit(name,frame,x,y){const a=C16_ART.banks[name];if(!a||!XART.rdy(a.key))return false;frame=clamp(Math.floor(frame||0),0,a.frames-1);ctx.drawImage(XART.get(a.key),frame%a.cols*a.w,Math.floor(frame/a.cols)*a.h,a.w,a.h,Math.round(x),Math.round(y),a.w,a.h);return true;}
function c16Mouth(b,s,pk){if(b.who!==pk.toUpperCase()||D1110.static||s.t>=b.speechEnd||!b.text)return 0;const ch=b.text[Math.floor(Math.max(0,s.t-.1)/.055)]?.toLowerCase()||' ';if(/[mbp\s.,!?;:'-]/.test(ch))return 0;if(/[a]/.test(ch))return 1;if(/[eiy]/.test(ch))return 2;if(/[owq]/.test(ch))return 3;if(ch==='u')return 4;if(/[fv]/.test(ch))return 5;return 6;}
function c16FacePlacement(pk,box){const[x,y,w,h]=box,a=C16_ART.banks['talk-'+pk];return{x:x+Math.round((w-a.w)/2),y:y+h-a.baselineY+2,bottom:y+h+2,baseline:a.baselineY};}
function c16Face(pk,box,b,s){const[x,y,w,h]=box,a=C16_ART.banks['backdrop-'+pk],at=c16FacePlacement(pk,box),frame=c16Mouth(b,s,pk);c16Blit('backdrop-'+pk,0,x+Math.round((w-a.w)/2),y+Math.round((h-a.h)/2));c16Blit('talk-'+pk,frame,at.x,at.y);return frame;}
function c16Frame(b,s){if(D1110.static)return b.hold??0;const a=C16_ART.banks[c16ArtName(b)];if(!a)return 0;if(b.hold!=null)return b.hold;if(b.kind==='warp')return 5-Math.min(4,Math.floor(s.t/.42));const pace=b.bank==='hq-laser-demo'?.35:b.bank==='satellite-takeover'?.48:.25;return b.kind==='portal'?Math.floor(s.t*12)%a.frames:Math.min(a.frames-1,Math.floor(Math.max(0,s.t-.1)/pace));}
function c16Clip(box,draw){ctx.save();ctx.beginPath();ctx.rect(...box);ctx.clip();draw();ctx.restore();}
function c16Illustration(b,s,box){const name=c16ArtName(b),a=C16_ART.banks[name],f=c16Frame(b,s),[x,y,w,h]=box;
 if(a)c16Blit(name,f,x+Math.round((w-a.w)/2),y+Math.round((h-a.h)/2));
 if(['travel','warp'].includes(b.kind)){
  const active=d1110Active(),space=b.location==='space'||b.location==='earth'||b.kind==='warp',u=clamp(s.t/Math.max(1,b.duration-.6),0,1);
  active.forEach((pk,i)=>{const key='ship-'+(space?'space':'earth')+'-'+pk,ship=C16_ART.banks[key];const xx=x+w/2+(i-(active.length-1)/2)*(ship.w+22),yy=y+h/2+42-u*(b.kind==='warp'?190:88);c16Blit(key,0,xx-ship.w/2,yy-ship.h/2);});
 }
}
d1110Visual=function(b,s){if(!b.c16)return C16.base.visual.apply(this,arguments);
 const page=C16_ART.pages[b.page],panels=page.panels.map(q=>[q[0]+37,q[1]+21,q[2],q[3]]),speaker=b.who.toLowerCase(),faces=[];
 ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#090b13';ctx.fillRect(0,0,912,512);c16Blit('page-'+b.page+'-bg',0,37,21);
 if(b.kind==='dialogue')panels.forEach((box,i)=>c16Clip(box,()=>faces.push({pilot:b.people[i%b.people.length],frame:c16Face(b.people[i%b.people.length],box,b,s)})));
 else{
  c16Clip(panels[0],()=>c16Illustration(b,s,panels[0]));
  if(panels[1])c16Clip(panels[1],()=>{const pk=C16_ART.pilots.includes(speaker)?speaker:b.people[0];faces.push({pilot:pk,frame:c16Face(pk,panels[1],b,s)});});
 }
 c16Blit('page-'+b.page+'-fg',0,37,21);c16Blit('name-'+b.page+'-'+speaker,0,page.name[0]+37,page.name[1]+21);
 msgFaceUse('dialogue');const title=b.who==='CAPTION'?'BULLETS OF FURY':b.who==='SYSTEM'?'':b.who;
 if(title)msgText(title,37+page.name[0]+page.name[2]/2,21+page.name[1]+page.name[3]/2,15,'#090b13',1,1,.04);
 if(b.text)msgDrawBlock({text:b.text,x:37+page.body[0]+9,y:21+page.body[1]+2,w:page.body[2]-18,h:page.body[3]-4,maxH:23,minH:18,lineMul:1.23,spacing:.04,color:'#fff0cf',budget:s.shown,valign:'middle'});
 controlHintRow([['pad_a',s.shown<b.text.length?'READ':'NEXT'],['pad_start','SKIP']],503,456,840,12);msgFaceUse(null);ctx.restore();
 C16.last={id:s.id,shot:b.id,who:b.who,text:b.text,pilot:run.pilot,coOp:d1110Active(),page:b.page,faces,kind:b.kind,bank:b.bank,frame:c16Frame(b,s),time:s.t};D1110.last=C16.last;
};
d1110Step=function(s,dt,onAdvance,onFinish){const b=s.beats[s.i];if(!b?.c16)return C16.base.step.apply(this,arguments);if(D1110.paused)return;
 s.age+=dt;s.d1110Wait=(s.d1110Wait||0)+dt;if(s.age>.15&&Input.menuStart()){onFinish();return;}
 const click=Input.mouse.down&&!s.md;s.md=!!Input.mouse.down;
 if(s.age>.15&&(Input.menuConfirm()||click)){if(s.shown<b.text.length){s.shown=b.text.length;s.t=Math.max(s.t,b.text.length/30);}else onAdvance();return;}
 if(!d1110Ready(s.d1110Keys||[])&&s.d1110Wait<15)return;
 const previous=s.t,before=s.shown;s.t+=Math.max(0,dt);s.shown=Math.max(s.shown,Math.min(b.text.length,Math.floor(s.t*30)));dialogueLetterTicks(b.text,before,s.shown);
 if(b.cue)d1110Cue(s,b,b.cue,b.cueAt??.08,previous);for(const q of b.c16Cues||[])d1110Cue(s,b,q.name,q.at,previous);
 if(s.t>=b.duration){s.shown=b.text.length;onAdvance();}
};
d1110Face=function(pk,x,y,t,talking,size=384){if(!C16_ART.pilots.includes(pk))return C16.base.face.apply(this,arguments);const variant=size<=90?'credit-':size<=96?'icon-':size<=180?'card-':'talk-',a=C16_ART.banks[variant+pk];return c16Blit(variant+pk,talking?Math.floor(t*10)%7:0,x+Math.round((size-a.w)/2),y+Math.round((size-a.h)/2));};
C16.base.comicFace=cb1110Face;
cb1110Face=function(pk,box,t,speaking){if(!C16_ART.pilots.includes(pk))return C16.base.comicFace.apply(this,arguments);const[x,y,w,h]=box,bg=C16_ART.banks['backdrop-'+pk],name=(h<180?'talk-mini-':h<256?'talk-small-':'talk-')+pk,a=C16_ART.banks[name];c16Clip(box,()=>{for(let yy=y;yy<y+h;yy+=bg.h)c16Blit('backdrop-'+pk,0,x+Math.round((w-bg.w)/2),yy);c16Blit(name,speaking&&!D1110.static?Math.floor(t*10)%7:0,x+Math.round((w-a.w)/2),y+h-a.baselineY+2);});};
s113Bank=function(name,f=0,x=456,y=256){const m=/^(landing|return|launch|flight)-(.+)$/.exec(name);if(m&&C16_ART.pilots.includes(m[2]))return c16Blit('marker-'+m[2],0,x-64,y-64);return C16.base.bank.apply(this,arguments);};
D1110.preview=S113.preview=async function(id,p='cole',route='left',partner=null){
 let rows=C16_STORY.scenes[id]?c16Rows(id,p,route):id.startsWith('hq-')?c16Rows(id==='hq-workshop'?'post-5':'post-3',p,route).filter(b=>b.tag===({'hq-briefing':'briefing','hq-prototypes':'prototypes','hq-workshop':'workshop'}[id])):null;
 if(!rows||['opening','ending','sting'].includes(id))return C16.base.preview(id,p,route,partner);
 BOFCinematicDirector.cancel();run.pilot=p;pilotIndex=PILOTS.findIndex(q=>q.key===p);run.mode='campaign';coopOn=C16_ART.pilots.includes(partner)&&partner!==p;if(coopOn){run2.pilot=partner;p2Index=PILOTS.findIndex(q=>q.key===partner);}Input.clearTaps();
 // Resolve after the partner is selected, so support and guard assignments agree with the real crew.
 rows=id.startsWith('hq-')?c16Rows(id==='hq-workshop'?'post-5':'post-3',p,route).filter(b=>b.tag===({'hq-briefing':'briefing','hq-prototypes':'prototypes','hq-workshop':'workshop'}[id])):c16Rows(id,p,route);
 return d1110Play('review-'+id,rows,()=>setState(GS.TITLE));
};
C16.rows=c16Rows;C16.keys=c16Keys;C16.mouth=c16Mouth;window.BOF_COMIC_STORY_1111=C16;
