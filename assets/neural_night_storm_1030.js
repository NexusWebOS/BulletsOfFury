'use strict';
/* NB81: night-cloud arena and unboxed code storm. The warning belongs to the
   caster; eruption positions commit once. Original plume alpha owns damage. */
const NB81={base:{start:nb23Start,tick:nb23AttackTick,body:nb23Body,draw:r30DrawBoss,warnings:nb23Warnings,scene:ad20Scene,bg:drawBG,keys:v18Keys,warm:v18Warm,load:stageLoadBegin,clear:v18Clear,sound:r30Sound,state:setState},events:[],draws:{},dim:0,audioOwner:null,tickOwner:null};
for(const [key,a]of Object.entries(NB81_ART.pages))XART._src[key]=a.path;
for(const a of Object.values(NB81_ART.arena))XART._src[a.key]=a.path;
function nb81Keys(){return[...Object.keys(NB81_ART.pages),...Object.values(NB81_ART.arena).map(a=>a.key),'cf50_scenery_dim',RD72_ART.asterisk.key];}
v18Keys=function(){return[...NB81.base.keys(),...nb81Keys()];};
v18Warm=function(){const prior=NB81.base.warm();return nb81Keys().map(k=>XART.rdy(k)).every(Boolean)&&prior;};
stageLoadBegin=function(n,keys){if(NB81.audioOwner){Snd.stopCue(CF48.key);NB81.audioOwner=null;}if(n===8)Snd.prepare(CF48.key);return NB81.base.load.call(this,n,n===8?[...(keys||[]),...nb81Keys()]:keys);};
function nb81Act(b){return b&&!b.dead&&nb23Own(b)&&b._r30.mode==='fight'&&b._r30.v18.attack?.type==='codeGeysers'?b._r30.v18.attack:null;}
function nb81Log(event,data={}){NB81.events.push({event,...data});if(NB81.events.length>160)NB81.events.shift();}
function nb81Targets(seed,count,left,right,top,safeLeft){let z=seed>>>0;const rand=()=>{z^=z<<13;z^=z>>>17;z^=z<<5;return(z>>>0)/4294967296;},lo=left+(safeLeft?125:40),hi=right-(safeLeft?40:125),span=hi-lo,order=Array.from({length:count},(_,i)=>i);for(let i=count-1;i>0;i--){const j=Math.floor(rand()*(i+1));[order[i],order[j]]=[order[j],order[i]];}
 return order.map(i=>({x:Math.round(lo+span*(i+.5+(rand()-.5)*.2)/count),y:Math.round(top+245+rand()*(VH-top-277)),released:false}));
}
nb23Start=function(b,type){const out=NB81.base.start.apply(this,arguments),P=nb81Act(b);if(!P)return out;const N=b._r30.v18,d=Math.min(2,v18Diff()),count=P.targets.length;
 N.nb81Casts=(N.nb81Casts||0)+1;P._nb81=true;P.tell=diffKey==='easy'?2.2:[2,1.8,1.6][d];P.safeLeft=player.x<=camLeftX()+viewW()/2;P.safeX=P.safeLeft?camLeftX()+55:camRightX()-55;
 P.seed=((N.seq*2654435761)^(N.nb81Casts*2246822519)^(Math.round(player.x)*31+Math.round(player.y)))>>>0||1;
 P.bounds={left:camLeftX(),right:camRightX(),top:viewTopY()};P.targets=nb81Targets(P.seed,count,P.bounds.left,P.bounds.right,P.bounds.top,P.safeLeft).map((q,i)=>({...q,at:i*[.40,.34,.29][d]}));
 nb81Log('storm-charge',{tell:P.tell,seed:P.seed,safeX:P.safeX,targets:P.targets.map(q=>({...q})),hp:b.hp});return out;
};
function nb81Level(P){if(P.t<P.tell){const u=P.t/P.tell;return clamp(Math.round(1+u*3+Math.sin(P.t*(15+u*15))*.9),1,5);}if(P.t<P.tell+P.active)return 4+Math.floor(P.t*9)%2;return Math.round(4*(1-clamp((P.t-P.tell-P.active)/P.recover,0,1)));}
function nb81Blit(name,f,x,y){const a=NB81_ART.banks[name][f];if(!XART.rdy(a.key))return false;ctx.drawImage(XART.get(a.key),...a.rect,Math.round(x+a.offset[0]),Math.round(y+a.offset[1]),a.w,a.h);NB81.draws[name]=(NB81.draws[name]||0)+1;return true;}
function nb81Body(b){const P=nb81Act(b),f=Math.floor((b._r30.v18.brainAge||0)*10)%9;nb81Blit('glow_'+nb81Level(P),f,b.x,b.y);
 // Keep native white damage feedback; the authored halo remains outside it.
 if(Math.max(b.flash||0,b.parts[0]?.flash||0)>0)nb23Blit(nb23Actor(b),b.x,b.y,true);
 nb80Blit('eyes_brain',f,b.x,b.y);
}
nb23Body=function(b){return nb81Act(b)?nb81Body(b):NB81.base.body.apply(this,arguments);};
nb23Warnings=function(b,P){if(nb81Act(b)){NB81.draws.boxesSuppressed=(NB81.draws.boxesSuppressed||0)+1;return;}return NB81.base.warnings.apply(this,arguments);};
r30DrawBoss=function(b){const P=nb81Act(b);if(!P)return NB81.base.draw.apply(this,arguments);const u=P.t-P.tell;
 if(u<0){const y=Math.min(VH-96,b.y+155);rd72Blit('asterisk',Math.floor(P.t*9)%2,b.x,y);NB81.draws.asterisk=(NB81.draws.asterisk||0)+1;NB81.warning={x:b.x,y,kind:'single-metal-asterisk'};}
 nb23Warnings(b,P);nb81Body(b);
 for(const q of P.targets){const age=u-q.at;if(age>=0&&age<.85)nb23Blit(nb23Cell('geyser',Math.floor(age/.85*NB23_ART.banks.geyser.length)),q.x,q.y);}
};
nb23AttackTick=function(b,dt){const P=nb81Act(b);if(!P)return NB81.base.tick.apply(this,arguments);NB81.tickOwner=b;try{return NB81.base.tick.apply(this,arguments);}finally{NB81.tickOwner=null;}};
r30Sound=function(key){if(key==='expBig'&&NB81.tickOwner){NB81.audioOwner=NB81.tickOwner;Snd.play(CF48.key,.68);nb81Log('lightning-release',{clock:NB81.tickOwner._r30.clock});return;}return NB81.base.sound.apply(this,arguments);};
ad20Scene=function(b,theme,wire=false){if(theme!=='sky')return NB81.base.scene.apply(this,arguments);const t=b._r30.clock||0,draw=(name,rate)=>{const a=NB81_ART.arena[name];if(!XART.rdy(a.key))return;const y=Math.floor(t*rate)%a.h;for(let n=-1;n<2;n++)ctx.drawImage(XART.get(a.key),0,y+n*a.h);NB81.draws[name]=(NB81.draws[name]||0)+1;return y;};
 const far=draw(wire?'download':'sky',3),near=wire?null:draw('clouds',9);NB81.scene={theme:'night-clouds',wire,worldX:0,far,near,t};return true;
};
drawBG=function(){const out=NB81.base.bg.apply(this,arguments),P=nb81Act(boss);NB81.dim=P?(P.t<P.tell?Math.round(P.t/P.tell*8):P.t<P.tell+P.active?8:Math.round(8*(1-clamp((P.t-P.tell-P.active)/P.recover,0,1)))):0;if(NB81.dim)cf50DimDraw(NB81.dim);return out;};
v18Clear=function(b){if(NB81.audioOwner===b){Snd.stopCue(CF48.key);NB81.audioOwner=null;}if(nb81Act(b))nb81Log('cancel');return NB81.base.clear.apply(this,arguments);};
setState=function(s){if(s!==GS.PLAY&&NB81.audioOwner){Snd.stopCue(CF48.key);NB81.audioOwner=null;}return NB81.base.state.apply(this,arguments);};
globalThis.BOF_NEURAL_NIGHT_STORM_1030=NB81;
