'use strict';
/* October 9 feedback pass (Mike, played locally). One owner for the combat fixes in this pass;
   the campaign-map camera lives in campaign_follow_1009.js. See docs/FEEDBACK_1009.md. */

/* ---------------------------------------------------------------- Stage 1: the land mask
   "There should be no boats on land."
   ensureS1LandMasks takes the live plate when it is decoded and the old 800x3616 mapJungle image
   otherwise, and caches whichever it got first forever. Stage 1's 680x4212 plate is rarely
   decoded on the first play frame, so in practice every boat and tank was placed against the old
   map: boats beached on its "land" and then slid down the screen over the real jungle. The mask
   now follows the plate as soon as it is ready, and remembers which image it was built from. */
const FB9_MASK_BASE=ensureS1LandMasks;
ensureS1LandMasks=function(){
 if(typeof _levelCfg!=='function'||typeof XART==='undefined')return;
 const c=run.stage===1?_levelCfg():_levelCfg(1);if(!c||!c.master)return FB9_MASK_BASE.apply(this,arguments);
 for(const [key,plate] of [['mapJungle',c.master],['mapJungleDam',c.destroyed]]){
  if(!plate)continue;const m=_landMasks[key];
  if(m&&m._plate===plate)continue;
  if(XART.rdy(plate)){delete _landMasks[key];_buildLandMask(XART.get(plate),key);
   if(_landMasks[key])_landMasks[key]._plate=plate;}
 }
 if(!_landMasks.mapJungle||!_landMasks.mapJungleDam)FB9_MASK_BASE.apply(this,arguments);
};

/* ---------------------------------------------------------------- Stage 1 miniboss (Razorback)
   "Do not allow the level one mini boss's sonic projectiles to be shootable."
   Measured on Normal and Furious: player fire never destroyed an rzbSonic orb, but it did shoot
   down the razor missiles that the hull launches straight out of the same green charge glow (27
   of them in a 40-second Furious fight). So every Razorback round is now weapon-proof: no
   interception, no lock-on target and no Retina reticle. Dodging is the counterplay. */
const FB9_RZB={shot:rzbShot,missile:rzbMissile,intercept:enemyOrdnanceCanIntercept,sprite:rzbSprite,
 muzzle:wm26Draw,draw:razorbackDraw};
function fb9RzbProof(from){for(let i=from;i<eBullets.length;i++){const q=eBullets[i];
 if(q&&q._rzb){q._weaponProof=true;q._shootable=false;q.hp=undefined;q._fb9RzbProof=true;}}}
rzbShot=function(){const n=eBullets.length,r=FB9_RZB.shot.apply(this,arguments);fb9RzbProof(n);return r;};
rzbMissile=function(){const n=eBullets.length,r=FB9_RZB.missile.apply(this,arguments);fb9RzbProof(n);return r;};
enemyOrdnanceCanIntercept=function(q){return q&&q._fb9RzbProof?false:FB9_RZB.intercept.apply(this,arguments);};

/* "Palette swap his charge up on Furious to be red instead of green."
   The charge draw asked rzbSprite for tint '#ff1838', but rzbSprite only recognises 'furious'
   (which swaps to the authored rzbf_ red set), so the green rzb_sonic_charge plate always drew.
   The release flash used the green sonic muzzle palette regardless of difficulty, too. */
let fb9RzbFurious=false;
rzbSprite=function(key,x,y,a,s,alpha,px,py,mul,tint){
 if(tint==='#ff1838'||fb9RzbFurious&&/^rzb_sonic_/.test(key))tint='furious';
 return FB9_RZB.sprite.call(this,key,x,y,a,s,alpha,px,py,mul,tint);};
razorbackDraw=function(b){fb9RzbFurious=!!(b&&b._rzb&&b._rzb.furious);
 try{return FB9_RZB.draw.apply(this,arguments);}finally{fb9RzbFurious=false;}};
wm26Draw=function(g,family,x,y,angle,progress,size,color){
 if(fb9RzbFurious&&family==='sonic')color='#ff2a3c';
 return FB9_RZB.muzzle.call(this,g,family,x,y,angle,progress,size,color);};

