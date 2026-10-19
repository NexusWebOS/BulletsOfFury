"""Small GIFs of actual native review gameplay, not synthesized boss composites."""
from pathlib import Path
from io import BytesIO
from playwright.sync_api import sync_playwright
from PIL import Image
import shoot

R=Path(__file__).resolve().parents[1];O=R/'_shots/lightning_depth_1018';O.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)))
  for name,url in [('dracodia-lightning','docs/previews/dracodia_archive_1018/index.html?scene=spiralLightning&difficulty=furious'),('stage4-lightning','docs/previews/storm_assault_1018/index.html?scene=charge&difficulty=furious')]:
   p.goto(f'http://127.0.0.1:{port}/'+url);p.wait_for_function('()=>ready&&!busy&&!document.querySelector("#replay").disabled');f=p.frames[1];f.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(40)
   p.click('#replay');p.wait_for_function('()=>ready&&!busy&&!document.querySelector("#replay").disabled')
   frames=[]
   for i in range(52):
    f.evaluate('()=>{for(let i=0;i<5;i++){updatePlay(1/60);drawWorld(1/60);}SC12.refresh();__bofFit();}');p.wait_for_timeout(5)
    im=Image.open(BytesIO(p.screenshot())).convert('RGB').resize((960,600),Image.Resampling.NEAREST);frames.append(im)
   # Sample actual pixels. Tiny filtered thumbnails average blue-white arcs
   # into grey and give the GIF a misleading palette despite correct gameplay.
   palette=Image.new('RGB',(960*2,600*4))
   for j in range(8):palette.paste(frames[j*7],(j%2*960,j//2*600))
   palette=palette.quantize(colors=256)
   gif=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
   gif[0].save(O/(name+'.gif'),save_all=True,append_images=gif[1:],duration=83,loop=0,optimize=True)
   frames[24].save(O/(name+'.png'))
   print(name+':52 actual gameplay captures saved',flush=True)
  assert not errors,errors
  br.close()
finally:stop()
