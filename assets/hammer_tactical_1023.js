'use strict';
/* Stage5 whole-actor tactical handoff. Authored pixels only; native combat owns
   HP, destruction, projectiles, warnings, music, and their established timing. */
const HT23={base:{draw:hammerBossDraw,blue:ha21Blue,tick:hb20PickupTick,pickupDraw:hb20PickupDraw,mount:hammerBlasterMount,load:stageLoadBegin,head:hammerHeadPoint},events:[],draws:{}};
for(const s of Object.values(HT23_ART.sheets))XART._src[s.key]=s.path;
for(const rows of Object.values(HT23_ART.banks))for(const a of rows)BOFX.cells[a.key]=[a.sheet,...a.cell];
XART._src.ht23_shoot=HT23_ART.shoot.path;
for(const s of Object.values(HT23_ARMOR.sheets))XART._src[s.key]=s.path;
for(const rows of Object.values(HT23_ARMOR.banks))for(const a of rows){BOFX.cells[a.key]=[a.sheet,...a.cell];if(a.white)BOFX.cells[a.white]=[a.sheet+'_hit',...a.cell];}
XART._src.ht23_plated_idle=HT23_ARMOR.platedIdle.path;
XART._src.ht23_plated_idle_hit=HT23_ARMOR.platedIdle.path.replace('.webp','_hit.webp');
function ht23Warm(){return [...Object.values(HT23_ARMOR.sheets).map(s=>s.key),...Object.values(HT23_ART.sheets).map(s=>s.key),'ht23_shoot','ht23_plated_idle','ht23_plated_idle_hit'].map(k=>XART.rdy(k)).every(Boolean);}
stageLoadBegin=function(n,keys){return HT23.base.load.call(this,n,[...(keys||[]),'boss_shoot_prompt',...(n===5?[...Object.values(HT23_ARMOR.sheets).map(s=>s.key),...Object.values(HT23_ART.sheets).map(s=>s.key),'ht23_shoot','ht23_plated_idle','ht23_plated_idle_hit']:[])]);};
function ht23Own(b){return run.stage===5&&b?._hammer&&!b._gp4Host&&!b.dead;}
function ht23Variant(b){return hf22Red(b)?'_red':(fr27Armor(b)?.activated||b._hammer.state==='fr_activation'&&b._hammer.t>=FR27_ACT.plate)&&fr27Armor(b)?.hp>0?'_armor':'';}
function ht23Row(b,bank,f){const rows=HT23_ART.banks[bank+ht23Variant(b)]||HT23_ART.banks[bank];return rows[Math.max(0,Math.min(rows.length-1,f|0))];}
function ht23DrawCell(a,x,y,flash=0){const key=flash>0&&a.white?a.white:a.key;if(!XART.rdy(key))return false;ctx.drawImage(XART.get(key),Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]));HT23.draws[a.key]=(HT23.draws[a.key]||0)+1;return true;}
function ht23GunPose(b){const h=b._hammer,f=h.state==='chaingun'?1+Math.floor(h.t*12)%8:0;return ht23Row(b,'fire',f);}
HT23.base.armorBegin=fr27BeginArmor;HT23.base.armorTick=fr27ActivationTick;
fr27BeginArmor=function(b){const gun=ht23Own(b)&&b._hammer.hb20PickupDone&&b._hammer.hammerDestroyed&&b._hammer.mode==='chaingun';const r=HT23.base.armorBegin.apply(this,arguments);if(gun)b._hammer._ht23ArmorGun=true;return r;};
fr27ActivationTick=function(b,dt){const h=b._hammer,gun=h._ht23ArmorGun,r=HT23.base.armorTick.apply(this,arguments);if(gun&&h.state!=='fr_activation'){h._ht23ArmorGun=false;h.mode='chaingun';hammerChainStart(b);HT23.events.push({type:'armor-returns-to-tactical',t:efxClock});}return r;};
ha21Blue=function(b){
 if(ht23Own(b)&&b._hammer.state==='fr_activation'&&!b._hammer._ht23ArmorGun){const rows=HT23_ARMOR.banks.activation,a=rows[Math.min(rows.length-1,Math.floor(clamp(b._hammer.t/FR27_ACT.end,0,.999)*rows.length))];if(XART.rdy(a.key)&&XART.rdy(a.white))return{a,k:1,rot:0,kind:'blue_chromium_clean'};}
 const q=HT23.base.blue.apply(this,arguments);
 if(ht23Own(b)&&q?.kind==='blue_chromium'&&b._hammer.state!=='fr_activation')return{a:HT23_ARMOR.platedIdle,k:1,rot:0,kind:'blue_chromium_clean'};
 return q;};
