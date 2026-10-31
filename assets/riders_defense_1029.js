'use strict';
/* Rough Riders: physical airspace, directional passes, gold shield counter and intro roller. */
const RR45={base:{tick:rebelSquadTick,act:rg4AttackTick,phase:vs41Phase,draw:rebelSquadDraw,
 intro:h3RebelTick,lines:h3RebelLines,demo:rs1004DemoTick,demoDraw:rs1004DemoDraw,
 helix:ra4Helix,rescue:rg4RescueStart,deploy:rr26Deploy,wall:rr26DrawWall,contact:rr26WallContact,safe:vs41Safe,
 beam:playerBeamRange,load:stageLoadBegin,wingNavigate:s6WingNavigate,wingArsenal:s6WingArsenal,wallRect:rr26WallRect},events:[],separations:0};
const RR45_BANKS={decker_charge:[128,128,8,16],shield_seed:[64,64,8,16],gold_wall:[480,64,8,40],entry_arrows:[40,40,4,4],entry_star:[40,40,1,1]};
for(const k of Object.keys(RR45_BANKS))XART._src['rr45_'+k]='assets/game/levels/stage_06/boss/riders_defense_1029/'+k+'.png';
stageLoadBegin=function(n,keys){return RR45.base.load.call(this,n,n===6?[...(keys||[]),...Object.keys(RR45_BANKS).map(k=>'rr45_'+k)]:keys);};
function rr45Scope(b=boss){return rr33Group(b)&&!b?.dead;}
function rr45Log(event,data={}){RR45.events.push({event,time:rg4State()?.age||boss?._rebels?.rough33?.t||0,...data});if(RR45.events.length>500)RR45.events.shift();}
function rr45Blit(name,f,x,y){const [w,h,cols,n]=RR45_BANKS[name],key='rr45_'+name;if(!XART.rdy(key))return;f=((f|0)%n+n)%n;ctx.drawImage(XART.get(key),f%cols*w,Math.floor(f/cols)*h,w,h,Math.round(x-w/2),Math.round(y-h/2),w,h);}
function rr45Bounds(q){const wh={voss:[42,54],rook:[38,48],nyx:[38,52],kaia:[42,50],jace:[42,55]}[q.key],a=(q.rfHeading??Math.PI/2)-Math.PI/2,k=q._rd21Scale||1,c=Math.abs(Math.cos(a)),s=Math.abs(Math.sin(a));return {w:(wh[0]*c+wh[1]*s)*k,h:(wh[0]*s+wh[1]*c)*k};}
function rr45Move(q,dx,dy){q.x+=dx;q.y+=dy;const A=q.rg4?.act;
 if(A){if(Number.isFinite(A.ox))A.ox+=dx;if(Number.isFinite(A.oy))A.oy+=dy;
  for(const k of ['from','home','perch','back','center','end','next'])if(A[k]){A[k].x+=dx;A[k].y+=dy;}}
 if(q._rk38Stun){q._rk38Stun.x+=dx;q._rk38Stun.y+=dy;}
}
const rr45Pins=rr33Pins;
rr33Pins=function(q){if(!rr45Scope())return rr45Pins.apply(this,arguments);const span=Math.min(190,(viewW()-100)/2),pin=[[0,28],[-.5,-28],[.5,-28],[-1,-84],[1,-84]][q.i];return{x:camLeftX()+viewW()/2+pin[0]*span,y:VH*.41+pin[1]};};
function rr45Separate(b){if(typeof rr65Separate==='function'&&rr45Scope(b))return rr65Separate(b);if(!rr45Scope(b)||rr33Protected(b)&&!['settle','dialogue'].includes(b._rebels.rough33?.phase))return;const ships=b._rebels.ships.filter(q=>rd21Live(q)&&q.y>PLAY.y-130&&q.y<VH+100&&q.x>camLeftX()-150&&q.x<camRightX()+150);
 if(!rr33Protected(b)&&!b._rebels.gang1004?.rd21?.fleet)for(const q of ships)if(!q.rg4?.act){q._rd21Scale=1;q.rfHeading=Math.PI/2;}
 const wall=b._rebels.gang1004?.rr26?.wall,liveWall=wall&&wall.t>=wall.cast+wall.build&&wall.t<wall.dur-wall.fade;
 const bounds=q=>{const p=rr45Bounds(q),air=vs41Safe(q);return{...p,left:camLeftX()+p.w+5,right:camRightX()-p.w-5,top:air?-Infinity:p.h+5,bot:air?Infinity:liveWall&&!(typeof rk50Fixed==='function'&&rk50Fixed(q))?rr26WallRect().y-p.h-4:VH*.59};};
 for(let pass=0;pass<24;pass++){let changed=false;
  for(let i=0;i<ships.length;i++)for(let j=i+1;j<ships.length;j++){
   const a=ships[i],b=ships[j],A=bounds(a),B=bounds(b),dx=b.x-a.x,dy=b.y-a.y,px=A.w+B.w+7-Math.abs(dx),py=A.h+B.h+9-Math.abs(dy);if(px<=.02||py<=.02)continue;
   const fixed=q=>typeof rk50Fixed==='function'&&rk50Fixed(q)?4:vs41Safe(q)?3:q.rg4?.act?2:q._rk38Stun?1:0,fa=fixed(a),fb=fixed(b),wa=fa>fb?0:fa<fb?1:.5,wb=1-wa;
   const horizontal=px<py||liveWall;let ax=0,ay=0,bx=0,by=0;
   if(horizontal){const sign=dx===0?(a.i<b.i?1:-1):Math.sign(dx);ax=-sign*(px+.05)*wa;bx=sign*(px+.05)*wb;
    ax=clamp(a.x+ax,A.left,A.right)-a.x;bx=clamp(b.x+bx,B.left,B.right)-b.x;
    const left=px-Math.abs(ax)-Math.abs(bx);if(left>.02){const sy=dy===0?(a.i<b.i?1:-1):Math.sign(dy);ay=-sy*(py+.05)*wa;by=sy*(py+.05)*wb;}}
   else{const sign=dy===0?(a.i<b.i?1:-1):Math.sign(dy);ay=-sign*(py+.05)*wa;by=sign*(py+.05)*wb;}
   // Offscreen turbo corridors remain independent; the resting squad reserves the space.
   if(!vs41Safe(a))ay=clamp(a.y+ay,A.top,Math.max(A.top,A.bot))-a.y;
   if(!vs41Safe(b))by=clamp(b.y+by,B.top,Math.max(B.top,B.bot))-b.y;
   if(Math.abs(ax)+Math.abs(ay)+Math.abs(bx)+Math.abs(by)>.001){rr45Move(a,ax,ay);rr45Move(b,bx,by);changed=true;RR45.separations++;}
  }if(!changed)break;
 }
 // If an evasive ship reaches an arena edge, reserve the other side of the
 // obstacle instead of repeatedly pressing it against that edge.
 const overlap=(a,b)=>{const A=rr45Bounds(a),B=rr45Bounds(b);return Math.abs(a.x-b.x)<A.w+B.w+6.9&&Math.abs(a.y-b.y)<A.h+B.h+8.9;};
 if(ships.some((a,i)=>ships.slice(i+1).some(b=>overlap(a,b)))){
  const priority=q=>typeof rk50Fixed==='function'&&rk50Fixed(q)?4:vs41Safe(q)?3:q.rg4?.act?2:0;const ordered=ships.slice().sort((a,b)=>priority(b)-priority(a)||a.i-b.i),placed=[];
  for(const q of ordered){const B=bounds(q);if(!placed.some(o=>overlap(q,o))){placed.push(q);continue;}
   const xs=[q.x,B.left,B.right],ys=[q.y,B.top,B.bot];for(const o of placed){const O=rr45Bounds(o);xs.push(o.x-O.w-B.w-7.1,o.x+O.w+B.w+7.1);ys.push(o.y-O.h-B.h-9.1,o.y+O.h+B.h+9.1);}
   let best=null;for(const x of xs)for(const y of ys){if(x<B.left||x>B.right||y<B.top||y>B.bot||!Number.isFinite(x+y))continue;
    if(placed.some(o=>{const O=rr45Bounds(o);return Math.abs(x-o.x)<B.w+O.w+7&&Math.abs(y-o.y)<B.h+O.h+9;}))continue;
    const cost=(x-q.x)**2+(y-q.y)**2;if(!best||cost<best.cost)best={x,y,cost};}
   if(best)rr45Move(q,best.x-q.x,best.y-q.y);else rr45Log('space-unresolved',{pilot:q.key});placed.push(q);
  }
 }
}
// Reserve the destination at the start of a Voss perch, before the approach is visible.
vs41Phase=function(q,A,next){if(!rr45Scope()||q.key!=='voss')return RR45.base.phase.apply(this,arguments);
 if(next==='dash'&&A.phase==='turn-south'&&!A.rr45SideDone){A.rr45SideDone=true;A.rr45Dir=q.x<camLeftX()+viewW()/2?0:2;A.rr45Lane=clamp(A.target.ref.y-100,PLAY.y+125,VH-120);A.rr45Edge=A.rr45Dir===0?camLeftX()-135:camRightX()+135;A.rr45Top=PLAY.y-145;RR45.base.phase.call(this,q,A,'rr45_route');return;}
 if(['north','approach'].includes(next)&&q.y<PLAY.y-50||next==='north'&&q.y>VH+50)q.x=clamp(q.x,camLeftX()+95,camRightX()-95);
 if(['north','approach'].includes(next)||next==='dash'&&['turn-south','rr45_return'].includes(A.phase)){
  A.rr45Next=next;RR45.base.phase.call(this,q,A,'rr45_entry');A.rr45Warm=.8;
  A.rr45Cue={x:q.x,y:next==='north'?VH-26:PLAY.y+28,dir:next==='north'?3:1};
  combatWarningTick(A,'voss-entry-'+next,0,A.rr45Warm);Audio.SFX.retinaLockBeep?.();rr45Log('voss-entry-warning',{next,...A.rr45Cue});return;
 }return RR45.base.phase.apply(this,arguments);
};
rg4AttackTick=function(q,R,G,dt){const A=q.rg4?.act;if(rr45Scope()&&q.key==='voss'&&A?._vs41&&A.phase==='rr45_entry'){
 if(!rd21Live(q)){q.rg4.act=null;return;}A.t+=Math.min(.05,dt);q.x=A.from.x;q.y=A.from.y;
 combatWarningTick(A,'voss-entry-'+A.rr45Next,A.t,A.rr45Warm);if(A.t>=A.rr45Warm){const next=A.rr45Next;delete A.rr45Cue;RR45.base.phase.call(this,q,A,next);}return;}
 if(rr45Scope()&&q.key==='voss'&&A?._vs41&&['rr45_route','rr45_cross','rr45_return'].includes(A.phase)){
  if(!rd21Live(q)){q.rg4.act=null;return;}A.t+=Math.min(.05,dt);const ease=u=>{u=clamp(u,0,1);return u*u*(3-2*u);};q._rd21Scale=1.15;
  if(A.phase==='rr45_route'){
   if(A.t<.6){q.x=lerp(A.from.x,A.rr45Edge,ease(A.t/.6));q.y=A.rr45Top;q.rfHeading=A.rr45Dir===0?Math.PI:0;}
   else{q.x=A.rr45Edge;q.y=lerp(A.rr45Top,A.rr45Lane,ease((A.t-.6)/.6));q.rfHeading=Math.PI/2;}
   if(A.t>=1.2){A.rr45Next='rr45_cross';RR45.base.phase.call(this,q,A,'rr45_entry');A.rr45Warm=.9;A.rr45Cue={x:A.rr45Dir===0?camLeftX()+26:camRightX()-26,y:A.rr45Lane,dir:A.rr45Dir};Audio.SFX.retinaLockBeep?.();rr45Log('voss-side-warning',{dir:A.rr45Dir,y:A.rr45Lane});}
  }else if(A.phase==='rr45_cross'){q.x=lerp(A.from.x,A.rr45Dir===0?camRightX()+135:camLeftX()-135,ease(A.t/1.2));q.y=A.rr45Lane;q.rfHeading=A.rr45Dir===0?0:Math.PI;if(A.t>=1.2){A.cycles++;RR45.base.phase.call(this,q,A,'rr45_return');}}
  else{if(A.t<.6){q.x=A.from.x;q.y=lerp(A.from.y,A.rr45Top,ease(A.t/.6));q.rfHeading=-Math.PI/2;}else{q.x=lerp(A.from.x,clamp(A.home.x,camLeftX()+95,camRightX()-95),ease((A.t-.6)/.6));q.y=A.rr45Top;q.rfHeading=A.rr45Dir===0?Math.PI:0;}if(A.t>=1.2)vs41Phase(q,A,A.cycles>=A.passes?'approach':'dash');}return;
 }
 return RR45.base.act.apply(this,arguments);
};
vs41Safe=function(q){return rr45Scope()&&q?.rg4?.act?._vs41&&['rr45_route','rr45_cross','rr45_return','rr45_entry'].includes(q.rg4.act.phase)||RR45.base.safe.apply(this,arguments);};
function rr45EntryDraw(q){const A=q.rg4?.act;if(!A?._vs41)return;let C=A.rr45Cue;
 if(A.phase==='turbocharge')C={x:q.x,y:clamp(q.y+76,PLAY.y+28,VH-120),dir:1};if(!C)return;
 const x=clamp(C.x,camLeftX()+25,camRightX()-25),y=C.y,dx=[1,0,-1,0][C.dir],dy=[0,1,0,-1][C.dir];
 rr45Blit('entry_star',0,x,y);for(const d of[42,78])rr45Blit('entry_arrows',C.dir,x+dx*d,y+dy*d);
}
// Native Maverick full-ball launch uses11.5 pixels/frame; enemy ordnance uses pixels/second.
ra4Helix=function(q,G,A){const n=G.ord.length,r=RR45.base.helix.apply(this,arguments);if(rr45Scope()&&q.key==='jace')for(const o of G.ord.slice(n))if(o.kind==='helix'){
 o.vx=Math.cos(A.a)*690;o.vy=Math.sin(A.a)*690;o._rr45Speed=690;rr45Log('jace-fast-helix',{speed:690});}return r;};
