/* tutorial_1015.js - THE TRAINING FLIGHT (Mike, 1015: "Design an in-game tutorial level for Bullets of
   Fury by asking players if they would like a tutorial before entering the game. This is strongly
   recommended as Bullets of Fury is not your average shmup by any means and combines many genre's and
   styles alike.")

   THE ASK. A new game that would open on Stage 1 - Campaign, Arcade or Co-op, straight off pilot select
   or the co-op roster - stops on GS.TUTASK first: an HQ dispatcher explains why, YES is the default and
   says RECOMMENDED. NO starts the game exactly as before. A password, a load, a continue, a debug jump or
   a later stage never asks: startRun is only intercepted for fromStage 1 from those two screens.

   THE FLIGHT. YES flies the chosen pilot over the real Stage-1 field with the real weapons, HUD and
   controls, but nothing of the stage's own content: its wave plan is emptied, its clock is held at 0 so
   no crate, miniboss or boss trigger can fire, and any unit some other system spawns is removed before it
   is drawn. Every lesson uses a system the game already owns - the barrel roll and somersault, the
   manual missile and Retina lock, supply crates, the pilot's special crate, the shared green/yellow/red
   lane warning (combatWarningDraw) and the ground-strike reticle (groundTargetingSpawn). Nothing here
   can kill you: a hit is shown and counted, never charged.

   THE END. The last lesson hands back to the start the player asked for - the same startRun(1) the pilot
   screen was about to make, with the run's mode and co-op seat restored - so Campaign still opens on its
   prologue and Arcade on Stage 1. SKIP TUTORIAL replaces RESTART LEVEL in the pause menu for the flight.
   Finishing it once is remembered (localStorage), which only changes the default answer to NO. */

GS.TUTASK='tutask';
const TUT_STORE='bof_tutorial_v1';
function tutStoreRead(){try{return JSON.parse(localStorage.getItem(TUT_STORE)||'{}')||{};}catch(e){return {};}}
function tutStoreWrite(o){try{localStorage.setItem(TUT_STORE,JSON.stringify(o));}catch(e){}}

const TUT_BASE={startRun,drawScene,drawIntro,updatePlay,playerHit,useBomb,applyPowerup,playPauseChoose,setState};
let tutAsk=null, TUT=null, tutBypass=false;
const TUT_TYPE=64;   // characters a second

/* ---- bind names, as a player would read them ------------------------------------------------------- */
const TUT_PADNAME={pad_b0:'A',pad_b1:'B',pad_b5:'C',pad_b2:'X',pad_b3:'Y',pad_b6:'LT',pad_b7:'RT',pad_b9:'START',
  pad_up:'UP',pad_down:'DOWN',pad_left:'LEFT',pad_right:'RIGHT'};
function tutKey(act){
  const L=(typeof keybind!=='undefined'&&keybind[act])?keybind[act]:[];
  const kb=L.find(k=>!/^pad|^mouse/.test(k)), pad=L.find(k=>/^pad_/.test(k));
  const name=k=>(typeof HELP_KEYNAME!=='undefined'&&HELP_KEYNAME[k]&&!/^pad/.test(k))?HELP_KEYNAME[k]:String(k).toUpperCase();
  const out=[];
  if(kb)out.push(name(kb));
  if(pad)out.push('PAD '+(TUT_PADNAME[pad]||pad.replace('pad_','').toUpperCase()));
  return out.length?out.join(' / '):'-';
}

/* ---- the instructor: a Fury pilot on the radio at HQ, never one who is in the air (Mike's 1002 rule,
   the same one fb2Dispatcher applies to the Stage-5 arrival) ----------------------------------------- */
const TUT_HQ=['cole','decker','axel','lizzie','falva'];
function tutDispatcher(lead){
  if(lead==='decker')return 'cole';
  if(lead==='cole')return 'decker';
  if(lead==='lizzie')return 'falva';
  if(lead==='falva')return 'lizzie';
  return (String(lead).length%2)?'cole':'decker';
}
function tutLeadKey(){const P=(typeof PILOTS!=='undefined'&&PILOTS[pilotIndex])||null;return P?P.key:(run.pilot||'cole');}

