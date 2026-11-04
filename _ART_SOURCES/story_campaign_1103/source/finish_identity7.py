from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw,ImageFont
W=Path(__file__).resolve().parent;D=W.parent if (W.parent/'overlay').is_dir() else W.parent/'outputs/BOF-Cutscenes-1103';O=D/'overlay';A=O/'assets/game/shared/cinematics/story_1103';S=D/'source-art/headset_motion_1103';V=D/'verification/revision7'
M=json.loads((A/'manifest.json').read_text());B=M['banks'];source_index=W/'generated.json'if (W/'generated.json').exists()else D/'source-art/generation_sources.json';sources=json.loads(source_index.read_text())
identities={'cole':{'outfit':'olive green','eyes':'blue, uncovered in headset portraits','reference':['coleyoung.png','boxcole.png']},'maverick':{'outfit':'neon electric lime green','eyewear':'green aviator sunglasses'}}
for p in identities:
 f=S/p/'08-right-quarter.png';shutil.copy2(f,D/'source-art'/('headset16-'+p+'.png'));shutil.copy2(f,D/'source-art/headsets-16bit'/(p+'.png'));sources['headset16-'+p]=str(f.resolve())
source_index.write_text(json.dumps(sources,indent=2));(D/'source-art/generation_sources.json').write_text(json.dumps({k:k+'.png'for k in sources},indent=2))
refs=S/'identity-references';refhash={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in refs.glob('*.png')}
M['headsetMotion']['identityOverrides']={'revision':7,'pilots':identities,'user_reference_sha256':refhash,'cole_palette':'30 shared body shades plus 2 reserved authored blue-iris shades'}
(S/'manifest.json').write_text(json.dumps(M['headsetMotion'],indent=2))
# Refresh the three stored comic fallback images affected by these identities.
def draw_bank(frame,name,f,x,y):
 a=B[name];im=Image.open(O/a['path']).convert('RGBA');im=im.crop((f%a['cols']*a['w'],f//a['cols']*a['h'],f%a['cols']*a['w']+a['w'],f//a['cols']*a['h']+a['h']));frame.alpha_composite(im,(x-a['pivot'][0],y-a['pivot'][1]))
for p in ['cole','maverick','decker']:
 frame=Image.new('RGBA',(912,512),'black');draw_bank(frame,'comic-scroll-'+p,0,456,196);contact='cole'if p=='decker'else'decker';draw_bank(frame,'headset-panel-'+contact,8,214,398);draw_bank(frame,'headset-panel-'+p,4,698,398);draw_bank(frame,'comic-border',0,456,256)
 frame.save(A/('comic-'+p+'.webp'),lossless=True,method=4)
for pp in [D/'source-art/provenance.json']:
 data=json.loads(pp.read_text())
 for r in data:
  for p in identities:
   if r['name']=='headset16-'+p:
    r['sha256']=hashlib.sha256((D/'source-art'/('headset16-'+p+'.png')).read_bytes()).hexdigest();r['derivation']='headset_motion_1103/'+p+'/08-right-quarter.png';r['identity_revision']=7
 pp.write_text(json.dumps(data,indent=2));M['source_art']=data
(A/'manifest.json').write_text(json.dumps(M,indent=2));(O/'assets/story_campaign_art_1103.js').write_text("'use strict';\nconst S113_ART="+json.dumps({'banks':B,'pilots':M['pilots'],'actorPoses':M['actorPoses'],'headsetMotion':M['headsetMotion'],'comicScroll':M['comicScroll']},separators=(',',':'))+';\n')
before=json.loads((V/'before-assets.json').read_text());changed=[p.stem for p in A.glob('*.webp')if p.name in before and hashlib.sha256(p.read_bytes()).hexdigest()!=before[p.name]]
expected={prefix+p for prefix in ['headset-','headset-panel-']for p in identities}|{'comic-cole','comic-maverick','comic-decker','comic-scroll-cole','comic-scroll-maverick','comic-scroll-decker'};assert set(changed)==expected,changed
facts=[]
for p in identities:
 greens=[];palette=[]
 for f in sorted((S/p).glob('[0-9][0-9]-*.png')):
  a=np.array(Image.open(f).convert('RGBA'));c=a[85:125,:,:3].astype(int);greens.append(int(np.count_nonzero((c[:,:,1]>170)&(c[:,:,1]>c[:,:,0]+25)&(c[:,:,1]>c[:,:,2]+40))));palette.append(len(np.unique(a[a[:,:,3]>0,:3],axis=0)))
 a=np.array(Image.open(S/p/'00-front-neutral.png').convert('RGBA'));c=a[32:84,:,:3].astype(int);blue=int(np.count_nonzero((c[:,:,2]>c[:,:,0]+18)&(c[:,:,2]>c[:,:,1]+5)&(c[:,:,2]>95)))
 if p=='cole':assert max(greens)==0 and blue>=8,(greens,blue)
 else:assert min(greens)>150,greens
 assert max(palette)<=32
 facts.append({'pilot':p,'frames':24,'front_blue_eye_pixels':blue,'jacket_neon_pixels_per_frame':greens,'maximum_opaque_palette':max(palette),'identity':identities[p]})
report={'pilots':facts,'changed_banks':changed,'unchanged_banks':len(before)-len(changed),'user_reference_sha256':refhash};(V/'identity-report.json').write_text(json.dumps(report,indent=2))
font=ImageFont.truetype(r'C:\Windows\Fonts\consolab.ttf',22)
def pair(f):
 board=Image.new('RGB',(832,448),'#15151c');dr=ImageDraw.Draw(board)
 for i,p in enumerate(identities):
  path=sorted((S/p).glob(str(f).zfill(2)+'-*.png'))[0];im=Image.open(path).convert('RGBA').resize((384,384),Image.Resampling.NEAREST);x=i*416+16;board.paste(im,(x,8),im);dr.text((x,403),'COLE · OLIVE'if p=='cole'else'MAVERICK · NEON GREEN',font=font,fill='white')
 return board
pair(0).save(D/'Cole-Maverick-corrected.png')
order=[0,1,2,1,3,0,4,6,4,0,8,10,8,0,12,13,14,15,16,17,18,19,20,21,22,23];gif=[pair(i)for i in order];gif[0].save(D/'Cole-Maverick-corrected.gif',save_all=True,append_images=gif[1:],duration=160,loop=0,optimize=False,disposal=2)
board=Image.new('RGB',(864,960),'#15151c');dr=ImageDraw.Draw(board)
for i,p in enumerate(M['pilots']):
 im=Image.open(S/p/'08-right-quarter.png').convert('RGBA').resize((256,256),Image.Resampling.NEAREST);x=i%3*288+16;y=i//3*320+8;board.paste(im,(x,y),im);dr.text((x,y+274),p.upper(),font=font,fill='white')
board.save(D/'Headsets-16bit.png')
lock='''# Current pilot identity correction — authoritative revision 7

Cole is the man in Mike's boxcole.png and coleyoung.png references. The headset version follows coleyoung: visible blue eyes, short spiky brown quiff with close-cut sides, strong brown beard/jaw, olive military flight jacket and raised green collar/scarf, black harness, silver buckles. The older boxcole image supports identity/outfit; its UI frame and sunglasses are omitted in this uncovered-eye headset variant.

Maverick is the neon-green pilot. Keep his brown hair/beard, green aviator sunglasses and neon lime jacket. Earlier records calling the neon-green headset pilot Cole are superseded and must not be used as identity guidance.

The 24 talking, directional and emotional frames for both identities are corrected. Other seven pilots are unchanged. Cole uses the brown/olive color-panel theme; Maverick uses the black/green theme. Both supplied Cole references are preserved under headset_motion_1103/identity-references.
'''
(D/'source-art/CURRENT_IDENTITIES.md').write_text(lock,encoding='utf-8');(S/'IDENTITY_LOCKS.md').write_text(lock,encoding='utf-8')
guide=S/'FRAME_GUIDE.txt';text=guide.read_text(encoding='utf-8').replace('Cole wears neon green.','Cole wears olive green and has blue eyes. Maverick wears neon green and aviators.');guide.write_text(text,encoding='utf-8')
print(json.dumps({'changed_banks':len(changed),'unchanged_banks':report['unchanged_banks'],'identity_frames':48,'cole_blue_iris_pixels':facts[0]['front_blue_eye_pixels'],'maverick_min_neon_pixels':min(facts[1]['jacket_neon_pixels_per_frame'])}))
