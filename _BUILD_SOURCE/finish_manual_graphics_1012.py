from pathlib import Path
import sys,json,zipfile
from playwright.sync_api import sync_playwright
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');E=R/'extensions/bof-field-manual';A=E/'art';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
d=json.loads((E/'data.js').read_text()[len('const MANUAL = '):-1]);port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1440,'height':1000});p.goto(f'http://localhost:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for f in d['fights']:
   if not f.get('scene') and f.get('art'):continue
   p.evaluate('f=>debugStartFight(f,{pilot:"cole"})',f);p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)}',arg=f['stage'],timeout=120000)
   p.evaluate('()=>{player.invuln=1e9;run.lives=99;}')
   for i in range(9):p.evaluate('()=>{player.invuln=1e9;}');p.evaluate(shoot.STEP,30);p.wait_for_timeout(80)
   fn=f'encounter-{f["stage"]}-{f["role"]}.png';p.screenshot(path=str(A/fn));f['scene']='art/'+fn;print(f['name'],flush=True)
  b.close()
finally:stop()
(E/'data.js').write_text('const MANUAL = '+json.dumps(d)+';',encoding='utf-8')
p=E/'guide.js';s=p.read_text(encoding='utf-8');s=s if "'sonic-wave'" in s else s.replace("function persist(){",'''add('abilities','sonic-wave','SONIC BOOM / SOUND FRONT','COLE · SECOND ATTACK','The damaging ring expands ahead of the ship. Distortion is left behind in the air, so the trail and damage front are different layers. This is the actual authored wave frame.','art/nsw_ring_2.png','#7ad63a');
add('abilities','heavy-mount','HEAVY TURRET / DOCKING MOUNT','LIZZIE · SECOND ATTACK','The attachment arcs in, scales down and docks at the nose. Heavy slugs trade fire rate for damage. The weapon expires independently of Atom Bomb stock.','art/nlz_mount.png','#ffc21a');
function persist(){''');p.write_text(s,encoding='utf-8')
read=E/'README.md';read.write_text(read.read_text(encoding='utf-8')+'\nRevision 1.1: illustrated HUD, nine ability loadouts, five paired-ability explanations, 24 enemy plates, artwork or live captures for every roster encounter, key fight arena screenshots. Original SPECIAL_INFO summaries were incomplete; display names now come from PC_SPECIAL and mechanics from the implemented controllers. Detailed attack timing research remains incomplete for some encounters.\n',encoding='utf-8')
O=Path(r'C:\Users\Mike\Documents\New project\output\bof-field-manual')
with zipfile.ZipFile(O/'BOF-Field-Manual-1.1.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in E.rglob('*'):
  if f.is_file():z.write(f,Path('bof-field-manual')/f.relative_to(E))
print('All encounters illustrated',len(d['fights']))