/* ---- intercept: a fresh Stage-1 start off pilot select or the co-op roster asks first ------------- */
startRun=function(fromStage){
  const s=(fromStage==null)?1:fromStage;
  if(!tutBypass && !TUT && s===1 && (state===GS.PILOT||state===GS.COOPROSTER)){ tutAskOpen(s); return; }
  return TUT_BASE.startRun.apply(this,arguments);
};
function tutAskOpen(stage){
  const seen=!!tutStoreRead().done, lead=tutLeadKey();
  tutAsk={stage, prev:state, sel:seen?1:0, t:0, seen, lead, disp:tutDispatcher(lead)};
  try{XART.rdy('fb2_dispatch_'+tutAsk.disp);XART.rdy('dlg_window');}catch(e){}
  setState(GS.TUTASK);
  if(Input.clearTaps)Input.clearTaps();
}
function tutAskRows(){
  const camp=(typeof run!=='undefined'&&run&&run.mode==='campaign');
  return ['YES - TAKE THE TRAINING FLIGHT', camp?'NO - START THE CAMPAIGN':'NO - STRAIGHT TO STAGE 1'];
}
function tutAskChoose(i){
  const A=tutAsk; if(!A)return;
  if(Audio.SFX.select)Audio.SFX.select();
  if(i===0){ tutAsk=null; tutStart(A); return; }
  tutAsk=null; tutBypass=true;
  try{ TUT_BASE.startRun(A.stage); } finally { tutBypass=false; }
}
function tutAskDraw(dt){
  const A=tutAsk; if(!A){ setState(GS.TITLE); return; }
  A.t+=dt;
  if(!(typeof drawCanonBackdrop==='function'&&drawCanonBackdrop('nbt_2',0.62))){ctx.fillStyle='#04060b';ctx.fillRect(0,0,VW,VH);}
  msgText('TRAINING FLIGHT',VW/2,46,22,'#f2f5ff',0,1,0.08);
  helpLabel('BEFORE YOU DEPLOY', VW/2, 72, 12, '#ffd36b');
  const D=A.disp.toUpperCase()+' - HQ';
  const body='BULLETS OF FURY IS NOT YOUR AVERAGE SHMUP. IT MIXES ARCADE SHOOTING WITH DODGE ROLLS, '
    +'LOCK-ON MISSILES, PILOT SPECIALS, ELEMENTS AND THE FORGE. FLY THE TRAINING ROUTE FIRST - '
    +'WE STRONGLY RECOMMEND IT.';
  /* the panel types on the game clock at TUT_TYPE characters a second, not dlgBox's wall clock, so a
     paused or slow frame cannot leave the reason half-written */
  dlgBox({who:D, full:body, shown:body.slice(0,Math.floor(A.t*TUT_TYPE)), portraitKey:'fb2_dispatch_'+A.disp, tint:'#9fd6ff', screenSpace:false,
          x:12, y:92, pw:VW-24, ph:150});
  const rows=tutAskRows(), y0=VH*0.60, gap=46;
  for(let i=0;i<rows.length;i++){
    const sel=i===A.sel, y=y0+i*gap;
    helpLabel(rows[i], VW/2+10, y, sel?15:13, sel?'#ffffff':'#8fa3b8');
    if(sel&&typeof drawSelArrow==='function')drawSelArrow(28, y-5, 20, false, 'g');
  }
  helpLabel(A.seen?'STRONGLY RECOMMENDED - YOU HAVE FLOWN IT BEFORE':'STRONGLY RECOMMENDED FOR FIRST-TIME PILOTS',
            VW/2, y0-28, 11, A.seen?'#7f93a8':'#ffd36b');
  helpLabel('ABOUT FOUR MINUTES - SKIP ANY TIME FROM THE PAUSE MENU', VW/2, y0+gap*2-4, 11, '#7f93a8');
  if(typeof controlHintRow==='function')controlHintRow([['pad_dpad','CHOOSE'],['pad_a','CONFIRM'],['pad_b','BACK']]);
  if(A.t<0.35)return;
  if(Input.menuUp()||Input.menuDown()){ A.sel=1-A.sel; if(Audio.SFX.blip)Audio.SFX.blip(); }
  if(Input.menuConfirm()){ tutAskChoose(A.sel); return; }
  if(Input.menuBack()){
    tutAsk=null;
    if(A.prev===GS.PILOT){ try{drawPilot._entered=false;drawPilot._pcFor=null;}catch(e){} pilotPending=null; pilotSlide=0; }
    setState(A.prev||GS.PILOT);
  }
}

