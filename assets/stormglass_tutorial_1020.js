'use strict';
/* Stormglass Academy: a tutorial-only course, never an eleventh campaign stage.
   Native ships, weapons, hit/death renderers, Retina, warnings and mixer remain owners. */
const SG20={key:'sg20_stormglass',width:680,speed:28,draws:0,base:{
 start:tutStart,finish:tutFinish,cleanup:tutCleanup,ask:tutAskOpen,rows:tutAskRows,
 intro:drawIntro,bg:drawBG,width:worldWidth,update:updatePlay,next:tutNext,
 overlay:tutOverlayDraw,shoot:tutShoot,spawn:tutSpawn,hold:tutHoldStage,scan:retinaScanFire,warning:combatWarningDraw,
 warmStage,load:stageLoadBegin,purge:tutPurge
}};
XART._src[SG20.key]='assets/game/levels/tutorial/stormglass_1020/architecture.webp';
const SG20_CLOUDS=Array.from({length:6},(_,i)=>'nl6c_low_rolling_bank_'+i);
function sg20State(){return tutLive()?TUT._sg:null;}
function sg20Warm(){XART.rdy(SG20.key);UI20.warm();
 for(const k of ['bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall','nbret_'+tutLeadKey()])XART.rdy(k);
 XART.rdy(SG20_WATER.key);for(const k of SG20_CLOUDS)XART.rdy(k);
 if(!SG20.audioWarm){SG20.audioWarm=true;Snd.prepare(['enemyMachineGunLight','hit','select','unlock','missile','retinaCharge']);}
}
function sg20Keys(){const keys=[SG20.key,SG20_WATER.key,...UI20_KEYS,'nbret_'+run.pilot,
 'fb2_dispatch_'+(TUT?.disp||tutDispatcher(run.pilot)),'bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall',
 'nca_en_s1','nca_eproj_s1','nca_s1combatfx','nca_player_weapons','nca_pickups','nca_fx_explosions','nca_fx_misc','nca_fx_debris',
 'bof_player_weapon_special_icons_atlas','bof_player_ordnance_projectiles_atlas'];
 for(const k of Object.keys(XART._src))if(k.startsWith('nl6c_low_rolling_bank_'))keys.push(k);
 return keys;
}
warmStage=function(n){if(tutLive()){sg20Warm();return SG20.base.load.call(this,1,sg20Keys());}
 return SG20.base.warmStage.apply(this,arguments);};
tutAskOpen=function(){const r=SG20.base.ask.apply(this,arguments);sg20Warm();
 if(tutAsk&&!tutStoreRead().stormglassDone){tutAsk.seen=false;tutAsk.sel=0;}return r;};
tutAskRows=function(){const rows=SG20.base.rows();rows[0]='YES - FLY STORMGLASS ACADEMY';return rows;};
tutStart=function(){const r=SG20.base.start.apply(this,arguments);
 if(TUT){TUT._sg={time:0,travel:0,multiFlights:0,volleys:0,phase:'FLIGHT DECK',completed:[]};sg20Warm();}
 return r;};
