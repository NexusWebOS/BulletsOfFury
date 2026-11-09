'use strict';
/* A short, safe mechanics flight. Native controls, targets, pickups, warnings and
   campaign handoff remain owners; the academy/exam/BOB itinerary is retired. */
const TS109={base:{update:updatePlay,start:tutStart,intro:drawIntro,hold:tutHold,jet:jetTick,flightEligible:gf113Eligible},revision:1,completed:[]};
const ts109Old=new Map(TUT_LESSONS.map(d=>[d.id,d]));
function ts109Bind(action){
 const keys=keybind[action]||[],k=action==='bomb'&&keys.includes(' ')?' ':keys.find(k=>k.startsWith('mouse'))||keys.find(k=>!k.startsWith('pad'))||keys[0];
 const mouse={mouse0:'LEFT CLICK',mouse2:'RIGHT CLICK',mouse3:'MOUSE 4',mouse4:'MOUSE 5'};
 return mouse[k]||(typeof HELP_KEYNAME!=='undefined'&&HELP_KEYNAME[k])||(k===' '?'SPACE':String(k||action).toUpperCase());
}
function ts109Keys(){return [SG20_WATER.key,...UI20_KEYS,'nbret_'+run.pilot,
 'fb2_dispatch_'+(TUT?.disp||tutDispatcher(run.pilot)),
 'bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall',
 'nca_en_s1','nca_eproj_s1','nca_s1combatfx','nca_player_weapons','nca_pickups',
 'nca_fx_explosions','nca_fx_misc','nca_fx_debris',
 'bof_player_weapon_special_icons_atlas','bof_player_ordnance_projectiles_atlas'];}
sg20Keys=ts109Keys;
sg20Warm=function(){UI20.warm();for(const k of ts109Keys())XART.rdy(k);
 if(!TS109.audioWarm){TS109.audioWarm=true;Snd.prepare(['enemyMachineGunLight','hit','select','unlock','missile','retinaCharge']);}};
sg20LayersReady=function(){return XART.rdy(SG20_WATER.key)&&UI20_KEYS.every(k=>XART.rdy(k));};
sg20Terrain=function(screen=false){
 const S=sg20State(),t=state===GS.INTRO?stateT:S?.time||0,w=screen?VW:SG20.width,top=screen?0:viewTopY();
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.fillStyle='#03151d';ctx.fillRect(0,top,w,VH-top);
 if(XART.rdy(SG20_WATER.key)){
  const f=Math.floor(t*SG20_WATER.fps)%SG20_WATER.frames,cell=SG20_WATER.cells[f],tw=SG20_WATER.width,th=SG20_WATER.height;
  const x0=(screen?0:camX*.76)%tw-tw,y0=top+(t*45)%th-th,im=XART.get(SG20_WATER.key);
  for(let y=y0;y<VH;y+=th)for(let x=x0;x<w;x+=tw)ctx.drawImage(im,...cell,Math.floor(x),Math.floor(y),tw,th);
  SG20.waterFrame=f;SG20.waterDraws=(SG20.waterDraws||0)+1;
 }
 // Scenery only: aircraft, ordnance, warning colours and HUD keep native brightness.
 ctx.fillStyle='rgba(0,0,0,.56)';ctx.fillRect(0,top,w,VH-top);ctx.restore();
 SG20.layers={ocean:t*45};TS109.waterDraws=(TS109.waterDraws||0)+1;
};
tutTop=function(){return PLAY.y+146;};
tutAskRows=function(){return ['YES - QUICK MECHANICS FLIGHT',run.mode==='campaign'?'NO - START THE CAMPAIGN':'NO - STRAIGHT TO STAGE 1'];};
drawIntro=function(dt){
 if(!tutLive())return TS109.base.intro.apply(this,arguments);
 sg20Warm();sg20Terrain(true);
 msgText('FLIGHT BASICS',VW/2,VH*.41,28,'#e8f8ff',0,1,.06);
 helpLabel('QUICK HANDS-ON MECHANICS',VW/2,VH*.50,12,'#a0e9e8');
 const ready=sg20LayersReady()&&stageLoadReady(1);
 if(!TUT.music&&ready){TUT.music=true;Audio.startMusic(curStage.music||'stage');}
 if(stateT>=.85&&ready){
  if(TUT._sg){TUT._sg.time=stateT;TUT._sg.travel=stateT*45;}
  player.x=SG20.width/2;player.y=PLAY.y+PLAY.h-65;camX=Math.max(0,(SG20.width-viewW())/2);
  tutHoldStage();setState(GS.PLAY);Input.clearTaps?.();
 }
};
function ts109Crate(kind){const p=tutDropCrate(kind);if(p)p.y=Math.max(tutTop()+35,player.y-100);return p;}
// Tethered practice targets do not join campaign sorties or run hidden attack clocks.
gf113Eligible=function(e){return !tutLive()&&TS109.base.flightEligible.apply(this,arguments);};
jetTick=function(e,dt){if(tutLive()&&e?._tut&&e._dyingT==null)return;return TS109.base.jet.apply(this,arguments);};
tutHold=function(dt){const r=TS109.base.hold.apply(this,arguments);
 if(tutLive())for(const e of enemies){if(!e._tut||e.dead||e._dyingT!=null)continue;
  e.spin=0;e._s1aNativeHead=Math.PI/2;
  for(const a of [e._s1aFlight,e._fb9Swoop,e._r46])if(a)a.head=Math.PI/2;
 }return r;};
