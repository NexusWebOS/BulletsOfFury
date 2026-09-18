/* ============================================================
   0917c - POWERS GAINED, the FURIOUS coin, the two bombs and the score bullets (Mike)

   "Powers Gained should have large boxes for the Element or Power upgrade we gained and have its own
    screen generated, and do not display what we can make with it. The weapons gained screen should be
    here when we unlock fire orb, ice freeze, thermofreeze ball, lightning orb, etc."
   "Furious Points = Needs our own currency graphic."
   "a 'Fury' Bomb which is our Bomb that blows up everything on screen when we get it. A 'Timed' Bomb
    ... acts like a thermal detonator that with your ship glowing goes beep...beep...beep.beep.beep and
    then does a cool blow up wave effect across the screen that overlays like an arcade effect and
    destroys everything including boxes and pills."
   "Score Point graphics that can be bonus pickups when we kill enemies. Im thinking bullets with #'s"

   Art: SpriteCook, assets/game/ui/forge_0917b/powers_bays.png (the Forge family, 477:266) and
   assets/game/ui/pickups_0917b/ (coin, fury bomb, timed bomb, four score bullets).
   ============================================================ */

/* ---- THE FURIOUS COIN ------------------------------------------------------------------------- */
function fpCoin(cx,cy,h,alpha){
  if(typeof XART==='undefined' || !XART.rdy('fury_coin_0917c')) return false;
  const im=XART.get('fury_coin_0917c');
  ctx.save(); ctx.globalAlpha*= (alpha==null?1:alpha); ctx.imageSmoothingEnabled=false;
  ctx.drawImage(im,cx-h/2,cy-h/2,h,h); ctx.restore(); return true;
}
/* "pre [coin] amt" set as ONE centred group - the coin is a glyph in the line, not a badge beside it */
function stageTextCoin(art,pre,amt,cx,cy,h,col,tintA,alpha,sp,amtCol){
  if(!art || typeof stageText!=='function') return;
  const coin=h*1.35, gap=h*0.32;
  const wp=pre?stageWidth(art,pre,h,sp):0, wa=stageWidth(art,amt,h,sp);
  const tot=wp+(pre?gap:0)+coin+gap+wa;
  let x=cx-tot/2;
  if(pre){ stageText(art,pre,x+wp/2,cy,h,col,tintA,alpha,sp); x+=wp+gap; }
  if(!fpCoin(x+coin/2,cy,coin,alpha)) stageText(art,'FP',x+coin/2,cy,h*0.8,'#ffd24a',0.9,alpha,sp);
  x+=coin+gap;
  stageText(art,amt,x+wa/2,cy,h,amtCol||col,tintA,alpha,sp);
}

