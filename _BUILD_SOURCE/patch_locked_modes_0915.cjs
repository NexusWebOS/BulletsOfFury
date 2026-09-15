const fs=require('fs'),path=require('path');
const ROOT=path.resolve(__dirname,'..');
const gamePath=path.join(ROOT,'assets','game.js');
const testPath=path.join(ROOT,'_BUILD_SOURCE','test_fl.js');
const recovery=path.join(ROOT,'_shots','locked_modes_0915','recovery');
fs.mkdirSync(recovery,{recursive:true});
const original=fs.readFileSync(gamePath,'utf8');
const originalTest=fs.readFileSync(testPath,'utf8');
if(original.includes('\r\n'))throw new Error('assets/game.js must remain LF');
if(!originalTest.includes('\r\n')||/(^|[^\r])\n/.test(originalTest))throw new Error('test_fl.js must remain CRLF');
fs.writeFileSync(path.join(recovery,'game.js.before'),original,'utf8');
fs.writeFileSync(path.join(recovery,'test_fl.js.before'),originalTest,'utf8');
let game=original;
function once(oldText,newText,label){
  const parts=game.split(oldText);
  if(parts.length!==2)throw new Error(label+' expected one match, got '+(parts.length-1));
  game=parts[0]+newText+parts[1];
}

once("  X._src['pause_button_0915']='assets/game/ui/pause_0915/button.png';\n",
"  X._src['pause_button_0915']='assets/game/ui/pause_0915/button.png';\n"+
"  /* Generated mode plates use a source crop because the generator baked a checkerboard beyond\n"+
"     their beveled frames. The exact Nexus II chain plate is clipped over the same silhouette. */\n"+
"  X._src['mode_boss_rush_0915']='assets/game/ui/modes_0915/boss_rush.png';\n"+
"  X._src['mode_time_attack_0915']='assets/game/ui/modes_0915/time_attack.png';\n"+
"  X._src['mode_lock_nexus_0915']='assets/game/ui/modes_0915/nexus_chains.webp';\n",'mode art registrations');

once("const WEAPONS=['MACHINE GUN','SPREAD FIRE','MISSILES','LASER','FLAMETHROWER','ICE ORB','LASER MIST'];\n",
"/* Boss Rush and Time Attack are account-level unlocks earned only by clearing the final\n"+
"   campaign stage. Their encounter routes arrive in ACH-14; keeping that readiness separate\n"+
"   prevents a newly revealed card from entering an unfinished runtime. */\n"+
"const BONUS_MODE_UNLOCK_KEY='bof_bonus_modes_v1';\n"+
"let bonusModesUnlocked=false;\n"+
"try{bonusModesUnlocked=localStorage.getItem(BONUS_MODE_UNLOCK_KEY)==='1';}catch(_bonusRead){}\n"+
"const BONUS_MODE_PLAYABLE=Object.freeze({bossrush:false,timeattack:false});\n"+
"function bonusModesAreUnlocked(){return !!bonusModesUnlocked;}\n"+
"function bonusModesUnlockFromCampaign(){\n"+
"  if(bonusModesUnlocked||run.mode!=='campaign'||run.stage!==CAMPAIGN_STAGES)return false;\n"+
"  bonusModesUnlocked=true;\n"+
"  try{localStorage.setItem(BONUS_MODE_UNLOCK_KEY,'1');}catch(_bonusWrite){}\n"+
"  return true;\n"+
"}\n"+
"const WEAPONS=['MACHINE GUN','SPREAD FIRE','MISSILES','LASER','FLAMETHROWER','ICE ORB','LASER MIST'];\n",'bonus-mode persistence');

once("function triggerVictory(){\n  achievementRunComplete();\n",
"function triggerVictory(){\n  bonusModesUnlockFromCampaign();\n  achievementRunComplete();\n",'victory unlock trigger');

