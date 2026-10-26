'use strict';
/* Stage5: gun ownership lasts until actual module exhaustion. Destruction,
   armor rupture and permanent rage each have an explicit physical sequence. */
const C29={events:[],base:{tick:hammerBossTick,damage:hammerBossDamage,module:hammerBossModuleBreak,
 blue:ha21Blue,draw:hammerBossDraw,fire:hammerBossChaingunFire,restore:fr27Restore,
 beginArmor:fr27BeginArmor,rage:c27RageTick,beginRage:hf22BeginBlueRage},draws:{}};
for(const s of Object.values(C29_ART.sheets))XART._src[s.key]=s.path;
for(const rows of Object.values(C29_ART.banks))for(const a of rows)BOFX.cells[a.key]=[a.sheet,...a.cell];
function c29Warm(){return Object.values(C29_ART.sheets).map(s=>XART.rdy(s.key)).every(Boolean);}
const c29Load=stageLoadBegin;
stageLoadBegin=function(n,keys){return c29Load.call(this,n,[...(keys||[]),...(n===5?Object.values(C29_ART.sheets).map(s=>s.key):[])]);};
function c29Log(type,data={}){C29.events.push({type,time:efxClock,...data});if(C29.events.length>400)C29.events.shift();}
function c29Gun(b){const h=b?._hammer;return c25Own(b)&&!b.dead&&h.hb20PickupDone&&h.hammerDestroyed&&!h.chainDestroyed&&!h.hb20Pickup;}
function c29Row(bank,f,mat='regular'){const rows=C29_ART.banks[bank+'_'+mat];return rows[Math.min(rows.length-1,Math.max(0,Math.floor(f)))];}
function c29Pose(bank,f,mat){const a=c29Row(bank,f,mat);return{a,k:1,rot:0,kind:'c29_'+bank+'_'+mat};}
function c29Hold(b,u=1,mat=c27Material(b)){
 const rows=C29_ART.banks['hold_'+mat],f=Math.min(rows.length-1,Math.floor(clamp(u,0,1)*(rows.length-1)));
 return c29Pose('hold',f,mat);
}
ha21Blue=function(b){if(!c25Own(b)||b.dead)return C29.base.blue.apply(this,arguments);
 const h=b._hammer,K=h.c29Break;
 if(K?.reason==='armor'){const t=K.t,u=t<.65?1-t/.65:t<2.2?0:clamp((t-2.2)/1.45,0,1);return c25Plate(b,'empty',u)||C29.base.blue.apply(this,arguments);}
 if(K){const t=K.t,mat=K.reason==='armor'?(t<.4?'chrome':'regular'):c27Material(b);
  return t<.65?c29Pose('stun',Math.min(2,Math.floor(t/.22)),mat):t<2.2?c29Pose('stun',2,mat):c29Pose('recall',Math.min(8,(t-2.2)/1.7*8),mat);}
 if(h._hf22Charge){const u=clamp(h._hf22Charge.t/1.8,0,1),mat=u>=.62?'red':c26Material(b);
  return u>.86?c29Pose('recall',8,mat):c29Pose('rage',clamp(u/.86,0,1)*(C29_ART.banks.rage_regular.length-1),mat);}
 if(h.state==='fr_activation'&&!h._ht23ArmorGun)return c29Hold(b,clamp(h.t/.85,0,1),h.t>=C27_ARMOR.plate?'chrome':'regular');
 if(h.recovery?.status==='charging'||h.state==='shield')return c29Hold(b,clamp(h.t/.85,0,1));
 return C29.base.blue.apply(this,arguments);
};
function c29DamageBudget(b,dt){const G=cr17Guard(b);G.tokens=Math.min(b.maxhp*.018,G.tokens+Math.max(0,dt)*b.maxhp*[.034,.030,.027,.024][vp12Tier()]);}
function c29Break(b,reason){const h=b._hammer;if(h.c29Break)return;
 const held=hammerHeadPoint(b),gun=c29Gun(b);h.c29Break={t:0,reason,gun,x0:b.x,x1:(camLeftX()+camRightX())/2,y0:b.y,y1:viewTopY()+190,from:{...held},away:{x:b.x-145,y:viewTopY()-75}};
 h.recovery=null;h.frRecovery=false;h.throw=null;h.c26Return=null;h.c27Combo=null;h._hj22Pair=null;h._hf22StormPair=null;h.er23DepthCombo=null;h.hc11Counter=null;
 h.shotCd=999;h.chainMuzzle=0;h.phasePending=false;h.chainDebrisT=0;h.hammerDestroyed=true;b._noHit=false;
 const A=fr27Armor(b);if(A){A.barrier=0;A.stunCritical=false;if(reason==='armor'){A.hp=0;A.active=false;A.activated=false;}}
 hammerState(b,'c29_break');
 if(reason==='armor'){for(const [x,y]of [[-64,-44],[64,-44],[0,6]])explode(b.x+x,b.y+y,44,'blue');spawnShockRing(b.x,b.y,180,'comet');shake=Math.max(shake,6);h.c29Break.ruptureBeat=0;b20Cue('shieldBreakCombat');}
 c29Log(reason+'-broken');
}
hammerBossModuleBreak=function(b,which){const r=C29.base.module.apply(this,arguments);if(c25Own(b)&&which==='chaingun')c29Break(b,'gun');return r;};
hammerBossDamage=function(b,dmg){if(!c25Own(b))return C29.base.damage.apply(this,arguments);
 const h=b._hammer;
 if(b._hammerModuleHit==='chaingun'&&!h.chainDestroyed&&(h.c29GunTime||0)<5){b._hammerModuleHit=null;if(dmg>0){markHit(b);if(gp4FlashRequest(h,'ch23GunFlash',.12))h.ch23GunFlash=.12;}return 0;}
 const A=fr27Armor(b),hp=A?.hp||0,r=C29.base.damage.apply(this,arguments);
 if(hp>0&&A.hp<=0&&!b.dead)c29Break(b,'armor');return r;
};
hammerBossChaingunFire=function(b){if(!c29Gun(b))return C29.base.fire.apply(this,arguments);
 const h=b._hammer,m=ch23Mount(b),u=clamp((h.c29GunTime||0)/4,0,1);
 h.chainMuzzle=.09;const muzzle=ch23Mount(b);eMG(muzzle.x,muzzle.muzzleY,Math.PI/2,hammerFurious()?5.6:5.0,'#a5cfff');
 ch23Round(eBullets[eBullets.length-1],4,'down');h.shotCd=lerp(.18,hammerFurious()?.045:.065,u);h.chainHeat=u;
 if((h.chainSfxCd||0)<=0){Audio.SFX.hammerChaingun?.();h.chainSfxCd=1.45;}
 c29Log('gun-shot',{interval:h.shotCd,x:muzzle.x,y:muzzle.muzzleY});
};
hammerBossTick=function(b,dt){if(!c25Own(b)||b.dead)return C29.base.tick.apply(this,arguments);
 const h=b._hammer,K=h.c29Break;
 if(K){K.t+=dt;h.t+=dt;
  // Finite armor rupture follows the living actor into its native stun pose.
  if(K.reason==='armor'){const beats=[{at:.16,points:[[-72,18],[70,30],[0,-52]]},{at:.34,points:[[-42,72],[42,72],[0,24]]}];while((K.ruptureBeat||0)<beats.length&&K.t>=beats[K.ruptureBeat||0].at){const beat=beats[K.ruptureBeat||0];K.ruptureBeat=(K.ruptureBeat||0)+1;for(const [x,y]of beat.points)explode(b.x+x,b.y+y,38,'blue',null,null,null,null,true);}}
 const v=clamp(K.t/.65,0,1);b.y=lerp(K.y0,K.y1,v*v*(3-2*v));b.x=lerp(K.x0,K.x1,v*v*(3-2*v));b._drawY=b.y;const A=fr27Armor(b);if(A)A.flash=Math.max(0,(A.flash||0)-dt);
  if(K.t>=2.2&&!K.recall){K.recall=true;b20Cue('hammerMagnet');c29Log('raised-hand-recall');}
  if(K.t>=4.4){delete h.c29Break;h.shotCd=.12;h.hammerHP=h.hammerMax;h.mode=K.gun?'chaingun':'hammer';h.hammerDestroyed=!!K.gun;
   if(K.gun){h.c29GunTime=0;hammerChainStart(b);}else hammerState(b,'hammer');c29Log('recovered',{armor:fr27Armor(b)?.hp||0,gun:K.gun});}
  return;
 }
 if(c29Gun(b)&&h.state!=='fr_activation'){
  if(!['chain_warn','chaingun'].includes(h.state)){hammerChainStart(b);c29Log('gun-retains-control');}
  if(h.state==='chain_warn')return C29.base.tick.apply(this,arguments);
  c29DamageBudget(b,dt); // This committed firing owner bypasses CR17's ordinary tick.
  h.t+=dt;h.c29GunTime=(h.c29GunTime||0)+dt;h.chainMuzzle=Math.max(0,(h.chainMuzzle||0)-dt);h.chainSfxCd=Math.max(0,(h.chainSfxCd||0)-dt);h.ch23GunFlash=Math.max(0,(h.ch23GunFlash||0)-dt);h.shotCd-=dt;
  const u=clamp(h.c29GunTime/4,0,1);h.ch23Rev=lerp(.3,1,u);h.ch23Spin=(h.ch23Spin||0)+dt*lerp(8,30,u);h.chainHeat=u;
  const left=camLeftX()+90,right=camRightX()-90;h.chainDir=h.chainDir||1;b.x+=h.chainDir*lerp(100,165,u)*dt;
  if(b.x>=right){b.x=right;h.chainDir=-1;}if(b.x<=left){b.x=left;h.chainDir=1;}b._drawY=b.y;
  if(h.shotCd<=0)hammerBossChaingunFire(b);const A=fr27Armor(b);if(A){A.flash=Math.max(0,(A.flash||0)-dt);A.t+=dt;}
  return;
 }
 return C29.base.tick.apply(this,arguments);
};
fr27Restore=function(b){const r=C29.base.restore.apply(this,arguments);if(c25Own(b)&&b._hammer.recovery?.status==='charging'){
 const q=c29Hold(b);b._hammer.c25ChargeY=viewTopY()+150-(q.a.tip[1]-q.a.pivot[1]);}return r;};
