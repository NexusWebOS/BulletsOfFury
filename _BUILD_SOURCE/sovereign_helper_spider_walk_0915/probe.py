"""Real Chromium proof for the Sovereign helper spider walk."""
import base64,json,math,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'sovereign_helper_spider_walk_0915';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image
def main():
  checks,errors,shots=[],[],[]
  def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  ' if v else 'FAIL ')+label,flush=True)
  class Quiet(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**k):super().__init__(*a,directory=str(ROOT),**k)
    def log_message(self,*a):pass
  server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=server.serve_forever,daemon=True).start()
  with sync_playwright() as pw:
    browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);page=browser.new_page(viewport={'width':1100,'height':1200})
    page.on('pageerror',lambda e:errors.append('page '+str(e)));page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
    page.goto(f'http://127.0.0.1:{server.server_port}/index.html',wait_until='load',timeout=120000);page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
    page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB);fight=page.evaluate("()=>window.__fight(4,'boss','yuri')");ok(fight.get('ok'),'native Stage-4 boss route opens in Chromium')
    page.evaluate("""()=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];state=GS.PLAY;stateT=1;
      run.stage=4;curStage=STAGES[3];player.x=worldWidth()*.5;player.y=650;player.invuln=1e9;player.dead=false;
      for(const k of ['s4w_boss_energized_0','s4w_helper_dual_0','s4w_helper_dual_hot_0','s4w_final_chaingun_0','s4w_lightning_shield_0','s4w_power_node_0'])XART.rdy(k);}""")
    for _ in range(240):
      ready=page.evaluate("()=>['s4w_boss_energized_0','s4w_helper_dual_0','s4w_final_chaingun_0'].every(k=>XART.rdy(k))")
      if ready:break
      page.wait_for_timeout(35)
    ok(ready,'authored boss and helper plates decode before the walk capture')
    def setup(level):page.evaluate("""k=>{diffKey=k;DIFF=DIFFS[k];boss=null;bossActive=false;eBullets=[];pBullets=[];spawnBoss('stormsovereign');boss.enter=false;boss.x=worldWidth()/2;boss.y=boss._s4war.homeY;boss._drawY=boss.y;boss.fireCd=999;bossActive=true;stage4CoreTurretSpawnMissing(boss,.5);for(const t of boss._s4war.coreTurrets){t.spawnT=1;t.materialize=1;}}""",level)
    def hit(i):return page.evaluate("""i=>{const n=boss._s4war.shield.nodes[i];boss._s4ShieldHit=n;_lastHitX=n.x;_lastHitY=n.y;hitBoss(1);const R=boss._s4war.coreEnrage;return {flag:!!n._coreRageTriggered,reacts:R&&R.reacts,walk:!!(R&&R.walkActive)};}""",i)
    def step(n):page.evaluate("n=>{for(let i=0;i<n;i++){boss.fireCd=999;updatePlay(1/60);stateT+=1/60;}}",n)
    def snap(name):
      page.evaluate("()=>{shake=0;boss.flash=0;drawWorld(0)}");d=page.evaluate("""()=>{const R=boss._s4war.coreEnrage,a=eBullets.filter(q=>q._s4CoreRage);return {walk:R&&{active:R.walkActive,t:R.walkT,offset:R.walkOffset,depth:R.walkDepth,up:R.walkSeenUp,back:R.walkSeenBack,reacts:R.reacts},helpers:boss._s4war.coreTurrets.map(t=>({side:t.side,x:t.x,y:t.y,rage:!!t.rage})),shots:a.length,left:a.filter(q=>q._s4CoreSide<0).length,right:a.filter(q=>q._s4CoreSide>0).length,gaps:boss._s4war.coreEnrageGapWindows};}""")
      raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));shots.append(p);return d
    setup('hard');first=hit(0);second=hit(1);ok(first['flag'] and second['flag'] and second['walk'] and second['reacts']==1,'a second live generator hit arms one bounded spider walk')
    step(95);up=snap('sovereign_spider_01_up');step(90);back=snap('sovereign_spider_02_back')
    ok(up['walk']['up'] and -58.1<=up['walk']['offset']<-52,'Hard reaches its limited 58-pixel upward bound')
    ok(back['walk']['back'] and back['helpers'][0]['y']>up['helpers'][0]['y']+28,'the pair reverses and walks back toward its starting row')
    bounds=page.evaluate("()=>({l:camLeftX(),r:camRightX()})");ok(all((t['x']<bounds['l']+90 if t['side']<0 else t['x']>bounds['r']-90) for t in up['helpers']+back['helpers']),'both halves of the walk preserve the edge-hugging route')
    ok(up['left'] and up['right'] and back['left'] and back['right'] and back['gaps']>up['gaps'],'both offset streams and their pause windows continue through the walk')
    step(30);again=hit(0);ok(again['walk'] and again['reacts']==2,'another generator hit can restart the bounded response after it returns')
    setup('furious');hit(0);hit(0);step(98);fury=page.evaluate("()=>({depth:boss._s4war.coreEnrage.walkDepth,offset:boss._s4war.coreEnrage.walkOffset})");ok(fury['depth']==72 and -72.1<=fury['offset']<-66,'Furious uses the explicit 72-pixel bound without leaving the side lane')
    setup('normal');hit(0);normal=hit(0);ok(not normal['walk'],'Normal remains isolated from helper spider-walk behavior')
    for p in shots:
      im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
    ok(not errors,'zero Chromium page or console errors');browser.close()
  server.shutdown();result={'checks':checks,'errors':errors,'fight':fight,'first':first,'second':second,'up':up,'back':back,'again':again,'fury':fury,'normal':normal,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
  passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
  if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
