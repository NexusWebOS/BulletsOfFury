"use strict";
/* Mike's October12 filmed demonstration: orbit files, depth curls, bomb rolls,
   southern crossings, spirals and visibly charged kamikazes. Authored poses only. */
const VP12={units:[],groups:[],events:[],stage:0,age:0,next:10,serial:0,base:{update:updatePlay,draw:drawEnemy,begin:beginStage},types:['orbit','corner','barrel','south','spiral','kamikaze','mixed']};
for(const d of Object.values(VP12_ART)){XART._src[d.key]=d.path;if(d.rollKey)XART._src[d.rollKey]=d.rollPath;}
const vp12Load=stageLoadBegin;stageLoadBegin=function(n,keys){const a=VP12_ART[n];return vp12Load.call(this,n,[...(keys||[]),...(a?[a.key,a.rollKey,'lz_bomb']:[])]);};
const vp12FireDraw=drawFireType;drawFireType=function(b){if(!b._vpBomb)return vp12FireDraw.apply(this,arguments);if(!XART.rdy('lz_bomb'))return false;const im=XART.get('lz_bomb'),h=24,w=h*im.width/im.height;ctx.drawImage(im,b.x-w/2,b.y-h/2,w,h);return true;};
function vp12Log(event,data={}){VP12.events.push({event,...data});if(VP12.events.length>240)VP12.events.shift();}
const vp12Tier=()=>({easy:0,normal:1,hard:2,furious:3,insanity:3}[diffKey]??1);
// These are the actual aircraft used as the authored pose-bank references.
// Read their live roster HP through EHP so difficulty, loadout pressure and co-op
// match a regular family member. Keep the formation's own movement controller.
function vp12FamilyHealth(stage){
 const family={1:'s1jetdelta',4:'s4interceptor',6:'s6dart',8:'s8interceptor'}[stage];
 const row=stage===1?NEF_S1[family]:stage===4?S4CHASE[family]:stage===6?S6STORM[family]:S8MEGA[family];
 // enc30's modular desert jet receives this same hull reinforcement after EHP.
 const hp=EHP(row.hp)*(stage===4?1.12:1);return{family,hp};
}
function vp12FireTiming(g,q){return{tell:g.type==='barrel'?.75:1.15,
 release:(g.type==='barrel'?1.1:[1.9,1.75,1.6,1.5][g.tier])+q.slot*.08,
 gap:[.48,.42,.36,.30][g.tier]};}
