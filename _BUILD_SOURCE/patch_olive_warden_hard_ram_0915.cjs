const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const file=path.join(root,'assets','game.js');
const backup=path.join(root,'_shots','backups','game_pre_olive_warden_hard_ram_0915.js');
let s=fs.readFileSync(file,'utf8');
if(s.includes('\r\n'))throw new Error('assets/game.js must remain LF-only');
fs.mkdirSync(path.dirname(backup),{recursive:true});
if(!fs.existsSync(backup))fs.copyFileSync(file,backup);
function rep(from,to,label){const n=s.split(from).length-1;if(n!==1)throw new Error(label+' expected exactly once, found '+n);s=s.replace(from,to);}
function repBetween(start,end,to,label){const a=s.indexOf(start),b=s.indexOf(end,a+start.length);if(a<0||b<0||s.indexOf(start,a+1)>=0)throw new Error(label+' boundaries are not unique');s=s.slice(0,a)+to+s.slice(b);}

rep(
  "    coreSpreadShots:0,coreSpreadLast:null};\n",
  "    coreSpreadShots:0,coreSpreadLast:null,miniHard:null,miniRamCount:0,miniHardLog:[]};\n",
  'Stage4 mini hard state');

const director=`function stage4MiniHardSet(b,mode){
  const S=b&&b._s4war;if(!S||!S.mini)return false;
  const W=worldWidth(),mid=W*.5,amp=Math.min(94,Math.max(42,W*.5-b.w*.60));
  stage4WarfareSetMode(b,mode);
  const H=S.miniHard||(S.miniHard={dir:1,lane:mid,locked:false,speed:0,fromX:b.x,fromY:b.y,log:[]});
  H.fromX=b.x;H.fromY=b.y;H.amp=amp;H.mid=mid;H.homeY=S.homeY;
  if(mode==='hardCircle'){
    H.dir=-H.dir;H.startA=Math.atan2((b.y-S.homeY)/38,(b.x-mid)/amp);H.log.push({mode:mode,t:b.t||0});
  }else if(mode==='hardGlide'){
    H.toX=H.dir>0?W-b.w*.55:b.w*.55;H.log.push({mode:mode,t:b.t||0});
  }else if(mode==='hardWarn'){
    H.lane=clamp(player.x,b.w*.50,W-b.w*.50);H.locked=false;H.log.push({mode:mode,t:b.t||0});
    stageRevisionCue(b,'wardenRackCharge',0);combatWarningTick(b,'olive-warden-hard-ram',0,1.20,true);
  }else if(mode==='hardRam'){
    H.speed=210;b.x=H.lane;b.y=S.homeY;S.miniRamCount++;H.log.push({mode:mode,lane:H.lane,t:b.t||0});
    stageRevisionCue(b,'sovereignDive',0);shake=Math.max(shake,7);
  }else if(mode==='hardReturn'){
    b._s4MiniSafe=true;H.p0={x:b.x,y:b.y};H.side=H.lane<mid?W+b.w*.58:-b.w*.58;
    H.p1={x:H.side,y:VH*.78};H.p2={x:H.side,y:S.homeY-126};H.p3={x:mid,y:S.homeY};
    H.log.push({mode:mode,t:b.t||0});
  }
  S.miniHardLog=H.log;return true;
}
function stage4MiniHardBezier(a,b,c,d,t){const u=1-t;return u*u*u*a+3*u*u*t*b+3*u*t*t*c+t*t*t*d;}
function stage4MiniHardTick(b,dt,phase){
  const S=b._s4war,H=S.miniHard,W=worldWidth(),mid=W*.5,furious=typeof diffKey!=='undefined'&&diffKey==='furious';
  if(!H)return false;S.poseRot=0;S.scale=1;b._animKey=null;b.fireCd=999;
  if(S.mode==='hardCircle'){
    const dur=furious?1.16:1.34,q=clamp(S.t/dur,0,1),a=H.startA+H.dir*TAU*q;
    b.x=mid+Math.cos(a)*H.amp;b.y=S.homeY+Math.sin(a)*38;
    while(S.shot<=S.t){S.shot+=furious?.145:.18;const slot=(S.wave&1)?'L':'R',off=(S.wave&3)<2?-.20:.20;
      stage4MiniMachine(b,slot,Math.PI/2+off,5.45+phase*.22);stage4WarfareMuzzle(b,slot,'mg',.68,.10);stageRevisionCue(b,'wardenGun',.11,.86);S.wave++;}
    if(q>=1)stage4MiniHardSet(b,'hardGlide');
  }else if(S.mode==='hardGlide'){
    const dur=furious?.86:1.02,q=clamp(S.t/dur,0,1),ease=q*q*(3-2*q);
    b.x=lerp(H.fromX,H.toX,ease);b.y=lerp(H.fromY,S.homeY,ease);
    while(S.shot<=S.t){S.shot+=furious?.085:.10;stage4MiniCenter(b);S.wave++;}
    if(q>=1)stage4MiniHardSet(b,'hardWarn');
  }else if(S.mode==='hardWarn'){
    const dur=1.20,lock=.72,q=clamp(S.t/dur,0,1);
    if(!H.locked&&S.t<lock)H.lane=clamp(player.x,b.w*.50,W-b.w*.50);
    if(!H.locked&&S.t>=lock){H.locked=true;H.log.push({mode:'hardLock',lane:H.lane,t:b.t||0});stageRevisionCue(b,'sovereignDive',0,.88);}
    b.x+=(H.lane-b.x)*Math.min(1,dt*8);b.y+=(S.homeY-b.y)*Math.min(1,dt*7);
    S.scale=1+q*.026+Math.sin(S.t*34)*q*.009;combatWarningTick(b,'olive-warden-hard-ram',S.t,dur,true);
    if(S.t>=.78)shake=Math.max(shake,2+Math.floor((S.t-.78)/.12));
    if(S.t>=dur)stage4MiniHardSet(b,'hardRam');
  }else if(S.mode==='hardRam'){
    H.speed=Math.min(furious?820:740,H.speed+(furious?760:660)*dt);b.x=H.lane;b.y+=H.speed*dt;S.scale=1.025;
    if(b.y>VH+b.h*.68)stage4MiniHardSet(b,'hardReturn');
  }else if(S.mode==='hardReturn'){
    const dur=furious?1.42:1.64,q=clamp(S.t/dur,0,1),ease=q*q*(3-2*q);
    b.x=stage4MiniHardBezier(H.p0.x,H.p1.x,H.p2.x,H.p3.x,ease);
    b.y=stage4MiniHardBezier(H.p0.y,H.p1.y,H.p2.y,H.p3.y,ease);S.scale=.92+.08*q;
    if(q>=1){b.x=mid;b.y=S.homeY;b._s4MiniSafe=false;stage4WarfareSetMode(b,'burst');}
  }else return false;
  b._drawY=b.y;return true;
}
function stage4MiniHardWarningDraw(b){
  const S=b&&b._s4war,H=S&&S.miniHard;if(!S||!S.mini||S.mode!=='hardWarn'||!H)return false;
  const p=shipBossMount(b,'C'),q=clamp(S.t/1.20,0,1);
  combatWarningDraw(b,{x:p.x,y:p.y,ex:H.lane,ey:VH+40,progress:q,width:96});return true;
}
function stage4MiniDirector(b,dt){
  const S=b._s4war,W=worldWidth(),phase=shipBossPhase(b),hard=typeof diffKey!=='undefined'&&(diffKey==='hard'||diffKey==='furious');
  S.t+=dt*(1+phase*.10);b.fireCd=999;S.poseRot=0;S.scale=1;b._animKey=null;S.summoned=false;S.drones.length=0;
  if(/^hard/.test(S.mode))return stage4MiniHardTick(b,dt,phase);
  const amp=Math.min(68,Math.max(24,W*.5-b.w*.62));b.y+=(S.homeY-b.y)*Math.min(1,dt*5.5);
  if(S.mode==='burst'){
    b.x=W*.5+Math.sin(S.t*1.12)*amp;
    while(S.shot<=S.t){S.shot+=hard?.095:.145;const o=Math.sin(S.wave*.38)*.24;
      for(const slot of ['L','R']){stage4MiniMachine(b,slot,Math.PI/2+o+(slot==='L'?.12:-.12),5.20+phase*.20);stage4WarfareMuzzle(b,slot,'mg',.65,.10);}
      stageRevisionCue(b,'wardenGun',.12,.90);S.wave++;
    }
    if(S.t>=3.2)stage4WarfareSetMode(b,'center');
  }else if(S.mode==='center'){
    b.x+=(W*.5-b.x)*Math.min(1,dt*5);
    while(S.shot<=S.t){S.shot+=hard?.072:.11;stage4MiniCenter(b);S.wave++;}
    if(S.t>=1.45){stage4WarfareSetMode(b,'rockets');stageRevisionCue(b,'wardenRackCharge',0);}
  }else{
    b.x=W*.5+Math.sin(S.t*.65)*amp*.5;
    if(S.t>=.68&&S.event<4&&S.shot<=S.t){S.shot=S.t+.48;const a=Math.PI/2+(S.event&1?-.16:.16);
      stage4MiniRocket(b,'L',a+.12);stage4MiniRocket(b,'R',a-.12);stageRevisionCue(b,'wardenRocket',.20);S.event++;}
    if(S.t>=3.1){if(hard)stage4MiniHardSet(b,'hardCircle');else stage4WarfareSetMode(b,'burst');}
  }
  b._drawY=b.y;return true;
}
`;
repBetween('function stage4MiniDirector(b,dt){','function stage4RamStart(b){',director,'Stage4 mini director');

