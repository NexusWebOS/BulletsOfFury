function laserMistDraw(b){
  const lv=clamp(b.lv||1,1,5),f=(Math.floor((b.t||0)*16)+(b._mistIndex||0))%4;
  const h=24+lv*3,w=10+lv*1.2,a=Math.atan2(b.vy||-1,b.vx||0)+Math.PI/2;
  ctx.save();ctx.translate(b.x,b.y);ctx.rotate(a);ctx.globalCompositeOperation='lighter';ctx.imageSmoothingEnabled=false;
  // Two dim atlas echoes show motion; they cannot form a full-width cyan slab.
  for(let i=2;i>=1;i--){ctx.globalAlpha=.12/i;laserMistAtlasBlit(ctx,'lmfx_beam_'+lv+'_'+((f+4-i)%4),0,h*.42*i,w*.82,h*.80,true);}
  ctx.globalAlpha=1;ctx.shadowColor='#4be8ff';ctx.shadowBlur=3+lv*.5;
  laserMistAtlasBlit(ctx,'lmfx_beam_'+lv+'_'+f,0,0,w,h,true);
  ctx.restore();
}
function laserMistFlash(x,y,lv,split){
  pImpacts.push({x:x,y:y,t:0,dur:split?.20:.16,size:split?28+lv*2:22+lv*2,rot:0,_lmFx:split?'decal':'impact'});
  if(pImpacts.length>180)pImpacts.splice(0,pImpacts.length-180);
}
