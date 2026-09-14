/* Native campaign adapter for the reviewed Tempest duo. The source AI owns only
   ship movement and phase decisions; BOF owns input, rounds, locks, damage,
   rendering, sound and the ordinary miniboss completion. Never call Duo.step:
   its standalone escape would move the campaign player. */
function tempestBrothersInit(b){
  tempestInit(b);
  delete b._tlv;
  b.kind='tempestbrothers'; b.name='TEMPEST LEVIATHAN BROTHERS';
  const ai=new TEMPEST_DUO_AI.Duo();
  /* A gray return warning is also an inbound pass. Let that pass and its
     counterattack finish before black warns a ram, then gray can regroup and
     hold. The standalone only included its initial warn/run states here. */
  const crossing=ai.grayCrossing.bind(ai);
  ai.grayCrossing=function(){const p=b._tempestDuo&&b._tempestDuo.ships[1];return (p&&p._jet.active)||crossing()||(!this.gray.gone&&
    (this.gray.state==='reentry'||this.gray.state==='counter'||
      (this.gray.state==='regroup'&&!this.gray.offscreen())));};
  b._tempestDuo={ai:ai, ships:[], hpSync:false};
  const busy=ai.blackBusy.bind(ai);
  ai.blackBusy=function(){const p=b._tempestDuo.ships[0];return b._tempestDuo.waitingForBlack||(p&&p._jet.active)||busy();};
  ai.ships.forEach(function(s,i){
    const p={x:0,y:0,w:b.w,h:b.h,_drawW:b._drawW,_drawH:b._drawH,
      hp:1,maxhp:1,flash:0,dead:false,dying:0,_tempestGray:i===1,
      _tlv:{ap:[],beams:[],fx:[],hitFlash:0,sfxT:0},_ai:s,_pending:[],_pid:0,
      _jet:{angle:Math.PI,baseAngle:Math.PI,active:false,state:'',cue:null,cooldown:i?3.8:1.8,
        passes:0,greens:0,thrusts:0}};
    b._tempestDuo.ships.push(p);
    const ports=s.ports.bind(s);
    s.ports=function(dir){
      /* The south-facing nose has the front aperture pair on its lower edge. */
      return ports(p._jet.baseAngle===Math.PI?-dir:dir).map(q=>Object.assign({},q,{dir:dir}));
    };
    /* Mounts stay at the authored hull's hardpoints. Source bullets are handed
       straight to BOF, rather than simulated once in each engine. */
    s.spawn=function(x,y,a,speed,kind){
      let id=0, best=Infinity;
      this.turrets().forEach(function(q){ const d=Math.hypot(x-q.x,y-q.y); if(d<best){best=d;id=q.id;} });
      p._pending.push({id:id,a:a,s: speed||480,kind:kind||'bolt'});
    };
    const enter=s.enter.bind(s);
    s.enter=function(phase){
      const old=this.phase;
      enter(phase);
      if(old!==this.phase){ p._pid++; p._pending=[];tempestJetCancel(b,p); tempestBrothersClear(p); tlvSfx('maverickHelixRelease'); }
      if(i===0&&(phase==='pursuit'||phase==='frenzy')) this.boss.y=(tempestBelowRow(p)-TLV_YOFF)/TLV_KY;
      if(phase==='death') tlvSfx('explosionBossCore');
    };
    if(i===0){
      const change=s.change.bind(s);
      s.change=function(state){
        change(state);
        const left=camLeftX();
        if(state==='edge') this.lockX=(tempestEdgeX(this.side)-left)/TLV_KX;
        if(state==='ram') this.ramTarget=(tempestRamToX(this.side)-left)/TLV_KX;
      };
      const move=s.move.bind(s);
      s.move=function(axis,target,speed,dt){
        const cross=this.phase==='overtake'||this.phase==='return';
        if(cross&&this.t<TLV_CROSS_WARN) return false;
        if(axis==='y'&&target===930) target=(tempestBelowRow(p)-TLV_YOFF)/TLV_KY;
        const done=move(axis,target,speed,dt);
        if(cross&&!done&&this.t>1.5) this.t=1.5; // finish crossing before changing phase
        return done;
      };
    }
  });
  for(const k in BOFX.img) if(k.indexOf('tlvb_')===0) XART.rdy(k);
  for(let i=0;i<4;i++)XART.rdy('ndr_dambreaker_bottomthruster_'+i);
  tempestBrothersSync(b);
}
function tempestBrothersClear(p){
  if(typeof eBullets!=='undefined') for(const q of eBullets) if(q._tempestShip===p) q.dead=true;
  if(typeof playerLocks!=='undefined') playerLocks=playerLocks.filter(function(L){return L.src!==p;});
  p._tlv.beams=[];
}
function tempestBrothersSync(b){
  const D=b._tempestDuo, scale=b.maxhp/16000;
  for(const p of D.ships){
    const s=p._ai,T=p._tlv;
    p.x=tlvX(s.boss.x); p.y=tlvY(s.boss.y); p.hp=s.hp*scale; p.maxhp=8000*scale;
    p.dead=s.phase==='death'||s.gone; p.dying=p.dead?s.t:0;
    T.phase=s.phase; T.state=s.state; T.t=s.t; T.st=s.st; T.time=s.time;
    T.axis=s.motionAxis; T.vuln=s.vulnerable&&!s.gone&&!p.dead;
    T.hitFlash=s.hitFlash; T.ramWarn=!!s.ramWarning; T.ramY=tlvY(s.ramY);
    T.cross=!p._tempestGray&&(s.phase==='overtake'||s.phase==='return') ?
      {to:s.phase==='overtake'?tempestBelowRow(p):tlvY(230)} : null;
    T.ap=s.rig.map(function(r){return {hp:r.hp*scale,max:300*scale,hit:r.hit,flash:r.flash,charge:r.charge};});
    T.beams=s.beams.map(function(q){ const pos=tempestPortXY(p,q.id); return {id:q.id,x:pos.x,y:pos.y,dir:q.dir,ang:p._jet.angle+TLV_PORTS[q.id][2]*Math.PI/2,active:q.active,charge:q.charge}; });
    T.fx=s.fx.map(function(f){return {ox:f.anchor?f.anchor.x:f.x-s.boss.x,
      oy:f.anchor?f.anchor.y:f.y-s.boss.y,age:f.age,life:f.life,s:f.s};});
  }
  b.hp=(D.ai.black.hp+D.ai.gray.hp)*scale;
  /* A broad phase enclosing the visible targetable ships, followed by actual
     part tests. The empty air between brothers never stops a round or a pilot. */
  const targets=D.ships.filter(function(p){return p._tlv.vuln;});
  const boxes=targets.length?targets:D.ships.filter(function(p){return !p._ai.gone;});
  if(boxes.length){
    const half=p=>({x:(Math.abs(Math.cos(p._jet.angle))*p._drawW+Math.abs(Math.sin(p._jet.angle))*p._drawH)/2,
      y:(Math.abs(Math.sin(p._jet.angle))*p._drawW+Math.abs(Math.cos(p._jet.angle))*p._drawH)/2});
    const l=Math.min(...boxes.map(p=>p.x-half(p).x)),r=Math.max(...boxes.map(p=>p.x+half(p).x));
    const t=Math.min(...boxes.map(p=>p.y-half(p).y)),bot=Math.max(...boxes.map(p=>p.y+half(p).y));
    b.x=(l+r)/2; b.y=(t+bot)/2; b.w=b._drawW=r-l; b.h=b._drawH=bot-t;
  }
}
function tempestBrothersPartAt(b,x,y){
  if(!b||b.dead||!b._tempestDuo) return null;
  for(let i=1;i>=0;i--){
    const p=b._tempestDuo.ships[i], key=tempestJetPartAt(p,x,y);
    if(key) return (i?'G':'B')+(key==='hull'?'hull':key.slice(2));
  }
  return null;
}
function tempestBrothersContact(b,x,y){
  return b._tempestDuo.ships.some(function(p){const q=tempestJetLocal(p,x,y);return p._tlv.vuln&&
    Math.abs(q.x)<p.w/2+10&&Math.abs(q.y)<p.h/2+10;});
}
function tempestBrothersBeamHit(b,beam,hx){
  const range=playerBeamRange(beam,hx);let best=null;
  if(!b||b.dead||!range)return null;
  for(const p of b._tempestDuo.ships){
    if(!p._tlv.vuln||p.dead)continue;
    let part=null;
    for(let i=0;i<4;i++)if(p._tlv.ap[i].hp>0){
      const q=TLV_PORTS[i],hit=tempestJetRectBeam(p,q[0]*TLV_S,q[1]*TLV_S,TLV_AP_BOX[0]*TLV_S,TLV_AP_BOX[1]*TLV_S,range);
      if(hit&&(!part||hit.entry>part.entry))part=Object.assign(hit,{key:(p._tempestGray?'G':'B')+i});
    }
    if(!part){
      const hit=tempestJetRectBeam(p,0,0,TLV_HULL_BOX[0]*TLV_S,TLV_HULL_BOX[1]*TLV_S,range);
      if(hit)part=Object.assign(hit,{key:(p._tempestGray?'G':'B')+'hull'});
    }
    if(part&&(!best||part.entry>best.entry))best=part;
  }
  return best;
}
function tempestBrothersHit(b,dmg,hx,hy){
  if(!(dmg>0)||b.dead) return;
  const D=b._tempestDuo, scale=b.maxhp/16000, before=b.hp;
  let keys=[];
  if(typeof _dmgBullet!=='undefined'&&_dmgBullet&&_dmgBullet.kind==='beam'){
    const hit=tempestBrothersBeamHit(b,_dmgBullet,hx);if(hit)keys=[hit.key];
  }else if(hx!=null&&hy!=null){
    const key=tempestBrothersPartAt(b,hx,hy);
    if(key) keys=[key];
  } else keys=D.ships.filter(p=>p._tlv.vuln).map(p=>(p._tempestGray?'G':'B')+'hull');
  for(const key of keys){
    const p=D.ships[key[0]==='G'?1:0],s=p._ai;
    if(!p._tlv.vuln) continue;
    if(typeof markHit==='function') markHit(p);
    if(key.slice(1)==='hull') s.damage(dmg/scale);
    else s.damageTurret(+key.slice(1),dmg/scale);
    /* Flash only the brother struck; the other hull keeps its own paint. */
    p.flash=0.045;
    if(s.events.indexOf('impact')>=0) tempestImpactSfx(p._tlv,0.12);
    weaponHitSfx('normal');
  }
  tempestBrothersSync(b);
  if(typeof stageStats!=='undefined') stageStats.dmgDealt+=Math.max(0,before-b.hp);
}
function tempestBrothersRound(p,q){
  const s=p._ai;
  if(p.dead||s.gone||s.rig[q.id].hp<=0) return;
  function launch(){
    const pos=tempestPortXY(p,q.id),needle=q.kind==='missile';
    const speed=q.s*TLV_KY*TLV_PFAST/60;
    const ang=p._jet.angle+TLV_PORTS[q.id][2]*Math.PI/2;
    eBullets.push({x:pos.x,y:pos.y,vx:Math.cos(ang)*speed,vy:Math.sin(ang)*speed,
      ang:ang,w:needle?12:9,h:needle?22:14,kind:needle?'tlvNeedle':'tlvBolt',
      hp:1,_shootable:needle,spd:speed,t:0,dmg:1,_tlv:true,_tempestShip:p});
    s.rig[q.id].flash=0.08;
  }
  if(q.kind==='missile'){
    const pid=p._pid,delay=TLV_LOCK_ARM+(p._needleN++||0)*TLV_LOCK_GAP;
    enemyLockOn(p,delay,{fire:function(){if(!p.dead&&!s.gone&&p._pid===pid&&s.rig[q.id].hp>0)launch();}});
  } else launch();
}
function tempestBrothersUpdate(b,dt){
  const D=b._tempestDuo,ai=D.ai;
  dt=clamp(dt||0,0,0.04);
  if(b._scene&&typeof sceneDirectorTick==='function'&&sceneDirectorTick(b,dt)){
    for(const p of D.ships){p._tlv.beams=[];p._tlv.ramWarn=false;tempestJetCancel(b,p);} return;
  }
  const target=ai.player;
  target.x=(player.x-((typeof camLeftX==='function')?camLeftX():0))/TLV_KX;
  target.y=(player.y-TLV_YOFF)/TLV_KY;
  for(const p of D.ships){
    const s=p._ai;
    p.flash=Math.max(0,p.flash-dt); p._tlv.sfxT=Math.max(0,p._tlv.sfxT-dt);
    if(s.gone) continue;
    p._jet.cooldown-=dt;
    const combat=s.phase==='chase'||s.phase==='hell'||s.phase==='pursuit'||s.phase==='frenzy';
    const safe=p._tempestGray?s.state==='counter':(s.state==='strafe'||s.state==='laser-track'||s.state==='punish'||s.state==='climb');
    if(!p._tempestGray&&combat&&safe&&!D.striker&&p._jet.cooldown<=0)D.waitingForBlack=true;
    if(combat&&safe&&!D.striker&&p._jet.cooldown<=0&&(!p._tempestGray||!ai.blackBusy())&&
      (p._tempestGray||!ai.grayCrossing()))tempestJetStart(b,p);
    if(p._jet.active)tempestJetTick(b,p,dt);else ai.think(s,dt);
    tempestJetPose(p,dt);
    if(s.phase==='escape'||s.phase==='victory'){
      s.gone=true;s.vulnerable=false;s.bullets=[];s.beams=[];s.entryWarn=null;
      tempestBrothersClear(p);
      tempestJetCancel(b,p);
      if(!ai.firstDown) ai.firstDown=p._tempestGray?'gray':'black';
      ai.alone=true;
    }
  }
  tempestBrothersSync(b);
  for(const p of D.ships){
    const s=p._ai;
    p._needleN=0;
    for(const q of p._pending) tempestBrothersRound(p,q);
    p._pending=[];
    if(s.events.indexOf('shot')>=0) tlvSfx('enemyMachineShotHeavy');
    if(s.events.indexOf('laser')>=0) tlvSfx('enemyPulseLaserBlue');
    if(s.events.indexOf('ram')>=0) tlvSfx('maverickHelixRelease');
    if(s.events.indexOf('impact')>=0) tempestImpactSfx(p._tlv,s.phase==='frenzy'?0.6:0.12);
    if(!p.dead&&!player.dead) for(const q of p._tlv.beams){
      if(tempestJetBeamTouches(q,player.x,player.y)){playerHit();break;}
    }
  }
  if(ai.ships.every(s=>s.gone)){
    b.dead=true;b.dying=0;b._deathFxStarted=true;
    /* Both falling reactors have already played. Complete once via the normal
       1.9-second slot release and powerup drop; no standalone player escape. */
    tlvSfx('expBig');shake=Math.max(shake||0,10);
  }
}
function tempestBrothersDraw(b){
  const D=b._tempestDuo;
  /* The 77px band belongs to the gauge. Attacks are clipped out of it, and the
     gauge is drawn after the ships, in screen space, for camera and zoom alike. */
  const L=camLeftX(),R=camRightX(),top=viewTopY()+77/viewZoom();
  ctx.save();ctx.beginPath();ctx.rect(L,top,R-L,VH-top+160);ctx.clip();
  for(const p of D.ships) if(!p._ai.gone){
    tempestJetShipDraw(p);
    const w=p._ai.entryWarn;
    if(w&&p._tempestGray){
      const x=tlvX(w.x),y=Math.max(top+6,tlvY(w.y)),pulse=0.6+0.3*Math.abs(Math.sin(p._ai.time*14));
      tempestBlit(tlvImg('tlv_charge'),x,y,30,30,pulse);
      ctx.save();ctx.strokeStyle='#ff536b';ctx.lineWidth=2;
      if(ctx.setLineDash)ctx.setLineDash([8,6]);
      const dx=(w.tx-w.x)*TLV_KX,dy=(w.ty-w.y)*TLV_KY,len=Math.hypot(dx,dy)||1;
      ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+dx/len*72,y+dy/len*72);ctx.stroke();ctx.restore();
    }
  }
  ctx.restore();
}
