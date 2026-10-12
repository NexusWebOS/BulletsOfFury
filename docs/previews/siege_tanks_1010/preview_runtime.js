"use strict";
/* Preview-only override in an isolated instance of the real game. */
window.PT10={unit:'sonic',t:0,speed:1,paused:false,auto:true,anchors:false,mode:'combat',part:'hull',
 originalDraw:drawWorld,parts:{},debris:[],bursts:[],decals:[],shots:[],attack:null,nextAuto:2,
 specs:{sonic:{name:'Sonic siege tank',width:240,tint:'#65e6ff'},devastator:{name:'Devastator assault tank',width:154.5,tint:'#ff6452'},deviator:{name:'Deviator missile tank',width:200,tint:'#90ed75'}}};
for(const bank of Object.values(ST10_ART))for(const a of bank)XART._src[a.key]=a.path;
PT10.banks=function(){return Object.entries(ST10_ART).filter(([k])=>k.startsWith(this.unit+'_')||k==='decals');};
PT10.ready=function(){return this.banks().every(([,v])=>v.every(a=>XART.rdy(a.key)))&&XART.rdy('nbret_yuri');};
PT10.rig=function(){return [
 {id:'trackL',part:'track_left',label:'Left track',x:-134,y:12},
 {id:'trackR',part:'track_right',label:'Right track',x:134,y:12},
 {id:'hull',part:'hull',label:'Armored hull',x:0,y:0},
 {id:'reactor',part:'reactor',label:'Reactor',x:0,y:-137},
 {id:'podL',part:'pod',label:'Left auxiliary pod',x:-98,y:50},
 {id:'podR',part:'pod',label:'Right auxiliary pod',x:98,y:50},
 {id:'sensor',part:'sensor',label:'Targeting array',x:0,y:-196},
 {id:'weapon',part:'weapon',label:'Main weapon',x:0,y:0}];};
PT10.restore=function(){this.parts=Object.fromEntries(this.rig().map(m=>[m.id,{damage:-1,flash:0,gone:false}]));
 this.debris=[];this.bursts=[];this.decals=[];this.shots=[];this.attack=null;this.nextAuto=this.t+2;};
PT10.scale=function(){const rig=this.rig();let left=Infinity,right=-Infinity;
 for(const m of rig){const a=ST10_ART[this.unit+'_'+m.part][0];left=Math.min(left,m.x+a.bounds[0]-a.pivot[0]);right=Math.max(right,m.x+a.bounds[2]-a.pivot[0]);}
 return this.specs[this.unit].width/(right-left);};
PT10.choose=function(unit){this.unit=unit;this.t=0;this.restore();run.pilot='yuri';pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');PILOTMOD={...PILOTS[pilotIndex]};
 diffKey='normal';DIFF=difficultyForRun('arcade',diffKey);run.mode='arcade';beginStage(1);setState(GS.PLAY);player.reset();
 stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];story=null;BOFCinematicDirector.cancel();
 boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;mapScroll=1600;
 player.x=worldWidth()/2;player.y=VH-82;player.invuln=1e9;camX=clamp(player.x-VW/2,0,worldWidth()-VW);
 this.x=worldWidth()/2;this.y=PLAY.y+PLAY.h*.31;this.target={x:this.x,y:PLAY.y+PLAY.h*.63};
 stageLoadBegin(1,this.banks().flatMap(([,v])=>v.map(a=>a.key)).concat(['nbret_yuri']));
 this.ready();};
PT10.cell=function(bank,f,x,y,k=1,angle=0,white=false){const list=ST10_ART[bank],a=list?.[((f%list.length)+list.length)%list.length];
 if(!a||!XART.rdy(a.key))return;const im=white?xartTint(a.key,'#ffffff',1):XART.get(a.key);
 ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();};
PT10.drawTank=function(x=this.x,y=this.y,width=this.specs[this.unit].width,frame=null){const k=this.scale()*width/this.specs[this.unit].width;
 const f=frame===null?Math.floor(this.t*16)%16:frame;
 for(const m of this.rig()){const p=this.parts[m.id];if(p.gone)continue;let bank=this.unit+'_'+m.part,index=m.part==='pod'||m.part==='sensor'||m.part==='reactor'?0:f;
  if(m.part==='weapon')index=this.attack?Math.min(15,Math.floor(this.attack.t/this.attack.life*16)):0;
  if(p.damage>=0){bank+='_damage';index=p.damage;}
  this.cell(bank,index,x+m.x*k,y+m.y*k,k,0,p.flash>0);
  if(this.anchors){ctx.strokeStyle=this.specs[this.unit].tint;ctx.lineWidth=1;ctx.strokeRect(x+m.x*k-3,y+m.y*k-3,6,6);}
 }};
PT10.point=function(id){const m=this.rig().find(q=>q.id===id),k=this.scale();return {x:this.x+m.x*k,y:this.y+m.y*k};};
PT10.muzzle=function(slot=0){const a=ST10_ART[this.unit+'_weapon'][0],k=this.scale();
 return {x:this.x+(slot===0?-1:1)*(this.unit==='sonic'?40:this.unit==='devastator'?39:35)*k,
  y:this.y+(a.bounds[3]-a.pivot[1]-4)*k};};
