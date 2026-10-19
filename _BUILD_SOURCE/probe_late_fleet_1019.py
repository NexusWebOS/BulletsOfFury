"""Native late-heavy hull weights, incoming projectile boundary and hit pixels."""
from pathlib import Path
import ast,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/late-fleet';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];rows=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  def frames(n):
   for i in range(0,n,12):p.evaluate(shoot.STEP,min(12,n-i));p.wait_for_timeout(5)
  for stage in [7,8]:
   for diff in ['normal','hard','furious']:
    p.evaluate(SETUP,dict(stage=stage,diff=diff,pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}',polling=50)
    p.evaluate('''()=>{BOFCinematicDirector.cancel();AP10_X.intro=null;story=fb2Talk=fb2Intro=thaw=s6Opening=null;H3.release=false;H3.ending=null;P2M.active=null;special=thunderStorm=null;run.sonicT=run.dkT=0;run.spaceMode=false;run.shield=0;playerHit=()=>{};
     VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;stagePlan=[];spawnClock=999999;subBossDone=subBossTriggered=aminiTriggered=bossWarned=true;warnT=0;powerups=[];for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.mouse.down=false;
     run.weapon=0;run.wlevel=0;run.wlevels=WEAPONS.map(()=>0);run.loadout=[0];run.forge={};run.forgeForms={};run.infusion=null;weaponFormSelect(0,{kind:'primary1003b',id:'mg'});run.wlevel=0;
     window.lf19Snap=(hull=false)=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.setTransform(SS,0,0,SS,-camX*SS,0);if(!hull)drawEnemy(E);else if(E._modTank)drawModularTank(E);else if(run.stage===7)drawS7Toxic(E);else drawS8Mega(E);const a=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return a;};
     window.lf19Total=()=>E.hp+(E._esh?.energy||0);
     window.lf19Round=()=>{pBullets=[];player.x=E.x;player.y=E.y+70;pShoot();for(const b of pBullets){b.x=E.x;b.y=E.y+6;b.vx=0;b.vy=-1;b.dmg=.25;}};
    }''')
    kinds=['s7tank','s7barge'] if stage==7 else ['s8deathorb','s8carrier','s8bomber','s8tentacle']
    for kind in kinds:
     row=p.evaluate('''kind=>{for(const e of enemies)e.dead=true;aiQueue=[];enemies=[];eBullets=[];pBullets=[];window.LF19_OFF=1;spawnEnemy(kind,worldWidth()/2,130,{});const before=enemies.at(-1).hp;enemies=[];window.LF19_OFF=0;spawnEnemy(kind,worldWidth()/2,130,{});window.E=enemies.at(-1);player.x=E.x;player.y=VH-80;camX=clamp(player.x-VW/2,0,worldWidth()-VW);return{kind,before,after:E.hp,authored:lf19Spec(E).hp,flag:!!E._lf19Hp};}''',kind);row.update(stage=stage,difficulty=diff);rows.append(row)
     ck(diff+' '+kind+' retains authored weight with native difficulty ratio',row['flag'] and row['after']>=row['authored'] and row['after']>row['before'],row)
     frames(18);p.wait_for_function('()=>Object.values(XART.img).every(im=>!im||im.complete!==false)',polling=50)
     p.evaluate('window.lfHP=lf19Total();window.lfClean=lf19Snap();lf19Round()');frames(1)
     hit=p.evaluate('''()=>{const b=lf19Snap();let white=0;for(let i=0;i<b.length;i+=4)if(b[i+3]>64&&Math.min(b[i],b[i+1],b[i+2])>160&&Math.min(lfClean[i],lfClean[i+1],lfClean[i+2])<120)white++;return{loss:lfHP-lf19Total(),timer:E.flash,white};}''')
     ck(diff+' '+kind+' primary hits native hull/shield and visibly flashes',hit['loss']>0 and hit['timer']>0 and hit['white']>10,hit)
     p.evaluate('pBullets=[];player.x=camLeftX()+20;player.y=VH-30');frames(30)
     expired=p.evaluate('''()=>{const timer=E.flash,a=lf19Snap(true);E.flash=0;const b=lf19Snap(true);E.flash=timer;let error=0,ink=0;for(let i=0;i<a.length;i+=4){error+=Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2]);if(Math.max(a[i],a[i+1],a[i+2],b[i],b[i+1],b[i+2])>16)ink++;}return{timer,error:error/Math.max(1,ink*3*255)};}''')
     ck(diff+' '+kind+' native flash expires to authored hull pixels',expired['timer']<=0 and expired['error']<.005,expired)
     boundary=[]
     for off in [0,1]:
      p.evaluate('off=>{window.LF19_OFF=off;E.y=-30;E._noHit=false;window.lfHP=lf19Total();lf19Round();}',off);frames(1);boundary.append(p.evaluate('lfHP-lf19Total()'))
     p.evaluate('window.LF19_OFF=0;pBullets=[];E.y=130')
     ck(diff+' '+kind+' rejects offscreen projectile contacts; disabled control really damages',boundary[0]==0 and boundary[1]>0,boundary)
     p.evaluate('E.y=8;window.lfHP=lf19Total();lf19Round()');frames(1);topBand=p.evaluate('lfHP-lf19Total()');p.evaluate('pBullets=[];E.y=130')
     ck(diff+' '+kind+' still accepts primary hits in the visible top band above PLAY.y',topBand>0,topBand)
     muzzle=p.evaluate('''()=>{const advance=()=>{for(let i=0;i<40;i++){const old=ai27Begin(E,1/60);ai27Context=old;}};E.y=PLAY.y-Math.max(E._drawH||E.h,E.h)*2;advance();const hidden={ready:E._ai27.visible,seen:E._ai27.seen};E.y=PLAY.y-8;const p=E._modTank?modularTankMuzzle(E):combatHardpoint(E,0,.31);advance();const a={muzzle:p.y,center:E.y,top:PLAY.y,ready:E._ai27.visible,seen:E._ai27.seen,hidden};E.y=130;return a;}''')
     ck(diff+' '+kind+' stays unready while its muzzle is outside the playfield',not muzzle['hidden']['ready'] and muzzle['hidden']['seen']==0,muzzle)
     ck(diff+' '+kind+' can warn after its real muzzle enters ahead of the hull center',muzzle['muzzle']>=muzzle['top']+8 and muzzle['center']<muzzle['top'] and muzzle['ready'] and muzzle['seen']>.5,muzzle)
     if diff=='normal':p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit()');p.screenshot(path=str(O/(kind+'.jpg')),type='jpeg',quality=78)
    scout='s7pipe' if stage==7 else 's8interceptor'
    control=p.evaluate('''kind=>{enemies=[];window.LF19_OFF=1;spawnEnemy(kind,worldWidth()/2,130,{});const before=enemies.at(-1).hp;enemies=[];window.LF19_OFF=0;spawnEnemy(kind,worldWidth()/2,130,{});const e=enemies.at(-1);return{before,after:e.hp,flag:!!e._lf19Hp};}''',scout)
    ck(diff+' '+scout+' keeps native scout health',control['before']==control['after'] and not control['flag'],control)
  br.close()
finally:stop()
ck('No page, console, draw or asset errors',not errors,errors);report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,rows=rows,errors=errors);(O/'native-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');sys.exit(report['failed']>0)
