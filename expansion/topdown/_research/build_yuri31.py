"""Whole authored Yuri motion, fixed half-scale, measured roots and gun sockets."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[3];A=R/'expansion/topdown/art/yuri31';S=A/'source';F=A/'frames';F.mkdir(parents=True,exist_ok=True);assets={};seqs={}
# Hand-checked source muzzle endpoints; a separate effect follows these sockets.
twistTips={0:(50,40),4:(54,40),5:(72,45),6:(112,58),7:(145,122),8:(177,126),9:(184,101),10:(186,82),11:(159,63),12:(175,49),13:(186,46),14:(186,46),15:(186,46),16:(186,46),20:(186,46)}
def frame(source,i,key,side=None,kind='roll'):
 im=Image.open(S/source/f'{i:02}.png').convert('RGBA');assert im.size==(192,224);im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0));b=im.getbbox()
 root=[124,b[3]]if kind=='roll'else[110,160]if kind=='slide'else[96,210]
 ox,oy=96-round(root[0]/2),160-round(root[1]/2);out=Image.new('RGBA',(192,224));out.alpha_composite(im.resize((96,112),Image.Resampling.NEAREST),(ox,oy));tip=None
 if kind=='slide':tip=twistTips[i]
 if kind=='down':
  points=[(x,y)for y in range(150,197)for x in range(91,101)if im.getpixel((x,y))[3]>127]
  y=max(p[1]for p in points);xs=[p[0]for p in points if p[1]==y];tip=(round(sum(xs)/len(xs)),y)
 muzzle=[ox+round(tip[0]/2),oy+round(tip[1]/2)]if tip else None
 if side=='east':out=out.transpose(Image.Transpose.FLIP_LEFT_RIGHT);muzzle=[191-muzzle[0],muzzle[1]]if muzzle else None
 path=F/(key+'.png');out.save(path);bounds=out.getbbox();assert bounds and min(bounds[:2])>0 and bounds[2]<192 and bounds[3]<224
 m={'file':path.relative_to(R).as_posix(),'size':[192,224],'anchor':[96,160],'bounds':list(bounds),'drawScale':1,'source':source,'sourceFrame':i,'sourceRoot':root,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 if muzzle:m['muzzle']=muzzle
 assets[key]=m;return key
for side in ['west','east']:
 keys=[frame('roll_complete',i,f'y31_roll_{side}_{n}',side)for n,i in enumerate(list(range(23))+[24])]
 seqs['y31_roll_'+side]={'frames':keys,'fps':48,'duration':.5,'loop':False,'phases':{'push':0,'inverted':7,'rotation_through':11,'boots_plant':16,'recover':23}}
 keys=[frame('roll_complete',i,f'y31_roll_prone_{side}_{i}',side)for i in range(17)]
 keys += [frame('prone_settle',i,f'y31_roll_prone_{side}_{12+i}',side)for i in range(5,17)]
 seqs['y31_roll_prone_'+side]={'frames':keys,'fps':58,'duration':.5,'loop':False,'landingSource':'approved Yuri30 kneel-to-prone drawings; generated airborne finish rejected'}
 selected=[0]+list(range(4,17))+[20]
 keys=[frame('slide_twist',i,f'y31_slide_turn_{side}_{n}',side,'slide')for n,i in enumerate(selected)]
 seqs['y31_slide_turn_'+side]={'frames':keys,'fps':44,'duration':.34,'loop':False,'reversible':True,'selection':selected,'rejectedFrames':{'1,2,3':'unwanted baked flash/sparks'}}
frame('down_setup',0,'y31_down_idle',kind='down')
keys=[frame('down_brace',i,f'y31_down_fire_{i-1}',kind='down')for i in range(1,9)]
seqs['y31_down_fire']={'frames':keys,'fps':64,'duration':.12,'loop':True}
pack={'build':'overdrive1015-yuri31-r1','assets':assets,'sequences':seqs,'unit':{'cell':[192,224],'anchor':[96,160],'bodyScale':.5},'notes':'Whole authored plates; same scale throughout. Roots, pose selection, and native barrel sockets are explicit. No skeletal puppetry.'}
(A/'manifest.json').write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8',newline='\n')
(A/'manifest.js').write_text('window.TD_YURI31_ART='+json.dumps(pack,separators=(',',':'))+';\nObject.assign(window.TD_ESCAPE29_ART.assets,window.TD_YURI31_ART.assets);\nObject.assign(window.TD_ESCAPE29_ART.sequences,window.TD_YURI31_ART.sequences);\n',encoding='utf-8',newline='\n')
Q=R/'_shots/yuri31';Q.mkdir(parents=True,exist_ok=True)
for bank,q in seqs.items():
 keys=q['frames'];out=Image.new('RGB',(192*5,240*((len(keys)+4)//5)),'#21313b');d=ImageDraw.Draw(out)
 for j,k in enumerate(keys):
  im=Image.open(R/assets[k]['file']);x=j%5*192;y=j//5*240;out.paste(im,(x,y),im);d.line((x,y+160,x+190,y+160),fill='#47604d');d.text((x+3,y+224),k,fill='white')
 out.save(Q/(bank+'.png'))
print(json.dumps({'exports':len(assets),'banks':len(seqs)}))
