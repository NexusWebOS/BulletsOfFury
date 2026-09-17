#!/usr/bin/env python3
"""
patch_forge_economy_0917.py - the currency behind the Forge: score -> Furious Points -> Armory levels.

Mike, 0917: "we need to design our currency system to unlock these upgrades. Furious Points are the
answer to incentivise playing the game on higher difficulties and other pilots, and your Score Points
in-game. Yes, the high-score points now become useful instead of a show off. You use your high score
points to purchase Furious Points. All icons here should get their level 1-5 upgrade generated
variants, and upgraded projectiles and more. Also, you may only equip 1 weapon type of each type."

Every edit is anchored on a single line of assets/game.js (LF) and refuses if the anchor is not found
exactly once - a patch that cannot fail is a patch that did not land (0906v).
"""
import os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, 'assets', 'game.js')
s = open(p, 'rb').read().decode('utf-8')
assert '\r\n' not in s, 'game.js is LF'
if 'SCORE_BANK_RATE' in s:
    print('already patched'); raise SystemExit(0)

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'anchor found %d times (wanted %d): %r' % (c, n, old[:90])
    s = s.replace(old, new)

# ---- 1. the balance counts exchanged points; the normaliser keeps forge levels and the bank ----------
rep("function furiousBalance(){return achievementPoints()-furiousSpent();}",
    "function furiousBalance(){return achievementPoints()+((typeof furiousExchanged==='function')?furiousExchanged():0)-furiousSpent();}")
rep("    for(const id of Object.keys(v.owned)){ if(!FURIOUS_SHOP[id]) continue; const q=v.owned[id]||{};\n"
    "      out.owned[id]={at:Number.isFinite(q.at)?q.at:0,cost:Number.isFinite(q.cost)?q.cost:(FURIOUS_SHOP[id].cost|0)}; }\n",
    "    for(const id of Object.keys(v.owned)){ if(!FURIOUS_SHOP[id] && !FORGE_LEVEL_ID_RE.test(id)) continue; const q=v.owned[id]||{};\n"
    "      out.owned[id]={at:Number.isFinite(q.at)?q.at:0,cost:Number.isFinite(q.cost)?q.cost:((FURIOUS_SHOP[id]||{}).cost|0)}; }\n"
    "  /* THE SCORE BANK (0917) rides the same store, for the same reason `owned` does: one profile, one\n"
    "     save, and a version bump would delete every award. Each field is re-typed on the way in. */\n"
    "  if(v.bank&&typeof v.bank==='object'){\n"
    "    const b=v.bank; out.bank={credit:Math.max(0,b.credit|0),runs:b.runs|0,pilots:{},exchanges:[],last:(b.last&&typeof b.last==='object')?b.last:null};\n"
    "    if(b.pilots&&typeof b.pilots==='object') for(const k of Object.keys(b.pilots)) out.bank.pilots[k]=b.pilots[k]|0;\n"
    "    if(Array.isArray(b.exchanges)) for(const x of b.exchanges){ if(x&&Number.isFinite(x.fp)) out.bank.exchanges.push({at:x.at|0,credit:x.credit|0,fp:x.fp|0}); }\n"
    "  }\n")
rep("function achievementProfileSnapshot(){return JSON.parse(JSON.stringify({version:achievementState.version,points:achievementPoints(),spent:furiousSpent(),balance:furiousBalance(),",
    "function achievementProfileSnapshot(){return JSON.parse(JSON.stringify({version:achievementState.version,points:achievementPoints(),spent:furiousSpent(),exchanged:(typeof furiousExchanged==='function')?furiousExchanged():0,bank:achievementState.bank||null,balance:furiousBalance(),")

