"""Export whole Yuri poses at the established body unit; never fit frames."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[3];A=R/'expansion/topdown/art/yuri32';S=A/'source';F=A/'frames';F.mkdir(parents=True,exist_ok=True);assets={};seqs={}

def emit(source,i,key,side=None,rootx=160,tipmode='side'):
 im=Image.open(S/source/f'{i:02}.png').convert('RGBA');assert im.size==(256,256)
 im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0));b=im.getbbox()
 # Grounded poses register their observed sole/contact line. The authored
 # flight phases retain the floor origin so airborne feet remain airborne.
 airborne=source=='run_slide'and i in [2,3,6,7,10,11]
 root=[rootx,234 if airborne else b[3]]
 # Source sockets are selected from the reviewed barrel edge, not a fixed
 # character-center offset. Raised rifles use the top, level rifles the left.
 if tipmode=='top':
  y=b[1];xs=[x for x in range(256)if im.getpixel((x,y))[3]];tip=[round(sum(xs)/len(xs)),y]
 else:
  cutoff=b[1]+max(30,round((b[3]-b[1])*.55));points=[(x,y)for y in range(b[1],cutoff)for x in range(b[0],b[2])if im.getpixel((x,y))[3]]
  x=min(p[0]for p in points);ys=[p[1]for p in points if p[0]==x];tip=[x,round(sum(ys)/len(ys))]
 ox,oy=96-round(root[0]/2),160-round(root[1]/2);out=Image.new('RGBA',(192,224));out.alpha_composite(im.resize((128,128),Image.Resampling.NEAREST),(ox,oy));muzzle=[ox+round(tip[0]/2),oy+round(tip[1]/2)]
 if side=='east':out=out.transpose(Image.Transpose.FLIP_LEFT_RIGHT);muzzle[0]=191-muzzle[0]
 b=out.getbbox();assert b and min(b[:2])>0 and b[2]<192 and b[3]<224,(key,b)
 p=F/(key+'.png');out.save(p);assets[key]={'file':p.relative_to(R).as_posix(),'size':[192,224],'anchor':[96,160],'drawScale':1,'bounds':list(b),'muzzle':muzzle,'source':source,'sourceFrame':i,'sourceRoot':root,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};return key

def bank(name,source,indices,rootxs=160,mode='side',fps=30):
 for side in ['west','east']:
  keys=[emit(source,i,f'y32_{name}_{side}_{n}',side,rootxs[i]if isinstance(rootxs,dict)else rootxs,mode(i)if callable(mode)else mode)for n,i in enumerate(indices)]
  seqs[f'y32_{name}_{side}']={'frames':keys,'fps':fps,'loop':False,'selection':indices,'source':source}

emit('up_setup',0,'y32_up_idle',rootx=128,tipmode='top')
seqs['y32_up_fire']={'frames':[emit('up_fire',i,f'y32_up_fire_{i-1}',rootx=128,tipmode='top')for i in range(1,9)],'fps':64,'loop':True}
bank('slide_hold','slide_hold',[0],160)
# Only contaminated frames are omitted; source motion and original body unit
# stay intact. Contact phases and original drawings remain in the manifest.
walk=list(range(11))+[12,13]+list(range(15,21))
walkroots={i:x for i,x in enumerate([128,120,112,107,87,92,105,111,121,139,158,160,160,160,160,160,160,160,160,160,160])}
run=[i for i in range(25)if i not in [15,17]]
runroots={i:x for i,x in enumerate([128,128,128,128,128,128,128,128,128,128,135,145,150,158,160,160,160,160,160,160,160,160,160,160,160])}
bank('walk_slide','walk_polished',walk,walkroots,fps=40)
bank('run_slide','run_slide',run,runroots,fps=46)
exitframes=[0,3,4,5,6,7,8,9,14,15,16]
bank('slide_exit','slide_exit',exitframes,{i:160 if i==0 else 128 for i in exitframes},fps=40)
bank('cover_peek','cover_peek_clean',[0]+list(range(3,21)),160,lambda i:'top'if i<=6 else'side',40)
bank('cover_crouch','cover_crouch',list(range(13)),160,'top',30)
bank('crouch_peek','crouch_peek',list(range(17)),160,lambda i:'top'if i<=3 else'side',36)
for side in ['west','east']:
 for name in ['cover','crouch']:
  q=seqs[f'y32_{name}_peek_{side}'];seqs[f'y32_{name}_return_{side}']={**q,'frames':list(reversed(q['frames'])),'reverseOf':f'y32_{name}_peek_{side}'}
 seqs[f'y32_cover_enter_{side}']={**seqs[f'y32_cover_return_{side}'],'use':'Tuck rifle and pivot back into protected stance.'}
pack={'build':'overdrive1015-yuri32-r1','assets':assets,'sequences':seqs,'unit':{'cell':[192,224],'anchor':[96,160],'bodyScale':.5},'notes':'Only whole authored Yuri and rifle pixels. Original character unit retained. Return banks reverse the controlled lean; no environmental objects.'}
(A/'manifest.json').write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8')
(A/'manifest.js').write_text('window.TD_YURI32_ART='+json.dumps(pack,separators=(',',':'))+';\nObject.assign(window.TD_ESCAPE29_ART.assets,window.TD_YURI32_ART.assets);\nObject.assign(window.TD_ESCAPE29_ART.sequences,window.TD_YURI32_ART.sequences);\n',encoding='utf-8')
Q=R/'_shots/yuri32';Q.mkdir(parents=True,exist_ok=True)
for name,q in seqs.items():
 if name.endswith('west')or'return'in name or'enter'in name:continue
 out=Image.new('RGB',(192*5,240*((len(q['frames'])+4)//5)),'#21313b');d=ImageDraw.Draw(out)
 for n,k in enumerate(q['frames']):
  im=Image.open(R/assets[k]['file']);x=n%5*192;y=n//5*240;out.paste(im,(x,y),im);d.line((x,y+160,x+190,y+160),fill='#47604d');d.text((x+3,y+224),k,fill='white')
 out.save(Q/(name+'.png'))
print(json.dumps({'frames':len(assets),'banks':len(seqs)}))
