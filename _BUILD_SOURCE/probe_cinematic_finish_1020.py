from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
from io import BytesIO
import ast,base64,json,http.server
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinematic_finish_1020';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport=dict(width=1280,height=720));p.set_default_timeout(180000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''))
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(100,100)
  p.evaluate('''()=>{Object.defineProperty(navigator,'getGamepads',{configurable:true,value:()=>[]});BOFCinematicDirector.cancel();run.pilot='cole';run.mode='campaign';drawVictory._ready=false;drawVictory._trueEnding=true;drawVictory._t=0;drawVictory._sfx={};drawVictory._wait=drawVictory._waitF=0;Input.clearTaps();Input.mouse.down=false;setState(GS.VICTORY);victoryEndingWarm();}''')
  p.wait_for_function('victoryEndingReady()&&ce20Warm()',polling=75)
  p.evaluate('''()=>{window.tags20=new WeakMap();window.used20=[];const get=XART.get,draw=ctx.drawImage;XART.get=function(k){const im=get.apply(this,arguments);if(im)tags20.set(im,k);return im;};ctx.drawImage=function(im){const key=tags20.get(im);if(key)used20.push(key);return draw.apply(this,arguments);};window.seek20=t=>{drawVictory._t=t;drawVictory._ready=true;used20=[];ctx.setTransform(SS,0,0,SS,0,0);drawVictory(0);return{t:drawVictory._t,last:CE20.last,hl:HL10.last,keys:[...new Set(used20)]};};}''')
  def image(name):
   im=Image.open(BytesIO(base64.b64decode(p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);if(state===GS.VICTORY)drawVictory(0);else if(BOFCinematicDirector.active)BOFCinematicDirector.draw();return cv.toDataURL().split(",")[1];}')))).convert('RGB');im.save(O/(name+'.png'));return im
  shots=[]
  for t,name in [(1.5,'portal'),(7.5,'approach'),(11.5,'landing'),(21,'doorway'),(28,'victory-debrief'),(34,'pilot-epilogue'),(39,'squad'),(46,'credits'),(51,'isolated-echo'),(54.5,'federation'),(57.5,'stinger'),(65,'final-card')]:
   row=p.evaluate('seek20',t);shots.append((name,image(name)));ck(name+' renders at the requested native clock',abs(row['t']-t)<.001,row)
  for pk in ['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']:
   p.evaluate('pk=>{run.pilot=pk;hl10Warm(pk);}',pk);p.wait_for_function('hl10Warm()',polling=75)
   a=p.evaluate('seek20',1.5);bb=p.evaluate('seek20',11.5);c=p.evaluate('seek20',34);d=p.evaluate('seek20',65)
   ck(pk+' keeps actual front/rear aircraft',f'ship_{pk}_so6' in a['keys'] and f'ship_{pk}_so2' in bb['keys'])
   ck(pk+' has an individual epilogue and actual body',c['last']['pilot']==pk and any(q['pilot']==pk for q in c['last']['cast']) and c['last']['caption']==p.evaluate('pk=>CE20_EPILOGUES[pk]',pk))
   ck(pk+' final card uses the actual victory portrait',f'comm_{pk}_victory' in d['keys'],d['keys'])
   if pk in ['cole','yuri','falva']:image(pk+'-epilogue-final')
  retired=p.evaluate("victoryEndingKeys().filter(k=>/^sv10_|^hc10_infection|^cinend_symbiote/.test(k))");ck('Ending excludes retired organic infection animation dependencies',not retired,retired)
  row=p.evaluate("""()=>{const native=SV10.base.load,retired=new Set(CE20.base.survivorAssets().map(a=>a.key));let keys=[];SV10.base.load=(n,k)=>{keys=k;};try{stageLoadBegin(8,[]);}finally{SV10.base.load=native;}return{old:keys.filter(k=>retired.has(k)),new:keys.includes('ce20_debrief')&&keys.includes('ce20_relay'),retired:retired.size,retiredBytes:CE20.base.survivorAssets().reduce((s,a)=>s+a.w*a.h*4,0)};}""")
  ck('Stage loading also excludes the retired family while keeping the new ending',not row['old'] and row['new'],row)
  p.evaluate("()=>{run.pilot='cole';drawVictory._trueEnding=false;}");row=p.evaluate('seek20',28);ck('Standard campaign branch still reaches its native final card',row['t']==p.evaluate('VICTORY_CARD_AT') and row['last']['scene']=='final-card')
  p.evaluate("()=>{run.mode='arcade';drawVictory._t=0;drawVictory._ready=true;}");p.evaluate('drawVictory(.1)');ck('Arcade remains on its native short score-card branch',p.evaluate("drawVictory._t<1&&run.mode==='arcade'"))
  p.evaluate("()=>{run.mode='campaign';drawVictory._trueEnding=true;}")
  for width,height in [(390,844),(1280,720),(1920,1080)]:
   p.set_viewport_size(dict(width=width,height=height));p.evaluate('_setCinematicViewport(true)');row=p.evaluate('seek20',39);image(f'squad-{width}')
   cast=row['last']['cast'];W=p.evaluate('cutsceneViewWidth()');H=p.evaluate('VH');ck(str(width)+' all nine actual pilot bodies remain inside the scene',len(cast)==9 and all(0<q['x']<W and q['bottom']<=H*.71 and q['bottom']-q['height']>0 for q in cast),cast)
   p.evaluate('seek20',65);image(f'card-{width}');ck(str(width)+' cinematic canvas matches the viewport aspect',p.evaluate('Math.abs(cv.width/cv.height-innerWidth/innerHeight)<.01'))
  p.set_viewport_size(dict(width=1280,height=720));p.evaluate('_setCinematicViewport(true)')
  p.evaluate("()=>{drawVictory._sfx={};CE20.events=[];seek20(40);seek20(51);seek20(54.5);}");ck('Seeking does not replay missed sound cues',p.evaluate('CE20.events.every(e=>!e.played)'),p.evaluate('CE20.events'))
  p.evaluate("()=>{drawVictory._sfx={};CE20.events=[];seek20(26.4);drawVictory(.12);seek20(31.60);drawVictory(.04);}");ck('Natural scene cue crossings request their shared mixer sounds',p.evaluate('CE20.events.some(e=>e.played&&e.name==="blip")&&CE20.events.some(e=>e.played&&e.name==="select")'),p.evaluate('CE20.events'))
  # Native cinematic director: preserve its input, branch callbacks and real pilot assets.
  for stage in [1,2,3,4,5,6,7,8,9]:
   p.evaluate('stage=>{BOFCinematicDirector.cancel();run.pilot="cole";run.mode="campaign";BOFCinematicDirector.start(stage,()=>{window.storyCompleted20=true;});BOFCinematicDirector.tick(.01);}',stage)
   scene=p.evaluate('BOFCinematicDirector.current');ck('Post-stage '+str(stage)+' keeps its native scene and branch',bool(scene and scene['beats']))
   for i,beat in enumerate(scene['beats']):
    if beat.get('_ce20Reveal') or beat.get('_ce20Hug') or (beat['who'] in ['COLE','DECKER'] and i==0):
     p.evaluate('i=>{const s=BOFCinematicDirector.current;s.i=i;s.t=2;s.shown=s.beats[i].text.length;for(const k of [s.beats[i].art,s.beats[i].bg])if(k)XART.rdy(k);}',i)
     if beat.get('_ce20Hug'):p.wait_for_function('XART.rdy("cin_cole_decker_hug_0924")')
     p.wait_for_timeout(100);p.evaluate('BOFCinematicDirector.draw()');image(f'story-{stage}-{i}')
   ck('Post-stage '+str(stage)+' uses actual pilot bodies and approved narrative poses',p.evaluate("BOFCinematicDirector.current.beats.every(b=>!CE20.pilots.includes(b.who.toLowerCase())||b.art===campaignIntroPortraitKey(b.who.toLowerCase())||b._ce20Hug&&b.art==='cin_cole_decker_hug_0924')"))
   if stage==3:ck('Original Cole/Decker lab hug still draws its approved native action artwork',p.evaluate("CE20.draws.cin_cole_decker_hug_0924>0"))
   p.evaluate('BOFCinematicDirector.finish()');ck('Post-stage '+str(stage)+' native callback runs once',p.evaluate('storyCompleted20===true'));p.evaluate('storyCompleted20=false')
  ck('No browser, draw or missing-asset errors',not errors,errors);b.close()
finally:stop()
sheet=Image.new('RGB',(3*384,((len(shots)+2)//3)*232),'#101522');d=ImageDraw.Draw(sheet)
for i,(name,im) in enumerate(shots):im.thumbnail((384,210));sheet.paste(im,((i%3)*384,(i//3)*232));d.text(((i%3)*384+8,(i//3)*232+211),name,fill='white')
sheet.save(O/'ending-contact-sheet.jpg',quality=90)
report=dict(passed=sum(q['passed'] for q in checks),checks=len(checks),errors=errors,results=checks);(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'}));raise SystemExit(not all(q['passed'] for q in checks))
