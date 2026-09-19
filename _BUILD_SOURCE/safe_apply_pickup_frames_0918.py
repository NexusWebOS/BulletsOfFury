from pathlib import Path
p=Path(__file__).resolve().parents[1]/'assets/game.js';s=p.read_text(encoding='utf-8')
def one(a,b):
 global s
 if s.count(a)!=1:raise SystemExit(f'{s.count(a)} matches: {a[:90]}')
 s=s.replace(a,b,1)

one("""      ctx.save(); ctx.translate(p.x,yb+Math.sin((p.bob||0)+performance.now()/300)*2.8);
      ctx.shadowColor=col; ctx.shadowBlur=18;
      let drew=null; if(typeof iconBlit==='function'){ try{ drew=iconBlit(ctx,'inf_'+p.elem,0,0,PICKUP_BOX*1.25,true); }catch(_fcb){} }
      if(drew==null){ ctx.rotate(Math.PI/4); ctx.fillStyle=I?I.body:'#888'; ctx.fillRect(-11,-11,22,22); }
      ctx.restore(); continue;""","""      const yy=yb+Math.sin((p.bob||0)+performance.now()/300)*2.8;
      if(pickupTurnFrame('turn_inf_'+p.elem+'_0918',p.x,yy,PICKUP_BOX*1.25,p.t,12))continue;
      ctx.save();ctx.translate(p.x,yy);ctx.fillStyle=I?I.body:'#888';ctx.fillRect(-11,-11,22,22);ctx.restore();continue;""")
one("""      ctx.save(); ctx.translate(p.x, yb+Math.sin((p.bob||0)+performance.now()/360)*2.4);
      ctx.shadowColor=col; ctx.shadowBlur=16;
      let drew=null;
      if(typeof iconBlit==='function'){ try{ drew=iconBlit(ctx,'inf_'+p.elem,0,0,PICKUP_BOX,true); }catch(_ib){ drew=null; } }""","""      const _infY=yb+Math.sin((p.bob||0)+performance.now()/360)*2.4;
      if(pickupTurnFrame('turn_inf_'+p.elem+'_0918',p.x,_infY,PICKUP_BOX,p.t,12))continue;
      ctx.save(); ctx.translate(p.x,_infY);
      let drew=null;""")
one("""  ctx.save(); ctx.translate(p.x, yb+bob);
  /* a cheap pulsing glow - one additive disc, never shadowBlur (0916ab: that was the space stages' whole cost) */
  const glow=p.kind==='scorechip'?({100:'#d08a4a',250:'#dfe8ff',500:'#ffd24a',1000:'#3fe3ff'}[p.val|0]||'#ffd24a'):(p.kind==='furybomb'?'#ff4a1a':'#ff2a2a');
  ctx.globalCompositeOperation='lighter'; ctx.globalAlpha=0.30+0.18*Math.sin(performance.now()/120);
  ctx.fillStyle=glow; ctx.beginPath(); ctx.arc(0,0,h*0.62,0,TAU); ctx.fill();
  ctx.globalCompositeOperation='source-over'; ctx.globalAlpha=1;
  if(XART.rdy(key)){ const im=XART.get(key), w=h*((im.naturalWidth||im.width)/(im.naturalHeight||im.height)); ctx.imageSmoothingEnabled=false; ctx.drawImage(im,-w/2,-h/2,w,h); }
  else { ctx.fillStyle=glow; ctx.fillRect(-8,-12,16,24); }
  ctx.restore();""","""  const turn=p.kind==='scorechip'?('turn_score_'+(p.val|0)+'_0918'):(p.kind==='furybomb'?'turn_furybomb_0918':'turn_timebomb_0918');
  if(pickupTurnFrame(turn,p.x,yb+bob,h,p.t,12))return true;
  if(XART.rdy(key)){const im=XART.get(key),w=h*((im.naturalWidth||im.width)/(im.naturalHeight||im.height));ctx.drawImage(im,p.x-w/2,yb+bob-h/2,w,h);}""")

for a,b in [
("floatText(p.x,p.y,'NUKES +2','#8de23a')","pickupAnnounce('NUKES +2','#8de23a')"),("floatText(p.x,p.y,'MISSILES +2','#8ecbff')","pickupAnnounce('MISSILES +2','#8ecbff')"),
("floatText(p.x,p.y,'NUKES +5','#8de23a')","pickupAnnounce('NUKES +5','#8de23a')"),("floatText(p.x,p.y,'MISSILES +5','#9fe0ff')","pickupAnnounce('MISSILES +5','#9fe0ff')"),
("floatText(p.x,p.y,'NUKES +10','#8de23a')","pickupAnnounce('NUKES +10','#8de23a')"),("floatText(p.x,p.y,'MISSILES +10','#ffd36b')","pickupAnnounce('MISSILES +10','#ffd36b')"),
("floatText(p.x,p.y,'NUKES +'+_c.n,'#8de23a')","pickupAnnounce('NUKES +'+_c.n,'#8de23a')"),("floatText(p.x,p.y,_c.label,_c.col)","pickupAnnounce(_c.label,_c.col)"),
("arcadeBanner('AKIMBO WEAPONS');floatText(x,y,'QUAD FIRE','#ff6848')","arcadeBanner('AKIMBO WEAPONS')"),
("arcadeBanner('HELPER ORB ONLINE');floatText(x,y,'AUTO SUPPORT','#62eaff')","arcadeBanner('HELPER ORB ONLINE')"),
("arcadeBanner('PROXIMITY MINE ARMED');floatText(x,y,'SPLASH + SHRAPNEL','#ff5848')","arcadeBanner('PROXIMITY MINE ARMED')")]:one(a,b)
p.write_text(s,encoding='utf-8',newline='\n');print('pickup frames applied',len(s.splitlines()),'lines')
