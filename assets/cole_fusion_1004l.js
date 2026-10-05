'use strict';
/* Cole's authored VI/VII/VIII arsenal. Charge and collisions belong to simulation;
   drawing never changes charge, hit lists, fragments or the ship's physical position. */
const CF1004_BASE={tick:spaceBulletTick,draw:fusion30BulletDraw,shoot:pShoot,hold:Input.hold,
 scan:retinaScanHeld,play:updatePlay,bg:drawBG,world:drawWorld,player:drawPlayer,
 equip:drawEquipCorner,effects:drawEffects,begin:beginStage,start:startRun,snapshot:campSnapshot,apply:campApply};
const CF1004={clock:0,events:[],hits:0,effects:[]},CF1004_LIMIT=3.15,CF1004_MIN=.06;
// The seat swap must own even empty values; otherwise P2 inherits P1's last selection.
for(const field of ['_cfTier','_cfUnlocked']){
 if(!SEAT_RUN_FIELDS.includes(field))SEAT_RUN_FIELDS.push(field);
 for(const r of [run,run2])if(!(field in r))r[field]=field==='_cfTier'?null:0;
}
for(const s of Object.values(CF1004_ART.sheets))XART._src[s.key]=s.path;
function cf1004Warm(){for(const s of Object.values(CF1004_ART.sheets))XART.rdy(s.key);}
function cf1004Cell(name,t,x,y,w,h,angle=0,g=ctx){
 const a=CF1004_ART.reels[name];if(!a)return false;const s=CF1004_ART.sheets[a.sheet];if(!XART.rdy(s.key))return false;
 const r=a.frames[((Math.floor(t*a.fps)%a.frames.length)+a.frames.length)%a.frames.length];
 g.save();g.imageSmoothingEnabled=false;g.globalCompositeOperation='source-over';g.translate(x,y);g.rotate(angle);
 g.drawImage(XART.get(s.key),...r,-w/2,-h/2,w,h);g.restore();return true;
}
function cf1004Log(event,data={}){CF1004.events.push({event,...data});if(CF1004.events.length>100)CF1004.events.shift();}
function cf1004Percent(){return (player._fuse||0)/FUSE_FULL;}
function cf1004Primary(){return colePilot()&&run.weapon===0&&!spaceWeaponsActive();}
function cf1004Locked(){return h3Locked()&&!H3.demo&&fb2Talk?.beats?.[fb2Talk.i]?.kind!=='demo';}
function cf1004Cancel(){
 if(player._fuseSnd)Snd?.loopOff?.(player._fuseLoop||'fusionChargeLoop');
 player._fuse=0;player._fuseSnd=0;player._cfWarn=0;player._cfRumble=0;
}
function cf1004Unlocked(){return Math.min(8,Math.max(run._cfUnlocked||0,run.wlevels?.[0]||0,run.wlevels?.[7]||0,([0,7].includes(run.weapon)?run.wlevel:0)||0));}
function cf1004Cycle(){
 if(!colePilot()||![0,7].includes(run.weapon)||spaceWeaponsActive()||player.dead||h3Locked())return false;
 const max=cf1004Unlocked();if(max<6)return false;
 run._cfUnlocked=max;const tiers=[6,7,8].filter(n=>n<=max),old=run._cfTier||run.wlevel;
 const next=tiers[(tiers.indexOf(old)+1)%tiers.length];cf1004Cancel();
 run._cfTier=next;run._primary1003b='mg';run.weapon=0;run.wlevel=next;
 if(run.loadout?.includes(7))run.loadout=run.loadout.map(w=>w===7?0:w);
 player._mgMuzT=0;player.fireCd=.08;player._retinaScan=null;Audio.SFX.select?.();cf1004Warm();
 cf1004Log('equip',{tier:next});return true;
}
function cf1004Input(){
 const fire=CF1004_BASE.hold.call(Input,_seat,'fire'),scan=CF1004_BASE.scan(),chord=fire&&scan;
 if(chord&&!player._cfChordWas&&cf1004Cycle()){player._cfBlockFire=true;player._cfBlockScan=true;}
 player._cfChordWas=chord;if(!fire)player._cfBlockFire=false;if(!scan)player._cfBlockScan=false;
 if(colePilot()&&[0,7].includes(run.weapon))run._cfUnlocked=cf1004Unlocked();
 if(cf1004Primary()&&run._cfTier>=6&&run._cfTier<=cf1004Unlocked()){run.wlevel=run._cfTier;run.wlevels[0]=run._cfTier;}
}
Input.hold=function(seat,action){if(action==='fire'&&seatShip(seat)?._cfBlockFire)return false;return CF1004_BASE.hold.apply(this,arguments);};
retinaScanHeld=function(){return player?._cfBlockScan?false:CF1004_BASE.scan.apply(this,arguments);};
coleFuseTick=function(dt,firing){
 if(!cf1004Primary()||run.wlevel<8||player.dead||cf1004Locked()||player._cfBlockFire){cf1004Cancel();return false;}
 if(firing){
  if(!player._fuseSnd){player._fuseSnd=1;cf1004Warm();(Audio.SFX.chargeStart||Audio.SFX.select)?.();}
  player._fuse=(player._fuse||0)+Math.max(0,dt);const p=cf1004Percent();
  if(p>=CF1004_LIMIT-1e-8){cf1004Cancel();const G=rg4State(),shield=G?.shield;if(G)G.shield=0;
   try{playerHit('fusionOvercharge');}finally{if(G)G.shield=shield;}
   cf1004Log('overload',{percent:315,dead:player.dead});return true;}
  player._fuseLoop=Snd?.pools?.fusionChargeLoop?'fusionChargeLoop':'helixCharge';Snd?.loopOn?.(player._fuseLoop,.35+.55*Math.min(1,p/3));
  if(p>2){const heat=clamp(p-2,0,1.15);player._cfRumble=heat*3.5;shake=Math.max(shake,1+heat*8);
   player._cfWarn=(player._cfWarn||0)-dt;if(player._cfWarn<=0){player._cfWarn=p>=3?.1:.32-.18*heat;Audio.SFX.retinaCharge?.();}}
  return true;
 }
 const held=player._fuse||0;if(held>=CF1004_MIN)coleFuseRelease(held);cf1004Cancel();return held>0;
};
coleFuseRelease=function(charge){
 if(player.dead||cf1004Locked())return false;const held=charge??player._fuse??FUSE_FULL;
 const p=held>0?held/FUSE_FULL:1;if(p>=CF1004_LIMIT-1e-8){player._fuse=held;coleFuseTick(0,true);return false;}
 const scale=clamp(p,.35,3.14),nose=wm26PlayerNose();cf1004Warm();
 for(const side of [-1,1])pBullets.push({kind:'colefuse',_cfFusion:true,x:player.x+side*13,y:nose.y-12,
  cx:player.x+side*13,side,vy:-(780+scale*35),vx:0,w:14*scale,h:56*scale,dmg:FUSE_DMG*Math.max(.25,scale),
  scale,charge:p,pierce:true,t:0,life:1.65,_hit:[],_cfMemo:new Map(),seat:_seat});
 player.fireCd=.25;shake=Math.max(shake,2+scale*2);player._cfMuzzle={t:0,life:.18,scale};
 av3Sound('fusion_cannon',Math.min(1,.7+scale*.1),.12);cf1004Log('release',{percent:p*100,scale});return true;
};
/* The primary lanes keep their existing cadence/damage; only authored laser bodies replace pellets. */
pShoot=function(){const first=pBullets.length,laser=cf1004Primary()&&run.wlevel>=6&&run.wlevel<=7;
 const r=CF1004_BASE.shoot.apply(this,arguments);if(laser)for(let i=first;i<pBullets.length;i++){
  const b=pBullets[i];if(b.kind==='mg'){b._cfLaser=run.wlevel;b.w=7;b.h=28;}
 }return r;
};
coleTriDraw=function(b){return cf1004Cell((b.lv||6)>=7?'black':'yellow',CF1004.clock+(b.t||0),b.x,b.y,9,30,Math.atan2(b.vy,b.vx)+Math.PI/2);};
// Cloak prevents acquisition, not physical gunfire. These bodies belong only to
// Fusion collision; adding them to spaceTargets would also expose missile locks.
function cf1004Targets(){
 const targets=spaceTargets(),R=boss?._rebels;
 if(!boss||!bossActive||boss.dead||boss._noHit||!R?.frIntro?.done||rg4State()?.scene)return targets;
 for(const q of R.ships)if(q.frCloak>0&&!q.dead&&q.mode!=='entry'&&!(q.warp>0)){
  if(!q._cfBody)q._cfBody={_cfOwner:boss,_cfShip:q,_cfId:q.key+'-hull',w:62,h:70,
   get x(){return q.x;},get y(){return q.y;},get dead(){return q.dead;}};
  targets.push(q._cfBody);
 }return targets;
}
function cf1004Owner(t){return t._retinaOwner||t._cfOwner||t;}
function cf1004Id(t){return t._retinaId||t._cfId||'hull';}
function cf1004Damage(t,dmg,b){
 if(!t._cfShip)return spaceDamageTarget(t,dmg,b);
 const own=t._cfOwner,q=t._cfShip;
 if(own!==boss||own.dead||own._noHit||q.dead||q.mode==='entry'||q.warp>0||rg4State()?.scene)return;
 own._rebels.hit=q.i;own._rebels.frHit=null;
 spaceDamageTarget(own,dmg,{...b,x:q.x,y:q.y});
}
function cf1004Memo(b,t){const owner=cf1004Owner(t),key=cf1004Id(t);let set=b._cfMemo.get(owner);if(!set)b._cfMemo.set(owner,set=new Set());
 if(set.has(key))return false;set.add(key);b._hit.push(t);return true;}