worldWidth=function(){return tutLive()?SG20.width:SG20.base.width.apply(this,arguments);};
function sg20LayersReady(){return XART.rdy(SG20.key)&&XART.rdy(SG20_WATER.key)&&SG20_CLOUDS.every(k=>XART.rdy(k));}
function sg20Clouds(t,w,top,near,screen){
 const h=VH-top,count=near?2:3,scale=near?1.15:1.6,speed=near?39:15,parallax=near?.82:.36;
 ctx.save();ctx.globalAlpha=near?.18:.14;
 for(let i=0;i<count;i++){
  const key=SG20_CLOUDS[(Math.floor(t*2.2)+i*2)%6];if(!XART.rdy(key))continue;
  const im=XART.get(key),cw=im.naturalWidth*scale,ch=im.naturalHeight*scale,span=h+ch;
  const y=top+((t*speed+i*span/count)%span)-ch;
  const x=(i%2?w*.78:w*.08)-cw/2+(screen?0:camX*(1-parallax))+Math.sin(t*.08+i)*20;
  ctx.drawImage(im,Math.round(x),Math.round(y),cw,ch);
 }ctx.restore();
}
function sg20Terrain(screen=false){
 const S=sg20State(),clock=S?S.travel:0,t=S?S.time:stateT,w=screen?VW:SG20.width;
 const top=screen?0:viewTopY(),bottom=VH;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.fillStyle='#06313c';ctx.fillRect(0,top,w,bottom-top);
 const waterFrame=Math.floor(t*SG20_WATER.fps)%SG20_WATER.frames;
 if(XART.rdy(SG20_WATER.key)){
  const sheet=XART.get(SG20_WATER.key),cell=SG20_WATER.cells[waterFrame],tw=SG20_WATER.width,th=SG20_WATER.height;
  const x0=(screen?0:camX*.76)%tw-tw,y0=top+(t*10)%th-th;
  for(let y=y0;y<bottom;y+=th)for(let x=x0;x<w;x+=tw)
   ctx.drawImage(sheet,...cell,Math.floor(x),Math.floor(y),tw,th);
  SG20.waterFrame=waterFrame;SG20.waterDraws=(SG20.waterDraws||0)+1;
 }
 sg20Clouds(t,w,top,false,screen);
 if(XART.rdy(SG20.key)){
  const im=XART.get(SG20.key),h=im.naturalHeight*w/im.naturalWidth;
  let y=bottom-h+(clock%h);while(y>top)y-=h;
  for(;y<bottom;y+=h)ctx.drawImage(im,0,Math.round(y),w,h+1);
  SG20.draws++;
 }sg20Clouds(t,w,top,true,screen);
 SG20.layers={ocean:t*10,farCloud:t*15,academy:clock,nearCloud:t*39};ctx.restore();
}
drawBG=function(){if(tutLive())return sg20Terrain();return SG20.base.bg.apply(this,arguments);};
combatWarningDraw=function(owner,q){return SG20.base.warning.call(this,owner,tutLive()?{...q,fieldOnly:true}:q);};
drawIntro=function(dt){
 if(!tutLive())return SG20.base.intro.apply(this,arguments);
 sg20Warm();sg20Terrain(true);
 ctx.fillStyle='#02101cba';ctx.fillRect(0,VH*.27,VW,VH*.41);
 msgText('STORMGLASS',VW/2,VH*.35,30,'#f0fff6',0,1,.06);
 msgText('ACADEMY',VW/2,VH*.42,24,'#7befe8',0,1,.06);
 helpLabel('CLASSIFIED OFFSHORE FLIGHT COURSE',VW/2,VH*.51,11,'#ffd36b');
 helpLabel('REAL CONTROLS. SAFE LIVE-FIRE TRAINING.',VW/2,VH*.57,10,'#d5eef2');
 const ready=sg20LayersReady()&&stageLoadReady(1);
 helpLabel(ready?'FLIGHT DECK CLEAR':'PREPARING THE COURSE',VW/2,VH*.64,11,ready?'#8dffa4':'#ffd36b');
 if(!TUT.music&&ready){TUT.music=true;Audio.startMusic(curStage.music||'stage');}
 if(stateT>=3.1&&ready){
  player.x=SG20.width/2;player.y=PLAY.y+PLAY.h-65;camX=Math.max(0,(SG20.width-viewW())/2);
  tutHoldStage();setState(GS.PLAY);Input.clearTaps?.();
 }
};
tutTop=function(){return PLAY.y+208;};
tutHoldStage=function(){SG20.base.hold();stageTimer=0;bossActive=false;subBossActive=false;
 // A separate visual clock lets the academy cruise forever without firing campaign triggers.
 boss=null;subBoss=null;
};
tutSpawn=function(type,x,y,hp,opt){const e=SG20.base.spawn.apply(this,arguments);if(e){
 // Training armor is fixed across difficulty modes; no random native shield or HP multiplier.
 e._esh=null;e._sgTrainer=true;e.score=0;
 }return e;};