/* ---- POWERS GAINED: its own screen (GS.POWERS) ------------------------------------------------ */
const POWERS_PLATE={
  title:[0.2129,0.0586,0.5741,0.1081],
  bays:[[0.1228,0.2982,0.1773,0.3099],[0.4113,0.3008,0.1781,0.3086],[0.6999,0.2982,0.1788,0.3099]],
  strips:[[0.0879,0.7109,0.2485,0.0755],[0.3750,0.7135,0.2500,0.0729],[0.6642,0.7109,0.2485,0.0755]],
  msg:[0.2885,0.8385,0.4230,0.0703]
};
/* one bay per ELEMENT, never per weapon - "do not display what we can make with it" */
function powersGained(){
  const C=(run && run._stageCombos) || [], out=[];
  for(const c of C) if(INFUSIONS[c.elem] && out.indexOf(c.elem)<0) out.push(c.elem);
  return out.slice(0,3);
}
function powersVisible(){ return powersGained().length>0; }
let powersScr=null;
function powersStart(onDone){
  powersScr={onDone:onDone||null, t:0, elems:powersGained(), md:!!(Input&&Input.mouse&&Input.mouse.down), popped:{}};
  try{ XART.rdy('powers_bays_0917c'); powersScr.elems.forEach(function(e){ XART.rdy('inf_'+e); }); fsx('life'); }catch(_p){ }
  setState(GS.POWERS);
}
function drawPowers(dt){
  const PS=powersScr;
  const W=(typeof cutsceneViewWidth==='function')?cutsceneViewWidth():VW, H=VH;
  ctx.fillStyle='#000'; ctx.fillRect(0,0,W,H);
  if(!PS){ setState(GS.TITLE); return; }
  PS.t+=dt; const t=PS.t;
  const art=(typeof curFontArt==='function')?curFontArt():null;
  const A=function(d){ return Math.max(0,Math.min(1,(t-d)/0.3)); };
  const plate=XART.rdy('powers_bays_0917c')?XART.get('powers_bays_0917c'):null;
  ctx.save(); ctx.globalAlpha=Math.min(1,t/0.4);
  if(plate){ ctx.imageSmoothingEnabled=false; ctx.drawImage(plate,0,0,W,H); } else { ctx.fillStyle='#161a22'; ctx.fillRect(0,0,W,H); }
  ctx.restore();
  const P=POWERS_PLATE, n=PS.elems.length;
  /* one power sits in the MIDDLE bay, two in the outer pair, three fill the row */
  const slots=n===1?[1]:(n===2?[0,2]:[0,1,2]);
  if(art){
    const T=frc(P.title,W,H);
    stageText(art,'POWERS GAINED',T[0]+T[2]/2,T[1]+T[3]/2,Math.min(T[3]*0.60,(typeof stageFitH==='function')?stageFitH(art,'POWERS GAINED',T[2]*0.9,T[3]*0.6,10,0.08):T[3]*0.5),'#ffd24a',0.9,A(0.1),0.08);
  }
  for(let b=0;b<3;b++){
    const r=frc(P.bays[b],W,H), k=slots.indexOf(b);
    if(k<0){ ctx.save(); ctx.globalAlpha=0.55*A(0.2); ctx.fillStyle='#000'; ctx.fillRect(r[0],r[1],r[2],r[3]); ctx.restore(); continue; }
    const e=PS.elems[k], I=INFUSIONS[e], d=0.45+k*0.35, a=A(d);
    if(a<=0) continue;
    if(!PS.popped[e]){ PS.popped[e]=1; fsx('powerup'); }
    const cx=r[0]+r[2]/2, cy=r[1]+r[3]/2, since=t-d, pop=1+0.35*Math.max(0,1-since/0.25);
    /* the element's own light behind it */
    ctx.save(); ctx.globalCompositeOperation='lighter'; ctx.globalAlpha=a*(0.30+0.14*Math.sin(t*4+k));
    const g=ctx.createRadialGradient(cx,cy,2,cx,cy,r[2]*0.62); g.addColorStop(0,I.glow); g.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle=g; ctx.fillRect(r[0],r[1],r[2],r[3]); ctx.restore();
    if(since<0.12){ ctx.save(); ctx.globalAlpha=(1-since/0.12)*0.8; ctx.fillStyle='#ffffff'; ctx.fillRect(r[0],r[1],r[2],r[3]); ctx.restore(); }
    forgeIconFit('inf_'+e,cx,cy,r[3]*0.80*pop,0,a);
    if(art){ const s=frc(P.strips[b],W,H), nm=I.name;
      stageText(art,nm,s[0]+s[2]/2,s[1]+s[3]/2,Math.min(s[3]*0.56,(typeof stageFitH==='function')?stageFitH(art,nm,s[2]*0.86,s[3]*0.56,8,0.06):s[3]*0.5),I.body,0.85,a,0.06); }
  }
  if(art){
    const M=frc(P.msg,W,H), msg=n>1?'NEW POWERS - TAKE THEM TO THE FORGE':'A NEW POWER - TAKE IT TO THE FORGE';
    stageText(art,msg,M[0]+M[2]/2,M[1]+M[3]/2,Math.min(M[3]*0.46,(typeof stageFitH==='function')?stageFitH(art,msg,M[2]*0.92,M[3]*0.46,7,0.06):11),'#9fd6ff',0.85,A(0.9),0.06);
  }
  const ready=t>0.45+n*0.35+0.3;
  if(ready && Math.floor(t*2)%2) controlHintRow([['pad_a','CONTINUE']],H*0.968,W/2,W-24);
  const fire=(keybind.fire||[]).filter(function(k){ return !/^mouse/.test(k); }).some(function(k){ return Input.tap(k); });
  const mS=(Input.menuStart?Input.menuStart():false);
  const click=Input.mouse.down&&!PS.md; PS.md=!!Input.mouse.down;
  if(ready && (fire||click||mS||Input.tap('enter'))){
    Input.mouse.down=false; fsx('blip');
    const done=PS.onDone; powersScr=null;
    if(done) done(); else setState(GS.TITLE);
  }
}

/* ---- THE BONUS PICKUPS: score bullets, the Fury Bomb, the Timed Bomb --------------------------- */
const SCORE_CHIP_P=0.12, FURY_BOMB_P=0.012, TIME_BOMB_P=0.012;
const SCORE_CHIP_VALS=[[100,0.55],[250,0.28],[500,0.13],[1000,0.04]];
function scoreChipRoll(){ let r=Math.random(); for(const v of SCORE_CHIP_VALS){ if(r<v[1]) return v[0]; r-=v[1]; } return 100; }
/* rolled from killDrop, the ONE kill-drop funnel, before its own gates - so a score bullet never
   competes with ammo, shield or life for the same 18% */