function vp12Blocked(){return state!==GS.PLAY||player.dead||bossActive||subBossActive||warnT>0||story||debugFight||wfx?.fseq||s6Opening||(typeof h3Locked==='function'&&h3Locked())||(typeof BOFCinematicDirector!=='undefined'&&BOFCinematicDirector.live);}
function vp12Point(g,q,t){const k=clamp(t,0,1),s=q.side,delay=q.slot*.015,u=clamp((k-delay)/(1-delay),0,1),w=g.right-g.left,h=PLAY.h;
 if(g.type==='orbit'||g.type==='mixed'){const a=-Math.PI/2+u*TAU*(g.type==='mixed'?1.25:1)-q.slot*.22,cx=g.left+w*.5+s*Math.sin(u*Math.PI)*w*.20,cy=PLAY.y+h*.36,r=w*.23;
  if(g.age<.9)return{x:cx+Math.cos(a)*r,y:lerp(PLAY.y-60-q.slot*8,cy+Math.sin(a)*r*.63,clamp(g.age/.9,0,1))};
  if(u<.72)return{x:cx+Math.cos(a)*r,y:cy+Math.sin(a)*r*.63};const v=(u-.72)/.28;return{x:lerp(cx+Math.cos(a)*r,g.target.x-s*w*.22,v),y:lerp(cy+Math.sin(a)*r*.63,PLAY.y+h+65,v)};}
 if(g.type==='corner'){const bend=-Math.sin(u*Math.PI)*s*w*.32;return{x:lerp(s<0?g.left-35:g.right+35,g.target.x,u)+bend,y:lerp(PLAY.y-55,PLAY.y+h+65,u)};}
 if(g.type==='barrel')return{x:lerp(s<0?g.left-60:g.right+60,s<0?g.right+70:g.left-70,u),y:PLAY.y+h*(.28+(q.slot%3)*.14)+Math.sin(u*TAU)*25};
 if(g.type==='south'){const a=u*Math.PI;return{x:g.left+w*.5+s*Math.cos(a)*w*.35,y:lerp(PLAY.y+h+50,PLAY.y-80,u)+Math.sin(a)*h*.22};}
 if(g.type==='spiral'){const a=-Math.PI/2+s*u*TAU*1.3,r=w*(.28-.15*u);return{x:g.left+w*.5+s*w*.16+Math.cos(a)*r,y:PLAY.y-45+u*(h+140)+Math.sin(a)*r*.45};}
 const charge=1.25+(.18*(3-g.tier));if(g.age<charge)return{x:g.left+w*(.12+.76*(q.slot+.5)/g.count),y:PLAY.y+58+Math.sin(g.age*10+q.slot)*2};
 const v=clamp((g.age-charge-q.slot*.13)/[2.4,2,1.8,1.6][g.tier],0,1),a=Math.atan2(g.target.y-q.oy,g.target.x-q.ox);return{x:q.ox+Math.cos(a)*600*v,y:q.oy+Math.sin(a)*600*v};
}
function vp12Spawn(type){const stage=run.stage,A=VP12_ART[stage];if(!A||!XART.rdy(A.key))return false;const tier=vp12Tier(),count=[3,5,7,9][tier],health=vp12FamilyHealth(stage),hp=type==='corner'?health.hp:Math.max(1,Math.min([6,8,10,12][tier],Math.ceil(health.hp*.5))),g={id:VP12.serial++,stage,type,tier,count,age:0,family:health.family,duration:type==='barrel'?4.4:type==='kamikaze'?6.2:7.4,left:camLeftX(),right:camRightX(),target:{x:player.x,y:player.y},live:0};
 for(let i=0;i<count;i++){const side=i%2?-1:1,q={slot:i,side,angle:Math.PI,scale:type==='corner'?1.8:1,shot:0,roll:0},e=spawnEnemy('drone',g.left+(g.right-g.left)*(.12+.76*(i+.5)/count),PLAY.y+58,{pattern:'vp12',hp,w:28,shoots:false});if(!e)continue;
  // The placeholder drone supplies collision/death bookkeeping only. Its
  // invisible cannon otherwise fires outside this formation's warned schedule.
  delete e._cn;e.pattern='vp12';e.shoots=false;e.vx=e.vy=0;e._bodShadow=true;e._noSep=true;e._vp12={g,q};q.ox=e.x;q.oy=e.y;const p=vp12Point(g,q,0);e.x=p.x;e.y=p.y;g.live++;}
 if(!g.live)return false;VP12.groups.push(g);vp12Log('formation',{stage,type,count:g.live});return true;
}
beginStage=function(n){VP12.groups=[];VP12.stage=n;VP12.age=0;VP12.next=10;const r=VP12.base.begin.apply(this,arguments);const a=VP12_ART[n];if(a){XART.rdy(a.key);if(a.rollKey)XART.rdy(a.rollKey);}return r;};
function vp12Move(e,dt){const {g,q}=e._vp12;if(g.stage!==run.stage){e.dead=true;return;}const p=vp12Point(g,q,g.age/g.duration),next=vp12Point({...g,age:g.age+.01},q,(g.age+.01)/g.duration);e.x=p.x;e.y=p.y;q.angle=Math.atan2(next.x-p.x,-(next.y-p.y));q.scale=g.type==='corner'?lerp(1.8,1,clamp(g.age/1.4,0,1)):1;e.shoots=false;e.vx=e.vy=0;e._noHit=g.type==='corner'&&g.age<.75;
 if(g.age>=g.duration)e.dead=true;
}
updatePlay=function(dt){const blocked=vp12Blocked();if(!blocked)for(const g of VP12.groups)g.age+=dt;for(const e of enemies)if(e._vp12&&!e.dead&&e._dyingT==null)vp12Move(e,dt);
 const r=VP12.base.update.apply(this,arguments);if(![1,4,6,8].includes(run.stage))return r;if(!blocked)VP12.age+=dt;
 const live=enemies.filter(e=>e._vp12&&!e.dead&&e._dyingT==null);VP12.groups=VP12.groups.filter(g=>g.age<g.duration&&live.some(e=>e._vp12.g===g));
 if(!blocked&&VP12.age>=VP12.next&&!VP12.groups.length&&enemies.filter(e=>!e.dead).length<10&&eBullets.length<85){vp12Spawn(VP12.types[VP12.serial%VP12.types.length]);VP12.next=VP12.age+[24,20,17,14][vp12Tier()];}
 for(const e of live){const {g,q}=e._vp12;vp12Move(e,dt);if(blocked){if(bossActive||subBossActive||warnT>0){e.dead=true;vp12Log('transition-clear',{stage:run.stage});}continue;}
  if(g.type==='kamikaze'){const warm=1.25+.18*(3-g.tier);if(g.age<warm)combatWarningTick(e,'vp12-charge',g.age,warm);continue;}
  const {tell,release,gap}=vp12FireTiming(g,q);
  if(g.age>=release-tell&&g.age<release)combatWarningTick(e,'vp12-pass',g.age-(release-tell),tell);
  const max=g.type==='barrel'?2:g.tier===3?2:1;
  if(q.shot<max&&g.age>=release+q.shot*gap&&e.y>PLAY.y+10&&e.y<PLAY.y+PLAY.h-22){const aim=Math.atan2(g.target.y-e.y,g.target.x-e.x),n=g.type==='barrel'?1:g.tier>=2?3:1;
   for(let i=0;i<n;i++){eShoot(e.x,e.y,g.type==='barrel'?Math.PI/2:aim+(i-(n-1)/2)*.18,g.type==='barrel'?2:2.8+g.tier*.25,g.type==='barrel'?'flare':'missile');const b=eBullets[eBullets.length-1];if(b){b._vp12=true;b._vp12Group=g.id;if(g.type==='barrel'){b._vpBomb=true;b.w=b.h=16;}}}
   q.shot++;Audio.SFX.enemyMissile?.();vp12Log(g.type==='barrel'?'bomb-drop':'volley',{stage:run.stage,type:g.type});}
 }return r;
};
drawEnemy=function(e){if(!e._vp12)return VP12.base.draw.apply(this,arguments);if(e.dead||e._dyingT!=null)return;const {g,q}=e._vp12,A=VP12_ART[g.stage];if(!A||!XART.rdy(A.key))return;
 const heading=(Math.round(((q.angle+TAU)%TAU)/TAU*8)%8),roll=g.type==='barrel'&&q.side<0&&A.rollKey&&XART.rdy(A.rollKey),frame=roll?Math.floor(g.age*10)%8:heading,key=roll?A.rollKey:A.key,size=64*q.scale;
 if(typeof air13DrawFlight!=="function"||!air13DrawFlight(e,g,q)){drawUnitShadow(e.x,e.y,size,size,.24,e);const im=e.flash>0?xartTint(key,hitFlashColor(e,'#ffffff'),.8):XART.get(key);
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,frame*96,0,96,96,e.x-size/2,e.y-size/2,size,size);ctx.restore();}
 const warm=1.25+.18*(3-g.tier),{release,tell}=vp12FireTiming(g,q);
 if(g.type==='kamikaze'&&g.age<warm){const flame='t_muz'+(Math.floor(g.age*16)%2);if(ASSETS.has(flame))ASSETS.blit(flame,e.x,e.y,28+g.age/warm*22,28+g.age/warm*22);ph8Icon(ctx,'retm_0',e.x,e.y,42);combatWarningDraw(e,{x:e.x,y:e.y,ex:g.target.x,ey:g.target.y,progress:g.age/warm,width:26,laneShape:'line'});}
 else{if(g.age>release-tell&&g.age<release)combatWarningDraw(e,{x:e.x,y:e.y,ex:g.type==='barrel'?e.x:g.target.x,ey:g.type==='barrel'?PLAY.y+PLAY.h:g.target.y,progress:(g.age-release+tell)/tell,width:18,laneShape:'line'});}
};
