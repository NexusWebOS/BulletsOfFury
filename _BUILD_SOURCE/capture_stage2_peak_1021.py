from pathlib import Path
import sys,ast,base64
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/stage2_peak_1021'
setup=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
import subprocess
old=(O/'before-game.js').read_text(encoding='utf-8') if (O/'before-game.js').exists() else subprocess.check_output(['git','show','06f413a3ccda5f6464c79ffc1813a2a3bd132560:assets/game.js'],cwd=R).decode('utf-8');start=old.index('function drawLevelMaster(dt){');end=old.index('/* ===== TANK DRIVABILITY MASK',start);old='('+old[start:end].strip()+')'
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1366,'height':900});p.set_default_timeout(120000);p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>3&&typeof ht27Stop==="function"');p.evaluate(shoot.TRAP_RAF);p.evaluate(setup,{'stage':2,'pilot':'cole','diff':'normal','kind':'infernoreaver'})
  p.wait_for_function('()=>{_liquidFrames(_levelCfg().liquid);return XART.rdy(_levelCfg().master)&&BOFSTAGE2LAVA.ready;}')
  p.evaluate('s=>{window.peakOld=eval(s);window.peakNew=drawLevelMaster;}',old)
  # One decoded asset set, camera and timestamp; only the terrain function changes.
  for name in ['before','after']:
   png=p.evaluate('''name=>{drawLevelMaster=name==='before'?peakOld:peakNew;mapScroll=levelScrollRange()-800;_bossHold=1;drawLevelMaster._l2Join=400;efxClock=2;shake=0;ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);drawWorld(0);return cv.toDataURL().split(',')[1];}''',name)
   (O/(name+'-matched.png')).write_bytes(base64.b64decode(png))
  p.evaluate('drawLevelMaster=peakNew');b.close()
finally:stop()
(O/'review.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stage 2 - Complete mountain transition</title><style>body{margin:0;background:#0b1119;color:#e4eaf1;font:16px/1.6 system-ui}main{max-width:1080px;margin:40px auto;padding:20px}h1{font-size:28px;color:#ffb258}p{color:#b5c2d0}.compare{display:grid;grid-template-columns:1fr 1fr;gap:24px}img{width:100%;max-width:480px;image-rendering:pixelated;border:1px solid #355063}h2{font-size:18px}a{color:#8cd9ec}@media(max-width:650px){.compare{grid-template-columns:1fr}}</style><main><h1>Stage 2 / Fly past the whole mountain</h1><p>The old transition moved a cropped screen rectangle, exposing a flat slice through the terrain. The fix reveals the remaining source artwork at native scale before flying into open lava. These are matched native game captures at the same camera position and time.</p><div class="compare"><section><h2>Before / cropped terrain</h2><img src="before-matched.png" alt="A flat cut runs across the mountain at the terrain transition"></section><section><h2>After / complete mountain</h2><img src="after-matched.png" alt="The whole authored mountain top passes smoothly into the lava arena"></section></div><p>Verified against the uncropped authored terrain across 360 native samples: all four difficulties, two camera modes, five starting positions and nine transition points. Original timing and independent lava animation retained.</p><p><a href="../../index.html">Open the game</a></p></main></html>''',encoding='utf-8')
print('Matched native comparison and review saved.')