hb20PickupTick=function(b,C,dt){if(C.corrupt||!ht23Own(b))return HT23.base.tick.apply(this,arguments);
 C.t+=dt;const u=v19Ease(Math.min(1,C.t/.8));b.x=lerp(C.origin.x,C.station.x,u);b.y=lerp(C.origin.y,C.station.y,u);
 if(!C.hit&&C.t>=1.78){C.hit=true;explode(C.box.x,C.box.y,54,'blue');b20Cue('hammerImpact');HT23.events.push({type:'crate-struck',t:C.t});}
 if(!C.released&&C.t>=2.26){C.released=true;C.release={x:b.x-75,y:b.y-172};b._hammer.hammerDestroyed=true;b20Cue('hammerThrow');HT23.events.push({type:'hammer-released-up',t:C.t});}
 if(!C.opened&&C.t>=2.86){C.opened=true;b20Cue('pickup');HT23.events.push({type:'gun-ejected',t:C.t});}
 if(!C.obtained&&C.t>=4.05){C.obtained=true;b20Cue('pickup');HT23.events.push({type:'gun-caught',t:C.t});}
 if(C.t>=4.5&&!C.ht23Done){C.ht23Done=true;HT23.events.push({type:'tactical-ready',t:C.t});}
 return C.t>=4.5;
};
hb20PickupDraw=function(b,C,corrupt){if(corrupt||!ht23Own(b))return HT23.base.pickupDraw.apply(this,arguments);
 const rows=HT23_ART.banks.crate,frame=C.t<1.78?0:Math.min(rows.length-1,Math.floor((C.t-1.78)/.8*rows.length));ht23DrawCell(rows[frame],C.box.x,C.box.y);
};
hammerHeadPoint=function(b){const C=b?._hammer?.hb20Pickup;if(ht23Own(b)&&C&&C.t>=1.78){if(C.released)return{x:C.release.x,y:C.release.y-(C.t-2.26)*650};const f=Math.max(0,Math.min(3,Math.floor((C.t-1.78)/1.08*9))),p=HT23_ART.heldHammer[f];return{x:b.x+p[0],y:b.y+p[1]};}return HT23.base.head.apply(this,arguments);};
hammerBlasterMount=function(b){if(ht23Own(b)&&['chain_warn','chaingun','chain_cool'].includes(b._hammer.state)){
 const a=ht23GunPose(b),x=b.x+a.muzzle[0]-a.pivot[0],muzzleY=b.y+a.muzzle[1]-a.pivot[1],y=b.y+40;return{x,y,muzzleY,left:x-40,top:y-20,scale:1};
 }return HT23.base.mount.apply(this,arguments);};
