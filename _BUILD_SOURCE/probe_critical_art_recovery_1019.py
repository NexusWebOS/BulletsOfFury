"""Abort actual critical PNG requests once; verify real native recovery and pixels."""
from pathlib import Path
from urllib.parse import urlparse,parse_qs
import ast,http.server,json,sys,time
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/asset-recovery';O.mkdir(exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
targets={'/assets/game/shared/fonts/fonts/command_0914/game-alpha.png':'game-font','/assets/game/shared/ui/ui_hud.png':'nca_ui_hud','/assets/game/shared/ui/ui_bossmode_fx.png':'nca_ui_bossmode_fx'}
checks=[];cases=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  for arm in ['disabled','repaired','persistent']:
   br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);context=br.new_context(viewport=dict(width=1600,height=1000));p=context.new_page();p.set_default_timeout(180000)
   attempts={k:0 for k in targets};injected=[];requests=[];browser=[]
   p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});"+('window.AR19_OFF=1;' if arm=='disabled' else ''))
   def route(r):
    path=urlparse(r.request.url).path
    if path in targets:
     attempts[path]+=1
     requests.append(dict(path=path,retry=parse_qs(urlparse(r.request.url).query).get('bof_art_retry',[None])[0]))
     if attempts[path]==1 or arm=='persistent':injected.append(dict(path=path,attempt=attempts[path]));r.abort('failed');return
    r.continue_()
   p.route('**/*',route)
   p.on('pageerror',lambda e:errors.append(str(e)))
   p.on('console',lambda m:browser.append(m.text[:500]) if m.type=='error' else None)
   p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
   # This guard was an investigation candidate, deliberately excluded from the
   # shipping index after the clean harness passed with it disabled.
   if p.evaluate('typeof AR19==="undefined"'):p.add_script_tag(path=str(O.parent/'candidates/critical_art_recovery_1019.js'))
   p.evaluate(SETUP,dict(stage=1,kind='razorback',mini=True,diff='normal',pilot='cole'))
   # These are the actual existing native Images. No ready flags or substitute
   # canvases/images are inserted into either cache.
   p.evaluate('XART.rdy("nca_ui_hud");XART.rdy("nca_ui_bossmode_fx");')
   if arm=='repaired':
    p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&bmfReady("game")&&XART.rdy("nca_ui_hud")&&XART.rdy("nca_ui_bossmode_fx")}',polling=50)
   else:p.wait_for_timeout(2000)
   row=p.evaluate('''()=>({candidateOnly:true,font:bmfReady('game'),fontSize:[BMF.game.img.naturalWidth,BMF.game.img.naturalHeight],hud:XART.rdy('nca_ui_hud'),boss:XART.rdy('nca_ui_bossmode_fx'),hudSize:[XART.raw('nca_ui_hud').naturalWidth,XART.raw('nca_ui_hud').naturalHeight],events:AR19.events,load:stageLoadInfo(1)})''')
   row.update(arm=arm,attempts=attempts.copy(),requests=requests.copy(),injected=injected.copy(),expectedBrowserErrors=browser.copy());cases.append(row)
   if arm=='disabled':
    ck('Busted control reproduces all three permanently cached failed Images',not row['font'] and not row['hud'] and not row['boss'] and not row['events'],row)
   elif arm=='repaired':
    ck('Actual font and both original UI PNGs recover after their first request fails',row['font'] and row['hud'] and row['boss'] and row['fontSize']==[512,160] and row['hudSize']==[3903,4029],row)
    # The same font URL has another native consumer with its own Image. Count
    # actual recovery requests by their tagged URL, not all requests for a path.
    retries=[q for q in requests if q['retry'] is not None]
    ck('Exactly one tagged retry per transiently failed Image',len(retries)==3 and all(q['retry']=='1' for q in retries) and len([e for e in row['events'] if e['event']=='recovered'])==3,row)
    pixels=p.evaluate('''()=>{const draw=ctx.drawImage;let blits=0;ctx.drawImage=function(im){if(im===BMF.game.img)blits++;return draw.apply(this,arguments);};ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,ctx.canvas.width/SS,ctx.canvas.height/SS);bmfDrawOn(ctx,'game','LIVES 03',80,80,24,'left');const rgba=ctx.getImageData(0,0,ctx.canvas.width,ctx.canvas.height).data;let ink=0;for(let i=3;i<rgba.length;i+=4)if(rgba[i]>100)ink++;ctx.restore();ctx.drawImage=draw;return{blits,ink};}''')
    ck('Recovered authored font really blits visible pixels through the native game context',pixels['blits']>=7 and pixels['ink']>100,pixels)
    p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();');p.screenshot(path=str(O/'recovered-full-field.png'))
   else:
    retries=[q for q in requests if q['retry'] is not None]
    ck('Persistent failures stop after two retries rather than loop or invent readiness',not row['font'] and not row['hud'] and not row['boss'] and len(retries)==6 and all(sorted(q['retry'] for q in retries if q['path']==path)==['1','2'] for path in targets) and len([e for e in row['events'] if e['event']=='retry'])==6,row)
   # Console errors here are the deliberately aborted requests, recorded above.
   # Keep any JavaScript/draw exceptions or unrelated HTTP failures as failures.
   unrelated=[m for m in browser if 'net::ERR_FAILED' not in m]
   errors.extend(unrelated);context.close();br.close()
finally:stop()
ck('No unexpected JavaScript,draw or network errors',not errors,errors);report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,cases=cases,errors=errors,method='Native Chromium and actual unchanged PNGs. Deliberately abort the first critical-asset request (or every request in the cap test); record those expected network errors. Busted control, real source-image dimensions, native font blits and full-field screenshot verify the recovery. No image/readiness mocks.');(O/'native-report.json').write_text(json.dumps(report,indent=2)+'\n');sys.exit(bool(report['failed']))
