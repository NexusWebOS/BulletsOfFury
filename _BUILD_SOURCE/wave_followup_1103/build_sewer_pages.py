"""Lossless page packing of existing Stage7 cells; original banks are retained."""
from pathlib import Path
import json, hashlib, math
import numpy as np
from PIL import Image

W=Path(__file__).parent
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
OUT=W/'pages'
OUT.mkdir(exist_ok=True)
def read(name):
    text=(R/'assets'/name).read_text(encoding='utf8')
    return json.loads(text[text.index('{'):text.rindex('}')+1])
sewer=read('stage7_amplify_art_1101.js')
flight=read('enemy_flight_art_1031.js')
ordnance=read('enemy_ordnance_art_1031.js')
feedback=read('enemy_feedback_art_1031.js')
banks={b['key']:b for b in sewer['banks'].values()}
for b in flight['models'].values():
    if 7 in b.get('stages',[]):banks[b['key']]=b
for signature,b in ordnance['glyphs'].items():
    if json.loads(signature)[0]==7:banks[b['key']]=b
for b in feedback['banks'].values():banks[b['key']]=b
result={'version':1,'maxPage':1536,'banks':{},'pages':{},'sourceBytes':0,'pageBytes':0,'cells':0,'uniqueCells':0,'pixelChecks':0}
for key,b in banks.items():
    im=Image.open(R/b['path']).convert('RGBA');c=b['cell']
    assert im.width%c==0 and im.height%c==0 and c%2==0,(key,im.size,c)
    cols,rows=im.width//c,im.height//c
    cells=[];unique=[];seen={}
    for row in range(rows):
        for col in range(cols):
            cell=im.crop((col*c,row*c,(col+1)*c,(row+1)*c));box=cell.getbbox()
            if not box:cells.append(None);continue
            box=(box[0]//2*2,box[1]//2*2,min(c,(box[2]+1)//2*2),min(c,(box[3]+1)//2*2))
            crop=cell.crop(box);signature=(box,hashlib.sha256(crop.tobytes()).hexdigest())
            if signature not in seen:
                seen[signature]=len(unique);unique.append({'image':crop,'offset':box[:2]})
            cells.append(seen[signature])
    pages=[];x=y=2;rowH=0;page=Image.new('RGBA',(1536,1536));usedW=usedH=2
    def save_page():
        pkey='s7p113_'+key+'_'+str(len(pages));filename=pkey+'.png';image=page.crop((0,0,(usedW+1)//2*2,(usedH+1)//2*2))
        image.save(OUT/filename,optimize=True)
        result['pages'][pkey]={'path':'assets/game/shared/combat/sewer_pages_1103/'+filename,'w':image.width,'h':image.height,'sha256':hashlib.sha256((OUT/filename).read_bytes()).hexdigest()}
        result['pageBytes']+=image.width*image.height*4;pages.append(pkey)
    for i in sorted(range(len(unique)),key=lambda i:(-unique[i]['image'].height,-unique[i]['image'].width)):
        u=unique[i];crop=u['image'];cw,ch=crop.size
        if x+cw+2>1536:x=2;y+=rowH+2;rowH=0
        if y+ch+2>1536:
            save_page();page=Image.new('RGBA',(1536,1536));x=y=2;rowH=0;usedW=usedH=2
        page.paste(crop,(x,y));u['rect']=[len(pages),x,y,cw,ch,*u['offset']]
        x+=cw+2;rowH=max(rowH,ch);usedW=max(usedW,x);usedH=max(usedH,y+ch+2)
    if unique:save_page()
    records=[None if i is None else unique[i]['rect']for i in cells]
    decoded=[Image.open(OUT/(p+'.png')).convert('RGBA')for p in pages]
    for index,rect in enumerate(records):
        restored=Image.new('RGBA',(c,c))
        if rect:
            n,sx,sy,cw,ch,ox,oy=rect;restored.paste(decoded[n].crop((sx,sy,sx+cw,sy+ch)),(ox,oy))
        original=im.crop((index%cols*c,index//cols*c,(index%cols+1)*c,(index//cols+1)*c))
        a=np.asarray(original);z=np.asarray(restored);visible=a[:,:,3]>0
        assert np.array_equal(a[:,:,3],z[:,:,3]) and np.array_equal(a[:,:,:3][visible],z[:,:,:3][visible]),(key,index)
        result['pixelChecks']+=1
    result['banks'][key]={'cell':c,'cols':cols,'rows':rows,'pages':pages,'cells':records,'source':b['path'],'sourceSHA':hashlib.sha256((R/b['path']).read_bytes()).hexdigest()}
    result['sourceBytes']+=im.width*im.height*4;result['cells']+=len(cells);result['uniqueCells']+=len(unique)
    print('PACKED',key,len(cells),'cells',len(pages),'pages',flush=True)
(W/'sewer_pages_1103.json').write_text(json.dumps(result,separators=(',',':'))+'\n',encoding='utf8')
(W/'sewer_pages_art_1103.js').write_text('"use strict";\nconst S7P113_ART='+json.dumps(result,separators=(',',':'))+';\n',encoding='utf8')
print(json.dumps({k:v for k,v in result.items()if k not in ['banks','pages']},indent=2),flush=True)
