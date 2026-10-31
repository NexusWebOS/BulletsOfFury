from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import math,json,hashlib
import numpy as np
W=Path(__file__).resolve().parent
F=next(p for p in [W.parent/'BOF-Pixelmap-Fonts-1027/fonts',W.parent.parent/'assets/game/shared/ui/pixelmap_fonts_1027']if p.exists())
O=W/'compiled';O.mkdir(exist_ok=True)
masters_path=next(p for p in [W.parent/'BOF-Pixelmap-Fonts-1027/glyph-masters.json',W.parent.parent/'_ART_SOURCES/pixelmap_fonts_1027/glyph-masters.json']if p.exists())
masters=json.loads(masters_path.read_text())
sizes={'command':[6,7,8,9,10,11,12,14,18,21,24,28,35,42],'fury_strike':[8,10,12,14,16,18,20,22,24,26,28,32],'command_narrow':[8]};palettes=['chrome','ice','ember','gold','toxic','rose','signal','corrupt'];M={'palettes':palettes,'banks':{},'arrows':{}}
def even(n):return math.ceil(n/2)*2
def optical(family,h,code,palette,cw,ch,top):
 c=chr(code);heavy=family=='fury_strike';rows=(masters['heavy'].get(c,masters['small'][c])if heavy else masters['small'][c]).split('/');raw=Image.new('L',(len(rows[0]),len(rows)));d=ImageDraw.Draw(raw)
 for y,row in enumerate(rows):
  for x,v in enumerate(row):
   if v=='1':d.point((x,y),fill=255)
 cap=9 if heavy else 7;short=c.islower()and c not in 'bdfhijklt';desc=c in 'gpqy'
 baseline_rows=5 if short else 7
 target_h=max(1,round(len(rows)*h/cap));target_w=max(1,round(len(rows[0])*h/cap))if heavy else len(rows[0]);y0=top+h-round(baseline_rows*h/cap)
 if heavy and c in masters['heavy']:target_h=h;y0=top
 # Deliberate row selection preserves the bars/counters when a master must lose a row.
 if h==6 and not heavy and len(rows)==7:
  raw=Image.new('L',(5,6));d=ImageDraw.Draw(raw)
  for y,sy in enumerate([0,1,2,3,5,6]):
   for x,v in enumerate(rows[sy]):
    if v=='1':d.point((x,y),fill=255)
  target_h=6
 if heavy and h==8 and c in masters['heavy']:
  raw=Image.new('L',(7,8));d=ImageDraw.Draw(raw)
  for y,sy in enumerate([0,1,2,3,4,5,7,8]):
   for x,v in enumerate(rows[sy]):
    if v=='1':d.point((x,y),fill=255)
  target_h=8
 core=raw.resize((target_w,target_h),Image.Resampling.NEAREST);mask=Image.new('L',(cw,ch));mask.paste(core,(max(1,round(h/9))if heavy else 1,y0));im=Image.new('RGBA',(cw,ch));px=im.load();ramp=[tuple(bytes.fromhex(v))for v in masters['palettes'][palette]]
 if heavy:im.paste((7,11,24,255),(0,0),mask.filter(ImageFilter.MaxFilter(3)))
 for y in range(ch):
  for x in range(cw):
   if mask.getpixel((x,y)):px[x,y]=(*ramp[0 if y<top+h*.3 else 1 if not heavy or y<top+h*.7 else 2],255)
 return im