fr27BeginArmor=function(b){const r=C29.base.beginArmor.apply(this,arguments);if(r&&c25Own(b)&&!b._hammer._ht23ArmorGun){
 const q=c29Hold(b),y=viewTopY()+145-(q.a.tip[1]-q.a.pivot[1]);b._hammer.frAct.y0=y;b._hammer.c27ArmorY=y;}return r;};
hf22BeginBlueRage=function(b){if(c29Gun(b)||b?._hammer?.c29Break)return;const from=c25Own(b)?{...hammerHeadPoint(b)}:null,r=C29.base.beginRage.apply(this,arguments);
 if(c25Own(b)&&b._hammer._hf22Charge&&!b._hammer._hf22Charge.tool){const C=b._hammer._hf22Charge;C.tool=from;C.y0=b.y;C.y1=Math.max(b.y,viewTopY()+260);b20Cue('hammerThrow');}return r;};
c27RageTick=function(b,dt){const C=b._hammer._hf22Charge;if(C&&Number.isFinite(C.y0)){const v=clamp(C.t/.25,0,1);b.y=lerp(C.y0,C.y1,v*v*(3-2*v));}
 return C29.base.rage.call(this,b,C?dt*1.8/7.2:dt);};
function c29Tool(b,from,to,u,scale=1,angle=0){const a=hf22Row('blue_tool',0);if(!a||!XART.rdy(a.key))return;
 const e=u*u*(3-2*u),x=lerp(from.x,to.x,e),y=lerp(from.y,to.y,e);ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.scale(scale,scale);ctx.drawImage(XART.get(a.key),-a.pivot[0],-a.pivot[1]);ctx.restore();}
