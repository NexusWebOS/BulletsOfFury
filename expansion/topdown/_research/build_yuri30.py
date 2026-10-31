"""Identity-only replacements for Escape29, retaining action keys, units and sockets."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,copy
R=Path(__file__).resolve().parents[3];A=R/'expansion/topdown/art/yuri30';S=A/'source';F=A/'frames';F.mkdir(parents=True,exist_ok=True)
old=json.loads((R/'expansion/topdown/art/escape29/manifest.json').read_text());assets={};audit=[]
for k,m in old['assets'].items():
 if not any(k.startswith('e29_'+s)for s in ['aim_','run_','vault_','roll_','crouch_','prone_','cover_peek_','slide_']):continue
 name=m['source'];i=m.get('sourceFrame',0);src=S/name/f'{i:02}.png';im=Image.open(src).convert('RGBA');assert im.size==(192,224),(src,im.size)
 im.putalpha(im.getchannel('A').point(lambda v:255 if v>=128 else 0))
 root=m.get('sourceRoot',[110,160]if name.startswith('slide')and name!='slide_flat'else[124,206])
 if name=='slide_flat':root=[124,Image.open(R/'expansion/topdown/art/escape29/source/escape29/slide_flat/00.png').getbbox()[3]]
 # Same whole-body proportional scale as the previous owner; preserve poses.
 im=im.resize((96,112),Image.Resampling.NEAREST);out=Image.new('RGBA',(192,224));out.alpha_composite(im,(96-round(root[0]*.5),160-round(root[1]*.5)))
 if '_east'in k or k in ['e29_slide_up','e29_slide_back','e29_slide_down']:out=out.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 bounds=out.getbbox();assert bounds and bounds[0]>0 and bounds[1]>0 and bounds[2]<192 and bounds[3]<224
 path=F/(k+'.png');out.save(path);meta=copy.deepcopy(m);meta.update(file=path.relative_to(R).as_posix(),bounds=list(bounds),identitySource='approved Yuri28 west_setup / original Yuri motion',correctionSource=src.relative_to(R).as_posix());assets[k]=meta;audit.append({'key':k,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bounds':list(bounds),'oldFile':m['file']})
assert len(assets)==213,len(assets)
pack={'build':'overdrive1015-yuri30-r1','assets':assets,'sequences':old['sequences'],'unit':old['unit'],'audit':audit,'reference':'expansion/topdown/art/yuri28/source/west_setup.png','scope':'Only new Escape29 Yuri identity; existing motions, gameplay and other art preserved.'}
(A/'manifest.json').write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8',newline='\n')
(A/'manifest.js').write_text('window.TD_YURI30_ART='+json.dumps(pack,separators=(',',':'))+';\nObject.assign(window.TD_ESCAPE29_ART.assets,window.TD_YURI30_ART.assets);\n',encoding='utf-8',newline='\n')
Q=R/'_shots/yuri30';Q.mkdir(parents=True,exist_ok=True)
for bank,q in old['sequences'].items():
 keys=[k for k in q['frames']if k in assets]
 if not keys:continue
 sheet=Image.new('RGB',(192*4,240*((len(keys)+3)//4)),'#24343e');d=ImageDraw.Draw(sheet)
 for i,k in enumerate(keys):
  im=Image.open(R/assets[k]['file']);x=i%4*192;y=i//4*240;sheet.paste(im,(x,y),im);d.line((x,y+160,x+190,y+160),fill='#46634e');d.text((x+3,y+225),k,fill='white')
 sheet.save(Q/(bank+'.png'))
print(json.dumps({'exports':len(assets),'sourceDrawings':len(set(a['correctionSource']for a in assets.values())),'unchangedGameplay':True}))
