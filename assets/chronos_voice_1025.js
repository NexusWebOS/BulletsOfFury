'use strict';
const C36={draw:hammerBossDraw,damage:hammerBossDamage,cue:b20Cue,tick:hammerBossTick,load:stageLoadBegin,caption:null};
stageLoadBegin=function(n,keys){const portraits=n===5?[...PILOTS.flatMap(p=>[commPortrait(p.key,'idle'),commPortrait(p.key,'talk')]),commPortrait('decker','idle'),commPortrait('decker','talk'),'fb1002_hammer_portrait']:[];return C36.load.call(this,n,[...(keys||[]),...portraits]);};
hammerBossDamage=function(b,dmg){if(c25Own(b)&&!b.dead&&hm10WallActive(b)){
 const h=b._hammer,hammerCounter=h.recovery?.status==='charging'&&b._hammerModuleHit==='hammer';
 if(!hammerCounter){b._hammerModuleHit=null;h.cp12Hit=.18;if((h.cp12Sound||0)<=0){h.cp12Sound=.09;Audio.SFX.shieldHitCombat?.();hm10ShieldImpact(b,b.x,b.y+85);}return 0;}
 }return C36.damage.apply(this,arguments);};
hammerBossDraw=function(b){const r=C36.draw.apply(this,arguments);C36.caption=null;if(!c25Own(b)||b.dead)return r;const q=ui20Radio();if(!q||fb2IntroActive()||!/CHRONOS/i.test(q.who))return r;
 const art=curFontArt(),words=q.text.toUpperCase().split(/\s+/),rows=[];let line='';for(const word of words){if(line&&(line+' '+word).length>15){rows.push(line);line=word;}else line+=(line?' ':'')+word;}if(line)rows.push(line);
 const right=b.x<(camLeftX()+camRightX())/2,x=clamp(b.x+(right?145:-145),camLeftX()+95,camRightX()-95),y=clamp(b.y-35,viewTopY()+90,viewTopY()+viewH()-rows.length*22-20);
 ctx.save();ctx.textAlign='center';rows.forEach((text,i)=>{for(const [dx,dy]of [[-1,0],[1,0],[0,-1],[0,1]])stageText(art,text,x+dx,y+i*22+dy,16,'#08364c',.85,1,.06);stageText(art,text,x,y+i*22,16,'#baf6ff',.85,1,.06);});ctx.restore();C36.caption={text:q.text,rows,x,y};return r;
};
window.BOF_CHRONOS_VOICE=C36;
