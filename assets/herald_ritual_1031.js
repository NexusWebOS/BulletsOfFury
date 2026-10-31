'use strict';
/* HR92: warning flash -> six audible inscriptions -> accelerating ruby seal ->
   expansion/shatter -> native tornadoes. Fixed authored cells, simulation events. */
const HR92={base:{start:hr28Start,tick:hd1003Tick,draw:heraldDeathDraw,bg:drawBG,blit:hd1003Blit,
 summon:hh69Summon,stormDraw:hh69StormDraw,stormBlit:hh69Blit,warning:combatWarningTick,
 load:stageLoadBegin,update:updatePlay,state:setState,duck:pauseMusicDuck},
 times:{flash:1.65,warning:2.15,lines:2.20,circle:7.20,spin:7.95,expand:10.20,shatter:11.00,release:11.65},
 events:[],draws:{},owner:null,ducked:false,reduced:typeof matchMedia==='function'&&matchMedia('(prefers-reduced-motion: reduce)').matches,keys:[]};
for(const[name,a]of Object.entries(HR92_ART)){XART._src[a.key]=a.path;ER28_ART['hr92_'+name]=a;}
for(const role of ['slice_0','slice_1','slice_2','lightning']){
 const key='herald92_'+role,uri='assets/game/shared/audio/herald_ritual_1031/'+role+'.mp3',slots=[],list=[];
 for(let i=0;i<(role==='lightning'?4:2);i++)Object.defineProperty(list,i,{enumerable:true,get(){if(!slots[i])slots[i]={el:new window.Audio(),uri,attached:false,used:0};return Snd._touchVoice(slots[i]);}});
 BOFA.sfx[key]=uri;Snd.pools[key]={list,slots,i:0};Snd.TAME[key]={g:role==='lightning'?.84:1.2,native:true,min:.08};Audio.SFX[key]=()=>Snd.play(key);HR92.keys.push(key);
}
function hr92Own(b){const A=b?._hd1003?.er28;return b&&b===subBoss&&run.stage===8&&!b.dead&&b._hd1003.mode==='er28-herald'&&A?.kind==='storm'&&A._hr92?A:null;}
function hr92Log(event,data={}){HR92.events.push({event,time:efxClock,...data});if(HR92.events.length>500)HR92.events.shift();}
function hr92Blit(name,f,x,y){HR92.draws[name]=(HR92.draws[name]||0)+1;return er28Blit('hr92_'+name,f,x,y);}
function hr92Stop(){for(const key of HR92.keys)for(const s of Snd.pools[key].slots)if(s?.el){s.el._bofEpoch=(s.el._bofEpoch||0)+1;s.el.pause();try{s.el.currentTime=0;}catch(e){}}HR92.owner=null;}
hr28Start=function(b,kind){const out=HR92.base.start.apply(this,arguments);if(kind==='storm'&&hh52Special(b)){
 const A=hh52Special(b);A.warm=HR92.times.release;A._hr87Seal=false;A.dark=0;A.stormBolts=[];A.stormFlash=[-100,-100];
 A._hr92={stroke:0,thunder:0,flash:false,burst:false,bolts:[],phase:'warning',dark:0};HR92.owner=b;
 hr92Log('ritual-start',{serial:A.serial,warm:A.warm,hp:b.hp});}return out;};
combatWarningTick=function(b,id,elapsed,duration,silent){const A=hr92Own(b);if(A&&String(id).startsWith('hh52-')){
 if(A.t<=HR92.times.warning)return HR92.base.warning.call(this,b,'hr92-'+A.serial,Math.min(A.t,HR92.times.warning),HR92.times.warning,silent);return;
 }return HR92.base.warning.apply(this,arguments);};
