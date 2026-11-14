'use strict';
/* Mike Oct26: louder Dracodia-derived lightning, exactly once per visible strike.
   Dedicated bounded voices; shared mixer/settings; no combat or attack-clock edits. */
const CF48={key:'chronosLightning1026',uri:'assets/game/shared/audio/chronos_lightning_1026/strike.mp3',
 base:{log:c45Log,sound:c33Sound,storm:c33Storm,update:updatePlay,state:setState,load:stageLoadBegin},
 owner:null,seen:new WeakMap(),events:[],lastStrike:null,voices:8};
BOFA.sfx[CF48.key]=CF48.uri;
{const slots=[],list=[];for(let i=0;i<CF48.voices;i++)Object.defineProperty(list,i,{enumerable:true,get(){
 if(!slots[i])slots[i]={el:new window.Audio(),uri:CF48.uri,attached:false,used:0};return Snd._touchVoice(slots[i]);}});
 Snd.pools[CF48.key]={list,slots,i:0};Snd.TAME[CF48.key]={g:1,native:true,min:0};}
function chronosLightningStop(){const pool=Snd.pools[CF48.key];for(const s of pool.slots)if(s?.el){
 s.el._bofEpoch=(s.el._bofEpoch||0)+1;try{s.el.pause();s.el.currentTime=0;}catch(e){}}
 CF48.owner=null;}
function chronosLightningStrike(b,token,family,index){
 if(!b||b.dead||!c25Own(b)||!token||state!==GS.PLAY)return false;
 let tokens=CF48.seen.get(b);if(!tokens){tokens=new WeakMap();CF48.seen.set(b,tokens);}
 let seen=tokens.get(token);if(!seen){seen=new Set();tokens.set(token,seen);}
 const id=family+':'+index;if(seen.has(id))return false;seen.add(id);
 if(seen.size>384)seen.delete(seen.values().next().value);
 if(CF48.owner&&CF48.owner!==b)chronosLightningStop();CF48.owner=b;
 const pool=Snd.pools[CF48.key],active=pool.slots.filter(s=>s?.attached&&!s.el.paused&&!s.el.ended).length;
 // Each attack stays audible; overlapping tails share a finite power budget.
 const focus=typeof chronosEnergyLightningGain==='function'?chronosEnergyLightningGain(b):1;
 const gain=.94*focus/Math.sqrt(1+active*.4),accepted=Snd.play(CF48.key,gain);
 CF48.events.push({family,index,time:efxClock,gain,active,accepted});
 if(CF48.events.length>500)CF48.events.shift();return accepted;
}
c45Log=function(type,data){const out=CF48.base.log.apply(this,arguments),b=boss,C=b?._hammer?._hf22Charge;
 if(C&&type==='strike')chronosLightningStrike(b,C,'rage',data.n);
 else if(C&&type==='final')chronosLightningStrike(b,C,'rage-final',0);return out;};
// Retire only the old sparse/doubled thunder during the newly owned sequences.
c33Sound=function(name,b,gain){const h=b?._hammer,R=h?.c30;
 if(name==='thunder'&&c25Own(b)&&(h?._hf22Charge||R&&['gather','thrust','beam','recover','kame_charge','kame_thrust','kame_fire','kame_recover'].includes(R.phase)))return false;
 return CF48.base.sound.apply(this,arguments);};
c33Storm=function(b){const out=CF48.base.storm.apply(this,arguments),d=C33.lastDraw,R=b?._hammer?.c30;
 if(d?.bolts&&d.strike&&d.level>.08&&R)chronosLightningStrike(b,R,'wave-'+(R.cycle||0),d.strike.beat);return out;};
function chronosKameLightningDraw(b){
 if(!c46Own(b))return;const R=b._hammer.c30,offset={kame_charge:0,kame_thrust:C46_T.charge,kame_fire:C46_T.charge+C46_T.thrust};
 if(offset[R.phase]==null)return;
 const elapsed=offset[R.phase]+R.t,beat=Math.floor(elapsed/.38),age=elapsed-beat*.38;
 if(age>=.30)return;const key='c42_bolt_'+Math.min(7,Math.floor(age/.30*8));if(!XART.rdy(key))return;
 // Reuse the existing single authored C42 bolt, behind the actor, during the opener.
 const lanes=[.18,.76,.39,.89,.58,.09,.68,.30],x=camLeftX()+(camRightX()-camLeftX())*lanes[beat%lanes.length],height=viewH(),k=height/256,head=clamp(age/.14,0,1)*height;
 const level=R.phase==='kame_charge'?clamp(R.t/.6,0,1):1;
 ctx.save();ctx.beginPath();ctx.rect(camLeftX(),viewTopY(),camRightX()-camLeftX(),viewH());ctx.clip();
 ctx.beginPath();ctx.rect(x-32*k,viewTopY(),64*k,head);ctx.clip();ctx.globalAlpha=level;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(key),x-32*k,viewTopY(),64*k,256*k);ctx.restore();
 CF48.lastStrike={phase:R.phase,beat,age,x,head,key,level};
 if(level>.08)chronosLightningStrike(b,R,'kame',beat);
}
stageLoadBegin=function(n,keys){if(n===5)Snd.prepare(CF48.key);return CF48.base.load.apply(this,arguments);};
updatePlay=function(dt){const r=CF48.base.update.apply(this,arguments);if(CF48.owner&&(CF48.owner!==boss||CF48.owner.dead||run.stage!==5))chronosLightningStop();return r;};
setState=function(s){if(s!==GS.PLAY)chronosLightningStop();return CF48.base.state.apply(this,arguments);};
globalThis.BOF_CHRONOS_LIGHTNING_AUDIO=CF48;
