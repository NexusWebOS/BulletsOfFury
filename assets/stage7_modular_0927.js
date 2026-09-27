"use strict";
/* Mike's modular sewer encounters. Whole plates elsewhere remain untouched.
   Art is generated; geometry here only rigs those authored parts and their hit regions. */
const S7M_ART={body:['warden_body_open_0927.png',1,1],warden:['warden_parts.png',4,2],tank:['tank_parts.png',2,2],portal:['portal_16.png',4,4],
  explosion:['explosion_16.png',4,4],spew:['spew_16.png',4,4],orb:['toxic_orb_8.png',4,2],shield:['shield_8.png',4,2]};
const S7M_CACHE=Object.create(null);
for(const [name,row] of Object.entries(S7M_ART))XART._src['s7m_'+name]='assets/game/stage7_modular_0927/'+row[0];
function s7mWarm(){for(const k of Object.keys(S7M_ART))XART.rdy('s7m_'+k);}
function s7mOwns(b){return !!(b&&run.stage===7&&(b._ship==='sludgeemperor'||b._ship==='dualscoopdredger'));}
function s7mRank(){return diffKey==='furious'||diffKey==='insanity'?2:diffKey==='hard'?1:0;}
// The final solid floor ends 610 source pixels below the decorative void in the master.
function s7mEndScroll(){return Math.max(0,levelScrollRange()-610);}
/* Trim the genuine alpha margin, never manufacture silhouettes or key dark armor away. */
function s7mCell(name,i,trim){
  const id=name+':'+i+':'+!!trim;if(S7M_CACHE[id])return S7M_CACHE[id];
  const key='s7m_'+name;if(!XART.rdy(key))return null;const im=XART.get(key),D=S7M_ART[name];
  const cw=(im.width||im.naturalWidth)/D[1],ch=(im.height||im.naturalHeight)/D[2];
  const rect=name==='warden'?[[22,27,405,463],[447,28,283,466],[806,24,350,471],[1274,24,250,472],[75,522,205,469],[488,536,204,450],[880,556,202,385],[1188,610,330,329]][i]:[(i%D[1])*cw,Math.floor(i/D[1])*ch,cw,ch];
  const c=document.createElement('canvas');c.width=Math.ceil(rect[2]);c.height=Math.ceil(rect[3]);const g=c.getContext('2d');
  g.drawImage(im,...rect,0,0,c.width,c.height);
  if(!trim)return S7M_CACHE[id]=c;
  const p=g.getImageData(0,0,c.width,c.height).data;let l=c.width,r=0,t=c.height,bt=0;
  for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++)if(p[(y*c.width+x)*4+3]>100){l=Math.min(l,x);r=Math.max(r,x);t=Math.min(t,y);bt=Math.max(bt,y);}
  if(r<l)return null;const out=document.createElement('canvas');out.width=r-l+1;out.height=bt-t+1;out.getContext('2d').drawImage(c,l,t,out.width,out.height,0,0,out.width,out.height);
  return S7M_CACHE[id]=out;
}
function s7mBlit(name,i,x,y,w,h,rot,alpha,flash){
  const im=s7mCell(name,i,name==='warden'||name==='tank'||name==='body');if(!im)return false;
  ctx.save();ctx.translate(x,y);ctx.rotate(rot||0);ctx.globalAlpha=alpha==null?1:alpha;ctx.imageSmoothingEnabled=false;
  ctx.drawImage(im,-w/2,-h/2,w,h);
  if(flash){const id='hit:'+name+':'+i;let tint=S7M_CACHE[id];if(!tint){tint=document.createElement('canvas');tint.width=im.width;tint.height=im.height;const g=tint.getContext('2d');g.drawImage(im,0,0);g.globalCompositeOperation='source-in';g.fillStyle='#ffffff';g.fillRect(0,0,tint.width,tint.height);S7M_CACHE[id]=tint;}ctx.globalAlpha*=Math.min(.8,flash*5);ctx.drawImage(tint,-w/2,-h/2,w,h);}
  ctx.restore();return true;
}
function s7mFX(x,y,size,spew){combatAtlasFx(x,y,'s7m_'+(spew?'spew':'explosion'),4,4,0,16,{life:spew?1.1:.85,wpx:size,hpx:size});}
function s7mSound(key){const f=Audio.SFX[key]||Audio.SFX.expBig;if(f)f();}
function s7mInit(b){
  if(b._s7mod)return b._s7mod;s7mWarm();const tank=b._ship==='dualscoopdredger',n=s7mRank(),hp=DIFF.eHp;
  const M=b._s7mod={tank,n,mode:tank?'entry':'portal',t:0,clock:0,seq:0,history:[],shot:0,shotCD:0,counter:0,stun:0,drop:0,height:0,lean:0,legCharge:0,mask:0,parts:[],shieldMax:Math.ceil(420*hp),shield:Math.ceil(420*hp),core:Math.ceil((tank?900:1200)*hp),coreMax:Math.ceil((tank?900:1200)*hp)};
  const add=(id,life)=>M.parts.push({id,hp:Math.ceil(life*hp),max:Math.ceil(life*hp),flash:0,stress:0});
  if(!tank){add('frontL',540);add('frontR',540);add('rearL',400);add('rearR',400);}
  add('gunL',tank?330:360);add('gunR',tank?330:360);
  b.name=tank?'CAUSTIC SIEGE TANK':'TOXIC PORTAL WARDEN';b.w=tank?176:286;b.h=tank?200:260;b.enter=false;b.fireCd=999;
  b.x=worldWidth()/2;b.y=tank?-115:92;b.ty=tank?145:175;b._be=null;b._late27=null;
  if(!tank){b._s7FinalNoBar=true;b._s7warden.noHit=true;b._s7warden.final.phase='portalClose';}
  b.maxhp=M.coreMax+(tank?0:M.shieldMax)+M.parts.reduce((s,p)=>s+p.max,0);b.hp=b.maxhp;
  return M;
}
function s7mLive(M,prefix){return M.parts.filter(p=>p.hp>0&&p.id.startsWith(prefix));}
function s7mStage(M){return M.tank?'tank':s7mLive(M,'front').length?'front':s7mLive(M,'rear').length?'rear':M.shield>0?'shield':'core';}
function s7mVulnerable(M,p){return p.hp>0&&(!p.id.startsWith('rear')||!s7mLive(M,'front').length);}
/* The authored 680px sewer has pipes beyond this conservative central walkway.
   Footprint bounds cover the full chassis, rather than clamping its center only. */