/* ---------------------------------------------------------------- jerky enemies (all stages)
   "Towards the middle of the level, before and after the mini boss... very jumpy enemies jerking
   around, and enemies appearing out of nowhere."
   Measured on Stage 1 (property traps on every enemy's x/y): every jump over 7px in one frame
   came from enemySeparate. It runs 20 relaxation passes and lands the whole correction in one
   frame, and sepClearAircraft can relocate a stuck aircraft to another lane outright, which reads
   as a jet appearing from nowhere. Stage 1 tanks then fought it: s1tank's drive step snaps x back
   to its own lane every frame, so a shoved tank vibrated between the two positions.
   Separation now has a per-frame budget for any unit on screen, so contacts resolve as a short
   glide. Units still above the reveal line queue at full strength, as before. A tank shoved
   sideways keeps the lane it was shoved to. */
const FB9_SEP={run:enemySeparate,x:sepShift,y:sepShiftY,step:3.2};
let fb9SepFrame=0;
function fb9SepBudget(e,axis,d){
 const half=(e.h||0)*.5,vt=typeof viewTopY==='function'?viewTopY():0;
 if(e.y+half<=vt||e.y-half>=VH)return d;                   // off screen: no one sees the queue
 if(e._fb9SepF!==fb9SepFrame){e._fb9SepF=fb9SepFrame;e._fb9SepX=0;e._fb9SepY=0;}
 const k=axis==='x'?'_fb9SepX':'_fb9SepY',used=e[k],room=FB9_SEP.step-Math.abs(used);
 if(room<=0)return 0;
 const out=clamp(d,-room,room);return out;
}
enemySeparate=function(){fb9SepFrame++;return FB9_SEP.run.apply(this,arguments);};
sepShift=function(e,dx){
 const want=fb9SepBudget(e,'x',dx);if(!want)return 0;
 const moved=FB9_SEP.x(e,want);
 if(moved){if(e._fb9SepF===fb9SepFrame)e._fb9SepX+=moved;if(e._tankLane!=null)e._tankLane+=moved;}
 return moved;
};
sepShiftY=function(e,dy){
 const want=fb9SepBudget(e,'y',dy);if(!want)return 0;
 const moved=FB9_SEP.y(e,want);
 if(moved&&e._fb9SepF===fb9SepFrame)e._fb9SepY+=moved;
 return moved;
};

/* ---------------------------------------------------------------- HUD at the bottom
   "The HUD for the game should be on the bottom of the screen, but the top section should still
   remain for the score bar that we created, and the boss bar will be below that."
   Every seat's 104px HUD row is a 70px five-panel housing over a 34px score strip, drawn to #hud
   (now off screen) by player_hud_1008.js, unchanged. After each frame's HUD draw this copies the
   score strips to #hud-top above the playfield and the housings to #hud-bot under it. The boss
   and miniboss bars are drawn at the top of the playfield, directly below the score strip.
   index.html's fit() splits the same height budget between the two rows. */
const FB9_HUD={rec:debugRecFrame,top:document.getElementById('hud-top'),bot:document.getElementById('hud-bot'),
 row:document.getElementById('hud-row'),div:document.getElementById('hud-div'),
 brow:document.getElementById('hud-bottom'),bdiv:document.getElementById('hud-div2'),ROW:104,HOUSE:70};