function ts109Ports(e){if(s1aJet(e))return [-1,1].map(s=>s1aPlaneMuzzle(e,s));
 return typeof r46Point==='function'&&r46Model(e)?['port','starboard'].map(k=>r46Point(e,k)):
 [-1,1].map(s=>({x:e.x+s*e.w*.22,y:e.y+e.h*.3}));}
const ts109Lessons=[
 {...ts109Old.get('move'),text:()=> 'MOVE WITH YOUR FLIGHT CONTROLS. TOUCH THE TWO MARKERS.',
  start(L){const F=tutField();L.beacons=[-.13,.13].map(x=>({x:F.cx+F.W*x,y:F.bot-95,hit:false}));},
  obj:L=>'FLY THROUGH THE MARKERS '+L.beacons.filter(b=>b.hit).length+' / 2'},
 {...ts109Old.get('fire'),text:()=> 'HOLD '+ts109Bind('fire')+' TO FIRE. CLEAR THESE TWO PRACTICE TARGETS.',
  start(L){const F=tutField();L.units=[-.1,.1].map(x=>tutSpawn('s1jetDelta',F.cx+F.W*x,tutTop()+28,12,{amp:0})).filter(Boolean);L.n=L.units.length;}},
 {...ts109Old.get('roll'),text:()=> 'DOUBLE-TAP LEFT OR RIGHT TO BARREL ROLL. YOU ARE PROTECTED DURING THE ROLL.',
  start(L){L.used=false;},tick(L){L.used=L.used||!!player.roll;return L.used&&!player.roll;}},
 {...ts109Old.get('somer'),text:()=> 'DOUBLE-TAP UP TO SOMERSAULT. THE LOOP ALSO PROTECTS YOU.',
  start(L){L.used=false;},tick(L){L.used=L.used||!!player.somer;return L.used&&!player.somer;}},
 {...ts109Old.get('retina'),text:()=> 'RELEASE FIRE. '+ts109Bind('retina')+' LOCKS A TARGET. '+ts109Bind('bomb')+' LAUNCHES A MISSILE.',
  start(L){run.bombs=Math.max(6,run.bombs);const F=tutField();L.units=[tutSpawn('s1jetDelta',F.cx,tutTop()+28,100,{amp:0})].filter(Boolean);L.base=TUT.ev.lockMissile;}},
 {...ts109Old.get('multi'),text:()=> 'HOLD '+ts109Bind('multilock')+' FOR TWO LOCKS. PRESS '+ts109Bind('bomb')+' TO LAUNCH BOTH.',
  start(L){L.base=sg20State().multiFlights;run.bombs=Math.max(6,run.bombs);sg20MultiTargets(L);}},
 {id:'warn',good:'WARNINGS SHOWN',text:()=> 'GREEN AIMS. YELLOW COMMITS. RED FIRES. MOVE CLEAR OF THE LANES AND THE RING.',
  start(L){const F=tutField();L.gun=tutSpawn('s1jetDelta',F.cx,tutTop()+28,9999,{amp:0});L.age=0;L.aim=player.x;L.shots=0;L.strike=null;},
  obj:L=>L.age<2.4?'LEAVE THE COLORED LANES':'MOVE CLEAR OF THE STRIKE RING',
  tick(L,dt){
   L.age+=dt;if(L.age<.8){L.aim=player.x;if(L.gun?._tutHold)L.gun._tutHold.x=L.aim;}
   if(L.gun&&!L.gun.dead&&L.age<2.4)combatWarningTick(L.gun,'ts109-lanes',L.age,2.4);
   if(L.gun&&!L.gun.dead&&L.age>=2.4&&L.shots<3&&L.age>=2.4+L.shots*.12){
    for(const {x,y}of ts109Ports(L.gun)){const a=Math.PI/2;
     const first=eBullets.length;tutShoot(x,y,a,3.5);
     if(eBullets.length>first)wm26Emit(L.gun,x,y,a,'mg',null,{size:20,life:.12});}
    Snd.play('enemyMachineGunLight');L.shots++;
   }
   if(L.age>=3.5&&!L.strike)L.strike=groundTargetingSpawn({kind:'lightning',warn:1.6,x:player.x,y:player.y,lane:false,radius:34});
   return L.strike&&(L.strike.dead||!groundTargetingFx.includes(L.strike))||L.age>8;
  },
  draw(L){if(L.age>=2.4||!L.gun||L.gun.dead)return;
   for(const {x,y}of ts109Ports(L.gun))combatWarningDraw(L.gun,{x,y,ex:x,ey:PLAY.y+PLAY.h+20,progress:L.age/2.4,width:20});}},
 {...ts109Old.get('crate'),text:()=> 'SHOOT THE SUPPLY CRATE, THEN COLLECT ITS WEAPON. REPEATS UPGRADE YOUR GUN.',
  start(L){L.base=TUT.ev.pick.weapon|0;L.crate=ts109Crate('crate');L.respawn=0;}},
 {...ts109Old.get('special'),text:()=> 'SHOOT THE RED CRATE AND COLLECT '+tutSpecialName()+'. THAT IS YOUR PILOT SPECIAL.',
  start(L){L.base={...TUT.ev.pick};L.crate=ts109Crate('scrate');L.respawn=0;},
  obj:L=>L.activated?'SPECIAL ONLINE':'COLLECT YOUR SPECIAL',
  tick(L,dt){if(!L.activated&&ts109Old.get('special').tick(L,dt))L.activated=true;
   if(L.activated){L.show=(L.show||0)+dt;return L.show>=2;}return false;}},
];
TUT_LESSONS.splice(0,TUT_LESSONS.length,...ts109Lessons);
BOFTUTORIAL.lessons=TUT_LESSONS.map(d=>d.id);
tutStart=function(){TS109.completed=[];return TS109.base.start.apply(this,arguments);};
const ts109Next=tutNext;
tutNext=function(){if(TUT?.L)TS109.completed.push({id:TUT.L.def.id,seconds:TUT.lt});return ts109Next.apply(this,arguments);};
updatePlay=function(dt){const T=TUT,L=T?.L,r=TS109.base.update.apply(this,arguments);
 if(tutLive()&&TUT===T&&T.L===L&&T.done>.4)tutNext();return r;};
