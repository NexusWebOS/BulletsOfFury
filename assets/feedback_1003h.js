'use strict';
/* October 3: protected Stage 6 story beats and the Hammer's orbital homecoming.
   Art inputs and exact generation prompts: _ART_SOURCES/feedback_1003h/generation.json. */
const H3_ART=['portrait_voss','portrait_nyx','portrait_rook','portrait_kaia','portrait_jace',
 'hammer_portrait','orbital_overhead_v2','earth_surface_v2','hammer_closeup','earth','orbital_aftermath'];
for(const k of H3_ART)XART._src['h3_'+k]='assets/game/shared/combat/feedback_1003h/'+k+'.png';
const H3={ending:null,release:false,demo:false,portraits:new Map(),lastMusic:null};
function h3Warm(){for(const k of H3_ART)XART.rdy('h3_'+k);for(const k of ['red','green','orange'])XART.rdy('fb2_stealth_'+k);furyShipWarm();}
const H3_PORTRAITS={voss:[24,74,519,541],nyx:[32,87,510,515],rook:[23,90,520,501],kaia:[33,108,507,492],jace:[22,83,521,515]};
function h3Portrait(key){
 if(H3.portraits.has(key))return H3.portraits.get(key);
 const r=H3_PORTRAITS[key],raw='h3_portrait_'+key;if(!r||!XART.rdy(raw))return null;
 const c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d');g.imageSmoothingEnabled=false;
 const s=248/Math.max(r[2],r[3]);g.drawImage(XART.get(raw),...r,(256-r[2]*s)/2,(256-r[3]*s)/2,r[2]*s,r[3]*s);
 c.complete=true;c.naturalWidth=c.naturalHeight=256;H3.portraits.set(key,c);return c;
}
const H3_TOUCH=XART._touch;
XART._touch=function(k){
 if(/^rr_portrait_/.test(k||''))return h3Portrait(k.slice(12));
 if(k==='fb2_hammer_avatar'||k==='fb1002_hammer_portrait')return H3_TOUCH.call(this,'h3_hammer_portrait');
 return H3_TOUCH.apply(this,arguments);
};

/* Every Stage 6 bomber path uses the approved stealth palette sheets, including
   direct/reinforcement spawns that do not receive the strike or mission tags. */
const H3_ENEMY_DRAW=drawEnemy;
drawEnemy=function(e){
 if(run.stage===6&&e&&!e.dead&&e._dyingT==null&&(e.type==='s6bomber'||e.type==='s1jetbomber_b'||e._fb2Stealth||e._mission29||e._s67Bomber)){
  const a=e._fb2Stealth||e._mission29||{},dir=a.direction||e._s6Strike?.direction||'south';
  const role=a.role||fb2MissionRole(a),s=e._s67Draw||104;
  if(role&&fb2SheetCell('fb2_stealth_'+role,FB2_DIR_FRAME[dir]??2,e.x-s/2,e.y-s/2,s,e)){e._drawW=e._drawH=s;return;}
 }
 return H3_ENEMY_DRAW.apply(this,arguments);
};

/* The source pitch sheet has unequal rows/columns. Measured opaque bounds,
   padded by three pixels at blit time, retain the entire ship in every pose. */
const H3_PITCH=[
 [[33,8,286,256],[339,52,236,196],[595,12,225,252],[850,47,270,153]],
 [[62,267,219,268],[344,303,228,213],[601,268,218,266],[876,305,218,201]],
 [[38,536,265,234],[332,555,256,197],[594,536,245,239],[852,568,265,168]],
 [[38,776,260,264],[330,829,245,198],[588,778,245,262],[851,844,268,158]],
 [[39,1044,257,291],[322,1092,262,207],[595,1045,230,290],[850,1096,270,148]]
];
const H3_REBEL_DRAW=fr27RebelDrawShip;
fr27RebelDrawShip=function(q){
 if(!(q.frSomersault&&q.evadeT>0&&q.rfHeading==null&&XART.rdy('fr27_rebel_pitch')))return H3_REBEL_DRAW.apply(this,arguments);
 const row=H3_PITCH[q.i],f=clamp(Math.floor((1-q.evadeT/.38)*4),0,3),r=row[f],scale=SHIP_DRAW_H*1.5/Math.max(...row.map(b=>Math.max(b[2],b[3]))) ;
 const sx=r[0]-3,sy=r[1]-3,cw=r[2]+6,ch=r[3]+6,w=cw*scale,h=ch*scale,im=XART.get('fr27_rebel_pitch');
 ctx.save();ctx.translate(q.x,q.y);ctx.imageSmoothingEnabled=false;ctx.globalAlpha=q.frCloak>0?.3:1;
 for(const[a,z,id]of [[0,.33,'left'],[.33,.67,null],[.67,1,'right']]){
  if(id&&fr27RebelModules(q).find(p=>p.id===id)?.hp<=0)continue;
  ctx.drawImage(im,sx+a*cw,sy,(z-a)*cw,ch,-w/2+a*w,-h/2,(z-a)*w,h);
 }
 ctx.restore();
};

