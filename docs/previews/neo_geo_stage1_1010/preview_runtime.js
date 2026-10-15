"use strict";
/* Loaded only by the candidate page, inside its own game iframe. */
window.PV10={unit:'razorback',t:0,speed:1,paused:false,original:false,anchors:false,gone:new Set(),debris:[],bursts:[],
 draw:drawWorld,tick:updatePlay,baseBoss:drawBoss,baseMini:razorbackDraw};
for(const bank of Object.values(PV10_ART))for(const a of bank)XART._src[a.key]=a.path;
PV10.ready=()=>Object.values(PV10_ART).flat().every(a=>XART.rdy(a.key))&&af10Ready();
PV10.choose=function(unit){this.unit=unit;this.t=0;this.restore();run.pilot='yuri';pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');PILOTMOD={...PILOTS[pilotIndex]};
 diffKey=unit==='furious_razorback'?'furious':'normal';DIFF=difficultyForRun('arcade',diffKey);run.mode='arcade';beginStage(1);setState(GS.PLAY);player.reset();stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];story=null;BOFCinematicDirector.cancel();
 boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=false;
 if(unit==='overlord')spawnBoss(STAGES[0].boss);else spawnSubBoss__inner('razorback');
 mapScroll=unit==='overlord'?curStage.length*40:1600;
 const b=boss||subBoss;b.enter=false;b.x=worldWidth()/2;b.y=PLAY.y+PLAY.h*.33;b._drawY=b.y;b._noHit=false;b._be=null;b._ovAirborne=false;if(b._ovIntro)b._ovIntro.done=true;
 camX=clamp(worldWidth()/2-VW/2,0,worldWidth()-VW);player.x=worldWidth()/2;player.y=VH-100;player.invuln=1e9;
 stageLoadBegin(1,[...Object.values(PV10_ART).flat(),...Object.values(AF10_ART).flat()].map(a=>a.key));af10Warm();};
PV10.restore=function(){this.gone.clear();this.debris=[];this.bursts=[];};
PV10.rig=function(){const heli=this.unit==='overlord',furious=this.unit==='furious_razorback',kit=(heli?'overlord':furious?'furious_razorback':'razorback')+'_kit_';
 return heli?[
 {id:'left',label:'left cannon',bank:kit+'1',x:-54,y:10,k:.23},
 {id:'right',label:'right cannon',bank:kit+'1',x:54,y:10,k:.23},
 {id:'podL',label:'left missile pod',bank:kit+'2',x:-44,y:-27,k:.19},
 {id:'podR',label:'right missile pod',bank:kit+'2',x:44,y:-27,k:.19},
 {id:'rotor',label:'main rotor',bank:kit+'0',x:0,y:-6,k:.86,rotor:true}]:[
 {id:'turbine',label:'turbine',bank:kit+'3',x:0,y:-54,k:.20},
 {id:'left',label:'left gun',bank:kit+'1',x:-43,y:furious?-75:-18,k:.24},
 {id:'right',label:'right gun',bank:kit+'1',x:43,y:furious?-75:-18,k:.24},
 {id:'podL',label:'left missile pod',bank:kit+'2',x:-45,y:24,k:.20},
 {id:'podR',label:'right missile pod',bank:kit+'2',x:45,y:24,k:.20},
 {id:'cannon',label:'main turret',bank:kit+'0',x:0,y:0,k:.43}];};
PV10.break=function(id){const m=this.rig().find(q=>q.id===id);if(!m||this.gone.has(id))return;this.gone.add(id);const b=boss||subBoss;
 const x=b.x+m.x,y=b.y+m.y;this.debris.push({...m,x,y,vx:m.x<0?-65:65,vy:-55,spin:0,t:0});this.bursts.push({x,y,t:0,bank:'electric_ring',life:1.35,size:70});};
PV10.cell=function(bank,f,x,y,k,angle=0){const a=PV10_ART[bank]?.[f%PV10_ART[bank].length];if(!a||!XART.rdy(a.key))return;
 ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();};
drawBoss=function(){if(PV10.original)return PV10.baseBoss.apply(this,arguments);};
razorbackDraw=function(){if(PV10.original)return PV10.baseMini.apply(this,arguments);};
updatePlay=function(dt){stageLoadTick();if(PV10.paused)return;dt*=PV10.speed;PV10.t+=dt;
 for(const d of PV10.debris){d.t+=dt;d.x+=d.vx*dt;d.y+=d.vy*dt;d.vy+=110*dt;d.spin+=dt*5;if(d.t>=.8){PV10.bursts.push({x:d.x,y:d.y,t:0,bank:'plasma_blast',size:85,life:1.4});d.dead=true;}}
 PV10.debris=PV10.debris.filter(d=>!d.dead);for(const q of PV10.bursts)q.t+=dt;PV10.bursts=PV10.bursts.filter(q=>q.t<q.life);};
drawWorld=function(dt){PV10.draw.apply(this,arguments);if(PV10.original||!PV10.ready())return;const b=boss||subBoss;if(!b)return;
 ctx.save();const vz=viewZoom();if(vz!==1){ctx.scale(vz,vz);ctx.translate(0,VH*(1-vz)/vz);}if(worldWidth()>viewW())ctx.translate(-camX,0);
 const heli=PV10.unit==='overlord',f=Math.floor(PV10.t*16)%16,overall=PV10.unit==='furious_razorback'?1.10:1;
 PV10.cell(PV10.unit+'_hull',f,b.x,b.y,heli?.72:(PV10.unit==='furious_razorback'?.88:.70));
 const cycle=PV10.t%2,fire=cycle<.4?Math.min(3,Math.floor(cycle*10)):0;
 for(const m of PV10.rig()){if(PV10.gone.has(m.id))continue;const x=b.x+m.x*overall,y=b.y+m.y*overall;
 PV10.cell(m.bank,m.rotor?0:m.id==='turbine'?Math.floor(PV10.t*16)%4:fire,x,y,m.k*overall,m.rotor?PV10.t*Math.PI*6:0);
 if(PV10.anchors){ctx.strokeStyle='#9fffd9';ctx.lineWidth=1;ctx.strokeRect(x-3,y-3,6,6);}}
 for(const d of PV10.debris)PV10.cell(d.bank,0,d.x,d.y,d.k,d.spin);
 for(const q of PV10.bursts)af10Cell(q.bank,q.t,q.life,q.x,q.y,q.size);ctx.restore();};
PV10.choose('razorback');
