"""Render actual candidate sprites for comparisons with the recording."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_shots/playthrough_1011/identity';OUT.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--mute-audio']);p=br.new_page(viewport=dict(width=1200,height=1000));p.set_default_timeout(120000)
  p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for stage,group,keys in [(6,'small',[f'l6x_{k}' for k in ['st','tf','cw','cr','tl','hw']]+['intcp','racer','topgun']),(7,'toxic',['s7lamprey','s7barge','s7pipe','s7sampler','s7serpent','s7mine','s7canister','s7tank','s7skimmer'])]:
   p.evaluate(shoot.SETUP,dict(state='PLAY',stage=stage,pilot='maverick',invuln=True));p.wait_for_function('n=>{stageLoadTick();return stageLoadInfo(n).ready}',arg=stage)
   p.evaluate('''keys=>{BOFCinematicDirector.cancel();story=s6Opening=null;H3.release=false;H3.ending=null;camX=0;enemies=[];window.units=keys.map((k,i)=>spawnEnemy(k,80+i%3*160,90+Math.floor(i/3)*175,{})).filter(Boolean);for(const e of units){e.enter=false;e.t=2;e._drawY=e.y;e.spin=0;}}''',keys)
   for i in range(12):
    p.evaluate('''()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#162030';ctx.fillRect(0,0,VW,VH);for(const e of units){drawEnemy(e);pcFontCenter(e.type,e.x,e.y+70,11,'#fff',1);}}''');p.wait_for_timeout(100)
   p.locator('#screen').screenshot(path=str(OUT/(group+'.png')))
   print(p.evaluate('units.map(e=>({type:e.type,art:e.art,pattern:e.pattern,mod:e._modTank,dr:e._dr}))'),flush=True)
  br.close()
finally:stop()
