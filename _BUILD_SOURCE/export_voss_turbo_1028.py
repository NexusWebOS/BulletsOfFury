from pathlib import Path
import ast,base64
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/voss_turbo_1028';D.mkdir(parents=True,exist_ok=True)
def strings(f):return[n.value for n in ast.walk(ast.parse((R/f).read_text(encoding='utf8')))if isinstance(n,ast.Constant)and isinstance(n.value,str)]
setup=next(s for s in strings('_BUILD_SOURCE/probe_feedback_1002.py')if s.startswith('c=>{ht27Stop'));init=next(s for s in strings('_BUILD_SOURCE/probe_rebel_balance_1019.py')if s.startswith('gang=>{window.R='))
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page();p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.evaluate(setup,dict(stage=6,kind='rebelsquad',diff='normal',pilot='cole'));p.evaluate(init,True)
  p.wait_for_function("()=>{stageLoadTick();return stageLoadReady(6)&&[0,1,2,3,4,5,6,7].every(i=>XART.rdy('florb_'+i))&&XART.rdy('nfrb_0')}")
  for key in ['florb_'+str(i)for i in range(8)]+['nfrb_0']:
   data=p.evaluate("key=>{const im=XART.get(key),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return c.toDataURL().split(',')[1]}",key);(D/(key+'.png')).write_bytes(base64.b64decode(data))
  b.close()
finally:stop()
print('Exported actual native orb sources through XART and native drawImage')