function fb9HudSplit(){
 const src=hudcv,T=FB9_HUD.top,B=FB9_HUD.bot;if(!src||!T||!B)return;
 const rows=Math.max(1,Math.round(src.height/(FB9_HUD.ROW*(src.width/VW)))),k=src.height/(FB9_HUD.ROW*rows);
 const strip=(FB9_HUD.ROW-FB9_HUD.HOUSE)*k,house=FB9_HUD.HOUSE*k,w=src.width;
 if(T.width!==w||T.height!==Math.round(strip*rows)){T.width=w;T.height=Math.round(strip*rows);}
 if(B.width!==w||B.height!==Math.round(house*rows)){B.width=w;B.height=Math.round(house*rows);}
 const tg=T.getContext('2d'),bg=B.getContext('2d');tg.imageSmoothingEnabled=false;bg.imageSmoothingEnabled=false;
 tg.clearRect(0,0,T.width,T.height);bg.clearRect(0,0,B.width,B.height);
 for(let i=0;i<rows;i++){const y=i*FB9_HUD.ROW*k;
  tg.drawImage(src,0,y+house,w,strip,0,i*strip,w,strip);
  bg.drawImage(src,0,y,w,house,0,i*house,w,house);}
 // The game shows, hides and greys the HUD through #hud-row / #hud-div / #hud; mirror it below.
 if(FB9_HUD.brow&&FB9_HUD.row)FB9_HUD.brow.style.visibility=FB9_HUD.row.style.visibility;
 if(FB9_HUD.bdiv&&FB9_HUD.div)FB9_HUD.bdiv.style.visibility=FB9_HUD.div.style.visibility;
 T.style.filter=B.style.filter=src.style.filter||'';
}
// loop() calls debugRecFrame once per frame immediately after it draws the HUD.
debugRecFrame=function(){fb9HudSplit();return FB9_HUD.rec.apply(this,arguments);};

/* ---------------------------------------------------------------- Stage 1 jets
   1) "The jets on level one have weird twisting animations." The evasive barrel roll plays the
      authored furyjet_<v>_roll_0..7 reel; on the black delta (variant 0) those cells are not a
      roll at all, they jump between unrelated headings. The art needs regenerating (held this
      pass), so the evasion keeps its sideways break on the steady nose-south pose instead.
   2) "Bomber jets... that actually function like bomber jets." Until new bomber art is generated
      the existing s1jetbomber flies a committed straight run with no guns and no hunting, and
      lays a stick of bombs along its lane. Each bomb is the shared ground-targeting strike: a
      floor reticle under the release point, then the blast, so the stick reads and is dodged
      sideways. The black _b bomber keeps its Stage 6 roles. */
const FB9_JET={tick:jetTick,evade:furyJetEvadeTick,draw:drawEnemy};
furyJetEvadeTick=function(e,dt,threat){
 const r=FB9_JET.evade.apply(this,arguments);
 if(run.stage===1&&e._furyMove&&e._furyMove.kind==='roll')e._furyMove=null;   // no roll reel
 return r;
};
function fb9BomberInit(e){
 e._fb9Bomber={drop:diffKey==='easy'?.62:diffKey==='normal'?.5:.42,cd:.35,n:0};
 e._atk='none';e.shoots=false;e.fk=null;e._route='straight';e._s1Elite=null;e._s1Rush=false;e._lane=e.x;
 // jetTick's own first-frame init would zero the reload (and fire its rocket that frame) and enrol
 // the Elite hunter, so the bomber arrives already initialised
 if(e._jet==null){e._jet=1;e._burst=0;e._burstCd=99;e._dodge=0;e._y0=e.y;}
 e._shotCd=99;
}
function fb9BomberTick(e,dt){
 const B=e._fb9Bomber;B.cd-=dt;
 const L=camLeftX()+24,R=camRightX()-24,inside=e.y>PLAY.y+24&&e.y<VH*.68&&e.x>L&&e.x<R;
 if(inside&&B.cd<=0&&B.n<(diffKey==='furious'?8:6)){
  B.cd=B.drop;B.n++;
  const q=groundTargetingSpawn({kind:'missile',x:clamp(e.x+rnd(-5,5),L,R),y:clamp(e.y+34,PLAY.y+40,VH-24),
   track:false,lane:false,warn:diffKey==='easy'?1.05:diffKey==='normal'?.92:.8,active:.42,radius:26,size:66,
   sound:'expBig',shake:3,onImpact:g=>{explode(g.x,g.y,48,'red');explode(g.x+rnd(-12,12),g.y+rnd(-8,8),22,'orange',null,null,null,null,true);}});
  if(q)q._fb9Bomb=true;
  if(Audio.SFX.bombDrop)Audio.SFX.bombDrop();else if(Audio.SFX.whip)Audio.SFX.whip();
 }
}

