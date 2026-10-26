"use strict";
// Native opening baseline. Storyroom snapshots this AFTER installation so Reset
// restores the repaired story, while saved user edits still retain precedence.
const OB24={baseVisual:ip21Visual,last:null};
// Mike's authored opening order, October24. The selected pilot is already
// airborne when HQ loses power; there is no preceding squad mission briefing.
for(const p of Object.keys(CAMPAIGN_SOLO_LINES))Object.assign(CAMPAIGN_SOLO_LINES[p],{
 report:'What the..? Hello? Team Fury, come in. I repeat, Team Fury, come in!',
 resolve:'Weird, radar is down too. I gotta get back to the base and find the others. Something is wrong.'
});
const ob24Rows=[
 {hq:true,who:'NARRATOR',text:'The year is 2026. On Planet Earth, the United States Government and Air Force formed a secret underground division of elite pilots from around the globe.'},
 {hq:true,who:'NARRATOR',text:'After the Cold War, military tensions still remained high and caused world governments to form secret societies and organizations, including the Fury Division.'},
 {hq:true,who:'NARRATOR',text:'The Fury Division was created for the sole purpose of defending us against unforeseen attacks and anomalies unknown to us all.'},
 {hq:true,who:'NARRATOR',text:'The Division has had many pilots come and go. But as the former generations grew old and rivalries formed, the remaining nine pilots were left seeking answers.'},
 {bg:'cin_war_civilian_collapse',who:'NARRATOR',text:'One day, it finally happened. Our infrastructure was hijacked.'},
 {bg:'cin_war_city_air_attack',who:'NARRATOR',text:'Machines turned on man, and chaos spread across the globe.'},
 {dispatch:'dispatch',alarm:true,who:'DECKER',text:'Are you seeing this? Signals are going off everywhere!'},
 {dispatch:'turn',alarm:true,who:'LIZZIE',text:"Oh my God! We have got to tell the others, now!"},
 {dispatch:'run',who:'',text:'',duration:3.7},
 {replay:'arrival',who:'',text:'',duration:6},
 {federation:true,replay:'takeover',who:'',text:'',duration:6},
 {blackout:true,who:'',text:'',duration:4},
 {flight:true,alarm:true,who:'FLIGHT SYSTEM',text:'Flight communications systems power OFF.'},
 {comic:true,who:'PILOT',pilotLine:'report'},
 {comic:true,who:'PILOT',pilotLine:'resolve'},
 {comic:true,who:'PILOT',text:'But what is going on down there in that jungle? Is it one of them?'}
];
OB24.finaleDuration=6;
Snd.prepare(['retinaLockBeep','warpGate','jetDash','hammerImpact']);
const ob24LineBase=ip21Line;
ip21Line=function(b,c){return b.pilotLine==='resolve'?CAMPAIGN_SOLO_LINES[c.pilot].resolve:ob24LineBase(b,c);};
let ob24At=0;
IP21.beats=ob24Rows.map(b=>{const chars=b.pilotLine?Math.max(...Object.keys(CAMPAIGN_SOLO_LINES).map(p=>ip21Line(b,{pilot:p}).length)):(b.text||'').length;
 const duration=b.dispatch==='run'?b.duration:Math.max(b.duration||5.5,chars/CAMPAIGN_INTRO_CPS+CAMPAIGN_INTRO_READ_HOLD);
 return {...b,duration,at:ob24At,to:ob24At+=duration};});
IP21.finaleAt=ob24At;IP21.end=ob24At+OB24.finaleDuration;
const ob24Keys=['decker','lizzie','cole_horror','axel_horror'].map(n=>INV20_ART.images[n].key);
const ob24OldKeys=campaignIntroKeys;
campaignIntroKeys=function(){return [...ob24OldKeys(),...ob24Keys];};
function ob24Person(name,x,y,h){const a=INV20_ART.images[name];if(!a||!XART.rdy(a.key))return;const k=h/a.h;
 ctx.drawImage(XART.get(a.key),x-a.w*k/2,y,a.w*k,h);}