# ---- 2. the economy block: the score bank, the exchange, the Armory's levels -------------------------
ECON = r"""
/* ============================================================
   THE SCORE EXCHANGE and THE ARMORY (Mike, 0917)
   "Furious Points are the answer to incentivise playing the game on higher difficulties and other
    pilots, and your Score Points in-game. Yes, the high-score points now become useful instead of a
    show off. You use your high score points to purchase Furious Points."

   Every run that ENDS - game over or victory - deposits its score into the profile's SCORE BANK as
   CREDIT, weighted by the difficulty it was flown on (SCORE_BANK_DIFF) and by whether that pilot has
   banked a run before (SCORE_BANK_NEW_PILOT: the first run on each pilot pays half again - that is
   the "other pilots" half of the brief). The VAULT's EXCHANGE row turns credit into Furious Points at
   SCORE_BANK_RATE. Credit below one point's worth stays in the bank for the next run.

   ⚠ THE BANK IS A LEDGER, NOT A COUNTER (0916's rule for the shop, applied again): what has been
   EXCHANGED is the sum of the exchange entries, and the balance is points + exchanged - spent. Two
   numbers describing one fact would drift the first time a save was interrupted between them.

   THE ARMORY sells the Forge's LEVELS. Level 1 of any weapon x element is earned in play - discover
   the element, combine it in the Forge - and levels 2..5 are bought here, per weapon x element,
   persistently (FORGE_LEVEL_COST). A forged weapon opens at its OWNED level; a repeat combine in the
   Forge still lifts it one more for the run, and a pickup in the field never lifts past the pickup
   ceiling (INFUSION_PICKUP_MAX), so the paid levels are the only road to IV and V.

   ⚠ ONE UPGRADE PER WEAPON TYPE, BY CONSTRUCTION. run.forge is keyed by SLOT - a slot holds one
   {elem, lv} and forgeCombine REPLACES it - and the loadout can never carry a slot twice
   (forgePick swaps). So "you may only equip 1 machine gun upgrade type, 1 laser upgrade type ..." is
   the shape of the data, not a check that could be forgotten. Section 372 pins it.
   ============================================================ */
const SCORE_BANK_RATE=1000;                                   /* 1 FURIOUS PT per 1,000 weighted score */
const SCORE_BANK_DIFF=Object.freeze({easy:0.5, normal:1.0, hard:1.5, furious:2.0, insanity:3.0});
const SCORE_BANK_NEW_PILOT=1.5;
const FORGE_LEVEL_COST=Object.freeze({2:150, 3:300, 4:600, 5:1000});
const FORGE_LEVEL_ID_RE=/^forge_[a-z]+_[0-9]_L[2-9]$/;
function scoreBank(){ if(!achievementState.bank) achievementState.bank={credit:0,runs:0,pilots:{},exchanges:[],last:null}; return achievementState.bank; }
function scoreBankCredit(){ return (achievementState.bank&&achievementState.bank.credit)|0; }
function scoreBankQuote(){ return Math.floor(scoreBankCredit()/SCORE_BANK_RATE); }
function scoreBankDeposit(score,dk,pk){
  score=Math.max(0,score|0); if(!score) return null;
  const B=scoreBank(), dm=SCORE_BANK_DIFF[dk]||1, first=!(B.pilots[pk]|0), pm=first?SCORE_BANK_NEW_PILOT:1;
  const credit=Math.round(score*dm*pm);
  B.credit=(B.credit|0)+credit; if(pk) B.pilots[pk]=(B.pilots[pk]|0)+1; B.runs=(B.runs|0)+1;
  B.last={score:score,diff:dk,pilot:pk,dm:dm,pm:pm,credit:credit,at:Date.now()};
  achievementSave();
  return B.last;
}
/* one deposit per run, whichever end it reaches first */
function scoreBankDepositRun(){
  if(!run||run._bankedOnce) return run?run._banked:null;
  run._bankedOnce=true;
  const total=(run.score|0)+((typeof coopOn!=='undefined'&&coopOn&&typeof run2!=='undefined'&&run2)?(run2.score|0):0);
  run._banked=scoreBankDeposit(total,diffKey,run.pilot);
  return run._banked;
}
function furiousExchanged(){ let n=0; const B=achievementState.bank; if(B&&B.exchanges) for(const x of B.exchanges) n+=x.fp|0; return n; }
/* returns the points bought, or 'empty' */
function scoreBankExchange(){
  const fp=scoreBankQuote(); if(fp<=0) return 'empty';
  const B=scoreBank(), used=fp*SCORE_BANK_RATE;
  B.credit=(B.credit|0)-used; B.exchanges.push({at:Date.now(),credit:used,fp:fp});
  achievementSave();
  return fp;
}
function forgeLevelId(elem,w,lv){ return 'forge_'+elem+'_'+(w|0)+'_L'+(lv|0); }
function forgeOwnedLevel(elem,w){ let lv=1; while(lv<INFUSION_MAX && furiousOwned(forgeLevelId(elem,w,lv+1))) lv++; return lv; }
function forgeLevelCost(elem,w){ const lv=forgeOwnedLevel(elem,w); return lv>=INFUSION_MAX?0:(FORGE_LEVEL_COST[lv+1]|0); }
/* 'ok' | 'maxed' | 'poor' | 'unknown' - a word, for the same reason furiousBuy returns one */
function forgeLevelBuy(elem,w){
  if(!INFUSIONS[elem]||!forgeCanTake(w)) return 'unknown';
  const lv=forgeOwnedLevel(elem,w); if(lv>=INFUSION_MAX) return 'maxed';
  const cost=FORGE_LEVEL_COST[lv+1]|0;
  if(furiousBalance()<cost) return 'poor';
  if(!achievementState.owned) achievementState.owned={};
  achievementState.owned[forgeLevelId(elem,w,lv+1)]={at:Date.now(),cost:cost};
  achievementSave();
  /* a level bought mid-run lands on the weapon that is already forged with that element */
  if(run&&run.forge&&run.forge[w]&&run.forge[w].elem===elem){ run.forge[w].lv=Math.max(run.forge[w].lv|0,lv+1); if((run.weapon|0)===w){ run.infusion=null; if(typeof forgeApply==='function') forgeApply(); } }
  return 'ok';
}
"""
rep("const ACHIEVEMENT_WEAPON_KEYS=Object.freeze(", ECON.lstrip('\n') + "const ACHIEVEMENT_WEAPON_KEYS=Object.freeze(")

