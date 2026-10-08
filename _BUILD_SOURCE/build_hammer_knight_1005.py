from pathlib import Path
from PIL import Image
import json,shutil,sys
W=Path(__file__).resolve().parent
R=W.parent if W.name=='_BUILD_SOURCE' else Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
G=Path(r'C:/Users/Mike/.codex/generated_images/01a0c9fd-a6cc-73a3-8dca-3e0f7a90a956')
SRC=R/'_ART_SOURCES/hammer_knight_1005'; OUT=R/'assets/game/hammer_knight_1005'
SRC.mkdir(parents=True,exist_ok=True); OUT.mkdir(parents=True,exist_ok=True)
files={'hammer':sys.argv[1] if len(sys.argv)>1 else 'hammer.png', 'knight':'exec-dad26f3d-e6d4-4e1e-94c8-4ef904f5b87a.png','effects':'exec-90c12749-997b-4971-9e19-c9507ebd3adc.png'}
# Native grids are measured from the generated sheet; no repainting or stretching.
centers={'hammer':[(178,139),(584,169),(963,161),(1350,170),(178,417),(578,414),(971,418),(1359,418),(190,664),(578,649),(970,656),(1347,671),(191,911),(585,889),(973,903),(1340,914)],
 'knight':[(165,151),(452,176),(781,195),(1086,183),(164,472),(473,514),(804,501),(1096,500),(166,792),(486,748),(794,807),(1107,769)]}
centers['hammer'][15]=(1245,868)
manifest={'tool':'built-in image_gen','processing':'Measured native source rectangles, segmented extraction of two overlapping atlas gutters, and transparent padding. Native sprite colors preserved; no painted replacement.','cells':{}}
art={}
for name,filename in files.items():
 source=G/filename
 if source.exists():shutil.copy2(source,SRC/(name+'.png'))
 im=Image.open(SRC/(name+'.png')).convert('RGBA'); width,height=im.size
 cols=[0,394,721,1140,1536] if name=='hammer' else [round(i*width/4) for i in range(5)]
 rows=[0,292,520,770,1024] if name=='hammer' else [round(i*height/4) for i in range(5)]
 art[name]=[];manifest['cells'][name]=[]
 for i in range(16):
  c,r=i%4,i//4; rect=(cols[c],rows[r],cols[c+1],rows[r+1]); cell=im.crop(rect)
  if name=='hammer':
   rect=[(0,0,394,292),(394,0,721,292),(721,0,1140,292),(1140,0,1536,294),
     (0,292,394,535),(394,292,721,505),(721,292,1140,516),(1140,294,1536,535),
     (0,535,430,770),(450,492,721,744),(721,516,1140,768),(1140,535,1536,778),
     (0,770,394,1024),(394,728,721,1024),(721,768,1140,1024),(1140,778,1381,1024)][i]
   cell=im.crop(rect)
   # Segmented native atlas extraction: exclude neighboring feet intruding into
   # the gutters beside these two raised hammers. Original sprite pixels are kept.
   if i==9:
    cell.paste((0,0,0,0),(0,0,60,22));cell.paste((0,0,0,0),(175,0,cell.width,10))
   if i==13:cell.paste((0,0,0,0),(190,0,cell.width,43))
  padded=Image.new('RGBA',(cell.width+32,cell.height+32));padded.alpha_composite(cell,(16,16));padded.save(OUT/(name+'_'+str(i)+'.png'),optimize=True)
  if name in centers and i<len(centers[name]):
   x,y=centers[name][i];px=(x-rect[0]+16)/padded.width;py=(y-rect[1]+16)/padded.height
  else: px=py=.5
  a={'key':'hk5_'+name+'_'+str(i),'path':'assets/game/levels/stage_08/boss/hammer_knight_1005/'+name+'_'+str(i)+'.png','w':padded.width,'h':padded.height,'px':px,'py':py}
  if name=='hammer':
   heads=[(298,226),(559,37),(962,32),(1383,247),(289,484),(452,378),(789,404),(1470,376),(369,618),(578,530),(981,718),(1460,715),(312,947),(507,778),(823,883),(1469,885)]
   hx,hy=heads[i];a['head']=[hx-rect[0]+16,hy-rect[1]+16]
  if name=='effects':
   box=cell.getbbox();a['foot']=(box[3]+16)/padded.height;a['top']=(box[1]+16)/padded.height
  art[name].append(a);manifest['cells'][name].append({'frame':i,'sourceRect':rect,'alphaBounds':padded.getbbox(),'anchor':[px,py]})
 if name=='hammer':
  # The detached authored throw is its own live module. Do not bake it into the
  # empty-handed robot AND draw the older blue campaign hammer over it.
  rect=(1381,804,1536,958);cell=im.crop(rect);padded=Image.new('RGBA',(cell.width+32,cell.height+32));padded.alpha_composite(cell,(16,16));padded.save(OUT/'hammer_16.png',optimize=True)
  px=(1469-rect[0]+16)/padded.width;py=(885-rect[1]+16)/padded.height
  art[name].append({'key':'hk5_hammer_16','path':'assets/game/levels/stage_08/boss/hammer_knight_1005/hammer_16.png','w':padded.width,'h':padded.height,'px':px,'py':py})
  manifest['cells'][name].append({'frame':16,'sourceRect':rect,'alphaBounds':padded.getbbox(),'anchor':[px,py]})
