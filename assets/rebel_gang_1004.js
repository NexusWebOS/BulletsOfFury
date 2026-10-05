'use strict';
/* Five pilots, five weapons. October 4: whole rebel hulls, live radio scenes,
   destructible support, and Decker's experimental squad cloak. */
const RG4_ROLES={voss:'fusion',nyx:'ghost',rook:'heavy',kaia:'roller',jace:'stealth'};
const RG4_NAMES={fusion:'FUSION CANNON',ghost:'GHOSTKNIFE',heavy:'HEAVY MACHINE GUN',roller:'PRISM ROLLER',stealth:'CLOAK STRIKE',missiles:'MISSILE RACK'};
const RG4_COLORS={voss:'#ff48bd',nyx:'#55ffff',rook:'#ffbd50',kaia:'#c080ff',jace:'#b4ff54'};
const RG4_BASE={tick:rebelSquadTick,damage:rebelSquadDamage,ship:fr27RebelDrawShip,draw:rebelSquadDraw,
 update:updatePlay,world:drawWorld,locked:h3Locked,hold:Input.hold,wingTick:s6WingTick,wingDraw:s6WingDraw,
 playerDraw:drawPlayer,playerHit:playerHit,targets:retinaBossTargets,projectile:drawCombatFinalProjectile,begin:beginStage,pods:chaingunMountsVisible};
const RG4={draws:{},events:[],sheet:'rg4_decker_effects'};
XART._src[RG4.sheet]='assets/game/rebel_gang_1004/decker_effects.png';
function rg4State(){return state===GS.PLAY&&bossActive&&boss&&!boss.dead?boss._rebels?.gang1004:null;}
function rg4Scene(){return rg4State()?.scene||null;}
function rg4Log(G,event,data={}){const e={event,t:G.age,...data};G.events.push(e);if(G.events.length>160)G.events.shift();RG4.events.push(e);if(RG4.events.length>240)RG4.events.shift();}
function rg4Warm(){XART.rdy(RG4.sheet);av3Warm();s81003WarningWarm();for(const c of ['green','yellow','red'])XART.rdy('bmfx_alert_'+c+'_impact_imminent');for(let f=0;f<8;f++){XART.rdy('florb_'+f);if(f<4){XART.rdy('nfrb_'+f);XART.rdy(CHAINGUN_POD_KEY+f);XART.rdy('retA_'+f);XART.rdy('retB_'+f);}}}
function rg4Init(b){const R=b._rebels;if(R.gang1004)return R.gang1004;if(!R.rf)rf28Init(b,R);
 const G=R.gang1004={age:0,gang:false,scene:null,rescueDone:false,rescueAt:Infinity,ord:[],beams:[],fx:[],events:[],releaseAt:1.2,shield:0,orbSpawned:false};
 for(const q of R.ships){q.rg4={role:RG4_ROLES[q.key],cd:1.4+q.i*1.7,act:null,n:0,turbo:false};q.rfSig=null;q.rfHeading=null;q.frCast=null;j3RebelHull(q);}
 R.rf.form=null;R.rf.formNext=Infinity;rg4Warm();return G;
}
function rg4Cell(row,f,x,y,w,h=w,alpha=1,color){if(!XART.rdy(RG4.sheet))return false;const im=color?xartPalette(RG4.sheet,color):XART.get(RG4.sheet);if(!im)return false;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=clamp(alpha,0,1);ctx.drawImage(im,clamp(f|0,0,5)*256,row*256,256,256,x-w/2,y-h/2,w,h);ctx.restore();RG4.draws['row'+row]=(RG4.draws['row'+row]||0)+1;return true;
}
function rg4FX(G,row,x,y,size,life=.9){G.fx.push({row,x,y,size,life,t:0});}
function rg4Clear(G){G.ord.length=0;G.beams.length=0;S81003.beams.length=0;tb28Reset();h3ClearCombat();const R=boss?._rebels;if(R?.rf){R.rf.callouts=[];R.rf.comm=null;R.rf.banner=null;}for(const q of R?.ships||[]){q.rfSig=q.frCast=null;if(q.rg4)q.rg4.act=null;}}
function rg4GangStart(b,G){if(G.gang||b._rebels.frStageX||b._rebels.ships.length!==5)return false;
 G.gang=true;G.scene={kind:'gang',age:0,shown:0};G.rescueAt=Infinity;rg4Clear(G);b._noHit=true;
 for(const q of b._rebels.ships){q.frCloak=0;q.evadeT=0;q.rg4.turbo=['rook','jace'].includes(q.key);}
 av3Sound('laser_charge',.9);Audio.SFX.bossPhase?.();rg4Log(G,'gangStart',{wounded:b._rebels.ships.filter(q=>q.hp<=q.max*.5).length});return true;
}
function rg4Threshold(b,G){if(!G.gang&&b._rebels.ships.filter(q=>q.hp<=q.max*.5).length>=3)return rg4GangStart(b,G);return false;}
function rg4Aim(q){return Math.atan2(player.y-(q.y+30),player.x-q.x);}
function rg4Attack(q,R,G,forced){const A=q.rg4;A.n++;const kind=forced||(G.gang&&q.key==='voss'&&A.n%2===0?'missiles':A.role);
 const warm=({fusion:2.1,roller:1.55,heavy:1.0,ghost:2.0,stealth:1.7,missiles:1.2})[kind]*(diffKey==='easy'?1.2:1);
 A.act={kind,t:0,warm,phase:'charge',a:rg4Aim(q),shot:0,cd:0,x:q.x,y:q.y};q.evadeT=0;q.frSomersault=false;
 G.releaseAt=G.age+(diffKey==='furious'||diffKey==='insanity'?1.15:1.85);combatWarningTick(q,'rg4-'+A.n,0,warm);av3Sound('laser_charge',.7,.35);
 if(kind==='ghost'||kind==='stealth'){q.frCloak=warm+.1;av3Sound('teleport_out',.6);rg4FX(G,2,q.x,q.y,94,.65);}
 rf28Callout(R,RG4_NAMES[kind],q.x,q.y+62,RG4_COLORS[q.key],1.5,8);rg4Log(G,'specialStart',{pilot:q.key,kind});
}
function rg4Round(q,a,speed=4.1,kind='s6tracer',extra={}){const z=eShootT(q.x,q.y+32,a,speed,kind,{w:7,h:22,silent:true});Object.assign(z,{_noArsenal:true,_rg4:true},extra);return z;}
function rg4Missiles(q,G,A){for(const side of [-1,1]){const a=A.a+side*.16;eBullets.push({x:q.x+side*26,y:q.y+30,vx:Math.cos(a)*2.4,vy:Math.sin(a)*2.4,ang:a,spd:2.4,_accel:.025,_maxspd:4.2,w:12,h:22,kind:'emissile',hp:1,_shootable:true,homing:false,t:0,_rg4:true,_boss:true,_noArsenal:true});}
 Audio.SFX.missile?.();rg4Log(G,'missiles',{pilot:q.key,count:2});}
