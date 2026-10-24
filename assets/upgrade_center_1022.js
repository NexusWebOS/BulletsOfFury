'use strict';
/* ==========================================================================================
   DECKER'S UPGRADE CENTER (Mike, 2026-10-22).

   "forge/loadout should allow you to enter - The Forge or Select your Loadout, our existing
    screens. But a player may have forgotten to upgrade a weapon, or wants to re-spec. This
    should be Decker's Upgrade Center. and be located on the map directly next to Fury HQ and
    we can travel to it too and select it to enter it."

   - A landmark island east of Fury HQ on the campaign map. UP from Stage 1 flies the jet to it
     (DOWN / LEFT / RIGHT / B fly back to Stage 1), a click on it does the same, and FIRE (or a
     second click) enters it.
   - Inside: Decker, and THE FORGE / SELECT YOUR LOADOUT / LEAVE. Both are the existing screens;
     each one comes back here when it closes, so a player can forge and then change the loadout.
   - The START menu's FORGE / LOADOUT row opens the same place.
   - The Forge keeps the stage's own upgrade and re-spec budget (forgeStart refills it on every
     open - the START menu note in start_menu_1022.js has the measurement).

   ART: the island is the authored 0930 northern hangar island (campaign_0930/northern_hq_island),
   retired from the map when Fury HQ moved onto its 1004f region. SpriteCook had 2 credits, so no
   new plate was generated; a dedicated one drops in by repointing UC22_ART.
   window.UC22_OFF=1 hides the landmark and puts the START row back on the direct Forge route.
   ========================================================================================== */
const UC22_ART='uc22_island';
XART._src[UC22_ART]='assets/game/shared/campaign/campaign_0930/northern_hq_island.png';
const UC22_GOLD='#ffd24a';
const UC22_ROWS=['THE FORGE','SELECT YOUR LOADOUT','RE-SPEC A WEAPON','LEAVE'];   // RE-SPEC: respec_1022.js
const UC22={pos:{x:880,y:300},size:330,focus:false,open:false,pending:false,frame:null,
            sel:0,t:0,md:false,mapMd:false,lift:0,msg:'',msgT:0};

function uc22Off(){ return typeof window!=='undefined' && !!window.UC22_OFF; }
function uc22Warm(){ try{ XART.rdy(UC22_ART); XART.rdy('pause_button_0915'); XART.rdy('dlg_window');
  XART.rdy('port_cf_decker_idle'); XART.rdy('port_cf_decker_happy'); }catch(_w){} }
/* the live campaign map, settled - never mid-boot, mid-zoom, mid-unlock or under a menu */
function uc22MapLive(){
  if(uc22Off()) return false;
  if(state!==GS.STAGESEL || run.mode!=='campaign' || !(typeof cmap2On==='function' && cmap2On())) return false;
  if(typeof campPauseIsCampaignScreen==='function' && !campPauseIsCampaignScreen()) return false;
  if(typeof campPause!=='undefined' && campPause) return false;
  if(sselBoot>0 || (typeof sselZoom!=='undefined' && sselZoom) || sselUnlockCine!=null) return false;
  if(typeof s9MapCine!=='undefined' && s9MapCine) return false;
  if(typeof riftReturn!=='undefined' && riftReturn) return false;
  if(window.sselCommitted) return false;
  if(typeof SM22!=='undefined' && SM22.open) return false;
  return true;
}
/* Mike's bonus rule: once Stage 9 is earned, only Stage 9 can be selected */
function uc22Reachable(){ return uc22MapLive() && !(campaign && campaign.bonusUnlocked) && !(typeof map4hXFocused==='function' && map4hXFocused()); }
/* the jet parks on the hangar's own runway */
function uc22Point(){ return {x:UC22.pos.x, y:UC22.pos.y-18}; }
function uc22At(mx,my){
  if(my<CM2_BAND_TOP || my>=CM2_BAND_BOT) return false;
  const q=cmap2ToScreen(UC22.pos.x,UC22.pos.y), w=UC22.size*cmap2.cam.z;
  return Math.abs(mx-q.x)<w*.42 && Math.abs(my-q.y)<w*.36;
}
function uc22Focus(){ UC22.focus=true; if(typeof MAP4E!=='undefined'){ MAP4E.focus=true; } try{ Audio.SFX.blip(); }catch(_b){} }
function uc22Leave(){
  UC22.focus=false; sselCursor=1;
  if(typeof MAP4E!=='undefined'){ MAP4E.focus=true; MAP4E.last=null; }
  try{ Audio.SFX.blip(); }catch(_b){}
}

