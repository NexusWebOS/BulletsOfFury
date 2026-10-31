'use strict';
/* SC86: original stone aperture, continuous post-Warden route and actual PixelLab
   metal-gated portals. Existing finale owns its one reward and stage transition. */
const SC86={base:{exit:fr27Exit,master:fr28SewerMaster,bg:drawBG,portal:drawS7FinalPortalWorld,camera:fr27CinematicCamera,cinematic:s7WardenCinematic,ship:drawPlayer,radio:s7WardenRadioDraw,load:stageLoadBegin,begin:beginStage,state:setState,gate:rd84Gate},events:[],draws:{},owner:null,aperture:{x:343,y:310}};
for(const a of Object.values(SC86_ART))XART._src[a.key]=a.path;
function sc86Log(event,data={}){SC86.events.push({event,time:efxClock,...data});if(SC86.events.length>500)SC86.events.shift();}
function sc86Own(b=boss){return run.stage===7&&b===boss&&!!b?._s7mod?.frExit?.sc86&&!b._s7mod.tank;}
function sc86State(){return sc86Own()?boss._s7mod.frExit.sc86:null;}
function sc86Blit(name,frame,x,y){const a=SC86_ART[name];if(!a||!XART.rdy(a.key))return false;frame=clamp(frame|0,0,a.frames-1);ctx.drawImage(XART.get(a.key),frame%a.cols*a.cw,Math.floor(frame/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);SC86.draws[name]=(SC86.draws[name]||0)+1;return true;}
function sc86Gate(color,phase,t,x,y,duration){const a=SC86_ART[color+'_'+phase],f=phase==='loop'?Math.floor(t*a.fps)%a.frames:Math.floor(clamp(t/duration,0,.99999)*a.frames);return sc86Blit(color+'_'+phase,f,x,y);}
function sc86Say(b,who,text,dur=4.0){const F=b._s7warden.final;F.radio={who:missionRadioWho(who),full:text,t:0,typed:0,dur};}
function sc86Phase(b,phase){const E=b._s7mod.frExit,Q=E.sc86;Q.phase=phase;Q.t=0;sc86Log('phase',{phase,source:Q.source,portal:{x:E.portalX,y:E.portalY}});
 if(phase==='advance')sc86Say(b,'DECKER','THE OLD PORTAL CHAMBER IS AHEAD. KEEP FLYING NORTH.');
 if(phase==='ready')sc86Say(b,'DECKER','THERE IS THE STONE CIRCLE. APPROACH IT TO ACTIVATE THE GREEN GATE.',6);
 if(phase==='form'){Q.seats=seatList().map(seat=>withSeat(seat,()=>({seat,x:player.x,y:player.y})));combatAudio0927(b,'warpCharge',.3);sc86Say(b,'COLE','GATE IS COMING ONLINE. THIS IS OUR WAY THROUGH!',3.5);}
 if(phase==='enter'){combatAudio0927(b,'warpGate',.3);sc86Say(b,'DECKER','SIGNAL IS BREAKING UP. STAY WITH US!',2.4);}
 if(phase==='close')combatAudio0927(b,'warpBurst',.3);
}
fr28SewerMaster=function(){return XART.rdy('nst7_master_v3')?XART.get('nst7_master_v3'):SC86.base.master();};
fr27Exit=function(b,dt){if(run.stage!==7||!b?._s7mod||b._s7mod.tank)return SC86.base.exit.apply(this,arguments);
 const M=b._s7mod,F=b._s7warden.final;let E=M.frExit;
 if(!E?.sc86){const source=Math.max(0,Number.isFinite(_masterSrcY)?_masterSrcY:0);E=M.frExit={t:0,beat:0,fx:0,startX:player.x,startY:player.y,groundY:b.y,sourceY:source,travel:0,serial:0,portalX:SC86.aperture.x,portalY:SC86.aperture.y-source,sc86:{age:0,t:0,phase:'wreck',source,startSource:source,duration:clamp(source/145,8,24),flash:0}};SC86.owner=b;groundTargetingCancel(b);sc86Say(b,'DECKER','THE WARDEN IS FINISHED. FOLLOW THE CHANNEL TO THE OLD PORTAL CHAMBER.');sc86Log('route-start',{source,duration:E.sc86.duration,world:worldWidth()});}
 const Q=E.sc86;if(Q.phase==='done')return true;dt=clamp(dt||0,0,.05);Q.age+=dt;Q.t+=dt;E.t=Q.age;M.t=Q.age;M.clock+=dt;F.phase='escape';F.shipHidden=['close','white'].includes(Q.phase);F.bossHidden=Q.phase!=='wreck';b._s7FinalNoBar=true;b._s7warden.noHit=true;bossDefeated=true;
 for(const seat of seatList())withSeat(seat,()=>{player.invuln=Math.max(player.invuln||0,3);});
 for(const q of eBullets)q.dead=true;for(const q of powerups)if(q.kind!=='forgecombo')q.dead=true;
 if(F.radio){F.radio.t+=dt;F.radio.typed+=dt*36;if(F.radio.t>F.radio.dur)F.radio=null;}
 if(Q.phase==='wreck'){
  Q.fx=(Q.fx||0)-dt;if(Q.fx<=0){Q.fx=.22;fr27ToxicExplosion(b.x+Math.sin(Q.age*13)*60,b.y+Math.cos(Q.age*9)*50,80+Q.age*15,E.serial++);combatAudio0927(b,Q.age>2?'expBig':'expSmall',.25);}if(Q.t>=3.4)sc86Phase(b,'advance');
 }else if(Q.phase==='advance'){
  const p=clamp(Q.t/Q.duration,0,1),k=p*p*(3-2*p);Q.source=lerp(Q.startSource,0,k);E.travel=E.sourceY-Q.source;b.y=E.groundY+E.travel;mapScroll=levelScrollRange()-Q.source;
  if(p>=1)sc86Phase(b,'ready');
 }else if(Q.phase==='ready'){
  let near=false;for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out&&Math.hypot(player.x-E.portalX,player.y-E.portalY)<128)near=true;});if(near)sc86Phase(b,'form');
 }else if(Q.phase==='form'){if(Q.t>=1.6)sc86Phase(b,'enter');}
 else if(Q.phase==='enter'){
  const p=clamp(Q.t/2.8,0,1),k=p*p*(3-2*p);for(const s of Q.seats)withSeat(s.seat,()=>{player.x=lerp(s.x,E.portalX,k);player.y=lerp(s.y,E.portalY,k);});if(p>=1)sc86Phase(b,'close');
 }else if(Q.phase==='close'){if(Q.t>=1.1)sc86Phase(b,'white');}
 else if(Q.phase==='white'){
  Q.flash=Math.min(6,Math.floor(Q.t/.55*7));if(Q.t>=.62){sc86Log('native-finish',{rewarded:!!b._forgeRewardDropped});Q.phase='done';
   // Hand the completed visual sequence to the current native October1 exit,
   // so Forge reward, results, campaign ledger and direct Stage8 entry stay owned there.
   Object.assign(E,{s67:true,k1001:true,S:E.travel,x:b.x,v:0,t:Q.age,beat:4,zoom:1,done:false,portalOn:false,portalYNow:E.portalY,closeT:Q.age-7,
    entry:{gone:true,goneAt:Q.age-8,t0:0},flame:{t0:Q.age-8,k:1,fx:1e9}});
   return SC86.base.exit.call(this,b,0);}
 }
 E.portalX=SC86.aperture.x;E.portalY=SC86.aperture.y-Q.source;_masterSrcY=Q.source;return true;
};
s7WardenCinematic=function(){const Q=sc86State();return Q? !['advance','ready'].includes(Q.phase):SC86.base.cinematic.apply(this,arguments);};
fr27CinematicCamera=function(){if(sc86Own())return;return SC86.base.camera.apply(this,arguments);};
drawS7FinalPortalWorld=function(){const Q=sc86State();if(!Q)return SC86.base.portal.apply(this,arguments);const E=boss._s7mod.frExit;
 sc86Blit('seal',0,E.portalX,E.portalY);
 if(Q.phase==='form')sc86Gate('green','form',Q.t,E.portalX,E.portalY,1.6);
 else if(Q.phase==='enter')sc86Gate('green','loop',Q.t,E.portalX,E.portalY);
 else if(Q.phase==='close')sc86Gate('green','close',Q.t,E.portalX,E.portalY,1.1);
};
drawPlayer=function(){const Q=sc86State();if(!Q)return SC86.base.ship.apply(this,arguments);if(['close','white','done'].includes(Q.phase))return;
 if(Q.phase==='enter'){const frames=RD84_ART.banks['ship_north_'+run.pilot];rd84Blit(frames[Math.round((1-clamp(Q.t/2.8,0,1))*31)],player.x,player.y);return;}
 return SC86.base.ship.apply(this,arguments);};
