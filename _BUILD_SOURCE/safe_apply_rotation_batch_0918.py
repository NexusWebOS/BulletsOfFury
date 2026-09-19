from pathlib import Path

p=Path(__file__).resolve().parents[1]/'assets/game.js'
s=p.read_text(encoding='utf-8')

def one(a,b):
    global s
    n=s.count(a)
    if n!=1: raise SystemExit(f'expected 1, got {n}: {a[:120]!r}')
    s=s.replace(a,b,1)

one("  X._src['mode_continue_up_0915']='assets/game/ui/pickups_0915/continue_up.png';",
"  X._src['mode_continue_up_0915']='assets/game/ui/pickups_0915/continue_up.png';\n  const _turn0918='assets/game/rotation_frames_0918/';\n  for(const [_tk,_tf] of Object.entries({turn_life_0918:'life_up_turn.png',turn_continue_0918:'continue_up_turn.png',turn_spacehelper_0918:'space_helper_turn.png',turn_spaceakimbo_0918:'space_akimbo_turn.png',turn_spacemine_0918:'space_mine_turn.png',turn_furybomb_0918:'fury_bomb_turn.png',turn_timebomb_0918:'timed_bomb_turn.png',turn_score_100_0918:'score_100_turn.png',turn_score_250_0918:'score_250_turn.png',turn_score_500_0918:'score_500_turn.png',turn_score_1000_0918:'score_1000_turn.png'}))X._src[_tk]=_turn0918+_tf;\n  for(const _e of ['fire','ice','lightning','prism','toxic','kinetic','chrome','water','dark'])X._src['turn_inf_'+_e+'_0918']=_turn0918+'inf_'+_e+'_turn.png';\n  for(const _f of ['arm_flame_intact','arm_flame_damaged','arm_flame_exposed','arm_cannon_intact','arm_cannon_damaged','arm_cannon_exposed','body_intact','body_damaged','body_exposed','body_wreck','body_rotor','body_rotor_damaged'])X._src['fzt_'+_f+'_turn0918']=_turn0918+'fzt_'+_f+'_turn.png';\n  X._src.bmbar_frame_shield_v2='assets/game/ui/bossbar_0918/shield_frame_v2.png';")

one("function fztSprite(key,x,y,a,s,alpha,sx,sy){",
"function fztTurnKey(key){const k=key+'_turn0918';return typeof XART!=='undefined'&&XART.rdy(k)?k:null;}\nfunction fztTurnDraw(key,x,y,a,s,alpha,sx,sy,tint){\n  const tk=fztTurnKey(key);if(!tk)return false;const im=tint&&typeof xartTint==='function'?xartTint(tk,'#ffffff',.9):XART.get(tk);if(!im)return false;\n  const n=16,fw=(im.width||im.naturalWidth)/n,fh=(im.height||im.naturalHeight),i=((Math.round((((a||0)%TAU)+TAU)%TAU/TAU*n)%n)+n)%n,sc=(s==null?1:s)*FZT_S;\n  ctx.save();ctx.translate(x,y);ctx.scale(sc*(sx||1),sc*(sy||1));if(alpha!=null)ctx.globalAlpha=clamp(alpha,0,1);ctx.drawImage(im,i*fw,0,fw,fh,-fw/2,-fh/2,fw,fh);ctx.restore();return true;\n}\nfunction fztSprite(key,x,y,a,s,alpha,sx,sy){\n  if(fztTurnDraw(key,x,y,a,s,alpha,sx,sy,false))return true;")
one("function fztFlashSprite(key,x,y,a,s,alpha,sx,sy){\n  /* fztSprite's own placement", "function fztFlashSprite(key,x,y,a,s,alpha,sx,sy){\n  if(fztTurnDraw(key,x,y,a,s,alpha,sx,sy,true))return true;\n  /* fztSprite's own placement")