/* ---- the flight ------------------------------------------------------------------------------------- */
function tutStart(A){
  TUT={stage:A.stage, mode:run.mode, ngplus:run.ngplus, coop:(typeof coopOn!=='undefined')?coopOn:false,
       lead:A.lead, disp:A.disp, i:-1, L:null, lt:0, done:0, msg:'', t:0, hits:0, ev:{missile:0,lockMissile:0,pick:{}},
       pauseRow:PLAY_PAUSE_ROWS[2], card:true, music:false, finished:false};
  if(typeof coopOn!=='undefined')coopOn=false;
  run.mode='arcade';
  PLAY_PAUSE_ROWS[2]='SKIP TUTORIAL';
  tutBypass=true;
  try{ TUT_BASE.startRun(1); } finally { tutBypass=false; }
}
function tutLive(){ return !!(TUT && !TUT.finished && run && run.stage===1); }
/* hand back to the start the player asked for, with everything the flight borrowed returned */
function tutFinish(completed){
  const T=TUT; if(!T)return;
  T.finished=true;
  if(completed){ const s=tutStoreRead(); s.done=true; s.at=Date.now(); tutStoreWrite(s); }
  tutCleanup();
  run.mode=T.mode; run.ngplus=T.ngplus; if(typeof coopOn!=='undefined')coopOn=T.coop;
  TUT=null;
  tutBypass=true;
  try{ TUT_BASE.startRun(T.stage); } finally { tutBypass=false; }
}
function tutCleanup(){
  try{ if(typeof special!=='undefined'&&special&&typeof endSpecial==='function')endSpecial(); }catch(e){}
  try{ if(typeof groundTargetingFx!=='undefined')groundTargetingFx.length=0; }catch(e){}
  try{ enemies.length=0; eBullets.length=0; powerups.length=0; }catch(e){}
  try{ retina.target=null; retina.phase=null; }catch(e){}
  try{ player.roll=null; player.somer=null; player.invuln=0; }catch(e){}
  try{ if(typeof lzMount!=='undefined')lzMount=null; }catch(e){}
  if(TUT&&TUT.pauseRow)PLAY_PAUSE_ROWS[2]=TUT.pauseRow;
}
/* leaving the flight for the title by any route (pause > RETURN TO MAIN MENU / QUIT) drops it whole */
setState=function(s){
  if(TUT && (s===GS.TITLE||s===GS.MODESEL||s===GS.GAMEOVER)){
    const T=TUT; tutCleanup(); run.mode=T.mode; run.ngplus=T.ngplus; if(typeof coopOn!=='undefined')coopOn=T.coop; TUT=null;
  }
  return TUT_BASE.setState.apply(this,arguments);
};
playPauseChoose=function(index){
  if(TUT && index===2 && playPause){
    if(Audio.SFX.select)Audio.SFX.select();
    playPause=null; TUT_BASE.setState(GS.PLAY);
    tutFinish(false); return;
  }
  return TUT_BASE.playPauseChoose.apply(this,arguments);
};

/* the stage card: a training card instead of STAGE 1 */
drawIntro=function(dt){
  if(!tutLive()) return TUT_BASE.drawIntro.apply(this,arguments);
  const t=stateT;
  ctx.fillStyle='#000'; ctx.fillRect(0,0,VW,VH);
  if(t>0.05 && !TUT.music){ TUT.music=true; if(Audio.startMusic)Audio.startMusic((curStage&&curStage.music)||'stage'); }
  const a=clamp(t/0.5,0,1)*(t>2.6?clamp((3.1-t)/0.5,0,1):1);
  msgText('TRAINING FLIGHT', VW/2, VH*0.40, 30, '#f2f5ff', 0, a, 0.08);
  helpLabel('FURY HQ PROVING GROUND', VW/2, VH*0.48, 14, '#ffd36b');
  const P=(typeof PILOTS!=='undefined')?PILOTS.find(p=>p.key===run.pilot):null;
  if(P)helpLabel('PILOT - '+P.name, VW/2, VH*0.55, 12, P.tint||'#9fd6ff');
  helpLabel('NOTHING OUT HERE CAN KILL YOU', VW/2, VH*0.66, 11, '#7f93a8');
  if(t>=3.1 || (t>0.7 && (keybind.fire.some(k=>Input.tap(k))||Input.menuStart()||Input.menuFaceTap()))){ proceedIntro(); }
};

/* a hit is shown and counted, never charged */
playerHit=function(source){
  if(!tutLive()) return TUT_BASE.playerHit.apply(this,arguments);
  if(player.dead || player.invuln>0 || player.roll || player.somer) return;
  TUT.hits++; if(TUT.L)TUT.L.hit=(TUT.L.hit||0)+1;
  try{ (TUT.hitLog||(TUT.hitLog=[])).push([TUT.L?TUT.L.def.id:'-', String(source||''), String(new Error().stack||'').split(String.fromCharCode(10)).slice(2,5).map(l=>l.trim()).join(' < ')]); }catch(e){}
  player.invuln=70; shake=Math.max(shake,6);
  if(Audio.SFX.hit)Audio.SFX.hit();
  TUT.flash={t:0, text:'HIT - IN A REAL FIGHT THAT COSTS A SHIELD OR A LIFE'};
};
useBomb=function(){
  const locked=!!(typeof retina!=='undefined'&&retina.phase==='locked'&&typeof retinaTargetValid==='function'&&retinaTargetValid(retina.target));
  const r=TUT_BASE.useBomb.apply(this,arguments);
  if(r===true && tutLive()){ TUT.ev.missile++; if(locked)TUT.ev.lockMissile++; }
  return r;
};
applyPowerup=function(p){
  if(tutLive()&&p&&p.kind){ TUT.ev.pick[p.kind]=(TUT.ev.pick[p.kind]||0)+1; }
  return TUT_BASE.applyPowerup.apply(this,arguments);
};