/* ---------------- the landmark, drawn with the regions (after Fury HQ, before Stage 1) ---------------- */
const UC22_REGION=map4eRegion;
map4eRegion=function(k){
  const r=UC22_REGION.apply(this,arguments);
  if(k==='hq' && !uc22Off()) uc22DrawRegion();
  return r;
};
function uc22DrawRegion(){
  uc22Warm(); if(!XART.rdy(UC22_ART)) return;
  const m=Input.mouse||{}, hover=sselBoot===0 && m.active && uc22At(m.x,m.y);
  const want=(UC22.focus||hover)&&sselBoot===0?1:0;
  UC22.lift+=(want-UC22.lift)*.12;
  const im=XART.get(UC22_ART), s=UC22.size, w=s, h=s*im.height/im.width;
  const x=UC22.pos.x, y=UC22.pos.y+Math.sin(cmap2.t*.8+1.3)*3-6*UC22.lift;
  ctx.save(); ctx.imageSmoothingEnabled=false;
  /* the same soft ground shadow the regions carry: the plate's own silhouette, darkened */
  ctx.globalAlpha=.32-.08*UC22.lift; ctx.filter='brightness(0)';
  ctx.drawImage(im,x-w/2+8+4*UC22.lift,UC22.pos.y-h/2+18+10*UC22.lift,w,h);
  ctx.filter='none'; ctx.globalAlpha=1;
  ctx.drawImage(im,x-w/2,y-h/2,w,h);
  ctx.restore();
  /* the name, screen-sized at any zoom, the way the flags are */
  if(sselBoot===0){
    const z=Math.max(.05,cmap2.cam.z), th=(UC22.focus?11:9)/z;
    ctx.save(); ctx.globalAlpha=UC22.focus?1:.82;
    campText('UPGRADE CENTER',x,y-h*.46,th,UC22.focus?UC22_GOLD:'#e8dcb0');
    ctx.restore();
  }
}