function bonusDrop(e){
  if(!e || !e.dropOk || typeof powerups==='undefined') return null;
  const m=(DIFF&&DIFF.dropMul)||1;
  let kind=null, extra={};
  if(Math.random()<SCORE_CHIP_P*m){ kind='scorechip'; extra={val:scoreChipRoll(), w:18, h:30}; }
  else if(Math.random()<FURY_BOMB_P*m) kind='furybomb';
  else if(Math.random()<TIME_BOMB_P*m) kind='timebomb';
  if(!kind) return null;
  const p=Object.assign({x:e.x, y:e.y, vy:0.9, t:0, kind:kind, w:24, h:24, bob:rnd(0,TAU)}, extra);
  powerups.push(p);
  try{ if(typeof stageStats!=='undefined' && stageStats.pickupsSeen!=null) stageStats.pickupsSeen++; }catch(_b){ }
  try{ XART.rdy(kind==='scorechip'?('score_bullet_'+p.val):(kind==='furybomb'?'fury_bomb_0917c':'timed_bomb_0917c')); }catch(_w){ }
  return p;
}
/* drawn from drawPowerups; true when it drew */
function bonusPickupDraw(p,yb){
  let key=null, h=30;
  if(p.kind==='scorechip'){ key='score_bullet_'+(p.val|0); h=46; }
  else if(p.kind==='furybomb'){ key='fury_bomb_0917c'; h=46; }
  else if(p.kind==='timebomb'){ key='timed_bomb_0917c'; h=44; }
  else return false;
  const bob=Math.sin((p.bob||0)+performance.now()/300)*2.4;
  ctx.save(); ctx.translate(p.x, yb+bob);
  /* a cheap pulsing glow - one additive disc, never shadowBlur (0916ab: that was the space stages' whole cost) */
  const glow=p.kind==='scorechip'?({100:'#d08a4a',250:'#dfe8ff',500:'#ffd24a',1000:'#3fe3ff'}[p.val|0]||'#ffd24a'):(p.kind==='furybomb'?'#ff4a1a':'#ff2a2a');
  ctx.globalCompositeOperation='lighter'; ctx.globalAlpha=0.30+0.18*Math.sin(performance.now()/120);
  ctx.fillStyle=glow; ctx.beginPath(); ctx.arc(0,0,h*0.62,0,TAU); ctx.fill();
  ctx.globalCompositeOperation='source-over'; ctx.globalAlpha=1;
  if(XART.rdy(key)){ const im=XART.get(key), w=h*((im.naturalWidth||im.width)/(im.naturalHeight||im.height)); ctx.imageSmoothingEnabled=false; ctx.drawImage(im,-w/2,-h/2,w,h); }
  else { ctx.fillStyle=glow; ctx.fillRect(-8,-12,16,24); }
  ctx.restore();
  return true;
}
/* applyPowerup's arm for the three; returns true when it handled the pickup */
function bonusPickupApply(p){
  if(p.kind==='scorechip'){
    const v=p.val|0; run.score=(run.score|0)+v-PICKUP_SCORE;      /* applyPowerup already paid PICKUP_SCORE: the bullet is worth its NUMBER */
    floatText(p.x,p.y-10,'+'+v,{100:'#e0a060',250:'#e8f0ff',500:'#ffd24a',1000:'#7ff0ff'}[v]||'#ffd24a');
    fsx('select')||fsx('blip');
    return true;
  }
  if(p.kind==='furybomb'){ furyBombDetonate(); return true; }
  if(p.kind==='timebomb'){ timeBombArm(); return true; }
  return false;
}

/* ---- THE BOMBS --------------------------------------------------------------------------------- */
const FURY_BOMB_BOSS_FRAC=0.10, TIME_BOMB_BOSS_FRAC=0.14, TIME_BOMB_FUSE=3.4, TIME_BOMB_WAVE_SPD=560;
let bombFx=null, timeBomb=null;
function bombOnScreen(x,y,pad){ pad=pad||24; return x>camLeftX()-pad && x<camRightX()+pad && y>-pad && y<VH+pad; }
function bombKill(e){
  if(!e || e.dead || e._dyingT!=null) return false;
  try{ explode(e.x,e.y,Math.max(18,(e.w||24)*0.9),'red'); }catch(_x){ }
  try{ killEnemy(e); }catch(_k){ e.dead=true; }
  return true;
}
/* ⚠ NEVER A ONE-SHOT ON A BOSS. A bomb that deletes a boss would skip every phase the fight was built
   around (and the no-one-shot rule, ENG-05). It takes a fixed SHARE of the bar through the ordinary hit
   path, so barriers, shields and part routers all still get their say. */