for family,heights in sizes.items():
 source='command'if family=='command_narrow'else family
 base=json.loads((F/(source+'_chrome.json')).read_text());sources=[Image.open(F/(source+'_'+p+'.png')).convert('RGBA')for p in palettes]
 for h in heights:
  k=h/base['capHeight'];kx=k*(.75 if family=='command_narrow'else 1);cw,ch=even(base['cw']*kx),even(base['ch']*k)
  if family=='fury_strike'and h<18:ch=max(ch,even(round((base['baseline']-base['capHeight'])*k)+h+math.ceil(2*h/9)+2))
  sw,sh=cw*16,ch*6;sheet=Image.new('RGBA',(sw*2,sh*8));glyphs={}
  for i,code in enumerate(range(32,127)):
   g=base['glyphs'][str(code)];glyphs[str(code)]={'x':i%16*cw,'y':i//16*ch,'advance':max(1,round(g['xadvance']*kx))}
  for p,src in enumerate(sources):
   plane=Image.new('RGBA',(sw,sh))
   for i,code in enumerate(range(32,127)):
    g=base['glyphs'][str(code)];q=src.crop((g['x'],g['y'],g['x']+g['w'],g['y']+g['h']));q=q.resize((round(q.width*kx),round(q.height*k)),Image.Resampling.NEAREST)
    if (family=='fury_strike'and h<18)or family=='command_narrow'or(family=='command'and h==6):q=optical(family,h,code,palettes[p],cw,ch,round((base['baseline']-base['capHeight'])*k))
    plane.alpha_composite(q,(i%16*cw,i//16*ch))
    if p==0:
     bounds=q.getbbox();glyphs[str(code)]['ink']=list(bounds)if bounds else [0,0,0,0]
     if bounds:glyphs[str(code)]['advance']=max(glyphs[str(code)]['advance'],bounds[2]-bounds[0]+1)
   dim=np.array(plane);dim[:,:,:3]=(dim[:,:,:3].astype(float)*.43).astype(np.uint8);sheet.alpha_composite(plane,(0,p*sh));sheet.alpha_composite(Image.fromarray(dim),(sw,p*sh))
  digit_advance=max(glyphs[str(c)]['advance']for c in range(48,58))
  for c in range(48,58):glyphs[str(c)]['advance']=digit_advance
  name=family+'_'+str(h);sheet.save(O/(name+'.png'),optimize=True);M['banks'][name]={'key':'pm27_'+name,'path':'assets/game/shared/ui/pixelmap_ui_1027/'+name+'.png','family':family,'height':h,'cw':cw,'ch':ch,'planeW':sw,'planeH':sh,'top':round((base['baseline']-base['capHeight'])*k),'baseline':round(base['baseline']*k),'glyphs':glyphs,'sha256':hashlib.sha256((O/(name+'.png')).read_bytes()).hexdigest()}
# Exact original selector pixels: one common scale, mirrored views, and baked
# white sweeps. The runtime chooses a cell; it adds no glow, tint or rotation.
for variant in ['b','r','g','y']:
 src=Image.open(W/'source'/('arrow-'+variant+'.png')).convert('RGBA');h=22;k=h/src.height;q=src.resize((round(src.width*k),h),Image.Resampling.NEAREST);cw,ch=even(q.width+4),26;frames=[]
 for mirror in [False,True]:
  for f in range(16):
   cell=Image.new('RGBA',(cw,ch));im=q.copy();a=np.array(im);t=f/16
   if t<.5:
    cut=round(im.height*(1-t*2));mask=np.indices(a.shape[:2])[0]>=cut;a[:,:,:3][mask]=(255,255,255)
   elif t<.75:
    cut=round(im.height*(t-.5)*4);mask=np.indices(a.shape[:2])[0]>=cut;a[:,:,:3][mask]=(255,255,255)
   im=Image.fromarray(a)
   if mirror:im=im.transpose(Image.Transpose.ROTATE_180)
   cell.alpha_composite(im,((cw-im.width)//2,2));frames.append(cell)
  # All frames retain the same even canvas and original orientation.
 sheet=Image.new('RGBA',(cw*8,ch*4))
 for i,im in enumerate(frames):sheet.alpha_composite(im,(i%8*cw,i//8*ch))
 name='arrow_'+variant;sheet.save(O/(name+'.png'));M['arrows'][variant]={'key':'pm27_'+name,'path':'assets/game/shared/ui/pixelmap_ui_1027/'+name+'.png','cw':cw,'ch':ch,'cols':8,'frames':32,'pivot':[cw//2,ch//2]}
(O/'manifest.json').write_text(json.dumps(M,indent=2));(W/'pixelmap_ui_art_1027.js').write_text('"use strict";\nconst PM27_ART='+json.dumps(M,separators=(',',':'))+';\n')
print('Built',len(M['banks']),'fixed-size font banks and four original selector banks.')
