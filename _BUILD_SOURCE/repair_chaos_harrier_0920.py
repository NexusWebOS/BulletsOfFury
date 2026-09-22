"""Apply the measured Chaos Harrier art/attack repair without rewriting game.js line endings."""
from pathlib import Path

path = Path('assets/game.js')
data = path.read_bytes()
assert b'\r\n' not in data, 'game.js must remain LF'
source = data.decode('utf-8')


def replace(old: str, new: str) -> None:
    global source
    count = source.count(old)
    assert count == 1, f'expected one match, found {count}: {old[:90]!r}'
    source = source.replace(old, new, 1)


replace("function chaosHarrierFlash(b, family, point){ b._chFlash={family,point,t:0,life:0.24}; }",
        "function chaosHarrierFlash(b, family, point){\n"
        "  (b._chFlashes||(b._chFlashes=[])).push({family,point,t:0,life:0.24});\n"
        "}")
replace("  if(b._chFlash){ b._chFlash.t+=dt; if(b._chFlash.t>=b._chFlash.life)b._chFlash=null; }",
        "  if(b._chFlashes) b._chFlashes=b._chFlashes.filter(F=>{F.t+=dt;return F.t<F.life;});")
replace("  const arrive = phase===1 ? 'warp_plasma' : (phase===2 ? 'warp_side' : 'warp_plasma');",
        "  /* Each arrival reveals a different authored weapon: wing plasma, the two missile bays,\n"
        "     then the wing lasers. The pinned damage window still follows exactly three warps. */\n"
        "  const arrive = ['warp_plasma','warp_missile','warp_side'][(b._chWarpCount||0)%3];")
replace("  chaosHarrierBeamRay(b,chaosHarrierPoint(b,'nose'),Math.PI/2+(b._chBeamAng||0),24);",
        "  chaosHarrierBeamRay(b,chaosHarrierPoint(b,'nose'),Math.PI/2+(b._chBeamAng||0),36);")
replace("  if(st==='plasma'){\n    const times=[0.05,0.20,0.38,0.53]",
        "  if(st==='plasma'){\n"
        "    /* Glide with the target during the volley; the hull stays level as Mike requested. */\n"
        "    const goal=clamp(player.x,arena.left,arena.right);\n"
        "    b.x+=clamp(goal-b.x,-90*dt,90*dt);\n"
        "    const times=[0.05,0.20,0.38,0.53]")
replace("  if(st==='missile'){\n    const times=[0.28];\n    while(b._chStep<times.length && b._chT>=times[b._chStep]){\n      chaosHarrierShot(b,'missile','missile_bay',Math.PI/2,1.70); b._chStep++;\n    }",
        "  if(st==='missile'){\n"
        "    /* Sequential, straight-lane launches from the actual left and right open bays. */\n"
        "    const times=[0.28,0.60], bays=['left_missile_bay','right_missile_bay'];\n"
        "    while(b._chStep<times.length && b._chT>=times[b._chStep]){\n"
        "      chaosHarrierShot(b,'missile',bays[b._chStep],Math.PI/2,1.70); b._chStep++;\n"
        "    }")
replace("        chaosHarrierFlash(b,'sideflash',chaosHarrierPoint(b,'left_cannon'));",
        "        chaosHarrierFlash(b,'sideflash',chaosHarrierPoint(b,'left_cannon'));\n"
        "        chaosHarrierFlash(b,'sideflash',chaosHarrierPoint(b,'right_cannon'));")

