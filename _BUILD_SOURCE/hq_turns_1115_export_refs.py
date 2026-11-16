from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
R=Path('D:/BOF-Downloads/2026-11-14/RevG-source');O=R/'_shots/hq_turns_1115';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
with sync_playwright()as w:
 b=w.chromium.launch();p=b.new_page();p.goto('http://127.0.0.1:8765/index.html?hq-turn-keys');p.wait_for_function('window.__bofFrames>5');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{for(const pk of HQ19_PILOTS)for(const suffix of ['', '_pv0','_pv1','_pv2','_pv3','_pv4'])for(const tail of ['','_g1','_g2'])XART.rdy('ship_'+pk+suffix+tail);}")
 p.wait_for_function("()=>HQ19_PILOTS.every(pk=>['','_pv0','_pv1','_pv2','_pv3','_pv4'].every(s=>XART.rdy('ship_'+pk+s)&&XART.rdy('ship_'+pk+s+'_g1')&&XART.rdy('ship_'+pk+s+'_g2')))")
 data=p.evaluate("""()=>{const out=[];for(const pk of HQ19_PILOTS){const prior=player._bank;for(const bank of [-.72,-.25,0,.25,.72]){player._bank=bank;const right=SHIP_BANK_FLIP[pk]?bank<0:bank>0,key='ship_'+pk+(Math.abs(bank)<.06?'':Math.abs(bank)<.5?(right?'_pv3':'_pv1'):(right?'_pv4':'_pv0')),im=D27_RAW_GET(key),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);out.push({pilot:pk,bank,key,w:im.width,h:im.height,png:c.toDataURL('image/png')});}player._bank=prior;}return out;}""")
 for a in data:
  name=a['key']+'.png';(O/name).write_bytes(base64.b64decode(a.pop('png').split(',')[1]));a['file']=name
 (O/'native-banks.json').write_text(json.dumps(data,indent=2),encoding='utf8')
 print(json.dumps([x for x in data if x['pilot']=='juggernaut'],indent=2));b.close()