(R/'assets/hammer_knight_art_1005.js').write_text('"use strict";\nconst HK5_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8')
(SRC/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
for name,directory in [('hammer_knight_1005.js','assets'),('test_hammer_knight_1005.cjs','_BUILD_SOURCE'),('probe_hammer_knight_1005.py','_BUILD_SOURCE')]:
 source=W/name;target=R/directory/name
 if source.exists() and source.resolve()!=target.resolve():shutil.copy2(source,target)
if Path(__file__).resolve()!=(R/'_BUILD_SOURCE/build_hammer_knight_1005.py').resolve():shutil.copy2(__file__,R/'_BUILD_SOURCE/build_hammer_knight_1005.py')
p=R/'assets/game.js'; s=p.read_bytes(); old=b'''    if(h.t<1.75){
      const half=h.spellHalf||0,want=clamp(player.x,camLeftX()+half+36,camRightX()-half-36);
      h.spellAnchor+=clamp(want-h.spellAnchor,-110*dt,110*dt);
      for(const q of h.spellTargets)q.x=h.spellAnchor+q.offset;
    }else for(const q of h.spellTargets)q.locked=true;'''
new=b'''    // Commit WORLD-space columns when the cast begins. Dodging never drags a warning.
    for(const q of h.spellTargets)q.locked=h.t>=.60;'''
if old in s: s=s.replace(old,new,1)
elif new not in s: raise AssertionError('Spell tracking block changed')
old=b";const ri=hammerFrame('reticle',0,k<.33?null:k<.66?'yellow':'red');for(let i=-2;i<=2;i++)hammerGroundReticleDraw(ri,b.x+i*w/5,hammerWarningFloorY(),Math.min(112,w/5),.55+.35*k);"
if old in s:s=s.replace(old,b'; /* Super blast uses the committed FOV lane only. */',1)
s=s.replace(b"else if(h.state==='mega_charge'){b.x+=clamp(homeX-b.x,-360*dt,360*dt);",b"else if(h.state==='mega_charge'){b.x=h.hkMegaX??b.x;",1)
s=s.replace(b"if(h.t>1.65){b.x=homeX;h.beamHit=false;",b"if(h.t>1.65){h.beamHit=false;",1)
s=s.replace(b'hammerChromiumDraw(q.x,PLAY.y+PLAY.h-12,PLAY.y,44,h.t,1.35)',b'hammerChromiumDraw(q.x,hammerWarningFloorY(),PLAY.y,44,h.t,1.35)',1)
p.write_bytes(s)
p=R/'index.html';s=p.read_bytes();needle=b'<script src="assets/dracodia_cinematic_1005.js"></script>'
add=b'\r\n<script src="assets/hammer_knight_art_1005.js"></script>\r\n<script src="assets/hammer_knight_1005.js"></script>'
if b'assets/hammer_knight_1005.js' not in s:s=s.replace(needle,needle+add,1);p.write_bytes(s)
p=R/'_BUILD_SOURCE/test_fl.js';s=p.read_bytes();needle=b"require('./test_dracodia_1005.cjs')(vm,ctxv,ok);"
add=b"\r\nrequire('./test_hammer_knight_1005.cjs')(vm,ctxv,ok);"
if b"require('./test_hammer_knight_1005.cjs')" not in s:s=s.replace(needle,needle+add,1);p.write_bytes(s)
for filename in ['probe_dracodia_1005.py','build_dracodia_review_1005.py']:
 p=R/'_BUILD_SOURCE'/filename
 if p.exists():p.write_bytes(p.read_bytes().replace(b'for(let i=1;i<8;i++)J.hp[i]=0',b'for(let i=1;i<J.hp.length;i++)J.hp[i]=0'))
p=R/'assets/password_catalog_1005.js';s=p.read_bytes();s=s.replace(b"'ACE','WARDEN'];",b"'ACE','WARDEN','CODE HAMMER'];",1);p.write_bytes(s)
if (W/'generation_manifest.json').exists():shutil.copy2(W/'generation_manifest.json',SRC/'generation_manifest.json')
print('Installed 49 native alpha cells, shared spell/FOV repairs and Hammer/knight combat layer')
