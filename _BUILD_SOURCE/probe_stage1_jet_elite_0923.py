"""Chromium gameplay check for Stage 1 Hard/Furious jet pursuit and attacks."""
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import base64,io,json,sys,http.server
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
from shoot import GAME,SETUP,TRAP_RAF,serve
OUT=ROOT/'_shots/stage1_jet_elite_0923';OUT.mkdir(exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=serve(GAME);errors=[];result={};screens=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1500,'height':1000})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(TRAP_RAF)
  for diff in ['normal','hard','furious']:
   pg.evaluate(SETUP,{'state':'PLAY','stage':1,'pilot':'axel','invuln':True})
   data=pg.evaluate("""d=>{
     diffKey=d;DIFF=DIFFS[d];story=null;stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;subBoss=null;bossActive=false;subBossActive=false;
     player.x=350;player.y=450;player.dead=false;player.invuln=9999;
     const types=['s1jetdelta','s1jetdelta_b','s1jetbomber','s1jetbomber_b'];
     const jets=types.map((type,i)=>spawnEnemy(type,i&1?360:90,60+i*16,{route:'straight'}));
     for(const e of jets){e._s1DelayFrames=0;e._stagger=0;jetTick(e,1/60)}
     const stats=jets.map(e=>({type:e.type,hp:e.hp,speed:e._jspd,fire:e._fmul,elite:!!e._s1Elite}));
     const pursuer=jets[0],x0=pursuer.x;
     for(let i=0;i<60;i++)jetTick(pursuer,1/60);
     const pursuit={start:x0,end:pursuer.x,y:pursuer.y,bank:pursuer.spin};
     enemies=[];eBullets=[];
     const gun=spawnEnemy('s1jetdelta',240,150,{route:'straight'});
     gun._s1DelayFrames=0;gun._stagger=0;player.x=320;jetTick(gun,1/60);
     gun._burstCd=0;jetTick(gun,1/60);jetTick(gun,1/60);
     const bullets=eBullets.filter(b=>b.kind==='s1bullet').map(b=>({vx:b.vx,vy:b.vy,x:b.x}));
     eBullets=[];
     const bomber=spawnEnemy('s1jetbomber',240,155,{route:'straight'});
     bomber._s1DelayFrames=0;bomber._stagger=0;jetTick(bomber,1/60);eBullets=[];bomber._shotCd=0;jetTick(bomber,1/60);
     const missile=eBullets.filter(b=>b.kind==='s1jungleMissile').map(b=>({vx:b.vx,vy:b.vy}));
     eBullets=[];
     const black=spawnEnemy('s1jetbomber_b',240,165,{route:'straight'});
     black._s1DelayFrames=0;black._stagger=0;jetTick(black,1/60);eBullets=[];black._salvo=0;
     const beats=[];for(let i=0;i<3;i++){black._shotCd=0;const n=eBullets.length;jetTick(black,1/60);beats.push(eBullets.slice(n).map(q=>({x:q.x,vx:q.vx,vy:q.vy})));}
     enemies=[jets[1],jets[2],gun,bomber,black];eBullets=eBullets.filter(q=>q.kind==='s1jungleMissile');
     for(const e of enemies)furyFleetPreload(e);
     return {stats,pursuit,bullets,missile,beats};
   }""",diff)
   result[diff]=data
   pg.wait_for_function("()=>[0,1,2,3].every(v=>XART.rdy('furyjet_'+v+'_bank_0'))")
   for _ in range(8):pg.evaluate("()=>drawWorld(0)");pg.wait_for_timeout(60)
   png=base64.b64decode(pg.evaluate("document.getElementById('screen').toDataURL('image/png').split(',')[1]"))
   (OUT/f'{diff}.png').write_bytes(png);screens.append(Image.open(io.BytesIO(png)).convert('RGB'))
  n,h,f=(result[k] for k in ['normal','hard','furious'])
  assert all(not x['elite'] for x in n['stats']),n['stats']
  assert all(x['elite'] for x in h['stats']+f['stats']),(h['stats'],f['stats'])
  for i in range(4):
   assert n['stats'][i]['speed']<h['stats'][i]['speed']<f['stats'][i]['speed']
   assert n['stats'][i]['hp']<h['stats'][i]['hp']<f['stats'][i]['hp']
   assert n['stats'][i]['fire']>h['stats'][i]['fire']>f['stats'][i]['fire']
  assert abs(n['pursuit']['end']-n['pursuit']['start'])<2,n['pursuit']
  assert h['pursuit']['end']>n['pursuit']['end']+20 and f['pursuit']['end']>h['pursuit']['end']+12,(n['pursuit'],h['pursuit'],f['pursuit'])
  assert len(n['bullets'])==len(h['bullets'])==len(f['bullets'])==2
  assert all(abs(b['vx'])<.001 for b in n['bullets']),n['bullets']
  assert all(b['vx']>0 and b['vy']>0 for b in h['bullets']+f['bullets']),(h['bullets'],f['bullets'])
  assert len(n['missile'])==len(h['missile'])==len(f['missile'])==1
  assert abs(n['missile'][0]['vx'])<.001 and h['missile'][0]['vx']>0 and f['missile'][0]['vx']>0
  for d in [n,h,f]:
   assert [len(b) for b in d['beats']]==[1,1,4],d['beats']
   assert d['beats'][0][0]['x']<d['beats'][1][0]['x'],d['beats']
  # No cross-stage spill; the Stage 3 delta still owns its loop/charge pattern.
  outside=pg.evaluate("""()=>{run.stage=3;const ice=spawnEnemy('s1jetdelta',90,80,{});run.stage=4;const highway=spawnEnemy('s1jetDelta',90,80,{});highway._s1DelayFrames=0;highway._stagger=0;jetTick(highway,1/60);return {ice:ice.pattern,highway:!!highway._s1Elite}}""")
  assert outside=={'ice':'loopcharge','highway':False},outside
  route=pg.evaluate("""()=>{run.stage=1;diffKey='furious';DIFF=DIFFS.furious;player.x=430;player.y=450;
    const e=spawnEnemy('s1jetdelta',240,180,{route:'cornerRL'});e._s1DelayFrames=0;e._stagger=0;
    jetTick(e,1/60);e.x=240;e.y=180;e._y0=0;const x=e.x;jetTick(e,1/60);
    return {route:e._route,dx:e.x-x,elite:!!e._s1Elite};}""")
  assert route['route']=='cornerRL' and route['dx']<0 and route['elite'],route
  assert not errors,errors
  contact=Image.new('RGB',(screens[0].width*3,screens[0].height))
  for i,img in enumerate(screens):contact.paste(img,(i*img.width,0))
  contact.save(OUT/'normal_hard_furious.png')
  result['outside']=outside;result['route']=route;result['errors']=errors
  (OUT/'results.json').write_text(json.dumps(result,indent=2))
  print('PASS: Stage 1 jet speed, hull, pursuit, aimed gun/missile fire, black-bomber sequence and cross-stage isolation in Chromium; no page or console errors.')
  br.close()
finally:stop()
