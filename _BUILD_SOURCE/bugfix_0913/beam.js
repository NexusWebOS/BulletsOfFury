/* Finite held-beam intersections: use exposed geometry, not a hull-center sample. */
function playerBeamRange(beam,hx){
  const x=Number.isFinite(beam.x)?beam.x:(Number.isFinite(hx)?hx:player.x);
  const top=Number.isFinite(beam.top)?beam.top:-20,bot=Number.isFinite(beam.bot)?beam.bot:player.y-14;
  return bot>top?{x:x,half:Math.max(0,(beam.w||0)/2),top:top,bot:bot}:null;
}
function beamCircleImpact(q,r,range){
  if(!range)return null;
  const x=clamp(q.x,range.x-range.half,range.x+range.half),dx=x-q.x;
  if(Math.abs(dx)>=r)return null;
  const chord=Math.sqrt(r*r-dx*dx),lo=Math.max(range.top,q.y-chord),hi=Math.min(range.bot,q.y+chord);
  return hi>lo?{x:x,y:(lo+hi)/2,entry:hi}:null;
}
function razorbackBeamHit(b,beam){
  const R=b&&b._rzb,range=playerBeamRange(beam);
  if(!R||b.dead||R.state==='arrival'||R.trans>0||!range)return null;
  let best=null;
  const parts=R.state==='guns'?['left','right']:[R.state];
  for(const key of parts){
    if(!(R.pools[key]>0))continue;
    const q=key==='left'||key==='right'?rzbWorld(b,key==='left'?-57:57,96):{x:b.x,y:b.y};
    const r=R.state==='guns'?RZB_R.gun:R.state==='turret'?RZB_R.turret:RZB_R.hull;
    const hit=beamCircleImpact(q,r,range);
    if(hit&&(!best||hit.entry>best.entry))best=Object.assign(hit,{key:key});
  }
  return best;
}
function subBossBeamImpact(b,beam){
  if(b._tempestDuo)return tempestBrothersBeamHit(b,beam);
  if(b._rzb)return razorbackBeamHit(b,beam);
  return null;
}
