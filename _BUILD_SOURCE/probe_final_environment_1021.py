from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,ast,json,base64,http.server
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/final_version_1021/environment';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
def ck(name,ok,data=None):checks.append(dict(name=name,ok=bool(ok),data=data));(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport=dict(width=1440,height=1000));p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for diff in ['easy','normal','hard','furious']:
   p.evaluate(SETUP,dict(stage=4,kind='stormsovereign',pilot='cole',diff=diff));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(4)}')
   row=p.evaluate('''()=>{const S=B._s4war,H=S.shield;S.mode='swerve';S.t=0;S.ram=null;S.coreEnrage=null;S.giantStrike=null;H.active=false;H.rearming=false;B.x=worldWidth()/2;const xs=[];for(let i=0;i<240;i++){B.t+=1/60;stage4WarfareTick(B,1/60);xs.push(B.x);}H.active=false;H.rearming=true;H.rearmT=0;B.x=camRightX()-80;for(let i=0;i<90;i++)stage4WarfareTick(B,1/60);const nodes=H.nodes.map(n=>({x:n.x,y:n.y,side:n.side,hp:n.hp}));return{travel:Math.max(...xs)-Math.min(...xs),nodes,finite:nodes.every(n=>Number.isFinite(n.x+n.y)),inside:nodes.every(n=>n.x>=camLeftX()+12&&n.x<=camRightX()-12),center:B.x};}''');ck(diff+' Stage4 carrier drifts and regenerated cores remain inside the view',row['travel']>5 and row['finite'] and row['inside'],row)
  p.evaluate(SETUP,dict(stage=6,pilot='cole'));p.evaluate('run._gp4StageX="right";CC21.owner=null;CC21.t=0;');p.wait_for_function('stageXArenaReady()')
  row=p.evaluate('''()=>{const timer=stageTimer,scroll=mapScroll;for(let i=0;i<120;i++)updatePlay(1/60);return{protected:stageTimer===timer&&mapScroll===scroll,card:CC21.card};}''');ck('campaign StageX entrance protects gameplay during its card',row['protected'] and 1.9<row['card']<2.1,row)
  row=p.evaluate('''()=>{const im=XART.get(CC21_ART.key),A=CC21_ART,scale=worldWidth()/A.w,samples=[];for(const t of [0,10,35,70,110]){CC21.t=t;stageXArenaDraw(0);samples.push(stageXArenaSrcY());}function sample(v){ctx.save();try{ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,VW,2);cc21Strip(im,v,2,0,0,VW,1);return Array.from(ctx.getImageData(0,0,VW,2).data);}finally{ctx.restore();}}let max=0;for(const boundary of [0,-A.urban,-2*A.urban]){const pixels=sample(boundary-1);for(let i=0;i<VW*4;i++)max=Math.max(max,Math.abs(pixels[i]-pixels[VW*4+i]));}return{samples,seamDifference:max};}''');ck('city camera travels one direction and adjoining district rows match',all(row['samples'][i]>row['samples'][i+1] for i in range(4)) and row['seamDifference']==0,row)
  p.evaluate('CC21.t=0;stageXArenaDraw(0)');a1=p.evaluate('cv.toDataURL()');p.evaluate('CC21.t=.15;stageXArenaDraw(0)');a2=p.evaluate('cv.toDataURL()');ck('coastal water and layered scenery visibly animate',a1!=a2)
  for t in [0,36,93]:p.evaluate('t=>{CC21.t=t;ctx.setTransform(SS,0,0,SS,0,0);stageXArenaDraw(0)}',t);(O/f'city-{t}.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
  ck('no native environment errors',not errors,errors);br.close()
finally:stop()
print(json.dumps(dict(checks=len(checks),passed=sum(q['ok'] for q in checks),errors=errors)));sys.exit(bool(errors) or not all(q['ok'] for q in checks))
