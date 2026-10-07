"""Cold/delayed/warm boot geometry, atomic controls, resize and fullscreen."""
from pathlib import Path
import asyncio,json,sys
from playwright.async_api import async_playwright
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/startup_layout_1007';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];runs=[]
def ck(v,n):checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
INIT='''(()=>{window.bootGeometry=[];let last='';function sample(){const q={};for(const id of ['game-frame','screen-area','screen']){const e=document.getElementById(id);if(e){const r=e.getBoundingClientRect();q[id]=[r.x,r.y,r.width,r.height];}}q.classes=document.body?.className;const h=document.getElementById('hint');q.hints=h?.children.length||0;q.hintVisibility=h?getComputedStyle(h).visibility:null;try{q.state=state}catch(e){}const s=JSON.stringify(q);if(s!==last){window.bootGeometry.push({t:Math.round(performance.now()),...q});last=s;}requestAnimationFrame(sample);}requestAnimationFrame(sample)})()'''
SNAP='''()=>{const out={};for(const id of ['game-frame','screen-area','screen','hint']){const e=document.getElementById(id),r=e.getBoundingClientRect();out[id]=[r.x,r.y,r.width,r.height];}out.hints=document.querySelectorAll('#hint span').length;out.visibility=getComputedStyle(document.getElementById('hint')).visibility;out.frames=window.__bofFrames||0;out.classes=document.body.className;try{out.state=state}catch(e){}return out;}'''
def same(a,b,k):return all(abs(x-y)<.1 for x,y in zip(a[k],b[k]))
async def main():
 port,stop=shoot.serve(str(R))
 try:
  async with async_playwright() as pw:
   br=await pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
   for name,size in [('desktop',{'width':1280,'height':900}),('narrow',{'width':390,'height':844}),('wide',{'width':1920,'height':1080})]:
    context=await br.new_context(viewport=size);p=await context.new_page();await p.add_init_script(INIT)
    p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' else None);p.on('response',lambda r:errors.append(f'{r.status} {r.url}') if r.status>=400 else None)
    async def delay(route):
     await asyncio.sleep(1.5 if route.request.url.endswith('/game.js') else 5 if route.request.url.endswith('/online.js') else 3)
     await route.continue_()
    await p.route('**/assets/game.js',delay);await p.route('**/assets/online.js',delay);await p.route('**/BOFCommandSignal.ttf',delay)
    nav=asyncio.create_task(p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000));await asyncio.sleep(.6)
    early=await p.evaluate(SNAP);await p.screenshot(path=str(O/(name+'-early.png')))
    ck(early['screen-area'][3]>100,name+' playfield has its final height before game.js arrives')
    await asyncio.sleep(1.5);mid=await p.evaluate(SNAP)
    ck(mid['frames']==0,name+' no partially registered runtime frames before final script')
    await nav;await p.wait_for_function('()=>window.__bofFrames>4&&controlHintShellTick.done',timeout=120000)
    await p.wait_for_timeout(400);boot=await p.evaluate(SNAP);history=await p.evaluate('()=>bootGeometry')
    ck(all(same(early,q,'game-frame') and same(early,q,'screen-area') and same(early,q,'screen') for q in history if 'screen' in q),name+' zero startup movement through script/font/art load')
    ck(boot['hints']==6 and boot['visibility']=='hidden',name+' complete control strip prewarms invisibly during boot')
    await p.screenshot(path=str(O/(name+'-boot.png')))
    if name=='desktop':
     await p.keyboard.press('Enter');await p.wait_for_timeout(1400);await p.keyboard.press('Enter')
     await p.wait_for_function('()=>state===GS.TITLE||state===GS.OPENER',timeout=30000)
     if await p.evaluate('()=>state===GS.OPENER'):
      await p.wait_for_timeout(350);await p.keyboard.press('Enter')
     await p.wait_for_function('()=>state===GS.TITLE',timeout=30000)
    else:await p.evaluate('()=>{setState(GS.TITLE);menuIndex=0;}')
    await p.wait_for_function('()=>getComputedStyle(document.getElementById("hint")).visibility==="visible"',timeout=15000)
    title=await p.evaluate(SNAP);ck(same(boot,title,'game-frame') and same(boot,title,'screen'),name+' completed menu/control reveal does not shift game')
    ck(title['hints']==6,name+' title reveals all six authored hints together')
    await p.screenshot(path=str(O/(name+'-title.png')))
    await p.keyboard.press('ArrowDown');await p.wait_for_timeout(80)
    ck(await p.evaluate('()=>menuIndex===1'),name+' keyboard menu input works after deferred startup')
    await p.evaluate('()=>{window.__bofFit();fitCanvas();window.dispatchEvent(new Event("load"));}')
    await p.wait_for_timeout(400);refit=await p.evaluate(SNAP);ck(same(title,refit,'screen'),name+' repeated fit/load events preserve identical geometry')
    await p.unroute_all(behavior='wait');await p.reload(wait_until='load');await p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);await p.wait_for_timeout(400)
    warm=await p.evaluate(SNAP);wh=await p.evaluate('()=>bootGeometry');ck(all(same(warm,q,'game-frame') and same(warm,q,'screen') for q in wh if 'screen' in q),name+' warm reload is stable from first paint')
    if name=='desktop':
     await p.evaluate('()=>setState(GS.TITLE)');await p.locator('#fs-btn').click();await p.wait_for_timeout(600);fs=await p.evaluate(SNAP)
     ck('fs' in fs['classes'].split() and fs['game-frame'][1]>=-.1,'fullscreen control still enters fitted fullscreen')
     await p.evaluate('()=>document.exitFullscreen()');await p.wait_for_timeout(400);out=await p.evaluate(SNAP)
     ck(same(title,out,'screen'),'leaving fullscreen restores the same shell geometry')
     await p.set_viewport_size({'width':1000,'height':760});await p.wait_for_timeout(400);resize=await p.evaluate(SNAP)
     ck(resize['game-frame'][1]>=0 and resize['game-frame'][1]+resize['game-frame'][3]<=761 and abs(resize['screen'][2]/resize['screen'][3]-480/512)<.003,'resize stays within viewport with correct canvas aspect')
     await p.screenshot(path=str(O/'resized.png'))
     await p.evaluate('()=>{setState(GS.STAGESEL);_setCampaignViewport();}');await p.wait_for_timeout(250)
     campaign=await p.evaluate(SNAP);ck(campaign['game-frame']==[0,0,1000,760],'campaign full-window layout retains its own viewport')
    runs.append({'name':name,'early':early,'mid':mid,'boot':boot,'title':title,'warm':warm,'geometry':history});await context.close()
   await br.close()
 finally:stop()
 ck(not errors,'zero page/console/missing-asset errors')
 report={'checks':checks,'errors':errors,'runs':runs,'scope':'Real Chromium cold, delayed and warm page navigation; native keyboard/menu and fullscreen; no mocked canvas.'}
 (O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 contact=Image.new('RGB',(1000,920),(8,10,17));g=ImageDraw.Draw(contact)
 for i,label in enumerate(['desktop-early','desktop-boot','desktop-title','narrow-title','wide-title','resized']):
  im=Image.open(O/(label+'.png')).convert('RGB');im.thumbnail((480,280));x=(i%2)*500;y=(i//2)*305;contact.paste(im,(x,y+20));g.text((x+8,y+3),label,fill=(235,235,245))
 contact.save(O/'contact.jpg',quality=92)
 print(json.dumps({'checks':len(checks),'failed':[q['name'] for q in checks if not q['ok']],'errors':errors}))
 if errors or any(not q['ok'] for q in checks):raise SystemExit(1)
asyncio.run(main())
