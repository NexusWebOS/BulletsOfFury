from pathlib import Path
import sys,json,http.server,subprocess
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/intro_repair_1021';http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R));errors=[];rows=[]
def functions(s):
 return s[s.index('function ui20PanelLayout('):s.index('function ui20Polygon(')]+s[s.index('function ui20Panel('):s.index('function ui20Portrait(')]
old=functions(subprocess.check_output(['git','show','HEAD:assets/command_ui_1020.js']).decode());new=functions((R/'assets/command_ui_1020.js').read_text())
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport=dict(width=1920,height=1080));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&ASSETS.ready');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('()=>{run.pilot="yuri";campaignIntroStart();campaignIntroWarm();UI20.warm();}');p.wait_for_function('()=>campaignIntroReady()&&XART.rdy("ui20_dialogue-a")&&XART.rdy("cinend_deep_space")&&XART.rdy("cin_federation_station_1")')
  if not p.evaluate('typeof IP21!=="undefined"'):
   p.add_script_tag(content='const IP21_ART={banks:{}};');p.add_script_tag(path=str(R/'assets/intro_repair_1021.js'))
  for width,height in [(1920,1080),(1366,768),(390,844)]:
   p.set_viewport_size(dict(width=width,height=height));p.evaluate('_setCinematicViewport(true)');p.wait_for_timeout(100)
   for label,code in [('before',old),('after',new)]:
    p.add_script_tag(content=code)
    row=p.evaluate('''()=>{const W=cutsceneViewWidth(),H=VH,b=IP21.beats.find(q=>q.federation),c=campaignIntro;c.t=b.to-.5;ctx.setTransform(SS,0,0,SS,0,0);cinCover('cinend_deep_space',W,H,.5);ip21Caption(b,c,W,H,1);const d=IP21.caption,a=ctx.getImageData(Math.floor((d.x+1)*SS),Math.floor((d.y+d.h*.4)*SS),Math.max(1,Math.floor(40*SS)),Math.max(1,Math.floor(d.h*.2*SS))).data;let metal=0;for(let i=0;i<a.length;i+=4)if(Math.min(a[i],a[i+1],a[i+2])>45&&Math.max(a[i],a[i+1],a[i+2])-Math.min(a[i],a[i+1],a[i+2])<35)metal++;return{W,H,caption:d,metal};}''')
    row.update(viewport=[width,height],version=label);rows.append(row);p.screenshot(path=str(O/(f'caption-{label}-{width}.png')))
  b.close()
finally:stop()
q=dict(rows=rows,errors=errors);(O/'caption-report.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(dict(errors=errors,rows=[dict(viewport=r['viewport'],version=r['version'],metal=r['metal'],bounds=[r['caption'][k] for k in ['x','y','w','h']],layout=r['caption']['layout']) for r in rows])));sys.exit(bool(errors))