h3RebelLines=function(R){const rows=RR45.base.lines.apply(this,arguments);if(!rr45Scope())return rows;for(const r of rows)if(r.who==='KAIA'){r.demo='rr45roller';r.text='THIS IS MY PRISM ROLLER. WATCH IT SPIN. TRY NOT TO GET FLATTENED.';}return rows;};
rs1004DemoTick=function(R,I,dt){const r=RR45.base.demo.apply(this,arguments),S=I.showcase,D=S?.current;if(rr45Scope()&&D?.kind==='rr45roller'&&D.q&&!D.released&&I.t>I.rows[I.i].text.length/32+.12){D.released=true;S.fx.push({kind:'rr45roller',x:D.q.x,y:D.q.y+48,vx:D.q.x<camLeftX()+viewW()/2?175:-175,vy:-90,t:0,life:1.5});Audio.SFX.falvaRelease?.();rr45Log('kaia-intro-roller');}return r;};
rs1004DemoDraw=function(R){const r=RR45.base.demoDraw.apply(this,arguments);if(!rr45Scope())return r;const S=R.h3Intro?.showcase,D=S?.current;
 if(D?.kind==='rr45roller'&&D.q&&!D.released)rr35RollerDraw(D.q.x,D.q.y+48,48,D.t,0,.7);
 for(const f of S?.fx||[])if(f.kind==='rr45roller')rr35RollerDraw(f.x,f.y,48,f.t,0,.8);return r;};