marker = "function chaosHarrierWarpFrame(b){"
insert = """/* The source plates store four poses across shifted columns. Draw an individual pose's ink
   at a stable hardpoint; drawing the full PNG made plasma, the reactor beam and lance jump by
   8-32 source pixels on every animation frame. These crops were measured from the alpha bounds. */
const CH_CROP={
  plasma:[[119,32,48,112],[87,32,48,112],[55,32,48,112],[23,32,48,112]],
  beam:[[81,46,64,299],[73,46,64,299],[55,46,64,299],[47,46,64,299]],
  lance:[[120,10,47,66],[88,10,47,66],[56,10,47,66],[24,10,47,66]],
  sidelaser:[[90,37,17,93],[82,37,17,93],[64,37,17,93],[56,37,17,93]]
};
const CH_EFFECT_CENTRES={
  sideflash:[[116,97],[110,109],[106,112],[95,105]],
  launchflash:[[117,93],[109,97],[106,118],[95,98]],
  charge:[[116,92],[108,92],[107,99],[95,93]]
};
function chaosHarrierCropped(key,crop,x,y,w,h,alpha,blend,rot){
  if(typeof XART==='undefined'||!XART.rdy(key))return false;
  ctx.save();ctx.translate(x,y);if(rot)ctx.rotate(rot);
  ctx.imageSmoothingEnabled=false;
  if(alpha!=null)ctx.globalAlpha=alpha;
  if(blend)ctx.globalCompositeOperation=blend;
  ctx.drawImage(XART.get(key),crop[0],crop[1],crop[2],crop[3],-w/2,-h/2,w,h);
  ctx.restore();return true;
}
function chaosHarrierEffect(family,fi,x,y,w,h,alpha){
  const c=CH_EFFECT_CENTRES[family][fi];
  return chaosHarrierCropped('ch_'+family+'_'+fi,[c[0]-90,c[1]-90,180,180],
                            x,y,w,h,alpha,'lighter',0);
}
"""
replace(marker, insert + marker)
replace("  const F=b._chFlash;\n  if(F){\n    const fi=clamp(Math.floor((F.t/F.life)*4),0,3), a=Math.max(0,1-F.t/F.life);\n    chaosHarrierImage('ch_'+F.family+'_'+fi,F.point.x,F.point.y,b.w*0.54,b.w*0.54,a,'lighter',0);\n  }",
        "  for(const F of (b._chFlashes||[])){\n"
        "    const fi=clamp(Math.floor((F.t/F.life)*4),0,3), a=Math.max(0,1-F.t/F.life);\n"
        "    chaosHarrierEffect(F.family,fi,F.point.x,F.point.y,b.w*0.54,b.w*0.54,a);\n"
        "  }")
replace("        const C=CH_SIDE_CROP, len=VH-p.y+120, w=CH_SIDE_HALF*2;",
        "        const C=CH_CROP.sidelaser[fi], len=VH-p.y+120, w=CH_SIDE_HALF*2;")
replace("      const lw=b.w*0.30, lh=lw*(138/47), la=Math.PI/2+ang;\n"
        "      /* chaosHarrierImage centres the plate, and the housing is the plate's TOP third (measured:\n"
        "         row density 9999999888867764455434422210). Seat it down the beam line so the housing\n"
        "         lands on the cannon instead of floating above the wing. */\n"
        "      chaosHarrierImage('ch_lance_'+fi,p.x+Math.cos(la)*lh*0.30,p.y+Math.sin(la)*lh*0.30,\n"
        "                        lw,lh,ca,'lighter',ang);",
        "      /* The supplied lance reel shifts 32px per frame and already contains a long bolt.\n"
        "         Keep just the charging emitter on the cannon; the separate beam owns the burn. */\n"
        "      chaosHarrierCropped('ch_lance_'+fi,CH_CROP.lance[fi],p.x,p.y+13,\n"
        "                            39,55,ca,'lighter',ang);")
replace("      chaosHarrierImage('ch_charge_'+fi,nose.x,nose.y,b.w*0.50,b.w*0.50,0.90,'lighter',0);",
        "      chaosHarrierEffect('charge',fi,nose.x,nose.y,b.w*0.50,b.w*0.50,0.90);")
replace("      if(XART.rdy('ch_beam_'+fi))ctx.drawImage(XART.get('ch_beam_'+fi),0,46,192,299,-39,-7,78,len);",
        "      if(XART.rdy('ch_beam_'+fi)){const C=CH_CROP.beam[fi];\n"
        "        ctx.drawImage(XART.get('ch_beam_'+fi),C[0],C[1],C[2],C[3],-39,-7,78,len);}")
replace("  const h=b._chKind==='sidelaser'?60:(b._chKind==='missile'?36:31);\n"
        "  const w=h*(im.naturalWidth/Math.max(1,im.naturalHeight));\n"
        "  ctx.save();ctx.translate(b.x,b.y);ctx.rotate(ang);ctx.imageSmoothingEnabled=false;\n"
        "  ctx.globalCompositeOperation='lighter';ctx.drawImage(im,-w/2,-h/2,w,h);ctx.restore();return true;",
        "  const C=b._chKind==='plasma'?CH_CROP.plasma[fi]:CH_CROP.sidelaser[fi];\n"
        "  const w=b._chKind==='plasma'?18:22,h=b._chKind==='plasma'?42:60;\n"
        "  ctx.save();ctx.translate(b.x,b.y);ctx.rotate(ang);ctx.imageSmoothingEnabled=false;\n"
        "  ctx.globalCompositeOperation='lighter';\n"
        "  ctx.drawImage(im,C[0],C[1],C[2],C[3],-w/2,-h/2,w,h);\n"
        "  ctx.restore();return true;")

path.write_bytes(source.encode('utf-8'))
assert b'\r\n' not in path.read_bytes()
print('Patched Chaos Harrier attack choreography and measured reel crops; LF preserved.')