tutShoot=function(x,y,ang,spd){
 const before=eBullets.length;SG20.base.shoot(x,y,ang,spd);
 for(let i=before;i<eBullets.length;i++){
  const b=eBullets[i],v=Math.hypot(b.vx,b.vy)||1;b.vx*=spd/v;b.vy*=spd/v;b._tut=1;
 }if(sg20State())sg20State().volleys++;
};
retinaScanFire=function(){const S=player._retinaScan,old=S?.queue;
 const r=SG20.base.scan.apply(this,arguments),q=player._retinaScan?.queue;
 if(sg20State()&&q&&q!==old&&q.targets.length>=2)sg20State().multiFlights++;
 return r;};
tutClearField=function(keepTargets){
 if(!keepTargets)for(const e of enemies)if(e._tut&&!e.dead)e.dead=true;
 eBullets.length=0;pBullets.length=0;powerups.length=0;
 if(typeof groundTargetingFx!=='undefined')for(const q of groundTargetingFx)q.dead=true;
 retina.target=null;retina.phase=null;retinaScanClear();
};
tutPurge=function(){SG20.base.purge();
 if(tutLive()&&!['crate','special'].includes(TUT.L?.def.id))powerups.length=0;
};
tutNext=function(){
 if(TUT?._sg&&TUT.L)TUT._sg.completed.push({id:TUT.L.def.id,hits:TUT.L.hit||0,time:TUT.lt});
 return SG20.base.next.apply(this,arguments);
};
updatePlay=function(dt){
 const S=sg20State();if(S){const elapsed=Math.min(.05,Math.max(0,dt));S.time+=elapsed;S.travel+=elapsed*SG20.speed;
  tutHoldStage();}
 const r=SG20.base.update.apply(this,arguments);
 if(sg20State()){
  tutHoldStage();
  // Tutorial cannot spend a real credit or award campaign score/armory currency.
  run.score=0;
  if(TUT.L&&TUT.lt>16&&!TUT.done&&TUT.L.def.retry)TUT.L.def.retry(TUT.L);
 }return r;
};
tutFinish=function(completed){
 if(completed&&TUT?._sg){const s=tutStoreRead();s.stormglassDone=true;
  s.stormglass={hits:TUT.hits,seconds:Math.round(TUT.t),grade:sg20Grade(),pilot:run.pilot};tutStoreWrite(s);}
 return SG20.base.finish.apply(this,arguments);
};
tutCleanup=function(){const r=SG20.base.cleanup.apply(this,arguments);pBullets.length=0;
 retinaScanClear();return r;};
