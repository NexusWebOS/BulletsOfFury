'use strict';
/* Repairs measured against Mike's October 4 complete-run recording.
   Evidence and remaining verification: docs/GAMEPLAY_AUDIT_1004.md. */
const GP4={route:null,routeReady:false,deaths:[],death:null,portraits:new Map(),clock:0};
const GP4_BASE={begin:beginStage,update:updatePlay,world:drawWorld,enemy:drawEnemy,
 shield:stage4ShieldTick,ace:whvAceKey,hit:markHit,wing:s6WingLaunch,start:startRun,
 password:submitPassword,leave:scLeaveStage,hammerDamage:hammerBossDamage,
 hammerTick:hammerBossTick,recoveryBreak:hammerRecoveryBreak};

// These aliases deliberately bypass the retired packed bank frames. Every pose
// comes from the same approved blue Nightwing source family, including damage.
for(const [k,file] of [['top','ace_top'],['belly','ace_belly'],['damaged','ace_damaged'],
 ...Array.from({length:8},(_,i)=>['br'+i,'ace_br'+i]),...Array.from({length:8},(_,i)=>['so'+i,'ace_so'+i])])
 XART._src['gp4_ace_'+k]='assets/game/bosses/skycarrier/'+file+'.png';
for(const m of ['body','wingL','wingR'])for(const v of ['','_dmg'])XART._src['gp4_acem_'+m+v]='assets/game/bosses/skycarrier/ace_mod_'+m+v+'.png';
function gp4AceWarm(){
 for(const k of Object.keys(XART._src))if(k.startsWith('gp4_ace')||k.startsWith('sky4i_'))XART.rdy(k);
}
whvAceKey=function(b,A){const key=GP4_BASE.ace(b,A),name=key==='whv_ace'?'top':key==='whv_ace_dmg'?'damaged':key.slice(8);return 'gp4_ace_'+name;};

// The September 30 renderer owns the larger fighter. Its underside/damage poses
// must share blue armor and its modular branch must honor the boss-wide flash.
// Shipping white PNGs have exact source alpha; no color-composite hit wash.
function gp4AceCell(name,frame,x,y,w,h,flash){
 const a=SKY4I_ART[name],key=flash?a.flash:a.key;if(!XART.rdy(key))return false;
 const r=a.frames[((frame|0)%a.frames.length+a.frames.length)%a.frames.length];
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(key),...r,Math.round(x-w/2),Math.round(y-h/2),w,h);ctx.restore();return true;
}
whvDrawAce=function(b){
 const A=b._whv?.ace;if(!A)return;
 const w=184,h=192;
 if(A.dash?.st==='warn')combatWarningDraw(b,{x:A.x,y:A.y,ex:A.dash.ex,ey:A.dash.ey,progress:A.dash.t/.95,width:w*.65});
 const P=A.desp;
 if(P?.st==='warn')combatWarningDraw(b,{x:A.x,y:A.y,ex:A.x,ey:VH+60,progress:P.t/.8,width:w*.65});
 if(P?.st==='cross'&&P.t<P.lead){combatWarningDraw(b,{x:P.x0,y:P.y0,ex:P.x1,ey:P.y1,progress:P.t/P.lead,width:95,fieldOnly:true});return;}
 const frame=enc30AceFrame(b,A),whole=b.dead||frame>1,hit=!b.dead&&b.flash>0;
 if(whole){
  ctx.save();ctx.translate(A.x,A.y);if(b.dead)ctx.rotate(A.spin||0);
  gp4AceCell('ace',frame,0,0,w,h,hit);ctx.restore();
 }else for(const [part,id] of [['wing_l','wingL'],['body','body'],['wing_r','wingR']]){
  const name='ace_'+part+(frame===1?'_damage':'');
  gp4AceCell(name,0,A.x,A.y,w,h,hit||(A.fl?.[id]||0)>0);
 }
 if(!b.dead&&!A.somer&&!A.inverted){
  const key='nthr_blue_'+(Math.floor(efxClock*14)%8);
  if(XART.rdy(key))for(const s of [-1,1]){ctx.save();ctx.translate(A.x+s*22,A.y-h*.30);ctx.rotate(Math.PI);ctx.imageSmoothingEnabled=false;ctx.globalAlpha=.85;ctx.drawImage(XART.get(key),-6,-1,12,48);ctx.restore();}
 }
 if(!b.dead){const r=b.hp/b.maxhp;whvPartFx(b,{x:A.x-58,y:A.y},r,false,.8,5);whvPartFx(b,{x:A.x+58,y:A.y},r,false,.8,6.3);}
};
// Part flashes expire in simulation, even while a roll draws the whole hull.
const GP4_WARHIVE_TICK=warhiveTick;
warhiveTick=function(b,dt){const A=b._whv?.ace;if(A?.fl)for(const id in A.fl)A.fl[id]=Math.max(0,A.fl[id]-dt);return GP4_WARHIVE_TICK.apply(this,arguments);};

