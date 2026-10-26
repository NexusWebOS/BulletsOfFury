"""Native Chromium helpers shared by the October25 barrage corrections."""
from pathlib import Path
from shoot import TRAP_RAF, STEP
import http.server

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/barrage_revision_1025'
OUT.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.protocol_version='HTTP/1.1'
http.server.ThreadingHTTPServer.request_queue_size=128

def boot(context,port,stage,errors,role='mini'):
    p=context.new_page()
    p.on('pageerror',lambda e:errors.append(str(e)))
    p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
    p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000)
    p.wait_for_function('window.__bofFrames>5&&typeof BH25!=="undefined"',timeout=180000)
    p.mouse.click(3,3)
    p.evaluate(TRAP_RAF)
    p.evaluate("""([s,r])=>{debugUnlocked=true;diffKey='furious';debugStartFight(debugFightFor(s,r),{pilot:'cole'});
      if(r==='mini')spawnSubBoss(debugFightFor(s,r).kind);else spawnBoss(debugFightFor(s,r).kind);
      debugFight.spawned=true;warnT=0;DBGT.god=true;DBGT.speed=1;player.invuln=1e9;player.x=worldWidth()/2;player.y=VH-65;
      BOFCinematicDirector.cancel();setState(GS.PLAY);for(const k of Object.keys(Input.keys))Input.keys[k]=false;
      BH25.events=[];window.reviewActor=r==='mini'?subBoss:boss;}""",[stage,role])
    p.wait_for_function('(s)=>{stageLoadTick();return stageLoadReady(s)}',arg=stage,timeout=180000)
    if stage==6:p.wait_for_function('()=>{sc13Warm();return SC13.keys.every(k=>XART.rdy(k))}',timeout=180000)
    return p

def advance(p,expression,limit=700,frames=20):
    for i in range(limit):
        p.evaluate(STEP,frames)
        if p.evaluate(expression):return True
        if i%8==0:p.wait_for_timeout(1)
    return False
