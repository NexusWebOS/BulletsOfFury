from pathlib import Path
import json,sys
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/riders_roll_type_1030/dialogue';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from barrage_review_common_1025 import boot
checks=[];errors=[]
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print('PASS'if v else'FAIL',n,d if not v else'')
M=json.loads((R/'assets/game/shared/ui/riders_dialogue_1030/manifest.json').read_text())
for name,a in M['banks'].items():
 im=Image.open(R/a['path']);bounds=[a['glyphs'][str(ord(c))]['ink']for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789']
 ck(name+' capitals/digits share a complete top and baseline',all(q[1]==a['top']and q[3]==a['baseline']for q in bounds),bounds)
 ck(name+' has even cells and transparent safety margins',a['cw']%2==a['ch']%2==0 and all(q[0]>0 and q[2]<a['cw']and q[3]<a['ch']for q in bounds))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,6,errors,role='boss');p.wait_for_function('()=>pm27Live()',timeout=120000)
  text='WE WERE ONE UNIT ONCE. IT DOES NOT HAVE TO BE LIKE THIS. WE CAN STILL STOP HIM.'
  def draw(count):
   return p.evaluate('''([text,count])=>{PM27.events=[];drawWorld(0);msgFaceUse('dialogue');const old=PM27.draws;dlgBox({who:'COLE',portrait:'cole',full:text,shown:text.slice(0,count),forceShown:true,x:PLAY.x+8,y:320,pw:460,ph:84});msgFaceUse(null);return{last:CD27.history.at(-1),role:PM27.role,events:PM27.events.slice(-10),draws:PM27.draws-old}}''',[text,count])
  part=draw(10);full=draw(len(text));p.screenshot(path=str(W/'dialogue-after.png'))
  ck('Dialogue uses aligned pixel-master banks in the actual renderer',any(q['family']=='command_dialogue'for q in full['events'])and full['draws']>0,full['events'])
  ck('Typewriter reveal retains the complete line layout',part['last']['layout']==full['last']['layout'],[part['last']['layout'],full['last']['layout']])
  ck('Dialogue selects the exact authored size used by its layout',all(q['height']==full['last']['layout']['H']for q in full['events']if q['family']=='command_dialogue'))
  ck('Font override restores after dialogue drawing',full['role']is None,full['role'])
  ck('Full sentence fits the compact portrait text aperture',full['last']['layout']['height']<=38,full['last']['layout'])
  ck('No native font or game exceptions',not errors,errors);br.close()
finally:stop()
(W/'font-checks.json').write_text(json.dumps(checks,indent=2));assert all(q['passed']for q in checks)