// Bombing passes are quick arcade targets at every difficulty. Apply after each
// owner assigns its HP, including opening bomb runs and planned reinforcements.
const GP4_BOMBER_HP=6,GP4_FLIGHT_SPAWN=fb2FlightSpawn,GP4_MISSION_SPAWN=missionJetSpawn;
function gp4BomberDurability(e){
 if(e&&run.stage===6){
  e.hp=e.maxhp=GP4_BOMBER_HP;e._gp4ArcadeBomber=true;
  // These fragile passes do not get the generic protected first impact.
  // A missile/heavy round with lethal damage must destroy one immediately.
  const marks=e._bofDamageEvents||(e._bofDamageEvents=Object.create(null));marks.hull=1;
 }
 return e;
}
fb2FlightSpawn=function(q){return gp4BomberDurability(GP4_FLIGHT_SPAWN.apply(this,arguments));};
missionJetSpawn=function(event,O){const e=GP4_MISSION_SPAWN.apply(this,arguments);return e&&(e._s67Bomber||event.kind==='bomb'||fb2MissionRole(e._mission29||{})==='green')?gp4BomberDurability(e):e;};
drawEnemy=function(e){
 if(run.stage===6&&e&&!e.dead&&e._dyingT==null&&(e.type==='s6bomber'||e.type==='s1jetbomber_b'||e._fb2Stealth||e._mission29||e._s67Bomber)){
  const a=e._fb2Stealth||e._mission29||{},dir=a.direction||e._s6Strike?.direction||'south';
  const role=a.role||fb2MissionRole(a),h=e._s67Draw||104;
  // These are four directional cells baked from the authored blue fighter. Their
  // red/green paint keeps the original shading, metal, outline and ordnance.
  if(role&&fb2SheetCell('fb2_stealth_'+role,FB2_DIR_FRAME[dir]??2,e.x-h/2,e.y-h/2,h,e)){
   e._drawW=e._drawH=h;return;
  }
 }
 return GP4_BASE.enemy.apply(this,arguments);
};

// Generators remain the quickest way through the field. Sustained shielding has
// a finite duty cycle so close-range weapons cannot leave the encounter sealed.
stage4ShieldTick=function(b,dt){GP4_BASE.shield.apply(this,arguments);const H=b?._s4war?.shield;if(!H||b.dead||b.enter)return;
 if(H.rearming){H.overloadAge=0;H.exposedFor=0;return;}
 if(H.exposedFor>0){H.exposedFor=Math.max(0,H.exposedFor-dt);if(!H.exposedFor&&H.nodes.some(n=>!n.dead)){H.active=true;H.overloadAge=0;stage4WarfareSound('shieldUp','bossPhase');}return;}
 if(!H.active){H.overloadAge=0;return;}H.overloadAge=(H.overloadAge||0)+dt;
 if(H.overloadAge>=18){H.active=false;H.exposedFor=8;H.overloadAge=0;H.breakT=.8;stage4WarfareSound('shieldBreak','bossPhase');floatText(b.x,b.y+b.h*.4,'GENERATOR OVERLOAD','#7feaff');}
};
markHit=function(t,f){
 if(t&&(t===boss||t===subBoss||t._mr27||t._r30)){
  const now=GP4.clock;if(now<(t._gp4FlashNext||0))return;t._gp4FlashNext=now+.14;f=Math.max(f||.16,.12);
 }
 return GP4_BASE.hit(t,f);
};