s7WardenRadioDraw=function(){if(!sc86Own())return SC86.base.radio.apply(this,arguments);const R=boss._s7warden.final.radio;if(!R)return;const full=subst(R.full),who=R.who||'FURY WING';
 dlgBox({who,full,shown:full.slice(0,Math.floor(R.typed)),forceShown:true,portrait:String(who).toLowerCase(),emo:'idle',x:10,pw:VW-20,y:VH-92,ph:82,fixedHeight:true,maxBottom:VH-10});};
drawBG=function(dt){const Q=sc86State();if(!Q)return SC86.base.bg.apply(this,arguments);const old=Q.source;const r=SC86.base.bg.call(this,0);_masterSrcY=old;return r;};
const sc86World=drawWorld;drawWorld=function(){const r=sc86World.apply(this,arguments),Q=sc86State();if(Q?.flash){const a=RD84_ART.flash[Q.flash];if(XART.rdy(a.key)){ctx.save();ctx.translate(-camLeftX(),0);ctx.drawImage(XART.get(a.key),camLeftX(),viewTopY());ctx.restore();}}return r;};
rd84Gate=function(t,x,y,phase){return sc86Gate('blue',phase,t,x,y,phase==='form'?.8:phase==='close'?1.2:undefined);};
stageLoadBegin=function(n,keys){if(n===7)Snd.prepare(['warpCharge','warpGate','warpBurst','expSmall','expBig']);const extra=n===7?[...Object.values(SC86_ART).filter(a=>!a.key.includes('blue')).map(a=>a.key),'nst7_master_v3',...RD84_ART.flash.map(a=>a.key),...RD84_ART.pilots.flatMap(pk=>RD84_ART.banks['ship_north_'+pk].map(a=>a.key))]:n===8?Object.values(SC86_ART).filter(a=>a.key.includes('blue')).map(a=>a.key):[];return SC86.base.load.call(this,n,[...(keys||[]),...new Set(extra)]);};
beginStage=function(n){SC86.owner=null;if(n===7)SC86.events=[];return SC86.base.begin.apply(this,arguments);};
globalThis.BOF_SEWER_CHAMBER=SC86;
