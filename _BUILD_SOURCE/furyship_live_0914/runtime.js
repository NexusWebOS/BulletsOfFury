/* Furyship 0914: one authored hull family on every space route. The approved
   frame 13 is the level plate; generated reels own actual pitch/roll views.
   Existing atlas art stays intact for the SPCBOY legacy selection. */
let furyLegacyShip=false, furyFlightTime=0;
const FURY_KIT=[
 {key:'wing_left',x:-25,y:17},{key:'wing_right',x:25,y:17},
 {key:'engine_left',x:-10,y:23},{key:'engine_right',x:10,y:23},
 {key:'hull',x:0,y:13},{key:'nose',x:0,y:-27}
];
const FURY_VIEWS=['top','left','back','right','front'];
const FURY_KEYS=['base'];
for(const q of FURY_KIT)for(const v of FURY_VIEWS)FURY_KEYS.push(q.key+'_'+v);
for(const f of ['roll','somersault','assembly','veil','speed','thrusters'])
 for(let i=0;i<(f==='somersault'?12:8);i++)FURY_KEYS.push(f+'_'+String(i).padStart(2,'0'));
const _furyCache=Object.create(null);
function furyTintedKey(k){return k==='base'||/^(nose|hull|wing_|engine_|roll_|somersault_)/.test(k);}
function furyShipWarm(){
 if(typeof XART==='undefined')return;
 for(const k of FURY_KEYS){
  const stem=k==='base'?'runtime_base':k;
  XART._src['fury_'+k]='assets/game/furyship_0914/'+stem+'.png';XART._touch('fury_'+k);
  if(furyTintedKey(k)){XART._src['fury_'+k+'_blue']='assets/game/furyship_0914/'+stem+'_blue.png';XART._touch('fury_'+k+'_blue');}
 }
}
function furyShipReady(){
 if(furyLegacyShip||typeof XART==='undefined')return false;
 return FURY_KEYS.every(k=>XART.rdy('fury_'+k)&&(!furyTintedKey(k)||XART.rdy('fury_'+k+'_blue')));
}
function furyShipCanvas(k,pilot){
 const ck=k+'|'+(pilot||'axel');if(_furyCache[ck])return _furyCache[ck];
 if(!XART.rdy('fury_'+k))return null;
 const src=XART.get('fury_'+k),tint=furyTintedKey(k)&&pilot&&pilot!=='axel';
 if(!tint)return src;
 if(!XART.rdy('fury_'+k+'_blue'))return null;
 const mask=XART.get('fury_'+k+'_blue'),c=document.createElement('canvas');c.width=src.naturalWidth||src.width;c.height=src.naturalHeight||src.height;
 const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.drawImage(src,0,0);
 const m=document.createElement('canvas');m.width=c.width;m.height=c.height;const mg=m.getContext('2d');mg.imageSmoothingEnabled=false;mg.drawImage(mask,0,0);
 const lum=GRAVITY_PILOT_LUM[pilot]||1;
 if(lum>1){mg.globalCompositeOperation='lighter';mg.globalAlpha=Math.min(1,lum-1);mg.drawImage(mask,0,0);mg.globalAlpha=1;}
 mg.globalCompositeOperation='multiply';mg.fillStyle=GRAVITY_PILOT_PAL[pilot]||GRAVITY_PILOT_PAL.axel;mg.fillRect(0,0,m.width,m.height);
 mg.globalCompositeOperation='destination-in';mg.drawImage(mask,0,0);g.drawImage(m,0,0);
 _furyCache[ck]=c;return c;
}
function furyShipBlit(k,x,y,w,h,pilot,alpha){
 const im=furyShipCanvas(k,pilot);if(!im)return false;
 ctx.save();if(alpha!=null)ctx.globalAlpha*=alpha;ctx.drawImage(im,x-w/2,y-h/2,w,h);ctx.restore();return true;
}
/* Engine-wide authored speed/transition reels use simulation time supplied by
   the caller; no performance.now clock advances them while the game is paused. */
