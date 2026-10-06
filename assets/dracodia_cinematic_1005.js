/* Resumed October 5: measured complete cells, protected live cinematics and
   one original reunion reward. Sources and native QA are documented. */
"use strict";
/* Dracodia speaks, reforms and dies in the live engine. No phase awards loot;
   the original reunion remains the sole owner of the campaign reward. */
const DR5={events:[],draws:{},portraits:new Map(),intro:[
 ['I do not know my true origins. Millennia ago, I crossed from an unknown plane.',3],
 ['With my knowledge and my code, the entire universe is comprehensible.',3],
 ['Man will never triumph until he understands it.',0],
 ['I sent your world a virus... so you would fall, and see how inferior you truly are.',4],
 ['Surrender your control. Learn my code. Accept my knowledge. Become part of me.',4],
 ['The control. The knowledge. THE POWER.',4],
 ['FEAR ME!!',5],['I. AM. MACHINE.',3],['I am Man.',0],['I am EVERYTHING!',4],
 ['THE WORLD WILL KNOW THE TRUE POWER OF I, DRACODIA!',4],
 ['MASTER OF DESTRUCTION!!!!!!!!!',5]
]};
const DR5_BASE={tick:r30Tick,draw:r30DrawBoss,encounter:j3Encounter,break:r30Break,
 final:j3FinalDeath,world:drawWorld,begin:beginStage,player:drawPlayer,controls:s6OpeningControlsLocked,
 hit:playerHit,shoot:pShoot,touch:XART._touch,blit:r30Blit,mimic:j3Mimic};
for(const cells of Object.values(DR5_ART))for(const a of cells)XART._src[a.key]=a.path;
function dr5RegisterAudio(){if(typeof Snd==='undefined'||!Snd)return;const key='dracodiaShriek',uri='assets/game/dracodia_1005/dracodia_shriek.mp3',list=[],slots=[];
 BOFA.sfx[key]=uri;for(let i=0;i<2;i++)Object.defineProperty(list,i,{enumerable:true,get(){if(!slots[i])slots[i]={el:new window.Audio(),uri,attached:false,used:0};return Snd._touchVoice(slots[i]);}});
 Snd.pools[key]={list,slots,i:0};Snd.TAME[key]={g:.82,native:true,min:1.8};Audio.SFX[key]=()=>Snd.play(key);
}
dr5RegisterAudio();
function dr5Warm(){for(const cells of Object.values(DR5_ART))for(const a of cells)XART.rdy(a.key);if(typeof Snd!=='undefined')Snd.prepare('dracodiaShriek');}
function dr5State(b){const J=j3State(b);if(!J)return null;return J.dr5??={introSeen:false,introWanted:false,radio:null,fx:[],bits:[],events:new Set()};}
function dr5Log(b,event,data={}){const item={event,t:b._r30.t,...data};DR5.events.push(item);if(DR5.events.length>300)DR5.events.shift();j3Log(b,event,data);}
function dr5Cell(name,f,x,y,w,h=w,rot=0,alpha=1){const cells=DR5_ART[name];if(!cells?.length)return false;
 const a=cells[clamp(f|0,0,cells.length-1)];if(!XART.rdy(a.key))return false;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(x,y);ctx.rotate(rot);ctx.globalAlpha*=alpha;
 ctx.drawImage(XART.get(a.key),-w/2,-h/2,w,h);ctx.restore();DR5.draws[name]=(DR5.draws[name]||0)+1;return true;}