PT10.hit=function(id){const p=this.parts[id];if(!p||p.gone)return;p.flash=.16;p.damage=Math.min(1,p.damage+1);
 const q=this.point(id);this.bursts.push({unit:this.unit,bank:'impact',t:0,life:.58,x:q.x,y:q.y,k:.16});};
PT10.flash=function(){for(const p of Object.values(this.parts))if(!p.gone)p.flash=.18;};
PT10.break=function(id,delay=0){const m=this.rig().find(q=>q.id===id),p=this.parts[id];if(!m||p.gone)return;p.gone=true;
 const q=this.point(id);this.debris.push({unit:this.unit,part:m.part,x:q.x,y:q.y,vx:m.x===0?28:m.x<0?-90:90,vy:-56,spin:0,t:-delay,k:this.scale(),life:.8,heldDamage:p.damage});
 this.bursts.push({unit:this.unit,bank:'impact',t:-delay,life:.65,x:q.x,y:q.y,k:.22});
 if(id==='weapon')this.attack=null;};
PT10.destroy=function(){for(const [i,m] of this.rig().entries())this.break(m.id,i*.085);
 this.bursts.push({unit:this.unit,bank:'explosion',t:-.65,life:1.65,x:this.x,y:this.y,k:this.scale()*.75});
 this.decal(this.x,this.y,1.05);this.nextAuto=Infinity;};
PT10.decal=function(x,y,k=.55){const row=this.unit==='sonic'?0:this.unit==='devastator'?4:8;
 this.decals.push({f:row+Math.floor(this.t*7)%4,x,y,k});if(this.decals.length>24)this.decals.shift();};
PT10.fire=function(charged=false){if(this.parts.weapon.gone||this.attack||!this.ready())return false;
 const life=charged&&this.unit==='sonic'?2.6:1.6;this.attack={t:0,life,charged:charged&&this.unit==='sonic',emitted:0};return true;};
PT10.release=function(slot,charged){const from=this.muzzle(slot),to={x:this.target.x+(charged?0:(slot===0?-50:50)),y:this.target.y};
 to.y=Math.max(to.y,from.y+48);const dir=Math.atan2(to.y-from.y,to.x-from.x),speed=this.unit==='sonic'?300:this.unit==='devastator'?330:230;
 this.shots.push({unit:this.unit,x:from.x,y:from.y,startX:from.x,startY:from.y,from,to,dir,speed,t:0,charged,
  k:this.unit==='sonic'?(charged?.66:.32):this.unit==='devastator'?.27:.28});
 this.bursts.push({unit:this.unit,bank:'impact',x:from.x,y:from.y,t:0,life:.30,k:this.unit==='sonic'?.13:.10});};
PT10.detonate=function(s){const bank=s.unit+'_explosion',ink=ST10_METRICS[bank].peakInk;
 const k=s.charged?Math.sqrt(viewW()*PLAY.h*.33/ink):s.unit==='sonic'?.26:s.unit==='devastator'?.24:.25;
 let x=s.to.x,y=s.to.y;
 if(s.charged){const a=ST10_ART[bank][0];
  // The pressure bloom rises from the contact flash; its complete authored
  // footprint stays within the active playfield at maximum expansion.
  x=clamp(x,camX+a.pivot[0]*k+4,camX+viewW()-(a.w-a.pivot[0])*k-4);
  y=clamp(y,PLAY.y+a.pivot[1]*k+4,PLAY.y+PLAY.h-(a.h-a.pivot[1])*k-4);
  this.bursts.push({unit:s.unit,bank:'impact',t:0,life:.5,x:s.to.x,y:s.to.y,k:.25});}
 this.bursts.push({unit:s.unit,bank:'explosion',t:0,life:s.charged?1.6:1.25,x,y,k,charged:s.charged});
 this.decal(s.to.x,s.to.y,s.charged?.90:.36);if(s.charged)this.coverage={requested:.33,k,ink};};
PT10.tick=function(dt){stageLoadTick();if(this.paused||!this.ready())return;dt*=this.speed;this.t+=dt;
 for(const p of Object.values(this.parts))p.flash=Math.max(0,p.flash-dt);
 if(this.auto&&this.mode==='combat'&&!this.attack&&this.t>=this.nextAuto){this.fire(this.unit==='sonic');this.nextAuto=this.t+6;}
 const a=this.attack;if(a){a.t+=dt;const start=a.charged?1.65:.43,count=this.unit==='deviator'?6:2,spacing=this.unit==='deviator'?.12:.18;
  while(a.emitted<count&&a.t>=start+a.emitted*spacing){if(!a.charged||a.emitted===0)this.release(a.emitted%2,a.charged);a.emitted++;}
  if(a.t>=a.life)this.attack=null;}
 for(const s of this.shots){s.t+=dt;const dx=s.to.x-s.x,dy=s.to.y-s.y,dist=Math.hypot(dx,dy);
  s.dir=Math.atan2(dy,dx);if(dist<=s.speed*dt){s.x=s.to.x;s.y=s.to.y;this.detonate(s);s.dead=true;}else{s.x+=Math.cos(s.dir)*s.speed*dt;s.y+=Math.sin(s.dir)*s.speed*dt;}}
 this.shots=this.shots.filter(s=>!s.dead);
 for(const d of this.debris){d.t+=dt;if(d.t<0)continue;d.x+=d.vx*dt;d.y+=d.vy*dt;d.vy+=160*dt;d.spin+=dt*(d.vx<0?-5:5);
  if(d.t>=d.life){this.bursts.push({unit:d.unit,bank:'explosion',x:d.x,y:d.y,t:0,life:1.15,k:.18});this.decal(d.x,d.y,.25);d.dead=true;}}
 this.debris=this.debris.filter(d=>!d.dead);for(const q of this.bursts)q.t+=dt;this.bursts=this.bursts.filter(q=>q.t<q.life);};