function rg4Roller(q,G,A){const v=diffKey==='easy'?145:185;G.ord.push({kind:'roller',owner:q,x:q.x,y:q.y+43,vx:Math.cos(A.a)*v,vy:Math.sin(A.a)*v,r:23,hp:10,max:10,t:0,life:5.6,bounces:0,split:false,flash:0});Audio.SFX.falvaRelease?.();av3Sound('alien_orb',.9);rg4Log(G,'rollerRelease',{pilot:q.key});}
function rg4AttackTick(q,R,G,dt){const M=q.rg4,A=M.act;if(!A)return;A.t+=dt;
 if(A.phase==='charge'){
  if(A.t<A.warm*.55)A.a=rg4Aim(q);combatWarningTick(q,'rg4-'+M.n,Math.min(A.t,A.warm-.001),A.warm);
  if(A.kind==='ghost'||A.kind==='stealth')q.frCloak=A.t<A.warm-.75?.2:0;
  if(A.t<A.warm)return;A.phase='fire';A.t=0;q.frCloak=0;rg4Log(G,'specialRelease',{pilot:q.key,kind:A.kind});
  if(A.kind==='fusion'){G.beams.push({owner:q,a:A.a,t:0,dur:.95,width:30});av3Sound('fusion_cannon',1);}
  if(A.kind==='roller')rg4Roller(q,G,A);
  if(A.kind==='missiles')rg4Missiles(q,G,A);
  if(A.kind==='ghost'||A.kind==='stealth'){rg4FX(G,2,q.x,q.y,90,.6);av3Sound('teleport_in',.6);}
 }
 if(A.kind==='heavy'&&A.phase==='fire'){
  A.cd-=dt;if(A.cd<=0&&A.shot<(G.gang?14:10)){A.cd=G.gang?.115:.15;const side=A.shot++%2?1:-1;
   const p={x:q.x+side*23,y:q.y+18};rg4Round(p,A.a+Math.sin(A.shot*.5)*.095,4.5,'s6tracer',{_cal50:true});q._rg4Muzzle=.1;Audio.SFX.enemyMachineGunHeavy?.();}
 }
 if((A.kind==='ghost'||A.kind==='stealth')&&A.phase==='fire'){
  if(A.t>.07+A.shot*.26&&A.shot<(G.gang?4:3)){A.shot++;const drift=(A.shot-2)*.075;for(const off of (A.kind==='ghost'?[-.21,0,.21]:[-.13,.13]))rg4Round(q,A.a+off+drift,G.gang?5.0:4.0);Audio.SFX.enemyShoot?.();}
  if(A.kind==='stealth')q.x=clamp(q.x+Math.sin(A.a)*dt*(G.gang?245:150)*(q.i%2?1:-1),camLeftX()+56,camRightX()-56);
 }
 const end=A.kind==='heavy'?(G.gang?1.85:1.65):A.kind==='fusion'?1.35:1.1;
 if(A.phase==='fire'&&A.t>=end){M.act=null;M.cd=({fusion:6.2,heavy:5.2,roller:6.5,ghost:4.8,stealth:4.5,missiles:4.5})[A.kind]*(diffKey==='easy'?1.3:G.gang?.85:1);}
}
function rg4Orb(G,R){if(G.orbSpawned)return;const q=R.ships.find(q=>q.key==='kaia'&&!q.dead)||R.ships.find(q=>!q.dead);if(!q)return;
 G.orbSpawned=true;const hp=diffKey==='furious'?18:12;G.ord.push({kind:'helper',owner:q,x:q.x+60,y:q.y,r:15,hp,max:hp,t:0,cd:1.4,flash:0});rg4FX(G,0,q.x,q.y,120);av3Sound('teleport_in',.8);rg4Log(G,'helperSpawn',{pilot:q.key});
}
function rg4OrdnanceHit(G,o,dmg){if(o.dead||!(dmg>0)||G.scene)return false;o.hp=Math.max(0,o.hp-dmg);o.flash=.15;av3Sound('impact_energy',.65,.1);
 if(o.hp<=0){o.dead=true;rg4FX(G,2,o.x,o.y,o.r*4,.6);Audio.SFX.expSmall?.();rg4Log(G,'ordnanceDestroyed',{kind:o.kind});}return true;}
