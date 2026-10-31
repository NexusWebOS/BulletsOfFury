'use strict';
/* WS56: front-most live barrels, exposed-core slam book, removed sluice hazards. */
const WS56={base:{pose:s7mPose,bank:sw28Bank,next:s7mNext,set:s7mSet,tick:s7mTick,draw:s7mDraw,warnings:s7mWarnings,
 load:stageLoadBegin,update:updatePlay,effects:drawEffects},events:[],fx:[]};
for(const[name,a]of Object.entries(WS56_ART)){ER28_ART['ws56_'+name]=a;XART._src[a.key]=a.path;}
function ws56Own(b){return wl39Own(b);}
function ws56Ready(b){const M=b?._s7mod;return ws56Own(b)&&!b.dead&&!M.frExit&&M.mode!=='dead'&&!sw28Limbs(M)&&!sw28Can(M).length;}
function ws56Active(b){return ws56Own(b)&&!b.dead&&!b._s7mod.frExit&&b._s7mod.mode.startsWith('ws56-')?b._s7mod.ws56:null;}
function ws56Log(event,data={}){WS56.events.push({event,time:efxClock,...data});if(WS56.events.length>900)WS56.events.shift();}
// These outlets are independent scenery/hazard actors, not the sewer floor.
stage7SluiceEvents=function(){if(run)run._s7Sluices=[];return[];};
stage7SluiceTick=function(){if(run?.stage===7)run._s7Sluices=[];};
stage7SluiceDraw=function(){};
stageLoadBegin=function(n,keys){if(n===7)Snd.prepare(['bodyDrop','combatToxic0927','bossWeaponCharge']);return WS56.base.load.call(this,n,n===7?[...(keys||[]),...Object.values(WS56_ART).map(a=>a.key)]:keys);};
s7mPose=function(b){let out=WS56.base.pose.apply(this,arguments);if(!ws56Own(b))return out;const A=ws56Active(b);
 if(A)out=[{id:'body',cell:0,x:0,y:-18,w:288,h:288,a:0},...out.filter(p=>p.id.startsWith('gun'))];
 // The native renderer paints in this order; hit-mask priority follows it too.
 return[...out.filter(p=>!p.id.startsWith('gun')),...out.filter(p=>p.id.startsWith('gun'))];};
sw28Bank=function(b,p){const A=ws56Active(b);if(A&&p.id==='body')return{name:A.kind==='spin'?'ws56_core':'ws56_front',f:A.frame};return WS56.base.bank.apply(this,arguments);};
s7mNext=function(b){if(!ws56Ready(b))return WS56.base.next.apply(this,arguments);const M=b._s7mod;
 const book=s7mLive(M,'gun').length?['er28-guns','ws56-spin','ws56-hop','er28-mortar']:['ws56-spin','ws56-hop','er28-mortar'];
 const kind=book[(M.ws56Turn||0)%book.length];M.ws56Turn=(M.ws56Turn||0)+1;M.seq++;return s7mSet(b,kind);};
s7mSet=function(b,mode){const out=WS56.base.set.apply(this,arguments);if(!ws56Own(b))return out;const M=b._s7mod;delete M.ws56;
 if(!mode.startsWith('ws56-'))return out;const kind=mode==='ws56-spin'?'spin':'hop',cx=worldWidth()/2,cy=VH*.50;
 const targets=kind==='spin'?Array.from({length:5},(_,i)=>({x:cx+Math.sin(i*TAU/5)*Math.min(76,viewW()*.15),y:cy+Math.cos(i*TAU/5)*42})):
 [{x:cx,y:cy-76},{x:cx,y:cy+65},{x:cx,y:cy}];
 Object.assign(M,{warn:.95,height:0,lean:0,ws56:{kind,t:0,frame:0,angle:0,cycle:0,period:kind==='spin'?1.08:1.16,targets,from:{x:b.x,y:b.y},last:{x:b.x,y:b.y},landed:-1}});
 b._s4MiniSafe=true;combatAudio0927(b,'bossWeaponCharge',.15);ws56Log('attack-start',{kind,targets,core:M.core});return out;};
