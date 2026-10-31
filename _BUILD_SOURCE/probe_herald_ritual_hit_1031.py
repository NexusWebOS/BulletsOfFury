from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/herald_ritual_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP,TRAP_RAF
http.server.ThreadingHTTPServer.request_queue_size=256;errors=[];checks=[]
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print('PASS'if v else'FAIL',n,d if not v else'')
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=8;stageLoadBegin(8)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)}',timeout=240000);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:8,role:'mini',kind:'heralddeath'},{pilot:'cole',record:false});spawnSubBoss('heralddeath');debugFight.spawned=true;subBossActive=true;warnT=0;DBGT.god=true;player.invuln=1e9;BOFCinematicDirector.cancel();story=null;setState(GS.PLAY);window.B=subBoss;}")
  for i in range(12):p.evaluate(STEP,15)
  p.evaluate("()=>{hr28Start(B,'storm')}")
  for i in range(10):p.evaluate(STEP,15)
  d=p.evaluate("""()=>{const part=hd1003Part(B,'wingL'),pt=hd1003Pose(B,part),hp=part.hp;B.flash=0;for(const q of B._hd1003.parts)q.flash=0;ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);heraldDeathDraw(B);const before=ctx.getImageData(0,0,cv.width,cv.height).data;hd1003Hit(B,5,pt.x,pt.y,'wingL');const fn=hh52Blit,calls=[];hh52Blit=function(...a){calls.push(a);return fn.apply(this,a)};ctx.clearRect(0,0,cv.width,cv.height);try{heraldDeathDraw(B)}finally{hh52Blit=fn}const after=ctx.getImageData(0,0,cv.width,cv.height).data;ctx.restore();let changed=0,whiteAfter=0;for(let i=0;i<before.length;i+=4)if(after[i]>240&&after[i+1]>240&&after[i+2]>240){whiteAfter++;if(before[i]+before[i+1]+before[i+2]<650)changed++;}return{hp,after:part.hp,white:changed,whiteAfter,flash:part.flash,bflash:B.flash,clip:hh52PoseBank(B),alpha:ctx.globalAlpha,calls};}""")
  ck('Native part damage still produces real white casting pixels',d['after']<d['hp']and d['white']>8,d)
  p.evaluate(STEP,20);ck('Part hit flash expires without interrupting the seal',p.evaluate("hd1003Part(B,'wingL').flash<=0&&!!hr92Own(B)"))
  p.evaluate("()=>{hr28Start(B,'storm');HR92.reduced=true}");
  for i in range(7):p.evaluate(STEP,15)
  d=p.evaluate("""()=>{const f=hr92Blit,a=[];hr92Blit=(...v)=>a.push(v);try{heraldDeathDraw(B)}finally{hr92Blit=f}return a;}""")
  ck('Reduced-motion warning holds red instead of the white flash',any(x[0]=='warning'and x[1]==2 for x in d)and not any(x[0]=='warning'and x[1]==3 for x in d),d)
  ck('Only one source owns the new seal',p.evaluate('!B._hd1003.er28._hr87Seal&&B._hd1003.er28.warm===11.65'))
  p.evaluate('HR92.reduced=false');ck('No extra native browser exceptions',not errors,errors);br.close()
finally:stop()
(W/'extra-checks.json').write_text(json.dumps(checks,indent=2));assert all(q['passed']for q in checks)