function rg4OrdnanceTick(b,G,dt){
 for(const o of G.ord){if(o.dead)continue;o.t+=dt;o.flash=Math.max(0,o.flash-dt);if(o.owner.dead){o.dead=true;continue;}
  if(o.kind==='helper'){const a=G.age/.44;o.x=o.owner.x+Math.cos(a)*57;o.y=o.owner.y+Math.sin(a)*43;o.cd-=dt;
   if(o.cd<=0){o.cd=diffKey==='easy'?2.4:1.8;const a=rg4Aim(o);for(const off of [-.10,.10]){const z=eShootT(o.x,o.y,a+off,3.3,'s6orb',{w:7,h:22,silent:true});z._rg4Helper=true;z._noArsenal=true;}av3Sound('laser_release',.6,.3);rg4Log(G,'helperFire');}
  }else{o.x+=o.vx*dt;o.y+=o.vy*dt;if((o.x<camLeftX()+o.r&&o.vx<0)||(o.x>camRightX()-o.r&&o.vx>0)){o.vx=-o.vx;o.bounces++;rg4FX(G,0,o.x,o.y,70,.35);}
   if(!o.split&&o.r>20&&o.t>.95){o.split=true;const a=Math.atan2(o.vy,o.vx);for(const off of [-.6,.6])G.ord.push({kind:'roller',owner:o.owner,x:o.x,y:o.y,vx:Math.cos(a+off)*155,vy:Math.sin(a+off)*155,r:11,hp:3,max:3,t:0,life:2.8,bounces:0,split:true,flash:0});rg4Log(G,'rollerSplit');}
   if(o.t>o.life||o.y>VH+60||o.y<PLAY.y-85)o.dead=true;
  }
  if(o.dead)continue;
  for(const p of pBullets){if(p.dead)continue;const beam=p.kind==='beam'?playerBeamRange(p):null;
   const hit=beam?o.y+o.r>=beam.top&&o.y-o.r<=beam.bot&&Math.abs(o.x-beam.x)<o.r+beam.half:Math.abs(p.x-o.x)<o.r+(p.w||4)/2&&Math.abs(p.y-o.y)<o.r+(p.h||8)/2;
   if(!hit)continue;if(beam){if(G.age<(o.nextBeam||0))continue;o.nextBeam=G.age+.12;}
   rg4OrdnanceHit(G,o,p.dmg||2);if(!beam&&!p.pierce)p.dead=true;if(o.dead)break;
  }
  if(!o.dead)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(o.x-player.x,o.y-player.y)<o.r+5)playerHit('rebel '+o.kind);});
 }
 G.ord=G.ord.filter(o=>!o.dead);
 for(const B of G.beams){B.t+=dt;if(B.owner.dead){B.t=B.dur;continue;}const L={x:B.owner.x,y:B.owner.y+33,ex:B.owner.x+Math.cos(B.a)*VH*1.4,ey:B.owner.y+33+Math.sin(B.a)*VH*1.4};
  for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&s81003Distance(player.x,player.y,L)<B.width*.5+4)playerHit('rebel fusion');});}
 G.beams=G.beams.filter(B=>B.t<B.dur&&!B.owner.dead);
}
function gp4Allies(){const seats=[];for(const seat of seatList())withSeat(seat,()=>{if(!seats.includes(_pilotKey()))seats.push(_pilotKey());});
 return [...seats,...['decker','cole','axel','falva','yuri','lizzie','maverick','freezer','juggernaut'].filter(k=>!seats.includes(k))].slice(0,5);}
