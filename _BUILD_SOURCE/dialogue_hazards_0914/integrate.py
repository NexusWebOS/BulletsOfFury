"""Apply this drop to the measured solid-assembly baseline; preserve runtime LF."""
from pathlib import Path
import hashlib
R=Path(__file__).resolve().parents[2]
p=R/'assets/game.js';s=p.read_text(encoding='utf-8')
assert hashlib.sha256(p.read_bytes()).hexdigest()=='5150c9c4134da494bec2d2789b9e7fecfd4c022f8647302a470945f4072109b5'
def rep(a,b):
 global s
 assert a in s,a[:120]
 s=s.replace(a,b,1)
def block(start,end,new):
 global s
 a=s.index(start);b=s.index(end,a);s=s[:a]+new+'\n'+s[b:]
rep("  for(const _f of ['ocean','bar','btn_save','btn_load','btn_exit'])", "  X._src['dlg_rect_0914']='assets/game/dialogue_0914/frame.png';\n  for(const _f of ['ocean','bar','btn_save','btn_load','btn_exit'])")
rep('function dlgBox(o){',(R/'_BUILD_SOURCE/dialogue_hazards_0914/frame.js').read_text()+'\nfunction dlgBox(o){')
rep("  const _portK=(_isPilot && typeof pilotPortrait==='function')", "  const _portK=o.portraitKey || ((_isPilot && typeof pilotPortrait==='function')")
rep("? pilotPortrait(_pk, _talking?'talk':(o.emo||'idle')) : null;", "? pilotPortrait(_pk, _talking?'talk':(o.emo||'idle')) : null);")
rep("o.pw || (_hasPort?344:300)","o.pw || (VW-20)")
rep("  const ph=o.ph || Math.round(VH*0.17);","  const ph=o.ph || Math.round(pw*0.28);")
rep("  if(!(typeof drawPanel==='function' && drawPanel('dlg_window', null, x, y, pw, ph))){", "  if(!dialogueFrameDraw(who,tint,x,y,pw,ph) && !(typeof drawPanel==='function' && drawPanel('dlg_window', null, x, y, pw, ph))){")
rep("msgTextLeft(who, ix, y+Math.round(ph*0.24)","msgTextLeft(who, ix+(iw-msgMeasure(who,_nh))/2, y+Math.round(ph*0.24)")
rep("color:DIALOGUE_BODY_COLOR,alpha:fade,outline:true});", "color:DIALOGUE_BODY_COLOR,alpha:fade,outline:true,align:'center',stableCenter:true,valign:'middle'});")
rep("yy=o.y+layout.H/2;", "yy=o.y+layout.H/2+(o.valign==='middle'?Math.max(0,(o.h-layout.height)/2):0);")
rep("msgMeasure(part,layout.H,o.spacing))/2;", "msgMeasure(o.stableCenter?line:part,layout.H,o.spacing))/2;")
# Modal comms use exactly the same frame and layout as in-play dialogue.
block('function drawCommWindow(o){','function drawPilotComm(P,t){', '''function drawCommWindow(o){
  const ap=clamp(o.appear==null?1:o.appear,0,1),pw=Math.min(VW-24,446),ph=Math.round(pw*.28);
  const px0=(VW-pw)/2,py0=VH*.34,ease=ap*ap*(3-2*ap);
  ctx.save();ctx.globalAlpha=.66*ap;ctx.fillStyle='#030407';ctx.fillRect(0,0,VW,VH);ctx.globalAlpha=1;
  const full=String(o.text||''),shown=o.charsShown==null?full:full.slice(0,Math.max(0,Math.floor(o.charsShown)));
  dlgBox({who:o.name,tint:o.tint,full,shown,portraitKey:o.portraitKey||o.cardKey,
    fade:ap,pw,ph,x:px0,y:py0+(1-ease)*20,screenSpace:false});
  ctx.restore();return {px0,py0,pw,ph,inL:px0+16,inT:py0+12,inW:pw-32,inH:ph-24,pbW:ph*.74};
}''')
rep("ctx.drawImage(XART.get(_dk),dx,dy,dw,dh);", "if(!dialogueFrameDraw(_who,null,dx,dy,dw,dh))ctx.drawImage(XART.get(_dk),dx,dy,dw,dh);\n  msgFaceUse('dialogue');")
rep("msgTextLeft(name,dx+padX,nameY+nameH*.5", "msgTextLeft(name,dx+(dw-msgMeasure(name,nameH,.06))/2,nameY+nameH*.5")
rep("color:DIALOGUE_BODY_COLOR,tintA:1,alpha:1,outline:1});", "color:DIALOGUE_BODY_COLOR,tintA:1,alpha:1,outline:1,align:'center',stableCenter:true,valign:'middle'});")
# Every visible asteroid is owned by the collision pool, never a decorative duplicate.
block('function l5FieldReset(){','/* ============================================================\n   STAGE-8 FURIOUS', '''function l5FieldReset(){
  l5Field=[]; // Retired scenery rocks: l5Rocks owns all visible asteroid bodies.
}
''')
a=s.index('  /* the celestial reel:',s.index('function bg5Draw(dt){'));b=s.index('\n}\n',a)
s=s[:a]+"  // Decorative comet reel retired: only shootable encounter comets may cross the playfield.\n"+s[b:]
rep('  r.maxhp=r.hp; r.rad=26*sc;', '  r.maxhp=r.hp;r._l5Rock=true;l5RockBounds(r);')
rep('function l5RocksReset(){ l5Rocks=[]; l5RockT=2.5; }', '''function l5RockBounds(r){
  const k='np5_ast_'+r.idx;
  const im=XART.rdy(k)?XART.get(k):null;
  // Authored plates are compact rock silhouettes; the inner body is the collision circle.
  r.rad=Math.min(im?(im.naturalWidth||im.width):174,im?(im.naturalHeight||im.height):174)*r.sc*.40;
  r.w=r.h=r.rad*2;return r.rad;
}
function l5RockDamage(r,dmg){
  if(r.dead||r._dieT>=0)return;
  r.hp-=dmg;r.flash=.10;if(r.hp<=0)l5RockBreak(r);
}
function l5RocksReset(){ l5Rocks=[]; l5RockT=2.5; }''')
a=s.index('  // SHATTER: throw smaller');b=s.index('  run.score+=',a)
s=s[:a]+"  // Authored explosion replaces the body; no harmless fading rock copies.\n  r.debris=[];\n"+s[b:]
rep('    r.x+=r.vx; r.y+=r.vy; r.rot+=r.spin*dt;', '    l5RockBounds(r);r.x+=r.vx*dt*60; r.y+=r.vy*dt*60; r.rot+=r.spin*dt;')
rep('      if(b.dead) continue;\n      if(Math.hypot(b.x-r.x, b.y-r.y) < r.rad){\n        r.hp-=(b.dmg||1); r.flash=0.10;', "      if(b.dead||String(b.kind||'').startsWith('space')||b._impact) continue;\n      if(Math.hypot(b.x-r.x, b.y-r.y) < r.rad+Math.max(b.w||2,b.h||2)*.25){\n        l5RockDamage(r,b.dmg||1);")
a=s.index('    if(r._dieT>=0){',s.index('function l5RocksDraw(){'));b=s.index("    const k='np5_ast_'+r.idx;",a)
s=s[:a]+"    if(r._dieT>=0)continue;\n"+s[b:]
rep('ctx.save(); ctx.translate(r.x,r.y); ctx.rotate(r.rot);', "ctx.save();ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over'; ctx.translate(r.x,r.y); ctx.rotate(r.rot);")
rep('  for(const p of powerups)if(spaceShootableContainer(p))a.push(p);', "  for(const p of powerups)if(spaceShootableContainer(p))a.push(p);\n  if(run.stage===5)for(const r of l5Rocks)if(!r.dead&&r._dieT<0){l5RockBounds(r);a.push(r);}")
rep("  if(t._retinaOwner){retinaMissileDamage(t,dmg,b);}","  if(t._l5Rock){l5RockDamage(t,dmg);}\n  else if(t._retinaOwner){retinaMissileDamage(t,dmg,b);}")
p.write_text(s,encoding='utf-8',newline='\n')