function cf1004Contact(b,t){
 if(!t||t.dead||t._dyingT!=null||t._noHit||t._retinaOwner?._noHit)return false;const y=spaceTargetY(t);
 if(Math.abs(t.x-b.x)>((t._drawW||t.w||28)+b.w)/2||Math.abs(y-b.y)>((t._drawH||t.h||28)+b.h)/2)return false;
 if(t._retinaOwner&&!retinaTargetValid(t))return false;
 if(t===boss&&!bossHitTest(b.x,b.y)&&!bossHitTest(t.x,y))return false;
 if(t===subBoss&&subBossSolidAt(t.x,y)===false)return false;return true;
}
function cf1004Splash(b,x,y,primary){
 const radius=35+17*b.scale,seen=new Set();for(const t of cf1004Targets()){
  if(t.dead||t._dyingT!=null||t._noHit||t._retinaOwner?._noHit||t._retinaOwner&&!retinaTargetValid(t))continue;
  const owner=cf1004Owner(t);if(owner===cf1004Owner(primary)||seen.has(owner))continue;
  if(Math.hypot(t.x-x,spaceTargetY(t)-y)<=radius){seen.add(owner);cf1004Damage(t,b.dmg*.23,b);}
 }
}
function cf1004Impact(b,t,x=b.x,y=spaceTargetY(t)){
 // Impact art is not ordnance: bullet consumers must never damage crates with it.
 CF1004.hits++;CF1004.effects.push({kind:'colefusionfx',x,y,w:46+20*b.scale,h:46+20*b.scale,t:0,life:.32});
 if(CF1004.effects.length>96)CF1004.effects.shift();
 if(!b._cfChild){cf1004Splash(b,x,y,t);
  const live=pBullets.filter(q=>!q.dead&&q._cfChild).length;
  if(live<100){const count=8;for(let i=0;i<count;i++){const a=i*TAU/count+.14;
   pBullets.push({kind:'colefragment',_cfChild:true,x,y,vx:Math.cos(a)*290,vy:Math.sin(a)*290,w:8,h:18,dmg:b.dmg*.14,
    scale:b.scale,seat:b.seat,t:0,life:.55,_hit:[],_cfMemo:new Map([[cf1004Owner(t),new Set([cf1004Id(t)])]])});}
   for(const side of [-1,1])pBullets.push({kind:'colefuse',_cfFusion:true,_cfChild:true,x,y,vx:side*410,vy:-280,w:10*b.scale,h:32*b.scale,
    dmg:b.dmg*.25,scale:b.scale,seat:b.seat,t:0,life:.4,pierce:true,_hit:[],_cfMemo:new Map([[cf1004Owner(t),new Set([cf1004Id(t)])]])});
  }
 }
 av3Sound('impact_energy',.8,.055);Audio.SFX.helixBurst?.();
}
function cf1004BulletTick(b,dt){
 if(b.kind==='colefusionfx'){b.t+=dt;if(b.t>=b.life)b.dead=true;return true;}
 if(!b._cfFusion&&b.kind!=='colefragment')return false;if(b.dead)return true;
 b.t+=dt;b.life-=dt;const n=Math.max(1,Math.ceil(Math.hypot(b.vx||0,b.vy||0)*dt/12)),step=dt/n;
 for(let i=0;i<n&&!b.dead;i++){
  b.y+=(b.vy||0)*step;if(b._cfChild)b.x+=(b.vx||0)*step;
  else b.x=b.cx+Math.sin((b.t-dt+(i+1)*step)*32+(b.side>0?Math.PI:0))*(2+Math.min(8,b.scale*2.5));
  for(const t of cf1004Targets())if(cf1004Contact(b,t)&&cf1004Memo(b,t)){
   cf1004Damage(t,b.dmg,b);cf1004Impact(b,t,b.x,clamp(spaceTargetY(t),b.y-b.h/2,b.y+b.h/2));
   if(b.kind==='colefragment'){b.dead=true;break;}
  }
  if(!b._cfChild)for(const q of eBullets){if(q.dead||!enemyOrdnanceCanIntercept(q))continue;
   if(Math.abs(q.x-b.x)<(b.w+(q.w||8))/2&&Math.abs(q.y-b.y)<(b.h+(q.h||12))/2){ordnanceBreak1002(q);q.dead=true;cf1004Impact(b,q,b.x,q.y);}}
 }
 if(b.life<=0||b.y+b.h/2<viewTopY()-45||b.y-b.h/2>VH+60||b.x<camLeftX()-130||b.x>camRightX()+130)b.dead=true;
 return true;
}
spaceBulletTick=function(b,dt){return cf1004BulletTick(b,dt)||CF1004_BASE.tick.apply(this,arguments);};
fusion30BulletDraw=function(b){
 if(b._cfLaser)return cf1004Cell(b._cfLaser>=7?'black':'yellow',CF1004.clock,b.x,b.y,7,28);
 if(b._cfFusion)return cf1004Cell('fusion',b.t*1.6,b.x,b.y,b.w,b.h,b._cfChild?Math.atan2(b.vy,b.vx)+Math.PI/2:0);
 if(b.kind==='colefragment')return cf1004Cell('fragment',b.t,b.x,b.y,9,20,Math.atan2(b.vy,b.vx)+Math.PI/2);
 if(b.kind==='colefusionfx')return cf1004Cell('impact',Math.min(3,Math.floor(b.t/.32*4))/18,b.x,b.y,b.w,b.h);
 return CF1004_BASE.draw.apply(this,arguments);
};
drawEffects=function(){const r=CF1004_BASE.effects.apply(this,arguments);for(const f of CF1004.effects)fusion30BulletDraw(f);return r;};
coleFuseDraw=function(b){return b._cfFusion?fusion30BulletDraw(b):fb2BeamDraw(b.x,b.y,b.w*1.35,b.h*1.15,CF1004.clock);};
drawColeCharge=function(){
 if(!cf1004Primary()||player.dead)return;const p=cf1004Percent(),m=player._cfMuzzle;
 if(m)for(const side of [-1,1])cf1004Cell('muzzle',m.t,player.x+side*13,wm26PlayerNose().y-7,22+m.scale*8,32+m.scale*8);
 if(p<=0)return;cf1004Cell('charge',CF1004.clock*(1+p*.32),player.x,player.y,72+Math.min(p,3)*8,94+Math.min(p,3)*9);
 const w=104,x=player.x-w/2,y=Math.max(PLAY.y+20,player.y-63),blink=Math.floor(CF1004.clock*12)%2;
 ctx.save();ctx.fillStyle='#130920';ctx.fillRect(x-2,y-2,w+4,10);ctx.fillStyle=p>=3?(blink?'#fff':'#ff2349'):p>2?'#ff48d5':'#bd71ff';ctx.fillRect(x,y,w*Math.min(1,p/CF1004_LIMIT),6);
 ctx.fillStyle='#f2dcff';for(const k of [1,2,3])ctx.fillRect(x+w*k/CF1004_LIMIT,y,1,6);ctx.restore();
 campText('FUSION '+Math.floor(p*100+1e-7)+'%',player.x,y-8,8,'#fff1fc');
 if(p>=3)campText('RELEASE!',player.x,y+18,10,blink?'#ffffff':'#ff2349');
};
drawPlayer=function(){const p=cf1004Primary()?player._cfRumble||0:0;if(!p||player.dead)return CF1004_BASE.player.apply(this,arguments);
 ctx.save();ctx.translate(Math.sin(CF1004.clock*83)*p,Math.cos(CF1004.clock*97)*p*.65);try{return CF1004_BASE.player.apply(this,arguments);}finally{ctx.restore();}
};
drawBG=function(dt){const r=CF1004_BASE.bg.apply(this,arguments);let heat=0;for(const seat of seatList())withSeat(seat,()=>{if(cf1004Primary()&&!player.dead)heat=Math.max(heat,cf1004Percent()-2);});
 if(heat>0){const on=Math.floor(CF1004.clock*(3+heat*2))%2;ctx.save();ctx.fillStyle='rgba(255,24,178,'+(on?.13+Math.min(heat,1.15)*.13:.025)+')';ctx.fillRect(camLeftX(),viewTopY(),viewW(),viewH());ctx.restore();}return r;
};
drawWorld=function(dt){const r=CF1004_BASE.world.apply(this,arguments);let danger=false;for(const seat of seatList())withSeat(seat,()=>{if(cf1004Primary()&&!player.dead&&cf1004Percent()>2)danger=true;});
 if(danger&&Math.floor(CF1004.clock*6)%2)campText('DANGER! OVERCHARGE ALERT!',VW/2,120,11,'#ff263e');return r;
};
drawEquipCorner=function(){if(!cf1004Primary()||run.wlevel<6)return CF1004_BASE.equip.apply(this,arguments);
 const {x,y,w,h}=bottomHudLayout().equip,im=XART.rdy('hud_equip_frame_0924')?XART.get('hud_equip_frame_0924'):null;
 if(im){ctx.save();ctx.globalAlpha=.25;ctx.drawImage(im,108,110,1320,760,x,y,w,h);ctx.restore();}
 const n=run.wlevel,name=n>=8?'FUSION':n>=7?'BLACK + HOMING':'YELLOW LASER';campText(name,x+w/2,y+10,6,'#eef3ff');
 cf1004Cell(n>=8?'fusion':n>=7?'black':'yellow',CF1004.clock,x+w/2,y+32,n>=8?14:10,27);campText('L'+n,x+w-14,y+h-6,7,'#ffd36c');
};
updatePlay=function(dt){CF1004.clock+=Math.max(0,dt);
 for(const f of CF1004.effects)f.t+=Math.max(0,dt);CF1004.effects=CF1004.effects.filter(f=>f.t<f.life);
 for(const seat of seatList())withSeat(seat,cf1004Input);
 const r=CF1004_BASE.play.apply(this,arguments);for(const seat of seatList())withSeat(seat,()=>{
  if(player._cfMuzzle){player._cfMuzzle.t+=dt;if(player._cfMuzzle.t>=player._cfMuzzle.life)player._cfMuzzle=null;}
  if(player.dead){run._cfTier=null;run._cfUnlocked=0;}
  if(player.dead||!cf1004Primary()||run.wlevel<8)cf1004Cancel();
 });return r;
};
beginStage=function(){CF1004.effects=[];const r=CF1004_BASE.begin.apply(this,arguments);for(const seat of seatList())withSeat(seat,()=>{cf1004Cancel();player._cfMuzzle=null;player._cfChordWas=player._cfBlockFire=player._cfBlockScan=false;});cf1004Warm();return r;};
startRun=function(){for(const r of [run,run2]){r._cfTier=null;r._cfUnlocked=0;}CF1004.effects=[];return CF1004_BASE.start.apply(this,arguments);};
campSnapshot=function(){const s=CF1004_BASE.snapshot.apply(this,arguments);s.coleLaserTier=run._cfTier||null;s.coleLaserUnlocked=run._cfUnlocked||0;return s;};
campApply=function(s){const r=CF1004_BASE.apply.apply(this,arguments);if(r){
 const earned=Math.min(8,Math.max(0,run.wlevels?.[0]||0,run.wlevels?.[7]||0));
 const saved=s.coleLaserUnlocked;
 run._cfUnlocked=Number.isInteger(saved)&&saved>=0&&saved<=8?Math.max(earned,saved):earned;
 run._cfTier=[6,7,8].includes(s.coleLaserTier)&&s.coleLaserTier<=run._cfUnlocked?s.coleLaserTier:null;
 cf1004Cancel();CF1004.effects=[];
 }return r;};
