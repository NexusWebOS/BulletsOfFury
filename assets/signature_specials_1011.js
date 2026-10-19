"use strict";
/* Enemy Rebels lead with their own signatures; Stage X earns Mk II.
   October 18: no automatic opening supply. Specials come from normal pickups. */
const FS11_KEY='bof_signature_mk2_v1';
const FS11_UPGRADES={
 axel:{name:'MEGA SHIELD MK II',bonus:'50% STRONGER REFLECTED SHOTS'},
 decker:{name:'CLOAKING SYSTEM MK II',bonus:'20 SECOND TARGETING DISRUPTION'},
 maverick:{name:'HELIX BEAM MK II',bonus:'25% STRONGER CHARGED HELIX'},
 freezer:{name:'THERMOSHOCK MK II',bonus:'DEEPER TIME FREEZE'},
 juggernaut:{name:'WRECKING BALL MK II',bonus:'20% FASTER FLAIL ROTATION'},
 yuri:{name:'CHAIN LIGHTNING MK II',bonus:'EXTRA CHAIN TIER'},
 cole:{name:'NUKE STRIKE MK II',bonus:'TWO ADDITIONAL WARHEADS'},
 lizzie:{name:'ATOM BOMB MK II',bonus:'TWO ADDITIONAL ATOM BOMBS'},
 falva:{name:'ROLLER BALL MK II',bonus:'25% STRONGER ROLLER BALL'}
};
const FS11_REBELS={
 voss:{kind:'turbo',name:'TURBO OVERDRIVE'},nyx:{kind:'cloak',name:'GHOSTKNIFE CLOAK'},
 rook:{kind:'slug',name:'HEAVY GUN BARRAGE'},kaia:{kind:'rockets',name:'TWIN SEEKER RACK'},
 jace:{kind:'helix',name:'MOLTEN HELIX NOVA'}
};
const FS11={receipt:null,pending:null,boxes:[],proof:null,reward:null,events:[],draws:{},seatStash:null,
 seat2:{special:null,falva:[],wreck:[],storm:null},base:{
 start:startRun,begin:beginStage,
 special:startSpecial,end:endSpecial,reflect:axelMegaReflect,helix:releaseHelix,
 roller:releaseRoller,wreck:wreckTick,spawnBoss,leave:scLeaveStage,reward:ap10StageXReward,
 snapshot:campSnapshot,apply:campApply,card:pcSpecial,hud:ph8Values,hudIcon:ph8Icon,brief:mapgBriefingDraw,
 state:setState,rebelInit:rg4Init,rebelKind:ra4AttackKind,rebelAttack:rg4Attack,rebelShip:fr27RebelDrawShip,
 seatIn,seatOut,updateSpecial
}};
FS11.base.stormTick=thunderStormTick;
FS11.base.specialPaint={};
function fs11ReceiptValid(q){return !!(q?.version===1&&q.stage==='X'&&['left','right'].includes(q.route)&&
 q.boss===(q.route==='left'?'warhive':'rebelsquad')&&q.earned===true&&Number.isFinite(q.at));}