tutOverlayDraw=function(){
 const T=TUT;if(!T?.L)return;const D=T.L.def,full=T.say||T.text;
 if(D.draw)tutWorldDraw(()=>D.draw(T.L));
 if(T._fullKey!==full){T._fullKey=full;T.typed=0;}
 const who=T.disp.toUpperCase(),x=12,y=PLAY.y+5,w=VW-24,h=84,r=ui20Panel(who,x,y,w,h,true);
 if(r){msgFaceUse('dialogue');const content=ui20PanelContents(who,full,Math.min(full.length,Math.floor(T.typed||0)),'fb2_dispatch_'+T.disp,r,12,14);msgFaceUse(null);
  UI20.dialogue={who,x,y,w,h,full:full.length,shown:Math.min(full.length,Math.floor(T.typed||0)),...content};}
 const label=T.done>0?D.good:D.obj?.(T.L)||'';
 helpLabel(label,VW/2,y+h+14,12,T.done>0?'#9dffac':'#ffe5a0');
 helpLabel('FLIGHT BASICS '+(T.i+1)+' / '+TUT_LESSONS.length+' - PAUSE TO SKIP',VW/2,y+h+32,9,'#a5c9d0');
 if(T.flash)helpLabel('PRACTICE HIT - LIVES PROTECTED',VW/2,PLAY.y+PLAY.h*.78,11,'#ffb799');
};
globalThis.BOF_TUTORIAL_SHOWCASE=TS109;
