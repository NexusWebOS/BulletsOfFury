'use strict';
/* SR93: constant-speed sewer collapse, last-moment native green gate rescue. */
const SR93={base:{exit:fr27Exit,portal:drawS7FinalPortalWorld,ship:drawPlayer,bg:drawBG,cinematic:s7WardenCinematic,
 load:stageLoadBegin,begin:beginStage,update:updatePlay},events:[],draws:{},owner:null,fx:[],speed:400,form:.60,entry:.70,close:.48,white:.38};
for(const[name,a]of Object.entries(SR93_ART)){XART._src[a.key]=a.path;ER28_ART['sr93_'+name]=a;}
function sr93Own(b=boss){return sc86Own(b)&&!!b._s7mod.frExit.sc86.sr93;}
function sr93State(){return sr93Own()?boss._s7mod.frExit.sc86.sr93:null;}
function sr93Log(event,data={}){SR93.events.push({event,time:efxClock,...data});if(SR93.events.length>500)SR93.events.shift();}
function sr93Say(b,text,dur=2.2){b._s7warden.final.radio={who:'DECKER',full:text,t:0,typed:0,dur};sr93Log('radio',{who:'DECKER',text});}
function sr93FX(name,x,y){if(SR93.fx.length>=76)return;SR93.fx.push({b:boss,name,x,y,age:0,life:name==='ring'?1.1:name==='engulf'?.78:.60});}
function sr93Phase(b,phase){const E=b._s7mod.frExit,Q=E.sc86,C=Q.sr93;C.phase=phase;C.t=0;Q.t=0;Q.phase=phase==='run'?'advance':phase;sr93Log('phase',{phase,source:Q.source,portalY:E.portalY,shipY:player.y});
 if(phase==='form'){combatAudio0927(b,'warpCharge',.2);C.alarm=false;}
 if(phase==='enter'){C.seats=seatList().map(s=>withSeat(s,()=>({seat:s,x:player.x,y:player.y})));Q.seats=C.seats;combatAudio0927(b,'warpGate',.2);}
 if(phase==='close'){b._s7warden.final.shipHidden=true;C.goneAt=Q.age;C.safeMargin=C.frontY-E.portalY;sr93Log('saved-before-blast',{margin:C.safeMargin,portalY:E.portalY});combatAudio0927(b,'warpBurst',.2);sr93FX('ring',E.portalX,E.portalY);for(let i=0;i<8;i++)sr93FX('engulf',camLeftX()+(i%3+.5)*viewW()/3,viewTopY()+90+Math.floor(i/3)*155);}
}
fr27Exit=function(b,dt){if(run.stage!==7||!b?._s7mod||b._s7mod.tank)return SR93.base.exit.apply(this,arguments);
 let E=b._s7mod.frExit;if(!E?.sc86){SR93.base.exit.call(this,b,0);E=b._s7mod.frExit;}
 const Q=E.sc86,M=b._s7mod,F=b._s7warden.final;
 if(!Q.sr93){Q.sr93={phase:'run',t:0,fx:0,ring:0,beat:0,frontY:VH+100,alarm:false};Q.age=Q.t=0;Q.phase='advance';Q.flash=0;SR93.owner=b;SR93.fx=[];sr93Say(b,'SELF-DESTRUCT! KEEP MOVING!',2.0);combatAudio0927(b,'jetDash',.2);sr93Log('escape-start',{source:Q.source,speed:SR93.speed,pilot:run.pilot});}
 const C=Q.sr93;if(C.phase==='done')return true;dt=clamp(dt||0,0,.05);Q.age+=dt;Q.t+=dt;C.t+=dt;E.t=Q.age;M.t=Q.age;M.clock+=dt;F.phase='escape';F.shipHidden=['close','white'].includes(C.phase);b._s7FinalNoBar=true;b._s7warden.noHit=true;bossDefeated=true;
 const old=Q.source;if(!F.shipHidden)Q.source=Math.max(0,Q.source-SR93.speed*dt);const d=old-Q.source;E.travel=E.sourceY-Q.source;E.portalX=SC86.aperture.x;E.portalY=SC86.aperture.y-Q.source;_masterSrcY=Q.source;mapScroll=levelScrollRange()-Q.source;b.y=E.groundY+E.travel;F.bossHidden=b.y-(b.h||260)*.5>VH+50;
 for(const f of SR93.fx){f.age+=dt;f.y+=d;}SR93.fx=SR93.fx.filter(f=>f.age<f.life&&f.y<VH+320);
 for(const s of seatList())withSeat(s,()=>{player.invuln=Math.max(player.invuln||0,3);player._thrustPower=1;});
 for(const q of eBullets)q.dead=true;for(const p of powerups)if(p.kind!=='forgecombo')p.dead=true;
 if(F.radio){F.radio.t+=dt;F.radio.typed+=dt*100;if(F.radio.t>F.radio.dur)F.radio=null;}
 const hidden=F.shipHidden;C.fx-=dt;C.ring-=dt;
 if(C.fx<=0){C.fx=hidden?.045:.075;const n=C.beat++,x=camLeftX()+viewW()*((n*.38196601125)%1),side=n%2?camLeftX()+55:camRightX()-55;
  sr93FX(hidden?'engulf':n%3===0?'barrage':'dense',hidden?x:side,viewTopY()+65+(n*83)%(viewH()-110));
  if(!hidden)sr93FX(n%2?'dense':'barrage',x,viewTopY()+50+(n*61)%(viewH()-110));
  if(n%2===0)sr93FX('radial',x,Math.max(C.frontY,viewTopY()+40)+(n%3)*25);
  if(n%3===0)combatAudio0927(b,hidden?'expBig':'expSmall',hidden?.16:.22);
 }
 if(C.ring<=0){C.ring=hidden?.35:.65;sr93FX('ring',camLeftX()+viewW()*((C.beat*.618034)%1),Math.min(VH+15,C.frontY));}
 if(C.phase==='run'){
  C.frontY=VH+55;for(const s of seatList())withSeat(s,()=>{player.y=clamp(player.y,VH*.62,VH-45);});if(Q.source<=520)sr93Phase(b,'form');
 }else if(C.phase==='form'){
  C.frontY=VH+25;if(!C.alarm&&C.t>=.16){C.alarm=true;const name=(PILOTS.find(p=>p.key===run.pilot)?.name||run.pilot).toUpperCase();sr93Say(b,'WHAT IS THAT? '+name+', NOOOO!',3.2);}
  if(C.t>=SR93.form)sr93Phase(b,'enter');
 }else if(C.phase==='enter'){
  const u=clamp(C.t/SR93.entry,0,1),k=u*u*(3-2*u);C.frontY=lerp(VH+25,E.portalY+22,k);
  for(const s of C.seats)withSeat(s.seat,()=>{player.x=lerp(s.x,E.portalX,k);player.y=lerp(s.y,E.portalY,k);});
  if(u>=1)sr93Phase(b,'close');
 }else if(C.phase==='close'){
  C.frontY=E.portalY-80;Q.flash=Math.min(3,Math.floor(C.t/.20*4));if(C.t>=SR93.close)sr93Phase(b,'white');
 }else if(C.phase==='white'){
  Q.flash=Math.min(6,3+Math.floor(C.t/SR93.white*4));if(C.t>=SR93.white){C.phase='done';Q.phase='done';sr93Log('native-finish',{source:Q.source,age:Q.age});
   Object.assign(E,{s67:true,k1001:true,S:E.travel,x:b.x,v:0,t:Q.age,beat:4,zoom:1,done:false,portalOn:false,portalYNow:E.portalY,closeT:Q.age-7,entry:{gone:true,goneAt:Q.age-8,t0:0},flame:{t0:Q.age-8,k:1,fx:1e9}});
   return SC86.base.exit.call(this,b,0);}
 }
 return true;
};
s7WardenCinematic=function(){const C=sr93State();return C?C.phase!=='run':SR93.base.cinematic.apply(this,arguments);};
drawS7FinalPortalWorld=function(){const C=sr93State();if(!C)return SR93.base.portal.apply(this,arguments);const E=boss._s7mod.frExit;sc86Blit('seal',0,E.portalX,E.portalY);
 if(C.phase==='form')return sc86Gate('green','form',C.t,E.portalX,E.portalY,SR93.form);
 if(C.phase==='enter')return sc86Gate('green','loop',C.t,E.portalX,E.portalY);
 if(C.phase==='close')return sc86Gate('green','close',C.t,E.portalX,E.portalY,SR93.close);
};
drawPlayer=function(){const C=sr93State();if(!C)return SR93.base.ship.apply(this,arguments);if(['close','white','done'].includes(C.phase))return;
 if(C.phase==='enter'){const a=RD84_ART.banks['ship_north_'+run.pilot],shrink=clamp((C.t/SR93.entry-.50)/.50,0,1);return rd84Blit(a[Math.round((1-shrink)*31)],player.x,player.y);}return SR93.base.ship.apply(this,arguments);};
drawBG=function(){const out=SR93.base.bg.apply(this,arguments);if(sr93State())for(const f of SR93.fx){const a=SR93_ART[f.name],frame=Math.min(a.frames-1,Math.floor(f.age/f.life*a.frames));er28Blit('sr93_'+f.name,frame,f.x,f.y);SR93.draws[f.name]=(SR93.draws[f.name]||0)+1;}return out;};
stageLoadBegin=function(n,keys){if(n===7)Snd.prepare(['jetDash','warpCharge','warpGate','warpBurst','expSmall','expBig']);return SR93.base.load.call(this,n,n===7?[...(keys||[]),...Object.values(SR93_ART).map(a=>a.key)]:keys);};
beginStage=function(){SR93.owner=null;SR93.fx=[];return SR93.base.begin.apply(this,arguments);};
updatePlay=function(){const out=SR93.base.update.apply(this,arguments);if(SR93.owner&&(!sr93Own(SR93.owner)||SR93.owner.dead)){SR93.owner=null;SR93.fx=[];}return out;};
globalThis.BOF_SEWER_RESCUE=SR93;