/* 3) "Two jets coming off the side of the screen... a half circle motion coming from the left and
      right side, circling down and trying to fly off the screen vertically south. Somersaults,
      machine gun rounds or missiles."
      fb9SwoopPair() launches one delta from each side. Each flies in level, carves a smooth turn
      onto a southbound heading, and dives off the bottom edge. One of the pair loops a somersault
      at the top of its turn; the other fires an unguided missile at the pilot's position on the
      way out. Both fire short machine-gun bursts down their nose during the turn. Drawn with the
      authored delta plate rotated to the flight heading (a pitch squash sells the somersault). */
function fb9SwoopPair(){
 if(run.stage!==1||state!==GS.PLAY)return;
 const loopSide=Math.random()<.5?-1:1;
 for(const side of [-1,1]){
  const e=spawnEnemy('s1jetdelta',side<0?camLeftX()-34:camRightX()+34,VH*(side<0?.15:.21),{route:'straight'});
  if(!e)continue;
  e.x=side<0?camLeftX()-34:camRightX()+34;e.y=VH*(side<0?.15:.21);e.t=0;e.vx=0;e.vy=0;
  e.pattern='s1jet';e.shoots=false;e.fk=null;e._atk='none';e._noSep=true;e._s1Elite=null;e._jet=1;
  e._fb9Swoop={side,head:side<0?0:Math.PI,phase:'in',t:0,speed:diffKey==='easy'?190:diffKey==='furious'?250:220,
   turnAt:side<0?camLeftX()+viewW()*.24:camRightX()-viewW()*.24,R:92,loop:side===loopSide,looped:false,k:0,
   burst:0,shotCd:.4,missile:side!==loopSide,fired:false};
 }
}
function fb9SwoopTick(e,dt){
 const S=e._fb9Swoop;S.t+=dt;
 const fwd=()=>[Math.cos(S.head),Math.sin(S.head)];
 let along=S.speed;
 if(S.phase==='in'){
  if(S.side<0?e.x>=S.turnAt:e.x<=S.turnAt)S.phase='turn';
 }else if(S.phase==='turn'){
  const want=Math.PI/2,turn=S.speed/S.R*dt,d=Math.atan2(Math.sin(want-S.head),Math.cos(want-S.head));
  if(S.loop&&!S.looped&&Math.abs(d)<Math.PI/4){S.phase='loop';S.k=0;if(Audio.SFX.whip)Audio.SFX.whip();}
  else{S.head+=clamp(d,-turn,turn);if(Math.abs(d)<.01){S.head=want;S.phase='exit';}}
 }else if(S.phase==='loop'){
  // a somersault seen from above: climb toward the camera, flip over the top, come back down
  S.k+=dt/.95;along=S.speed*.9*Math.cos(S.k*TAU);
  if(S.k>=1){S.k=0;S.looped=true;S.phase='turn';}
 }else{
  along=S.speed*Math.min(1.45,1+(S.t-2)*.12);
  if(S.missile&&!S.fired&&e.y>VH*.30){S.fired=true;
   const T=targetShip(e.x,e.y),a=Math.atan2(T.y-e.y,T.x-e.x);
   const q=eShootT(e.x,e.y+18,a,3.4,'emissile',{w:11,h:18});if(q){q.homing=false;q._committed=true;q.turn=0;}}
 }
 const [fx,fy]=fwd();e.x+=fx*along*dt;e.y+=fy*along*dt;e.vx=fx*along/60;e.spin=0;
 // machine-gun bursts down the nose while the turn brings it across the field
 S.shotCd-=dt;
 if((S.phase==='turn'||S.phase==='exit')&&e.y>PLAY.y+16&&e.y<VH*.72&&e.x>camLeftX()+8&&e.x<camRightX()-8){
  if(S.burst>0&&S.shotCd<=0){S.burst--;S.shotCd=S.burst>0?.11:.85;
   const n=[Math.cos(S.head),Math.sin(S.head)],p=[-n[1],n[0]];
   for(const s of [-1,1])eShootT(e.x+n[0]*24+p[0]*s*9,e.y+n[1]*24+p[1]*s*9,S.head,4.4,'s1bullet',{silent:s>0});
   if(Audio.SFX.enemyMachineGun)Audio.SFX.enemyMachineGun();}
  else if(S.burst<=0&&S.shotCd<=0)S.burst=4;
 }
 if(e.y>VH+90||e.x<camLeftX()-140||e.x>camRightX()+140||S.t>12)e.dead=true;
}
function fb9SwoopDraw(e){
 const S=e._fb9Swoop,v=Math.max(0,furyJetVariant(e)),key='furyjet_'+v+'_bank_0';
 if(!XART.rdy(key))return false;
 const im=furyJetGreenFrame(key,v,XART.get(key)),size=Math.max(e.w,e.h)*1.10;
 const pitch=S.phase==='loop'?Math.cos(S.k*TAU):1,lift=S.phase==='loop'?1+.32*Math.sin(S.k*Math.PI):1;
 e._drawW=size;e._drawH=size;
 ctx.save();ctx.imageSmoothingEnabled=false;
 const shadow=xartTint(key,'#000000',1);
 if(shadow){ctx.save();ctx.globalAlpha=.25;ctx.translate(e.x+10*lift,e.y+18*lift);ctx.rotate(S.head-Math.PI/2);ctx.scale(1,pitch);
  ctx.drawImage(shadow,-size/2,-size/2,size,size);ctx.restore();}
 ctx.translate(e.x,e.y);ctx.rotate(S.head-Math.PI/2);ctx.scale(lift,lift*pitch);
 ctx.drawImage(im,-size/2,-size/2,size,size);
 const tint=tintColor(e);if(tint){const hit=xartTint(key,tint,tint==='#ffffff'?.9:.55);if(hit)ctx.drawImage(hit,-size/2,-size/2,size,size);}
 ctx.restore();return true;
}
jetTick=function(e,dt){
 if(e&&e._fb9Swoop&&!e.dead)return fb9SwoopTick(e,dt);
 if(run.stage===1&&e&&e.type==='s1jetbomber'&&!e._fb9Bomber&&!e.dead)fb9BomberInit(e);
 // jetTick's last branch fires a rocket for every _atk that is not mg/salvo, 'none' included
 if(e&&e._fb9Bomber)e._shotCd=99;
 const r=FB9_JET.tick.apply(this,arguments);
 if(e&&e._fb9Bomber&&!e.dead){e._s1Elite=null;fb9BomberTick(e,dt);}   // a bomber flies its lane, it does not hunt
 return r;
};
drawEnemy=function(e){
 if(e&&e._fb9Swoop&&!e.dead&&e._dyingT==null&&fb9SwoopDraw(e))return;
 return FB9_JET.draw.apply(this,arguments);
};