function bombHitBosses(frac){
  try{ if(typeof boss!=='undefined' && boss && bossActive && !boss.dead && typeof hitBoss==='function'){
    window._lastHitX=boss.x; window._lastHitY=boss.y; hitBoss(Math.max(1,Math.round((boss.maxhp||boss.hp||100)*frac))); } }catch(_b){ }
  try{ if(typeof subBoss!=='undefined' && subBoss && subBossActive && !subBoss.dead && typeof hitSubBoss==='function')
    hitSubBoss(Math.max(1,Math.round((subBoss.maxhp||subBoss.hp||100)*frac*1.5))); }catch(_s){ }
}
function furyBombDetonate(){
  let n=0;
  for(const e of enemies.slice()) if(bombOnScreen(e.x,e.y) && bombKill(e)) n++;
  for(const b of eBullets) b.dead=true;
  bombHitBosses(FURY_BOMB_BOSS_FRAC);
  shake=Math.max(shake,14); bombFlash=Math.max(bombFlash,0.75);
  bombFx={kind:'fury', t:0, x:player.x, y:player.y, n:n};
  fsx('explodeBig')||fsx('boom')||fsx('explosion');
  return n;
}
function timeBombArm(){
  timeBomb={t:0, next:0, beeps:0, flash:0};
  if(typeof arcadeBanner==='function') arcadeBanner('TIMED BOMB ARMED','#ff5a3a');
}
function timeBombBlow(){
  bombFx={kind:'time', t:0, x:player.x, y:player.y, r:0, bossHit:false, n:0};
  shake=Math.max(shake,16); bombFlash=Math.max(bombFlash,0.5);
  fsx('explodeBig')||fsx('boom')||fsx('explosion');
}
/* score bullets DRIFT to the ship once it is close - the arcade courtesy that stops a 1000 slipping past a
   pilot who was busy dodging. Short range, and only the bullets: a bomb is still a deliberate grab. */