/* ---------------- travel: the jet and the camera follow the landmark while it has the focus ---------------- */
const UC22_DEST=cf9Dest;
cf9Dest=function(){ return (UC22.focus && !sselUnlockCine) ? uc22Point() : UC22_DEST.apply(this,arguments); };
const UC22_SHIP=cf9ShipTick;
cf9ShipTick=function(dt){
  if(!(UC22.focus && !sselUnlockCine && sselShip)) return UC22_SHIP.apply(this,arguments);
  const sh=sselShip, dest=uc22Point(); sh.t+=dt;
  if(sh.cur!=='uc'){ sh.head=map4eShipHeading(sh.cur,'uc',dest.x-sh.x); if(Audio.SFX.mapMove) Audio.SFX.mapMove(); sh.cur='uc'; }
  if(!Number.isFinite(sh.head)) sh.head=0;
  sh.face=sh.head<0?-1:1; sh.tx=dest.x; sh.ty=dest.y;
  const dx=dest.x-sh.x, dy=dest.y-sh.y, d=Math.hypot(dx,dy), k=.07;
  sh.x+=dx*Math.min(1,dt*60*k); sh.y+=dy*Math.min(1,dt*60*k); sh.bank=0;
  if(sh.phase==='flyin'&&d<4) sh.phase='idle'; sh.moving=d>3; sh.trail-=dt;
  if(sh.moving&&sh.trail<=0){ sh.trail=.03; const ux=Math.sin(sh.head), uy=-Math.cos(sh.head);
    particles.push({x:sh.x-ux*17,y:sh.y-uy*17,vx:-ux*.35+rnd(-.2,.2),vy:-uy*.35+rnd(-.2,.2),
      life:rnd(.18,.36),t:0,r:rnd(1,2.2),color:d>90?'#ffd27a':'#8fd0ff'}); }
};
/* "directly next to Fury HQ": while the jet is parked here the camera frames the two together */
const UC22_CAM=cmap2CameraTick;
cmap2CameraTick=function(dt,cine,selected){
  const r=UC22_CAM.apply(this,arguments);
  if(UC22.focus && !cine && !uc22Off() && sselBoot===0 && !(typeof cmap2!=='undefined' && cmap2.focus==='bar')){
    const hq=cmap2World('hq'), u=UC22.pos, bandH=CM2_BAND_BOT-CM2_BAND_TOP;
    const z=Math.min(1.0,(VW-20)/(Math.abs(u.x-hq.x)+560),(bandH-10)/(Math.abs(u.y-hq.y)+470));
    /* its own eased camera, written over the close follow-camera: easing the shared one would settle
       half way between the two targets (measured z 1.13 against the 0.48 asked for) */
    const t={x:(hq.x+u.x)/2, y:(hq.y+u.y)/2-10, z}, e=1-Math.exp(-Math.max(0,dt)*3);
    if(!UC22.cam) UC22.cam={x:cmap2.cam.x,y:cmap2.cam.y,z:cmap2.cam.z};
    for(const k of ['x','y','z']) UC22.cam[k]+=(t[k]-UC22.cam[k])*e;
    Object.assign(cmap2.cam,UC22.cam);
  } else UC22.cam=null;
  return r;
};
/* north to the center, south back to Stage 1 - the hull never flies sideways up the coast */
const UC22_HEAD=map4eShipHeading;
map4eShipHeading=function(from,to,dx){
  if(to==='uc') return 0;
  if(from==='uc') return Math.PI;
  return UC22_HEAD.apply(this,arguments);
};

/* ---------------- map input: reach it, leave it, enter it ---------------- */
const UC22_INPUT=Rival24.mapInput;
Rival24.mapInput=function(){
  if(!uc22Reachable()) return UC22_INPUT.apply(this,arguments);
  if(typeof cmap2!=='undefined' && cmap2.focus==='bar') return UC22_INPUT.apply(this,arguments);
  if(typeof _selFlash!=='undefined' && _selFlash) return UC22_INPUT.apply(this,arguments);
  const m=Input.mouse||{}, click=!!m.down && !UC22.mapMd; UC22.mapMd=!!m.down;
  if(click && stateT>.4 && uc22At(m.x,m.y)){
    if(UC22.focus) uc22Enter(); else uc22Focus();
    return true;
  }
  if(UC22.focus){
    if(Input.menuDown()||Input.menuLeft()||Input.menuRight()){ uc22Leave(); return true; }
    Input.menuUp();
    if(stateT>.4 && Input.menuConfirm()) uc22Enter();
    return true;
  }
  if(sselCursor===1 && Input.menuUp()){ uc22Focus(); return true; }
  return UC22_INPUT.apply(this,arguments);
};
/* B on the landmark flies back to Stage 1; it is a move inside the map, so the game-mode lock lets it through */
const UC22_INSIDE=sm22BackInside;
sm22BackInside=function(){
  if(state===GS.STAGESEL && (UC22.open || (UC22.focus && !uc22Off()))) return true;
  return UC22_INSIDE.apply(this,arguments);
};
const UC22_CAMP=campaignMenuInputTick;
campaignMenuInputTick=function(){
  if(UC22.focus && uc22MapLive() && Input.menuBack()){ uc22Leave(); return true; }
  return UC22_CAMP.apply(this,arguments);
};
/* the card and the hint row say where the jet is */
const UC22_BRIEF=mapgBriefingDraw;
mapgBriefingDraw=function(info){
  if(UC22.focus && state===GS.STAGESEL && !uc22Off())
    info={key:'uc22',title:"DECKER'S UPGRADE CENTER",
          body:'FORGOT AN UPGRADE, OR WANT A RE-SPEC? THE FORGE AND YOUR LOADOUT ARE HERE.'};
  return UC22_BRIEF.call(this,info);
};
const UC22_HINT=drawHintBar;
drawHintBar=function(items){
  if(UC22.focus && state===GS.STAGESEL && !uc22Off() && Array.isArray(items))
    items=[['pad_dpad','STAGE'],['pad_a','ENTER'],['pad_b','BACK']];
  return UC22_HINT.call(this,items);
};

