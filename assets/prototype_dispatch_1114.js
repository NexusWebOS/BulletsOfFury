"use strict";
/* The Federation kit is found in pieces; binding happens during the native ascent. */
const KD17={base:{rows:c16Rows,keys:d1110Keys,visual:d1110Visual,furyDialogue:furyIntroDialogue},last:null};
for(const a of Object.values(KD17_ART.banks))XART._src[a.key]=a.path;
C16_STORY.scenes['post-4']=[
 cw16Row('B401','PILOT',"Team, we found it! The prototype attachments are here, but... they're all in separate pieces?",{people:['$pilot','$tech']}),
 cw16Row('KIT4-02','PILOT','$techName, do you know anything about this?',{people:['$pilot','$tech']}),
 cw16Row('POST4-02','TECH',"They're meant to bind to your ship as you begin to fly off into space.",{people:['$pilot','$tech']}),
 cw16Row('KIT4-04','TECH',"The Federation has been having me work on this binding technology. The pieces attach to your aircraft during ascent.",{people:['$pilot','$tech']}),
 cw16Row('CW4-03','TECH',"The airbase caught another uplink. Look at what attacked that dish.",{people:['$pilot','$tech']}),
 cw16Row('B403','SYSTEM','',{kind:'wide',kit17:'satellite',duration:6.2,cue:'crackle',cueAt:.4,people:['$pilot','$tech']}),
 cw16Row('POST4-05','TECH','And whatever attacked that dish is still hacking our networks!',{people:['$pilot','$tech']}),
 cw16Row('POST4-06','PILOT','Then we have no choice. One of us will have to go straight for it and get to the bottom of this.',{people:['$pilot','$tech']}),
 cw16Row('POST4-07','TECH','Well, whoever decides to go, just let the team know the kit is ready. Awaiting your orders, sir!',{upgrade:4,people:['$pilot','$tech']}),
 cw16Row('KIT4-11','PILOT',"Team, the kit is ready. One last check, then I'm going up.",{people:['$pilot','$tech']}),
 cw16Row('POST4-10','SYSTEM','',{kind:'travel',art:'sky',kit17:'departure',duration:6.2,cue:'jetDash',cueAt:.25,people:['$pilot','$tech']})
];
c16Rows=function(id,p=run.pilot,route=s113Route()){
 const rows=KD17.base.rows.apply(this,arguments);if(id!=='post-4')return rows;
 const tech=d1110Tech(p);
 for(let i=0;i<rows.length;i++){
  const b=rows[i];for(const pk of b.people||[])b.fpLocations[pk]=pk===tech?(tech==='decker'?'workshop':'conference'):'hangar';
  if(b.id==='KIT4-04'&&tech==='cole')b.text="The Federation has had Decker working on this new binding technology. I've been helping him test it. The pieces attach during ascent.";
  if(b.id==='POST4-07')b.text=C16_STORY.scenes['post-4'].find(q=>q.id==='POST4-07').text;
  if(b.id==='KIT4-11'&&d1110Active(p).length>1)b.text="Team, the kit is ready. One last check, then we're going up.";
  b.duration=Math.max(b.duration,b.text.length/30+2.8+(b.cm3?.readAt||0),b.text.length*.055+.75);b.speechEnd=b.text.length/30+(b.cm3?.readAt||0);
  // Cut directly from the silent full panel to the next speaker. The native
  // comic scroller must not redraw the retired small insert during its exit.
  if(b.kit17&&rows[i+1]?.cm3)b.cm3.group=rows[i+1].cm3.group;
 }return rows;
};
C16.rows=CM3.rows=FP5.rows=c16Rows;
d1110Keys=function(rows,p=run.pilot){const keys=KD17.base.keys.apply(this,arguments);if(rows.some(b=>b.kit17==='satellite'))keys.push(KD17_ART.banks.satellite.key);
 if(rows.some(b=>b.kit17==='departure')){keys.push(STAGE6_TRANSITION_SKY);for(let i=0;i<7;i++)keys.push('cm2_cloud_'+i);for(const pk of d1110Active(p))for(const tail of ['','_g1','_g2'])keys.push('ship_'+pk+tail);}
 return [...new Set(keys)];};
function kd17Satellite(box){const a=KD17_ART.banks.satellite;if(!XART.rdy(a.key))return;const[x,y,w,h]=box,k=Math.max(w/a.w,h/a.h),dw=Math.round(a.w*k),dh=Math.round(a.h*k);ctx.drawImage(XART.get(a.key),Math.round(x+(w-dw)/2),Math.round(y+(h-dh)/2),dw,dh);}
function kd17Departure(b,s,box){
 const[x,y,w,h]=box,t=Math.max(0,s.t-(b.cm3?.readAt||0)),u=clamp(t/5.8,0,1),e=u*u*(3-2*u),k=w/VW;
 ctx.save();ctx.translate(x,y);ctx.scale(k,k);stage5AscentBackgroundDraw(t*850);furyIntroClouds({space:false,t:t+3,scroll:FURY_INTRO_SPEED*2.4+t*850});ctx.restore();
 const planes=[];for(const [i,pk]of d1110Active().entries()){
  const xx=x+w/2+(i-(d1110Active().length-1)/2)*140,yy=y+lerp(h*.76,h*.29,e)+i*20,size=lerp(186,148,e);
  pt11OpeningShip(pk,t,xx,yy,size,.66+.34*u);planes.push({...PT11_UI.ship});
 }
 KD17.last={mode:'departure',planes,unconverted:true,gravityReady:!!run.gravityShipReady,scroll:t*850,time:t};
}
d1110Visual=function(b,s){if(!b.kit17)return KD17.base.visual.apply(this,arguments);
 const box=[12,12,888,488];ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#080d14';ctx.fillRect(0,0,912,512);
 c16Clip(box,()=>{if(b.kit17==='satellite'){kd17Satellite(box);KD17.last={mode:'satellite',key:KD17_ART.banks.satellite.key,frame:0,singlePanel:true};}else kd17Departure(b,s,box);});sl14Frame(box);
 if(b.kit17==='departure'&&s.t>b.duration-.45){ctx.fillStyle='rgba(0,0,0,'+clamp((s.t-b.duration+.45)/.45,0,1)+')';ctx.fillRect(0,0,912,512);}
 msgFaceUse('dialogue');controlHintRow([['pad_start','SKIP']],730,505,887,9);msgFaceUse(null);ctx.restore();
 KD17.last={...KD17.last,shot:b.id,caption:false,dialogueBox:false,time:s.t,pilot:run.pilot};D1110.last=KD17.last;
};
// Keep the existing assembly clock and line intact; use the actual technician
// when Decker is the flying pilot instead of having him call himself from HQ.
furyIntroDialogue=function(G){if(!G||G.narrative===false||G.phase==='active'||G.dialogueT<=G.dialogueDelay)return;
 const tech=d1110Tech(run.pilot),who=tech.toUpperCase(),full=G.line||'',shown=G.phase==='drift'?full.slice(0,Math.max(0,Math.floor((G.dialogueT-G.dialogueDelay)*GRAVITY_DIALOGUE_CPS))):full;
 dlgBox({who,tint:dialogueNameColor(who,'#ffb347'),full,shown,fade:clamp((G.dialogueT-G.dialogueDelay)/.28,0,1),portrait:tech,pw:Math.round(VW*.76),ph:Math.min(128,Math.round(VH*.25)),x:Math.round(VW*.12),y:12,screenSpace:false});
};
KD17.rows=c16Rows;KD17.preview=(p='cole')=>D1110.preview('post-4',p);window.BOF_PROTOTYPE_DISPATCH_1114=KD17;