rg4RescueStart=function(b,G){if(!rr45Scope(b))return RR45.base.rescue.apply(this,arguments);if(G.rescueDone||b.dead||!s6Wing?.ships.some(q=>q.key==='decker'&&q.hp>0)&&_pilotKey()!=='decker')return false;G.rescueDone=true;G.scene=null;rr26State(G).queue.push(['decker','COVER ME. GOLDEN AEGIS IS CHARGING!']);rr26Deploy(G);return true;};
rr26Deploy=function(G){if(!rr45Scope())return RR45.base.deploy.apply(this,arguments);const S=rr26State(G);if(S.wall)return;
 const caster=s6Wing?.ships.find(q=>q.key==='decker'&&q.hp>0)||(_pilotKey()==='decker'?player:null);if(!caster){G.rescueDone=false;return;}
 S.wall={_rr45:true,t:0,cast:2.35,build:.67,hold:10,fade:.5,dur:13.52,hits:0,caster,origin:{x:caster.x,y:caster.y-24},pulse:0};
 S.queue.push(['decker','GOLDEN AEGIS! LET THEIR OWN WEAPONS DO THE WORK.']);Audio.SFX.bossWeaponCharge?.();rr45Log('gold-shield-charge');
};
rr26WallRect=function(){const r=RR45.base.wallRect.apply(this,arguments);if(rg4State()?.rr26?.wall?._rr45)return{...r,y:VH*.62-r.h/2};return r;};
rr26DrawWall=function(W){if(!W._rr45)return RR45.base.wall.apply(this,arguments);const r=rr26WallRect(),q=W.caster;if(W.t<1.6){if(q&&!q.dead)rr45Blit('decker_charge',Math.floor(W.t*24),q.x,q.y);return;}
 if(W.t<W.cast){const u=clamp((W.t-1.6)/(W.cast-1.6),0,1),v=u*u*(3-2*u),p=q&&!q.dead?{x:q.x,y:q.y-30}:W.origin;
  rr45Blit('shield_seed',Math.floor(W.t*24),lerp(p.x,r.x+r.w/2,v),lerp(p.y,r.y+r.h/2,v));return;}
 let f=W.t<W.cast+W.build?Math.min(15,Math.floor((W.t-W.cast)/W.build*16)):W.t>W.dur-W.fade?32+Math.min(7,Math.floor((W.t-(W.dur-W.fade))/W.fade*8)):16+Math.floor(W.t*24)%16;
 rr45Blit('gold_wall',f,r.x+r.w/2,r.y+r.h/2);
};
s6WingNavigate=function(q,W,dt){const wall=rg4State()?.rr26?.wall;if(rr45Scope()&&wall?._rr45&&wall.caster===q&&wall.t<wall.cast){q.x=wall.origin.x;q.y=wall.origin.y+24;q.vx=q.vy=0;q.dodgeT=0;return;}return RR45.base.wingNavigate.apply(this,arguments);};
s6WingArsenal=function(q){const wall=rg4State()?.rr26?.wall;if(rr45Scope()&&wall?._rr45&&wall.caster===q&&wall.t<wall.cast)return;return RR45.base.wingArsenal.apply(this,arguments);};
// Native contact owns enemy reflection and damage. Friendly rounds pass the new wall.
rr26WallContact=function(G,dt){if(!G.rr26?.wall?._rr45)return RR45.base.contact.apply(this,arguments);const old=pBullets;pBullets=[];try{return RR45.base.contact.apply(this,arguments);}finally{pBullets=old;}};
playerBeamRange=function(p){if(rg4State()?.rr26?.wall?._rr45)return rr26BeamBase.apply(this,arguments);return RR45.base.beam.apply(this,arguments);};
const rr45Reflect=rr26Reflect;
rr26Reflect=function(G,o){const first=G.rr26?.wall?._rr45&&G.rr26.wall.hits===0,r=rr45Reflect.apply(this,arguments);if(first){const S=rr26State(G);S.queue=S.queue.filter(row=>!['OUR SHOTS ARE COMING BACK! BREAK FORMATION!','HA! YOU BUILT THAT AND NEVER TOLD US?','I WAS SAVING IT FOR A GOOD FIRST IMPRESSION.','NICK OF TIME, DECKER. NICK OF TIME!'].includes(row[1]));S.queue.push(['voss','YOU THINK YOU CAN TURN OUR FIRE AGAINST US?!'],['rook','DECKER! I AM GOING TO TEAR THAT SHIELD APART!'],['decker','BE MY GUEST. EVERY SHOT COMES WITH A RETURN ADDRESS.']);rr45Log('riders-angry-reflection');}return r;};
h3RebelTick=function(b,dt){const r=RR45.base.intro.apply(this,arguments);if(rr45Scope(b))rr45Separate(b);return r;};
rebelSquadTick=function(b,dt){const r=RR45.base.tick.apply(this,arguments);if(rr45Scope(b)&&b._rebels.frIntro?.done)rr45Separate(b);return r;};
rebelSquadDraw=function(b){const r=RR45.base.draw.apply(this,arguments);if(rr45Scope(b))for(const q of b._rebels.ships)if(q.key==='voss'&&!q.dead)rr45EntryDraw(q);return r;};
globalThis.BOF_RIDERS_DEFENSE_1029=RR45;