/* ---------------- inside ---------------- */
function uc22Enter(){
  try{ Audio.SFX.select&&Audio.SFX.select(); }catch(_s){}
  UC22.focus=true; UC22.pending=true;
}
/* opened on the frame after the map has been drawn, so the frozen picture behind is the map */
function uc22OpenNow(){
  const cv=document.getElementById('screen'), c=document.createElement('canvas');
  c.width=cv?cv.width:1; c.height=cv?cv.height:1;
  try{ if(cv) c.getContext('2d').drawImage(cv,0,0); }catch(_e){}
  UC22.frame=c; UC22.open=true; UC22.sel=0; UC22.t=0; UC22.msg=''; UC22.msgT=0; UC22.rs=null;
  UC22.md=!!(Input.mouse&&Input.mouse.down); uc22Warm(); Input.clearTaps();
}
function uc22Close(){ UC22.rs=null; UC22.open=false; UC22.frame=null; Input.clearTaps(); try{ Audio.SFX.blip(); }catch(_b){} }
/* each screen comes back to the map with the jet still parked here and Decker's menu up again */
function uc22Return(){
  if(typeof openStageSelect==='function') openStageSelect(run.stage,{}); else setState(GS.STAGESEL);
  UC22.focus=true; UC22.pending=true;
}
function uc22Choose(i){
  if(i===3){ uc22Close(); return; }
  if(i===2){ UC22.rs={sel:0,t0:UC22.t}; UC22.msg=''; UC22.msgT=0; Input.clearTaps(); try{ Audio.SFX.select&&Audio.SFX.select(); }catch(_s){} return; }
  try{ Audio.SFX.select&&Audio.SFX.select(); }catch(_s){}
  UC22.open=false; UC22.frame=null; Input.clearTaps();
  if(i===0){
    /* forgeStart refills the stage budget; put back what this stage had left */
    const combos=run.forgeCombos, respecs=run.forgeRespecs, shown=run._forgeShown;
    forgeStart(function(){ run._forgeShown=shown; uc22Return(); });
    run.forgeCombos=combos==null?0:combos; run.forgeRespecs=respecs==null?0:respecs;
  } else {
    loadoutStart(uc22Return);
  }
}
function uc22ButtonArt(cx,cy,w,h,sel){
  const im=(typeof xartPalette==='function')?xartPalette('pause_button_0915',UC22_GOLD):null;
  if(!im) return false;
  const r=PAUSE_BUTTON_RECT, cap=Math.min(r[3]*.65,r[2]/3), dc=Math.min(h*.65,w/3);
  ctx.save(); ctx.globalAlpha*=sel?1:.72;
  if(sel){ ctx.shadowColor=UC22_GOLD; ctx.shadowBlur=9; }
  ctx.drawImage(im,r[0],r[1],cap,r[3],cx-w/2,cy-h/2,dc,h);
  ctx.drawImage(im,r[0]+cap,r[1],r[2]-cap*2,r[3],cx-w/2+dc,cy-h/2,w-dc*2,h);
  ctx.drawImage(im,r[0]+r[2]-cap,r[1],cap,r[3],cx+w/2-dc,cy-h/2,dc,h);
  ctx.restore(); return true;
}
const UC22_LINE='FORGOT TO UPGRADE SOMETHING, PILOT? BRING IT TO MY BENCH. I CAN FORGE AN UPGRADE, '+
                'RE-SPEC A WEAPON OR SWAP YOUR LOADOUT BEFORE YOU HEAD OUT.';