/* ---------------------------------------------------------------- Stage 2 miniboss (Inferno Reaver)
   "Cold damage is not actually doing critical damage to our boss nor making him flash blue. His
   body has too much HP or is taking too little damage... make his body spin and do other attacks...
   spinning around, aggressively charge at you and fling himself at you."
   Measured (Normal): cold rounds already deal +50% (3 vs 2 per round) and the shared gate sets
   _hitFlashColor blue, but av3ReaverHit cancels the hull flash and every module flashed a fixed
   white plate, so no hit ever looked cold. The modules hold 953 of 2016 HP, so ~1060 was left on
   the bare core, and the core's pixel test let 34 of 40 spread rounds through its gaps.
   Now: module flashes take the weakness colour. When the last module breaks, the core is capped
   at 28% HP, gets a fair round hitbox, and fights on its own: spinning fire spray, a warned
   spinning charge at the pilot, and a leap that slams down where the pilot stood. */
const FB9_RV={tick:er26Tick,brk:av3Break,at:av3ReaverAt,partDraw:av3PartDraw,draw:shipBossDraw};
av3PartDraw=function(b,p,q,alpha=1){
 const col=b&&['#83d9ff','#ff3b30'].includes(b._hitFlashColor)?b._hitFlashColor:null;
 if(!(p.flash>0)||!col||!XART.rdy('av3_reaver_parts'))return FB9_RV.partDraw.apply(this,arguments);
 const f=p.flash;p.flash=0;try{FB9_RV.partDraw.call(this,b,p,q,alpha);}finally{p.flash=f;}
 const r=AV3_ART.parts[p.cell],key='fb9-part-'+col+'-'+p.cell;let tint=AV3.cells.get(key);
 if(!tint){tint=document.createElement('canvas');tint.width=r[2];tint.height=r[3];const g=tint.getContext('2d');
  g.drawImage(XART.get('av3_reaver_parts'),...r,0,0,r[2],r[3]);g.globalCompositeOperation='source-in';g.fillStyle=col;g.fillRect(0,0,r[2],r[3]);AV3.cells.set(key,tint);}
 ctx.save();ctx.translate(q.x,q.y);ctx.rotate(q.a);ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=alpha*Math.min(.85,f*5);
 ctx.drawImage(tint,-p.pivot[0]*q.w,-p.pivot[1]*q.h,q.w,q.h);ctx.restore();
};
function fb9ReaverBare(b){return !!(b&&b._av3Reaver&&b._av3Reaver.parts.every(p=>p.id==='core'||p.dead));}
av3Break=function(b,p){const r=FB9_RV.brk.apply(this,arguments);
 if(b&&!b._fb9Body&&!b.dead&&fb9ReaverBare(b))fb9BodyStart(b);return r;};