function c29RecallDraw(b,K){const target=c35Catch(b),head=target.at;
 const u=clamp((K.t-3.35)/1.05,0,1);if(K.gun)return;
 if(K.reason==='armor'&&K.t<.7)c29Tool(b,K.from,K.away,K.t/.7,lerp(1,.3,K.t/.7));
 else if(u>0){c29Tool(b,K.away,head,u,lerp(.3,target.scale,u),target.angle);c25Bolt(head,K.away,K.t,10,.5);}
}
function c29Bar(b){const m=ch23Mount(b),h=b._hammer,w=94,y=m.top-14,x=m.x-w/2;
 ctx.save();ctx.fillStyle='#050a12';ctx.fillRect(x-2,y-2,w+4,12);ctx.strokeStyle='#b8dfff';ctx.lineWidth=1;ctx.strokeRect(x-2,y-2,w+4,12);ctx.fillStyle='#1d3347';ctx.fillRect(x,y,w,8);ctx.fillStyle=h.ch23GunFlash>0?'#ffffff':'#efb633';ctx.fillRect(x,y,w*clamp(h.chainHP/h.chainMax,0,1),8);ctx.restore();C29.bar={x,y,w,hp:h.chainHP,max:h.chainMax};}
hammerBossDraw=function(b){if(!c25Own(b)||b.dead)return C29.base.draw.apply(this,arguments);const h=b._hammer;
 if(h.c29Break){hammerBossAtmosphereDraw(b);
  // Armor can rupture while the gun is still intact. Keep that real weapon
  // gripped through the stagger; only gun destruction earns a hammer recall.
  if(h.c29Break.gun){const f=Math.min(5,Math.floor(h.c29Break.t*8)%6),m=ch23Mount(b),flash=Math.max(b.flash||0,h.ch23GunFlash||0);
   ch23Blit(ch23Cell('body',b,f),b.x,b.y,flash);ch23Blit(m.a,m.x,m.y,flash);ch23Blit(ch23Cell('hands',b,f),b.x,b.y,flash);c29Bar(b);return;}
  const q=ha21Blue(b);ha21Body(b,q);c29RecallDraw(b,h.c29Break);return;}
 const r=C29.base.draw.apply(this,arguments);
 if(ch23Armed(b))c29Bar(b);
 if(h.recovery?.status==='charging'&&h.t>.85){const head=hammerHeadPoint(b);c25Bolt(head,{x:b.x-18,y:b.y+5},h.t,17,.85);c25Bolt(head,{x:b.x+22,y:b.y+12},h.t+.3,14,.7);}
 if(h._hf22Charge){const C=h._hf22Charge,u=C.t/1.8,q=ha21Blue(b),grip=hb20World(q.a,q.a.hand||[q.a.pivot[0]-60,q.a.pivot[1]-130],b,1,0),hand={x:grip.x+120,y:grip.y},away={x:b.x-145,y:viewTopY()-60};
  if(u<.16)c29Tool(b,C.tool||hand,away,u/.16,lerp(1,.3,u/.16));else if(u>.86){c29Tool(b,away,hand,(u-.86)/.14,lerp(.3,1,(u-.86)/.14),Math.PI/2);c25Bolt(hand,away,h.t,10,.5);}
  if(u>.24&&u<.86){c25Bolt({x:b.x-55,y:b.y+85},{x:b.x+42,y:b.y-65},h.t*2,16,.65);}
 }
 return r;
};
window.BOF_CHRONOS_COMMITMENT=C29;c29Warm();

// A destroyed gun cannot re-enter the legacy half-health arsenal cycle.
const c29PhaseTwo=hammerPhaseTwoStart,c29ChainStart=hammerChainStart;
function c29GunGone(b){if(!c25Own(b)||!b._hammer.chainDestroyed)return false;const h=b._hammer;h.phasePending=false;h.mode='hammer';h.hammerDestroyed=false;h.chainMuzzle=0;
 if(!h.c29Break&&!h._hf22Red)hammerState(b,'hammer');return true;}
hammerPhaseTwoStart=function(b){if(c29GunGone(b))return;return c29PhaseTwo.apply(this,arguments);};
hammerChainStart=function(b){if(c29GunGone(b))return;return c29ChainStart.apply(this,arguments);};
