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
   October 10 correction: Furious razor missiles are interceptable again. The sonic
   rounds remain weapon-proof; the earlier blanket rule also prevented missile
   acceleration/Retina steering because those share the interception update. */
const FB9_RZB={shot:rzbShot,missile:rzbMissile,intercept:enemyOrdnanceCanIntercept,sprite:rzbSprite,
 muzzle:wm26Draw,draw:razorbackDraw};
function fb9RzbProof(from){for(let i=from;i<eBullets.length;i++){const q=eBullets[i];
 if(q&&q._rzb){const missile=q.kind==='rzbMissile'&&q._rzbFurious;
  q._weaponProof=!missile;q._shootable=!!missile;q.hp=missile?1:undefined;q._fb9RzbProof=!missile;
  q._s3kOriginalProof=!missile;}}}
rzbShot=function(){const n=eBullets.length,r=FB9_RZB.shot.apply(this,arguments);fb9RzbProof(n);return r;};
rzbMissile=function(){const n=eBullets.length,r=FB9_RZB.missile.apply(this,arguments);fb9RzbProof(n);return r;};
enemyOrdnanceCanIntercept=function(q){return q&&(q._fb9RzbProof||q._ovSonicWave)?false:FB9_RZB.intercept.apply(this,arguments);};

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
 if(window.__bofSideHudOwnsLayout&&!debugRecActive())return;
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

/* Stage1 paired entrance: mirrored curves settle into a brief southbound row,
   then peel outward while aiming native machine-gun bursts at the player. */
function fb9SwoopPair(){
 if(run.stage!==1||state!==GS.PLAY)return;
 XART.rdy('air13_s1_s1jetdelta_heading');
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
 if(!S.route){const L=camLeftX(),R=camRightX(),mid=(L+R)/2,gap=Math.max(92,Math.max(e.w,e.h)*.8);
  S.route={start:{x:e.x,y:e.y},row:{x:mid+S.side*gap,y:PLAY.y+150},exit:{x:S.side<0?L-115:R+115,y:PLAY.y+380}};}
 const P=S.route,enter=1.45,row=.48,leave=1.6;
 const curve=(a,b,c,d,u)=>{const v=1-u;return {x:v*v*v*a.x+3*v*v*u*b.x+3*v*u*u*c.x+u*u*u*d.x,y:v*v*v*a.y+3*v*v*u*b.y+3*v*u*u*c.y+u*u*u*d.y,dx:3*v*v*(b.x-a.x)+6*v*u*(c.x-b.x)+3*u*u*(d.x-c.x),dy:3*v*v*(b.y-a.y)+6*v*u*(c.y-b.y)+3*u*u*(d.y-c.y)};};
 let q;
 if(S.t<enter){S.phase='in';q=curve(P.start,{x:P.row.x,y:P.start.y},{x:P.row.x,y:P.row.y-29},P.row,S.t/enter);}
 else if(S.t<enter+row){S.phase='row';q={x:P.row.x,y:P.row.y+(S.t-enter)*60,dx:0,dy:60};}
 else{S.phase='exit';const start={x:P.row.x,y:P.row.y+row*60};q=curve(start,{x:start.x,y:start.y+32},{x:P.exit.x-S.side*90,y:P.exit.y-30},P.exit,clamp((S.t-enter-row)/leave,0,1));}
 const oldX=e.x;e.x=q.x;e.y=q.y;S.head=Math.atan2(q.dy,q.dx);e.vx=(e.x-oldX)/Math.max(dt,.001)/60;e.spin=0;
 S.shotCd-=dt;
 if(S.phase!=='in'&&S.shotCd<=0&&e.x>camLeftX()+12&&e.x<camRightX()-12){
  const n=[Math.cos(S.head),Math.sin(S.head)],p=[-n[1],n[0]],T=targetShip(e.x,e.y);
  for(const side of [-1,1]){const x=e.x+n[0]*24+p[0]*side*9,y=e.y+n[1]*24+p[1]*side*9;eShootT(x,y,Math.atan2(T.y-y,T.x-x),4.4,'s1bullet',{silent:side>0});}
  if(Audio.SFX.enemyMachineGun)Audio.SFX.enemyMachineGun();S.burst=(S.burst+1)%4;S.shotCd=S.burst?.11:.65;
 }
 if(S.t>=enter+row+leave)e.dead=true;
}

function fb9SwoopDraw(e){
 const p=air13Pose('s1jetdelta','heading',e._fb9Swoop.head);
 if(!p)return true; // Never substitute a rotated static hull while the bank loads.
 const span=Math.max(e.w,e.h)*1.10*86/128;
 e._drawW=e._drawH=span;e._air13RenderedKey=p.key;e._air13Frame=p.f;
 air13Blit(p,e.x+10,e.y+18,span,.25,'#000000');
 air13Blit(p,e.x,e.y,span);
 const tint=tintColor(e);if(tint)air13Blit(p,e.x,e.y,span,1,tint);
 return true;
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