function uc22Draw(dt){
  dt=Number.isFinite(dt)?dt:1/60; const P=UC22; P.t+=dt; if(P.msgT>0) P.msgT-=dt;
  const F=sm22Field();
  ctx.save(); ctx.setTransform(1,0,0,1,0,0);
  ctx.fillStyle='#000'; ctx.fillRect(0,0,F.W,F.H);
  if(P.frame){ ctx.save(); ctx.filter='brightness(.42)'; ctx.drawImage(P.frame,0,0); ctx.restore(); }
  ctx.restore();
  ctx.save(); ctx.setTransform(F.k,0,0,F.k,F.ox,F.oy);
  msgText("DECKER'S UPGRADE CENTER",VW/2,46,22,UC22_GOLD,0,1,.12);
  /* Decker at his bench */
  const px=24, py=72, pw=VW-48, ph=128;
  if(typeof drawPanel==='function') drawPanel('dlg_window','black',px,py,pw,ph);
  const typing=Math.floor(P.t*42)<UC22_LINE.length;
  const pk=(typeof pilotPortrait==='function')?pilotPortrait('decker',typing?'talk':'happy'):'port_cf_decker_idle';
  if(XART.rdy(pk)){ const im=XART.get(pk), s=96; ctx.save(); ctx.imageSmoothingEnabled=false; ctx.drawImage(im,px+14,py+16,s,s); ctx.restore(); }
  if(typeof msgDrawBlock==='function'){
    const prior=(typeof _msgFace!=='undefined')?_msgFace:null;
    try{ msgFaceUse('dialogue'); }catch(_f){}
    msgDrawBlock({text:'DECKER',budget:6,x:px+124,y:py+14,w:pw-140,h:16,maxH:12,minH:9,color:UC22_GOLD,align:'left',valign:'middle',lineMul:1.1});
    msgDrawBlock({text:UC22_LINE,budget:Math.floor(P.t*42),x:px+124,y:py+34,w:pw-142,h:ph-46,maxH:11,minH:8,color:'#f2ead2',align:'left',valign:'top',lineMul:1.3});
    try{ if(prior) msgFaceUse(prior); }catch(_f){}
  }
  /* what this stage still allows */
  const combos=Math.max(0,run.forgeCombos|0), respecs=Math.max(0,run.forgeRespecs|0);
  msgText('UPGRADES LEFT '+combos+'     RE-SPECS LEFT '+respecs,VW/2,py+ph+20,11,'#d8c890',0,1,.06);
  if(P.rs){ uc22RespecDraw(py+ph); ctx.restore(); return; }
  /* the choices */
  const m=Input.mouse||{}, w=Math.min(300,VW-96), h=34, gap=42, y0=py+ph+62;
  let clicked=-1;
  if(P.t>.2){ let ch=0; if(Input.menuDown()) ch=1; if(Input.menuUp()) ch=-1;
    if(ch){ P.sel=(P.sel+ch+UC22_ROWS.length)%UC22_ROWS.length; try{ Audio.SFX.blip(); }catch(_b){} } }
  for(let i=0;i<UC22_ROWS.length;i++){
    const k=clamp((P.t-i*.085)/.28,0,1); if(k<=0) continue;
    const y=y0+i*gap+(1-k)*(1-k)*60, sel=i===P.sel;
    ctx.save(); ctx.globalAlpha=k;
    if(!uc22ButtonArt(VW/2,y,w,h,sel)){
      octFill(VW/2-w/2,y-h/2,w,h,7,sel?'#3a2f10':'#1b1712');
      ctx.strokeStyle=sel?UC22_GOLD:'#5a4c2c'; ctx.lineWidth=sel?2:1; ctx.strokeRect(VW/2-w/2+4,y-h/2+3,w-8,h-6);
    }
    campText(UC22_ROWS[i],VW/2,y+(typeof PAUSE_LABEL_DY==='number'?PAUSE_LABEL_DY:-2),12,sel?'#fff4d2':'#c2b48c');
    if(sel && typeof menuSelMark==='function') menuSelMark(VW/2,y,w/2,'yellow');
    ctx.restore();
    const mx=sm22MouseX(), my=sm22MouseY();
    if(k===1 && m.inside && Math.abs(mx-VW/2)<=w/2 && Math.abs(my-y)<h/2){
      if(Input.consumeMouseMoved()) P.sel=i;
      if(m.down && !P.md && P.t>.6) clicked=i;
    }
  }
  P.md=!!m.down;
  ctx.restore();
  if(Input.menuBack() || sm22StartTap()){ uc22Close(); return; }
  if(clicked>=0){ P.sel=clicked; uc22Choose(clicked); return; }
  if(P.t>.6 && Input.menuConfirm()) uc22Choose(P.sel);
}