av3ReaverAt=function(b,x,y){const r=FB9_RV.at.apply(this,arguments);
 if(r||!b||!b._fb9Body||b.dead||b.enter||b._noHit||!Number.isFinite(x+y))return r;
 const q=av3PartPose(b,av3Part(b,'core'));return Math.hypot(x-q.x,y-q.y)<=q.w*.56?'core':null;};
function fb9BodyStart(b){
 const R=b._er26;b.hp=Math.min(b.hp,Math.ceil(b.maxhp*.28));
 b._l23Beam=null;if(R){R.warnings=[];R.mode='recover';}groundTargetingCancel(b);
 b.w=b.h=104;b._noHit=false;b._s4MiniSafe=false;
 b._fb9Body={mode:'expose',t:0,spin:0,spinV:2,n:0,lift:0,vx:0,vy:0,shotCd:0,
  home:{x:(camLeftX()+camRightX())/2,y:R?R.home:150},warn:null,land:null,lvl:typeof er26Level==='function'?er26Level():0};
 explode(b.x,b.y,96,'orange');shake=Math.max(shake,8);
 if(typeof floatText==='function')floatText(b.x,b.y-60,'CORE EXPOSED','#ffb347');
 if(Audio.SFX.bossPhase)Audio.SFX.bossPhase();
}
function fb9BodyShot(b,a,speed,large){
 const q=eShootT(b.x,b._drawY??b.y,a,speed,'magma',{w:large?20:12,h:large?20:12,silent:true,noMuzzle:true});
 q._boss=true;q._noArsenal=true;q._er26Art='fire';q._er26Source='magmaward';q._er26Draw=large?44:30;
 q._er26Charred=!!(b._er26&&b._er26.level===2);q._weaponProof=true;return q;
}
function fb9BodyTick(b,dt){
 const B=b._fb9Body,M=b._av3Reaver,core=av3Part(b,'core');
 M.clock+=dt;for(const p of M.parts){p.flash=Math.max(0,p.flash-dt);p.kick=Math.max(0,p.kick-dt*35);}
 for(const d of M.debris){d.t+=dt;d.pose.x+=d.vx*dt;d.pose.y+=d.vy*dt;d.pose.a+=d.spin*dt;}M.debris=M.debris.filter(d=>d.t<1.2);
 B.t+=dt;b.fireCd=999;
 const L=camLeftX()+56,Rx=camRightX()-56,Top=PLAY.y+64,Bot=VH-64,lv=B.lvl,next=m=>{B.mode=m;B.t=0;};
 const ease=k=>{b.x+=(B.home.x-b.x)*Math.min(1,dt*k);b.y+=(B.home.y-b.y)*Math.min(1,dt*k);};
 if(B.mode==='expose'){B.spinV=lerp(B.spinV,4,dt*3);ease(2);if(B.t>.9)next('spray');}
 else if(B.mode==='spray'){                       // spin up and hose fire out of three arms
  B.spinV=lerp(B.spinV,9+lv*1.5,dt*3);ease(1.2);B.shotCd-=dt;
  if(B.t>.35&&B.shotCd<=0){B.shotCd=.13-lv*.015;for(let k=0;k<3;k++)fb9BodyShot(b,B.spin+k*TAU/3,2.5+lv*.3);}
  if(B.t>2.1+lv*.35)next('aim');
 }
 else if(B.mode==='aim'){                         // lock the pilot, wind up, show the lane
  B.spinV=lerp(B.spinV,15,dt*4);const T=targetShip(b.x,b.y);
  if(B.t<.45||!B.target)B.target={x:T.x,y:T.y};
  B.warn={x:b.x,y:b.y,ex:B.target.x+(B.target.x-b.x)*.35,ey:B.target.y+(B.target.y-b.y)*.35,progress:clamp(B.t/(.8-lv*.1),0,1),width:96};
  if(B.t>=.8-lv*.1){const a=Math.atan2(B.target.y-b.y,B.target.x-b.x),s=520+lv*70;B.vx=Math.cos(a)*s;B.vy=Math.sin(a)*s;B.warn=null;
   if(Audio.SFX.whip)Audio.SFX.whip();shake=Math.max(shake,4);next('charge');}
 }
 else if(B.mode==='charge'){                      // spinning ram; caroms off the play edges
  b.x+=B.vx*dt;b.y+=B.vy*dt;B.spinV=18;
  if(b.x<L||b.x>Rx){B.vx*=-.75;b.x=clamp(b.x,L,Rx);shake=Math.max(shake,5);explode(b.x,b.y,40,'orange');}
  if(b.y<Top||b.y>Bot){B.vy*=-.75;b.y=clamp(b.y,Top,Bot);shake=Math.max(shake,5);explode(b.x,b.y,40,'orange');}
  if(B.t>.95)next('skid');
 }
 else if(B.mode==='skid'){B.vx*=Math.pow(.02,dt);B.vy*=Math.pow(.02,dt);b.x+=B.vx*dt;b.y+=B.vy*dt;
  b.x=clamp(b.x,L,Rx);b.y=clamp(b.y,Top,Bot);B.spinV=lerp(B.spinV,5,dt*3);if(B.t>.55)next('recover');}
 else if(B.mode==='recover'){B.spinV=lerp(B.spinV,3,dt*2);ease(3.2);
  if(B.t>1.05){B.n++;next(B.n%2?'crouch':'spray');}}
 else if(B.mode==='crouch'){                      // brace, then fling itself at the pilot
  B.spinV=lerp(B.spinV,1,dt*6);const T=targetShip(b.x,b.y);
  B.land={x:clamp(T.x,L,Rx),y:clamp(T.y,Top,Bot),progress:clamp(B.t/.55,0,1)};
  if(B.t>.55-lv*.08){B.from={x:b.x,y:b.y};B.to={x:B.land.x,y:B.land.y};b._s4MiniSafe=true;if(Audio.SFX.whip)Audio.SFX.whip();next('leap');}
 }
 else if(B.mode==='leap'){
  const u=clamp(B.t/(.95-lv*.08),0,1),e=u*u*(3-2*u);B.spinV=11;
  b.x=lerp(B.from.x,B.to.x,e);b.y=lerp(B.from.y,B.to.y,e);B.lift=Math.sin(u*Math.PI)*95;
  B.land={x:B.to.x,y:B.to.y,progress:.5+u*.5};
  if(u>=1){B.lift=0;b._s4MiniSafe=false;B.land=null;
   const n=10+lv*4;for(let i=0;i<n;i++)fb9BodyShot(b,i*TAU/n+B.spin,2.2+lv*.3,i%2===0);
   explode(b.x,b.y,110,'orange');shake=Math.max(shake,10);if(Audio.SFX.expBig)Audio.SFX.expBig();next('slam');}
 }
 else if(B.mode==='slam'){B.spinV=lerp(B.spinV,2,dt*4);if(B.t>.6)next('recover');}
 B.spin=(B.spin+B.spinV*dt)%TAU;core.rot=B.spin;
 b._drawY=b.y-(B.lift||0);
 return true;
}
er26Tick=function(b,dt){if(b&&b._fb9Body&&!b.dead)return fb9BodyTick(b,dt);return FB9_RV.tick.apply(this,arguments);};
shipBossDraw=function(b){
 const B=b&&b._fb9Body;
 if(B&&!b.dead){
  if(B.land&&typeof groundTargetReticleDraw==='function')groundTargetReticleDraw(B.land.x,B.land.y,120,B.land.progress,.9);
  if(B.warn&&typeof combatWarningDraw==='function')combatWarningDraw(b,{x:B.warn.x,y:B.warn.y,ex:B.warn.ex,ey:B.warn.ey,progress:B.warn.progress,width:B.warn.width});
  if(B.lift>1){const c=av3PartPose(b,av3Part(b,'core')),k=1-B.lift/260;ctx.save();ctx.globalAlpha=.32;ctx.fillStyle='#000';
   ctx.beginPath();ctx.ellipse(b.x,b.y+10,c.w*.42*k,c.w*.22*k,0,0,TAU);ctx.fill();ctx.restore();}
 }
 return FB9_RV.draw.apply(this,arguments);
};

