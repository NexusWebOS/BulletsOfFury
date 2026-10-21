from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/hammer_acting_1021/references';D.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page();p.set_default_timeout(180000);p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('()=>{for(const k of ["arch_ship_transform","arch_spiked_ball","arch_death","arch_stun_0920"])XART.rdy(k);}')
  p.wait_for_function('()=>["arch_ship_transform","arch_spiked_ball","arch_death","arch_stun_0920"].every(k=>XART.rdy(k))')
  audit=[]
  for name,key,frame in [('blue_ship','ship_transform',15),('blue_ball','spiked_ball',15),('blue_kneel','stun_0920',1)]:
   row=p.evaluate('''([key,f])=>{const q=hammerArchFrame(key,f),c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d');g.imageSmoothingEnabled=false;const k=Math.min(1,228/Math.max(q.sw,q.sh)),w=q.sw*k,h=q.sh*k;g.drawImage(q.im,q.sx,q.sy,q.sw,q.sh,128-w/2,112-h/2,w,h);return{png:c.toDataURL(),source:[q.sw,q.sh],scale:k};}''',[key,frame]);(D/(name+'.png')).write_bytes(base64.b64decode(row.pop('png').split(',')[1]));audit.append(dict(name=name,key=key,frame=frame,**row))
  (D/'native-export.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps(audit));b.close()
finally:stop()
