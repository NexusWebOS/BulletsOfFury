from pathlib import Path
import sys,ast,json,base64,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/final_version_1021';O.mkdir(exist_ok=True,parents=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
port,stop=shoot.serve(str(R));errors=[];rows=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport=dict(width=1366,height=900));p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for stage in [1,5,6]:
   p.evaluate(SETUP,dict(stage=stage,pilot='yuri'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}');p.evaluate('BOFCinematicDirector.cancel();story=null;run.spaceMode=run.stage===5;run._earnedUnlocks={chaingun:true};chaingunUnlocked=true;run._chainSeeded=true;run.loadout=[7,1,2,3,4,5,6];')
   for weapon in range(8):
    row=p.evaluate('''w=>{const P=forgePreviewNew(w,'fire',w===7?1:3),samples=[];for(let i=0;i<180;i++){forgePreviewTick(P,260,300,1/60);if(i%6===0){ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#06101b';ctx.fillRect(0,0,VW,VH);forgePreviewDraw(P,30,30,260,300);}if(i%15===0)samples.push(P.bullets.map(b=>({k:b.kind,x:b.x,y:b.y,vx:b.vx,vy:b.vy,side:run._chainSide})));}return{stage:run.stage,w,err:P.err,fired:P.fired,samples,restored:{space:run.spaceMode,weapon:run.weapon,stage:run.stage}};}''',weapon);rows.append(row)
    if weapon==7:(O/f'forge-before-s{stage}-chain.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
  for diff in ['easy','normal','hard','furious']:
   p.evaluate(SETUP,dict(stage=5,pilot='cole',kind='siegebomber',mini=True,diff=diff));row=p.evaluate('''()=>{B._bomber.mode='recover';const C=B._bomber,initial={core:C.core,parts:C.parts.map(p=>[p.id,p.hp]),hp:B.hp};siegeBomberHit(B,C.core,NaN,NaN,'core');return{diff:diffKey,initial,after:{core:C.core,hp:B.hp,dead:B.dead,liveParts:C.parts.filter(p=>p.hp>0).length}};}''');rows.append(row)
  (O/'bug-audit.json').write_text(json.dumps(dict(rows=rows,errors=errors),indent=2),encoding='utf-8');br.close()
finally:stop()
print(json.dumps({'rows':len(rows),'errors':errors,'summary':[{'stage':r['stage'],'w':r['w'],'err':r['err'],'fired':r['fired'],'last':r['samples'][-1][:3]} if 'w' in r else r for r in rows]}))
