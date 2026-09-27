"""27 native Chromium runs. A limited input bot; no invulnerability or forced damage."""
from pathlib import Path
import json,base64,http.server,time
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overnight_0927/campaign');OUT.mkdir(exist_ok=True,parents=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];runs=[]
SETUP="""c=>{for(const k of Object.keys(Input.keys))Input.keys[k]=false;diffKey=c.diff;DIFF=DIFFS[diffKey];run.mode='arcade';run.pilot='yuri';pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');run.lives=4;run.contUsed=0;run.weapon=0;run.wlevel=3;run.wlevels=[3,1,1,1,1,1,0,0,0];run.missileLevel=2;run.forge={};run.forgeForms={};run.wvars=[];run.bombs=12;run.shield=0;run.retinaScan=false;beginStage(c.stage);setState(GS.PLAY);player.reset();story=null;special=null;s6Opening=null;run.spaceWeapon=0;run.spaceLevels=[3,3,3];window.Q={frames:0,deaths:0,lastDead:false,maxEnemy:0,maxBullet:0,patterns:[],bossSeen:false,miniSeen:false,shots:0,cues:{},lastX:player.x,lastY:player.y,maxMove:0};
 if(!window.__realCue){window.__realCue=Snd.play;Snd.play=function(n,v){if(window.Q)Q.cues[n]=(Q.cues[n]||0)+1;return __realCue.call(Snd,n,v);};}
 return {stage:c.stage,diff:c.diff,world:worldWidth()};}"""
STEP="""n=>{for(let i=0;i<n;i++){
 if(state!==GS.PLAY)break;Q.frames++;const dt=1/60;
 for(const k of Object.keys(Input.keys))Input.keys[k]=false;
 if(!player.dead){
  const left=Math.max(24,camLeftX()+20),right=Math.min(worldWidth()-24,camRightX()-20),y=VH*.80;
  if(Q.frames%12===1){let best=Infinity,chosen=player.x;
   for(let x=left;x<=right;x+=24){let risk=Math.abs(x-player.x)*.1;
    for(const b of eBullets){if(b.dead)continue;const bx=b.x+(b.vx||0)*18,by=b.y+(b.vy||0)*18,d=Math.hypot(x-bx,y-by);if(d<90)risk+=(90-d)*3;}
    for(const e of enemies){if(!e.dead&&Math.abs(e.y-y)<90)risk+=Math.max(0,90-Math.abs(e.x-x))*2;}
    if(bossActive&&boss&&!boss.dead){risk+=Math.abs(x-boss.x)*.035;if(Math.abs(boss.y-y)<100)risk+=Math.max(0,120-Math.abs(boss.x-x))*3;}
    if(risk<best){best=risk;chosen=x;}}
   Q.aim=chosen;
  }
  const hold=a=>(keybindFor(1)[a]||[]).filter(k=>!k.startsWith('pad_')).forEach(k=>Input.keys[k]=true);
  if(player.x<(Q.aim||player.x)-7)hold('right');if(player.x>(Q.aim||player.x)+7)hold('left');
  if(player.y<y-8)hold('down');if(player.y>y+8)hold('up');hold('fire');
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
  for diff in ['normal','hard','furious']:
   for stage in range(1,10):
    case={'stage':stage,'diff':diff};print('RUN',case,flush=True);p.evaluate(SETUP,case)
    for sec in range(120):
     status=p.evaluate(STEP,60);p.wait_for_timeout(8)
     if sec in [19,59,99]:
      (OUT/f'{stage}-{diff}-{sec+1}.png').write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
     if status['state']!='play':break
    result=p.evaluate('c=>({...c,...Q,state,stageTimer,hp:boss?.hp,miniHp:subBoss?.hp,ammo:run.bombs,finite:[...eBullets,...pBullets].every(b=>Number.isFinite(b.x)&&Number.isFinite(b.y))})',case)
    runs.append(result);(OUT/'report.json').write_text(json.dumps({'runs':runs,'errors':errors},indent=2),encoding='utf-8')
    print({k:result[k] for k in ['stage','diff','state','deaths','bossSeen','maxEnemy','maxBullet']},flush=True)
  br.close()
finally:stop()
assert not errors,errors
assert all(r['finite'] for r in runs)
