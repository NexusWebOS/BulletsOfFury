from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
from io import BytesIO
import sys,ast,json,base64,http.server
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/menu_heart_1021';checks=[];errors=[]
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
def ck(n,v,data=None):checks.append({'name':n,'ok':bool(v),'data':data});print(('PASS ' if v else 'FAIL ')+n,flush=True)
try:
 with sync_playwright() as pw:
  for browser in (['msedge'] if '--reel-only' in sys.argv else ['chrome','firefox','msedge']):
   br=pw.firefox.launch() if browser=='firefox' else pw.chromium.launch(channel=browser,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000);p.add_init_script(shoot.TRAP_RAF);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('typeof CH21!=="undefined"&&ASSETS.ready')
   p.evaluate('()=>{for(const a of Object.values(MW21_ART))XART.rdy(a.key);UI20.warm();wm26Warm();}');p.wait_for_function('()=>Object.values(MW21_ART).every(a=>XART.rdy(a.key))&&UI20_KEYS.every(k=>XART.rdy(k))')
   p.evaluate('()=>{setState(GS.PILOT);run.mode="campaign";tutAskOpen(1);tutAsk.t=2;Input.clearTaps();}');p.keyboard.press('ArrowDown');p.evaluate('drawScene(0)');ck(browser+' real keyboard changes tutorial selection',p.evaluate('tutAsk?.sel===1'))
   p.keyboard.press('Escape');p.evaluate('drawScene(0)');ck(browser+' Back returns to pilot select',p.evaluate('state===GS.PILOT&&tutAsk===null'))
   p.evaluate('()=>{tutAskOpen(1);tutAsk.t=2;tutAsk.sel=0;Input.clearTaps();}');p.keyboard.press('Enter');p.evaluate('drawScene(0)');ck(browser+' confirm starts actual tutorial with instructor',p.evaluate('!!TUT&&TUT.lead===tutLeadKey()'))
   p.evaluate('()=>{tutCleanup();TUT=null;BOFCinematicDirector.cancel();story=null;Input.clearTaps();run._heartMode=false;}');p.evaluate(SETUP,{'stage':5,'pilot':'falva','diff':'normal','kind':'chromehammer'});p.evaluate('()=>{run._heartMode=true;ch21Init(boss);window.B=boss;for(const k of ch21Keys())XART.rdy(k);player.invuln=1e9;warnT=0;stageTimer=0;enemies=[];}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&ch21Keys().every(k=>XART.rdy(k));}')
   for action in ['dance','slam','shield','waltz','bouquet']:
    row=p.evaluate('''type=>{const Q=B._heart;Q.action=null;Q.shield=0;B.x=worldWidth()/2;B.y=PLAY.y+130;const A=ch21Start(B,type);for(let i=0;i<90;i++)updateBoss(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return{bank:ch21Pose(B).name,draws:{...CH21.draws},ready:XART.rdy(ch21Bank(ch21Pose(B).name)?.key),target:retinaBossTargets(B).length};}''',action);ck(browser+' '+action+' draws actual atlas and target',row['ready'] and row['target']==1,row)
   p.goto(f'http://127.0.0.1:{port}/_shots/menu_heart_1021/review.html');p.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth)');ck(browser+' review has five full concepts and four menu frames',p.evaluate('document.querySelectorAll(\'article[id^="concept-"]\').length===5&&document.querySelectorAll("#frames article img").length===4'))
   p.set_viewport_size({'width':390,'height':844});ck(browser+' review fits mobile width',p.evaluate('document.documentElement.scrollWidth<=innerWidth'));p.set_viewport_size({'width':1440,'height':1000});ck(browser+' review fits desktop width',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
   if browser=='msedge':
    p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('typeof CH21!=="undefined"&&ASSETS.ready');p.evaluate(SETUP,{'stage':5,'pilot':'lizzie','diff':'normal','kind':'chromehammer'});p.evaluate('()=>{run._heartMode=true;ch21Init(boss);window.B=boss;for(const k of ch21Keys())XART.rdy(k);player.invuln=1e9;warnT=0;stageTimer=0;stagePlan=[];enemies=[];wm26Warm();}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&ch21Keys().every(k=>XART.rdy(k));}');frames=[]
    for action in ['dance','shield','slam','waltz','bouquet']:
     p.evaluate('''type=>{B.x=worldWidth()/2;B.y=PLAY.y+130;B._heart.action=null;B._heart.shield=0;B._heart.cool=999;eBullets=[];ch21Start(B,type);}''',action)
     for k in range(56):
      data=p.evaluate('''()=>{for(let i=0;i<5;i++)updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);shake=0;drawWorld(0);return cv.toDataURL().split(',')[1];}''');im=Image.open(BytesIO(base64.b64decode(data))).convert('RGB');frames.append(im)
    frames[0].save(O/'heart-actions.gif',save_all=True,append_images=frames[1:],duration=84,loop=0,optimize=True);ck('Native Chrome Heart animated reel saved',True,{'frames':len(frames),'bytes':(O/'heart-actions.gif').stat().st_size})
   br.close()
finally:stop()
(O/('reel-check.json' if '--reel-only' in sys.argv else 'cross-browser.json')).write_text(json.dumps({'checks':checks,'errors':errors},indent=2));print(json.dumps({'checks':len(checks),'passed':sum(c['ok'] for c in checks),'errors':errors}),flush=True);sys.exit(not all(c['ok'] for c in checks) or bool(errors))
