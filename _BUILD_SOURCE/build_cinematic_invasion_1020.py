"""Build PixelLab cinematic exports; never repack the existing game atlas."""
from pathlib import Path
from PIL import Image,ImageDraw
from concurrent.futures import ThreadPoolExecutor
import json,urllib.request,hashlib,shutil,sys
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');S=R/'_ART_SOURCES/cinematic_invasion_1020';W=S if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;D=R/'assets/game/shared/cinematics/cinematic_invasion_1020';O=R/'_shots/cinematic_invasion_1020'
for p in [S,D,O]:p.mkdir(parents=True,exist_ok=True)
if W!=S:shutil.copytree(W/'raw',S/'raw',dirs_exist_ok=True)
art={'images':{},'banks':{}};audit={'images':{},'banks':{}}
def save(name,im,pivot=None):
 assert im.width%2==im.height%2==0,(name,im.size)
 path=D/(name+'.png');im.save(path,optimize=True);a={'key':'inv20_'+name,'path':path.relative_to(R).as_posix(),'w':im.width,'h':im.height}
 if pivot:a['pivot']=pivot
 audit['images'][name]={'size':im.size,'bbox':im.getbbox(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()};return a
pilots=['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']
for name in ['panel',*pilots,*[p+'_horror' for p in pilots],'base_clean','coast_clean','earth_clean','solar_clean','remnant','clump']:
 p=W/'raw'/(name+'.png');im=Image.open(p).convert('RGBA');shutil.copy2(p,S/(name+'.png'));name=name.replace('_clean','')
 if name in pilots or name.endswith('_horror'):assert im.size==(256,384)
 art['images'][name]=save(name,im)
# PixelLab alphabet was laid out by visual glyph spacing rather than the requested
# cell coordinates. Recover its actual six independent glyphs in each row, once.
# Preserve native generated pixels; no smoothing, tracing or synthetic replacement.
raw=Image.open(W/'raw/font2.png').convert('L');shutil.copy2(W/'raw/font2.png',S/'font-master.png')
mask=raw.point(lambda n:255 if n>=128 else 0);runs=lambda vals:[(a,b) for a,b in []]
def spans(values):
 out=[];start=None
 for i,v in enumerate([*values,False]):
  if v and start is None:start=i
  if not v and start is not None:out.append((start,i));start=None
 return out
ys=spans([bool(mask.crop((0,y,384,y+1)).getbbox()) for y in range(384)]);assert len(ys)==6,ys
sheet=Image.new('RGBA',(512,512));glyphs={};sources={};chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';cell=64
for row,(y0,y1) in enumerate(ys):
 strip=mask.crop((0,y0,384,y1));xs=spans([bool(strip.crop((x,0,x+1,y1-y0)).getbbox()) for x in range(384)]);assert len(xs)==6,(row,xs)
 for col,(x0,x1) in enumerate(xs):
  ch=chars[row*6+col]
  if ch in '456789':continue # cropped bottom row is rejected; use the native numerals below
  i=chars.index(ch);x=(i%8)*64;y=(i//8)*64;g=Image.new('RGBA',(x1-x0,y1-y0),'white');g.putalpha(mask.crop((x0,y0,x1,y1)));sheet.alpha_composite(g,(x+4,y+4))
  glyphs[ch]={'sprite_rect':[x+4,y+4,g.width,g.height],'bounds_in_cell':[0,0,g.width,g.height],'x_advance':g.width+6};sources[ch]=[x0,y0,x1,y1]
# Existing exact punctuation/numerals supplement the accepted PixelLab letterforms.
native=R/'assets/game/shared/fonts/fonts/command_0914';nm=json.loads((native/'dialogue-map.json').read_text());ni=Image.open(native/'dialogue-alpha.png').convert('RGBA')
for ch in '456789.,!?:;\'"-+()/&%<>=[]#@_*':
 if ch in glyphs:continue
 g=nm['glyphs'].get(ch)
 if not g:continue
 x0,y0,w,h=g['sprite_rect'];src=ni.crop((x0,y0,x0+w,y0+h));src=src.resize((w*6,h*6),Image.Resampling.NEAREST);i=len(glyphs);x=(i%8)*64;y=(i//8)*64
 sheet.alpha_composite(src,(x+4,y+4));glyphs[ch]={'sprite_rect':[x+4,y+4,src.width,src.height],'bounds_in_cell':[0,max(0,48-src.height),src.width,48],'x_advance':src.width+6}
glyphs[' ']={'sprite_rect':[0,0,0,0],'bounds_in_cell':[0,0,0,0],'x_advance':24}
art['font']={'schema':'coleforge.bitmap-font.v2','family':'Fury Signal / PixelLab 1020','capsOnly':True,'line_height':54,'baseline':48,'glyphs':glyphs};art['images']['font']=save('font',sheet)
(S/'font-source-rects.json').write_text(json.dumps(sources,indent=2));(S/'font-map.json').write_text(json.dumps(art['font'],indent=2))
if '--stills' in sys.argv:
 (R/'assets/cinematic_invasion_art_1020.js').write_text('"use strict";\nconst INV20_ART='+json.dumps(art,separators=(',',':'))+';\n',newline='\n')
 print('Stills and font built for native preflight; animations not installed.');raise SystemExit(0)
# Raw animation banks use one fixed canvas/pivot, never per-frame alpha fitting.
jobs=json.loads((W/'animation-jobs.json').read_text())
def fetch(row):
 name,job,i=row;p=S/name/f'{i:02}.png';p.parent.mkdir(exist_ok=True)
 local=W/'animation'/name/f'{i:02}.png'
 if not p.exists() and local.exists():shutil.copy2(local,p)
 if not p.exists():p.write_bytes(urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{job}/download?index={i}',timeout=90).read())
 return p
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(fetch,[(name,a['id'],i) for name,a in jobs.items() for i in range(a['frames'])]))
for name,a in jobs.items():
 poses=[];rows=[]
 for i in a.get('acceptedFrames',range(a['frames'])):
  im=Image.open(S/name/f'{i:02}.png').convert('RGBA');assert im.size==(256,256),(name,i,im.size)
  # 16px common padding preserves every frame and the same cable-root position.
  out=Image.new('RGBA',(288,288));out.alpha_composite(im,(16,16));rows.append(save(name+f'_{i:02}',out,[144,186]));poses.append(out)
 art['banks'][name]=rows;audit['banks'][name]={'frames':len(rows),'canvas':[288,288],'pivot':[144,186],'sourceCanvas':[256,256],'sharedPadding':16,'fixedRoot':True}
 contact=Image.new('RGBA',(288*5,288*((len(poses)+4)//5)),(8,10,20,255))
 for i,im in enumerate(poses):contact.alpha_composite(im,((i%5)*288,(i//5)*288))
 contact.convert('RGB').save(O/(name+'-all-frames.jpg'),quality=93)
for name in ['jobs-final.json','animation-jobs.json']:
 if W!=S:shutil.copy2(W/name,S/name)
if W!=S:shutil.copytree(W/'references',S/'references',dirs_exist_ok=True)
(D/'manifest.json').write_text(json.dumps({'art':art,'audit':audit},indent=2)+'\n')
(R/'assets/cinematic_invasion_art_1020.js').write_text('"use strict";\n// Owned by build_cinematic_invasion_1020.py.\nconst INV20_ART='+json.dumps(art,separators=(',',':'))+';\n',newline='\n')
print(json.dumps({'images':len(art['images']),'banks':audit['banks'],'fontGlyphs':len(glyphs)}))