const oldItems=`const MODE_ITEMS=[
  {name:'CAMPAIGN', sub:'WORLD MAP - STORY - REVISIT STAGES', mode:'campaign', open:true,  pill:'nms_campaign'},
  {name:'ARCADE',   sub:'STRAIGHT RUN - CLASSIC PROGRESSION', mode:'arcade',   open:true,  pill:'nms_arcade'},
  /* OPEN AS OF 0902f. The sub-line still reads TWO PILOTS because that is exactly what it is:
     the arcade run with a second seat. See the co-op block beside \`run2\` for why \`run.mode\` does
     NOT become 'coop'. */
  {name:'CO-OP',    sub:'TWO PILOTS',                         mode:'coop',     open:true,  pill:'nms_coop'},
  /* VERSUS IS GONE (Mike, 0902): "remove the vs. or versus button from the game entirely.
     were not doing a DM mode with this game as much as I would have liked to. That's a bof2
     idea." The nms_versus pill art stays registered and unused - deleting art is not what he
     asked for, and BOF2 is where this belongs. Do not re-add the row because the art exists. */
];`;
const newItems=`const MODE_ITEMS=[
  {name:'CAMPAIGN',    sub:'WORLD MAP - STORY - REVISIT STAGES', mode:'campaign',   open:true, pill:'nms_campaign'},
  {name:'ARCADE',      sub:'STRAIGHT RUN - CLASSIC PROGRESSION', mode:'arcade',     open:true, pill:'nms_arcade'},
  /* Co-op is the arcade run with a second seat; run.mode intentionally remains arcade. */
  {name:'CO-OP',       sub:'TWO PILOTS',                         mode:'coop',       open:true, pill:'nms_coop'},
  {name:'BOSS RUSH',   sub:'THE FURY GAUNTLET',                  mode:'bossrush',   open:true, pill:'mode_boss_rush_0915', crop:[0,78,2170,515], requiresFinalClear:true},
  {name:'TIME ATTACK', sub:'RACE EVERY SECOND',                  mode:'timeattack', open:true, pill:'mode_time_attack_0915',crop:[0,78,2170,515], requiresFinalClear:true},
  /* Versus remains intentionally absent. Its old art is retained for a possible sequel. */
];
function modeItemUnlocked(it){return !(it&&it.requiresFinalClear)||bonusModesAreUnlocked();}
function modeItemOpen(it){
  if(!it||!it.open||!modeItemUnlocked(it))return false;
  return !it.requiresFinalClear||!!BONUS_MODE_PLAYABLE[it.mode];
}`;
once(oldItems,newItems,'mode roster');

const drawStart='function drawModeSelect(dt){\n';
const helpers=`function modePanelPath(x,y,w,h){
  const b=Math.min(12,h*.24);
  ctx.beginPath();ctx.moveTo(x+b,y);ctx.lineTo(x+w-b,y);ctx.lineTo(x+w,y+b);
  ctx.lineTo(x+w,y+h-b);ctx.lineTo(x+w-b,y+h);ctx.lineTo(x+b,y+h);
  ctx.lineTo(x,y+h-b);ctx.lineTo(x,y+b);ctx.closePath();
}
function modePanelDraw(it,cx,cy,pw,locked){
  if(typeof XART==='undefined'||!it.pill||!XART.rdy(it.pill))return null;
  const im=XART.get(it.pill),crop=it.crop||null;
  const ar=crop?(crop[2]/crop[3]):((im.naturalWidth||1)/(im.naturalHeight||1));
  const ph=pw/ar,x=cx-pw/2,y=cy-ph/2;
  ctx.save();modePanelPath(x,y,pw,ph);ctx.clip();ctx.imageSmoothingEnabled=false;
  if(locked)ctx.filter='grayscale(1) brightness(.55)';
  if(crop)ctx.drawImage(im,crop[0],crop[1],crop[2],crop[3],x,y,pw,ph);
  else ctx.drawImage(im,x,y,pw,ph);
  ctx.restore();return{x,y,w:pw,h:ph,key:crop?null:it.pill};
}
function modeLockDraw(rect){
  if(!rect||typeof XART==='undefined'||!XART.rdy('mode_lock_nexus_0915'))return false;
  const im=XART.get('mode_lock_nexus_0915'),w=rect.w*1.02,h=w*((im.naturalHeight||614)/(im.naturalWidth||1100));
  ctx.save();modePanelPath(rect.x,rect.y,rect.w,rect.h);ctx.clip();ctx.imageSmoothingEnabled=false;
  ctx.drawImage(im,rect.x+(rect.w-w)/2,rect.y+(rect.h-h)/2,w,h);ctx.restore();return true;
}
function modeLockedDeny(it){
  drawModeSelect._deny={t:1.05,text:modeItemUnlocked(it)?'MODE DEVELOPMENT IN PROGRESS':'CLEAR CAMPAIGN TO UNLOCK'};
  const s=Audio&&Audio.SFX&&(Audio.SFX.blocked||Audio.SFX.alertDanger||Audio.SFX.dangerAlert||Audio.SFX.blip);
  if(s)s();
}
`+drawStart;
once(drawStart,helpers,'mode helpers');

