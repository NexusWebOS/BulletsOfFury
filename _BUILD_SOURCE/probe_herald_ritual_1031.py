from pathlib import Path
import sys,json,http.server,math
from playwright.sync_api import sync_playwright
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/herald_ritual_1031';W.mkdir(parents=True,exist_ok=True);O=W/'probe';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP,TRAP_RAF
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,str(d)[:350]if not v else'',flush=True)
def step(p,n):
 for i in range(0,n,15):
  e=p.evaluate(STEP,min(15,n-i));assert not e,e;p.wait_for_timeout(1)
def until(p,t):
 for _ in range(2000):
  if p.evaluate('(t)=>A.t>=t',t):return
  step(p,1)
 raise RuntimeError('Attack clock stalled')
def calls(p):return p.evaluate("""()=>{const h=hr92Blit,o=hh69Blit,s=hs53Blit,out=[];hr92Blit=function(...a){out.push(['new',...a]);return h.apply(this,a)};hh69Blit=function(...a){out.push(['old',...a]);return o.apply(this,a)};hs53Blit=function(...a){out.push(['source',...a]);return s.apply(this,a)};try{heraldDeathDraw(B)}finally{hr92Blit=h;hh69Blit=o;hs53Blit=s}return out;}""")
def snap(p,n):p.evaluate('drawWorld(0)');p.screenshot(path=str(O/(n+'.png')))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=8;stageLoadBegin(8)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)}',timeout=240000);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:8,role:'mini',kind:'heralddeath'},{pilot:'cole',record:false});spawnSubBoss('heralddeath');debugFight.spawned=true;subBossActive=true;warnT=0;DBGT.god=true;player.invuln=1e9;BOFCinematicDirector.cancel();story=null;setState(GS.PLAY);window.B=subBoss;pBullets=[];eBullets=[];}");step(p,150)
  ck('All authored seal, lightning and warning banks preload',p.evaluate('Object.values(HR92_ART).every(a=>XART.rdy(a.key))'))
  p.evaluate("()=>{window.bgmean=()=>{drawBG(0);const d=ctx.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<d.length;i+=4)n+=d[i]+d[i+1]+d[i+2];return n/d.length*4/3};window.beforeDark=bgmean();hr28Start(B,'storm');window.A=B._hd1003.er28;window.Q=A._hr92;window.full=B.hp;HR92.events=[];HH52.events=[];HR87.draws={};}")
  ck('Native attack waits for the full11.65second ritual',p.evaluate('A.warm===11.65&&!A._hr87Seal'))
  until(p,.80);d=calls(p);ck('Warning stays ahead of the inscription',not any(q[0]=='new'and q[1]in['inscribe','spin','expand','shatter']for q in d));ck('Scene pixels darken strongly before the first line',p.evaluate('bgmean()<beforeDark*.50'),p.evaluate('({before:beforeDark,after:bgmean(),level:Q.dark})'));snap(p,'01-yellow-warning')
  until(p,1.4);d=calls(p);ck('Warning becomes solid red before the flash',any(q[0]=='new'and q[1]=='warning'and q[2]==2 for q in d),d[:3])
  until(p,1.72);d=calls(p);ck('The final red warning visibly flashes white',any(q[0]=='new'and q[1]=='warning'and q[2]==3 for q in d));ck('No line appears during the official warning flash',not any(q[0]=='new'and q[1]=='inscribe'for q in d));snap(p,'02-official-flash')
  until(p,2.10);ck('No slice is scheduled before the warning completes',p.evaluate('Q.stroke===0&&!HR92.events.some(e=>e.event==="line-slice")'))
  until(p,2.38);d=calls(p);ck('The first larger stroke appears after the final warning',any(q[0]=='new'and q[1]=='inscribe'and q[2]<12 for q in d));ck('The old warning does not overlap the drawn star',not any(q[0]=='new'and q[1]=='warning'for q in d));ck('The blade stroke and lightning share one simulation event',p.evaluate('Q.stroke===1&&Q.thunder===1&&Q.bolts.length===3'));snap(p,'03-first-slice')
  ck('Tornadoes remain absent during inscription',not any(q[0]=='old'and q[1]in['arrive','flash','depart']for q in d))
  before=p.evaluate('({t:A.t,n:HR92.events.length,hp:B.hp})');p.evaluate('setState(GS.PAUSE)');step(p,90);ck('Pause freezes inscription and emits no extra cues',p.evaluate('A.t')==before['t']and p.evaluate('HR92.events.length')==before['n']);p.evaluate('setState(GS.PLAY)')
  until(p,4.40);snap(p,'04-three-lines');d=calls(p);ck('Line3 selects its own authored stroke frames',any(q[0]=='new'and q[1]=='inscribe'and 24<=q[2]<36 for q in d));ck('Charging skull uses its existing animated glowing face',any(q[0]=='source'and q[1]=='head_cast'for q in d))
  until(p,6.45);snap(p,'05-five-lines');ck('Exactly five sword strokes precede the circle',p.evaluate('Q.stroke===5'))
  until(p,7.82);d=calls(p);snap(p,'06-circle-complete');ck('Circle forms as a distinct final inscription',any(q[0]=='new'and q[1]=='inscribe'and q[2]>=80 for q in d))
  ev=p.evaluate('HR92.events.filter(e=>e.event==="line-slice"||e.event==="circle-slice")');ck('All six loud slices are exactly one second apart',len(ev)==6 and all(abs(b['t']-a['t']-1)<.04 for a,b in zip(ev,ev[1:])),ev)
  ck('Each inscription owns a lightning release',p.evaluate('HR92.events.filter(e=>e.event==="line-lightning").length===6'))
  until(p,9.35);d=calls(p);snap(p,'07-accelerating-1015-spin');ck('Completed glowing seal spins before expansion',any(q[0]=='new'and q[1]=='spin'for q in d));ck('Native warmup still prevents any tornado contact or volley',p.evaluate('A.t<A.warm&&!HH52.events.some(e=>e.event==="tornado-volley")'))
  until(p,10.85);d=calls(p);snap(p,'08-expanded-seal');ck('Seal expansion uses authored larger frames',any(q[0]=='new'and q[1]=='expand'and q[2]>20 for q in d))
  until(p,11.13);d=calls(p);snap(p,'09-exact-seal-shards');ck('The actual seal shatters before the funnels arrive',any(q[0]=='new'and q[1]=='shatter'for q in d)and not any(q[0]=='old'and q[1]=='arrive'for q in d));ck('Shatter sound is scheduled only once',p.evaluate('HR92.events.filter(e=>e.event==="seal-shatter").length===1'))
  until(p,11.45);d=calls(p);snap(p,'10-funnels-form');ck('Authored tornado arrival follows the seal explosion',any(q[0]=='old'and q[1]=='arrive'for q in d))
  until(p,11.86);d=calls(p);snap(p,'11-native-tornado-volley');ck('Native tornado attacks release after the entire ritual',p.evaluate('HH52.events.some(e=>e.event==="tornado-volley")&&A.phase==="active"'))
  ck('No old fast inscription draws underneath the new seal',p.evaluate('Object.keys(HR87.draws).length===0'))
  ck('Casting preserves original HP until player attacks',p.evaluate('B.hp===full'))
  for _ in range(160):
   if not p.evaluate('!!hr92Own(B)'):break
   step(p,5)
  ck('Native recovery relinquishes the special instead of looping',p.evaluate('!hr92Own(B)'))
  ck('Caster and storm leave no renderer exceptions',not errors,errors)
  p.evaluate("hr28Start(B,'storm')");step(p,150);p.evaluate('()=>{B.dead=true;updatePlay(1/60)}');ck('Death cancels owned casting audio and visuals',p.evaluate('!HR92.owner&&!hr92Own(B)'))
  p.evaluate("()=>{beginStage(1);BOFCinematicDirector.cancel();setState(GS.PLAY)}");step(p,3);ck('Stage change clears the ritual and ducking',p.evaluate('!HR92.owner&&!HR92.ducked'))
  (W/'events.json').write_text(json.dumps(ev,indent=2));br.close()
finally:stop()
print('RESULT',sum(q['passed']for q in checks),'/',len(checks));assert all(q['passed']for q in checks)
