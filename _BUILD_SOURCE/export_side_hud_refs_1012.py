"""Native game references for a review-only side HUD; no shipping edits."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot,base64,json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/previews/side_hud_1012';QA=ROOT/'_shots/side_hud_1012'
OUT.mkdir(parents=True,exist_ok=True);QA.mkdir(parents=True,exist_ok=True)
errors=[];captures={}
def save(url,path):path.write_bytes(base64.b64decode(url.split(',')[1]))
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--mute-audio','--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport=dict(width=1920,height=1080));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4')
  p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(40)
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=1,pilot='cole',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&bmfReady("game")&&fs11ArtReady("cole")}',polling=50)
  for i in range(16):
   err=p.evaluate(shoot.STEP,30)
   if err:errors.append(err)
   p.wait_for_timeout(35)
  def capture(name):
   p.evaluate('()=>{window.__bofFit();}')
   captures[name]=p.evaluate('()=>{const r=cv.getBoundingClientRect();return {state,backing:[cv.width,cv.height],logical:[VW,VH],screen:[r.x,r.y,r.width,r.height],classes:document.body.className};}')
   save(p.evaluate('cv.toDataURL("image/png")'),OUT/(name+'.png'))
   p.screenshot(path=str(QA/(name+'-current.png')))
  capture('gameplay')
  p.evaluate('()=>{setState(GS.LAUNCH);stateT=0;drawLaunch._phase=undefined;}')
  for i in range(6):
   p.evaluate(shoot.STEP,30);p.wait_for_timeout(80)
  capture('fly-in')
  p.evaluate('()=>{setState(GS.CONTINUE);stateT=3;drawContinue._vo=true;ctx.setTransform(SS,0,0,SS,0,0);drawContinue(0);}')
  capture('continue')
  p.wait_for_function('()=>XART.rdy("hud_radar_bezel_0924")',polling=50)
  save(p.evaluate('()=>{const im=XART.get("hud_radar_bezel_0924"),c=document.createElement("canvas");c.width=im.width;c.height=im.height;c.getContext("2d").drawImage(im,0,0);return c.toDataURL();}'),OUT/'radar-bezel.png')
  br.close()
finally:stop()
report=dict(captures=captures,errors=errors)
(OUT/'native-references.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
raise SystemExit(bool(errors))
