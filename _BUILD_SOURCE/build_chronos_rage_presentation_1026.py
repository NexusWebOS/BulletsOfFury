"""Source-derived, fixed-cell Chronos rage rings, scenery veil and red HUD palette."""
from pathlib import Path
import json,subprocess,hashlib,re
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
if not (ROOT/'assets/game.js').exists():ROOT=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
OUT=ROOT/'assets/game/levels/stage_05/boss/chronos_rage_presentation_1026'
SRC=ROOT/'_ART_SOURCES/chronos_rage_presentation_1026'
PALETTE=np.array([[90,7,18],[216,24,8],[255,58,16],[255,106,24],[255,208,64],[255,246,176],[255,253,241]],dtype=np.uint8)

def main():
 OUT.mkdir(parents=True,exist_ok=True);SRC.mkdir(parents=True,exist_ok=True)
 node=r'C:/Program Files/nodejs/node.exe'
 js='const fs=require("fs"),vm=require("vm"),s={window:{}};vm.runInNewContext(fs.readFileSync("assets/manifest.js","utf8"),s);const a=s.window.BOFX;process.stdout.write(JSON.stringify(Array.from({length:8},(_,i)=>({key:"nsr_comet_"+i,path:a.img["nsr_comet_"+i],cell:a.cells["nsr_comet_"+i]}))));'
 refs=json.loads(subprocess.check_output([node,'-e',js],cwd=ROOT,text=True));frames=[]
 for ref in refs:
  _,x,y,w,h=ref['cell'];frames.append(Image.open(ROOT/ref['path']).convert('RGBA').crop((x,y,x+w,y+h)))
 banks={};sheets={}
 for name,r,cell in [('small',150,416),('large',230,624)]:
  sheet=Image.new('RGBA',(cell*4,cell*4));rows=[]
  for f in range(16):
   p=f/15;diameter=2*round((r*.30+(r*1.35-r*.30)*p));diameter=min(cell,diameter)
   base=frames[min(7,int(p*8))].resize((diameter,diameter),Image.Resampling.NEAREST)
   a=np.array(base);lum=a[:,:,:3].max(axis=2)/255
   idx=np.clip(np.floor(lum*6.999).astype(int),0,6)
   # Release starts white-hot/gold and settles to the same red/orange outer palette.
   idx=np.clip(idx-f//4+(1 if f<3 else 0),0,6);a[:,:,:3]=PALETTE[idx]
   a[:,:,3]=(np.round(a[:,:,3]/255*(1-p*p)*4)/4*255).astype(np.uint8)
   im=Image.fromarray(a);frame=Image.new('RGBA',(cell,cell));frame.alpha_composite(im,((cell-diameter)//2,(cell-diameter)//2))
   x=f%4*cell;y=f//4*cell;sheet.alpha_composite(frame,(x,y));rows.append({'key':f'cf50_ring_{name}_{f}','cell':[x,y,cell,cell],'pivot':[cell//2,cell//2]})
  path=OUT/(name+'_rings.png');sheet.save(path);key='cf50_ring_'+name
  sheets[key]={'path':str(path.relative_to(ROOT)).replace('\\','/'),'w':cell*4,'h':cell*4}
  banks[name]={'sheet':key,'frames':rows,'life':.42}
 # Authored alpha tiles: native-size blits cover arbitrary playfields without runtime fades.
 dim=Image.new('RGBA',(256,256))
 for i in range(16):dim.paste((0,0,0,round(i/15*.75*255)),(i%4*64,i//4*64,i%4*64+64,i//4*64+64))
 dim.save(OUT/'scenery_dim.png');sheets['cf50_scenery_dim']={'path':str((OUT/'scenery_dim.png').relative_to(ROOT)).replace('\\','/'),'w':256,'h':256}
 # Retain the complete approved HUD housing. Only the measured HP apertures change hue.
 gauge_src=ROOT/'assets/game/levels/stage_05/ui/enemy_bars_1007c.png';im=Image.open(gauge_src).convert('RGBA');before=np.array(im);after=before.copy()
 wells=[(177,385,1319,37),(172,553,1329,37)]
 for x,y,w,h in wells:
  a=after[y:y+h,x:x+w];v=a[:,:,:3].max(axis=2).astype(float);bright=v>28
  new=np.stack([np.minimum(255,v*1.12),v*.16,v*.12],axis=2)
  a[:,:,:3][bright]=new.astype(np.uint8)[bright]
 assert np.array_equal(before[:,:,3],after[:,:,3])
 mask=np.zeros(before.shape[:2],bool)
 for x,y,w,h in wells:mask[y:y+h,x:x+w]=True
 assert np.array_equal(before[~mask],after[~mask])
 Image.fromarray(after).save(OUT/'rage_health_bar.png');sheets['cf50_rage_health']={'path':str((OUT/'rage_health_bar.png').relative_to(ROOT)).replace('\\','/'),'w':im.width,'h':im.height}
 art={'sheets':sheets,'banks':banks,'dim':{'sheet':'cf50_scenery_dim','tile':64,'levels':16,'maximumAlpha':.75},'health':'cf50_rage_health'}
 (ROOT/'assets/chronos_rage_presentation_art_1026.js').write_text("'use strict';\nconst CF50_ART="+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8')
 audit={'sourceRings':refs,'sourceAtlasSha256':hashlib.sha256((ROOT/refs[0]['path']).read_bytes()).hexdigest(),'sourceGauge':str(gauge_src.relative_to(ROOT)).replace('\\','/'),'sourceGaugeSha256':hashlib.sha256(gauge_src.read_bytes()).hexdigest(),'palette':PALETTE.tolist(),'ringCount':32,'ringFrameCounts':[16,16],'evenFixedCells':[416,624],'nativeRingLife':.42,'hudAlphaPreserved':True,'hudPixelsOutsideHpWellsPreserved':True,'dim':'16 authored black-alpha64px tiles, no runtime opacity or filter','builder':'_BUILD_SOURCE/build_chronos_rage_presentation_1026.py','art':art}
 (SRC/'manifest.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
 # Small contact sheet for palette/pixel review; game uses the fixed-cell sheets above.
 review=Image.new('RGBA',(624,312),(18,25,38,255))
 for i,f in enumerate([0,3,6,9,12,15]):
  row=banks['large']['frames'][f];sheet=Image.open(OUT/'large_rings.png');x,y,w,h=row['cell'];tile=sheet.crop((x,y,x+w,y+h)).resize((208,208),Image.Resampling.NEAREST)
  review.alpha_composite(tile,(i%3*208,i//3*156))
 review.save(SRC/'ring_palette_review.png')
 print(json.dumps({'sheets':list(sheets),'frames':32,'gaugeAlphaPreserved':True,'evenCells':[416,624]}))
if __name__=='__main__':main()