const SCORE_MAGNET_R=96, SCORE_MAGNET_SPD=3.2;
function scoreMagnetTick(){
  if(typeof player==='undefined' || !player || player.dead) return;
  for(const p of powerups){
    if(p.dead || p.kind!=='scorechip') continue;
    const dx=player.x-p.x, dy=player.y-p.y, d=Math.hypot(dx,dy);
    if(d>1 && d<SCORE_MAGNET_R){ const sp=SCORE_MAGNET_SPD*(1+(SCORE_MAGNET_R-d)/SCORE_MAGNET_R); p.x+=dx/d*sp; p.y+=dy/d*sp; }
  }
}
function bombTick(dt){
  scoreMagnetTick();
  if(timeBomb){
    const B=timeBomb; B.t+=dt;
    const k=Math.min(1,B.t/TIME_BOMB_FUSE);
    /* beep... beep... beep.. beep.beep.beep - each gap shorter than the last, on the game's own clock */
    if(B.t>=B.next && B.t<TIME_BOMB_FUSE){ B.beeps++; B.flash=1; fsx('retinaLockBeep')||fsx('blip'); B.next=B.t+(0.55*Math.pow(1-k,1.6)+0.055); }
    B.flash=Math.max(0,B.flash-dt*7);
    if(B.t>=TIME_BOMB_FUSE){ timeBomb=null; timeBombBlow(); }
  }
  if(bombFx){
    const F=bombFx; F.t+=dt;
    if(F.kind==='time'){
      F.r+=TIME_BOMB_WAVE_SPD*dt;
      /* the wave takes what it REACHES, not the whole screen at once - that is what makes it a wave */
      for(const e of enemies.slice()){ if(bombOnScreen(e.x,e.y) && Math.hypot(e.x-F.x,e.y-F.y)<=F.r && bombKill(e)) F.n++; }
      for(const b of eBullets){ if(!b.dead && Math.hypot(b.x-F.x,b.y-F.y)<=F.r) b.dead=true; }
      /* "destroys everything including boxes and pills": the supply crates and capsules break OPEN */
      for(const p of powerups){
        if(p.dead || !(p.kind==='crate'||p.kind==='capsule'||p.kind==='scrate'||p.kind==='mcrate'||p.kind==='hqspacebox')) continue;
        if(Math.hypot(p.x-F.x,p.y-F.y)<=F.r){ p.hp=0; p.dead=true; try{ breakContainer(p); }catch(_c){ } }
      }
      if(!F.bossHit){ const bb=(typeof boss!=='undefined'&&boss&&bossActive&&!boss.dead)?boss:((typeof subBoss!=='undefined'&&subBoss&&subBossActive&&!subBoss.dead)?subBoss:null);
        if(bb && Math.hypot(bb.x-F.x,(bb._drawY!=null?bb._drawY:bb.y)-F.y)<=F.r+(bb.w||100)*0.4){ F.bossHit=true; bombHitBosses(TIME_BOMB_BOSS_FRAC); } }
      if(F.t>2.4) bombFx=null;
    } else if(F.t>1.1) bombFx=null;
  }
}
function bombReset(){ bombFx=null; timeBomb=null; }
/* screen space - called at the tail of drawWorld, after its camera is undone */
function bombWorldToScreen(x,y){ const z=(typeof viewZoom==='function')?viewZoom():1; return [(x-camLeftX())*z, y*z+VH*(1-z)]; }
function bombFxDraw(){
  const art=(typeof curFontArt==='function')?curFontArt():null;
  if(timeBomb && typeof player!=='undefined' && player){
    const B=timeBomb, s=bombWorldToScreen(player.x,player.y), k=Math.min(1,B.t/TIME_BOMB_FUSE);
    ctx.save(); ctx.globalCompositeOperation='lighter';
    /* the SHIP glows: a hot core that swells with the fuse and flares white on every beep, plus a ring that snaps out */
    const R=46+B.flash*26+k*22;
    ctx.globalAlpha=0.45+0.5*B.flash+0.25*k;
    const g=ctx.createRadialGradient(s[0],s[1],2,s[0],s[1],R); g.addColorStop(0,'#ffffff'); g.addColorStop(0.30,'#ff5a1a'); g.addColorStop(0.65,'rgba(255,40,20,0.45)'); g.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle=g; ctx.beginPath(); ctx.arc(s[0],s[1],R,0,TAU); ctx.fill();
    if(B.flash>0){ ctx.globalAlpha=B.flash; ctx.strokeStyle='#ffffff'; ctx.lineWidth=3; ctx.beginPath(); ctx.arc(s[0],s[1],24+(1-B.flash)*40,0,TAU); ctx.stroke(); }
    ctx.restore();
    const left=Math.max(0,TIME_BOMB_FUSE-B.t), txt=left.toFixed(1);
    if(art) stageText(art,txt,s[0],s[1]-38,12,B.flash>0.4?'#ffffff':'#ff5a3a',0.9,1,0.06);
  }
  if(!bombFx) return;
  const F=bombFx, W=VW, H=VH;
  const cyc=['#ff2a6a','#ffd24a','#2ad6ff','#ffffff'][Math.floor(F.t*18)%4];
  if(F.kind==='time'){
    const s=bombWorldToScreen(F.x,F.y);
    /* the ring: three stepped bands, arcade-bright, on 'lighter' */
    ctx.save(); ctx.globalCompositeOperation='lighter';
    [[22,'#ff3a1a',0.55],[10,'#ffd24a',0.8],[4,'#ffffff',1]].forEach(function(L){
      ctx.globalAlpha=L[2]*Math.max(0,1-F.t/2.4); ctx.strokeStyle=L[1]; ctx.lineWidth=L[0];
      ctx.beginPath(); ctx.arc(s[0],s[1],Math.max(1,F.r),0,TAU); ctx.stroke(); });
    ctx.restore();
  }
  /* THE ARCADE OVERLAY: a palette flash cycling at 18 Hz and scanline bands rolling down the glass */
  const fade=Math.max(0,1-F.t/(F.kind==='time'?1.6:1.0));
  if(fade>0){
    ctx.save(); ctx.globalAlpha=0.20*fade; ctx.fillStyle=cyc; ctx.fillRect(0,0,W,H);
    ctx.globalAlpha=0.35*fade; ctx.fillStyle='#000';
    const off=Math.floor(F.t*240)%8; for(let y=off;y<H;y+=8) ctx.fillRect(0,y,W,3);
    ctx.restore();
    if(art){ const word=F.kind==='time'?'KA-BOOM!':'FURY BOMB!', sc=1+0.5*Math.max(0,1-F.t/0.18);
      stageText(art,word,W/2,H*0.40,Math.min(40,(typeof stageFitH==='function')?stageFitH(art,word,W*0.8,40,14,0.08):30)*sc,cyc,0.9,fade,0.08); }
  }
}
