'use strict';
/* Wave atmosphere and owner-scoped ElevenLabs cues. No combat timing changes. */
const C33={base:{draw:hammerBossDraw,tick:hammerBossTick,cue:b20Cue,laser:hammerLaser,load:stageLoadBegin},events:[],last:new Map(),owner:null,lightning:null};
const C33_CUES=['rage','wave','palm','charge','thunder','smash','hammercharge'];
for(const name of C33_CUES){const key='c33_'+name,uri='assets/game/shared/combat/chronos_storm_1025/'+name+'.mp3',list=[],slots=[];
 BOFA.sfx[key]=uri;for(let i=0;i<3;i++)Object.defineProperty(list,i,{enumerable:true,get(){if(!slots[i])slots[i]={el:new window.Audio(),uri,attached:false,used:0};return Snd._touchVoice(slots[i]);}});
 Snd.pools[key]={list,slots,i:0};Snd.TAME[key]={g:name==='palm'?.55:.78,native:true,min:name==='palm'?.09:.3};Audio.SFX[key]=()=>c33Sound(name,boss);
}
function c33Sound(name,b,gain=1){if(!c25Own(b)||b.dead)return false;const key='c33_'+name,last=C33.last.get(key);if(last!=null&&efxClock-last<(name==='palm'?.09:.3))return false;
 C33.last.set(key,efxClock);C33.owner=b;C33.events.push({cue:name,time:efxClock,state:b._hammer.state});if(C33.events.length>500)C33.events.shift();return Snd.play(key,gain);}
function c33Stop(){for(const name of C33_CUES)for(const s of Snd.pools['c33_'+name].slots)if(s?.el){s.el.pause();s.el.currentTime=0;}C33.owner=null;C33.last.clear();}
stageLoadBegin=function(n,keys){if(n===5)Snd.prepare(C33_CUES.map(n=>'c33_'+n));return C33.base.load.call(this,n,[...(keys||[]),...(n===5?['arch_hammer_lightning_0926']:[])]);};
b20Cue=function(key){if(c25Own(boss)&&!boss.dead){const h=boss._hammer;
 if(key==='hammerImpact')return c33Sound('smash',boss);
 if(key==='shadowCharge'&&(c30Own(boss)||h.state==='fr_activation'))return c33Sound(h.state==='fr_activation'?'hammercharge':'charge',boss);
 if(key==='fusionBeam'&&c30Own(boss))return c33Sound('wave',boss);
 if(key==='shieldBreakCombat'&&h.c29Break)return c33Sound('thunder',boss);
 if(key==='bossPhase'&&h._hf22Charge)return c33Sound('thunder',boss);
 }return C33.base.cue.apply(this,arguments);};
hammerLaser=function(x,y,a,speed,silent){if(c32Own(boss)){const r=C33.base.laser.call(this,x,y,a,speed,true);if(!silent)c33Sound('palm',boss);return r;}return C33.base.laser.apply(this,arguments);};
hammerBossTick=function(b,dt){const old=b?._hammer?._hf22Charge,prior=b?._hammer?.state,r=C33.base.tick.apply(this,arguments);if(c25Own(b)&&!b.dead){const h=b._hammer,R=h.c30;
 if(h._hf22Charge&&!old)c33Sound('rage',b);
 if(['fr_activation','storm_raise'].includes(h.state)&&prior!==h.state)c33Sound('hammercharge',b);
 if(c30Own(b)&&R?.phase==='beam'){const beat=Math.floor(R.t/.55);if(R.c33Thunder!==beat){R.c33Thunder=beat;c33Sound('thunder',b,.48);}}else if(R)R.c33Thunder=-1;
 }return r;};
const c33Update=updatePlay;updatePlay=function(dt){if(C33.owner&&(C33.owner!==boss||C33.owner.dead||run.stage!==5))c33Stop();return c33Update.apply(this,arguments);};
function c33Storm(b){const R=b._hammer.c30;if(!c30Own(b)||!R||!['gather','thrust','beam','recover'].includes(R.phase)){C33.lastDraw=null;return;}
 const level=R.phase==='gather'?clamp(R.t/.6,0,1):R.phase==='recover'?1-clamp(R.t/.7,0,1):1;
 ctx.save();ctx.beginPath();ctx.rect(camLeftX(),viewTopY(),camRightX()-camLeftX(),viewH());ctx.clip();ctx.fillStyle='rgba(2,0,8,'+(level*.72)+')';ctx.fillRect(camLeftX(),viewTopY(),camRightX()-camLeftX(),viewH());
 const key='arch_hammer_lightning_0926';let bolts=0;
 if(XART.rdy(key)){if(!C33.lightning)C33.lightning=C31Texture.palette(XART.get(key),'red');ctx.globalCompositeOperation='screen';ctx.imageSmoothingEnabled=false;
 for(let i=0;i<4;i++){const age=R.phase==='recover'?Math.min(.819,.45+R.t): (efxClock+i*.19)%.82,u=clamp(age/.16,0,1),f=Math.min(7,Math.floor(age/.82*8)),height=310+(i%2)*110,width=height*228/416,x=clamp(b.x+[-165,-85,90,180][i],camLeftX()+30,camRightX()-30);
 ctx.save();ctx.beginPath();ctx.rect(x-width/2,viewTopY(),width,height*u);ctx.clip();ctx.globalAlpha=1;if(R.phase==='recover'&&R.t>=.37){ctx.restore();continue;}ctx.drawImage(C33.lightning,f%4*384+78,Math.floor(f/4)*512+48,228,416,x-width/2,viewTopY()-10,width,height);ctx.restore();bolts++;}}
 ctx.restore();C33.lastDraw={phase:R.phase,level,bolts,frame:Math.floor(efxClock*18)%8};
}
hammerBossDraw=function(b){if(c25Own(b)&&!b.dead)c33Storm(b);return C33.base.draw.apply(this,arguments);};
window.BOF_CHRONOS_STORM=C33;