function furyEffect(f,t,x,y,w,h,alpha,loop){
 const n=loop?((Math.floor(Math.max(0,t)*12))%8):clamp(Math.floor(Math.max(0,t)*12),0,7);
 return furyShipBlit(f+'_'+String(n).padStart(2,'0'),x,y,w,h,null,alpha);
}
function furyShipPose(p,forced){
 if(forced!=null)return {key:'roll_'+String(clamp(Math.floor(forced/17*8),0,7)).padStart(2,'0'),roll:clamp(Math.floor(forced/17*8),0,7)};
 if(p&&p.roll){const u=clamp(p.roll.t/Math.max(.001,p.roll.dur),0,.9999),i=Math.floor(u*8),n=p.roll.dir>0?(8-i)%8:i;return {key:'roll_'+String(n).padStart(2,'0'),roll:n};}
 if(p&&p.somer){const n=clamp(Math.floor(p.somer.t/Math.max(.001,p.somer.dur)*12),0,11);return {key:'somersault_'+String(n).padStart(2,'0'),pitch:n};}
 const bank=p?clamp(p._bank||0,-1,1):0;
 return Math.abs(bank)>.35?{key:bank>0?'roll_01':'roll_07',roll:bank>0?1:7}:{key:'base'};
}
function furyShipPlume(pose,x,y,size,t){
 const pitch=pose.pitch,roll=pose.roll;
 // On front end-on views the exhaust mouths are behind the hull.
 if(pitch===8||pitch===9)return;
 let cy=51,sx=1,sy=1;
 if(pitch!=null){cy=[48,31,15,0,-22,-35,-43,-34,0,0,20,46][pitch];sy=[1,.85,.5,.22,-.5,-.85,-1,-.85,0,0,.5,.9][pitch];}
 if(roll!=null)sx=[1,.85,.24,.85,1,.85,.24,.85][roll];
 const im=furyShipCanvas('thrusters_'+String(4+(Math.floor(t*12)&1)).padStart(2,'0'),null);if(!im)return;
 ctx.save();ctx.translate(x,y);ctx.scale(size/128,size/128);ctx.globalCompositeOperation='lighter';
 ctx.translate(0,cy);ctx.scale(sx,sy);ctx.drawImage(im,-64,-32,128,128);ctx.restore();
}
function furyShipDrawFlight(x,y,size,pilot,pose,t){
 furyShipPlume(pose,x,y,size,t);
 furyShipBlit(pose.key,x,y,size,size,pilot);
}
function furyShipDrawPhase(G,x,y,size,planeH,pilot){
 const phase=G.phase,t=G.age||0,scale=size/128;
 if(['drift','charge','scatter','snap'].includes(phase)){
  const snap=phase==='snap'?clamp(G.t/GRAVITY_SNAP_DUR,0,1):0;
  ctx.save();ctx.globalAlpha*=1-snap;drawShipSprite(x,y,gravityPlaneH(planeH,size,phase,G.t),'');ctx.restore();
  for(let i=0;i<FURY_KIT.length;i++){
   const q=FURY_KIT[i],sign=i&1?-1:1,base=i*TAU/FURY_KIT.length-Math.PI/2,radius=(125+(i%3)*20)*scale;
   const angle=base+sign*gravitySpinAngle(phase==='charge'?G.t:GRAVITY_CHARGE_DUR);
   const ox=x+Math.cos(angle)*radius,oy=y+Math.sin(angle)*radius*.65;
   let px=x+Math.cos(base)*radius*1.25,py=y+Math.sin(base)*radius*.8,spin=t*(phase==='drift'?.6:2.5);
   if(phase==='charge'){const e=clamp(G.t/.58,0,1);px=lerp(px,ox,e);py=lerp(py,oy,e);spin=gravitySpinAngle(G.t);}
   if(phase==='scatter'||phase==='snap'){
    const s=phase==='scatter'?clamp(G.t/GRAVITY_SCATTER_DUR,0,1):1;
    px=ox+Math.cos(angle)*90*scale*s;py=oy+Math.sin(angle)*60*scale*s+35*scale*s*s;
   }
   if(phase==='snap'){const e=snap*snap;px=lerp(px,x+q.x*scale,e);py=lerp(py,y+q.y*scale,e);}
   const turn=(spin+i*.83)%FURY_VIEWS.length,a=Math.floor(turn),blend=turn-a,locked=snap>.55;
   ctx.save();ctx.translate(px,py);ctx.rotate(locked?0:Math.sin(spin+i)*.4);
   const opacity=snap>.78?1-(snap-.78)/.22:1;
   if(locked)furyShipBlit(q.key+'_top',0,0,size,size,pilot,opacity);
   else {furyShipBlit(q.key+'_'+FURY_VIEWS[a],0,0,size,size,pilot,(1-blend)*opacity);furyShipBlit(q.key+'_'+FURY_VIEWS[(a+1)%5],0,0,size,size,pilot,blend*opacity);}
   ctx.restore();
  }
  if(phase==='snap'&&snap>.78)furyShipBlit('base',x,y,size,size,pilot,(snap-.78)/.22);
  if(phase!=='drift')furyEffect('assembly',phase==='snap'?G.t:t,x,y,size*2.6,size*1.65,.65,phase!=='snap');
 }else{
  const forced=phase==='active'&&typeof warpForcedRollFrame==='function'?warpForcedRollFrame():null;
  const pose=phase==='active'?furyShipPose(player,forced):{key:'base'};
  if(phase==='active'&&(player.roll||player.somer||forced!=null))furyEffect('speed',furyFlightTime,x,y,size*3,size*5,.22,true);
  furyShipDrawFlight(x,y,size,pilot,pose,phase==='active'?furyFlightTime:t);
  if(phase==='pixelglow')furyEffect('assembly',G.t,x,y,size*2.1,size*1.4,.8,false);
 }
}
function furyShipVeil(G){
 const phase=G.phase;
 if(phase!=='whiteout'&&phase!=='reveal')return;
 const t=phase==='whiteout'?clamp(G.t/GRAVITY_WHITE_DUR,0,1)*4/12:(4+clamp(G.t/GRAVITY_REVEAL_DUR,0,1)*3)/12;
 const draw=()=>furyEffect('veil',t,VW/2,VH/2,VW,VH,.95,false);
 if(typeof screenBar==='function')screenBar(draw);else draw();
 // A short opaque seam covers the background handoff; the authored curtain
 // opens around it instead of holding the old full-screen white wash.
 gravityWhite(phase==='whiteout'?clamp((G.t/GRAVITY_WHITE_DUR-.7)/.3,0,1):clamp(1-G.t/.18,0,1));
}
