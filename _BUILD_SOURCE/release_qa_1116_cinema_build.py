from pathlib import Path
from PIL import Image
import json,hashlib,shutil,struct,zlib
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/release_qa_1116';A=R/'assets/game/shared/cinematics/release_qa_1116';S.mkdir(parents=True,exist_ok=True);A.mkdir(parents=True,exist_ok=True)
src=Path(r'C:\Users\Mdogg\.codex\generated_images\01a0d568-40a4-7b70-97c0-acc501f39d5b\exec-49f60247-d410-4e4b-96f2-c61a5575c57b.png')
if(S/'juggernaut-guitar-approved-cast.png').exists():src=S/'juggernaut-guitar-approved-cast.png'
if src.resolve()!=(S/'juggernaut-guitar-approved-cast.png').resolve():shutil.copyfile(src,S/'juggernaut-guitar-approved-cast.png')
ref=R/'_BUILD_SOURCE/front_pilots_1111/masters/juggernaut-master.png';shutil.copyfile(ref,S/'juggernaut-approved-reference.png')
im=Image.open(src).convert('RGBA');assert im.size==(1536,1024)
frames=[im.crop((i%3*512,i//3*512,i%3*512+512,i//3*512+512))for i in range(6)]
for i,f in enumerate(frames):f.save(S/f'juggernaut-guitar-{i:02d}.png')
out=A/'juggernaut-guitar.webp';im.save(out,lossless=True,exact=True);assert Image.open(out).convert('RGBA').tobytes()==im.tobytes()
TIMES=[220,180,250,260,320,700]
def string(s):
 b=s.encode('utf8');return struct.pack('<H',len(b))+b
def chunk(k,d):return struct.pack('<IH',6+len(d),k)+d
def layer(s,flags):return chunk(0x2004,struct.pack('<6HB3x',flags,0,0,0,0,0,255)+string(s))
def cel(idx,img=None,link=None):
 d=struct.pack('<HhhBHh5x',idx,0,0,255,1 if link is not None else 2,0)
 return chunk(0x2005,d+(struct.pack('<H',link)if link is not None else struct.pack('<HH',*img.size)+zlib.compress(img.tobytes(),9)))
aseframes=[];reference=Image.open(ref).convert('RGBA').resize((512,512),Image.Resampling.NEAREST)
for i,f in enumerate(frames):
 cs=([layer('Approved identity reference - hidden',68),layer('Generated complete cinematic pose',3)]if i==0 else[])+[cel(0,reference)if i==0 else cel(0,link=0),cel(1,f)]
 body=b''.join(cs);aseframes.append(struct.pack('<IHHH2xI',16+len(body),0xF1FA,len(cs),TIMES[i],0)+body)
head=bytearray(128);struct.pack_into('<I5HIHII',head,0,128+sum(map(len,aseframes)),0xA5E0,6,512,512,32,1,220,0,0);head[34:36]=bytes([1,1]);struct.pack_into('<HH',head,40,16,16)
(S/'juggernaut-guitar.aseprite').write_bytes(bytes(head)+b''.join(aseframes))
manifest={'key':'release16_juggernaut_guitar','path':out.relative_to(R).as_posix(),'w':512,'h':512,'cols':3,'frames':6,'pivot':[256,256],'durations':TIMES,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
comic=Image.new('RGBA',(1080,540))
for i,f in enumerate(frames):comic.paste(f.resize((270,270),Image.Resampling.NEAREST),(i%4*270,i//4*270))
cp=A/'juggernaut-guitar-comic.webp';comic.save(cp,lossless=True,exact=True)
cm={'key':'release16_comic_guitar','path':cp.relative_to(R).as_posix(),'w':270,'h':270,'cols':4,'frames':6,'pivot':[135,135],'source':manifest['path'],'sourceScale':270/512,'sha256':hashlib.sha256(cp.read_bytes()).hexdigest()}
(S/'juggernaut-guitar-comic.json').write_text(json.dumps(cm,indent=2),encoding='utf8')
(S/'juggernaut-guitar.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
(S/'art-brief.txt').write_text('Imagegen edit of the existing six-pose 1536x1024 guitar atlas using Mike-confirmed row-B Juggernaut identity. Preserve six512x512 poses, room, camera, guitar and native timing. Use orange sleeveless tactical vest, black undershirt/harness, silver buckles/dog tags, brown hair/beard, wraparound sunglasses and skull upper-arm tattoo. No dialogue/text/gutter. No runtime visual effects. Exact generated master and separate whole-frame PNGs retained; WebP is pixel-exact lossless. This is a six-pose identity correction, not a claim of16 newly authored poses.',encoding='utf8')
js='''"use strict";
/* Release QA1116: current approved guitar identity and readable ending holds.
   Reuses native text, portraits, typewriter, skip/input and continuation owners. */
const READ16={base:{rows:c16Rows,play:BOFCinematicDirector.play},adjusted:[],art:ART,comicArt:COMIC};
D1110_ART.banks['juggernaut-guitar']=READ16.art;
XART._src[READ16.art.key]=READ16.art.path+'?v='+READ16.art.sha256.slice(0,12);
C16_ART.banks['art-juggernaut-guitar']=READ16.comicArt;
XART._src[READ16.comicArt.key]=READ16.comicArt.path+'?v='+READ16.comicArt.sha256.slice(0,12);
function read16Rows(rows,ending=false){return rows.map(b=>{
 if(!b.d1110||!b.cm3||!b.text||(!ending&&!String(b.id).startsWith('ENDING-')))return b;
 const readAt=Number(b.cm3.readAt)||0,typed=String(b.text).length/30,words=(String(b.text).match(/\\S+/g)||[]).length,
  hold=Math.max(2.25,Math.min(5,words/6)),required=readAt+typed+hold+.18,duration=Math.max(Number(b.duration)||0,required);
 const q={...b,duration,cm3:{...b.cm3,baseDuration:duration-readAt-.14},read16:{typed,hold,readAt,minimum:required}};
 READ16.adjusted.push({id:b.id,before:b.duration,after:duration});if(READ16.adjusted.length>256)READ16.adjusted.shift();return q;
});}
c16Rows=function(){return read16Rows(READ16.base.rows.apply(this,arguments),arguments[0]==='ending');};
C16.rows=CM3.rows=FP5.rows=c16Rows;
BOFCinematicDirector.play=function(id,rows,done,live=false){return READ16.base.play.call(this,id,read16Rows(rows,id==='ending'),done,live);};
'''.replace('art:ART','art:'+json.dumps(manifest,separators=(',',':'))).replace('comicArt:COMIC','comicArt:'+json.dumps(cm,separators=(',',':')))
(R/'assets/release_cinema_1116.js').write_text(js,encoding='utf8',newline='\n');(S/'release_cinema_1116.js').write_text(js,encoding='utf8',newline='\n')
index=R/'index.html';s=index.read_text(encoding='utf8');backup=S/'index.html.before'
if not backup.exists():shutil.copyfile(index,backup)
s=s.replace('<script src="assets/online.js"></script>','<script src="assets/online.js?v=release-1116-1"></script>')
tag='<script src="assets/release_cinema_1116.js?v=3"></script>';s=s.replace('assets/release_cinema_1116.js?v=1','assets/release_cinema_1116.js?v=3').replace('assets/release_cinema_1116.js?v=2','assets/release_cinema_1116.js?v=3')
if tag not in s:s=s.replace('</body>',tag+'\n</body>')
index.write_text(s,encoding='utf8',newline='\n')
print('Built six exact512x512 approved-identity frames, layered source and ending read holds.')
