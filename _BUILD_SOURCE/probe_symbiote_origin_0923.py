"""Render campaign-origin beats in Chromium and check image readiness/errors."""
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import base64, io, json, sys, http.server

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
from shoot import GAME, SETUP, STEP, TRAP_RAF, serve

OUT=ROOT/'_shots/symbiote_origin_0923';OUT.mkdir(exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=serve(GAME);errors=[];report=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1500,'height':1000})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(TRAP_RAF)
  pg.evaluate(SETUP,{'state':'PLAY','stage':1,'pilot':'axel','invuln':True})
  pg.evaluate("()=>{run.mode='campaign';run.pilot='axel';campaignIntroStart(()=>{});}")
  pg.wait_for_function('()=>campaignIntroReady()',timeout=45000)
  beats=[('arrival',1.0),('satellite',5.8),('radio',10.6),('tower',15.4),
         ('land',20.2),('hq',25.0),('pov',29.8),('warroom',34.2),('pilot',38.5)]
  thumbs=[]
  for name,t in beats:
   pg.evaluate('t=>{campaignIntro.t=t;campaignIntro.ready=true;}',t)
   assert pg.evaluate(STEP,1) is None
   png=base64.b64decode(pg.evaluate("document.getElementById('screen').toDataURL('image/png').split(',')[1]"))
   (OUT/(name+'.png')).write_bytes(png)
   im=Image.open(io.BytesIO(png)).convert('RGB')
   thumbs.append(im.resize((im.width//3,im.height//3),Image.Resampling.NEAREST))
   report.append({'beat':name,'t':t,'size':im.size,'center':im.getpixel((im.width//2,im.height//2))})
  w=max(im.width for im in thumbs);h=max(im.height for im in thumbs)
  contact=Image.new('RGB',(w*3,h*3),(0,0,0))
  for i,im in enumerate(thumbs):contact.paste(im,((i%3)*w,(i//3)*h))
  contact.save(OUT/'contact.png')
  assert pg.evaluate('()=>CAMPAIGN_INTRO_BEATS.length')==11
  assert not errors,errors
  (OUT/'results.json').write_text(json.dumps({'beats':report,'errors':errors},indent=2))
  print('PASS: 9 origin/cockpit cinematic beats rendered in Chromium; no page or console errors.')
  br.close()
finally:stop()