/* ---- training targets: real enemy units, held on a tether ------------------------------------------ */
/* the highest a training target may hover: clear of HQ's instruction panel and the objective line under it */
function tutTop(){ return PLAY.y+Math.min(PLAY.h*0.42, 196); }
function tutField(){ const L=camLeftX(), R=camRightX(); return {L, R, W:R-L, cx:(L+R)/2, top:PLAY.y, bot:PLAY.y+PLAY.h}; }
function tutSpawn(type, x, y, hp, opt){
  opt=opt||{};
  T_spawning=true; let e=null;
  try{ e=spawnEnemy(type, x, y, {pattern:'straight'}); }catch(err){ e=null; } finally { T_spawning=false; }
  if(!e)return null;
  e._tut=1; e._tutHold={x, y, ph:Math.random()*6.28, amp:opt.amp==null?6:opt.amp};
  e.shoots=false; e.vx=0; e.vy=0; e.score=e.score||100;
  if(hp){ e.hp=hp; e.maxhp=hp; }
  return e;
}
let T_spawning=false;
function tutHold(dt){
  for(const e of enemies){
    if(!e._tut || e.dead || e._dyingT!=null || !e._tutHold) continue;
    const H=e._tutHold; H.ph+=dt*1.6;
    e.x=H.x+Math.sin(H.ph)*H.amp; e.y=H.y+Math.cos(H.ph*0.8)*H.amp*0.6;
    e.vx=0; e.vy=0; e.shoots=false;
  }
}
function tutAlive(list){ return list.filter(e=>e && !e.dead && e._dyingT==null && enemies.indexOf(e)>=0); }
function tutShoot(x,y,ang,spd){ try{ eShoot(x,y,ang,spd,'mg'); const b=eBullets[eBullets.length-1]; if(b)b._tut=1; }catch(e){} }
function tutDropCrate(kind){
  const before=powerups.length; spawnContainer(kind);
  for(let i=before;i<powerups.length;i++){ const p=powerups[i]; p.x=clamp(player.x, camLeftX()+40, camRightX()-40); p._tut=1; }
  return powerups[powerups.length-1]||null;
}

