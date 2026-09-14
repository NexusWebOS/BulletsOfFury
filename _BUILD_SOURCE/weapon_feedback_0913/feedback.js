/* 0913: weapon feedback uses existing authored plates and the simulation clock. */
function weaponFeedbackArt(key,x,y,w,h,alpha,ang,add){
  if(typeof XART==='undefined'||!XART.rdy(key))return false;
  const im=XART.get(key),iw=im.naturalWidth||im.width,ih=im.naturalHeight||im.height;
  if(!iw||!ih)return false;
  ctx.save();ctx.translate(x,y);if(ang)ctx.rotate(ang);
  ctx.globalAlpha=clamp(alpha==null?1:alpha,0,1);ctx.imageSmoothingEnabled=false;
  if(add)ctx.globalCompositeOperation='lighter';
  const dh=h||w*ih/iw;
  ctx.drawImage(im,-w/2,-dh/2,w,dh);ctx.restore();return true;
}
function weaponFeedbackSound(name,vol){
  if(typeof Snd!=='undefined'&&Snd&&Snd.play)return Snd.play(name,vol==null?1:vol);
  return false;
}
function weaponFeedbackLoop(name,vol){
  if(typeof Snd!=='undefined'&&Snd&&Snd.loopOn)Snd.loopOn(name,vol);
}
function weaponFeedbackOff(name){
  if(typeof Snd!=='undefined'&&Snd&&Snd.loopOff)Snd.loopOff(name);
}
function weaponFeedbackWarm(pilot){
  const keys=pilot==='cole'?['nsw_ring_0','nsw_ring_1','nsw_ring_2','nsw_ring_3','nsw_circ_0','nsw_circ_1','nsw_circ_2','nsw_circ_3','nsw_dist_0','nsw_dist_1','nsw_dist_2','nsw_dist_3']:
    ['jchg_0','jchg_1','jchg_2','jchg_3','jwb_ball','jwb_ball_hot','jwb_link','jwb_burst','ndr_dambreaker_bottomthruster_0','ndr_dambreaker_bottomthruster_1','ndr_dambreaker_bottomthruster_2','ndr_dambreaker_bottomthruster_3'];
  if(typeof XART!=='undefined')for(const key of keys)XART.rdy(key);
  if(typeof XART!=='undefined')XART.rdy('ship_'+pilot);
  if(typeof Snd!=='undefined'&&Snd&&Snd.prepare)Snd.prepare(pilot==='cole'?['colePressureStart','colePressureLoop','colePressureRelease','colePressureImpact']:
    ['juggernautChargeStart','juggernautChargeLoop','juggernautRamLaunch','juggernautRamLoop','juggernautRamStop','juggernautChains','juggernautWreckHit','juggernautWreckBlock']);
  if(typeof Snd!=='undefined'&&Snd&&Snd.loopPrepare)for(const name of pilot==='cole'?['colePressureLoop']:['juggernautChains','juggernautChargeLoop','juggernautRamLoop'])Snd.loopPrepare(name);
}
function weaponFeedbackBurst(kind,x,y,size,dur,rot){
  if(typeof pImpacts==='undefined')return;
  pImpacts.push({x:x,y:y,t:0,dur:dur||.28,size:size,rot:rot||0,_weaponFx:kind});
  if(pImpacts.length>180)pImpacts.splice(0,pImpacts.length-180);
}
function weaponFeedbackDraw(p){
  if(!p._weaponFx)return false;
  const u=clamp(p.t/p.dur,0,1),f=Math.min(3,Math.floor(u*4));
  const key=p._weaponFx==='wreck'?'jwb_burst':'jchg_'+f;
  weaponFeedbackArt(key,p.x,p.y,p.size*(.65+u*.55),null,(1-u)*(p._weaponFx==='wreck'?1:.72),p.rot,true);
  return true;
}
function wreckStrike(b,x,y,heavy){
  b.hot=1;b._kick=.07;
  weaponFeedbackBurst('wreck',x,y,heavy?58:28,heavy?.27:.16,b.a);
  weaponFeedbackSound(heavy?'juggernautWreckHit':'juggernautWreckBlock',heavy?1:.55);
}
function sonicFrontGeometry(b){
  const p=clamp(b._p||0,0,1);
  return {w:(b.w||34)*(1.15+.30*p),h:18+16*p,alpha:.66+.30*p,frame:Math.floor((b.t||0)*18)%4};
}
function sonicDrawFront(b){
  const g=sonicFrontGeometry(b),p=clamp(b._p||0,0,1);
  weaponFeedbackArt('nsw_dist_'+g.frame,b.x,b.y,g.w,g.h,g.alpha,0,true);
  // A dim circular pressure edge gives the crescent thickness without hiding targets.
  weaponFeedbackArt('nsw_ring_3',b.x,b.y+4,g.w*.90,g.h*1.35,.20+.15*p,0,true);
}
function sonicImpact(x,y,p){
  sonicTrail.push({x:x,y:y,t:0,dur:.30,circ:true,p:p,hit:true});
  weaponFeedbackSound('colePressureImpact',.55+.35*(p||0));
}