try{const q=JSON.parse(localStorage.getItem(FS11_KEY)||'null');if(fs11ReceiptValid(q))FS11.receipt=q;}catch(_){}
function fs11Log(event,data={}){FS11.events.push({event,...data});if(FS11.events.length>180)FS11.events.shift();}
function fs11Enhanced(){return fs11ReceiptValid(FS11.receipt);}
function fs11Active(k){return !!(specialActive(k)&&special._fs11Level===2);}
function fs11IconKey(pk){return pk==='yuri'&&run._thunderStormUnlocked?'yuri_storm_icon_0919':PC_SPECIAL[pk].icon;}
function fs11ArtReady(pk){const key=fs11IconKey(pk),cell=BOFX.icons?.[key];
 const iconReady=XART.rdy(cell?(cell[4]||'nia_icons'):key),boxReady=XART.rdy('special_'+pk);
 return iconReady&&boxReady;
}
function fs11Warm(pk){fs11ArtReady(pk);}
// The old SPECIAL global let P2's pickup replace P1's active ability. Keep the
// existing seat window as the sole owner of both the timer and attached helpers.
if(!SEAT_RUN_FIELDS.includes('_chainLightningLevel'))SEAT_RUN_FIELDS.push('_chainLightningLevel');
run2._chainLightningLevel=run2._chainLightningLevel||1;
function fs11SeatBundle(){return {special,falva:falvaBalls,wreck:wreckBalls,storm:thunderStorm};}
function fs11SeatSet(q){special=q.special;falvaBalls=q.falva;wreckBalls=q.wreck;thunderStorm=q.storm;}
seatIn=function(n){const switched=FS11.base.seatIn.apply(this,arguments);if(switched){FS11.seatStash=fs11SeatBundle();fs11SeatSet(FS11.seat2);}return switched;};
seatOut=function(){if(_seat===2&&FS11.seatStash){FS11.seat2=fs11SeatBundle();fs11SeatSet(FS11.seatStash);FS11.seatStash=null;}return FS11.base.seatOut.apply(this,arguments);};
updateSpecial=function(dt){
 if(coopActive()&&_seat===1){for(const seat of seatList())withSeat(seat,()=>FS11.base.updateSpecial.call(this,dt));
  const freeze=[special,FS11.seat2.special].find(q=>q?.pilot==='freezer'&&q.t>0);
  if(freeze&&run.stage!==6)timeScale=freeze._fs11Level===2?.4:.5;
  return;
 }return FS11.base.updateSpecial.apply(this,arguments);
};
thunderStormTick=function(dt){
 if(coopActive()&&_seat===1){for(const seat of seatList())withSeat(seat,()=>FS11.base.stormTick.call(this,dt));return;}
 return FS11.base.stormTick.apply(this,arguments);
};
// These authored effects live outside drawPlayer's existing seat loop. Keep
// their original under/over passes, but render the attached helpers for both.
for(const name of ['drawFalvaAura','drawFalvaCharge','drawFalvaOrbs','drawFalvaBalls',
 'drawMavCoilUnder','drawMavCoilOver','drawWreckChains','drawWreckBalls','drawChargeFX','thunderStormDraw']){
 FS11.base.specialPaint[name]=window[name];
 window[name]=function(){const draw=FS11.base.specialPaint[name],args=arguments;
  if(coopActive()&&_seat===1){for(const seat of seatList().slice().reverse())withSeat(seat,()=>{if(!player.out)draw.apply(this,args);});return;}
  return draw.apply(this,args);
 };
}
startRun=function(from=1){
 FS11.boxes=[];FS11.proof=null;FS11.reward=null;FS11.seat2={special:null,falva:[],wreck:[],storm:null};
 FS11.pending=null;
 for(const seat of seatList())withSeat(seat,()=>fs11Warm(_pilotKey()));
 return FS11.base.start.apply(this,arguments);
};
beginStage=function(n){FS11.pending=null;FS11.boxes=[];FS11.proof=null;FS11.seat2={special:null,falva:[],wreck:[],storm:null};
 const r=FS11.base.begin.apply(this,arguments);
 return r;
};
setState=function(next){if(next===GS.TITLE||next===GS.PASSWORD){FS11.pending=null;FS11.boxes=[];FS11.proof=null;FS11.seat2={special:null,falva:[],wreck:[],storm:null};}return FS11.base.state.apply(this,arguments);};

startSpecial=function(){
 // End the previous window through its real cleanup before replacing it.
 if(special)endSpecial();const r=FS11.base.special.apply(this,arguments);
 if(!special)return r;special._fs11Level=fs11Enhanced()?2:1;
 if(!fs11Enhanced())return r;
 special.t=special.dur=20;const k=special.pilot;
 if(k==='cole'||k==='lizzie'){special.strikes+=2;run.bombs=special.strikes;}
 if(k==='yuri'){special._fs11ChainBefore=run._chainLightningLevel||1;run._chainLightningLevel=special._fs11ChainBefore+1;}
 if(k==='freezer'&&run.stage!==6){timeScale=.4;try{if(Snd.cur)Snd.cur.playbackRate=.4;}catch(_){} }
 pickupAnnounce(FS11_UPGRADES[k].name,_pilotTint());fs11Log('enhanced-special',{pilot:k});return r;
};
endSpecial=function(){const before=special;
 if(before?._fs11ChainBefore!=null)run._chainLightningLevel=before._fs11ChainBefore;
 return FS11.base.end.apply(this,arguments);
};
axelMegaReflect=function(q){const r=FS11.base.reflect.apply(this,arguments);if(r&&fs11Active('axel'))q._megaDamage*=1.5;return r;};
releaseHelix=function(){const first=pBullets.length,r=FS11.base.helix.apply(this,arguments);
 if(fs11Active('maverick'))for(const b of pBullets.slice(first)){b.dmg*=1.25;b._fs11Level=2;}return r;};
releaseRoller=function(){const first=rollers.length,r=FS11.base.roller.apply(this,arguments);
 if(fs11Active('falva'))for(const b of rollers.slice(first)){b.dmg*=1.25;b._fs11Level=2;}return r;};
wreckTick=function(dt){return FS11.base.wreck.call(this,dt*(fs11Active('juggernaut')?1.2:1));};
pcSpecial=function(pk){const q=FS11.base.card.apply(this,arguments);return fs11Enhanced()&&FS11_UPGRADES[pk]?{...q,name:FS11_UPGRADES[pk].name}:q;};
ph8Values=function(){const q=FS11.base.hud.apply(this,arguments);
 if(specialActive()&&special._fs11Level)q.name=q.pilot==='yuri'&&run._thunderStormUnlocked?'THUNDER STORM':SPECIAL_INFO[q.pilot].name;
 if(fs11Enhanced()&&FS11_UPGRADES[q.pilot]){
  if(specialActive()||!q.loans.length)q.name=q.pilot==='yuri'&&run._thunderStormUnlocked?'THUNDER STORM MK II':FS11_UPGRADES[q.pilot].name;
  if(!specialActive()&&!q.loans.length)q.detail='MK II UNLOCKED';
 }return q;};