function h3RebelIntro(){return state===GS.PLAY&&boss&&!boss.dead&&boss._rebels&&!boss._rebels.frIntro?.done;}
function h3Locked(){return state===GS.PLAY&&!!(fb2TalkActive()||h3RebelIntro()||H3.ending);}
function h3ClearCombat(){
 eBullets.length=0;pBullets.length=0;groundTargetingReset();polishLanes=[];bombReset();
 player._tapHeld=false;player._tapT=null;player._mgMuzT=0;player._spaceMuzzle=0;
 Input.clearTaps?.();H3.release=true;
}
const H3_HOLD=Input.hold,H3_TAP=Input.tapSeat;
Input.hold=function(seat,action){if((h3Locked()||H3.release)&&['fire','bomb','special'].includes(action))return false;return H3_HOLD.apply(this,arguments);};
Input.tapSeat=function(seat,action){if((h3Locked()||H3.release)&&['fire','bomb','special'].includes(action))return false;return H3_TAP.apply(this,arguments);};
const H3_SHOOT=pShoot,H3_BOMB=useBomb,H3_SPECIAL=startSpecial,H3_AUTO=autoFireMissiles,H3_HIT=playerHit;
pShoot=function(){if((h3Locked()||H3.release)&&!H3.demo)return;return H3_SHOOT.apply(this,arguments);};
useBomb=function(){if(h3Locked()||H3.release)return;return H3_BOMB.apply(this,arguments);};
startSpecial=function(){if(h3Locked()||H3.release)return;return H3_SPECIAL.apply(this,arguments);};
autoFireMissiles=function(){if(h3Locked()||H3.release)return;return H3_AUTO.apply(this,arguments);};
playerHit=function(){if(h3Locked())return;return H3_HIT.apply(this,arguments);};
const H3_TALK_START=fb2TalkStart;
fb2TalkStart=function(){const r=H3_TALK_START.apply(this,arguments);h3ClearCombat();return r;};
fb2TalkTick=function(dt){
 const S=fb2Talk;if(!S||S.done)return;if(!fb2TalkActive()){S.done=true;return;}
 S.age+=dt;S.t+=dt;const b=S.beats[S.i];if(!b)return fb2TalkNext();
 if(b.kind==='callisto')return fb2CallistoTick(S,b,dt);
 if(b.kind==='demo'){
  H3.demo=true;try{fb2DemoTick(S,dt);}finally{H3.demo=false;}
  // Only the scripted demonstration moves. Enemy AI and collision remain frozen.
  for(const p of pBullets){p.x+=(p.vx||0)*dt*60;p.y+=(p.vy||0)*dt*60;p.t=(p.t||0)+dt;}
  pBullets=pBullets.filter(p=>!p.dead&&p.y>-160&&p.t<4);
  return;
 }
 const full=b.text.length,n=Math.min(full,Math.floor(S.t*32));
 dialogueLetterTicks?.(b.text,S.shown,n);S.shown=n;
 const hold=/[^.\s]/.test(b.text)?Math.max(2.6,b.text.split(/\s+/).length*.16):1.6;
 if(S.t>=full/32+hold)fb2TalkNext();
};