/* RE-SPEC A WEAPON (Mike, 2026-10-22: "the option to actually re-spec ... in this new menu during
   the map"). Every loadout weapon and every weapon carrying a forged upgrade, LEFT / RIGHT to pick,
   FIRE once to arm and again to re-spec (respecPress, respec_1022.js), B back to Decker's rows. */
function uc22RespecWeapons(){
  const out=((run&&run.loadout&&run.loadout.length)?run.loadout:(typeof forgeLoadoutSync==='function'?forgeLoadoutSync():[])).slice();
  for(const k of Object.keys((run&&run.forgeForms)||{})){ const w=+k; if(out.indexOf(w)<0&&Object.keys(run.forgeForms[k]||{}).length) out.push(w); }
  return out;
}
function uc22RespecDraw(top){
  const P=UC22, R=P.rs, list=uc22RespecWeapons(), m=Input.mouse||{}, mx=sm22MouseX(), my=sm22MouseY();
  R.sel=clamp(R.sel|0,0,Math.max(0,list.length-1));
  const n=list.length, pitch=Math.min(66,(VW-60)/Math.max(1,n)), ih=40, iy=top+64, x0=VW/2-pitch*(n-1)/2;
  let clicked=-1, pressBtn=false;
  const click=m.down&&!P.md&&P.t-R.t0>.3;
  for(let i=0;i<n;i++){
    const w=list[i], cx=x0+i*pitch, key=(typeof forgeSlotKey==='function')?forgeSlotKey(w):null, sel=i===R.sel;
    const has=typeof respecInfo==='function'&&respecInfo(w).forms.length>0;
    if(key) XART.rdy(key);
    ctx.save(); ctx.fillStyle=sel?'#2a2416':'#14141c'; ctx.globalAlpha=.88; ctx.fillRect(cx-pitch*.46,iy-ih*.62,pitch*.92,ih*1.24); ctx.restore();
    if(key&&typeof forgeIconFit==='function') forgeIconFit(key,cx,iy,ih,0,has?1:.42);
    if(sel){ ctx.save(); ctx.globalAlpha=.7+.3*Math.sin(P.t*9); ctx.strokeStyle=UC22_GOLD; ctx.lineWidth=2;
      ctx.strokeRect(cx-pitch*.46,iy-ih*.62,pitch*.92,ih*1.24); ctx.restore(); }
    if(click&&Math.abs(mx-cx)<=pitch*.46&&Math.abs(my-iy)<=ih*.62) clicked=i;
  }
  const w=list[R.sel], I=(w!=null&&typeof respecInfo==='function')?respecInfo(w):null;
  if(w!=null){
    msgText((typeof respecLabel==='function')?respecLabel(w):WEAPONS[w],VW/2,iy+44,13,UC22_GOLD,0,1,.08);
    const line=I&&I.forms.length?'FORGED  '+I.names.join(' + '):'BASE FORM  -  NOTHING TO RE-SPEC';
    msgText(line,VW/2,iy+64,10,I&&I.forms.length?'#9fd6ff':'#8a96a8',0,1,.05);
  } else msgText('NO WEAPONS YET',VW/2,iy+44,12,'#8a96a8',0,1,.06);
  const armed=w!=null&&typeof rs22Armed==='function'&&rs22Armed(R,w,P.t), by=iy+104, bw=Math.min(260,VW-120), bh=34;
  uc22ButtonArt(VW/2,by,bw,bh,true);
  campText(armed?'CONFIRM RE-SPEC':'RE-SPEC',VW/2,by+(typeof PAUSE_LABEL_DY==='number'?PAUSE_LABEL_DY:-2),12,armed?'#ff6a52':'#fff4d2');
  if(armed){ ctx.save(); ctx.globalAlpha=.6+.4*Math.sin(P.t*14); ctx.strokeStyle='#ff4a3a'; ctx.lineWidth=2; ctx.strokeRect(VW/2-bw/2+2,by-bh/2+1,bw-4,bh-2); ctx.restore(); }
  if(click&&Math.abs(mx-VW/2)<=bw/2&&Math.abs(my-by)<bh/2) pressBtn=true;
  if(P.msgT>0) msgText(P.msg,VW/2,by+34,10,'#ffffff',0,1,.05);
  P.md=!!m.down;
  if(P.t-R.t0<.25) return;
  const mL=Input.menuLeft(), mR=Input.menuRight();
  if(Input.menuBack()){ P.rs=null; P.sel=2; try{ Audio.SFX.blip(); }catch(_b){} return; }
  if(sm22StartTap()){ uc22Close(); return; }
  if(n&&(mL||mR)){ R.sel=(R.sel+(mL?-1:1)+n)%n; R._rsArm=null; try{ Audio.SFX.blip(); }catch(_b){} }
  if(clicked>=0&&clicked!==R.sel){ R.sel=clicked; R._rsArm=null; try{ Audio.SFX.blip(); }catch(_b){} return; }
  if(pressBtn||clicked===R.sel||Input.menuConfirm()){
    const q=respecPress(R,w,P.t); P.msg=q.msg; P.msgT=q.r==='armed'?RS22_ARM_T:2.6;
    try{ const s=rs22SfxFor(q.r); Audio.SFX[s]&&Audio.SFX[s](); }catch(_s){}
  }
}