hammerBossDraw=function(b){const C=b?._hammer?.hb20Pickup,h=b?._hammer;
 if(!ht23Own(b)||C&&C.t<1.78||!C&&!['chain_warn','chaingun','chain_cool'].includes(h.state)&&!h._ht23ArmorGun)return HT23.base.draw.apply(this,arguments);
 hammerBossAtmosphereDraw(b);hf22Aura(b);ctx.save();ctx.imageSmoothingEnabled=false;
 if(C){
  hb20PickupDraw(b,C,false);
  const toss=C.t<2.86,bank=toss?'toss':'catch',u=toss?(C.t-1.78)/1.08:(C.t-2.86)/1.44,f=Math.min(8,Math.floor(Math.max(0,u)*9));
  ht23DrawCell(ht23Row(b,bank,f),b.x,b.y,Math.max(b.flash||0,b._lastPart?.flash||0));
  if(C.released){const p=hammerHeadPoint(b);if(p.y+180>viewTopY())ht23DrawCell(ht23Row(b,'tool',0),p.x,p.y);}
  if(C.t>=2.86&&f<3&&!toss){const u=Math.min(1,(C.t-2.86)/.48),x=lerp(C.box.x,b.x-15,u),y=lerp(C.box.y,b.y+120,u)-Math.sin(u*Math.PI)*22;ht23DrawCell(ht23Row(b,'gun_prop',0),x,y);}
 }else{
  const a=ht23GunPose(b),m=hammerBlasterMount(b);ht23DrawCell(a,b.x,b.y,Math.max(b.flash||0,b._lastPart?.flash||0));
  if(h.state==='chain_warn'){const warm=hammerFurious()?.65:hammerHard()?.75:.85;combatWarningDraw(b,{x:m.x,y:m.muzzleY,ex:m.x,ey:PLAY.y+PLAY.h,progress:clamp(h.t/warm,0,1),width:44,alertX:b.x,alertY:b.y-80});}
  if(h.chainMuzzle>0)wm26Draw(ctx,'chaingun',m.x,m.muzzleY,Math.PI/2,1-h.chainMuzzle/.09,48);
 }
 ctx.restore();hm10WallDraw(b);hf19Caption(b);
};
window.BOF_HAMMER_TACTICAL=HT23;ht23Warm();

// Announcements share the portrait owner while combat continues underneath.
HT23.speech=[];HT23.speechSerial=0;
function ht23Say(b,text){
 if(!ht23Own(b)||state!==GS.PLAY)return;
 if(text==='Chromium Shield, Activate!'&&b._hammer.state==='fr_activation')text='Chromium Armor, Activated!';
 const current=BOFCinematicDirector.current;
 if(current?.id.startsWith('ht23-announcement-')&&HT23.speechOwner===b&&current.beats[0]?.text===text||HT23.speech.some(q=>q.b===b&&q.text===text))return;
 HT23.speech.push({b,text});HT23.events.push({type:'portrait-announcement',text,t:efxClock});
}
HT23.base.caption=cp12Caption;
cp12Caption=function(b,text){
 if(!ht23Own(b))return HT23.base.caption.apply(this,arguments);
 // t=0 retires both legacy floating-caption renderers.
 b._hammer.cp12Caption={text,t:0};cp12Log('caption',{text});ht23Say(b,text);
};
const ht23ArmorAnnouncement=fr27BeginArmor;
// The opening-jump gate legitimately declines activation (null). Only a real
// activation may enqueue dialogue; announcing a declined attempt freezes the
// jump and immediately queues the same line again on the next combat tick.
fr27BeginArmor=function(b){const r=ht23ArmorAnnouncement.apply(this,arguments);if(r&&ht23Own(b))ht23Say(b,'Chromium Armor, Activated!');return r;};
HT23.base.play=updatePlay;HT23.base.begin=beginStage;
updatePlay=function(dt){
 // Native combat owns flash expiry while dialogue continues.
 if(BOFCinematicDirector.current?.id.startsWith('ht23-announcement-')&&HT23.speechOwner===boss){
  // No duplicate combat timers in this overlay.
 }
 const r=HT23.base.play.apply(this,arguments),current=BOFCinematicDirector.current;
 if(current?.id.startsWith('ht23-announcement-')&&(!ht23Own(HT23.speechOwner)||HT23.speechOwner!==boss||state!==GS.PLAY)){BOFCinematicDirector.cancel();HT23.speechOwner=null;}
 HT23.speech=HT23.speech.filter(q=>q.b===boss&&ht23Own(q.b)&&state===GS.PLAY);
 if(!BOFCinematicDirector.active&&HT23.speech.length){const q=HT23.speech.shift();HT23.speechOwner=q.b;
  BOFCinematicDirector.play('ht23-announcement-'+(++HT23.speechSerial),[{who:'CHRONOS',art:'fb1002_hammer_portrait',text:q.text}],()=>{HT23.speechOwner=null;},true);
 }
 return r;
};
beginStage=function(){HT23.speech.length=0;HT23.speechOwner=null;return HT23.base.begin.apply(this,arguments);};