# ---- 3. five levels; pickups stop at three; the named level's name carries upward ----------------------
rep("const INFUSION_MAX=3;\n",
    "const INFUSION_MAX=5;               /* 3 -> 5 (0917): IV and V are the ARMORY's paid levels */\n"
    "const INFUSION_PICKUP_MAX=3;        /* a pickup in the field never lifts an element past the named level */\n")
rep("  if(run.infusion && run.infusion.elem!==elem && (run.infusion.lv|0)>=INFUSION_MAX && typeof infusionFusion==='function') infusionFusion(run.infusion.elem, elem);",
    "  if(run.infusion && run.infusion.elem!==elem && (run.infusion.lv|0)>=INFUSION_PICKUP_MAX && typeof infusionFusion==='function') infusionFusion(run.infusion.elem, elem);")
rep("  else run.infusion.lv=Math.min(INFUSION_MAX,(run.infusion.lv|0)+1);\n",
    "  else run.infusion.lv=Math.min(Math.max(INFUSION_PICKUP_MAX,run.infusion.lv|0),(run.infusion.lv|0)+1);   /* never DOWN from a forged IV/V, never UP past III by pickup */\n")
rep("  const nm=(I.named&&I.named[lv])||null;\n",
    "  const nm=(I.named&&(I.named[lv]||(lv>INFUSION_PICKUP_MAX?I.named[INFUSION_PICKUP_MAX]:null)))||null;\n")
rep("  else run.forge[w]={elem:elem, lv:1};\n",
    "  else run.forge[w]={elem:elem, lv:(typeof forgeOwnedLevel==='function')?forgeOwnedLevel(elem,w):1};   /* opens at the level the ARMORY owns (0917) */\n")

