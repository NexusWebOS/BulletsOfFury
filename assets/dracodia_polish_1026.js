'use strict';
/* Mike Oct26: cyclic subframes, stepped opacity, one closing roar and rising thunder. */
const RD27={base:{bank:er23DrawBank,plate:rd26Plate,tick:rb23SceneTick,sound:r30Sound,body:v18Body},blends:new Map(),audio:[],intro:null};
function rd27Blend(kind,phase){
 const carrier=kind==='carrier',a=carrier?ER23_ART.banks.symbiote:RD26_ART[kind],count=carrier?24:RD26_ART.frames,
  w=carrier?256:512,h=w,key=a.key,p=((phase%1)+1)%1*count,f=Math.floor(p),mix=Math.round((p-f)*32)/32;
 if(!XART.rdy(key))return null;let q=RD27.blends.get(kind);
 if(!q){const c=document.createElement('canvas');c.width=w;c.height=h;q={c,tag:null};RD27.blends.set(kind,q);}
 const tag=f+':'+mix;if(q.tag===tag)return q.c;
 const g=q.c.getContext('2d');g.clearRect(0,0,w,h);g.imageSmoothingEnabled=false;
 for(const [i,alpha]of [[f,1-mix],[(f+1)%count,mix]]){if(!alpha)continue;
  const cell=carrier?[i%8*256,Math.floor(i/8)*256,256,256]:RD26_ART.cells[i];
  g.globalCompositeOperation='lighter';g.globalAlpha=alpha;g.drawImage(XART.get(key),...cell,0,0,w,h);}
 g.globalAlpha=1;g.globalCompositeOperation='source-over';q.tag=tag;return q.c;
}
function rd27Visibility(t){const frame=clamp(Math.floor((t-7)/7*24),0,23);return{frame,alpha:.25+.75*frame/23};}
er23DrawBank=function(name,frame,x,y,flash=false){
 if(name==='symbiote'&&rd25Own(boss)&&boss._r30.t>=7&&boss._r30.t<14&&!flash){
  const t=boss._r30.t,V=rd27Visibility(t),im=rd27Blend('carrier',t*20/24);if(!im)return false;
  ctx.save();ctx.globalAlpha*=V.alpha;ctx.drawImage(im,x-128,y-128,256,256);ctx.restore();RD27.intro={...V,t};return true;
 }return RD27.base.bank.apply(this,arguments);
};
rd26Plate=function(Q,wire=false){const im=rd27Blend(wire?'wire':'body',Q.yaw/TAU);if(!im)return;
 ctx.drawImage(im,-256*Q.k,-256*Q.k,512*Q.k,512*Q.k);
};
function rd27Carrier(Q){return rd27Blend('carrier',Q.yaw/TAU);}
v18Body=function(b){if(rb23Host(b)&&b._r30.mode==='dr5er23rebirth'&&b._r30.t<4){
 return bi24Draw(bi24Sample('dracodia_recover',1),b,360);
 }return RD27.base.body.apply(this,arguments);
};
// Preserve the speech text and faces; only the final exclamation owns the scream.
for(let i=0;i<DR5.intro.length-1;i++)if(DR5.intro[i][1]===5)DR5.intro[i][1]=4;
// Dedicated voices keep the formation mix independent of ordinary beam shots.
function rd27ThunderReady(){const source=Snd.pools.combatBeam0927;if(!source)return false;
 if(!Snd.pools.rd27Lightning){if(!source.slots.some(Boolean))void source.list[0];const uri=source.slots.find(Boolean).uri,slots=[],list=[];
  for(let i=0;i<6;i++)Object.defineProperty(list,i,{enumerable:true,get(){if(!slots[i])slots[i]={el:new window.Audio(),uri,attached:false,used:0};return Snd._touchVoice(slots[i]);}});
  Snd.pools.rd27Lightning={list,slots,i:0};Snd.TAME.rd27Lightning={g:1.35,native:true,min:0};}
 return true;
}
function rd27Thunder(b,beat,kind){if(!rd27ThunderReady())return false;const R=b._r30.v18.rb23Rebirth;if(!R)return false;
 const seen=R.rd27AudioSeen||(R.rd27AudioSeen=new Set()),id=kind+':'+beat;if(seen.has(id))return false;seen.add(id);RD27.lightningOwner=b;
 const active=Snd.pools.rd27Lightning.slots.filter(v=>v?.attached&&!v.el.paused&&!v.el.ended).length,
  strength=.82+.18*clamp((b._r30.t-14)/11.6,0,1),gain=strength/Math.sqrt(1+active*.45),played=Snd.play('rd27Lightning',gain);
 RD27.audio.push({beat,gain,strength,active,played,t:b._r30.t,kind});return played;
}
function rd27ThunderStop(){const pool=Snd.pools.rd27Lightning;if(pool)for(const v of pool.slots)if(v?.el){v.el._bofEpoch=(v.el._bofEpoch||0)+1;try{v.el.pause();v.el.currentTime=0;}catch(_){}}RD27.lightningOwner=null;}
const rd27Load=stageLoadBegin;stageLoadBegin=function(n){rd27ThunderStop();if(n===8&&rd27ThunderReady())Snd.prepare('rd27Lightning');return rd27Load.apply(this,arguments);};
const rd27SetState=setState;setState=function(s){if(s!==GS.PLAY&&RD27.lightningOwner)rd27ThunderStop();return rd27SetState.apply(this,arguments);};
r30Sound=function(key){if(key==='combatBeam0927'&&rd25Own(boss)){
 return rd27Thunder(boss,boss._r30.v18.rb23Rebirth.bolts,'native');
 }return RD27.base.sound.apply(this,arguments);
};
rb23SceneTick=function(b,dt){const out=RD27.base.tick.apply(this,arguments);
 if(rd25Own(b)){const t=b._r30.t,R=b._r30.v18.rb23Rebirth;
  if(t>=23&&t<25.6&&rd27ThunderReady()){
   const beat=rd26StrikeClock(t,R).beat;if(beat!==R.rd27SoundBeat){R.rd27SoundBeat=beat;
    rd27Thunder(b,beat,'ending');}
  }
 }
 if(!rd25Own(b)&&RD27.lightningOwner===b)rd27ThunderStop();
 if(RD27.audio.length>180)RD27.audio.splice(0,RD27.audio.length-180);return out;
};
globalThis.BOF_DRACODIA_POLISH_1026=RD27;
