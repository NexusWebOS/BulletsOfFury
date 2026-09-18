#!/usr/bin/env python3
"""
patch_forge_sequence_0917c.py - Mike's second pass on the Forge sequence, plus the bomb/score pickups.
Every anchor asserted (0906v: a str.replace whose needle is absent does not raise).
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
P = os.path.join(ROOT, 'assets', 'game.js')
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, 'anchor found %d times (want %d): %r' % (n, count, old[:100])
    s = s.replace(old, new)

# ---- art
rep("""  X._src['loadout_bays_0917b']='assets/game/ui/forge_0917b/loadout_bays.png';
""", """  X._src['loadout_bays_0917b']='assets/game/ui/forge_0917b/loadout_bays.png';
  /* 0917c: POWERS GAINED's own plate (same family), the FURIOUS coin, the two bombs, the score bullets */
  X._src['powers_bays_0917c']='assets/game/ui/forge_0917b/powers_bays.png';
  X._src['fury_coin_0917c']='assets/game/ui/pickups_0917b/fury_coin.png';
  X._src['fury_bomb_0917c']='assets/game/ui/pickups_0917b/fury_bomb.png';
  X._src['timed_bomb_0917c']='assets/game/ui/pickups_0917b/timed_bomb.png';
  for(const _v of [100,250,500,1000]) X._src['score_bullet_'+_v]='assets/game/ui/pickups_0917b/score_'+_v+'.png';
""")

# ---- the POWERS state
rep("""  FORGING:'forging', FORGED:'forged', LOADOUT:'loadout' };""",
    """  FORGING:'forging', FORGED:'forged', LOADOUT:'loadout', POWERS:'powers' };""")
rep("""  return st===GS.STAGECLEAR||st===GS.UNLOCKS||st===GS.FORGE||st===GS.FORGING||st===GS.FORGED||st===GS.LOADOUT;""",
    """  return st===GS.STAGECLEAR||st===GS.UNLOCKS||st===GS.POWERS||st===GS.FORGE||st===GS.FORGING||st===GS.FORGED||st===GS.LOADOUT;""")
rep("""    case GS.LOADOUT:    return drawLoadout(dt);
""", """    case GS.LOADOUT:    return drawLoadout(dt);
    case GS.POWERS:     return drawPowers(dt);