hh69Summon=function(b,A){if(A._hr92)return;return HR92.base.summon.apply(this,arguments);};
function hr92Phase(t){const T=HR92.times;return t<T.lines?'warning':t<T.circle?'lines':t<T.spin?'circle':t<T.expand?'spin':t<T.shatter?'expand':t<T.release?'shatter':'tornado';}
hd1003Tick=function(b,dt){const before=hr92Own(b),out=HR92.base.tick.apply(this,arguments),A=hr92Own(b);
 if(!A)return out;const Q=A._hr92,T=HR92.times,t=A.t;Q.phase=hr92Phase(t);
 Q.dark=t<A.warm+4.8?Math.min(15,Math.floor(t/.65*15)):Math.max(0,15-Math.floor((t-A.warm-4.8)*15));
 if(!Q.flash&&t>=T.flash){Q.flash=true;Snd.play('alertLockon',.85);hr92Log('warning-red-flash',{serial:A.serial,t});}
 while(Q.stroke<6&&t>=T.lines+Q.stroke){const i=Q.stroke++,at=T.lines+i;Snd.play('herald92_slice_'+i%3,1);
  const lane=[.12,.82,.35,.68,.21,.90][i],other=[.73,.25,.90,.16,.62,.40][i];
  for(let j=0;j<3;j++)Q.bolts.push({at:at+.04+j*.08,x:camLeftX()+viewW()*([lane,other,(lane+other)/2][j]),y:viewTopY()+viewH()/2});
  hr92Log(i===5?'circle-slice':'line-slice',{serial:A.serial,index:i,t,at});}
 while(Q.thunder<Q.stroke&&t>=T.lines+Q.thunder+.04){const index=Q.thunder++;Snd.play('herald92_lightning',.88);hr92Log('line-lightning',{serial:A.serial,index,t});}
 if(!Q.burst&&t>=T.shatter){Q.burst=true;combatAudio0927(b,'timedBombBlast',.1);combatAudio0927(b,'iceOrbImpact',.1);hr92Log('seal-shatter',{serial:A.serial,t});}
 if(t<A.warm){
  if(t<T.lines)hh52Clip(b,'cast',Math.floor(t/T.lines*12));
  else if(t<T.spin)hh52Clip(b,'cast',12+Math.min(19,Math.floor((t-T.lines)/(T.spin-T.lines)*20)));
  else hh52Clip(b,'raised',Math.floor((t-T.spin)*(20+Math.min(20,(t-T.spin)*6)))%16);
 }
 return out;
};
hh69Blit=function(name,f,x,y){const A=hr92Own(subBoss);if(name==='warning'&&A){const t=A.t;if(t>=HR92.times.warning)return false;
 const phase=t<.65?0:t<1.25?1:t<HR92.times.flash?2:HR92.reduced?2:Math.floor((t-HR92.times.flash)/.16)%2===0?3:2;
 return hr92Blit('warning',phase,x,y);
 }return HR92.base.stormBlit.apply(this,arguments);};
hh69StormDraw=function(b,A,u){if(A._hr92){for(const p of A._hr92.bolts){const age=A.t-p.at;if(age>=0&&age<16/60)hr92Blit('lightning',Math.floor(age*60),p.x,p.y);}}
 return HR92.base.stormDraw.apply(this,arguments);};
hd1003Blit=function(p,P,flash=0,alpha=1){const A=hr92Own(subBoss);if(A&&A.t<HR92.times.release&&p.id==='head'&&!p.dead)return hs53Blit('head_cast',Math.floor(A.t*(HR92.reduced?12:24))%32,P.x,P.y,flash>0);return HR92.base.blit.apply(this,arguments);};
drawBG=function(){const A=hr92Own(subBoss),old=A?.dark;if(A)A.dark=0;let out;try{out=HR92.base.bg.apply(this,arguments);}finally{if(A)A.dark=old;}
 if(A&&A._hr92.dark>0)for(let y=Math.floor(viewTopY()/64)*64;y<VH;y+=64)for(let x=Math.floor(camLeftX()/64)*64;x<camRightX();x+=64)hr92Blit('dark',A._hr92.dark,x+32,y+32);return out;};
heraldDeathDraw=function(b){const out=HR92.base.draw.apply(this,arguments),A=hr92Own(b);if(!A)return out;
 const T=HR92.times,t=A.t,p=hs53SealPoint(b);let bank,f;
 if(t>=T.lines&&t<T.circle){const i=Math.min(4,Math.floor(t-T.lines)),u=t-T.lines-i;bank='inscribe';f=i*12+Math.min(11,Math.floor(u/.20*12));}
 else if(t>=T.circle&&t<T.spin){bank='inscribe';f=60+Math.min(23,Math.floor((t-T.circle)/.60*24));}
 else if(t>=T.spin&&t<T.expand){bank='spin';f=Math.min(89,Math.floor((t-T.spin)*40));}
 else if(t>=T.expand&&t<T.shatter){bank='expand';f=Math.min(31,Math.floor((t-T.expand)*40));}
 else if(t>=T.shatter&&t<T.release){bank='shatter';f=Math.min(25,Math.floor((t-T.shatter)*40));}
 if(bank){if(HR92.reduced&&bank==='spin')f=Math.floor(f/3)*3;hr92Blit(bank,f,p.x,p.y);}return out;
};
stageLoadBegin=function(n,keys){if(n===8)Snd.prepare([...HR92.keys,'alertLockon','timedBombBlast','iceOrbImpact']);return HR92.base.load.call(this,n,n===8?[...(keys||[]),...Object.values(HR92_ART).map(a=>a.key)]:keys);};
pauseMusicDuck=function(){const A=hr92Own(HR92.owner);return HR92.base.duck()*(A&&A.t<HR92.times.release+.5?.38:1);};
updatePlay=function(dt){const out=HR92.base.update.apply(this,arguments);if(HR92.owner&&!hr92Own(HR92.owner))hr92Stop();const active=!!hr92Own(HR92.owner);
 if(Snd.cur&&(active||HR92.ducked))Snd.cur.volume=clamp(Snd.vol.music*Snd.vol.master*pauseMusicDuck(),0,1);HR92.ducked=active;return out;};
setState=function(next){if(next!==GS.PLAY)hr92Stop();const out=HR92.base.state.apply(this,arguments);if(next===GS.PLAY&&hr92Own(subBoss))HR92.owner=subBoss;return out;};
globalThis.BOF_HERALD_RITUAL=HR92;
