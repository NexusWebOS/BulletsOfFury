from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,sys,colorsys,re
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;C=W/'candidate';D=C/'frames';D.mkdir(parents=True,exist_ok=True)
O=W if W.parent.name=='_ART_SOURCES' else W.parents[1]/'outputs/dracodia-explosions';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(W/'support'));sys.path.insert(0,'C:/Users/Mike/.codex/skills/clean-pixel-effect-gifs/scripts');import pixelcore as px
before=(W/'before.js').read_bytes() if (W/'before.js').exists() else (R/'assets/dracodia_terminal_1030.js').read_bytes();(C/'before.js').write_bytes(before);code=before.decode()
old=json.JSONDecoder().raw_decode(code.split('const DF110_ART=',1)[1])[0];records={k:v for k,v in old.items() if k.startswith('body-') or k.startswith('piece-')}
families=[('boss-cascade','boss-cascade'),('dracodia-final','dracodia-final-purple'),('stage5-rupture','stage5-rupture')];effects=[]
def violet(c):
 r,g,b=map(int,c);h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
 if b>r+4 and b>=g and s>.04:
  # Replace blue/cyan palette ramps with violet; retain value, ink and neutral metal.
  h=.755+(h-.61)*.10;r,g,b=[round(n*255) for n in colorsys.hsv_to_rgb(h,s,v)]
 return [r,g,b]
contacts=Image.new('RGB',(960,320),'#10192b');draw=ImageDraw.Draw(contacts)
for row,(source,name) in enumerate(families):
 folder=W/'sources'/source
 if not folder.exists():folder=W.parents[1]/'outputs/boss-deaths'/source
 meta=json.loads((folder/f'{source}-sheet.json').read_text());basepal=np.array([list(bytes.fromhex(c[1:])) for c in meta['meta']['palette']],dtype=np.uint8);pal=np.array([violet(c) for c in basepal],dtype=np.uint8) if name.endswith('purple') else basepal
 mapping={tuple(map(int,c)):pal[i] for i,c in enumerate(basepal)};master=Image.open(folder/'generated-master.png').convert('RGB');count=len(meta['frames']);assert count==14
 for suffix,size,content,pad in [('',176,168,4),('-large',320,313,4),('-mega',480,464,8)]:
  strip=Image.new('RGBA',(size*14,size))
  for f in range(14):
   if size==176:
    v=np.array(Image.open(folder/'frames'/f'{source}-{f:02}.png').convert('RGBA'));original_alpha=v[:,:,3].copy()
    if name.endswith('purple'):
     for color,target in mapping.items():
      keep=(v[:,:,:3]==color).all(2)&(v[:,:,3]>0);v[keep,:3]=target
    v[v[:,:,3]==0]=0;cell=Image.fromarray(v);assert np.array_equal(v[:,:,3],original_alpha)
   else:
    x,y=round(f%4*master.width/4),round(f//4*master.height/4);q=np.array(master.crop((x,y,x+313,y+313)));alpha=px.key_mask(q,'magenta');q=px.despill(q,alpha,'magenta');rgb=px.map_to_palette(q,basepal)
    if name.endswith('purple'):
     for color,target in mapping.items():
      keep=(rgb==color).all(2);rgb[keep]=target
    v=np.dstack([rgb,alpha.astype('uint8')*255]);v[v[:,:,3]==0]=0;im=Image.fromarray(v)
    if content!=313:im=im.resize((content,content),Image.Resampling.NEAREST)
    cell=Image.new('RGBA',(size,size));cell.paste(im,(pad,pad))
   strip.paste(cell,(f*size,0))
   if size==320 and f==6:contacts.paste(cell,(row*320,0),cell);draw.text((row*320+5,5),name,fill='white')
  key=name+suffix;strip.save(D/(key+'.png'),optimize=True);records[key]={'path':f'assets/game/levels/stage_08/ending/dracodia_explosions_1110/{key}.png','cell':size}
 effects.append({'family':name,'source':source,'source_master_sha256':hashlib.sha256((folder/'generated-master.png').read_bytes()).hexdigest(),'frames':14,'cells':[176,320,480],'source_palette':['#%02x%02x%02x'%tuple(c) for c in basepal],'palette':['#%02x%02x%02x'%tuple(c) for c in pal],'alpha_preserved':True})
start=code.index('const DF110_ART=');end=code.index('const DF110=',start);code=code[:start]+'const DF110_ART='+json.dumps(records,separators=(',',':'))+';\n'+code[end:]
oldfamilies="families:['boss-heavy','dracodia-surge','stage5-core']";assert oldfamilies in code;code=code.replace(oldfamilies,"families:['boss-cascade','dracodia-final-purple','stage5-rupture']",1)
needle='Math.round(y-size/2),size,size);}'
assert needle in code
code=code.replace(needle,"Math.round(y-size/2),size,size);if(k.startsWith('dracodia-final-purple')){DF110.stats.purpleDraws=(DF110.stats.purpleDraws||0)+1;DF110.stats.purpleSizes||={};DF110.stats.purpleSizes[size]=(DF110.stats.purpleSizes[size]||0)+1;}}",1)
old="for(const f of Q.fx)rd84Bank(f.bank,f.t*24,f.anchor?x+f.dx:f.x,f.anchor?y+f.dy:f.y);"
new="for(const f of Q.fx){const n=f.bank==='electric_small'?0:f.bank==='electric_medium'?2:1,s=f.bank==='electric_small'?'':f.bank==='electric_medium'?'-large':'-mega';df110Blit(DF110.families[n]+s,Math.min(13,Math.floor(f.t/f.life*14)),f.anchor?x+f.dx:f.x,f.anchor?y+f.dy:f.y);}"
assert old in code;code=code.replace(old,new,1)
(C/'dracodia_terminal_1030.js').write_text(code,encoding='utf-8',newline='\n');contacts.save(W/'effect-contact.png');contacts.save(O/'effects.png')
manifest={'expected_source_hash':hashlib.sha256(before).hexdigest(),'effects':effects,'scope':'Only explosion artwork and selection; teleport, swelling, red core transition, timings, fragments, portal and victory retained','records':records,'purple_family':'dracodia-final-purple','early_terminal_bursts_also_replaced':True,'frames_per_family':14,'frame_seconds':.055,'concurrency_cap':24}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps({'families':[e['family'] for e in effects],'new_sheets':len(list(D.glob('*.png'))),'purple_palette_changes':sum(a!=b for a,b in zip(effects[1]['source_palette'],effects[1]['palette']))}))