ph8Icon=function(g,key,x,y,h){
 if(specialActive()&&special._fs11Level&&key===specialArtKey('spicon_'+run.pilot))key=fs11IconKey(run.pilot);
 return FS11.base.hudIcon.call(this,g,key,x,y,h);
};

spawnBoss=function(kind){const r=FS11.base.spawnBoss.apply(this,arguments);
 if(run.stage===6&&run._gp4StageX&&kind===(run._gp4StageX==='left'?'warhive':'rebelsquad')&&boss)
  FS11.proof={route:run._gp4StageX,kind,ref:boss};
 return r;};
function fs11UnlockFromStageX(){
 const P=FS11.proof;
 if(fs11Enhanced()||!P||run.stage!==6||run._gp4StageX!==P.route||!bossDefeated||!P.ref.dead||P.ref.hp>0)return false;
 FS11.receipt={version:1,stage:'X',route:P.route,boss:P.kind,earned:true,at:Date.now(),pilot:run.pilot,difficulty:diffKey};
 try{localStorage.setItem(FS11_KEY,JSON.stringify(FS11.receipt));}catch(_){}
 if(campaign.stageX1004)campaign.stageX1004.signatureMk2=true;
 FS11.reward={pilot:run.pilot};fs11Log('signature-mk2-unlocked',{route:P.route});return true;
}
ap10StageXReward=function(){fs11UnlockFromStageX();return FS11.base.reward.apply(this,arguments);};
scLeaveStage=function(){fs11UnlockFromStageX();return FS11.base.leave.apply(this,arguments);};
campSnapshot=function(){const q=FS11.base.snapshot.apply(this,arguments);if(fs11Enhanced())q.signatureMk2={...FS11.receipt};return q;};
campApply=function(s){const ok=FS11.base.apply.apply(this,arguments);if(ok&&fs11ReceiptValid(s?.signatureMk2)&&!fs11Enhanced()){
 FS11.receipt={...s.signatureMk2};try{localStorage.setItem(FS11_KEY,JSON.stringify(FS11.receipt));}catch(_){}
 }FS11.boxes=[];FS11.pending=null;FS11.proof=null;FS11.seat2={special:null,falva:[],wreck:[],storm:null};return ok;};
mapgBriefingDraw=function(info){
 if(FS11.reward&&AP10_X.reward){const saved=AP10_X.reward;AP10_X.reward=null;
  try{return FS11.base.brief.call(this,{key:'fs11-mk2',title:'STAGE X CLEAR - SIGNATURE MK II',
   body:'ALL NINE PILOT SPECIALS ENHANCED. 20 SECOND WINDOWS. YOUR NEXT SPECIAL PICKUP USES MK II. AIR SUPERIORITY SUPPLIES ALSO AWARDED.'});}
  finally{AP10_X.reward=saved;}
 }
 if(!fs11Enhanced()&&String(info?.key||'').startsWith('cf4-x-'))
  info={...info,body:info.body+' REWARD: SIGNATURE MK II FOR ALL NINE PILOTS.'};
 return FS11.base.brief.call(this,info);
};

rg4Init=function(b){const G=FS11.base.rebelInit.apply(this,arguments);
 for(const q of b._rebels.ships)if(q.rg4&&!q.rg4._fs11Own){q.rg4._fs11Own=true;q.rg4._fs11First=true;q.rg4.signature=FS11_REBELS[q.key];}
 return G;
};
ra4AttackKind=function(q,G){if(q.rg4._fs11First&&FS11_REBELS[q.key]){
 q.rg4._fs11First=false;if(q.key!=='rook')q.rg4.serial++;return FS11_REBELS[q.key].kind;
 }return FS11.base.rebelKind.apply(this,arguments);};
rg4Attack=function(q,R,G){const before=q.rg4?.act,labels=R.rf.callouts.length,r=FS11.base.rebelAttack.apply(this,arguments),A=q.rg4?.act;
 if(A&&A!==before&&FS11_REBELS[q.key]){
  A._fs11Name=A.kind===FS11_REBELS[q.key].kind?FS11_REBELS[q.key].name:(A.title||RA4_NAMES[A.kind]||RG4_NAMES[A.kind]||A.kind.toUpperCase());
  if(R.rf.callouts.length===labels)rf28Callout(R,A._fs11Name,q.x,q.y+62,RA4_COLORS[q.key],Math.min(2,A.warm||1.4),8);
  fs11Log('rebel-signature-start',{pilot:q.key,kind:A.kind,name:A._fs11Name});
 }return r;};
fr27RebelDrawShip=function(q){const r=FS11.base.rebelShip.apply(this,arguments),A=q.rg4?.act;
 if(!q.dead&&A?._fs11Name&&A.phase!=='recover'){
  const im=ra4Image('icon_'+q.key);if(im)ra4Blit(im,q.x-34,q.y-36,22,22);
  FS11.draws[q.key]=(FS11.draws[q.key]||0)+1;
 }return r;};