/* ---------------------------------------------------------------- Stage 4 barrels
   "On level four the barrels are moving instead of remaining stationary where they're placed."
   Measured (property traps on live s4barrel units): three systems moved a barrel that s4ChaseTick
   meant to keep "fixed to its placement and carried only by the scrolling highway":
     - the generic catch-all exit push in updatePlay (+0.7px/frame once a unit is 9s old),
     - enemyEntrySweep's sideways entry swing (up to 4.5px/frame),
     - terrainScrollPx returning its cached step while the road stood still.
   A barrel is now anchored to the map row and lane it was placed on. Every frame, after enemy
   movement and before separation, it is put back exactly there (y = mapY - levelSrcY()). It still
   blocks other units in separation, but nothing can shove it. */
const FB9_BAR={sep:enemySeparate,mov:sepMovable};
function fb9BarrelAnchor(){
 if(run.stage!==4||typeof levelSrcY!=='function')return;
 const src=levelSrcY();if(!Number.isFinite(src))return;
 for(const e of enemies){
  if(e.dead||e._dyingT!=null||e._s4chase!=='s4barrel')continue;
  if(!e._fb9Anchor){e._fb9Anchor={x:e._lane!=null?e._lane:e.x,mapY:e.y+src};e._esw=null;}
  e.x=e._fb9Anchor.x;e._lane=e._fb9Anchor.x;e.y=e._fb9Anchor.mapY-src;e.vx=0;e.vy=0;
 }
}
enemySeparate=function(){fb9BarrelAnchor();return FB9_BAR.sep.apply(this,arguments);};
sepMovable=function(e){return e&&e._fb9Anchor?false:FB9_BAR.mov.apply(this,arguments);};
// Stage 4 advances its road scroll inside the level draw, so re-seat each barrel on the road
// again just before it is drawn; otherwise it trails the ground by one frame's step.
const FB9_BAR_DRAW=drawEnemy;
drawEnemy=function(e){
 if(e&&e._fb9Anchor&&run.stage===4&&typeof levelSrcY==='function'){const src=levelSrcY();if(Number.isFinite(src))e.y=e._fb9Anchor.mapY-src;}
 return FB9_BAR_DRAW.apply(this,arguments);
};