s6WingLaunch=function(n,all){
 const r=GP4_BASE.wing.apply(this,arguments),W=s6Wing;if(!W)return r;
 const allowed=gp4Allies();W.ships=W.ships.filter(q=>allowed.includes(q.key));
 W.ships.forEach((q,i)=>q.slot=i);return r;
};

PASSWORDS.RIFT9=9;PASSWORDS.XHARR=6;PASSWORDS.XREBEL=6;PASSWORDS.HARR6=6;PASSWORDS.REBEL6=6;
const GP4_MUSIC=Audio.startMusic;
Audio.startMusic=function(name){if(run._gp4StageX&&run.stage===6&&/^(boss\d+(mus)?|stagex|rival)$/.test(name))name='stagex';return GP4_MUSIC.call(this,name);};
submitPassword=function(){const code=String(pwInput).toUpperCase();GP4.route=['XHARR','HARR6'].includes(code)?'left':['XREBEL','REBEL6'].includes(code)?'right':null;
 GP4.stage6Only=code==='HARR6'||code==='REBEL6';return GP4_BASE.password.apply(this,arguments);};
function gp4QuickEncounter(){
 if(!GP4.routeReady||state!==GS.PLAY)return;const route=GP4.route,stageX=!GP4.stage6Only;GP4.routeReady=false;
 if(stageX)run._gp4StageX=route;else delete run._gp4StageX;GP4.route=null;GP4.stage6Only=false;
 s6Opening=null;story=null;fb2Talk=null;stagePlan=[];spawnClock=9999;waveIdx=9999;stageTimer=80;
 enemies=[];pBullets=[];eBullets=[];powerups=[];subBoss=null;subBossActive=false;subBossDone=subBossTriggered=true;
 s6WingInit();s6Wing.route=route;s6Wing.all=true;s6Wing.beats=3;s6Wing.fakeDone=true;s6Wing.supplyIndex=3;
 s6WingLaunch(4,true);s6Wing.line=null;bossDefeated=false;spawnBoss(route==='right'?'rebelsquad':'warhive');
 Audio.startMusic(stageX||route==='right'?'stagex':'boss6');H3.release=false;Input.clearTaps?.();
}
startRun=function(fromStage=1){const r=GP4_BASE.start.apply(this,arguments);
 // Boss passwords skip the level's opening flight; the encounter retains its own live introduction.
 if(fromStage===6&&GP4.routeReady){BOFCinematicDirector.cancel();storySkip();setState(GS.PLAY);gp4QuickEncounter();}return r;
};
beginStage=function(num){
 const r=GP4_BASE.begin.apply(this,arguments);GP4.deaths=[];GP4.death=null;GP4.routeReady=num===6&&!!GP4.route;
 delete run._gp4StageX;GP4.clock=0;smokeTrails=[];pImpacts=[];sprAnims=[];fadeOuts=[];pilotFx=[];
 efxBursts=[];fireDebris=[];_smokeRings=[];_navalFlashes=[];hudCallout=null;flashScreen=whiteBlast=shake=0;
 S81003.beams=[];s67Clouds=[];if(num===6)gp4AceWarm();return r;
};
scLeaveStage=function(R){
 if(run.stage!==6)return GP4_BASE.leave.apply(this,arguments);
 run.score=(run.score|0)+(R.bonus||0);run.lives=clamp(run.lives,0,9);
 if(R.seats)run2.score=(run2.score|0)+R.seats[1].bonus;
 drawStageClear._init=false;drawStageClear._res=null;Audio.stopMusic();run.mode='campaign';Rival24.scatterAfterHarrier();
 // Password entrants get the same deliberate map choice after Stage 6.
 run.mode='campaign';campaign.unlockedMax=Math.max(campaign.unlockedMax||1,7);
 campAutoAfterClear(6,7,R.rank);campSuspend();openStageSelect(7,{unlock:7});
};
updatePlay=function(dt){GP4.clock+=Math.max(0,dt);gp4QuickEncounter();
 if(run.stage===6&&(fb2TalkActive()||h3RebelIntro())){enemies.length=0;powerups.length=0;}
 return GP4_BASE.update.apply(this,arguments);};
