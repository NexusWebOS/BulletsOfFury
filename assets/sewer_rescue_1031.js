'use strict';
/* SR93: constant-speed sewer collapse, last-moment native green gate rescue. */
const SR93={base:{exit:fr27Exit,portal:drawS7FinalPortalWorld,ship:drawPlayer,bg:drawBG,cinematic:s7WardenCinematic,
 load:stageLoadBegin,begin:beginStage,update:updatePlay,master:fr28SewerMaster},events:[],draws:{},owner:null,fx:[],terrain:null,speed:400,extra:6144,tileCut:1024,tileHeight:512,form:1.6,entry:.60,close:.48,white:.38};
for(const[name,a]of Object.entries(SR93_ART)){XART._src[a.key]=a.path;ER28_ART['sr93_'+name]=a;}
function sr93Own(b=boss){return sc86Own(b)&&!!b._s7mod.frExit.sc86.sr93;}
function sr93State(){return sr93Own()?boss._s7mod.frExit.sc86.sr93:null;}
function sr93Log(event,data={}){SR93.events.push({event,time:efxClock,...data});if(SR93.events.length>500)SR93.events.shift();}
function sr93Say(b,text,dur=2.2,who='DECKER'){b._s7warden.final.radio={who,full:text,t:0,typed:0,dur};sr93Log('radio',{who,text});}
function sr93FX(name,x,y){if(SR93.fx.length>=76)return;SR93.fx.push({b:boss,name,x,y,age:0,life:name==='ring'?1.1:name==='engulf'?.78:.60});}
// The original cap and starting floor stay registered. Source-pixel ping-pong
// tiles join identical edge rows; terrain mirroring never changes aircraft art.
fr28SewerMaster=function(){const im=SR93.base.master();if(!sr93Own()||!im)return im;if(SR93.terrain)return SR93.terrain;
 const cut=SR93.tileCut,h=SR93.tileHeight,c=document.createElement('canvas');c.width=im.width;c.height=im.height+SR93.extra;
 const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.drawImage(im,0,0,im.width,cut,0,0,im.width,cut);
 for(let n=0;n<SR93.extra/h;n++){const y=cut+n*h;g.save();if(n%2){g.translate(0,y+h);g.scale(1,-1);g.drawImage(im,0,cut,im.width,h,0,0,im.width,h);}else g.drawImage(im,0,cut,im.width,h,0,y,im.width,h);g.restore();}
 g.drawImage(im,0,cut,im.width,im.height-cut,0,cut+SR93.extra,im.width,im.height-cut);SR93.terrain=c;return c;
};
function sr93Dodge(C,dt){const lanes=[.72,.25,.78,.31,.66,.22,.74,.38],n=Math.floor(C.t/1.35),u=C.t/1.35-n,k=u*u*(3-2*u);
 for(const seat of seatList())withSeat(seat,()=>{if(player.dead||player.out)return;
  const flight=C.flight[seat]||(C.flight[seat]={start:player.x,last:player.x,bank:0}),span=worldWidth()-130,
   lane=i=>seat===2?1-lanes[(i+3)%lanes.length]:lanes[i%lanes.length],from=n?65+span*lane(n-1):flight.start,to=65+span*lane(n),target=lerp(from,to,k);
  if(!Input.hold(seat,'left')&&!Input.hold(seat,'right'))player.x+=clamp(target-player.x,-380*dt,380*dt);
  player.x=clamp(player.x,65,worldWidth()-65);player.y=clamp(player.y,VH*.64,VH-45);
  const vx=(player.x-flight.last)/Math.max(dt,.001);flight.bank=lerp(flight.bank,clamp(vx/260,-.76,.76),1-Math.exp(-dt*12));player._bank=flight.bank;flight.last=player.x;
 });
 if(n!==C.dodge){C.dodge=n;sr93Log('dodge',{lane:n,x:player.x});if(n>0){sr93FX('barrage',player.x+(n%2?80:-80),player.y+35);combatAudio0927(boss,'jetDash',.4);}}
}
function sr93DrawFX(){for(const f of SR93.fx){const a=SR93_ART[f.name],frame=Math.min(a.frames-1,Math.floor(f.age/f.life*a.frames));er28Blit('sr93_'+f.name,frame,f.x,f.y);SR93.draws[f.name]=(SR93.draws[f.name]||0)+1;}}
function sr93Phase(b,phase){const E=b._s7mod.frExit,Q=E.sc86,C=Q.sr93;C.phase=phase;C.t=0;Q.t=0;Q.phase=phase==='run'?'advance':phase;sr93Log('phase',{phase,source:Q.source,portalY:E.portalY,shipY:player.y});
 if(phase==='form'){combatAudio0927(b,'warpCharge',.2);C.alarm=false;C.look=seatList().map(s=>withSeat(s,()=>({seat:s,x:player.x,y:player.y})));sr93Say(b,"A PORTAL... IT'S THE ONLY WAY OUT!",2.4,String(run.pilot||'cole').toUpperCase());sr93Log('portal-sighted',{x:E.portalX,y:E.portalY});}
 if(phase==='enter'){C.seats=seatList().map(s=>withSeat(s,()=>({seat:s,x:player.x,y:player.y})));Q.seats=C.seats;sr93Say(b,'HERE GOES NOTHING!',2.5,String(run.pilot||'cole').toUpperCase());combatAudio0927(b,'jetDash',.2);combatAudio0927(b,'warpGate',.2);}
 if(phase==='close'){b._s7warden.final.shipHidden=true;C.goneAt=Q.age;C.safeMargin=C.frontY-E.portalY;sr93Log('saved-before-blast',{margin:C.safeMargin,portalY:E.portalY});combatAudio0927(b,'warpBurst',.2);sr93FX('ring',E.portalX,E.portalY);sr93FX('engulf',E.portalX,E.portalY);for(let i=0;i<8;i++)sr93FX('engulf',camLeftX()+(i%3+.5)*viewW()/3,viewTopY()+90+Math.floor(i/3)*155);}
}
fr27Exit=function(b,dt){if(run.stage!==7||!b?._s7mod||b._s7mod.tank)return SR93.base.exit.apply(this,arguments);
 let E=b._s7mod.frExit;if(!E?.sc86){SR93.base.exit.call(this,b,0);E=b._s7mod.frExit;}
 const Q=E.sc86,M=b._s7mod,F=b._s7warden.final;
 if(!Q.sr93){Q.sr93={phase:'run',t:0,fx:0,hole:0,ring:0,beat:0,frontY:VH+100,alarm:false,flight:{},dodge:-1};Q.source+=SR93.extra;Q.startSource=E.sourceY=Q.source;E.travel=0;Q.age=Q.t=0;Q.phase='advance';Q.flash=0;SR93.owner=b;SR93.fx=[];sr93Say(b,'SELF-DESTRUCT! KEEP MOVING!',2.0);combatAudio0927(b,'jetDash',.2);sr93Log('escape-start',{source:Q.source,speed:SR93.speed,extra:SR93.extra,pilot:run.pilot});}
 const C=Q.sr93;if(C.phase==='done')return true;dt=clamp(dt||0,0,.05);Q.age+=dt;Q.t+=dt;C.t+=dt;E.t=Q.age;M.t=Q.age;M.clock+=dt;F.phase='escape';F.shipHidden=['close','white'].includes(C.phase);b._s7FinalNoBar=true;b._s7warden.noHit=true;bossDefeated=true;
 const old=Q.source,speed=C.phase==='run'?SR93.speed:C.phase==='form'?120:60;if(!F.shipHidden)Q.source=Math.max(0,Q.source-speed*dt);const d=old-Q.source;E.travel=E.sourceY-Q.source;E.portalX=SC86.aperture.x;E.portalY=SC86.aperture.y-Q.source;_masterSrcY=Q.source;mapScroll=levelScrollRange()-clamp(Q.source-SR93.extra,0,levelScrollRange());b.y=E.groundY+E.travel;F.bossHidden=b.y-(b.h||260)*.5>VH+50;
 for(const f of SR93.fx){f.age+=dt;f.y+=d;}SR93.fx=SR93.fx.filter(f=>f.age<f.life&&f.y<VH+320);
 for(const s of seatList())withSeat(s,()=>{player.invuln=Math.max(player.invuln||0,3);player._thrustPower=1;});
 for(const q of eBullets)q.dead=true;for(const p of powerups)if(p.kind!=='forgecombo')p.dead=true;
 if(F.radio){F.radio.t+=dt;F.radio.typed+=dt*100;if(F.radio.t>F.radio.dur)F.radio=null;}
 const hidden=F.shipHidden;C.fx-=dt;C.ring-=dt;C.hole-=dt;
 if(C.hole<=0&&E.portalY>-160&&E.portalY<VH+160){C.hole=hidden?.09:.16;const side=C.beat%2?1:-1;
  sr93FX(hidden?'engulf':'dense',E.portalX+(hidden?0:side*112),E.portalY+(hidden?0:side*48));if(hidden)sr93FX('barrage',E.portalX-side*65,E.portalY+side*45);
 }
 if(C.fx<=0){C.fx=hidden?.045:.075;const n=C.beat++,x=camLeftX()+viewW()*((n*.38196601125)%1),side=n%2?camLeftX()+55:camRightX()-55;
  sr93FX(hidden?'engulf':n%3===0?'barrage':'dense',hidden?x:side,viewTopY()+65+(n*83)%(viewH()-110));
  if(!hidden)sr93FX(n%2?'dense':'barrage',x,viewTopY()+50+(n*61)%(viewH()-110));
  if(n%2===0)sr93FX('radial',x,Math.max(C.frontY,viewTopY()+40)+(n%3)*25);
  if(n%3===0)combatAudio0927(b,hidden?'expBig':'expSmall',hidden?.16:.22);
 }
 if(C.ring<=0){C.ring=hidden?.35:.65;sr93FX('ring',camLeftX()+viewW()*((C.beat*.618034)%1),Math.min(VH+15,C.frontY));}
 if(C.phase==='run'){
  C.frontY=VH+55;sr93Dodge(C,dt);if(Q.source<=400)sr93Phase(b,'form');
 }else if(C.phase==='form'){
  C.frontY=VH+25;const u=clamp(C.t/SR93.form,0,1),k=u*u*(3-2*u);for(const s of C.look)withSeat(s.seat,()=>{player.x=lerp(s.x,E.portalX,k*.8);player._bank=clamp((E.portalX-s.x)/250,-.5,.5)*(1-u);});
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
drawS7FinalPortalWorld=function(){const C=sr93State();if(!C)return SR93.base.portal.apply(this,arguments);const E=boss._s7mod.frExit;
 if(C.phase==='form')sc86Gate('green','form',C.t,E.portalX,E.portalY,SR93.form);
 else if(C.phase==='enter')sc86Gate('green','loop',C.t,E.portalX,E.portalY);
 else if(C.phase==='close')sc86Gate('green','close',C.t,E.portalX,E.portalY,SR93.close);
 sr93DrawFX();
};
drawPlayer=function(){const C=sr93State();if(!C)return SR93.base.ship.apply(this,arguments);if(['close','white','done'].includes(C.phase))return;
 if(C.phase==='enter'){const a=RD84_ART.banks['ship_north_'+run.pilot],shrink=clamp((C.t/SR93.entry-.50)/.50,0,1);return rd84Blit(a[Math.round((1-shrink)*31)],player.x,player.y);}return SR93.base.ship.apply(this,arguments);};
drawBG=function(){return SR93.base.bg.apply(this,arguments);};
stageLoadBegin=function(n,keys){if(n===7)Snd.prepare(['jetDash','warpCharge','warpGate','warpBurst','expSmall','expBig']);return SR93.base.load.call(this,n,n===7?[...(keys||[]),...Object.values(SR93_ART).map(a=>a.key)]:keys);};
beginStage=function(){SR93.owner=null;SR93.fx=[];SR93.terrain=null;return SR93.base.begin.apply(this,arguments);};
updatePlay=function(){const out=SR93.base.update.apply(this,arguments);if(SR93.owner&&(!sr93Own(SR93.owner)||SR93.owner.dead)){SR93.owner=null;SR93.fx=[];}return out;};
globalThis.BOF_SEWER_RESCUE=SR93;
