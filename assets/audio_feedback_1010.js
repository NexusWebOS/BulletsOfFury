"use strict";
/* Mike's Normal playthrough, October 10. One owner per corrected behavior. */
const AP10={events:[],base:{get:XART.get,fury:furyShipCanvas,shoot:pShoot,bomb:useBomb,
 retinaFire:retinaFire,autoMissile:autoFireMissiles,volley:spaceVolleyAutoTick,
 elem:elementalDamageResult,weather:wfxUpdate,ram:ac10Ram,spawn:spawnEnemy},clock:0};
function ap10Log(kind,data={}){AP10.events.push({kind,...data});if(AP10.events.length>160)AP10.events.shift();}
// Ordinary neutral flight is the approved stable plate; banking, rolls and
// attack poses remain owned by their existing authored reels.
XART.get=function(key){if(/^ship_(axel|cole|decker|falva|freezer|juggernaut|lizzie|maverick|yuri)$/.test(key))return SM10.base.get.call(this,key);
 return AP10.base.get.apply(this,arguments);};
furyShipCanvas=function(key,pilot){return key==='base'?SM10.base.fury.call(this,key,pilot):AP10.base.fury.apply(this,arguments);};
function ap10Charging(){
 return !!(special?.mavCharging||special?.charging||special?.held||
  specialActive('falva')&&special?.charging||player?._fuse>0||player?._chgOn||
  typeof _frzOrb!=='undefined'&&_frzOrb?.charging||run?._spaceShadowHeld||run?._spaceShadowCharge>0);
}
useBomb=function(){if(ap10Charging())return;return AP10.base.bomb.apply(this,arguments);};
retinaFire=function(){if(ap10Charging())return true;return AP10.base.retinaFire.apply(this,arguments);};
autoFireMissiles=function(){if(ap10Charging())return;return AP10.base.autoMissile.apply(this,arguments);};
spaceVolleyAutoTick=function(dt,firing){if(ap10Charging())return;return AP10.base.volley.apply(this,arguments);};
// Normal spread pellets retain their physical lanes; incoming orb-work aiming
// must not turn a spread weapon into a homing weapon.
const AP10_STEER=fb10Steer;
fb10Steer=function(b,dt){if(b.kind==='spread'){b._steerX=null;return;}return AP10_STEER.apply(this,arguments);};
// All MG upgrades use at most the two physical wing lanes. Other specials and
// independent helper guns remain separate emitters.
pShoot=function(){const n=pBullets.length,r=AP10.base.shoot.apply(this,arguments);
 if(!spaceWeaponsActive()&&[0,7].includes(run.weapon)&&!specialActive()){
  const born=pBullets.slice(n).filter(b=>b.kind==='mg'&&!b._child&&!b.ally);
  if(born.length>2){const order=born.slice().sort((a,b)=>a.x-b.x),keep=new Set([order[0],order.at(-1)]);
   pBullets=pBullets.filter((b,i)=>i<n||!born.includes(b)||keep.has(b));}
 }return r;};
// Same-element bosses resist the whole damaging round, including orb shards.
// Keep the existing critical weakness reactions and ordinary enemy tuning.
elementalDamageResult=function(t,role,b,dmg,x,y){const r=AP10.base.elem.apply(this,arguments);
 if(['boss','subboss'].includes(role)&&r.reaction?.startsWith('absorb-'))r.dmg=Math.min(r.dmg,dmg*.20);
 return r;};

/* The generic motion bank used to intercept these planes before their actual
   stealth palette could draw. Keep the existing flight/attack controller and
   select the authored direction cell before that fallback. */
