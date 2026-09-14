/* Mike's revised Tempest flight: nose toward the pilot, sharp banks and slides,
   red aim -> green commit -> afterburner pass. Positions remain campaign-owned. */
const TLV_JET_RED='#ff3c44',TLV_JET_GREEN='#69ff8a';
function tempestJetAngle(from,to,rate,dt){
  const delta=Math.atan2(Math.sin(to-from),Math.cos(to-from));
  return from+clamp(delta,-rate*dt,rate*dt);
}
function tempestJetLocal(p,x,y){
  const a=p._jet.angle,c=Math.cos(a),sn=Math.sin(a),dx=x-p.x,dy=y-p.y;
  return {x:dx*c+dy*sn,y:-dx*sn+dy*c};
}
function tempestJetPartAt(p,x,y){
  if(p.dead||!p._tlv.vuln) return null;
  const q=tempestJetLocal(p,x,y);
  for(let i=0;i<4;i++) if(p._tlv.ap[i].hp>0){
    const port=TLV_PORTS[i];
    if(Math.abs(q.x-port[0]*TLV_S)<TLV_AP_BOX[0]*TLV_S&&Math.abs(q.y-port[1]*TLV_S)<TLV_AP_BOX[1]*TLV_S) return 'ap'+i;
  }
  return Math.abs(q.x)<TLV_HULL_BOX[0]*TLV_S&&Math.abs(q.y)<TLV_HULL_BOX[1]*TLV_S?'hull':null;
}
function tempestJetRectBeam(p,lx,ly,hw,hh,range){
  if(!range)return null;
  const c=Math.cos(p._jet.angle),sn=Math.sin(p._jet.angle);
  let poly=[[-hw,-hh],[hw,-hh],[hw,hh],[-hw,hh]].map(q=>{
    const x=q[0]+lx,y=q[1]+ly;return {x:p.x+x*c-y*sn,y:p.y+x*sn+y*c};
  });
  /* Clip the rotated physical part to the beam's actual width and endpoints. */
  for(const [axis,edge,sign]of [['x',range.x-range.half,1],['x',range.x+range.half,-1],['y',range.top,1],['y',range.bot,-1]]){
    const clipped=[];
    for(let i=0;i<poly.length;i++){
      const a=poly[i],b=poly[(i+1)%poly.length],insideA=(a[axis]-edge)*sign>=0,insideB=(b[axis]-edge)*sign>=0;
      if(insideA)clipped.push(a);
      if(insideA!==insideB){const t=(edge-a[axis])/(b[axis]-a[axis]);clipped.push({x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t});}
    }
    poly=clipped;if(!poly.length)return null;
  }
  const ys=poly.map(q=>q.y),entry=Math.max(...ys);
  if(entry-Math.min(...ys)<1e-7)return null;
  return {x:poly.reduce((v,q)=>v+q.x,0)/poly.length,y:poly.reduce((v,q)=>v+q.y,0)/poly.length,entry:entry};
}
function tempestJetCancel(b,p){
  if(!p._jet) return;
  const owned=b._tempestDuo.striker===p;
  p._jet.active=false;p._jet.cue=null;p._jet.cooldown=p._tempestGray?4.8:3.8;
  if(!p._tempestGray)b._tempestDuo.waitingForBlack=false;
  if(b._tempestDuo.striker===p)b._tempestDuo.striker=null;
  if(owned&&typeof Snd!=='undefined'&&Snd.loopOff)Snd.loopOff('tlvJetEngine');
}
function tempestJetStart(b,p){
  const D=b._tempestDuo,J=p._jet,s=p._ai;
  if(D.striker||!s.vulnerable||s.gone||p.dead) return false;
  D.striker=p;J.active=true;J.state='slide';J.t=0;J.leg=0;J.side=p._tempestGray?-1:1;
  if(!p._tempestGray)D.waitingForBlack=false;
  J.vx=0;J.vy=0;J.cue=null;J.shot=0;J.passes++;
  s.beams=[];p._pending=[];
  J.row=clamp((player.y-145-TLV_YOFF)/TLV_KY,160,320);
  J.targetX=J.side>0?700:200;
  tlvSfx('tlvJetTurn');
  return true;
}
function tempestJetBounds(p){
  const J=p._jet,c=Math.abs(Math.cos(J.angle)),sn=Math.abs(Math.sin(J.angle));
  const x=tlvX(p._ai.boss.x),y=tlvY(p._ai.boss.y);
  const hx=(c*p._drawW+sn*p._drawH)/2,hy=(sn*p._drawW+c*p._drawH)/2;
  return {left:x-hx,right:x+hx,top:y-hy,bottom:y+hy};
}
function tempestJetOutside(p,margin=0){
  const q=tempestJetBounds(p);
  return q.right<camLeftX()-margin||q.left>camRightX()+margin||
    q.bottom<viewTopY()-margin||q.top>VH+margin;
}
function tempestJetTick(b,p,dt){
  const D=b._tempestDuo,J=p._jet,s=p._ai;
  s.events=[];s.time+=dt;s.t+=dt;s.st+=dt;s.motionAxis='jet';s.ramWarning=false;s.beams=[];
  s.hitFlash=Math.max(0,s.hitFlash-dt);s.shake=Math.max(0,s.shake-dt*25);
  s.fx=s.fx.filter(f=>(f.age+=dt)<f.life);
  for(const r of s.rig){r.hit=Math.max(0,r.hit-dt);r.flash=Math.max(0,r.flash-dt);r.charge=0;}
  s.vulnerable=true;J.t+=dt;
  const move=(tx,ty,speed)=>{
    const dx=(tx-s.boss.x)*TLV_KX,dy=(ty-s.boss.y)*TLV_KY,d=Math.hypot(dx,dy)||1;
    const step=Math.min(d,speed*dt);
    s.boss.x+=dx/d*step/TLV_KX;s.boss.y+=dy/d*step/TLV_KY;return d<5;
  };
  if(J.state==='slide'){
    const reached=move(J.targetX,J.row,460);
    J.angle=tempestJetAngle(J.angle,Math.PI+J.side*0.65,13,dt);
    s.mode='BANK AND SLIDE';
    if(reached||J.t>(J.leg?0.34:0.38)){
      if(J.leg===0){J.leg=1;J.side*=-1;J.targetX=J.side>0?720:180;J.t=0;tlvSfx('tlvJetTurn');}
      else{J.state='charge';J.t=0;J.cue='red';J.lock={x:D.ai.player.x,y:D.ai.player.y};tlvSfx('tlvJetCharge');}
    }
  } else if(J.state==='charge'){
    /* Red can still aim. Green locks the pass and remains visible for 220ms. */
    if(J.t<0.78)J.lock={x:D.ai.player.x,y:D.ai.player.y};
    else if(J.cue!=='green'){J.cue='green';J.greens++;tlvSfx('tlvJetReady');}
    const dx=(J.lock.x-s.boss.x)*TLV_KX,dy=(J.lock.y-s.boss.y)*TLV_KY;
    const dist=Math.hypot(dx,dy),aim=dist>1e-6?Math.atan2(dy,dx)+Math.PI/2:J.angle;
    J.angle=tempestJetAngle(J.angle,aim,15,dt);
    s.mode=J.cue==='green'?'GREEN — COMMITTED':'RED — AIMING';
    /* Finish the visible turn before ignition; never snap a sideways nose at launch. */
    if(J.t>=1&&Math.abs(Math.atan2(Math.sin(aim-J.angle),Math.cos(aim-J.angle)))<0.025){
      const speed=(s.phase==='hell'||s.phase==='frenzy'?960:840)*(D.ai.alone&&p._tempestGray?1.15:1);
      J.vx=Math.sin(aim)*speed;J.vy=-Math.cos(aim)*speed;
      J.state='thrust';J.t=0;J.thrusts++;J.travel=0;
      /* Align the nose exactly with the committed velocity. No tracking after green. */
      J.angle=Math.atan2(J.vy,J.vx)+Math.PI/2;
      tlvSfx('tlvJetThrust');
    }
  } else if(J.state==='thrust'){
    s.mode='AFTERBURNER PASS';
    const speed=Math.hypot(J.vx,J.vy),step=speed*dt;
    s.boss.x+=J.vx*dt/TLV_KX;s.boss.y+=J.vy*dt/TLV_KY;J.travel+=step;
    if(J.t>0.12)J.cue=null;
    /* The entire hull AND its exhaust must leave the camera before the turn. */
    if(tempestJetOutside(p,90)){
      J.state='offscreen-turn';J.t=0;J.cue=null;
      const inset=Math.max(p._drawW/2+22,52),top=viewTopY()+77/viewZoom();
      const x=clamp(tlvX(D.ai.player.x)+(p._tempestGray?-96:96),camLeftX()+inset,camRightX()-inset);
      const y=Math.max(tlvY(230),top+p._drawH/2+12);
      J.reentry={x:(x-camLeftX())/TLV_KX,y:(y-TLV_YOFF)/TLV_KY};
      tlvSfx('tlvJetBrake');tlvSfx('tlvJetTurn');
    }
  } else if(J.state==='offscreen-turn'){
    s.mode='OFFSCREEN — TURNING BACK';
    const dx=(J.reentry.x-s.boss.x)*TLV_KX,dy=(J.reentry.y-s.boss.y)*TLV_KY;
    const aim=Math.atan2(dy,dx)+Math.PI/2;
    J.angle=tempestJetAngle(J.angle,aim,12,dt);
    if(J.t>=0.35&&Math.abs(Math.atan2(Math.sin(aim-J.angle),Math.cos(aim-J.angle)))<0.025){
      J.angle=aim;J.state='return';J.t=0;tlvSfx('tlvJetThrust');
    }
  } else if(J.state==='return'){
    s.mode='INBOUND — RETURN PASS';
    const dx=(J.reentry.x-s.boss.x)*TLV_KX,dy=(J.reentry.y-s.boss.y)*TLV_KY;
    if(Math.hypot(dx,dy)>1e-6)J.angle=Math.atan2(dy,dx)+Math.PI/2;
    if(move(J.reentry.x,J.reentry.y,560)){J.state='settle';J.t=0;tlvSfx('tlvJetTurn');}
  } else if(J.state==='settle'){
    s.mode='BANK — READY FOR NEXT PASS';
    const dx=(D.ai.player.x-s.boss.x)*TLV_KX,dy=(D.ai.player.y-s.boss.y)*TLV_KY;
    const aim=Math.atan2(dy,dx)+Math.PI/2;
    J.angle=tempestJetAngle(J.angle,aim,13,dt);
    if(J.t>=0.24&&Math.abs(Math.atan2(Math.sin(aim-J.angle),Math.cos(aim-J.angle)))<0.025){
      tempestJetCancel(b,p);
      J.cooldown=p._tempestGray?4.8:5.6;
      s.change(p._tempestGray?'regroup':(s.phase==='chase'||s.phase==='hell'?'strafe':'track'));
    }
  }
  /* Front guns follow the nose. Every shot still belongs to a live aperture. */
  if(J.state==='slide'||J.state==='thrust'){
    J.shot-=dt;
    if(J.shot<=0){J.shot=0.18;for(const id of [0,2])if(s.rig[id].hp>0){p._pending.push({id:id,a:J.angle-Math.PI/2,s:620,kind:'bolt',front:true});s.events.push('shot');}}
  }
  if((J.state==='thrust'||J.state==='return')&&typeof Snd!=='undefined'&&Snd.loopOn)Snd.loopOn('tlvJetEngine',J.state==='thrust'?0.88:0.55);
  if(s.phase==='frenzy')s.explode(dt,false);
  const bounds=tempestJetBounds(p);
  s.vulnerable=bounds.right>camLeftX()&&bounds.left<camRightX()&&bounds.bottom>viewTopY()+77/viewZoom()&&bounds.top<VH;
}
function tempestJetPose(p,dt){
  const J=p._jet,s=p._ai;
  J.baseAngle=s.boss.y>s.player.y?0:Math.PI;
  if(J.active||p.dead||s.gone)return;
  /* Rapid banking preserves the original travel paths between committed passes. */
  const dx=(s.stepDX||0)*TLV_KX,bank=Math.abs(dx)>0.1?clamp(dx*0.045,-0.28,0.28):0;
  J.angle=tempestJetAngle(J.angle,J.baseAngle+bank,13,dt);
}
function tempestJetBeamEnd(q){
  const top=viewTopY()+77/viewZoom(),left=camLeftX(),right=camRightX();
  const dx=Math.cos(q.ang),dy=Math.sin(q.ang),ts=[];
  if(Math.abs(dx)>1e-6){const t=(dx>0?right-q.x:q.x-left)/Math.abs(dx);if(t>0)ts.push(t);}
  if(Math.abs(dy)>1e-6){const t=(dy>0?VH+8-q.y:q.y-top)/Math.abs(dy);if(t>0)ts.push(t);}
  const len=ts.length?Math.min(...ts):VH;
  return {x:q.x+dx*len,y:q.y+dy*len,len:len};
}
function tempestJetBeamsDraw(p){
  for(const q of p._tlv.beams){
    const end=tempestJetBeamEnd(q);
    ctx.save();ctx.translate(q.x,q.y);ctx.rotate(q.ang-Math.PI/2);
    if(q.active){const im=tlvImg('tlv_beam');if(im){ctx.globalAlpha=0.9;ctx.drawImage(im,-17*TLV_S,0,34*TLV_S,end.len);}ctx.fillStyle='#f0ffff';ctx.fillRect(-2*TLV_S,0,4*TLV_S,end.len);}
    else{ctx.strokeStyle='rgba(70,220,255,0.68)';ctx.lineWidth=2;if(ctx.setLineDash)ctx.setLineDash([12,9]);ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,end.len);ctx.stroke();}
    ctx.restore();
  }
}
function tempestJetBeamTouches(q,x,y){
  const dx=x-q.x,dy=y-q.y,c=Math.cos(q.ang),sn=Math.sin(q.ang);
  const along=dx*c+dy*sn,side=-dx*sn+dy*c;
  return q.active&&along>0&&along<tempestJetBeamEnd(q).len&&Math.abs(side)<TLV_BEAM_HALF*TLV_S;
}
function tempestJetShipDraw(p){
  const J=p._jet,s=p._ai,T=p._tlv,beams=T.beams,key=tempestPlateKey(p);
  tempestJetBeamsDraw(p);
  ctx.save();ctx.translate(p.x,p.y);ctx.rotate(J.angle);ctx.translate(-p.x,-p.y);
  T.beams=[];p._jetLocalDraw=true;
  try{
    /* Authored paired engine flames, measured against the jet's two tail bells. */
    if(!p.dead){
      const im=tlvImg('ndr_dambreaker_bottomthruster_'+(Math.floor(s.time*20)%4));
      if(im){const h=J.active&&J.state==='thrust'?68:J.active&&J.state==='return'?42:J.cue?32:18;ctx.save();ctx.globalAlpha=0.82;ctx.drawImage(im,p.x-9,p.y+46*TLV_S,18,h);ctx.restore();}
    }
    tempestDraw(p);
    if(!p.dead&&J.cue&&typeof xartTint==='function'){
      const tint=xartTint(key,J.cue==='green'?TLV_JET_GREEN:TLV_JET_RED,0.85);
      if(tint){ctx.save();ctx.globalAlpha=J.cue==='green'?0.68:0.2+0.3*Math.abs(Math.sin(J.t*22));ctx.drawImage(tint,p.x-p._drawW/2,p.y-p._drawH/2,p._drawW,p._drawH);ctx.restore();}
    }
    if(p.dead)for(const f of T.fx)tempestBlit(tlvImg('nxp_barrage_'+Math.min(7,Math.floor(f.age/f.life*8))),p.x+f.ox*TLV_S,p.y+f.oy*TLV_S,f.s*TLV_S,f.s*TLV_S);
  }finally{p._jetLocalDraw=false;T.beams=beams;ctx.restore();}
  if(J.active&&J.state==='charge'){
    const x=tlvX(J.lock.x),y=tlvY(J.lock.y);
    ctx.save();ctx.strokeStyle=J.cue==='green'?TLV_JET_GREEN:TLV_JET_RED;ctx.globalAlpha=0.7;ctx.lineWidth=2;
    if(ctx.setLineDash)ctx.setLineDash([12,9]);ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(x,y);ctx.stroke();
    ctx.beginPath();ctx.arc(x,y,14,0,Math.PI*2);ctx.stroke();ctx.restore();
  }
}