/* ---- the lessons ------------------------------------------------------------------------------------ */
/* each: text (what HQ says), obj (the live objective line), start, tick -> true when met, draw (world). */
const TUT_LESSONS=[
  {id:'move', good:'NICE FLYING',
   text:T=>'WELCOME TO THE PROVING GROUND, '+tutPilotName()+'. FLY WITH '+tutKey('up').split(' / ')[0]+tutKey('left').split(' / ')[0]+tutKey('down').split(' / ')[0]+tutKey('right').split(' / ')[0]+', THE ARROWS OR THE D-PAD. TOUCH ALL FOUR BEACONS.',
   start(L){ const F=tutField(); L.beacons=[[F.L+F.W*0.18,tutTop()+40],[F.L+F.W*0.82,tutTop()+40],[F.L+F.W*0.82,F.bot-90],[F.L+F.W*0.18,F.bot-90]].map(p=>({x:p[0],y:p[1],hit:false})); },
   obj:L=>'BEACONS '+L.beacons.filter(b=>b.hit).length+' / 4',
   tick(L){ for(const b of L.beacons){ if(!b.hit && Math.hypot(player.x-b.x,player.y-b.y)<30){ b.hit=true; if(Audio.SFX.select)Audio.SFX.select(); } } return L.beacons.every(b=>b.hit); },
   draw(L){ for(const b of L.beacons) tutBeaconDraw(b.x,b.y,b.hit); }},

  {id:'fire', good:'TARGETS DOWN',
   text:T=>'HOLD FIRE - '+tutKey('fire')+' - AND KEEP IT HELD. YOUR GUN NEVER RUNS DRY. TAKE OUT THE TRAINING DRONES.',
   start(L){ const F=tutField(); L.units=[0.2,0.4,0.6,0.8].map(k=>tutSpawn('s1jetDelta', F.L+F.W*k, tutTop()+20, 30)).filter(Boolean); L.n=L.units.length; },
   obj:L=>'DRONES '+(L.n-tutAlive(L.units).length)+' / '+L.n,
   tick(L){ return !tutAlive(L.units).length; }},

  {id:'crate', good:'WEAPON UP',
   text:T=>'SUPPLY CRATES FALL IN DURING A STAGE. SHOOT THIS ONE OPEN, THEN FLY INTO THE WEAPON THAT FALLS OUT. THE SAME WEAPON AGAIN RAISES IT A LEVEL, I TO V - DIE AND YOU DROP BACK TO YOUR STARTING GUN.',
   start(L){ L.base=(TUT.ev.pick.weapon|0); L.crate=tutDropCrate('crate'); L.respawn=0; },
   obj:L=>'COLLECT THE WEAPON',
   tick(L,dt){
     if((TUT.ev.pick.weapon|0)>L.base) return true;
     const live=powerups.some(p=>p._tut||p.kind==='weapon'||p.kind==='crate');
     if(!live){ L.respawn+=dt; if(L.respawn>1.2){ L.respawn=0; L.crate=tutDropCrate('crate'); } }
     return false; }},

  {id:'roll', good:'UNTOUCHABLE',
   text:T=>'BARREL ROLL - DOUBLE-TAP LEFT OR RIGHT. YOU CANNOT BE HIT FOR THE WHOLE ROLL. IT RECHARGES IN '+(typeof BR_COOL==='number'?BR_COOL:5)+' SECONDS - WATCH THE ROLL BAR ON THE HUD.',
   start(L){ L.was=!!player.roll; },
   obj:L=>'BARREL ROLL ONCE',
   tick(L){ const now=!!player.roll, edge=now&&!L.was; L.was=now; return edge; }},

  {id:'somer', good:'CLEAN LOOP',
   text:T=>'SOMERSAULT - DOUBLE-TAP UP. A FULL LOOP WITH THE SAME PROTECTION, HEAVIER THAN A ROLL, AND IT ENDS WHERE IT BEGAN. '+(typeof SS_COOL==='number'?SS_COOL:7)+' SECOND RECHARGE.',
   start(L){ L.was=!!player.somer; },
   obj:L=>'SOMERSAULT ONCE',
   tick(L){ const now=!!player.somer, edge=now&&!L.was; L.was=now; return edge; }},

  {id:'missile', good:'DIRECT HIT',
   text:T=>'MANUAL MISSILES - PRESS '+tutKey('bomb')+'. THEY HIT FAR HARDER THAN YOUR GUN, BUT STOCK IS LIMITED - THE COUNT IS ON YOUR HUD. MISSILE CRATES REFILL IT. FIRE ONE AT THE ARMORED TARGET.',
   start(L){ run.bombs=Math.max(run.bombs|0,4); const F=tutField(); L.units=[tutSpawn('s1jetBomber', F.cx, tutTop()+30, 120, {amp:4})].filter(Boolean); L.base=TUT.ev.missile; },
   obj:L=>'FIRE A MISSILE',
   tick(L){ if(run.bombs<1)run.bombs=2; return TUT.ev.missile>L.base; }},

  {id:'retina', good:'LOCKED AND LAUNCHED',
   text:T=>'THE RETINA - TAP '+tutKey('retina')+' TO LOCK THE NEAREST TARGET, THEN FIRE A MISSILE AND IT FLIES TO THE LOCK. HOLD '+tutKey('multilock')+' TO SCAN SEVERAL TARGETS AT ONCE.',
   start(L){ run.bombs=Math.max(run.bombs|0,4); const F=tutField();
     L.units=[0.22,0.78].map(k=>tutSpawn('s1jetDelta', F.L+F.W*k, tutTop()+10, 60)).filter(Boolean); L.base=TUT.ev.lockMissile; },
   obj:L=>(typeof retina!=='undefined'&&retina.phase==='locked')?'LOCKED - NOW FIRE A MISSILE':'LOCK A TARGET',
   tick(L){ if(run.bombs<1)run.bombs=2;
     if(!tutAlive(L.units).length){ const F=tutField(); L.units=[tutSpawn('s1jetDelta', F.cx, tutTop()+10, 60)].filter(Boolean); }
     return TUT.ev.lockMissile>L.base; }},

  {id:'warn', good:'READ AND DODGED',
   text:T=>'LEARN THE COLORS. A GREEN LANE MEANS SOMETHING IS AIMING AT YOU. YELLOW - IT HAS LOCKED ITS AIM. RED - IT IS FIRING DOWN THAT LANE. MOVE OUT BEFORE RED.',
   start(L){ const F=tutField();
     L.gun=tutSpawn('s1jetBomber', player.x, tutTop(), 9999, {amp:0}); L.clean=0; L.cycles=0; L.c=null; },
   obj:L=>'DODGE THE LANE '+L.clean+' / 2',
   tick(L,dt){
     if(!L.gun || L.gun.dead){ const F=tutField(); L.gun=tutSpawn('s1jetBomber', player.x, tutTop(), 9999, {amp:0}); }
     if(!L.c) L.c={t:-0.8, x:player.x, hit0:TUT.hits, fired:0};
     const C=L.c, DUR=2.4; C.t+=dt;
     if(C.t<0) return false;
     if(C.t<DUR/3){ C.x+=clamp(player.x-C.x,-160*dt,160*dt); }           // green: it follows you
     if(L.gun && L.gun._tutHold){ L.gun._tutHold.x=C.x; }
     if(C.t<DUR){ combatWarningTick(L.gun, 'tut-lane', C.t, DUR); return false; }
     if(C.fired<12 && C.t>=DUR+C.fired*0.045){                              // red: a dense column down the lane
       const y=L.gun.y+30; for(const dx of [-12,0,12]) tutShoot(C.x+dx, y, Math.PI/2, 6.2);
       C.fired++; return false;
     }
     if(C.t>=DUR+1.3){ L.cycles++; if(TUT.hits===C.hit0)L.clean++; else TUT.say='TOO SLOW - GET OUT OF THE LANE BEFORE IT TURNS RED.'; L.c=null; }
     return L.clean>=2 || L.cycles>=5;
   },
   draw(L){ const C=L.c; if(!C||C.t<0||C.t>=2.4||!L.gun)return;
     combatWarningDraw(L.gun,{x:C.x, y:L.gun.y+24, ex:C.x, ey:PLAY.y+PLAY.h+20, progress:C.t/2.4, width:40}); }},

  {id:'strike', good:'CLEAR OF THE BLAST',
   text:T=>'GROUND STRIKES USE THE SAME COLORS. THE RETICLE FOLLOWS YOU WHILE IT IS GREEN, THEN COMMITS. BE SOMEWHERE ELSE WHEN IT GOES RED.',
   start(L){ L.n=0; L.next=0.6; L.hit0=TUT.hits; L.clean=0; L.cur=null; },
   obj:L=>'SURVIVE THE STRIKES '+L.clean+' / 3',
   tick(L,dt){
     if(L.cur){ if(L.cur.dead||groundTargetingFx.indexOf(L.cur)<0){ if(TUT.hits===L.h0)L.clean++; else TUT.say='CAUGHT IN IT - MOVE AS SOON AS THE RETICLE TURNS YELLOW.'; L.cur=null; L.next=0.5; } return L.clean>=3 || L.n>=6; }
     L.next-=dt; if(L.next>0) return false;
     L.n++; L.h0=TUT.hits;
     L.cur=groundTargetingSpawn({kind:'lightning', warn:1.9, x:player.x, y:player.y, lane:false, radius:38});
     return false; }},

  {id:'special', good:'SPECIAL ONLINE',
   text:T=>'YOUR SPECIAL - '+tutSpecialName()+'. IT RIDES IN THE RED CRATE. SHOOT IT OPEN AND FLY INTO WHAT DROPS OUT. A SPECIAL IS ON A TIMER, SO SPEND IT.'+(run.pilot==='juggernaut'?' WITH IT LIVE, HOLD '+tutKey('charge')+' THEN HOLD UP TO RAM.':''),
   start(L){ L.base=Object.assign({},TUT.ev.pick); L.crate=tutDropCrate('scrate'); L.respawn=0;
     const F=tutField(); L.units=[0.3,0.7].map(k=>tutSpawn('s1jetDelta', F.L+F.W*k, tutTop()+10, 40)).filter(Boolean); },
   obj:L=>'COLLECT YOUR SPECIAL',
   tick(L,dt){
     const P=TUT.ev.pick, got=['special','specialicon','sonicbox','lzmgbox','dkshotbox'].some(k=>(P[k]|0)>(L.base[k]|0));
     if(got || (typeof specialActive==='function'&&specialActive())) return true;
     if(!powerups.some(p=>p._tut||/crate|special|box/.test(p.kind||''))){ L.respawn+=dt; if(L.respawn>1.2){ L.respawn=0; L.crate=tutDropCrate('scrate'); } }
     return false; }},

  {id:'brief1', info:true, good:'',
   text:T=>'BOSSES DROP ELEMENTS. AFTER EACH STAGE THE FORGE FUSES AN ELEMENT INTO ANY WEAPON. FIRE HITS ICE ENEMIES TWICE AS HARD AND ICE DOES THE SAME TO FIRE - BUT AN ENEMY SHRUGS OFF HALF OF ITS OWN ELEMENT.'},
  {id:'brief2', info:true, good:'',
   text:T=>'BLUE RINGS ARE ENEMY SHIELDS - BREAK ONE AND THE ENEMY IS STUNNED FOR A MOMENT. KILL FAST TO CHAIN YOUR SCORE, AND SCORE BECOMES FURY POINTS FOR THE ARMORY BETWEEN STAGES.'},

  {id:'exam', good:'TRAINING COMPLETE',
   text:T=>'FINAL DRILL. THESE DRONES SHOOT BACK. USE EVERYTHING - FIRE, ROLL, LOCK, MISSILES. CLEAR THE WAVE.',
   start(L){ run.bombs=Math.max(run.bombs|0,3); const F=tutField();
     L.units=[[0.18,0],[0.5,0],[0.82,0],[0.34,100],[0.66,100]].map(p=>tutSpawn('s1jetDelta', F.L+F.W*p[0], tutTop()+p[1], 45)).filter(Boolean);
     L.n=L.units.length; L.fireT=1.2; L.strikeT=5; },
   obj:L=>'DRONES '+(L.n-tutAlive(L.units).length)+' / '+L.n,
   tick(L,dt){
     const live=tutAlive(L.units); if(!live.length) return true;
     L.fireT-=dt; if(L.fireT<=0){ L.fireT=1.15; const e=live[(Math.random()*live.length)|0]; tutShoot(e.x, e.y+16, Math.atan2(player.y-e.y, player.x-e.x), 2.6); }
     L.strikeT-=dt; if(L.strikeT<=0){ L.strikeT=6; groundTargetingSpawn({kind:'lightning', warn:1.9, x:player.x, y:player.y, lane:false, radius:38}); }
     return false; }},
];
function tutPilotName(){ const P=(typeof PILOTS!=='undefined')?PILOTS.find(p=>p.key===run.pilot):null; return P?P.name:'PILOT'; }
function tutSpecialName(){ try{ return pcSpecial(run.pilot).name; }catch(e){ return 'YOUR SPECIAL'; } }

