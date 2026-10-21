from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
from io import BytesIO
import sys,base64,json,http.server
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=Path(__file__).parent;sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/cinematic_invasion_1020';O.mkdir(exist_ok=True);checks=[];errors=[];shots=[];final='--final' in sys.argv
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport=dict(width=1280,height=720));p.set_default_timeout(180000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(50,50)
  if not final:
   p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/cinematic_invasion_art_1020.js');p.add_script_tag(content=(W/'invasion.js').read_text())
  p.evaluate('''()=>{Object.defineProperty(navigator,'getGamepads',{configurable:true,value:()=>[]});BOFCinematicDirector.cancel();run.pilot='cole';run.mode='campaign';run.score=123456;coopOn=false;drawVictory._ready=true;drawVictory._trueEnding=true;drawVictory._t=0;drawVictory._sfx={};Input.clearTaps();Input.mouse.down=false;setState(GS.VICTORY);victoryEndingWarm();}''')
  p.wait_for_function('victoryEndingReady()',polling=75)
  p.evaluate('''()=>{window.tags21=new WeakMap();window.used21=[];window.portals21=[];const get=XART.get,draw=ctx.drawImage,pd=PL11.draw;PL11.draw=function(){portals21.push(arguments[1].bank);return pd.apply(this,arguments);};XART.get=function(k){const im=get.apply(this,arguments);if(im)tags21.set(im,k);return im;};ctx.drawImage=function(im){const k=tags21.get(im);if(k)used21.push(k);return draw.apply(this,arguments);};window.seek21=t=>{drawVictory._t=t;used21=[];portals21=[];ctx.setTransform(SS,0,0,SS,0,0);drawVictory(0);return {t:drawVictory._t,last:INV20.last,hl:HL10.last,flight:HC10.last,caption:INV20.caption,portals:portals21,keys:[...new Set(used21)]};};}''')
  def capture(name,t):
   row=p.evaluate('seek21',t);data=p.evaluate('''()=>{ctx.setTransform(SS,0,0,SS,0,0);drawVictory(0);return cv.toDataURL().split(',')[1];}''');im=Image.open(BytesIO(base64.b64decode(data))).convert('RGB');im.save(O/(name+'.png'));return row,im
  cases=[('blue-portal',1.4),('approach',8),('nose-first-landing',11.5),('walk',21),('report',29),('relief',37),('alarm',42),('federation',47.5),('federation-hack',52.3),('horror',60),('base',67),('waters',77),('earth',88),('solar',100),('return',131),('credits',139),('card',148)]
  if final:cases[14:14]=[('growth-start',105.1),('growth',109),('scream',114),('scream-close',117),('escape',122)]
  for name,t in cases:
   row,im=capture(name,t);shots.append((name,im));ck(name+' renders at its actual clock',abs(row['t']-t)<.001,row)
   if name=='blue-portal':ck('Return portal uses the blue PixelLab bank, never the old purple gate',row['flight']['portal']['source'].startswith('pxv17_blue_rift_') and not any(k in [a['key'] for a in p.evaluate('AP10_CIN_ART.void')] for k in row['keys']))
   if name=='nose-first-landing':ck('Landing draws the actual front aircraft image', 'ship_cole_so6' in row['keys'] and 'ship_cole_so2' not in row['keys'])
   if name=='waters':ck('Naval siege uses actual game warboats',len(row['last']['units'])==20 and all('boat' in a['key'] for a in row['last']['units']))
   if name=='earth':ck('Earth siege uses actual game drones/carrier and black void rifts',len(row['last']['units'])==28 and row['portals'].count('black_void')==4)
  for pk in p.evaluate('CE20.pilots'):
   p.evaluate('pk=>{run.pilot=pk;hl10Warm(pk);}',pk);p.wait_for_function('hl10Warm()',polling=75)
   a=p.evaluate('seek21',11.5);c=p.evaluate('seek21',29);d=p.evaluate('seek21',60)
   ck(pk+' aircraft stays nose-first during landing',f'ship_{pk}_so6' in a['keys'] and f'ship_{pk}_so2' not in a['keys'])
   ck(pk+' new reporting pose uses its own identity bank',f'inv20_{pk}' in c['keys'])
   pixels=p.evaluate('''pk=>{seek21(29);const c=INV20.caption,hex=inv20Color(pk).slice(1),rgb=[0,2,4].map(i=>parseInt(hex.slice(i,i+2),16)),a=ctx.getImageData(Math.floor((c.x+22)*SS),Math.floor((c.y+10)*SS),Math.ceil(Math.min(200,c.w-44)*SS),Math.ceil(22*SS)).data;let n=0;for(let i=0;i<a.length;i+=4)if(rgb.every((v,k)=>Math.abs(a[i+k]-v)<8)&&a[i+3]>200)n++;return n;}''',pk)
   ck(pk+' name has its actual coloured glyph pixels',pixels>2,pixels)
   ck(pk+' has its own horrified reaction',f'inv20_{pk}_horror' in d['keys'])
   ck(pk+' speaker name uses canonical pilot palette',p.evaluate('pk=>inv20Color(pk)===PILOTS.find(p=>p.key===pk).tint',pk))
  p.evaluate("()=>{run.pilot='cole';coopOn=true;p2Index=PILOTS.findIndex(p=>p.key==='yuri');run2.score=654321;hl10Warm('yuri');}");p.wait_for_function("hl10Warm('yuri')")
  row,im=capture('coop-landing',11.5);ck('Co-op lands both actual front-facing aircraft',all(k in row['keys'] for k in ['ship_cole_so6','ship_yuri_so6']))
  row,im=capture('coop-report',29);ck('Both returning pilots give the report',len(row['last']['cast'])==2 and row['last']['partner']=='yuri');shots.append(('coop-report',im))
  for width,height in [(390,844),(1920,1080)]:
   p.set_viewport_size(dict(width=width,height=height));p.evaluate('_setCinematicViewport(true)');row,im=capture('horror-'+str(width),60);shots.append(('horror-'+str(width),im))
   cast=row['last']['cast'];Wv=p.evaluate('cutsceneViewWidth()');ck(str(width)+' all nine reactions stay inside the frame',len(cast)==9 and all(a and a['x']>0 and a['x']<Wv for a in cast))
   c=row['caption'];ck(str(width)+' caption fits cinematic canvas',c['x']>=0 and c['y']+c['h']<=p.evaluate('VH'))
   capture('title-'+str(width),131)
  p.set_viewport_size(dict(width=1280,height=720));p.evaluate('_setCinematicViewport(true)');p.evaluate("()=>{coopOn=false;run.pilot='cole';}")
  ck('New PixelLab font is loaded and all letters/numerals resolve',p.evaluate("()=>{inv20InstallFont();return bmfReady('invasion')&&'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'.split('').every(k=>BMF.invasion.map.glyphs[k]);}"))
  p.evaluate("()=>{drawVictory._sfx={};INV20.events=[];seek21(38.98);drawVictory(.04);drawVictory(.04);}");ck('Natural alarm cue fires once through existing mixer',p.evaluate("INV20.events.filter(e=>e.id==='alarm'&&e.played).length===1"),p.evaluate('INV20.events'))
  p.evaluate("()=>{drawVictory._sfx={};INV20.events=[];seek21(40);seek21(88);}");ck('Seeking across scenes does not play skipped cues',p.evaluate('INV20.events.every(e=>!e.played)'),p.evaluate('INV20.events'))
  # Native post-stage dialogue still owns timing, pad input and callbacks.
  for stage in [1,3,4,6,8,9]:
   p.evaluate('n=>{BOFCinematicDirector.cancel();BOFCinematicDirector.start(n,()=>{window.inv20Done=true;});BOFCinematicDirector.tick(.01);}',stage)
   ck('Post-stage '+str(stage)+' keeps its authored scene',p.evaluate('!!BOFCinematicDirector.current?.beats?.length'))
   p.evaluate('''()=>{const s=BOFCinematicDirector.current;s.shown=s.beats[s.i].text.length;BOFCinematicDirector.draw();}''')
   if stage in [1,4]:
    data=p.evaluate('cv.toDataURL().split(",")[1]');Image.open(BytesIO(base64.b64decode(data))).save(O/f'story-{stage}.png')
   p.evaluate('BOFCinematicDirector.finish()');ck('Post-stage '+str(stage)+' callback still completes',p.evaluate('inv20Done===true'));p.evaluate('inv20Done=false')
  p.evaluate("()=>{BOFCinematicDirector.cancel();setState(GS.VICTORY);run.mode='campaign';drawVictory._ready=true;drawVictory._trueEnding=false;drawVictory._t=28;drawVictory(0);}");ck('Standard ending retains its score card branch',p.evaluate('drawVictory._t===VICTORY_CARD_AT'))
  p.evaluate("()=>{run.mode='arcade';drawVictory._t=0;drawVictory(.1);}");ck('Arcade still uses its short score branch',p.evaluate('drawVictory._t<1'))
  if final:
   p.evaluate("()=>{run.mode='campaign';drawVictory._trueEnding=true;drawVictory._ready=true;drawVictory._t=60;Input.clearTaps();}");p.keyboard.press('Enter');p.evaluate('drawVictory(.016)');ck('Old ending clock cannot exit the new story early',p.evaluate('state===GS.VICTORY'));p.evaluate('Input.clearTaps()')
   p.evaluate('drawVictory._t=151');p.keyboard.press('Enter');p.evaluate('drawVictory(.016)');ck('Final native Start returns to title',p.evaluate('state===GS.TITLE'))
  ck('No native browser/draw/asset errors',not errors,errors);b.close()
finally:stop()
sheet=Image.new('RGB',(4*384,((len(shots)+3)//4)*238),'#101522');d=ImageDraw.Draw(sheet)
for i,(name,im) in enumerate(shots):im.thumbnail((384,216));sheet.paste(im,((i%4)*384,(i//4)*238));d.text(((i%4)*384+5,(i//4)*238+218),name,fill='white')
sheet.save(O/'ending-contact-sheet.jpg',quality=94)
report=dict(passed=sum(c['passed'] for c in checks),checks=len(checks),errors=errors,results=checks);(O/('report.json' if final else 'preflight.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'}));raise SystemExit(not all(c['passed'] for c in checks))
