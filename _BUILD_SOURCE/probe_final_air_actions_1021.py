from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,ast,json,http.server,argparse
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/final_version_1021/air-actions';O.mkdir(parents=True,exist_ok=True);ap=argparse.ArgumentParser();ap.add_argument('--browser',default='msedge');a=ap.parse_args();checks=[];errors=[]
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
def ck(name,ok,data=None):checks.append(dict(name=name,ok=bool(ok),data=data));(O/(a.browser+'.json')).write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.firefox.launch() if a.browser=='firefox' else pw.chromium.launch(channel=a.browser);p=br.new_page(viewport=dict(width=1440,height=1000));p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None);p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  models=p.evaluate('Object.entries(AF21_ART.models).filter(([id,m])=>!m.aliases.some(a=>["nyx","rook","kaia","jace","voss"].includes(a))).map(([id,m])=>({id,stage:m.stages[0],type:m.aliases[0]}))')
  for m in models:
   p.evaluate(SETUP,dict(stage=m['stage'],pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}');p.evaluate('''type=>{window.E=spawnEnemy(type,worldWidth()/2,220,{});E.x=worldWidth()/2;E.y=220;E.hp=E.maxhp=Math.max(40,E.hp);E._scaleIn=E._spawnScale=null;}''',m['type'])
   for kind in ['idle','drift','attack','roll','somer']:
    row=p.evaluate('''kind=>{E._af21Rendered=null;E.flash=0;E._air13Motion=['roll','somer'].includes(kind)?{kind,t:.32,dur:.72}:null;E._barrelT=0;E.vx=kind==='drift'?1:0;E.spin=0;E.fireCd=999;E._af21FireAt=kind==='attack'?efxClock:-999;E._af21LastCd=999;ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);drawEnemy(E);return E._af21Rendered;}''',kind);ck(m['id']+' selects '+kind,row is not None and row['kind']==kind,row)
  ck('no renderer errors',not errors,errors);br.close()
finally:stop()
print(json.dumps(dict(checks=len(checks),passed=sum(q['ok'] for q in checks),errors=errors)));sys.exit(bool(errors) or not all(q['ok'] for q in checks))