PT10.effect=function(q){if(q.t<0)return;const count=ST10_ART[q.unit+'_'+q.bank].length,f=Math.min(count-1,Math.floor(q.t/q.life*count));
 this.cell(q.unit+'_'+q.bank,f,q.x,q.y,q.k);};
PT10.world=function(){if(!this.ready())return;ctx.save();const vz=viewZoom();if(vz!==1){ctx.scale(vz,vz);ctx.translate(0,VH*(1-vz)/vz);}if(worldWidth()>viewW())ctx.translate(-camX,0);
 if(this.mode==='damage'){const parts=ST10_ART[this.unit+'_'+this.part+'_damage'];
  for(let i=0;i<4;i++){const x=this.x-165+i*110;
   this.cell(this.unit+'_'+this.part+'_damage',i,x,PLAY.y+PLAY.h*.32,.30);
   this.cell(this.unit+'_debris',i,x,PLAY.y+PLAY.h*.63,.75,Math.sin(this.t*.8)*.15);
   this.cell('decals',(this.unit==='sonic'?0:this.unit==='devastator'?4:8)+i,x,PLAY.y+PLAY.h*.88,.27);}
 }else if(this.mode==='effects'){const cx=this.x,cy=PLAY.y+PLAY.h*.5;
  this.cell(this.unit+'_charge',Math.floor(this.t*16)%16,cx-100,cy-108,.58);
  this.cell(this.unit+'_projectile',Math.floor(this.t*16)%16,cx+95,cy-108,.55);
  this.cell(this.unit+'_impact',Math.floor(this.t*20)%16,cx-100,cy+85,.47);
  this.cell(this.unit+'_explosion',Math.floor(this.t*24)%32,cx+95,cy+85,.43);
 }else if(this.mode==='scale'){
  this.drawTank(this.x+67,PLAY.y+PLAY.h*.43);const e=this.referenceTank;if(e){e.x=this.x-143;e.y=PLAY.y+PLAY.h*.34;e.flash=0;drawEnemy(e);}
  const b=this.referenceMini;if(b){b.x=this.x-120;b.y=PLAY.y+PLAY.h*.76;b._drawY=b.y;razorbackDraw(b);}
 }else{
  for(const d of this.decals)this.cell('decals',d.f,d.x,d.y,d.k);
  this.drawTank();const a=this.attack;if(a){const p=this.muzzle(0),q=this.muzzle(1),cx=(p.x+q.x)/2,cy=(p.y+q.y)/2;
   if(a.t<(a.charged?1.65:.43)){this.cell(this.unit+'_charge',Math.min(15,Math.floor(a.t/(a.charged?1.65:.43)*16)),cx,cy,this.unit==='sonic'?.46:.28);
    drawBossRetina(this.t,this.target.x,this.target.y,this.t*2,.95);}}
  for(const s of this.shots)this.cell(s.unit+'_projectile',Math.floor(s.t*24)%16,s.x,s.y,s.k,s.dir-Math.PI/2);
  for(const d of this.debris){if(d.t>=0)this.cell(d.unit+'_'+d.part+'_damage',2,d.x,d.y,d.k,d.spin);
   else this.cell(d.unit+'_'+d.part+(d.heldDamage>=0?'_damage':''),d.heldDamage>=0?d.heldDamage:0,d.x,d.y,d.k);}
  for(const q of this.bursts)this.effect(q);
 }
 ctx.restore();};
PT10.reference=function(){enemies=[];spawnEnemy('s1tankheavy',this.x-143,170);this.referenceTank=enemies.at(-1);this.referenceTank._modAngle=Math.PI/2;enemies=[];
 const oldDiff=diffKey,oldDIFF=DIFF;diffKey='furious';DIFF=difficultyForRun('arcade','furious');spawnSubBoss__inner('razorback');this.referenceMini=subBoss;
 subBoss=null;subBossActive=false;diffKey=oldDiff;DIFF=oldDIFF;story=null;BOFCinematicDirector.cancel();};
updatePlay=function(dt){PT10.tick(dt);};
drawWorld=function(dt){PT10.originalDraw.apply(this,arguments);PT10.world();};
PT10.choose('sonic');PT10.reference();
