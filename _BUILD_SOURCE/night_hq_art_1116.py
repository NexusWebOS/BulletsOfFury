from pathlib import Path
from PIL import Image
import json,hashlib,shutil,struct,zlib
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/cinema_overnight_1116';A=R/'assets/game/shared/cinematics/cinema_overnight_1116';S.mkdir(parents=True,exist_ok=True);A.mkdir(parents=True,exist_ok=True)
src=S/'hq-conference-approved.png'
if not src.exists():shutil.copyfile(Path(r'C:\Users\Mdogg\.codex\generated_images\01a0d568-40a4-7b70-97c0-acc501f39d5b\exec-da76719a-ca4e-4be6-907a-60e431d099ab.png'),src)
generated=Image.open(src).convert('RGBA');assert generated.size in[(1776,888),(1774,887)],generated.size
# The returned atlas is two pixels narrower and one pixel shorter than requested.
# Preserve its actual artwork; transparently pad each whole cell to888x444.
# Never stretch it to force the expected dimensions.
cutx=[0,round(generated.width/2),generated.width];cuty=[0,round(generated.height/2),generated.height];frames=[];sourceRects=[]
for i in range(4):
 rect=(cutx[i%2],cuty[i//2],cutx[i%2+1],cuty[i//2+1]);cell=generated.crop(rect);im=Image.new('RGBA',(888,444));im.alpha_composite(cell);frames.append(im);sourceRects.append(rect)
master=Image.new('RGBA',(1776,888))
for i,im in enumerate(frames):master.paste(im,(i%2*888,i//2*444))
for i,im in enumerate(frames):im.save(S/f'hq-conference-{i:02}.png')
sheet=A/'hq-conference.webp';master.save(sheet,lossless=True,exact=True);assert Image.open(sheet).convert('RGBA').tobytes()==master.tobytes()
comic=Image.new('RGBA',(3016,270));cropH=round(888*270/754);top=max(0,min(444-cropH,round(444*.20)))
for i,im in enumerate(frames):comic.paste(im.crop((0,top,888,top+cropH)).resize((754,270),Image.Resampling.NEAREST),(i*754,0))
cp=A/'hq-conference-comic.webp';comic.save(cp,lossless=True,exact=True);assert Image.open(cp).convert('RGBA').tobytes()==comic.tobytes()
def meta(key,path,w,h,cols):return{'key':key,'path':path.relative_to(R).as_posix(),'w':w,'h':h,'cols':cols,'frames':4,'pivot':[w//2,h//2],'durations':[900,900,1100,2000],'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
full=meta('nq16_hq_conference',sheet,888,444,2);small=meta('nq16_hq_conference_comic',cp,754,270,4);small.update({'source':full['path'],'sharedCrop':[0,top,888,cropH],'directFromMaster':True})
def string(s):
 b=s.encode('utf8');return struct.pack('<H',len(b))+b
def chunk(k,d):return struct.pack('<IH',6+len(d),k)+d
def layer(s,flags):return chunk(0x2004,struct.pack('<6HB3x',flags,0,0,0,0,0,255)+string(s))
def cel(idx,img=None,link=None):
 d=struct.pack('<HhhBHh5x',idx,0,0,255,1 if link is not None else 2,0)
 return chunk(0x2005,d+(struct.pack('<H',link)if link is not None else struct.pack('<HH',*img.size)+zlib.compress(img.tobytes(),9)))
refpath=R/'_BUILD_SOURCE/front_pilots_1111/masters/juggernaut-master.png';ref=Image.open(refpath).convert('RGBA');ref.thumbnail((888,444),Image.Resampling.NEAREST);identity=Image.new('RGBA',(888,444));identity.alpha_composite(ref,((888-ref.width)//2,(444-ref.height)//2));chunks=[]
for i,im in enumerate(frames):
 cs=([layer('Approved row-B Juggernaut identity - hidden',68),layer('Whole conference pose - generated edit',3)]if i==0 else[])+[cel(0,identity)if i==0 else cel(0,link=0),cel(1,im)]
 body=b''.join(cs);chunks.append(struct.pack('<IHHH2xI',16+len(body),0xF1FA,len(cs),full['durations'][i],0)+body)
head=bytearray(128);struct.pack_into('<I5HIHII',head,0,128+sum(map(len,chunks)),0xA5E0,4,888,444,32,1,900,0,0);head[34:36]=bytes([1,1]);struct.pack_into('<HH',head,40,16,16);(S/'hq-conference.aseprite').write_bytes(bytes(head)+b''.join(chunks))
manifest={'full':full,'comic':small,'source':src.relative_to(R).as_posix(),'generatedSize':generated.size,'sourceRects':sourceRects,'normalization':'Transparent right/bottom padding only; no artwork resampling in the master.','reference':refpath.relative_to(R).as_posix(),'scope':'Four retained conference poses; approved orange-vest Juggernaut identity correction. Not sixteen new animation poses.'};(S/'hq-conference.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
js='''"use strict";
/* Current approved costume in every whole HQ conference pose. */
const CQA16_HQ=MANIFEST;
D1110_ART.banks['hq-conference']=HQ1110_ART.banks['hq-conference']=CQA16_HQ.full;
C16_ART.banks['art-hq-conference']=CQA16_HQ.comic;
for(const a of [CQA16_HQ.full,CQA16_HQ.comic])XART._src[a.key]=a.path+'?v='+a.sha256.slice(0,12);
'''.replace('MANIFEST',json.dumps(manifest,separators=(',',':')))
(R/'assets/night_hq_art_1116.js').write_text(js,encoding='utf8',newline='\n')
p=R/'index.html';s=p.read_text(encoding='utf8');tag='<script src="assets/night_hq_art_1116.js?v=1"></script>'
if tag not in s:s=s.replace('</body>',tag+'\n</body>');p.write_text(s,encoding='utf8',newline='\n')
prompt=Path(__file__).with_name('night_hq_prompt_1116.txt')
if prompt.exists():shutil.copyfile(prompt,S/'hq-conference-prompt.txt')
print(json.dumps({'master':master.size,'poses':4,'comic':comic.size,'crop':[0,top,888,cropH],'even':all(v%2==0 for v in[888,444,754,270])}))