# ---- 4. the levels ride the round ------------------------------------------------------------------------
rep("      if(b._inf==='fire') b._el='fire'; else if(b._inf==='ice') b._el='ice';\n",
    "      if(b._inf==='fire') b._el='fire'; else if(b._inf==='ice') b._el='ice';\n"
    "      /* THE ARMORY'S LEVELS RIDE THE ROUND (0917): above the pickup ceiling every level grows the round and\n"
    "         its damage a step - a change you can measure, not a colour. The beam is one reused object that sets\n"
    "         its own width every shot (kinetic reads beam.w), so it is left alone. */\n"
    "      if(b._inf && !b._child && b.kind!=='beam' && !b._infScaled){ b._infScaled=1; const _il=(run.infusion.lv|0);\n"
    "        if(_il>INFUSION_PICKUP_MAX){ const _s=1+0.12*(_il-INFUSION_PICKUP_MAX); b.w=(b.w||6)*_s; b.h=(b.h||10)*_s; b.dmg=Math.round((b.dmg||1)*(1+0.10*(_il-INFUSION_PICKUP_MAX))); } }\n")

# ---- 5. every run banks its score at its end ----------------------------------------------------------
rep("  setState(GS.GAMEOVER); Audio.stopMusic(); Audio.SFX.gameover();\n  if(run.score>=highScore)",
    "  if(typeof scoreBankDepositRun==='function') scoreBankDepositRun();   /* the score becomes bank credit (0917) */\n"
    "  setState(GS.GAMEOVER); Audio.stopMusic(); Audio.SFX.gameover();\n  if(run.score>=highScore)")
rep("function triggerVictory(){\n  bonusModesUnlockFromCampaign();\n  achievementRunComplete();\n",
    "function triggerVictory(){\n  bonusModesUnlockFromCampaign();\n  achievementRunComplete();\n  if(typeof scoreBankDepositRun==='function') scoreBankDepositRun();\n")
rep("  ctx.fillStyle='#9aa0aa'; ctx.font='10px \"BOFmil\", monospace'; ctx.fillText('HIGH  '+pad(highScore,8),VW/2,VH/2+28);\n  /* THE AUTHORED GAME OVER",
    "  ctx.fillStyle='#9aa0aa'; ctx.font='10px \"BOFmil\", monospace'; ctx.fillText('HIGH  '+pad(highScore,8),VW/2,VH/2+28);\n"
    "  /* the run's score just became bank credit - say so, with the weighting that made it (0917) */\n"
    "  if(run._banked&&run._banked.credit>0){ const B=run._banked; ctx.fillStyle='#8de23a'; ctx.font='bold 9px \"BOFmil\", monospace';\n"
    "    ctx.fillText('BANKED  '+pad(B.credit,8)+'  X'+B.dm+' '+String(B.diff||'').toUpperCase()+(B.pm>1?'  NEW PILOT X'+B.pm:''),VW/2,VH/2+44); }\n"
    "  /* THE AUTHORED GAME OVER")

# ---- 6. the VAULT: the EXCHANGE row on top, THE ARMORY row underneath ---------------------------------------
rep("function vaultRows(){\n  return furiousShopIds().map(function(id){\n    const it=FURIOUS_SHOP[id];\n    return {id:id,name:it.name,cost:it.cost|0,kind:it.kind,blurb:it.blurb||'',\n            pending:furiousSellable(id)?null:(it.pending||'NOT AVAILABLE YET'),\n            owned:furiousOwned(id)};\n  });\n}\n",
    "function vaultRows(){\n"
    "  const credit=scoreBankCredit(), fp=scoreBankQuote();\n"
    "  const rows=[{id:'__exchange',exchange:true,name:'EXCHANGE SCORE  -  '+credit+' CREDIT',cost:0,kind:'exchange',owned:false,pending:null,\n"
    "               blurb:fp>0?('BUY '+fp+' FURIOUS PTS AT '+SCORE_BANK_RATE+' CREDIT EACH'):('EVERY RUN BANKS ITS SCORE - HARDER FLIES PAY MORE')}];\n"
    "  for(const id of furiousShopIds()){\n"
    "    const it=FURIOUS_SHOP[id];\n"
    "    rows.push({id:id,name:it.name,cost:it.cost|0,kind:it.kind,blurb:it.blurb||'',\n"
    "            pending:furiousSellable(id)?null:(it.pending||'NOT AVAILABLE YET'),\n"
    "            owned:furiousOwned(id)});\n"
    "  }\n"
    "  rows.push({id:'__armory',armory:true,name:'THE ARMORY',cost:0,kind:'armory',owned:false,pending:null,blurb:'FORGE LEVELS II - V, PER WEAPON AND ELEMENT'});\n"
    "  return rows;\n"
    "}\n")