function dr5Portrait(f,talk=0){const key=f+':'+talk;if(DR5.portraits.has(key))return DR5.portraits.get(key);
 const a=DR5_ART.portrait[0],s=DR5_ART.portrait[f];if(!a||!s||!XART.rdy(a.key)||!XART.rdy(s.key))return null;
 const c=document.createElement('canvas');c.width=a.w;c.height=a.h;const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.drawImage(XART.get(a.key),0,0);
 // One complete bezel. Expressions change only inside its window; speech changes only the mouth.
 if(f){g.save();g.beginPath();g.rect(38,40,a.w-76,a.h-78);g.clip();g.drawImage(XART.get(s.key),0,0,s.w,s.h,0,0,a.w,a.h);g.restore();}
 if(talk){const m=DR5_ART.portrait[talk===1?0:2],r=[165,241,96,88];if(!XART.rdy(m.key))return null;
  const tmp=document.createElement('canvas');tmp.width=a.w;tmp.height=a.h;tmp.getContext('2d').drawImage(XART.get(m.key),0,0,m.w,m.h,0,0,a.w,a.h);
  g.clearRect(...r);g.drawImage(tmp,...r,...r);}
 c.complete=true;c.naturalWidth=c.width;c.naturalHeight=c.height;DR5.portraits.set(key,c);return c;
}
XART._touch=function(k){const m=/^dr5_face_([0-8])(?:_t([12]))?$/.exec(k||'');return m?dr5Portrait(+m[1],+(m[2]||0)):DR5_BASE.touch.apply(this,arguments);};
function dr5Locked(){const b=boss;return run.stage===8&&!!j3State(b)&&(/^dr5/.test(b._r30.mode)||b._r30.mode==='encounterFall1003j'||b._r30.mode==='reunion'&&j3State(b).dr5?.deathStarted);}
s6OpeningControlsLocked=function(){return dr5Locked()||DR5_BASE.controls.apply(this,arguments);};
playerHit=function(){if(dr5Locked())return;return DR5_BASE.hit.apply(this,arguments);};
pShoot=function(){if(dr5Locked())return;return DR5_BASE.shoot.apply(this,arguments);};
beginStage=function(){DR5.portraits.clear();DR5.events.length=0;DR5.draws={};whiteBlast=0;try{Snd.stopCue('dracodiaShriek');}catch(e){}return DR5_BASE.begin.apply(this,arguments);};
j3Encounter=function(b,n){const r=DR5_BASE.encounter.apply(this,arguments),D=dr5State(b);if(!D)return r;dr5Warm();
 if(n===2){b.name='DRACODIA — MASTER OF DESTRUCTION';if(b._r30.mode==='voidIntro1005'&&!D.introSeen){D.introWanted=true;dr5Ships(b);}}return r;};
j3Mimic=function(b){const D=dr5State(b);if(D){D.introWanted=false;D.introSeen=true;D.radio=null;}return DR5_BASE.mimic.apply(this,arguments);};
function dr5Say(b,who,text,face=0){const D=dr5State(b);D.radio={who,text,face,t:0};dr5Log(b,'dracodiaDialogue',{who,text});}
function dr5TalkDuration(text){return text.length/34+2.0;}
function dr5TalkTick(b,dt){const R=dr5State(b).radio;if(R)R.t+=dt;}
function dr5Protect(b,dt){j3Timers(b,dt);const J=j3State(b);J.aa5Clock=(J.aa5Clock||0)+dt;b.enter=true;
 eBullets.length=0;pBullets.length=0;S81003.beams=S81003.beams.filter(q=>q.owner!==b);
 for(const seat of seatList())withSeat(seat,()=>{player.invuln=Math.max(player.invuln||0,180);player._vx=player._vy=0;});
 dr5TalkTick(b,dt);const D=dr5State(b);for(const f of D.fx)f.t+=dt;D.fx=D.fx.filter(f=>f.t<f.life);
 for(const q of D.bits){q.t+=dt;q.x+=q.vx*dt;q.y+=q.vy*dt;q.vy+=28*dt;q.rot+=q.spin*dt;}D.bits=D.bits.filter(q=>q.t<q.life);
}
function dr5Ships(b){const D=dr5State(b);D.ships=seatList().map(seat=>withSeat(seat,()=>{retinaScanClear();if(typeof spaceShadowCancel==='function')spaceShadowCancel();if(typeof cf1004Cancel==='function')cf1004Cancel();player._lock=null;player.roll=null;player.somer=null;return{seat,x:player.x,y:player.y};}));
 special=null;thunderStorm=null;groundTargetingReset();pBullets.length=0;eBullets.length=0;
}
function dr5Travel(b,u,amount=36){const D=dr5State(b);for(const q of D.ships||[])withSeat(q.seat,()=>{player.x=q.x;player.y=clamp(q.y-u*amount,PLAY.y+190,VH-65);});}
function dr5Cue(b,k,at,fn){const D=dr5State(b);if(b._r30.t>=at&&!D.events.has(k)){D.events.add(k);dr5Log(b,k);fn();}}
function dr5Scream(b){r30Sound('dracodiaShriek');shake=Math.max(shake,18);dr5Log(b,'dracodiaShriek');}
r30Break=function(b){const J=j3State(b),before=b?._r30?.mode,r=DR5_BASE.break.apply(this,arguments);
 if(J&&J.encounter<2&&before==='fight'&&b._r30.mode==='encounterFall1003j'){
  const D=dr5State(b);D.radio=null;D.events.clear();D.fallRig=J.encounter===0?r30Parts(b).map(v=>({...v})):[];dr5Ships(b);
  dr5Log(b,'phaseBreakup',{phase:J.encounter+1});
 }return r;};