gp4AceWarm();

// A threshold-crossing hit cannot skip the one final emergency reserve.
hammerBossDamage=function(b,dmg){const h=b._hammer;
 if(fb1002NormalHammer(b)&&!b.dead){
  if(h.gp4Emergency)return 0;
  const out=GP4_BASE.hammerDamage.apply(this,arguments);
  return h.gp4FailsafeSeen?out:Math.min(out,Math.max(0,b.hp-b.maxhp*.08));
 }return GP4_BASE.hammerDamage.apply(this,arguments);
};
hammerBossTick=function(b,dt){const h=b._hammer;
 if(fb1002NormalHammer(b)&&!b.dead&&!b.enter){
  if(!h.gp4FailsafeSeen&&b.hp<=b.maxhp*.08001){
   h.gp4FailsafeSeen=true;h.gp4Emergency={t:0,from:b.hp};h.recovery=null;h.frRecovery=false;
   h.restorationSeen=true;h._fb2RageDone=true;h.hammerDestroyed=false;h.hammerHP=h.hammerMax;
   const A=fr27Armor(b)||fr27BeginArmor(b);if(A){A.hp=0;A.active=false;A.barrier=0;A.checkpoints=[.75,.50,.35,.15];A.rage=true;}
   hammerState(b,'storm_raise');h.empowered=true;h.empowerLevel=1;
   floatText(b.x,b.y-100,'EMERGENCY RESERVE','#ff66bf');Audio.SFX.bossWeaponCharge?.();
  }
  const E=h.gp4Emergency;if(E){E.t+=dt;h.t=E.t;h.chromiumT=(h.chromiumT||0)+dt;
   b.hp=lerp(E.from,b.maxhp*.38,clamp(E.t/3,0,1));b.flash=0;
   if(E.t>=3){b.hp=b.maxhp*.38;h.gp4Emergency=null;h.rage=999;h.empowered=false;
    h.mode='hammer';h.comboPending=false;h.followCount=0;h.frResume=null;hammerTarget(b);hammerState(b,'warn');
    spawnShockRing(b.x,b.y,180,'comet');Audio.SFX.bossPhase?.();}return;
  }
  // An interrupted ordinary restore gives a short punish, then resumes combat.
  if(h.state==='fr_stun'&&h.t>=1.6)h.t=Math.max(h.t,FR27_STUN_T-dt);
 }
 return GP4_BASE.hammerTick.apply(this,arguments);
};

