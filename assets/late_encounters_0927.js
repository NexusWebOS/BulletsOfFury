"use strict";
/* Whole authored Stage 7/9 bosses; committed warnings, distinct attack turns and
   recoveries. Their existing damage routing, transformations and endings remain. */
function late27Level(){return diffKey==='furious'||diffKey==='insanity'?2:diffKey==='hard'?1:0;}
function late27Owns(b){return !!(b&&!b._scene&&((run.stage===7&&b._ship==='dualscoopdredger')||(run.stage===9&&b._ship==='tidalsovereign')));}
function late27Warm(){
  for(const row of Object.values(S9A))for(let i=0;i<8;i++)XART.rdy(row[0]+'_'+i);
  for(const key of ['cfx_stage7_warden_walk','cfx_stage7_warden_cannon','cfx_stage7_warden_rail','cfx_stage7_warden_projectiles','cfx_stage7_warden_mine'])XART.rdy(key);
}
function late27Init(b,type){
  if(b._late27&&b._late27.type===type)return b._late27;
  const n=late27Level(),home=type==='warden'?178:type==='horizon'?145:type==='dredger'?145:140;
  const A=b._late27={type,n,t:0,clock:0,index:-1,mode:'recover',warm:0,dur:1.2,shots:0,history:[],paths:[],home,
    side:1,phase:0,from:{x:b.x,y:b.y},to:{x:worldWidth()/2,y:home}};
  if(type==='dredger'||type==='tidal'){b.hp=b.maxhp=Math.ceil((type==='dredger'?1900:5000)*DIFF.eHp);b.fireCd=999;}
  late27Warm();return A;
}
function late27Book(A){
  if(A.type==='dredger')return ['sluice-crossfire','bucket-run','spore-bloom','mine-gate'];
  if(A.type==='horizon')return ['needle-relay','rift-gates','horizon-orbit','prism-sweep'];
  if(A.type==='warden')return A.phase>0?['stalk','leap','rail','minefield','chain','leap','burst']:['stalk','burst','leap','minefield','rail'];
  return ['tidal-scissors','torpedo-hunt','abyssal-gates','maelstrom-crown','hydro-sweep'];
}
function late27Set(b,mode){
  const A=b._late27,n=A.n;A.mode=mode;A.t=0;A.shots=0;A.paths=[];A.side=-A.side;
  A.from={x:b.x,y:b.y};A.target={x:player.x,y:player.y};
  A.warm=[1.05,.90,.78][n];A.live=[1.75,1.90,2.05][n];A.gap=[.32,.25,.20][n];
  A.phase=b.hp<=b.maxhp*.5?1:0;
  A.to={x:clamp(worldWidth()/2+A.side*worldWidth()*.23,b.w*.4+18,worldWidth()-b.w*.4-18),y:A.home};
  if(mode==='recover'){A.live=[1.2,.95,.78][n];A.warm=0;A.to.x=clamp(b.x,b.w*.4+18,worldWidth()-b.w*.4-18);}
  else if(mode==='stalk'){A.warm=.9;A.live=1.1;A.to={x:clamp(player.x,85,worldWidth()-85),y:Math.min(230,A.home+44)};}
  else if(mode==='leap'||mode==='bucket-run'){A.warm=[1.12,.98,.86][n];A.live=mode==='leap'?.74:1.05;A.to={x:clamp(player.x,100,worldWidth()-100),y:clamp(player.y-75,225,310)};}
  else if(mode==='minefield'||mode==='mine-gate'){A.warm=1.10;A.live=.20;}
  A.dur=A.warm+A.live;A.next=0;
  if(mode==='leap'||mode==='bucket-run'){
    // This circle marks the actual landing feet, from the beginning of the windup.
    A.landing=groundTargetingSpawn({kind:'missile',x:A.to.x,y:A.to.y+65,owner:b,warn:A.dur,active:.34,radius:48,size:105,track:false,lane:false,
      sound:'wardenRail',shake:5,onImpact:q=>combatAtlasFx(q.x,q.y,'cfx_stage7_warden_projectiles',4,3,8,4,{life:.34,wpx:110,hpx:80})});
    A.landing._late27=true;
  }
  A.history.push({mode,time:A.clock,phase:A.phase});if(A.history.length>60)A.history.shift();
  if(mode!=='recover')combatWarningTick(b,'late27-'+A.type,0,A.warm,true);
  late27Paths(b);
}
function late27Mount(b,slot){
  if(b._s9rift){const w=b._s9rift.core;return{x:w.x+(slot==='L'?-1:slot==='R'?1:0)*w.w*.24,y:w.y+w.h*.23};}
  return shipBossMount(b,slot);
}
function late27Path(b,slot,angle,width){const p=late27Mount(b,slot);return {slot,x:p.x,y:p.y,a:angle,ex:p.x+Math.cos(angle)*760,ey:p.y+Math.sin(angle)*760,width:width||22};}
function late27Paths(b){
  const A=b._late27,m=A.mode,C=late27Mount(b,'C'),aim=p=>Math.atan2(A.target.y-p.y,A.target.x-p.x);
  A.aim=aim(C);A.paths=[];const add=(s,a,w)=>A.paths.push(late27Path(b,s,a,w));
  if(m==='recover')return;
  if(m==='leap'||m==='bucket-run'||m==='stalk'){A.paths=[{x:b.x,y:b.y,ex:A.to.x,ey:A.to.y,width:m==='stalk'?110:125}];return;}
  if(m==='minefield'||m==='mine-gate'||m==='rift-gates'||m==='abyssal-gates'){
    const cols=7,gap=clamp(Math.floor(A.target.x/worldWidth()*cols),1,cols-2);A.gapLane=gap;
    for(let i=0;i<cols;i++){if(Math.abs(i-gap)<(A.n===0?2:1))continue;const x=(i+.5)*worldWidth()/cols,s=i<3?'L':'R',p=late27Mount(b,s),y=VH*.60;add(s,Math.atan2(y-p.y,x-p.x),24);A.paths[A.paths.length-1].anchor={x,y};}
  }else if(m==='spore-bloom'||m==='horizon-orbit'||m==='maelstrom-crown'){
    const n=12+A.n*2;for(let i=0;i<n;i++){const a=i*TAU/n,d=Math.abs(Math.atan2(Math.sin(a-A.aim),Math.cos(a-A.aim)));if(d>.58)add('C',a,18);}
  }else if(m==='tidal-scissors'||m==='sluice-crossfire'){
    for(const s of ['L','R'])for(const o of [.05,.18,.31])add(s,Math.PI/2+(s==='L'?1:-1)*o,18);
  }else if(m==='prism-sweep'||m==='hydro-sweep'){
    for(const s of ['L','R'])for(const o of [-.32,-.16,0,.16,.32])add(s,Math.PI/2+o,18);
  }else{
    for(const s of ['L','R']){const p=late27Mount(b,s),a=aim(p);for(const o of m==='rail'?[-.24,0,.24]:[-.07,0,.07])add(s,a+o,m==='rail'?24:16);}
  }
}
function late27Shot(b,p,kind,speed){
  const A=b._late27,port=late27Mount(b,p.slot||'C');let q;
  if(A.type==='warden')q=s7WardenShot(b,p.slot||'C',p.a,speed,kind,{silent:A.shots>0});
  else if(A.type==='dredger')q=s7BossShot(port.x,port.y,p.a,speed,kind,{silent:A.shots>0,szMul:kind==='s7spore'?.55:1,w:kind==='s7spore'?24:undefined,h:kind==='s7spore'?24:undefined});
  else if(S9A[kind])q=s9aShot(port.x,port.y,p.a,speed,kind,{silent:A.shots>0});
  else q=spaceBossShot(port.x,port.y,p.a,speed,kind,{silent:A.shots>0});
  if(q){q._late27=true;if(kind==='tidaltorp'){q._shootable=true;q.hp=1;q._energyOrdnance=true;q._accel=.011;q._maxspd=4.8;}}
  navalFlash(null,port,.72,BPFX_MUZZLE_LASER,{n:8,hpx:40,life:.13,follow:()=>!b.dead?late27Mount(b,p.slot||'C'):null});
}
function late27Emit(b){
  const A=b._late27,m=A.mode,wave=A.shots++,paths=A.paths,n=A.n;
  if(typeof combatAudio0927==='function')combatAudio0927(b,A.type==='dredger'?'combatToxic0927':/sweep|rail/.test(m)?'combatBeam0927':'combatOrb0927',.24);
  if(m==='minefield'||m==='mine-gate'){
    if(wave)return;for(const p of paths){const q=s7WardenShot(b,p.slot,p.a,1.5,'mine',{silent:true,targetX:p.anchor.x,targetY:p.anchor.y});
      q._late27=true;q._energyOrdnance=true;q._wardenTravel={x:q.x,y:q.y,dur:1.1};}return;
  }
  if(m==='spore-bloom'||m==='horizon-orbit'||m==='maelstrom-crown'){
    if(wave>1+A.phase)return;for(const p of paths)late27Shot(b,p,A.type==='dredger'?'s7spore':m==='horizon-orbit'?'warporb':'tidalcrown',2.0+n*.20);return;
  }
  if(m==='rift-gates'||m==='abyssal-gates'){
    if(wave>1+A.phase)return;for(const p of paths)late27Shot(b,p,m==='rift-gates'?'warpshard':'tidaltorp',m==='rift-gates'?3.1:1.9);return;
  }
  if(m==='sluice-crossfire'||m==='tidal-scissors'){
    const side=wave%2?'R':'L';for(const p of paths.filter(p=>p.slot===side))late27Shot(b,p,m==='sluice-crossfire'?'s7acid':'tidalcut',2.65+n*.24);return;
  }
  if(m==='prism-sweep'||m==='hydro-sweep'){
    const i=wave%5;for(const side of ['L','R']){const p=paths.filter(p=>p.slot===side)[A.side>0?i:4-i];late27Shot(b,p,m==='prism-sweep'?'warplance':'tidalcrown',3.8+n*.25);}return;
  }
  const slot=wave%2?'R':'L',rows=paths.filter(p=>p.slot===slot);
  for(const p of rows)late27Shot(b,p,m==='rail'?'rail':m==='chain'||m==='burst'?'shell':m==='torpedo-hunt'?'tidaltorp':'s9needle',m==='torpedo-hunt'?1.8:3.8+n*.3);
}
function late27Step(b,dt){
  const A=b._late27;
  if(!A.engaged){A.engaged=true;if(A.mode==='recover'){A.from={x:b.x,y:b.y};A.t=0;}}
  A.t+=dt;A.clock+=dt;b.fireCd=999;
  if(A.mode==='recover'){
    const p=clamp(A.t/A.dur,0,1),e=p*p*(3-2*p);b.x=lerp(A.from.x,A.to.x,e);b.y=lerp(A.from.y,A.home,e);
    if(A.t>=A.dur){const book=late27Book(A);late27Set(b,book[(++A.index)%book.length]);}
  }else{
    combatWarningTick(b,'late27-'+A.type,Math.min(A.t,A.warm),A.warm);
    if(A.t>=A.warm){
      if(['leap','bucket-run','stalk'].includes(A.mode)){
        const p=clamp((A.t-A.warm)/A.live,0,1),e=p*p*(3-2*p);
        if(A.mode==='stalk'&&b._s7warden){
          const S=b._s7warden,dx=A.to.x-b.x,dy=A.to.y-b.y,d=Math.hypot(dx,dy);S.dir=dx>0?1:-1;
          if(d>1){const x=b.x;s7WardenCrawl(b,dt,125);const step=Math.min(d,Math.abs(b.x-x));b.x=x+dx/d*step;b.y+=dy/d*step;}
        }else{b.x=lerp(A.from.x,A.to.x,e);b.y=lerp(A.from.y,A.to.y,e)-(A.mode==='leap'?Math.sin(p*Math.PI)*76:0);}
        if(p>=1&&A.shots===0){A.shots++;if(A.mode!=='stalk')s7WardenMechSound('foot');}
      }else if(A.t-A.warm>=A.next){A.next+=['spore-bloom','horizon-orbit','maelstrom-crown','rift-gates','abyssal-gates'].includes(A.mode)?1.0:A.gap;late27Emit(b);}
    }
    if(A.t>=A.dur+.18)late27Set(b,'recover');
  }
  b._drawY=b.y;
}
function late27Tick(b,dt){
  if(!late27Owns(b)||b.dead||b.enter)return false;
  const A=late27Init(b,b._ship==='dualscoopdredger'?'dredger':'tidal');
  late27Step(b,dt);return true;
}
function late27Warden(b,dt){
  if(b._scene)return false;
  const A=late27Init(b,'warden'),S=b._s7warden;
  if(S.final.phase!=='fight')return false;
  if(A.suspended){A.suspended=false;late27Set(b,'recover');}
  S.mode='late27';S.noHit=false;S.bodyDrop=0;S.travel=0;
  late27Step(b,dt);return true;
}
function late27Suspend(b){const A=b._late27;if(A){A.suspended=true;if(A.landing)A.landing.dead=true;}}
function late27Horizon(b,dt){
  if(b._scene)return false;const F=b._s9rift,w=F.core;F.t+=dt;
  const A=late27Init(b,'horizon');
  // Keep the fully scaled spawn pool; the old first-tick reset discarded almost half its HP.
  if(w.flash>0)w.flash=Math.max(0,w.flash-dt);
  if(F.t<1.65){const p=clamp(F.t/1.65,0,1);w.x=b.x=worldWidth()/2;w.y=b.y=lerp(-145,A.home,p*p*(3-2*p));b.enter=true;return true;}
  b.enter=false;b.hp=w.hp;late27Step(b,dt);w.x=b.x;w.y=b.y;w.spin=0;return true;
}
function late27Twins(b,dt){
  const F=b._s9fusion;if(!F||F.phase!=='twins'||b._scene)return false;
  const D=F._late27||(F._late27={t:0,index:0,turn:null,rest:1.0,history:[]});D.t+=dt;F.t+=dt;
  const p=clamp(F.t/1.65,0,1);b.enter=p<1;
  for(const w of [F.left,F.right]){w.flash=Math.max(0,w.flash-dt);w.spin=0;w.y=lerp(-130,135,p*p*(3-2*p));w.x=worldWidth()*(w.side==='L'?.30:.70);}
  b.x=worldWidth()/2;b.y=135;b.hp=F.left.hp+F.right.hp;
  if(b.enter)return true;
  if(D.turn){const w=D.turn;if(w.disabled){w._s9VolleyWarn=null;D.turn=null;D.rest=.8;}
    else if(s9FusionWardenWarningTick(b,w,dt)){D.turn=null;D.rest=[.9,.70,.52][late27Level()];}return true;}
  D.rest-=dt;if(D.rest>0)return true;
  const alive=[F.left,F.right].filter(w=>!w.disabled);if(!alive.length)return true;
  const w=alive[D.index%alive.length],phase=D.index++*.75;
  D.history.push(w.side);if(D.history.length>30)D.history.shift();
  s9FusionWardenWarningStart(b,w,phase,'late27-sentinel-'+w.side);w._s9VolleyWarn.warm=[1.02,.88,.76][late27Level()];D.turn=w;
  return true;
}
function late27Draw(front){
  for(const b of [boss,subBoss]){
    const A=b&&b._late27;if(!A||b.dead||b.enter||A.mode==='recover'||A.t>=A.warm||A.suspended)continue;
    const k=clamp(A.t/A.warm,0,1);
    if(!front)for(const p of A.paths)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:p.width,fieldOnly:true});
    else combatWarningDraw(b,{x:b.x,y:b.y,ex:A.target.x,ey:A.target.y,progress:k,alertOnly:true,alertX:b.x,alertY:Math.max(65,b.y-b.h*.4)});
  }
}
