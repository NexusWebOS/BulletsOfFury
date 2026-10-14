from pathlib import Path
import sys,json,subprocess
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/performance_1012/paired';O.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(R));results=[];errors=[];checks=[]
def check(n,v,data=None):checks.append({'name':n,'passed':bool(v),'data':data});print(('PASS ' if v else 'FAIL ')+n,flush=True)
reference=json.loads((R/'_BUILD_SOURCE/performance_reference_1012.json').read_text(encoding='utf-8'));original=reference['hud']
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio'])
  for version in ['before','after']:
   p=b.new_page(viewport={'width':1366,'height':768});p.on('pageerror',lambda e:errors.append(str(e)))
   p.on('console',lambda m:errors.append(m.text+' '+str(m.location)) if m.type=='error' else None)
   p.route('**/favicon.ico',lambda route:route.fulfill(status=204,body=''))
   if version=='before':p.route('**/assets/siege_console_1012.js*',lambda route:route.fulfill(body=original,content_type='application/javascript'))
   p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4',timeout=120000)
   p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(50);p.evaluate(shoot.SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':True})
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&XART.rdy(SC12_ART.key)&&bmfReady("game");}',timeout=120000)
   p.evaluate('()=>{run.score=123456;run.lives=7;run.bombs=12;stateT=3;SC12.clock=5;SC12.previousT=3;SC12.refresh();}')
   cdp=p.context.new_cdp_session(p)
   for rate in ([] if '--quick' in sys.argv else [1,4]):
    cdp.send('Emulation.setCPUThrottlingRate',{'rate':rate})
    q=p.evaluate('''async()=>{const timings=[];for(let i=0;i<150;i++){await new Promise(resolve=>__bofRealRAF(resolve));stateT+=1/60;const t=performance.now();SC12.refresh();if(i>=20)timings.push(performance.now()-t);}timings.sort((a,b)=>a-b);return{mean:timings.reduce((a,b)=>a+b,0)/timings.length,p95:timings[Math.floor(timings.length*.95)],painted:SC12.widgetsPainted,skipped:SC12.widgetsSkipped};}''')
    results.append({'version':version,'rate':rate,**q});print(json.dumps(results[-1]),flush=True)
   cdp.send('Emulation.setCPUThrottlingRate',{'rate':1})
   if version=='after':
    p.evaluate('()=>{SC12.clock=9;SC12.previousT=stateT;run.score=987654321;run.lives=1;run.bombs=0;player._rollCool=BR_COOL*.6;player._somerCool=SS_COOL*.8;run.speedLevel=3;run.shield=4;special={pilot:"cole",t:8,dur:15,strikes:2};SC12.refresh();}')
    p.screenshot(path=str(O/'dirty.png'))
    q=p.evaluate('''()=>{const old=SC12.panels.map(c=>c.getContext('2d').getImageData(0,0,c.width,c.height));SC12.invalidate();SC12.refresh();let changed=0,maxVisibleDelta=0;for(let n=0;n<2;n++){const c=SC12.panels[n],now=c.getContext('2d').getImageData(0,0,c.width,c.height).data;for(let i=0;i<now.length;i+=4){const a=now[i+3],b=old[n].data[i+3];maxVisibleDelta=Math.max(maxVisibleDelta,Math.abs(a-b));for(let j=0;j<3;j++)maxVisibleDelta=Math.max(maxVisibleDelta,Math.abs(now[i+j]*a/255-old[n].data[i+j]*b/255));for(let j=0;j<4;j++)if(now[i+j]!==old[n].data[i+j])changed++;}}return{changed,maxVisibleDelta};}''')
    check('Dirty and complete HUD repaint match within premultiplied canvas rounding',q['maxVisibleDelta']<=2,q)
    p.screenshot(path=str(O/'edge_hud.png'))
    q=p.evaluate('''()=>{const plate=document.createElement('canvas');plate.width=plate.height=16;const out=[];for(let i=0;i<5;i++){lateSpriteBake(plate,[0,0,16,16],16,16,'#ffaa33',4,null,false);bofDerivedCachesRetire();out.push({count:_lateSpriteCache.size,bytes:_lateSpriteBytes});}return out;}''')
    check('Stage cache retirement resets both sprite plates and byte accounting',all(x['count']==0 and x['bytes']==0 for x in q),q)
    p.evaluate('()=>{window.perfOldHud=0;const old=drawHUDStrip;drawHUDStrip=function(){perfOldHud++;return old.apply(this,arguments);};}')
    p.evaluate(shoot.STEP,3);check('Native loop skips the hidden legacy HUD under the side console',p.evaluate('perfOldHud')==0)
    p.evaluate('()=>{setState(GS.TITLE);setState(GS.PLAY);SC12.refresh();}')
    check('Side HUD still refreshes after a menu round trip',p.evaluate('SC12.active()&&SC12.last.length===1&&SC12.last[0].score===987654321'))
    oldEffects=reference['effects']
    p.evaluate('(source)=>{window.pfOldEffects=(0,eval)("("+source+")");window.pfNewEffects=_drawEffectsInner;}',oldEffects)
    p.evaluate('()=>{special=null;explosions.length=0;particles.length=0;pilotFx.length=0;efxBursts.length=0;XART.rdy("nx_smoke_0");XART.rdy("nx_small_1");XART.rdy("nxp_white_0");}')
    p.wait_for_function('XART.rdy("nx_smoke_0")&&XART.rdy("nx_small_1")&&XART.rdy("nxp_white_0")')
    p.evaluate('()=>{for(let i=0;i<8;i++)explode(50+i*48,140+(i%3)*80,55,"orange",null,null,null,null,true);for(const e of explosions)e.t=.15;for(const x of particles){x.t=.15;x.life=.7;}window.pfTint=xartTint;window.pfCalls=0;xartTint=function(){pfCalls++;return pfTint.apply(this,arguments);};pfOldEffects();}')
    p.wait_for_timeout(300)
    q=p.evaluate('''()=>{const paint=fn=>{ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=1;ctx.fillStyle='#05090e';ctx.fillRect(0,0,VW,VH);pfCalls=0;fn();ctx.restore();return{calls:pfCalls,pixels:ctx.getImageData(0,0,cv.width,cv.height).data};};const old=paint(pfOldEffects),now=paint(pfNewEffects);let delta=0;for(let i=0;i<now.pixels.length;i++)if(now.pixels[i]!==old.pixels[i])delta++;return{oldCalls:old.calls,newCalls:now.calls,pixelChanges:delta,particles:particles.length};}''')
    check('Explosion-particle batching preserves the complete rendered pixels',q['pixelChanges']==0,q)
    check('Explosion particles reuse sprite/tint lookups instead of resolving every spark',q['newCalls']<q['oldCalls']/4,q)
    p.evaluate('()=>{xartTint=pfTint;_drawEffectsInner=pfNewEffects;}')
   p.close()
  b.close()
finally:stop()
check('No page or console errors',not errors,errors)
(O/'verification.json').write_text(json.dumps({'measurements':results,'checks':checks,'errors':errors},indent=2),encoding='utf-8')
assert not errors and all(c['passed'] for c in checks)