// Play the existing modular body/head death before allowing the still sequence.
const GP4_END_START=h3EndingStart,GP4_END_TICK=h3EndingTick,GP4_END_DRAW=h3EndingDraw;
h3EndingStart=function(b){GP4_END_START(b);H3.ending.engineDeath=0;H3.ending.phase='engineDeath';b.dying=0;};
h3EndingTick=function(dt){const e=H3.ending;if(!e)return;
 if(e.engineDeath!=null){e.engineDeath+=dt;e.phase='engineDeath';stageEnding=0;
  hammerBossDeathTick(e.boss,dt);_stage5SpaceScroll+=dt*24;efxTick(dt);tickSmokeRings(dt);
  if(e.engineDeath>=8){delete e.engineDeath;e.t=0;e.phase='overhead';whiteBlast=shake=0;}return;
 }
 const r=GP4_END_TICK(dt);
 if(H3.ending&&['welcome','descent'].includes(e.phase)){e.homeAge=(e.homeAge||0)+dt;_stage5SpaceScroll+=dt*55*(1-clamp(e.descent/8,0,1));}return r;
};
h3EndingDraw=function(){const e=H3.ending;if(!e)return;
 if(e.phase!=='engineDeath'&&!['welcome','descent'].includes(e.phase))return GP4_END_DRAW();
 ctx.save();worldXformEscape();ctx.save();ctx.translate(-camX,0);drawBG(0);
 if(e.phase==='engineDeath'){
  drawSmokeRings(false);fb1002HammerDeathDraw(e.boss);const t=e.engineDeath;
  for(let i=0;i<10;i++){const age=t-3.9-i*.21;if(age>=0&&age<1.5){const x=e.boss.x+Math.sin(i*4.3)*80,y=e.boss.y+Math.cos(i*2.8)*80;
   efxFrame('efx_burst_fire',Math.min(7,Math.floor(age/1.5*8)),x-70,y-70,140,140,1);}}
  drawSmokeRings(true);furyShipDrawFlight(player.x,Math.min(player.y,VH*.78),SPACE_SHIP_SIZE*1.5,_pilotKey(),{key:'base'},t);
  ctx.restore();if(whiteBlast>0){ctx.fillStyle='rgba(255,255,255,'+clamp(whiteBlast,0,1)+')';ctx.fillRect(0,0,VW,VH);}
  if(t>7){ctx.fillStyle='rgba(0,0,0,'+clamp(t-7,0,1)+')';ctx.fillRect(0,0,VW,VH);}ctx.restore();return;
 }
 ctx.restore();const u=clamp(e.descent/8,0,1),smooth=u*u*(3-2*u),size=VW*(.22+.04*smooth),py=VH*.20;
 if(XART.rdy('h3_earth'))ctx.drawImage(XART.get('h3_earth'),VW/2-size/2,py-size/2,size,size);
 const y=lerp(VH*.68,py,smooth),ship=lerp(SPACE_SHIP_SIZE*1.5,3,smooth);
 furyShipDrawFlight(VW/2,y,ship,_pilotKey(),{key:'base'},e.t);
 for(let i=0;i<6;i++){const age=(e.homeAge||0)-i*.23;if(age>=0&&age<1.25)efxFrame('efx_burst_fire',Math.min(7,Math.floor(age*6)),VW*(.22+(i%3)*.28)-30,VH*.43+Math.floor(i/3)*60,60,60,.85);}
 if(e.phase==='welcome'&&e.cheer<H3_CHEERS.length){const [who,line]=h3Cheer(e);h3Radio(who,line,e.shown,VH*.75);}
 const fade=Math.max(1-clamp((e.homeAge||0)/1.2,0,1),clamp((e.descent-8)/1.6,0,1));
 if(fade){ctx.fillStyle='rgba(0,0,0,'+fade+')';ctx.fillRect(0,0,VW,VH);}ctx.restore();
};

