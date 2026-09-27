"""36 bounded native stage-script samples. Limited input bot, MG III / space laser III, normal damage, no forced kills; not campaign wins."""
from pathlib import Path
import json,base64,http.server,time,sys
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/modular_roster_0927/balance');OUT.mkdir(exist_ok=True,parents=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];runs=[]
SETUP="""c=>{for(const k of Object.keys(Input.keys))Input.keys[k]=false;diffKey=c.diff;DIFF=DIFFS[diffKey];run.mode='arcade';run.pilot='yuri';pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');run.lives=DIFF.startLives;run.contUsed=0;run.weapon=0;run.wlevel=3;run.wlevels=[3,1,1,1,1,1,0,0,0];run.missileLevel=2;run.forge={};run.forgeForms={};run.wvars=[];run.bombs=DIFF.startBombs;run.shield=0;run.retinaScan=false;beginStage(c.stage);setState(GS.PLAY);player.reset();story=null;special=null;s6Opening=null;run.spaceWeapon=0;run.spaceLevels=[3,3,3];timeScale=1;run.infusion=null;run._lifeCombatT=0;run._lifeThreat=0;window.Q={hits:[],rolls:0,flips:0,frames:0,deaths:0,lastDead:false,maxEnemy:0,maxBullet:0,patterns:[],bossSeen:false,miniSeen:false,shots:0,cues:{},lastX:player.x,lastY:player.y,maxMove:0};
 if(!window.__realHit){window.__realHit=playerHit;playerHit=function(...args){const before=!!player.dead;const hit={stack:new Error().stack,at:Q.frames/60,cause:args[0]||'contact',x:player.x,y:player.y,stageTime:stageTimer,mini:subBoss?.kind,boss:boss?.kind,grounds:groundTargetingFx.filter(g=>!g.dead&&Math.hypot(g.x-player.x,g.y-player.y)<100).map(g=>({kind:g.kind,x:g.x,y:g.y,t:g.t,warn:g.warn})),nearestBullet:eBullets.reduce((n,b)=>Math.min(n,Math.hypot(b.x-player.x,b.y-player.y)),1e6)};const r=__realHit.apply(this,args);if(!before&&player.dead)Q.hits.push(hit);return r;};}
 if(!window.__realCue){window.__realCue=Snd.play;Snd.play=function(n,v){if(window.Q)Q.cues[n]=(Q.cues[n]||0)+1;return __realCue.call(Snd,n,v);};}
 return {stage:c.stage,diff:c.diff,world:worldWidth()};}"""