function sg20Grade(){return TUT.hits===0?'ACE':TUT.hits<=4?'FLIGHT READY':'QUALIFIED';}
function sg20Text(id,text){const d=TUT_LESSONS.find(l=>l.id===id);if(d)d.text=typeof text==='function'?text:()=>text;return d;}
sg20Text('move',()=> 'WELCOME TO STORMGLASS, '+tutPilotName()+'. MOVE WITH YOUR FLIGHT CONTROLS. TOUCH ALL FOUR GUIDANCE BEACONS. TAKE YOUR TIME.');
sg20Text('fire',()=> 'HOLD FIRE - '+tutKey('fire')+'. YOUR GUN NEVER RUNS DRY. LINE UP BELOW THESE FOUR TRAINING DRONES.');
sg20Text('crate','SHOOT THE SUPPLY CRATE, THEN COLLECT THE WEAPON. PICKING UP THE SAME GUN AGAIN INCREASES ITS LEVEL.');
sg20Text('roll','DOUBLE-TAP LEFT OR RIGHT TO BARREL ROLL. YOU ARE INVULNERABLE DURING THE ROLL. THE HUD BAR SHOWS ITS RECHARGE.');
sg20Text('somer','DOUBLE-TAP UP TO SOMERSAULT. THE LOOP PROTECTS YOU AND RETURNS YOU TO YOUR STARTING POSITION. WATCH ITS OWN RECHARGE BAR.');
sg20Text('missile',()=> 'PRESS '+tutKey('bomb')+' TO FIRE A MANUAL MISSILE. LINE UP WITH THE ARMORED TARGET. THE HUD SHOWS YOUR MISSILE STOCK.');
sg20Text('retina',()=> 'TAP '+tutKey('retina')+' TO ACQUIRE A RETINA LOCK. WHEN IT LOCKS, PRESS '+tutKey('bomb')+' TO SEND A MISSILE TO THAT TARGET.');
sg20Text('warn','GREEN: AIMING. YELLOW: AIM COMMITTED. RED: FIRING. LEAVE THE COLORED LANE BEFORE RED. PRACTICE TWO CLEAN DODGES.');
sg20Text('strike','GROUND RETICLES FOLLOW YOU WHILE GREEN, THEN COMMIT. MOVE CLEAR AS THEY TURN YELLOW. PRACTICE THREE SAFE ESCAPES.');
sg20Text('special',()=> 'YOUR SPECIAL: '+tutSpecialName()+'. SHOOT THE RED CRATE, THEN COLLECT THE PICKUP. YOUR HUD TRACKS ITS TIMER.');
sg20Text('brief1','BOSS ELEMENTS CAN BE FUSED INTO WEAPONS AT THE FORGE. FIRE BEATS ICE; ICE BEATS FIRE. MATCHING AN ENEMY ELEMENT DOES LESS DAMAGE.');
sg20Text('brief2',()=>{
 const v=ui20Seat(1);return 'YOUR LOADOUT: '+v.primary+'. SECONDARY: '+v.secondary+'. CHECK HELP FOR PILOT-SPECIFIC CONTROLS. SHIELDS ABSORB HITS; SCORE EARNS ARMORY POINTS.';
});
const SG20_MULTI={id:'multi',good:'WING LOCKED',
 text:()=> 'RELEASE FIRE. HOLD '+tutKey('multilock')+' TO LOCK TWO DRONES, THEN PRESS '+tutKey('bomb')+'. MULTI-LOCK SPENDS A MISSILE FOR EACH TARGET.',
 start(L){L.base=sg20State().multiFlights;run.bombs=Math.max(6,run.bombs);sg20MultiTargets(L);},
 obj:L=>{const n=(player._retinaScan?.marks||[]).filter(m=>m.phase==='locked').length;return n>=2?'TWO LOCKS - FIRE A MISSILE':'HOLD MULTI-LOCK - '+Math.min(2,n)+' / 2';},
 tick(L){if(sg20State().multiFlights>L.base)return true;
  if(tutAlive(L.units).length<2)sg20MultiTargets(L);if(run.bombs<2)run.bombs=6;return false;}
};
function sg20MultiTargets(L){tutClearField();const F=tutField();
 L.units=[.34,.66].map(k=>tutSpawn('s1jetDelta',F.L+F.W*k,tutTop()+24,160,{amp:3})).filter(Boolean);
}
TUT_LESSONS.splice(TUT_LESSONS.findIndex(l=>l.id==='warn'),0,SG20_MULTI);
const SG20_EXAM=TUT_LESSONS.find(l=>l.id==='exam');
Object.assign(SG20_EXAM,{
 text:()=> 'SURPRISE: THE ACADEMY HAS AN ACE! FIRST CLEAR TWO ESCORT WAVES, THEN DEFEAT THE INSTRUCTOR DRONE. USE THE WARNINGS AND YOUR FULL LOADOUT.',
 start(L){L.wave=0;L.units=[];L.gap=0;run.bombs=Math.max(8,run.bombs);sg20ExamWave(L);},
 obj:L=>'GRADUATION '+Math.min(3,L.wave)+' / 3 - '+(L.wave===3?'INSTRUCTOR DRONE':'ESCORTS '+tutAlive(L.units).length),
 tick(L,dt){
  let alive=tutAlive(L.units);if(!alive.length){L.gap+=dt;if(L.gap<1.3)return false;if(L.wave>=3)return true;sg20ExamWave(L);alive=tutAlive(L.units);}
  L.age+=dt;L.fireT-=dt;
  // Only one shooter at a time. Open side lanes and a long commitment window survive all modes.
  if(L.wave<3){if(L.fireT<=0){L.fireT=1.7;const e=alive[L.shot++%alive.length];
    tutShoot(e.x,e.y+20,Math.atan2(player.y-e.y,player.x-e.x),2.4);}return false;}
  const e=alive[0],F=tutField();if(!e)return false;
  e._tutHold.x=F.cx+Math.sin(L.age*.6)*F.W*.23;
  if(!L.c)L.c={t:-1.1,x:player.x,fired:0};
  const C=L.c;C.t+=dt;if(C.t<0)return false;
  if(C.t<1)C.x+=clamp(player.x-C.x,-110*dt,110*dt);
  if(C.t<3){combatWarningTick(e,'sg20-ace',C.t,3);return false;}
  if(C.fired<5&&C.t>=3+C.fired*.14){
   const a=Math.atan2(PLAY.y+PLAY.h-e.y,C.x-e.x);
   for(const offset of [-.10,0,.10])tutShoot(e.x,e.y+22,a+offset,3.0);
   C.fired++;}
  if(C.t>4.8)L.c=null;return false;
 },
 draw(L){const e=tutAlive(L.units)[0],C=L.c;if(L.wave===3&&e&&C&&C.t>=0&&C.t<3)
  combatWarningDraw(e,{x:e.x,y:e.y+20,ex:C.x,ey:PLAY.y+PLAY.h+20,progress:C.t/3,width:54});}
});
function sg20ExamWave(L){
 tutClearField();L.wave++;L.gap=0;L.age=0;L.fireT=1.8;L.shot=0;L.c=null;
 const F=tutField(),ace=L.wave===3;
 L.units=(ace?[.5]:L.wave===1?[.3,.7]:[.22,.5,.78]).map(k=>
  tutSpawn(ace?'s1jetBomber':'s1jetDelta',F.L+F.W*k,tutTop()+35,ace?220:L.wave===1?35:45,{amp:ace?4:12})).filter(Boolean);
}
TUT_LESSONS.push({id:'debrief',info:true,good:'',
 text:()=> 'STORMGLASS CLEAR. RATING: '+sg20Grade()+'. TRAINING HITS: '+TUT.hits+'. YOUR REAL LIVES ARE SAFE. THE NEXT TAKEOFF BEGINS YOUR OPERATION. GOOD HUNTING, '+tutPilotName()+'.'
});
tutOverlayDraw=function(){
 const T=TUT;if(!T?.L)return;const D=T.L.def,S=sg20State();
 if(D.draw)tutWorldDraw(()=>D.draw(T.L));
 const full=T.say||T.text;if(T._fullKey!==full){T._fullKey=full;T.typed=0;}
 const x=12,y=PLAY.y+5,pw=VW-24,ph=100;
 const who=T.disp.toUpperCase(),shown=Math.min(full.length,Math.floor(T.typed||0)),port='fb2_dispatch_'+T.disp;
 const panel=ui20Panel(who,x,y,pw,ph,true);
 if(panel){msgFaceUse('dialogue');const content=ui20PanelContents(who,full,shown,port,panel,12,14);msgFaceUse(null);
  UI20.dialogue={who,x,y,w:pw,h:ph,full:full.length,shown,...content};}
 ctx.fillStyle='#02111eea';ctx.fillRect(x,y+ph+2,pw,43);
 const label=T.done>0&&D.good?D.good:D.info?'PRESS FIRE TO CONTINUE':D.obj?D.obj(T.L):'';
 helpLabel(label,VW/2,y+ph+14,12,T.done>0?'#9dffac':'#ffe5a0');
 helpLabel('STORMGLASS '+(T.i+1)+' / '+TUT_LESSONS.length+'  -  PAUSE TO SKIP',VW/2,y+ph+32,9,'#a5c9d0');
 if(T.flash)helpLabel('TRAINING HIT - LIVES PROTECTED',VW/2,PLAY.y+PLAY.h*.78,11,'#ffb799');
 if(S)S.phase=T.i<4?'FLIGHT DECK':T.i<10?'LIVE-FIRE CHANNEL':T.i<14?'TACTICAL RANGE':'GRADUATION';
};
window.BOFSTORMGLASS={name:'Stormglass Academy',get live(){return sg20State();},warm:sg20Warm,
 get artReady(){return sg20LayersReady();},get lessons(){return TUT_LESSONS.map(l=>l.id);}};
// Keep the public tutorial itinerary current for replay tools and accessibility inspectors.
BOFTUTORIAL.lessons=TUT_LESSONS.map(l=>l.id);
