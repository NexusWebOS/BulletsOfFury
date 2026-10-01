import sys,json,time,http.server,base64
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
OUT=ROOT/'_shots/repair_0930';OUT.mkdir(parents=True,exist_ok=True)
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
port,stop=sh.serve(sh.GAME);errors=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page()
 p.on('pageerror',lambda e:errors.append(str(e)))
 p.on('console',lambda m:errors.append(m.text) if 'draw error' in m.text or m.type=='error' else None)
 p.goto('http://127.0.0.1:%s/index.html'%port,timeout=120000);p.wait_for_function('() => (window.__bofFrames|0)>4');p.evaluate(sh.TRAP_RAF)
 p.evaluate("""() => {run.pilot='yuri';run.mode='campaign';beginStage(6);setState(GS.STAGECLEAR);drawStageClear._init=false;stateT=1.4;run.score=9876543;stageStats.kills=112;stageStats.shots=1945;stageStats.hits=901;drawStageClear(.016);} """)
 p.wait_for_timeout(2500)
 r=p.evaluate("""() => {let d=0,solid=0,tint=0;const draw=ctx.drawImage,s=drawFrameSolid,t=drawFrameTinted;
 ctx.drawImage=function(){d++;return draw.apply(this,arguments);};drawFrameSolid=function(){solid++;return s.apply(this,arguments);};drawFrameTinted=function(){tint++;return t.apply(this,arguments);};
 let times=[];for(let i=0;i<24;i++){stateT=1.35+i/60;let at=performance.now();drawStageClear(1/60);ctx.getImageData(0,0,1,1);times.push(performance.now()-at);}
 ctx.drawImage=draw;drawFrameSolid=s;drawFrameTinted=t;
 return {ms:times.reduce((a,b)=>a+b)/times.length,max:Math.max(...times),draws:d/24,solid:solid/24,tint:tint/24,score:drawStageClear._scoreShown,rank:drawStageClear._stamp};}""")
 report={'profile':r,'errors':errors};print(json.dumps(report));(OUT/'stats_profile.json').write_text(json.dumps(report,indent=2));(OUT/'stats_tally.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL()').split(',')[1]));b.close()
stop()
