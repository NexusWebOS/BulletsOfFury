'use strict';
/* RD74: Dracodia-only Chronos motion/armor/rage owner. Native form HP/progression. */
const RD74={base:{enter:v18Enter,tick:v19NativeTick,draw:v19DonorDraw,pose:hb20Pose,start:hb20Start,rig:v19HammerRig,at:v19AtRect,hit:modularHit,targets:retinaBossTargets,clear:v18Clear,load:stageLoadBegin,keys:v18Keys,warm:v18Warm,bg:drawBG,health:bossHealthFraction,theme:eh7Theme,clip:v18Clip},events:[],serial:0,draws:{},voices:['rd74RageCharge','rd74RageRelease','rd74WaveCharge','rd74WaveFire']};
for(const a of Object.values(RD74_ART.banks)){XART._src[a.key]=a.path;XART._src[a.hitKey]=a.hitPath;}
for(const a of Object.values(RD74_ART.effects))XART._src[a.key]=a.path;
XART._src.rd74_portrait='assets/game/levels/stage_08/cinematics/dracodia_portrait_box_1020/portrait.webp';
for(const [key,file]of Object.entries({rd74RageCharge:'dbz-powerup-minus2-reverb.mp3',rd74RageRelease:'saiyan-minus2-reverb.mp3',rd74WaveCharge:'kame_charge-minus2-reverb.mp3',rd74WaveFire:'basicbeam_fire-minus2-reverb.mp3'}))rd71Pool(key,'assets/game/shared/audio/original_sfx_minus2_reverb_1026/'+file);
function rd74Own(b){return !!b&&hb20Own(b);}
function rd74Log(event,data={}){RD74.events.push({event,clock:efxClock,...data});if(RD74.events.length>1200)RD74.events.shift();}
function rd74Keys(){return [...Object.values(RD74_ART.banks).flatMap(a=>[a.key,a.hitKey]),...Object.values(RD74_ART.effects).map(a=>a.key),'rd74_portrait','cf50_scenery_dim',CF50_ART.health];}
function rd74Init(b){const Q=hb20State(b);if(Q.rd74)return Q;Q.rd74=true;Q.action=null;Q.cool=.65;Q.shield=Q.gateFlash=0;Q.scale=1;Q.angle=0;Q.chrome=!!Q.rage;Q.opening=false;Q.seq=0;Q.rd74Age=0;Q.ragePool=Q.rage?b.hp:null;Q.broken=!!Q.rage;Q.parts[1].destroyed=false;Q.parts[2].destroyed=true;Q.waves=[];Q.fire=[];b.name='DRACODIA â€” CORRUPTED CHRONOS';rd74Log('form-enter',{hp:b.hp,max:b.maxhp});return Q;}
v18Enter=function(b){const r=RD74.base.enter.apply(this,arguments);if(rd74Own(b))rd74Init(b);return r;};
const rd74SetMode=v18SetMode;
// The native final handoff changes form before rebuilding anatomy. Retire the
// hammer/gun IDs here with the native zero-HP body factory; never heal a pool.
v18SetMode=function(b,mode){const N=b?._r30?.v18,Q=b?._r30&&j3State(b).hb20;if(mode==='v19FinalReform'&&N?.deathForm===8&&Q?.rd74&&b.parts===Q.parts){v18PartsBuild(b,0);rd74Log('reform-anatomy',{hp:b.hp,parts:b.parts.map(p=>p.id)});}return rd74SetMode.apply(this,arguments);};
v18Keys=function(){return run.stage===8?[...RD74.base.keys(),...rd74Keys()]:RD74.base.keys();};
v18Warm=function(){const prior=RD74.base.warm();return run.stage!==8?prior:rd74Keys().map(k=>XART.rdy(k)).every(Boolean)&&prior;};
stageLoadBegin=function(n,keys){if(n===8)Snd.prepare([...RD74.voices,CF48.key,'hammerThrow','hammerImpact','hammerMagnet','hammerChaingun']);return RD74.base.load.call(this,n,n===8?[...(keys||[]),...rd74Keys()]:keys);};
function rd74Stop(){for(const key of RD74.voices)Snd.stopCue(key);}
function rd74Say(b,text){hb20State(b).speech={text,t:0};rd74Log('portrait-announcement',{text});}
function rd74Sound(A,key,gain=1){A.sounds??=new Set();if(A.sounds.has(key))return;A.sounds.add(key);Snd.play(key,gain);rd74Log('sound',{key});}
function rd74Sample(bank,f=0){const a=RD74_ART.banks[bank];f=clamp(Math.floor(f),0,a.frames-1);const m=a.meta[f];return{a:{...m,key:a.key,white:a.hitKey,w:a.cw,h:a.ch,pivot:a.pivot,bank,frame:f,_rd74:true},k:1,rot:0,kind:bank};}
function rd74Blit(q,x,y,hit=false){const a=RD74_ART.banks[q.a.bank],f=q.a.frame,key=hit?a.hitKey:a.key;if(!XART.rdy(key))return false;ctx.drawImage(XART.get(key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);RD74.draws[q.a.bank]=(RD74.draws[q.a.bank]||0)+1;return true;}
function rd74Fx(n,f,x,y){const a=RD74_ART.effects[n];if(!a||!XART.rdy(a.key))return;f=clamp(f|0,0,a.frames-1);ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);}
function rd74Mat(Q){return Q.rage?'red':Q.chrome?'chrome':'regular';}
function rd74Point(b,q,p='tip'){return{x:b.x+q.a[p][0]-q.a.pivot[0],y:b.y+q.a[p][1]-q.a.pivot[1]};}
function rd74JumpPose(Q,A){const m=rd74Mat(Q),u=A.t-A.tell;if(A.t<.55)return rd74Sample('depart_'+m,A.t/.55*16);if(u<0)return rd74Sample('depart_'+m,16);if(u<.55)return rd74Sample('approach_'+m,u/.55*16);if(u<1)return rd74Sample('strike_'+m,(u-.55)/.45*16);if(u<1.4)return rd74Sample('retract_'+m,(u-1)/.4*16);if(A.strikes>1&&u<2.3)return u<1.85?rd74Sample('windup_'+m,(u-1.4)/.45*16):rd74Sample('strike_'+m,(u-1.85)/.45*16);if(A.strikes>1&&u<2.7)return rd74Sample('retract_'+m,(u-2.3)/.4*16);if(A.strikes===4&&u<4.1)return rd74Sample((u<3.4?'left_':'right_')+m,(u-(u<3.4?2.7:3.4))/.7*16);return rd74Sample('retract_'+m,16);}
hb20Pose=function(b){if(!rd74Own(b))return RD74.base.pose.apply(this,arguments);const Q=rd74Init(b),A=Q.action,m=rd74Mat(Q);if(b.hp<=0)return rd74Sample('stun_'+m,Math.floor(efxClock*9)%3);if(!A)return Q.rage?rd74Sample('rage_idle',Q.rd74Age*14%16):rd74Sample('idle_'+m,Q.rd74Age*10%9);
 const t=A.t,u=t-A.tell;
 if(A.type==='skystrike')return rd74JumpPose(Q,A);
 if(A.type==='armor')return rd74Sample('activation',t/4.2*24);
 if(A.type==='arsenal')return t<.95?rd74Sample('windup_'+m,t/.95*16):t<1.55?rd74Sample('empty_'+m,(t-.95)/.6*16):rd74Sample('pickup_'+m,clamp((t-1.55)/1.7,0,1)*16);
 if(A.type==='recall')return rd74Sample((A.fromRage?'rage_recall_':'gun_recall_')+m,t/.8*8);
 if(A.type==='rage'){
  if(t<.95)return rd74Sample('windup_'+m,t/.95*16);
  if(t<1.55)return rd74Sample('empty_'+m,(t-.95)/.6*16);
  if(t<2.75)return rd74Sample('rage_'+m,clamp((t-1.55)/1.2*2,0,2));
  if(t<5.8)return rd74Sample('charge',(t-2.75)/3.05*47);
  return rd74Sample('rage_red',7+(t-5.8)/1.4*5);
 }
 if(A.type==='throw')return t<A.tell?rd74Sample('windup_'+m,t/A.tell*16):u>4.6?rd74Sample('empty_retract_'+m,clamp((u-4.6)/.8,0,1)*16):rd74Sample('empty_'+m,clamp(u/.4,0,1)*16);
 if(A.type==='side')return rd74Sample((u<.7?'left_':'right_')+m,u<0?0:(u<.7?u/.7:(u-.7)/.7)*16);
 if(A.type==='spin')return rd74Sample('spin_'+m,u<0?0:Math.floor(u*24)%32);
 if(A.type==='gun')return rd74Sample('gun_'+(Q.rage?'red':'chrome'),t<.4?0:Math.floor(t*(u<0?8:24))%24);
 if(A.type==='wave')return rd74Sample('palm_'+m,t<1?0:t<3.3?(t-1)/2.3*5:t<5.1?5:Math.max(0,5-(t-5.1)/.6*5));
 if(A.type==='stun')return rd74Sample('stun_'+m,Math.floor(t*9)%3);
 return rd74Sample('retract_'+m,16);
};
function rd74Finish(b,A){const Q=hb20State(b);Q.action=null;Q.cool=.8;Q.shield=0;b._noHit=false;Q.previousHead=null;if(A.type==='skystrike')Q.opening=true;if(A.type==='armor'){Q.chrome=Q.gunSeen=true;Q.pendingArsenal=true;}if(A.type==='arsenal')Q.pendingGun=true;if(A.type==='rage'){Q.rage=Q.broken=true;Q.ragePool=A.ragePool;Q.pendingRecall='rage';b.name='DRACODIA â€” CRIMSON CODE RAGE';}if(A.type==='gun'){Q.parts[2].destroyed=true;Q.pendingRecall='gun';}rd74Stop();rd74Log('attack-end',{type:A.type,hp:b.hp});if(Q.pendingRecall){Q.cool=0;hb20Start(b,'recall');}else if(A.type==='arsenal'){Q.cool=0;hb20Start(b,'gun');}}
hb20Start=function(b,type){if(!rd74Own(b))return RD74.base.start.apply(this,arguments);const Q=rd74Init(b),p=b20Target(b),book=Q.rage?['skystrike','throw','wave','spin','side','wave']:['skystrike','side','throw','spin','skystrike','gun'];
 if(!type){type=!Q.opening?'skystrike':!Q.chrome?'armor':Q.pendingArsenal?'arsenal':Q.pendingGun?'gun':!Q.rage&&b.hp<=b.maxhp*.29?'rage':book[Q.seq++%book.length];}
 type=({shield:Q.chrome?'side':'armor',pickup:'armor',redrage:'rage',break:'rage',fire:'rage',charge:'wave',ball:'spin',dance:'side',luminaire:'wave'})[type]||type;
 if(type==='gun'&&Q.gunHP<=0)type='side';const A=Q.action={type,t:0,tell:1.15,origin:{x:b.x,y:b.y},target:{x:clamp(p.x,camLeftX()+100,camRightX()-100),y:clamp(p.y,viewTopY()+170,VH-90)},serial:++RD74.serial,next:0,hit:new Set(),hits:new Map(),bolts:[],n:0};Q.pendingGun=Q.pendingArsenal=false;Q.shield=0;Q.previousHead=null;
 if(type==='skystrike'){A.strikes=diffKey==='furious'?4:diffKey==='hard'?2:1;A.duration=A.tell+(A.strikes===4?4.6:A.strikes===2?3.2:1.9);}
 else if(type==='armor'){A.tell=0;A.duration=4.2;rd74Say(b,'CHROMIUM CODE ARMOR, ACTIVATED.');}
 else if(type==='arsenal'){A.tell=0;A.duration=3.55;}
 else if(type==='recall'){A.tell=0;A.duration=.8;A.fromRage=Q.pendingRecall==='rage';Q.pendingRecall=null;}
 else if(type==='rage'){A.tell=0;A.duration=7.2;A.ragePool=b.hp;rd74Say(b,'YOUR POWER... REWRITTEN. CRIMSON RAGE, ACTIVATE!');}
 else if(type==='throw'){A.tell=1.0;A.duration=6.4;A.orbit=0;A.direction=1;}
 else if(type==='wave'){A.tell=3.3;A.duration=5.7;A.target.x=clamp(p.x,camLeftX()+90,camRightX()-90);rd74Say(b,'EVERY WEAPON YOU HAVE... IS MINE.');}
 else if(type==='gun'){A.tell=1.2;A.duration=5;Q.parts[2].destroyed=false;}
 else A.duration=A.tell+(type==='spin'?2.6:type==='stun'?1.4:1.8);
 b20Cue('bossWeaponCharge');rd74Log('attack-start',{type,strikes:A.strikes,hp:b.hp});return A;
};
function rd74ToolAt(b,A){const Q=hb20State(b),u=A.t-A.tell;if(u<0)return rd74Point(b,hb20Pose(b));const home=rd74Point(b,rd74Sample('retract_'+rd74Mat(Q),16));if(!A.launch)return home;const cx=(camLeftX()+camRightX())/2,cy=viewTopY()+viewH()*.5,rx=viewW()*.5-65,ry=viewH()*.5-80,theta=A.theta0+A.orbit,edge={x:cx+Math.cos(theta)*rx,y:cy+Math.sin(theta)*ry};if(u<.3)return{x:lerp(A.launch.x,edge.x,u/.3),y:lerp(A.launch.y,edge.y,u/.3)};if(u>4.6){const v=clamp((u-4.6)/.8,0,1);return{x:lerp(edge.x,home.x,v),y:lerp(edge.y,home.y,v)};}return edge;}
function rd74Melee(b,A,part,head){if(!A.hits.has(part))A.hits.set(part,new Set());if(A.last&&A.last.part===part)b20HitSegment(b,A.last.head,head,27,'Corrupted chromium hammer',A.hits.get(part));A.last={part,head};}
function rd74Impact(b,A,i){if(A['impact'+i])return;A['impact'+i]=true;const bank=i<3?'strike':i===3?'left':'right',at=rd74Point(b,rd74Sample(bank+'_'+rd74Mat(hb20State(b)),16));explode(at.x,at.y,65,hb20State(b).rage?'red':'purple');b20Cue('hammerImpact');shake=Math.max(shake,6);rd74Log('hammer-impact',{stroke:i,x:at.x,y:at.y});}
function rd74BoltTick(b,A,dt){const progress=clamp((A.t-2.75)/3.05,0,1),n=Math.floor(26*(1-Math.pow(1-progress,1.6)));while(A.n<n){const k=++A.n,side=k%2?-1:1,x=clamp(b.x+side*(115-k*3),camLeftX()+25,camRightX()-25);A.bolts.push({x,t:0});Snd.play(CF48.key,.63);rd74Log('rage-lightning',{n:k,x});shake=Math.max(shake,2+k*.14);}for(const q of A.bolts)q.t+=dt;A.bolts=A.bolts.filter(q=>q.t<.18);}
v19NativeTick=function(b,dt){if(!rd74Own(b))return RD74.base.tick.apply(this,arguments);const Q=rd74Init(b),N=b._r30.v18;dt=clamp(dt,0,.05);Q.age+=dt;Q.rd74Age+=dt;if(Q.speech){const S=Q.speech;S.t+=dt;const n=Math.min(S.text.length,Math.floor(S.t*34));dialogueLetterTicks(S.text,S.shown||0,n);S.shown=n;if(S.t>S.text.length/34+2)Q.speech=null;}N.donorAge=(N.donorAge||0)+dt;Q.cool=Math.max(0,Q.cool-dt);Q.shield=Q.gateFlash=0;b._noHit=false;
 if(!Q.action&&Q.cool<=0)hb20Start(b);const A=Q.action;
 if(A){A.t+=dt;const u=A.t-A.tell;if(A.tell>0&&A.t<=A.tell)combatWarningTick(b,'rd74-'+A.serial+'-'+A.type,A.t,A.tell);
  if(A.type==='skystrike'){
   const end=rd74Sample('strike_'+rd74Mat(Q),16),off={x:end.a.tip[0]-end.a.pivot[0],y:end.a.tip[1]-end.a.pivot[1]},destination={x:clamp(A.target.x-off.x,camLeftX()+120,camRightX()-120),y:clamp(A.target.y-off.y,viewTopY()+135,VH-155)};
   if(A.t<.55){const v=v19Ease(A.t/.55);b.x=A.origin.x;b.y=lerp(A.origin.y,viewTopY()+30,v);b._noHit=true;}
   else if(u<0){b.x=lerp(A.origin.x,destination.x,clamp((A.t-.55)/.6,0,1));b.y=viewTopY()+30;b._noHit=true;}
   else if(u<.55){const v=v19Ease(u/.55);b.x=destination.x;b.y=lerp(viewTopY()+30,destination.y,v);b._noHit=u<.4;}
   else{b.x=destination.x;b.y=destination.y+Math.sin(Q.rd74Age*2)*3;const active=u<1?1:A.strikes>1&&u>=1.85&&u<2.3?2:A.strikes===4&&u>=2.7&&u<4.1?(u<3.4?3:4):0;if(active)rd74Melee(b,A,active,rd74Point(b,hb20Pose(b)));else A.last=null;}
   if(u>=1)rd74Impact(b,A,1);if(A.strikes>1&&u>=2.3)rd74Impact(b,A,2);if(A.strikes===4&&u>=3.4)rd74Impact(b,A,3);if(A.strikes===4&&u>=4.1)rd74Impact(b,A,4);
  }else if(A.type==='armor'){b._noHit=true;b.y=A.origin.y+Math.sin(A.t*3)*3;rd74Sound(A,'bossWeaponCharge');}
  else if(A.type==='arsenal'){b._noHit=true;b.x=A.origin.x;b.y=A.origin.y;if(A.t>=.95&&!A.launch){A.launch=rd74Point(b,rd74Sample('windup_'+rd74Mat(Q),16));rd74Sound(A,'hammerThrow');rd74Log('arsenal-hammer-up');}if(A.t>=2.35&&!A.caught){A.caught=true;rd74Sound(A,'weapon');rd74Log('arsenal-gun-catch');}}
  else if(A.type==='recall'){b.x=A.origin.x;b.y=A.origin.y;rd74Sound(A,'hammerMagnet');}
  else if(A.type==='rage'){
   b._noHit=true;b.x=A.origin.x+(A.t>2.75?Math.sin(A.t*67)*Math.min(4,(A.t-2.75)*1.4):0);b.y=A.origin.y+Math.sin(A.t*2)*3-Math.max(0,A.t-2.75)*2;
   if(A.t>=.95&&!A.launch){A.launch=rd74Point(b,rd74Sample('windup_'+rd74Mat(Q),16));rd74Sound(A,'hammerThrow');}
   if(A.t>=2.75){rd74Sound(A,'rd74RageCharge');rd74BoltTick(b,A,dt);}if(A.t>=5.8){rd74Sound(A,'rd74RageRelease');if(!A.flash){A.flash=true;flashScreen=Math.max(flashScreen||0,.26);}}
  }else if(A.type==='throw'){
   if(u>=0){if(!A.launch){A.launch=rd74Point(b,rd74Sample('windup_'+rd74Mat(Q),16));A.theta0=Math.atan2((A.launch.y-(viewTopY()+viewH()*.5))/(viewH()*.5-80),(A.launch.x-(camLeftX()+camRightX())/2)/(viewW()*.5-65));rd74Sound(A,'hammerThrow');}A.orbit+=dt*TAU/2.2*A.direction;rd74Melee(b,A,1,rd74ToolAt(b,A));}
  }else if(A.type==='side'||A.type==='spin'){b.y=A.origin.y+Math.sin(Q.rd74Age*2)*4;if(u>=0)rd74Melee(b,A,A.type==='side'?(u<.7?1:2):1,rd74Point(b,hb20Pose(b)));}
  else if(A.type==='gun'){
   b.x=clamp(A.origin.x+Math.sin(A.t*1.1)*90,camLeftX()+100,camRightX()-100);b.y=A.origin.y+Math.sin(A.t*2)*4;
   if(u>=0&&!Q.parts[2].destroyed&&u>=A.next){A.next=u+.15;const m=rd74Point(b,hb20Pose(b),'muzzle'),fan=A.n++%2===0,dirs=fan?[-.40,-.20,0,.20,.40]:[-.025,.025];for(const d of dirs){const q=eShootT(m.x,m.y,Math.PI/2+d,5.2,'mg',{w:6,h:16});if(q){q._hb20Owner=b;q._weaponProof=true;}}A.muzzle=.09;rd74Log('gun-volley',{x:m.x,y:m.y,fan});if(u>=A.sfxNext||!A.sfxNext){Snd.play('hammerChaingun',.6);A.sfxNext=u+1.3;}}
   A.muzzle=Math.max(0,(A.muzzle||0)-dt);
  }else if(A.type==='wave'){
   if(!A.lock)A.target.x=clamp(targetShip(b.x,b.y).x,camLeftX()+95,camRightX()-95);b.x=clamp(lerp(A.origin.x,A.target.x-112,v19Ease(clamp(A.t/2.5,0,1))),camLeftX()+105,camRightX()-140);b.y=A.origin.y+Math.sin(Q.rd74Age*2)*4;const m=rd74Point(b,hb20Pose(b),'muzzle');A.muzzle=m;
   if(A.t>=1)rd74Sound(A,'rd74WaveCharge');if(A.t>=2.5&&!A.lock){A.lock=true;A.fireX=rd74Point(b,rd74Sample('palm_'+rd74Mat(Q),5),'muzzle').x;}
   if(A.t>=3.3){rd74Sound(A,'rd74WaveFire');const from={x:A.fireX,y:m.y},to={x:A.fireX,y:VH+30};b20HitSegment(b,from,to,36,'Crimson code wave',A.hit);}
  }
  if(A.t>=A.duration)rd74Finish(b,A);
 }
 if(!Q.action){const home={x:(camLeftX()+camRightX())/2,y:viewTopY()+viewH()*.30};b.x+=clamp(home.x-b.x,-90*dt,90*dt);b.y+=clamp(home.y-b.y,-80*dt,80*dt);b.y+=Math.sin(Q.rd74Age*2)*dt*5;}
 Q.parts[0].hp=b.hp;Q.parts[1].hp=Q.hammerHP;Q.parts[1].destroyed=['gun','rage','arsenal','recall'].includes(Q.action?.type);Q.parts[2].destroyed=Q.action?.type!=='gun'||Q.gunHP<=0;Q.parts[2].hp=Q.gunHP;b._drawY=b.y;j3Save(b);
 if(N.donorAge>52&&!Q.action&&j3State(b).hp[0]>0)j3Morph(b,'home');
};
v19HammerRig=function(b){if(!rd74Own(b))return RD74.base.rig.apply(this,arguments);const Q=rd74Init(b),q=hb20Pose(b),core=b20Piece(Q.parts[0],q.a,b,0,1,'core',1);core._rd74=true;const out=[core],A=Q.action;
 if(!Q.parts[1].destroyed){const at=A?.type==='throw'&&A.launch?rd74ToolAt(b,A):rd74Point(b,q);out.push({...core,p:Q.parts[1],x:at.x,y:at.y,w:70,h:80,z:5,_rd74:false,_hb20Target:true,layer:'hammer',spec:{role:'hammerHead',hidden:true}});}
 if(A?.type==='gun'&&!Q.parts[2].destroyed){const at=rd74Point(b,q,'muzzle');out.push({...core,p:Q.parts[2],x:at.x,y:at.y-40,w:85,h:100,z:5,_rd74:false,_hb20Target:true,layer:'chaingun',spec:{role:'weapon',hidden:true}});}return out;
};
v19AtRect=function(v,x,y){if(!v._rd74)return RD74.base.at.apply(this,arguments);const px=Math.floor(x-v.ax+v.a.pivot[0]),py=Math.floor(y-v.ay+v.a.pivot[1]),row=v.a.spans?.[py];if(!row)return false;for(let i=0;i<row.length;i+=2)if(px>=row[i]&&px<row[i+1])return true;return false;};
modularHit=function(dmg){const b=boss;if(!rd74Own(b))return RD74.base.hit.apply(this,arguments);const Q=rd74Init(b);if(!r30Live(b)||b._noHit||!(dmg>0))return;const p=Q.parts.includes(b._lastPart)?b._lastPart:Q.parts[0];
 if(p.id==='hammer'){const missile=_dmgSrc==='missile'||_dmgBullet&&typeof hammerMissile==='function'&&hammerMissile(_dmgBullet);if(missile&&Q.action?.type==='throw'&&Q.action.launch){Q.action.direction*=-1;markHit(p,.10);rd74Log('hammer-reversed',{direction:Q.action.direction});}return;}
 if(p.id==='chaingun'){Q.gunHP=Math.max(0,Q.gunHP-dmg);p.hp=Q.gunHP;markHit(p,.12);if(!Q.gunHP){p.destroyed=true;explode(b.x,b.y+75,45,'purple');}return;}
 const floor=!Q.chrome?b.maxhp*.65:!Q.rage?b.maxhp*.28:0,d=Math.max(0,Math.min(dmg,b.hp-floor));b.hp-=d;Q.parts[0].hp=b.hp;stageStats.dmgDealt+=d;markHit(b,.12);j3Save(b);if(b.hp<=0)r30Break(b);
};
function rd74DrawTool(b,A){const Q=hb20State(b),m=rd74Mat(Q),u=A.t-A.tell;let at;if(A.type==='rage'||A.type==='arsenal'){if(A.t<.95||A.t>2.1||!A.launch)return;const v=(A.t-.95)/1.15;at={x:A.launch.x,y:lerp(A.launch.y,viewTopY()-180,v)};}else if(A.type==='recall'){const q=hb20Pose(b),to=rd74Point(b,q);at={x:to.x,y:lerp(viewTopY()-180,to.y,v19Ease(A.t/.8))};}else if(u>=0)at=rd74ToolAt(b,A);if(at){const q=rd74Sample('tool_'+m,A.type==='recall'?Math.round(((-Math.PI/2-.12)+Math.PI/2)/TAU*64+64)%64:Math.floor(A.t*28)%64),off=rd74Point({x:0,y:0},q);rd74Blit(q,at.x-off.x,at.y-off.y);}}
v19DonorDraw=function(b){if(!rd74Own(b))return RD74.base.draw.apply(this,arguments);const Q=rd74Init(b),A=Q.action,q=hb20Pose(b);if((Q.rage||A?.type==='rage'&&A.t>5.8)&&(q.a.depth??1)>.85)rd74Blit(rd74Sample('rage_flame',Math.floor(Q.rd74Age*18)%21),b.x,b.y);rd74Blit(q,b.x,b.y,(b.flash||0)>.075&&Math.floor(efxClock*40)%2===0);
 if(A){const u=A.t-A.tell;if(A.type==='skystrike'&&u<.9)b20Reticle(A.target.x,A.target.y,52,clamp(A.t/(A.tell+.9),0,1));if(['throw','rage','arsenal','recall'].includes(A.type))rd74DrawTool(b,A);
  if(A.type==='arsenal'&&A.t>1.2){const f=clamp(Math.floor((A.t-1.8)*8),0,RD74_ART.effects.crate.frames-1),fall=Math.max(0,A.t-3.0);rd74Fx('crate',f,b.x,b.y+154+fall*fall*850);}
  if(A.type==='throw'&&u<0)rd72Blit('asterisk',Math.floor(A.t*10)%8,b.x,b.y-135);
  if(A.type==='rage'){for(const bolt of A.bolts)rd74Fx('lightning',Math.floor(bolt.t*44)%8,bolt.x,viewTopY()-12);}
  if(A.type==='wave'){
   if(A.t>=1&&A.t<3.3){rd74Fx('gather',Math.floor(clamp((A.t-1)/2.3,0,1)*15),A.muzzle.x,A.muzzle.y);rd72Blit('asterisk',Math.floor(A.t*10)%8,b.x,b.y-135);b20Field(b,{x:A.fireX??A.target.x,y:A.muzzle.y},{x:A.fireX??A.target.x,y:VH},76,clamp((A.t-1)/2.3,0,1));}
   if(A.t>=3.3&&A.t<5.1){const f=c41Frame(A.t-3.3,1.8);rd74Fx('wave_'+(Q.rage?'red':'purple'),f,A.fireX,A.muzzle.y);}
  }
  if(A.type==='gun'&&A.muzzle>0){const at=rd74Point(b,q,'muzzle');wm26Draw(ctx,'chaingun',at.x,at.y,Math.PI/2,1-A.muzzle/.09,48);}
 }
 if(Q.speech){const S=Q.speech,w=cd27Width(VW-20),x=(VW-w)/2,y=48;ctx.save();worldXformEscape();CD27.inDlg++;msgFaceUse('dialogue');try{const r=ui20Panel('DRACODIA',x,y,w,CD27.height,true);if(r)ui20PanelContents('DRACODIA',S.text,S.shown||0,'rd74_portrait',r);}finally{msgFaceUse(null);CD27.inDlg--;ctx.restore();}}
 // No legacy bubble, circular aura, floating tool rig or fire-fist fallback.
};
drawBG=function(){const r=RD74.base.bg.apply(this,arguments),b=boss;if(rd74Own(b)&&!b.dead){const Q=hb20State(b),A=Q?.action;let level=Q?.rage?7:0;if(A?.type==='rage')level=Math.round(clamp((A.t-2.75)/3.05,0,1)*15);if(A?.type==='wave')level=Math.max(level,Math.round(clamp((A.t-1)/1.5,0,1)*11));if(level)cf50DimDraw(level);}return r;};
bossHealthFraction=function(b){if(rd74Own(b)){const Q=hb20State(b),A=Q?.action;if(A?.type==='rage')return lerp(b.hp/b.maxhp,1,clamp((A.t-2.75)/3.05,0,1));if(Q?.rage&&Q.ragePool)return clamp(b.hp/Q.ragePool,0,1);}return RD74.base.health.apply(this,arguments);};
eh7Theme=function(b){const Q=rd74Own(b)&&hb20State(b);if(Q&&(Q.rage||Q.action?.type==='rage'&&Q.action.t>=2.75))return 'cf50_rage';return RD74.base.theme.apply(this,arguments);};
v18Clip=function(name,t,d,x,y){if(name==='morph_hammer')return rd74Blit(rd74Sample('retract_regular',16),x,y);return RD74.base.clip.apply(this,arguments);};
v18Clear=function(b){if(rd74Own(b)){rd74Stop();const Q=hb20State(b);if(Q){Q.action=null;Q.waves=[];Q.fire=[];Q.speech=null;Q.shield=0;}rd74Log('cleanup');}return RD74.base.clear.apply(this,arguments);};
globalThis.BOF_DRACODIA_CHRONOS=RD74;
