"""Retain Stage6 Royal/Blackice material palettes across the complete motion banks.
References are exported from the current native XART plates. No recoloring of
ordnance, neutral highlights, dark outlines, alpha or frame geometry.
Run after build_enemy_flight_1031.py.
"""
from pathlib import Path
import json,sys,base64,hashlib,copy
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF
O=R/'assets/game/shared/combat/enemy_flight_1031';S=R/'_BUILD_SOURCE/enemy_flight_1031/palette_sources';S.mkdir(exist_ok=True)
keys=['n6v'+str(i)+'_'+g for i in range(3)for g in['steel','royal','blackice']]
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page();p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(6,"hard")');print('Stage6 palette source warm',flush=True);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000)
  p.evaluate('()=>{for(const g of ["s","r","b"])for(let i=0;i<3;i++){const e=spawnEnemy("l6v_"+g+i,240,180);R46.base.draw(e);}}');print('Exporting native palette plates',flush=True)
  p.evaluate('(k)=>k.forEach(x=>XART.get(x+"_intact_c"))',keys);p.wait_for_function('(k)=>k.every(x=>{const im=XART.get(x+"_intact_c");return im&&(im.naturalWidth||im.width)>0})',arg=keys,timeout=30000)
  for key in keys:
   raw=p.evaluate('(k)=>{const im=XART.get(k+"_intact_c"),c=document.createElement("canvas");c.width=im.naturalWidth||im.width;c.height=im.naturalHeight||im.height;c.getContext("2d").drawImage(im,0,0);return c.toDataURL().split(",")[1]}',key);(S/(key+'.png')).write_bytes(base64.b64decode(raw))
  b.close()
finally:stop()
meta=json.loads((O/'manifest.json').read_text());audit=json.loads((R/'_shots/enemy_flight_1031/before/audit.json').read_text())
for i in range(3):
 for group,short in[('royal','r'),('blackice','b')]:
  ref=np.array(Image.open(S/(f'n6v{i}_{group}.png')).convert('RGBA'));base=np.array(Image.open(S/(f'n6v{i}_steel.png')).convert('RGBA'))
  lum=base[:,:,:3]@[.2126,.7152,.0722];rlum=ref[:,:,:3]@[.2126,.7152,.0722]
  material=ref[:,:,:3][(ref[:,:,3]>180)&(rlum>22)&(rlum<235)];material=material[np.argsort(material@[.2126,.7152,.0722])];source=lum[(base[:,:,3]>180)&(lum>22)&(lum<235)]
  knots=[22,42,65,90,120,150,180,210,235];palette=[]
  for l in knots:
   percentile=float((source<l).mean());lo=max(0,round((percentile-.045)*len(material)));hi=min(len(material),max(lo+1,round((percentile+.045)*len(material))))
   if hi>lo:
    # Median ratios keep authored metallic shading, including darker Blackice.
    ratio=np.median(material[lo:hi].astype(float),axis=0)/l;palette.append(ratio.tolist())
   else:palette.append(palette[-1]if palette else[1,1,1])
  model=copy.deepcopy(meta['models']['af_l6v_s'+str(i)]);im=np.array(Image.open(R/model['path']).convert('RGBA'));rgb=im[:,:,:3].astype(float);l=rgb@[.2126,.7152,.0722]
  # The actual ship material is low saturation; retain colored engine/weapon pixels.
  mask=(im[:,:,3]>0)&(l>23)&(l<224)&((rgb.max(2)-rgb.min(2))<58)
  mapped=np.stack([np.interp(l,knots,[c[ch]for c in palette])*l for ch in range(3)],axis=2)
  im[:,:,:3][mask]=np.clip(mapped[mask],0,255).astype('uint8')
  name=f'af_l6v_{short}{i}';path=O/(name+'.webp');Image.fromarray(im).save(path,format='WEBP',lossless=True,method=4)
  alias=f'l6v_{short}{i}';legacy={d['key']for q in audit['rows']if q['stage']==6 and q['spec']['type']==alias for d in q.get('stats',{}).get('draws',[])if d['key'].startswith(('af21_','bf22_','cp22_','sm10_','s6atk_','n6v','n6x','overhaul_stage'))}
  model.update(id=name,key='r46_'+name,path=path.relative_to(R).as_posix(),aliases=[alias],nativeRatios={alias:next(iter(model['nativeRatios'].values()),1)},legacyKeys=sorted(set(model['legacyKeys'])|legacy),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),paletteOwner=Path(__file__).relative_to(R).as_posix(),paletteReference=(S/f'n6v{i}_{group}.png').relative_to(R).as_posix(),paletteKnots=knots,paletteRatios=palette)
  meta['models'][name]=model;meta['aliases'][f'6|l6v_{short}{i}']=name
(O/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8');(R/'assets/enemy_flight_art_1031.js').write_text('"use strict";\nconst R46_ART='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print('Preserved all six authored Royal/Blackice material variants')