// Shock portraits are the fourth expression in each approved four-column sheet.
const GP4_TOUCH=XART._touch;
XART._touch=function(k){if(!String(k).startsWith('gp4_death_'))return GP4_TOUCH.apply(this,arguments);
 const pilot=k.slice(10),raw='h3_portrait_'+pilot;if(!XART.rdy(raw))return null;
 let c=GP4.portraits.get(pilot);if(!c){c=document.createElement('canvas');c.width=c.height=256;c.complete=true;c.naturalWidth=c.naturalHeight=256;GP4.portraits.set(pilot,c);}
 const g=c.getContext('2d'),im=XART.get(raw),sw=im.width/4,s=Math.min(256/sw,256/im.height),w=sw*s,h=im.height*s;
 g.clearRect(0,0,256,256);g.imageSmoothingEnabled=false;g.drawImage(im,sw*3,0,sw,im.height,(256-w)/2,(256-h)/2,w,h);
 const d=GP4.death;if(d?.q.key===pilot){g.globalCompositeOperation='source-atop';g.fillStyle='rgba(255,255,255,'+clamp((d.t-.8)/3.2,0,1)+')';g.fillRect(0,0,256,256);g.globalCompositeOperation='source-over';}return c;
};
const GP4_REBEL_TICK=rebelSquadTick,GP4_REBEL_DRAW=rebelSquadDraw;
rebelSquadDamage=function(b,dmg){const R=b._rebels,q=R.ships[R.hit],G=R.gang1004;R.hit=-1;
 if(!q||q.dead||!R.frIntro?.done||G?.scene||q.mode==='entry'||q.warp>0||!(dmg>0))return;
 const dealt=Math.min(q.hp,dmg);q.hp-=dealt;b.hp=Math.max(0,b.hp-dealt);q.flash=.12;stageStats.dmgDealt+=dealt;
 if(q.hp<=0){q.dead=true;q.frCloak=0;q._gpDeath={t:0,x:q.x,y:q.y};q.rg4&&(q.rg4.deathSeen=true,q.rg4.act=null);
  GP4.deaths.push({q,t:0});if(G){G.beams=G.beams.filter(v=>v.owner!==q);G.ord=G.ord.filter(v=>v.owner!==q);}Audio.SFX.playerHit?.();}
 if(G&&R.ships.some(v=>!v.dead))rg4Threshold(b,G);
};
rebelSquadTick=function(b,dt){const r=GP4_REBEL_TICK.apply(this,arguments);if(b.dead)return r;
 for(const q of b._rebels.ships){const D=q._gpDeath;if(!D)continue;D.t+=dt;
  if(D.t>=2.8&&!D.crash){D.crash=true;const y=D.y+Math.min(110,VH-D.y-60);spawnShockRing(D.x,y,85,'comet');explode(D.x,y,80,'red');Audio.SFX.expBig?.();}}
 if(!GP4.death&&GP4.deaths.length)GP4.death=GP4.deaths.shift();if(GP4.death){GP4.death.t+=dt;if(GP4.death.t>=4.4)GP4.death=null;}
 if(!GP4.death&&!GP4.deaths.length&&b._rebels.ships.every(q=>q.dead&&q._gpDeath?.crash))bossDie();return r;
};
rebelSquadDraw=function(b){GP4_REBEL_DRAW.apply(this,arguments);
 for(const q of b._rebels.ships){const D=q._gpDeath;if(!D||D.t>=2.8)continue;const key='rr_ship_'+REBEL_SHIPS[q.i];if(!XART.rdy(key))continue;
  const im=XART.get(key),u=D.t/2.8,w=SHIP_DRAW_H*1.5,h=w*im.height/im.width,y=D.y+u*u*Math.min(110,VH-D.y-60);
  ctx.save();ctx.translate(D.x,y);ctx.rotate(u*TAU*2);ctx.drawImage(im,-w/2,-h/2,w,h);ctx.restore();
  efxFrame('efx_burst_fire',Math.floor(D.t*14)%8,D.x-28,y-28,56,56,.8);}
};
drawWorld=function(dt){const r=GP4_BASE.world.apply(this,arguments),d=GP4.death;if(!d||state!==GS.PLAY)return r;
 const who=d.q.key.toUpperCase(),line={voss:'MY ENGINES... I CANNOT HOLD HER!',nyx:'NO! MY CLOAK IS GONE!',rook:'HULL BREACH! MAYDAY!',kaia:'I... I CANNOT PULL OUT!',jace:'CONTROLS ARE DEAD! MAYDAY!'}[d.q.key];
 ctx.save();ctx.setTransform(SS,0,0,SS,0,0);dlgBox({who,portrait:false,portraitKey:'gp4_death_'+d.q.key,full:line,shown:line.slice(0,Math.floor(d.t*35)),screenSpace:false,forceShown:true,fade:1,tint:REBEL_TINT[d.q.i],pw:VW*.94,ph:VH*.26,x:VW*.03,y:VH*.69});ctx.restore();return r;
};

// Keep the original pattern grammars, but remove dead air and strengthen the
// surviving central battery after the player dismantles the side weapons.
const GP4_ER_SET=er26Set,GP4_ER_COMBAT=er26Combat;
er26Set=function(b,mode){GP4_ER_SET.apply(this,arguments);const R=b._er26;if(!R||![3,4].includes(ER26_STAGE[b._ship]))return;
 if(mode==='recover')R.dur*=diffKey==='furious'?.62:diffKey==='hard'?.78:.9;
 else if(!['form-change','nuclear','overdrive'].includes(mode)){
  R.live*=diffKey==='furious'?1.20:1.08;R.dur=R.warm+R.live;R.gap*=diffKey==='furious'?.84:.94;
 }R.gp4CoreBeat=0;
};
er26Combat=function(b,dt){const r=GP4_ER_COMBAT.apply(this,arguments),R=b._er26;
 if(!R||!['frostcruiser','cryospear','olivewarden'].includes(b._ship)||R.t<R.warm||R.t>=R.dur)return r;
 if(!mr27CanFire(b,'L')&&!mr27CanFire(b,'R')){
  const live=R.t-R.warm,beat=Math.floor(live/(diffKey==='furious'?.8:1.15));
  if(beat>=R.gp4CoreBeat){R.gp4CoreBeat=beat+1;const a=R.angles[1];
   for(const off of [-.23,0,.23]){const q=eShootT(b.x,b.y+b.h*.32,a+off,3.6,'mg',{w:7,h:17,owner:b});q._boss=true;}
   Audio.SFX.enemyBossCannon?.();}
 }return r;
};