one('function drawHealthBarV2(kind, frac, cx, cy, w, inWorld){','function drawHealthBarV2(kind, frac, cx, cy, w, inWorld, lagKey){')
one('  const ok = drawHealthBarArt(kind, frac, cx, cy, w, inWorld)\n          || drawHealthBarDrawn(kind, frac, cx, cy, w, inWorld);','  const ok = drawHealthBarArt(kind, frac, cx, cy, w, inWorld, lagKey)\n          || drawHealthBarDrawn(kind, frac, cx, cy, w, inWorld, lagKey);')
one("        if(drawShieldBarArt(sf, cx, sy+h/2, w) && typeof drawBossTab==='function')\n          drawBossTab('shield', cx, sy, w);","        drawShieldBarArt(sf, cx, sy+h/2, w);")
one('function drawHealthBarArt(kind, frac, cx, cy, w, inWorld){','function drawHealthBarArt(kind, frac, cx, cy, w, inWorld, lagKey){')
one("  const key=kind||'boss';","  const key=lagKey||kind||'boss';")
one('function drawHealthBarDrawn(kind, frac, cx, cy, w, inWorld){','function drawHealthBarDrawn(kind, frac, cx, cy, w, inWorld, lagKey){')
one("  const key = kind || 'boss';","  const key = lagKey || kind || 'boss';")
one("function drawSubBossBar(b){\n  if(!b || b.dead || b.enter) return;","function drawSubBossBar(b){\n  if(!b || b.dead || b.enter) return;\n  if(b._rzbPair&&b._rzbPair.actors){const ps=b._rzbPair.actors,w=VW*.43,tab=BMTAB.h*(w/BMBAR.frameW);screenBar(function(){for(let i=0;i<2;i++){const p=ps[i],f=p&&p.maxhp?clamp(p.hp/p.maxhp,0,1):0;drawHealthBarV2('mini',f,VW*(i?0.745:0.255),20+tab+3,w,false,'razorback'+i);}});return;}")
one("if(R.state==='turret') rzbFlash(tk,p.x,p.y,R.turret,1,128,128,R.flash.turret,mul);","rzbFlash(tk,p.x,p.y,R.turret,1,128,128,R.flash.turret,mul);")

old=s[s.index('function drawShieldBarArt('):s.index('\n}\n\n/* the 0810n drawn gauge',s.index('function drawShieldBarArt('))+2]
assert len(old)<1800
new="""function drawShieldBarArt(frac, cx, cy, w){
  if(typeof XART==='undefined'||!XART.rdy('bmbar_frame_shield_v2'))return false;
  const im=XART.get('bmbar_frame_shield_v2'),fill=bmbarShieldFill(frac);if(!fill)return false;
  frac=clamp(frac||0,0,1);const ar=(im.naturalWidth||im.width)/(im.naturalHeight||im.height),h=w/ar;
  const x=Math.round(cx-w/2),y=Math.round(cy-h/2),fx=x+w*.067,fy=y+h*.43,fw=w*.866,fh=h*.235;
  ctx.save();ctx.imageSmoothingEnabled=true;ctx.drawImage(im,x,y,w,h);
  if(frac>0){ctx.save();ctx.beginPath();ctx.rect(fx,fy,fw*frac,fh);ctx.clip();ctx.drawImage(fill,fx,fy,fw,fh);ctx.globalAlpha=.12+.08*Math.sin(stateT*5);ctx.fillStyle='#e8fdff';ctx.fillRect(fx,fy,fw,fh);ctx.restore();}
  ctx.restore();return true;
}"""
one(old,new)

one("function floatText(x,y,txt,color){ floaters.push({x,y,txt,color,t:0,life:1.1}); }","function pickupAnnounce(txt,color){ if(typeof arcadeBanner==='function') arcadeBanner(String(txt||'').toUpperCase(),color); }\nfunction floatText(x,y,txt,color){ floaters.push({x,y,txt,color,t:0,life:1.1}); }")
for a,b in [
("floatText(p.x,p.y,'CONTINUE UP','#62e6ff');","pickupAnnounce('CONTINUE UP','#62e6ff');"),
("if(typeof floatText==='function') floatText(x==null?240:x, y==null?200:y, c.label, c.col);","if(typeof pickupAnnounce==='function') pickupAnnounce(c.label,c.col);"),
("floatText(p.x,p.y,'SPEED L'+run.speedLevel,'#7fd1ff')","pickupAnnounce('SPEED L'+run.speedLevel,'#7fd1ff')"),
("floatText(p.x,p.y,'SHIELD L'+run.shield, '#4ea0ff')","pickupAnnounce('SHIELD L'+run.shield, '#4ea0ff')"),
("floatText(p.x,p.y,_ms.name+' MISSILES','#9fe0ff')","pickupAnnounce(_ms.name+' MISSILES','#9fe0ff')"),
("floatText(p.x,p.y,'MISSILE+','#ff8a2e')","pickupAnnounce('MISSILE+','#ff8a2e')"),
("floatText(p.x,p.y,'1UP','#ff5a8a')","pickupAnnounce('1UP','#ff5a8a')"),
("floatText(p.x,p.y-10,'+'+v,{100:'#e0a060',250:'#e8f0ff',500:'#ffd24a',1000:'#7ff0ff'}[v]||'#ffd24a')","pickupAnnounce('+'+v,{100:'#e0a060',250:'#e8f0ff',500:'#ffd24a',1000:'#7ff0ff'}[v]||'#ffd24a')"),
]: one(a,b)