function h3RebelLines(R){
 const alive=R.ships.filter(q=>!q.dead),pilot=_pilotKey().toUpperCase();
 const words={voss:'THE DIVISION BETRAYED EVERY ONE OF US. THERE ARE NO ORDERS LEFT WORTH FOLLOWING.',
  nyx:'THEY BUILT THIS WORLD ON OUR BONES. NOW WE TAKE BACK WHAT THEY STOLE.',
  rook:'YOUR ARMOR WILL NOT SAVE YOU. YOU KNOW WHAT MY GUNS CAN DO.',
  kaia:'YOU SHOULD HAVE STAYED OUT OF THIS. I WILL NOT MISS A SECOND TIME.',
  jace:'LAST CHANCE TO TURN BACK. WE ARE NOT GOING HOME EMPTY-HANDED.'};
 const rows=alive.map(q=>({who:q.key.toUpperCase(),text:words[q.key]}));
 rows.splice(1,0,{who:pilot,text:'WE WERE ONE UNIT ONCE. IT DOES NOT HAVE TO BE LIKE THIS. WE CAN STILL STOP THIS.'});
 rows.push({who:(alive[0]?.key||'voss').toUpperCase(),text:'GET OUT OF OUR WAY, OR BURN WITH IT.'});return rows;
}
function h3RebelTick(b,dt){
 const R=b._rebels;if(!R.rf)rf28Init(b,R);
 if(!R.h3Intro){R.h3Intro={rows:h3RebelLines(R),i:0,t:-3,shown:0,age:0};R.frIntro={t:0,beat:0,done:false};h3ClearCombat();if(s6Wing)s6Wing.line=null;R.frRadio=null;h3RebelMusic();}
 const I=R.h3Intro;I.t+=dt;I.age+=dt;R.frIntro.t=I.age;b._noHit=true;
 const line=I.rows[I.i];if(line){const n=Math.min(line.text.length,Math.floor(Math.max(0,I.t)*32));dialogueLetterTicks?.(line.text,I.shown,n);I.shown=n;
  if(I.t>line.text.length/32+2.8){I.i++;I.t=0;I.shown=0;R.frIntro.beat=I.i;}}
 const alive=R.ships.filter(q=>!q.dead),cx=camLeftX()+viewW()/2,span=Math.min(124,(viewW()-126)/2);
 const offsets=[[0,0],[-.5,-36],[.5,-36],[-1,-72],[1,-72]],ease=1-Math.pow(1-clamp(I.age/3,0,1),2);
 for(const q of alive){const o=alive.length===1?[0,0]:offsets[q.i];q.x=clamp(cx+o[0]*span+Math.sin(I.age*.65)*12,camLeftX()+54,camRightX()-54);
  q.y=lerp(-120,VH*.33+o[1],ease)+Math.sin(I.age*1.3+q.i)*3;q.mode='entry';q.t=I.age;q.evadeT=0;}
 if(I.i>=I.rows.length){R.frIntro.done=true;b._noHit=false;R.t=0;R.releaseAt=1.6;
  for(const q of alive){q.mode='fight';q.t=0;q.cd=1.6+q.i*.4;}Input.clearTaps?.();}
}
function h3Radio(who,text,shown,y){
 const key=who.toLowerCase(),rebel=!!H3_PORTRAITS[key],pw=Math.round(VW*.94),ph=Math.max(104,Math.round(VH*.23));
 dlgBox._tw={key:'h3|'+who+'|'+text,count:shown,at:performance.now(),auto:false};
 dlgBox({who,portrait:rebel?false:key,portraitKey:rebel?'rr_portrait_'+key:undefined,full:text,shown:text.slice(0,shown),forceShown:true,fade:1,
  tint:dialogueNameColor(who,'#cfd6e6'),pw,ph,x:(VW-pw)/2,y:y??VH*.58});
}
function h3RebelMusic(){if(Audio._h3RebelMusic!==boss){Audio._h3RebelMusic=boss;Audio.startMusic('stagex');}}
const H3_MUSIC=Audio.startMusic;
Audio.startMusic=function(name){
 if(state===GS.PLAY&&boss&&!boss.dead&&boss._rebels&&/^(boss\d+(mus)?|stagex|rival)$/.test(name))name='stagex';
 H3.lastMusic=name;return H3_MUSIC.call(this,name);
};
const H3_REBEL_TICK=rebelSquadTick;
rebelSquadTick=function(b,dt){if(!b._rebels.frIntro?.done)return h3RebelTick(b,dt);h3RebelMusic();return H3_REBEL_TICK.apply(this,arguments);};

const H3_ARMOR=fr27BeginArmor;
fr27BeginArmor=function(b){const a=H3_ARMOR.apply(this,arguments);
 if(a&&run.stage===5&&diffKey==='furious'&&fb1002NormalHammer(b)){a.max=Math.round(a.max*.75);a.hp=a.max;a.h3Reduced=true;}return a;};
const H3_RESTORE=fr27Restore;
fr27Restore=function(b){const r=H3_RESTORE.apply(this,arguments),a=fr27Armor(b),h=b._hammer;
 if(a?.h3Reduced&&h.recovery?.armor)h.recovery.amount*=.75;return r;};

