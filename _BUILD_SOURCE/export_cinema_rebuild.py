from pathlib import Path
import sys,json,base64,hashlib
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');O=Path(__file__).parent/'BOF-Cinema-Rebuild';D=O/'references';D.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
pilots=['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']
port,stop=shoot.serve(str(R));records=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(120000)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  groups={'pilots':['inv20_'+k for k in pilots], 'ships':['ship_'+k for k in pilots], 'enemies':['ns9e_wskim_idle','ns9e_pneedle_idle','ns9e_vmanta_idle','ns9x_dreadv','nef_s1_missile_gunboat_intact_idle','nef_s1_river_patrol_boat_intact_idle']}
  groups['front-rear']=['ship_'+k+'_so'+str(v) for k in pilots for v in [6,2]]
  groups['portals']=p.evaluate("PL11.keys('blue_rift').filter((k,i)=>i===3).concat(DR21_ART.banks.symbiote.slice(0,1).map(a=>a.key))")
  groups['environments']=['cut_furyhq_command_center','cin_story_lab_empty','cinend_deep_space']
  (D/'runtime-groups.json').write_text(json.dumps(groups,indent=2),encoding='utf-8')
  for group,keys in groups.items():
   exports=[]
   for key in keys:
    p.wait_for_function('k=>XART.rdy(k)',arg=key,polling=50)
    q=p.evaluate("k=>{const im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);return {w:c.width,h:c.height,data:c.toDataURL('image/png').split(',')[1]};}",key)
    target=D/(key+'.png');target.write_bytes(base64.b64decode(q.pop('data')));records.append(dict(key=key,group=group,**q,sha256=hashlib.sha256(target.read_bytes()).hexdigest()));exports.append((key,target))
   sheet=Image.new('RGB',(1536,512*((len(exports)+2)//3)),'#101824');g=ImageDraw.Draw(sheet)
   for n,(key,path) in enumerate(exports):
    im=Image.open(path).convert('RGBA');im.thumbnail((480,466),Image.Resampling.NEAREST);x=n%3*512+(512-im.width)//2;y=n//3*512+20;sheet.paste(im,(x,y),im);g.text((n%3*512+20,n//3*512+490),key,fill='white')
   sheet.save(D/(group+'-identity.png'))
  b.close()
finally:stop()
(D/'manifest.json').write_text(json.dumps(records,indent=2),encoding='utf-8');print('Exported',len(records),'actual runtime references')