function tutBeaconDraw(x,y,hit){
  const k='nbret_'+(run.pilot||'cole');
  const pulse=1+0.08*Math.sin((stateT||0)*6);
  ctx.save(); ctx.imageSmoothingEnabled=false;
  if(typeof XART!=='undefined' && XART.rdy(k)){
    const im=XART.get(k), h=(hit?34:46)*pulse, w=h*(im.naturalWidth/Math.max(1,im.naturalHeight));
    ctx.globalAlpha=hit?0.28:0.95; ctx.drawImage(im, Math.round(x-w/2), Math.round(y-h/2), Math.round(w), Math.round(h));
  } else {
    ctx.globalAlpha=hit?0.3:0.9; ctx.strokeStyle='#7ad6ff'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(x,y,18*pulse,0,6.283); ctx.stroke();
  }
  ctx.restore();
}

/* ---- the per-frame director ------------------------------------------------------------------------ */
function tutHoldStage(){
  if(typeof stagePlan!=='undefined' && stagePlan && stagePlan.length) stagePlan=[];
  stageTimer=0;
  try{ if(typeof CP12!=='undefined')CP12.next=1e9; }catch(e){}
  try{ if(typeof story!=='undefined'&&story&&typeof storySkip==='function')storySkip(); }catch(e){}
}
function tutPurge(){
  /* anything the tutorial did not put on the field leaves before it is drawn */
  if(enemies.some(e=>!e._tut)) enemies=enemies.filter(e=>e._tut);
  if(eBullets.some(b=>!b._tut)) eBullets=eBullets.filter(b=>b._tut);
}
/* every lesson starts on an empty field: the last lesson's targets, rounds and strike reticles leave
   with it, so an info card is never interrupted by a stray round from the drill before */