const H3_CHEERS=[
 ['COLE','THAT IS HOW FURY GETS IT DONE! BRING IT HOME.'],['DECKER','DIRECT HIT! YOUR REENTRY COURSE IS CLEAR.'],
 ['AXEL','YES! YOU JUST LIT UP THE WHOLE SKY!'],['LIZZIE','BEAUTIFUL SHOT! WELCOME BACK TO EARTH!'],
 ['FALVA','WE SAW THAT FROM DOWN HERE. YOU DID IT!'],['YURI','HA! EVEN I FELT THAT ONE. WELCOME HOME!'],
 ['FREEZER','ORBIT IS CLEAR. COME ON DOWN, HERO.'],['MAVERICK','NICE FLYING. WE HAVE YOUR SIX ALL THE WAY HOME.'],
 ['JUGGERNAUT','THAT WAS ONE HELL OF A HIT! WELCOME HOME!']
];
function h3Cheer(e){const [who,text]=H3_CHEERS[e.cheer];return [who,who.toLowerCase()===_pilotKey()?'THANKS, EVERYONE. I AM COMING HOME.':text];}
function h3EndingStart(b){
 H3.ending={boss:b,t:0,events:new Set(),cheer:0,cheerT:0,shown:0,descent:0,phase:'overhead',scroll:mapScroll};
 h3Warm();h3ClearCombat();BOFCinematicDirector.cancel();story=null;special=null;thunderStorm=null;
 Audio.startMusic('cinematics');whiteBlast=0;shake=0;
}
const H3_BOSS_DIE=bossDie;
bossDie=function(){const b=boss,ending=state===GS.PLAY&&run.stage===5&&fb1002NormalHammer(b)&&!b.dead;
 const r=H3_BOSS_DIE.apply(this,arguments);if(ending&&b.dead)h3EndingStart(b);return r;};
function h3EndingTick(dt){
 const e=H3.ending;if(!e)return;const ready=H3_ART.slice(5).every(k=>XART.rdy('h3_'+k))&&furyShipReady();
 if(!ready)return;e.t+=dt;stageEnding=0;whiteBlast=0;shake=0;
 const cue=(id,at,sfx)=>{if(e.t>=at&&!e.events.has(id)){e.events.add(id);Audio.SFX[sfx]?.();}};
 cue('missile',.4,'missile');cue('impact',2.4,'expBig');cue('orbit',5.8,'expBig');cue('shock',12.7,'bossRoar');cue('head-blast',14.1,'expBig');
 if(e.t<5)e.phase='overhead';else if(e.t<9.5)e.phase='surface';else if(e.t<17.5)e.phase='face';else if(e.t<23.5)e.phase='aftermath';
 else if(e.cheer<H3_CHEERS.length){
  e.phase='welcome';e.cheerT+=dt;const line=h3Cheer(e)[1],n=Math.min(line.length,Math.floor(e.cheerT*34));dialogueLetterTicks?.(line,e.shown,n);e.shown=n;
  if(e.cheerT>=line.length/34+1.8){e.cheer++;e.cheerT=0;e.shown=0;}
 }else{
  e.phase='descent';e.descent+=dt;
  // The same authored Furyship used by gameplay shrinks into the planet.
  const u=clamp(e.descent/8,0,1);_stage5SpaceScroll+=dt*90*(1-u)*(1-u);
  if(e.descent>=9.8){
   for(const p of powerups)if(p.kind==='forgecombo'&&!p.dead){applyPowerup(p);p.dead=true;}
   if(run.score>highScore){highScore=run.score;try{localStorage.setItem('bof_hi',highScore);}catch(_e){}}
   H3.ending=null;drawStageClear._init=false;drawStageClear._res=null;Audio.stopMusic();Input.clearTaps?.();setState(GS.STAGECLEAR);
  }
 }
}
function h3Plate(key,rect,y,h,scale){
 if(!XART.rdy(key))return;const im=XART.get(key),r=rect||[0,0,im.width,im.height],s=Math.min(VW/r[2],h/r[3])*(scale||1);
 ctx.drawImage(im,...r,VW/2-r[2]*s/2,y+(h-r[3]*s)/2,r[2]*s,r[3]*s);
}
/* One fixed image and fixed draw rectangle for the entire six-second hold.
   The only animated property is saturation: color -> monochrome, no camera drift. */
