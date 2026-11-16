"use strict";
/* Overnight cinematic QA: current story continuity and complete-text holds.
   Native clocks, typing, manual advance, skip, rewards and continuations persist. */
const CQA16={base:{rows:c16Rows,play:BOFCinematicDirector.play,step:d1110Step,visual:d1110Visual,intro:drawCampaignIntro,material:kd18Material},adjusted:[],waiting:[],version:3};
// The speaker owns the communicator material. A hostile encounter's menu
// context must not recolor a friendly pilot's standard framed avatar.
kd18Material=function(o){
 const speaker=String(o?.who||'').trim().toLowerCase();
 return PILOTS.some(p=>p.key===speaker)?'crew':CQA16.base.material.apply(this,arguments);
};
if(C16_STORY.voices?.juggernaut)C16_STORY.voices.juggernaut=C16_STORY.voices.juggernaut.replace('an open dark vest','an orange sleeveless tactical vest over a black undershirt');
const cqa16Post1=C16_STORY.scenes['post-1'];
for(const b of cqa16Post1){
 if(b.id==='POST1-02')Object.assign(b,{who:'FLIGHT SYSTEM',text:'Repeating transmission detected. A surface relay is answering.',kind:'insert',bank:'warp-drive-lock',people:['$pilot']});
 if(b.id==='POST1-04')Object.assign(b,{who:'FLIGHT SYSTEM',text:'Strongest return: the volcanic belt. Squad channel still unavailable.',kind:'insert',bank:'warp-drive-lock',people:['$pilot']});
}
const cqa16Airbase=C16_STORY.scenes['arrival-4'].find(b=>b.id==='ARRIVAL4-02');
if(cqa16Airbase)cqa16Airbase.text='Find the Federation prototypes. Keep the team covered.';
function cqa16Readable(rows){return rows.map(b=>{
 // Physical evacuation/death action reels retain Mike's requested timing.
 if(!b.d1110||!b.cm3||!b.text||b.hq19)return b;
 const readAt=Number(b.cm3.readAt)||0,text=String(b.text),typed=text.length/30,
  words=(text.match(/\S+/g)||[]).length,hold=Math.max(2.25,Math.min(5,words/6)),minimum=readAt+typed+hold+.18,
  duration=Math.max(Number(b.duration)||0,minimum);
 if(duration<=b.duration)return b;
 const out={...b,duration,cm3:{...b.cm3,baseDuration:duration-readAt-.14},cqa16:{readAt,typed,hold,minimum}};
 CQA16.adjusted.push({id:b.id,before:b.duration,after:duration});if(CQA16.adjusted.length>256)CQA16.adjusted.shift();return out;
});}
c16Rows=function(){return cqa16Readable(CQA16.base.rows.apply(this,arguments));};
C16.rows=CM3.rows=FP5.rows=c16Rows;
BOFCinematicDirector.play=function(id,rows,done,live=false){return CQA16.base.play.call(this,id,cqa16Readable(rows),done,live);};
function cqa16SceneReady(s){
 const keys=s?.d1110Keys;if(!keys?.length)return true;
 if(s.cqa16LoadedKeys===keys)return true;
 if(d1110Ready(keys)){s.cqa16LoadedKeys=keys;s.cqa16Waiting=false;return true;}
 s.cqa16Waiting=true;return false;
}
d1110Step=function(s,dt,onAdvance,onFinish){
 const b=s?.beats?.[s.i];
 if(b?.d1110&&!D1110.paused&&!cqa16SceneReady(s)){
  s.age+=Math.max(0,dt||0);s.d1110Wait=(s.d1110Wait||0)+Math.max(0,dt||0);
  if(s.age>.15&&Input.menuStart()){onFinish();return;}
  // Consume a loading-screen press so it cannot reveal/advance after decode.
  Input.menuConfirm();s.md=!!Input.mouse.down;
  if(!s.cqa16WaitLogged){CQA16.waiting.push({id:s.id,shot:b.id});if(CQA16.waiting.length>64)CQA16.waiting.shift();s.cqa16WaitLogged=true;}
  return;
 }
 return CQA16.base.step.apply(this,arguments);
};
d1110Visual=function(b,s){
 if(b?.d1110&&s?.cqa16Waiting&&!cqa16SceneReady(s)){
  ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#000';ctx.fillRect(0,0,912,512);
  msgFaceUse('dialogue');msgText('RECEIVING TRANSMISSION',456,236,20,'#f0e4c7',1,1,.04);
  controlHintRow([['pad_start','SKIP']],493,456,840,11);msgFaceUse(null);ctx.restore();return;
 }
 return CQA16.base.visual.apply(this,arguments);
};
drawCampaignIntro=function(dt){
 const C=campaignIntro;
 if(C?.fury14&&!C.ready){
  C.cqa16WaitAge=(C.cqa16WaitAge||0)+Math.max(0,dt||0);
  if(C.cqa16WaitAge>.3&&Input.menuStart()){campaignIntroFinish();return;}
 }
 return CQA16.base.intro.apply(this,arguments);
};