function ob24HQ(W,H,t){
 const a=C22_ART.images.hq_regroup;if(!XART.rdy(a.key))return;
 const k=Math.max(W/a.w,H/a.h)*1.015,x=(W-a.w*k)/2,y=(H-a.h*k)*.35;
 ctx.drawImage(XART.get(a.key),x,y,a.w*k,a.h*k);
 // The old square motion patch replaced people as well as screens and visibly
 // broke the room's perspective. Keep the room intact; animate its monitor only.
 ctx.save();ctx.beginPath();ctx.rect(x+309*k,y+39*k,64*k,35*k);ctx.clip();
 ip21Blit('corruption',Math.floor(t*7)%33,x+341*k,y+56*k,36*k,36*k);ctx.restore();
}
ip21Visual=function(b,c,t,W,H){
 if(b.alarm){
  const pulse=Math.floor(t/.38);
  if(pulse<5){const key='ob24-beep-'+b.at+'-'+pulse;c._ob24Beeps??=new Set();if(!c._ob24Beeps.has(key)){c._ob24Beeps.add(key);Snd.play('retinaLockBeep');}}
 }
 if(b.hq){cinCover('cin_origin_hq_iso',W,H,.5);OB24.last={shot:'hq',frame:0};return;}
 if(b.blackout){
  cinCover('cin_origin_hq_iso',W,H,.5);const darkness=clamp(t/2.4,0,.96);
  ctx.fillStyle='rgba(0,0,0,'+darkness+')';ctx.fillRect(0,0,W,H);
  OB24.last={shot:'blackout',darkness};return;
 }
 if(b.flight){campaignIntroJungle(W,H,c.t*9);pt11OpeningShip(c.pilot,c.t,W*.5,H*.35,H*.28,.55);OB24.last={shot:'flight',pilot:c.pilot};return;}
 if(b.dispatch){
  // Preserve the full two-person composition; never cover-crop their heads.
  c22Plate('hq_alarm',W,H,t);const a=IP21_ART.banks[b.dispatch],f=Math.min(a.frames-1,Math.floor(t*(b.dispatch==='run'?9:8)));
  ip21Blit(b.dispatch,f,W/2,H*.37,W,H*.73);OB24.last={shot:b.dispatch,frame:f};return;
 }
 if(b.replay){
  cinCover('cinend_deep_space',W,H,.5);const arrival=b.replay==='arrival';
  ip21Blit(arrival?'clean':'corruption',arrival?0:Math.min(32,Math.floor(Math.max(0,t-.5)*7)),W*.57,H*.37,H*.65,H*.65);
  if(arrival){const u=clamp(t/1.4,0,1),emerge=clamp((t-1.4)/2.8,0,1);
   c22Bank('void_portal',t,W*(.19+.08*emerge),H*.32,H*.48*u,false,clamp((8.8-t)/1.5,0,1));
   if(emerge>0)c22Bank('remnant',t,W*(.19+.27*emerge),H*(.32+.03*emerge),H*(.12+.23*emerge),false,emerge);
   ip21Cue(c,'ob24-portal',b.at+.1,'warpGate',c.t-.03);
  }else {
   c22Bank('remnant',t,W*.46,H*.35,H*.35,false,clamp(1-t/1.8,0,1));
   c22Bank('code_fragments',t,W*.57,H*.37,H*.62,false,.35);
  }
  msgFaceUse('dialogue');msgText('FURY SATELLITE / ORBITAL WATCH',W/2,H*.055,Math.max(9,H*.021),'#a8e7ef',1,.9,.02);msgFaceUse(null);
  OB24.last={shot:b.replay,frame:arrival?Math.floor(t*12)%9:Math.min(32,Math.floor(Math.max(0,t-.5)*7))};return;
 }
 if(b.brief){
  ob24HQ(W,H,t);
  if(b.brief==='decker'||b.brief==='lizzie'){
   // Authored full-height body cutouts, kept above the dialogue aperture.
   ob24Person(b.brief,W*.34,H*.035,H*.70);
  }else if(b.brief.startsWith('reaction')){
   ob24Person(b.brief==='reaction'?'cole_horror':'axel_horror',W*.36,H*.025,H*.72);
   ob24Person(b.brief==='reaction'?'axel_horror':'cole_horror',W*.72,H*.045,H*.67);
  }
  OB24.last={shot:b.brief,frame:Math.floor(t*8)%9};return;
 }
 return OB24.baseVisual.apply(this,arguments);
};

// Quick authored logo / active-thruster fly-off, then one native map handoff.
// No added narration or invented mission orders after Mike's final pilot line.
ip21Finale=function(c,q,W,H,previous){
 campaignIntroJungle(W,H,c.t*9);ip21Jet(c,q,W,H);ip21Logo(c,q,W,H);
 ip21Cue(c,'ob24-logo',IP21.finaleAt+.02,'hammerImpact',previous);
 ip21Cue(c,'ob24-boost',IP21.finaleAt+.16,'jetDash',previous);
 if(q>=4&&Snd?.cur){const level=Snd.vol.music*Snd.vol.master;Snd.cur.volume=clamp(level*(1-(q-4)/2),0,1);}
 const fade=clamp((q-4)/2,0,1);ctx.fillStyle='rgba(0,0,0,'+fade+')';ctx.fillRect(0,0,W,H);
 IP21.last={kind:'finale',q,fade,bullets:false};
};
