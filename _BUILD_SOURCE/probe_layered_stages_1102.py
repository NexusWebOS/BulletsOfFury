from pathlib import Path
import sys,json,hashlib,datetime
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=Path(__file__).parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF
checks=[];errors=[];http=[]
def ck(name,ok,data=None):
 checks.append({'name':name,'passed':bool(ok),'data':data});(O/'checks.json').write_text(json.dumps(checks,indent=2),encoding='utf8');print('PASS' if ok else 'FAIL',name,str(data)[:1200] if not ok else '',flush=True)
 assert ok,(name,data)
SETUP='''n=>{EA11.setup(n,'furious');stagePlan=[];waveIdx=0;subBossTriggered=subBossDone=aminiTriggered=true;bossWarned=true;DBGT.god=true;DBGT.speed=1;boss=null;subBoss=null;bossActive=subBossActive=false;stageEnding=null;enemies=[];powerups=[];eBullets=[];pBullets=[];stageTimer=0;_adaptiveSpawnT=99999;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;for(const k of Object.keys(Input.keys))Input.keys[k]=false;player.x=worldWidth()/2;player.y=VH-65;camX=Math.max(0,player.x-VW/2);return _levelCfg();}'''
port,stop=serve(str(R));url=f'http://127.0.0.1:{port}/index.html'
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
  p=b.new_page(viewport={'width':1280,'height':900});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:http.append((r.status,r.url.split('?')[0])) if r.status>=400 else None)
  p.goto(url,wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>4',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  ck('Live renderer registers the new layer owner',p.evaluate('!!window.BOF_LAYERED_STAGES'))
  p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  baseline=p.evaluate('()=>({stage1:LS112.base.cfg(1).master,plan:STAGES.map(s=>({length:s.length,sub:s.subboss,boss:s.boss}))})')
  for n in range(1,10):
   cfg=p.evaluate(SETUP,n)
   p.wait_for_function('n=>{stageLoadTick();return stageLoadReady(n)&&(!ls112Live(n)||ls112Keys(n).every(k=>XART.rdy(k)))}',arg=n,timeout=180000)
   q=p.evaluate('''()=>{ctx.setTransform(SS,0,0,SS,0,0);window.__bofFrames++;drawWorld(0);return BOF_LAYERED_STAGES.info();}''')
   ck('Stage '+str(n)+' retains its native width and encounter scroll budget',q['worldWidth']==680 and (n==1 or q['nativeRange']==p.evaluate('LS112_ART.levels[String(run.stage)].nativeRange')),q)
   if n==1:ck('Stage 1 retains its own master',cfg['master']==baseline['stage1']);continue
   ck('Stage '+str(n)+' uses its approved terrain',cfg['master']=='ls112_stage_'+str(n))
   for fraction,label in [(0,'entry'),(.5,'middle'),(.94,'north')]:
    p.evaluate('''f=>{const a=LS112_ART.levels[String(run.stage)];mapScroll=a.nativeRange*f;if(run.stage===5)_stage5SpaceScroll=(a.h-viewH())*f/.34;if(run.stage===6)_stage6SkyScroll=(a.h-viewH())*f;if(run.stage===9)_stage9SpaceScroll=(a.h-viewH())*f/.32;if(run.stage===8)LS112.clock.realmTravel=(a.h-viewH())*f;ctx.setTransform(SS,0,0,SS,0,0);window.__bofFrames++;drawWorld(0);}''',fraction)
    p.locator('#screen').screenshot(path=str(O/f'stage-{n}-{label}.png'))
   old=p.evaluate('()=>({map:mapScroll,clock:efxClock,bed:LS112.clock.bed?.frame})')
   q=p.evaluate('''()=>{for(let i=0;i<70;i++){updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);window.__bofFrames++;drawWorld(1/60);}return {map:mapScroll,clock:efxClock,bed:LS112.clock.bed?.frame,layer:BOF_LAYERED_STAGES.info(),pools:enemies.length};}''')
   ck('Stage '+str(n)+' advances through native updates without render errors',q['clock']>old['clock'] and q['map']>=old['map'],q)
   if cfg['liquid']:ck('Stage '+str(n)+' has an independently animated material layer',q['layer']['clock']['bed']['time']>old['clock'])
  p.evaluate(SETUP,4);p.wait_for_function('()=>{stageLoadTick();return ls112Keys(4).every(k=>XART.rdy(k))}',timeout=180000)
  q=p.evaluate('''()=>{const a=LS112_ART.levels['4'];mapScroll=a.nativeRange*(1-2100/(a.h-viewH()));const vals=[];for(let j=0;j<12;j++){for(let i=0;i<6;i++){updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);window.__bofFrames++;drawWorld(1/60);}vals.push({frame:LS112.clock.tesla?.frame,y:LS112.clock.tesla?.y,sockets:LS112.clock.tesla?.sockets});}return vals;}''')
  ck('All six Tesla sockets pulse through a live frame sequence',len({v['frame'] for v in q})>=10 and all(len(v['sockets'])==6 for v in q),q)
  p.locator('#screen').screenshot(path=str(O/'tesla-live.png'))
  # Fixed native field for a compact authored-animation review movie/GIF.
  p.evaluate('()=>{window.__padMap=mapScroll;}');frames=[]
  for i in range(24):
   p.evaluate('()=>{efxClock+=1/18;mapScroll=window.__padMap;ctx.setTransform(SS,0,0,SS,0,0);window.__bofFrames++;drawWorld(0)}')
   path=O/f'tesla-{i:02d}.png';p.locator('#screen').screenshot(path=str(path));frames.append(path)
  p.evaluate(SETUP,6);p.wait_for_function('()=>{ls112Warm("X");return ls112Keys("X").every(k=>XART.rdy(k))}',timeout=180000)
  q=p.evaluate('''()=>{const before=mapScroll;ctx.setTransform(SS,0,0,SS,0,0);stageXArenaDraw(1/60);return {draws:LS112.draws['stage-X'],before,after:mapScroll,terrain:LS112.clock.terrain};}''');ck('Stage X renders its own forward city without advancing campaign waves',q['draws']>0 and q['before']==q['after'],q)
  ck('No page, console, image or renderer errors',not errors and not http,{'errors':errors,'http':http});b.close()
 (O/'report.json').write_text(json.dumps({'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'fixture':'Native engine graphics/update checks. Isolated debug scenes, not survival balance certification.'},indent=2),encoding='utf8')
 from PIL import Image
 ims=[Image.open(f).convert('RGB') for f in frames];ims[0].save(O/'tesla-live.gif',save_all=True,append_images=ims[1:],duration=56,loop=0)
 print('RESULT',len(checks),'passed',flush=True)
finally:stop()