const oldLoop=`  /* SPACING (drop 0801bu). Mike: "space them out vertically to be more neat and
     structured and organized, all menu buttons." Four pills on a 512 field: the
     block now sits centred with even air above and below instead of crowding the
     top third. */
  const y0=132, gap=98;
  for(let i=0;i<MODE_ITEMS.length;i++){
    const it=MODE_ITEMS[i], sel=(i===modeIndex), y=y0+i*gap;
    ctx.save();
    if(typeof XART!=='undefined' && it.pill && XART.rdy(it.pill)){
      const im=XART.get(it.pill), pw=sel?324:300, ph=pw*(im.naturalHeight/im.naturalWidth);
      // remember where the highlighted pill actually landed, so confirming it can
      // strobe THAT rect instead of the whole screen
      if(sel) drawModeSelect._selRect={x:VW/2-pw/2, y:y-ph/2, w:pw, h:ph, key:it.pill};
      if(!it.open) ctx.globalAlpha=0.4;                       // grayed = locked
      if(sel && it.open){ ctx.shadowColor='#ffd75a'; ctx.shadowBlur=16; }
      ctx.drawImage(im, VW/2-pw/2, y-ph/2, pw, ph);
      ctx.restore(); ctx.save();
      if(sel) menuSelMark(VW/2, y, pw/2, '#ff2a2a');   // same cursor, palette-swapped RED for this screen
      ctx.shadowBlur=0;
      if(!it.open){ ctx.globalAlpha=1; ctx.fillStyle='#ff5a5a'; ctx.font='bold 10px "BOFmil", monospace'; ctx.textAlign='center';
        ctx.fillText('LOCKED', VW/2, y+ph/2-2); }
      else { ctx.globalAlpha=1; ctx.fillStyle=sel?'#9fb0cd':'#6b7690'; ctx.font='8px "BOFmil", monospace'; ctx.textAlign='center';
        ctx.fillText(it.sub, VW/2, y+ph/2+4); }
    } else {
      // fallback: framed text rows
      ctx.globalAlpha=it.open?1:0.45;
      ctx.fillStyle=sel?'rgba(20,26,40,0.85)':'rgba(8,10,18,0.72)';
      ctx.fillRect(VW/2-150,y-26,300,52);
      ctx.strokeStyle=sel?'#ffd75a':'#3a4258'; ctx.lineWidth=sel?2:1; ctx.strokeRect(VW/2-150,y-26,300,52);
      ctx.textAlign='center';
      ctx.fillStyle=sel?menuSelWhite():'#dfe6f2'; ctx.font='bold 17px "BOFmil", monospace'; ctx.fillText(it.name,VW/2,y-2);
      if(sel) menuSelMark(VW/2, y, 150, '#ff2a2a');
      ctx.fillStyle=it.open?'#8fa0bd':'#7c5560'; ctx.font='9px "BOFmil", monospace';
      ctx.fillText(it.open?it.sub:'COMING SOON',VW/2,y+15);
    }
    ctx.restore();
  }`;
