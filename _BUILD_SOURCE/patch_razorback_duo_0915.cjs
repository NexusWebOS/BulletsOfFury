const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p,'utf8');
if(s.includes('\r\n'))throw new Error('game.js must remain LF');
function one(a,b,label){const n=s.split(a).length-1;if(n!==1)throw new Error(label+' matches '+n);s=s.replace(a,b);}
one("function razorbackPartAt(b,x,y){",`/* Hard mode fields two complete tanks inside the one campaign miniboss slot. Each actor keeps its
   own authored rig, phase pools, projectiles and locks; the controller owns only the combined gauge,
   broad-phase bounds and one encounter completion. */
function razorbackPairInit(b){
  if(!b||!b._rzb||typeof diffKey==='undefined'||diffKey!=='hard')return false;
  const W=worldWidth(),L=camLeftX(),span=camRightX()-L,single=b.maxhp,actors=[];
  for(const side of [-1,1]){
    const p={kind:'razorback',x:W/2,y:-150,ty:VH*.27,t:0,enter:false,hp:single,maxhp:single,w:b.w,h:b.h,
      flash:0,dead:false,dying:0,fireCd:999,drift:0,atkPhase:0,phaseT:1.2,sub:true,name:'RAZORBACK'};
    razorbackInit(p);p.hp=p.maxhp=single;p.enter=false;p._pairController=b;p._rzb.pairSide=side;
    p._rzb.homeX=L+span*(side<0 ? .28 : .72);p._rzb.tgt.x=p._rzb.homeX;p.x=p._rzb.homeX;
    /* Offset the attack books by one entry: two tanks fight together without stacking the same
       release on the same frame. */
    p._rzb.attackOffset=side<0?0:1;p._rzb.idx=-1+p._rzb.attackOffset;actors.push(p);
  }
  delete b._rzb;b._rzbPair={actors:actors,singleMax:single,cleared:false};b.name='RAZORBACK DUO';
  b.hp=b.maxhp=single*2;b.enter=false;b.fireCd=999;razorbackPairSync(b);return true;
}
function razorbackPairSync(b){
  const P=b&&b._rzbPair;if(!P)return;const shown=P.actors.filter(p=>!p._rzbGone),live=P.actors.filter(p=>!p.dead);
  b.hp=live.reduce((n,p)=>n+Math.max(0,p.hp),0);
  const boxes=shown.length?shown:P.actors;if(!boxes.length)return;
  const l=Math.min(...boxes.map(p=>p.x-p.w*.5)),r=Math.max(...boxes.map(p=>p.x+p.w*.5)),
        t=Math.min(...boxes.map(p=>p.y-p.h*.5)),bot=Math.max(...boxes.map(p=>p.y+p.h*.5));
  b.x=(l+r)*.5;b.y=(t+bot)*.5;b._drawY=b.y;b.w=b._drawW=r-l;b.h=b._drawH=bot-t;
}
function razorbackPairPartAt(b,x,y){
  if(!b||b.dead||!b._rzbPair)return null;
  for(let i=b._rzbPair.actors.length-1;i>=0;i--){const p=b._rzbPair.actors[i],part=razorbackPartAt(p,x,y);if(part)return i+':'+part;}
  return null;
}
function razorbackPairBeamHit(b,beam){
  if(!b||b.dead||!b._rzbPair)return null;let best=null;
  for(let i=0;i<b._rzbPair.actors.length;i++){const p=b._rzbPair.actors[i],q=razorbackBeamHit(p,beam);if(q&&(!best||q.entry>best.entry))best=Object.assign({},q,{actor:i});}
  return best;
}
function razorbackPairContact(b,x,y){
  return !!(b&&b._rzbPair&&b._rzbPair.actors.some(p=>!p.dead&&!p._rzbGone&&Math.abs(p.x-x)<p.w*.5+10&&Math.abs(p.y-y)<p.h*.5+10));
}
function razorbackPairHit(b,dmg,hx,hy){
  const P=b&&b._rzbPair;if(!P||b.dead||!(dmg>0))return 0;let targets=[];
  if(typeof _dmgBullet!=='undefined'&&_dmgBullet&&_dmgBullet.kind==='beam'){
    const q=razorbackPairBeamHit(b,_dmgBullet);if(q)targets=[P.actors[q.actor]];
  }else if(hx!=null&&hy!=null){const id=razorbackPairPartAt(b,hx,hy);if(id)targets=[P.actors[+id.split(':')[0]]];}
  else if(typeof _dmgBullet!=='undefined'&&_dmgBullet&&_dmgBullet.kind==='flame'&&typeof flameHit==='function')
    targets=P.actors.filter(p=>!p.dead&&flameHit(_dmgBullet,p.x,p.y,p.w,p.h));
  else targets=P.actors.filter(p=>!p.dead);
  const before=b.hp;for(const p of targets){if(!p||p.dead)continue;const dealt=razorbackHit(p,dmg,hx,hy);if(!(dealt>0))continue;
    p.hp=Math.max(0,p.hp-dealt);p.flash=.18;if(typeof markHit==='function')markHit(p);weaponHitSfx('normal');
    if(p.hp<=0&&!p.dead){p.dead=true;p.dying=0;razorbackClear(p);if(typeof unitDeathFX==='function')unitDeathFX(p,'mini','red');}
  }
  razorbackPairSync(b);if(typeof stageStats!=='undefined')stageStats.dmgDealt+=Math.max(0,before-b.hp);return Math.max(0,before-b.hp);
}
function razorbackPairUpdate(b,dt){
  const P=b._rzbPair;for(const p of P.actors){p.t+=dt;if(p.dead){p.dying+=dt;if(p.dying>=1.05)p._rzbGone=true;}else razorbackUpdate(p,dt);}
  razorbackPairSync(b);
  if(!P.cleared&&P.actors.every(p=>p._rzbGone)){P.cleared=true;b.dead=true;b.dying=0;b._deathFxStarted=true;
    achievementEncounterDefeat(b,'miniboss');rzbSfx('expBig');shake=Math.max(shake||0,10);}
}
function razorbackPairDraw(b){for(const p of b._rzbPair.actors)if(!p._rzbGone)razorbackDraw(p);}
function razorbackPartAt(b,x,y){`,'pair functions');
one("  const R=b._rzb, W=(typeof worldWidth==='function')?worldWidth():VW, list=RZB_ATTACKS[R.state]||RZB_ATTACKS.guns;\n  R.attack=list[++R.idx%list.length]; R.at=0; R.beat=-1; R.mgBeat=-1; R.charge=0;\n  R.tgt={x:(R.idx%2)?W*0.27:W*0.73, y:(R.idx%3===0)?VH*0.36:VH*0.24};",
"  const R=b._rzb, W=(typeof worldWidth==='function')?worldWidth():VW, L=camLeftX(),span=camRightX()-L,list=RZB_ATTACKS[R.state]||RZB_ATTACKS.guns;\n  R.attack=list[++R.idx%list.length]; R.at=0; R.beat=-1; R.mgBeat=-1; R.charge=0;\n  if(R.pairSide){const inner=(R.idx%2)!==0;R.homeX=L+span*(R.pairSide<0 ? .28 : .72);R.tgt={x:L+span*(R.pairSide<0 ? (inner ? .34 : .25) : (inner ? .66 : .75)),y:(R.idx%3===0)?VH*.36:VH*.24};}\n  else R.tgt={x:(R.idx%2)?W*0.27:W*0.73, y:(R.idx%3===0)?VH*.36:VH*.24};",
'pair lanes');
one("  const R=b._rzb; R.state=state; R.pt=0; R.trans=1.4; R.idx=-1; razorbackClear(b);",
"  const R=b._rzb; R.state=state; R.pt=0; R.trans=1.4; R.idx=-1+(R.attackOffset||0); razorbackClear(b);",
'pair attack offset');
one("    R.tgt={x:(typeof worldWidth==='function'?worldWidth():VW)/2, y:VH*0.27};",
"    R.tgt={x:R.homeX==null?(typeof worldWidth==='function'?worldWidth():VW)/2:R.homeX, y:VH*0.27};",
'pair arrival');
one("      if(R.beat<0){ R.beat=0; stageRevisionCue(b,'razorbackRam',.12); } }   // the rush winds up audibly",
"      if(R.pairSide){const L=camLeftX(),right=camRightX(),half=(L+right)*.5,gap=b.w*.5+9;R.ramX=clamp(R.ramX,R.pairSide<0?L+b.w*.5:half+gap,R.pairSide<0?half-gap:right-b.w*.5);}\n      if(R.beat<0){ R.beat=0; stageRevisionCue(b,'razorbackRam',.12); } }   // the rush winds up audibly",
'pair ram');
one("    else R.tgt={x:W/2, y:VH*0.26};",
"    else R.tgt={x:R.homeX==null?W/2:R.homeX, y:VH*0.26};",
'pair ram return');
one("  for(const q of eBullets) if(q._rzb) q.dead=true;",
"  for(const q of eBullets) if(q._rzb&&(!q._rzbOwner||q._rzbOwner===b)) q.dead=true;",
'owned clear');
one("  eBullets.push({x:p.x,y:p.y,vx:Math.cos(ga)*v,vy:Math.sin(ga)*v,w:r,h:r,kind:kind,t:0,_rzb:true,ang:ga,spin:Math.random()*6});",
"  eBullets.push({x:p.x,y:p.y,vx:Math.cos(ga)*v,vy:Math.sin(ga)*v,w:r,h:r,kind:kind,t:0,_rzb:true,_rzbOwner:b,ang:ga,spin:Math.random()*6});",
'shot owner');
one("    _shootable:true,spd:v,_accel:0.0264,_maxspd:5.04,t:0,_rzb:true});",
"    _shootable:true,spd:v,_accel:0.0264,_maxspd:5.04,t:0,_rzb:true,_rzbOwner:b});",
'missile owner');
one("        for(let i=n0;i<eBullets.length;i++) eBullets[i]._rzb=true;",
"        for(let i=n0;i<eBullets.length;i++){eBullets[i]._rzb=true;eBullets[i]._rzbOwner=b;}",
'mg owner');
one("  continueRewardMark(b);\n  subBoss=b; subBossActive=true;",
"  if(kind==='razorback'&&typeof razorbackPairInit==='function')razorbackPairInit(b);\n  continueRewardMark(b);\n  subBoss=b; subBossActive=true;",
'spawn pair');
one("  if(b._rzb){ razorbackUpdate(b,dt); return; }          // the tank owns its arrival, drive and weapons (0912r)",
"  if(b._rzbPair){razorbackPairUpdate(b,dt);return;}\n  if(b._rzb){ razorbackUpdate(b,dt); return; }          // the tank owns its arrival, drive and weapons (0912r)",
'update pair');
one("  if(b._rzb){ razorbackDraw(b); return; }",
"  if(b._rzbPair){razorbackPairDraw(b);return;}\n  if(b._rzb){ razorbackDraw(b); return; }",
'draw pair');
one("  if(b._rzb && typeof razorbackPartAt==='function') return razorbackPartAt(b,x,y);   // only the EXPOSED part stops a shot",
"  if(b._rzbPair&&typeof razorbackPairPartAt==='function')return razorbackPairPartAt(b,x,y);\n  if(b._rzb && typeof razorbackPartAt==='function') return razorbackPartAt(b,x,y);   // only the EXPOSED part stops a shot",
'part pair');
one("  if(b._tempestDuo)return tempestBrothersBeamHit(b,beam);\n  if(b._rzb)return razorbackBeamHit(b,beam);",
"  if(b._tempestDuo)return tempestBrothersBeamHit(b,beam);\n  if(b._rzbPair)return razorbackPairBeamHit(b,beam);\n  if(b._rzb)return razorbackBeamHit(b,beam);",
'beam pair');
one("  if(b._rzb) return razorbackPartAt(b,x,y)!==null;",
"  if(b._rzbPair)return razorbackPairPartAt(b,x,y)!==null;\n  if(b._rzb) return razorbackPartAt(b,x,y)!==null;",
'solid pair');
one("  if(b._tempestDuo){ tempestBrothersHit(b,dmg,hx,hy); return; }",
"  if(b._tempestDuo){ tempestBrothersHit(b,dmg,hx,hy); return; }\n  if(b._rzbPair){razorbackPairHit(b,dmg,hx,hy);return;}",
'damage pair');
one("  }else if(b._rzb){\n    sectional=true;const R=b._rzb,ids=R.state==='guns'?['left','right']:[R.state];",
"  }else if(b._rzbPair){\n    sectional=true;for(let ai=0;ai<b._rzbPair.actors.length;ai++){const p=b._rzbPair.actors[ai],R=p._rzb,ids=R.state==='guns'?['left','right']:[R.state];\n      if(!p.dead&&R.state!=='arrival'&&R.trans<=0)for(const id of ids)if(R.pools[id]>0){const rid=ai+':'+id,state=()=>{const q=id==='left'||id==='right'?rzbWorld(p,id==='left'?-57:57,96):{x:p.x,y:p.y};return{x:q.x,y:q.y,hp:R.pools[id],dead:p.dead||R.pools[id]<=0||R.state!==((id==='left'||id==='right')?'guns':id)||R.trans>0};};\n        a.push(retinaImpactTarget(b,rid,'razorback '+(ai+1)+' '+id,state,(RZB_R[id==='left'||id==='right'?'gun':id]||34)*2,(RZB_R[id==='left'||id==='right'?'gun':id]||34)*2));}\n    }\n  }else if(b._rzb){\n    sectional=true;const R=b._rzb,ids=R.state==='guns'?['left','right']:[R.state];",
'retina pair');
one("        if(b._sbt<=0&&(subBoss._rzb||subBoss._tempestDuo)){",
"        if(b._sbt<=0&&(subBoss._rzb||subBoss._rzbPair||subBoss._tempestDuo)){",
'held beam pair');
one("&& (!subBoss._tempestDuo||tempestBrothersContact(subBoss,player.x,player.y)) && Math.abs(subBoss.x-player.x)",
"&& (!subBoss._tempestDuo||tempestBrothersContact(subBoss,player.x,player.y)) && (!subBoss._rzbPair||razorbackPairContact(subBoss,player.x,player.y)) && Math.abs(subBoss.x-player.x)",
'contact pair');
one("function encounterDamageOverlay(b,isMini){\n  if(!b||b.dead||!(b.maxhp>0)||b.hp/b.maxhp>.50||typeof XART==='undefined')return;",
"function encounterDamageOverlay(b,isMini){\n  if(b&&b._rzbPair){for(const p of b._rzbPair.actors)encounterDamageOverlay(p,true);return;}\n  if(!b||b.dead||!(b.maxhp>0)||b.hp/b.maxhp>.50||typeof XART==='undefined')return;",
'damage overlay pair');
fs.writeFileSync(p,s,'utf8');console.log('PATCHED_RAZORBACK_DUO_0915');