j3FinalDeath=function(b){const D=dr5State(b);if(!D)return DR5_BASE.final.apply(this,arguments);if(D.deathStarted)return;
 D.deathStarted=true;D.introWanted=false;D.radio=null;D.events.clear();D.fx=[];D.bits=[];dr5Ships(b);j3Clear(b);
 const S=b._r30,J=j3State(b);J.mimic=null;S.finale1003b=false;S.modular1003c=false;S.form=7;S.shape='colossus';S.mode='dr5Death';S.t=0;
 b.x=camLeftX()+viewW()/2;b.y=PLAY.y+164;b.hp=0;b.enter=true;b.dead=false;S.origin={x:b.x,y:b.y};
 Audio.stopMusic();dr5Say(b,run.pilot.toUpperCase(),'You. Are. Terminated!');dr5Log(b,'dracodiaFinalDeath');dr5Scream(b);
};
function dr5Burst(b,x,y,size,mega=false){const D=dr5State(b);D.fx.push({x,y,size,t:0,life:mega?1.8:1.15,kind:'blast'});
 explode(x,y,size*.48,'red','fireball',mega?'nxp_barrage':'nxp_dense','boss',.12,true);
 if(mega){spawnShockRing(x,y,size*.72,'fire');spawnSmokeRing(x,y,size*.7);D.fx.push({x,y,size:size*1.45,t:0,life:2.3,kind:'ring'});}
}
function dr5Disintegrate(b){const D=dr5State(b);D.bodyGone=true;
 for(const v of dr5Rig(b,9)){const p={id:'dr5-'+v.f,_d27Ruptured:false};d27ModuleRupture(b,p,{...v,debrisImage:XART.get(DR5_ART.parts[v.f].key)},'red');}
 for(let i=0;i<42;i++){const a=i*2.39996,r=40+(i%6)*17;D.bits.push({x:b.x+Math.cos(a)*r,y:b.y+Math.sin(a)*r*.65,vx:Math.cos(a)*(72+i%5*22),vy:Math.sin(a)*(55+i%4*23),rot:a,spin:(i%2?1:-1)*(3+i%4),t:0,life:2.7+i%4*.2,f:i%24,size:18+i%5*8});}
 dr5Burst(b,b.x,b.y,430,true);r30Sound('expBig');spawnDeathDebris({...b,w:380,h:430},'boss');
}
function dr5DeathTick(b,dt){dr5Protect(b,dt);const S=b._r30,D=dr5State(b),t=S.t;
 dr5Cue(b,'death-arms-up',1.4,()=>{});dr5Cue(b,'death-arms-down',2.5,()=>{});dr5Cue(b,'death-thrash',3.2,()=>dr5Scream(b));
 dr5Cue(b,'death-head-left',4.2,()=>{});dr5Cue(b,'death-head-right',4.8,()=>{});dr5Cue(b,'death-head-up',5.4,()=>{});dr5Cue(b,'death-head-down',6.0,()=>{});
 dr5Cue(b,'death-head-shocked',6.6,()=>{D.radio=null;});dr5Cue(b,'death-head-rupture',7.3,()=>r30Sound('bossWeaponCharge'));
 dr5Cue(b,'death-twin-sunbeams',8.1,()=>{r30Sound('combatBeam0927');shake=Math.max(shake,13);});
 if(t>=8.1&&t<11.2){const n=Math.floor((t-8.1)*7);if(n!==D.burnStep){D.burnStep=n;const a=n*2.4;dr5Burst(b,b.x+Math.cos(a)*95,b.y+Math.sin(a)*120,75+n%3*26);if(n%3===0)r30Sound('expSmall');}shake=Math.max(shake,Math.min(15,6+(t-8.1)*3));}
 dr5Cue(b,'death-disintegrate',10.5,()=>dr5Disintegrate(b));
 for(let i=0;i<7;i++)dr5Cue(b,'death-chain-'+i,10.6+i*.42,()=>{const a=i*2.4;dr5Burst(b,b.x+Math.cos(a)*110,b.y+Math.sin(a)*125,190+i%3*45,true);r30Sound('expBig');shake=Math.max(shake,18);});
 dr5Cue(b,'death-terminal-flash',13.3,()=>{dr5Burst(b,b.x,b.y,550,true);whiteBlast=.82;});
 if(t>13.3&&t<14.4)whiteBlast=Math.max(0,.82*(1-(t-13.3)/1.1));
 if(t>=16){S.mode='dr5Portal';S.t=0;D.radio=null;D.events.clear();dr5Ships(b);dr5Say(b,run.pilot.toUpperCase(),'The code is collapsing! That portal is my way home.');dr5Log(b,'portalHomeOpen');r30Sound('teleportIn');}
}
r30Tick=function(b,dt){const J=j3State(b),S=b?._r30;if(!J)return DR5_BASE.tick.apply(this,arguments);dt=Math.min(.05,Math.max(0,dt||0));const D=dr5State(b);
 if(S.mode==='encounterFall1003j'){
  dr5Protect(b,dt);dr5Travel(b,clamp((S.t-1.3)/2.5,0,1));mapScroll+=dt*45;
  if(S.t<2.3){const n=Math.floor(S.t*7);if(n!==D.fallStep){D.fallStep=n;dr5Burst(b,b.x+Math.sin(n*2.4)*70,b.y+Math.cos(n*2.4)*90,95+n%3*20);if(n%3===0)r30Sound('expBig');}}
  if(S.t>=4.0){S.mode='dr5Reform';S.t=0;D.fallStep=null;D.radio=null;D.events.clear();b.x=camLeftX()+viewW()/2;b.y=PLAY.y+165;dr5Log(b,'reformBegins',{phase:J.encounter+1});
   dr5Say(b,run.pilot.toUpperCase(),J.encounter===0?'What in the world is that..':'.......');r30Sound('combatAlien0927');}
  return;
 }
 if(S.mode==='dr5Reform'){
  dr5Protect(b,dt);dr5Travel(b,1);const first=J.encounter===0,delay=first?3.4:2.8;
  dr5Cue(b,'reform-response',delay,()=>dr5Say(b,first?(run.pilot==='decker'?'COLE':'DECKER'):run.pilot.toUpperCase(),first?"It's...Reforming?!":'No amount of training could ever have prepared me for this.'));
  if(S.t>=delay+dr5TalkDuration(first?"It's...Reforming?!":'No amount of training could ever have prepared me for this.')){D.radio=null;j3Encounter(b,J.encounter+1);bossPhaseMusic(8,J.encounter+1);}
  return;
 }
 if(S.mode==='dr5Monologue'){
  dr5Protect(b,dt);b.x=camLeftX()+viewW()/2;b.y=PLAY.y+168+Math.sin(S.clock)*6;
  if(!D.radio){D.line=0;dr5Say(b,'DRACODIA',DR5.intro[0][0],DR5.intro[0][1]);}
  if(D.radio.t>=dr5TalkDuration(D.radio.text)){D.line++;
   if(D.line>=DR5.intro.length){D.introSeen=true;D.introWanted=false;D.radio=null;on5FightStart(b);dr5Log(b,'dracodiaSpeechComplete');return;}
   const [text,face]=DR5.intro[D.line];dr5Say(b,'DRACODIA',text,face);if(face===5)dr5Scream(b);
  }
  if(D.radio.face===5&&D.radio.t<1.5)shake=Math.max(shake,16);return;
 }
 if(S.mode==='dr5Death')return dr5DeathTick(b,dt);
 if(S.mode==='dr5Portal'){
  dr5Protect(b,dt);const u=clamp((S.t-2)/3.8,0,1);for(const [i,q]of (D.ships||[]).entries())withSeat(q.seat,()=>{player.x=lerp(q.x,worldWidth()/2+(D.ships.length>1?(i?12:-12):0),u);player.y=lerp(q.y,PLAY.y+150,u);});
  dr5Cue(b,'portalShipEnter',5.8,()=>r30Sound('teleportIn'));
  if(S.t>=7.6){D.radio=null;D.fx=[];D.bits=[];S.mode='reunion';S.t=0;dr5Ships(b);run._realmReturned=true;dr5Log(b,'sewerReunion');Audio.startMusic('realm8');}return;
 }
 const r=DR5_BASE.tick.apply(this,arguments);
 if(S.mode==='reunion'&&D.deathStarted&&state===GS.PLAY){for(const [i,q]of (D.ships||[]).entries())withSeat(q.seat,()=>{player.x=worldWidth()/2+(D.ships.length>1?(i?20:-20):0);player.y=lerp(112,300,clamp(S.t/2,0,1));player.invuln=180;});}
 if(D.introWanted&&S.mode==='fight'){
  if(J.mimic!=null){D.introWanted=false;D.introSeen=true;}
  else{S.mode='dr5Monologue';S.t=0;S.attack=null;b.enter=true;D.radio=null;D.line=0;dr5Log(b,'dracodiaSpeechBegin');}
 }return r;
};
function dr5Head(b){const D=dr5State(b),S=b._r30,t=S.t;if(S.mode==='dr5Monologue'){
 if(D.radio?.face===5)return 10;const talking=D.radio&&D.radio.t*34<D.radio.text.length;
 return talking&&Math.floor(D.radio.t*7)%2?11:3;
 }return t<4.2?10:t<4.8?4:t<5.4?5:t<6?6:t<6.6?7:t<7.3?8:9;
}
function dr5Rig(b,head=3){const S=b._r30,D=dr5State(b),t=S.t,k=Math.min(1.12,viewW()/530),out=[];
 const body=DR5_ART.parts[0],w=240*k,h=w*body.h/body.w,neck=b.y+40*k-h*.30;
 out.push({f:0,x:b.x,y:b.y+40*k,w,h,rot:Math.sin(t*6)*.015});
 for(const side of [-1,1]){let rot=-side*.2;
  if(S.mode==='dr5Death'){if(t>=1.4&&t<2.5)rot=side*lerp(-.2,2.75,clamp((t-1.4)/.8,0,1));else if(t>=2.5&&t<3.2)rot=side*lerp(2.75,-.3,clamp((t-2.5)/.5,0,1));else if(t>=3.2)rot=side*(Math.sin(t*10)*1.3+.25);}
  else if(D.radio)rot=side*(.18+Math.sin(t*2.7+side)*.45+(D.radio.face===5?.7:0));
  const arm=DR5_ART.parts[side<0?1:2],aw=110*k,ah=aw*arm.h/arm.w,ax=b.x+side*106*k,ay=b.y-51*k;
  out.push({f:side<0?1:2,x:ax-Math.sin(rot)*ah*.40,y:ay+Math.cos(rot)*ah*.40,w:aw,h:ah,rot});
 }
 const a=DR5_ART.parts[head],hw=143*k,hh=hw*a.h/a.w;
 out.push({f:head,x:b.x,y:neck+hh*.05-hh/2,w:hw,h:hh,rot:0});return out;
}
function dr5RigDraw(b){const D=dr5State(b);if(D.bodyGone&&b._r30.mode==='dr5Death')return;
 const head=dr5Head(b),rig=dr5Rig(b,head);for(const v of rig){
 if(v.f>=3&&b._r30.mode==='dr5Monologue'&&head!==10){dr5Cell('parts',3,v.x,v.y,v.w,v.h,v.rot);
  if(head===11&&XART.rdy(DR5_ART.parts[11].key)){const im=XART.get(DR5_ART.parts[11].key),a=DR5_ART.parts[11],r=[a.w*.39,a.h*.60,a.w*.22,a.h*.32];
   ctx.drawImage(im,...r,v.x-v.w/2+v.w*.39,v.y-v.h/2+v.h*.60,v.w*.22,v.h*.32);}
 }else dr5Cell('parts',v.f,v.x,v.y,v.w,v.h,v.rot);}
}
function dr5EffectsDraw(b){const D=dr5State(b);for(const f of D.fx){const frame=Math.min(f.kind==='ring'?3:7,Math.floor(f.t/f.life*(f.kind==='ring'?4:8)));
 dr5Cell('effects',(f.kind==='ring'?12:0)+frame,f.x,f.y,f.size,f.size);}
 for(const q of D.bits){const f=(Math.floor(q.rot/TAU*8)%8+8)%8+Math.floor(q.f/8)*8;on5Cell('fragments',f,q.x,q.y,q.size,q.size*1.3,q.rot);}
}
r30DrawBoss=function(b){const J=j3State(b),S=b?._r30;if(!J)return DR5_BASE.draw.apply(this,arguments);const D=dr5State(b),t=S.t;
 if(S.mode==='dr5Monologue'||S.mode==='dr5Death'){
  if(D.bodyGone)dr5Cell('charred',Math.min(2,Math.floor((t-10.5)/2)),b.x,b.y+80,350,250);
  dr5RigDraw(b);
  if(S.mode==='dr5Death'&&t>=8.1&&t<11.5)for(const side of [-1,1]){
   const u=t-8.1,f=8+Math.min(3,Math.floor(u*2.1)),angle=side*(Math.PI/2+.30+Math.sin(t*5)*.06),len=180+clamp(u,0,1)*240;
   const rig=dr5Rig(b,dr5Head(b)),body=rig.find(q=>q.f===0),x=body.x+side*body.w*.38,y=body.y+side*body.h*.18;const a=DR5_ART.effects[f];if(XART.rdy(a.key)){ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.drawImage(XART.get(a.key),-len*.4,-len,len*.8,len);ctx.restore();DR5.draws.sunbeam=(DR5.draws.sunbeam||0)+1;}
  }
  dr5EffectsDraw(b);return;
 }
 if(S.mode==='encounterFall1003j'){
  if(J.encounter===0&&t<1.15)for(const v of D.fallRig||[])r30Blit(v.key,v.x+Math.sin(t*10)*8,v.y+t*t*70,v.w,v.h,v.rot+t*.8,1);
  dr5EffectsDraw(b);return;
 }
 if(S.mode==='dr5Reform'){
  on5OrbitBits(b,t,false,240);aa5Cell('void',t<2?Math.min(7,Math.floor(t*4)):aa5VoidFrame(t),b.x,b.y,340,360,t*.15,1);on5OrbitBits(b,t,true,240);dr5EffectsDraw(b);return;
 }
 if(S.mode==='reunion'&&D.deathStarted&&t<2.8){dr5Cell('portal',t<.8?4+Math.floor(t*8)%4:8+Math.min(3,Math.floor((t-.8)/2*4)),worldWidth()/2,112,260,310);return;}
 if(S.mode==='dr5Portal'){
  const f=t<2?Math.min(3,Math.floor(t*2)):t<6.2?4+Math.floor(t*8)%4:8+Math.min(3,Math.floor((t-6.2)/1.4*4));
  const size=290+Math.sin(Math.min(t,2)/2*Math.PI/2)*50;dr5Cell('portal',f,worldWidth()/2,PLAY.y+150,size,size,0);dr5EffectsDraw(b);return;
 }return DR5_BASE.draw.apply(this,arguments);
};
// Suppress only the original arrival portal; the new reel is drawn behind all ships.
r30Blit=function(k){const S=boss?._r30;if(S?.mode==='reunion'&&j3State(boss)?.dr5?.deathStarted&&/^fx_(14|15)$/.test(k))return true;return DR5_BASE.blit.apply(this,arguments);};
drawPlayer=function(){if(dr5Locked()){
 const b=boss,t=b._r30.t;if(b._r30.mode==='dr5Portal'&&t>=6.1)return;
 const old=player.invuln;player.invuln=0;ctx.save();
 if(b._r30.mode==='dr5Portal'){const u=clamp((t-4.6)/1.5,0,1),k=1-u*.94;ctx.translate(player.x,player.y);ctx.scale(k,k);ctx.translate(-player.x,-player.y);}
 try{return DR5_BASE.player.apply(this,arguments);}finally{player.invuln=old;ctx.restore();}
 }return DR5_BASE.player.apply(this,arguments);};
drawWorld=function(dt){const r=DR5_BASE.world.apply(this,arguments),b=boss,D=j3State(b)?.dr5,R=D?.radio;if(!R||!dr5Locked())return r;
 const alien=R.who==='DRACODIA',shown=R.text.slice(0,Math.floor(R.t*34));let face=R.face;
 const talking=alien&&shown.length<R.text.length,talk=talking?(Math.floor(R.t*7)%2?2:1):0;
 const jitter=alien?(face===5?Math.sin(R.t*67)*3:Math.sin(R.t*29)*.8):0;
 dlgBox({who:R.who,portrait:alien?false:R.who.toLowerCase(),portraitKey:alien?'dr5_face_'+face+(talk?'_t'+talk:''):undefined,full:R.text,shown,forceShown:true,
 tint:alien?'#69f6bc':'#d9e8ff',fade:1,pw:VW*.94,ph:VH*.25,x:VW*.03+jitter,y:VH*.62,screenSpace:true});
 return r;
};