""")

# ---- WEAPONS GAINED is weapons only again; POWERS GAINED is its own screen
rep("""  const C=(run && run._stageCombos) || [];
  for(const c of C){
    const nm=(typeof forgeComboName==='function')?forgeComboName(c.elem,c.w):String(c.elem).toUpperCase();
    rows.push([nm, 'micon_forge_'+c.elem+'_'+c.w, (INFUSIONS[c.elem]||{}).body||null, 'power']);
  }
  return rows.slice(0, UNLOCK_MAX);""",
"""  /* ⚠ 0917c: THE BOSS'S POWERS ARE NOT LISTED HERE ANY MORE (Mike: "The weapons gained screen should be
     here when we unlock fire orb, ice freeze, thermofreeze ball, lightning orb, etc." and POWERS GAINED
     "should have its own screen"). They go to GS.POWERS, one bay per ELEMENT, naming no weapon. */
  return rows.slice(0, UNLOCK_MAX);""")
rep("""    const _uTitle=unlockHasPower(U.rows)?(unlockHasWeapon(U.rows)?'WEAPONS AND POWERS GAINED':'POWERS GAINED'):'NEW WEAPONS UNLOCKED';""",
    """    const _uTitle='WEAPONS GAINED';   /* Mike's name for it (0917c); POWERS GAINED is its own screen */""")
rep("""      const _forgeThen=function(){ if(typeof forgeVisible==='function' && forgeVisible()) forgeStart(_toLoadout); else _toLoadout(); };""",
"""      const _toForge=function(){ if(typeof forgeVisible==='function' && forgeVisible()) forgeStart(_toLoadout); else _toLoadout(); };
      /* weapons gained -> POWERS GAINED (its own screen, 0917c) -> the forge */
      const _forgeThen=function(){ if(typeof powersVisible==='function' && powersVisible()) powersStart(_toForge); else _toForge(); };""")

# ---- no weapon LEVELS in the Forge sequence (Mike: "thats handled in game with the icons")
rep("""          ctx.save(); ctx.globalAlpha=a; iconBlit(ctx,'inf_'+f.elem,bx+bw-eh*0.62,RY+eh*0.62,eh,true); ctx.restore();
          stageText(art,'L'+f.lv,bx+bw-eh*0.62,RY+eh*1.22,Math.max(7,eh*0.32),'#ffffff',0.8,a,0.06);""",
"""          ctx.save(); ctx.globalAlpha=a; iconBlit(ctx,'inf_'+f.elem,bx+bw-eh*0.62,RY+eh*0.62,eh,true); ctx.restore();""")
rep("""l2=forgeName(selW)+'   -   '+INFUSIONS[f.elem].name+' LEVEL '+f.lv+'   -   FIRE ADDS, CHARGE RE-SPECS'; }""",
    """l2=forgeName(selW)+'   -   '+INFUSIONS[f.elem].name+'   -   CHARGE RE-SPECS'; }""")
rep("""    if(product){
      const lit=(i+1)<=FG.lv, cur=(i+1)===FG.lv;
      const lbl='LEVEL '+FORGE_ROMAN[i+1];
      const lh=Math.min(r[3]*0.38,(typeof stageFitH==='function')?stageFitH(art2,lbl,r[2]*0.86,r[3]*0.38,7,0.06):r[3]*0.3);
      if(lit){ ctx.save(); ctx.globalAlpha=cur?(0.30+0.18*Math.sin(t*6)):0.16; ctx.fillStyle=I.body; ctx.fillRect(r[0]+3,r[1]+3,r[2]-6,r[3]-6); ctx.restore(); }
      if(art2) stageText(art2,lbl,cx,cy,lh,lit?(cur?'#ffffff':I.body):'#4a5266',0.85,1,0.06);
    } else {""", """    /* the loadout, in both phases - levels are the in-game upgrade, not the Forge's (Mike, 0917c) */
    {""")
rep("""    const lines=[WEAPONS[FG.w]||'WEAPON','+',I.name,'=',(FG.doneT>=0?(FORGE_ROMAN[FG.lv]||''):'?')];""",
    """    const lines=[WEAPONS[FG.w]||'WEAPON','+',I.name,'=',(FG.doneT>=0?'FORGED':'?')];""")
rep("""    const nm=(I.named&&I.named[FG.lv])?(I.name+' LEVEL '+FORGE_ROMAN[FG.lv]+'  -  '+I.named[FG.lv]):(I.name+'  LEVEL '+FORGE_ROMAN[FG.lv]);""",
    """    const nm=(WEAPONS[FG.w]||'WEAPON')+'   +   '+I.name;""")
rep("""(f?('   -   '+INFUSIONS[f.elem].name+' '+FORGE_ROMAN[f.lv]):'')""", """(f?('   -   '+INFUSIONS[f.elem].name):'')""")

# ---- the loadout's icons sit on the bays' MEASURED centres (Mike: "Center all icons in boxes")
rep("""  bayX:[0.0837,0.2276,0.3693,0.5132,0.6571,0.7973], bayY:0.3320, bayW:0.1205, bayH:0.2135,""",
"""  /* ⚠ the bay INTERIORS, measured 0917c: the first cut used the outer bevel box (y .3320 h .2135), which
     centred every icon ~6px above the well - Mike's "center all icons in boxes". Four wells read clean;
     the two whose edges merge with the frame take the same measured pitch (.14315). */
  bayX:[0.0858,0.2297,0.3721,0.5153,0.6584,0.8016], bayY:0.3555, bayW:0.1130, bayH:0.1888,""")
rep("""    forgeIconFit(key,cx,cy,bh*0.80,bw*0.80,a);""", """    forgeIconFit(key,cx,cy,Math.min(bh,bw)*0.86,0,a);   /* centred, never stretched */""")
rep("""      ctx.save(); ctx.globalAlpha=(L.row===0?1:0.45); if(L.row===0) forgeHexPointer(key,cx,cy,bh*0.80,'#ffd24a'); ctx.restore();""",
    """      ctx.save(); ctx.globalAlpha=(L.row===0?1:0.45); if(L.row===0) forgeHexPointer(key,cx,cy,Math.min(bh,bw)*0.86,'#ffd24a'); ctx.restore();""")

# ---- the FURIOUS coin wherever points are shown
rep("""      const conv='LEVEL SCORE '+_sc.toLocaleString('en-US')+'   =   +'+_n+' FURIOUS PTS';""",
    """      const conv='LEVEL SCORE '+_sc.toLocaleString('en-US')+'   =   '+'XX+'+_n;   /* XX = the coin's width, for fitting */""")
rep("""        stageText(art,conv,gx+gw/2,(g0+g1)/2,cH,'#ffd24a',0.9,1,0.06);""",
    """        stageTextCoin(art,'LEVEL SCORE '+_sc.toLocaleString('en-US')+'   =','+'+_n,gx+gw/2,(g0+g1)/2,cH,'#ffd24a',0.9,1,0.06);""")
rep("""        stageText(art,conv,b[0]+b[2]/2,b[1]+b[3]*0.24,cH,'#ffd24a',0.9,1,0.06);""",
    """        stageTextCoin(art,'LEVEL SCORE '+_sc.toLocaleString('en-US')+'   =','+'+_n,b[0]+b[2]/2,b[1]+b[3]*0.24,cH,'#ffd24a',0.9,1,0.06);""")
rep("""    const _fpL=(run._fpLevel&&run._fpLevel.fp>0)?('      FURIOUS  +'+run._fpLevel.fp):'';
    const l1='COMBINE  X'+(run.forgeCombos|0)+'      RE-SPEC  X'+(run.forgeRespecs|0)+'      LOADOUT  '+load.length+' OF '+FORGE_LOADOUT_MAX+_fpL;
    const h1=Math.min(13,(typeof stageFitH==='function')?stageFitH(art,l1,b[2]*0.94,b[3]*0.42,8,0.06):11);
    stageText(art,l1,b[0]+b[2]/2,b[1]+b[3]*0.30,h1,'#9fd6ff',0.8,A(0.20),0.06);""",
"""    const _fpN=(run._fpLevel&&run._fpLevel.fp>0)?(run._fpLevel.fp|0):0;
    const l1='COMBINE  X'+(run.forgeCombos|0)+'      RE-SPEC  X'+(run.forgeRespecs|0)+'      LOADOUT  '+load.length+' OF '+FORGE_LOADOUT_MAX;
    const h1=Math.min(13,(typeof stageFitH==='function')?stageFitH(art,l1+(_fpN?'      XX+'+_fpN:''),b[2]*0.94,b[3]*0.42,8,0.06):11);
    /* the level's conversion is the FURIOUS coin and its number, set on the end of the same line (0917c) */
    if(_fpN) stageTextCoin(art,l1+'     ','+'+_fpN,b[0]+b[2]/2,b[1]+b[3]*0.30,h1,'#9fd6ff',0.8,A(0.20),0.06,'#ffd24a');
    else stageText(art,l1,b[0]+b[2]/2,b[1]+b[3]*0.30,h1,'#9fd6ff',0.8,A(0.20),0.06);""")
rep("""    const head=(V.msgT>0&&V.msg)?String(V.msg).toUpperCase():(bal+' FURIOUS PTS');
    const hc=(V.msgT>0&&V.msg)?'#ffd24a':'#8de23a';
    const hh=(typeof stageFitH==='function')?stageFitH(art,head,VW-40,11,7,0.06):11;
    stageText(art,head,VW/2,44,hh,hc,0.85,1,0.06);""",
"""    const head=(V.msgT>0&&V.msg)?String(V.msg).toUpperCase():null;
    const hc=(V.msgT>0&&V.msg)?'#ffd24a':'#8de23a';
    const hh=(typeof stageFitH==='function')?stageFitH(art,head||String(bal),VW-40,11,7,0.06):11;
    if(head) stageText(art,head,VW/2,44,hh,hc,0.85,1,0.06); else stageTextCoin(art,'',String(bal),VW/2,44,hh,hc,0.85,1,0.06);""")
rep("""    const head=(A.msgT>0&&A.msg)?String(A.msg).toUpperCase():(bal+' FURIOUS PTS');
    const hc=(A.msgT>0&&A.msg)?'#ffd24a':'#8de23a';
    const hh=(typeof stageFitH==='function')?stageFitH(art,head,VW-40,10,7,0.06):10;
    stageText(art,head,VW/2,40,hh,hc,0.85,1,0.06);""",
"""    const head=(A.msgT>0&&A.msg)?String(A.msg).toUpperCase():null;
    const hc=(A.msgT>0&&A.msg)?'#ffd24a':'#8de23a';
    const hh=(typeof stageFitH==='function')?stageFitH(art,head||String(bal),VW-40,10,7,0.06):10;
    if(head) stageText(art,head,VW/2,40,hh,hc,0.85,1,0.06); else stageTextCoin(art,'',String(bal),VW/2,40,hh,hc,0.85,1,0.06);""")
rep("""    const p='+'+T.points+' FURIOUS';
    const hp=Math.max(7,Math.min(h*0.16,(typeof stageFitH==='function')?stageFitH(art,p,bs*1.9,h*0.16,7,0.05):7));
    const wp=(typeof stageWidth==='function')?stageWidth(art,p,hp,0.05):0;
    const pcx=Math.max(x+h*0.10+wp/2, bx+bs/2);
    stageText(art,p,pcx,by+bs+hp*0.80,hp,'#8de23a',0.9,a,0.05);""",
"""    const p='+'+T.points;
    const hp=Math.max(7,Math.min(h*0.16,(typeof stageFitH==='function')?stageFitH(art,'XX'+p,bs*1.9,h*0.16,7,0.05):7));
    const wp=((typeof stageWidth==='function')?stageWidth(art,p,hp,0.05):0)+hp*1.67;   /* + the coin and its gap */
    const pcx=Math.max(x+h*0.10+wp/2, bx+bs/2);
    stageTextCoin(art,'',p,pcx,by+bs+hp*0.80,hp,'#8de23a',0.9,a,0.05);""")
rep("""      const pt=String(r.cost);
      stageText(art,pt,x0+w-pad-((typeof stageWidth==='function')?stageWidth(art,pt,fh,0.06):0)/2,ry+rh/2,fh,bal>=r.cost?'#ffd24a':'#b06a6a',0.85,1,0.06);""",
"""      const pt=String(r.cost), gw=((typeof stageWidth==='function')?stageWidth(art,pt,fh,0.06):0)+fh*1.67;
      stageTextCoin(art,'',pt,x0+w-pad-gw/2,ry+rh/2,fh,bal>=r.cost?'#ffd24a':'#b06a6a',0.85,1,0.06);""")

# ---- the pickups and bombs: drop, collect, draw, tick, reset
rep("""function killDrop(e){
  if(!e || !e.dropOk || typeof dropPowerup!=='function') return;""",
"""function killDrop(e){
  if(!e || !e.dropOk || typeof dropPowerup!=='function') return;
  if(typeof bonusDrop==='function') bonusDrop(e);   /* score bullets and the two bombs - their own roll (0917c) */""")
rep("""  else if(p.kind==='capsule'){ crateBreak(p.x,p.y,'#7fd1ff'); p={kind:(Math.random()<0.5)?'speed':'shield',x:p.x,y:p.y}; }
  switch(p.kind){""",
"""  else if(p.kind==='capsule'){ crateBreak(p.x,p.y,'#7fd1ff'); p={kind:(Math.random()<0.5)?'speed':'shield',x:p.x,y:p.y}; }
  if(typeof bonusPickupApply==='function' && bonusPickupApply(p)) return;   /* score bullets and the bombs (0917c) */
  switch(p.kind){""")
rep("""    if(p.kind==='forgecombo'){
      /* the ELEMENT badge with the WEAPON's own icon inside it""",
"""    if(typeof bonusPickupDraw==='function' && bonusPickupDraw(p,yb)) continue;   /* 0917c */
    if(p.kind==='forgecombo'){
      /* the ELEMENT badge with the WEAPON's own icon inside it""")
rep("""  if(typeof stylishTick==='function') stylishTick(dt);""",
    """  if(typeof stylishTick==='function') stylishTick(dt);
  if(typeof bombTick==='function') bombTick(dt);   /* the Fury/Timed bombs (0917c) */""")
rep("""  // CRT scanlines
  drawScanlines();""", """  if(typeof bombFxDraw==='function') bombFxDraw();   /* the bombs' glow, wave and arcade overlay - screen space (0917c) */
  // CRT scanlines
  drawScanlines();""")
rep("""  if(run){ run._stageCombos=[]; run._forgeShown=false; }""",
    """  if(run){ run._stageCombos=[]; run._forgeShown=false; }
  if(typeof bombReset==='function') bombReset();   /* a fuse never carries into the next stage (0917c) */""")

NEW = open(os.path.join(ROOT, '_BUILD_SOURCE', 'forge_sequence_0917c.js'), encoding='utf-8').read()
rep("""
function drawGameOver(dt){""", "\n" + NEW + "\nfunction drawGameOver(dt){")
open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('patched OK')
