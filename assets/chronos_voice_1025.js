'use strict';
const C36={draw:hammerBossDraw,damage:hammerBossDamage,cue:b20Cue,tick:hammerBossTick,load:stageLoadBegin,caption:null};
stageLoadBegin=function(n,keys){const portraits=n===5?[...PILOTS.flatMap(p=>[commPortrait(p.key,'idle'),commPortrait(p.key,'talk')]),commPortrait('decker','idle'),commPortrait('decker','talk'),'fb1002_hammer_portrait']:[];return C36.load.call(this,n,[...(keys||[]),...portraits]);};
hammerBossDamage=function(b,dmg){if(c25Own(b)&&!b.dead&&hm10WallActive(b)){
 const h=b._hammer,hammerCounter=h.recovery?.status==='charging'&&b._hammerModuleHit==='hammer';
 if(!hammerCounter){b._hammerModuleHit=null;h.cp12Hit=.18;if((h.cp12Sound||0)<=0){h.cp12Sound=.09;Audio.SFX.shieldHitCombat?.();hm10ShieldImpact(b,b.x,b.y+85);}return 0;}
 }return C36.damage.apply(this,arguments);};
hammerBossDraw=function(b){const r=C36.draw.apply(this,arguments);C36.caption=null;if(!c25Own(b)||b.dead)return r;const q=ui20Radio();if(!q||fb2IntroActive()||!/CHRONOS/i.test(q.who))return r;
 // C113 draws this cue through the shared portrait panel after world rendering.
 C36.caption={text:q.text,who:q.who,owner:b,portraitPanel:true};return r;
};
window.BOF_CHRONOS_VOICE=C36;
