"""Native late-stage hull weights, real projectile hit pixels and flash expiry."""
from pathlib import Path
import argparse,ast,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019';checks=[];errors=[];rows=[]
ap=argparse.ArgumentParser();ap.add_argument('--stage',type=int,choices=[5,9],default=9);a=ap.parse_args();STAGE=a.stage;REPORT='stage5-hulls-native.json' if STAGE==5 else 'late-hulls-native.json'
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=128
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("n=>{pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.pilot='cole';startRun(n);}",STAGE)
  def frames(n):
   for i in range(0,n,12):p.evaluate(shoot.STEP,min(12,n-i));p.wait_for_timeout(5)
  for diff in ['normal','hard','furious']:
   p.evaluate(SETUP,dict(stage=STAGE,diff=diff,pilot='cole'))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}',polling=50)
   p.evaluate('''()=>{BOFCinematicDirector.cancel();AP10_X.intro=null;story=fb2Talk=fb2Intro=thaw=s6Opening=null;H3.release=false;H3.ending=null;P2M.active=null;run.spaceMode=true;run.shield=0;special=thunderStorm=null;run.sonicT=run.dkT=0;playerHit=()=>{};Input.keys={};Input.mouse.down=false;
    VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;stagePlan=[];spawnClock=999999;subBossDone=subBossTriggered=aminiTriggered=bossWarned=true;warnT=0;powerups=[];
    window.le19Snap=(hullOnly=false)=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);if(hullOnly){if(run.stage===5)drawS5Space(E);else drawS9Void(E);}else drawEnemy(E);const a=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return a;};}''')
   kinds=p.evaluate('Object.keys(run.stage===5?S5SPACE:S9VOID)')
   for kind in kinds:
    row=p.evaluate('''kind=>{enemies=[];eBullets=[];pBullets=[];const flag=run.stage===5?'CA19_OFF':'LE19_OFF',spec=run.stage===5?S5SPACE:S9VOID;window[flag]=1;spawnEnemy(kind,worldWidth()/2,130,{});const before=enemies.at(-1).hp;enemies=[];window[flag]=0;spawnEnemy(kind,worldWidth()/2,130,{});window.E=enemies.at(-1);player.x=E.x;player.y=VH-80;camX=clamp(player.x-VW/2,0,worldWidth()-VW);return{kind,before,after:E.hp,authored:spec[kind].hp,hasPool:run.stage===5?!!E._ca19Hp:E._le19HP,flash:E.flash};}''',kind);row['difficulty']=diff;rows.append(row)
    ck(diff+' '+kind+' retains authored hull weight and positive native difficulty scaling',row['hasPool'] and row['after']>=row['authored'] and row['after']>row['before'],row)
    frames(18);p.wait_for_function('()=>Object.values(XART.img).every(im=>!im||im.complete!==false)',polling=50)
    # Actual native projectile collision, using a low-damage QA chip round to
    # keep every target alive for the pixel/expiry comparison. Not a DPS test.
    p.evaluate('''()=>{player.x=E.x;player.y=E.y+80;window.le19Before=E.hp;pBullets=[];spaceLaserFire();for(const q of pBullets){q.x=E.x;q.y=E.y+8;q.vx=0;q.vy=-1;q.dmg=.25;}Input.keys={};}''');frames(1)
    flash=p.evaluate('''()=>{const old=E.flash;E.flash=0;const a=le19Snap();E.flash=old;const b=le19Snap();let pixels=0;for(let i=0;i<a.length;i+=4)if(b[i+3]>80&&Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>15)pixels++;return{loss:le19Before-E.hp,timer:old,pixels,dead:E.dead};}''')
    ck(diff+' '+kind+' real projectile damage changes actual hit pixels',flash['loss']>0 and flash['timer']>0 and flash['pixels']>10 and not flash['dead'],flash)
    p.evaluate('pBullets=[];player.x=camLeftX()+20;player.y=VH-30;');frames(30)
    expired=p.evaluate('''()=>{const timer=E.flash,actual=le19Snap(true);E.flash=0;const clean=le19Snap(true);E.flash=timer;let changed=0,totalError=0,ink=0,whiteActual=0,whiteClean=0;for(let i=0;i<actual.length;i+=4){const delta=Math.max(Math.abs(actual[i]-clean[i]),Math.abs(actual[i+1]-clean[i+1]),Math.abs(actual[i+2]-clean[i+2]));if(delta>5)changed++;totalError+=Math.abs(actual[i]-clean[i])+Math.abs(actual[i+1]-clean[i+1])+Math.abs(actual[i+2]-clean[i+2]);if(Math.max(actual[i],actual[i+1],actual[i+2],clean[i],clean[i+1],clean[i+2])>16)ink++;if(Math.min(actual[i],actual[i+1],actual[i+2])>224)whiteActual++;if(Math.min(clean[i],clean[i+1],clean[i+2])>224)whiteClean++;}return{timer,changed,normalizedError:totalError/Math.max(1,ink*3*255),whiteActual,whiteClean};}''')
    # Keep native timers untouched. Check the actual hull owner separately
    # from rotating warning overlays. Positive damage above uses drawEnemy.
    # Fractional minified hulls can change a few edge texels on readback.
    # A persistent hit wash cannot pass either mean-color or white-area check.
    ck(diff+' '+kind+' hit flash expires on native clock and pixels return to authored palette',expired['timer']<=0 and expired['normalizedError']<.005 and abs(expired['whiteActual']-expired['whiteClean'])<=max(3,expired['whiteClean']*.03),expired)
  heavy='s5station' if STAGE==5 else 's9gunship';light='s5interceptor' if STAGE==5 else 's9interceptor'
  ck('Authored heavy hulls remain heavier than interceptors on every difficulty',all(next(r['after'] for r in rows if r['kind']==heavy and r['difficulty']==d)>next(r['after'] for r in rows if r['kind']==light and r['difficulty']==d) for d in ['normal','hard','furious']))
  br.close()
finally:stop()
ck('No page/console/draw/asset errors',not errors,errors);report=dict(stage=STAGE,passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,rows=rows,errors=errors);(O/REPORT).write_text(json.dumps(report,indent=2)+'\n');sys.exit(report['failed']>0)