function tutClearField(keepTargets){
  if(!keepTargets) for(const e of enemies) if(e._tut && !e.dead) e.dead=true;
  eBullets.length=0;
  try{ if(typeof groundTargetingFx!=='undefined') for(const q of groundTargetingFx) q.dead=true; }catch(e){}
}
function tutNext(){
  const T=TUT; T.i++; T.lt=0; T.done=0; T.say='';
  const keep=TUT_LESSONS[T.i]&&TUT_LESSONS[T.i].keepTargets;
  tutClearField(keep);
  const D=TUT_LESSONS[T.i];
  if(!D){ tutFinish(true); return; }
  T.L={def:D}; T.text=D.text(T);
  if(D.start)D.start(T.L);
  try{ XART.rdy('fb2_dispatch_'+T.disp); XART.rdy('nbret_'+run.pilot); }catch(e){}
}
updatePlay=function(dt){
  if(!tutLive()) return TUT_BASE.updatePlay.apply(this,arguments);
  tutHoldStage();
  const r=TUT_BASE.updatePlay.apply(this,arguments);
  if(!tutLive()) return r;
  const T=TUT; T.t+=dt; T.typed=(T.typed||0)+dt*TUT_TYPE;
  tutPurge(); tutHold(dt);
  if(player.dead){ player.dead=false; player.alive=true; }
  if(T.flash){ T.flash.t+=dt; if(T.flash.t>2.2)T.flash=null; }
  if(T.i<0){ if(T.t>1.0) tutNext(); return r; }
  const L=T.L, D=L.def; T.lt+=dt;
  if(T.done>0){ T.done+=dt; if(T.done>(D.info?0.25:1.5)) tutNext(); return r; }
  if(D.info){
    if(T.lt>1.2 && (T.typed||0)>=T.text.length && (keybind.fire.some(k=>Input.tap(k))||Input.menuFaceTap())){ T.done=0.01; if(Audio.SFX.blip)Audio.SFX.blip(); }
    return r;
  }
  if(T.lt>0.6 && D.tick && D.tick(L,dt)){ T.done=0.01; if(Audio.SFX.select)Audio.SFX.select(); if(Audio.SFX.unlock)Audio.SFX.unlock(); }
  return r;
};