// Each new hull has a repeatable ranged identity. Hellhugger intentionally stays
// a fragile melee assassin; dismantling a weapon still cancels that weapon.
const GP4_MM_FIRE=mm1003Fire,GP4_MM_TICK=mm1003Tick;
mm1003Fire=function(e){const A=e._mm1003,D=MM1003_DEF[e._mutator1003];
 if(!['fan','pair','siege','cast'].includes(D.attack))return GP4_MM_FIRE(e);
 const beat=Math.floor(A.age/(D.attack==='pair'?.20:.34));if(beat<(A.gp4Beat||0)||beat>=4)return;
 A.gp4Beat=beat+1;const T=A.target,aim=(x,y)=>Math.atan2(T.y-y,T.x-x);
 if(D.attack==='fan'){
  const x=e.x,y=e.y+e.h*.25;for(let i=-2;i<=2;i++)mm1003Shot(e,x,y,aim(x,y)+i*.23+(beat%2?.09:-.09),3.3+beat*.15,'blue');
 }else if(D.attack==='pair'){
  for(const side of [-1,1]){const x=e.x+side*e.w*.20,y=e.y+e.h*.28;mm1003Shot(e,x,y,aim(x,y)+side*(.18-beat*.04),4.1,'fire');}
 }else if(D.attack==='siege'){
  const side=beat%2?1:-1,x=e.x+side*e.w*.36,y=e.y+e.h*.21;
  for(const off of [-.24,0,.24])mm1003Shot(e,x,y,aim(x,y)+off,2.9,'fire',true);
 }else for(const p of A.parts.filter(p=>!p.dead&&p.kind==='arm')){
  const m=mm1003Pose(e,p);for(const off of [-.16,.16])mm1003Shot(e,m.mx,m.my,aim(m.mx,m.my)+off,3.2,'fire');p.recoil=3;
 }A.fired++;r30Sound(D.attack==='pair'?'enemyBossCannon':'combatOrb0927');
};
mm1003Tick=function(e,dt){const A=e._mm1003;if(!A)return GP4_MM_TICK.apply(this,arguments);
 const phase=A.phase;if(phase!=='fire')A.gp4Beat=0;
 // The committed salvo runs for four beats before its ordinary recovery.
 if(mm1003Alive(e)&&phase==='fire'&&['fan','pair','siege','cast'].includes(MM1003_DEF[e._mutator1003].attack)){
  if(mm1003Disarmed(e)){groundTargetingCancel(e);mm1003Set(e,'recover');return;}
  A.age+=dt;A.t+=dt;for(const p of A.parts){p.recoil=Math.max(0,p.recoil-dt*26);p.flash=Math.max(0,(p.flash||0)-dt);}
  mm1003Fire(e);if(A.age>1.4)mm1003Set(e,'recover');return;
 }return GP4_MM_TICK.apply(this,arguments);
};

