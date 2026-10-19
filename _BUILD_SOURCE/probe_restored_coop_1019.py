"""Native restored-hull co-op scaling and real Player-2 projectile damage."""
from pathlib import Path
import argparse,ast,base64,json,http.server,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/restored-coop';O.mkdir(parents=True,exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--label',default='');ap.add_argument('--stages',default='5,7,8,9');ap.add_argument('--diffs',default='normal,hard,furious');ap.add_argument('--types',default='');args=ap.parse_args()
if args.label:O=O/args.label;O.mkdir(exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];rows=[];errors=[];port,stop=shoot.serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=128
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  def frames(n):
   for i in range(0,n,12):p.evaluate(shoot.STEP,min(12,n-i));p.wait_for_timeout(5)
  for stage in map(int,args.stages.split(',')):
   for diff in args.diffs.split(','):
    p.evaluate(SETUP,dict(stage=stage,diff=diff,pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}',polling=50)
    p.evaluate('''()=>{BOFCinematicDirector.cancel();AP10_X.intro=null;story=fb2Talk=fb2Intro=thaw=s6Opening=null;H3.release=false;H3.ending=null;P2M.active=null;special=thunderStorm=null;run.sonicT=run.dkT=0;run.shield=0;run.spaceMode=[5,9].includes(run.stage);playerHit=()=>{};stagePlan=[];spawnClock=999999;VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;subBossDone=subBossTriggered=aminiTriggered=bossWarned=true;warnT=0;powerups=[];groundTargetingReset();for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.mouse.down=false;
     window.rc19Kinds=()=>run.stage===5?Object.keys(S5SPACE):run.stage===9?Object.keys(S9VOID):[...LF19.heavy].filter(k=>k.startsWith('s'+run.stage));
     window.rc19Spawn=kind=>{for(const e of enemies)e.dead=true;enemies=[];aiQueue=[];pBullets=[];eBullets=[];spawnEnemy(kind,worldWidth()/2,130,{});window.E=enemies.at(-1);return E.hp;};
     window.rc19Total=()=>E.hp+(E._esh?.energy||0);
     window.rc19Snap=(hull=false)=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.setTransform(SS,0,0,SS,-camX*SS,0);if(!hull)drawEnemy(E);else if(E._s5space)drawS5Space(E);else if(E._modTank)drawModularTank(E);else if(E._s7toxic)drawS7Toxic(E);else if(E._s8mega)drawS8Mega(E);else drawS9Void(E);const a=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return a;};
    }''')
    for kind in p.evaluate('rc19Kinds()'):
     if args.types and kind not in args.types.split(','):continue
     row=p.evaluate('''kind=>{coopOn=false;window.LC19_OFF=0;const solo=rc19Spawn(kind);coopOn=true;window.LC19_OFF=1;const before=rc19Spawn(kind);window.LC19_OFF=0;const party=rc19Spawn(kind);
      p2Index=PILOTS.findIndex(q=>q.key==='decker');PILOTMOD2={...PILOTS[p2Index]};run2.pilot='decker';run2.weapon=0;run2.wlevel=0;run2.wlevels=WEAPONS.map(()=>0);run2.loadout=[0];run2.forge={};run2.forgeForms={};run2.infusion=null;run2.missileLevel=0;run2.shield=0;run2._primary1003b='mg';run2.dkT=run2.sonicT=0;
      withSeat(2,()=>{player.reset();player.x=E.x+55;player.y=VH-90;player.invuln=40002;player.fireCd=99999;});player.x=E.x-55;player.y=VH-90;player.invuln=40002;player.fireCd=99999;camX=clamp(E.x-VW/2,0,worldWidth()-VW);return{kind,solo,before,party,multiplier:COOP_EHP_MUL,ratio:party/solo,seats:seatList().length};}''',kind);row.update(stage=stage,difficulty=diff);rows.append(row)
     ck(diff+' '+kind+' restores the native party factor rather than canceling it',row['seats']==2 and row['party']>row['before'] and abs(row['ratio']-row['multiplier'])<.13 and (diff!='normal' or abs(row['party']-row['solo']*row['multiplier'])<=1),row)
     frames(16);p.wait_for_function('()=>Object.values(XART.img).every(im=>!im||im.complete!==false)',polling=50)
     shot=p.evaluate('''()=>{window.rcHP=rc19Total();window.rcClean=rc19Snap();pBullets=[];withSeat(2,()=>{player.x=E.x;player.y=E.y+80;player.fireCd=0;pShoot();});const count=pBullets.length;for(const b of pBullets){b.x=E.x;b.y=E.y+6;b.vx=0;b.vy=-1;b.dmg=.25;}return{count,seat:_seat,p2:run2.pilot};}''');frames(1)
     hit=p.evaluate('''()=>{const a=rc19Snap();let white=0;for(let i=0;i<a.length;i+=4)if(a[i+3]>64&&Math.min(a[i],a[i+1],a[i+2])>160&&Math.min(rcClean[i],rcClean[i+1],rcClean[i+2])<120)white++;return{loss:rcHP-rc19Total(),flash:E.flash,white,seat:_seat};}''')
     ck(diff+' '+kind+' real Player-2 shot damages and flashes the scaled hull/shield',shot['count']>0 and hit['loss']>0 and hit['flash']>0 and hit['white']>10 and hit['seat']==1,dict(shot=shot,hit=hit))
     p.evaluate('pBullets=[];player2.fireCd=player.fireCd=999999;player.x=camLeftX()+20;player2.x=camRightX()-20;player.y=player2.y=VH-30');frames(24)
     expiry=p.evaluate('''()=>{const compare=(a,b)=>{let error=0,ink=0;for(let i=0;i<a.length;i+=4){error+=Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2]);if(Math.max(a[i],a[i+1],a[i+2],b[i],b[i+1],b[i+2])>16)ink++;}return{ink,error:error/Math.max(1,ink*3*255)};},state=()=>Object.fromEntries(Object.entries(E).filter(([k,v])=>v==null||['number','string','boolean'].includes(typeof v))),timer=E.flash,before=state(),first=rc19Snap(),afterFirst=state(),a=rc19Snap(),afterSecond=state(),actual=cv.toDataURL();E.flash=0;const b=rc19Snap(),clean=cv.toDataURL();E.flash=timer;const h=rc19Snap(true);E.flash=0;const j=rc19Snap(true);E.flash=timer;return{timer,...compare(a,b),sameTimer:compare(first,a),hull:compare(h,j),mutations:Object.keys(afterSecond).filter(k=>before[k]!==afterSecond[k]).map(k=>({key:k,before:before[k],first:afterFirst[k],second:afterSecond[k]})),actual,clean};}''')
     for name in ['actual','clean']:
      url=expiry.pop(name)
      if expiry['error']>=.005:(O/f'{diff}-{kind}-{name}.png').write_bytes(base64.b64decode(url.split(',')[1]))
     ck(diff+' '+kind+' keeps native flash expiry and actual visible palette return',expiry['timer']<=0 and expiry['ink']>40 and expiry['error']<.005,expiry)
     if diff=='normal' and kind in ['s5station','s7tank','s8carrier','s9gunship']:
      p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit()');p.screenshot(path=str(O/(kind+'.jpg')),type='jpeg',quality=80)
  br.close()
finally:stop()
ck('No page, console, draw or asset errors',not errors,errors);q=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,rows=rows,errors=errors);(O/'native-report.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8');sys.exit(q['failed']>0)
