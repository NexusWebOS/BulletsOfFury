"""Native Chromium regression proof for Stage 8's actual boss identities."""
from pathlib import Path
import ast,json,http.server,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage8_identity_1018/native';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];rows=[];http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof V19!=="undefined"');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(40)
  p.evaluate("pilotIndex=PILOTS.findIndex(q=>q.key==='cole');run.pilot='cole';startRun(8)")
  p.evaluate('''()=>{window.vHits=0;playerHit=function(){vHits++;};window.vPixels=fn=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const a=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return a;};
  window.vChanged=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)n++;return n;};}''')
  def frames(n):
   for i in range(0,n,12):
    p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);debugRecFrame();}}',min(12,n-i));p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}');p.screenshot(path=str(O/(name+'.png')))
  def setup(phase=2,form=0,diff='normal'):
   p.evaluate(SETUP,dict(stage=8,diff=diff,kind='vileexistence',pilot='cole'))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&bmfReady("game")}')
   p.evaluate('''([phase,form])=>{s6Opening=null;story=fb2Talk=fb2Intro=null;BOFCinematicDirector.cancel();AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;
    stagePlan=[];warnT=0;warnKind=null;subBossDone=true;subBossTriggered=aminiTriggered=true;enemies=[];powerups=[];eBullets=[];pBullets=[];
    v18Budget(B);v18Enter(B,phase,form);B._r30.v18.arenaPhase=phase;v18Fight(B);player.x=worldWidth()/2;player.y=VH-70;player.invuln=0;run.shield=0;run.spaceMode=false;bossWarned=true;bossDefeated=false;
    for(const k of ['j','k','y','a','d','w','s'])Input.keys[k]=false;V19.events=[];V19.draws={};V18.events=[];__bofFit();}''',[phase,form])
  for diff in (['normal'] if '--smoke' in sys.argv else ['normal','hard','furious']):
   for phase,form in ([(2,6)] if '--harrier' in sys.argv else [(2,2)] if '--volcano' in sys.argv else [(2,8),(2,2),(2,6),(2,0),(0,0),(1,0),(2,1)]):
    setup(phase,form,diff)
    p.evaluate('()=>{if(j3State(B).encounter===2)for(const i of V18.forms)if(i!==B._r30.v18.form)j3State(B).hp[i]=0;}')
    frames(180 if '--smoke' in sys.argv else 1800)
    row=p.evaluate('''()=>({form:B._r30.v18.form,phase:j3State(B).encounter,diff:diffKey,mode:B._r30.mode,parts:B.parts.map(p=>p.id),states:V19.events.filter(e=>e.event==='donor-state').map(e=>e.state),attacks:V19.events.filter(e=>e.event==='organic-release').map(e=>e.type),shots:eBullets.length,draws:Object.keys(V19.draws),hp:B.hp,targets:retinaBossTargets(B).length})''');rows.append(row)
    check(diff+' '+str(phase)+':'+str(form)+' owns a finite active fight',row['mode']=='fight' and row['hp']>0,row)
    if form in [8,2,6]:check(diff+' '+str(form)+' uses native donor controller',len(row['states'])>0,row)
    if diff=='normal':snap(str(phase)+'-'+str(form))
    # Stable simulation clock makes this real hit pixel proof, not animation.
    hit=p.evaluate('''()=>{const v=v18Rig(B).find(v=>v.p.id===(B._r30.v18.form===2?'left':'core'));const a=vPixels(()=>r30DrawBoss(B)),hp=B.hp;B._lastPart=v.p;hitBoss(1);const c=vPixels(()=>r30DrawBoss(B));return{hp:hp-B.hp,pixels:vChanged(a,c),flash:v.p.flash,owner:B.flash};}''')
    check(diff+' '+str(form)+' native damage visibly flashes actual pixels',hit['hp']>=0 and hit['pixels']>20 and hit['flash']>0 and hit['owner']>0,hit)
    frames(18);check(diff+' '+str(form)+' hit flash expires',p.evaluate('B.flash<=0&&B.parts.every(p=>p.flash<=0)'))
  check('no native page, console, draw or asset errors',not errors,errors[:30])
  br.close()
finally:stop()
result=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,rows=rows,errors=errors)
(O/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:result[k] for k in ['passed','failed','errors']}));sys.exit(1 if result['failed'] else 0)