STEP="""n=>{for(let i=0;i<n;i++){
 if(state!==GS.PLAY)break;Q.frames++;const dt=1/60;
 for(const k of Object.keys(Input.keys))Input.keys[k]=false;
 if(!player.dead){
  const left=24,right=worldWidth()-24;
  const bodies=[...enemies.filter(e=>!e.dead&&!e._noHit&&e._dyingT==null),...[bossActive?boss:null,subBossActive?subBoss:null].flatMap(b=>!b||b.dead||b.enter?[]:b._tempestDuo?b._tempestDuo.ships.filter(p=>!p.dead&&p._tlv.vuln):[b])];
  const bodyRisk=(x,y,margin)=>bodies.reduce((sum,b)=>{const a=b._jet?.angle||0,c=Math.cos(a),sn=Math.sin(a),vx=b._jet?.active&&b._jet.state==='thrust'?b._jet.vx:0,vy=b._jet?.active&&b._jet.state==='thrust'?b._jet.vy:0;let worst=0;for(const lead of [0,.16,.32]){const dx=x-b.x-vx*lead,dy=y-b.y-vy*lead,u=Math.abs(dx*c+dy*sn),v=Math.abs(-dx*sn+dy*c),hw=(b._jet?b._drawW:b.w)/2+margin,hh=(b._jet?b._drawH:b.h)/2+margin;if(u<hw&&v<hh)worst=Math.max(worst,Math.min(hw-u,hh-v));}return sum+worst;},0);
  const target=_lockTargets().filter(t=>!t.dead&&t.y>PLAY.y-30&&t.y<player.y-45).sort((a,b)=>{
   const rank=q=>(q._retinaOwner||q._bossModule||q._boss||q===boss||q===subBoss?0:1000)+Math.abs(q.x-player.x)+Math.abs(q.y-player.y)*.15;
   return rank(a)-rank(b);
  })[0]||((subBossActive&&subBoss&&!subBoss.enter)?subBoss:bossActive&&boss&&!boss.enter?boss:null);
  if(Q.frames%8===1){let best=Infinity,chosen={x:player.x,y:player.y};
   for(let y=VH*.40;y<=VH*.84;y+=VH*.11)for(let x=left;x<=right;x+=30){let risk=Math.hypot(x-player.x,y-player.y)*.11+Math.abs(y-VH*.77)*.065+(target?Math.abs(x-target.x)*.30:Math.abs(x-worldWidth()/2)*.015);
    if(target&&target.y>y-70)risk+=100;
    for(const b of eBullets){if(b.dead)continue;for(const lead of [4,14,24]){const bx=b.x+(b.vx||0)*lead,by=b.y+(b.vy||0)*lead,d=Math.hypot(x-bx,y-by);if(d<55)risk+=(55-d)*1.8;}}
    for(const g of groundTargetingFx){if(g.dead||g.delay>0||g.t<g.warn*.30)continue;const d=g.kind==='missile'?Math.hypot(x-g.x,y-g.y):Math.abs(x-g.x);risk+=Math.max(0,g.radius+45-d)*8;}
    risk+=bodyRisk(x,y,44)*15;
    if(subBoss?._tempestDuo)for(const ship of subBoss._tempestDuo.ships)for(const beam of ship._tlv.beams){const dx=x-beam.x,dy=y-beam.y,side=Math.abs(-dx*Math.sin(beam.ang)+dy*Math.cos(beam.ang)),along=dx*Math.cos(beam.ang)+dy*Math.sin(beam.ang);if(along>0)risk+=Math.max(0,38-side)*(beam.active?10:6);}
    if(risk<best){best=risk;chosen={x,y};}}
   Q.aim=chosen.x;Q.aimY=chosen.y;
  }
  const hold=a=>(keybindFor(1)[a]||[]).filter(k=>!k.startsWith('pad_')).forEach(k=>Input.keys[k]=true);
  const groundDanger=groundTargetingFx.some(g=>!g.dead&&g.delay<=0&&g.t>g.warn-.25&&(g.kind==='missile'?Math.hypot(player.x-g.x,player.y-g.y):Math.abs(player.x-g.x))<g.radius+16);const danger=bodyRisk(player.x,player.y,24)>0||groundDanger||eBullets.some(b=>!b.dead&&Math.hypot(player.x-b.x-(b.vx||0)*8,player.y-b.y-(b.vy||0)*8)<29);
  if(danger&&!player.roll&&!player.somer){
   if(!(player._rollCool>0)){const dir=Q.aim>player.x?1:-1;startRoll(dir);if(player.roll)Q.rolls++;}
   else if(!(player._somerCool>0)){startSomersault();if(player.somer)Q.flips++;}
  }
  if(player.x<(Q.aim||player.x)-7)hold('right');if(player.x>(Q.aim||player.x)+7)hold('left');
  if(player.y<(Q.aimY||VH*.79)-8)hold('down');if(player.y>(Q.aimY||VH*.79)+8)hold('up');hold('fire');
  if(Q.frames%150===0&&run.bombs>0)Input.injectTap((keybindFor(1).bomb||['k'])[0]);
 }
 updatePlay(dt);Q.maxMove=Math.max(Q.maxMove,Math.hypot(player.x-Q.lastX,player.y-Q.lastY));Q.lastX=player.x;Q.lastY=player.y;
 if(player.dead&&!Q.lastDead)Q.deaths++;Q.lastDead=player.dead;
 Q.maxEnemy=Math.max(Q.maxEnemy,enemies.filter(e=>!e.dead).length);Q.maxBullet=Math.max(Q.maxBullet,eBullets.filter(e=>!e.dead).length);
 Q.bossSeen=Q.bossSeen||!!bossActive;Q.miniSeen=Q.miniSeen||!!subBossActive;
 for(const b of [boss,subBoss]){const m=b?._hammer?.state||b?._bomber?.mode||b?._s7mod?.mode||b?._er26?.mode||b?._late27?.mode||b?._v24?.pattern?.type||b?._whv?.st;if(m&&!Q.patterns.includes(m))Q.patterns.push(m);}
 if(i%6===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(dt*6);}
 }return {state,seconds:Q.frames/60,deaths:Q.deaths};}"""
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1000,'height':1050})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  for diff in ['easy','normal','hard','furious']:
   for stage in ([int(x) for x in sys.argv[1:]] if len(sys.argv)>1 else range(1,10)):
    case={'stage':stage,'diff':diff};print('RUN',case,flush=True);p.evaluate(SETUP,case)
    for sec in range(180):
     status=p.evaluate(STEP,60);p.wait_for_timeout(8)
     if sec in [29,89,179]:
      (OUT/f'{stage}-{diff}-{sec+1}.png').write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
     if status['state']!='play':break
    result=p.evaluate('c=>({...c,...Q,state,stageTimer,hp:boss?.hp,miniHp:subBoss?.hp,weapon:run.weapon,level:run.wlevel,score:run.score,stageClear:bossDefeated,ammo:run.bombs,finite:[...eBullets,...pBullets].every(b=>Number.isFinite(b.x)&&Number.isFinite(b.y))})',case)
    runs.append(result);(OUT/'report.json').write_text(json.dumps({'runs':runs,'errors':errors},indent=2),encoding='utf-8')
    print({k:result[k] for k in ['stage','diff','state','deaths','bossSeen','maxEnemy','maxBullet']},flush=True)
  br.close()
finally:stop()
assert not errors,errors
assert all(r['finite'] for r in runs)
