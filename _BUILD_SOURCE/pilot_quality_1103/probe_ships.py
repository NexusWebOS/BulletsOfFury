from pathlib import Path
import sys,json,base64,ast,time,hashlib
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw

R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
W=Path(__file__).parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import TRAP_RAF
T=ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf8'))
SETUP=next(ast.literal_eval(n.value) for n in T.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
errors=[];checks=[];rows=[];policies=[]
def check(ok,name):
 checks.append({'ok':bool(ok),'name':name})
 if not ok: print('FAIL '+name,flush=True)
def save(data,path):path.write_bytes(base64.b64decode(data.split(',')[-1]))

DRAW=r'''c=>{
 const pk=c.pk;run.pilot=pk;pilotIndex=PILOTS.findIndex(p=>p.key===pk);PILOTMOD={...PILOTS[pilotIndex]};
 run.stage=c.space?5:1;run.spaceMode=!!c.space;gravityMode=c.space?{...GRAVITY_SHIP_ACTIVE,narrative:false}:null;
 player.dead=player.out=false;player.invuln=0;player._bank=c.bank||0;player.roll=player.somer=null;
 player._spawnClearT=0;run.shield=0;player._hitFlash=0;player.x=worldWidth()/2;player.y=VH/2;camX=player.x-VW/2;
 player._lx=player.x;player._ly=player.y;player.vx=player.vy=0;
 if(c.kind==='roll')player.roll={t:c.f/8+.001,dur:1,dir:1};
 if(c.kind==='somer')player.somer={t:c.f/(c.space?12:8)+.001,dur:1};
 setRenderScale(c.scale);ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;
 ctx.clearRect(0,0,VW,VH);ctx.save();ctx.translate(-camX,0);drawPlayer();ctx.restore();
 const raw=ctx.getImageData(Math.round((VW/2-54)*SS),Math.round((VH/2-54)*SS),108*SS,108*SS);
 let opaque=0;const colors=new Set();for(let i=0;i<raw.data.length;i+=4)if(raw.data[i+3]>100){opaque++;colors.add((raw.data[i]<<16)|(raw.data[i+1]<<8)|raw.data[i+2]);}
 const crop=document.createElement('canvas');crop.width=crop.height=108*SS;crop.getContext('2d').putImageData(raw,0,0);
 return{pilot:pk,space:c.space,kind:c.kind,f:c.f,bank:c.bank,scale:SS,opaque,colors:colors.size,
   frame:c.space?furyShipPose(player,null).key:(somerFrameKey()||rollFrameKey()||_shipFrameKey(pk)),
   logicalHeight:c.space?SPACE_SHIP_SIZE:SHIP_DRAW_H,png:crop.toDataURL()};
}'''

with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
 p=b.new_page(viewport={'width':1280,'height':800})
 p.route('**/assets/online-config.js',lambda r:r.fulfill(status=200,content_type='application/javascript',body='window.BOF_ONLINE_CONFIG={};'))
 p.on('pageerror',lambda e:errors.append(str(e)))
 p.on('console',lambda m:errors.append(m.text[:300]) if m.type=='error' or 'DRAW ERROR' in m.text else None)
 print('Loading native game',flush=True)
 p.goto('http://127.0.0.1:65041/game/index.html',wait_until='load',timeout=180000)
 print('Native game loaded',flush=True)
 try:p.wait_for_function('window.__bofFrames>5',timeout=30000)
 except Exception:
  print('Load diagnostic '+json.dumps({'errors':errors,'state':p.evaluate('({ready:document.readyState,frames:window.__bofFrames,state:typeof state,scale:typeof SS,assets:typeof ASSETS})')}),flush=True)
  raise
 p.evaluate(TRAP_RAF)
 check(p.evaluate('SS===2'),'ordinary URL starts with high-quality backing')
 p.evaluate(SETUP,{'stage':1,'pilot':'cole'})
 p.evaluate('()=>{furyShipWarm();for(const p of PILOTS)for(let f=0;f<8;f++){XART.rdy("ship_"+p.key+"_br"+f);XART.rdy("ship_"+p.key+"_so"+f);}}')
 p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&furyShipReady()&&PILOTS.every(p=>["",...Array.from({length:8},(_,i)=>"_br"+i),...Array.from({length:8},(_,i)=>"_so"+i)].every(s=>XART.rdy("ship_"+p.key+s)))}',timeout=180000)
 print('All ship banks decoded',flush=True)
 pilots=p.evaluate('PILOTS.map(p=>p.key)')
 for space in [False,True]:
  for pk in pilots:
   samples=[]
   poses=[('idle',0,0),('bank',0,-1),('bank',0,1)]+[('roll',f,0)for f in range(8)]+[('somer',f,0)for f in range(12 if space else 8)]
   for kind,f,bank in poses:
    q=p.evaluate(DRAW,{'pk':pk,'space':space,'kind':kind,'f':f,'bank':bank,'scale':2})
    check(q['opaque']>10,f'{pk} {"space" if space else "air"} {kind} {f} {bank}: visible native pixels')
    png=q.pop('png');rows.append(q)
    if kind=='idle' or kind in ['roll','somer'] and f in [2,4,6]:
     path=W/f'{pk}-{"space" if space else "air"}-{kind}-{f}.png';save(png,path);samples.append(path)
   for scale in [1,2]:
    q=p.evaluate(DRAW,{'pk':pk,'space':space,'kind':'idle','f':0,'bank':0,'scale':scale})
    save(q.pop('png'),W/f'{pk}-{"space" if space else "air"}-quality-{scale}.png')
    rows.append(q)
   print(pk+(' space' if space else ' aircraft')+' verified',flush=True)
 # Simulate sustained loading/capture hitches. They must not change ship detail.
 p.evaluate('()=>{setRenderScale(2);stateT=10;for(let i=0;i<600;i++)renderPerformanceTick(.08);}')
 check(p.evaluate('SS===2'),'600 slow-frame notices preserve ship quality')
 check(p.evaluate('SHIP_DRAW_H===60&&SPACE_SHIP_SIZE===48'),'native aircraft/space footprints unchanged')
 # Verify both space stages actually use the Furyship renderer through drawPlayer.
 for stage in [5,9]:
  p.evaluate(SETUP,{'stage':stage,'pilot':'maverick'})
  p.wait_for_function('(s)=>{stageLoadTick();return stageLoadReady(s)}',arg=stage,timeout=180000)
  p.evaluate('()=>{run.spaceMode=true;setRenderScale(2);story=null;BOFCinematicDirector.cancel();player._spawnClearT=0;player.dead=false;player.invuln=1e9;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
  save(p.evaluate('cv.toDataURL()'),W/f'stage-{stage}-native.png')
  check(p.evaluate('spaceShipActive()&&furyShipReady()&&SS===2'),f'Stage {stage}: actual space renderer high quality')
 b.close()
 # Query policy is checked from a fresh, ordinary page, never a test-only setter.
 for query,expected in [('',2),('?quality=auto',2),('?quality=default',2),('?quality=high',2),('?quality=performance',1),('?quality=low',1)]:
  b=pw.chromium.launch(channel='msedge',headless=True)
  p=b.new_page();p.route('**/assets/online-config.js',lambda r:r.fulfill(status=200,content_type='application/javascript',body='window.BOF_ONLINE_CONFIG={};'))
  p.goto('http://127.0.0.1:65041/game/index.html'+query,wait_until='load',timeout=180000)
  p.wait_for_function('typeof SS!=="undefined"',timeout=180000)
  got=p.evaluate('({SS,width:cv.width,height:cv.height,smooth:ctx.imageSmoothingEnabled})');policies.append({'query':query,'expected':expected,**got})
  check(got['SS']==expected and not got['smooth'],f'launch policy {query or "default"}')
  b.close()

# Display paired actual engine crops at the same size; nearest enlargement only.
for space in [False,True]:
 sheet=Image.new('RGB',(9*180,2*235),(10,18,28));d=ImageDraw.Draw(sheet)
 for i,pk in enumerate(pilots):
  for j,scale in enumerate([1,2]):
   im=Image.open(W/f'{pk}-{"space" if space else "air"}-quality-{scale}.png').convert('RGBA')
   im=im.crop((im.width//2-42*scale,im.height//2-42*scale,im.width//2+42*scale,im.height//2+42*scale)).resize((168,168),Image.Resampling.NEAREST)
   sheet.paste(im,(i*180+6,j*235+40),im);d.text((i*180+8,j*235+10),pk.upper(),fill='white');d.text((i*180+8,j*235+214),'BEFORE' if scale==1 else 'HIGH QUALITY',fill='cyan')
 sheet.save(W/f'{"space" if space else "aircraft"}-comparison.png')

report={'checks':checks,'errors':errors,'frames':rows,'launchPolicies':policies,'gameSha256':hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest()}
(W/'ships-native.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps({'checks':len(checks),'failed':sum(not x['ok'] for x in checks),'errors':errors,'frames':len(rows)},indent=2),flush=True)
assert all(x['ok']for x in checks) and not errors