const AP10_AIR_TYPES=new Set(['s6lancer','s6cyclone','s6skimmer','s6dart','s6thunder','s6bomber','s6mine']);
const AP10_ENEMY_DRAW=drawEnemy;
function ap10StealthDraw(e){
 if(run.stage!==6||e.dead||e._dyingT!=null||!AP10_AIR_TYPES.has(e.type)&&!e._mission29&&!e._fb2Stealth&&!e._s6Strike)return false;
 const A=e._fb2Stealth||e._mission29||e._s6Strike||{},dir=A.direction||'south';
 let role=e._fb2Stealth?.role||(e._mission29?fb2MissionRole(A):null);
 if(!role&&on5Bomber(e))role=(e._side??e._dir??1)>0?'red':'green';
 if(role==='orange')role=null;
 const size=e._s67Draw||((e._mission29||e._fb2Stealth)?104:Math.max(64,e._drawH||e.h||64));
 let drawn=false;
 if(role){fb2Warm();drawn=fb2SheetCell('fb2_stealth_'+role,FB2_DIR_FRAME[dir]??2,e.x-size/2,e.y-size/2,size,e);}
 else {const f=dir==='east'?0:dir==='west'?1:2;ctx.save();ctx.translate(e.x,e.y);if(dir==='north')ctx.rotate(Math.PI);
  drawn=missionCell('bluejets',f,-size/2,-size/2,size,size);
  if(drawn&&e.flash>0)s67CellFlash('bluejets',f,-size/2,-size/2,size,size,e);ctx.restore();}
 if(drawn){e._sm10Facing=dir;e._ap10Palette=role||'blue';e._drawW=e._drawH=size;}return drawn;
}
drawEnemy=function(e){if(ap10StealthDraw(e))return;return AP10_ENEMY_DRAW.apply(this,arguments);};
// Wave birth owns the audible arrival. Simulation checks this once, with no
// delayed callback that can become blocked by the next boss warning.
wfxUpdate=function(dt){const old=wfx?.fseq?.wave,r=AP10.base.weather.apply(this,arguments),wave=wfx?.fseq?.wave;
 if(wave&&wave!==old)ap10Log('firewall-arrival');
 return r;};
// Easy kills and purposeful dives. The target freezes at the end of the tell;
// Hard/Furious add one circular approach, never a steering ram after release.
ac10Ram=function(e,dt){
 delete e._esh;delete e._s2Act;delete e._s3Act;e.armed=false;e.shoots=false;e.fireCd=999;
 const furious=diffKey==='furious'||diffKey==='insanity',hard=diffKey==='hard'||furious;
 const q=e._ac10Ram||(e._ac10Ram={phase:'entry',t:0,speed:0});q.t+=dt;e._bank=0;e.spin=0;
 if(q.phase==='entry'){e.y+=(hard?150:125)*dt;
  if(e.y>=PLAY.y+PLAY.h*.24){q.phase=hard?'orbit':'tell';q.t=0;q.cx=e.x;q.cy=e.y;
   q.tell=furious?.44:hard?.54:.70;
   const p=targetShip(e.x,e.y);q.x=p.x;q.y=p.y;q.angle=Math.atan2(p.y-e.y,p.x-e.x);}}
 else if(q.phase==='orbit'){
  const duration=furious?.70:.95,a=q.t/duration*TAU,side=q.cx<worldWidth()/2?-1:1;
  e.x=q.cx+Math.sin(a)*38*side;e.y=q.cy+(1-Math.cos(a))*30;
  if(q.t>=duration){e.x=q.cx;e.y=q.cy;q.phase='tell';q.t=0;const p=targetShip(e.x,e.y);q.x=p.x;q.y=p.y;q.angle=Math.atan2(p.y-e.y,p.x-e.x);}
 }else if(q.phase==='tell'){
  e._chg=1;const tell=q.tell=furious?.44:hard?.54:.70;
  if(q.t>=tell){q.phase='ram';q.t=0;q.speed=hard?190:150;e._chg=0;Audio.SFX.turbo?.();}
 }else{
  q.speed=Math.min(furious?400:hard?300:260,q.speed+480*dt);
  e.x+=Math.cos(q.angle)*q.speed*dt;e.y+=Math.sin(q.angle)*q.speed*dt;
  let contact=false;for(const seat of seatList())withSeat(seat,()=>{
   if(!player.dead&&!player.out&&Math.abs(e.x-player.x)<e.w*.5+(player._hx??9)-1&&Math.abs(e.y-player.y)<e.h*.5+(player._hy??10)-2){contact=true;playerHit('Kamikaze impact');}});
  if(contact){e.hp=0;e.score=0;e.dropOk=false;killEnemy(e);return;}
  if(e.y>VH+80||e.y<PLAY.y-100||e.x<camLeftX()-100||e.x>camRightX()+100)e.dead=true;
 }
};
spawnEnemy=function(){const n=enemies.length,r=AP10.base.spawn.apply(this,arguments),e=enemies.length>n?enemies.at(-1):null;
 if(e&&ac10Small(e)){e.hp=e.maxhp=e._maxhp=EHP(diffKey==='easy'?4:diffKey==='normal'?6:8);
  e.w=Math.max(e.w||0,30);e.h=Math.max(e.h||0,34);e._drawW=Math.max(e._drawW||0,48);e._drawH=Math.max(e._drawH||0,52);}
 return r;};

