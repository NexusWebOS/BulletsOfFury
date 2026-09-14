/* Solid kit choreography: real top plates only, no perspective crossfade,
   mirroring, opacity ramp or substitute side. Each piece has its own entrance. */
const FURY_PART_START=3.1,FURY_PART_GAP=.54,FURY_PART_RISE=1.1;
function furyPartsTick(G){
 if(!G||G.phase==='active')return;
 if(G.partStartAge==null&&G.age>=FURY_PART_START&&furyShipReady())G.partStartAge=G.age;
 if(G.partStartAge==null)return;
 const n=clamp(Math.floor((G.age-G.partStartAge)/FURY_PART_GAP)+1,0,FURY_KIT.length);
 while((G.partCueCount||0)<n){
  const i=G.partCueCount||0;G.partCueCount=i+1;
  if(Audio.SFX.furyPartArrival)Audio.SFX.furyPartArrival(i);
 }
}
function furyPartsReadyToFuse(G){
 return G&&G.partStartAge!=null&&G.age>=G.partStartAge+(FURY_KIT.length-1)*FURY_PART_GAP+FURY_PART_RISE+.5;
}
function furyPartPose(G,i,x,y,size){
 const q=FURY_KIT[i],phase=G.phase,age=G.age||0;
 const start=G.partStartAge==null?FURY_PART_START:G.partStartAge;
 const elapsed=age-start-i*FURY_PART_GAP;
 if(elapsed<0)return null;
 const scale=size/128,sign=i&1?-1:1,base=i*TAU/FURY_KIT.length-Math.PI/2;
 const snap=phase==='pixelglow'?1:phase==='snap'?clamp(G.t/GRAVITY_SNAP_DUR,0,1):0;
 const spin=phase==='charge'?gravitySpinAngle(G.t):(['scatter','snap','pixelglow'].includes(phase)?gravitySpinAngle(GRAVITY_CHARGE_DUR):0);
 // Shared orbital clock preserves even spacing; each sprite may still rotate
 // independently without the large hardware collapsing into overlapping piles.
 const angle=base+(age-start)*.65+spin,radius=(92+(i%2)*45)*scale;
 let px=x+Math.cos(angle)*radius,py=y+Math.sin(angle)*radius*.65;
 if(phase==='scatter'||phase==='snap'){
  const s=phase==='scatter'?clamp(G.t/GRAVITY_SCATTER_DUR,0,1):1;
  px+=Math.cos(angle)*28*scale*s;py+=Math.sin(angle)*25*scale*s+12*scale*s*s;
 }
 // The full cell starts below the playfield. All entrances run upward into
 // their moving orbit; no part is born at a final orbit position.
 const entry=_ease(clamp(elapsed/FURY_PART_RISE,0,1));
 px=lerp(x+((i%3)-1)*52,px,entry);py=lerp(VH+size*1.8,py,entry);
 const e=snap*snap;px=lerp(px,x+q.x*scale,e);py=lerp(py,y+q.y*scale,e);
 return {key:q.key+'_top',x:px,y:py,rotation:(base+sign*elapsed*.9)*(1-e),size:size*(q.partScale||1)*lerp(1.65,1,snap),entry};
}
function furyShipDrawPhase(G,x,y,size,planeH,pilot){
 const phase=G.phase,t=G.age||0;
 if(['drift','charge','scatter','snap','pixelglow'].includes(phase)){
  // Opaque plane and solid pieces persist until the full-screen white covers
  // the completed assembly. The finished fighter replaces them under white.
  drawShipSprite(x,y,gravityPlaneH(planeH,size,phase,G.t),'');
  // The plane is glimpsed through the deck. Incoming hardware is above that
  // deck, so each individual arrival remains visible instead of being buried.
  if(state===GS.LAUNCH&&run.stage===5&&drawLaunch._furyIntro)furyIntroClouds(drawLaunch._furyIntro);
  for(let i=0;i<FURY_KIT.length;i++){
   const p=furyPartPose(G,i,x,y,size);if(!p)continue;
   ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rotation);
   furyShipBlit(p.key,0,0,p.size,p.size,pilot,1);ctx.restore();
  }
  if(phase!=='drift')furyEffect('assembly',phase==='snap'||phase==='pixelglow'?G.t:t,x,y,size*1.12,size*.8,.48,phase==='charge'||phase==='scatter');
 }else{
  const forced=phase==='active'&&typeof warpForcedRollFrame==='function'?warpForcedRollFrame():null;
  const pose=phase==='active'?furyShipPose(player,forced):{key:'base'};
  if(phase==='active'&&(player.roll||player.somer||forced!=null))furyEffect('speed',furyFlightTime,x,y,size*3,size*5,.22,true);
  furyShipDrawFlight(x,y,size,pilot,pose,phase==='active'?furyFlightTime:t);
 }
}
