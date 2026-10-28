from pathlib import Path
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import json,sys,math,numpy as np,http.server,hashlib
R=Path(__file__).resolve().parents[1];W=R/'_shots/nightwing_shadow_turn_1028';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256
checks=[];errors=[];http=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,http=http),indent=2));assert v,(n,d)
M=json.loads((R/'assets/game/levels/stage_06/boss/nightwing_wind_1028/manifest.json').read_text());images={k:Image.open(R/a['path']).convert('RGBA')for k,a in M['banks'].items()}
def cell(k,f):
 a=M['banks'][k];return images[k].crop((f%a['cols']*a['cw'],f//a['cols']*a['ch'],f%a['cols']*a['cw']+a['cw'],f//a['cols']*a['ch']+a['ch']))
ck('Directional heading has 64 actual frames for each of three bank attitudes',M['banks']['heading']['frames']==192 and M['banks']['heading']['directions']==64)
ck('Each drift has 48 distinct pre-rendered banked turning/depth frames',all(M['banks'][k]['frames']==48 and len({cell(k,i).tobytes()for i in range(48)})==48 for k in ['drift_left','drift_right']))
ck('All textures use fixed even cells and fit4096px',all(a['cw']%2==a['ch']%2==0 and max(images[k].size)<=4096 for k,a in M['banks'].items()))
shadowNames=[k for k in M['banks']if k.endswith('_shadow')]
ck('Every normal, directional, depth and gun pose has a shadow',set(shadowNames)=={k+'_shadow'for k in ['whole','clean','heading','flyover','drift_left','drift_right','approach','death_large','gun_left','gun_right']})
ck('All shadow cells exactly match their source pose alpha and stored opacity',all(np.array_equal(np.rint(np.asarray(cell(k[:-7],i).getchannel('A'))*.56),np.asarray(cell(k,i).getchannel('A')))for k in shadowNames for i in range(M['banks'][k]['frames'])))
ck('All aircraft and shadow cells retain clear canvas borders',all((lambda b,a:b and b[0]>0 and b[1]>0 and b[2]<a['cw']and b[3]<a['ch'])(cell(k,i).getbbox(),a)for k,a in M['banks'].items()if k in shadowNames or k in ['heading','drift_left','drift_right']for i in range(a['frames'])))
H=json.loads((R/'_ART_SOURCES/nightwing_wind_1028/source-hashes.json').read_text());stable=[k for k in M['banks']if not k.endswith('_shadow')and k not in ['heading','heading_hit','drift_left','drift_left_hit','drift_right','drift_right_hit']]
ck('Canonical hull, weapons, wind gusts, charge, rings and thrusters are byte-identical',all(hashlib.sha256((R/M['banks'][k]['path']).read_bytes()).hexdigest()==H.get(str(Path(M['banks'][k]['path'])),H.get(str(R/M['banks'][k]['path'])))for k in stable),stable)
for name,side in [('drift_left',-1),('drift_right',1)]:
 ck(name+' yaw follows the exact half-circle flight tangent and ends south',all(abs(math.atan2(math.sin(m['angle']-(math.pi+side*math.pi*i/47)),math.cos(m['angle']-(math.pi+side*math.pi*i/47))))<1e-8 for i,m in enumerate(M['sockets'][name])))
board=Image.new('RGBA',(4*288,4*310),(13,24,35,255));d=ImageDraw.Draw(board)
for j,i in enumerate(range(0,48,3)):
 q=cell('drift_right',i);q=q.resize((288,288),Image.Resampling.NEAREST);board.alpha_composite(q,(j%4*288,j//4*310));d.text((j%4*288+5,j//4*310+290),f'Turn frame {i}/47',fill='white')
board.save(W/'turn-contact.png')
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append(r.url)if r.status>=400 else None);p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000);p.evaluate(TRAP_RAF)
  def step(n):
   e=p.evaluate(STEP,n)
   if e:raise RuntimeError(e)
  p.evaluate("()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'warhive'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('warhive');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;s6Wing.ships=[];delete boss._carrier17;boss._whv.mode='ace';whvAceSpawn(boss);}");step(430)
  ck('Live stage load resolves the updated frame metadata',p.evaluate("nf29Art('heading').frames===192&&nf29Art('drift_left').frames===48&&Object.values(NW30_ART.banks).every(a=>XART.rdy(a.key))"))
  p.evaluate('''()=>{window.flightCalls=[];window.flightDraw=ctx.drawImage;ctx.drawImage=function(im,...a){for(const[k,m]of Object.entries(NW30_ART.banks))if(im===XART.get(m.key)){flightCalls.push({bank:k,frame:Math.floor(a[1]/m.ch)*m.cols+Math.floor(a[0]/m.cw),x:a[4],y:a[5],w:a[6],h:a[7]});break;}return flightDraw.apply(this,[im,...a]);};}''')
  for name,config in [('cruise',{}),('bank',dict(vx=200)),('roll',dict(roll=dict(t=.07,dir=1))),('somer',dict(somer=dict(t=.11))),('inverted',dict(inverted=True)),('heading',dict(pose=dict(bank='heading',frame=116,scale=1))),('flyover',dict(pose=dict(bank='flyover',frame=3,scale=1.6))),('drift',dict(pose=dict(bank='drift_right',frame=19,scale=1.25))),('return',dict(pose=dict(bank='approach',frame=10,scale=.9)))]:
   q=p.evaluate('''c=>{const b=boss,A=b._whv.ace;nw30Cancel(b);A._nw28.mode='fight';A.st='fight';A.dash=A.desp=A.roll=A.somer=A._nf29Pose=null;A.inverted=false;A.vx=0;A.x=camLeftX()+viewW()/2;A.y=190;b._noHit=false;b.dead=false;b.flash=0;Object.assign(A,c);A._nf29Pose=c.pose||null;flightCalls=[];nw28DrawBody(b);return{calls:flightCalls,pose:nw30Pose(b),modular:nw30Modular(b)};}''',config)
   calls=q['calls'];sh=[c for c in calls if c['bank'].endswith('_shadow')];body=[c for c in calls if not c['bank'].endswith('_shadow')and c['bank']in ['whole','clean','heading','flyover','drift_right','approach']]
   ck(name+' draws one complete matching shadow behind the aircraft layers',len(body)==1 and len(sh)==(3 if q['modular']else 1)and all(c['bank'].endswith('_shadow')for c in calls[:len(sh)]),calls)
   if not q['modular']:ck(name+' shadow uses the same actual rotation/frame and depth offset',sh[0]['frame']==body[0]['frame']and sh[0]['bank']==body[0]['bank']+'_shadow'and sh[0]['y']>body[0]['y'])
   p.evaluate('()=>{flightCalls=[];drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/(name+'.png')))
  q=p.evaluate('''()=>{const b=boss,A=b._whv.ace;A._nf29Pose=A.roll=A.somer=A.dash=A.desp=null;A.inverted=false;A.vx=0;ctx.clearRect(0,0,cv.width,cv.height);nw30Shadow(b,nw30Pose(b));const d=ctx.getImageData(0,0,cv.width,cv.height).data;let visible=0,lower=0;for(let y=0;y<cv.height;y++)for(let x=0;x<cv.width;x++){const i=(y*cv.width+x)*4;if(d[i+3]>100){visible++;if(y>A.y+80)lower++;}}return{visible,lower};}''');ck('Native shadow pixels are actually present beneath the aircraft',q['visible']>8000 and q['lower']>2000,q)
  q=p.evaluate('''()=>{const b=boss,A=b._whv.ace;let out=[];for(let i=0;i<64;i++){A._nf29Pose=nf29Heading(Math.PI/2+i*TAU/64);flightCalls=[];nw28DrawBody(b);out.push(flightCalls.find(c=>c.bank==='heading')?.frame);}return out;}''');ck('All64 headings select distinct actual authored native cells',q==list(range(64)),q)
  q=p.evaluate('''()=>{const b=boss,A=b._whv.ace;A._nf29Pose=null;A.dash={st:'warn',t:0,x0:A.x,y0:A.y};A.gunCd=A.rollCd=A.somerCd=99;b._nw30.gunCd=b._nw30.windCd=99;return true;}''')
  poses=[]
  for i in range(410):
   step(1);q=p.evaluate('''()=>{const A=boss._whv.ace,p=A._nf29Pose;return{state:A.dash?.st,pose:p,x:A.x,y:A.y,angle:p?nw30Pose(boss).meta.angle:null};}''');poses.append(q)
  dr=[q for q in poses if q['state']=='drift'and q['pose']and q['pose']['bank'].startswith('drift_')];ck('Natural native charge plays at least45 different drift rotation frames',len({q['pose']['frame']for q in dr})>=45,len({q['pose']['frame']for q in dr}))
  errs=[]
  for a,b in zip(dr,dr[1:]):
   dx=b['x']-a['x'];dy=b['y']-a['y']
   if abs(dx)+abs(dy)>.01:
    yaw=b['angle']+math.pi/2;delta=math.atan2(dy,dx)-yaw;errs.append(abs(math.atan2(math.sin(delta),math.cos(delta))))
  ck('The rendered swerve points along actual native motion',bool(errs)and max(errs)<.14,max(errs)if errs else None)
  ck('Native charge returns to normal foreground combat',p.evaluate('!boss._whv.ace.dash&&!boss._whv.ace._nf29Pose&&!boss._noHit'))
  q=p.evaluate('''()=>{const b=boss,A=b._whv.ace;A.dash={_nf29:true,st:'offscreen'};flightCalls=[];nw28DrawBody(b);const n=flightCalls.length;A.dash=null;return n;}''');ck('Hidden offscreen flight draws no lingering shadow or aircraft',q==0)
  q=p.evaluate('''()=>{const b=boss,A=b._whv.ace;A._nf29Pose={bank:'drift_right',frame:35,scale:.8};A.dash=A.somer=A.roll=A.desp=null;b._gp4FlashNext=0;markHit(b);flightCalls=[];nw28DrawBody(b);return{flash:b.flash,calls:flightCalls};}''');ck('Damage retains matched white-hit art with a dark unchanged shadow',q['flash']>0 and any(c['bank']=='drift_right_hit'and c['frame']==35 for c in q['calls'])and any(c['bank']=='drift_right_shadow'and c['frame']==35 for c in q['calls']),q)
  p.evaluate('()=>{boss._whv.ace._nf29Pose=null;ctx.drawImage=flightDraw}');step(20);ck('Native hit flash expires normally',p.evaluate('boss.flash<=0'))
  p.evaluate('run.stage=7');ck('Other stages retain their original flight metadata',p.evaluate("nf29Art('heading')===NF29_ART.banks.heading&&nf29Art('heading').frames===96"))
  ck('No live game, draw or HTTP errors',not errors and not http,dict(errors=errors,http=http));br.close()
finally:stop()
print(len(checks),'shadow and authored-turn checks passed')