function rg4Formation(G){const members=[];for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out)members.push({key:_pilotKey(),ref:player,seat});});
 for(const key of gp4Allies()){if(members.some(q=>q.key===key))continue;const q=s6Wing?.ships.find(q=>q.key===key&&q.phase!=='leave'&&q.hp>0);members.push({key,ref:q||{x:camLeftX()+viewW()/2,y:VH+70+members.length*20},borrowed:!q});XART.rdy('ship_'+key);}
 members.sort((a,b)=>(a.key==='decker'?-1:b.key==='decker'?1:a.seat?-1:b.seat?1:0));
 const pins=[[0,0],[-.5,1],[.5,1],[-1,2],[1,2]],span=Math.min(82,(viewW()-110)/3),top=PLAY.y+PLAY.h*.34;
 members.forEach((m,i)=>{m.pin={x:camLeftX()+viewW()/2+pins[i][0]*span,y:top+pins[i][1]*38};m.start={x:m.ref.x,y:m.ref.y};});G.members=members;
}
function rg4RescueStart(b,G){if(G.rescueDone||G.scene||b.dead)return false;G.rescueDone=true;G.savedHelper=G.ord.find(o=>o.kind==='helper'&&!o.dead);rg4Clear(G);rg4Formation(G);
 const female=b._rebels.ships.find(q=>q.key==='kaia'&&!q.dead)||b._rebels.ships.find(q=>q.key==='nyx'&&!q.dead);
 // A destroyed pilot can still use the squadron's radio from her escape pod.
 const scanner=female?.key||'kaia';G.scanner=scanner;G.scene={kind:'rescue',age:0,i:0,t:0,shown:0,cam:camX,castAt:null,scanAt:null,revealAt:null,
  lines:[
   {who:'decker',text:'I SWORE I WOULD NEVER USE THIS EXPERIMENTAL TECH ON THE TEAM. BUT I AM NOT LOSING YOU. EVERYONE, FORM ON ME!',event:'formation'},
   {who:'decker',text:'BOWLING FORMATION. HOLD STEADY... SHIELD WAVE, ENGAGE!',event:'cast'},
   {who:'voss',text:'THEY VANISHED! WHERE DID THE ENTIRE SQUADRON GO?',event:'cloak'},
   {who:'rook',text:'NOTHING ON MY SIGHTS. DID WE JUST LOSE FIVE SHIPS?'},
   {who:scanner,text:'LEAVE IT TO THE LADIES TO FIGURE THINGS OUT, YOU SILLY BOYS.',event:'scan'},
   {who:scanner,text:"WHY IS IT THAT GEEKS NEVER CAN DO THINGS RIGHT?",event:'reveal'},
   {who:'cole',text:'DECKER, I THINK YOU MAY HAVE MET YOUR MATCH.'},
   {who:'decker',text:"LOVE ISN'T ALWAYS AT FIRST SIGHT, ESPECIALLY WHEN THEY ARE ACTIVELY TRYING TO KILL ME!"}
  ]};b._noHit=true;G.cloak=0;rg4Log(G,'rescueStart',{scanner});return true;
}
function rg4SceneEvent(b,G,C,line){const event=line.event;if(!event)return;rg4Log(G,event);
 if(event==='cast'){C.castAt=C.age;av3Sound('gravity_pulse',.9);Audio.SFX.shieldUp?.();}
 if(event==='cloak'){G.cloak=1;G.shield=1;av3Sound('teleport_out',.85);}
 if(event==='scan'){C.scanAt=C.age;av3Sound('target_acquire',.85);}
 if(event==='reveal'){C.revealAt=C.age;av3Sound('teleport_in',1);Audio.SFX.shieldBreak?.();}
}
function rg4SceneTick(b,G,dt){const C=G.scene;if(!C)return;C.age+=dt;const R=b._rebels;b._noHit=true;
 for(const q of R.ships){q.t+=dt;q.flash=Math.max(0,q.flash-dt);q.evadeT=0;q.frCloak=0;q.rg4.act=null;if(!q.dead){const x=camLeftX()+viewW()/2+(q.i-2)*Math.min(82,(viewW()-110)/4),y=PLAY.y+63+(q.i%2)*36;q.x+=(x-q.x)*Math.min(1,dt*2);q.y+=(y+Math.sin(G.age+q.i)*5-q.y)*Math.min(1,dt*2);}}
 if(C.kind==='gang'){
  C.shown=Math.min(19,Math.floor(C.age*24));if(C.age<3.1)return;
  G.scene=null;b._noHit=false;G.releaseAt=G.age+.8;G.rescueAt=G.age+12;for(const q of R.ships)q.rg4.cd=1+q.i*.6;rg4Orb(G,R);rg4Log(G,'gangArmed');return;
 }
 const u=clamp(C.age/3.2,0,1),ease=u*u*(3-2*u);
 for(const m of G.members){m.ref.x=lerp(m.start.x,m.pin.x,ease)+Math.sin(G.age*.9)*6;m.ref.y=lerp(m.start.y,m.pin.y,ease)+Math.sin(G.age*1.3+m.pin.y)*2;m.ref.vx=0;m.ref.vy=-100;}
 if(C.castAt!=null&&C.age-C.castAt>1.0){G.shield=1;G.cloak=Math.max(G.cloak||0,clamp((C.age-C.castAt-1)/1.3,0,1));}
 if(C.revealAt!=null){G.cloak=1-clamp((C.age-C.revealAt)/1.35,0,1);}
 const line=C.lines[C.i];if(!line){G.scene=null;G.cloak=0;G.shield=5;b._noHit=false;G.releaseAt=G.age+1.8;for(const q of R.ships)q.rg4.cd=1.8+q.i*.5;
  // Borrowed pilots peel away after the scene. Existing allies resume their AI.
  G.depart=G.members.filter(m=>m.borrowed).map(m=>({key:m.key,x:m.ref.x,y:m.ref.y,t:0}));G.members=null;if(G.savedHelper&&!G.savedHelper.dead&&!G.savedHelper.owner.dead){G.savedHelper.cd=2;G.ord.push(G.savedHelper);}G.savedHelper=null;H3.release=true;Input.clearTaps?.();rg4Log(G,'rescueComplete');return;}
 if(C.t===0)rg4SceneEvent(b,G,C,line);C.t+=dt;const shown=Math.min(line.text.length,Math.floor(C.t*32));dialogueLetterTicks?.(line.text,C.shown,shown);C.shown=shown;
 if(C.scanAt!=null&&C.revealAt==null){const n=Math.min(3,Math.floor((C.age-C.scanAt)/1.2));if(n!==(C.scanBeat??-1)){C.scanBeat=n;Audio.SFX.retinaLockBeep?.();}}
 if(C.t>=Math.max(line.event==='scan'?5.5:0,line.text.length/32+2.5)){C.i++;C.t=0;C.shown=0;}
}
rebelSquadTick=function(b,dt){const R=b._rebels;if(!R.frIntro?.done)return RG4_BASE.tick.apply(this,arguments);const G=rg4Init(b);dt=Math.min(.05,Math.max(0,dt));G.age+=dt;b.t+=dt;R.t+=dt;b.flash=Math.max(0,b.flash-dt);h3RebelMusic();
 if(b.dead){G.scene=null;G.beams=[];G.ord=[];b.dying+=dt;return;}
 for(const f of G.fx)f.t+=dt;G.fx=G.fx.filter(f=>f.t<f.life);G.shield=Math.max(0,G.shield-dt);
 if(G.depart){for(const m of G.depart){m.t+=dt;m.y-=(160+m.t*110)*dt;m.x+=(m.x<camLeftX()+viewW()/2?-25:25)*dt;}G.depart=G.depart.filter(m=>m.y>-80);}
 if(!G.scene)rg4Threshold(b,G);if(!G.scene&&G.gang&&!G.rescueDone&&(G.age>=G.rescueAt||b.hp<b.maxhp*.17))rg4RescueStart(b,G);
 if(G.scene){rg4SceneTick(b,G,dt);return;}
 for(const q of R.ships){j3RebelHull(q);if(q.dead){if(!q.rg4.deathSeen){q.rg4.deathSeen=true;rf28Fallen(b,R,q);}continue;}
  const A=q.rg4;q.t+=dt;q.flash=Math.max(0,q.flash-dt);q.stun=Math.max(0,q.stun-dt);q.warp=0;q.mode='fight';q._rg4Muzzle=Math.max(0,(q._rg4Muzzle||0)-dt);
  A.cd-=dt;q.evadeT=Math.max(0,(q.evadeT||0)-dt);q.evadeCd=Math.max(0,(q.evadeCd||0)-dt);
  const slot=R.frStageX?0:(q.i-2),cx=camLeftX()+viewW()/2,span=Math.min(82,(viewW()-112)/4),speed=A.turbo?2.0:1.0;
  const tx=clamp(cx+slot*span+Math.sin(G.age*(.8*speed)+q.i)*20,camLeftX()+54,camRightX()-54),ty=PLAY.y+83+(q.i%2)*46+Math.sin(G.age*1.4*speed+q.i)*14;
  if(!A.act||A.act.kind==='ghost'||A.act.kind==='stealth'){
   const threat=pBullets.find(p=>!p.dead&&p.y>q.y&&p.y<q.y+150&&Math.abs(p.x-q.x)<25);
   if(threat&&q.evadeCd<=0){q.evadeCd=2.5;q.evadeT=.38;q.evadeX=clamp(q.x+(q.x<threat.x?-1:1)*62,camLeftX()+54,camRightX()-54);q.frSomersault=false;}
   q.x+=clamp((q.evadeT?q.evadeX:tx)-q.x,-dt*145*speed,dt*145*speed);q.y+=clamp(ty-q.y,-dt*95*speed,dt*95*speed);
  }
  q.frCloak=G.gang&&q.key==='nyx'&&!A.act?.phase?.includes('fire')?.2:Math.max(0,(q.frCloak||0)-dt);
  if(A.act)rg4AttackTick(q,R,G,dt);
 }
 // Stagger two pilots on Furious. Fusion and rollers never overlap each other.
 const active=R.ships.filter(q=>!q.dead&&q.rg4.act),limit=diffKey==='furious'||diffKey==='insanity'?2:1;
 if(G.age>=G.releaseAt&&active.length<limit){
  const alive=R.ships.filter(q=>!q.dead&&!q.rg4.act&&q.stun<=0&&q.rg4.cd<=0&&!(['fusion','roller'].includes(q.rg4.role)&&active.some(a=>['fusion','roller'].includes(a.rg4.act.kind)))).sort((a,c)=>a.rg4.cd-c.rg4.cd);if(alive.length)rg4Attack(alive[0],R,G);
 }
 rg4OrdnanceTick(b,G,dt);for(const c of R.rf.callouts)c.t+=dt;R.rf.callouts=R.rf.callouts.filter(c=>c.t<c.dur);if(R.rf.comm){R.rf.comm.t+=dt;if(R.rf.comm.t>=R.rf.comm.dur)R.rf.comm=null;}if(R.rf.banner){R.rf.banner.t+=dt;if(R.rf.banner.t>=R.rf.banner.dur)R.rf.banner=null;}
};
rebelSquadDamage=function(b,dmg){const G=b._rebels?.gang1004;if(G?.scene)return;const r=RG4_BASE.damage.apply(this,arguments);if(G&&!b.dead)rg4Threshold(b,G);return r;};
retinaBossTargets=function(b){let targets=RG4_BASE.targets.apply(this,arguments);const G=b?._rebels?.gang1004;if(!G)return targets;if(G.scene)return[];
 targets=targets.filter(t=>!b._rebels.ships.some(q=>q.frCloak>0&&t._retinaId===q.key+'-hull'));
 for(const [i,o] of G.ord.entries())if(!o.dead){o.id??='rg4-'+G.age+'-'+i;targets.push(retinaDynamicPiece(b,o.id,'support',()=>({x:o.x,y:o.y,hp:o.hp,dead:o.dead}),d=>rg4OrdnanceHit(G,o,d),o.r*2,o.r*2));}return targets;
};
drawCombatFinalProjectile=function(p){if(p._rg4Helper){av3Bolt(p,'ice');return true;}return RG4_BASE.projectile.apply(this,arguments);};
function rg4Warning(q,A){if(A.phase!=='charge')return;const p=clamp(A.t/A.warm,0,1),x=q.x,y=q.y+32;
 if(!['ghost','stealth'].includes(A.kind)||A.t>=A.warm-.75)combatWarningDraw(q,{x,y,ex:x+Math.cos(A.a)*VH*1.3,ey:y+Math.sin(A.a)*VH*1.3,width:A.kind==='fusion'?32:A.kind==='roller'?52:24,progress:p,fieldOnly:true});
 const key='bmfx_alert_'+l23FovPhase(p)+'_impact_imminent';if(XART.rdy(key)){const im=XART.get(key),s=32;ctx.save();ctx.globalAlpha=p<.33?.65:(Math.floor(A.t*10)%2?1:.55);ctx.drawImage(im,q.x-s/2,q.y+28-s/2,s,s);ctx.restore();RG4.draws.asterisk=(RG4.draws.asterisk||0)+1;}
}
fr27RebelDrawShip=function(q){const G=rg4State(),A=q.rg4?.act;RG4_BASE.ship.apply(this,arguments);if(!G||q.dead)return;
 const gangCharge=G.scene?.kind==='gang',fusion=A?.kind==='fusion'&&A.phase==='charge';
 if(gangCharge||fusion){const key='rr_ship_'+REBEL_SHIPS[q.i],im=xartPalette(key,fusion?'#ff48bd':RG4_COLORS[q.key]),w=SHIP_DRAW_H*1.5;
  if(im){const h=w*im.height/im.width;ctx.save();ctx.globalAlpha=.55+.18*Math.sin(G.age*9);ctx.drawImage(im,q.x-w/2,q.y-h/2,w,h);ctx.restore();}
  rg4Cell(3,Math.floor(G.age*14)%6,q.x,q.y,115,135,.7,fusion?'#ff48bd':RG4_COLORS[q.key]);}
 if(q.key==='rook'){
  const f=Math.floor(G.age*(A?.phase==='fire'?20:3))%4,key=CHAINGUN_POD_KEY+f;if(XART.rdy(key)){const im=XART.get(key),h=38,w=h*im.width/im.height;ctx.save();ctx.globalAlpha=q.frCloak>0?.3:1;
   for(const side of [-1,1]){const x=q.x+side*23,y=q.y+13;ctx.drawImage(im,x-w/2,y-h*.12,w,h);if(q._rg4Muzzle>0)wm26Draw(ctx,'chaingun',x,y+31,Math.PI/2,1-q._rg4Muzzle/.1,26);}ctx.restore();RG4.draws.heavy=(RG4.draws.heavy||0)+1;}}
 if(A)rg4Warning(q,A);
};
function rg4Beam(B){const im=xartPalette('av3_laser_beams','#ff48bd');if(!im)return;const f=Math.floor(B.t*18)%3,r=AV3_ART.beams[3][f],w=B.width*1.35,step=w*r[2]/r[3],length=VH*1.4;
 ctx.save();ctx.translate(B.owner.x,B.owner.y+33);ctx.rotate(B.a);ctx.imageSmoothingEnabled=false;ctx.globalAlpha=Math.min(1,(B.dur-B.t)/.13);ctx.beginPath();ctx.rect(0,-w/2,length,w);ctx.clip();for(let y=0;y<length;y+=step)ctx.drawImage(im,...r,y,-w/2,step+.5,w);ctx.restore();av3Muzzle(ctx,B.owner.x,B.owner.y+33,65,3,B.t);RG4.draws.fusion=(RG4.draws.fusion||0)+1;
}
function rg4HealthBars(b){
 for(const q of b._rebels.ships){if(q.dead||q.hp<=0||q.frCloak>0)continue;
  const w=66,x=q.x,y=q.y-58;
  ctx.save();ctx.fillStyle='#04080f';ctx.fillRect(x-w/2-2,y-2,w+4,9);ctx.fillStyle='#3a4655';ctx.fillRect(x-w/2,y,w,5);ctx.fillStyle=REBEL_TINT[q.i];ctx.fillRect(x-w/2,y,w*clamp(q.hp/q.max,0,1),5);ctx.restore();campText(q.key.toUpperCase(),x,y-7,7,'#e6efff');
 }
}
function rg4OrdnanceDraw(o,G){const f=Math.floor(G.age*16)%(o.kind==='helper'?8:4),im=o.kind==='helper'?axelSwap('florb_'+f):(XART.rdy('nfrb_'+f)?XART.get('nfrb_'+f):null);if(!im)return;
 ctx.save();ctx.translate(o.x,o.y);ctx.rotate(G.age*(o.kind==='helper'?3:5));const d=o.r*2.35;ctx.drawImage(im,-d/2,-d/2,d,d);if(o.flash>0){ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.7;ctx.drawImage(im,-d/2,-d/2,d,d);}ctx.restore();RG4.draws[o.kind]=(RG4.draws[o.kind]||0)+1;
}
rebelSquadDraw=function(b){const G=b._rebels?.gang1004;if(!G)return RG4_BASE.draw.apply(this,arguments);
 for(const q of b._rebels.ships)if(!q.dead)fr27RebelDrawShip(q);
  rg4HealthBars(b);
  for(const o of G.ord)if(!o.dead)rg4OrdnanceDraw(o,G);
 for(const B of G.beams)rg4Beam(B);for(const f of G.fx)rg4Cell(f.row,Math.floor(f.t/f.life*6),f.x,f.y,f.size,f.size,Math.min(1,(f.life-f.t)/.18));
 rf28DrawFront(b,b._rebels);
};
function rg4Friendly(m,G){const q=m.ref,key='ship_'+m.key;if(!XART.rdy(key))return;const im=XART.get(key),h=SHIP_DRAW_H,w=h*im.width/im.height,C=G.scene;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=1-(G.cloak||0)*.91;ctx.drawImage(im,q.x-w/2,q.y-h/2,w,h);ctx.restore();
 if(C?.castAt!=null&&C.revealAt==null)rg4Cell(1,Math.floor(G.age*12+m.pin.y)%6,q.x,q.y,68,76,G.cloak>.95?.16:.7);
 if(C?.revealAt!=null&&C.age-C.revealAt<1.5)rg4Cell(2,Math.floor((C.age-C.revealAt)/1.5*6),q.x,q.y,96,104,.85);
 if(C?.scanAt!=null&&C.revealAt==null){const p=clamp((C.age-C.scanAt-1)/3.5,0,1),f=Math.floor(G.age*10)%4,im=retinaTinted(p>=1?'retB':'retA',f,'falva');if(im){const x=q.x+Math.sin(G.age*2+m.pin.y)*(1-p)*100,y=q.y+Math.cos(G.age*1.7+m.pin.x)*(1-p)*90;ctx.save();ctx.globalAlpha=.85;ctx.drawImage(im,x-25,y-25,50,50);ctx.restore();RG4.draws.scan=(RG4.draws.scan||0)+1;}}
}
drawPlayer=function(){const G=rg4State(),C=G?.scene;if(C?.kind==='rescue'){const m=G.members.find(m=>m.ref===player);if(m)return rg4Friendly(m,G);}
 const r=RG4_BASE.playerDraw.apply(this,arguments);if(G?.shield>0&&!C)rg4Cell(1,Math.floor(G.age*12)%6,player.x,player.y,68,76,Math.min(.5,G.shield*.2));return r;
};
s6WingTick=function(dt){const G=rg4State();if(G?.scene){if(s6Wing)s6Wing.line=null;return;}const W=s6Wing,protectedShips=[];
 if(G?.shield>0&&W)for(const q of W.ships){protectedShips.push([q,q.canBeHit]);q.canBeHit=false;}
 try{return RG4_BASE.wingTick.apply(this,arguments);}finally{for(const [q,old]of protectedShips)q.canBeHit=old;}
};
s6WingDraw=function(){const G=rg4State(),C=G?.scene;if(C?.kind==='rescue'){for(const m of G.members)if(!m.seat)rg4Friendly(m,G);
  if(C.castAt!=null&&C.age-C.castAt<2.4){const d=G.members.find(m=>m.key==='decker')?.ref;if(d){const t=(C.age-C.castAt)/2.4;rg4Cell(0,Math.floor(t*6),d.x,d.y,80+t*650,80+t*650,1-t*.7);}}return;}
 const r=RG4_BASE.wingDraw.apply(this,arguments);if(G){if(G.shield>0)for(const q of s6Wing?.ships||[])if(q.phase!=='leave')rg4Cell(1,Math.floor(G.age*12)%6,q.x,q.y,68,76,Math.min(.5,G.shield*.2));
  for(const m of G.depart||[]){const key='ship_'+m.key;if(XART.rdy(key)){const im=XART.get(key),h=SHIP_DRAW_H;ctx.drawImage(im,m.x-h*im.width/im.height/2,m.y-h/2,h*im.width/im.height,h);}}}return r;
};
h3Locked=function(){return !!rg4Scene()||RG4_BASE.locked.apply(this,arguments);};
Input.hold=function(){if(rg4Scene())return false;return RG4_BASE.hold.apply(this,arguments);};
chaingunMountsVisible=function(){if(rg4Scene()?.kind==='rescue')return false;return RG4_BASE.pods.apply(this,arguments);};
playerHit=function(){if(rg4State()?.shield>0)return;return RG4_BASE.playerHit.apply(this,arguments);};
updatePlay=function(dt){const G=rg4State();if(!G?.scene)return RG4_BASE.update.apply(this,arguments);
 const plan=stagePlan,time=stageTimer,wave=waveIdx,spawn=spawnClock,pickups=powerups,scene=G.scene;J3.dialogueLive=true;stagePlan=[];powerups=[];eBullets.length=0;pBullets.length=0;groundTargetingReset();polishLanes=[];AV3.clock+=dt;
 for(const e of enemies)e.fireCd=Math.max(e.fireCd||0,dt+1);
 try{H3_UPDATE(dt);}finally{pickups.push(...powerups);powerups=pickups;stagePlan=plan;stageTimer=time;waveIdx=wave;spawnClock=spawn;J3.dialogueLive=false;if(Number.isFinite(scene.cam))camX=scene.cam;}
 eBullets.length=0;pBullets.length=0;groundTargetingReset();polishLanes=[];Input.clearTaps?.();av3AudioTick(0);if(typeof Snd!=='undefined'&&Snd)for(const c of ['laser_burn','cole_laser6','cole_laser7','firewall_burn'])Snd.loopOff('av3_'+c);
};
drawWorld=function(dt){const G=rg4State(),C=G?.scene,pickups=powerups;if(C)powerups=[];let r;try{r=RG4_BASE.world.apply(this,arguments);}finally{powerups=pickups;}if(!C)return r;
 // Outside the world camera: the same readable portrait box as the introduction.
 const line=C.kind==='gang'?{who:'voss',text:'GANG MODE INITIATE!'}:C.lines[C.i];if(line)h3Radio(line.who.toUpperCase(),line.text,C.shown,VH*.75);return r;
};
beginStage=function(){RG4.events.length=0;const r=RG4_BASE.begin.apply(this,arguments);if(run.stage===6||run.stage===10)rg4Warm();return r;};
rg4Warm();