// Lock pilot movement for the stolen-tech showcase, while the simulation,
// background and every scripted ship continue advancing normally.
const AP10_HOLD=Input.hold;
Input.hold=function(seat,action){
 if(h3RebelIntro()&&['up','down','left','right'].includes(action))return false;
 return AP10_HOLD.apply(this,arguments);
};
const AP10_CONTROLS=s6OpeningControlsLocked;
s6OpeningControlsLocked=function(){return h3RebelIntro()||AP10_CONTROLS.apply(this,arguments);};
const AP10_RETINA=updateRetina;
updateRetina=function(dt){
 const t=retina.target;
 if(t&&(!Number.isFinite(t.x+t.y)||t.hp<=0||t.dead||t._dyingT!=null||t._retinaOwner?.dead)){
  retina.target=null;retina.phase=null;retina.holdCd=0;
 }
 return AP10_RETINA.apply(this,arguments);
};
// A second controller used to draw a smaller rebel radio over the cinematic
// plate. During the introduction the H3 radio owns the single live window.
const AP10_REBEL_RADIO=s6WingRadioDraw;
s6WingRadioDraw=function(){if(h3RebelIntro()||fb2TalkActive())return;return AP10_REBEL_RADIO.apply(this,arguments);};

/* Map directions mean the direction on screen. A missing neighbor holds the
   cursor instead of wrapping to the other side of the campaign. */
function ap10MapNeighbor(from,dx,dy,lo=1,hi=Math.min(8,campaign.unlockedMax||1)){
 const p=cmap2World(from);if(!p)return from;let best=from,score=Infinity;
 const cleared8=campaign.rank?.[8]&&campaign.rank[8]!=='incomplete';
 for(let k=lo;k<=hi;k++){
  if(k===from||k===1&&from>=7&&!cleared8)continue;
  const q=cmap2World(k);if(!q)continue;const x=q.x-p.x,y=q.y-p.y,along=x*dx+y*dy,cross=Math.abs(x*dy-y*dx);
  if(along<=2)continue;const value=Math.hypot(x,y)+cross*1.8;
  if(value<score){score=value;best=k;}
 }return best;
}
sselMoveHorizontal=function(dir,lo,hi,from){return ap10MapNeighbor(from??sselCursor,dir<0?-1:1,0,lo,hi);};
map4hVertical=function(dir){
 if(sselCursor===6&&dir<0&&!campaign.bonusUnlocked){map4hSelectX();return;}
 const k=ap10MapNeighbor(sselCursor,0,dir);if(k!==sselCursor){sselCursor=k;Audio.SFX.blip();}
};
map4eShipHeading=function(from,to,dx){
 const p=from==='x'?map4eStageXPoint():cmap2World(from),q=to==='x'?map4eStageXPoint():cmap2World(to);
 return p&&q?Math.atan2(q.x-p.x,p.y-q.y):dx<0?-Math.PI/2:Math.PI/2;
};
const AP10_MAP={open:openStageSelect,bob:cmap2Bob,bar:cmap2BarDraw};
openStageSelect=function(){
 for(const key of Object.keys(XART._src))if(/^(cm2_|map4f_|map4h_|mapg_)/.test(key))XART.rdy(key);
 return AP10_MAP.open.apply(this,arguments);
};
cmap2Bob=function(k){return AP10_MAP.bob.apply(this,arguments)+(k===sselCursor?Math.sin(cmap2.t*2.4)*5:0);};
cmap2BarDraw=function(dt){if(cmap2.focus!=='bar'&&!campPause)return;return AP10_MAP.bar.apply(this,arguments);};
sselShipDraw=function(){
 if(!sselShip)return;const sh=sselShip,pk=_pilotKey(),im=map4eShipFrame('ship_'+pk,sh.head)||map4eShipFrame('ship_cole',sh.head);if(!im)return;
 const size=40/(cmap2On()?Math.max(.25,cmap2.cam.z):1),k=size/Math.max(im.width,im.height);
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,sh.x-im.width*k/2,sh.y-im.height*k/2,im.width*k,im.height*k);ctx.restore();
};
