"""Palette variants of the exact gold Retina sonic-pulse reel Mike identified."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];D=R/'assets/game/shared/combat/razorback_pulse_1021';O=R/'_shots/razorback_arc_1021';S=R/'_ART_SOURCES/razorback_pulse_1021'
for p in [D,O,S]:p.mkdir(exist_ok=True,parents=True)
text=(R/'assets/playthrough_art_1011.js').read_text();art=json.JSONDecoder().raw_decode(text.split('const PT11_ART=',1)[1])[0]['sonic_pulse']
banks={};audit=[];luma=np.array([.2126,.7152,.0722])
for color,ramp in [('red',[1,.035,.12]),('green',[.22,1,.12])]:
 ramp=np.array(ramp);threshold=ramp@luma*255;sheet=Image.new('RGBA',(1024,256));contact=Image.new('RGBA',(1024,292),(15,20,27,255));pen=ImageDraw.Draw(contact);cells=[]
 for i,a in enumerate(art):
  original=Image.open(R/a['path']).convert('RGBA');src=np.array(original);assert original.size==(128,128)
  rgb=src[:,:,:3].astype(float);L=rgb@luma;out=src.copy();lo=L<=threshold
  mapped=np.where(lo[:,:,None],L[:,:,None]/threshold*ramp*255,255*(ramp+(1-ramp)*(L[:,:,None]-threshold)/(255-threshold)))
  chromatic=rgb.max(2)-rgb.min(2)>12;out[chromatic,:3]=np.clip(mapped[chromatic],0,255).round().astype('uint8')
  assert np.array_equal(out[:,:,3],src[:,:,3]);assert abs((out[:,:,:3]@luma-L)[src[:,:,3]>30]).max()<1
  im=Image.fromarray(out);x=i%8*128;y=i//8*128;sheet.paste(im,(x,y));cells.append([x,y,128,128]);contact.alpha_composite(im,(x,i//8*146));pen.text((x+3,i//8*146+128),str(i),fill='white')
 path=D/(color+'.webp');sheet.save(path,lossless=True,exact=True,method=6);contact.convert('RGB').save(O/(color+'-pulse-contact.jpg'),quality=95)
 banks['pulse_'+color]=dict(key='rp21_pulse_'+color,path=path.relative_to(R).as_posix(),sourceKey='pt11_sonic_pulse_0',w=128,h=128,pivot=[64,64],frames=16,fps=16,cells=cells)
 audit.append(dict(color=color,source=[a['path'] for a in art],frames=16,canvas=[128,128],pivot=[64,64],sourceScale=1,alphaExact=True,luminanceErrorMax=1,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
(R/'assets/razorback_pulse_art_1021.js').write_text("'use strict';\nObject.assign(SX21_ART.banks,"+json.dumps(banks,separators=(',',':'))+');\n',newline='\n')
(S/'export-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
tax=R/'assets/data/ART_TAXONOMY.json';text=tax.read_text()
if 'rp21_' not in json.loads(text):
 entry={'rp21_':dict(role='razorback_targeted_sonic_pulse',sheet=None,owner='_BUILD_SOURCE/build_razorback_pulse_1021.py',note='Exact16 original pt11_sonic_pulse gold arcs, recolored red/green with original alpha and luminance preserved. Fixed128x128/pivot64,64,scale1. Enemy Retina pulse only; player Forge gold art unchanged.')}
 tax.write_text('{\n'+json.dumps(entry,indent=2)[2:-2]+',\n'+text[2:],newline='\n')
print(json.dumps(dict(banks=2,frames=32,bytes=sum(p.stat().st_size for p in D.glob('*.webp')))))