const newLoop=`  /* Five evenly spaced authored mode plates fit the 480x512 field without touching the hint bar. */
  const y0=92, gap=82;
  for(let i=0;i<MODE_ITEMS.length;i++){
    const it=MODE_ITEMS[i],sel=(i===modeIndex),y=y0+i*gap;
    const unlocked=modeItemUnlocked(it),open=modeItemOpen(it),pw=sel?292:270;
    ctx.save();if(sel&&open){ctx.shadowColor='#ffd75a';ctx.shadowBlur=16;}
    const rect=modePanelDraw(it,VW/2,y,pw,!unlocked);
    ctx.restore();
    if(rect){
      if(!unlocked)modeLockDraw(rect);
      if(sel)menuSelMark(VW/2,y,pw/2,'#ff2a2a');
      ctx.save();ctx.textAlign='center';ctx.font='8px "BOFmil", monospace';
      ctx.fillStyle=!unlocked?'#ff7b7b':(open?(sel?'#b9c9e8':'#8290aa'):'#d2a36a');
      ctx.fillText(!unlocked?'CLEAR CAMPAIGN TO UNLOCK':(open?it.sub:'MODE DEVELOPMENT IN PROGRESS'),VW/2,rect.y+rect.h+9);
      ctx.restore();
      if(sel)drawModeSelect._selRect=rect;
    }else{
      ctx.save();ctx.globalAlpha=unlocked?1:.55;ctx.fillStyle=sel?'rgba(20,26,40,.9)':'rgba(8,10,18,.78)';
      ctx.fillRect(VW/2-135,y-27,270,54);ctx.strokeStyle=sel?'#ffd75a':'#3a4258';ctx.strokeRect(VW/2-135,y-27,270,54);
      ctx.textAlign='center';ctx.fillStyle=sel?menuSelWhite():'#dfe6f2';ctx.font='bold 15px "BOFmil", monospace';ctx.fillText(it.name,VW/2,y-3);
      ctx.font='8px "BOFmil", monospace';ctx.fillStyle=unlocked?'#8fa0bd':'#ff7b7b';ctx.fillText(unlocked?it.sub:'CLEAR CAMPAIGN TO UNLOCK',VW/2,y+15);
      if(sel)menuSelMark(VW/2,y,135,'#ff2a2a');ctx.restore();
      if(sel)drawModeSelect._selRect={x:VW/2-135,y:y-27,w:270,h:54,key:null};
    }
  }
  if(drawModeSelect._deny&&drawModeSelect._deny.t>0){
    drawModeSelect._deny.t-=dt;ctx.save();ctx.textAlign='center';ctx.font='bold 9px "BOFmil", monospace';
    ctx.fillStyle='#ffeb7a';ctx.shadowColor='#ff2a2a';ctx.shadowBlur=8;ctx.fillText(drawModeSelect._deny.text,VW/2,478);ctx.restore();
  }`;
once(oldLoop,newLoop,'mode draw loop');

once("    if(it.open){\n      // flash white, THEN move on",
"    if(modeItemOpen(it)){\n      // flash white, THEN move on",'mode activation gate');
once("    else { if(Audio.SFX&&Audio.SFX.blip)Audio.SFX.blip(); }\n  };\n",
"    else modeLockedDeny(it);\n  };\n",'mode denial alert');

fs.writeFileSync(gamePath,game,'utf8');
if(game.includes('\r\n'))throw new Error('game line endings changed');

const include="require('./test_locked_modes_0915.cjs')(vm,ctxv,ok);\r\n\r\n";
const marker="console.log('\\n============================================');\r\n";
if(!originalTest.includes(include)){
  const count=originalTest.split(marker).length-1;
  if(count!==1)throw new Error('test marker expected once, got '+count);
  fs.writeFileSync(testPath,originalTest.replace(marker,include+marker),'utf8');
}
const finalTest=fs.readFileSync(testPath,'utf8');
if(/(^|[^\r])\n/.test(finalTest))throw new Error('test_fl.js line endings changed');
console.log('patched locked mode cards and campaign-clear gate');