// Fresh map art is registered under fresh keys to avoid stale packed/cached art.
const GP4_MAP_KEYS=[1,2,3,4,5,6,7,8,'hub'];
// Generated sheet order: infernal ruins -> 8, desert highway -> 4, orbital port -> 5.
const GP4_MAP_FILE={1:1,2:2,3:3,4:5,5:8,6:6,7:7,8:4,hub:'hub'};
XART._src.gp4_bridge='assets/game/gameplay_1004/bridge.png';XART.rdy('gp4_bridge');
for(const k of GP4_MAP_KEYS)for(const v of ['','_lock','_shadow','_glow']){
 const key='gp4_island_'+k+v;XART._src[key]='assets/game/gameplay_1004/island_'+GP4_MAP_FILE[k]+v+'.png';XART.rdy(key);
}
Object.assign(SSEL_POS,{1:[350,250],2:[700,250],3:[1050,250],4:[1050,600],5:[1050,950],6:[700,950],7:[350,950],8:[350,600]});
cmap2Order._o=null;
cmap2Size=function(k){return k===9?130:362;};
cmap2Bob=function(k){return Math.sin(cmap2.t*1.15+(k==='hub'?0:k)*1.7)*1.6-10*(cmap2.lift[k]||0);};
const GP4_MAP_CAMERA=cmap2CameraTick,GP4_MAP_RESET=cmap2Reset;
cmap2Reset=function(opts){const r=GP4_MAP_RESET.apply(this,arguments);cmap2.gp4Arrival=opts?.boot?0:null;return r;};
cmap2CameraTick=function(dt,cine,sel){
 if(sselBoot>0){cmap2.gp4Arrival=(cmap2.gp4Arrival||0)+dt;const u=clamp(cmap2.gp4Arrival/4,0,1);
  const target=map30Overview();cmap2.cam.x=target.x;cmap2.cam.y=target.y;cmap2.cam.z=target.z*lerp(.60,1,u*u*(3-2*u));return;}
 if(cine||s9MapCine||riftReturn||sel===9||Rival24.mapFocused||Rival24.flying)return GP4_MAP_CAMERA.apply(this,arguments);
 // Once the full theater is assembled, move into the selected region. The
 // camera follows navigation, so the authored islands are readable at play size.
 const p=cmap2World(sel)||cmap2World('hub'),z=.40,target=cmap2Clamp({x:lerp(700,p.x,.68),y:p.y},z),k=1-Math.exp(-dt*2.5);
 cmap2.cam.x+=(target.x-cmap2.cam.x)*k;cmap2.cam.y+=(target.y-cmap2.cam.y)*k;cmap2.cam.z+=(z-cmap2.cam.z)*k;
};
cmap2DrawWorld=function(dt,sel){const order=cmap2Order();ctx.save();ctx.imageSmoothingEnabled=false;
 if(XART.rdy('gp4_bridge'))for(const [a,b] of [[1,2],[2,3],[8,'hub'],['hub',4],[7,6],[6,5],[1,8],[8,7],[2,'hub'],['hub',6],[3,4],[4,5]]){
  const p=cmap2World(a),q=cmap2World(b),dx=q.x-p.x,dy=q.y-p.y;ctx.save();ctx.translate(p.x,p.y);ctx.rotate(Math.atan2(dy,dx));ctx.drawImage(XART.get('gp4_bridge'),0,-10,Math.hypot(dx,dy),20);ctx.restore();}
 for(const k of CM2_ISLANDS)cmap2.lift[k]=(cmap2.lift[k]||0)+((k===sel&&sselBoot===0?1:0)-(cmap2.lift[k]||0))*Math.min(1,dt*8);
 for(const k of order){const w=cmap2World(k),s=cmap2Size(k),prefix=k===9?'cm2_isl_9':'gp4_island_'+k,key=prefix+'_shadow';
  if(XART.rdy(key)){ctx.globalAlpha=.5;ctx.drawImage(XART.get(key),w.x-s/2+10,w.y-s/2+20,s,s);}}
 ctx.globalAlpha=1;
 for(const k of order){const w=cmap2World(k),s=cmap2Size(k),y=w.y+cmap2Bob(k)-4*(cmap2.lift[k]||0),prefix=k===9?'cm2_isl_9':'gp4_island_'+k;
  if(k===sel&&XART.rdy(prefix+'_glow')){ctx.globalAlpha=.45*(cmap2.lift[k]||0);ctx.drawImage(XART.get(prefix+'_glow'),w.x-s/2,y-s/2,s,s);ctx.globalAlpha=1;}
  const key=prefix+(cmap2Unlocked(k)?'':'_lock');if(XART.rdy(key))ctx.drawImage(XART.get(key),w.x-s/2,y-s/2,s,s);
 }ctx.restore();cmap2DrawClouds(sel);
};