rep("  const r=vault.rows[vault.i]; if(!r) return null;\n  const res=furiousBuy(r.id);\n",
    "  const r=vault.rows[vault.i]; if(!r) return null;\n"
    "  if(r.exchange){\n"
    "    const fp=scoreBankExchange();\n"
    "    if(fp==='empty'){ vaultSay('NOTHING TO EXCHANGE - FINISH A RUN FIRST'); try{ Audio.SFX.blocked&&Audio.SFX.blocked(); }catch(_ve1){} }\n"
    "    else { vaultSay('+'+fp+' FURIOUS PTS'); try{ Audio.SFX.select&&Audio.SFX.select(); }catch(_ve2){} }\n"
    "    vault.rows=vaultRows(); return fp==='empty'?'empty':'exchange';\n"
    "  }\n"
    "  if(r.armory){ armoryOpen('vault'); setState(GS.ARMORY); return 'armory'; }\n"
    "  const res=furiousBuy(r.id);\n")
rep("    if(!r.owned && !r.pending){\n      const pt=String(r.cost);\n",
    "    if(!r.owned && !r.pending && !r.armory){\n      const pt=r.exchange?('+'+scoreBankQuote()):String(r.cost);\n")

# ---- 7. the ARMORY screen --------------------------------------------------------------------------------
rep("  VAULT:'vault' };", "  VAULT:'vault', ARMORY:'armory' };")
rep("    case GS.VAULT:        return drawVault(dt);\n", "    case GS.VAULT:        return drawVault(dt);\n    case GS.ARMORY:       return drawArmory(dt);\n")
ARMORY = r"""/* ---- THE ARMORY (0917): the Forge's levels, bought with Furious Points ----------------------------
   Six tabs - one per forgeable weapon - and nine element rows under each, every row wearing its badge
   at the level OWNED. FIRE buys the next level. Reached from the VAULT (its last row) and from the
   Forge (RETINA), and BACK returns to whichever opened it. */
const ARMORY_VIEW=5;
let armory=null;
function armoryOpen(back){
  armory={tab:0,i:0,scroll:0,t:0,msg:'',msgT:0,back:back||'vault'};
  try{ if(typeof XART!=='undefined'){ XART.rdy('statpanel_full_0916');
    for(const e of Object.keys(INFUSIONS)) for(const w of FORGE_WEAPONS) for(let l=1;l<=INFUSION_MAX;l++) XART.rdy('micon_forge_'+e+'_'+w+(l>1?'_'+l:'')); } }catch(_ao){}
}
function armorySay(m){ if(armory){ armory.msg=m; armory.msgT=2.2; } }
function armoryRows(w){
  return Object.keys(INFUSIONS).map(function(e){
    const lv=forgeOwnedLevel(e,w);
    return {elem:e,w:w,name:(FORGE_NAMES[e]&&FORGE_NAMES[e][w])||(INFUSIONS[e].name+' '+WEAPONS[w]),lv:lv,cost:forgeLevelCost(e,w),
            open:infusionGateOpen(e),gate:INFUSIONS[e].gate||null};
  });
}
function armoryBuy(){
  const A=armory; if(!A) return null;
  const w=FORGE_WEAPONS[A.tab|0], r=armoryRows(w)[A.i|0]; if(!r) return null;
  if(!r.open){ armorySay(r.gate==='ngplus'?'DARK MATTER OPENS IN NEW GAME +':'TIDAL OPENS AFTER STAGE 9'); try{ Audio.SFX.blocked&&Audio.SFX.blocked(); }catch(_ab0){} return 'gated'; }
  const res=forgeLevelBuy(r.elem,w);
  if(res==='ok'){ armorySay(r.name+'  -  LEVEL '+forgeOwnedLevel(r.elem,w)); try{ Audio.SFX.select&&Audio.SFX.select(); }catch(_ab1){} }
  else if(res==='maxed') armorySay(r.name+' IS AT LEVEL '+INFUSION_MAX);
  else if(res==='poor') armorySay('NEED '+Math.max(0,r.cost-furiousBalance())+' MORE FURIOUS PTS');
  else armorySay('NOT AVAILABLE');
  if(res!=='ok'){ try{ Audio.SFX.blocked&&Audio.SFX.blocked(); }catch(_ab2){} }
  return res;
}
function drawArmory(dt){
  const A=armory||(armoryOpen('vault'),armory); A.t+=dt; if(A.msgT>0) A.msgT-=dt;
  if(typeof scrollSpaceBG==='function') scrollSpaceBG(dt); else { ctx.fillStyle='#0a0c14'; ctx.fillRect(0,0,VW,VH); }
  const art=(typeof curFontArt==='function')?curFontArt():null;
  const bal=furiousBalance();
  A.tab=((A.tab|0)%FORGE_WEAPONS.length+FORGE_WEAPONS.length)%FORGE_WEAPONS.length;
  const w=FORGE_WEAPONS[A.tab], rows=armoryRows(w);
  if(art && typeof stageText==='function'){
    stageText(art,'THE ARMORY',VW/2,22,18,'#ffd24a',0.9,1,0.08);
    const head=(A.msgT>0&&A.msg)?String(A.msg).toUpperCase():(bal+' FURIOUS PTS');
    const hc=(A.msgT>0&&A.msg)?'#ffd24a':'#8de23a';
    const hh=(typeof stageFitH==='function')?stageFitH(art,head,VW-40,10,7,0.06):10;
    stageText(art,head,VW/2,40,hh,hc,0.85,1,0.06);
  }
  /* the weapon tabs */
  const tabY=54, tabH=13, tx0=18, tw=(VW-36)/FORGE_WEAPONS.length;
  for(let i=0;i<FORGE_WEAPONS.length;i++){
    const on=(i===A.tab), bx=tx0+i*tw;
    ctx.save(); ctx.fillStyle=on?'rgba(255,210,74,0.16)':'rgba(16,18,26,0.55)'; ctx.fillRect(bx+1,tabY,tw-2,tabH);
    ctx.strokeStyle=on?'#ffd24a':'#3c4354'; ctx.lineWidth=1; ctx.strokeRect(bx+1.5,tabY+0.5,tw-3,tabH-1); ctx.restore();
    if(art){ const lb=String(WEAPONS[FORGE_WEAPONS[i]]||'').toUpperCase();
      const fh=(typeof stageFitH==='function')?stageFitH(art,lb,tw-8,8,6,0.06):8;
      stageText(art,lb,bx+tw/2,tabY+tabH/2,fh,on?'#ffd24a':'#7f8899',0.85,1,0.06); }
  }
  const pl=(typeof XART!=='undefined' && XART.rdy('statpanel_full_0916')) ? XART.get('statpanel_full_0916') : null;
  const x0=18, wdt=VW-36, y0=72, rowH=(VH-y0-40)/ARMORY_VIEW, rh=rowH*0.88;
  const maxScroll=Math.max(0,rows.length-ARMORY_VIEW);
  A.i=clamp(A.i|0,0,Math.max(0,rows.length-1));
  if(A.i<A.scroll) A.scroll=A.i; else if(A.i>=A.scroll+ARMORY_VIEW) A.scroll=A.i-ARMORY_VIEW+1;
  A.scroll=clamp(A.scroll|0,0,maxScroll);
  for(let k=0;k<ARMORY_VIEW;k++){
    const r=rows[k+A.scroll]; if(!r) break;
    const ry=y0+k*rowH, sel=((k+A.scroll)===A.i);
    ctx.save();
    if(pl && typeof unlockPanel==='function') unlockPanel(pl,UNLOCK_ART.strip,x0,ry,wdt,rh,true);
    else { ctx.fillStyle='#16161f'; ctx.fillRect(x0,ry,wdt,rh); ctx.strokeStyle='#705848'; ctx.lineWidth=1; ctx.strokeRect(x0+0.5,ry+0.5,wdt-1,rh-1); }
    if(sel){ ctx.strokeStyle='#ffd24a'; ctx.lineWidth=2; ctx.strokeRect(x0+1,ry+1,wdt-2,rh-2); }
    ctx.restore();
    /* the badge at the level owned - the same key weaponIconKey answers once the weapon is forged */
    const ik='micon_forge_'+r.elem+'_'+w+(r.lv>1?'_'+r.lv:''), ih=rh*0.82, ix=x0+wdt*0.012+ih/2, iy=ry+rh/2;
    ctx.save(); ctx.globalAlpha=r.open?1:0.35;
    if(typeof iconBlit==='function'){ if(XART.rdy(ik)) iconBlit(ctx,ik,ix,iy,ih,true); else if(XART.rdy('micon_forge_'+r.elem+'_'+w)) iconBlit(ctx,'micon_forge_'+r.elem+'_'+w,ix,iy,ih,true); }
    ctx.restore();
    if(!art) continue;
    const pad=wdt*0.035+ih, lh=Math.min(rh*0.40,10);
    const col=!r.open?'#6a7180':(r.lv>=INFUSION_MAX?'#8de23a':(bal>=r.cost?'#ffd24a':'#b06a6a'));
    const nm=String(r.name).toUpperCase(), room=wdt-pad*2-60;
    const fh=(typeof stageFitH==='function')?stageFitH(art,nm,room,lh,7,0.06):lh;
    stageText(art,nm,x0+pad+((typeof stageWidth==='function')?stageWidth(art,nm,fh,0.06):0)/2,ry+rh*0.34,fh,col,0.85,1,0.06);
    const sub=!r.open?(r.gate==='ngplus'?'NEW GAME + ONLY':'AFTER STAGE 9'):('LEVEL '+r.lv+(r.lv>=INFUSION_MAX?'  -  MAX':('  -  NEXT: LEVEL '+(r.lv+1))));
    const sh=(typeof stageFitH==='function')?stageFitH(art,sub,room,lh*0.85,6,0.06):lh*0.85;
    stageText(art,sub,x0+pad+((typeof stageWidth==='function')?stageWidth(art,sub,sh,0.06):0)/2,ry+rh*0.70,sh,'#7f8899',0.8,1,0.06);
    if(r.open && r.lv<INFUSION_MAX){ const pt=String(r.cost);
      stageText(art,pt,x0+wdt-wdt*0.04-((typeof stageWidth==='function')?stageWidth(art,pt,fh,0.06):0)/2,ry+rh/2,fh,bal>=r.cost?'#ffd24a':'#b06a6a',0.85,1,0.06); }
  }
  if(maxScroll>0){
    const ax=VW-12, tw2=8, th=7;
    ctx.save(); ctx.fillStyle='#9fd6ff';
    if(A.scroll>0){ ctx.beginPath(); ctx.moveTo(ax-tw2/2,y0+th); ctx.lineTo(ax+tw2/2,y0+th); ctx.lineTo(ax,y0); ctx.closePath(); ctx.fill(); }
    if(A.scroll<maxScroll){ const by=y0+ARMORY_VIEW*rowH; ctx.beginPath(); ctx.moveTo(ax-tw2/2,by-th); ctx.lineTo(ax+tw2/2,by-th); ctx.lineTo(ax,by); ctx.closePath(); ctx.fill(); }
    ctx.restore();
  }
  if(typeof controlHintRow==='function')
    controlHintRow([['pad_dpad','WEAPON / ELEMENT'],['pad_a','BUY LEVEL'],['pad_b','BACK']],VH-14,VW/2,VW-24);
  /* each read ONCE - these consume their tap */
  const up=(Input.menuUp?Input.menuUp():false), dn=(Input.menuDown?Input.menuDown():false);
  const lf=(Input.menuLeft?Input.menuLeft():false), rt=(Input.menuRight?Input.menuRight():false);
  const go=(Input.menuConfirm?Input.menuConfirm():false);
  if(dn){ A.i=Math.min(rows.length-1,A.i+1); try{ Audio.SFX.blip&&Audio.SFX.blip(); }catch(_a3){} }
  else if(up){ A.i=Math.max(0,A.i-1); try{ Audio.SFX.blip&&Audio.SFX.blip(); }catch(_a4){} }
  if(lf||rt){ A.tab=((A.tab+(rt?1:-1))%FORGE_WEAPONS.length+FORGE_WEAPONS.length)%FORGE_WEAPONS.length; A.i=0; A.scroll=0; try{ Audio.SFX.blip&&Audio.SFX.blip(); }catch(_a5){} }
  if(go) armoryBuy();
  if(Input.menuBack&&Input.menuBack()){
    if(A.back==='forge' && typeof forge!=='undefined' && forge) setState(GS.FORGE);
    else { setState(GS.VAULT); vaultOpen(); }
  }
}
function drawAwards(dt){"""
rep("function drawAwards(dt){", ARMORY)