const UC22_SCENE=drawScene;
drawScene=function(dt){
  if(UC22.open){
    if(state!==GS.STAGESEL || uc22Off()){ UC22.open=false; UC22.frame=null; return UC22_SCENE.apply(this,arguments); }
    if(typeof window!=='undefined') window.__bofFrames=(window.__bofFrames|0)+1;
    return uc22Draw(dt);
  }
  if(state!==GS.STAGESEL && UC22.focus && state!==GS.FORGE && state!==GS.LOADOUT &&
     state!==GS.FORGING && state!==GS.FORGED){ UC22.focus=false; UC22.pending=false; }   // left the map some other way
  const r=UC22_SCENE.apply(this,arguments);
  if(UC22.pending && uc22MapLive()){ UC22.pending=false; uc22OpenNow(); }
  return r;
};
const UC22_FOOT=menuControlFooter;
menuControlFooter=function(){
  if(UC22.open){
    const F=sm22Field();
    ctx.save(); ctx.setTransform(F.k,0,0,F.k,F.ox,F.oy);
    ctx.fillStyle='rgba(0,0,0,.88)'; ctx.fillRect(-F.ox/F.k,VH-34,F.W/F.k,34+F.oy/F.k);
    controlHintRow(UC22.rs?[['pad_dpad','WEAPON'],['pad_a','RE-SPEC'],['pad_b','BACK']]:[['pad_dpad','CHOOSE'],['pad_a','SELECT'],['pad_b','LEAVE']]);
    ctx.restore(); return;
  }
  return UC22_FOOT.apply(this,arguments);
};

/* the START menu's FORGE / LOADOUT row is this place too */
const UC22_SM22FL=sm22ForgeLoadout;
sm22ForgeLoadout=function(){
  if(uc22Off()) return UC22_SM22FL.apply(this,arguments);
  UC22.focus=true; UC22.pending=true;
};
if(typeof window!=='undefined'){ window.UC22=UC22; window.uc22Enter=uc22Enter; }
uc22Warm();