one("function drawPowerups(){","function pickupTurnFrame(key,x,y,h,t,frames){frames=frames||12;if(typeof XART==='undefined'||!XART.rdy(key))return false;const im=XART.get(key),fw=(im.naturalWidth||im.width)/frames,fh=(im.naturalHeight||im.height),i=((Math.floor((t||0)*12)%frames)+frames)%frames,w=h*(fw/fh);ctx.save();ctx.translate(Math.round(x),Math.round(y));ctx.imageSmoothingEnabled=false;ctx.drawImage(im,i*fw,0,fw,fh,-w/2,-h/2,w,h);ctx.restore();return true;}\nfunction drawPowerups(){")
one("  const im=XART.get(key),pulse=.5+.5*Math.sin((p.t||0)*7.5),h=48+2*pulse,w=h*(im.naturalWidth/im.naturalHeight);\n  ctx.save();ctx.translate(Math.round(p.x),Math.round(y));ctx.imageSmoothingEnabled=false;\n  ctx.globalAlpha=.97;ctx.shadowColor=p.kind==='life'?'#ff5b20':'#4deaff';ctx.shadowBlur=3+3*pulse;\n  ctx.drawImage(im,-w/2,-h/2,w,h);ctx.restore();return true;","  const pulse=.5+.5*Math.sin((p.t||0)*7.5),h=48+2*pulse,turn=p.kind==='life'?'turn_life_0918':'turn_continue_0918';\n  return pickupTurnFrame(turn,p.x,y,h,p.t,12);")
one("  const key=keys[p.kind];if(!key)return false;const box=p.kind==='hqspacebox',pulse=.5+.5*Math.sin((p.t||0)*7);\n  return spaceArmoryArt(key,p.x,y,(box?58:49)+pulse*2,box?'#55bcff':p.kind==='spacemine'?'#ff4a38':'#68eaff',0);","  const key=keys[p.kind];if(!key)return false;const box=p.kind==='hqspacebox',pulse=.5+.5*Math.sin((p.t||0)*7);\n  if(!box){const turn={spacehelper:'turn_spacehelper_0918',spaceakimbo:'turn_spaceakimbo_0918',spacemine:'turn_spacemine_0918'}[p.kind];if(pickupTurnFrame(turn,p.x,y,49+pulse*2,p.t,12))return true;}\n  return spaceArmoryArt(key,p.x,y,(box?58:49)+pulse*2,box?'#55bcff':p.kind==='spacemine'?'#ff4a38':'#68eaff',0);")

one("const S2VENT={warn:0.95, gap:[6.2,10.4], first:4.5, debris:5};","const S2VENT={warn:0.95,gap:[6.2,10.4],first:4.5,debris:5,edgeMin:10,edgeMax:42};")
one("try{ if(Audio.SFX.furnaceFlameRelease) Audio.SFX.furnaceFlameRelease(); }catch(_s){ }","try{ if(Audio.SFX.s2GeyserErupt) Audio.SFX.s2GeyserErupt(); }catch(_s){ }")
one("const v={side:side, x:side<0?L+rnd(24,64):R-rnd(24,64), y:(y!=null?y:rnd(VH*0.62,VH+4)), t:0, done:false};","const v={side:side,x:side<0?L+rnd(S2VENT.edgeMin,S2VENT.edgeMax):R-rnd(S2VENT.edgeMin,S2VENT.edgeMax),y:(y!=null?y:VH+2),t:0,done:false};")
one("try{ if(Audio.SFX.furnaceFlameIgnite) Audio.SFX.furnaceFlameIgnite(); }catch(_s){ }","try{ if(Audio.SFX.s2GeyserWarn) Audio.SFX.s2GeyserWarn(); }catch(_s){ }")
one("          if(w.caught && typeof playerHit==='function') playerHit();","          if(w.caught && typeof playerHit==='function') playerHit();\n          if(!w._passed&&w.y>player.y+hh*.34){w._passed=true;try{Audio.SFX.firewallPass&&Audio.SFX.firewallPass();}catch(_fp){}}")
one("    firewallPass:'assets/game/sounds/firewall_pass.wav',","    firewallPass:'assets/game/sounds/firewall_pass.wav',\n    s2GeyserWarn:'assets/game/sounds/s2_geyser_warn_0918.wav',\n    s2GeyserErupt:'assets/game/sounds/s2_geyser_erupt_0918.wav',")
one("    firewallPass:     {g:0.46, lp:4200, min:1.20},","    firewallPass:     {g:0.62, native:true, min:0.45},\n    s2GeyserWarn:      {g:0.64, native:true, min:0.70},\n    s2GeyserErupt:     {g:0.74, native:true, min:0.70},")

p.write_text(s,encoding='utf-8',newline='\n')
print('safe repair batch applied',len(s.splitlines()),'lines')