# ---- 8. the Forge opens the Armory on RETINA -------------------------------------------------------------
rep("                 :[['pad_a','SELECT SLOT'],['pad_x','RE-SPEC'],['pad_start','CONTINUE']];",
    "                 :[['pad_a','SELECT SLOT'],['pad_x','RE-SPEC'],['pad_y','ARMORY'],['pad_start','CONTINUE']];")
rep("  const charge=(keybind.charge||[]).some(function(k){ return Input.tap(k); });\n  const click=Input.mouse.down&&!F.md;",
    "  const charge=(keybind.charge||[]).some(function(k){ return Input.tap(k); });\n"
    "  const retina=(keybind.retina||[]).some(function(k){ return Input.tap(k); });\n"
    "  const click=Input.mouse.down&&!F.md;")
rep("    else if(mS||enter){\n      Input.mouse.down=false;\n      run._wbag=[];\n      const done=F.onDone; forge=null;",
    "    else if(retina){ armoryOpen('forge'); setState(GS.ARMORY); }   /* the Armory, and BACK returns here (0917) */\n"
    "    else if(mS||enter){\n      Input.mouse.down=false;\n      run._wbag=[];\n      const done=F.onDone; forge=null;")

# ---- 9. the badge at the level, on every surface ---------------------------------------------------------
rep("  if(typeof forgeEntry==='function'){ const _fe=forgeEntry(w); if(_fe && _fe.elem && XART._src && XART._src['micon_forge_'+_fe.elem+'_'+w]) return 'micon_forge_'+_fe.elem+'_'+w; }\n",
    "  if(typeof forgeEntry==='function'){ const _fe=forgeEntry(w); if(_fe && _fe.elem && XART._src){\n"
    "    const _fk='micon_forge_'+_fe.elem+'_'+w, _fl=_fe.lv|0;\n"
    "    if(_fl>1 && XART._src[_fk+'_'+_fl]) return _fk+'_'+_fl;      /* the level's own badge (II..V), when its plate landed */\n"
    "    if(XART._src[_fk]) return _fk; } }\n")
rep("    for(const _fs of [0,1,2,3,5,7]) X._src['micon_forge_'+_fe+'_'+_fs]='assets/game/ui/forge_0917/micon_forge_'+_fe+'_'+_fs+'.png';\n",
    "    for(const _fs of [0,1,2,3,5,7]){ X._src['micon_forge_'+_fe+'_'+_fs]='assets/game/ui/forge_0917/micon_forge_'+_fe+'_'+_fs+'.png';\n"
    "      for(let _fl=2;_fl<=5;_fl++) X._src['micon_forge_'+_fe+'_'+_fs+'_'+_fl]='assets/game/ui/forge_0917/micon_forge_'+_fe+'_'+_fs+'_'+_fl+'.png'; }\n")

open(p, 'wb').write(s.encode('utf-8'))
print('patched: score bank + exchange, armory levels, INFUSION_MAX 5, round scaling, game-over line, vault rows, GS.ARMORY, forge hook, icon levels')
