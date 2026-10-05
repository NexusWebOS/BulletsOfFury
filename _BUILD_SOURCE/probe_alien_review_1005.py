"""Verify the review's ordinary password launch, not a forced combat fixture."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/alien_arena_1005';errors=[]
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1200,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/_shots/alien_arena_1005/review.html',timeout=120000)
  p.get_by_role('button',name='FINAL3',exact=True).click();p.wait_for_function('()=>document.getElementById("status").textContent==="Practice ready."',timeout=120000)
  f=p.frame_locator('#game');game=p.frames[1];game.evaluate(sh.TRAP_RAF)
  game.wait_for_function('()=>Object.values(AA5_ART).every(a=>a.every(c=>XART.rdy(c.key)))',timeout=120000,polling=50)
  for i in range(35):game.evaluate('()=>{for(let i=0;i<20;i++){player.invuln=1e9+2;updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}}');p.wait_for_timeout(8)
  result=game.evaluate('()=>({phase:j3State(boss)?.encounter,mode:boss?._r30?.mode,arena:aa5Arena(boss),code:AA5.draws.code,void:AA5.draws.void,diff:diffKey})')
  p.locator('#game').screenshot(path=str(O/'review-playable.png'))
  assert result['phase']==2 and result['mode']=='fight' and result['arena'] and result['code'] and result['void'] and result['diff']=='furious' and not errors
  result['errors']=errors;(O/'review-launch.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result));b.close()
finally:stop()