function h3AftermathDraw(g,x,y,w,h,t){
 if(!XART.rdy('h3_orbital_aftermath'))return false;
 const u=clamp((t-1.25)/3.25,0,1),fade=u*u*(3-2*u);
 g.save();g.filter='grayscale('+fade+')';g.imageSmoothingEnabled=false;
 g.drawImage(XART.get('h3_orbital_aftermath'),x,y,w,h);g.restore();return true;
}
function h3EndingDraw(){
 const e=H3.ending;if(!e)return;ctx.save();worldXformEscape();ctx.fillStyle='#000';ctx.fillRect(0,0,VW,VH);ctx.imageSmoothingEnabled=false;
 if(e.phase==='overhead'||e.phase==='surface'){
  const phaseT=e.phase==='overhead'?e.t:e.t-5;
  h3Plate('h3_'+(e.phase==='overhead'?'orbital_overhead_v2':'earth_surface_v2'),null,0,VH,1+Math.min(.035,phaseT*.007));
 }else if(e.phase==='face'){
  const t=e.t-9.5,im=XART.get('h3_hammer_closeup'),f=t<1.6?0:t<3.2?1:t<4.6?2:3;
  if(t<6.8){ctx.save();ctx.globalAlpha=t>5.6?clamp((6.8-t)/1.2,0,1):1;
   h3Plate('h3_hammer_closeup',[(f%2)*im.width/2,Math.floor(f/2)*im.height/2,im.width/2,im.height/2],0,VH,1);ctx.restore();}
  if(t>=4.6){
   for(let n=0;n<9;n++){const age=t-4.6-n*.13;if(age<0||age>1.4)continue;
    const x=VW*(.25+(n%3)*.25),y=VH*(.35+Math.floor(n/3)*.15),size=Math.min(VW,VH)*.75;
    fb1002Cell('electrical',Math.min(15,Math.floor(age/1.4*16)),x,y,size,size,null,0,1);
    efxFrame('efx_burst_fire',Math.min(7,Math.floor(age/1.4*8)),x-size/2,y-size/2,size,size,1);
   }
  }
 }else if(e.phase==='aftermath'){
  const im=XART.get('h3_orbital_aftermath'),s=Math.min(VW/im.width,VH/im.height),w=im.width*s,h=im.height*s;
  h3AftermathDraw(ctx,(VW-w)/2,(VH-h)/2,w,h,e.t-17.5);
 }else{
  // Existing authored space background, then the generated Earth and CURRENT Furyship.
  ctx.save();ctx.translate(-camX,0);drawBG(0);ctx.restore();
  const u=clamp(e.descent/8,0,1),smooth=u*u*(3-2*u),planetSize=VW*(.78+.08*smooth),py=VH*.60;
  if(XART.rdy('h3_earth'))ctx.drawImage(XART.get('h3_earth'),VW/2-planetSize/2,py-planetSize/2,planetSize,planetSize);
  const size=lerp(SPACE_SHIP_SIZE*1.5,4,smooth),y=lerp(VH*.21,py+.025*VH,smooth);
  ctx.save();ctx.translate(VW/2,y);ctx.rotate(Math.PI);furyShipDrawFlight(0,0,size,_pilotKey(),{key:'base'},e.t);ctx.restore();
  if(e.phase==='welcome'&&e.cheer<H3_CHEERS.length){const [who,text]=h3Cheer(e);h3Radio(who,text,e.shown,VH*.73);}
  if(e.descent>8){ctx.fillStyle='rgba(0,0,0,'+clamp((e.descent-8)/1.6,0,1)+')';ctx.fillRect(0,0,VW,VH);}
 }
 ctx.restore();
}
const H3_UPDATE=updatePlay;
updatePlay=function(dt){
 if(H3.ending&&state===GS.PLAY){h3EndingTick(dt);return;}
 if(fb2TalkActive()){
  fb2TalkTick(dt);Input.clearTaps?.();if(fb2Talk?.done)pBullets.length=0;return;
 }
 if(h3RebelIntro()){h3RebelTick(boss,dt);Input.clearTaps?.();return;}
 if(H3.release&&[1,2].every(s=>['fire','bomb','special'].every(k=>!H3_HOLD.call(Input,s,k)))){H3.release=false;Input.clearTaps?.();}
 return H3_UPDATE.apply(this,arguments);
};
const H3_WORLD=drawWorld;
drawWorld=function(dt){
 if(H3.ending&&state===GS.PLAY)return h3EndingDraw();
 const r=H3_WORLD.apply(this,arguments);
 if(h3RebelIntro()){const i=boss._rebels.h3Intro,line=i?.rows[i.i];if(line&&i.t>=0){ctx.save();worldXformEscape();h3Radio(line.who,line.text,i.shown);ctx.restore();}}
 return r;
};
const H3_DIALOGUE=dlgBox;
dlgBox=function(o){return H3_DIALOGUE.call(this,fb2TalkActive()?Object.assign({},o,{forceShown:true}):o);};
const H3_BEGIN=beginStage;
beginStage=function(){H3.ending=null;H3.release=false;Audio._h3RebelMusic=null;h3Warm();return H3_BEGIN.apply(this,arguments);};
h3Warm();
