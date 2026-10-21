"use strict";
/* October 11 menu layout. Input/selection remains owned by drawPilot. */
const PT11_UI={card:null};
for(const name of ['emergence','contact'])XART._src['pt11_mystery_'+name]='assets/game/shared/cinematics/playthrough_1011/mystery-'+name+'.webp';
function pt11PilotCard(P,PX,PY,PW,PH,spin,locked){
 const wide=PW>560,pad=12,bodyW=PW*(wide?.28:.38),shipW=wide?PW*.29:PW-bodyW-pad*2;
 const by=PY+32,bh=PH-44,bx=PX+pad,sx=bx+bodyW+pad;
 const shipH=wide?bh*.82:Math.min(bh*.39,190),shipY=by+shipH/2;
 const infoX=wide?sx+shipW+pad:sx,infoY=wide?by:by+shipH+10;
 const infoW=PX+PW-pad-infoX,infoH=PY+PH-pad-infoY;
 psPanelBox(PX,PY,PW,PH,P.tint,true);
 const launching=pilotPending!=null;
 if(locked){pcFontLeft('LOCKED',bx+8,by+bh*.42,16,'#dce2ea',1);pcFontLeft('PASSWORD REQUIRED',infoX,infoY+32,10,'#ffe98a',1);return;}
 const body=psBodyKey(P.key);psBlitFit(body||'port_'+P.key+'_idle',bx+bodyW/2,by+bh/2,bodyW-8,bh,1);
 // The broad actual gameplay ship is easiest to identify; no generated substitute.
 const ship=psShipKey(P.key,null);psBlitFit(ship,sx+shipW/2,shipY,shipW-12,shipH-8,1);
 const M=BOFX.pilotcard?.[P.key]||{},stats=pcStats(P.key),sp=pcSpecial(P.key),copy=pcScreenCopy(P);
 pilotNameDraw(launching?'GOOD LUCK, '+P.name+'!':pcRevealText(copy,0),PX+PW/2,PY+17,20,P.tint,1);
 PT11_UI.card={pilot:P.key,body:[bx,by,bodyW,bh],ship:[sx,by,shipW,shipH],info:[infoX,infoY,infoW,infoH],key:ship};
 if(launching)return;
 const title=pcRevealText(copy,1),call=pcRevealText(copy,2),aff=pcRevealText(copy,3);
 pcFontLeft(title,infoX,infoY+5,pcFontFit(title,infoW,10,8),P.tint,1);
 pcFontLeft(call,infoX,infoY+20,pcFontFit(call,infoW,10,8),'#f0f4ff',1);
 const emblem=affilEmblemKey(M.affil),eh=Math.min(46,infoH*.16),emblemReady=!!(emblem&&XART.rdy(emblem)),emblemSpace=emblemReady?eh+8:0;
 if(emblemReady)psBlitFit(emblem,infoX+eh/2,infoY+37+eh/2,eh,eh,1);
 for(const [i,line] of pcFontWrap(aff,infoW-emblemSpace,10).entries())pcFontLeft(line,infoX+emblemSpace,infoY+42+i*14,10,'#cfeaff',1);
 const specialH=44,statH=stats.length*13,statY=infoY+infoH-specialH-statH-9,bioTop=infoY+43+eh,bioBottom=statY-5;
 const bio=pcRevealText(copy,4),bioLines=pcFontWrap(bio,infoW,8);
 for(let i=0;i<bioLines.length&&bioTop+11*i<bioBottom;i++)pcFontLeft(bioLines[i],infoX,bioTop+11*i,8,'#dbe8f3',1);
 const barX=infoX+infoW*.51,barW=infoW*.49;
 for(let i=0;i<stats.length;i++){
  const y=statY+i*13,frac=pcVisibleSegments(i,stats[i].val)/PC_MAX_SEG;
  const ready=pcard&&(pcard.done||pcard.phase==='special'||pcard.phase==='hold'||pcard.phase==='bars'&&pcard.bar>=i);
  if(ready)pcFontLeft(stats[i].label,infoX,y,pcFontFit(stats[i].label,infoW*.49,8,7),'#dbe8ff',1);
  ctx.fillStyle='#0c1522';ctx.fillRect(barX,y-3,barW,7);ctx.fillStyle=P.tint;ctx.fillRect(barX+1,y-2,(barW-2)*frac,5);
 }
 if(pcard&&(pcard.done||pcard.phase==='special'||pcard.phase==='hold')){
  const y=infoY+infoH-22,a=pcard.done?1:pcard.spT||0;ctx.save();ctx.globalAlpha=a;
  iconDraw('spicon_'+P.key,infoX+20,y,40,true);ctx.restore();
  const lines=sp.name.replace(' + ',' / ').split(' / '),width=infoW-48;
  lines.forEach((line,i)=>pcFontLeft(line,infoX+48,y+(i-(lines.length-1)/2)*13,pcFontFit(line,width,10,7),P.tint,a));
 }
}
// Body portraits have their own source rectangle. Mirroring only that rectangle
// leaves the authored lettering and cabinet frame facing the correct way.
function pt11DifficultyFace(im,key,x,y,w,h){
 if(!['diff_easy_0916','diff_normal_0916','diff_hard_0916'].includes(key))return;
 const sx=33,sy=18,sw=77,sh=78,k=w/im.width;
 ctx.save();ctx.translate(x+(sx+sw)*k,y+sy*k);ctx.scale(-1,1);
 ctx.drawImage(im,sx,sy,sw,sh,0,0,sw*k,sh*k);ctx.restore();
}