function ws56Landing(b,A,P,index){const M=b._s7mod,ground={x:P.x,y:P.y+M.drop+40},count=8+M.n*3;
 M.height=0;for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(player.x-ground.x,player.y-ground.y)<34)playerHit('Warden core ground slam');});
 for(let i=0;i<count;i++){if(!sw28Budget(b))break;sw28Orb(b,ground.x,ground.y,i*TAU/count+index*.31,2.45+M.n*.12);}
 WS56.fx.push({b,x:ground.x,y:ground.y,t:0});shake=Math.max(shake,4);combatAudio0927(b,'bodyDrop',.2);combatAudio0927(b,'combatToxic0927',.15);
 ws56Log('slam',{kind:A.kind,index,x:P.x,y:P.y,impact:ground,count});
}
s7mTick=function(b,dt){const A=ws56Active(b);if(!A)return WS56.base.tick.apply(this,arguments);const M=b._s7mod;
 sw28Common(b,dt);M.lean=0;b._s4MiniSafe=true;A.t+=dt;A.angle+=dt*(A.kind==='spin'?TAU*1.1:0);A.frame=A.kind==='spin'?Math.floor(A.angle/TAU*32)%32:Math.floor(M.clock*20)%16;
 const u=A.t-M.warn;if(u<0){M.height=0;combatWarningTick(b,'ws56-'+A.kind,M.t,M.warn);}
 else{const cycle=Math.min(A.targets.length-1,Math.floor(u/A.period)),v=clamp((u-cycle*A.period)/A.period,0,1),end=A.targets[cycle],from=cycle?A.targets[cycle-1]:A.from;
  const ease=v*v*(3-2*v);b.x=lerp(from.x,end.x,ease);b.y=lerp(from.y,end.y,ease);M.height=Math.sin(v*Math.PI)*(A.kind==='spin'?86:128);
  // The warning is committed a whole hop before the matching actual impact.
  A.cycle=cycle;A.progress=v;
  const completed=Math.min(A.targets.length,Math.floor((u+1e-7)/A.period));
  while(A.landed<completed-1){A.landed++;const target=A.targets[A.landed];ws56Landing(b,A,target,A.landed);}
  if(u>=A.period*A.targets.length){M.height=0;const end=A.targets.at(-1),v=clamp((u-A.period*A.targets.length)/.65,0,1),k=v*v*(3-2*v);
   b.x=lerp(end.x,worldWidth()/2,k);b.y=lerp(end.y,VH*.5,k);
   if(v>=1){ws56Log('attack-complete',{kind:A.kind,x:b.x,y:b.y});s7mSet(b,'recover');}}
 }
 b._drawY=b.y+M.drop-M.height;const G=r25Gait(b);G.yaw=0;G.speed=0;G.floorRate=0;G.lastDX=G.lastDY=0;return true;
};
s7mDraw=function(b){const A=ws56Active(b);if(!A)return WS56.base.draw.apply(this,arguments);const M=b._s7mod,f=A.kind==='spin'?A.frame:0;
 er28Blit('ws56_shadow',f,b.x,b.y+M.drop+25);
 er28Blit(A.kind==='spin'?'ws56_core':'ws56_front',A.frame,b.x,b.y+M.drop-M.height-18,Math.max(b.flash||0,M.coreFlash||0)>0);
 for(const p of s7mPose(b).filter(p=>p.id.startsWith('gun'))){const part=M.parts.find(q=>q.id===p.id);if(!part||part.hp<=0)continue;const q=s7mWorld(b,p),bank=sw28Bank(b,p);if(bank)er28Blit(bank.name,bank.f,q.x,q.y,part.flash>0);}
 return true;
};
s7mWarnings=function(front){const A=ws56Active(boss);if(!A)return WS56.base.warnings.apply(this,arguments);if(front)return;const M=boss._s7mod;
 if(A.t>=M.warn+A.period*A.targets.length)return;
 const index=Math.min(A.targets.length-1,A.t<M.warn?0:Math.floor((A.t-M.warn)/A.period)),target=A.targets[index],k=A.t<M.warn?A.t/M.warn:(A.t-M.warn)%A.period/A.period;
 df55Blit('ground_'+(k<.5?'green':k<.8?'yellow':'red'),0,target.x,target.y+M.drop+40);
};
updatePlay=function(dt){const out=WS56.base.update.apply(this,arguments);for(const F of WS56.fx)F.t+=dt;WS56.fx=WS56.fx.filter(F=>F.t<.5&&F.b===boss&&!F.b.dead&&F.b._s7mod.mode!=='dead'&&run.stage===7);return out;};
drawEffects=function(){const out=WS56.base.effects.apply(this,arguments);for(const F of WS56.fx)df55Blit('ooze',Math.min(15,Math.floor(F.t/.5*16)),F.x,F.y);return out;};
globalThis.BOF_WARDEN_SPIN_1029={state:WS56};
