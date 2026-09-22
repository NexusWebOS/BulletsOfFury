from playwright.sync_api import sync_playwright
from shoot import serve, SETUP, STEP, TRAP_RAF
from pathlib import Path

root=Path(__file__).resolve().parents[1]
port,stop=serve(str(root))
try:
    with sync_playwright() as pw:
        br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
        pg=br.new_page(viewport={'width':1100,'height':1200})
        pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
        pg.wait_for_function('()=>(window.__bofFrames|0)>4')
        pg.evaluate(TRAP_RAF)
        pg.evaluate(SETUP,{'state':'PLAY','stage':3,'pilot':'cole','invuln':True})
        pg.evaluate(STEP,8)
        print(pg.evaluate("""() => Object.fromEntries(['game-frame','hud-row','equip-dom','equipcv','screen-area','screen'].map(id=>{
          let q=document.getElementById(id),r=q.getBoundingClientRect();
          return [id,{x:r.x,y:r.y,w:r.width,h:r.height}];}))"""))
        br.close()
finally:
    stop()