function s7mGround(x,y,half){const W=worldWidth(),l=W*.345+half,r=W*.655-half;return {x:clamp(x,Math.min(l,r),(l+r)/2+Math.abs(r-l)/2),y:clamp(y,110,VH*.57)};}
function s7mSet(b,mode){const M=b._s7mod;M.mode=mode;M.t=0;M.shot=0;M.shotCD=0;M.from={x:b.x,y:b.y};M.target={x:player.x,y:player.y};M.aim=aimPlayer(b.x,b.y+50);M.history.push(mode);M.history=M.history.slice(-60);M.height=0;M.landing=null;
  if(typeof combatAudioState0927==='function')combatAudioState0927(b,mode);
  if(/laser|mortar|tank-charge/.test(mode)&&typeof combatAudio0927==='function')combatAudio0927(b,'bossWeaponCharge',.6);
  M.warn=[1.10,.94,.80][M.n];M.live=[1.65,1.85,2.05][M.n];
  if(mode==='jump'){M.warn=2.55;M.live=.75;M.target={x:clamp(player.x,130,worldWidth()-130),y:clamp(player.y-35,175,VH*.62)};
    M.landing=groundTargetingSpawn({kind:'missile',owner:b,x:M.target.x,y:M.target.y+55,warn:M.warn,active:.48,radius:70,size:150,track:false,shake:13,onImpact:q=>{s7mFX(q.x,q.y,190,true);s7mSound('expBig');}});M.landing._late27=true;
  }
  if(mode==='drop'||mode==='roar'||mode==='jump')s7WardenMechSound(mode==='drop'?'scream':'roar');
  if(mode==='chain'||mode==='aim'||mode==='laser'||mode==='orbs')combatWarningTick(b,'s7m-'+mode,0,M.warn,true);
}
function s7mNext(b){const M=b._s7mod,phase=s7mStage(M);let book;
  if(M.tank)book=['tank-cross','tank-mortar','tank-charge','tank-orbits'];
  else if(phase==='front')book=['chase','chain','mortar','orbs','bounce','jump'];
  else if(phase==='rear')book=['crawl','mortar','bounce','chain','orbs'];
  else if(phase==='shield')book=['orbs','mortar'];
  else book=s7mLive(M,'gun').length?['aim','mortar']:['laser','laser','orbs'];
  let next=book[M.seq++%book.length];if(['chain','aim','tank-cross'].includes(next)&&!s7mLive(M,'gun').length)next=M.tank?'tank-orbits':'orbs';
  s7mSet(b,next);
}
function s7mPose(b){const M=b._s7mod,t=M.clock,phase=s7mStage(M),parts=[],tank=M.tank;
  const add=(id,cell,x,y,w,h,a)=>parts.push({id,cell,x,y,w,h,a:a||0});
  const joint=(id,cell,x,y,w,h,a)=>add(id,cell,x-Math.sin(a)*h*.42,y+Math.cos(a)*h*.42,w,h,a);
  if(tank){
    add('body',0,0,0,176,192);const tracking=M.t>M.warn?M.aim:Math.atan2(player.y-b.y,player.x-b.x);
    for(const s of [-1,1])add(s<0?'gunL':'gunR',1,s*43,65,67,105,clamp(tracking+(M.t>M.warn?Math.sin((M.t-M.warn)*2.1+(s<0?0:Math.PI))*.20:0)-Math.PI/2,-.75,.75));
    add('core',2,0,-39,76,68);return parts;
  }
  const moving=['entry','chase','crawl','recover','bounce'].includes(M.mode),rearOpen=phase!=='front';
  for(const s of [-1,1]){
    const id=s<0?'rearL':'rearR',gait=moving?Math.sin(t*(phase==='rear'?9:13)+(s<0?Math.PI:0)):0;
    joint(id,s<0?3:4,s*65,-78,46,rearOpen?138:120,-s*(rearOpen?.55:.62)+gait*.065);
  }
  add('body',0,0,-18,168,198);
  for(const s of [-1,1]){
    let swing=0;const active=M.mode==='swipeX'||M.mode===(s<0?'swipeL':'swipeR');
    if(active)swing=Math.sin(clamp((M.t-M.warn)/.38,0,1)*Math.PI)*s*(M.mode==='swipeX'?1.32:Math.PI/4);
    const raised=['roar','jump'].includes(M.mode)?Math.sin(clamp(M.t/(M.mode==='roar'?2.4:.65),0,1)*Math.PI)*1.8:0;
    const gait=moving?Math.sin(t*(M.mode==='chase'?14:9)+(s<0?0:Math.PI))*.15:0;
    joint(s<0?'frontL':'frontR',s<0?1:2,s*65,-14,64,128,-s*.18+s*raised+swing+gait);
    add(s<0?'canL':'canR',6,s*55,-63+(['roar','mortar'].includes(M.mode)?Math.sin(t*12+s)*7:0),34,88);
    const gun=s<0?'gunL':'gunR',extension=['chain','aim'].includes(M.mode)?Math.min(1,M.t/.65)*15:0;
    const ga=M.aim+(M.t>M.warn&&['chain','aim'].includes(M.mode)?Math.sin((M.t-M.warn)*2.1+(s<0?0:Math.PI))*.20:0);
    add(gun,5,s*34,49+extension/2,34,84+extension,clamp(ga-Math.PI/2,-.68,.68));
  }
  add('mask',7,0,60-M.mask*37,47,43);return parts;
}
function s7mWorld(b,p){const M=b._s7mod,c=Math.cos(M.lean),s=Math.sin(M.lean);return{x:b.x+p.x*c-p.y*s,y:b.y+M.drop-M.height+p.x*s+p.y*c};}
function s7mAt(b,x,y){const M=b._s7mod;if(!M||['portal','entry','roar','dead','jump'].includes(M.mode))return null;
  const pose=s7mPose(b);for(const p of pose.slice().reverse()){
    const part=M.parts.find(q=>q.id===p.id);if(part&&part.hp<=0)continue;if(!part&&!['body','core','canL','canR'].includes(p.id))continue;
    const q=s7mWorld(b,p),a=p.a+M.lean,c=Math.cos(a),s=Math.sin(a),dx=(x-q.x)*c+(y-q.y)*s,dy=-(x-q.x)*s+(y-q.y)*c;
    if(Math.abs(dx)<p.w*.48&&Math.abs(dy)<p.h*.48)return part?part.id:p.id.startsWith('can')?'canister':'core';
  }return null;
}
function s7mBeamImpact(b,beam){
  for(let y=Math.min(beam.bot==null?player.y:beam.bot,b.y+180);y>=Math.max(beam.top||0,b.y-180);y-=3)
    for(const x of [beam.x,beam.x-(beam.w||4)*.4,beam.x+(beam.w||4)*.4]){const id=s7mAt(b,x,y);if(id)return{x,y,id};}
  return null;
}
function s7mSyncHP(b){const M=b._s7mod;b.hp=Math.max(1,M.core+(M.tank?0:M.shield)+M.parts.reduce((s,p)=>s+Math.max(0,p.hp),0));}
function s7mHit(b,dmg,x,y,id){const M=b._s7mod;if(!M||!Number.isFinite(dmg)||dmg<=0||['portal','entry','roar','dead','jump'].includes(M.mode))return true;
  id=id||s7mAt(b,x,y);if(!id)return true;if(id==='canister'){M.shieldFlash=.12;return true;}const phase=s7mStage(M),p=M.parts.find(p=>p.id===id);
  if(p){if(!s7mVulnerable(M,p))return true;p.hp=Math.max(0,p.hp-dmg);p.flash=.18;p.stress+=dmg;
    if(p.id.startsWith('front')&&M.mode==='chase'&&p.stress>=p.max*.16){p.stress=0;s7mSet(b,'stun');s7mSound('blocked');}
    if(p.hp<=0){const pose=s7mPose(b).find(q=>q.id===id),q=s7mWorld(b,pose);if(typeof d27ModuleRupture==='function')d27ModuleRupture(b,p,{...q,w:pose.w,h:pose.h},'green');s7mFX(q.x,q.y,110,false);s7mFX(q.x,q.y,88,true);s7mSound('expBig');if(typeof combatAudio0927==='function')combatAudio0927(b,'combatModule0927',.2);shake=Math.max(shake,7);
      if(phase==='front'&&!s7mLive(M,'front').length){groundTargetingCancel(b);s7mSet(b,'drop');}
      else if(phase==='rear'&&!s7mLive(M,'rear').length){groundTargetingCancel(b);s7mSet(b,'stun');s7mFX(b.x,b.y,160,true);}
    }
  }else if(id==='core'){
    if(M.tank){M.core=Math.max(0,M.core-dmg*(s7mLive(M,'gun').length?.42:1));M.coreFlash=.18;}
    else if(phase==='front'||phase==='rear'){M.shieldFlash=.22;s7mSound('blocked');return true;}
    else if(phase==='shield'){M.shield=Math.max(0,M.shield-dmg);M.shieldFlash=.26;if(M.counter<=0){M.counter=[.9,.72,.58][M.n];s7mVolley(b,5+M.n*2,aimPlayer(b.x,b.y),.13,2.7);}
      if(M.shield<=0){s7mFX(b.x,b.y,210,true);s7mSet(b,'stun');}}
    else{M.core=Math.max(0,M.core-dmg);M.coreFlash=.18;}
  }
  s7mSyncHP(b);if(M.core<=0){groundTargetingCancel(b);eBullets=eBullets.filter(q=>q._s7modOwner!==b);s7mSet(b,'dead');b._s7FinalNoBar=true;
    if(!M.tank){b._s7warden.final.phase='defeat';b._s7warden.noHit=true;bossDefeated=true;}
  }return true;
}
function s7mTargets(b){const M=b._s7mod;if(!M||['portal','entry','roar','jump','dead'].includes(M.mode))return [];
  const ids=M.parts.filter(p=>s7mVulnerable(M,p)).map(p=>p.id);if(M.tank||!s7mLive(M,'front').length&&!s7mLive(M,'rear').length)ids.push('core');
  return ids.map(id=>{const state=()=>{const p=s7mPose(b).find(p=>p.id===id)||(s7mPose(b).find(p=>p.id==='body')),q=s7mWorld(b,p),part=M.parts.find(p=>p.id===id);return{x:q.x,y:q.y,hp:part?part.hp:M.shield>0&&!M.tank?M.shield:M.core,dead:b.dead||M.mode==='dead'||!!(part&&!s7mVulnerable(M,part))};};
    return retinaDynamicPiece(b,id,'toxic module',state,d=>s7mHit(b,d,0,0,id),id==='core'?92:48,id==='core'?102:68);});
}
function s7mMuzzle(b,id){const M=b._s7mod;if(id==='emitter'){const q=s7mWorld(b,{x:0,y:59});return {...q,a:Math.PI/2+M.lean};}const p=s7mPose(b).find(p=>p.id===id)||s7mPose(b).find(p=>p.id==='body'||p.id==='core');const a=p.a+M.lean,q=s7mWorld(b,p);return{x:q.x-Math.sin(a)*p.h*.47,y:q.y+Math.cos(a)*p.h*.47,a:Math.PI/2+a};}
function s7mShot(b,x,y,a,speed,kind){if(kind==='laser'&&typeof combatAudio0927==='function')combatAudio0927(b,'combatBeam0927',.35);const q=eShootT(x,y,a,speed,kind==='laser'?'s7laser':kind==='gun'?'s7shard':'s7acid',{w:kind==='laser'?10:kind==='gun'?7:18,h:kind==='laser'?32:kind==='gun'?16:18,silent:true,szMul:kind==='laser'?.65:1});q._s7modOwner=b;q._noArsenal=true;q._boss=true;if(kind==='gun')q._s7modGun=true;else if(kind!=='laser')q._s7modOrb=true;return q;}
function s7mVolley(b,count,a,spread,speed){for(let i=0;i<count;i++)s7mShot(b,b.x,b.y+55,a+(i-(count-1)/2)*spread,speed);s7mSound('bossfireSludgeemperor');}
function s7mWaves(b,wave){if(typeof combatAudio0927==='function')combatAudio0927(b,'combatToxic0927',.25);for(let i=0;i<12;i++){const a=-Math.PI/2+(i+(wave&1)*.5)*TAU/12;s7mShot(b,b.x+Math.cos(a)*70,b.y+55+Math.sin(a)*45,a,2.45+b._s7mod.n*.32+wave*.13);}s7mFX(b.x,b.y+55,145,true);}
function s7mMortar(b){const M=b._s7mod,count=3+M.n,step=worldWidth()/(count+1),gap=Math.floor(Math.random()*count);for(let i=0;i<count;i++){
  if(i===gap)continue;const x=(i+1)*step,y=clamp(M.target.y+(i%2?30:-35),200,VH-84),q=groundTargetingSpawn({kind:'missile',owner:b,x,y,warn:[1.45,1.23,1.08][M.n]+i*.10,active:.72,radius:40,size:90,track:false,shake:3,onImpact:p=>s7mFX(p.x,p.y,110,true)});q._s7mMortar={x:b.x,y:b.y-25};q._late27=true;
  }s7mSound('wardenRail');
}
function s7mMove(b,tx,ty,speed,dt){const M=b._s7mod;if(M.tank){const q=s7mGround(tx,ty,88);tx=q.x;ty=q.y;}
  else {tx=clamp(tx,145,worldWidth()-145);ty=clamp(ty,120,VH*.59);}
  const dx=tx-b.x,dy=ty-b.y,d=Math.hypot(dx,dy),step=Math.min(d,speed*dt);if(d>.001){b.x+=dx/d*step;b.y+=dy/d*step;}
}
function s7mTick(b,dt){if(!s7mOwns(b))return false;const M=s7mInit(b);M.t+=dt;M.clock+=dt;M.counter=Math.max(0,M.counter-dt);M.coreFlash=Math.max(0,(M.coreFlash||0)-dt);M.shieldFlash=Math.max(0,(M.shieldFlash||0)-dt);M.shotCD-=dt;
  for(const p of M.parts)p.flash=Math.max(0,p.flash-dt);const ph=s7mStage(M),mode=M.mode;
  M.lean+=(M.tank?0:(s7mLive(M,'front').length===1?(s7mLive(M,'front')[0].id==='frontL'?-.15:.15):0)-M.lean)*Math.min(1,dt*4);
  M.drop+=((!M.tank&&ph!=='front'?25:0)-M.drop)*Math.min(1,dt*(mode==='drop'?8:3));
  if(!M.tank){b._s7warden.noHit=['portal','entry','roar','jump','dead'].includes(mode);b._s7warden.final.phase=mode==='dead'?'defeat':mode==='portal'?'portalClose':mode==='entry'?'walkIn':mode==='roar'?'roar':'fight';b._s7warden.final.t=M.t;b._s7FinalNoBar=['portal','entry','roar','dead'].includes(mode);}
  if(mode==='portal'){if(M.t>=1.4)s7mSet(b,'entry');return true;}
  if(mode==='entry'){b.y+=dt*(M.tank?75:48);if(b.y>=b.ty){b.y=b.ty;s7mSet(b,M.tank?'recover':'roar');}return true;}
  if(mode==='roar'){if(M.t>=1.3&&!M.shot){M.shot=1;shake=Math.max(shake,11);s7mFX(b.x,b.y+85,170,true);s7mSound('wardenRail');}if(M.t>=2.65)s7mSet(b,'recover');return true;}
  if(mode==='dead'){while(M.shot<12&&M.t>=M.shot*.19){const i=M.shot++;s7mFX(b.x+Math.sin(i*2.4)*66,b.y+Math.cos(i*1.8)*60,140+i*8,false);if(i%2===0)s7mFX(b.x+Math.sin(i)*70,b.y+55,135,true);s7mSound('expBig');shake=Math.max(shake,11);}
    if(M.t>3.3){if(M.tank){b.dead=true;subBossActive=false;subBossDone=true;run.score+=7000;continueRewardResolve(b,b.x,b.y,'miniboss');dropPowerup(b.x,b.y,'weapon');}else{if(!b._forgeRewardDropped){b._forgeRewardDropped=true;forgeBossDrop(b.x,b.y);run.score+=35000;}s7WardenFinishCampaign(b);}}return true;}
  if(mode==='drop'){if(M.t>.23&&!M.shot){M.shot=1;shake=Math.max(shake,15);s7mFX(b.x,b.y+80,200,true);s7mSound('expBig');}if(M.t>1.45)s7mSet(b,'recover');return true;}
  if(mode==='recover'||mode==='stun'){s7mMove(b,worldWidth()/2,M.tank?145:175,mode==='stun'?35:62,dt);if(M.t>(mode==='stun'?1.65:[1.1,.9,.75][M.n]))s7mNext(b);return true;}
  if(mode==='chase'||mode==='crawl'){
    if(Math.floor(M.t*2.5)!==M.shot){M.shot=Math.floor(M.t*2.5);M.target.x=player.x;s7WardenMechSound('foot');}
    const planted=(Math.floor(M.t*9)%2)?1.55:.45;s7mMove(b,M.target.x,Math.min(VH*.59,player.y-70),[125,148,172][M.n]*planted*(mode==='crawl'?.48:1),dt);
    if(M.t>2.7)s7mSet(b,mode==='crawl'?'bounce':'swipeL');return true;
  }
  if(mode.startsWith('swipe')){
    const side=mode==='swipeL'?-1:mode==='swipeR'?1:0;
    if(M.t<M.warn)combatWarningTick(b,'s7m-swipe',M.t,M.warn);
    if(M.t>=M.warn&&!M.shot){M.shot=1;s7mSound('hammerThrow');}
    if(M.t>=M.warn&&M.t<M.warn+.38)for(const seat of seatList())withSeat(seat,()=>{const dx=player.x-b.x,dy=player.y-(b.y+65);if(dy>-25&&dy<125&&Math.abs(dx)<145&&(side===0||dx*side>-18))playerHit('toxic claw');});
    if(M.t>M.warn+.55)s7mSet(b,mode==='swipeL'?'swipeR':mode==='swipeR'?'swipeX':'jump');return true;
  }
  if(mode==='jump'){
    if(M.t<.65){M.height=Math.sin(M.t/.65*Math.PI/2)*560;}
    else if(M.t<M.warn-.68){M.height=560;M.target.x+=clamp(player.x+Math.sin(M.t*5)*32-M.target.x,-155*dt,155*dt);M.target.y+=clamp(player.y-55-M.target.y,-110*dt,110*dt);M.target.x=clamp(M.target.x,140,worldWidth()-140);M.target.y=clamp(M.target.y,175,VH*.61);M.landing.x=M.target.x;M.landing.y=M.target.y+55;}
    else{const q=clamp((M.t-(M.warn-.68))/.68,0,1);M.height=560*(1-q*q);b.x=M.target.x;b.y=M.target.y;}
    if(M.t>=M.warn){while(M.shot<3&&M.t>=M.warn+M.shot*.28)s7mWaves(b,M.shot++);}
    if(M.t>M.warn+1.25)s7mSet(b,'recover');return true;
  }
  if(mode==='bounce'){
    const cycle=.85,u=(M.t%cycle)/cycle;M.height=Math.sin(u*Math.PI)*(ph==='rear'?32:77);s7mMove(b,M.target.x,Math.min(M.target.y-85,VH*.56),45,dt);
    if(Math.floor(M.t/cycle)>M.shot){M.shot++;s7mFX(b.x,b.y+65,125,true);shake=Math.max(shake,7);s7mVolley(b,3+M.n*2,Math.PI/2,.28,2.7);}
    if(M.t>cycle*3){M.height=0;s7mSet(b,'recover');}return true;
  }
  if(mode==='tank-charge'){if(M.t<M.warn)combatWarningTick(b,'s7m-tank-charge',M.t,M.warn);else s7mMove(b,M.target.x,Math.min(M.target.y-75,285),140+M.n*22,dt);}
  else if(mode==='mortar'||mode==='tank-mortar'){if(M.t>=M.warn&&!M.shot){M.shot=1;s7mMortar(b);}}
  else if(mode==='orbs'||mode==='tank-orbits'){
    if(M.t<M.warn)combatWarningTick(b,'s7m-'+mode,M.t,M.warn);
    else if(M.shotCD<=0&&M.shot<3){M.shotCD=.48;M.shot++;s7mVolley(b,5+M.n*2,M.aim+(M.shot-2)*.12,.18,2.65+M.n*.38);}
  }else if(['chain','aim','laser','tank-cross'].includes(mode)){
    // Open the faceplate during the tell, before the exposed emitter fires.
    if(mode==='laser')M.mask=Math.min(1,M.mask+dt*2.6);
    if(M.t<M.warn)combatWarningTick(b,'s7m-'+mode,M.t,M.warn);
    else if(M.shotCD<=0){M.shotCD=mode==='laser'?[.13,.10,.075][M.n]:[.15,.12,.09][M.n];M.shot++;
      if(mode==='laser'){const a=Math.PI/2+Math.sin((M.t-M.warn)*3.2)*.88;const q=s7mMuzzle(b,'emitter');s7mShot(b,q.x,q.y,a,6.8+M.n*.6,'laser');navalFlash(null,q,.6,'weapon_muzzle_toxic',{n:4,hpx:35,life:.12,follow:()=>s7mMuzzle(b,'emitter')});}
      else for(const p of s7mLive(M,'gun')){const q=s7mMuzzle(b,p.id);s7mShot(b,q.x,q.y,q.a,4.4+M.n*.48,'gun');navalFlash(null,q,.55,'weapon_muzzle_rotary',{n:4,hpx:28,life:.10,follow:()=>s7mMuzzle(b,p.id)});if(M.shot%3===1)s7mSound('machineGun');}
    }
  }
  if(M.t>M.warn+M.live)s7mSet(b,'recover');return true;
}
function s7mDraw(b){const M=b._s7mod||s7mInit(b);if(M.mode==='portal')return true;
  if(M.mode==='dead'&&M.t>1.3)return true;
  if(M.mode==='jump'&&M.height>330){const q=M.landing;if(q){ctx.save();ctx.globalAlpha=.12+.2*clamp(M.t/M.warn,0,1);ctx.fillStyle='#000';ctx.beginPath();ctx.ellipse(q.x,q.y,45+55*M.t/M.warn,18+22*M.t/M.warn,0,0,TAU);ctx.fill();ctx.restore();}return true;}
  for(const p of s7mPose(b)){const part=M.parts.find(q=>q.id===p.id);if(part&&part.hp<=0)continue;
    const q=s7mWorld(b,p),fl=part?part.flash:(p.id==='body'||p.id==='core'?Math.max(M.coreFlash||0,M.mode==='roar'?.07+.035*Math.sin(M.clock*24):0):0);s7mBlit(M.tank?'tank':p.id==='body'?'body':'warden',p.cell,q.x,q.y,p.w,p.h,p.a+M.lean,1,fl);
    if((p.id.startsWith('can')||p.id==='core')&&['roar','mortar','orbs','tank-mortar'].includes(M.mode))s7mBlit(M.tank?'tank':'warden',p.cell,q.x,q.y,p.w,p.h,p.a+M.lean,.14+.14*Math.sin(M.clock*19),.8);
  }
  if(!M.tank&&M.shield>0&&M.mode!=='entry'){
    const phase=s7mStage(M),strength=phase==='front'||phase==='rear'?.48:.20;
    s7mBlit('shield',Math.floor(M.clock*10)%8,b.x,b.y-10+M.drop-M.height,210,210,0,strength+(M.shieldFlash||0));
  }
  return true;
}
function s7mPortalDraw(){if(run.stage!==7)return false;s7mWarm();const b=boss,M=b&&b._s7mod;
  if(!M||M.tank||!['portal','entry','roar'].includes(M.mode))return true;
  const fi=M.mode==='portal'?Math.min(7,Math.floor(M.t*5)):M.mode==='entry'?4+Math.floor(M.clock*10)%8:12+Math.min(3,Math.floor(M.t/.30));
  if(M.mode==='roar'&&M.t>1.2)return true;s7mBlit('portal',fi,worldWidth()/2,149,240,274,0,1);return true;
}
function s7mWarnings(front){for(const b of [boss,subBoss]){const M=b&&b._s7mod;if(!M||b.dead)continue;
  const mode=M.mode,p=clamp(M.t/M.warn,0,1);if(M.landing&&!M.landing.impact&&!M.landing.dead){if(front)combatWarningDraw(b,{x:M.landing.x,y:M.landing.y,ex:M.landing.x,ey:M.landing.y,progress:p,alertOnly:true,alertX:M.landing.x,alertY:M.landing.y-58});}
  if(M.t>=M.warn||!['chain','aim','laser','orbs','swipeL','swipeR','swipeX','tank-cross','tank-charge'].includes(mode))continue;
  if(front)combatWarningDraw(b,{x:b.x,y:b.y,ex:player.x,ey:player.y,progress:p,alertOnly:true,alertX:b.x,alertY:Math.max(54,b.y-112)});
  else if(mode.startsWith('swipe'))combatWarningDraw(b,{x:b.x,y:b.y+40,ex:b.x+(mode==='swipeL'?-90:mode==='swipeR'?90:0),ey:b.y+178,progress:p,width:90,fieldOnly:true});
  else if(mode==='laser'){
    const q=s7mMuzzle(b,'emitter');
    // One authored cone covers the sweep envelope, rooted at the actual emitter.
    combatWarningDraw(b,{x:q.x,y:q.y,ex:q.x,ey:VH,progress:p,width:Math.tan(.88)*Math.max(1,VH-q.y),alpha:.52,fieldOnly:true});
  }else if(['chain','aim','tank-cross'].includes(mode)){
    for(const gun of s7mLive(M,'gun')){const q=s7mMuzzle(b,gun.id);combatWarningDraw(b,{x:q.x,y:q.y,ex:q.x+Math.cos(q.a)*600,ey:q.y+Math.sin(q.a)*600,progress:p,width:35,fieldOnly:true});}
  }else {const q={x:b.x,y:b.y+55};combatWarningDraw(b,{x:q.x,y:q.y,ex:q.x+Math.cos(M.aim)*600,ey:q.y+Math.sin(M.aim)*600,progress:p,width:mode==='tank-charge'?150:35,fieldOnly:true});}
  if(!front&&mode==='aim')groundTargetReticleDraw(M.target.x,M.target.y,88,p,1);
 }
 if(!front)for(const q of groundTargetingFx){if(!q._s7mMortar||q.impact||q.dead)continue;const u=clamp(q.t/q.warn,0,1),from=q._s7mMortar;s7mBlit('orb',Math.floor(q.t*12)%8,lerp(from.x,q.x,u),lerp(from.y,q.y,u)-Math.sin(u*Math.PI)*155,28,28,0,1);}
}