rep(
  "  stage4RamShadowDraw(b);\n  const fi=Math.floor((b.t||0)*22)%8,bk='s4w_drone_barrel_'+fi;\n",
  "  stage4RamShadowDraw(b);\n  stage4MiniHardWarningDraw(b);\n  const fi=Math.floor((b.t||0)*22)%8,bk='s4w_drone_barrel_'+fi;\n",
  'Stage4 Hard warning draw');

rep(
  "    if(typeof subBoss!=='undefined' && subBoss && subBossActive && !subBoss.dead && !subBoss.enter && !subBoss._jcGhost && (!subBoss._harrier||subBoss._chCollision) && (!subBoss._tempestDuo||tempestBrothersContact(subBoss,player.x,player.y)) && Math.abs(subBoss.x-player.x)<(subBoss.w/2+10) && Math.abs((subBoss._drawY||subBoss.y)-player.y)<(subBoss.h/2+10)){\n",
  "    if(typeof subBoss!=='undefined' && subBoss && subBossActive && !subBoss.dead && !subBoss.enter && !subBoss._jcGhost && !subBoss._s4MiniSafe && (!subBoss._harrier||subBoss._chCollision) && (!subBoss._tempestDuo||tempestBrothersContact(subBoss,player.x,player.y)) && Math.abs(subBoss.x-player.x)<(subBoss.w/2+10) && Math.abs((subBoss._drawY||subBoss.y)-player.y)<(subBoss.h/2+10)){\n",
  'Stage4 return contact safety');

if(s.includes('\r\n'))throw new Error('patch introduced CRLF');
fs.writeFileSync(file,s,'utf8');
console.log('patched Olive Warden Hard/Furious circle, glide, warning, ram and return');