/* ---- drawing ---------------------------------------------------------------------------------------- */
function tutWorldDraw(fn){
  const z=(typeof viewZoom==='function')?viewZoom():1;
  ctx.save();
  if(z!==1){ ctx.scale(z,z); ctx.translate(0, VH*(1-z)/z); }
  if(worldWidth()>viewW()) ctx.translate(-camX,0);
  const was=_inWorldXform; _inWorldXform=true;
  try{ fn(); }catch(e){} finally { _inWorldXform=was; ctx.restore(); }
}
function tutOverlayDraw(){
  const T=TUT; if(!T||T.i<0||!T.L)return;
  const D=T.L.def;
  if(D.draw) tutWorldDraw(()=>D.draw(T.L));
  const who=T.disp.toUpperCase()+' - HQ', full=T.say||T.text;
  const pw=VW-16, x=PLAY.x+8, y=PLAY.y+6;
  if(T._fullKey!==full){ T._fullKey=full; T.typed=0; }
  dlgBox({who, full, shown:full.slice(0,Math.floor(T.typed||0)), portraitKey:'fb2_dispatch_'+T.disp, tint:'#9fd6ff', screenSpace:false, x, y, pw, ph:104});
  let ph=118;
  try{ const bay=clamp(Math.round(pw*.13),76,106), col=pw-36-bay-14; ph=Math.min(Math.round(VH*.29),Math.max(104,msgBlockLayout(full,col,1000,14,14,1.3).height+60)); }catch(e){}
  const oy=y+ph+16;
  const step=(T.i+1)+' / '+TUT_LESSONS.length;
  if(T.done>0 && D.good){
    const a=clamp(T.done/0.2,0,1);
    msgText(D.good, VW/2, PLAY.y+PLAY.h*0.46, 24, '#7dff9a', 0, a, 0.08);
  } else if(D.info){
    if(T.lt>1.2 && (T.typed||0)>=full.length) helpLabel('PRESS '+tutKey('fire')+' TO CONTINUE', VW/2, oy, 12, (Math.floor((stateT||0)*2.5)%2)?'#ffd36b':'#cfe2ff');
  } else if(D.obj){
    helpLabel(D.obj(T.L), VW/2, oy, 13, '#ffd36b');
  }
  helpLabel('TRAINING '+step+'  -  PAUSE TO SKIP', VW/2, oy+21, 11, '#6d8096');
  if(T.flash){ const a=clamp(1-(T.flash.t-1.6)/0.6,0,1); helpLabel(T.flash.text, VW/2, PLAY.y+PLAY.h*0.62, 11, 'rgba(255,120,110,'+a.toFixed(2)+')'); }
}
drawScene=function(dt){
  if(state===GS.TUTASK){ try{ tutAskDraw(dt); }catch(e){ if(!drawScene._tutErr){drawScene._tutErr=1;console.error('tutorial ask',e);} } return; }
  const r=TUT_BASE.drawScene.apply(this,arguments);
  if(state===GS.PLAY && tutLive()){ try{ tutOverlayDraw(); }catch(e){ if(!drawScene._tutErr2){drawScene._tutErr2=1;console.error('tutorial overlay',e);} } }
  return r;
};
window.BOFTUTORIAL={lessons:TUT_LESSONS.map(l=>l.id), get live(){return TUT;}, get ask(){return tutAsk;}, next:()=>{if(TUT){TUT.done=0.01;}}, store:tutStoreRead, reset:()=>tutStoreWrite({})};
