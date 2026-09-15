const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');
let s=fs.readFileSync(p,'utf8');
if(s.includes('\r\n'))throw new Error('game.js must remain LF');
function one(a,b,label){const n=s.split(a).length-1;if(n!==1)throw new Error(label+' matches '+n);s=s.replace(a,b);}
one("    coreEnrage:null,coreEnrageCount:0,coreEnrageShots:0,coreEnrageGapWindows:0,\n    chainBolts:0,chainOrbs:0,chainLastAngles:[],chainCycles:0,",
"    coreEnrage:null,coreEnrageCount:0,coreEnrageShots:0,coreEnrageGapWindows:0,\n    chainBolts:0,chainOrbs:0,chainLastAngles:[],chainCycles:0,giantStrike:null,giantStrikeCount:0,giantStrikeHits:0,",
'init');
one("function stage4WarfareMiniTick(b,dt){return stage4MiniDirector(b,dt);}",`/* Furious-only finisher after the widened chain-lightning cycle. The five-second clock is real
   time rather than the boss phase-scaled S.t clock, so low health cannot silently shorten the
   warning. The centre is lethal only after release; the outer 17% of each camera edge remains a
   measured safe corner throughout the strike. */
const S4_GIANT_STRIKE={charge:5.00,active:.88,recover:.72,safeFrac:.17};
function stage4GiantStrikeBounds(){
  const left=camLeftX(),right=camRightX(),safe=(right-left)*S4_GIANT_STRIKE.safeFrac;
  return {left:left+safe,right:right-safe,safe:safe,viewLeft:left,viewRight:right};
}
function stage4GiantStrikeColor(G){return G.t<G.charge*.56?'yellow':'red';}
function stage4GiantStrikeStart(b){
  const S=b&&b._s4war;if(!S||S.mini||S.giantStrike||typeof diffKey==='undefined'||diffKey!=='furious')return false;
  stage4WarfareSetMode(b,'giantStrike');const R=stage4GiantStrikeBounds();
  S.giantStrike={t:0,charge:S4_GIANT_STRIKE.charge,active:S4_GIANT_STRIKE.active,recover:S4_GIANT_STRIKE.recover,
    left:R.left,right:R.right,safe:R.safe,released:false,redWarned:false,hitSeats:{},_arrowN:-1,_warnSfx:0};
  S.giantStrikeCount++;l23FovWarm();
  try{if(typeof XART!=='undefined')for(const k of ['cfx_stage4_chain_lightning','s4w_lightning_ball_0'])XART.rdy(k);}catch(_s4gw){}
  stage4WarfareSound('bossWeaponCharge','enemyElectricBolt');return true;
}
function stage4GiantStrikeTick(b,dt){
  const S=b&&b._s4war,G=S&&S.giantStrike;if(!G)return false;G.t+=Math.max(0,dt||0);
  const R=stage4GiantStrikeBounds();G.left=R.left;G.right=R.right;G.safe=R.safe;
  const mid=(R.viewLeft+R.viewRight)*.5;b.x+=(mid-b.x)*Math.min(1,dt*7);b.y+=(S.homeY-b.y)*Math.min(1,dt*7);
  S.poseRot=0;S.scale=1+Math.sin(G.t*22)*Math.min(.016,G.t*.004);
  if(!G.released){
    l23WarnSound(G);
    if(stage4GiantStrikeColor(G)==='red'&&!G.redWarned){G.redWarned=true;stage4WarfareSound('dangerAlert','alertLockon');}
    if(G.t>=G.charge){G.released=true;G.t=G.charge;stage4WarfareSound('enemyHeavyLaser','laserCannon');shake=Math.max(shake,18);}
  }
  if(G.released){
    const live=G.t-G.charge;
    if(live<=G.active)for(const seat of seatList())withSeat(seat,()=>{
      const key=String(seat),half=Math.max(5,(player.w||24)*.28);
      if(!G.hitSeats[key]&&!player.dead&&player.y>b.y&&player.x+half>G.left&&player.x-half<G.right){
        G.hitSeats[key]=true;S.giantStrikeHits++;playerHit();
      }
    });
    if(live>=G.active+G.recover){S.giantStrike=null;stage4WarfareSetMode(b,'burst');}
  }
  return true;
}
function stage4GiantStrikeDraw(b){
  const S=b&&b._s4war,G=S&&S.giantStrike;if(!G||typeof XART==='undefined')return false;
  const R=stage4GiantStrikeBounds(),p=shipBossMount(b,'C'),charging=!G.released,
        q=clamp(G.t/Math.max(.001,G.charge),0,1),live=Math.max(0,G.t-G.charge),frame=Math.floor((b.t||G.t)*22)%8;
  ctx.save();ctx.fillStyle='rgba(1,3,12,'+(charging?(.13+.28*q):.46)+')';ctx.fillRect(R.viewLeft,0,R.viewRight-R.viewLeft,VH);ctx.restore();
  if(charging){
    const col=stage4GiantStrikeColor(G),B={family:'rime',angles:[Math.PI/2],t:G.t,warm:G.charge,released:false,fovColor:col};
    ctx.save();ctx.translate(p.x,p.y);l23FovDraw(b,B,0,p,q,(R.right-R.left)*.5);ctx.restore();
    const ak='bmfx_alert_'+col+'_danger';
    if(XART.rdy(ak)&&(Math.floor(G.t*(col==='red'?8:4))%2)===0){
      const im=XART.get(ak),h=46,w=h*(im.naturalWidth/Math.max(1,im.naturalHeight)),top=(b._drawY!=null?b._drawY:b.y)-b.h*.5;
      ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=col==='red'?1:.92;ctx.drawImage(im,p.x-w/2,Math.max(L23_WARN_MINY+35,top+6),w,h);ctx.restore();
    }
    combatAtlasDraw('cfx_stage4_chain_lightning',4,2,frame,p.x,p.y,58+q*42,82+q*62,{blend:'lighter',alpha:.48+.46*q});
    const orb='s4w_lightning_ball_'+(Math.floor(G.t*18)%16);
    if(XART.rdy(orb)){const im=XART.get(orb),sz=36+q*55;ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.48+.46*q;ctx.drawImage(im,p.x-sz/2,p.y-sz/2,sz,sz);ctx.restore();}
    if(G.t>G.charge-.34){const f=clamp((G.t-(G.charge-.34))/.34,0,1);ctx.save();ctx.fillStyle='rgba(255,20,28,'+(.08+.20*f*(.55+.45*Math.sin(G.t*62)))+')';ctx.fillRect(R.viewLeft,0,R.viewRight-R.viewLeft,VH);ctx.restore();}
  }else if(live<=G.active){
    const width=R.right-R.left,cols=7,cw=width/cols*1.30,h=Math.max(120,VH-p.y+50),cy=p.y+h*.5;
    for(let i=0;i<cols;i++)combatAtlasDraw('cfx_stage4_chain_lightning',4,2,(frame+i*3)%8,R.left+(i+.5)*width/cols,cy,cw,h,{blend:'lighter',alpha:.82});
    combatAtlasDraw('cfx_stage4_chain_lightning',4,2,(frame+5)%8,(R.left+R.right)*.5,cy,width*.20,h*1.03,{blend:'lighter',alpha:1});
    const flash=clamp(1-live/.20,0,1);if(flash>0){ctx.save();ctx.fillStyle='rgba(255,24,32,'+(.28*flash)+')';ctx.fillRect(R.viewLeft,0,R.viewRight-R.viewLeft,VH);ctx.restore();}
  }
  return true;
}
function stage4WarfareMiniTick(b,dt){return stage4MiniDirector(b,dt);}`,'functions');
one("  stage4ShieldTick(b,dt);\n  const coreRageActive=!!(S.coreEnrage&&S.coreEnrage.active);\n  if(!coreRageActive)stage4FinalChaingunTick(b,dt,phase);\n  stage4CoreTurretTick(b,dt,phase);",
"  stage4ShieldTick(b,dt);\n  const coreRageActive=!!(S.coreEnrage&&S.coreEnrage.active),giantActive=!!(S.giantStrike&&S.mode==='giantStrike');\n  if(!coreRageActive&&!giantActive)stage4FinalChaingunTick(b,dt,phase);\n  if(!giantActive)stage4CoreTurretTick(b,dt,phase);",
'suspend guns');
one("  if(S.ram&&stage4RamTick(b,dt))return true;\n  const mid=(camLeftX()+camRightX())*.5,sy=S.homeY,margin=Math.max(154,b.w*.54),amp=S.shield.active?2:12;S.poseRot=0;S.scale=1;",
"  if(S.ram&&stage4RamTick(b,dt))return true;\n  if(giantActive){stage4GiantStrikeTick(b,dt);b._animKey=!S.giantStrike||S.giantStrike.released?'s4w_boss_energized_'+(Math.floor((b.t||0)*11)%12):'s4w_boss_charge_'+clamp(Math.floor(S.giantStrike.t/S.giantStrike.charge*12),0,11);return true;}\n  const mid=(camLeftX()+camRightX())*.5,sy=S.homeY,margin=Math.max(154,b.w*.54),amp=S.shield.active?2:12;S.poseRot=0;S.scale=1;",
'giant branch');
one("    if(S.t>=P.end)stage4WarfareSetMode(b,'burst');",
"    if(S.t>=P.end){if(!P.furious||!stage4GiantStrikeStart(b))stage4WarfareSetMode(b,'burst');}",
'transition');
one("  stage4RamShadowDraw(b);\n  stage4MiniHardWarningDraw(b);",
"  stage4RamShadowDraw(b);\n  stage4MiniHardWarningDraw(b);\n  stage4GiantStrikeDraw(b);",
'draw call');
fs.writeFileSync(p,s,'utf8');console.log('PATCHED_SOVEREIGN_GIANT_STRIKE_0915');
