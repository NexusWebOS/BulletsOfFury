from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
S=R/'_BUILD_SOURCE/stage8_amplify_1101';Q=R/'_shots/stage8_amplify_1101'
for p in[S,Q]:p.mkdir(parents=True,exist_ok=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page(viewport=dict(width=1280,height=800));p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(8,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)}',timeout=180000)
 specs=json.loads((R/'_shots/enemy_flight_1031/before/stage8-specs.json').read_text());meta=[];keys=set()
 for s in specs:
  if s['type']=='ll18raptor':continue
  q=p.evaluate('''s=>{EA11.case(s);if(!E)return null;const native=E._s8mega&&S8MEGA[E._s8mega],m=r46Model(E);return {type:E.type,name:E.name,hp:E.hp,art:E.art,native,model:m?.id,legacy:m?.legacyKeys,mm:E._mm1003,alien:E._alien1003,keys:Object.keys(E).filter(k=>/^_(s8|mm|r30|alien|orbit)/.test(k))};}''',s)
  if q:
   meta.append(q)
   if q.get('art'):keys.add(q['art'])
   if q.get('native'):keys.add('s8atk_'+q['native']['art']+'_0')
   keys.update(q.get('legacy')or[])
 keys.update(p.evaluate('Object.keys(XART._src).filter(k=>/bluehybrid|warp_sentinel|orbital_stalker|impharrow|hexpyre|armored_leech|hunter_pod|alien_hunter|furnacemaw/.test(k))'))
 p.evaluate('(ks)=>ks.forEach(k=>XART.rdy(k))',list(keys));p.wait_for_timeout(1500)
 exported=[]
 for k in keys:
  a=p.evaluate('''k=>{if(!XART.rdy(k))return null;const im=XART.get(k),c=document.createElement('canvas');c.width=im.naturalWidth||im.width;c.height=im.naturalHeight||im.height;c.getContext('2d').drawImage(im,0,0);return {data:c.toDataURL().split(',')[1],source:XART._src[k],w:c.width,h:c.height};}''',k)
  if a:
   (S/(k+'.png')).write_bytes(base64.b64decode(a.pop('data')));exported.append(dict(key=k,**a))
 (Q/'references.json').write_text(json.dumps(dict(actors=meta,images=exported),indent=2));b.close()
selected=[x for x in exported if any(t in x['key']for t in ['bluehybrid','warp','hunter','impharrow','hexpyre','armored_leech'])and not any(t in x['key']for t in ['attack','drift','roll','somer'])][:32]
out=Image.new('RGB',(1000,170*((len(selected)+4)//5)),(8,12,21));d=ImageDraw.Draw(out)
for i,v in enumerate(selected):
 im=Image.open(S/(v['key']+'.png')).convert('RGBA');im.thumbnail((190,140));x=i%5*200;y=i//5*170;out.paste(im,(x+(200-im.width)//2,y),im);d.text((x+2,y+142),v['key'][:29],fill='white')
out.save(Q/'reference-contact.jpg');print('Exported',len(exported),'native source images and',len(meta),'actor specifications')