// The intro keeps the selected pilot's real ship and face throughout the shot.
function pt11OpeningShip(pk,t,x,y,h,power){
 const ph=SHIP_GLOW_SEQ[Math.floor(t*1000/SHIP_GLOW_MS)%SHIP_GLOW_SEQ.length],base='ship_'+pk;
 const key=ph&&window.BOFX?.ships?.[base+'_'+ph]?base+'_'+ph:base;
 if(!XART.rdy(key))return false;const im=XART.get(key),w=h*im.width/im.height;
 // Opening time owns exhaust even while the combat clock/player is idle.
 const burn=power??(.48+.06*Math.sin(t*17)),previous=player._thrustFrame;
 let plume=false;player._thrustFrame=Math.floor(t*1000/55);
 try{plume=pf27PlaneThrustDraw(ctx,key,x,y,w,h,burn);}finally{player._thrustFrame=previous;}
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,x-w/2,y-h/2,w,h);ctx.restore();
 PT11_UI.ship={pilot:pk,key,x,y,w,h,power:burn,plume,thrustFrame:Math.floor(t*1000/55)};return true;
}
const pt11IntroWarm=campaignIntroWarm;
campaignIntroWarm=function(){const r=pt11IntroWarm.apply(this,arguments);
 for(const k of ['nbl_logo_0916','cpov_male_hand','cpov_female_hand'])XART.rdy(k);
 for(const pk of OPN_ORDER)for(const suffix of ['','_g1','_g2'])XART.rdy('ship_'+pk+suffix);
 if(typeof HQ10_ART!=='undefined')for(const a of HQ10_ART.radar)XART.rdy(a.key);
 return r;
};
function pt11CockpitInstruments(C,t,W,H){
 if(typeof HQ10_ART==='undefined')return;const bank=HQ10_ART.radar,a=bank[Math.floor(t*16)%bank.length];
 if(a&&XART.rdy(a.key)){
  const x=W*.613,y=H*.615,size=H*.12;ctx.save();ctx.beginPath();ctx.ellipse(x,y,size*.48,size*.50,0,0,TAU);ctx.clip();
  ctx.fillStyle='#00141c';ctx.fillRect(x-size/2,y-size/2,size,size);
  ctx.drawImage(XART.get(a.key),x-size/2,y-size/2,size,size);ctx.restore();
 }
 const beat=Math.floor(t*1.4);if(C._pt11RadarBeat!==beat){C._pt11RadarBeat=beat;if(Audio.SFX.retinaLockBeep)Audio.SFX.retinaLockBeep();}
 // Existing authored hand poses settle onto the existing control stick.
 if(typeof cockpitHandTint==='function'){
  const hand=cockpitHandTint(C.pilot);if(hand){const fw=hand.width/4,fh=hand.height,w=W*.42,h=w*fh/fw,u=clamp(t/.9,0,1),ease=u*u*(3-2*u);
   ctx.drawImage(hand,0,0,fw,fh,W*.5-w*.49,H*.65-h*.24+(1-ease)*H*.55,w,h);}
 }
 PT11_UI.radar={frame:Math.floor(t*16)%bank.length,beat};
}
campaignIntroFinale=function(C,t,W,H){
 const q=Math.max(0,t-CAMPAIGN_INTRO_FINALE),u=clamp(q/2.2,0,1),y=H*(.82-.69*u);
 campaignIntroJungle(W,H,q*1.75);pt11OpeningShip(C.pilot,q,W*.5,y,H*.24);
 if(ASSETS.has('bullet_mg_a'))for(let i=0;i<9;i++)for(const side of [-1,1]){
  const by=y-((q*600+i*57)%H);if(by>0)ASSETS.blit('bullet_mg_a',W*.5+side*H*.028,by,6,20);
 }
 const burst=Math.floor(q*7);if(C._pt11TitleBurst!==burst){C._pt11TitleBurst=burst;if(q<2.4&&Audio.SFX.machineGun)Audio.SFX.machineGun();}
 if(XART.rdy('nbl_logo_0916')){const im=XART.get('nbl_logo_0916'),w=Math.min(W*.66,H*.9),h=w*im.height/im.width;
  ctx.save();ctx.globalAlpha=clamp(q/.35,0,1);ctx.drawImage(im,(W-w)/2,H*.40-h/2,w,h);ctx.restore();}
 const lines=['ONE PILOT. ONE WAY HOME.','STAGE 1 - THE JUNGLE CORRIDOR'];
 for(let i=0;i<lines.length;i++){
  const shown=Math.max(0,Math.floor((q-.5-i*.55)*36)),last=C['_pt11Title'+i]||0;
  dialogueLetterTicks(lines[i],last,Math.min(shown,lines[i].length));C['_pt11Title'+i]=Math.min(shown,lines[i].length);
  msgFaceUse('dialogue');msgText(lines[i].slice(0,shown),W/2,H*(.67+i*.09),Math.max(12,H*.027),i?'#9fe2b8':'#f3f7ff',1,1,.06);msgFaceUse(null);
 }
 PT11_UI.title={q,logo:XART.rdy('nbl_logo_0916'),pilot:C.pilot};
};
