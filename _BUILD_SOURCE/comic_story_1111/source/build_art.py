"""Register fixed native-pixel banks. Every runtime draw is a 1:1 raster blit."""
from pathlib import Path
from PIL import Image,ImageSequence,ImageDraw
import json,hashlib,shutil,re
P=Path(__file__).resolve().parents[1]
G=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
OLD=P.parent/'BOF-Cinema-1110/overlay/assets'
DEST=P/'overlay/assets/game/shared/cinematics/comic_story_1111';DEST.mkdir(parents=True,exist_ok=True)
banks={};registry={}
for f in OLD.glob('*_art_1110.js'):
 data=json.JSONDecoder().raw_decode(f.read_text(encoding='utf8').split('=',1)[1])[0]
 registry.update(data.get('banks',{}))
def save(name,frames,source,**extra):
 w,h=frames[0].size;assert w%2==h%2==0
 assert all(f.size==(w,h)for f in frames)
 cols=min(4,len(frames));rows=(len(frames)+cols-1)//cols
 sheet=Image.new('RGBA',(w*cols,h*rows))
 for i,im in enumerate(frames):sheet.paste(im,(i%cols*w,i//cols*h))
 path=DEST/(name+'.webp');sheet.save(path,lossless=True,method=0)
 banks[name]=dict(key='c16_'+name,path='assets/game/shared/cinematics/comic_story_1111/'+path.name,w=w,h=h,cols=cols,frames=len(frames),pivot=[w//2,h//2],source=source,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**extra)
def bankFrames(name):
 a=registry[name];im=Image.open(G/a['path'].split('?')[0]).convert('RGBA')
 return [im.crop((i%a['cols']*a['w'],i//a['cols']*a['h'],i%a['cols']*a['w']+a['w'],i//a['cols']*a['h']+a['h']))for i in range(a['frames'])]
pilots=['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']
checks=[]
for pk in pilots:
 frames=[Image.open(P/f'portraits/{pk}/{i}.png').convert('RGBA')for i in range(7)]
 bounds=[im.getbbox()for im in frames];visible=[min(b[0]for b in bounds)*2,min(b[1]for b in bounds)*2,max(b[2]for b in bounds)*2,max(b[3]for b in bounds)*2]
 save('talk-'+pk,[im.resize((256,256),Image.Resampling.NEAREST)for im in frames],f'portraits/{pk}.aseprite',native=[128,128],offlineScale=2,visibleBounds=visible,baselineY=visible[3],panelBleed=2)
 save('backdrop-'+pk,[Image.open(P/f'masters/pilot-backgrounds/{pk}.png').convert('RGBA')],f'masters/pilot-backgrounds/{pk}.aseprite')
 small=[im.resize((180,180),Image.Resampling.NEAREST)for im in frames];bottom=max(im.getbbox()[3]for im in small)
 save('talk-small-'+pk,small,f'portraits/{pk}.aseprite',native=[128,128],offlineScale=1.40625,baselineY=bottom,panelBleed=2)
 mini=[im.resize((96,96),Image.Resampling.NEAREST)for im in frames]
 save('talk-mini-'+pk,mini,f'portraits/{pk}.aseprite',native=[128,128],offlineScale=.75,baselineY=max(im.getbbox()[3]for im in mini),panelBleed=2)
 save('icon-'+pk,[frames[0].resize((96,96),Image.Resampling.NEAREST)],f'portraits/{pk}.aseprite',native=[128,128],offlineScale=.75)
 # Legacy victory portraits use these explicit 180/90 display banks, without runtime fitting.
 save('card-'+pk,[frames[0].resize((180,180),Image.Resampling.NEAREST)],f'portraits/{pk}.aseprite',native=[128,128],offlineScale=1.40625)
 save('credit-'+pk,[frames[0].resize((90,90),Image.Resampling.NEAREST)],f'portraits/{pk}.aseprite',native=[128,128],offlineScale=.703125)
 for i,frame in enumerate(frames):
  job=next(j for j in json.loads((P/'source/portrait-editor-jobs.json').read_text())if j['pilot']==pk)
  base=Image.open(job['native']).convert('RGBA');m=job['mouth'];a=frame.load();b=base.load();bad=0;alpha=0
  for y in range(128):
   for x in range(128):
    if ((x-m[0])/m[2])**2+((y-m[1])/m[3])**2>1 and a[x,y]!=b[x,y]:bad+=1
    if a[x,y][3]!=b[x,y][3]:alpha+=1
  checks.append(dict(pilot=pk,frame=i,outsideMouthDifferent=bad,alphaDifferent=alpha));assert bad==alpha==0
 # The real in-game top views keep each pilot's actual hull and palette.
 for view,name in [('earth','native-'+pk+'-top'),('space','actual-space-'+pk+'-base')]:
  save('ship-'+view+'-'+pk,bankFrames(name),registry[name]['path'])
 native=bankFrames('native-'+pk+'-top')[0];k=min(128/native.width,128/native.height);small=native.resize((round(native.width*k),round(native.height*k)),Image.Resampling.NEAREST);marker=Image.new('RGBA',(128,128));marker.paste(small,((128-small.width)//2,(128-small.height)//2));save('marker-'+pk,[marker],registry['native-'+pk+'-top']['path'])
pages=json.loads((P/'source/page-editor-jobs.json').read_text())
for page in pages:
 for layer in ['bg','fg']:
  name='page-'+str(page['id'])+'-'+layer
  save(name,[Image.open(P/f'masters/pages/page-{page["id"]}.0-{layer}.png').convert('RGBA')],f'masters/pages/page-{page["id"]}.0-{layer}.aseprite')
 # Native-size nameplate palette replacements: speaker box matches pilot's aircraft tint.
 for pk in pilots:
  f=P/f'masters/pages/name-{page["id"]}-{pk}.png'
  if f.exists():save('name-'+str(page['id'])+'-'+pk,[Image.open(f).convert('RGBA')],'source/author_nameplates.lua')
aliases={'launch-correlation':'bridge-launch-correlation','airbase-arrival':'bridge-airbase-recon','subsurface-search':'bridge-subsurface-scan','river-arrival':'bridge-river-recon','warp-drive-lock':'warp-drive'}
story=json.loads((P/'source/human-story.json').read_text(encoding='utf8'))
used=sorted({aliases.get(b['bank'],b['bank'])for rows in story['scenes'].values()for b in rows if b.get('bank')}|{'warp-arrival'})
for name in used:
 frames=bankFrames(name);wide=name=='hq-conference';out=[]
 for im in frames:
  if wide:
   # One crop shared by every frame; the complete nine-person row remains in the opening shot.
   w,h=im.size;cropH=round(w*270/754);top=max(0,min(h-cropH,round(h*.20)));im=im.crop((0,top,w,top+cropH)).resize((754,270),Image.Resampling.NEAREST)
  else:
   k=min(270/im.width,270/im.height);size=(round(im.width*k),round(im.height*k));r=im.resize(size,Image.Resampling.NEAREST);im=Image.new('RGBA',(270,270));im.paste(r,((270-r.width)//2,(270-r.height)//2))
  out.append(im)
 save('art-'+name,out,registry[name]['path'],sharedCrop=wide,offlineCanvas=[754,270]if wide else[270,270])
# Existing authored backgrounds supply the brief location images. Crop/export offline, never stretch at runtime.
for file,var in [('story_campaign_art_1103.js','S113_ART'),('cinema_story_art_1021.js','C22_ART')]:
 text=(G/'assets'/file).read_text(encoding='utf8');data=json.JSONDecoder().raw_decode(text.split('=',1)[1])[0]
 if var=='S113_ART':storyArt=data['banks']
 else:legacy=data
portal=legacy['banks']['blue_portal'];im=Image.open(G/portal['path']).convert('RGBA')
save('portal',[im.crop((i%portal['columns']*256,i//portal['columns']*256,i%portal['columns']*256+256,i//portal['columns']*256+256))for i in range(portal['frames'])],portal['path'])
maps={'city':('legacy','peace_city'),'sky':('s113','sky'),'space':('legacy','space'),'earth':('s113','earth-approach'),'sewer':('s113','sewer')}
for label,(owner,name)in maps.items():
 a=storyArt.get(name)if owner=='s113'else legacy['images'].get(name)
 if label=='earth':a=registry['earth-approach']
 if label=='space':a={'path':'assets/game/levels/stage_09/stage/expansion_v1/space/nst9_starfield.png','w':1024,'h':1024}
 if not a:
  # Specific authored location bank names are recorded in the manifest, never guessed in the renderer.
  if label=='city':a=storyArt.get('peace-city')or storyArt.get('city')
  if label=='space':a=legacy['images'].get('space_invasion')or legacy['images'].get('space')
 if not a:raise ValueError((label,list(storyArt)))
 im=Image.open(G/a['path']).convert('RGBA').crop((0,0,a['w'],a['h']));w,h=im.size;cropH=min(h,round(w*270/754));top=0 if label=='space'else(h-cropH)//2
 im=im.crop((0,top,w,top+cropH));k=min(754/im.width,270/im.height);im=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST)
 canvas=Image.new('RGBA',(754,270));canvas.paste(im,((754-im.width)//2,(270-im.height)//2));save('location-'+label,[canvas],a['path'])
art=dict(version=1,revision=2,portraitMount='visible-body-bottom-with-two-pixel-border-overlap',canvas=[912,512],pages=pages,pilots=pilots,banks=banks,aliases=aliases)
(P/'overlay/assets/comic_story_art_1111.js').write_text("'use strict';\nconst C16_ART="+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8')
(P/'verification/portrait-pixel-checks.json').write_text(json.dumps(checks,indent=2),encoding='utf8')
(P/'source/art-manifest.json').write_text(json.dumps(art,indent=2),encoding='utf8')
print(json.dumps(dict(banks=len(banks),portraitChecks=len(checks),frames=sum(a['frames']for a in banks.values()))))
